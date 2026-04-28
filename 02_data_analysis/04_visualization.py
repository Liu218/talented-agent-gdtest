# Pandas 第四课：数据可视化（Matplotlib）
# ==========================================
# 用刚才的销售数据画图

import pandas as pd
import matplotlib.pyplot as plt

# 解决中文显示问题（macOS）
plt.rcParams["font.sans-serif"] = ["Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False

# 读取数据
df = pd.read_csv("data/sales.csv")
df["month"] = pd.to_datetime(df["date"]).dt.month

# ── 1. 柱状图：各产品总销售额 ──
product_revenue = df.groupby("product")["total"].sum().sort_values(ascending=False)

plt.figure(figsize=(8, 5))
product_revenue.plot(kind="bar", color="#4A90D9")
plt.title("各产品总销售额")
plt.xlabel("产品")
plt.ylabel("销售额（元）")
plt.xticks(rotation=0)          # 横轴标签不旋转
plt.tight_layout()               # 自动调整布局
plt.savefig("data/01_product_revenue.png", dpi=150)
plt.close()
print("✅ 图1 已保存：data/01_product_revenue.png")

# ── 2. 折线图：月度销售趋势 ──
monthly = df.groupby("month")["total"].sum()

plt.figure(figsize=(8, 5))
monthly.plot(kind="line", marker="o", color="#E74C3C", linewidth=2)
plt.title("月度销售趋势")
plt.xlabel("月份")
plt.ylabel("销售额（元）")
plt.xticks(range(1, 7))
plt.grid(True, alpha=0.3)       # 添加网格线
plt.tight_layout()
plt.savefig("data/02_monthly_trend.png", dpi=150)
plt.close()
print("✅ 图2 已保存：data/02_monthly_trend.png")

# ── 3. 饼图：各城市订单占比 ──
city_count = df.groupby("city")["order_id"].count()

plt.figure(figsize=(7, 7))
city_count.plot(
    kind="pie",
    autopct="%1.1f%%",          # 显示百分比
    startangle=90,               # 起始角度
    colors=["#4A90D9", "#E74C3C", "#2ECC71", "#F39C12", "#9B59B6"],
)
plt.title("各城市订单占比")
plt.ylabel("")                   # 去掉默认的 y 轴标签
plt.tight_layout()
plt.savefig("data/03_city_pie.png", dpi=150)
plt.close()
print("✅ 图3 已保存：data/03_city_pie.png")

# ── 4. 水平柱状图：各城市销售额对比 ──
city_revenue = df.groupby("city")["total"].sum().sort_values()

plt.figure(figsize=(8, 5))
city_revenue.plot(kind="barh", color="#2ECC71")
plt.title("各城市销售额对比")
plt.xlabel("销售额（元）")
plt.ylabel("城市")
plt.tight_layout()
plt.savefig("data/04_city_revenue.png", dpi=150)
plt.close()
print("✅ 图4 已保存：data/04_city_revenue.png")

print("\n所有图表已保存到 data/ 目录，双击 png 文件即可查看")
