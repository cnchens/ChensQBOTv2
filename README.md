# ChensQBOTv2
ChensQBOT的改进版

# 简介
ChensQBOTv2（简称CQBv2），是一款多功能的QQ群机器人，基于[NoneBot2](https://github.com/nonebot/nonebot2)开发，使用MongoDB数据库

# 运行需求
Python 3.10+  
MongoDB 6.0.0+  
NoneBot2

# 安装
- 在[MongoDB](https://www.mongodb.com/try/download/community-kubernetes-operator)页面下载符合你系统的MongoDB数据库安装程序（需求MongoDB 6.0.0以上）  
各个系统安装MongoDB的方式都有所不同，所以请自行百度  
**注意：在安装完成后请记牢MongoDB连接ip和端口！**  
- 在[Releases](https://github.com/cnchens/ChensQBOTv2/releases)页面下载最新的机器人源文件并解压  
1. 安装所需的插件：`pip install -r ./requirements.txt`  
2. 打开`./ChensBOTv2/src/config/chensbot_config.json`， 修改其中`mdb_conn`键的值，改为你的MongoDB连接地址  
示例：`"mdb_conn" : "mongodb://127.0.0.1:27017/"`  
3. 运行主程序：`nb run`  **（在执行此步骤前请务必确认已经正确配置MongoDB及chensbot_config.json，否则会报错！）**  
等待导入完成（一般导入时间在1~3分钟不等）  
- 在[go-cqhttp](https://github.com/Mrs4s/go-cqhttp/releases)页面下载符合你系统的go-cqhttp
1. 创建一个空文件夹存放解压好的go-cqhttp文件  
2. 在终端中运行go-cqhttp，选择`反向Websocket通信`，等待`config.yml`生成  
3. 打开`config.yml`，配置：  
`account -> uin: 你的QQ账号`  
`account -> password: 你的QQ密码（可选）`  
`servers -> - ws-reverse -> universal: ws://127.0.0.1:20010/onebot/v11/ws`  
4. 运行go-cqhttp

至此，你已经成功安装并运行了ChensQBOTv2  
发送/help可以查看帮助文档

# 帮助文档
暂时还未完成，可前往QQ群：281814041寻求帮助（入群验证填写github）

# License
GNU GPLv3