#bin/bash
CODE_PATH='./code' # your code path
cd ${CODE_PATH}
GIT=`which git`
${GIT} add --all
${GIT} pull --rebase
time=`date`
echo $time
${GIT} commit -m "提交的时间是: $time"
${GIT} push origin server_backup
