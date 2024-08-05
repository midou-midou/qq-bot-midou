# midou-qq-bot 蜜豆QQ机器人

## 如何使用

**因涉及到Python虚拟环境(.venv)，暂时必须安装完所需环境及使用`nb-cli`创建一个新项目，之后把蜜豆机器人项目拖进去覆盖**

1. 安装`nonebot` [参考文档快速入门](https://nonebot.dev/docs/quick-start)
2. `nb create`命令创建一个项目，为了把此项目的代码拖进去
3. `nb run`运行项目，可以加选项`-r`

项目中已配置好`AppId`、`Token`、`Secert`，**不要配置到dotenv文件中**  
QQ机器人相关配置需要到 [QQ开放平台](https://q.qq.com/#/app/bot)  

## 现有功能  
* Minecraft Java版服务器、基岩版服务器状态查询  
  + 仅支持查询在线人数、连通性、延迟
