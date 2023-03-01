from nonebot.plugin.on import on_command
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from urllib.request import Request, urlopen
from urllib.parse import urlencode
import re
import ast

matcher = on_command('rdsimg')

@matcher.handle()
async def _(event: GroupMessageEvent):
    request_qid = str(event.user_id)
    ua = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.47'}
    url = 'https://api.lolicon.app/setu/v2'
    # url = 'https://www.dmoe.cc/random.php?return=json'
    # data = {'r18' : 2, 'num' : 1}
    requ = Request(url=url, headers=ua)
    repo = urlopen(requ).read()
    brepo_str = repo.decode()
    brepo_dict = ast.literal_eval(brepo_str)

    imgurl = brepo_dict['imgurl']
    send_img = re.sub(r'\\', '', imgurl)
    await matcher.send(MessageSegment.at(request_qid) + MessageSegment.image(send_img))
