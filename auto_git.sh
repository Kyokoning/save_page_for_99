echo `date +"%Y-%m-%d %H:%M:%S"`
echo "####### 进入项目路径 #######"
/home/xnchen/code/save_page_for_99
echo "####### 开始自动备份 #######" 
git add .

sleep 1s
git commit -m "auto_update"
sleep 1s
git push -u origin master

echo "####### 自动备份执行完毕 #######"
