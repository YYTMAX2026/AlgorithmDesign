/*
 * 排序算法实验 - 冒泡排序、归并排序、快速排序
 * 记录比较操作次数，分析不同输入规模下的算法性能
 * 云南大学信息学院《算法设计与分析》2026春季学期
 */

#include <iostream>
#include <fstream>
#include <vector>
#include <random>
#include <chrono>
#include <cstring>
#include <iomanip>
using namespace std;

// ======================== 全局计数器 ========================
long long bubble_cmp_count = 0;   // 冒泡排序比较次数
long long merge_cmp_count  = 0;   // 归并排序比较次数
long long quick_cmp_count  = 0;   // 快速排序比较次数

// 归并排序子问题规模记录
vector<int> merge_subproblem_sizes;
// 快速排序子问题规模记录
vector<int> quick_subproblem_sizes;

// ======================== 冒泡排序 ========================
void bubbleSort(vector<int>& arr) {
    int n = arr.size();
    bubble_cmp_count = 0;
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            bubble_cmp_count++;
            if (arr[j] > arr[j + 1]) {
                swap(arr[j], arr[j + 1]);
            }
        }
    }
}

// ======================== 归并排序 ========================
void merge(vector<int>& arr, int left, int mid, int right) {
    vector<int> L(arr.begin() + left, arr.begin() + mid + 1);
    vector<int> R(arr.begin() + mid + 1, arr.begin() + right + 1);
    int i = 0, j = 0, k = left;
    while (i < (int)L.size() && j < (int)R.size()) {
        merge_cmp_count++;
        if (L[i] <= R[j]) arr[k++] = L[i++];
        else               arr[k++] = R[j++];
    }
    while (i < (int)L.size()) arr[k++] = L[i++];
    while (j < (int)R.size()) arr[k++] = R[j++];
}

void mergeSort(vector<int>& arr, int left, int right) {
    if (left >= right) return;
    int subSize = right - left + 1;
    merge_subproblem_sizes.push_back(subSize);  // 记录子问题规模
    int mid = left + (right - left) / 2;
    mergeSort(arr, left, mid);
    mergeSort(arr, mid + 1, right);
    merge(arr, left, mid, right);
}

// ======================== 快速排序 ========================
int partition(vector<int>& arr, int low, int high) {
    int pivot = arr[high];
    int i = low - 1;
    for (int j = low; j < high; j++) {
        quick_cmp_count++;
        if (arr[j] <= pivot) {
            i++;
            swap(arr[i], arr[j]);
        }
    }
    swap(arr[i + 1], arr[high]);
    return i + 1;
}

void quickSort(vector<int>& arr, int low, int high) {
    if (low >= high) return;
    int subSize = high - low + 1;
    quick_subproblem_sizes.push_back(subSize);  // 记录子问题规模
    int pi = partition(arr, low, high);
    quickSort(arr, low, pi - 1);
    quickSort(arr, pi + 1, high);
}

// ======================== 生成随机数 ========================
vector<int> generateRandom(int n, int seed = 42) {
    mt19937 rng(seed);
    uniform_int_distribution<int> dist(1, 1000000);
    vector<int> arr(n);
    for (int& x : arr) x = dist(rng);
    return arr;
}

// ======================== 主测试函数 ========================
int main() {
    // 任务①：生成两次100个随机数，比较比较次数
    cout << "========== 任务①：100个随机数的两次测试 ==========" << endl;
    for (int trial = 1; trial <= 2; trial++) {
        vector<int> arr = generateRandom(100, trial * 1000);
        cout << "\n--- 第" << trial << "次测试数据（前20个）: ";
        for (int i = 0; i < 20; i++) cout << arr[i] << " ";
        cout << "..." << endl;

        // 冒泡排序
        vector<int> b = arr;
        bubbleSort(b);
        long long bc = bubble_cmp_count;

        // 归并排序
        vector<int> m = arr;
        merge_cmp_count = 0;
        merge_subproblem_sizes.clear();
        mergeSort(m, 0, (int)m.size() - 1);
        long long mc = merge_cmp_count;

        // 快速排序
        vector<int> q = arr;
        quick_cmp_count = 0;
        quick_subproblem_sizes.clear();
        quickSort(q, 0, (int)q.size() - 1);
        long long qc = quick_cmp_count;

        cout << "冒泡排序比较次数: " << bc << endl;
        cout << "归并排序比较次数: " << mc << endl;
        cout << "快速排序比较次数: " << qc << endl;
    }

    // 任务②③：不同规模测试数据
    vector<int> sizes = {10, 100, 1000, 2000, 5000, 10000, 100000};
    cout << "\n========== 任务②③：不同规模测试 ==========" << endl;
    cout << left << setw(10) << "规模N"
         << setw(16) << "冒泡比较次数"
         << setw(16) << "归并比较次数"
         << setw(16) << "快排比较次数" << endl;
    cout << string(58, '-') << endl;

    // 输出到CSV文件
    ofstream csv("../data/sorting_results.csv");
    csv << "N,BubbleCmp,MergeCmp,QuickCmp,MergeSubproblems,QuickSubproblems" << endl;

    for (int n : sizes) {
        vector<int> arr = generateRandom(n);

        // 冒泡排序
        vector<int> b = arr;
        bubble_cmp_count = 0;
        bubbleSort(b);
        long long bc = bubble_cmp_count;

        // 归并排序
        vector<int> m = arr;
        merge_cmp_count = 0;
        merge_subproblem_sizes.clear();
        mergeSort(m, 0, (int)m.size() - 1);
        long long mc = merge_cmp_count;
        int merge_sub_cnt = (int)merge_subproblem_sizes.size();

        // 快速排序
        vector<int> q = arr;
        quick_cmp_count = 0;
        quick_subproblem_sizes.clear();
        quickSort(q, 0, (int)q.size() - 1);
        long long qc = quick_cmp_count;
        int quick_sub_cnt = (int)quick_subproblem_sizes.size();

        cout << left << setw(10) << n
             << setw(16) << bc
             << setw(16) << mc
             << setw(16) << qc << endl;

        csv << n << "," << bc << "," << mc << "," << qc
            << "," << merge_sub_cnt << "," << quick_sub_cnt << endl;

        // 输出子问题规模（仅对n<=1000详细输出）
        if (n <= 1000) {
            ofstream subf("../data/subproblems_n" + to_string(n) + ".txt");
            subf << "=== N=" << n << " 归并排序子问题规模 ===" << endl;
            subf << "子问题总数: " << merge_subproblem_sizes.size() << endl;
            // 按规模分组统计
            map<int,int> mcnt;
            for (int s : merge_subproblem_sizes) mcnt[s]++;
            for (auto& p : mcnt)
                subf << "规模 " << p.first << ": " << p.second << " 个" << endl;

            subf << "\n=== N=" << n << " 快速排序子问题规模 ===" << endl;
            subf << "子问题总数: " << quick_subproblem_sizes.size() << endl;
            map<int,int> qcnt;
            for (int s : quick_subproblem_sizes) qcnt[s]++;
            for (auto& p : qcnt)
                subf << "规模 " << p.first << ": " << p.second << " 个" << endl;
            subf.close();
        }
    }
    csv.close();
    cout << "\n数据已保存到 ../data/sorting_results.csv" << endl;
    return 0;
}
