#!/bin/bash

X=3  # 需要随机抽取的帧数
sum_atoms=$(sed -n '7p' XDATCAR | awk '{for (i=1;i<=NF;i++) sum+=$i; print sum}')

# 提取所有帧编号（从 OSZICAR 中第一列）
all_steps=($(grep 'F=' OSZICAR | awk '{print $1}' | sort -n | uniq))
total_steps=${#all_steps[@]}

# 检查是否足够帧可供选择
if [ "$X" -gt "$total_steps" ]; then
    echo "Error: Only $total_steps steps available, but requested $X."
    exit 1
fi

# 随机抽取 X 个不重复帧编号
selected_steps=($(printf "%s\n" "${all_steps[@]}" | shuf -n "$X"))

# 循环写入 POSCAR-序号-帧数 文件
i=5
for j in "${selected_steps[@]}"; do
    outfile="POSCAR-${i}-${j}"
    awk 'NR<8' XDATCAR > "$outfile"
    grep -xA "$sum_atoms" "Direct configuration= *$j" XDATCAR >> "$outfile"
    ((i++))
done

