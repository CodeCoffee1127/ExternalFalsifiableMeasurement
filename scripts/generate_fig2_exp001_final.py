#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fig. 2: VSP Four-Criteria Verification (EXP001) - FINAL VERSION
VSP四维度验证 - 最终版本

修正要求：
1. 从柱状图改回雷达图（与§3-B文本描述严格对应）
2. 四轴分别对应：Stability、Precision、Calibration、Structural Consistency
3. Calibration轴用红色标记为FAIL，标注"|bias|=0.50 (25× tolerance)"
4. 通过准则填充浅蓝色，失败准则填充浅红色
5. 阈值线使用橙色虚线
6. 添加图例："Blue: Actual value; Orange: VSP threshold; Red: Calibration failure"
7. 文件名改为LaTeX兼容格式：fig2_exp001_vsp_radar.{pdf/png}
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

project_root = Path(__file__).parent.parent
FIGURES_DIR = project_root / "figures" / "paper"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# EXP001实验数据（来自论文）
# 四个准则的实际值和阈值
criteria = [
    "Stability (r)",
    "Precision (CV)",
    "Calibration (|bias|)",
    "Structural (ρ)"
]

# 实际值
actual_values = [0.9897, 0.0170, 0.5000, 0.8168]

# 阈值
thresholds = [0.9500, 0.0500, 0.0200, 0.7000]

# 方向：True表示越大越好，False表示越小越好
directions = [True, False, False, True]

# 状态
statuses = ["PASS", "PASS", "FAIL", "PASS"]

# 计算归一化值（用于雷达图，统一为"越大越好"）
def normalize_values(values, thresholds, directions):
    """将值归一化到0-1范围，统一为越大越好"""
    normalized = []
    for val, thresh, dir in zip(values, thresholds, directions):
        if dir:
            # 越大越好
            if val >= thresh:
                norm_val = 0.9 + (val - thresh) * 0.1  # 超过阈值的部分映射到0.9-1.0
                norm_val = min(norm_val, 1.0)
            else:
                norm_val = (val / thresh) * 0.9  # 未超过阈值的部分映射到0-0.9
        else:
            # 越小越好
            if val <= thresh:
                norm_val = 0.9 + (1 - val/thresh) * 0.1  # 低于阈值的部分映射到0.9-1.0
                norm_val = min(norm_val, 1.0)
            else:
                norm_val = (1 - (val - thresh)/max(val, thresh)) * 0.9  # 超过阈值的部分映射到0-0.9
                norm_val = max(norm_val, 0.0)
        normalized.append(norm_val)
    return normalized

# 计算归一化阈值
def normalize_thresholds(thresholds, directions):
    """将阈值归一化到0-1范围"""
    normalized = []
    for thresh, dir in zip(thresholds, directions):
        if dir:
            # 越大越好，阈值对应0.9
            normalized.append(0.9)
        else:
            # 越小越好，阈值对应0.9
            normalized.append(0.9)
    return normalized

def generate_fig2_radar():
    """生成Fig. 2: VSP Four-Criteria Verification（雷达图版本）"""
    
    plt.rcParams.update({
        'font.size': 10,
        'axes.labelsize': 11,
        'axes.titlesize': 12,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 9,
        'figure.dpi': 300,
        'savefig.dpi': 300,
        'savefig.bbox': 'tight',
        'axes.linewidth': 0.8,
        'xtick.major.width': 0.8,
        'ytick.major.width': 0.8,
    })
    
    # 计算归一化值
    norm_actual = normalize_values(actual_values, thresholds, directions)
    norm_threshold = normalize_thresholds(thresholds, directions)
    
    # 雷达图参数
    N = len(criteria)
    angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
    angles += angles[:1]  # 闭合
    
    norm_actual += norm_actual[:1]
    norm_threshold += norm_threshold[:1]
    
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    
    # 调整布局
    plt.subplots_adjust(left=0.1, right=0.9, top=0.85, bottom=0.15)
    
    # 绘制阈值多边形（橙色虚线）
    ax.plot(angles, norm_threshold, 'o--', linewidth=2, color='#FF9800', alpha=0.7,
            label='VSP threshold')
    
    # 填充通过区域（浅蓝色半透明）
    pass_values = [norm_actual[i] if statuses[i] == "PASS" else 0 for i in range(N)]
    pass_values += pass_values[:1]
    ax.fill(angles, pass_values, color='#E3F2FD', alpha=0.4, edgecolor='#2196F3', linewidth=1)
    
    # 填充失败区域（浅红色半透明）
    fail_values = [norm_actual[i] if statuses[i] == "FAIL" else 0 for i in range(N)]
    fail_values += fail_values[:1]
    ax.fill(angles, fail_values, color='#FFEBEE', alpha=0.4, edgecolor='#F44336', linewidth=1)
    
    # 绘制实际值点（蓝色）
    for i in range(N):
        if statuses[i] == "FAIL":
            # 失败的点用红色
            ax.plot(angles[i], norm_actual[i], 'o', markersize=10, 
                    color='#F44336', markeredgecolor='black', linewidth=1.5,
                    label='Calibration failure' if i == 2 else "")
        else:
            # 通过的点用蓝色
            ax.plot(angles[i], norm_actual[i], 'o', markersize=8, 
                    color='#2196F3', markeredgecolor='black', linewidth=1)
    
    # 绘制实际值连线（蓝色）
    ax.plot(angles, norm_actual, '-', linewidth=2, color='#2196F3', alpha=0.8,
            label='Actual value')
    
    # 设置角度标签
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(criteria, fontsize=10, fontweight='bold')
    
    # 设置径向标签
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels(['0', '0.25', '0.5', '0.75', '1.0'], fontsize=8)
    ax.set_ylim(0, 1.1)
    
    # 添加标题
    ax.set_title('Fig. 2: VSP Four-Criteria Verification (EXP001)', 
                fontsize=13, fontweight='bold', pad=20)
    
    # 添加图例
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=9)
    
    # 添加详细标注
    # Calibration轴的特殊标注
    ax.annotate(
        '|bias|=0.50\n(25× tolerance)',
        xy=(angles[2], norm_actual[2]),
        xytext=(angles[2] + 0.3, norm_actual[2] + 0.1),
        fontsize=10, fontweight='bold', color='#F44336',
        bbox=dict(boxstyle='round', facecolor='#FFEBEE', 
                 edgecolor='#F44336', linewidth=1.5),
        arrowprops=dict(arrowstyle='->', color='#F44336', lw=1.5),
        zorder=10
    )
    
    # 其他通过轴的标注
    # Stability
    ax.annotate(
        f'r = {actual_values[0]:.4f}',
        xy=(angles[0], norm_actual[0]),
        xytext=(angles[0] - 0.2, norm_actual[0] + 0.05),
        fontsize=9, fontweight='bold', color='#2196F3',
        bbox=dict(boxstyle='round', facecolor='#E3F2FD', 
                 edgecolor='#2196F3', linewidth=1),
        arrowprops=dict(arrowstyle='->', color='#2196F3', lw=1),
        zorder=10
    )
    
    # Precision
    ax.annotate(
        f'CV = {actual_values[1]:.4f}',
        xy=(angles[1], norm_actual[1]),
        xytext=(angles[1] - 0.2, norm_actual[1] + 0.05),
        fontsize=9, fontweight='bold', color='#2196F3',
        bbox=dict(boxstyle='round', facecolor='#E3F2FD', 
                 edgecolor='#2196F3', linewidth=1),
        arrowprops=dict(arrowstyle='->', color='#2196F3', lw=1),
        zorder=10
    )
    
    # Structural
    ax.annotate(
        f'ρ = {actual_values[3]:.4f}',
        xy=(angles[3], norm_actual[3]),
        xytext=(angles[3] + 0.2, norm_actual[3] + 0.05),
        fontsize=9, fontweight='bold', color='#2196F3',
        bbox=dict(boxstyle='round', facecolor='#E3F2FD', 
                 edgecolor='#2196F3', linewidth=1),
        arrowprops=dict(arrowstyle='->', color='#2196F3', lw=1),
        zorder=10
    )
    
    # 添加总体状态标注
    total_pass = sum(1 for s in statuses if s == "PASS")
    ax.text(
        0.5, 0.05, 
        f'{total_pass}/4 Criteria Passed',
        transform=ax.transAxes,
        fontsize=12, fontweight='bold', color='black',
        horizontalalignment='center',
        bbox=dict(boxstyle='round', facecolor='white', 
                 edgecolor='black', linewidth=1.5)
    )
    
    # 美化网格
    ax.grid(color='#E0E0E0', linestyle='--', linewidth=0.8, alpha=0.7)
    
    plt.tight_layout()
    
    # 保存图片（LaTeX兼容文件名）
    png_path = FIGURES_DIR / "fig2_exp001_vsp_radar.png"
    fig.savefig(png_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Saved: {png_path}")
    
    pdf_path = FIGURES_DIR / "fig2_exp001_vsp_radar.pdf"
    fig.savefig(pdf_path, format='pdf', bbox_inches='tight', facecolor='white')
    print(f"Saved: {pdf_path}")
    
    plt.close()
    
    # 生成详细报告
    print("\nFig. 2: VSP Four-Criteria Verification (EXP001) - FINAL VERSION")
    print("=" * 80)
    print("\nCriteria Summary:")
    print("-" * 80)
    for i, (crit, actual, thresh, status) in enumerate(zip(criteria, actual_values, thresholds, statuses)):
        direction = ">" if directions[i] else "<"
        print(f"{crit:25} | {actual:7.4f} {direction} {thresh:7.4f} | {status}")
    print("-" * 80)
    print(f"Overall: {total_pass}/4 criteria passed")
    print("\nKey Findings:")
    print("  • Calibration failure: |bias|=0.50 is 25× larger than target (|bias|=0.02)")
    print("  • All other criteria exceed VSP thresholds")
    print("  • Radar chart format visualizes trade-off space between criteria")
    print("  • Shaded areas represent passing/failing regions")
    
    return 0


if __name__ == "__main__":
    print("=" * 80)
    print("Generating Fig. 2: VSP Four-Criteria Verification (EXP001) - FINAL VERSION")
    print("=" * 80)
    generate_fig2_radar()
