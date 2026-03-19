import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# 1. 数据录入
n_values = [5, 10, 11, 12, 13, 14, 15]

# BranchBound 方法的时间
t_bb = [0.006, 0.778, 4.492, 12.708, 87.964, 526.62, 1171.43]

# Gurobi-1D 方法的时间
t_gurobi = [0.022, 1.425, 2.647, 14.210, 123.76, 889.46, 1401.49]

# 2. 设置绘图
plt.figure(figsize=(10, 6))

# 绘制 BranchBound 线条 (蓝色圆点实线)
plt.plot(n_values, t_bb,
         marker='o', markersize=8, linestyle='-', linewidth=2,
         color='#1f77b4', label='BranchBound')

# 绘制 Gurobi-1D 线条 (红色方块虚线)
plt.plot(n_values, t_gurobi,
         marker='s', markersize=8, linestyle='--', linewidth=2,
         color='#d62728', label='Gurobi-1D')

# 3. 坐标轴与刻度设置
plt.title('Running Time Comparison: BranchBound vs Gurobi-1D', fontsize=20)
plt.xlabel('n (Instance Size)', fontsize=20)
plt.ylabel('t_run [s] (Log Scale)', fontsize=20)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)

# 设置 X 轴刻度，强制只显示数据中存在的 n 值
plt.xticks(n_values)

# *** 关键设置：开启对数坐标 ***
# 如果不开启对数坐标，前几个点会挤在 0 附近看不清
plt.yscale('log')

# 设置Y轴网格，方便读数
plt.grid(True, which="both", ls="-", alpha=0.2)

# 4. 添加图例
plt.legend(fontsize=20)

# # 5. 显示具体数值 (可选：在点旁边标注数值，防止对数坐标不好读数)
# # 这里只标注 n=15 的最大值，避免太乱
# plt.text(15, 1171.43, ' 1171s', va='top', ha='right', fontsize=9, color='#1f77b4')
# plt.text(15, 1401.49, ' 1401s', va='bottom', ha='right', fontsize=9, color='#d62728')

plt.tight_layout()
plt.savefig('BB-1D.svg')
plt.show()