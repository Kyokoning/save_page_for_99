#!/bin/sh
# server.py是进程名称，修改为自己的即可
# 用crontab -e将此守护进程添加到定时任务，可实现每小时/分钟重启server.py
# 55 7 * * * /home/username/code/save_page_for_99/server_daemon.sh
# 如果crontab -e的运行环境缺失部分环境变量

# 应用启动的根目录
TZ='Asia/Shanghai'; export TZ;
nohup python -u /home/xnchen/code/save_page_for_99/tool/launcher.py --cfg /home/xnchen/code/save_page_for_99/config/test.yaml >> server.log 2>&1 &
