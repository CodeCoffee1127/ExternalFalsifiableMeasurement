#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
EXP025 Parser: AST Depth and Correlation Detection

Purpose: Scan query pools and compute features for feasibility pass
"""

import json
import sqlparse
from sqlparse.sql import Parenthesis, Identifier, Where
from sqlparse.tokens import Keyword, DML
from pathlib import Path
import pandas as pd
from typing import List, Dict, Any, Optional, Tuple
from loguru import logger

# Configure logging
logger.add("logs/exp025_parser.log", rotation="10 MB", retention="7 days")


def compute_ast_depth(query: str) -> int:
    """
    Compute AST nesting depth using sqlparse.
    
    Counts Parenthesis tokens containing SELECT as nested levels.
    
    Args:
        query: SQL query string
        
    Returns:
        Nesting depth (integer >= 1)
    """
    if not query or not query.strip():
        return 1
    
    try:
        parsed = sqlparse.parse(query.strip())[0]
    except Exception as e:
        logger.warning(f"Parse failed for query: {query[:50]}... Error: {e}")
        return 1
    
    max_depth = [1]
    
    def traverse(token, depth):
        if isinstance(token, Parenthesis):
            token_str = str(token).strip().upper()
            # Only count as nested if it contains SELECT
            if token_str.startswith('(') and 'SELECT' in token_str:
                max_depth[0] = max(max_depth[0], depth + 1)
                for sub in getattr(token, 'tokens', []):
                    traverse(sub, depth + 1)
                return
        for sub in getattr(token, 'tokens', []):
            traverse(sub, depth)
    
    traverse(parsed, 0)
    return max_depth[0]


def has_correlated_subquery(query: str) -> bool:
    """
    Detect if query has correlated subqueries.
    
    Simplified heuristic: looks for patterns indicating outer reference
    in subqueries.
    
    Args:
        query: SQL query string
        
    Returns:
        True if likely correlated, False otherwise
    """
    if not query or not query.strip():
        return False
    
    query_upper = query.upper()
    
    # Heuristic 1: Check for EXISTS/NOT EXISTS (often correlated)
    if 'WHERE EXISTS' in query_upper or 'WHERE NOT EXISTS' in query_upper:
        return True
    
    # Heuristic 2: Check for subquery with comparison to outer alias
    # Pattern: WHERE ... alias.column ... (SELECT ... WHERE ... alias.column)
    # Look for repeated table aliases across nesting levels
    
    # Count SELECT keywords (indicates subqueries)
    select_count = query_upper.count(' SELECT ') + (1 if query_upper.startswith('SELECT') else 0)
    
    if select_count < 2:
        # Only one SELECT, no subquery
        return False
    
    # Heuristic 3: Look for patterns like "e.column" in WHERE clause
    # after FROM table alias
    # This is a simplified check for alias.column references
    
    # Check if there's a pattern suggesting correlation:
    # - Multiple tables with aliases
    # - WHERE clause with cross-table references
    
    # Extract table aliases (simplified: look for "FROM table alias" or "JOIN table alias")
    import re
    
    # Pattern: FROM table_name alias or JOIN table_name alias
    alias_pattern = r'(?:FROM|JOIN)\s+(\w+)(?:\s+(?:AS\s+)?(\w+))?'
    aliases = re.findall(alias_pattern, query, re.IGNORECASE)
    
    if len(aliases) >= 2:
        # Multiple tables with potential aliases
        # Check if WHERE clause references multiple aliases
        where_match = re.search(r'WHERE\s+(.+?)(?:GROUP|ORDER|LIMIT|$)', query, re.IGNORECASE | re.DOTALL)
        if where_match:
            where_clause = where_match.group(1)
            # Check for alias.column pattern
            alias_refs = re.findall(r'(\w+)\.(\w+)', where_clause)
            if len(alias_refs) >= 2:
                # Multiple alias.column references in WHERE
                # Could indicate correlation
                unique_aliases = set(ref[0] for ref in alias_refs)
                if len(unique_aliases) >= 2:
                    return True
    
    # Heuristic 4: Deep nesting (3+ levels) often indicates correlation
    depth = compute_ast_depth(query)
    if depth >= 3:
        return True
    
    return False


def extract_features(query: str) -> Dict[str, Any]:
    """
    Extract surface complexity features from SQL query.
    
    Args:
        query: SQL query string
        
    Returns:
        Dictionary of features
    """
    features = {
        'table_count': 0,
        'join_count': 0,
        'predicate_count': 0,
        'ast_node_count': 0,
        'token_count': 0,
        'has_aggregation': False,
        'ast_depth': 1,
        'has_correlation': False
    }
    
    if not query or not query.strip():
        return features
    
    try:
        parsed = sqlparse.parse(query.strip())[0]
        
        # Count tokens
        all_tokens = list(parsed.flatten())
        features['token_count'] = len(all_tokens)
        
        # Count AST nodes
        features['ast_node_count'] = len(list(parsed.tokens))
        
        # Compute AST depth
        features['ast_depth'] = compute_ast_depth(query)
        
        # Count tables (FROM and JOIN keywords)
        query_upper = query.upper()
        features['table_count'] = query_upper.count(' FROM ') + query_upper.count(' JOIN ')
        
        # Count JOINs
        features['join_count'] = query_upper.count(' JOIN ')
        
        # Count predicates (WHERE, HAVING, ON)
        features['predicate_count'] = (
            query_upper.count(' WHERE ') +
            query_upper.count(' HAVING ') +
            query_upper.count(' ON ')
        )
        
        # Check for aggregation
        features['has_aggregation'] = any(agg in query_upper for agg in [
            ' GROUP BY ', ' COUNT(', ' SUM(', ' AVG(', ' MAX(', ' MIN(',
            'COUNT(', 'SUM(', 'AVG(', 'MAX(', 'MIN('
        ])
        
        # Detect correlation
        features['has_correlation'] = has_correlated_subquery(query)
        
    except Exception as e:
        logger.error(f"Feature extraction failed for query: {query[:50]}... Error: {e}")
        features['parse_error'] = True
    
    return features


def load_query_pool(path: str) -> List[Dict[str, Any]]:
    """
    Load queries from JSONL or JSON file.
    
    Args:
        path: Path to query file
        
    Returns:
        List of query records
    """
    queries = []
    path = Path(path)
    
    if not path.exists():
        logger.warning(f"Query pool file not found: {path}")
        return queries
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            if path.suffix == '.jsonl':
                for line in f:
                    if line.strip():
                        queries.append(json.loads(line))
            elif path.suffix == '.json':
                queries = json.load(f)
            elif path.suffix == '.txt':
                # JSONL format (one JSON object per line)
                for line in f:
                    if line.strip():
                        try:
                            queries.append(json.loads(line))
                        except json.JSONDecodeError:
                            # Try as plain SQL
                            queries.append({'query': line.strip(), 'db_id': 'unknown'})
    except Exception as e:
        logger.error(f"Failed to load query pool {path}: {e}")
    
    return queries


def scan_query_pools(pool_paths: List[str]) -> pd.DataFrame:
    """
    Scan all query pools and compute features.
    
    Args:
        pool_paths: List of paths to query pool files
        
    Returns:
        DataFrame with all queries and features
    """
    all_queries = []
    
    for path in pool_paths:
        logger.info(f"Loading query pool: {path}")
        queries = load_query_pool(path)
        logger.info(f"Loaded {len(queries)} queries from {path}")
        
        for i, q in enumerate(queries):
            query_text = q.get('query', '')
            db_id = q.get('db_id', 'unknown')
            
            features = extract_features(query_text)
            
            all_queries.append({
                'source': str(path),
                'index': i,
                'query_text': query_text,
                'db_id': db_id,
                **features
            })
    
    df = pd.DataFrame(all_queries)
    logger.info(f"Total queries scanned: {len(df)}")
    
    return df


def compute_feasibility_stats(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Compute feasibility statistics for EXP025.
    
    Args:
        df: DataFrame with all queries and features
        
    Returns:
        Dictionary of feasibility statistics
    """
    stats = {
        'total_queries': len(df),
        'by_depth': {},
        'condition_b_candidates': 0,
        'condition_a_candidates': 0,
        'matchability_ratio': 0.0,
        'parser_error_rate': 0.0
    }
    
    # Depth distribution
    depth_counts = df['ast_depth'].value_counts().to_dict()
    stats['by_depth'] = {int(k): int(v) for k, v in depth_counts.items()}
    
    # Condition B candidates (d >= 2 + correlation)
    condition_b = df[(df['ast_depth'] >= 2) & (df['has_correlation'] == True)]
    stats['condition_b_candidates'] = len(condition_b)
    
    # Condition A candidates (d = 1 or d = 2 without correlation)
    condition_a = df[(df['ast_depth'] == 1) | ((df['ast_depth'] == 2) & (df['has_correlation'] == False))]
    stats['condition_a_candidates'] = len(condition_a)
    
    # Matchability ratio (A / B)
    if stats['condition_b_candidates'] > 0:
        stats['matchability_ratio'] = stats['condition_a_candidates'] / stats['condition_b_candidates']
    
    # Parser error rate
    if 'parse_error' in df.columns:
        stats['parser_error_rate'] = df['parse_error'].sum() / len(df)
    
    return stats


def generate_feasibility_memo(stats: Dict[str, Any], output_path: str):
    """
    Generate feasibility memo in markdown format.
    
    Args:
        stats: Feasibility statistics
        output_path: Path to output file
    """
    memo = f"""# EXP025 Feasibility Memo

**Generated:** {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## Query Pool Summary

| Metric | Value |
|--------|-------|
| Total Queries | {stats['total_queries']} |
| Parser Error Rate | {stats['parser_error_rate']:.2%} |

---

## AST Depth Distribution

| Depth | Count | Percentage |
|-------|-------|------------|
"""
    
    for depth, count in sorted(stats['by_depth'].items()):
        pct = count / stats['total_queries'] * 100
        memo += f"| {depth} | {count} | {pct:.1f}% |\n"
    
    memo += f"""
---

## Feasibility Assessment

### Condition B (Deep-Nesting + Recursive)

**Criteria:** d ≥ 2 AND has_correlation = TRUE

**Candidates:** {stats['condition_b_candidates']}

**Feasibility Tier:**
"""
    
    if stats['condition_b_candidates'] >= 30:
        memo += "- ✅ **Standard tier** (N ≥ 30): Full paired comparative analysis supported\n"
    elif stats['condition_b_candidates'] >= 15:
        memo += "- ⚠️ **Reduced tier** (15 ≤ N < 30): Degraded analysis, weaker conclusions\n"
    else:
        memo += "- ❌ **Feasibility failure** (N < 15): Cannot proceed with strong attribution\n"
    
    memo += f"""
### Condition A (Shallow / Non-Recursive Control)

**Criteria:** d = 1 OR (d = 2 AND has_correlation = FALSE)

**Candidates:** {stats['condition_a_candidates']}

### Matchability

**Matchability Ratio (A/B):** {stats['matchability_ratio']:.2f}

**Interpretation:**
"""
    
    if stats['matchability_ratio'] >= 2.0:
        memo += "- ✅ Sufficient Condition A samples for matching\n"
    elif stats['matchability_ratio'] >= 1.0:
        memo += "- ⚠️ Limited Condition A samples; matching may be challenging\n"
    else:
        memo += "- ❌ Insufficient Condition A samples for matching\n"
    
    memo += f"""
---

## Feasibility Conclusion

**Continuation Mode:**
"""
    
    if stats['condition_b_candidates'] >= 30 and stats['matchability_ratio'] >= 1.0:
        memo += "- ✅ **Full continuation**: Proceed with all layers\n"
    elif stats['condition_b_candidates'] >= 15:
        memo += "- ⚠️ **Degraded continuation**: Proceed with limitations\n"
    else:
        memo += "- ❌ **Stopped**: Feasibility failure\n"
    
    memo += f"""
**Rationale:**

[To be completed based on detailed analysis]

---

**Next Steps:**

1. Load tier labels from exp003_tier_report.json
2. Load HC3 violation status from exp012_results.json
3. Apply Condition B inclusion criteria (tier=Complex + HC3_violated=TRUE)
4. Re-compute feasibility with full criteria

---

*Memo generated by EXP025 Parser*
"""
    
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(memo)
    
    logger.info(f"Feasibility memo written to {output_path}")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='EXP025 Parser: Scan query pools and compute feasibility')
    parser.add_argument('--output', type=str, default='results/exp025_complex_tier_analysis/feasibility/EXP025_feasibility_memo.md',
                        help='Output path for feasibility memo')
    parser.add_argument('--pools', nargs='+', default=[
        'data/calibration_214.txt',
        'data/test_320.txt',
        'spider/train_spider.json'
    ], help='Query pool files to scan')
    parser.add_argument('--spider-only', action='store_true', help='Scan only SPIDER data')
    
    args = parser.parse_args()
    
    if args.spider_only:
        args.pools = ['spider/train_spider.json']
    
    # Scan query pools
    df = scan_query_pools(args.pools)
    
    # Compute feasibility stats
    stats = compute_feasibility_stats(df)
    
    # Generate memo
    generate_feasibility_memo(stats, args.output)
    
    # Print summary
    print(f"\n=== EXP025 Feasibility Summary ===")
    print(f"Total queries: {stats['total_queries']}")
    print(f"Depth distribution:")
    for depth, count in sorted(stats['by_depth'].items()):
        print(f"  Depth {depth}: {count} queries")
    print(f"Condition B candidates (d>=2 + correlation): {stats['condition_b_candidates']}")
    print(f"Condition A candidates: {stats['condition_a_candidates']}")
    print(f"Matchability ratio: {stats['matchability_ratio']:.2f}")
    
    if stats['condition_b_candidates'] >= 30:
        print("Feasibility: ✅ Standard tier")
    elif stats['condition_b_candidates'] >= 15:
        print("Feasibility: ⚠️ Reduced tier")
    else:
        print("Feasibility: ❌ Failure")


if __name__ == '__main__':
    main()
