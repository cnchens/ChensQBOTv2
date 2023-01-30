# from nonebot.plugin.on import on_command
# from nonebot.adapters import Message
# from nonebot.params import EventMessage
# from nonebot.adapters.onebot.v11.event import GroupMessageEvent
import pymongo
import json

f = open('src/config/chensbot_config.json', 'r', encoding='utf-8')# 读取config
json_res = json.load(f)
mdb_conn = json_res['mdb_conn']# mongodb连接地址

client = pymongo.MongoClient(mdb_conn)# mongodb连接地址
db = client['ChensBOTv2']

config_col = db['cb_config']

# test = on_command('test')

# config_col.update_many({'_id' : '0'}, {'$push' : {'t0_op' : {'qid' : 'x', 'grp' : 'x'}}})

for i in config_col.find():
    for j in i['t0_op']:
        print(j['qid'])

# @test.handle()
# async def _(event: GroupMessageEvent, rxmsg: Message = EventMessage()):
#     receive_msg = str(rxmsg).strip().split()
#     request_qid = event.user_id
#     request_grpid = str(type(event.group_id))
# 
# 
# 
#     await test.send(
# f'''
# [CQ:at,qq={request_qid}]
# {request_grpid}
# '''.strip()
#     )