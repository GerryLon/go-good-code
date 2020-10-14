#!/usr/bin/python3

import argparse
import asyncio
import time
from inspect import getframeinfo, stack
import logging
from threading import Timer
from typing import List
from concurrent.futures import ThreadPoolExecutor
import re
import copy


import netmiko
# import telnetlib3

import consts.consts as consts
import utils.utils as utils
import telnetlib as mtl  # my telnet lib => mtl
import timeout.timeout as timeout
from model.model import Account, Host, ConnectDetail, ExecuteResult, CliOptions, Closer

# 全局变量
DEBUG_MODE = False


def debug_print(msg, flush=True):
	if DEBUG_MODE:
		caller = getframeinfo(stack()[1][0])
		print("[{2}][{0}-DEBUG]: {1}".format(caller.lineno, msg, utils.get_current_time()), flush=flush)


def raise_exception(msg):
	debug_print("[Exception]:" + msg)
	raise Exception(str(msg) + consts.EOL)


def get_device_type(login_type: str, arg_device_type: str) -> []:
	m = consts.DEVICE_TYPE_MAPPING.get(login_type)
	if not m:
		raise_exception("unsupported login_type: {0}".format(login_type))

	return m.get(arg_device_type)


class SwitchRouterCommandExecutor:
	"""
	解析命令行参数
	"""
	def __init__(self):
		self.cos = SwitchRouterCommandExecutor.__parse_options()
		# 如果使用logging.DEBUG, 日志太多了， 没法看
		logging.basicConfig(
			format='%(name)s %(filename)s %(lineno)s %(levelname)s %(message)s',
			level=(logging.INFO if self.cos.debug else logging.ERROR)
		)
		# 初始化定时器
		self.__ttlTimer = Timer(self.cos.ttl, self.ttl_exit, args=[])
		#  需要关闭的资源的队列
		self.__closerList: List[Closer] = []

	def cancel_timer(self):
		self.__ttlTimer.cancel()

	def add_closer(self, closer: Closer):
		# debug_print("add closer: {}".format(closer))
		self.__closerList.append(closer)

	def pop_closer(self) -> Closer or None:
		if len(self.__closerList) > 0:
			return self.__closerList.pop()
		return None

	def ttl_exit(self):
		while True:
			closer = self.pop_closer()
			if not closer:
				break
			closer.close()
			debug_print(closer.name + " closed")

		utils.exit_err("process timeout at: " + utils.get_current_time(), exit_immediately=True)

	@staticmethod
	# def parse_options() -> CliOptions:
	def __parse_options():
		parser = argparse.ArgumentParser(description="配置下发/获取工具")

		parser.add_argument(
			"-a", "--account",
			type=str,
			help="""
				登录时的用户名密码，可指定多对。用户名和密码之间用空格分隔；每对之间用空格分隔。
				如：
				user1 pass1 user2 pass2 user3 pass3

				如果同时指定了--account-from-file, 则以--account-from-file为准
				"""
		)
		parser.add_argument(
			"--account-from-file",
			help="以文件的形式指定用户名密码。格式为: user1 pass1<换行>user2 pass2<换行>user3 pass3"
		)
		# get or set
		parser.add_argument(
			"--opmode",
			choices=[consts.OP_MODE_GET, consts.OP_MODE_SET],
			required=True,
			help="操作模式（设置:get, 还是读取: set)"
		)
		parser.add_argument(
			"--one-command-timeout",
			type=int,
			default=600,
			help="get模式下每条命令超时时间(一条命令最长执行多久). 单位为秒. 默认为600"
		)
		# 采用手动登录的形式， 不借助库来登录； 只依赖于prompt
		# # 这个device-type选项只在ssh中有用， 如果写了auto, 会自动探测
		# parser.add_argument(
		# 	"-t", "--device-type",
		# 	choices=[
		# 		consts.MF_CISCO, consts.MF_HUAWEI, consts.MF_H3C,
		# 		consts.MF_JUNIPER, consts.MF_LINUX, consts.MF_AUTODETECT
		# 	],
		# 	default=consts.MF_AUTODETECT,
		# 	help="设备类型, 只针对ssh登录(opmode=set). h3c的自动检测不出来, 可以指定一下. 默认自动检测, 支持: cisco|h3c|juniper|huawei|linux|autodetect")
		parser.add_argument(
			"--host",
			default='',
			required=False,
			help="""
				对哪个host的设备操作，多个用英文逗号分隔, 每一个的格式为 ip[ device_type],
					如 "192.168.3.3 cisco" 或者"192.168.3.3", 其中device_type可选, 无默认值, 不指定的话将会自动探测.
				如果同时指定了--host-from-file, 以--host-from-file为准
				"""
		)
		parser.add_argument(
			"--host-from-file",
			required=False,
			help="""
				如果host太多，可用文件指定， 一行一个, 每行的格式为: ip[ device_type].
				如 "192.168.3.3 cisco" 或者"192.168.3.3", 其中device_type可选, 无默认值, 不指定的话将会自动探测.
				"""
		)
		parser.add_argument(
			"--conn-timeout",
			required=False,
			default=5,
			type=int,
			help="""
						每个设备通过ssh/telnet建立TCP连接的超时时间(秒). 如果指定时间内未连接成功, 认为连接失败.
						"""
		)
		parser.add_argument(
			"--empty-command-interval",
			required=False,
			default=30,
			type=int,
			help="""
			一个命令执行时间过长时, 可能会导致连接会话断开, 需要下发空命令(如空格)来实现"保活"
			此选项即为 下发空命令的时间间隔, 单位为秒
			"""
		)
		parser.add_argument(
			"--command",
			default='',
			required=False,
			help="要执行的命令，多个用英文分号分隔. 如果同时指定了command-from-file, 以--command-from-file为准"
		)
		parser.add_argument(
			"--command-from-file",
			required=False,
			help="如果命令太多，可用文件指定，一行一条命令. 会忽略空白行"
		)
		parser.add_argument(
			"--protocol",
			default='',
			choices=["ssh", "telnet"],
			help="登录时使用的协议，目前支持ssh, telnet. 不指定的话取所有支持的挨个试。"
		)
		parser.add_argument("--ssh-port", default=22, type=int, help="ssh协议端口，默认22")
		parser.add_argument("--telnet-port", default=23, type=int, help="telnet协议端口，默认23")
		parser.add_argument("--command-interval", default=0.5, type=float, help="两条命令之间执行的间隔，单位为秒。默认0.5")
		# parser.add_argument(
		# 	"--cmd-exec-until-prompt",
		# 	default=False,
		# 	action="store_true",
		# 	help="""
		# 		get模式时, 每条命令执行直到出现提示符(一般为主机名), 默认为true
		# 		如果这个选项为true, 则会忽略--cmd-interval
		# 		"""
		# )
		parser.add_argument("--debug", default=False, help="开启debug模式,默认为false", action="store_true")
		# parser.add_argument("--parallel", default=False, help="多个host并发执行,默认为false", action="store_true")
		parser.add_argument(
			"--concurrency",
			default=1,
			type=int,
			help="并发执行时, 同时最多的协程数(默认为1). 为1时表示表示串行, 大于1表示并发"
		)
		# 对某设备在执行命令时， 发现有报错的（如： Error: Unrecognized command）， 跳过此设备
		# 如在ssh中执行发现有命令报错的， telnet的也不要再执行了
		parser.add_argument(
			"--ignore-on-command-error",
			default=False,
			help="如果命令执行过程出错，是否直接跳过当前设备？ 默认为false， 即：命令执行出错就跳过当前设备",
			action="store_true"
		)
		parser.add_argument(
			"--output",
			default='stdout',
			choices=["stdout", "file"],
			help="结果输出位置， 默认为标准输出。 如果要输出到文件， 传file"
		)
		parser.add_argument("--output-dir", default=".", help="如果是输出到文件， 文件放到哪个目录？ 默认为当前目录")
		parser.add_argument(
			"--output-filename-format",
			default="{protocol}-{host}-{username}-{connect_ok}-{login_ok}-{time}",
			help="""
				如果选择输出到文件， 文件名的格式。time为生成结果时的时间，格式(年月日时分秒)如：20200723_153029.
				默认为: {protocol}-{host}-{username}-{connect_ok}-{login_ok}-{time}
				其中的{host}, {protocol}等为占位符， 中间的连字符可换成其他的字符。
				{login_ok}表示是否登录成功， 具体的会以login_ok, login_err来作为实际的值
				如： {host}@{protocol}-{time}
				"""
		)
		parser.add_argument(
			"--ttl",
			type=int,
			default=1800,
			help="""
				脚本执行总时长(秒), 不管多少个主机, 默认1800秒(30分钟).
				如果过了这个时间, 脚本会立刻退出
			""",
		)
		parser.add_argument(
			"--output-password",
			default=False,
			help="""
				输出结果时要不要打印密码, 默认为false
			""",
			action="store_true",
		)
		args = parser.parse_args()
		args_map = vars(args)

		# debug模式
		global DEBUG_MODE
		DEBUG_MODE = args_map.get("debug")
		args_map2 = copy.deepcopy(args_map)
		if not args_map.get("output_password"):
			args_map2.pop("account")
		debug_print("options passed from cli: {}".format(args_map2))

		# 命令行参数校验
		host = args_map.get("host")
		host_from_file = args_map.get("host_from_file")

		host_list = None  # split host to list
		if host:
			host_list = host.split(",")
		if host_from_file:  # 未指定host,则从文件读取
			host_list = utils.get_file_as_lines(host_from_file, ignore_empty_line=True)

		if not host_list:
			utils.exit_err(msg="host is empty")

		# host去重复, 如果重复给出提示
		tmp_host_list = []
		host_obj_list = []  # Host object slice
		for host in host_list:
			if not host:
				continue

			host = host.strip()
			host_pair = host.split(" ")  # format: ip[ device_type]
			host_addr = host_pair[0]
			host_device_type = consts.MF_AUTODETECT
			if len(host_pair) > 2:
				utils.exit_err("host format error: " + host)
			if len(host_pair) == 2:
				host_device_type = host_pair[1]
			host_obj_list.append(Host(addr=host_addr, device_type=host_device_type))

			# 重复判断
			if host not in tmp_host_list:
				tmp_host_list.append(host)
			else:
				utils.exit_err(msg="duplicated host: " + host)

		# 每个host都要合法(暂时按ipv4来判断）
		for host_obj in host_obj_list:
			host_obj.addr = host_obj.addr.strip()
			if not utils.valid_ipv4(host_obj.addr):
				utils.exit_err(msg="invalid ipv4 " + host_obj.addr)

		args_map["host_list"] = host_obj_list

		# 处理command
		command = args_map.get("command")
		command_from_file = args_map.get("command_from_file")
		command_list = None
		if command:
			command_list = command.split(";")
		if command_from_file:
			command_list = utils.get_file_as_lines(command_from_file, ignore_empty_line=True)

		if not command_list:
			utils.exit_err(msg="command is empty")

		# 针对特殊前缀的命令做处理(转ascii码)
		# 如C^-32 => ' '
		for i, _ in enumerate(command_list):
			if command_list[i].startswith(consts.EMPTY_CMD_PREFIX):
				command_list[i] = chr(int(command_list[i][len(consts.EMPTY_CMD_PREFIX):]))

		args_map["command_list"] = command_list

		# 处理用户名密码
		account = args_map.get("account")
		account_from_file = args_map.get("account_from_file")
		account_list = []
		accounts = []  # [u1, p1, u2, p2, ..., un, pn]
		if account:
			accounts = account.split(" ")
		if account_from_file:
			tmp_accounts = utils.get_file_as_lines(account_from_file)
			for a in tmp_accounts:
				pair = a.split(" ")
				if len(pair) != 2:
					utils.exit_err("username password: {} format error".format(pair))
				u = pair[0].strip()
				p = pair[1].strip()
				accounts.append(u)
				accounts.append(p)

		if len(accounts) % 2 != 0:
			utils.exit_err("username and password count not match")

		i = 0
		while i < len(accounts):
			account_list.append(Account(
				username=accounts[i+0],
				password=accounts[i+1],
				string_show_password=args_map.get("output_password"),
			))
			i += 2

		if not account_list:
			utils.exit_err(msg="account is empty")

		cos = CliOptions()
		cos.account_list = account_list
		cos.host_list = host_list
		cos.command_list = command_list
		fields = vars(cos)

		for k in args_map:
			if k in fields:
				cos.__setattr__(k, args_map[k])

		# print(vars(cos))
		return cos

	# 标记登录成功使用的登录方式
	@staticmethod
	def __login_success_mark(login_type=consts.LOGIN_TYPE_TELNET, login_username=''):
		return "[%d]: login by %s success(username:%s).\n" % (int(time.time()), login_type, login_username)

	@staticmethod
	def __close_netmiko_connect(net_connect: netmiko.ConnectHandler):
		if net_connect:
			net_connect.disconnect()

	# 建立 netmiko 连接
	def __netmiko_connect(self, host: Host = None, username='', password='') -> (object, str):
		net_connect = None
		real_dt = ''  # 实际的device_type, 探测到的 或者 手动指定的
		try:
			debug_print("starting {} login into {} by user: {}".format(host.protocol, host.addr, username))
			dt = host.device_type
			# if dt == consts.MF_AUTODETECT:
			# 	# # code from https://ktbyers.github.io/netmiko/COMMON_ISSUES.html
			# 	dt = self.__auto_detect(host, username=username, password=password)
			# 	if not dt:
			# 		debug_print("when login: auto detect failed: {}", host.addr)
			# 		dt = "terminal_server"
			# 		real_dt = consts.MF_AUTODETECT
			# 	else:
			# 		real_dt = dt
			# else:
			# 	debug_print("manual device_type: " + dt)
			# 	dts = get_device_type(host.protocol, dt)
			# 	if not dts:
			# 		debug_print("no such device type mapping: protocol: {}, type: {}".format(host.protocol, dt))
			# 		dt = "terminal_server"
			# 		real_dt = consts.MF_AUTODETECT
			# 	else:
			# 		real_dt = dt = dts[0]
			# 	debug_print("netmiko real device_type: " + dt)

			if dt == consts.MF_AUTODETECT:
				dt = "terminal_server"
				real_dt = consts.MF_AUTODETECT
			else:
				debug_print("manual device_type: " + dt)
				dts = get_device_type(host.protocol, dt)
				if not dts:
					debug_print("no such device type mapping: protocol: {}, type: {}".format(host.protocol, dt))
					dt = "terminal_server"
					real_dt = consts.MF_AUTODETECT
				else:
					real_dt = dt = dts[0]
				debug_print("netmiko real device_type: " + dt)

			device = {
				"device_type": dt,
				"host": host.addr,
				"username": username,
				"password": password,
				"conn_timeout": self.cos.conn_timeout,
				# 目前只有telnet和ssh两种协议
				"port": self.cos.ssh_port if host.protocol == consts.LOGIN_TYPE_SSH else self.cos.telnet_port,
			}
			net_connect = netmiko.ConnectHandler(**device)
		except Exception as e:
			net_connect = None
			utils.stderr_write("ssh connect err: {0}, username: {1}\n".format(e, username))
		finally:
			if net_connect:
				# 添加到closer队列, 脚本超时退出时会调用close关闭
				self.add_closer(self.__wrap_net_connect(net_connect=net_connect, host=host))
			return net_connect, real_dt

	def __set_config(self, net_connect=None, device_type='cisco') -> str:
		if device_type != consts.MF_AUTODETECT:
			netmiko.redispatch(net_connect, device_type=device_type)

		# Now just do your normal Netmiko operations
		output = net_connect.send_config_set(
			enter_config_mode=True,
			exit_config_mode=True,
			config_commands=self.cos.command_list,
		)
		return output

	# redispatch参数必须要device_type
	# 运维的同事说又不想指定设备类型，只好自动检测了
	def __auto_detect(self, host: Host, username='', password=''):
		debug_print("auto detect: " + host.addr)
		best_match = ''
		# telnet目前不支持 auto detect
		if host.protocol == consts.LOGIN_TYPE_TELNET:
			debug_print("TELNET NOT SUPPORT autodetect")

		try:
			remote_device = {
				'device_type': 'autodetect',
				'host': host.addr,
				'username': username,
				'password': password,
				'port': self.cos.ssh_port,  # 目前不支持telnet auto detect
			}

			guesser = netmiko.SSHDetect(**remote_device)
			best_match = guesser.autodetect()
			if best_match:
				debug_print("autodetect success: host: {}, best_match: {}".format(host.addr, best_match))
			else:
				debug_print("autodetect failed: host: {}".format(host.addr))
		# print(best_match)  # Name of the best device_type to use further
		# print(guesser.potential_matches)  # Dictionary of the whol
		except Exception as e:
			utils.stderr_write("ssh err occurred when auto detect host: {0}, username: {1}, err: {2}".format(
				host.addr, username, e))

		return best_match

	@classmethod
	def __wrap_net_connect(cls, net_connect: netmiko.ConnectHandler, host: Host) -> Closer:
		name = "{}-{}-{}".format(host.addr, host.device_type, host.protocol)

		def close_net_connect():
			debug_print("will close net_connect: " + name)
			if net_connect:
				net_connect.disconnect()
			debug_print("closed net_connect: " + name, flush=True)
		net_connect.close = close_net_connect
		return Closer(net_connect, name=name)

	# 通过ssh抓取配置
	def pull_config_by_ssh(self, host: Host = None, username='', password='') -> ExecuteResult:
		result = ExecuteResult(
			host=host.addr,
			username=username,
			password=password,
			protocol=consts.LOGIN_TYPE_SSH,
			connect_detail=ConnectDetail())
		net_connect, real_dt = self.__netmiko_connect(host=host, username=username, password=password)
		if not net_connect:
			result.err += 'connect to {} timeout in {} seconds'.format(host.addr, self.cos.conn_timeout)
			return result
		# result.connect_success = True
		result.detail.ssh_connect_success = True
		# net_connect创建成功就表示登录成功
		debug_print("login success into host: {} by protocol: {}. real device type: {} ".format(
			host.addr, host.protocol, real_dt))
		result.login_success = True
		net_connect.write_channel("\r\n")
		time.sleep(1)
		net_connect.read_channel()
		net_connect.a = ""
		try:
			# TODO: 这个循环进不进都行， 连接成功以net_connect创建成功为准
			# Manually handle the Username and Password, 重试3次
			for i in range(0):
				output = net_connect.read_channel()
				# if 'Username' in output:
				if utils.match_list(output, consts.CLI_PROMPT_USERNAME):
					net_connect.write_channel(username + '\r\n')
					time.sleep(1)
					output = net_connect.read_channel()
				# Search for password pattern / send password
				elif utils.match_list(output, consts.CLI_PROMPT_PASSWORD):
					net_connect.write_channel(password + '\r\n')
					time.sleep(.5)
					output = net_connect.read_channel()
					# Did we successfully login
					if utils.match_list(output, consts.CLI_PROMPT_LOGIN_SUCCESS):
						debug_print("login success into host: " + host.addr)
						result.login_success = True
						break
				debug_print("total:", output)
				net_connect.write_channel('\r\n')
				time.sleep(.5)

			if not result.login_success:
				msg = "login by " + consts.LOGIN_TYPE_SSH + " failed"
				debug_print(msg)
				result.err += msg
				return result

			prompt_str = net_connect.find_prompt(delay_factor=5)
			debug_print("prompt: " + prompt_str + ", len: " + str(len(prompt_str)))

			# 发空命令
			def send_empty_cmd(cmd_index: int) -> Timer:
				try:
					# if cmd_index > 0:
					debug_print("write empty command")
					if net_connect:
						net_connect.write_channel(utils.encode_str("\r\n"))
						t = Timer(self.cos.empty_command_interval, send_empty_cmd, [cmd_index])
						t.start()
						return t
				except:
					return None

			if self.cos.opmode == consts.OP_MODE_GET:
				empty_cmd_timer = None
				for index, cmd in enumerate(self.cos.command_list):  # 只获取最后一个命令的输出
					if empty_cmd_timer:
						empty_cmd_timer.cancel()
					elif net_connect:
						empty_cmd_timer = send_empty_cmd(index)

					debug_print("execute command: " + cmd)
					net_connect.write_channel(cmd + "\n")
					# tmp_result = net_connect.read_until_pattern(
					# 	pattern=r"(\r|\n|\r\n)"+prompt_str+r"$"
					# 	# 和telnet的保持一致
					# 	# pattern=prompt_str + r"[\d\D]+(\r\n|\r|\n)" + prompt_str + "$"
					# )

					@timeout.timeout(self.cos.one_command_timeout)
					def read_until(prefix: str):
						ret = net_connect.read_until_pattern(
							pattern=re.escape(prefix) + r"[\d\D]*(\r|\n|\r\n)" + re.escape(prompt_str) + "$",
							max_loops=99999,
						)
						# print("output:", ret)
						return ret
					try:
						tmp_result = read_until(cmd)
					except timeout.TimeoutException:
						print("hello")
						msg = "! exec cmd: {} timeout in {} seconds".format(cmd, self.cos.one_command_timeout)
						debug_print(msg)
						result.err += msg
						continue
					time.sleep(self.cos.command_interval)

					# # 0.2是这个delay_factor会乘的数（看send_command的源代码知道的）
					# tmp_result = net_connect.send_command(
					# 	cmd,
					# 	delay_factor=self.cos.command_interval / 0.2,
					# 	strip_command=False,
					# 	strip_prompt=False,
					# 	max_loops=1000,
					# 	expect_string=prompt_str if prompt_str else None,
					# )

					result.output += tmp_result  # 命令错误的也记录下来
					if utils.match_list(tmp_result, consts.UNKNOWN_COMMANDS):
						debug_print("unknown command: " + cmd)
						result.command_ok = False  # 有命令错误直接退出
						result.err += "command error: " + tmp_result
						if not self.cos.ignore_on_command_error:
							return result
			# set模式单独处理
			elif self.cos.opmode == consts.OP_MODE_SET:
				if real_dt == consts.MF_AUTODETECT:
					debug_print("in set mode, device type is: " + consts.MF_AUTODETECT + " .")
				# set模式自己手动处理
				# result.output = self.__set_config(net_connect, device_type=real_dt)
				for cmd in self.cos.command_list:
					net_connect.write_channel(cmd + "\n")
					time.sleep(self.cos.command_interval)
					tmp_result = net_connect.read_channel()
					result.output += tmp_result  # 命令错误的也记录下来
					if utils.match_list(tmp_result, consts.UNKNOWN_COMMANDS):
						debug_print("unknown command: " + cmd)
						result.command_ok = False  # 有命令错误直接退出
						result.err += "command error: " + tmp_result
						if not self.cos.ignore_on_command_error:
							return result
			else:
				utils.stderr_write("unsupported opmode: " + self.cos.opmode)
				return result
		except Exception as e:
			utils.stderr_write("ssh err occurred when pull_config_by_ssh: {0}, username: {1}".format(e, username))
			result.err += "exception: {}".format(e)
		finally:
			if net_connect:
				net_connect.disconnect()
			return result

	def __gen_telnet_shell(self, username='', password='', result=None):
		async def telnet_shell(reader, writer):
			login_success = False
			for i in range(3):
				# read stream until '?' mark is found
				outp = await reader.read(1024)
				if not outp:
					break
				elif utils.match_list(outp, consts.CLI_PROMPT_USERNAME):
					# elif 'Username:' in outp:
					debug_print("enter username: " + username)
					writer.write(username + consts.EOL)
					time.sleep(1)
				elif utils.match_list(outp, consts.CLI_PROMPT_PASSWORD):
					# elif 'Password:' in outp:
					debug_print("enter password: ", outp)
					writer.write(password + consts.EOL)
					time.sleep(1)

				elif utils.match_list(outp, consts.CLI_PROMPT_LOGIN_SUCCESS):
					# elif 'Router#' in outp:
					# debug_print("enter command: ", outp)
					for cmd in self.cos.command_list:
						debug_print("enter command: " + cmd)
						writer.write(cmd + consts.EOL)
						time.sleep(self.cos.command_interval)
						outp = await reader.read(-1)
						debug_print(outp)
					login_success = True
					break  # 写完， 从外部读输出
				else:
					debug_print("nothing match in telnet")
					time.sleep(0.5)

			result.login_success = login_success
		return telnet_shell

	# debug_print("telnet output: " + outp)
	# 通过telnet抓取配置
	def pull_config_by_telnet(self, host_addr='', username='', password='') -> ExecuteResult:
		result = ExecuteResult(
			host=host_addr,
			username=username,
			password=password,
			protocol=consts.LOGIN_TYPE_TELNET,
			connect_detail=ConnectDetail())
		# shell = self.__gen_telnet_shell(username=username, password=password, result=result)
		debug_print("starting telnet login into " + host_addr)
		tn = None
		try:
			tn = mtl.Telnet(host=host_addr, port=self.cos.telnet_port, timeout=self.cos.conn_timeout)
			if not tn:
				result.err += 'connect to {} timeout in {} seconds'.format(host_addr, self.cos.conn_timeout)
				debug_print("telnet login into " + host_addr + " failed")
				return result
			# result.connect_success = True
			result.detail.telnet_connect_success = True
			debug_print("telnet login {} success".format(host_addr))

			self.add_closer(Closer(tn, name="{}-{}".format(host_addr, consts.LOGIN_TYPE_TELNET)))

			# 输入用户名
			debug_print("waiting for username prompt:")
			index, aa, bb = tn.expect(utils.encode_list(consts.CLI_PROMPT_USERNAME), 5)
			if index < 0:
				msg = "expect username prompt failed"
				result.err += msg
				debug_print(msg)
				print(index, aa, bb)
				return result
			debug_print("input username " + username)
			tn.write(utils.encode_str(username + "\n"))
			time.sleep(1)

			# 输入密码
			debug_print("waiting for password prompt:")
			index, _, _ = tn.expect(utils.encode_list(consts.CLI_PROMPT_PASSWORD), 5)
			if index < 0:
				msg = "expect password prompt failed"
				result.err += msg
				debug_print(msg)
				return result
			debug_print("input password ")
			tn.write(utils.encode_str(password + "\n"))
			time.sleep(1)

			# 多敲几个回车 # 等待登录成功
			prompt_str = ''
			for _ in range(3):
				debug_print("empty newline")
				index, _, prompt_bytes = tn.expect(utils.encode_list(consts.CLI_PROMPT_LOGIN_SUCCESS), 1)
				# print(prompt_bytes)
				# index, _, prompt_bytes = tn.expect(utils.encode_list(["\r\n<Huawei>$"]), 1)
				if index < 0:
					tn.write(utils.encode_str("\r\n"))
					debug_print("expect login success prompt failed. got: " + str(prompt_bytes, encoding="utf-8").strip())
					continue
				else:
					# 再敲几次回车
					for _ in range(2):
						tn.write(utils.encode_str("\r\n"))
						index, _, prompt_bytes = tn.expect(utils.encode_list(consts.CLI_PROMPT_LOGIN_SUCCESS), 1)

					prompt_str = str(prompt_bytes, encoding="utf-8").strip()
					debug_print("expect login success prompt success. got: " + prompt_str)
					break
			# debug_print("waiting for login success prompt:")
			# index, _, prompt_bytes = tn.expect(utils.encode_list(consts.CLI_PROMPT_LOGIN_SUCCESS), 5)
			# if index < 0:
			# 	debug_print("expect login success prompt failed")
			# 	return result
			if not prompt_str:
				msg = "waiting for login success prompt failed"
				result.err += msg
				debug_print(msg)
				return result

			debug_print(host_addr + " login success. prompt is: " + prompt_str)
			result.login_success = True

			# 发空命令
			def send_empty_cmd(cmd_index: int) -> Timer:
				try:
					# if cmd_index > 0:
					debug_print("write empty command")
					tn.write(utils.encode_str("\r\n"))
					t = Timer(self.cos.empty_command_interval, send_empty_cmd, [cmd_index])
					t.start()
					return t
				except:
					return None

			empty_cmd_timer = None
			for index, cmd in enumerate(self.cos.command_list):
				debug_print(host_addr + " telnet exec cmd: " + cmd)
				tn.write(utils.encode_str(cmd + "\n"))
				if self.cos.opmode == consts.OP_MODE_GET:
					# 空命令逻辑
					if empty_cmd_timer:
						# 每次开始新命令都取消之前的timer
						empty_cmd_timer.cancel()
					else:
						empty_cmd_timer = send_empty_cmd(index)

					output = ''
					try:
						_, _, output = tn.expect(
							list=utils.encode_list([re.escape(cmd) + r"[\d\D]*(\r\n|\r|\n)" + re.escape(prompt_str) + "$"]),
							timeout=self.cos.one_command_timeout  # 一条命令最长时间
						)
					# print("output: ", output)
					except EOFError:
						msg = "! exec cmd: {} timeout in {} seconds".format(cmd, self.cos.one_command_timeout)
						debug_print(msg)
						result.err += msg
					time.sleep(self.cos.command_interval)
				else:
					# set操作执行很快, 停留一会就行. 而且prompt可能变, 所以不管, 就依次执行命令就行
					# 这里就让它match失败, 超时就行
					output = tn.read_until(match="!@#$%^&*()_+123jfla".encode("ascii"), timeout=self.cos.command_interval)
					debug_print("set result: " + str(output, encoding="utf-8"))
				# print("output", output)
				tmp_result = str(output, encoding="utf-8")
				result.output += tmp_result
				# 检测是否有命令错误
				if utils.match_list(tmp_result, consts.UNKNOWN_COMMANDS):
					msg = "unknown command " + tmp_result
					debug_print(msg)
					result.err += msg
					result.command_ok = False
					if not self.cos.ignore_on_command_error:
						return result
		except Exception as e:
			utils.stderr_write("pull_config_by_telnet: {0}".format(e))
			result.err += "exception {}".format(e)
		finally:
			if tn:
				tn.close()
			return result

	async def pull_one_async(self, loop=None, semaphore=None, host: Host = None, protocol_list=None):
		async with semaphore:
			# return self.pull_one_sync(host=host, protocol_list=protocol_list)
			executor = ThreadPoolExecutor()
			return await loop.run_in_executor(executor, self.pull_one_sync, host, protocol_list)

	def pull_one_sync(self, host: Host = None, protocol_list=None) -> ExecuteResult:
		result = None
		for p in protocol_list:
			for a in self.cos.account_list:
				if p == consts.LOGIN_TYPE_SSH:
					pre_result = result
					result = self.pull_config_by_ssh(host=host, username=a.username, password=a.password)
					if pre_result:
						result.detail.telnet_connect_success = pre_result.detail.telnet_connect_success
					# 连接失败可能是用户名或者密码错误, 端口可能能连上
					if not result.detail.ssh_connect_success:
						utils.debug_print("detect ssh port {}".format(self.cos.ssh_port))
						result.detail.ssh_connect_success = utils.detect_port(
							addr=host.addr,
							port=self.cos.ssh_port,
							timeout_seconds=max(self.cos.conn_timeout, 10))
				elif p == consts.LOGIN_TYPE_TELNET:
					pre_result = result
					result = self.pull_config_by_telnet(host_addr=host.addr, username=a.username, password=a.password)
					if pre_result:
						result.detail.ssh_connect_success = pre_result.detail.ssh_connect_success
				else:
					utils.debug_print("unsupported login type: {}".format(p))
					continue

				# host.protocol = p  # 指定以什么协议来抓取
				# # telnet/ssh都通过netmiko来登录
				# result = self.pull_config_by_ssh(host=host, username=a.username, password=a.password)

				# 只要有登录成功的就退出(如果命令出错, 说明是命令不对(和类型不匹配), 换协议, 换账号也没用)， 避免无用的tcp连接
				if result.login_success:
					return result

				# 同上说明, 命令出错, 换协议,换账号都不会有用的
				# 如果配置了ignore_on_command_error为false，且发现有命令错误的， 直接退出
				if not self.cos.ignore_on_command_error and not result.command_ok:
					return result
		return result

	def gen_filename(self, host='', protocol='', username='', connect_ok=False, login_ok=False):
		time_str = utils.get_current_time(time_format='%Y%m%d_%H%M%S', with_ms=False)
		m = {
			"host": host,
			"protocol": protocol,
			"username": username,
			"connect_ok": "connect_" + ("ok" if connect_ok else "err"),
			"login_ok": "login_" + ("ok" if login_ok else "err"),
			"time": time_str,
		}
		return self.cos.output_filename_format.format(**m)

	def __write_result(self, result: ExecuteResult):
		formatted_output = """
--host--: {host},
--username--: {username},
--password--: {password},
--protocol--: {protocol},
--login_success--: {login_success},
--connect_success--: {connect_success},
--command_ok--: {command_ok},
--ssh_port--: {ssh_port},
--telnet_port: {telnet_port},
--ssh_connect_success--: {ssh_connect_success},
--telnet_connect_success--: {telnet_connect_success},
--command_list--:{command_list},
--err--: {err},
--result--:
{result}

""".format(
			host=result.host,
			username=result.username,
			password=result.password if self.cos.output_password else "<DO NOT SHOW PASSWORD>",
			protocol=result.protocol,
			login_success=str(result.login_success),
			connect_success=str(result.detail.ssh_connect_success or result.detail.telnet_connect_success),
			command_ok=str(result.command_ok),
			ssh_port=self.cos.ssh_port,
			telnet_port=self.cos.telnet_port,
			ssh_connect_success=result.detail.ssh_connect_success,
			telnet_connect_success=result.detail.telnet_connect_success,
			command_list=" ".join(self.cos.command_list),
			err=result.err,
			result=result.output
		)
		if self.cos.output == "file":
			# 写入文件的同时, 也写到标准输出, 这样便于调用者处理
			utils.stdout_write(formatted_output, flush=True)

			filename = self.gen_filename(
				host=result.host,
				protocol=result.protocol,
				username=result.username,
				login_ok=result.login_success,
				connect_ok=result.detail.ssh_connect_success or result.detail.telnet_connect_success,
			)
			filename += ".txt"

			a, b = utils.write_file(dir=self.cos.output_dir, filename=filename, content=formatted_output)
			filename_full_path = filename if not self.cos.output_dir else self.cos.output_dir + "/" + filename
			if not a and not b:
				debug_print("write file: {} failed".format(filename_full_path))
				return
			debug_print("write to file: {} success".format(filename_full_path))
		else:  # 如果不是文件的话， 都输出到stdout
			# lst = [
			# 	"\n--host--: " + result.host,
			# 	"--username--: " + result.username,
			# 	# "--password--: " + result.password,
			# 	"--protocol--: " + result.protocol,
			# 	"--login_success--: " + str(result.login_success),
			# 	"--connect_success--: " + str(result.connect_success),
			# 	"--command_ok--: " + str(result.command_ok),
			# 	"--err--: " + str(result.err),
			# 	"--result--:\n" + result.output,
			# ]
			# utils.stdout_write('\n'.join(lst), flush=True)
			utils.stdout_write(formatted_output, flush=True)

	def run_async(self):
		# # 注意要引入，否则会报错(在用telnetlib3的时候)
		# import nest_asyncio
		# nest_asyncio.apply()

		# print(vars(co))
		if self.cos.protocol == '':
			# 注意这里的登录的顺序， ssh优先
			self.cos.protocol = ','.join([consts.LOGIN_TYPE_SSH, consts.LOGIN_TYPE_TELNET])

		loop = None
		try:
			loop = asyncio.get_event_loop()
			semaphore = asyncio.Semaphore(self.cos.concurrency)
			tasks = []
			protocol_list = self.cos.protocol.split(",")
			for host in self.cos.host_list:
				tasks.append(asyncio.ensure_future(self.pull_one_async(loop, semaphore, host=host, protocol_list=protocol_list)))
			dones, _ = loop.run_until_complete(asyncio.wait(tasks))

			for r in dones:
				result = r.result()  # 可以host来区分结果是谁的
				self.__write_result(result)
		finally:
			loop.close()

	def run_sync(self):
		# print(vars(co))
		if self.cos.protocol == '':
			# 注意这里的登录的顺序， ssh优先
			self.cos.protocol = ','.join([consts.LOGIN_TYPE_SSH, consts.LOGIN_TYPE_TELNET])

		protocol_list = self.cos.protocol.split(",")
		for host in self.cos.host_list:
			result = self.pull_one_sync(host=host, protocol_list=protocol_list)
			self.__write_result(result)

	def run(self):
		start = time.time()
		utils.stdout_write("process start at: " + utils.get_current_time(), flush=True)
		self.__ttlTimer.start()
		if self.cos.concurrency > 1:
			self.run_async()
		else:
			self.run_sync()

		self.cancel_timer()
		utils.stdout_write("run end. used {} seconds".format('%.2f' % (time.time() - start)), flush=True)


def main():
	SwitchRouterCommandExecutor().run()


if __name__ == '__main__':
	main()
