import nonebot
from nonebot.adapters.qq import Adapter as QQAdapter  # 避免重复命名
import yaml

# 读取qqbot相关配置
with open("qqbotsecert.yml",'r', encoding="utf-8") as fp:
    get_result= yaml.load(fp.read(),Loader=yaml.SafeLoader)

# 初始化 NoneBot
nonebot.init(qq_bots=get_result)
# config = nonebot.get_driver().config

# 注册适配器
driver = nonebot.get_driver()
driver.register_adapter(QQAdapter)

# 在这里加载插件
nonebot.load_plugins("./plugins")

if __name__ == "__main__":
    nonebot.run()