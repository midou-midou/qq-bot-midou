# qq-bot-midou 蜜豆QQ机器人

## 如何使用

**必须安装完所需环境及`nb-cli`**

1. 安装`nb-cli` [参考文档快速入门](https://nonebot.dev/docs/quick-start)
2. 安装依赖`pip install -r requirements.txt`
3. `nb run`运行项目，可以加选项`-r`

### 配置文件  
QQ机器人配置文件实例
```yaml
-
  id: "10220xxxx"
  token: "你的token"
  secret: "你的secret"
  intent:
    c2c_group_at_messages: true
-
 更多配置...
```  
**在`git clone`项目后，在项目根目录创建配置文件：`qqbotsecret.yml`  文件名字必须一样！！！**

QQ机器人相关配置需要到 [QQ开放平台](https://q.qq.com/#/app/bot)  

Minecraft插件机器人配置实例  
```yaml
-
  "server_name": "1.20.1 虚无世界 暮色森林 血族传说"
  "server_addr": "192.168.1.2:25568"
  "server_type": "Java"
-
  "server_name": "1.20.1 枪械 魔法 更多怪物 Mod服"
  "server_addr": "192.168.1.2:25567"
  "server_type": "Java"
```  
**在`git clone`项目后，在项目根目录创建配置文件：`minecraft_server_status_config.yml`  文件名字必须一样！！！**

## 现有功能  
* Minecraft Java版服务器、基岩版服务器状态查询  
  + 仅支持查询在线人数、连通性、延迟
