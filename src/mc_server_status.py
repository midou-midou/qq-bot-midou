from nonebot import on_command

from nonebot.adapters.qq import Message,MessageEvent
from nonebot.params import CommandArg

ping = on_command("ping",aliases={"乒"}) #触发该指令可使用代号“乒”
@ping.handle()
async def _(event:MessageEvent,args:Message = CommandArg()):
  # event 代表指令接受的消息类型 args代表除触发指令之外的其他参数
  await ping.send("pong! "+args)
  # await ping.finish()失效，请使用send()