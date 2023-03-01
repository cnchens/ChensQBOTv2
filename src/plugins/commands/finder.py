from nonebot.plugin.on import on_command
from nonebot.adapters import Message
from nonebot.params import EventMessage
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from urllib.request import Request, urlopen
from urllib.parse import urlencode
import pymongo
import json
import ast

f = open('src/config/chensbot_config.json', 'r', encoding='utf-8')# 读取config
json_res = json.load(f)
mdb_conn = json_res['mdb_conn']# mongodb连接地址

client = pymongo.MongoClient(mdb_conn)# mongodb连接地址
db = client['ChensQBOTv2']
prisgk_col = db['private_sgk']

matcher = on_command('finder')

@matcher.handle()
async def _(event: GroupMessageEvent, rxmsg: Message = EventMessage()):
    receive_msg = str(rxmsg).strip().split()
    request_qid = str(event.user_id)
    request_grpid = str(event.group_id)

    if len(receive_msg) == 3:
        ua = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.47'}
        find_mode = receive_msg[1]
        find_data = receive_msg[2]
        send_message = '\n'
        in_prisgk = False

        if receive_msg[1] == 'qid':
            global repo_phone
            # q2p
            try:
                data = {'qq' : receive_msg[2]}
                data = urlencode(data).encode('UTF-8')
                requ = Request(url='https://api.xywlapi.cc/qqapi', data=data, headers=ua)
                repo = urlopen(requ).read()
                brepo_str = repo.decode()
                brepo_dict = ast.literal_eval(brepo_str)
                repo_stat = brepo_dict['status']
                if repo_stat == 200:
                    repo_ph_place = brepo_dict['phonediqu']
                    repo_phone = brepo_dict['phone']
                    send_message = send_message + f'查询内容：{find_mode} -> {find_data}\n手机：{repo_phone}\n手机归属地：{repo_ph_place}'
                    
                    # p2w
                    
                    data = {'phone' : repo_phone}
                    data = urlencode(data).encode('UTF-8')
                    requ = Request(url='https://api.xywlapi.cc/wbphone', data=data, headers=ua)
                    repo = urlopen(requ).read()
                    brepo_str = repo.decode()
                    brepo_dict = ast.literal_eval(brepo_str)
                    repo_stat = brepo_dict['status']
                    if repo_stat == 200:
                        repo_wid = brepo_dict['id']
                        send_message = send_message + f'\n微博：{repo_wid}'
                    else:
                        repo_msg = brepo_dict['message']
                        send_message = send_message + f'\n微博：{repo_msg}'
                else:
                    repo_msg = brepo_dict['message']
                    send_message = send_message + f'查询内容：{find_mode} -> {find_data}\n手机：{repo_msg}\n微博：没有找到'
            except:
                send_message = send_message + f'查询内容：{find_mode} -> {find_data}\n手机：查询失败\n手机归属地：查询失败'
            # q2l
            try:
                data = {'qq' : receive_msg[2]}
                data = urlencode(data).encode('UTF-8')
                requ = Request(url='https://api.xywlapi.cc/qqlol', data=data, headers=ua)
                repo = urlopen(requ).read()
                brepo_str = repo.decode()
                brepo_dict = ast.literal_eval(brepo_str)
                repo_stat = brepo_dict['status']
                if repo_stat == 200:
                    repo_name = brepo_dict['name']
                    repo_daqu = brepo_dict['daqu']
                    send_message = send_message + f'\n王者ID：{repo_name}\n所属区服：{repo_daqu}'
                else:
                    repo_msg = brepo_dict['message']
                    send_message = send_message + f'\n王者ID：{repo_msg}'
            except:
                send_message = send_message + f'\n王者ID：查询失败\n所属区服：查询失败'

            # q2pwd
            try:
                data = {'qq' : receive_msg[1]}
                data = urlencode(data).encode('UTF-8')
                requ = Request(url='https://api.xywlapi.cc/qqlm', data=data, headers=ua)
                repo = urlopen(requ).read()
                brepo_str = repo.decode()
                brepo_dict = ast.literal_eval(brepo_str)

                repo_stat = brepo_dict['status']
                if repo_stat == 200:
                    repo_qqlm = brepo_dict['qqlm']
                    send_message = send_message + f'\nQQ老密：{repo_qqlm}'
                else:
                    repo_msg = brepo_dict['message']
                    send_message = send_message + f'\nQQ老密：{repo_msg}'
            except:
                send_message = send_message + f'\nQQ老密：查询失败'
        
            for i in prisgk_col.find():
                if i['qid'] == receive_msg[2]:
                    up_time = i['time']
                    qid = i['qid']
                    qqlm = i['qqlm']
                    phone = i['phone']
                    phone_location = i['phone_location']
                    weibo = i['weibo']
                    lol = i['lol']
                    real_name = i['real_name']
                    sfz = i['sfz']
                    home_location = i['home_location']
                    col_else = i['else']
                    send_message = send_message + f'\nChensQBOTv2私有库：\n上传时间：{up_time}\nQQ号：{qid}\nQQ老密：{qqlm}\n手机号：{phone}\n手机归属地：{phone_location}\n微博：{weibo}\n王者ID：{lol}\n真实姓名：{real_name}\n身份证：{sfz}\n地址：{home_location}\n其他：{col_else}'
                    in_prisgk = True
                    pass
                else:
                    in_prisgk = False
                    pass

            if in_prisgk == True:
                await matcher.send(MessageSegment.at(request_qid) + send_message)
            else:
                send_message = send_message + '\nChensQBOTv2私有库：没有找到'
                await matcher.send(MessageSegment.at(request_qid) + send_message)

        elif receive_msg[1] == 'wid':
            # w2p
            try:
                data = {'id' : receive_msg[1]}
                data = urlencode(data).encode('UTF-8')
                requ = Request(url='https://api.xywlapi.cc/wbapi', data=data, headers=ua)
                repo = urlopen(requ).read()
                brepo_str = repo.decode()
                brepo_dict = ast.literal_eval(brepo_str)

                repo_stat = brepo_dict['status']
                if repo_stat == 200:
                    repo_phone = brepo_dict['phone']
                    repo_ph_place = brepo_dict['phonediqu']
                    send_message = send_message + f'查询内容：{find_mode} -> {find_data}\n手机：{repo_phone}\n手机归属地：{repo_ph_place}'
                    for i in prisgk_col.find():
                        if i['weibo'] == receive_msg[2]:
                            up_time = i['time']
                            qid = i['qid']
                            qqlm = i['qqlm']
                            phone = i['phone']
                            phone_location = i['phone_location']
                            weibo = i['weibo']
                            lol = i['lol']
                            real_name = i['real_name']
                            sfz = i['sfz']
                            home_location = i['home_location']
                            col_else = i['else']
                            send_message = send_message + f'\nChensQBOTv2私有库：\n上传时间：{up_time}\nQQ号：{qid}\nQQ老密：{qqlm}\n手机号：{phone}\n手机归属地：{phone_location}\n微博：{weibo}\n王者ID：{lol}\n真实姓名：{real_name}\n身份证：{sfz}\n地址：{home_location}\n其他：{col_else}'
                            in_prisgk = True
                            pass
                        else:
                            in_prisgk = False
                            pass
                    if in_prisgk == True:
                        await matcher.send(MessageSegment.at(request_qid) + send_message)
                    else:
                        send_message = send_message + '\nChensQBOTv2私有库：没有找到'
                        await matcher.send(MessageSegment.at(request_qid) + send_message)
                else:
                    repo_msg = brepo_dict['message']
                    send_message = send_message + f'查询内容：{find_mode} -> {find_data}\n手机：{repo_msg}'
                    for i in prisgk_col.find():
                        if i['weibo'] == receive_msg[2]:
                            up_time = i['time']
                            qid = i['qid']
                            qqlm = i['qqlm']
                            phone = i['phone']
                            phone_location = i['phone_location']
                            weibo = i['weibo']
                            lol = i['lol']
                            real_name = i['real_name']
                            sfz = i['sfz']
                            home_location = i['home_location']
                            col_else = i['else']
                            send_message = send_message + f'\nChensQBOTv2私有库：\n上传时间：{up_time}\nQQ号：{qid}\nQQ老密：{qqlm}\n手机号：{phone}\n手机归属地：{phone_location}\n微博：{weibo}\n王者ID：{lol}\n真实姓名：{real_name}\n身份证：{sfz}\n地址：{home_location}\n其他：{col_else}'
                            in_prisgk = True
                            pass
                        else:
                            in_prisgk = False
                            pass
                    if in_prisgk == True:
                        await matcher.send(MessageSegment.at(request_qid) + send_message)
                    else:
                        send_message = send_message + '\nChensQBOTv2私有库：没有找到'
                        await matcher.send(MessageSegment.at(request_qid) + send_message)
            except:
                send_message = send_message + f'查询内容：{find_mode} -> {find_data}\n查询失败'
                await matcher.send(MessageSegment.at(request_qid) + send_message)

        elif receive_msg[1] == 'lol':
            # l2q
            try:
                data = {'name' : receive_msg[1]}
                data = urlencode(data).encode('UTF-8')
                requ = Request(url='https://api.xywlapi.cc/lolname', data=data, headers=ua)
                repo = urlopen(requ).read()
                brepo_str = repo.decode()
                brepo_dict = ast.literal_eval(brepo_str)

                repo_stat = brepo_dict['status']
                if repo_stat == 200:
                    repo_qid = brepo_dict['qq']
                    send_message = send_message + f'查询内容：{find_mode} -> {find_data}\nQQ号：{repo_qid}'
                    for i in prisgk_col.find():
                        if i['lol'] == receive_msg[2]:
                            up_time = i['time']
                            qid = i['qid']
                            qqlm = i['qqlm']
                            phone = i['phone']
                            phone_location = i['phone_location']
                            weibo = i['weibo']
                            lol = i['lol']
                            real_name = i['real_name']
                            sfz = i['sfz']
                            home_location = i['home_location']
                            col_else = i['else']
                            send_message = send_message + f'\nChensQBOTv2私有库：\n上传时间：{up_time}\nQQ号：{qid}\nQQ老密：{qqlm}\n手机号：{phone}\n手机归属地：{phone_location}\n微博：{weibo}\n王者ID：{lol}\n真实姓名：{real_name}\n身份证：{sfz}\n地址：{home_location}\n其他：{col_else}'
                            in_prisgk = True
                            pass
                        else:
                            in_prisgk = False
                            pass
                    if in_prisgk == True:
                        await matcher.send(MessageSegment.at(request_qid) + send_message)
                    else:
                        send_message = send_message + '\nChensQBOTv2私有库：没有找到'
                        await matcher.send(MessageSegment.at(request_qid) + send_message)

                else:
                    repo_msg = brepo_dict['message']
                    send_message = send_message + f'查询内容：{find_mode} -> {find_data}\nQQ号：{repo_msg}'
                    for i in prisgk_col.find():
                        if i['lol'] == receive_msg[2]:
                            up_time = i['time']
                            qid = i['qid']
                            qqlm = i['qqlm']
                            phone = i['phone']
                            phone_location = i['phone_location']
                            weibo = i['weibo']
                            lol = i['lol']
                            real_name = i['real_name']
                            sfz = i['sfz']
                            home_location = i['home_location']
                            col_else = i['else']
                            send_message = send_message + f'\nChensQBOTv2私有库：\n上传时间：{up_time}\nQQ号：{qid}\nQQ老密：{qqlm}\n手机号：{phone}\n手机归属地：{phone_location}\n微博：{weibo}\n王者ID：{lol}\n真实姓名：{real_name}\n身份证：{sfz}\n地址：{home_location}\n其他：{col_else}'
                            in_prisgk = True
                            pass
                        else:
                            in_prisgk = False
                            pass
                    if in_prisgk == True:
                        await matcher.send(MessageSegment.at(request_qid) + send_message)
                    else:
                        send_message = send_message + '\nChensQBOTv2私有库：没有找到'
                        await matcher.send(MessageSegment.at(request_qid) + send_message)
            except:
                send_message = send_message + f'查询内容：{find_mode} -> {find_data}\n查询失败'
                await matcher.send(MessageSegment.at(request_qid) + send_message)

        elif receive_msg[1] == 'ph':
            #     elif receive_msg[0] == 'p2q':
#         ua = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.47'}
#         url = 'https://api.xywlapi.cc/qqphone'
#         data = {'phone' : receive_msg[1]}
#         data = urlencode(data).encode('UTF-8')
#         requ = Request(url=url, data=data, headers=ua)
#         repo = urlopen(requ).read()
#         brepo_str = repo.decode()
#         brepo_dict = ast.literal_eval(brepo_str)
# 
#         repo_stat = brepo_dict['status']
#         if repo_stat == 200:
#             repo_msg = brepo_dict['message']
#             repo_qid = brepo_dict['qq']
#             repo_phone = receive_msg[1]
#             repo_ph_place = brepo_dict['phonediqu']
#             send_message = f'[CQ:at,qq={req_qid}]finder StatusCode：{repo_stat} {repo_msg}\n查询手机：{repo_phone}\n绑定qid：{repo_qid}\n归属地：{repo_ph_place}'
#             await session.send(send_message)
#         else:
#             repo_msg = brepo_dict['message']
#             send_message = f'[CQ:at,qq={req_qid}]finder StatusCode：{repo_stat} {repo_msg}'
#             await session.send(send_message)
# 
#     elif receive_msg[0] == 'l2q':
#         ua = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.47'}
#     
            await matcher.send(MessageSegment.at(request_qid) + '暂时停用')
        elif receive_msg[1] == 'cqsgk':
            for i in prisgk_col.find():
                await matcher.send(MessageSegment.at(request_qid) + '维护')
        else:
            await matcher.send(MessageSegment.at(request_qid) + '\n' + 
'''
示例：
/finder [MODE] [INFO]
MODE：
qid -> 通过QQ号查询信息
wid -> 通过微博号查询信息
lol -> 通过王者ID查询信息
ph -> 通过手机号查询信息
cqsgk -> 查询ChensQBOTv2私有库
INFO：
要查询的信息
'''.strip()
            )
    else:
        await matcher.send(MessageSegment.at(request_qid) + '\n' + 
'''
示例：
/finder [MODE] [INFO]
MODE：
qid -> 通过QQ号查询信息
wid -> 通过微博号查询信息
lol -> 通过王者ID查询信息
ph -> 通过手机号查询信息
cqsgk -> 查询ChensQBOTv2私有库
INFO：
要查询的信息
'''.strip()
        )
    
    
