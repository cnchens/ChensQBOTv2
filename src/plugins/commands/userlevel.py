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

matcher = on_command('userlevel')

@matcher.handle()
async def _(event: GroupMessageEvent):
    request_qid = str(event.user_id)
    request_grpid = str(event.group_id)

    isadmin = False
    for i in rootuser_col.find():
        if request_qid == i['qid']:
            await matcher.send(MessageSegment.at(request_qid) + '你的权限组为：管理员 -> rootuser')
            break
        else:
            isadmin = False
            pass
    for i in t0op_col.find():
        if request_qid == i['qid']:
            if request_grpid == i['grp']:
                await matcher.send(MessageSegment.at(request_qid) + f'你在群{request_grpid}的权限组为：管理员 -> t0')
                break
            else:
                isadmin = False
                pass
        else:
            isadmin = False
            pass
    for i in t1op_col.find():
        if request_qid == i['qid']:
            if request_grpid == i['grp']:
                await matcher.send(MessageSegment.at(request_qid) + f'你在群{request_grpid}的权限组为：管理员 -> t1')
                break
            else:
                isadmin = False
                pass
        else:
            isadmin = False
            pass
    for i in t2op_col.find():
        if request_qid == i['qid']:
            if request_grpid == i['grp']:
                await matcher.send(MessageSegment.at(request_qid) + f'你在群{request_grpid}的权限组为：管理员 -> t2')
                break
            else:
                isadmin = False
                pass
        else:
            isadmin = False
            pass

    if isadmin == True:
        pass
    else:
        await matcher.send(MessageSegment.at(request_qid) + f'你在群{request_grpid}的权限组为：普通用户')