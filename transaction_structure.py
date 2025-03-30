from web3 import Web3
from dotenv import load_dotenv
import os
import json
from datetime import datetime
import pprint

# Load environment variables
load_dotenv()

# Alchemy API key
ALCHEMY_API_KEY = os.getenv('ALCHEMY_API_KEY')

# Connect to Ethereum node
w3 = Web3(Web3.HTTPProvider(f'https://eth-mainnet.g.alchemy.com/v2/{ALCHEMY_API_KEY}'))

def get_transaction_data(tx):
    """Get detailed transaction data including receipt"""
    try:
        receipt = w3.eth.get_transaction_receipt(tx.hash)
        
        tx_data = {
            # 基本信息
            "hash": tx.hash.hex(),
            "nonce": tx.nonce,
            "block_hash": tx.blockHash.hex(),
            "block_number": tx.blockNumber,
            "transaction_index": tx.transactionIndex,
            
            # 地址信息
            "from": tx['from'],
            "to": tx.to if tx.to else 'Contract Creation',
            
            # 值和数据
            "value": str(w3.from_wei(tx.value, 'ether')),
            "input": tx.input.hex() if tx.input != '0x' else None,
            
            # Gas相关
            "gas": tx.gas,
            "gas_price": str(w3.from_wei(tx.gasPrice, 'gwei')),
            
            # 交易收据信息
            "receipt": {
                "status": receipt.status,
                "gas_used": receipt.gasUsed,
                "cumulative_gas_used": receipt.cumulativeGasUsed,
                "contract_address": receipt.contractAddress.hex() if receipt.contractAddress else None,
                "logs_count": len(receipt.logs)
            }
        }
        
        # 可选字段
        if hasattr(tx, 'maxFeePerGas'):
            tx_data["max_fee_per_gas"] = str(w3.from_wei(tx.maxFeePerGas, 'gwei'))
        if hasattr(tx, 'maxPriorityFeePerGas'):
            tx_data["max_priority_fee_per_gas"] = str(w3.from_wei(tx.maxPriorityFeePerGas, 'gwei'))
        if hasattr(tx, 'type'):
            tx_data["type"] = tx.type
            
        return tx_data
    except Exception as e:
        print(f"Error processing transaction {tx.hash.hex()}: {str(e)}")
        return None

def get_block_transactions(block_number='latest', max_transactions=5):
    """Get transactions in a block with detailed information (limited to max_transactions)"""
    print(f"Getting block data...")
    block = w3.eth.get_block(block_number, full_transactions=True)
    
    print(f"Found {len(block.transactions)} transactions in block {block.number}")
    print(f"Processing first {max_transactions} transactions...")
    
    transactions_data = []
    for i, tx in enumerate(block.transactions[:max_transactions]):
        print(f"Processing transaction {i+1}/{max_transactions}...")
        tx_data = get_transaction_data(tx)
        if tx_data:
            transactions_data.append(tx_data)
    
    return {
        "block_number": block.number,
        "block_hash": block.hash.hex(),
        "timestamp": datetime.fromtimestamp(block.timestamp).strftime('%Y-%m-%d %H:%M:%S'),
        "transactions_count": len(block.transactions),
        "transactions_processed": len(transactions_data),
        "transactions": transactions_data
    }

def save_transactions_data(data, filename="blockchain_data/transactions_structure.json"):
    """Save transactions data to file"""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    print("Fetching latest block transactions...")
    tx_data = get_block_transactions(max_transactions=5)  # 限制只处理5笔交易
    
    print("\nTransactions Structure:")
    pp = pprint.PrettyPrinter(indent=2, width=80)
    pp.pprint(tx_data)
    
    save_transactions_data(tx_data)
    print("\nData saved to blockchain_data/transactions_structure.json")

if __name__ == "__main__":
    main() 