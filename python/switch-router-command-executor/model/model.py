#!/usr/bin/python3


import consts.consts as consts


# model


class Account:
	"""
	登录凭据抽象
	"""
	def __init__(self, username='', password='', string_show_password=False):
		self.username = username
		self.password = password
		self.string_show_password = string_show_password

	def __str__(self) -> str:
		return "username: {username}, password: {password}".format(
			username=self.username,
			password=self.password if self.string_show_password else "*" * len(self.password)
		)

	def __repr__(self):
		return self.__str__()


class Host:
	"""
	路由器/交换机

	protocol: 指定的登录方式, 默认ssh
	"""
	def __init__(self, addr='', device_type='cisco', protocol=consts.LOGIN_TYPE_SSH):
		self.addr = addr
		self.device_type = device_type
		self.protocol = protocol

	def __str__(self) -> str:
		return "host: {addr}, {device_type}, {protocol}".format(
			addr=self.addr, device_type=self.device_type, protocol=self.protocol)


class ConnectDetail:
	"""
	连接详情
	"""
	def __init__(
		self,
		ssh_connect_success=False,
		telnet_connect_success=False
	):
		self.ssh_connect_success = ssh_connect_success
		self.telnet_connect_success = telnet_connect_success


class ExecuteResult:
	"""
	关于某台设备的 执行结果抽错
	"""
	def __init__(
		self,
		host: str = '',
		username: str = '',
		password: str = '',
		protocol='',
		connect_detail: ConnectDetail = None,
		login_success=False,  # 是否登录成功
		output='',  # 执行结果（如show run的返回）
		err: str = '',  # 记录执行的错误
		command_ok=True,  # 执行命令时是否有报错（一般为不识别的命令）
	):
		self.host = host
		self.username = username
		self.password = password
		self.protocol = protocol
		self.detail = connect_detail
		self.login_success = login_success
		self.output = output
		self.err = err
		self.command_ok = command_ok


class CliOptions:
	"""
	表示命令行参数的类， 免得用map引用不清晰
	"""

	def __init__(
		self,
		account_list=None,
		opmode='',
		one_command_timeout: int = 10,
		host_list=None,
		command_list=None,
		conn_timeout=5,
		empty_command_interval=30,
		protocol='',
		ssh_port=22,
		telnet_port=23,
		command_interval=0.5,
		# parallel=False,
		concurrency=1,
		ignore_on_command_error=False,
		output='',
		output_dir='',
		output_filename_format='',
		debug=False,
		ttl=600,
		output_password=False):

		self.account_list = account_list
		self.opmode = opmode
		self.one_command_timeout = max(one_command_timeout, 1)  # 最小为1
		self.host_list = host_list
		self.command_list = command_list
		self.conn_timeout = max(conn_timeout, 1)  # 最小为1
		self.empty_command_interval = empty_command_interval
		self.protocol = protocol
		self.ssh_port = ssh_port
		self.telnet_port = telnet_port
		self.command_interval = float(command_interval)
		# self.parallel = parallel
		self.concurrency = max(concurrency, 1)  # 最小为1
		self.ignore_on_command_error = ignore_on_command_error
		self.output = output
		self.output_dir = output_dir
		self.output_filename_format = output_filename_format
		self.debug = debug
		self.ttl = ttl
		self.output_password = output_password


class Closer:
	"""
	obj: 一个有close方法的对象
	"""
	def __init__(self, __obj: object, name: str = ''):
		self.__obj = __obj
		self.name = name

	def __str__(self) -> str:
		return "closer: {}".format(self.name)

	def close(self):
		try:
			if not self.__obj:
				return
			if "close" in dir(self.__obj):
				self.__obj.close()
			else:
				pass
		except:
			pass
