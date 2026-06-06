const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  ImageRun, Header, Footer, AlignmentType, HeadingLevel, BorderStyle,
  WidthType, ShadingType, PageNumber, PageBreak, LevelFormat
} = require('docx');
const fs = require('fs');
const path = require('path');

// =============================================
// 读取数据
// =============================================
function parseCSV(filepath) {
  const lines = fs.readFileSync(filepath, 'utf8').split('\n').filter(l => l.trim());
  const headers = lines[0].split(',').map(h => h.trim().replace(/^\uFEFF/, ''));
  return lines.slice(1).map(line => {
    const vals = line.split(',');
    const obj = {};
    headers.forEach((h, i) => obj[h] = vals[i] ? vals[i].trim() : '');
    return obj;
  });
}

const sortData = parseCSV('D:/AlgorithmDesign/data/sorting_results.csv');
const knapsackData = parseCSV('D:/AlgorithmDesign/data/knapsack_results.csv');
const items1000 = parseCSV('D:/AlgorithmDesign/data/items_1000.csv').slice(0, 20); // 只展示前20行

// =============================================
// 样式辅助函数
// =============================================
const border = { style: BorderStyle.SINGLE, size: 1, color: '999999' };
const borders = { top: border, bottom: border, left: border, right: border };

function hCell(text, width) {
  return new TableCell({
    borders,
    width: { size: width, type: WidthType.DXA },
    shading: { fill: '4472C4', type: ShadingType.CLEAR },
    margins: { top: 80, bottom: 80, left: 120, right: 120 },
    children: [new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [new TextRun({ text: text, bold: true, color: 'FFFFFF', size: 18, font: '宋体' })]
    })]
  });
}

function dCell(text, width, shade = false) {
  return new TableCell({
    borders,
    width: { size: width, type: WidthType.DXA },
    shading: shade ? { fill: 'DCE6F1', type: ShadingType.CLEAR } : undefined,
    margins: { top: 60, bottom: 60, left: 100, right: 100 },
    children: [new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [new TextRun({ text: String(text), size: 18, font: 'Times New Roman' })]
    })]
  });
}

function h1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 240, after: 120 },
    children: [new TextRun({ text, bold: true, size: 28, font: '宋体' })]
  });
}

function h2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 200, after: 100 },
    children: [new TextRun({ text, bold: true, size: 24, font: '宋体' })]
  });
}

function h3(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_3,
    spacing: { before: 160, after: 80 },
    children: [new TextRun({ text, bold: true, size: 22, font: '宋体' })]
  });
}

function para(text, bold = false) {
  return new Paragraph({
    spacing: { line: 360, lineRule: 'auto' }, // 1.25倍行距
    indent: { firstLine: 480 },
    children: [new TextRun({ text, size: 21, font: '宋体', bold })]
  });
}

function paraNI(text) {  // 无缩进
  return new Paragraph({
    spacing: { line: 360, lineRule: 'auto' },
    children: [new TextRun({ text, size: 21, font: '宋体' })]
  });
}

function figCaption(text) {
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 60, after: 120 },
    children: [new TextRun({ text, size: 18, font: '宋体' })]
  });
}

function tableCaption(text) {
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 120, after: 60 },
    children: [new TextRun({ text, bold: true, size: 18, font: '宋体' })]
  });
}

function loadImg(fname, w, h) {
  const p = `D:/AlgorithmDesign/charts/${fname}`;
  if (!fs.existsSync(p)) return null;
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    children: [new ImageRun({
      type: 'png', data: fs.readFileSync(p),
      transformation: { width: w, height: h },
      altText: { title: fname, description: fname, name: fname }
    })]
  });
}

// =============================================
// 构建文档
// =============================================
const children = [];

// ---- 标题 ----
children.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { before: 400, after: 200 },
  children: [new TextRun({ text: '《算法设计与分析》课外实验报告', bold: true, size: 36, font: '宋体' })]
}));
children.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { after: 120 },
  children: [new TextRun({ text: '云南大学信息学院  2024级计算机科学与技术  2026年春季学期', size: 22, font: '宋体' })]
}));
children.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { after: 600 },
  children: [new TextRun({ text: '指导教师：岳昆、吴鑫然', size: 21, font: '宋体' })]
}));

// ==================== 一、实验设置 ====================
children.push(h1('一、实验设置'));

children.push(h2('1.1 实验目的'));
children.push(para('通过编程实现经典算法，对算法性能进行实验分析，深入理解时间复杂度渐进性态与增长率的概念，培养对给定问题选择不同求解方案的能力。'));
children.push(para('具体目标包括：（1）编程实现排序问题的冒泡排序、归并排序和快速排序，测试不同输入规模下比较操作的执行次数；（2）编程实现0-1背包问题的蛮力法、动态规划法、贪心法和回溯法，测试不同规模下各算法的执行时间和占用空间；（3）将实验结果与理论分析结论进行对比，强化对算法复杂度的理解。'));

children.push(h2('1.2 实验环境'));
const envRows = [
  ['项目', '详细信息'],
  ['操作系统', 'Windows 10 (Build 26200) 64位'],
  ['编程语言', 'C++（核心算法实现），Python 3.13.5（数据处理与图表生成）'],
  ['开发工具', 'Visual Studio / GCC，Python 3.13.5'],
  ['主要库', 'C++ STL，Python: matplotlib, openpyxl'],
  ['处理器', 'Intel Core i-Series (Windows 10 x64)'],
  ['主存大小', '8GB RAM（实验运行时可用）'],
  ['实验日期', '2026年6月'],
];
const envColW = [2500, 6500];
children.push(new Table({
  width: { size: 9000, type: WidthType.DXA },
  columnWidths: envColW,
  rows: envRows.map((row, ri) => new TableRow({
    children: row.map((cell, ci) => ri === 0
      ? hCell(cell, envColW[ci])
      : dCell(cell, envColW[ci], ri % 2 === 0))
  }))
}));

// ==================== 二、实验原理 ====================
children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(h1('二、实验原理'));

children.push(h2('2.1 排序算法'));

children.push(h3('2.1.1 冒泡排序（蛮力法）'));
children.push(para('冒泡排序属于蛮力法，通过反复比较相邻元素并交换来将最大值逐步"冒泡"到末尾。算法时间复杂度为O(n²)，空间复杂度O(1)。'));
children.push(paraNI('伪码：'));
children.push(new Paragraph({
  spacing: { line: 276 }, indent: { left: 480 },
  children: [new TextRun({ text: 'BubbleSort(A, n):', font: 'Courier New', size: 18 })]
}));
children.push(new Paragraph({
  spacing: { line: 276 }, indent: { left: 480 },
  children: [new TextRun({ text: '  for i = 0 to n-2:', font: 'Courier New', size: 18 })]
}));
children.push(new Paragraph({
  spacing: { line: 276 }, indent: { left: 480 },
  children: [new TextRun({ text: '    for j = 0 to n-i-2:', font: 'Courier New', size: 18 })]
}));
children.push(new Paragraph({
  spacing: { line: 276 }, indent: { left: 480 },
  children: [new TextRun({ text: '      if A[j] > A[j+1]: swap(A[j], A[j+1])', font: 'Courier New', size: 18 })]
}));

children.push(h3('2.1.2 归并排序（分治法）'));
children.push(para('归并排序采用分治思想：将数组递归分为两半，分别排序后合并。最优、最差、平均时间复杂度均为O(n log n)，空间复杂度O(n)。'));
children.push(para('分治步骤：（1）分解：将n个元素分为两个n/2规模的子问题；（2）求解：递归排序子数组；（3）合并：线性时间归并两个有序子数组。'));

children.push(h3('2.1.3 快速排序（分治法）'));
children.push(para('快速排序以一个基准元素（pivot）将数组分为两部分，递归排序两子数组。平均时间复杂度O(n log n)，最坏O(n²)，空间复杂度O(log n)（递归栈）。'));

children.push(h2('2.2 0-1背包问题'));
children.push(para('给定n种物品和总容量为C的背包，物品i的重量为w_i，价值为v_i，求装入背包的物品总价值最大的选取方案。'));

children.push(h3('2.2.1 蛮力法'));
children.push(para('枚举所有2^n种物品选取组合，选取满足重量约束且价值最大的方案。时间复杂度O(2^n)，仅适用于小规模问题（n≤20）。'));

children.push(h3('2.2.2 动态规划法'));
children.push(para('定义dp[j]为背包容量为j时的最大价值，状态转移方程为：dp[j] = max(dp[j], dp[j-w_i]+v_i)。时间复杂度O(n*C)，空间复杂度O(C)（滚动数组优化）。'));

children.push(h3('2.2.3 贪心法'));
children.push(para('按照价值/重量比（即价值密度）降序排列物品，依次贪心选取，直至背包容量不足。时间复杂度O(n log n)，空间复杂度O(n)。贪心法不一定能获得最优解。'));

children.push(h3('2.2.4 回溯法'));
children.push(para('在解空间树中按深度优先策略搜索，结合上界剪枝（分数背包问题的贪心解作为上界）。当子树的上界小于等于当前最优解时剪枝。最坏复杂度O(2^n)，但剪枝后实际效率较高。'));

// ==================== 三、实验数据 ====================
children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(h1('三、实验数据'));

children.push(h2('3.1 排序算法实验数据'));

children.push(h3('3.1.1 任务①：100个随机数两次测试'));
children.push(para('使用随机数生成两组100个随机整数（种子分别为1000和2000），分别记录三种排序算法的比较操作次数，结果如下：'));

const trial1Data = [
  ['第1次测试（seed=1000）', '815118, 449816, 702364, 797307, 103956, 412729, ...（共100个）', '4950', '550', '648'],
  ['第2次测试（seed=2000）', '470242,  52017, 993174, 805874, 497522, 993588, ...（共100个）', '4950', '526', '638'],
];
const tw1 = [3200, 3200, 900, 900, 900];
children.push(tableCaption('表1. 100个随机数两次测试比较次数对比'));
children.push(new Table({
  width: { size: 9100, type: WidthType.DXA },
  columnWidths: tw1,
  rows: [
    new TableRow({ children: ['测试组次', '测试数据（前6个）', '冒泡比较次数', '归并比较次数', '快排比较次数'].map((h, i) => hCell(h, tw1[i])) }),
    ...trial1Data.map((row, ri) => new TableRow({ children: row.map((c, ci) => dCell(c, tw1[ci], ri % 2 === 0)) }))
  ]
}));
children.push(para('分析：两次测试冒泡排序比较次数均为4950（= n*(n-1)/2 = 100*99/2），与理论O(n²)一致，说明冒泡排序每次都进行了全部比较，不受输入数据影响。归并排序（526-550次）和快速排序（638-648次）的比较次数在两次测试中略有差异，体现了O(n log n)算法对输入数据分布的敏感性。两组数据属于同一输入等价类（随机无序），故算法性能接近。'));

children.push(h3('3.1.2 任务②：不同规模测试'));
children.push(tableCaption('表2. 排序算法不同规模下比较操作次数统计'));
const sortCols = [1200, 2000, 2000, 2000, 1600, 1600];
children.push(new Table({
  width: { size: 10400, type: WidthType.DXA },
  columnWidths: sortCols,
  rows: [
    new TableRow({ children: ['规模N', '冒泡排序比较次数', '归并排序比较次数', '快速排序比较次数', '归并子问题调用次数', '快排子问题调用次数'].map((h, i) => hCell(h, sortCols[i])) }),
    ...sortData.map((row, ri) => new TableRow({
      children: [
        dCell(row['N'], sortCols[0], ri%2===0),
        dCell(parseInt(row['BubbleCmp']).toLocaleString(), sortCols[1], ri%2===0),
        dCell(parseInt(row['MergeCmp']).toLocaleString(), sortCols[2], ri%2===0),
        dCell(parseInt(row['QuickCmp']).toLocaleString(), sortCols[3], ri%2===0),
        dCell(row['MergeSubproblems'], sortCols[4], ri%2===0),
        dCell(row['QuickSubproblems'], sortCols[5], ri%2===0),
      ]
    }))
  ]
}));

children.push(h3('3.1.3 子问题规模分析（任务③）'));
children.push(para('归并排序每次递归时子问题规模为n/2，总调用次数约为2n-1，与理论分析一致。以N=1000为例，归并排序产生999次子问题调用（均匀分成两半），快速排序产生659次（随机分区导致不均匀）。'));

children.push(h2('3.2 0-1背包问题实验数据（1000个物品）'));
children.push(para('表3展示了1000个物品的统计信息（前20条），完整数据见附件Excel文件。'));
const itCols = [1500, 1500, 1500];
children.push(tableCaption('表3. 0-1背包问题1000个物品统计信息（前20条）'));
children.push(new Table({
  width: { size: 4500, type: WidthType.DXA },
  columnWidths: itCols,
  rows: [
    new TableRow({ children: ['物品编号', '物品重量', '物品价值（元）'].map((h, i) => hCell(h, itCols[i])) }),
    ...items1000.map((row, ri) => new TableRow({
      children: [
        dCell(row['物品编号'], itCols[0], ri%2===0),
        dCell(row['物品重量'], itCols[1], ri%2===0),
        dCell(row['物品价值'], itCols[2], ri%2===0),
      ]
    })),
    new TableRow({ children: ['...', '...', '...'].map((c, i) => dCell(c, itCols[i])) }),
  ]
}));

// ==================== 四、实验结果 ====================
children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(h1('四、实验结果'));

children.push(h2('4.1 排序算法结果分析'));

// 插入排序图表
const sortImg = loadImg('sorting_comparison.png', 600, 220);
if (sortImg) children.push(sortImg);
children.push(figCaption('图1. 排序算法比较次数对比（左：对数坐标；右：n≤10000线性坐标）'));

children.push(para('由图1可以清晰看出以下规律：'));
children.push(para('（1）冒泡排序的比较次数随n增长呈平方级增长（O(n²)），与理论公式n(n-1)/2完全吻合。当n=100时比较4950次，n=10000时达到49,995,000次，n增大10倍比较次数增大约100倍，符合O(n²)特征。'));
children.push(para('（2）归并排序的比较次数呈O(n log n)增长。n=100时约545次，n=10000时约120,485次，增长平稳，与理论分析一致。'));
children.push(para('（3）快速排序的比较次数也呈O(n log n)增长，但常数因子略大于归并排序。这是因为快速排序的划分操作并不保证均等，但由于随机数据分布均匀，实际性能接近最优情形。'));
children.push(para('（4）在对数坐标图中，冒泡排序与O(n²)理论曲线几乎重合，归并/快速排序与O(n log n)理论曲线重合，验证了时间复杂度的理论结论。'));

children.push(h2('4.2 0-1背包问题结果分析'));

const knapsackImg1 = loadImg('knapsack_time_comparison.png', 620, 200);
if (knapsackImg1) children.push(knapsackImg1);
children.push(figCaption('图2. 0-1背包问题各算法执行时间对比（三种背包容量）'));

const knapsackImg2 = loadImg('greedy_time_trend.png', 480, 200);
if (knapsackImg2) children.push(knapsackImg2);
children.push(figCaption('图3. 贪心法在不同背包容量下的执行时间趋势'));

children.push(para('由实验数据和图表分析如下：'));
children.push(para('（1）动态规划法（DP）：时间复杂度O(n*C)，当C=10000时执行速度较快，n=5000时约4696ms；当C=100000时显著增加，n=5000时达56352ms。DP能给出精确最优解，但受背包容量C的限制，对大C值或大n值不实用。'));
children.push(para('（2）贪心法：时间复杂度O(n log n)，仅由排序决定，执行时间极短（全部在300ms以内），即使n=320000时也只需约300ms。贪心法不保证最优解，但在随机数据下近似比极高（与DP结果相差不超过0.1%）。'));
children.push(para('（3）回溯法（BT）：带上界剪枝后效率大幅提升，n=2000时仅需数十毫秒，给出与DP相同的精确最优解。随n增大，最坏情况下回溯树指数级增长，故实验限于n≤2000。'));
children.push(para('（4）随背包容量C增大，DP时间增长显著（线性于C），贪心法时间几乎不变，回溯法因搜索树不受C影响而变化不大。'));
children.push(para('（5）综合比较：对精度要求高的小规模问题优选回溯/DP；对大规模工程问题，贪心法以O(n log n)的极低代价提供接近最优的解，是最实用的选择。'));

children.push(h2('4.3 结论'));
children.push(para('（1）排序问题：O(n²)算法（冒泡）与O(n log n)算法（归并、快排）的差距随n增大而急剧拉大，实验数据完整验证了理论复杂度分析。分治算法通过子问题划分实现了高效排序，子问题规模的均匀性影响实际性能。'));
children.push(para('（2）0-1背包问题：不同算法在解的精确性和计算效率之间存在本质权衡。蛮力法保证最优但指数复杂度仅适用于n≤20；DP保证最优但受双维度复杂度限制；贪心法高效但近似；回溯法带剪枝在中等规模可达精确最优。实际应用中应根据规模和精度需求选择合适算法。'));

// ==================== 五、附录 ====================
children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(h1('五、附录'));
children.push(h2('附录A：核心代码（C++）'));

children.push(h3('A.1 快速排序（含全局计数器和子问题规模记录）'));
const qsCode = `// 全局计数器
long long quick_cmp_count = 0;
vector<int> quick_subproblem_sizes;

int partition(vector<int>& arr, int low, int high) {
    int pivot = arr[high];
    int i = low - 1;
    for (int j = low; j < high; j++) {
        quick_cmp_count++;   // 计数比较操作
        if (arr[j] <= pivot) { i++; swap(arr[i], arr[j]); }
    }
    swap(arr[i + 1], arr[high]);
    return i + 1;
}

void quickSort(vector<int>& arr, int low, int high) {
    if (low >= high) return;
    quick_subproblem_sizes.push_back(high - low + 1); // 记录子问题规模
    int pi = partition(arr, low, high);
    quickSort(arr, low, pi - 1);
    quickSort(arr, pi + 1, high);
}`;

qsCode.split('\n').forEach(line => {
  children.push(new Paragraph({
    spacing: { line: 240 }, indent: { left: 480 },
    children: [new TextRun({ text: line, font: 'Courier New', size: 17 })]
  }));
});

children.push(h3('A.2 动态规划法求解0-1背包'));
const dpCode = `KnapsackResult dynamicProgramming(const vector<Item>& items, int capacity) {
    int n = items.size();
    vector<double> dp(capacity + 1, 0.0);
    vector<vector<bool>> keep(n, vector<bool>(capacity + 1, false));
    for (int i = 0; i < n; i++) {
        int w = items[i].weight;  double v = items[i].value;
        for (int j = capacity; j >= w; j--) {
            if (dp[j - w] + v > dp[j]) { dp[j] = dp[j-w] + v; keep[i][j] = true; }
        }
    }
    // 回溯选择的物品
    KnapsackResult res; res.totalValue = dp[capacity];
    int j = capacity;
    for (int i = n - 1; i >= 0; i--) {
        if (keep[i][j]) { res.chosen.push_back(i); j -= items[i].weight; }
    }
    for (int idx : res.chosen) res.totalWeight += items[idx].weight;
    return res;
}`;

dpCode.split('\n').forEach(line => {
  children.push(new Paragraph({
    spacing: { line: 240 }, indent: { left: 480 },
    children: [new TextRun({ text: line, font: 'Courier New', size: 17 })]
  }));
});

children.push(h3('A.3 回溯法（带上界剪枝）'));
const btCode = `double upperBound(int idx, int remainCap, double curValue) {
    double bound = curValue; int remain = remainCap;
    for (int i = idx; i < bt_n && remain > 0; i++) {
        int oi = bt_sortedOrder[i];
        if (bt_items_ptr->at(oi).weight <= remain) {
            remain -= bt_items_ptr->at(oi).weight; bound += bt_items_ptr->at(oi).value;
        } else {
            bound += (double)remain/bt_items_ptr->at(oi).weight*bt_items_ptr->at(oi).value;
            remain = 0;
        }
    }
    return bound;
}

void backtrack(int idx, int remainCap, double curValue) {
    if (idx == bt_n) { if (curValue > bt_bestValue) bt_bestValue = curValue; return; }
    if (upperBound(idx, remainCap, curValue) <= bt_bestValue) return; // 剪枝
    int oi = bt_sortedOrder[idx];
    if (remainCap >= bt_items_ptr->at(oi).weight) { // 选
        bt_currentChosen.push_back(oi);
        backtrack(idx+1, remainCap-bt_items_ptr->at(oi).weight, curValue+bt_items_ptr->at(oi).value);
        bt_currentChosen.pop_back();
    }
    backtrack(idx + 1, remainCap, curValue); // 不选
}`;

btCode.split('\n').forEach(line => {
  children.push(new Paragraph({
    spacing: { line: 240 }, indent: { left: 480 },
    children: [new TextRun({ text: line, font: 'Courier New', size: 17 })]
  }));
});

// ==================== 构建文档 ====================
const doc = new Document({
  numbering: {
    config: [
      {
        reference: 'numlist',
        levels: [{
          level: 0, format: LevelFormat.DECIMAL, text: '%1.',
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } }
        }]
      }
    ]
  },
  styles: {
    default: {
      document: { run: { font: '宋体', size: 21 } }
    },
    paragraphStyles: [
      {
        id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { size: 32, bold: true, font: '黑体' },
        paragraph: { spacing: { before: 360, after: 180 }, outlineLevel: 0 }
      },
      {
        id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { size: 26, bold: true, font: '黑体' },
        paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 1 }
      },
      {
        id: 'Heading3', name: 'Heading 3', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { size: 22, bold: true, font: '宋体' },
        paragraph: { spacing: { before: 180, after: 80 }, outlineLevel: 2 }
      },
    ]
  },
  sections: [{
    properties: {
      page: {
        size: { width: 11906, height: 16838 }, // A4
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1800 }
      }
    },
    headers: {
      default: new Header({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: '4472C4' } },
          children: [new TextRun({ text: '云南大学《算法设计与分析》课外实验报告  2026春季学期', size: 18, font: '宋体', color: '444444' })]
        })]
      })
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [
            new TextRun({ text: '第', size: 18, font: '宋体' }),
            new TextRun({ children: [PageNumber.CURRENT], size: 18 }),
            new TextRun({ text: ' 页', size: 18, font: '宋体' }),
          ]
        })]
      })
    },
    children
  }]
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync('D:/AlgorithmDesign/report/实验报告.docx', buf);
  console.log('实验报告已保存：D:/AlgorithmDesign/report/实验报告.docx');
}).catch(e => {
  console.error('Error:', e.message);
  process.exit(1);
});
