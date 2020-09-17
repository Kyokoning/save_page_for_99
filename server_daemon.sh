#!/bin/sh
# server.py是进程名称，修改为自己的即可
# 用crontab -e将此守护进程添加到定时任务，可实现每小时/分钟重启server.py
# 55 7 * * * /home/username/code/save_page_for_99/server_daemon.sh
# 如果crontab -e的运行环境缺失部分环境变量

v_num=`ps -ef | grep "server.py" | grep -v "grep" | grep -v "server_daemon.sh"|wc -l`
if [ $v_num -eq 0 ]
then 
date
echo "进程不存在"
# 应用启动的根目录
cd /home/s/auto
# 应用启动的命令,-u是考虑到python的缓存输出问题
nohup python -u tool/launcher.py --cfg config/test.yaml >> server.log 2>&1 &

v_num=`ps -ef | grep "tool/launcher.py" | grep -v "grep" | grep -v "server_daemon.sh"|wc -l`
if [ $v_num -eq 1 ]
then 
date
echo "正常启动"
fi
 
else 
date
echo "程序正常运行，不需要重启!"
fi
 
