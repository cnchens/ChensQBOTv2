from nonebot.plugin.on import on_command
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
import json
import datetime
import pytz

f = open('src/config/chensbot_config.json', 'r', encoding='utf-8')# 读取config
json_res = json.load(f)
mdb_conn = json_res['mdb_conn']# mongodb连接地址

matcher = on_command('time')

@matcher.handle()
async def _(event: GroupMessageEvent):
    gmt8_time = datetime.datetime.now(tz=pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')
    utc_time = datetime.datetime.now(tz=pytz.timezone('UTC')).strftime('%Y-%m-%d %H:%M:%S')
    await matcher.send(
f'''
当前GMT+8时间：{gmt8_time}
当前UTC时间：{utc_time}
'''.strip()
    )