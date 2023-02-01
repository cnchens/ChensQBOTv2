from nonebot.plugin.on import on_notice
from nonebot.adapters.onebot.v11.event import GroupIncreaseNoticeEvent
import pymongo
import json
import time
import datetime
import pytz

f = open('src/config/chensbot_config.json', 'r', encoding='utf-8')# 读取config
json_res = json.load(f)
mdb_conn = json_res['mdb_conn']# mongodb连接地址

client = pymongo.MongoClient(mdb_conn)# mongodb连接地址
db = client['ChensQBOTv2']

ban_col = db['banlist']
kick_col = db['kicklist']

matcher = on_notice()

@matcher.handle()
async def _(event: GroupIncreaseNoticeEvent):
    request_qid = str(event.user_id)
    request_grpid = str(event.group_id)

    # global_variable
    kicked = False
    ban_col_findout = {}

    # ban_kick
    for i in ban_col.find():
        if at_qid in i['ban_qid']:
            ban_col_findout = i
            pass
        else:
            pass
    
    if len(ban_col_findout) != 0:
        ban_reason = ban_col_findout['ban_reason']
        ban_time = ban_col_findout['ban_time']
        await matcher.send(f'BANBOT联合封禁：您已经被封禁，如有疑问请联系该群群主或群管理员！\n最后一次封禁于{ban_time}\n封禁原因：{ban_reason}')
        kick_grpid = matcher.event.group_id
        kick_qid = matcher.event.user_id
        time.sleep(1)
        await bot.set_group_kick(group_id=kick_grpid, user_id=kick_qid)

        gmt8 = 'Asia/Shanghai'
        gmt8_time = datetime.datetime.now(tz=pytz.timezone(gmt8)).strftime('%Y-%m-%d %H:%M:%S')

        kick_grpid = str(kick_grpid)
        kick_qid = str(kick_qid)
        up_dict = {
            'kick_time' : gmt8_time, 
            'kick_grp' : kick_grpid, 
            'kick_qid' : kick_qid, 
            'kick_reason' : 'Automatic Kick by banlist', 
            'performer' : 'BOT'
        }

        kick_col.insert_one(up_dict)

        kicked = True
    else:
        kicked = False
        pass

    at_qid = str(matcher.event.user_id)
    join_grp = str(matcher.event.group_id)
    
    # akt外群去重
    for i in grp_col.find():
        if at_qid in i['qid']:
            for j in cannot_enter_grp:
                if join_grp in j:
                    if i['status'] == 'in_grp':
                        await matcher.send(f'BANBOT自动踢出\n[CQ:at,qq={at_qid}]您已添加过其他群，请勿重复添加，占用资源！')

                        kick_grpid = matcher.event.group_id
                        kick_qid = matcher.event.user_id
                        time.sleep(1)

                        gmt8 = 'Asia/Shanghai'
                        gmt8_time = datetime.datetime.now(tz=pytz.timezone(gmt8)).strftime('%Y-%m-%d %H:%M:%S')
                        
                        kick_grpid = str(matcher.event.group_id)
                        kick_qid = str(matcher.event.user_id)

                        up_dict = {
                            'ban_time' : gmt8_time, 
                            'ban_grp' : kick_grpid, 
                            'ban_qid' : kick_qid, 
                            'ban_reason' : '您已添加过其他群，请勿重复添加，占用资源！[code00001]', 
                            'performer' : 'BOT'
                        }

                        ban_col.insert_one(up_dict)

                        
                        await bot.set_group_kick(group_id=kick_grpid, user_id=kick_qid)

                        gmt8 = 'Asia/Shanghai'
                        gmt8_time = datetime.datetime.now(tz=pytz.timezone(gmt8)).strftime('%Y-%m-%d %H:%M:%S')

                        kicked = True
                        break
                    else:
                        kicked = False
                        pass
                else:
                    kicked = False
                    pass

    grpid = str(matcher.event.group_id)
    at_qid = str(matcher.event.user_id)

    # 入群欢迎
    if kicked == True:
        pass
    elif kicked == False:
        if grpid == '760327885':# aniakt
            await matcher.send(f'[CQ:at,qq={at_qid}]进群看公告，有事找群主')
        elif grpid == '706125200':# only
            await matcher.send(f'[CQ:at,qq={at_qid}]进群是吧，给我撅三回啊三回')
        elif grpid == '544033107':# gsakt
            await matcher.send(f'[CQ:at,qq={at_qid}]进群是吧，给我撅三回啊三回')
        elif grpid == '511824025':# akt4
            await matcher.send(f'[CQ:at,qq={at_qid}]进群看公告，有事找群主')
        elif grpid == '317096220':# akt2
            await matcher.send(f'[CQ:at,qq={at_qid}]进群看公告，有事找群主')
        elif grpid == '730804591':# akt3
            await matcher.send(f'[CQ:at,qq={at_qid}]加新群760327885')
        elif grpid == '793395527':# 原神崩坏交流群
            await matcher.send(f'[CQ:at,qq={at_qid}]进群看公告，有事找群主')
        elif grpid == '774244770':# akt5
            await matcher.send(f'[CQ:at,qq={at_qid}]进群看公告，有事找群主')
        elif grpid == '784793447':# akt6
            await matcher.send(f'[CQ:at,qq={at_qid}]进群看公告，有事找群主')
        elif grpid == '785056064':# akt7
            await matcher.send(f'[CQ:at,qq={at_qid}]进群看公告，有事找群主')
        elif grpid == '784733617':# akt8
            await matcher.send(f'[CQ:at,qq={at_qid}]进群看公告，有事找群主')
        elif grpid == '784956578':# akt9
            await matcher.send(f'[CQ:at,qq={at_qid}]进群看公告，有事找群主')
        elif grpid == '784700021':# akt10
            await matcher.send(f'[CQ:at,qq={at_qid}]进群看公告，有事找群主')
        elif grpid == '123881900':# akt11
            await matcher.send(f'[CQ:at,qq={at_qid}]进群看公告，有事找群主')
        elif grpid == '320202467':# akt12
            await matcher.send(f'[CQ:at,qq={at_qid}]进群看公告，有事找群主')
        elif grpid == '195943111':# akt13
            await matcher.send(f'[CQ:at,qq={at_qid}]进群看公告，有事找群主')
        elif grpid == '238106549':# akt14
            await matcher.send(f'[CQ:at,qq={at_qid}]进群看公告，有事找群主')
        elif grpid == '326570597':# akt15
            await matcher.send(f'[CQ:at,qq={at_qid}]进群看公告，有事找群主')
        
        else:
            pass
    else:
        pass

    finder_qid = at_qid

    # gmt8_time = '无法获取'
    # repo_qqlm = '无法获取'
    # repo_phone = '无法获取'
    # repo_ph_place = '无法获取'
    # repo_wid = '无法获取'
    # repo_lol = '无法获取'

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

    gmt8 = 'Asia/Shanghai'
    gmt8_time = datetime.datetime.now(tz=pytz.timezone(gmt8)).strftime('%Y-%m-%d %H:%M:%S')

    add_dict = {
        'join_time' : gmt8_time, 
        'grp' : grpid, 
        'status' : 'in_grp', 
        'qid' : at_qid, 
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