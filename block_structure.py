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

def get_block_structure():
    """Get the complete structure of the latest block"""
    
    # Get latest block
    latest_block = w3.eth.get_block('latest', full_transactions=True)
    
    block_data = {
        "Block Header": {
            "slot": "Requires special API access",
            "proposer_index": "Requires special API access",
            "parent_root": latest_block.parentHash.hex(),
            "state_root": latest_block.stateRoot.hex(),
        },
        
        "Block Body": {
            "randao_reveal": "Requires special API access",
            "eth1_data": "Requires special API access",
            "graffiti": "Requires special API access",
            "proposer_slashings": "Requires special API access",
            "attester_slashings": "Requires special API access",
            "attestations": "Requires special API access",
            "deposits": "Requires special API access",
            "voluntary_exits": "Requires special API access",
            "sync_aggregate": "Requires special API access",
            "execution_payload": {
                "parent_hash": latest_block.parentHash.hex(),
                "fee_recipient": latest_block.miner,
                "state_root": latest_block.stateRoot.hex(),
                "receipts_root": latest_block.receiptsRoot.hex(),
                "logs_bloom": latest_block.logsBloom.hex(),
                "prev_randao": latest_block.mixHash.hex() if hasattr(latest_block, 'mixHash') else None,
                "block_number": latest_block.number,
                "gas_limit": latest_block.gasLimit,
                "gas_used": latest_block.gasUsed,
                "timestamp": datetime.fromtimestamp(latest_block.timestamp).strftime('%Y-%m-%d %H:%M:%S'),
                "extra_data": latest_block.extraData.hex(),
                "base_fee_per_gas": str(w3.from_wei(latest_block.baseFeePerGas, 'gwei')) if hasattr(latest_block, 'baseFeePerGas') else None,
                "block_hash": latest_block.hash.hex(),
                "transactions": [{
                    "hash": tx.hash.hex(),
                    "from": tx['from'],
                    "to": tx.to if tx.to else 'Contract Creation',
                    "value": str(w3.from_wei(tx.value, 'ether')),
                    "gas_price": str(w3.from_wei(tx.gasPrice, 'gwei')),
                    "nonce": tx.nonce,
                    "input": tx.input.hex() if tx.input != '0x' else None
                } for tx in latest_block.transactions[:5]],  # Limiting to first 5 transactions
                "withdrawals": "Requires special API access"
            }
        },
        
        "Attestations Data (Requires special API access)": {
            "aggregation_bits": "Requires special API access",
            "data": {
                "slot": "Requires special API access",
                "index": "Requires special API access",
                "beacon_block_root": "Requires special API access",
                "source": "Requires special API access",
                "target": "Requires special API access"
            },
            "signature": "Requires special API access"
        },
        
        "Withdrawals (Requires special API access)": {
            "address": "Requires special API access",
            "amount": "Requires special API access",
            "index": "Requires special API access",
            "validatorIndex": "Requires special API access"
        }
    }
    
    return block_data

def save_block_structure(block_data, filename="blockchain_data/block_structure.json"):
    """Save block structure to file"""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(block_data, f, ensure_ascii=False, indent=2)

def main():
    print("Fetching latest block structure...")
    block_data = get_block_structure()
    
    # Print data structure
    print("\nBlock Structure:")
    pp = pprint.PrettyPrinter(indent=2, width=80)
    pp.pprint(block_data)
    
    # Save to file
    save_block_structure(block_data)
    print("\nData saved to blockchain_data/block_structure.json")

if __name__ == "__main__":
    main() 