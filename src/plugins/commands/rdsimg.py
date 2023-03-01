from nonebot.plugin.on import on_command
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from urllib.request import Request, urlopen
from urllib.parse import urlencode
import re
import ast
import json

matcher = on_command('rdsimg')

@matcher.handle()
async def _(event: GroupMessageEvent):
    setu_ok = False
    while setu_ok == False:
        try:
            request_qid = str(event.user_id)
            ua = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.47'}
            data = {'Content-Type' : 'application/json'}
            url = 'https://api.lolicon.app/setu/v2'
            # url = 'https://www.dmoe.cc/random.php?return=json'
            # data = {'r18' : 2, 'num' : 1}
            data = urlencode(data).encode('utf-8')
            requ = Request(url=url, data=data, headers=ua, method='POST')
            repo = urlopen(requ)
            brepo_str = repo
            brepo_dict = json.load(brepo_str)
            # brepo_dict = ast.literal_eval(brepo_str)

            errormsg = brepo_dict['error']
            setu = brepo_dict['data'][0]
            setu_pid = setu['pid']
            setu_ai = setu['aiType']
            setu_url = setu['urls']
            setu_url_original = setu_url['original']

            if setu_ai == 1:
                setu_ai_type = 'AI作图：否'
            elif setu_ai == 2:
                setu_ai_type = 'AI作图：是'
            else:
                setu_ai_type = 'AI作图：未知'

            await matcher.send(MessageSegment.at(request_qid) + MessageSegment.image(setu_url_original) + f'{errormsg}\npid：{setu_pid}\n{setu_ai_type}')
            setu_ok = True
        except:
            setu_ok = False
