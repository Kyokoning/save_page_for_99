
### abstract

这是一个兴趣使然的网络爬虫，给没法早起的我自己

### 实现目标

- 在服务器上运行的脚本，每天7：55唤醒（需要守护进程）

- 在手机/远程PC上运行的服务端，用来发送给服务器想要存的东西
    - 存贴模式是多选，包括输入贴号和关键字存贴
    - 输入贴号：当天输入的99帖子号码，后一天7：55唤醒之后会被存取（如果存在的话）
    - 关键字存贴：当天输入的帖子关键字，后一天7：55唤醒之后会被存取（当天可以搜索到关键字的帖子）

### 文件结构
```
.
├── README.md
├── server_daemon.sh
├── config
├── output
├── log
├── temp
├── server_daemon.sh
├── lib
│   ├── config.py
│   ├── fetch_post.py
│   └── logger.py
└── tool
    ├── _init_paths.py
    ├── server.py
    └── launcher.py
```

`launcher.py`: 服务器存贴脚本入口

`server.py`: 服务器接收网络消息的脚本

`server_daemon.sh` : 守护进程shell文件（施工中）

`log/`: log文件存放

`output/`: 存储帖子的位置，存储格式是readme（暂时），path格式是`output/日期/帖标题`

`temp/`: 移动端当日发送到服务器端的请求会被存储在temp文件夹，等待日清前读取


