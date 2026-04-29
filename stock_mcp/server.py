"""
股票 MCP Server
提供三个工具：搜索股票、查询行情、条件选股
数据源：akshare（免费 A 股数据接口）
"""

import logging
from mcp.server.fastmcp import FastMCP

import akshare as ak
import pandas as pd

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("stock-mcp")

# 创建 MCP Server 实例
mcp = FastMCP(
    "stock-server",
    instructions="A 股股票工具集：搜索、行情查询、条件选股",
)


@mcp.tool()
def search_stock(keyword: str) -> str:
    """根据关键词搜索 A 股股票，支持股票代码或名称模糊匹配。

    Args:
        keyword: 搜索关键词，可以是股票代码（如 600519）或名称（如 贵州茅台）
    """
    try:
        # 获取 A 股全量股票列表
        df = ak.stock_info_a_code_name()

        # 模糊匹配代码或名称
        mask = df["code"].str.contains(keyword, na=False) | df["name"].str.contains(
            keyword, na=False
        )
        result = df[mask].head(20)

        if result.empty:
            return f"未找到与 '{keyword}' 相关的股票"

        # 格式化输出
        lines = [f"搜索 '{keyword}' 的结果（共 {len(result)} 条）：", ""]
        for _, row in result.iterrows():
            lines.append(f"  {row['code']}  {row['name']}")

        return "\n".join(lines)

    except Exception as e:
        logger.error("搜索股票失败: %s", e)
        return f"搜索失败: {e}"


@mcp.tool()
def get_stock_quote(symbol: str, period: str = "daily", days: int = 10) -> str:
    """查询个股实时行情和近期 K 线数据。

    Args:
        symbol: 股票代码，如 600519、000001
        period: K 线周期，可选 daily（日线）、weekly（周线）、monthly（月线），默认 daily
        days: 返回最近多少根 K 线，默认 10
    """
    try:
        # 1. 获取实时行情快照
        realtime_df = ak.stock_zh_a_spot_em()
        stock_row = realtime_df[realtime_df["代码"] == symbol]

        lines: list[str] = []

        if not stock_row.empty:
            row = stock_row.iloc[0]
            lines.append(f"【{row['名称']}（{row['代码']}）实时行情】")
            lines.append(f"  最新价:   {row.get('最新价', '-')}")
            lines.append(f"  涨跌幅:   {row.get('涨跌幅', '-')}%")
            lines.append(f"  涨跌额:   {row.get('涨跌额', '-')}")
            lines.append(f"  成交量:   {row.get('成交量', '-')} 手")
            lines.append(f"  成交额:   {row.get('成交额', '-')} 元")
            lines.append(f"  换手率:   {row.get('换手率', '-')}%")
            lines.append(f"  今开:     {row.get('今开', '-')}")
            lines.append(f"  最高:     {row.get('最高', '-')}")
            lines.append(f"  最低:     {row.get('最低', '-')}")
            lines.append(f"  昨收:     {row.get('昨收', '-')}")
            lines.append(f"  总市值:   {_format_amount(row.get('总市值', 0))}")
            lines.append(f"  流通市值: {_format_amount(row.get('流通市值', 0))}")
            lines.append(f"  市盈率:   {row.get('市盈率-动态', '-')}")
            lines.append(f"  市净率:   {row.get('市净率', '-')}")
        else:
            lines.append(f"未找到代码为 {symbol} 的实时行情")

        # 2. 获取近期 K 线
        lines.append("")
        lines.append(f"【近 {days} 个交易日 K 线（{period}）】")

        kline_df = ak.stock_zh_a_hist(
            symbol=symbol,
            period=period,
            adjust="qfq",  # 前复权
        )

        if kline_df.empty:
            lines.append("  暂无 K 线数据")
        else:
            recent = kline_df.tail(days)
            lines.append(
                f"  {'日期':>12}  {'开盘':>10}  {'收盘':>10}  {'最高':>10}  {'最低':>10}  {'涨跌幅':>8}  {'成交量':>12}"
            )
            for _, r in recent.iterrows():
                lines.append(
                    f"  {str(r['日期']):>12}  {r['开盘']:>10.2f}  {r['收盘']:>10.2f}  "
                    f"{r['最高']:>10.2f}  {r['最低']:>10.2f}  {r.get('涨跌幅', 0):>7.2f}%  "
                    f"{int(r.get('成交量', 0)):>12}"
                )

        return "\n".join(lines)

    except Exception as e:
        logger.error("查询行情失败: %s", e)
        return f"查询行情失败: {e}"


@mcp.tool()
def screen_stocks(
    min_change_pct: float | None = None,
    max_change_pct: float | None = None,
    min_turnover_rate: float | None = None,
    max_turnover_rate: float | None = None,
    min_market_cap: float | None = None,
    max_market_cap: float | None = None,
    min_pe: float | None = None,
    max_pe: float | None = None,
    min_volume: float | None = None,
    sort_by: str = "涨跌幅",
    ascending: bool = False,
    limit: int = 20,
) -> str:
    """根据条件筛选 A 股股票，支持涨跌幅、换手率、市值、市盈率等多维度过滤。

    Args:
        min_change_pct: 最小涨跌幅（%），如 5 表示涨幅 >= 5%
        max_change_pct: 最大涨跌幅（%），如 -5 表示跌幅 >= 5%
        min_turnover_rate: 最小换手率（%）
        max_turnover_rate: 最大换手率（%）
        min_market_cap: 最小总市值（亿元）
        max_market_cap: 最大总市值（亿元）
        min_pe: 最小市盈率（动态）
        max_pe: 最大市盈率（动态）
        min_volume: 最小成交量（手）
        sort_by: 排序字段，可选：涨跌幅、换手率、成交量、成交额、总市值、市盈率-动态，默认按涨跌幅
        ascending: 是否升序排列，默认 False（降序）
        limit: 返回条数，默认 20，最大 50
    """
    try:
        df = ak.stock_zh_a_spot_em()

        # 排除 ST 和退市股
        df = df[~df["名称"].str.contains("ST|退", na=False)]

        # 应用筛选条件
        if min_change_pct is not None:
            df = df[pd.to_numeric(df["涨跌幅"], errors="coerce") >= min_change_pct]
        if max_change_pct is not None:
            df = df[pd.to_numeric(df["涨跌幅"], errors="coerce") <= max_change_pct]
        if min_turnover_rate is not None:
            df = df[pd.to_numeric(df["换手率"], errors="coerce") >= min_turnover_rate]
        if max_turnover_rate is not None:
            df = df[pd.to_numeric(df["换手率"], errors="coerce") <= max_turnover_rate]
        if min_market_cap is not None:
            df = df[
                pd.to_numeric(df["总市值"], errors="coerce") >= min_market_cap * 1e8
            ]
        if max_market_cap is not None:
            df = df[
                pd.to_numeric(df["总市值"], errors="coerce") <= max_market_cap * 1e8
            ]
        if min_pe is not None:
            df = df[pd.to_numeric(df["市盈率-动态"], errors="coerce") >= min_pe]
        if max_pe is not None:
            df = df[pd.to_numeric(df["市盈率-动态"], errors="coerce") <= max_pe]
        if min_volume is not None:
            df = df[pd.to_numeric(df["成交量"], errors="coerce") >= min_volume]

        if df.empty:
            return "没有符合条件的股票"

        # 排序
        limit = min(limit, 50)
        if sort_by in df.columns:
            df[sort_by] = pd.to_numeric(df[sort_by], errors="coerce")
            df = df.sort_values(by=sort_by, ascending=ascending)

        result = df.head(limit)

        # 格式化输出
        conditions = _build_condition_desc(
            min_change_pct,
            max_change_pct,
            min_turnover_rate,
            max_turnover_rate,
            min_market_cap,
            max_market_cap,
            min_pe,
            max_pe,
            min_volume,
        )
        lines = [
            f"【选股结果】筛选条件: {conditions}",
            f"排序: {sort_by}（{'升序' if ascending else '降序'}），共 {len(df)} 只符合条件，展示前 {len(result)} 只：",
            "",
            f"  {'代码':>8}  {'名称':<8}  {'最新价':>8}  {'涨跌幅':>8}  {'换手率':>8}  {'成交量(手)':>12}  {'总市值':>12}  {'市盈率':>8}",
        ]

        for _, r in result.iterrows():
            lines.append(
                f"  {r['代码']:>8}  {r['名称']:<8}  {r.get('最新价', '-'):>8}  "
                f"{r.get('涨跌幅', '-'):>7}%  {r.get('换手率', '-'):>7}%  "
                f"{r.get('成交量', '-'):>12}  {_format_amount(r.get('总市值', 0)):>12}  "
                f"{r.get('市盈率-动态', '-'):>8}"
            )

        return "\n".join(lines)

    except Exception as e:
        logger.error("选股失败: %s", e)
        return f"选股失败: {e}"


# ---- 辅助函数 ----


def _format_amount(value: float | int | str) -> str:
    """将金额格式化为 亿/万 单位的可读字符串。"""
    try:
        num = float(value)
    except (ValueError, TypeError):
        return str(value)

    if num >= 1e8:
        return f"{num / 1e8:.2f}亿"
    elif num >= 1e4:
        return f"{num / 1e4:.2f}万"
    else:
        return f"{num:.2f}"


def _build_condition_desc(
    min_change_pct,
    max_change_pct,
    min_turnover_rate,
    max_turnover_rate,
    min_market_cap,
    max_market_cap,
    min_pe,
    max_pe,
    min_volume,
) -> str:
    """将筛选条件拼成可读的描述文本。"""
    parts: list[str] = []
    if min_change_pct is not None:
        parts.append(f"涨跌幅>={min_change_pct}%")
    if max_change_pct is not None:
        parts.append(f"涨跌幅<={max_change_pct}%")
    if min_turnover_rate is not None:
        parts.append(f"换手率>={min_turnover_rate}%")
    if max_turnover_rate is not None:
        parts.append(f"换手率<={max_turnover_rate}%")
    if min_market_cap is not None:
        parts.append(f"总市值>={min_market_cap}亿")
    if max_market_cap is not None:
        parts.append(f"总市值<={max_market_cap}亿")
    if min_pe is not None:
        parts.append(f"市盈率>={min_pe}")
    if max_pe is not None:
        parts.append(f"市盈率<={max_pe}")
    if min_volume is not None:
        parts.append(f"成交量>={min_volume}手")
    return "、".join(parts) if parts else "无（全量）"


# 入口
if __name__ == "__main__":
    mcp.run()
