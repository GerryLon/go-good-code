#!/usr/bin/env bash

# 使用多进程来模拟多线程序

# 可实现类似这样的效果, 最多三个ping在跑
#$ ps -ef|grep ping
#gerrylon 19486 19485  0 08:50 pts/0    00:00:00 ping -c 1 -W 1 10.25.8.216
#gerrylon 19488 19487  0 08:50 pts/0    00:00:00 ping -c 1 -W 1 10.25.8.217
#gerrylon 19490 19489  0 08:50 pts/0    00:00:00 ping -c 1 -W 1 10.25.8.218
#gerrylon 19492 18467  0 08:50 pts/3    00:00:00 grep --color=auto ping
concurrency=${1:-3} # 并发数, 默认为3

fd=8 # 临时的文件描述符
fifoFile=/tmp/$$.fifo # 命名管道文件

clean() {
  exec 8>&-
  rm -f $fifoFile
}

# echo "pid: $$"
mkfifo $fifoFile # 创建命名管道文件
exec 8<> $fifoFile # 8号文件描述符与管道文件绑定(输入输出都绑定)
#rm -vf $fifoFile # 删除这个不影响.
trap clean EXIT # 解绑

for _ in $(seq "$concurrency"); do
  echo >& $fd
done

for i in $(seq 1 254); do
  read -r -u $fd
  {
  ip="10.25.8.$i"
  if ping -c 1 -W 1 "$ip" >/dev/null 2>&1; then
    echo "$ip is up"
  else
    echo "$ip is down"
  fi
  echo >& $fd
  }&
done

exit 0
