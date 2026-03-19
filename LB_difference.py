import pandas as pd
import matplotlib.pyplot as plt
import os


def plot_lower_bound_difference(file1_path, file2_path, output_folder="plot/LB_difference_domi_s"):
    """
    读取两个CSV文件，计算并绘制其"Lower Bound"列的差值散点图，
    并将图像保存到指定文件夹中，命名沿用输入数据的文件命名。

    Args:
        file1_path (str): 第一个CSV文件的路径。
        file2_path (str): 第二个CSV文件的路径。
        output_folder (str): 保存图像的文件夹路径。默认为 "output_plots"。
    """
    try:
        # 读取第一个CSV文件
        df1 = pd.read_csv(file1_path)
        # 读取第二个CSV文件
        df2 = pd.read_csv(file2_path)
    except FileNotFoundError:
        print("错误：文件未找到。请检查文件路径是否正确。")
        return
    except KeyError:
        print("错误：CSV文件中未找到 'Lower Bound' 列。请检查列名是否正确。")
        return
    except Exception as e:
        print(f"读取CSV文件时发生错误：{e}")
        return

    # 确保两个DataFrame都有 'Lower Bound' 列
    if 'Lower Bound' not in df1.columns or 'Lower Bound' not in df2.columns:
        print("错误：两个CSV文件都必须包含 'Lower Bound' 列。")
        return

    min_rows = min(len(df1), len(df2))

    lb1 = df1['Lower Bound'].iloc[:min_rows]
    lb2 = df2['Lower Bound'].iloc[:min_rows]

    differences = lb1 - lb2

    # 创建散点图
    plt.figure(figsize=(12, 7))  # 可以稍微调整图的大小以更好地显示
    plt.scatter(range(len(differences)), differences, alpha=0.7, s=10)  # s参数控制散点大小
    plt.title(f'Lower Bound Difference')
    plt.xlabel('Data Point Index')
    plt.ylabel('Lower Bound Difference (File1 - File2)')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.axhline(0, color='red', linestyle='--', linewidth=1)  # 添加零线

    # --- 添加保存图像的逻辑 ---
    # 创建输出文件夹，如果它不存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"创建了输出文件夹：{output_folder}")

    # 获取第一个CSV文件的文件名（不带路径和扩展名）
    file1_name_base = os.path.splitext(os.path.basename(file1_path))[0]
    # 获取第二个CSV文件的文件名（不带路径和扩展名）
    file2_name_base = os.path.splitext(os.path.basename(file2_path))[0]

    # 构建图像文件名
    # 例如：10part_log_2_first_level_lbs_vs_10part_log_2_second_level_lbs_diff.png
    output_filename = f"{file2_name_base}_diff.png"
    output_filepath = os.path.join(output_folder, output_filename)

    # 保存图像
    plt.savefig(output_filepath, bbox_inches='tight')  # bbox_inches='tight' 确保所有内容都包含在内
    plt.show()
    # plt.close()  # 关闭图形，避免在循环中生成过多图形占用内存

    print(f"差值散点图已生成并保存到：{output_filepath}")

file_path_1 = 'Data/logs_LBupdate_test_DP_hashDP_correction_exchange_s_domi/15part_log_1_first_level_lbs.csv'
file_path_2 = 'Data/logs_LBupdate_test_DP_hashDP_correction_exchange_p_domi/15part_log_1_first_level_lbs.csv' # 假设第二个文件的名称
plot_lower_bound_difference(file_path_1, file_path_2)