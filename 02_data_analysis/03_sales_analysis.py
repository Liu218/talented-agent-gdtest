# Pandas 第三课：销售数据实战分析
# ==================================
# 综合运用前面学的所有知识

import pandas as pd

# ── 1. 读取 CSV ──
df = pd.read_csv("data/sales.csv")

print("=== 数据概览 ===")
print(f"数据量：{df.shape[0]} 行，{df.shape[1]} 列")
print(f"列名：{list(df.columns)}")
print('df.head():')
print(df.head())
print('df.describe()')
print(df.describe())
print()

# ── 2. 各产品销售额排名 ──
# SQL: SELECT product, SUM(total) as revenue FROM sales GROUP BY product ORDER BY revenue DESC
product_revenue = (
    df.groupby("product")["total"]
    .sum()
    .sort_values(ascending=False)
)
print("=== 各产品总销售额 ===")
print(product_revenue)
print()

# ── 3. 各城市销售情况 ──
city_stats = df.groupby("city").agg(
    订单数=("order_id", "count"),
    总销售额=("total", "sum"),
    平均客单价=("total", "mean"),
)
city_stats = city_stats.sort_values("总销售额", ascending=False)
print("=== 各城市销售统计 ===")
print(city_stats)
print()

# ── 4. 月度销售趋势 ──
# 先从 date 列提取月份
df["month"] = pd.to_datetime(df["date"]).dt.month
monthly = df.groupby("month")["total"].sum()
print("=== 月度销售额 ===")
print(monthly)
print()

# ── 5. 找出销售额 Top 5 的订单 ──
top5 = df.nlargest(5, "total")[["order_id", "product", "city", "qty", "total"]]
print("=== 销售额 Top 5 订单 ===")
print(top5)
print()

# ── 6. 筛选分析：哪些城市的手机卖得最好？ ──
phone_sales = df[df["product"] == "手机"]
phone_by_city = (
    phone_sales.groupby("city")["total"]
    .sum()
    .sort_values(ascending=False)
)
print("=== 各城市手机销售额 ===")
print(phone_by_city)
print()

# ── 7. 交叉分析：城市 × 产品 的销售额矩阵 ──
cross = df.pivot_table(
    values="total",
    index="city",
    columns="product",
    aggfunc="sum",
    fill_value=0,
)
print("=== 城市×产品 销售额矩阵 ===")
print(cross)

#作业来了，自己写一段分析代码：
# 找出每个月卖得最好的产品是什么（按月分组，再按产品分组，求销售额）
# 计算每个产品的平均客单价（total 的平均值）
# 找出哪个城市的订单量最少
# 提示：

# 第1题需要两层 groupby：df.groupby(["month", "product"])["total"].sum()
monthly_product = df.groupby(["month","product"])["total"].sum()
best_product = monthly_product.groupby('month').idxmax()
print("=== 每个月卖得最好的产品是 ===")
print(best_product)
print()
# 第2题用 groupby("product")["total"].mean()
print("=== 计算每个产品的平均客单价 ===")
product_mean = df.groupby("product")["total"].mean()
print(product_mean)
# 第3题用 groupby("city")["order_id"].count() 然后取最小
print("=== 哪个城市的订单量最少 ===")
city_cnt = df.groupby("city")["order_id"].count().idxmin()
print(city_cnt)