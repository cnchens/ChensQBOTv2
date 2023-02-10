from nonebot.plugin.on import on_command
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
import pymongo
import json
import random

f = open('src/config/chensbot_config.json', 'r', encoding='utf-8')# 读取config
json_res = json.load(f)
mdb_conn = json_res['mdb_conn']# mongodb连接地址

client = pymongo.MongoClient(mdb_conn)# mongodb连接地址
db = client['ChensQBOTv2']
sfz_col = db['sfz']

matcher = on_command('rdsfz')

@matcher.handle()
async def _(event: GroupMessageEvent):
    request_qid = str(event.user_id)
    n = str(random.randint(1, 131460))
    for i in sfz_col.find():
        if i['num'] == n:
            sfz = i['info']
            await matcher.send(MessageSegment.at(request_qid) + sfz)
            break
        else:
            pass
