from nonebot.plugin.on import on_command
from nonebot.adapters import Message
from nonebot.params import EventMessage
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
import pymongo
import json

f = open('src/config/chensbot_config.json', 'r', encoding='utf-8')# 读取config
json_res = json.load(f)
mdb_conn = json_res['mdb_conn']# mongodb连接地址

client = pymongo.MongoClient(mdb_conn)# mongodb连接地址
db = client['ChensQBOTv2']

matcher = on_command('finder')

@matcher.handle()
async def _(event: GroupMessageEvent, rxmsg: Message = EventMessage()):
    receive_msg = str(rxmsg).strip().split()
    request_qid = str(event.user_id)
    request_grpid = str(event.group_id)
    await matcher.send(MessageSegment.at(request_qid) + '未开放')
    
'''
示例：
/finder [MODE] [INFO]
MODE：
qid -> 通过QQ号查询信息
wid -> 通过微博号查询信息
lol -> 通过王者ID查询信息
ph -> 通过手机号查询信息
INFO：
要查询的信息
'''