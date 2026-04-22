# 第二课：列表、字典、集合
# ========================

# ── 1. 列表 list ──
# 有序、可重复、可修改
fruits = ["apple", "banana", "cherry"]

fruits.append("orange")        # 末尾添加
fruits.insert(1, "mango")      # 在索引1插入
fruits.remove("banana")        # 删除指定值
popped = fruits.pop()          # 删除并返回最后一个

print(fruits)
print(f"弹出的是：{popped}")
print(f"长度：{len(fruits)}")
print(f"是否包含apple：{'apple' in fruits}")

# 列表推导式（数据分析常用）
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
for n in numbers:
    print(n)
evens = [n for n in numbers if n % 2 == 0]       # 筛选偶数
squares = [n ** 2 for n in numbers]               # 每个数平方
print(f"偶数：{evens}")
print(f"平方：{squares}")

# ── 2. 字典 dict ──
# 键值对，类似 SQL 里的一行数据
# 你第4题做对了，这里扩展更多操作
student = {
    "name": "Alice",
    "age": 25,
    "scores": [85, 92, 78]
}

# 读取（推荐用 get，避免 key 不存在时报错）
print(student["name"])                    # 直接取，key不存在会报错
print(student.get("email", "未填写"))     # 安全取，不存在返回默认值

# 遍历字典
for key, value in student.items():
    print(f"{key}: {value}")

# 字典推导式
prices = {"apple": 3, "banana": 2, "cherry": 8}
expensive = {k: v for k, v in prices.items() if v > 2}
print(f"价格大于2的：{expensive}")

# ── 3. 集合 set ──
# 无序、不重复，常用于去重和集合运算
tags_a = {"python", "data", "ml"}
tags_b = {"python", "web", "api"}

print(f"交集：{tags_a & tags_b}")    # 共同有的
print(f"并集：{tags_a | tags_b}")    # 全部
print(f"差集：{tags_a - tags_b}")    # a有b没有

# 去重经典用法
raw = [1, 2, 2, 3, 3, 3, 4]
unique = list(set(raw))
print(f"去重后：{unique}")

# ── 4. 对比总结 ──
# list  → 有序有重复，用于存储序列数据
# dict  → 键值对，用于存储结构化数据（像一行 JSON）
# set   → 无序无重复，用于去重和集合运算

####课后练习
####用列表推导式筛选出成绩大于80分的学生名字列表，结果应该是 ['Alice', 'Charlie']。
students = [
    {"name": "Alice", "score": 92},
    {"name": "Bob", "score": 75},
    {"name": "Charlie", "score": 88},
    {"name": "Diana", "score": 60},
]
# 答案一
result1 = []
for s in students:
    if s['score'] > 80:
        result1.append(s['name'])
print(result1)

# 答案二 
result2 = [s["name"] for s in students if s["score"] > 80]
print(result2)