# Page Rank
## 要求
已知一个有向图有N个点，M条边，其中点的编号为0到N-1，请求出其各点的PageRank值。
　　题目保证给出的有向图中有且只有一个SCC（强连通分量）包含了大于一个的点，你应该首先去掉不属于这个SCC的点，再进行计算。假设这个大SCC包含了X个点，那么最后算出来的这X点的PageRank之和应该等于1.
　　题目保证没有自环和重边。
　　题目假设随机跳转概率为0。
　　题目保证那个大SCC对应的马尔科夫链是非周期的，所以用迭代法做最后肯定可以收敛
### 输入格式

输入的第一行包含两个整数N, M分别表示有向图的点数和边数，其中0<N<=1000， 0 < M <= 10000。
　　接下来的M行每行有两个整数a和b，表示存在一条边从a点指向b点，0<=a, b <N。
　　接下来的一行有一个整数K，0<K<=N，表示你只需要输出其中的K个点的答案即可。
　　接下来的一行有K个整数，表示你需要输出答案的点的编号。
6 7
1 2
2 1
1 3
3 2
0 1
1 4
4 5
5
0 2 1 3 4
```
0->1
1->2 3 4
2->1 
3->2
4->5
```
### 输出格式

输出K行，第i行表示第i个点的PageRank值，需要精确到5位小数（四舍五入），如果这个点恰好不在那个大SCC中，则只需要输出字符串“None”，字符串不包含双引号。

None
0.40000
0.40000
0.20000
None
## windows 下重定向
```shell
Get-Content input.txt |./main.exe
```
## windows 下`msvc`使用
[doc](https://docs.microsoft.com/en-us/cpp/build/reference/compiler-options-listed-alphabetically?view=msvc-160)
```shell
cl /EHsc main.cpp
```
## code描述
+ main.cpp 处理输入输出
+ pagerank.h 处理网络节点结构与pagerank对应的去除DeadEnd，in分量，以及快速的稀疏矩阵运算。
+ input*.txt 自己构造的测试数据集，其中input2.txt包含一个in节点和两个deadEnd.
+ sub.cpp 是main.cpp和pagerank.h的合并，用于提交。
+ CMakeLists.txt 用于指定编译依赖。
### pagerank算法
> n为节点数，m为边数
+ 每个节点包含in,out的链表，因为每个页面链接不多，使用链表方便节点的增加与去除，O(n+m)
+ 对节点循环扫描，直至无deadEnd和in分量，O(n)
+ 重新构建in,out的vector，方便后续计算索引，O(n+m)
+ 计算scc内节点概率，反复迭代，直至精度变化小于1e-6；在矩阵计算中仅计算节点in向量对应节点，复杂度为O(m)*迭代次数。