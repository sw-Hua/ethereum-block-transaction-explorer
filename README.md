# 以太坊区块浏览器

这是一个使用 web3.py 开发的以太坊区块浏览器项目，用于获取以太坊区块和交易数据。

## 功能特点

- 连接以太坊节点（通过 Alchemy）
- 获取区块信息
- 获取区块内的交易信息
- 获取交易回执信息

## 环境要求

- Python 3.8+
- web3.py
- python-dotenv

## 安装步骤

1. 克隆项目
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
3. 配置环境变量：
   - 复制 `.env.example` 为 `.env`
   - 在 `.env` 文件中填入你的 Alchemy API 密钥

## 使用方法

### 区块数据结构分析
```bash
python3 block_structure.py
```
输出最新区块的完整数据结构，包括区块头、区块体等信息。

### 交易数据结构分析
```bash
python3 transaction_structure.py
```
分析最新区块中的交易数据结构，展示交易的原始信息和执行结果。

### 区块浏览
```bash
python3 block_explorer.py
```
交互式浏览最新区块信息，可以逐笔查看交易详情。

### 区块监控
```bash
python3 block_monitor.py
```
持续监控新区块的生成，实时显示区块信息和交易分析。

## 数据结构示例

### 区块数据结构
```json
{
    "Block Header": {
        "slot": "...",
        "proposer_index": "...",
        "parent_root": "..."
    }
}
```

## 数据结构示例

### 区块数据结构 (来自 block_structure.py)
```json
{
    "Block Header": {
        "slot": "Requires special API access",
        "proposer_index": "Requires special API access",
        "parent_root": "0x...",
        "state_root": "0x..."
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
            "parent_hash": "0x...",
            "fee_recipient": "0x...",
            "state_root": "0x...",
            "receipts_root": "0x...",
            "logs_bloom": "0x...",
            "prev_randao": "0x...",
            "block_number": "...",
            "gas_limit": "...",
            "gas_used": "...",
            "timestamp": "...",
            "extra_data": "0x...",
            "base_fee_per_gas": "...",
            "block_hash": "0x...",
            "transactions": "..."
        }
    }
}
```

### 交易数据结构 (来自 transaction_structure.py)
```json
{
    "block_number": "区块号",
    "block_hash": "区块哈希",
    "timestamp": "区块时间戳",
    "transactions_count": "区块内总交易数",
    "transactions_processed": "处理的交易数量",
    "transactions": [
        {
            "hash": "0x...",
            "nonce": "交易序号",
            "block_hash": "0x...",
            "block_number": "区块号",
            "transaction_index": "交易索引",
            "from": "发送方地址",
            "to": "接收方地址",
            "value": "ETH数量",
            "input": "输入数据",
            "gas": "gas限制",
            "gas_price": "gas价格",
            "receipt": {
                "status": "交易状态(1成功/0失败)",
                "gas_used": "使用的gas量",
                "cumulative_gas_used": "累计使用的gas量",
                "contract_address": "合约地址(如果是合约创建)",
                "logs_count": "日志数量"
            },
            "max_fee_per_gas": "最大gas费用",
            "max_priority_fee_per_gas": "最大优先费用",
            "type": "交易类型"
        }
    ]
}
```

## 项目结构

# 虚拟环境
venv/
env/

# IDE
.idea/
.vscode/
```

## 文件说明

- `block_structure.py`: 区块数据结构分析工具
- `transaction_structure.py`: 交易数据结构分析工具
- `block_explorer.py`: 区块浏览工具
- `block_monitor.py`: 区块监控工具
- `requirements.txt`: 项目依赖
- `.env.example`: 环境变量模板文件


