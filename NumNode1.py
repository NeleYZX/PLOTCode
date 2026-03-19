import matplotlib.pyplot as plt
import numpy as np

# ==========================================
# 顶级期刊标准排版设置 - 全局黑字加粗适配
# ==========================================
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']
plt.rcParams['font.size'] = 12
plt.rcParams['axes.linewidth'] = 1.2  # 配合大图，边框稍微加粗
plt.rcParams['text.color'] = 'black'

COLOR_BLUE = '#1f77b4'  # BB-parallel
COLOR_RED = '#d62728'   # BB-serial
COLOR_AMBER = '#FFBF00' # BB-hybrid (亮黄色)
GRID_COLOR = '#EAEAEA'

# ==========================================
# 数据准备 (取表格中各 n 值的平均值，单位：10^6)
# ==========================================
n_vals = np.array([14, 15, 16, 17, 18, 19])

# 平均值计算 (10^6 单位)
avg_par = np.array([77.7, 236.1, 616.6, 1869.3, 4626.3, 9382.1]) / 10
avg_ser = np.array([60.1, 174.2, 551.8, 1654.8, 4093.8, 6447.8]) / 10
avg_hyb = np.array([74.4, 221.0, 583.2, 1775.6, 4376.0, 9162.4]) / 10

# ==========================================
# 绘制高清对比图 - 放大尺寸
# ==========================================
# 【修改点 1】：图片长宽放大到 12 x 7.5
fig, ax = plt.subplots(figsize=(12, 7.5))
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

x_pos = np.arange(len(n_vals))
width = 0.28

# 绘制三组柱状图
bars1 = ax.bar(x_pos - width, avg_par, width, label='BB-parallel', color=COLOR_BLUE, edgecolor='black', alpha=0.85, zorder=5)
bars2 = ax.bar(x_pos, avg_ser, width, label='BB-serial', color=COLOR_RED, edgecolor='black', alpha=0.85, zorder=5)
bars3 = ax.bar(x_pos + width, avg_hyb, width, label='BB-hybrid', color=COLOR_AMBER, edgecolor='black', alpha=0.85, zorder=5)

# 【修改点 2】：坐标轴标签强制纯黑、加粗，字号放大至 14
ax.set_xlabel('Number of parts ($n$)', color='black', fontweight='bold', fontsize=26)
ax.set_ylabel('Average Explored Nodes ($10^6$)', color='black', fontweight='bold', fontsize=26)
ax.set_xticks(x_pos)

# 调高 Y 轴上限，防止数字顶到边框
ax.set_ylim(0, max(avg_par) * 1.15)

# ------------------------------------------
# 数值标注 - 强制黑字加粗，字号10
# ------------------------------------------
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        label_text = f'{height:.1f}' if height < 100 else f'{height:.0f}'
        ax.text(rect.get_x() + rect.get_width() / 2, height + (max(avg_par) * 0.015),
                label_text, ha='center', va='bottom',
                color='black', fontsize=16, fontweight='bold', zorder=14)

autolabel(bars1)
autolabel(bars2)
autolabel(bars3)

# ------------------------------------------
# 全局样式收尾 - 刻度和图例黑字加粗
# ------------------------------------------
# X轴刻度黑字加粗
ax.set_xticklabels(n_vals, color='black', fontweight='bold', fontsize=24)

# Y轴刻度黑字加粗
for label in ax.get_yticklabels():
    label.set_color('black')
    label.set_fontweight('bold')
    label.set_fontsize(24)

ax.grid(True, axis='y', ls="--", linewidth=0.5, color=GRID_COLOR, zorder=0)

# 图例边框和文字黑字加粗
legend = ax.legend(loc='upper left', frameon=True, edgecolor='black')
for text in legend.get_texts():
    text.set_color('black')
    text.set_fontweight('bold')
    text.set_fontsize(22)

plt.tight_layout()
fig.savefig('triple_algorithm_large_bold.pdf', format='pdf', dpi=600, bbox_inches='tight')
plt.show()