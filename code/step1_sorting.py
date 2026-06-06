"""
第一步：生成排序算法实验数据
"""
import random, csv, os, sys, time
from collections import Counter

os.makedirs('D:/AlgorithmDesign/data', exist_ok=True)

def generate_random(n, seed=42):
    rng = random.Random(seed)
    return [rng.randint(1, 1000000) for _ in range(n)]

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

def merge_sort(arr):
    sub_sizes = []
    cmp = [0]
    def _ms(arr, l, r):
        if l >= r: return
        sub_sizes.append(r - l + 1)
        m = (l + r) // 2
        _ms(arr, l, m)
        _ms(arr, m+1, r)
        L = arr[l:m+1]; R = arr[m+1:r+1]
        i = j = 0; k = l
        while i < len(L) and j < len(R):
            cmp[0] += 1
            if L[i] <= R[j]: arr[k] = L[i]; i += 1
            else: arr[k] = R[j]; j += 1
            k += 1
        while i < len(L): arr[k] = L[i]; i += 1; k += 1
        while j < len(R): arr[k] = R[j]; j += 1; k += 1
    arr = arr[:]
    sys.setrecursionlimit(300000)
    _ms(arr, 0, len(arr)-1)
    return arr, cmp[0], sub_sizes

def quick_sort_iterative(arr):
    """非递归快排，避免递归深度问题，同时记录子问题规模"""
    arr = arr[:]
    n = len(arr)
    cmp = [0]
    sub_sizes = []
    stack = [(0, n-1)]
    while stack:
        low, high = stack.pop()
        if low >= high: continue
        sub_sizes.append(high - low + 1)
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            cmp[0] += 1
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i+1], arr[high] = arr[high], arr[i+1]
        pi = i + 1
        stack.append((low, pi-1))
        stack.append((pi+1, high))
    return arr, cmp[0], sub_sizes

# ==========================================
# 任务①：100个随机数两次测试
# ==========================================
print("=" * 60)
print("任务①：100个随机数的两次测试")
print("=" * 60)
for trial in range(1, 3):
    arr = generate_random(100, seed=trial * 1000)
    print(f"\n--- 第{trial}次（前10个）: {arr[:10]}")
    _, bc = bubble_sort(arr)
    _, mc, _ = merge_sort(arr)
    _, qc, _ = quick_sort_iterative(arr)
    print(f"  冒泡比较次数: {bc}  归并比较次数: {mc}  快排比较次数: {qc}")

# ==========================================
# 任务②③：不同规模
# ==========================================
print("\n" + "=" * 60)
sizes = [10, 100, 1000, 2000, 5000, 10000, 100000]
rows = []
print(f"{'N':<8}{'冒泡':<14}{'归并':<14}{'快排':<14}{'归并子问题数':<14}{'快排子问题数'}")
print("-" * 78)
for n in sizes:
    arr = generate_random(n)
    _, bc = bubble_sort(arr) if n <= 10000 else (None, n*(n-1)//2)  # 10万冒泡太慢，用理论值
    if n == 100000:
        # 冒泡理论值（近似）
        bc = 4999950000  # n*(n-1)/2 ≈ O(n^2)
        print(f"  (n=100000 冒泡用理论值 n*(n-1)/2={bc})")
    _, mc, msub = merge_sort(arr)
    _, qc, qsub = quick_sort_iterative(arr)
    msc = len(msub)
    qsc = len(qsub)
    print(f"{n:<8}{bc:<14}{mc:<14}{qc:<14}{msc:<14}{qsc}")
    rows.append([n, bc, mc, qc, msc, qsc])

    # 保存子问题统计
    if n <= 1000:
        mc2 = Counter(msub); qc2 = Counter(qsub)
        with open(f'D:/AlgorithmDesign/data/subproblems_n{n}.txt','w',encoding='utf-8') as f:
            f.write(f"=== N={n} 归并排序子问题规模统计 ===\n")
            f.write(f"子问题总调用次数: {len(msub)}\n")
            for k in sorted(mc2): f.write(f"  规模 {k}: {mc2[k]} 个\n")
            f.write(f"\n=== N={n} 快速排序子问题规模统计 ===\n")
            f.write(f"子问题总调用次数: {len(qsub)}\n")
            for k in sorted(qc2): f.write(f"  规模 {k}: {qc2[k]} 个\n")

with open('D:/AlgorithmDesign/data/sorting_results.csv','w',newline='',encoding='utf-8-sig') as f:
    w = csv.writer(f)
    w.writerow(['N','BubbleCmp','MergeCmp','QuickCmp','MergeSubproblems','QuickSubproblems'])
    w.writerows(rows)
print("\n排序数据已保存！")
