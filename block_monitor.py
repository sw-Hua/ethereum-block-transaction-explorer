from web3 import Web3
from dotenv import load_dotenv
import os
import json
from datetime import datetime
import time
from decimal import Decimal

# 加载环境变量
load_dotenv()

# 连接到以太坊节点
ALCHEMY_API_KEY = os.getenv('ALCHEMY_API_KEY')
w3 = Web3(Web3.HTTPProvider(f'https://eth-mainnet.g.alchemy.com/v2/{ALCHEMY_API_KEY}'))

# 常见合约地址列表
COMMON_CONTRACTS = {
    '0xdAC17F958D2ee523a2206206994597C13D831ec7': 'USDT',
    '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48': 'USDC',
    '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2': 'WETH',
    '0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599': 'WBTC',
    '0x7D1AfA7B718fb893dB30A3aBc0Cfc608AaCfeBB0': 'MATIC',
    '0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984': 'UNI',
    '0x6B175474E89094C44Da98b954EedeAC495271d0F': 'DAI'
}

def format_timestamp(timestamp):
    """将Unix时间戳转换为可读格式"""
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def format_eth(value):
    """格式化ETH金额"""
    return f"{float(value):.8f}"

def analyze_transactions(transactions):
    """分析交易数据"""
    total_value = 0
    contract_calls = 0
    unique_addresses = set()
    token_transfers = 0
    
    for tx in transactions:
        # 计算总ETH转账金额
        value = w3.from_wei(tx.value, 'ether')
        total_value += float(value)
        
        # 统计合约调用（通过检查接收地址是否在常见合约列表中）
        if tx.to and tx.to in COMMON_CONTRACTS:
            contract_calls += 1
            token_transfers += 1
            
        # 统计唯一地址
        unique_addresses.add(tx['from'])
        if tx.to:
            unique_addresses.add(tx.to)
    
    return {
        "total_value": total_value,
        "contract_calls": contract_calls,
        "unique_addresses": len(unique_addresses),
        "token_transfers": token_transfers
    }

def print_block_info(block):
    """打印区块信息"""
    print("\n" + "="*50)
    print(f"区块 #{block.number}")
    print("="*50)
    print(f"时间: {format_timestamp(block.timestamp)}")
    print(f"区块哈希: {block.hash.hex()}")
    print(f"父区块哈希: {block.parentHash.hex()}")
    print(f"矿工地址: {block.miner}")
    print(f"Gas使用量: {block.gasUsed:,}")
    print(f"Gas限制: {block.gasLimit:,}")
    print(f"交易数量: {len(block.transactions)} 笔")
    
    # 分析交易
    analysis = analyze_transactions(block.transactions)
    print("\n交易分析:")
    print(f"总ETH转账: {format_eth(analysis['total_value'])} ETH")
    print(f"代币转账数量: {analysis['token_transfers']}")
    print(f"涉及唯一地址数: {analysis['unique_addresses']}")
    
    # 显示前5笔交易
    print("\n前5笔交易:")
    for i, tx in enumerate(block.transactions[:5], 1):
        print(f"\n交易 #{i}:")
        print(f"交易哈希: {tx.hash.hex()}")
        print(f"发送方: {tx['from']}")
        print(f"接收方: {tx.to if tx.to else '合约创建'}")
        print(f"金额: {format_eth(w3.from_wei(tx.value, 'ether'))} ETH")
        print(f"Gas价格: {w3.from_wei(tx.gasPrice, 'gwei'):.2f} Gwei")
        if tx.to in COMMON_CONTRACTS:
            print(f"代币类型: {COMMON_CONTRACTS[tx.to]}")

def monitor_new_blocks():
    """监控新区块"""
    print("开始监控新区块...")
    last_block = w3.eth.block_number
    
    while True:
        try:
            current_block = w3.eth.block_number
            
            if current_block > last_block:
                # 获取新区块信息
                block = w3.eth.get_block(current_block, full_transactions=True)
                print_block_info(block)
                last_block = current_block
            
            # 等待12秒（以太坊平均出块时间）
            time.sleep(12)
            
        except KeyboardInterrupt:
            print("\n停止监控")
            break
        except Exception as e:
            print(f"发生错误: {str(e)}")
            time.sleep(5)  # 发生错误时等待5秒后重试

def main():
    print("以太坊区块监控器")
    print("1. 查看最新区块")
    print("2. 持续监控新区块")
    choice = input("请选择操作 (1/2): ")
    
    if choice == "1":
        # 获取最新区块
        latest_block = w3.eth.block_number
        block = w3.eth.get_block(latest_block, full_transactions=True)
        print_block_info(block)
    elif choice == "2":
        monitor_new_blocks()
    else:
        print("无效的选择")

if __name__ == "__main__":
    main() 