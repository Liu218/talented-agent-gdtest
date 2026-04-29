# Stock MCP Server

A 股股票工具集 MCP Server，提供三个核心工具：

## 工具列表

| 工具 | 说明 |
|------|------|
| `search_stock` | 根据关键词搜索股票代码和名称 |
| `get_stock_quote` | 查询个股实时行情 + 近期 K 线 |
| `screen_stocks` | 多维度条件选股（涨跌幅、换手率、市值、市盈率等） |

## 数据源

使用 [AKShare](https://akshare.akfamily.xyz/) 作为数据源，免费、无需 API Key。

## 安装依赖

```bash
cd stock_mcp
uv pip install -e .
```

## 运行方式

### 直接运行（调试）

```bash
python server.py
```

### 在 Kiro 中配置

编辑 `.kiro/settings/mcp.json`，添加：

```json
{
  "mcpServers": {
    "stock-server": {
      "command": "uv",
      "args": ["run", "--directory", "/你的项目路径/stock_mcp", "python", "server.py"],
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

## 使用示例

- "帮我搜一下茅台的股票代码"  → `search_stock("茅台")`
- "查一下 600519 的行情"       → `get_stock_quote("600519")`
- "找出今天涨幅超过 5% 的股票" → `screen_stocks(min_change_pct=5)`
- "筛选市值 100 亿以上、市盈率 20 以下的股票" → `screen_stocks(min_market_cap=100, max_pe=20)`
