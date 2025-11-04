# 配置文件示例 - config_example.py
# 复制此文件为 config_local.py 并填入你的API密钥
# 将API密钥单独存储，避免硬编码在主程序中

ACCOUNTS = [
    {
        "name": "主账户",
        "api_key": "your_api_key_here",
        "api_secret": "your_api_secret_here",
        "testnet": False  # True表示使用测试网
    },
    {
        "name": "备用账户",
        "api_key": "your_api_key_here",
        "api_secret": "your_api_secret_here",
        "testnet": False  # True表示使用测试网
    },
]

# API权限要求:
# 1. 读取权限 (必须)
# 2. 现货和杠杆交易 (如果要查看现货)
# 3. 合约交易 (如果要查看合约)

# - 需要开启 "读取" 权限
# - 不需要 "交易" 和 "提现" 权限
# - 建议设置IP白名单提高安全性

#
# ⚠️ 安全建议:
# - 不要启用提现权限
# - 不要将 config_local.py 上传到公共代码仓库
# - config_local.py 已在 .gitignore 中被忽略