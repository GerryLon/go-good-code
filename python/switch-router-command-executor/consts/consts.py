#!/usr/bin/python3

# 厂商分类
# MFG_AUTO = 0 # 自动推测
MF_CISCO = "cisco"  # manufacturer
MF_H3C = "h3c"
MF_JUNIPER = "juniper"
MF_HUAWEI = "huawei"
MF_LINUX = "linux"  # 测试用
# MF_ALL = "all"  # 以上设备都不是， 就用这个
MF_AUTODETECT = "autodetect"  # 自动检测


# 登录类型
LOGIN_TYPE_SSH = "ssh"
LOGIN_TYPE_TELNET = "telnet"

# 参考: https://github.com/ktbyers/netmiko/blob/master/netmiko/ssh_dispatcher.py
# 设备对应的device_type, Netmiko这个库会用到
DEVICE_TYPE_MAPPING = {
	LOGIN_TYPE_SSH: {
		MF_CISCO: ["cisco_ios"],
		MF_H3C: ["hp_comware", "hp_procurve"], # TODO netmiko暂时不支持h3c, 用hp的试试
		MF_JUNIPER: ["juniper_junos"],

		# https://github.com/ktbyers/netmiko/blob/master/netmiko/ssh_dispatcher.py
		MF_HUAWEI: ["huawei", "huawei_vrpv8"],  # TODO netmiko支持多个 , 可以按","分隔多试试
		MF_LINUX: ["linux"],
	},

	# netmiko支持部分 telnet
	LOGIN_TYPE_TELNET: {
		MF_CISCO: ["cisco_ios_telnet", "cisco_xr_telnet"],
		MF_H3C: ["hp_comware_telnet", "hp_procurve_telnet"],
		MF_JUNIPER: ["juniper_junos_telnet"],
		MF_HUAWEI: ["huawei_telnet"],
		MF_LINUX: ["generic_telnet"],  # 测试用
	}
}

EOL = "\n"

PROMPT_USERNAME = 1
PROMPT_PASSWORD = 2
PROMPT_LOGIN_SUCCESS = 3

# telnetlib需要的, 对应输入用户名和密码时的提示, 各个设备不太一样
# 只是针对telnetlib这个库用的
# 可以使用正则
# TODO, 需要完善，细化
# 这里其实不用区分
# 这个提示名完全可以由运维自定义的， 根据型号来区分没有意义
PROMPT_LOGIN_SUCCESS_COMMON = "[a-zA-Z][a-zA-Z0-9_\-]{2,}"
DEVICE_PROMPT_MAPPING = {
	PROMPT_USERNAME: {
		MF_CISCO: ["^(?:[Uu]ser[Nn]ame|[Ll]ogin): ?$"],
		MF_H3C: ["^(?:[Uu]ser[Nn]ame|[Ll]ogin): ?$"],
		# MFG_ALL: ["\[[a-zA-Z0-9\-_#\] ]+: ?$", "^.+[:#] ?$", "^.+$"],
		MF_AUTODETECT: ["^(?:[Uu]ser[Nn]ame|[Ll]ogin): ?$"],
	},
	PROMPT_PASSWORD: {
		MF_CISCO: ["^[Pp]ass[Ww]ord: ?$"],
		MF_H3C: ["^[Pp]ass[Ww]ord: ?$"],
		# MFG_ALL: ["[a-zA-Z]+: ?$", "^.+: ?$"],
		MF_AUTODETECT: ["^[Pp]ass[Ww]ord: ?$"],
	},

	# 登录成功后的提示, 如"xxx-CISC1234#", "<xxx-001>"
	# 一般为主机名
	PROMPT_LOGIN_SUCCESS: {
		MF_CISCO: [""+PROMPT_LOGIN_SUCCESS_COMMON+"#$", "<"+PROMPT_LOGIN_SUCCESS_COMMON+">$", ""+PROMPT_LOGIN_SUCCESS_COMMON+"$"],
		MF_H3C: [""+PROMPT_LOGIN_SUCCESS_COMMON+"#$", "<"+PROMPT_LOGIN_SUCCESS_COMMON+">$", ""+PROMPT_LOGIN_SUCCESS_COMMON+"$"],
		MF_AUTODETECT: [""+PROMPT_LOGIN_SUCCESS_COMMON+"#$", "<"+PROMPT_LOGIN_SUCCESS_COMMON+">$", ""+PROMPT_LOGIN_SUCCESS_COMMON+"$"],
	}
}

CLI_PROMPT_USERNAME = ["([Uu]ser[Nn]ame|[Ll]ogin): ?$"]
CLI_PROMPT_PASSWORD = ["[Pp]ass[Ww]ord: ?$"]
CLI_PROMPT_LOGIN_SUCCESS = [
	r"(\r\n|\r|\n)"+PROMPT_LOGIN_SUCCESS_COMMON+"#$",
	r"(\r\n|\r|\n)<"+PROMPT_LOGIN_SUCCESS_COMMON+">$",
	r"(\r\n|\r|\n)"+PROMPT_LOGIN_SUCCESS_COMMON+"$",
]

# 操作类型： 读取 or 设置
OP_MODE_GET = "get"
OP_MODE_SET = "set"

# 执行过程中遇到命令错误的
UNKNOWN_COMMANDS = [
	"Unknown command",
	"Error: Unrecognized command",
	"% Unrecognized command",
	"% Invalid input",
	"% Too many parameters",
]

# format placeholder
FPH_IP = "{ip}"
FPH_PROTOCOL = "{protocol}"
FPH_USERNAME = "{username}"
FPH_TIME = "{time}"
FPH_LOGIN_OK = "{login_ok}"
FPH_CONNECT_OK = "{connect_ok}"

# {protocol}-{host}-{username}-{login_ok}-{time}

# 如果要执行空命令(为了保活, 避免长期不动导致session退出)
# 实际使用例如:
# C^-32 表示当前要执行空格
EMPTY_CMD_PREFIX = "C^-"
