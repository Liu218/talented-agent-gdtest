# 生成模拟销售数据，运行一次就行
import pandas as pd
import random

random.seed(42)

products = ["手机", "笔记本", "耳机", "平板", "键盘", "鼠标"]
cities = ["北京", "上海", "广州", "深圳", "杭州"]
prices = {"手机": 3999, "笔记本": 6999, "耳机": 299, "平板": 2999, "键盘": 499, "鼠标": 129}

rows = []
for i in range(200):
    product = random.choice(products)
    rows.append({
        "order_id": f"ORD{i+1:04d}",
        "date": f"2025-{random.randint(1,6):02d}-{random.randint(1,28):02d}",
        "product": product,
        "price": prices[product],
        "qty": random.randint(1, 5),
        "city": random.choice(cities),
    })

df = pd.DataFrame(rows)
df["total"] = df["price"] * df["qty"]
df.to_csv("data/sales.csv", index=False, encoding="utf-8-sig")
print(f"已生成 {len(df)} 条销售数据 → data/sales.csv")
