from string import Template
from os import path
import yaml

from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
import math
from nonebot import on_command

from nonebot.adapters.qq import Message,MessageEvent,MessageSegment
from nonebot.params import CommandArg

from mcstatus import JavaServer, BedrockServer
from dahlia import Dahlia

from .config import Config

# 插件元数据配置
__plugin_meta__ = PluginMetadata(
    name="minecraft_server_status",
    description="我的世界Minecraft服务器状态查询插件",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)
motd = Dahlia()

# 自定义配置
with open(path.abspath(path.join(__plugin_meta__.name+"_config.yml")),'r', encoding="utf-8") as fp:
    customConfig= yaml.load(fp.read(),Loader=yaml.SafeLoader)

ping_fail_qq_message_template=Template('\n ${server_name} \n 离线: 🔴')
ping_success_qq_message_template=Template('\n ${server_name} \n '+
                                          '在线: 🟢 \n '+
                                          '在线人数: ${server_online_people}/${server_max_people} \n '+
                                          '详情: ${server_motd} \n'+
                                          '延迟: ${server_ping}ms')

# mc服务器状态 本来服务器就不多，列出所有服务器
ss = on_command("ss",aliases={"服务器状态", "ss"})
@ss.handle()
async def _(event:MessageEvent, args:Message = CommandArg()):
  for index, server in enumerate(customConfig):
    status, ping = await mcStatus(customConfig[index])
    if status == "fail":
      await ss.send(ping_fail_qq_message_template.substitute(server['server_name']))
      return
    serverStatus = {
      "server_name": server['server_name'],
      "server_online_people": status.players.online,
      "server_max_people": status.players.max,
      "server_ping": math.ceil(ping),
      "server_motd": motd.convert(status.motd.raw.text),
    }
    await ss.send(ping_success_qq_message_template.substitute(serverStatus))

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
