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

matcher = on_command('finder')

@matcher.handle()
async def _(event: GroupMessageEvent, rxmsg: Message = EventMessage()):
    receive_msg = str(rxmsg).strip().split()
    request_qid = str(event.user_id)
    request_grpid = str(event.group_id)
    await matcher.send(MessageSegment.at(request_qid) + '未开放')

    if len(receive_msg) == 3:
        if receive_msg[1] == 'qid':
            ua = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.47'}
            q2p_url = 'https://api.xywlapi.cc/qqapi'
            q2p_data = {'qq' : receive_msg[2]}
            data = urlencode(data).encode('UTF-8')
            requ = Request(url=url, data=data, headers=ua)
            repo = urlopen(requ).read()
            brepo_str = repo.decode()
            brepo_dict = ast.literal_eval(brepo_str)

            p2q_url = 'https://api.xywlapi.cc/qqphone'
            p2q_data = {'phone' : receive_msg[2]}



    if receive_msg[0] == 'q2p':
        ua = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.47'}
        url = 'https://api.xywlapi.cc/qqapi'
        data = {'qq' : receive_msg[1]}
        data = urlencode(data).encode('UTF-8')
        requ = Request(url=url, data=data, headers=ua)
        repo = urlopen(requ).read()
        brepo_str = repo.decode()
        brepo_dict = ast.literal_eval(brepo_str)

        repo_stat = brepo_dict['status']
        if repo_stat == 200:
            repo_msg = brepo_dict['message']
            repo_qid = brepo_dict['qq']
            repo_phone = brepo_dict['phone']
            repo_ph_place = brepo_dict['phonediqu']
            send_message = f'[CQ:at,qq={req_qid}]finder StatusCode：{repo_stat} {repo_msg}\n查询qid：{repo_qid}\n绑定手机：{repo_phone}\n归属地：{repo_ph_place}'
            await session.send(send_message)
        else:
            repo_msg = brepo_dict['message']
            send_message = f'[CQ:at,qq={req_qid}]finder StatusCode：{repo_stat} {repo_msg}'
            await session.send(send_message)

    elif receive_msg[0] == 'p2q':
        ua = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.47'}
        url = 'https://api.xywlapi.cc/qqphone'
        data = {'phone' : receive_msg[1]}
        data = urlencode(data).encode('UTF-8')
        requ = Request(url=url, data=data, headers=ua)
        repo = urlopen(requ).read()
        brepo_str = repo.decode()
        brepo_dict = ast.literal_eval(brepo_str)

        repo_stat = brepo_dict['status']
        if repo_stat == 200:
            repo_msg = brepo_dict['message']
            repo_qid = brepo_dict['qq']
            repo_phone = receive_msg[1]
            repo_ph_place = brepo_dict['phonediqu']
            send_message = f'[CQ:at,qq={req_qid}]finder StatusCode：{repo_stat} {repo_msg}\n查询手机：{repo_phone}\n绑定qid：{repo_qid}\n归属地：{repo_ph_place}'
            await session.send(send_message)
        else:
            repo_msg = brepo_dict['message']
            send_message = f'[CQ:at,qq={req_qid}]finder StatusCode：{repo_stat} {repo_msg}'
            await session.send(send_message)

    elif receive_msg[0] == 'q2l':
        ua = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.47'}
        url = 'https://api.xywlapi.cc/qqlol'
        data = {'qq' : receive_msg[1]}
        data = urlencode(data).encode('UTF-8')
        requ = Request(url=url, data=data, headers=ua)
        repo = urlopen(requ).read()
        brepo_str = repo.decode()
        brepo_dict = ast.literal_eval(brepo_str)

        repo_stat = brepo_dict['status']
        if repo_stat == 200:
            repo_msg = brepo_dict['message']
            repo_qid = brepo_dict['qq']
            repo_name = brepo_dict['name']
            repo_daqu = brepo_dict['daqu']
            send_message = f'[CQ:at,qq={req_qid}]finder StatusCode：{repo_stat} {repo_msg}\n查询qid：{repo_qid}\n游戏名：{repo_name}\n服务器：{repo_daqu}'
            await session.send(send_message)
        else:
            repo_msg = brepo_dict['message']
            send_message = f'[CQ:at,qq={req_qid}]finder StatusCode：{repo_stat} {repo_msg}'
            await session.send(send_message)

    elif receive_msg[0] == 'l2q':
        ua = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.47'}
        url = 'https://api.xywlapi.cc/lolname'
        data = {'name' : receive_msg[1]}
        data = urlencode(data).encode('UTF-8')
        requ = Request(url=url, data=data, headers=ua)
        repo = urlopen(requ).read()
        brepo_str = repo.decode()
        brepo_dict = ast.literal_eval(brepo_str)

        repo_stat = brepo_dict['status']
        if repo_stat == 200:
            repo_msg = brepo_dict['message']
            repo_qid = brepo_dict['qq']
            repo_name = brepo_dict['name']
            repo_daqu = brepo_dict['daqu']
            send_message = f'[CQ:at,qq={req_qid}]finder StatusCode：{repo_stat} {repo_msg}\n查询游戏名：{repo_name}\n服务器：{repo_daqu}\n绑定qid：{repo_qid}'
            await session.send(send_message)
        else:
            repo_msg = brepo_dict['message']
            send_message = f'[CQ:at,qq={req_qid}]finder StatusCode：{repo_stat} {repo_msg}'
            await session.send(send_message)

    elif receive_msg[0] == 'q2pwd':
        ua = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.47'}
        url = 'https://api.xywlapi.cc/qqlm'
        data = {'qq' : receive_msg[1]}
        data = urlencode(data).encode('UTF-8')
        requ = Request(url=url, data=data, headers=ua)
        repo = urlopen(requ).read()
        brepo_str = repo.decode()
        brepo_dict = ast.literal_eval(brepo_str)

        repo_stat = brepo_dict['status']
        if repo_stat == 200:
            repo_msg = brepo_dict['message']
            repo_qid = brepo_dict['qq']
            repo_qqlm = brepo_dict['qqlm']
            send_message = f'[CQ:at,qq={req_qid}]finder StatusCode：{repo_stat} {repo_msg}\n查询qid：{repo_qid}\nlm_id：{repo_qqlm}'
            await session.send(send_message)
        else:
            repo_msg = brepo_dict['message']
            send_message = f'[CQ:at,qq={req_qid}]finder StatusCode：{repo_stat} {repo_msg}'
            await session.send(send_message)

    elif receive_msg[0] == 'w2p':
        ua = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.47'}
        url = 'https://api.xywlapi.cc/wbapi'
        data = {'id' : receive_msg[1]}
        data = urlencode(data).encode('UTF-8')
        requ = Request(url=url, data=data, headers=ua)
        repo = urlopen(requ).read()
        brepo_str = repo.decode()
        brepo_dict = ast.literal_eval(brepo_str)

        repo_stat = brepo_dict['status']
        if repo_stat == 200:
            repo_msg = brepo_dict['message']
            wid = receive_msg[1]
            repo_phone = brepo_dict['phone']
            repo_ph_place = brepo_dict['phonediqu']
            send_message = f'[CQ:at,qq={req_qid}]finder StatusCode：{repo_stat} {repo_msg}\n查询微博id：{wid}\n绑定手机：{repo_phone}\n归属地：{repo_ph_place}'
            await session.send(send_message)
        else:
            repo_msg = brepo_dict['message']
            send_message = f'[CQ:at,qq={req_qid}]finder StatusCode：{repo_stat} {repo_msg}'
            await session.send(send_message)

    elif receive_msg[0] == 'p2w':
        ua = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.47'}
        url = 'https://api.xywlapi.cc/wbphone'
        data = {'phone' : receive_msg[1]}
        data = urlencode(data).encode('UTF-8')
        requ = Request(url=url, data=data, headers=ua)
        repo = urlopen(requ).read()
        brepo_str = repo.decode()
        brepo_dict = ast.literal_eval(brepo_str)

        repo_stat = brepo_dict['status']
        if repo_stat == 200:
            repo_msg = brepo_dict['message']
            phone = receive_msg[1]
            repo_wid = brepo_dict['id']
            repo_ph_place = brepo_dict['phonediqu']
            send_message = f'[CQ:at,qq={req_qid}]finder StatusCode：{repo_stat} {repo_msg}\n查询手机：{phone}\n绑定微博id：{repo_wid}\n归属地：{repo_ph_place}'
            await session.send(send_message)
        else:
            repo_msg = brepo_dict['message']
            send_message = f'[CQ:at,qq={req_qid}]finder StatusCode：{repo_stat} {repo_msg}'
            await session.send(send_message)

    elif receive_msg[0] == 'sms':
        await session.send('停用')
        # client = pymongo.MongoClient('mongodb://192.168.1.114:27017/')
        # dblist = client.list_database_names()
        # db = client['QBOT_DB']
        # col = db['sms_bomber_url']

    else:
    
'''
示例：
/finder [MODE] [INFO]
MODE：
qid -> 通过QQ号查询信息
wid -> 通过微博号查询信息
lol -> 通过王者ID查询信息
ph -> 通过手机号查询信息
INFO：
要查询的信息
'''