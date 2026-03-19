import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker
import os

# ================== 1. 数据录入 (根据你的图片) ==================
data = {
    'NumParts': [
        2, 3, 4, 5, 6, 7, 8, 9, 10,
        11, 12, 13, 14, 15, 16, 17, 18,
        19, 20, 21, 22, 23, 24, 25
    ],
    'LB_Value': [
        787, 2149, 6757, 14939, 18120, 30553, 25512, 41857, 74336,
        135500, 227226, 253983, 244446, 357595, 395229, 379704, 453260,
        500479, 574366, 635949, 799235, 951248, 1002018, 1154840
    ]
}

df = pd.DataFrame(data)

# ================== 2. 绘图设置 ==================
# 设置风格：白色背景带网格
sns.set_theme(style="whitegrid", context="talk")

plt.figure(figsize=(12, 7))

# 定义颜色 (你可以改成之前喜欢的颜色)
point_color = "#4C72B0"  # 经典的深蓝色
line_color = "#4C72B0"

# --- A. 绘制折线图 (作为背景趋势) ---
# alpha=0.5 让线稍微淡一点，突出原本的点
sns.lineplot(
    x='NumParts',
    y='LB_Value',
    data=df,
    color=line_color,
    alpha=0.5,
    linewidth=2
)

# --- B. 绘制散点图 (核心数据) ---
# s=100 设置点的大小
# edgecolor='white' 给点加个白边，更有质感
sns.scatterplot(
    x='NumParts',
    y='LB_Value',
    data=df,
    color=point_color,
    s=120,
    edgecolor='white',
    linewidth=1.5,
    zorder=10  # 保证点在折线图的上层
)

# ================== 3. 细节美化 ==================

# 标题和标签
plt.title('LB-serial/LB-paral', fontsize=20, fontweight='bold', pad=20, color='#333333')
plt.xlabel('NumParts', fontsize=24, fontweight='bold', labelpad=10, color='#555555')
plt.ylabel('LB-serial/LB-paral', fontsize=24, fontweight='bold', labelpad=10, color='#555555')

# 设置 X 轴刻度 (确保显示整数，且不要太拥挤)
plt.xticks(range(2, 26, 2), fontsize=18)  # 每隔2个数字显示一个刻度
plt.yticks(fontsize=18)

# 设置 Y 轴格式化 (优化大数字显示)
ax = plt.gca()
# 方案 A: 使用科学计数法 (推荐，适合百万级数据)
formatter = ticker.ScalarFormatter(useMathText=True)
formatter.set_scientific(True)
formatter.set_powerlimits((-1, 1))
ax.yaxis.set_major_formatter(formatter)

# 方案 B: 如果你不想用科学计数法，想用千分位逗号 (如 1,000,000)，请取消下面这行的注释
# ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))

# 去除多余边框
sns.despine(trim=False, left=True)

# 优化网格线
ax.yaxis.grid(True, linestyle='--', which='major', color='grey', alpha=0.3)
ax.xaxis.grid(False)  # 竖向网格线通常不需要，看起来更干净

plt.tight_layout()

# 保存图片
save_path = 'plot/scatter_NumParts_trend.svg'
# 确保目录存在
if not os.path.exists('plot'):
    os.makedirs('plot')

plt.savefig(save_path, dpi=300, bbox_inches='tight')
print(f"散点图已保存至: {save_path}")

plt.show()