import random
import re
import sys

# 可调参数：要随机抽取的帧数
X = 3

# XDATCAR 和 OSZICAR 文件名
xdatcar_path = "XDATCAR"
oszicar_path = "OSZICAR"

# 读取原子总数（XDATCAR 第 7 行）
with open(xdatcar_path, 'r') as f:
    lines = f.readlines()
    atom_counts = list(map(int, lines[6].split()))
    sum_atoms = sum(atom_counts)

# 提取所有帧编号（从 XDATCAR 中）
with open(oszicar_path, 'r') as f:
    all_steps = sorted(set(
        int(line.split()[2])
        for line in f if 'configuration' in line
    ))

total_steps = len(all_steps)

# 错误检查
if X > total_steps:
    print(f"Error: Only {total_steps} steps available, but requested {X}.")
    sys.exit(1)

# 随机选择 X 个不重复帧
selected_steps = random.sample(all_steps, X)

# 从 XDATCAR 中提取并写入帧
i = 0
with open(xdatcar_path, 'r') as f:
    xdatcar_lines = f.readlines()

for step in selected_steps:
    outfile = f"POSCAR-{i}-{step}"
    with open(outfile, 'w') as out:
        # 写入头部前 7 行 + 原子数行
        out.writelines(xdatcar_lines[:7])
        out.write(xdatcar_lines[7])

        # 匹配对应帧的行号
        pattern = re.compile(rf"Direct configuration= *{step}")
        for idx, line in enumerate(xdatcar_lines):
            if pattern.match(line):
                out.write(line)  # 写入配置标题
                out.writelines(xdatcar_lines[idx + 1 : idx + 1 + sum_atoms])
                break
    i += 1
