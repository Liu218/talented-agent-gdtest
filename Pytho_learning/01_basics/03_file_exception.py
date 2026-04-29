# 第三课：文件读写 + 异常处理
# ============================

# ── 1. 写文件 ──
# with 语句会自动关闭文件，推荐写法
with open("data/students.txt", "w", encoding="utf-8") as f:
    f.write("Alice,92\n")
    f.write("Bob,75\n")
    f.write("Charlie,88\n")
    f.write("Diana,60\n")

print("文件写入完成")

# ── 2. 读文件 ──
with open("data/students.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()   # 读取所有行，返回列表

print(lines)
for line in lines:
    line = line.strip()     # 去掉每行末尾的 \n
    name, score = line.split(",")   # 按逗号拆分
    print(f"姓名：{name}，分数：{score}")

# ── 3. 异常处理 ──
# 读一个不存在的文件，不用 try/except 会直接崩掉
# 用 try/except 可以优雅地处理错误

try:
    with open("data/not_exist.txt", "r") as f:
        content = f.read()
except FileNotFoundError:
    print("文件不存在，请检查路径")

# 多种异常分开处理
def parse_score(value: str) -> int:
    """将字符串转换为整数分数，处理可能的转换错误"""
    try:
        return int(value)
    except ValueError:
        print(f"无法转换为数字：{value}，返回0")
        return 0

print(parse_score("88"))    # 正常：88
print(parse_score("abc"))   # 异常：打印提示，返回0

# ── 4. 综合练习准备：读文件并处理数据 ──
with open("data/students.txt", "r", encoding="utf-8") as f:
    students = []
    for line in f:
        name, score = line.strip().split(",")
        students.append({"name": name, "score": int(score)})

print(students)
avg = sum(s["score"] for s in students) / len(students)
print(f"班级平均分：{avg:.1f}")   # :.1f 表示保留1位小数


print("课后作业:")
def load_and_analyze(filepath: str) -> dict:
    """读取成绩文件并分析"""
    # 1. 打开文件，读每一行，拆成 name 和 score
    with open(filepath, "r", encoding="utf-8") as f:
        students = []
        for line in f:
            name, score = line.strip().split(",")
            students.append({"name": name, "score": int(score)})

    # 2. 用 sum/len 算平均分
    avg = sum(s["score"] for s in students) / len(students)

    # 3. 用 max 找最高分的学生
    top = max(students, key=lambda s: s["score"])

    # 4. 返回字典
    return {
        "students": students,
        "avg": round(avg, 1),
        "top": top["name"]
    }

# 调用
result = load_and_analyze("data/students.txt")
print(result)

