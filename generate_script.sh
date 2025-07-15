#!/bin/bash

# 读取目录.txt文件内容
echo "#!/bin/sh -f"
echo "#PBS -N vasp"
echo "#PBS -l nodes=1:ppn=32"
echo "#PBS -l walltime=1200:00:00"
echo "#PBS -q batch"
echo "#PBS -V"
echo "source /opt/intel/compilers_and_libraries_2018/linux/bin/compilervars.sh intel64 "
echo "source /opt/intel/mkl/bin/mklvars.sh intel64"
echo "source /opt/intel/impi/2018.1.163/bin64/mpivars.sh"
while IFS= read -r line; do
    # 输出模板内容，并在中间插入当前行
    echo "cd \$PBS_O_WORKDIR"
    echo "$line"
    echo "mpirun  -n 32 /opt/vasp.5.4.1/bin/vasp_std >> log"
    echo "wait"
    echo ""  # 添加空行分隔不同的任务块
done < "disrs.txt"