#bin/bash
cd /home/xnchen/code/save_page_for_99
GIT=`which git`
${GIT} pull --rebase
${GIT} add --all
time=`date`
${GIT} commit -m "提交的时间是: $time"
HOME=/home/xnchen ${GIT} push origin master