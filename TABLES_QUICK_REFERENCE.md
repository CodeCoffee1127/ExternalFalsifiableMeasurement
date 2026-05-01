# 表11-13 快速参考指南

## 📊 表格概览

| 表格 | 内容 | 数据文件 | 实验报告 |
|------|------|---------|---------|
| **Table 11** | 动力学方程拟合指标 | [JSON](results/table11_fit_metrics.json) / [CSV](results/table11_fit_metrics.csv) | [EXP003报告](experiment_reports/EXP003_Fit_Analysis/README.md) |
| **Table 12** | Ljung-Box残差检验 | [JSON](results/table12_ljung_box.json) / [CSV](results/table12_ljung_box.csv) | [EXP008报告](experiment_reports/EXP008_LjungBox_Test/README.md) |
| **Table 13a** | Bootstrap置信区间 | [JSON](results/table13a_bootstrap_ci.json) / [CSV](results/table13a_bootstrap_ci.csv) | [EXP003报告](experiment_reports/EXP003_Fit_Analysis/README.md) |
| **Table 13b** | 分割敏感性分析 | [JSON](results/table13b_split_sensitivity.json) / [CSV](results/table13b_split_sensitivity.csv) | [EXP003报告](experiment_reports/EXP003_Fit_Analysis/README.md) |

## 🚀 快速开始

### 1. 查看表格数据

```bash
# JSON格式 (带元数据)
cat results/table11_fit_metrics.json | python -m json.tool

# CSV格式 (电子表格)
# 用Excel或Google Sheets打开 results/table11_fit_metrics.csv
```

### 2. 在Python中使用

```python
import json

# 加载Table 11数据
with open('results/table11_fit_metrics.json') as f:
    table11 = json.load(f)

print(f"R² = {table11['data']['rescue_model']['R2']}")
print(f"RMSE = {table11['data']['rescue_model']['RMSE']}")

# 加载Table 12数据
with open('results/table12_ljung_box.json') as f:
    table12 = json.load(f)

for row in table12['data']:
    print(f"{row['subset']}: p = {row['p_value']}")
```

### 3. 同步到GitHub

```bash
# Windows批处理脚本
sync_tables_to_github.bat

# 或手动执行
git add tables/ results/table1*_*.json results/table1*_*.csv
git add experiment_reports/EXP003_Fit_Analysis/ experiment_reports/EXP008_LjungBox_Test/
git commit -m "Add Table 11-13 data"
git push origin main
```

## 📁 目录结构

```
ExternalFalsifiableMeasurementforSubmission/
├── tables/                              # LaTeX源文件
│   ├── README.md                        # ← 从这里开始
│   ├── table_fit.tex                    # Table 11
│   ├── table_ljung.tex                  # Table 12
│   ├── table_sensitivity_samples.tex    # Table 13a
│   └── table_sensitivity_split.tex      # Table 13b
│
├── results/                             # 结构化数据
│   ├── table11_fit_metrics.{json,csv}
│   ├── table12_ljung_box.{json,csv}
│   ├── table13a_bootstrap_ci.{json,csv}
│   └── table13b_split_sensitivity.{json,csv}
│
├── experiment_reports/                  # 详细报告
│   ├── EXP003_Fit_Analysis/README.md
│   └── EXP008_LjungBox_Test/README.md
│
└── TABLES_11_13_SUPPLEMENT_REPORT.md    # 完整报告
```

## 🔍 关键发现

### Table 11: 模型拟合
- **R² = 0.945**: Rescue模型解释94.5%方差
- **优于基线**: ΔR² = +0.525 vs 线性基线
- **残差白噪声**: Ljung-Box p = 0.258

### Table 12: 残差诊断
- **所有层**: p = 0.258 > 0.05
- **结论**: 残差为白噪声，模型充分

### Table 13a: 参数稳定性
- **窄置信区间**: 表明参数稳定
- **Bootstrap N=1000**: 重采样验证

### Table 13b: 鲁棒性
- **80/20分割**: 用于主要分析
- **跨分割一致**: R² 0.953 vs 0.945

## ✅ 验证状态

```
✓ 23/23 检查通过
✓ 所有文件存在且非空
✓ JSON结构完整
✓ 关键数据值准确
```

运行 `python verify_tables_data.py` 重新验证。

## 📖 详细文档

- [完整补充报告 (英文)](TABLES_11_13_SUPPLEMENT_REPORT.md)
- [完成报告 (中文)](表11-13数据补充完成报告.md)
- [FILE_MANIFEST.md](FILE_MANIFEST.md)
- [SUBMISSION_DISCLOSURE.md](SUBMISSION_DISCLOSURE.md)

## 📞 支持

如有问题，请参考：
1. `tables/README.md` - 表格详细说明
2. `experiment_reports/` - 实验方法论
3. `docs/disclosures/` - 披露声明

---

**最后更新**: 2026-05-01  
**GitHub**: https://github.com/CodeCoffee1127/ExternalFalsifiableMeasurement
