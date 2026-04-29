# Pandas 第一课：DataFrame 基础
# ================================
# DataFrame 就是一张表，你可以把它想象成 Excel 表格或 SQL 表

import pandas as pd

# ── 1. 创建 DataFrame ──
# 从字典创建（最常用）
data = {
    "name": ["Alice", "Bob", "Charlie", "Diana", "Eve"],
    "age": [25, 30, 35, 28, 22],
    "city": ["北京", "上海", "北京", "广州", "上海"],
    "salary": [15000, 20000, 25000, 18000, 12000],
}
df = pd.DataFrame(data)
print(df)
print()

# ── 2. 基本信息 ──
print(f"形状（行数, 列数）：{df.shape}")
print(f"列名：{list(df.columns)}")
print(f"数据类型：\n{df.dtypes}")
print()

# ── 3. 查看数据 ──
print("前3行：")
print(df.head(3))       # 类似 SQL: SELECT * FROM df LIMIT 3
print()

print("统计摘要：")
print(df.describe())    # 自动算 count/mean/std/min/max
print()

# ── 4. 选择列 ──（类似 SQL 的 SELECT）
# 选一列 → 返回 Series
print(df["name"])
print()

# 选多列 → 返回 DataFrame
print(df[["name", "salary"]])
print()

# ── 5. 筛选行 ──（类似 SQL 的 WHERE）
# 工资大于15000
high_salary = df[df["salary"] > 15000]
print("工资 > 15000：")
print(high_salary)
print()

# 多条件：北京 且 年龄 > 25
# SQL: WHERE city = '北京' AND age > 25
beijing_senior = df[(df["city"] == "北京") & (df["age"] > 25)]
print("北京且年龄>25：")
print(beijing_senior)
print()

# ── 6. 排序 ──（类似 SQL 的 ORDER BY）
by_salary = df.sort_values("salary", ascending=False)
print("按工资降序：")
print(by_salary)
print()

# ── 7. 新增列 ──
df["annual_salary"] = df["salary"] * 12
print("新增年薪列：")
print(df)
