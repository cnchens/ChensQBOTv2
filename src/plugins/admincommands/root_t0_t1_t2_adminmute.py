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
t1op_col = db['admin_t1op']
t2op_col = db['admin_t2op']
mute_col = db['mutelist']

matcher = on_command('adminmute')

@matcher.handle()
async def _(bot: Bot, event: GroupMessageEvent, rxmsg: Message = EventMessage()):
    receive_msg = str(rxmsg).strip().split()
    request_qid = str(event.user_id)
    request_grpid = str(event.group_id)

    isrootuser = False
    ist0 = False
    ist1 = False
    ist2 = False
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
    for i in t1op_col.find():
        if request_qid == i['qid']:
            ist1 = True
            break
        else:
            ist1 = False
            pass
    for i in t2op_col.find():
        if request_qid == i['qid']:
            ist2 = True
            break
        else:
            ist2 = False
            pass

    if isrootuser == True or ist0 == True or ist1 == True or ist2 == True:
        if len(receive_msg) == 3:
            try:
                gmt8_time = datetime.datetime.now(tz=pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')
                if receive_msg[1] == 'this':
                    if receive_msg[2] == 'all':
                        mute_grpid = int(request_grpid)
                        if mute_time == 0:
                            bot.set_group_whole_ban(group_id=mute_grpid, enable=True)

                            mute_grpid = str(mute_grpid)
                            mute_col.insert_one({'time' : gmt8_time, 'grp' : mute_grpid, 'qid' : 'all', 'mute_time' : 'enable', 'operator' : request_qid})
                            await matcher.send(MessageSegment.at(request_qid) + '全体禁言成功')
                        else:
                            await matcher.send(MessageSegment.at(request_qid) + '\n' + 
'''
错误：语法错误
示例：
/adminmute [GRPID] [QID] [TIME]
GRPID：
this -> 本群
或指定某群ID
QID：
all -> 全体禁言
或禁言的QID
TIME：
全体禁言下必须留空
单独禁言下留空默认为30分钟
单独禁言下填写此值使用的单位为分钟（建议不要超过43200分钟）
解除禁言此值需要填写0
'''.strip()
                            )
                    else:
                        await matcher.send(MessageSegment.at(request_qid) + '\n' + 
'''
错误：语法错误
示例：
/adminmute [GRPID] [QID] [TIME]
GRPID：
this -> 本群
或指定某群ID
QID：
all -> 全体禁言
或禁言的QID
TIME：
全体禁言下必须留空
单独禁言下留空默认为30分钟
单独禁言下填写此值使用的单位为分钟（建议不要超过43200分钟）
解除禁言此值需要填写0
'''.strip()
                        )
                else:
                    mute_grpid = int(receive_msg[2])
                    if mute_time == 0:
                        bot.set_group_whole_ban(group_id=mute_grpid, enable=True)

                        mute_grpid = str(mute_grpid)
                        mute_col.insert_one({'time' : gmt8_time, 'grp' : mute_grpid, 'qid' : 'all', 'mute_time' : 'enable', 'operator' : request_qid})
                        await matcher.send(MessageSegment.at(request_qid) + '全体禁言成功')
                    else:
                        await matcher.send(MessageSegment.at(request_qid) + '\n' + 
'''
错误：语法错误
示例：
/adminmute [GRPID] [QID] [TIME]
GRPID：
this -> 本群
或指定某群ID
QID：
all -> 全体禁言
或禁言的QID
TIME：
全体禁言下必须留空
单独禁言下留空默认为30分钟
单独禁言下填写此值使用的单位为分钟（建议不要超过43200分钟）
解除禁言此值需要填写0
'''.strip()
                        )
            except:
                await matcher.send(MessageSegment.at(request_qid) + '错误：禁言失败')
        if len(receive_msg) == 4:
            try:
                gmt8_time = datetime.datetime.now(tz=pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')
                if receive_msg[1] == 'this':
                    if receive_msg[2] == 'all':
                        mute_grpid = int(request_grpid)
                        mute_time = int(receive_msg[3])
                        if mute_time == 0:
                            bot.set_group_whole_ban(group_id=mute_grpid, enable=False)

                            mute_grpid = str(mute_grpid)
                            mute_col.insert_one({'time' : gmt8_time, 'grp' : mute_grpid, 'qid' : 'all', 'mute_time' : 'disable', 'operator' : request_qid})
                            await matcher.send(MessageSegment.at(request_qid) + '解除全体禁言成功')
                        else:
                            await matcher.send(MessageSegment.at(request_qid) + '\n' + 
'''
错误：语法错误
示例：
/adminmute [GRPID] [QID] [TIME]
GRPID：
this -> 本群
或指定某群ID
QID：
all -> 全体禁言
或禁言的QID
TIME：
全体禁言下必须留空
单独禁言下留空默认为30分钟
单独禁言下填写此值使用的单位为分钟（建议不要超过43200分钟）
解除禁言此值需要填写0
'''.strip()
                            )
                    else:
                        mute_grpid = int(request_grpid)
                        mute_qid = int(receive_msg[2])
                        mute_time = int(receive_msg[3]) * 60
                        bot.set_group_ban(group_id=mute_grpid, user_id=mute_qid, duration=mute_time)

                        mute_grpid = str(mute_grpid)
                        mute_qid = str(mute_qid)
                        mute_time = str(mute_time)
                        mute_col.insert_one({'time' : gmt8_time, 'grp' : mute_grpid, 'qid' : mute_qid, 'mute_time' : mute_time, 'operator' : request_qid})
                        await matcher.send(MessageSegment.at(request_qid) + '禁言成功')
                else:
                    if receive_msg[2] == 'all':
                        mute_grpid = int(receive_msg[1])
                        mute_time = int(receive_msg[3])
                        if mute_time == 0:
                            bot.set_group_whole_ban(group_id=mute_grpid, enable=False)

                            mute_grpid = str(mute_grpid)
                            mute_col.insert_one({'time' : gmt8_time, 'grp' : mute_grpid, 'qid' : 'all', 'mute_time' : 'disable', 'operator' : request_qid})
                            await matcher.send(MessageSegment.at(request_qid) + '解除全体禁言成功')
                        else:
                            await matcher.send(MessageSegment.at(request_qid) + '\n' + 
'''
错误：语法错误
示例：
/adminmute [GRPID] [QID] [TIME]
GRPID：
this -> 本群
或指定某群ID
QID：
all -> 全体禁言
或禁言的QID
TIME：
全体禁言下必须留空
单独禁言下留空默认为30分钟
单独禁言下填写此值使用的单位为分钟（建议不要超过43200分钟）
解除禁言此值需要填写0
'''.strip()
                            )
                    else:
                        mute_grpid = int(receive_msg[1])
                        mute_qid = int(receive_msg[2])
                        mute_time = int(receive_msg[3]) * 60
                        bot.set_group_ban(group_id=mute_grpid, user_id=mute_qid, duration=mute_time)

                        mute_grpid = str(mute_grpid)
                        mute_qid = str(mute_qid)
                        mute_time = str(mute_time)
                        mute_col.insert_one({'time' : gmt8_time, 'grp' : mute_grpid, 'qid' : mute_qid, 'mute_time' : mute_time, 'operator' : request_qid})
                        await matcher.send(MessageSegment.at(request_qid) + '禁言成功')
            except:
                await matcher.send(MessageSegment.at(request_qid) + '错误：禁言失败')
        else:
            await matcher.send(MessageSegment.at(request_qid) + '\n' + 
'''
示例：
/adminmute [GRPID] [QID] [TIME]
GRPID：
this -> 本群
或指定某群ID
QID：
all -> 全体禁言
或禁言的QID
TIME：
全体禁言下必须留空
单独禁言下留空默认为30分钟
单独禁言下填写此值使用的单位为分钟（建议不要超过43200分钟）
解除禁言此值需要填写0
'''.strip()
            )
    else:
        await matcher.send(MessageSegment.at(request_qid) + '错误：权限不足')
    