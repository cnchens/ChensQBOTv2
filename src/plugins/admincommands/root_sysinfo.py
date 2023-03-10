from nonebot.plugin.on import on_command
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
import pymongo
import json
import datetime
import pytz
import psutil
import platform
import wmi
import time

f = open('src/config/chensbot_config.json', 'r', encoding='utf-8')# 读取config
json_res = json.load(f)
mdb_conn = json_res['mdb_conn']# mongodb连接地址

client = pymongo.MongoClient(mdb_conn)# mongodb连接地址
db = client['ChensQBOTv2']

rootuser_col = db['admin_rootuser']

matcher = on_command('sysinfo')

@matcher.handle()
async def _(event: GroupMessageEvent):
    request_qid = str(event.user_id)
    isrootuser = False
    for i in rootuser_col.find():# 判定是否为rootuser
        if i['qid'] == request_qid:
            isrootuser = True
            break
        else:
            isrootuser = False
            pass
    if isrootuser == True:
        try:
            ostime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            cpuinfo = wmi.WMI()
            for cpu in cpuinfo.Win32_Processor():# cpu使用
                cpuname = cpu.Name
                cpuload = str(cpu.LoadPercentage) + '%'
            cpucore = str(psutil.cpu_count(logical=False))# cpu物理核心
            cpulogcore = str(psutil.cpu_count(logical=True))# cpu逻辑核心
            # 内存使用
            used = str(round(psutil.virtual_memory().used / (1024.0 * 1024.0 * 1024.0), 2))
            total = str(round(psutil.virtual_memory().total / (1024.0 * 1024.0 * 1024.0), 2))
            # 操作系统
            osinfo = platform.platform()
            await matcher.send(MessageSegment.at(request_qid) + '\n' + 
f'''
CPU：{cpuname}
CPU核心：{cpucore}C{cpulogcore}T
CPU使用：{cpuload}
内存：{used}/{total}GB
操作系统：{osinfo}
系统时间：{ostime}
'''.strip()
            )
        except:
            await matcher.send(MessageSegment.at(request_qid) + '错误：调用失败\n请前往 https://github.com/cnchens/ChensQBOTv2/ 提交issue报告')
    else:
        await matcher.send(MessageSegment.at(request_qid) + '错误：权限不足')