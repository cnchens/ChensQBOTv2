from nonebot.plugin.on import on_command
from nonebot.adapters import Message
from nonebot.params import EventMessage
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
import pymongo
import json
import datetime
import pytz
import psutil
import platform
import wmi

f = open('src/config/chensbot_config.json', 'r', encoding='utf-8')# 读取config
json_res = json.load(f)
mdb_conn = json_res['mdb_conn']# mongodb连接地址

client = pymongo.MongoClient(mdb_conn)# mongodb连接地址
db = client['ChensBOTv2']

config_col = db['cb_config']
rootuser_col = db['admin_rootuser']

sysinfo = on_command('sysinfo')

@sysinfo.handle()
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
            mdbtz_time = ''
            for i in config_col.find():
                timezone = i['timezone']
                mdbtz_time = datetime.datetime.now(tz=pytz.timezone(timezone)).strftime('%Y-%m-%d %H:%M:%S')
            cpuinfo = wmi.WMI()
            for cpu in cpuinfo.Win32_Processor():# cpu使用
                cpuname = cpu.Name
                cpuload = str(cpu.LoadPercentage) + '%'
            cpucore = str(psutil.cpu_count(logical=False))# cpu物理核心
            cpulogcore = str(psutil.cpu_count(logical=True))# cpu逻辑核心
            # 内存使用
            free = str(round(psutil.virtual_memory().free / (1024.0 * 1024.0 * 1024.0), 2))+'GB'
            total = str(round(psutil.virtual_memory().total / (1024.0 * 1024.0 * 1024.0), 2))+'GB'
            # 操作系统
            osinfo = platform.platform()
            await sysinfo.send(
f'''
MongoDB设置时区：{timezone}
当前时间：{mdbtz_time}
CPU：{cpuname}
物理核心：{cpucore}
逻辑核心：{cpulogcore}
CPU使用：{cpuload}
总内存：{total}
可用内存：{free}
操作系统：{osinfo}
'''.strip()
            )
        except:
            await sysinfo.send('错误：调用失败')
    else:
        await sysinfo.send('错误：权限不足')