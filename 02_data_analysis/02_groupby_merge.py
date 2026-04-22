# Pandas 第二课：分组聚合 + 表合并
# ==================================
# 这课对应 SQL 的 GROUP BY 和 JOIN

import pandas as pd

# ── 准备数据 ──
employees = pd.DataFrame({
    "name": ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank"],
    "dept": ["技术", "技术", "产品", "产品", "技术", "销售"],
    "salary": [15000, 20000, 18000, 16000, 12000, 22000],
    "age": [25, 30, 35, 28, 22, 32],
})
print("员工表：")
print(employees)
print()

# ── 1. groupby 分组聚合 ──
# SQL: SELECT dept, AVG(salary) FROM employees GROUP BY dept
avg_by_dept = employees.groupby("dept")["salary"].mean()
print("各部门平均工资：")
print(avg_by_dept)
print()

# SQL: SELECT dept, COUNT(*) FROM employees GROUP BY dept
count_by_dept = employees.groupby("dept")["name"].count()
print("各部门人数：")
print(count_by_dept)
print()

# 多个聚合函数一起用
# SQL: SELECT dept, COUNT(*), AVG(salary), MAX(salary) FROM employees GROUP BY dept
dept_stats = employees.groupby("dept")["salary"].agg(["count", "mean", "max"])
print("各部门薪资统计：")
print(dept_stats)
print()

# ── 2. 多列聚合 ──
dept_detail = employees.groupby("dept").agg(
    人数=("name", "count"),
    平均工资=("salary", "mean"),
    平均年龄=("age", "mean"),
)
print("部门详细统计：")
print(dept_detail)
print()

# ── 3. 表合并 merge ──（类似 SQL 的 JOIN）
# 部门信息表
dept_info = pd.DataFrame({
    "dept": ["技术", "产品", "销售"],
    "manager": ["张三", "李四", "王五"],
    "budget": [500000, 300000, 400000],
})
print("部门信息表：")
print(dept_info)
print()

# SQL: SELECT * FROM employees LEFT JOIN dept_info ON employees.dept = dept_info.dept
merged = pd.merge(employees, dept_info, on="dept", how="left")
print("合并后（LEFT JOIN）：")
print(merged)
print()

# ── 4. 数据透视表 ──（类似 Excel 的数据透视）
# 按部门统计各项指标
pivot = employees.pivot_table(
    values="salary",
    index="dept",
    aggfunc=["mean", "max", "count"]
)
print("数据透视表：")
print(pivot)
