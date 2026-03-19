import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- 数据读取部分 (保持不变) ---
file_path_1 = 'Data/logs_LBupdate_test_DP_Ptcompare/13part_log_1_first_level_lbs.csv'
file_path_2 = 'Data/logs_BF_DFS_compare/13part_log_1_first_level_lbs.csv'

file_name_prefix = os.path.splitext(os.path.basename(file_path_1))[0]
output_folder = 'plot/boxplot_Ptcompare'
output_filename = f'{file_name_prefix}_boxplot_colored.svg'
output_path = os.path.join(output_folder, output_filename)

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

try:
    df1 = pd.read_csv(file_path_1)
    df2 = pd.read_csv(file_path_2)
except FileNotFoundError:
    exit()

df1['Source'] = 'LB_serial'
df2['Source'] = 'LB_parallel'
combined_df = pd.concat([df1, df2])

# ================== 🎨 配色方案 (保持不变) ==================
my_colors = ["#778899", "#B0C4DE"]
# ===========================================================

# 设置全局风格
sns.set_theme(style="whitegrid", context="talk")

# 保持你设定的大小
plt.figure(figsize=(12, 7))

# 绘制箱型图
ax = sns.boxplot(
    x='Source',
    y='Lower Bound',
    data=combined_df,
    palette=my_colors,
    width=0.5,
    linewidth=2,
    fliersize=0,
    saturation=0.9,
    order=['LB_serial', 'LB_parallel']
)

# 标题和标签美化
plt.title(f'Lower Bound Comparison', fontsize=24, fontweight='bold', pad=20, color='#333333')
plt.xlabel('Algorithm Strategy', fontsize=24, labelpad=10, fontweight='bold', color='#555555')
plt.ylabel('Lower Bound Value', fontsize=24, labelpad=10, fontweight='bold', color='#555555')

# 坐标轴刻度美化
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)

# --- 【修改点 1】 去边框设置 ---
# 将 trim=True 改为 trim=False (或者直接去掉 trim 参数，默认为 False)
# 这样 X 轴的线条就会贯穿整个底部，而不会只显示在两个刻度之间
sns.despine(trim=False, left=True)

# 优化网格线
ax.yaxis.grid(True, linestyle='--', which='major', color='grey', alpha=0.2)
ax.xaxis.grid(False)

# 自动调整布局
plt.tight_layout()

# --- 【修改点 2】 保存设置 ---
# 添加 bbox_inches='tight'，这能防止下方的文字标签在保存时被切掉
plt.savefig(output_path, dpi=300, bbox_inches='tight')

print(f"图表已保存 (修复X轴显示): {output_path}")
plt.show()