from nonebot.plugin.on import on_command
from nonebot.adapters import Message
from nonebot.params import EventMessage
import pymongo

admingiveop = on_command('admingiveop')

@admingiveop.handle()
async def _(rxmsg: Message = EventMessage()):
    await admingiveop.send(rxmsg)