#!/usr/bin/python3

import time
import sys
import re
from inspect import getframeinfo, stack
import os
import signal
import socket


def exit_err(msg='', status_code=1, new_line=True, exit_immediately=False):
	if msg:
		if new_line:
			msg = msg + "\n"
		sys.stderr.write(msg)
	if exit_immediately:
		os._exit(status_code)
	else:
		sys.exit(status_code)


def exit_ok(msg=''):
	if msg:
		sys.stdout.write(msg)
	sys.exit(0)


# 标准输出
def stdout_write(msg, flush=False, newline=True):
	if newline:
		msg = msg + "\n"
	sys.stdout.write(msg)
	if flush:
		sys.stdout.flush()


# 标准错误输出
def stderr_write(arg):
	if type(arg) == str and arg[-1] != "\n":
		arg += "\n"
	sys.stderr.write(arg)
	debug_print("[STDERR]:" + arg)


def debug_print(msg):
	caller = getframeinfo(stack()[2][0])
	print("[{2}][{0}-DEBUG]:{1}".format(caller.lineno, msg, get_current_time()))


# 获取文件行数(不包括开始和结尾的空白)及文件内容(列表）（去除了开始和结束的空白）
def get_file_as_lines(file, ignore_empty_line=False):
	lines = []
	with open(file) as f:
		content = f.read().strip()
		if len(content) == 0:
			return lines
		
		# 统一换行符
		sep = "\n"
		re_eol = "\r\n|\r|\n"
		content = re.sub(re_eol, sep, content)
		
		if ignore_empty_line:
			for line in content.split("\n"):
				stripped_line = line.strip()
				if stripped_line:
					lines.append(stripped_line)
		else:
			for line in content.split("\n"):
				lines.append(line)
	
	return lines


def valid_ipv4(s: str):
	if not s:
		return False
	
	a = s.split('.')
	if len(a) != 4:
		return False
	for x in a:
		if not x.isdigit():
			return False
		i = int(x)
		if i < 0 or i > 255:
			return False
	return True


# 判断一个字符串是不是匹配给定的一系列正则
def match_list(s, regexp_list):
	for regexp in regexp_list:
		if re.findall(regexp, s, flags=re.M):
			return True
	return False


# 返回类似: 2018-06-04 19:06:32.641
def get_current_time(time_format="%Y-%m-%d %H:%M:%S", with_ms=True):
	ct = time.time()
	local_time = time.localtime(ct)
	data_head = time.strftime(time_format, local_time)
	if not with_ms:
		return data_head
	data_secs = (ct - int(ct)) * 1000
	time_str = "%s.%03d" % (data_head, data_secs)
	return time_str


RE_REPEAT = re.compile(r"^repeat\((\d+)\)-.+$")
def write_file(dir, filename, content):
	target_dir = os.path.normpath(dir)
	if not os.path.exists(target_dir):
		os.makedirs(target_dir)
	
	# filename = filename.decode('utf-8')
	filename_base = filename
	already_exist = False
	repeat_count = 0
	try:
		while os.path.isfile(os.path.normpath(os.path.join(target_dir, filename))):
			print("already exist:" + filename)
			already_exist = True
			match_obj = RE_REPEAT.match(filename)
			if match_obj:
				repeat_count = int(match_obj.group(1)) + 1
			else:
				repeat_count = 1
			filename = "repeat({0})-{1}".format(repeat_count, filename_base)
		# filename = filename.decode('utf-8')
		
		full_path = os.path.normpath(os.path.join(target_dir, filename))
		with open(full_path, 'w') as the_file:
			the_file.write(content)
		
		# 由于要打包发给客户使用, 用相对路径
		relative_path = os.path.normpath(os.path.join(dir, filename))
		# return fullPath, already_exist
		return relative_path, already_exist
	except Exception as e:
		return '', ''
	

def encode_str(s: str, encoding="ascii") -> bytes:
	return s.encode(encoding)

	
def encode_list(str_list, encoding="ascii") -> list:
	"""
	对一个str list中的所有元素重新编码
	"""
	new_list = list()
	for s in str_list:
		new_list.append(encode_str(s, encoding=encoding))
	return new_list


def signal_timeout_wrapper(timeout: int, func, *args, **kwargs):
	"""
	返回值表示func返回值 及 func是否超时
	"""
	def handler(signum, frame):
		raise AssertionError
	try:
		signal.signal(signal.SIGALRM, handler)
		signal.alarm(timeout)
		ret = func(*args, **kwargs)
		signal.alarm(0)
		return ret, False
	except AssertionError:
		return None, True


def spin_timeout_wrapper(timeout: int, func, *args, **kwargs):
	timeout = max(1, timeout)  # 最小为1
	end = time.time() + timeout
	func_called = False
	ret = None
	is_timeout = False  # 是否超时
	
	while time.time() < end:
		if not func_called:
			call_start = time.time()
			ret = func(*args, **kwargs)
			if time.time() - call_start > timeout:
				is_timeout = True
			func_called = True
		else:
			time.sleep(0.1)
	return ret, is_timeout


def detect_port(addr: str, port: int, timeout_seconds=3) -> bool:
	"""
	检测tcp 端口是否开放
	"""
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.settimeout(timeout_seconds)
		ok = s.connect_ex((addr, port)) == 0
		debug_print("detect_port: {}:{}, ok: {}".format(addr, port, ok))
		return ok
