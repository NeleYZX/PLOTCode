import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.lines import Line2D

# 1. 原始数据录入
data = {
    'n': [
        5, 5, 5, 5,
        10, 10, 10, 10,
        11, 11, 11, 11,
        12, 12, 12, 12,
        13, 13, 13, 13,
        14, 14, 14, 14,
        15, 15, 15, 15
    ],
    '2D_run': [
        0.093, 0.081, 0.088, 0.142,
        3.664, 2.732, 1.995, 1.771,
        2.338, 4.589, 1.798, 2.794,
        6.082, 11.048, 3.666, 6.083,
        12.062, 26.167, 6.024, 8.162,
        41.842, 321.42, 36.546, 41.937,
        1800.26, 1800.105, 531.593, 266.734
    ],
    '1D_run': [
        0.022, 0.015, 0.032, 0.038,
        1.425, 2.293, 0.414, 0.213,
        2.647, 4.267, 0.383, 0.657,
        14.21, 16.771, 1.454, 2.006,
        123.756, 159.804, 2.44, 4.469,
        889.461, 650.071, 12.409, 10.276,
        1401.486, 1800.108, 46.107, 216.388
    ]
}

df = pd.DataFrame(data)

# 2. 筛选逻辑
# 保留：(1D <= 2D) 或者 (两者都超时 > 1800)
LIMIT = 1800
condition_better = df['1D_run'] <= df['2D_run']
condition_both_timeout = (df['1D_run'] > LIMIT) & (df['2D_run'] > LIMIT)

df_filtered = df[condition_better | condition_both_timeout].copy()


# 3. 重新计算偏移量 (Jitter)
def calculate_offset(group):
    count = len(group)
    indices = np.arange(count)
    group['x_plot'] = group['n'] + (indices - (count - 1) / 2) * 0.15
    return group


df_filtered = df_filtered.groupby('n', group_keys=False).apply(calculate_offset)

# 4. 绘图
plt.figure(figsize=(12, 7))

# --- 绘制 2D 数据 ---
mask_2d_normal = df_filtered['2D_run'] <= LIMIT
mask_2d_out = df_filtered['2D_run'] > LIMIT

# 2D 实心 (正常)
plt.scatter(df_filtered.loc[mask_2d_normal, 'x_plot'],
            df_filtered.loc[mask_2d_normal, '2D_run'],
            color='tab:red', alpha=0.8, s=60, marker='o', label='_nolegend_')

# 2D 空心 (超时)
plt.scatter(df_filtered.loc[mask_2d_out, 'x_plot'],
            df_filtered.loc[mask_2d_out, '2D_run'],
            facecolors='none', edgecolors='tab:red', linewidths=1.5,
            s=80, marker='o', label='_nolegend_')

# --- 绘制 1D 数据 ---
mask_1d_normal = df_filtered['1D_run'] <= LIMIT
mask_1d_out = df_filtered['1D_run'] > LIMIT

# 1D 实心 (正常)
plt.scatter(df_filtered.loc[mask_1d_normal, 'x_plot'],
            df_filtered.loc[mask_1d_normal, '1D_run'],
            color='tab:blue', alpha=0.8, s=60, marker='s', label='_nolegend_')

# 1D 空心 (超时)
plt.scatter(df_filtered.loc[mask_1d_out, 'x_plot'],
            df_filtered.loc[mask_1d_out, '1D_run'],
            facecolors='none', edgecolors='tab:blue', linewidths=1.5,
            s=80, marker='s', label='_nolegend_')

# 5. 辅助线
unique_ns = df_filtered['n'].unique()
for n_val in unique_ns:
    plt.axvline(x=n_val, color='gray', linestyle='--', alpha=0.2, linewidth=1)

# 6. 【关键修改】自定义四项图例
legend_elements = [
    # 1. 红色实心圆
    Line2D([0], [0], marker='o', color='w', label='2D (Optimal)',
           markerfacecolor='tab:red', markersize=10),

    # 2. 红色空心圆
    Line2D([0], [0], marker='o', color='w', label='2D (>1800s,Feasible)',
           markerfacecolor='none', markeredgecolor='tab:red', markeredgewidth=1.5, markersize=10),

    # 3. 蓝色实心方块
    Line2D([0], [0], marker='s', color='w', label='1D (Optimal)',
           markerfacecolor='tab:blue', markersize=10),

    # 4. 蓝色空心方块
    Line2D([0], [0], marker='s', color='w', label='1D (>1800s,Feasible)',
           markerfacecolor='none', markeredgecolor='tab:blue', markeredgewidth=1.5, markersize=10)
]

plt.legend(handles=legend_elements, fontsize=20, loc='upper left')

# 7. 坐标轴设置
plt.title('Running Time Comparison (Filtered)', fontsize=20)
plt.xlabel('n (Instance Size)', fontsize=20)
plt.ylabel('t_run (seconds) - Log Scale', fontsize=20)
plt.xticks(unique_ns, fontsize=20)
plt.yticks(fontsize=20)
plt.yscale('log')
plt.grid(True, which="both", ls="-", alpha=0.2)

plt.tight_layout()
plt.savefig('D:\PLOT\PlotCode\TT2D-1D.svg')
plt.show()