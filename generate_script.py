#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

# 获取当前目录下的所有条目
entries = os.listdir()

# 筛选出文件夹（排除文件）
folders = [entry for entry in entries if os.path.isdir(entry)]

# 将文件夹名称写入dirs.txt文件
with open('dirs.txt', 'w', encoding='utf-8') as f:
    for folder in folders:
        f.write(f"{folder}\n")

print(f"已成功将 {len(folders)} 个文件夹名称写入 dirs.txt")


def generate_vasp_script():
    # 输出PBS头信息
    header = """#!/bin/sh -f
#PBS -N vasp
#PBS -l nodes=1:ppn=24
#PBS -l walltime=1200:00:00
#PBS -q batch
#PBS -V
source /opt/intel/compilers_and_libraries_2018/linux/bin/compilervars.sh intel64
source /opt/intel/mkl/bin/mklvars.sh intel64
source /opt/intel/impi/2018.1.163/bin64/mpivars.sh
"""

    # 读取dirs.txt文件并生成任务脚本
    try:
        with open("dirs.txt", "r") as f:
            directories = f.read().splitlines()
    except FileNotFoundError:
        print("错误: 未找到disrs.txt文件")
        return

    script_content = header
    for directory in directories:
        if directory.strip():  # 忽略空行
            script_content += f"""
cd $PBS_O_WORKDIR
cd {directory}
mpirun -n 24 /opt/vasp.5.4.1/bin/vasp_std >> log
wait

"""

    # 将生成的脚本写入文件
    output_file = "vaspall.sh"
    with open(output_file, "w") as f:
        f.write(script_content)
    
    print(f"VASP作业脚本已生成到 {output_file}")
    print("请记得给脚本添加执行权限: chmod +x vaspall.sh")

if __name__ == "__main__":
    generate_vasp_script()
