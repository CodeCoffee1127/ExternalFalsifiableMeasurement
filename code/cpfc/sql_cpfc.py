"""
CPFC协议 - Text-to-SQL的Constraint-Propagation Fact-Chain Validation实例化
将SQL查询编译为facts和constraints
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Callable
import sqlparse
from sqlparse.sql import IdentifierList, Identifier, Where, Token
from sqlparse.tokens import Keyword, DML

from .dependency_extractor import SQLDependencyExtractor


@dataclass
class Fact:
    """事实陈述"""
    id: int
    content: str
    type: str  # projection, source, condition, join, aggregation, etc.


@dataclass
class Constraint:
    """约束规则"""
    id: int
    type: str  # syntax, schema, type, semantic
    rule: str
    target: Optional[str] = None
    validator: Optional[Callable] = None


class SQLCPFCProtocol:
    """
    Text-to-SQL的CPFC实例化
    将SQL查询编译为facts和constraints
    """

    def __init__(self):
        self.dependency_extractor = SQLDependencyExtractor()

    def compile_facts(self, sql: str, schema: dict) -> List[Fact]:
        """
        提取SQL中的事实陈述：
        - SELECT子句 → fact: "需要返回字段X"
        - WHERE子句 → fact: "条件Y必须满足"
        - JOIN子句 → fact: "表A与表B通过Z关联"

        返回：Fact列表
        """
        facts = []
        fact_id = 1

        try:
            parsed = sqlparse.parse(sql)
            if not parsed:
                return facts

            stmt = parsed[0]
            tokens = list(stmt.flatten())

            # 提取SELECT子句
            select_parts = []
            in_select = False
            for token in tokens:
                if token.ttype is DML and token.value.upper() == 'SELECT':
                    in_select = True
                    continue
                if in_select:
                    if token.ttype is Keyword and token.value.upper() in ('FROM', 'WHERE', 'GROUP', 'ORDER', 'HAVING', 'LIMIT'):
                        break
                    if token.value.strip() and token.value.strip() != ',':
                        select_parts.append(token.value.strip())

            if select_parts:
                facts.append(Fact(
                    id=fact_id,
                    content="SELECT " + ", ".join(select_parts),
                    type="projection"
                ))
                fact_id += 1

            # 提取FROM子句
            from_idx = None
            for i, token in enumerate(tokens):
                if token.ttype is Keyword and token.value.upper() == 'FROM':
                    from_idx = i
                    break

            if from_idx is not None and from_idx + 1 < len(tokens):
                from_content = []
                for i in range(from_idx + 1, len(tokens)):
                    t = tokens[i]
                    if t.ttype is Keyword and t.value.upper() in ('WHERE', 'GROUP', 'ORDER', 'HAVING', 'JOIN', 'LEFT', 'RIGHT', 'INNER', 'OUTER', 'ON', 'LIMIT'):
                        break
                    if t.value.strip():
                        from_content.append(t.value.strip())
                if from_content:
                    facts.append(Fact(
                        id=fact_id,
                        content="FROM " + " ".join(from_content),
                        type="source"
                    ))
                    fact_id += 1

            # 提取WHERE子句
            for token in stmt.tokens:
                if isinstance(token, Where):
                    facts.append(Fact(
                        id=fact_id,
                        content=str(token).strip(),
                        type="condition"
                    ))
                    fact_id += 1
                    break

            # 检测JOIN
            sql_upper = sql.upper()
            if 'JOIN' in sql_upper:
                facts.append(Fact(
                    id=fact_id,
                    content="表通过JOIN关联",
                    type="join"
                ))
                fact_id += 1

            # 检测聚合
            agg_keywords = ['COUNT', 'SUM', 'AVG', 'MAX', 'MIN']
            for agg in agg_keywords:
                if agg in sql_upper:
                    facts.append(Fact(
                        id=fact_id,
                        content=f"使用{agg}聚合函数",
                        type="aggregation"
                    ))
                    fact_id += 1
                    break

        except Exception:
            pass

        return facts

    def compile_constraints(self, sql: str, schema: dict) -> List[Constraint]:
        """
        提取约束规则（验证器规则库的基础）：
        1. 语法约束：SQL语法正确性
        2. 模式约束：表名/列名存在于schema
        3. 类型约束：WHERE条件类型匹配
        4. 语义约束：GROUP BY与聚合函数配合

        返回：Constraint列表
        """
        constraints = []
        constraint_id = 1

        # 1. 语法约束
        constraints.append(Constraint(
            id=constraint_id,
            type="syntax",
            rule="valid_sql_syntax",
            target=None
        ))
        constraint_id += 1

        # 2. 模式约束 - 从 schema 提取
        table_names = []
        if schema and 'table_names' in schema:
            table_names = list(schema['table_names'])
        elif schema and 'tables' in schema:
            for table_info in schema['tables']:
                if isinstance(table_info, dict):
                    t = table_info.get('table_name', table_info.get('name', ''))
                else:
                    t = ''
                if t:
                    table_names.append(t)
        for table in table_names:
            if table:
                constraints.append(Constraint(
                    id=constraint_id,
                    type="schema",
                    rule="table_exists",
                    target=table
                ))
                constraint_id += 1

        # 3. 类型约束
        constraints.append(Constraint(
            id=constraint_id,
            type="type",
            rule="type_match",
            target=None
        ))
        constraint_id += 1

        # 4. 语义约束
        sql_upper = sql.upper()
        if 'GROUP BY' in sql_upper or 'HAVING' in sql_upper:
            constraints.append(Constraint(
                id=constraint_id,
                type="semantic",
                rule="group_by_aggregation",
                target=None
            ))
            constraint_id += 1

        return constraints

    def extract_dependencies(self, sql: str) -> Dict[str, List[str]]:
        """
        【重点】自动化提取SQL内部依赖关系
        使用dependency_extractor模块
        """
        return self.dependency_extractor.extract_dependencies(sql)
