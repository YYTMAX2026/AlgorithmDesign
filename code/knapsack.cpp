/*
 * 0-1背包问题 - 四种算法实现
 * 蛮力法 / 动态规划法 / 贪心法 / 回溯法
 * 云南大学信息学院《算法设计与分析》2026春季学期
 */

#include <iostream>
#include <fstream>
#include <vector>
#include <random>
#include <chrono>
#include <algorithm>
#include <numeric>
#include <iomanip>
#include <cstring>
#include <map>
using namespace std;

// ============================================================
// 数据结构
// ============================================================
struct Item {
    int    id;
    int    weight;   // 重量 1~100
    double value;    // 价值 100.00~1000.00（保留两位小数）
};

// ============================================================
// 生成随机物品
// ============================================================
vector<Item> generateItems(int n, int seed = 42) {
    mt19937 rng(seed);
    uniform_int_distribution<int>    wdist(1, 100);
    uniform_real_distribution<double> vdist(100.0, 1000.0);
    vector<Item> items(n);
    for (int i = 0; i < n; i++) {
        items[i].id     = i + 1;
        items[i].weight = wdist(rng);
        // 保留两位小数
        items[i].value  = round(vdist(rng) * 100.0) / 100.0;
    }
    return items;
}

// ============================================================
// 1. 蛮力法 (仅适用于小规模，n<=25)
// ============================================================
struct KnapsackResult {
    double totalValue = 0;
    int    totalWeight = 0;
    vector<int> chosen; // 选中物品的下标（0-based）
    long long execTimeMs = 0;
};

KnapsackResult bruteForce(const vector<Item>& items, int capacity) {
    int n = items.size();
    KnapsackResult best;
    long long total = 1LL << n;
    for (long long mask = 0; mask < total; mask++) {
        int w = 0; double v = 0;
        vector<int> chosen;
        for (int i = 0; i < n; i++) {
            if (mask >> i & 1) {
                w += items[i].weight;
                v += items[i].value;
                chosen.push_back(i);
            }
        }
        if (w <= capacity && v > best.totalValue) {
            best.totalValue  = v;
            best.totalWeight = w;
            best.chosen      = chosen;
        }
    }
    return best;
}

// ============================================================
// 2. 动态规划法
// ============================================================
KnapsackResult dynamicProgramming(const vector<Item>& items, int capacity) {
    int n = items.size();
    // 为避免超内存，当n*capacity很大时使用滚动数组（只记录最优值）
    // 这里对n<=3000且capacity<=1000000时做精确DP
    // 若capacity过大则使用估算（贪心）代替
    long long tableSize = (long long)(n + 1) * (capacity + 1);
    KnapsackResult res;

    if (tableSize > 200000000LL) {
        // 容量太大，用近似处理：按价值密度排序近似
        // 此分支实际上不会被主程序调用（主程序对大规模只调用贪心）
        res.totalValue = -1;
        return res;
    }

    // 滚动数组 DP
    vector<double> dp(capacity + 1, 0.0);
    vector<vector<bool>> keep(n, vector<bool>(capacity + 1, false));

    for (int i = 0; i < n; i++) {
        int w = items[i].weight;
        double v = items[i].value;
        for (int j = capacity; j >= w; j--) {
            if (dp[j - w] + v > dp[j]) {
                dp[j] = dp[j - w] + v;
                keep[i][j] = true;
            }
        }
    }

    res.totalValue = dp[capacity];

    // 回溯选择的物品
    int j = capacity;
    for (int i = n - 1; i >= 0; i--) {
        if (keep[i][j]) {
            res.chosen.push_back(i);
            j -= items[i].weight;
        }
    }
    for (int idx : res.chosen) res.totalWeight += items[idx].weight;
    return res;
}

// ============================================================
// 3. 贪心法（按价值/重量比降序）
// ============================================================
KnapsackResult greedySolve(const vector<Item>& items, int capacity) {
    int n = items.size();
    vector<int> order(n);
    iota(order.begin(), order.end(), 0);
    sort(order.begin(), order.end(), [&](int a, int b){
        return (double)items[a].value / items[a].weight
             > (double)items[b].value / items[b].weight;
    });

    KnapsackResult res;
    int remain = capacity;
    for (int idx : order) {
        if (items[idx].weight <= remain) {
            res.chosen.push_back(idx);
            remain -= items[idx].weight;
            res.totalWeight += items[idx].weight;
            res.totalValue  += items[idx].value;
        }
    }
    return res;
}

// ============================================================
// 4. 回溯法（带上界剪枝，适用于中等规模）
// ============================================================
static double bt_bestValue;
static int    bt_capacity;
static int    bt_n;
static vector<Item>* bt_items_ptr;
static vector<int>   bt_currentChosen;
static vector<int>   bt_bestChosen;
static vector<int>   bt_sortedOrder; // 按价值密度排序的下标

// 计算上界（用分数背包贪心）
double upperBound(int idx, int remainCap, double curValue) {
    double bound = curValue;
    int remain = remainCap;
    for (int i = idx; i < bt_n && remain > 0; i++) {
        int origIdx = bt_sortedOrder[i];
        if (bt_items_ptr->at(origIdx).weight <= remain) {
            remain -= bt_items_ptr->at(origIdx).weight;
            bound  += bt_items_ptr->at(origIdx).value;
        } else {
            bound += (double)remain / bt_items_ptr->at(origIdx).weight
                   * bt_items_ptr->at(origIdx).value;
            remain = 0;
        }
    }
    return bound;
}

void backtrack(int idx, int remainCap, double curValue) {
    if (idx == bt_n) {
        if (curValue > bt_bestValue) {
            bt_bestValue  = curValue;
            bt_bestChosen = bt_currentChosen;
        }
        return;
    }
    // 剪枝
    if (upperBound(idx, remainCap, curValue) <= bt_bestValue) return;

    int origIdx = bt_sortedOrder[idx];
    // 选当前物品
    if (remainCap >= bt_items_ptr->at(origIdx).weight) {
        bt_currentChosen.push_back(origIdx);
        backtrack(idx + 1,
                  remainCap - bt_items_ptr->at(origIdx).weight,
                  curValue  + bt_items_ptr->at(origIdx).value);
        bt_currentChosen.pop_back();
    }
    // 不选当前物品
    backtrack(idx + 1, remainCap, curValue);
}

KnapsackResult backtrackSolve(const vector<Item>& items, int capacity) {
    bt_n = items.size();
    bt_capacity = capacity;
    bt_items_ptr = const_cast<vector<Item>*>(&items);
    bt_bestValue = 0;
    bt_currentChosen.clear();
    bt_bestChosen.clear();

    // 按价值密度排序
    bt_sortedOrder.resize(bt_n);
    iota(bt_sortedOrder.begin(), bt_sortedOrder.end(), 0);
    sort(bt_sortedOrder.begin(), bt_sortedOrder.end(), [&](int a, int b){
        return (double)items[a].value / items[a].weight
             > (double)items[b].value / items[b].weight;
    });

    backtrack(0, capacity, 0.0);

    KnapsackResult res;
    res.totalValue  = bt_bestValue;
    res.chosen      = bt_bestChosen;
    for (int idx : res.chosen) res.totalWeight += items[idx].weight;
    return res;
}

// ============================================================
// 格式化输出结果
// ============================================================
void printResult(const string& algoName, const KnapsackResult& r,
                 const vector<Item>& items, int n_show = 10) {
    cout << "\n[" << algoName << "] 总价值=" << fixed << setprecision(2)
         << r.totalValue << "  总重量=" << r.totalWeight
         << "  执行时间=" << r.execTimeMs << "ms" << endl;
    cout << "  选中物品数: " << r.chosen.size() << endl;
    if (!r.chosen.empty()) {
        cout << "  前" << min(n_show,(int)r.chosen.size()) << "件物品: ";
        for (int i = 0; i < min(n_show,(int)r.chosen.size()); i++) {
            int idx = r.chosen[i];
            cout << "(id=" << items[idx].id << " w=" << items[idx].weight
                 << " v=" << fixed << setprecision(2) << items[idx].value << ") ";
        }
        cout << endl;
    }
}

// ============================================================
// 主程序
// ============================================================
int main() {
    // 物品规模列表
    vector<int> nList = {1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000,
                         10000, 20000, 40000, 80000, 160000, 320000};
    // 背包容量列表
    vector<int> cList = {10000, 100000, 1000000};

    // 结果CSV文件
    ofstream csv("../data/knapsack_results.csv");
    csv << "Algorithm,N,Capacity,TotalValue,TotalWeight,SelectedCount,TimeMs\n";

    // 1000个物品的详细数据（用于表1）
    {
        cout << "生成1000个物品的详细数据..." << endl;
        vector<Item> items1000 = generateItems(1000);
        ofstream f1000("../data/items_1000.csv");
        f1000 << "物品编号,物品重量,物品价值\n";
        for (auto& it : items1000)
            f1000 << it.id << "," << it.weight << ","
                  << fixed << setprecision(2) << it.value << "\n";
        f1000.close();
        cout << "已保存 data/items_1000.csv" << endl;
    }

    // 测试各算法
    for (int capacity : cList) {
        cout << "\n========== 背包容量 C=" << capacity << " ==========" << endl;
        for (int n : nList) {
            vector<Item> items = generateItems(n);

            // ---- 蛮力法（仅n<=20时运行）----
            if (n <= 20) {
                auto t0 = chrono::high_resolution_clock::now();
                KnapsackResult r = bruteForce(items, capacity);
                auto t1 = chrono::high_resolution_clock::now();
                r.execTimeMs = chrono::duration_cast<chrono::milliseconds>(t1-t0).count();
                cout << "BF n=" << n << " C=" << capacity;
                printResult("蛮力法", r, items);
                csv << "BruteForce," << n << "," << capacity << ","
                    << fixed << setprecision(2) << r.totalValue << ","
                    << r.totalWeight << "," << r.chosen.size() << "," << r.execTimeMs << "\n";
            }

            // ---- 动态规划法（n<=10000且capacity<=100000）----
            if (n <= 10000 && capacity <= 100000) {
                auto t0 = chrono::high_resolution_clock::now();
                KnapsackResult r = dynamicProgramming(items, capacity);
                auto t1 = chrono::high_resolution_clock::now();
                r.execTimeMs = chrono::duration_cast<chrono::milliseconds>(t1-t0).count();
                cout << "DP n=" << n << " C=" << capacity << " val="
                     << fixed << setprecision(2) << r.totalValue
                     << " time=" << r.execTimeMs << "ms" << endl;
                csv << "DynamicProgramming," << n << "," << capacity << ","
                    << fixed << setprecision(2) << r.totalValue << ","
                    << r.totalWeight << "," << r.chosen.size() << "," << r.execTimeMs << "\n";
            }

            // ---- 贪心法（全规模）----
            {
                auto t0 = chrono::high_resolution_clock::now();
                KnapsackResult r = greedySolve(items, capacity);
                auto t1 = chrono::high_resolution_clock::now();
                r.execTimeMs = chrono::duration_cast<chrono::milliseconds>(t1-t0).count();
                cout << "Greedy n=" << n << " C=" << capacity << " val="
                     << fixed << setprecision(2) << r.totalValue
                     << " time=" << r.execTimeMs << "ms" << endl;
                csv << "Greedy," << n << "," << capacity << ","
                    << fixed << setprecision(2) << r.totalValue << ","
                    << r.totalWeight << "," << r.chosen.size() << "," << r.execTimeMs << "\n";
            }

            // ---- 回溯法（n<=2000）----
            if (n <= 2000) {
                auto t0 = chrono::high_resolution_clock::now();
                KnapsackResult r = backtrackSolve(items, capacity);
                auto t1 = chrono::high_resolution_clock::now();
                r.execTimeMs = chrono::duration_cast<chrono::milliseconds>(t1-t0).count();
                cout << "BT n=" << n << " C=" << capacity << " val="
                     << fixed << setprecision(2) << r.totalValue
                     << " time=" << r.execTimeMs << "ms" << endl;
                csv << "Backtrack," << n << "," << capacity << ","
                    << fixed << setprecision(2) << r.totalValue << ","
                    << r.totalWeight << "," << r.chosen.size() << "," << r.execTimeMs << "\n";
            }
        }
    }

    csv.close();
    cout << "\n所有结果已保存到 ../data/knapsack_results.csv" << endl;
    return 0;
}
