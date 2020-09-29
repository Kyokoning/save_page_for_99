
## abstract

这是一个兴趣使然的网络爬虫，给没法早起的我自己(来自@donlv1997的吐槽，比我起得)

## 功能

- 在服务器上运行的脚本，每天7：55唤醒（需要守护进程）

- 在服务器上的配置文件中设置功能
    - 存贴模式是多选，包括输入贴号和关键字存贴
    - 输入贴号：当天输入的99帖子号码，后一天7：55唤醒之后会被存取（如果存在的话）
    - 关键字存贴：当天输入的帖子关键字，后一天7：55唤醒之后会被存取（当天可以搜索到关键字的帖子）

## 文件结构
```
.
├── README.md
├── server_daemon.sh
├── config
├── output
├── log
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

`server.py`: 服务器接收网络消息的脚本（然而现在并没有用到）

`server_daemon.sh` : 守护进程shell文件

`log/`: log文件存放

`output/`: 存储帖子的位置，存储格式是markdown（暂时），path格式是`output/日期/帖标题`

## Quick Start

### 1.安装依赖：

`pip install -r requirements.txt`

### 2.根据需要修改配置文件：

使用任何文本编辑器打开`config/test.yaml`，修改配置。配置细节在下表列出。

配置选项|默认值|描述|示例
:-------:|:----:|-------|----
OUTPUT_DIR|output|保存存档的地址(绝对地址/相对地址都ok)|output/
LOG_DIR|log|脚本输出提示信息存储地址|log/
KEYWORD|true|搜索关键词模式|true或者false都可以
KEYWORD_LIST|\["ggl"\]|如果选择了搜索关键词模式，那么脚本自动搜索并存储这个list里面所有列出的tag中当天的帖子|\['ggl', 'miu'\]
POST|flase|搜索楼号模式|true或者false都可以
POST_LIST|[]|如果选择了楼号模式，那么脚本自动存储这个list里面所有列出的当天楼号|\['785773'\]

#### 几个tips

    1. 在linux系统中会出现标题名长度限制，目前长度设置为50个字符。
    2. 搜索tag的方法：因为是做给自己的，只弄了使用帖子标题搜索的方法。

### 3.普通方法

在你想要存贴的时候，跳转到code所在文件夹，并在命令行中输入 

`python tool/launcher.py --cfg config/test.yaml`

将会根据你在配置文件中的设置存储帖子

### 守护进程

本脚本最重要的部分。需要服务器。

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



### 使用脚本自动push来远程访问的方法

当你的代码在远程服务器设置好之后，可以使用git的小脚本+守护进程来自动push到私人gitlab等。

这一方法在`auto_git.sh`中由绿绿实现。(@donlv1997 excuse me?wsm要call我这个名字???)

### 自动GIT PUSH的办法

请您不要作死使用下面的表达式，把cron表达式改为每天（而不是每分钟）。从而避免被GIT仓库管理员打死。

```shell
0-59 * * * * /bin/sh /home/usrname/code/save_page_for_99/auto_git.sh >> /home/usrname/code/auto_git.log 2>&1
```
