from nonebot.adapters.onebot.v12 import MetaEvent
from nonebot import on_command
import nonebot

@on_command('test')
async def _():
    bot = nonebot.get_bot()
    await bot.send(message='123t')