"""
基于AST自动提取SQL内部依赖关系
用于计算I+(正向依赖强度)和I-(冲突依赖)
"""

from typing import Dict, List, Tuple

try:
    import sqlglot
    from sqlglot import parse_one, exp
    HAS_SQLGLOT = True
except ImportError:
    HAS_SQLGLOT = False


class SQLDependencyExtractor:
    """
    基于AST自动提取SQL内部依赖关系
    """

    def extract_dependencies(self, sql: str) -> Dict[str, List[str]]:
        """
        提取SQL查询的依赖图

        返回格式：
        {
            'select': ['from'],
            'from': [],
            'where': ['from', 'select'],
            'group_by': ['from'],
            'having': ['group_by'],
            'order_by': ['select']
        }
        """
        if not HAS_SQLGLOT:
            return self._fallback_extract(sql)

        try:
            ast = parse_one(sql, read='sqlite')
        except Exception:
            return self._fallback_extract(sql)

        dependencies = {}

        # 1. SELECT依赖于FROM（需要知道表结构）
        if ast.find(exp.Select):
            from_node = ast.find(exp.From)
            if from_node:
                dependencies['select'] = ['from']
            else:
                dependencies['select'] = []

            # 2. WHERE依赖于FROM和可能的SELECT
            where_node = ast.find(exp.Where)
            if where_node:
                deps = ['from']
                select_node = ast.find(exp.Select)
                if select_node and self._references_select_alias(where_node, select_node):
                    deps.append('select')
                dependencies['where'] = deps

            # 3. GROUP BY依赖于FROM
            group_by_node = ast.find(exp.Group)
            if group_by_node:
                dependencies['group_by'] = ['from']

            # 4. HAVING依赖于GROUP BY
            having_node = ast.find(exp.Having)
            if having_node:
                dependencies['having'] = ['group_by']

            # 5. ORDER BY依赖于SELECT
            order_by_node = ast.find(exp.Order)
            if order_by_node:
                dependencies['order_by'] = ['select']

            # 6. 子查询依赖
            subqueries = list(ast.find_all(exp.Subquery))
            for i, subq in enumerate(subqueries):
                dependencies[f'subquery_{i}'] = ['from']

            # 确保from存在
            if 'from' not in dependencies:
                dependencies['from'] = []

        return dependencies

    def _fallback_extract(self, sql: str) -> Dict[str, List[str]]:
        """当sqlglot不可用时使用简单启发式"""
        sql_upper = sql.upper()
        dependencies = {'from': []}

        if 'SELECT' in sql_upper:
            dependencies['select'] = ['from'] if 'FROM' in sql_upper else []
        if 'WHERE' in sql_upper:
            dependencies['where'] = ['from']
        if 'GROUP BY' in sql_upper:
            dependencies['group_by'] = ['from']
        if 'HAVING' in sql_upper:
            dependencies['having'] = ['group_by']
        if 'ORDER BY' in sql_upper:
            dependencies['order_by'] = ['select'] if 'select' in dependencies else ['from']

        return dependencies

    def compute_dependency_strength(
        self, dependencies: Dict[str, List[str]], current_clause: str
    ) -> Tuple[float, float]:
        """
        计算I+(正向依赖强度)和I-(冲突依赖)

        I+ = 当前子句被依赖的次数（下游依赖数）
        I- = 当前子句产生冲突的可能性（启发式）

        返回：(I_plus, I_minus)
        """
        # 构建反向依赖图
        reverse_deps = {}
        for clause, deps in dependencies.items():
            for dep in deps:
                if dep not in reverse_deps:
                    reverse_deps[dep] = []
                reverse_deps[dep].append(clause)

        # I+：有多少子句依赖当前子句
        I_plus = len(reverse_deps.get(current_clause, []))

        # I-：冲突检测（简化版）
        I_minus = 0.0
        if current_clause == 'where' and 'group_by' in dependencies:
            I_minus = 0.5
        if current_clause == 'having' and 'where' in dependencies:
            I_minus = 0.3

        # 归一化
        I_plus_norm = I_plus / max(len(dependencies), 1)

        return I_plus_norm, I_minus

    def _references_select_alias(self, where_node, select_node) -> bool:
        """
        检查WHERE是否引用了SELECT中定义的别名
        """
        if not where_node or not select_node:
            return False

        try:
            aliases = set()
            for alias_node in select_node.find_all(exp.Alias):
                if hasattr(alias_node, 'alias'):
                    aliases.add(alias_node.alias)
                elif hasattr(alias_node, 'this'):
                    aliases.add(str(alias_node.this))

            for col in where_node.find_all(exp.Column):
                col_name = getattr(col, 'name', str(col))
                if col_name in aliases:
                    return True
        except Exception:
            pass

        return False
