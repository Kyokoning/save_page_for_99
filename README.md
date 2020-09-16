


### 组织结构

- 在服务器上运行的脚本，每天7：55唤醒

- 在手机/远程PC上运行的服务端，设置存贴模式和内容
    - 存贴模式是多选，包括输入贴号和关键字存贴
    - 输入贴号：当天输入的99帖子号码，后一天7：55唤醒之后会被存取（如果存在的话）
    - 关键字存贴：当天输入的帖子关键字，后一天7：55唤醒之后会被存取（当天可以搜索到关键字的帖子）
    
### 文件结构
```
.
├── README.md
├── config
│   └── test.yaml
├── lib
│   ├── config.py
│   ├── fetch_post.py
│   └── logger.py
├── output
├── server.py
├── server_daemon.sh
└── tool
    ├── _init_paths.py
    └── launcher.py
```