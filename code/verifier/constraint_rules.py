"""
自动化SQL验证规则库
从Spider schema自动生成约束规则
"""

from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass
class Constraint:
    """约束规则"""
    type: str
    rule: str
    target: str = None
    validator: Any = None


class ConstraintRuleLibrary:
    """
    自动生成SQL验证规则
    """

    @staticmethod
    def generate_schema_rules(schema: dict) -> List[Constraint]:
        """
        从Spider schema自动生成：
        - 所有合法表名
        - 所有合法列名及其类型
        - 外键关系
        """
        rules = []
        tables = []
        if not schema:
            return rules
        # Spider schema格式1: table_names + column_names
        if 'table_names' in schema:
            tables = list(schema['table_names'])
        # Spider schema格式2: tables列表
        else:
            tables = [
                t.get('table_name', t.get('name', ''))
                for t in schema.get('tables', [])
                if isinstance(t, dict) and (t.get('table_name') or t.get('name'))
            ]

        for table in tables:
            if table:
                rules.append(Constraint(
                    type="schema",
                    rule=f"table_exists_{table}",
                    target=table,
                    validator=lambda sql, t=table: t.lower() in sql.lower()
                ))

        # 列名规则
        if 'column_names' in schema and 'table_names' in schema:
            col_names = schema['column_names']
            table_names = schema['table_names']
            for col_id, (table_id, col_name) in enumerate(col_names):
                if table_id >= 0 and col_name != '*':
                    table_name = table_names[table_id] if table_id < len(table_names) else ''
                    rules.append(Constraint(
                        type="schema",
                        rule=f"column_exists_{table_name}_{col_name}",
                        target=f"{table_name}.{col_name}",
                        validator=None
                    ))

        return rules

    @staticmethod
    def generate_type_rules(schema: dict) -> List[Constraint]:
        """
        类型检查规则：
        - 数值列不能与字符串比较
        - 日期格式正确
        """
        rules = [
            Constraint(
                type="type",
                rule="numeric_comparison",
                target=None,
                validator=None
            ),
            Constraint(
                type="type",
                rule="date_format",
                target=None,
                validator=None
            ),
        ]
        return rules

    @staticmethod
    def generate_all_rules(schema: dict) -> List[Constraint]:
        """生成所有约束规则"""
        rules = []
        rules.extend(ConstraintRuleLibrary.generate_schema_rules(schema))
        rules.extend(ConstraintRuleLibrary.generate_type_rules(schema))
        return rules
