from nonebot.plugin.on import on_command
from nonebot.adapters import Message
from nonebot.params import EventMessage
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
import pymongo
import json

f = open('src/config/chensbot_config.json', 'r', encoding='utf-8')# 读取config
json_res = json.load(f)
mdb_conn = json_res['mdb_conn']# mongodb连接地址

client = pymongo.MongoClient(mdb_conn)# mongodb连接地址
db = client['ChensBOTv2']

config_col = db['cb_config']

admingiveop = on_command('admingiveop')

@admingiveop.handle()
async def _(event: GroupMessageEvent, rxmsg: Message = EventMessage()):
    receive_msg = str(rxmsg).strip().split()
    request_qid = str(event.user_id)
    request_grpid = str(event.group_id)

    config_col_rootuser = config_col.find_one()['rootuser']
    for i in config_col_rootuser:
        if i == request_qid:
            if len(receive_msg) == 2:
                if receive_msg[1] == 'help':
                    await admingiveop.send(
f'''
[CQ:at,qq={request_qid}]
示例：
/admingiveop [GRPID] [OP_LEVEL] [QID]
GRPID：
this -> 本群
或指定某群ID
OP_LEVEL：
0   最高权限（次于rootuser权限）
1   中等权限
2   最低权限
QID：
给予OP权限的QID
'''.strip()
                    )
            else:
                if len(receive_msg) == 4:
                    try:
                        if receive_msg[1] == 'this':
                            grpid = event.get
        else:
            await admingiveop.send(f'[CQ:at,qq={request_qid}]错误：权限不足')

    