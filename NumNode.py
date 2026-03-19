import matplotlib.pyplot as plt
import numpy as np

# ==========================================
# 顶级期刊标准排版设置
# ==========================================
# 强制使用 Times New Roman 字体
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']
plt.rcParams['font.size'] = 12
plt.rcParams['axes.linewidth'] = 1.0

COLOR_BLUE = '#1f77b4'  # BB_par: 蓝色
COLOR_RED = '#d62728'  # BB_serial: 红色
# 【修改核心 1】：替换为高对比度且美观的亮橙色 (Vivid Orange)
COLOR_LINE = '#FF9900'
GRID_COLOR = '#EAEAEA'
TEXT_COLOR = '#000000'

# ==========================================
# 数据准备
# ==========================================
n_vals = np.array([14, 15, 16, 17, 18, 19])
par_nodes_m = np.array([7.7, 23, 62, 187, 462, 929])
ser_nodes_m = np.array([6.5, 17, 55, 165, 409, 644])
reduction_pct = np.array([15.6, 22.8, 10.5, 11.6, 11.4, 30.6])

# ==========================================
# 绘制高清、清晰对比的双轴组合图
# ==========================================
fig, ax_bar = plt.subplots(figsize=(8.5, 5.5))
ax_bar.spines['top'].set_visible(False)

x_pos = np.arange(len(n_vals))
width = 0.35

# 绘制柱状图 (位于底层 ax_bar)
bars1 = ax_bar.bar(x_pos - width / 2, par_nodes_m, width, label=r'$BB_{par}$', color=COLOR_BLUE, edgecolor='black',
                   alpha=0.85)
bars2 = ax_bar.bar(x_pos + width / 2, ser_nodes_m, width, label=r'$BB_{serial}$', color=COLOR_RED, edgecolor='black',
                   alpha=0.85)

ax_bar.set_xlabel('Number of parts ($n$)', color='black', fontweight='bold', fontsize=13)
ax_bar.set_ylabel('Average Explored Nodes ($10^6$)', color='black', fontweight='bold', fontsize=13)
ax_bar.set_xticks(x_pos)
ax_bar.set_xticklabels(n_vals)

# 调高左轴 Y 轴上限，防止柱子顶到最上面
ax_bar.set_ylim(0, max(par_nodes_m) * 1.25)

# ------------------------------------------
# 创建共享 X 轴的右侧折线图层 (ax_line)
# ------------------------------------------
ax_line = ax_bar.twinx()
ax_line.spines['top'].set_visible(False)

# 绘制折线图 (Z-order=5，处于折线图层底部)
line = ax_line.plot(x_pos, reduction_pct, color=COLOR_LINE, marker='o', markersize=9,
                    linewidth=3, linestyle='-', label='Nodes Reduced (%)', zorder=5,
                    markeredgecolor='white', markeredgewidth=2)

# 带橙色边框的折线悬浮数据标签
bbox_props = dict(boxstyle="round,pad=0.3", fc="white", ec=COLOR_LINE, lw=1.5, alpha=0.95)

# 为每个百分比标签定制垂直偏移量，物理避开柱子顶部的数字
# 特别是针对 n=18 (索引4)，使其标签向下偏移(-25)，完美让出空间
y_offsets = [15, 15, -20, 15, -25, -20]

for i, txt in enumerate(reduction_pct):
    ax_line.annotate(f'{txt:.1f}%', (x_pos[i], reduction_pct[i]), xytext=(0, y_offsets[i]),
                     textcoords="offset points", ha='center', va='center',
                     fontweight='bold', color=COLOR_LINE, fontsize=11,
                     bbox=bbox_props, zorder=6)

ax_line.set_ylabel('Reduction in Search Space (%)', color=COLOR_LINE, fontweight='bold', fontsize=13)
ax_line.set_ylim(0, max(reduction_pct) * 1.35)

# ------------------------------------------
# 【修改核心 2】：跨图层写入柱状图数字，彻底解决遮挡！
# ------------------------------------------
# 将柱子的数字写在 ax_line 图层上，并使用 ax_bar 的坐标系 (transform=ax_bar.transData)
# 这样不仅保证数字绝对处于折线之上 (zorder=10)，而且坐标完全精准。
for bar in bars1 + bars2:
    height = bar.get_height()
    label_text = f'{height:.1f}' if height < 10 else f'{height:.0f}'

    # 注意这里使用的是 ax_line.text，但映射了 ax_bar 的坐标系
    ax_line.text(bar.get_x() + bar.get_width() / 2, height + (max(par_nodes_m) * 0.015),
                 label_text, transform=ax_bar.transData,
                 ha='center', va='bottom', fontsize=9, fontweight='bold', zorder=10)

# ------------------------------------------
# 全局样式与排版收尾
# ------------------------------------------
for label in (ax_bar.get_xticklabels() + ax_bar.get_yticklabels() + ax_line.get_yticklabels()):
    label.set_fontweight('bold')

ax_bar.grid(True, axis='y', ls="--", linewidth=0.5, color=GRID_COLOR, zorder=0)

# 合并双轴图例
lines_1, labels_1 = ax_bar.get_legend_handles_labels()
lines_2, labels_2 = ax_line.get_legend_handles_labels()
ax_bar.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left', frameon=True, edgecolor='#CCCCCC', fontsize=11)

plt.tight_layout()
fig.savefig('fig5_dual_axis_combo_perfect.png', format='png', dpi=600, bbox_inches='tight')
plt.show()

print("完美版双轴图已生成：色彩高级、0遮挡、超高对比度！")