import pandas as pd
import matplotlib.pyplot as plt

# 读取 CSV 文件
df = pd.read_csv('data.csv')

# 绘图
plt.figure(figsize=(10, 6))
plt.plot(df['Time'], df['UB'], label='UB (Upper Bound)', color='red')
plt.plot(df['Time'], df['LB'], label='LB (Lower Bound)', color='blue')
plt.xlabel('Time')
plt.ylabel('Value')
plt.title('UB and LB over Time')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
