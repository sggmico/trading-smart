#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
币安多账号持仓查看工具
支持现货和合约账户
"""

import requests
import hmac
import hashlib
import time
from typing import Dict, List
from datetime import datetime

class BinanceAccount:
    def __init__(self, name: str, api_key: str, api_secret: str, testnet: bool = False):
        self.name = name
        self.api_key = api_key
        self.api_secret = api_secret
        
        if testnet:
            self.base_url = "https://testnet.binance.vision"
            self.futures_url = "https://testnet.binancefuture.com"
        else:
            self.base_url = "https://api.binance.com"
            self.futures_url = "https://fapi.binance.com"
    
    def _generate_signature(self, params: Dict) -> str:
        """生成签名"""
        query_string = '&'.join([f"{key}={value}" for key, value in params.items()])
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature
    
    def _request(self, endpoint: str, params: Dict = None, base_url: str = None) -> Dict:
        """发送请求"""
        if params is None:
            params = {}
        
        if base_url is None:
            base_url = self.base_url
        
        params['timestamp'] = int(time.time() * 1000)
        params['signature'] = self._generate_signature(params)
        
        headers = {'X-MBX-APIKEY': self.api_key}
        
        try:
            response = requests.get(f"{base_url}{endpoint}", headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ 请求失败 ({self.name}): {str(e)}")
            return None
    
    def get_spot_balance(self) -> List[Dict]:
        """获取现货账户余额"""
        endpoint = "/api/v3/account"
        data = self._request(endpoint)
        
        if not data:
            return []
        
        balances = []
        for balance in data.get('balances', []):
            free = float(balance['free'])
            locked = float(balance['locked'])
            total = free + locked
            
            if total > 0:
                balances.append({
                    'asset': balance['asset'],
                    'free': free,
                    'locked': locked,
                    'total': total
                })
        
        return balances
    
    def get_futures_balance(self) -> List[Dict]:
        """获取合约账户余额"""
        endpoint = "/fapi/v2/account"
        data = self._request(endpoint, base_url=self.futures_url)
        
        if not data:
            return []
        
        balances = []
        for asset in data.get('assets', []):
            wallet_balance = float(asset['walletBalance'])
            
            if wallet_balance > 0:
                balances.append({
                    'asset': asset['asset'],
                    'wallet_balance': wallet_balance,
                    'unrealized_profit': float(asset['unrealizedProfit']),
                    'available_balance': float(asset['availableBalance'])
                })
        
        return balances
    
    def get_futures_positions(self) -> List[Dict]:
        """获取合约持仓"""
        endpoint = "/fapi/v2/positionRisk"
        data = self._request(endpoint, base_url=self.futures_url)
        
        if not data:
            return []
        
        positions = []
        for pos in data:
            position_amt = float(pos['positionAmt'])
            
            if position_amt != 0:
                positions.append({
                    'symbol': pos['symbol'],
                    'position_amt': position_amt,
                    'entry_price': float(pos['entryPrice']),
                    'mark_price': float(pos['markPrice']),
                    'unrealized_profit': float(pos['unRealizedProfit']),
                    'leverage': pos['leverage']
                })
        
        return positions


def format_number(num: float, decimals: int = 2) -> str:
    """格式化数字"""
    return f"{num:,.{decimals}f}"


def print_account_summary(account: BinanceAccount):
    """打印账户摘要"""
    print(f"\n{'='*80}")
    print(f"📊 账户: {account.name}")
    print(f"{'='*80}")
    
    # 现货账户
    # print("\n💰 现货账户余额:")
    # spot_balances = account.get_spot_balance()
    
    # if spot_balances:
    #     print(f"{'资产':<10} {'可用':<15} {'冻结':<15} {'总计':<15}")
    #     print("-" * 60)
    #     for balance in spot_balances:
    #         print(f"{balance['asset']:<10} "
    #               f"{format_number(balance['free']):<15} "
    #               f"{format_number(balance['locked']):<15} "
    #               f"{format_number(balance['total']):<15}")
    # else:
    #     print("  无持仓或获取失败")
    
    # 合约账户余额
    print("\n📈 合约账户余额:")
    futures_balances = account.get_futures_balance()
    
    if futures_balances:
        print(f"{'资产':<10} {'钱包余额':<15} {'未实现盈亏':<15} {'可用余额':<15}")
        print("-" * 60)
        for balance in futures_balances:
            pnl = balance['unrealized_profit']
            pnl_str = f"+{format_number(pnl)}" if pnl >= 0 else format_number(pnl)
            print(f"{balance['asset']:<10} "
                  f"{format_number(balance['wallet_balance']):<15} "
                  f"{pnl_str:<15} "
                  f"{format_number(balance['available_balance']):<15}")
    else:
        print("  无余额或获取失败")
    
    # 合约持仓
    print("\n🎯 合约持仓:")
    positions = account.get_futures_positions()
    
    if positions:
        print(f"{'交易对':<12} {'持仓量':<15} {'开仓价':<12} {'标记价':<12} {'未实现盈亏':<15} {'杠杆':<8}")
        print("-" * 80)
        for pos in positions:
            pnl = pos['unrealized_profit']
            pnl_str = f"+{format_number(pnl)}" if pnl >= 0 else format_number(pnl)
            position_type = "多" if pos['position_amt'] > 0 else "空"
            
            print(f"{pos['symbol']:<12} "
                  f"{format_number(abs(pos['position_amt']), 4)} {position_type:<10} "
                  f"{format_number(pos['entry_price'], 4):<12} "
                  f"{format_number(pos['mark_price'], 4):<12} "
                  f"{pnl_str:<15} "
                  f"{pos['leverage']}x")
    else:
        print("  无持仓或获取失败")


def main():
    """主函数"""
    print("🚀 币安多账号持仓查看工具")
    print(f"⏰ 查询时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 配置你的多个账号
    accounts = [
        BinanceAccount(
            name="主账号",
            api_key="YOUR_API_KEY_1",
            api_secret="YOUR_API_SECRET_1"
        ),
        BinanceAccount(
            name="副账号",
            api_key="YOUR_API_KEY_2",
            api_secret="YOUR_API_SECRET_2"
        ),
        # 添加更多账号...
    ]
    
    # 遍历所有账号
    for account in accounts:
        print_account_summary(account)
    
    print(f"\n{'='*80}")
    print("✅ 查询完成")


if __name__ == "__main__":
    main()