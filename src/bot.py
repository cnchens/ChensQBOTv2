import os
import nonebot
import config
import pymongo
import time
import json

f = open('config.json', 'r', encoding='utf-8')# 读取config
json_res = json.load(f)
mdb_conn = json_res['mdb_conn']# mongodb连接地址

client = pymongo.MongoClient(mdb_conn)# mongodb连接地址
dblist = client.list_database_names()
if 'BANBOT' not in dblist:
    print('首次运行，准备创建数据库')
    print('三秒后开始导入，请等待提示导入完成')
    time.sleep(3)
    
    db = client['ChensBOTv2']

    grpmembers_col = db['grp_members']
    grpmembers_dict = {
                'join_time' : 'x', 
                'grp' : 'x', 
                'status' : 'x', 
                'qid' : 'x', 
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
    grpmembers_col.insert_one(grpmembers_dict)
    print('导入1/3')

    kick_col = db['kicklist']
    kick_dict = {'kick_time' : 'x', 'kick_grp' : 'x', 'kick_qid' : 'x', 'kick_reason' : 'x', 'performer' : 'x'}
    kick_col.insert_one(kick_dict)
    print('导入2/3')

    ban_col = db['banlist']
    ban_dict = {'ban_time' : 'x', 'ban_grp' : 'x', 'ban_qid' : 'x', 'ban_reason' : 'x', 'performer' : 'x'}
    ban_col.insert_one(ban_dict)
    print('导入3/3')

    print('导入完成')
else:
    print('数据库检查通过，准备运行')
    time.sleep(3)

if __name__ == '__main__':
    nonebot.init()

    nonebot.load_plugins(
        os.path.join(os.path.dirname(__file__), 'src', 'plugins'),
        'src.plugins'
    )
    
    nonebot.run()