from nonebot.adapters.onebot.v11 import Adapter as onebotv11_adapter
import nonebot
import pymongo
import time
import json
import datetime
import pytz

f = open('src/config/chensbot_config.json', 'r', encoding='utf-8')# 读取config
json_res = json.load(f)
mdb_conn = json_res['mdb_conn']# mongodb连接地址

client = pymongo.MongoClient(mdb_conn)# mongodb连接地址
dblist = client.list_database_names()
if 'ChensQBOTv2' not in dblist:# mongodb初始化
    for i in range(5):
        time.sleep(1)
        print('\r', '首次运行，准备创建数据库（注意：请按照提示执行） ' + '{:d}'.format(4-i), end='', flush=True)
    print('\n')

    db = client['ChensQBOTv2']

    gmt8_time = datetime.datetime.now(tz=pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')

    rootuser_col = db['admin_rootuser']
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
    rootuser_dict = {'time' : gmt8_time, 'qid' : rootuser_input}
    rootuser_col.insert_one(rootuser_dict)
    print('已经导入1个集合')

    t0op_col = db['admin_t0op']
    t0op_dict = {'time' : 'x', 'grp' : 'x', 'qid' : 'x'}
    t0op_col.insert_one(t0op_dict)
    print('已经导入2个集合')

    t1op_col = db['admin_t1op']
    t1op_dict = {'time' : 'x', 'grp' : 'x', 'qid' : 'x'}
    t1op_col.insert_one(t1op_dict)
    print('已经导入3个集合')

    t2op_col = db['admin_t2op']
    t2op_dict = {'time' : 'x', 'grp' : 'x', 'qid' : 'x'}
    t2op_col.insert_one(t2op_dict)
    print('已经导入4个集合')

    config_col = db['cb_config']
    version = 'v1.0.0b'
    config_dict = {'version' : version}
    config_col.insert_one(config_dict)
    print('已经导入5个集合')

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
    print('已经导入6个集合')

    mute_col = db['mutelist']
    mute_dict = {'time' : 'x', 'grp' : 'x', 'qid' : 'x', 'mute_time' : 'x', 'operator' : 'x'}
    mute_col.insert_one(mute_dict)
    print('已经导入7个集合')

    kick_col = db['kicklist']
    kick_dict = {'time' : 'x', 'grp' : 'x', 'qid' : 'x', 'reason' : 'x', 'operator' : 'x'}
    kick_col.insert_one(kick_dict)
    print('已经导入8个集合')

    ban_col = db['banlist']
    ban_dict = {'time' : 'x', 'grp' : 'x', 'qid' : 'x', 'reason' : 'x', 'operator' : 'x'}
    ban_col.insert_one(ban_dict)
    print('已经导入9个集合')

    sfz_col = db['sfz']
    f = open('src/static/text/90亿身份证信息.txt', 'r', encoding='GBK', errors='ignore')
    n = '0'
    for i in f:
        n = str(int(n) + 1)
        sfz_dict = {'num' : n, 'info' : i}
        sfz_col.insert_one(sfz_dict)
        print('\r', f'写入密集：此集合已导入{n}条数据', end='', flush=True)
    print('\n已经导入10个集合')

    sf_col = db['sf']
    f = open('src/static/text/十万顺丰快递.txt', 'r', encoding='GBK', errors='ignore')
    n = '0'
    for i in f:
        n = str(int(n) + 1)
        sf_dict = {'num' : n, 'info' : i}
        sf_col.insert_one(sf_dict)
        print('\r', f'写入密集：此集合已导入{n}条数据', end='', flush=True)
    print('\n已经导入11个集合')

    roll_col = db['roll']
    roll_dict = {'time' : 'x', 'roll_code' : 'x', 'uuid' : 'x', 'qid' : 'x'}
    roll_col.insert_one(roll_dict)
    print('已经导入12个集合')

    print('导入完成')

    time.sleep(1)
else:
    for i in range(5):
        time.sleep(1)
        print('\r', '数据库检查通过，准备运行 ' + '{:d}'.format(4-i), end='', flush=True)
    print('\n')

if __name__ == '__main__':
    nonebot.init()

    driver = nonebot.get_driver()
    driver.register_adapter(onebotv11_adapter)

    nonebot.load_plugins(
        'src/plugins/commands', # 指令
        'src/plugins/groupmgmt', # 群管理
        'src/plugins/admincommands/global_admincommands', # 全局管理员指令
        'src/plugins/admincommands/rootuser', # 根用户指令
        'src/plugins/admincommands/t0op', # t0权限管理员指令
        'src/plugins/admincommands/t1op', # t1权限管理员指令
        'src/plugins/admincommands/t2op', # t2权限管理员指令
        # 'src/plugins/test' # 测试
    )

    nonebot.run()