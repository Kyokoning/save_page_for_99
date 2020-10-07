#!/bin/sh
# server.py是进程名称，修改为自己的即可
# 用crontab -e将此守护进程添加到定时任务，可实现每小时/分钟重启server.py
# 55 7 * * * /home/username/code/save_page_for_99/server_daemon.sh
# 如果crontab -e的运行环境缺失部分环境变量

# 应用启动的根目录

CODE_PATH='.' # your code path
PYTHON_PATH='/bin/python' # your python interpreter path

TZ='Asia/Shanghai'; export TZ;
cd ${CODE_PATH}/save_page_for_99/
nohup ${PYTHON_PATH}/python -u tool/launcher.py --cfg config/test.yaml >> launcher.log 2>&1 &
echo `date +"%Y-%m-%d %H:%M:%S"`
echo "success"
