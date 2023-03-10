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
    finder_qid = request_qid

    
    try:
        global repo_phone, repo_ph_place
        ua = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.47'}
        url = 'https://api.xywlapi.cc/qqapi'
        data = {'qq' : finder_qid}
        data = urlencode(data).encode('UTF-8')
        requ = Request(url=url, data=data, headers=ua)

        repo = urlopen(requ).read()
        brepo_str = repo.decode()
        brepo_dict = ast.literal_eval(brepo_str)
        repo_stat = brepo_dict['status']
        if repo_stat == 200:
            repo_phone = brepo_dict['phone']
            repo_ph_place = brepo_dict['phonediqu']
        else:
            repo_phone = '没有找到'
            repo_ph_place = '没有找到'
    except:
        repo_phone = '获取失败'
        repo_ph_place = '获取失败'

    try:
        global repo_wid
        ua = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.47'}
        url = 'https://api.xywlapi.cc/qqapi'
        data = {'qq' : finder_qid}
        data = urlencode(data).encode('UTF-8')
        requ = Request(url=url, data=data, headers=ua)

        repo = urlopen(requ).read()
        brepo_str = repo.decode()
        brepo_dict = ast.literal_eval(brepo_str)
        repo_stat = brepo_dict['status']
        if repo_stat == 200:
            repo_phone = brepo_dict['phone']
            repo_ph_place = brepo_dict['phonediqu']
            ua = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.47'}
            url = 'https://api.xywlapi.cc/wbphone'
            data = {'phone' : repo_phone}
            data = urlencode(data).encode('UTF-8')
            requ = Request(url=url, data=data, headers=ua)
            repo = urlopen(requ).read()
            brepo_str = repo.decode()
            brepo_dict = ast.literal_eval(brepo_str)
            repo_stat = brepo_dict['status']
            if repo_stat == 200:
                repo_wid = brepo_dict['id']
            else:
                repo_wid = '没有找到'
        else:
            repo_wid = '没有找到'
    except:
        repo_wid = '获取失败'

    try:
        global repo_lol
        ua = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.47'}
        url = 'https://api.xywlapi.cc/qqlol'
        data = {'qq' : finder_qid}
        data = urlencode(data).encode('UTF-8')
        requ = Request(url=url, data=data, headers=ua)

        repo = urlopen(requ).read()
        brepo_str = repo.decode()
        brepo_dict = ast.literal_eval(brepo_str)
        repo_stat = brepo_dict['status']
        if repo_stat == 200:
            repo_lol_name = brepo_dict['name']
            repo_daqu = brepo_dict['daqu']
            repo_lol = repo_lol_name + repo_daqu
        else:
            repo_lol = '没有找到'
    except:
        repo_lol = '获取失败'

    try:
        global repo_qqlm
        ua = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.47'}
        url = 'https://api.xywlapi.cc/qqlm'
        data = {'qq' : finder_qid}
        data = urlencode(data).encode('UTF-8')
        requ = Request(url=url, data=data, headers=ua)

        repo = urlopen(requ).read()
        brepo_str = repo.decode()
        brepo_dict = ast.literal_eval(brepo_str)
        repo_stat = brepo_dict['status']
        if repo_stat == 200:
            repo_qqlm = brepo_dict['qqlm']
        else:
            repo_qqlm = '没有找到'
    except:
        repo_qqlm = '获取失败'

    gmt8_time = datetime.datetime.now(tz=pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')

    add_dict = {
        'join_time' : gmt8_time, 
        'grp' : request_grpid, 
        'status' : 'in_grp', 
        'qid' : request_qid, 
        'qqlm' : repo_qqlm, 
        'phone' : repo_phone,
        'phone_location' : repo_ph_place, 
        'weibo' : repo_wid, 
        'lol' : repo_lol, 
        'real_name' : '无', 
        'sfz' : '无', 
        'home_location' : '无', 
        'else' : '无'
    }

    grp_col.insert_one(add_dict)