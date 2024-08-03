import nonebot
from nonebot.adapters.qq import Adapter as QQAdapter  # 避免重复命名

# 初始化 NoneBot
# .env中表述数组有问题 暂时直接传入配置（QQ开放平台配置）
nonebot.init(qq_bots=[{
    "id": "102201809",
    "token":"LxoKAfijwGwt76BNmcz2RlY8VDEEuwIk",
    "secret":"DxhRBwhSDyjUG2oaM8uhUH4reRE2qeSG",
    "intent":{ 
        "c2c_group_at_messages":True
    }
}])
# config = nonebot.get_driver().config

# 注册适配器
driver = nonebot.get_driver()
driver.register_adapter(QQAdapter)

# 在这里加载插件
nonebot.load_plugins("./plugins")  # 内置插件

if __name__ == "__main__":
    nonebot.run()