"""
第二步：生成0-1背包问题实验数据
蛮力法(小规模) / 动态规划 / 贪心 / 回溯
"""
import random, csv, os, sys, time

os.makedirs('D:/AlgorithmDesign/data', exist_ok=True)

def gen_items(n, seed=42):
    rng = random.Random(seed)
    return [{'id': i+1, 'w': rng.randint(1,100),
             'v': round(rng.uniform(100.0, 1000.0), 2)} for i in range(n)]

# ---- 动态规划（精确解）----
def dp_knap(items, C):
    n = len(items)
    dp = [0.0] * (C + 1)
    keep = [[False]*(C+1) for _ in range(n)]
    for i, it in enumerate(items):
        w, v = it['w'], it['v']
        for j in range(C, w-1, -1):
            if dp[j-w] + v > dp[j]:
                dp[j] = dp[j-w] + v
                keep[i][j] = True
    chosen = []
    j = C
    for i in range(n-1, -1, -1):
        if keep[i][j]:
            chosen.append(i)
            j -= items[i]['w']
    tv = dp[C]
    tw = sum(items[i]['w'] for i in chosen)
    return tv, tw, len(chosen)

# ---- 贪心 ----
def greedy_knap(items, C):
    order = sorted(range(len(items)), key=lambda i: items[i]['v']/items[i]['w'], reverse=True)
    tv = 0.0; tw = 0; sc = 0; rem = C
    for idx in order:
        if items[idx]['w'] <= rem:
            rem -= items[idx]['w']
            tw += items[idx]['w']
            tv += items[idx]['v']
            sc += 1
    return tv, tw, sc

# ---- 回溯（带剪枝）----
def bt_knap(items, C):
    n = len(items)
    order = sorted(range(n), key=lambda i: items[i]['v']/items[i]['w'], reverse=True)
    si = [items[i] for i in order]
    def ub(idx, rem, cv):
        b = cv
        for i in range(idx, n):
            if si[i]['w'] <= rem:
                rem -= si[i]['w']; b += si[i]['v']
            else:
                b += rem/si[i]['w']*si[i]['v']; break
        return b
    best = [0.0]; bc = [[]]
    cur = []
    def bt(idx, rem, cv):
        if idx == n:
            if cv > best[0]: best[0]=cv; bc[0]=cur[:]
            return
        if ub(idx, rem, cv) <= best[0]: return
        it = si[idx]
        if it['w'] <= rem:
            cur.append(order[idx])
            bt(idx+1, rem-it['w'], cv+it['v'])
            cur.pop()
        bt(idx+1, rem, cv)
    sys.setrecursionlimit(500000)
    bt(0, C, 0.0)
    tv = best[0]
    tw = sum(items[i]['w'] for i in bc[0])
    return tv, tw, len(bc[0])

# 保存1000个物品详细数据
items_1000 = gen_items(1000)
with open('D:/AlgorithmDesign/data/items_1000.csv','w',newline='',encoding='utf-8-sig') as f:
    w = csv.writer(f)
    w.writerow(['物品编号','物品重量','物品价值'])
    for it in items_1000:
        w.writerow([it['id'], it['w'], f"{it['v']:.2f}"])
print('items_1000.csv 已保存')

# 主测试
n_list = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000,
          10000, 20000, 40000, 80000, 160000, 320000]
c_list = [10000, 100000, 1000000]

rows = []
for C in c_list:
    print(f'\n===== C={C} =====')
    for n in n_list:
        items = gen_items(n)

        # 动态规划（n<=5000 且 C<=100000）
        if n <= 5000 and C <= 100000:
            t0 = time.perf_counter()
            tv, tw, sc = dp_knap(items, C)
            ms = int((time.perf_counter()-t0)*1000)
            print(f'  DP     n={n:<7} val={tv:>12.2f} tw={tw:<6} sc={sc:<5} {ms}ms', flush=True)
            rows.append(['DynamicProgramming', n, C, f'{tv:.2f}', tw, sc, ms])

        # 贪心（全规模）
        t0 = time.perf_counter()
        tv, tw, sc = greedy_knap(items, C)
        ms = int((time.perf_counter()-t0)*1000)
        print(f'  Greedy n={n:<7} val={tv:>12.2f} tw={tw:<6} sc={sc:<5} {ms}ms', flush=True)
        rows.append(['Greedy', n, C, f'{tv:.2f}', tw, sc, ms])

        # 回溯（n<=2000）
        if n <= 2000:
            t0 = time.perf_counter()
            tv, tw, sc = bt_knap(items, C)
            ms = int((time.perf_counter()-t0)*1000)
            print(f'  BT     n={n:<7} val={tv:>12.2f} tw={tw:<6} sc={sc:<5} {ms}ms', flush=True)
            rows.append(['Backtrack', n, C, f'{tv:.2f}', tw, sc, ms])

with open('D:/AlgorithmDesign/data/knapsack_results.csv','w',newline='',encoding='utf-8-sig') as f:
    w = csv.writer(f)
    w.writerow(['Algorithm','N','Capacity','TotalValue','TotalWeight','SelectedCount','TimeMs'])
    w.writerows(rows)
print('\n背包问题数据已保存！')
