import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker

# ==========================================
# 顶级期刊标准排版设置
# ==========================================
# 强制使用 Times New Roman 字体
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']
plt.rcParams['font.size'] = 12
plt.rcParams['axes.linewidth'] = 1.0

# ==========================================
# 参考示例图的经典 Matplotlib 配色方案
# ==========================================
COLOR_BLUE = '#1f77b4'   # BB_par: 蓝色
COLOR_ORANGE = '#ff7f0e' # Gurobi: 橙色
COLOR_GREEN = '#2ca02c'  # BB_hyb: 绿色
COLOR_RED = '#d62728'    # BB_serial: 红色 (新增颜色)
GRID_COLOR = '#EAEAEA'   # 极淡的网格色

# 修改为纯黑，以满足“黑色加粗、清晰”的要求
TEXT_COLOR = '#000000'
plt.rcParams['text.color'] = TEXT_COLOR
plt.rcParams['axes.labelcolor'] = TEXT_COLOR
plt.rcParams['xtick.color'] = TEXT_COLOR
plt.rcParams['ytick.color'] = TEXT_COLOR

# ==========================================
# 图 1: 算法效率对比折线图 (4种方法)
# ==========================================
n_exp1 = np.arange(10, 20)

# 根据您最新表1数据提取的 4 种算法平均时间 (秒)
time_gurobi = [1.31, 4.91, 18.37, 144.36, 306.64, 1137.72, 420.24, 1623.77, 1573.93, 3088.72]
time_bb_par = [0.19, 0.41, 1.22, 3.75, 11.62, 36.44, 109.33, 373.21, 1040.41, 3601.41]
time_bb_serial = [0.36, 1.00, 2.71, 6.82, 17.16, 34.64, 150.17, 465.81, 1148.48, 3601.35]
time_bb_hyb = [0.14, 0.38, 1.24, 3.98, 12.35, 39.05, 105.72, 363.49, 1014.78, 3601.57]

fig1, ax1 = plt.subplots(figsize=(6.5, 4.5))

# 极简边框
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['left'].set_color('#888888')
ax1.spines['bottom'].set_color('#888888')

# 绘制线条 - 4种方法
# 1. Gurobi: 橙色虚线 + 三角
ax1.plot(n_exp1, time_gurobi, marker='^', linestyle='--', color=COLOR_ORANGE,
         linewidth=2, markersize=7, label='Gurobi', zorder=3)
# 2. BB_par: 蓝色实线 + 圆点
ax1.plot(n_exp1, time_bb_par, marker='o', linestyle='-', color=COLOR_BLUE,
         linewidth=2, markersize=7, label=r'$BB_{par}$', zorder=3)
# 3. BB_serial: 红色点划线 + 菱形
ax1.plot(n_exp1, time_bb_serial, marker='d', linestyle='-.', color=COLOR_RED,
         linewidth=2, markersize=7, label=r'$BB_{serial}$', zorder=3)
# 4. BB_hyb: 绿色实线 + 方块
ax1.plot(n_exp1, time_bb_hyb, marker='s', linestyle='-', color=COLOR_GREEN,
         linewidth=2, markersize=7, label=r'$BB_{hyb}$', zorder=3)

# 坐标轴与网格设置 - 强制黑色加粗
ax1.set_yscale('log')
ax1.set_xlabel('Number of parts ($n$)', color='black', fontweight='bold', fontsize=13)
ax1.set_ylabel('Average CPU Time (s) [Log Scale]', color='black', fontweight='bold', fontsize=13)
ax1.set_xticks(n_exp1)

# 将刻度标签也设置为粗体（可选，让整体更醒目）
for label in (ax1.get_xticklabels() + ax1.get_yticklabels()):
    label.set_fontweight('bold')

# 开启主网格和次网格
ax1.grid(True, which="major", axis='both', ls="-", linewidth=0.8, color=GRID_COLOR, zorder=0)
ax1.grid(True, which="minor", axis='y', ls="-", linewidth=0.5, color=GRID_COLOR, zorder=0)

# 图例设置
ax1.legend(loc='upper left', frameon=True, fancybox=False, edgecolor='#CCCCCC', fontsize=11)

plt.tight_layout()
# 导出为 600 DPI 的 PNG 图片
fig1.savefig('fig1_efficiency_ref.png', format='png', dpi=600, bbox_inches='tight')
plt.close(fig1)


# ==========================================
# 图 2: 平台容量影响柱状图
# ==========================================
n_exp2 = np.arange(12, 19)
time_10x10 = [1.08, 4.22, 8.44, 31.07, 36.07, 133.86, 363.09]
time_20x20 = [1.86, 7.12, 22.09, 59.14, 176.42, 669.21, 1820.25]

fig2, ax2 = plt.subplots(figsize=(6.5, 4.5))

ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['left'].set_color('#888888')
ax2.spines['bottom'].set_color('#888888')

x = np.arange(len(n_exp2))
width = 0.35

# 柱状图配色
bars1 = ax2.bar(x - width/2, time_10x10, width, label='Restrictive ($10 \\times 10$)', color=COLOR_ORANGE, zorder=3, alpha=0.9)
bars2 = ax2.bar(x + width/2, time_20x20, width, label='Spacious ($20 \\times 20$)', color=COLOR_BLUE, zorder=3, alpha=0.9)

# 数值标签 - 设为加粗
def add_labels(bars):
    for bar in bars:
        height = bar.get_height()
        label_val = f'{height:.1f}' if height < 100 else f'{height:.0f}'
        ax2.annotate(label_val,
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 4),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=10, color='black', fontweight='bold', fontfamily='sans-serif')

add_labels(bars1)
add_labels(bars2)

# 坐标轴与网格设置 - 强制黑色加粗
ax2.set_yscale('log')
ax2.set_xlabel('Number of parts ($n$)', color='black', fontweight='bold', fontsize=13)
ax2.set_ylabel('CPU Time (s) [Log Scale]', color='black', fontweight='bold', fontsize=13)
ax2.set_xticks(x)
ax2.set_xticklabels(n_exp2)

for label in (ax2.get_xticklabels() + ax2.get_yticklabels()):
    label.set_fontweight('bold')

ax2.grid(True, which="major", axis='y', ls="-", linewidth=0.8, color=GRID_COLOR, zorder=0)
ax2.grid(True, which="minor", axis='y', ls="-", linewidth=0.5, color=GRID_COLOR, zorder=0)

# 调整 y 轴上限以容纳标签
ax2.set_ylim(top=max(time_20x20) * 3.5)

# 图例设置
ax2.legend(loc='upper left', frameon=True, fancybox=False, edgecolor='#CCCCCC', fontsize=11)

plt.tight_layout()
# 导出为 600 DPI 的 PNG 图片
fig2.savefig('fig2_capacity_ref.png', format='png', dpi=600, bbox_inches='tight')
plt.close(fig2)

print("4种算法对比的 PNG 图表已成功生成：fig1_efficiency_ref.png 和 fig2_capacity_ref.png")