"""
验证表11-13数据完整性的脚本
Checks that all table data files exist and contain expected content
"""

import json
import os
import sys
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

# Expected files
EXPECTED_FILES = {
    "tables": [
        "README.md",
        "table_fit.tex",
        "table_ljung.tex",
        "table_sensitivity_samples.tex",
        "table_sensitivity_split.tex",
        "table_tier.tex",
        "table_vsp.tex",
    ],
    "results": [
        "table11_fit_metrics.json",
        "table11_fit_metrics.csv",
        "table12_ljung_box.json",
        "table12_ljung_box.csv",
        "table13a_bootstrap_ci.json",
        "table13a_bootstrap_ci.csv",
        "table13b_split_sensitivity.json",
        "table13b_split_sensitivity.csv",
    ],
    "experiment_reports": [
        "EXP003_Fit_Analysis/README.md",
        "EXP008_LjungBox_Test/README.md",
    ],
}

# Expected JSON structure
EXPECTED_JSON_KEYS = {
    "table11_fit_metrics.json": ["table_id", "caption", "data", "experiment"],
    "table12_ljung_box.json": ["table_id", "caption", "data", "experiment"],
    "table13a_bootstrap_ci.json": ["table_id", "caption", "data", "experiment"],
    "table13b_split_sensitivity.json": ["table_id", "caption", "data", "experiment"],
}

# Expected data values (spot check)
EXPECTED_VALUES = {
    "table11_fit_metrics.json": {
        "path": ["data", "rescue_model", "R2"],
        "value": 0.945,
    },
    "table12_ljung_box.json": {
        "path": ["data", 0, "p_value"],
        "value": 0.258,
    },
}


def check_file_exists(filepath):
    """检查文件是否存在"""
    return filepath.exists() and filepath.stat().st_size > 0


def check_json_structure(json_file, expected_keys):
    """检查JSON文件结构"""
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        missing_keys = [key for key in expected_keys if key not in data]
        return len(missing_keys) == 0, missing_keys
    except Exception as e:
        return False, [str(e)]


def check_json_value(json_file, path, expected_value):
    """检查JSON文件中的特定值"""
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Navigate path
        current = data
        for key in path:
            current = current[key]
        
        return current == expected_value, current
    except Exception as e:
        return False, str(e)


def main():
    print("=" * 60)
    print("验证表11-13数据完整性")
    print("=" * 60)
    print()

    all_passed = True
    total_checks = 0
    passed_checks = 0

    # Check file existence
    print("[1/3] 检查文件存在性...")
    for category, files in EXPECTED_FILES.items():
        category_dir = BASE_DIR / category
        print(f"\n  {category}/:")
        
        for filename in files:
            filepath = category_dir / filename
            exists = check_file_exists(filepath)
            total_checks += 1
            
            if exists:
                passed_checks += 1
                print(f"    ✓ {filename}")
            else:
                all_passed = False
                print(f"    ✗ {filename} [MISSING OR EMPTY]")

    print()

    # Check JSON structure
    print("[2/3] 检查JSON文件结构...")
    for json_file, expected_keys in EXPECTED_JSON_KEYS.items():
        json_path = BASE_DIR / "results" / json_file
        
        if not json_path.exists():
            print(f"    ✗ {json_file} [FILE NOT FOUND]")
            all_passed = False
            continue
        
        valid, missing = check_json_structure(json_path, expected_keys)
        total_checks += 1
        
        if valid:
            passed_checks += 1
            print(f"    ✓ {json_file} (keys: {', '.join(expected_keys)})")
        else:
            all_passed = False
            print(f"    ✗ {json_file} [MISSING KEYS: {', '.join(missing)}]")

    print()

    # Check data values
    print("[3/3] 检查关键数据值...")
    for json_file, config in EXPECTED_VALUES.items():
        json_path = BASE_DIR / "results" / json_file
        
        if not json_path.exists():
            print(f"    ✗ {json_file} [FILE NOT FOUND]")
            all_passed = False
            continue
        
        match, actual = check_json_value(json_path, config["path"], config["value"])
        total_checks += 1
        
        if match:
            passed_checks += 1
            print(f"    ✓ {json_file}: {config['value']}")
        else:
            all_passed = False
            print(f"    ✗ {json_file}: expected {config['value']}, got {actual}")

    print()
    print("=" * 60)
    print(f"验证结果: {passed_checks}/{total_checks} 检查通过")
    
    if all_passed:
        print("✓ 所有检查通过！数据完整性验证成功。")
        print()
        print("已添加的文件:")
        print("  - tables/: 6个LaTeX表格文件 + 1个README")
        print("  - results/: 8个JSON/CSV数据文件 (表11-13)")
        print("  - experiment_reports/: 2个实验报告目录")
        print()
        print("下一步: 运行 sync_tables_to_github.bat 同步到GitHub")
    else:
        print("✗ 部分检查未通过，请检查上述错误。")
        sys.exit(1)
    
    print("=" * 60)


if __name__ == "__main__":
    main()
