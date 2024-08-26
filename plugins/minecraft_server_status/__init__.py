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
from utils.tool import is_strIntNum

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
                                       '-------------------- \n'+
                                       '${server_reason} \n'
                                       '-------------------- \n'+
                                       '${server_err} \n'
                                       )
ping_success_qq_message_template=Template('\n ${server_name} \n '+
                                          '在线: 🟢 \n '+
                                          '在线人数: ${server_online_people}/${server_max_people} \n '+
                                          '延迟: ${server_ping}ms \n'+
                                          '-------------------- \n'+
                                          '${server_motd} \n')

# mc服务器状态 本来服务器就不多，列出所有服务器
ss = on_command("ss",aliases={"服务器状态"}, force_whitespace=True)
@ss.handle()
async def _(event:MessageEvent, args:Message = CommandArg()):
  indies = args.extract_plain_text().split()
  if len(indies) != 1:
    await ss.send(
      '\n指令使用错误!!! \n'+
      '格式: /服务器状态 序号 \n'+
      '例子. '+
      '/服务器状态 1 \n'+
      '注意: 序号必须和 /所有服务器序号 指令给你的序号一样'
    )
    await ss.finish()
  if is_strIntNum(indies[0]) is False:
    await ss.send(
      '\n你的服务器序号输错了!! \n'+
      '序号为: ' + indies[0] + '\n'+
      '应该用数字序号'
    )
    await ss.finish()
  if int(indies[0]) < 1 or int(indies[0]) > len(customConfig):
    await ss.send(
      '\n认真点!! \n'+
      '服务器序号错误,没有查询到序号为:' + indies[0] + ' 的MC服务器 \n'
    )
    await ss.finish()
  server = customConfig[int(indies[0])-1]
  status, ping = await mcStatus(server)
  if ping == 0:
    serverStatus = {
      "server_name": server['server_name'],
      "server_reason": status["reason"],
      "server_err": status["err"]
    }
    if status["type"] == "unknown_err" or status["type"] == "connect_remote_server_fail":
      await ss.send(ping_fail_qq_message_template.substitute(serverStatus))
      await ss.finish()
    elif status["type"] == "connect_mc_server_fail":
      await ss.send(ping_fail_qq_message_template.substitute(serverStatus))
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

gss = on_command("gss", aliases={"所有服务器序号"})
@gss.handle()
async def list_all_mc_server():
  res = '\n'
  for index, server in enumerate(customConfig):
    res = res + '序号: ' + str(index+1) + '  (' + server['server_name'] + ')\n'
  res = res + '-------------------- \n' + '使用序号查看我的世界服务器状态'
  await gss.send(res)


async def mcStatus(serverInfo = {"server_addr": "", "server_type": ""}):
  if serverInfo["server_type"] == "Java":
    try:
      server = JavaServer.lookup(serverInfo["server_addr"])
      return server.status(), server.ping()
    except ConnectionRefusedError as e:
      return {"type": "connect_remote_server_fail", "reason": "服务器可能没有开，联系群管理员@_midou", "err": e}, 0
    except IOError as e:
      return {"type": "connect_mc_server_fail", "reason": "mc服务端程序可能没有启动，联系群管理员@_midou", "err": e}, 0
    except Exception as e:
      return {"type": "unknown_err", "reason": "服务器错误，联系群管理员@_midou", "err": e}, 0
    
  elif serverInfo["server_type"] == "Bedrock":
    server = BedrockServer.lookup(serverInfo["server_addr"])
    return server.status()
