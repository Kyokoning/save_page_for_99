
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

`server_daemon.sh` : 守护进程shell文件

`log/`: log文件存放

`output/`: 存储帖子的位置，存储格式是markdown（暂时），path格式是`output/日期/帖标题`

`temp/`: 移动端当日发送到服务器端的请求会被存储在temp文件夹，等待日清前读取


### 注意事项

#### 守护进程

本脚本最重要的部分。

使用守护进程在规定时间运行代码目录下的`server_daemon.sh`脚本。

如果你有一台持续运行的服务器，那么我们就可以通过守护进程来实现这一功能。

首先打开`server_daemon.sh`修改设置：

    CODE_PATH={你的CODE存放位置}/save_page_for_99
    PYTHON_PATH={你的python解释器位置}

然后设置守护进程：指令`crontab -e`

第一次使用cron会让你选择默认编辑器，请选择大家都很喜欢的vim。

在最后插入:

    CODE_PATH={你的CODE存放位置}/save_page_for_99
    55 7 * * * /bin/sh ${CODE_PATH}/server_daemon.sh

注意：cron的指令格式为：分钟 小时 日 月 星期 要运行的命令

要注意确定你的服务器是否是标准的东八区时间，如果不是，有两种解决方法：

- 修改你的服务器默认时间
- 将cron命令修改至能在东八区7：55运行

#### 保存名称

在linux系统中会出现标题名长度限制，目前长度设置为50个字符。

#### 搜索tag的方法

因为是做给自己的，只弄了使用帖子标题搜索的方法。


