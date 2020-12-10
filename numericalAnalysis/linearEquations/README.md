# 线性方程组数值解法
## Jacobi,Gauss,SOR迭代法
需要求解的矩阵系数位于inputEquation.csv中

求解运行程序如下
```shell
# 自动执行命令，需要预装make和bash环境，或者在linux系统下执行
make 1/iteration.png
```
或者手动分步执行
```shell
# Jacobi 算法
mkdir -p 1/
python solveEquation.py -i 0 0 0 -e inputEquation.csv -m Jacobi -o 1/Jacobi.h5 -w 0.8 1 1.2 1.4 1.6 > 1/Jacobi.h5.log
# GS 算法
mkdir -p 1/
python solveEquation.py -i 0 0 0 -e inputEquation.csv -m GS -o 1/GS.h5 -w 0.8 1 1.2 1.4 1.6 > 1/GS.h5.log
# SOR 算法
mkdir -p 1/
python solveEquation.py -i 0 0 0 -e inputEquation.csv -m SOR -o 1/SOR.h5 -w 0.8 1 1.2 1.4 1.6 > 1/SOR.h5.log
# SOR best算法
mkdir -p 1/
python solveEquation.py -i 0 0 0 -e inputEquation.csv -m SORbest -o 1/SORbest.h5 -w 0.8 1 1.2 1.4 1.6 > 1/SORbest.h5.log
# 画图
python comparePlot.py -i 1/Jacobi.h5 1/GS.h5 1/SOR.h5 1/SORbest.h5 -o 1/iteration.png -w 0.8 1 1.2 1.4 1.6 > 1/iteration.png.log 2>&1
```
## Jacobi,CG
因为矩阵数目不定原因，矩阵被硬编码在程序中，但是仍然可以通过调整程序中定义的类的初始化方法动态调整矩阵的值。

求解运行程序如下
```shell
# 自动执行命令，需要预装make和bash环境，或者在linux系统下执行
make 2/iteration100.png
make 2/iteration10000.png
```
或者手动分步执行
```shell
# 计算迭代100次结果
mkdir -p 2/
python solveSparseEquation.py -n 100 -i 0 0 0 -m Jacobi -o 2/Jacobi100.h5 > 2/Jacobi100.h5.log 2>&1
mkdir -p 2/
python solveSparseEquation.py -n 100 -i 0 0 0 -m CG -o 2/CG100.h5 > 2/CG100.h5.log 2>&1
python compareSparsePlot.py -i 2/Jacobi100.h5 2/CG100.h5 -o 2/iteration100.png > 2/iteration100.png.log 2>&1
#计算迭代10000次结果
mkdir -p 2/
python solveSparseEquation.py -n 10000 -i 0 0 0 -m Jacobi -o 2/Jacobi10000.h5 > 2/Jacobi10000.h5.log 2>&1
mkdir -p 2/
python solveSparseEquation.py -n 10000 -i 0 0 0 -m CG -o 2/CG10000.h5 > 2/CG10000.h5.log 2>&1
python compareSparsePlot.py -i 2/Jacobi10000.h5 2/CG10000.h5 -o 2/iteration10000.png > 2/iteration10000.png.log 2>&1
```
## 共轭梯度法(CG)
需要求解的矩阵系数位于inputEquation2.csv中

求解运行程序如下
```shell
# 自动执行命令，需要预装make和bash环境，或者在linux系统下执行
make 3/iteration.png
```
或者手动分步执行
```shell
# mkdir -p 
mkdir -p 3/
python solveNoSymEquation.py -i 0 0 0 -e inputEquation2.csv -m CG -o 3/CG.h5 > 3/CG.h5.log
python compareNoSymPlot.py -i 3/CG.h5 -o 3/iteration.png > 3/iteration.png.log 2>&1
```
将矩阵化成对称矩阵，利用Gauss变换矩阵`aL(1,3)+bL(2,3)`作用后的矩阵为对称矩阵

2.51a+1.48b+2.68=4.53
1.48a+0.93b+3.04=-1.3
解得
a=
b=