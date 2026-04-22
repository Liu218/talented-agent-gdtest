# 第一课：Python 基础语法
# ========================

# ── 1. 变量与数据类型 ──
name = "Alice"
age = 25
height = 1.68
is_student = True

print(type(name))      # <class 'str'>
print(type(age))       # <class 'int'>

# ── 2. f-string（推荐的字符串拼接方式）──
greeting = f"你好，我叫 {name}，今年 {age} 岁"
print(greeting)

# ── 3. 切片：左闭右开，end 位置取不到 ──
x = [1, 2, 3, 4, 5]
#     0  1  2  3  4  ← 索引
print(x[1:4])   # [2, 3, 4]  不包含索引4
print(x[:3])    # [1, 2, 3]  从头开始
print(x[2:])    # [3, 4, 5]  到末尾
print(x[-1])    # 5          最后一个元素

# ── 4. 条件判断 ──
score = 85
if score >= 90:
    print("优秀")
elif score >= 60:
    print("及格")
else:
    print("不及格")

# ── 5. for 循环 ──
for i in range(5):      # range(5) 生成 0,1,2,3,4
    print(i, end=" ")
print()                 # 换行

# ── 6. 函数（修正你第2题的写法）──
def is_even(n: int) -> bool:
    """判断一个整数是否为偶数"""
    return n % 2 == 0   # 直接返回表达式结果，更简洁

print(is_even(4))   # True
print(is_even(7))   # False

# ── 7. 你第3题不会的：求平均分 ──
scores = [85, 92, 78, 90, 88]
avg = sum(scores) / len(scores)
print(f"平均分：{avg}")

# ── 8. 你第5题不会的：列表推导式 ──
words = ["apple", "banana", "cherry", "avocado", "blueberry"]
a_words = [w for w in words if w.startswith("a")]
print(a_words)   # ['apple', 'avocado']

# 作业1 
score = 95
if score >= 90:
    print("优秀")
elif score >= 60:
    print("及格")
else:
    print("不及格")

#作业2 
def get_grade(score: int) -> str:
    """根据分数返回等级"""
    if score >= 90:
        return "优秀"
    elif score >= 60:
        return "及格"
    else:
        return "不及格"

print(get_grade(95))   # 优秀
print(get_grade(75))   # 及格
print(get_grade(50))   # 不及格
