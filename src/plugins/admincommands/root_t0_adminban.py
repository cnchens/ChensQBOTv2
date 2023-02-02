from nonebot.plugin.on import on_command
from nonebot.adapters import Message
from nonebot.params import EventMessage
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from nonebot.adapters.onebot.v11.bot import Bot
import pymongo
import json
import datetime
import pytz

f = open('src/config/chensbot_config.json', 'r', encoding='utf-8')# 读取config
json_res = json.load(f)
mdb_conn = json_res['mdb_conn']# mongodb连接地址

client = pymongo.MongoClient(mdb_conn)# mongodb连接地址
db = client['ChensQBOTv2']

rootuser_col = db['admin_rootuser']
t0op_col = db['admin_t0op']
ban_col = db['banlist']

matcher = on_command('adminban')

@matcher.handle()
async def _(bot: Bot, event: GroupMessageEvent, rxmsg: Message = EventMessage()):
    receive_msg = str(rxmsg).strip().split()
    request_qid = str(event.user_id)
    request_grpid = str(event.group_id)

    isrootuser = False
    ist0 = False
    for i in rootuser_col.find():
        if request_qid == i['qid']:
            isrootuser = True
            break
        else:
            isrootuser = False
            pass
    for i in t0op_col.find():
        if request_qid == i['qid']:
            ist0 = True
            break
        else:
            ist0 = False
            pass

    if isrootuser == True or ist0 == True:
        if len(receive_msg) == 4:
            try:
                gmt8_time = datetime.datetime.now(tz=pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')
                if receive_msg[1] == 'this':
                    ban_grpid = int(request_grpid)
                    ban_qid = int(receive_msg[2])
                    ban_reason = receive_msg[3]
                    bot.set_group_kick(group_id=ban_grpid, user_id=ban_qid)

                    ban_grpid = str(ban_grpid)
                    ban_qid = str(ban_qid)
                    ban_col.insert_one({'time' : gmt8_time, 'grp' : ban_grpid, 'qid' : ban_qid, 'reason' : ban_reason, 'operator' : request_qid})
                    await matcher.send(MessageSegment.at(request_qid) + '封禁成功')
                else:
                    ban_grpid = int(receive_msg[1])
                    ban_qid = int(receive_msg[2])
                    ban_reason = receive_msg[3]
                    bot.set_group_kick(group_id=ban_grpid, user_id=ban_qid)

                    ban_grpid = str(ban_grpid)
                    ban_qid = str(ban_qid)
                    ban_col.insert_one({'time' : gmt8_time, 'grp' : ban_grpid, 'qid' : ban_qid, 'reason' : ban_reason, 'operator' : request_qid})
                    await matcher.send(MessageSegment.at(request_qid) + '封禁成功')
            except:
                await matcher.send(MessageSegment.at(request_qid) + '\n' + 
'''
错误：语法错误
示例：
/adminban [GRPID] [QID] [REASON]
GRPID：
this -> 本群
或指定某群ID
QID：
封禁的QID
REASON：
封禁的原因
'''.strip()
            )
        else:
            await matcher.send(MessageSegment.at(request_qid) + '\n' + 
'''
示例：
/adminban [GRPID] [QID] [REASON]
GRPID：
this -> 本群
或指定某群ID
QID：
封禁的QID
REASON：
封禁的原因
'''.strip()
            )
    else:
        await matcher.send(MessageSegment.at(request_qid) + '错误：权限不足')
    