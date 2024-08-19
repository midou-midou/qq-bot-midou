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
# from dahlia import Dahlia, clean

from .config import Config

# 插件元数据配置
__plugin_meta__ = PluginMetadata(
    name="minecraft_server_status",
    description="我的世界Minecraft服务器状态查询插件",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)
# motd = Dahlia()

# 自定义配置
with open(path.abspath(path.join(__plugin_meta__.name+"_config.yml")),'r', encoding="utf-8") as fp:
    customConfig= yaml.load(fp.read(),Loader=yaml.SafeLoader)

ping_fail_qq_message_template=Template('\n ${server_name} \n 离线: 🔴 \n'+
                                       '------------------------'+
                                       '${server_reason}'
                                       '------------------------'+
                                       '${server_err}'
                                       )
ping_success_qq_message_template=Template('\n ${server_name} \n '+
                                          '在线: 🟢 \n '+
                                          '在线人数: ${server_online_people}/${server_max_people} \n '+
                                          '延迟: ${server_ping}ms \n'+
                                          '------------------------ \n'+
                                          '${server_motd} \n')

# mc服务器状态 本来服务器就不多，列出所有服务器
ss = on_command("ss",aliases={"服务器状态", "ss"})
@ss.handle()
async def _(event:MessageEvent, args:Message = CommandArg()):
  for index, server in enumerate(customConfig):
    status, ping = await mcStatus(customConfig[index])
    if status["type"] == "unknown_err" or status["type"] == "connect_remote_server_fail":
      await ss.send(ping_fail_qq_message_template.substitute({
        "server_name": server['server_name'],
        "server_reason": status["reason"],
        "server_err": status["err"]
      }))
      return
    elif status["type"] == "connect_mc_server_fail":
      await ss.send(ping_fail_qq_message_template.substitute({
        "server_name": server['server_name'],
        "server_reason": status["reason"],
        "server_err": status["err"]
      }))
    else:
      serverStatus = {
        "server_name": server['server_name'],
        "server_online_people": status.players.online,
        "server_max_people": status.players.max,
        "server_ping": math.ceil(ping),
        # "server_motd": clean(status.motd.raw['text']),
        "server_motd": status.motd.to_plain(),
      }
      await ss.send(ping_success_qq_message_template.substitute(serverStatus))

async def mcStatus(serverInfo = {"server_addr": "", "server_type": ""}):
  if serverInfo["server_type"] == "Java":
    try:
      server = JavaServer.lookup(serverInfo["server_addr"])
      return server.status(), server.ping()
    except IOError as e:
      return {"type": "connect_mc_server_fail", "reason": "mc服可能没有开，联系群管理员@_midou", "err": e}, 0
    except IOError as e:
      return {"type": "connect_remote_server_fail", "reason": "mc运行的服务器可能没有开，联系群管理员@_midou", "err": e}, 0
    except Exception as e:
      return {"type": "unknown_err", "reason": "服务器错误，联系群管理员@_midou", "err": e}, 0
    
  elif serverInfo["server_type"] == "Bedrock":
    server = BedrockServer.lookup(serverInfo["server_addr"])
    return server.status()
