# 第四课：lambda、排序、常用内置函数
# ====================================

# ── 1. lambda 匿名函数 ──
# lambda 就是一个"一次性的小函数"，不用 def 定义

# 普通写法
def add(a, b):
    return a + b

# lambda 写法（完全等价）
add2 = lambda a, b: a + b

print(add(3, 5))    # 8
print(add2(3, 5))   # 8

# lambda 最常用的场景：作为参数传给其他函数
# 比如上节课的 max(students, key=lambda s: s["score"])
# 意思是：告诉 max 函数，按每个字典的 "score" 来比大小

# ── 2. sorted 排序 ──
numbers = [5, 2, 8, 1, 9, 3]

print('基本排序---------------------------')
# 基本排序
print(sorted(numbers))              # [1, 2, 3, 5, 8, 9] 升序
print(sorted(numbers, reverse=True)) # [9, 8, 5, 3, 2, 1] 降序
print(sorted(numbers,reverse = False))

# 对字典列表排序（数据分析超常用）
students = [
    {"name": "Alice", "score": 92},
    {"name": "Bob", "score": 75},
    {"name": "Charlie", "score": 88},
    {"name": "Diana", "score": 60},
]

print('# 按分数从高到低排')
by_score = sorted(students, key=lambda s: s["score"], reverse=True)
print(by_score)
for s in by_score:
    print(f"{s['name']}: {s['score']}")

# ── 3. map：对每个元素做同一个操作 ──
prices = [10, 20, 30, 40]

# 所有价格打8折
discounted = list(map(lambda p: p * 0.8, prices))
print(f"打折后：{discounted}")

# 等价的列表推导式写法（推荐，更易读）
discounted2 = [p * 0.8 for p in prices]
print(f"推导式：{discounted2}")

# ── 4. filter：筛选元素 ──
ages = [12, 18, 25, 8, 30, 15]

# 筛选成年人（>=18）
adults = list(filter(lambda a: a >= 18, ages))
print(f"成年人：{adults}")

# 等价的列表推导式写法（推荐）
adults2 = [a for a in ages if a >= 18]
print(f"推导式：{adults2}")

# ── 5. 其他常用内置函数 ──
nums = [3, 1, 4, 1, 5, 9, 2, 6]

print(f"最大值：{max(nums)}")
print(f"最小值：{min(nums)}")
print(f"求和：{sum(nums)}")
print(f"长度：{len(nums)}")
print(f"是否全部大于0：{all(n > 0 for n in nums)}")
print(f"是否存在大于8：{any(n > 8 for n in nums)}")

# enumerate：循环时同时拿到索引和值
fruits = ["apple", "banana", "cherry"]
for i, fruit in enumerate(fruits):
    print(f"第{i}个：{fruit}")

# zip：把两个列表配对
names = ["Alice", "Bob", "Charlie"]
scores = [92, 75, 88]
for name, score in zip(names, scores):
    print(f"{name} → {score}")

print()
print('---------课后作业-------------')
# 有一份订单数据：
orders = [
    {"product": "手机", "price": 3999, "qty": 2},
    {"product": "耳机", "price": 299, "qty": 5},
    {"product": "笔记本", "price": 6999, "qty": 1},
    {"product": "键盘", "price": 499, "qty": 3},
    {"product": "鼠标", "price": 129, "qty": 10},
]
# 完成以下任务：

# 给每个订单新增一个 "total" 字段，值为 price * qty
# 按 total 从高到低排序
# 筛选出 total > 2000 的订单
# 打印结果
# 提示：

# 第1步可以用 for 循环给字典加字段
# 第2步用 sorted + lambda
# 第3步用列表推导式
print(orders)
print()
for order in orders:
    print(order)
    order['total'] = order['price'] * order['qty']
print('-----------------orders')
print(orders)
# for order in orders:
#     print(order)

sorted_orders = sorted(orders, key=lambda o: o["price"], reverse=True)
print(sorted_orders)


big_order = list(filter(lambda o: o['total'] >= 2000, orders))
print(f"大订单：{big_order}")

# 等价的列表推导式写法（推荐）
big_order2 = [o for o in orders if o['total'] > 2000]
print(f"推导式大订单：：{big_order2}")

big_orders = [o for o in sorted_orders if o["total"] > 2000]


print('打印')
for o in big_orders:
    print(f"{o['product']}: 单价{o['price']} × {o['qty']}件 = {o['total']}")
