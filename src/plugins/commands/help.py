from nonebot.plugin.on import on_command
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.adapters.onebot.v11.event import GroupMessageEvent

matcher = on_command('help')

@matcher.handle()
async def _(event: GroupMessageEvent):
    request_qid = str(event.user_id)
    await matcher.send(MessageSegment.at(request_qid) + '\n' + 
'''
使用帮助：
/help       显示本帮助
/finder     社工库查找
/pxfinder   （预留命令）
/rdsfz      随机身份证
/rdsimg     随机涩图
/serverinfo （预留命令）
/time       报时
/userlevel  显示当前用户组
'''.strip()    
    )
    
