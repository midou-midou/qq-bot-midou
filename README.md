# midou-qq-bot 蜜豆QQ机器人

## 如何使用

**因涉及到Python虚拟环境(.venv)，必须安装完所需环境及`nb-cli`**

1. 安装`nb-cli` [参考文档快速入门](https://nonebot.dev/docs/quick-start)
2. 安装`virtualenv`，`pip install virtualenv`  
3. 在项目根目录使用`virtualenv`创建一个虚拟环境，`virtualenv .venv`（虚拟环境文件夹名字必须是`.venv`）  
4. 激活虚拟环境  
  win: `.venv/bin/activate`执行  
  linux: `source .venv/bin/activate`执行
5. 安装依赖`pip install -r requirements.txt`
3. `nb run`运行项目，可以加选项`-r`

项目中已配置好`AppId`、`Token`、`Secert`，**不要配置到dotenv文件中**  
QQ机器人相关配置需要到 [QQ开放平台](https://q.qq.com/#/app/bot)  

## 现有功能  
* Minecraft Java版服务器、基岩版服务器状态查询  
  + 仅支持查询在线人数、连通性、延迟
