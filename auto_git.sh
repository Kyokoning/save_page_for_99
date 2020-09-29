echo `date +"%Y-%m-%d %H:%M:%S"`
echo "####### 进入项目路径 #######"
/home/xnchen/code/save_page_for_99
echo "####### 开始自动备份 #######" 
nohup git add . >> git.log 2>&1 &

sleep 1s
nohup git commit -m "auto_update" >> git.log 2>&1 &
sleep 1s
git stash
nohup git pull --rebase >> git.log 2>&1 &
git stash pop
sleep 5s
nohup git push -u origin master >> git.log 2>&1 &

echo "####### 自动备份执行完毕 #######"

