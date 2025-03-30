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

### 交易数据结构
```json
{
    "Transaction Fields": {
        "hash": "0x...",
        "from": "0x...",
        "to": "0x...",
        "value": "..."
    },
    "Transaction Receipt Fields": {
        "status": 1,
        "gas_used": "...",
        "logs": [...]
    }
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


