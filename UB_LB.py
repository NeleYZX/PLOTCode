import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
import os

def UB_LB(path):
    # 设置风格和字体
    sns.set(style="whitegrid")
    mpl.rcParams['font.family'] = 'serif'
    mpl.rcParams['font.size'] = 12
    mpl.rcParams['axes.titlesize'] = 14
    mpl.rcParams['axes.labelsize'] = 12
    mpl.rcParams['legend.fontsize'] = 11
    mpl.rcParams['xtick.labelsize'] = 11
    mpl.rcParams['ytick.labelsize'] = 11
    mpl.rcParams['axes.edgecolor'] = 'black'
    mpl.rcParams['axes.linewidth'] = 1.0

    # 读取数据
    df = pd.read_csv(path)
    base_filename = os.path.splitext(os.path.basename(path))[0]

    # 创建图像，固定宽高比（6.5:4.5）
    fig, ax = plt.subplots(figsize=(6.5, 4.5))

    # 绘制UB和LB曲线
    ax.plot(df['Time'], df['UB'], label='Upper Bound (UB)', color='red', linewidth=2)
    ax.plot(df['Time'], df['LB'], label='Lower Bound (LB)', color='steelblue', linewidth=2)

    # 设置标题和坐标轴标签
    ax.set_title('UB and LB over Time', fontweight='bold')
    ax.set_xlabel('Time')
    ax.set_ylabel('Value')

    # 添加网格线
    ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)

    # 图例在右上角，带边框
    ax.legend(loc='upper right', frameon=True, edgecolor='black')

    # # 标注极值点
    # # max_ub = df.loc[df['UB'].idxmax()]
    # # min_lb = df.loc[df['LB'].idxmin()]
    #
    # ax.annotate(f'Max UB = {max_ub["UB"]:.1f}',
    #             xy=(max_ub['Time'], max_ub['UB']),
    #             xytext=(max_ub['Time'] + 1, max_ub['UB'] + 10),
    #             arrowprops=dict(arrowstyle='->', color='gray'),
    #             fontsize=10)
    #
    # ax.annotate(f'Min LB = {min_lb["LB"]:.1f}',
    #             xy=(min_lb['Time'], min_lb['LB']),
    #             xytext=(min_lb['Time'] + 1, min_lb['LB'] - 20),
    #             arrowprops=dict(arrowstyle='->', color='gray'),
    #             fontsize=10)

    # 保留四边边框（关闭默认despine去除边框的行为）
    sns.despine(ax=ax, top=False, right=False, left=False, bottom=False)

    # 自动调整布局，保持比例
    plt.tight_layout()

    # 保存图像
    output_dir = 'plot/logs_LBupdate_base_BF_DFS_DP'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f'{base_filename}_UB_LB.png')
    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f'图像已保存至: {output_path}')


exp = ['Data/logs_BF_DFS/5part_log_1_bounds.csv', 'Data/logs_BF_DFS/10part_log_2_bounds.csv', 'Data/logs_BF_DFS/11part_log_3_bounds.csv',
        'Data/logs_BF_DFS/12part_log_1_bounds.csv','Data/logs_BF_DFS/13part_log_1_bounds.csv', 'Data/logs_BF_DFS/14part_log_1_bounds.csv',
       'Data/logs_BF_DFS/15part_log_1_bounds.csv']
exp1 = ['Data/logs_LBupdate_base_BF_DFS_DP/11part_log_1_bounds.csv']
for i in exp1:
    UB_LB(i)



