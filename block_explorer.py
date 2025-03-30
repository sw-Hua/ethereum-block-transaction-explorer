from web3 import Web3
from dotenv import load_dotenv
import os
import json
from datetime import datetime
import time

# 加载环境变量
load_dotenv()

# 连接到以太坊节点
ALCHEMY_API_KEY = os.getenv('ALCHEMY_API_KEY')
w3 = Web3(Web3.HTTPProvider(f'https://eth-mainnet.g.alchemy.com/v2/{ALCHEMY_API_KEY}'))

def get_block_info(block_number):
    """获取指定区块的信息"""
    print(f"正在获取区块 {block_number} 的信息...")
    block = w3.eth.get_block(block_number, full_transactions=True)
    return block

def get_transaction_receipt(tx_hash):
    """获取交易回执信息"""
    receipt = w3.eth.get_transaction_receipt(tx_hash)
    return receipt

def format_timestamp(timestamp):
    """将Unix时间戳转换为可读格式"""
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def print_block_info(block):
    """打印区块信息"""
    print(f"\n新区块 #{block.number} 的信息:")
    print(f"时间戳: {format_timestamp(block.timestamp)}")
    print(f"交易数量: {len(block.transactions)} 笔")
    print(f"Gas使用量: {block.gasUsed}")
    print(f"区块哈希: {block.hash.hex()}")
    print("-" * 50)

def main():
    # 获取当前时间
    current_time = datetime.now()
    print(f"\n当前时间: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 获取最新区块
    latest_block = w3.eth.block_number
    print(f"最新区块号: {latest_block}")
    
    # 获取区块信息
    block = get_block_info(latest_block)
    
    # 打印区块基本信息
    print(f"\n区块 {latest_block} 的基本信息:")
    print(f"区块时间戳: {format_timestamp(block.timestamp)}")
    print(f"交易总数: {len(block.transactions)} 笔")
    print(f"Gas使用量: {block.gasUsed}")
    
    # 显示所有交易的信息
    print(f"\n显示区块内所有交易的时间顺序:")
    for i, tx in enumerate(block.transactions, 1):
        receipt = w3.eth.get_transaction_receipt(tx.hash)
        print(f"\n交易 {i}/{len(block.transactions)}:")
        print(f"交易哈希: {tx.hash.hex()}")
        print(f"发送方: {tx['from']}")
        print(f"接收方: {tx['to']}")
        print(f"交易金额: {w3.from_wei(tx.value, 'ether')} ETH")
        print(f"Gas使用量: {receipt['gasUsed']}")
        
        # 只显示前5笔交易，然后询问是否继续
        if i == 5:
            response = input("\n已显示前5笔交易，是否继续显示更多？(y/n): ")
            if response.lower() != 'y':
                print(f"\n已停止显示。区块内还有 {len(block.transactions) - 5} 笔交易未显示。")
                break

    print("\n数据获取完成！")

if __name__ == "__main__":
    main() 