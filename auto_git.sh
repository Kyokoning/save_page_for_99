#bin/bash
cd /home/xnchen/code/save_page_for_99
GIT=`which git`
${GIT} add --all
${GIT} pull --rebase
time=`date`
${GIT} commit -m "提交的时间是: $time"
HOME=/home/xnchen ${GIT} push origin master:server_backup