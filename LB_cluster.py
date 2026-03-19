import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np

# ================= 配置区域 =================
FILE_SERIAL = 'Data/logs_LBupdate_test_DP_hashDP_correction_exchange_fl_s_domi/15part_log_1_first_level_details.csv'  # compute_unassigned_lower_bound2 (DP/Serial)
FILE_PARALLEL = 'Data/logs_LBupdate_test_DP_hashDP_correction_exchange_fl_p_domi/15part_log_1_first_level_details.csv'  # compute_unassigned_lower_bound (Simple/Parallel)

# 输出文件夹名称
OUTPUT_DIR = 'plot/LB_cluster/15part'


# ===========================================

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def load_data():
    print(">>> 1. 正在读取 CSV 文件...")
    if not os.path.exists(FILE_SERIAL) or not os.path.exists(FILE_PARALLEL):
        raise FileNotFoundError("找不到输入文件，请检查文件名配置！")

    df_s = pd.read_csv(FILE_SERIAL)
    df_p = pd.read_csv(FILE_PARALLEL)

    df_s.columns = [c.strip() for c in df_s.columns]
    df_p.columns = [c.strip() for c in df_p.columns]

    df_s = df_s.rename(columns={'Lower Bound': 'LB_Serial'})
    df_p = df_p.rename(columns={'Lower Bound': 'LB_Parallel'})

    merged = pd.merge(
        df_s,
        df_p[['Node Name', 'LB_Parallel']],
        on='Node Name',
        suffixes=('_Serial', '_Parallel'),
        how='inner'
    )

    merged['Diff'] = merged['LB_Serial'] - merged['LB_Parallel']

    # 确保计数列是数字类型
    merged['Unassigned Count'] = pd.to_numeric(merged['Unassigned Count'], errors='coerce')

    # 原始索引（搜索顺序）
    merged['Original_Index'] = range(len(merged))

    return merged


def plot_charts(df, output_folder):
    sns.set_theme(style="ticks", font_scale=1.1)

    # 全局设置：让高值颜色更深，点更清晰
    GLOBAL_CMAP = 'viridis_r'  # 反转色谱：高值=深紫/蓝，低值=黄/绿
    GLOBAL_ALPHA = 0.8  # 提高不透明度
    GLOBAL_S = 12  # 点的大小

    # =========================================================
    # 图 0: 按未分配数量排序 (颜色加深版)
    # =========================================================
    print(">>> 正在绘制 [图 0]: 排序后的整体分布图...")
    df_sorted = df.sort_values(by=['Unassigned Count', 'Original_Index'], ascending=[True, True]).reset_index(drop=True)

    plt.figure(figsize=(16, 8))
    # 使用 viridis_r 让大值变深色
    sc = plt.scatter(df_sorted.index, df_sorted['Diff'], c=df_sorted['Diff'],
                     cmap=GLOBAL_CMAP, alpha=GLOBAL_ALPHA, s=GLOBAL_S, edgecolors='none')
    plt.axhline(0, color='red', linestyle='--', linewidth=1.5)

    unique_counts = sorted(df_sorted['Unassigned Count'].dropna().unique())
    last_boundary = 0
    colors = ['#f7f7f7', '#eef2f5']

    for i, count_val in enumerate(unique_counts):
        group_len = len(df_sorted[df_sorted['Unassigned Count'] == count_val])
        current_boundary = last_boundary + group_len
        if i < len(unique_counts) - 1:
            plt.axvline(current_boundary, color='gray', linestyle=':', alpha=0.5)

        mid_point = last_boundary + (group_len / 2)
        if group_len > len(df_sorted) * 0.02:
            plt.text(mid_point, df_sorted['Diff'].max() * 1.02, f"n={int(count_val)}",
                     ha='center', va='bottom', fontsize=10, fontweight='bold', color='#333')

        plt.axvspan(last_boundary, current_boundary, facecolor=colors[i % 2], alpha=0.3, zorder=0)
        last_boundary = current_boundary

    plt.title('LB Difference Sorted by Unassigned Part Count', fontsize=16)
    plt.xlabel('Sorted Node Index', fontsize=12)
    plt.ylabel('Difference (Serial - Parallel)', fontsize=12)
    plt.colorbar(sc, label='Difference Scale')
    plt.ylim(df_sorted['Diff'].min() * 1.05, df_sorted['Diff'].max() * 1.15)
    plt.tight_layout()
    plt.savefig(os.path.join(output_folder, '0_Scatter_Sorted_by_Count.png'), dpi=300)
    plt.close()

    # =========================================================
    # 图 1: 原始索引 (保持不变)
    # =========================================================
    print(">>> 正在绘制 [图 1]: 原始搜索顺序着色图...")
    plt.figure(figsize=(14, 8))
    sns.scatterplot(data=df, x='Original_Index', y='Diff', hue='Unassigned Count', palette='Spectral_r', alpha=0.6,
                    s=15, edgecolor=None)
    plt.axhline(0, color='black', linestyle='--')
    plt.title('LB Difference by Search Order (Colored by Count)', fontsize=16)
    plt.savefig(os.path.join(output_folder, '1_Scatter_SearchOrder.png'), dpi=300)
    plt.close()

    # =========================================================
    # 图 2: 箱线图 (保持不变)
    # =========================================================
    print(">>> 正在绘制 [图 2]: 箱线图...")
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df, x='Unassigned Count', y='Diff', hue='Unassigned Count', palette="Blues", legend=False)
    plt.axhline(0, color='red', linestyle='--')
    plt.title('Distribution of Diff by Unassigned Count', fontsize=16)
    plt.savefig(os.path.join(output_folder, '2_BoxPlot.png'), dpi=300)
    plt.close()

    # =========================================================
    # 自动列名检测
    # =========================================================
    target_col = None
    possible_names = ['Unassigned Parts', 'Unassigned Parts_Serial']
    for name in possible_names:
        if name in df.columns:
            target_col = name
            break

    if target_col:
        # =========================================================
        # 图 3: Top 20 Worst Cases (保持不变)
        # =========================================================
        print(">>> 正在绘制 [图 3]: 表现最差的 Top 20 零件组合...")
        worst_df = df.sort_values('Diff').head(20)
        plt.figure(figsize=(12, 8))
        y_labels = worst_df[target_col].apply(lambda x: str(x)[:40] + '...' if len(str(x)) > 40 else str(x))
        sns.barplot(x=worst_df['Diff'], y=y_labels, hue=y_labels, palette='Reds_r', legend=False)
        plt.title('Top 20 Worst Cases (Specific Part Combinations)', fontsize=16)
        plt.xlabel('Difference (Serial - Parallel)')
        plt.ylabel('Unassigned Parts Combination')
        plt.axvline(0, color='black', linestyle='--')
        plt.tight_layout()
        plt.savefig(os.path.join(output_folder, '3_Worst_Cases_Parts.png'), dpi=300)
        plt.close()

        # 准备数据：增加 Has_Zero 列
        def check_contains_zero(val):
            if pd.isna(val): return False
            parts = str(val).strip().split(';')
            return '0' in parts

        df_z = df.copy()
        df_z['Has_Zero'] = df_z[target_col].apply(check_contains_zero)

        # =========================================================
        # 图 4: 是否包含零件 0 (颜色加深版)
        # =========================================================
        print(">>> 正在绘制 [图 4]: 是否包含零件 0 的对比分析...")
        df_sorted_z = df_z.sort_values(by=['Has_Zero', 'Original_Index']).reset_index(drop=True)

        plt.figure(figsize=(16, 8))
        sc = plt.scatter(df_sorted_z.index, df_sorted_z['Diff'],
                         c=df_sorted_z['Diff'], cmap=GLOBAL_CMAP, alpha=GLOBAL_ALPHA, s=GLOBAL_S, edgecolors='none')
        plt.axhline(0, color='red', linestyle='--', linewidth=1.5)

        count_no_zero = len(df_sorted_z[df_sorted_z['Has_Zero'] == False])
        total_len = len(df_sorted_z)

        if 0 < count_no_zero < total_len:
            plt.axvline(count_no_zero, color='black', linestyle='-', linewidth=2, alpha=0.5)

        if count_no_zero > 0:
            plt.axvspan(0, count_no_zero, facecolor='#f7f7f7', alpha=0.5)
            plt.text(count_no_zero / 2, df_sorted_z['Diff'].max() * 1.05,
                     f"WITHOUT Part 0\n(Count: {count_no_zero})",
                     ha='center', va='bottom', fontsize=12, fontweight='bold', color='darkblue')

        if count_no_zero < total_len:
            plt.axvspan(count_no_zero, total_len, facecolor='#fff3cd', alpha=0.3)
            center_pos = count_no_zero + (total_len - count_no_zero) / 2
            plt.text(center_pos, df_sorted_z['Diff'].max() * 1.05,
                     f"WITH Part 0\n(Count: {total_len - count_no_zero})",
                     ha='center', va='bottom', fontsize=12, fontweight='bold', color='darkred')

        plt.title('LB Difference Analysis: Presence of Part 0', fontsize=16)
        plt.ylim(df_sorted_z['Diff'].min() * 1.05, df_sorted_z['Diff'].max() * 1.15)
        plt.colorbar(sc, label='Difference Scale')
        plt.tight_layout()
        plt.savefig(os.path.join(output_folder, '4_Scatter_Part0_Presence.png'), dpi=300)
        plt.close()

        # =========================================================
        # [新增] 图 5: 嵌套聚类 (Has Zero -> Unassigned Count)
        # =========================================================
        print(">>> 正在绘制 [图 5]: 嵌套聚类分析 (Part 0 -> Count)...")

        # 1. 嵌套排序：先按 Has_Zero, 再按 Count, 最后按 Index
        df_nested = df_z.sort_values(by=['Has_Zero', 'Unassigned Count', 'Original_Index']).reset_index(drop=True)

        plt.figure(figsize=(16, 8))
        sc = plt.scatter(df_nested.index, df_nested['Diff'],
                         c=df_nested['Diff'], cmap=GLOBAL_CMAP, alpha=GLOBAL_ALPHA, s=GLOBAL_S, edgecolors='none')
        plt.axhline(0, color='red', linestyle='--', linewidth=1.5)

        # 2. 绘制主要分界线 (Part 0)
        split_idx = len(df_nested[df_nested['Has_Zero'] == False])
        if 0 < split_idx < len(df_nested):
            plt.axvline(split_idx, color='black', linestyle='-', linewidth=2.5, alpha=0.6)

            # 绘制左右大背景
            plt.axvspan(0, split_idx, facecolor='#f7f7f7', alpha=0.5)  # 左：灰
            plt.axvspan(split_idx, len(df_nested), facecolor='#fff3cd', alpha=0.3)  # 右：黄

            # 大标签
            plt.text(split_idx / 2, df_nested['Diff'].max() * 1.10, "WITHOUT Part 0",
                     ha='center', va='bottom', fontsize=14, fontweight='bold', color='darkblue')
            plt.text(split_idx + (len(df_nested) - split_idx) / 2, df_nested['Diff'].max() * 1.10, "WITH Part 0",
                     ha='center', va='bottom', fontsize=14, fontweight='bold', color='darkred')

        # 3. 绘制次级分界线 (Unassigned Count)
        # 我们需要分别遍历两部分来画虚线，避免画在主分界线旁边太乱

        # 辅助函数：绘制内部虚线和标签
        def draw_sub_dividers(start_idx, sub_df):
            unique_cts = sorted(sub_df['Unassigned Count'].dropna().unique())
            last_sub_bound = start_idx

            for i, ct in enumerate(unique_cts):
                count_len = len(sub_df[sub_df['Unassigned Count'] == ct])
                current_sub_bound = last_sub_bound + count_len

                # 画虚线 (不要画在最右边，也不要和主分界线重叠)
                if i < len(unique_cts) - 1:
                    plt.axvline(current_sub_bound, color='gray', linestyle=':', linewidth=1, alpha=0.5)

                # 写小标签 (n=x)
                mid = last_sub_bound + (count_len / 2)
                # 只有当区域够宽时才写，防止密密麻麻
                if count_len > len(df_nested) * 0.015:
                    plt.text(mid, df_nested['Diff'].max() * 1.02, f"n={int(ct)}",
                             ha='center', va='bottom', fontsize=9, color='#555')

                last_sub_bound = current_sub_bound

        # 对左半部分 (No Zero) 画细分
        draw_sub_dividers(0, df_nested[df_nested['Has_Zero'] == False])

        # 对右半部分 (With Zero) 画细分
        draw_sub_dividers(split_idx, df_nested[df_nested['Has_Zero'] == True])

        plt.title('Nested Clustering: Presence of Part 0 -> Unassigned Count', fontsize=16)
        plt.xlabel('Sorted Node Index', fontsize=12)
        plt.ylabel('Difference (Serial - Parallel)', fontsize=12)
        plt.colorbar(sc, label='Difference Scale')
        plt.ylim(df_nested['Diff'].min() * 1.05, df_nested['Diff'].max() * 1.18)  # 留更多顶部空间给两层标签
        plt.tight_layout()
        plt.savefig(os.path.join(output_folder, '5_Scatter_Nested_Clustering.png'), dpi=300)
        plt.close()
        print("    -> 图 5 绘制成功！")

    else:
        print(f"    -> 错误：未找到未分配零件列，跳过图 3, 4, 5。现有列: {list(df.columns)}")

def main():
    ensure_dir(OUTPUT_DIR)
    try:
        df = load_data()
        plot_charts(df, OUTPUT_DIR)
        print(f"\n✅ 分析完成！结果保存在: ./{OUTPUT_DIR}/")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()