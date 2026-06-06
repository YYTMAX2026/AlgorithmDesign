# 算法设计与分析 · 课外实验作业

**课程**：算法设计与分析（2026年春季学期）  
**仓库地址**：https://github.com/YYTMAX2026/AlgorithmDesign

---

## 实验概述

本实验对**排序算法**和**0-1背包问题**的两类经典算法进行实证性能测试，通过实际运行收集数据，绘制图表，分析时间复杂度与运行效率。

---

## 实验内容

### 一、排序算法实验

实现并测试以下三种排序算法：
- **冒泡排序**（Bubble Sort）：O(n²)，基础比较排序
- **归并排序**（Merge Sort）：O(n log n)，分治策略
- **快速排序**（Quick Sort）：O(n log n)，分治策略（含迭代版优化，避免大数组栈溢出）

测试规模：n = 10, 100, 1000, 2000, 5000, 10000, 100000

---

### 二、0-1背包问题实验

实现并测试以下四种算法：
- **蛮力法**：枚举所有 2ⁿ 种组合，指数级复杂度
- **动态规划（DP）**：滚动数组优化，O(n×C)
- **贪心法**：按价值密度排序选取，O(n log n)
- **回溯法**：含上界剪枝优化

测试规模：n = 10~5000，容量 C = 10000 / 100000 / 1000000

---

## 项目结构

```
AlgorithmDesign/
├── code/                   # 源代码
│   ├── sorting.cpp         # C++ 排序算法实现（含比较计数器）
│   ├── knapsack.cpp        # C++ 背包算法实现
│   ├── step1_sorting.py    # 排序实验 Python 脚本
│   ├── step2_knapsack.py   # 背包实验 Python 脚本
│   ├── step3_charts.py     # matplotlib 图表生成脚本
│   ├── step4_excel.py      # openpyxl Excel 汇总脚本
│   ├── generate_report.js  # Node.js Word 报告生成脚本
│   └── install_deps.py     # 依赖安装脚本
├── data/                   # 实验数据
│   ├── sorting_results.csv      # 排序算法比较次数数据
│   ├── knapsack_results.csv    # 背包算法运行时间数据
│   ├── items_1000.csv          # 1000个物品详细数据
│   ├── subproblems_n10.txt    # n=10 子问题规模统计
│   ├── subproblems_n100.txt   # n=100 子问题规模统计
│   ├── subproblems_n1000.txt  # n=1000 子问题规模统计
│   └── 实验数据.xlsx            # Excel 数据汇总（含折线图）
├── charts/                 # 实验图表
│   ├── sorting_comparison.png         # 排序算法比较次数对比
│   ├── knapsack_time_comparison.png   # 背包算法时间对比
│   └── greedy_time_trend.png          # 贪心法时间趋势
├── report/                 # 实验报告
│   └── 实验报告.docx       # 完整 Word 实验报告
└── 实验报告.docx            # 报告副本
```

---

## 环境依赖

| 工具 | 版本 |
|------|------|
| Python | 3.13+ |
| Node.js | 22.x |
| matplotlib | 3.x |
| openpyxl | 3.x |
| docx (Node.js) | 9.x |

---

## 运行步骤

### 1. 安装 Python 依赖

```bash
pip install matplotlib openpyxl
```

### 2. 运行排序实验

```bash
python code/step1_sorting.py
```

生成 `data/sorting_results.csv`

### 3. 运行背包实验

```bash
python code/step2_knapsack.py
```

生成 `data/knapsack_results.csv`

### 4. 生成图表

```bash
python code/step3_charts.py
```

生成 `charts/` 目录下三张 PNG 图表

### 5. 生成 Excel 汇总

```bash
python code/step4_excel.py
```

生成 `data/实验数据.xlsx`

### 6. 生成 Word 实验报告

```bash
cd code
npm install docx
node generate_report.js
```

生成 `report/实验报告.docx`

---

## 主要实验结果

### 排序算法

| 规模 n | 冒泡排序（比较次数） | 归并排序（比较次数） | 快速排序（比较次数） |
|--------|-------------------|-------------------|-------------------|
| 10     | ~45               | ~25               | ~30               |
| 100    | ~4950             | ~664              | ~700              |
| 1000   | ~499500           | ~8966             | ~9500             |
| 10000  | ~49995000         | ~132877           | ~140000           |
| 100000 | ~4.99×10⁹         | ~1760918          | ~1.85×10⁶         |

> 冒泡排序比较次数约为 n(n-1)/2，归并与快速排序接近 O(n log n) 理论值。

### 背包算法

- **DP 算法**：n≤5000 且 C≤100000 时可在合理时间内完成
- **贪心算法**：效率最高，O(n log n)，但解不一定最优
- **回溯算法**：含上界剪枝，n≤30 可在合理时间内完成

---

## 实验结论

1. **排序算法**：冒泡排序在 n≥10000 时性能急剧下降；归并排序稳定且高效；快速排序平均性能最优，但最坏情况退化至 O(n²)。
2. **背包问题**：DP 算法能保证最优解但受容量限制；贪心算法速度快但可能非最优；回溯+剪枝在中小规模下表现良好。
3. **算法选择**：实际应用中需根据数据规模、最优性要求、时间限制综合选择算法。
