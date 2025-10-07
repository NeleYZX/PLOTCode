import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 假设你的两个CSV文件路径如下
file_path_1 = '5part_log_2_first_level_lbs.csv'
file_path_2 = '5part_log_1_first_level_lbs.csv' # 假设第二个文件的名称

# 读取第一个CSV文件
try:
    df1 = pd.read_csv(file_path_1)
    print(f"成功读取文件: {file_path_1}")
    print(df1.head())
except FileNotFoundError:
    print(f"错误：文件 {file_path_1} 未找到。请检查文件路径。")
    exit()

# 读取第二个CSV文件
try:
    df2 = pd.read_csv(file_path_2)
    print(f"成功读取文件: {file_path_2}")
    print(df2.head())
except FileNotFoundError:
    print(f"错误：文件 {file_path_2} 未找到。请检查文件路径。")
    exit()

# 合并两个DataFrame，添加一个'Source'列来区分数据来源
df1['Source'] = 'File 2' # 根据你的文件名，我将第一个文件标记为'File 2'
df2['Source'] = 'File 1' # 假设这是另一个文件

combined_df = pd.concat([df1, df2])

# 绘制箱型图
plt.figure(figsize=(10, 6))
sns.boxplot(x='Source', y='Lower Bound', data=combined_df)

plt.title('Comparison of Lower Bounds from Two Files')
plt.xlabel('Data Source')
plt.ylabel('Lower Bound Value')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

print("\n箱型图已生成。")