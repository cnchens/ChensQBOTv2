from nonebot.plugin.on import on_notice
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.adapters.onebot.v11.event import GroupIncreaseNoticeEvent
from nonebot.adapters.onebot.v11.bot import Bot
from urllib.request import Request, urlopen
from urllib.parse import urlencode
import pymongo
import json
import time
import datetime
import pytz
import ast

f = open('src/config/chensbot_config.json', 'r', encoding='utf-8')# 读取config
json_res = json.load(f)
mdb_conn = json_res['mdb_conn']# mongodb连接地址

client = pymongo.MongoClient(mdb_conn)# mongodb连接地址
db = client['ChensQBOTv2']

ban_col = db['banlist']
kick_col = db['kicklist']
grp_col = db['grp_members']

matcher = on_notice()

@matcher.handle()
async def _(event: GroupIncreaseNoticeEvent, bot: Bot):
    request_qid = str(event.user_id)
    request_grpid = str(event.group_id)

    # 全局变量 防止报错
    kicked = False
    ban_col_findout = {}

    # 联合封禁
    for i in ban_col.find():
        if request_qid in i['qid']:
            ban_col_findout = i
            pass
        else:
            pass
    
    if len(ban_col_findout) != 0:
        ban_reason = ban_col_findout['reason']
        ban_time = ban_col_findout['time']
        ban_grp = ban_col_findout['grp']
        await matcher.send(MessageSegment.at(request_qid) + f'联合封禁：您已经被封禁，如有疑问请联系该群群主或群管理员！\n最后一次封禁于：{ban_time}\n封禁群组：{ban_grp}\n封禁原因：{ban_reason}')
        kick_grpid = event.group_id
        kick_qid = event.user_id
        time.sleep(1)
        await bot.set_group_kick(group_id=kick_grpid, user_id=kick_qid)

        gmt8_time = datetime.datetime.now(tz=pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')

        kick_grpid = str(kick_grpid)
        kick_qid = str(kick_qid)
        kick_col.insert_one(
            {
                'time' : gmt8_time, 
                'grp' : kick_grpid, 
                'qid' : kick_qid, 
                'reason' : '联合封禁自动踢出', 
                'operator' : 'BOT'
            }
        )

        kicked = True
    else:
        kicked = False
        pass

    # 入群欢迎
    if kicked == True:
        pass
    else:
        await matcher.send(MessageSegment.at(request_qid) + '欢迎入群，进群看公告')
