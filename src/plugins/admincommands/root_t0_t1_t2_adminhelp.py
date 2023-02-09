from nonebot.plugin.on import on_command
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
import pymongo
import json

f = open('src/config/chensbot_config.json', 'r', encoding='utf-8')# 读取config
json_res = json.load(f)
mdb_conn = json_res['mdb_conn']# mongodb连接地址

client = pymongo.MongoClient(mdb_conn)# mongodb连接地址
db = client['ChensQBOTv2']

rootuser_col = db['admin_rootuser']
t0op_col = db['admin_t0op']
t1op_col = db['admin_t1op']
t2op_col = db['admin_t2op']

matcher = on_command('help')

@matcher.handle()
async def _(event: GroupMessageEvent):
    request_qid = str(event.user_id)

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
        await matcher.send(MessageSegment.at(request_qid) + '\n' + 
'''
管理员命令使用帮助：
/adminhelp      显示本帮助  root，t0，t1，t2
/admingiveop    给予op权限  root
/admindeop      卸载op权限  root
/sysinfo        系统信息    root
/adminban       用户封禁    root，t0
/adminkick      用户踢出    root，t0，t1
/adminmute      用户禁言    root，t0，t1，t2
'''.strip()    
        )
    else:
        await matcher.send(MessageSegment.at(request_qid) + '错误：权限不足')
