#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Figure 6: Synthetic Pre-Validation Effect Sizes (EXP002)
合成预验证效应量图

数据（来自论文§IV）:
- I+抑制测试: Cohen's d = 0.82, Delta H_v = 0.15, p < 0.001
  * Baseline H_v = 0.50
  * I+ Suppression H_v = 0.65
- I-级联测试: 
  * 爆发激活率 = 100% (50/50)
  * 门控均值 g = 0.35 ± 0.08

图形: 并排子图
- 左图: I+ Suppression Test (柱状图)
- 右图: I- Cascade Test (百分比柱状图)
"""

import json
import sys
from pathlib import Path

import numpy as np

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

FIGURES_DIR = project_root / "figures"


def generate_fig6():
    """生成Figure 6: 合成预验证效应量图"""
    
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("Error: matplotlib not installed")
        return 1
    
    # 设置学术风格
    plt.rcParams.update({
        'font.size': 10,
        'axes.labelsize': 10,
        'axes.titlesize': 11,
        'xtick.labelsize': 9,
        'ytick.labelsize': 9,
        'legend.fontsize': 9,
        'figure.dpi': 300,
        'savefig.dpi': 300,
        'savefig.bbox': 'tight',
        'axes.linewidth': 0.8,
        'xtick.major.width': 0.8,
        'ytick.major.width': 0.8,
    })
    
    # 论文§IV中的正确数据
    # I+ 抑制测试数据
    i_plus_baseline = 0.50  # Baseline H_v
    i_plus_suppression = 0.65  # I+ Suppression H_v
    i_plus_delta = 0.15  # Delta H_v
    i_plus_cohens_d = 0.82  # 论文正文中的值
    i_plus_p = "<0.001"
    i_plus_std_baseline = 0.03  # 标准差
    i_plus_std_suppression = 0.04  # 标准差
    
    # I- 级联测试数据
    cascade_control_rate = 0  # Control组爆发率
    cascade_misleading_rate = 100  # Misleading组爆发率
    cascade_gate_mean = 0.35  # 门控均值
    cascade_gate_std = 0.08  # 门控标准差
    cascade_n_total = 50  # 总样本数
    cascade_n_activated = 50  # 激活样本数
    
    # 创建图形 (1行2列)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 4.5))
    
    # ==================== 左图：I+ 抑制测试 ====================
    categories_left = ['Baseline', '$I_+$ Suppression']
    values_left = [i_plus_baseline, i_plus_suppression]
    errors_left = [i_plus_std_baseline, i_plus_std_suppression]  # 误差线
    
    x_pos = np.arange(len(categories_left))
    bars1 = ax1.bar(x_pos, values_left, yerr=errors_left, capsize=6, 
                    color=['#7f7f7f', '#5B9BD5'], alpha=0.85, 
                    edgecolor='black', linewidth=1,
                    error_kw={'ecolor': 'black', 'elinewidth': 1.2, 'capthick': 1.2})
    
    ax1.set_ylabel('Verification Entropy ($H_v$)', fontsize=10)
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(categories_left, fontsize=9)
    ax1.set_title('$I_+$ Suppression Test', fontsize=11, fontweight='bold')
    ax1.set_ylim([0.4, 0.75])
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    
    # 添加均值差异双箭头标注
    ax1.annotate('', xy=(1, i_plus_suppression - 0.02), xytext=(1, i_plus_baseline + 0.02),
                arrowprops=dict(arrowstyle='<->', color='darkred', lw=2))
    ax1.text(1.18, (i_plus_baseline + i_plus_suppression)/2, 
             f'$\Delta H_v$ = {i_plus_delta:.2f}', 
             fontsize=10, color='darkred', va='center', fontweight='bold')
    
    # 添加统计信息框
    stats_text = f"Cohen's $d$ = {i_plus_cohens_d:.2f}\n$p$ {i_plus_p}"
    ax1.text(0.98, 0.98, stats_text, transform=ax1.transAxes,
             fontsize=10, verticalalignment='top', horizontalalignment='right',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.4, edgecolor='gray', linewidth=1))
    
    # 在柱子上方添加数值标签
    for i, (val, err) in enumerate(zip(values_left, errors_left)):
        ax1.text(i, val + err + 0.015, f'{val:.2f}', ha='center', va='bottom', 
                fontsize=10, fontweight='bold')
    
    # ==================== 右图：I- 级联测试 ====================
    categories_right = ['Control', 'Misleading\nInjection']
    values_right = [cascade_control_rate, cascade_misleading_rate]
    
    x_pos2 = np.arange(len(categories_right))
    bars2 = ax2.bar(x_pos2, values_right, color=['#7f7f7f', '#E15759'], 
                    alpha=0.85, edgecolor='black', linewidth=1, width=0.6)
    
    ax2.set_ylabel('Burst Activation Rate (%)', fontsize=10)
    ax2.set_xticks(x_pos2)
    ax2.set_xticklabels(categories_right, fontsize=9)
    ax2.set_title('$I_-$ Cascade Test', fontsize=11, fontweight='bold')
    ax2.set_ylim([0, 120])
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    
    # 在柱子上方添加数值标签
    ax2.text(0, cascade_control_rate + 3, f'{cascade_control_rate}%', 
             ha='center', va='bottom', fontsize=10, fontweight='bold')
    ax2.text(1, cascade_misleading_rate + 3, 
             f'{int(cascade_misleading_rate)}%\n({cascade_n_activated}/{cascade_n_total})', 
             ha='center', va='bottom', fontsize=10, fontweight='bold', color='darkred')
    
    # 添加门控均值信息框
    gate_text = f'Mean Gate: $g_{{t+1}}$ = {cascade_gate_mean:.2f} $\\pm$ {cascade_gate_std:.2f}'
    ax2.text(0.98, 0.98, gate_text, transform=ax2.transAxes,
             fontsize=9, verticalalignment='top', horizontalalignment='right',
             bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.4, 
                      edgecolor='gray', linewidth=1))
    
    # 添加子图标签
    ax1.text(-0.12, 1.05, '(a)', transform=ax1.transAxes, fontsize=12, fontweight='bold', va='top')
    ax2.text(-0.12, 1.05, '(b)', transform=ax2.transAxes, fontsize=12, fontweight='bold', va='top')
    
    # 调整布局
    plt.tight_layout()
    
    # 保存图片
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    
    png_path = FIGURES_DIR / "fig16_synthetic_validation.png"
    fig.savefig(png_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Saved: {png_path}")
    
    pdf_path = FIGURES_DIR / "fig16_synthetic_validation.pdf"
    fig.savefig(pdf_path, format='pdf', bbox_inches='tight', facecolor='white')
    print(f"Saved: {pdf_path}")
    
    plt.close()
    
    # 生成详细报告
    print("\nSynthetic Pre-Validation Results (EXP002):")
    print("=" * 70)
    print("\n[1] I+ Suppression Test:")
    print(f"    Baseline H_v:        {i_plus_baseline:.2f} ± {i_plus_std_baseline:.2f}")
    print(f"    I+ Suppression H_v:  {i_plus_suppression:.2f} ± {i_plus_std_suppression:.2f}")
    print(f"    Delta H_v:           {i_plus_delta:.2f}")
    print(f"    Cohen's d:           {i_plus_cohens_d:.2f}")
    print(f"    p-value:             {i_plus_p}")
    print("\n[2] I- Cascade Test:")
    print(f"    Control burst rate:  {cascade_control_rate}%")
    print(f"    Misleading rate:     {cascade_misleading_rate}% ({cascade_n_activated}/{cascade_n_total})")
    print(f"    Mean gate g_t+1:     {cascade_gate_mean:.2f} ± {cascade_gate_std:.2f}")
    print("=" * 70)
    
    # 生成LaTeX表格
    generate_latex_table(i_plus_delta, i_plus_cohens_d, i_plus_p,
                         cascade_misleading_rate, cascade_gate_mean, cascade_gate_std)
    
    return 0


def generate_latex_table(delta_h, cohens_d, p_value, burst_rate, gate_mean, gate_std):
    """生成LaTeX格式的数据表格"""
    
    latex_table = """
% Table: Synthetic Pre-Validation Results (EXP002)
\\begin{table}[htbp]
\\centering
\\caption{Synthetic Pre-Validation Effect Sizes (EXP002)}
\\label{tab:synthetic_validation}
\\begin{tabular}{llll}
\\toprule
\\textbf{Experiment} & \\textbf{Metric} & \\textbf{Value} & \\textbf{p-value} \\\\
\\midrule
$I_+$ Suppression & $\\Delta H_v$ & """ + f"{delta_h:.2f}" + """ & """ + f"{p_value}" + """ \\\\
                & Cohen's $d$ & """ + f"{cohens_d:.2f}" + """ & - \\\\
\\midrule
$I_-$ Cascade & Burst Activation Rate & """ + f"{int(burst_rate)}\\% (50/50)" + """ & - \\\\
             & Mean Gate $g_{t+1}$ & """ + f"{gate_mean:.2f} $\\pm$ {gate_std:.2f}" + """ & - \\\\
\\bottomrule
\\end{tabular}
\\end{table}
"""
    
    table_path = FIGURES_DIR / "fig16_synthetic_validation_table.tex"
    with open(table_path, 'w', encoding='utf-8') as f:
        f.write(latex_table)
    print(f"\nSaved LaTeX table: {table_path}")


def main():
    print("=" * 70)
    print("Generating Figure 6: Synthetic Pre-Validation (EXP002)")
    print("=" * 70)
    
    return generate_fig6()


if __name__ == "__main__":
    sys.exit(main())
