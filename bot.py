import nonebot
from nonebot.adapters.qq import Adapter as QQAdapter  # 避免重复命名

# 初始化 NoneBot
nonebot.init()
# config = nonebot.get_driver().config

# 注册适配器
driver = nonebot.get_driver()
driver.register_adapter(QQAdapter)

# 在这里加载插件
nonebot.load_plugins("./src")  # 内置插件

if __name__ == "__main__":
    nonebot.run()