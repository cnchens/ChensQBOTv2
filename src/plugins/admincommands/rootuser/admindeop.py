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
db = client['ChensQBOTv2']

config_col = db['cb_config']
rootuser_col = db['admin_rootuser']
t0op_col = db['admin_t0op']
t1op_col = db['admin_t1op']
t2op_col = db['admin_t2op']

matcher = on_command('admindeop')

@matcher.handle()
async def _(event: GroupMessageEvent, rxmsg: Message = EventMessage()):
    receive_msg = str(rxmsg).strip().split()
    request_qid = str(event.user_id)
    request_grpid = str(event.group_id)
    isrootuser = False
    for i in rootuser_col.find():
        if request_qid == i['qid']:
            isrootuser = True
            break
        else:
            isrootuser = False
            pass
    if isrootuser == True:
        if len(receive_msg) == 3:
            try:
                if receive_msg[1] == 'this':
                    qid = receive_msg[2]
                    delcount_t0 = t0op_col.delete_many({'grp' : request_grpid, 'qid' : qid}).deleted_count
                    delcount_t1 = t1op_col.delete_many({'grp' : request_grpid, 'qid' : qid}).deleted_count
                    delcount_t2 = t2op_col.delete_many({'grp' : request_grpid, 'qid' : qid}).deleted_count
                    delcount = str(delcount_t0 + delcount_t1 + delcount_t2)
                    await matcher.send(f'群组：{request_grpid}\n管理员：{qid}\n找到了{delcount}个符合的数据')
                else:
                    grpid = receive_msg[1]
                    qid = receive_msg[3]
                    delcount_t0 = t0op_col.delete_many({'grp' : grpid, 'qid' : qid}).deleted_count
                    delcount_t1 = t1op_col.delete_many({'grp' : grpid, 'qid' : qid}).deleted_count
                    delcount_t2 = t2op_col.delete_many({'grp' : grpid, 'qid' : qid}).deleted_count
                    delcount = str(delcount_t0 + delcount_t1 + delcount_t2)
                    await matcher.send(f'群组：{grpid}\n管理员：{qid}\n找到了{delcount}个符合的数据')
            except:
                await matcher.send('错误：运行错误')
        else:
            await matcher.send(
'''
示例：
/admindeop [GRPID] [QID]
GRPID：
this -> 本群
或指定某群ID
QID：
删除OP权限的QID
'''.strip()
            )
    else:
        await matcher.send(f'错误：权限不足')

    