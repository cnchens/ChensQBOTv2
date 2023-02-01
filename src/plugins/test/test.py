from nonebot.plugin.on import on_command
from nonebot.adapters import Message
from nonebot.params import EventMessage
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
import pymongo
import json
import wmi
import psutil
import platform

matcher = on_command('test')

@matcher.handle()
async def _(event: GroupMessageEvent):
    await matcher.send('[CQ:at,qq=349256817]t')

# f = open('src/config/chensbot_config.json', 'r', encoding='utf-8')# 读取config
# json_res = json.load(f)
# mdb_conn = json_res['mdb_conn']# mongodb连接地址
# 
# client = pymongo.MongoClient(mdb_conn)# mongodb连接地址
# db = client['ChensBOTv2']
# 
# config_col = db['cb_config']
# rootuser_col = db['admin_rootuser']
# t0op_col = db['admin_t0op']
# t1op_col = db['admin_t1op']
# t2op_col = db['admin_t2op']
# 
# delcount = str(t0op_col.delete_many({'grp' : '114', 'qid' : '114'}).deleted_count)
# print(type(delcount))

# cpuinfo = wmi.WMI()
# for cpu in cpuinfo.Win32_Processor():# cpu使用
#     cpuname = cpu.Name
#     cpuload = str(cpu.LoadPercentage) + '%'
# cpucore = str(psutil.cpu_count(logical=False))# cpu物理核心
# cpulogcore = str(psutil.cpu_count(logical=True))# cpu逻辑核心
# # 内存使用
# free = str(round(psutil.virtual_memory().free / (1024.0 * 1024.0 * 1024.0), 2))+'GB'
# total = str(round(psutil.virtual_memory().total / (1024.0 * 1024.0 * 1024.0), 2))+'GB'
# # 操作系统
# osinfo = platform.platform()
# cpuinfo = wmi.WMI()
# for cpu in cpuinfo.Win32_Processor():
#     cpuname = cpu.Name
#     cpuload = cpu.LoadPercentage
#     print(cpuload)
#     print("您的CPU已使用:%d%%" % cpu.LoadPercentage)

# import time
# for i in range(15):
#     time.sleep(0.5)
#     print('\r', "{:d}".format(15-i), end='', flush=True)
# 

# f = open('src/config/chensbot_config.json', 'r', encoding='utf-8')# 读取config
# json_res = json.load(f)
# mdb_conn = json_res['mdb_conn']# mongodb连接地址
# 
# client = pymongo.MongoClient(mdb_conn)# mongodb连接地址
# db = client['ChensBOTv2']
# 
# config_col = db['cb_config']
# 
# 
# x = config_col.update_many({'t0_op' : {'qid' : '123', 'grp' : '114'}}, {'$set' : {'t0_op' : {'qid' : '114514', 'grp' : '1919710'}}})
# # test = on_command('test')
# 
# # x = config_col.update_many({'_id' : '0'}, {'$push' : {'t0_op' : {'qid' : '1144', 'grp' : '414'}}})
# print(x.matched_count)
# print(type(x.matched_count))
# print(x.modified_count)
# print(type(x.modified_count))

# for i in config_col.find():
#     for j in i['t0_op']:
#         print(j['qid'])

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