#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
币安多账号持仓查看工具 - 主程序
从配置文件读取账号信息
"""

import sys
from binance_portfolio_viewer import BinanceAccount, print_account_summary
from datetime import datetime

def main():
    """主函数"""
    print("🚀 币安多账号持仓查看工具")
    print(f"⏰ 查询时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 尝试导入配置文件
    try:
        from config_local import ACCOUNTS
    except ImportError:
        print("\n❌ 错误: 未找到配置文件!")
        print("请执行以下步骤:")
        print("1. 复制 config_example.py 为 config_local.py")
        print("2. 在 config_local.py 中填入你的API密钥")
        print("3. 重新运行此程序")
        sys.exit(1)
    
    if not ACCOUNTS:
        print("\n❌ 错误: 配置文件中没有账号信息!")
        sys.exit(1)
    
    # 创建账号实例并查询
    for account_config in ACCOUNTS:
        account = BinanceAccount(
            name=account_config['name'],
            api_key=account_config['api_key'],
            api_secret=account_config['api_secret'],
            testnet=account_config.get('testnet', False)
        )
        print_account_summary(account)
    
    print(f"\n{'='*80}")
    print("✅ 查询完成")

if __name__ == "__main__":
    main()