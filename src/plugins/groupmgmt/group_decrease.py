from nonebot.plugin.on import on_notice
from nonebot.adapters.onebot.v11.event import GroupDecreaseNoticeEvent
import pymongo
import json

f = open('src/config/chensbot_config.json', 'r', encoding='utf-8')# 读取config
json_res = json.load(f)
mdb_conn = json_res['mdb_conn']# mongodb连接地址

client = pymongo.MongoClient(mdb_conn)# mongodb连接地址
db = client['ChensQBOTv2']

grp_col = db['grp_members']

matcher = on_notice()

@matcher.handle()
async def _(event: GroupDecreaseNoticeEvent):
    request_grpid = str(event.group_id)
    operator_qid = str(event.operator_id)
    decrease_type = event.sub_type

    try:
        for i in grp_col.find():
            if operator_qid in i['qid']:
                db_qid = i['qid']
                db_grp = i['grp']
                up_qid = {'grp' : db_grp, 'qid' : db_qid}
                up_stat = {'$set' : {'status' : decrease_type}}
                grp_col.update_many(up_qid, up_stat)
                pass
            else:
                pass
    except:
        grp_col.insert_one(
            {
                'join_time' : 'x', 
                'grp' : request_grpid, 
                'status' : decrease_type, 
                'qid' : operator_qid, 
                'qqlm' : 'x', 
                'phone' : 'x',
                'phone_location' : 'x', 
                'weibo' : 'x', 
                'lol' : 'x', 
                'real_name' : 'x', 
                'sfz' : 'x', 
                'home_location' : 'x', 
                'else' : 'x'
            }
        )