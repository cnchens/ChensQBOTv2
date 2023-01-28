import nonebot
import pymongo
import time
import json

f = open('chensbot_config.json', 'r', encoding='utf-8')# 读取config
json_res = json.load(f)
mdb_conn = json_res['mdb_conn']# mongodb连接地址

client = pymongo.MongoClient(mdb_conn)# mongodb连接地址
dblist = client.list_database_names()
if 'ChensBOTv2' not in dblist:
    print('首次运行，准备创建数据库（注意：请按照提示执行）')
    print('三秒后开始导入，请等待提示导入完成')
    time.sleep(3)
    
    db = client['ChensBOTv2']

    kick_col = db['cb_config']

    isint = False
    rootuser_input = 0
    while isint == False:
        rootuser_input = input('请输入根用户QQ号码（此用户将获得最高权限，请知悉）')
        try:
            rootuser_input = int(rootuser_input)
            isint = True
            break
        except:
            print('请输入正确的QQ号')
            isint = False
            continue
    
    rootuser_input = str(rootuser_input)

    version = 'v1.0.0b'

    kick_dict = {'version' : version, 'rootuser' : [rootuser_input], 't0_op' : [], 't1_op' : [], 't2_op' : []}
    kick_col.insert_one(kick_dict)
    print('导入1/8')

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
    print('导入2/8')

    mute_col = db['mutelist']
    mute_dict = {'time' : 'x', 'grp' : 'x', 'qid' : 'x', 'mute_time' : 'x', 'performer' : 'x'}
    mute_col.insert_one(kick_dict)
    print('导入3/8')

    kick_col = db['kicklist']
    kick_dict = {'time' : 'x', 'grp' : 'x', 'qid' : 'x', 'reason' : 'x', 'performer' : 'x'}
    kick_col.insert_one(kick_dict)
    print('导入4/8')

    ban_col = db['banlist']
    ban_dict = {'time' : 'x', 'grp' : 'x', 'qid' : 'x', 'reason' : 'x', 'performer' : 'x'}
    ban_col.insert_one(ban_dict)
    print('导入5/8')

    sfz_col = db['sfz']
    f = open('src/static/text/90亿身份证信息.txt', 'r', encoding='GBK', errors='ignore')
    n = '0'
    for i in f:
        n = str(int(n) + 1)
        sfz_dict = {'num' : n, 'info' : i}
        sfz_col.insert_one(sfz_dict)
    print('导入6/8')

    sf_col = db['sf']
    f = open('src/static/text/十万顺丰快递.txt', 'r', encoding='GBK', errors='ignore')
    n = '0'
    for i in f:
        n = str(int(n) + 1)
        sf_dict = {'num' : n, 'info' : i}
        sf_col.insert_one(sf_dict)
    print('导入7/8')

    roll_col = db['roll']
    roll_dict = {'time' : 'x', 'roll_code' : 'x', 'uuid' : 'x', 'qid' : 'x'}
    roll_col.insert_one(roll_dict)
    print('导入8/8')

    print('导入完成')
else:
    print('数据库检查通过，准备运行')
    time.sleep(3)

nonebot.init()
nonebot.load_all_plugins(['src/plugins'])
app = nonebot.get_asgi()
nonebot.run()