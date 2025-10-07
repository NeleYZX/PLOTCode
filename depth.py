import pandas as pd
import matplotlib.pyplot as plt
import os

def depth(path):
    # 读取 CSV 文件
    df = pd.read_csv(path)
    base_filename = os.path.splitext(os.path.basename(path))[0]
    # 设置绘图风格
    plt.style.use('seaborn-v0_8-whitegrid')  # 替代 seaborn-whitegrid

    # 绘图
    plt.figure(figsize=(8, 5))
    plt.plot(df['Depth'], df['PrunedNodes'], marker='o', linestyle='-', linewidth = 3,color='blue')
    plt.xticks(df['Depth'])  # 保证横坐标为整数
    plt.xlabel('Depth', fontsize=12)
    plt.ylabel('Pruned Nodes', fontsize=12)
    plt.title('Pruned Nodes vs Depth', fontsize=14)
    plt.tight_layout()

    # 保存图片
    # 保存路径设定
    output_dir = 'plot/logs_LBupdate_base_BF_DFS_DP'  # 替换为你需要的保存路径
    os.makedirs(output_dir, exist_ok=True)

    # 保存图像到该路径
    # plt.savefig(os.path.join(output_dir, f'{base_filename}.pdf'))
    plt.savefig(os.path.join(output_dir, f'{base_filename}.png'), dpi=300)
    plt.show()

exp = exp = ['Data/logs_NewLB/5part_log_5_pruned_per_depth.csv', 'Data/logs_NewLB/10part_log_4_pruned_per_depth.csv', 'Data/logs_NewLB/11part_log_4_pruned_per_depth.csv',
        'Data/logs_NewLB/12part_log_4_pruned_per_depth.csv','Data/logs_NewLB/13part_log_2_pruned_per_depth.csv', 'Data/logs_NewLB/14part_log_3_pruned_per_depth.csv',
       'Data/logs_NewLB/15part_log_3_pruned_per_depth.csv']
exp1 = ['Data/logs_LBupdate_base_BF_DFS_DP/11part_log_1_pruned_per_depth.csv']
for i in exp1:
    depth(i)

