import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# 1. 数据准备
n_values = [5, 10, 11, 12, 13, 14, 15]

# DFS 数据
t_dfs = [0.006, 0.777, 3.555, 16.380, 235.048, 587.306, 1587.368]

# BFS&DFS 数据
t_bfs_dfs = [0.006, 0.778, 4.492, 12.708, 87.964, 526.618, 1171.430]

# BFS 数据处理
# 有效部分
n_bfs_valid = [5, 10, 11, 12]
t_bfs_valid = [0.004, 1.785, 9.124, 60.307]

# 失效部分 (n=13, 14, 15)
n_bfs_fail = [13, 14, 15]
# 设定一个“顶部值”，用于在图最上方画叉
TOP_Y = 4000
t_bfs_fail = [TOP_Y] * len(n_bfs_fail)

# 合并 BFS 数据用于画连线
n_bfs_all = n_bfs_valid + n_bfs_fail
t_bfs_all = t_bfs_valid + t_bfs_fail

# 2. 开始绘图
plt.figure(figsize=(10, 6))

# --- 绘制 DFS (蓝色圆点实线) ---
plt.plot(n_values, t_dfs,
         marker='o', markersize=6, linestyle='-', linewidth=2,
         color='#1f77b4', label='DFS')

# --- 绘制 BFS&DFS (绿色方块实线) ---
plt.plot(n_values, t_bfs_dfs,
         marker='s', markersize=6, linestyle='-', linewidth=2,
         color='#2ca02c', label='BFS & DFS')

# --- 绘制 BFS (特殊处理) ---
# 步骤A: 画一条贯穿所有点的橙色虚线
plt.plot(n_bfs_all, t_bfs_all,
         linestyle='--', linewidth=2, color='#ff7f0e', zorder=1)

# 步骤B: 在有效点位置覆盖橙色三角
plt.scatter(n_bfs_valid, t_bfs_valid,
            marker='^', s=60, color='#ff7f0e', zorder=2)

# 步骤C: 在无效点位置覆盖黑色叉号 (Black Cross)
plt.scatter(n_bfs_fail, t_bfs_fail,
            marker='x', s=80, color='black', linewidths=2, zorder=3)

# 3. 坐标轴设置
plt.title('Running Time Comparison', fontsize=20)
plt.xlabel('n (Instance Size)', fontsize=20)
plt.ylabel('t_run [s] (Log Scale)', fontsize=20)

plt.xticks(n_values,fontsize=20)
plt.yticks(fontsize=20)# 强制显示所有n
plt.yscale('log')    # 对数坐标

# 设置 Y 轴范围，确保顶部的叉号能显示出来，并且上面留一点白边
plt.ylim(0.002, TOP_Y * 1.5)

plt.grid(True, which="both", ls="-", alpha=0.2)

# 4. 自定义图例
# 因为 BFS 我们分了三步画，为了图例好看，我们手动定义
legend_elements = [
    Line2D([0], [0], marker='o', color='#1f77b4', label='DFS', markersize=8),
    Line2D([0], [0], marker='^', color='#ff7f0e', linestyle='--', label='BFS (Optimal Found)', markersize=8),
    Line2D([0], [0], marker='s', color='#2ca02c', label='BFS & DFS', markersize=8),
    # 单独解释黑色的叉
    Line2D([0], [0], marker='x', color='w', label='BFS (> 1800s,Feasible Found)',
           markeredgecolor='black', markeredgewidth=2, markersize=8)
]

plt.legend(handles=legend_elements, fontsize=15, loc='upper left')

plt.tight_layout()
plt.savefig('Node-selection.svg')
plt.show()