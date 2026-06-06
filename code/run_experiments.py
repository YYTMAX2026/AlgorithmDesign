"""
算法实验数据生成脚本
实现排序和背包算法，生成实验数据CSV文件
"""
import random
import time
import csv
import os
import sys

# 确保输出目录存在
os.makedirs("D:/AlgorithmDesign/data", exist_ok=True)

# ============================================================
# 排序算法
# ============================================================
def bubble_sort(arr):
    arr = arr[:]
    n = len(arr)
    cnt = 0
    for i in range(n - 1):
        for j in range(n - i - 1):
            cnt += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr, cnt

def merge_sort(arr, subproblem_sizes=None):
    if subproblem_sizes is None:
        subproblem_sizes = []
    cmp_count = [0]

    def _merge(arr, left, right):
        if left >= right:
            return
        sub_size = right - left + 1
        subproblem_sizes.append(sub_size)
        mid = (left + right) // 2
        _merge(arr, left, mid)
        _merge(arr, mid + 1, right)
        L = arr[left:mid + 1]
        R = arr[mid + 1:right + 1]
        i = j = 0
        k = left
        while i < len(L) and j < len(R):
            cmp_count[0] += 1
            if L[i] <= R[j]:
                arr[k] = L[i]; i += 1
            else:
                arr[k] = R[j]; j += 1
            k += 1
        while i < len(L):
            arr[k] = L[i]; i += 1; k += 1
        while j < len(R):
            arr[k] = R[j]; j += 1; k += 1

    arr = arr[:]
    _merge(arr, 0, len(arr) - 1)
    return arr, cmp_count[0], subproblem_sizes

def quick_sort(arr, subproblem_sizes=None):
    if subproblem_sizes is None:
        subproblem_sizes = []
    cmp_count = [0]

    def _partition(arr, low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            cmp_count[0] += 1
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

    def _quick(arr, low, high):
        if low >= high:
            return
        sub_size = high - low + 1
        subproblem_sizes.append(sub_size)
        pi = _partition(arr, low, high)
        _quick(arr, low, pi - 1)
        _quick(arr, pi + 1, high)

    sys.setrecursionlimit(500000)
    arr = arr[:]
    _quick(arr, 0, len(arr) - 1)
    return arr, cmp_count[0], subproblem_sizes

def generate_random(n, seed=42):
    rng = random.Random(seed)
    return [rng.randint(1, 1000000) for _ in range(n)]

# ============================
# 任务①：100个随机数两次测试
# ============================
print("=" * 60)
print("任务①：100个随机数的两次测试")
print("=" * 60)
trial_results = []
for trial in range(1, 3):
    arr = generate_random(100, seed=trial * 1000)
    print(f"\n--- 第{trial}次测试数据（前20个）:")
    print(arr[:20])

    _, bc = bubble_sort(arr)
    _, mc, _ = merge_sort(arr)
    _, qc, _ = quick_sort(arr)

    print(f"冒泡排序比较次数: {bc}")
    print(f"归并排序比较次数: {mc}")
    print(f"快速排序比较次数: {qc}")
    trial_results.append({'trial': trial, 'data': arr[:20], 'bubble': bc, 'merge': mc, 'quick': qc})

# ============================
# 任务②③：不同规模测试
# ============================
print("\n" + "=" * 60)
print("任务②③：不同规模测试")
print("=" * 60)
sizes = [10, 100, 1000, 2000, 5000, 10000, 100000]
print(f"{'规模N':<10} {'冒泡比较次数':<16} {'归并比较次数':<16} {'快排比较次数':<16} {'归并子问题数':<14} {'快排子问题数':<14}")
print("-" * 86)

sorting_rows = []
subproblem_data = {}  # n -> {merge_sizes, quick_sizes}

for n in sizes:
    arr = generate_random(n)
    m_sub = []
    q_sub = []

    _, bc = bubble_sort(arr)
    _, mc, m_sub = merge_sort(arr)
    _, qc, q_sub = quick_sort(arr)

    merge_sub_cnt = len(m_sub)
    quick_sub_cnt = len(q_sub)
    print(f"{n:<10} {bc:<16} {mc:<16} {qc:<16} {merge_sub_cnt:<14} {quick_sub_cnt:<14}")
    sorting_rows.append([n, bc, mc, qc, merge_sub_cnt, quick_sub_cnt])

    if n <= 1000:
        subproblem_data[n] = {'merge': m_sub, 'quick': q_sub}

# 保存排序结果CSV
with open("D:/AlgorithmDesign/data/sorting_results.csv", "w", newline='', encoding='utf-8-sig') as f:
    w = csv.writer(f)
    w.writerow(["N", "BubbleCmp", "MergeCmp", "QuickCmp", "MergeSubproblems", "QuickSubproblems"])
    w.writerows(sorting_rows)
print("\n排序数据已保存到 D:/AlgorithmDesign/data/sorting_results.csv")

# 保存子问题规模统计
for n, data in subproblem_data.items():
    fname = f"D:/AlgorithmDesign/data/subproblems_n{n}.txt"
    from collections import Counter
    with open(fname, "w", encoding='utf-8') as f:
        f.write(f"=== N={n} 归并排序子问题规模统计 ===\n")
        mc = Counter(data['merge'])
        f.write(f"子问题总调用次数: {len(data['merge'])}\n")
        for k in sorted(mc.keys()):
            f.write(f"  规模 {k}: {mc[k]} 个\n")
        f.write(f"\n=== N={n} 快速排序子问题规模统计 ===\n")
        qc = Counter(data['quick'])
        f.write(f"子问题总调用次数: {len(data['quick'])}\n")
        for k in sorted(qc.keys()):
            f.write(f"  规模 {k}: {qc[k]} 个\n")
    print(f"子问题规模数据已保存: {fname}")

# ============================================================
# 0-1背包问题算法
# ============================================================
print("\n" + "=" * 60)
print("0-1背包问题数据生成")
print("=" * 60)

def generate_items(n, seed=42):
    rng = random.Random(seed)
    items = []
    for i in range(n):
        w = rng.randint(1, 100)
        v = round(rng.uniform(100.0, 1000.0), 2)
        items.append({'id': i+1, 'weight': w, 'value': v})
    return items

# 保存1000个物品数据（表1）
items_1000 = generate_items(1000)
with open("D:/AlgorithmDesign/data/items_1000.csv", "w", newline='', encoding='utf-8-sig') as f:
    w = csv.writer(f)
    w.writerow(["物品编号", "物品重量", "物品价值"])
    for it in items_1000:
        w.writerow([it['id'], it['weight'], f"{it['value']:.2f}"])
print("1000个物品数据已保存: D:/AlgorithmDesign/data/items_1000.csv")

# ---------- 动态规划 ----------
def dp_knapsack(items, capacity):
    n = len(items)
    # 使用滚动数组
    dp = [0.0] * (capacity + 1)
    keep = [[False] * (capacity + 1) for _ in range(n)]
    for i, item in enumerate(items):
        w, v = item['weight'], item['value']
        for j in range(capacity, w - 1, -1):
            if dp[j - w] + v > dp[j]:
                dp[j] = dp[j - w] + v
                keep[i][j] = True
    total_val = dp[capacity]
    # 回溯
    chosen = []
    j = capacity
    for i in range(n - 1, -1, -1):
        if keep[i][j]:
            chosen.append(i)
            j -= items[i]['weight']
    total_w = sum(items[i]['weight'] for i in chosen)
    return total_val, total_w, len(chosen)

# ---------- 贪心 ----------
def greedy_knapsack(items, capacity):
    order = sorted(range(len(items)), key=lambda i: items[i]['value'] / items[i]['weight'], reverse=True)
    total_v = 0.0; total_w = 0; chosen = []; remain = capacity
    for idx in order:
        if items[idx]['weight'] <= remain:
            chosen.append(idx)
            remain -= items[idx]['weight']
            total_w += items[idx]['weight']
            total_v += items[idx]['value']
    return total_v, total_w, len(chosen)

# ---------- 回溯（带上界剪枝）----------
def backtrack_knapsack(items, capacity):
    n = len(items)
    order = sorted(range(n), key=lambda i: items[i]['value'] / items[i]['weight'], reverse=True)
    sorted_items = [items[i] for i in order]

    def upper_bound(idx, remain, cur_v):
        b = cur_v
        for i in range(idx, n):
            if sorted_items[i]['weight'] <= remain:
                remain -= sorted_items[i]['weight']
                b += sorted_items[i]['value']
            else:
                b += remain / sorted_items[i]['weight'] * sorted_items[i]['value']
                break
        return b

    best = [0.0]
    best_chosen = [[]]
    current = []

    def bt(idx, remain, cur_v):
        if idx == n:
            if cur_v > best[0]:
                best[0] = cur_v
                best_chosen[0] = current[:]
            return
        if upper_bound(idx, remain, cur_v) <= best[0]:
            return
        item = sorted_items[idx]
        if item['weight'] <= remain:
            current.append(order[idx])
            bt(idx + 1, remain - item['weight'], cur_v + item['value'])
            current.pop()
        bt(idx + 1, remain, cur_v)

    sys.setrecursionlimit(500000)
    bt(0, capacity, 0.0)
    total_w = sum(items[i]['weight'] for i in best_chosen[0])
    return best[0], total_w, len(best_chosen[0])

# ---------- 主测试 ----------
n_list = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000,
          10000, 20000, 40000, 80000, 160000, 320000]
c_list = [10000, 100000, 1000000]

knapsack_rows = []

for capacity in c_list:
    print(f"\n--- 背包容量 C={capacity} ---")
    for n in n_list:
        items = generate_items(n)

        # 动态规划（n<=10000, capacity<=100000）
        if n <= 10000 and capacity <= 100000:
            t0 = time.time()
            val, tw, sc = dp_knapsack(items, capacity)
            t1 = time.time()
            ms = int((t1 - t0) * 1000)
            print(f"  DP     n={n:<7} val={val:>12.2f}  tw={tw:<7} selected={sc:<6} time={ms}ms")
            knapsack_rows.append(["DynamicProgramming", n, capacity, f"{val:.2f}", tw, sc, ms])

        # 贪心（全规模）
        t0 = time.time()
        val, tw, sc = greedy_knapsack(items, capacity)
        t1 = time.time()
        ms = int((t1 - t0) * 1000)
        print(f"  Greedy n={n:<7} val={val:>12.2f}  tw={tw:<7} selected={sc:<6} time={ms}ms")
        knapsack_rows.append(["Greedy", n, capacity, f"{val:.2f}", tw, sc, ms])

        # 回溯（n<=3000，避免超时）
        if n <= 3000:
            t0 = time.time()
            val, tw, sc = backtrack_knapsack(items, capacity)
            t1 = time.time()
            ms = int((t1 - t0) * 1000)
            print(f"  BT     n={n:<7} val={val:>12.2f}  tw={tw:<7} selected={sc:<6} time={ms}ms")
            knapsack_rows.append(["Backtrack", n, capacity, f"{val:.2f}", tw, sc, ms])

with open("D:/AlgorithmDesign/data/knapsack_results.csv", "w", newline='', encoding='utf-8-sig') as f:
    w = csv.writer(f)
    w.writerow(["Algorithm", "N", "Capacity", "TotalValue", "TotalWeight", "SelectedCount", "TimeMs"])
    w.writerows(knapsack_rows)
print("\n背包问题结果已保存到 D:/AlgorithmDesign/data/knapsack_results.csv")
print("\n所有实验数据生成完毕！")
