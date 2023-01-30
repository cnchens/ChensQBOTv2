from nonebot.plugin.on import on_command
from nonebot.adapters import Message
from nonebot.params import EventMessage
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
import pymongo
import json
import datetime
import pytz

f = open('src/config/chensbot_config.json', 'r', encoding='utf-8')# 读取config
json_res = json.load(f)
mdb_conn = json_res['mdb_conn']# mongodb连接地址

client = pymongo.MongoClient(mdb_conn)# mongodb连接地址
db = client['ChensBOTv2']

config_col = db['cb_config']
rootuser_col = db['admin_rootuser']
t0op_col = db['admin_t0op']
t1op_col = db['admin_t1op']
t2op_col = db['admin_t2op']

for i in config_col.find():
    timezone = i['timezone']
mdbtz_time = datetime.datetime.now(tz=pytz.timezone(timezone)).strftime('%Y-%m-%d %H:%M:%S')

admingiveop = on_command('admingiveop')

@admingiveop.handle()
async def _(event: GroupMessageEvent, rxmsg: Message = EventMessage()):
    receive_msg = str(rxmsg).strip().split()
    request_qid = str(event.user_id)
    request_grpid = str(event.group_id)
    if request_qid in rootuser_col.find_one()['rootuser']:
        if len(receive_msg) == 4:
            try:
                if receive_msg[1] == 'this':
                    op_level = receive_msg[2]
                    qid = receive_msg[3]
                    if op_level == '0':
                        t0op_col.insert_many({'time' : mdbtz_time, 'grp' : request_grpid, 'qid' : qid})
                        await admingiveop.send(f'成功\n时间：{mdbtz_time}\n群组：{request_grpid}\n管理员：{qid}')
                    elif op_level == '1':
                        config_col.update_many({'_id' : '0'}, {'$push' : {'t1_op' : {'qid' : qid, 'grp' : request_grpid}}})
                        await admingiveop.send(f'成功\n群组：{request_grpid}\n管理员：{qid}\n权限等级：{op_level}')
                    elif op_level == '2':
                        config_col.update_many({'_id' : '0'}, {'$push' : {'t2_op' : {'qid' : qid, 'grp' : request_grpid}}})
                        await admingiveop.send(f'成功\n群组：{request_grpid}\n管理员：{qid}\n权限等级：{op_level}')
                    else:
                        await admingiveop.send(
'''
错误：语法错误
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
                    grpid = receive_msg[1]
                    op_level = receive_msg[2]
                    qid = receive_msg[3]
                    if op_level == '0':
                        config_col.update_many({'_id' : '0'}, {'$push' : {'t0_op' : {'qid' : qid, 'grp' : grpid}}})
                        await admingiveop.send(f'成功\n群组：{grpid}\n管理员：{qid}\n权限等级：{op_level}')
                    elif op_level == '1':
                        config_col.update_many({'_id' : '0'}, {'$push' : {'t1_op' : {'qid' : qid, 'grp' : grpid}}})
                        await admingiveop.send(f'成功\n群组：{grpid}\n管理员：{qid}\n权限等级：{op_level}')
                    elif op_level == '2':
                        config_col.update_many({'_id' : '0'}, {'$push' : {'t2_op' : {'qid' : qid, 'grp' : grpid}}})
                        await admingiveop.send(f'成功\n群组：{grpid}\n管理员：{qid}\n权限等级：{op_level}')
                    else:
                        await admingiveop.send(
'''
错误：语法错误
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
            except:
                await admingiveop.send('错误：运行错误')
        else:
            await admingiveop.send(
'''
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
        await admingiveop.send(f'错误：权限不足')

    