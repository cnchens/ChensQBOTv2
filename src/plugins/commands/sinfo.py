from nonebot.plugin.on import on_command
from nonebot.adapters import Message
from nonebot.params import EventMessage
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from urllib.request import Request, urlopen
from urllib.parse import urlencode
import pymongo
import json
import datetime
import pytz

f = open('src/config/chensbot_config.json', 'r', encoding='utf-8')# 读取config
json_res = json.load(f)
mdb_conn = json_res['mdb_conn']# mongodb连接地址

client = pymongo.MongoClient(mdb_conn)# mongodb连接地址
db = client['ChensQBOTv2']
config_col = db['cb_config']

matcher = on_command('sinfo')

# @matcher.handle()
# async def _(event: GroupMessageEvent, rxmsg: Message = EventMessage()):
#     receive_msg = str(rxmsg).strip().split()
#     request_qid = str(event.user_id)
#     request_grpid = str(event.group_id)
# 
#     ua = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.47'}
# 
#     if len(receive_msg) == 2:
#         if receive_msg[1] == 'mc':
#             for i in config_col.find():
#                 if len(i['mcs_edition']) != 0 and len(i['mcs_serverip']) != 0:
#                     mcs_stat = i['mcs_stat']
#                     mcs_edition = i['mcs_edition']
#                     mcs_serverip = i['mcs_serverip']
#             requ = Request(url=url, headers=ua)
#             repo = urlopen(requ).read()
#             brepo_str = repo.decode()
# 
#             gmt8_time = datetime.datetime.now(tz=pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')
# 
#             try:
#                 brepo_dict = json.loads(brepo_str)
#                 online = brepo_dict['online']
#                 version = brepo_dict['version']['name_raw']
#                 online_players = brepo_dict['players']['online']
#                 max_players = brepo_dict['players']['max']
#                 motd = brepo_dict['motd']['raw']
# 
# 
# '''
# 示例：
# /sinfo [SERVER]
# SERVER：
# mc -> 查询当前MC服务器状态（前提是配置好服务器地址）
# '''