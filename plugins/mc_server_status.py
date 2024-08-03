from string import Template
import math
from nonebot import on_command

from nonebot.adapters.qq import Message,MessageEvent,MessageSegment
from nonebot.params import CommandArg

from mcstatus import JavaServer, BedrockServer

# mc服务器默认打开了server.propertires中的query配置项，且默认都是
serverConfig = [
  {
    "server_name": "1.20.1 原版服",
    "server_addr": "60.205.14.12:25565",
    "server_type": "Java"
  },
  {
    "server_name": "1.20.1 Mod服",
    "server_addr": "60.205.14.12:25567",
    "server_type": "Java"
  }
]

# mc服务器状态 本来服务器就不多，列出所有服务器
ss = on_command("ss",aliases={"服务器状态", "ss"})
@ss.handle()
async def _(event:MessageEvent, args:Message = CommandArg()):
  for index, server in enumerate(serverConfig):
    status, ping = await mcStatus(serverConfig[index])
    if status == "fail":
      serverQQTemp = Template('${server_name} \n 离线: 🔴')
      await ss.send(serverQQTemp.substitute(server_name=server['server_name']))
    else:
      serverQQTemp = Template('${server_name} \n 在线: 🟢 \n 在线人数: ${server_online_people}/${server_max_people} \n 延迟: ${server_ping}ms')
      await ss.send(serverQQTemp.substitute(server_name=server['server_name'], server_online_people=status.players.online, server_max_people=status.players.max, server_ping=math.ceil(ping)))

async def mcStatus(serverInfo = {"server_addr": "", "server_type": ""}):
  if serverInfo["server_type"] == "Java":
    try:
      server = JavaServer.lookup(serverInfo["server_addr"])
      return server.status(), server.ping()
    except Exception as e:
      return "fail", 0
    
  elif serverInfo["server_type"] == "Bedrock":
    server = BedrockServer.lookup(serverInfo["server_addr"])
    return server.status()
