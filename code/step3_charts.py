"""
生成实验图表
1. 排序算法比较次数对比折线图
2. 背包问题各算法执行时间对比图
"""
import csv, os, math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# 中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

os.makedirs('D:/AlgorithmDesign/charts', exist_ok=True)

# =====================================================
# 图1：排序算法比较次数对比（线性坐标）
# =====================================================
with open('D:/AlgorithmDesign/data/sorting_results.csv', encoding='utf-8-sig') as f:
    rows = list(csv.DictReader(f))

Ns      = [int(r['N']) for r in rows]
bubble  = [int(r['BubbleCmp']) for r in rows]
merge_c = [int(r['MergeCmp']) for r in rows]
quick_c = [int(r['QuickCmp']) for r in rows]

# 理论曲线（归一化）
def theory_n2(n):   return n*(n-1)/2
def theory_nlogn(n): return n * math.log2(n) if n > 1 else 0

t_bubble  = [theory_n2(n) for n in Ns]
t_nlogn   = [theory_nlogn(n) for n in Ns]

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# 左图：对数坐标
ax = axes[0]
ax.plot(Ns, bubble,  'r-o', label='冒泡排序（实测）', linewidth=2, markersize=5)
ax.plot(Ns, merge_c, 'b-s', label='归并排序（实测）', linewidth=2, markersize=5)
ax.plot(Ns, quick_c, 'g-^', label='快速排序（实测）', linewidth=2, markersize=5)
ax.plot(Ns, t_bubble, 'r--', label='O(n²)理论', alpha=0.5)
ax.plot(Ns, t_nlogn,  'b--', label='O(nlogn)理论', alpha=0.5)
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('输入规模 n（对数）', fontsize=12)
ax.set_ylabel('比较次数（对数）', fontsize=12)
ax.set_title('排序算法比较次数对比（对数坐标）', fontsize=13)
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3)
ax.set_xticks(Ns)
ax.get_xaxis().set_major_formatter(ticker.ScalarFormatter())

# 右图：仅中小规模（n<=10000）线性坐标
ax2 = axes[1]
idx_small = [i for i,n in enumerate(Ns) if n <= 10000]
Ns_s  = [Ns[i] for i in idx_small]
b_s   = [bubble[i] for i in idx_small]
m_s   = [merge_c[i] for i in idx_small]
q_s   = [quick_c[i] for i in idx_small]
ax2.plot(Ns_s, b_s, 'r-o', label='冒泡排序', linewidth=2)
ax2.plot(Ns_s, m_s, 'b-s', label='归并排序', linewidth=2)
ax2.plot(Ns_s, q_s, 'g-^', label='快速排序', linewidth=2)
ax2.set_xlabel('输入规模 n', fontsize=12)
ax2.set_ylabel('比较次数', fontsize=12)
ax2.set_title('排序算法比较次数对比（n≤10000，线性坐标）', fontsize=13)
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.3)

fig.tight_layout()
fig.savefig('D:/AlgorithmDesign/charts/sorting_comparison.png', dpi=150, bbox_inches='tight')
print('图1已保存：sorting_comparison.png')
plt.close(fig)

# =====================================================
# 图2：背包问题各算法执行时间对比
# =====================================================
with open('D:/AlgorithmDesign/data/knapsack_results.csv', encoding='utf-8-sig') as f:
    krows = list(csv.DictReader(f))

algos = ['DynamicProgramming', 'Greedy', 'Backtrack']
algo_labels = {'DynamicProgramming': '动态规划', 'Greedy': '贪心法', 'Backtrack': '回溯法'}
colors = {'DynamicProgramming': 'blue', 'Greedy': 'green', 'Backtrack': 'orange'}
markers = {'DynamicProgramming': 's', 'Greedy': '^', 'Backtrack': 'D'}

capacities = [10000, 100000, 1000000]

fig2, axes2 = plt.subplots(1, 3, figsize=(18, 5))

for ci, cap in enumerate(capacities):
    ax = axes2[ci]
    data = {}
    for algo in algos:
        ns = []; ts = []
        for r in krows:
            if r['Algorithm'] == algo and int(r['Capacity']) == cap:
                ns.append(int(r['N']))
                ts.append(int(r['TimeMs']))
        if ns:
            data[algo] = (ns, ts)

    for algo in algos:
        if algo in data:
            ns, ts = data[algo]
            ax.plot(ns, ts, color=colors[algo], marker=markers[algo],
                    label=algo_labels[algo], linewidth=2, markersize=5)

    ax.set_xlabel('物品数量 n', fontsize=11)
    ax.set_ylabel('执行时间 (ms)', fontsize=11)
    ax.set_title(f'背包容量 C={cap:,}', fontsize=12)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

fig2.suptitle('0-1背包问题各算法执行时间对比', fontsize=14, y=1.01)
fig2.tight_layout()
fig2.savefig('D:/AlgorithmDesign/charts/knapsack_time_comparison.png', dpi=150, bbox_inches='tight')
print('图2已保存：knapsack_time_comparison.png')
plt.close(fig2)

# =====================================================
# 图3：贪心法全规模趋势（大规模）
# =====================================================
fig3, ax3 = plt.subplots(figsize=(10, 5))
for cap in capacities:
    ns = []; ts = []
    for r in krows:
        if r['Algorithm'] == 'Greedy' and int(r['Capacity']) == cap:
            ns.append(int(r['N']))
            ts.append(int(r['TimeMs']))
    ax3.plot(ns, ts, marker='o', label=f'C={cap:,}', linewidth=2, markersize=5)

ax3.set_xlabel('物品数量 n', fontsize=12)
ax3.set_ylabel('执行时间 (ms)', fontsize=12)
ax3.set_title('贪心法：不同背包容量下执行时间趋势', fontsize=13)
ax3.legend(fontsize=10)
ax3.grid(True, alpha=0.3)
fig3.tight_layout()
fig3.savefig('D:/AlgorithmDesign/charts/greedy_time_trend.png', dpi=150, bbox_inches='tight')
print('图3已保存：greedy_time_trend.png')
plt.close(fig3)

print('\n所有图表生成完毕！')
