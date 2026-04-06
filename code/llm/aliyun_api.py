"""
阿里云通义千问API封装
用于Text-to-SQL生成
"""

import json
import time
import os
from typing import List, Dict, Optional
import requests
import numpy as np
from loguru import logger

try:
    from joblib import Parallel, delayed
    HAS_JOBLIB = True
except ImportError:
    HAS_JOBLIB = False


# ============================================================
# USAGE: Set environment variable before running:
#   export ALIYUN_API_KEY="your-api-key-here"   (Linux/Mac)
#   set ALIYUN_API_KEY=your-api-key-here        (Windows CMD)
# Do NOT hardcode API keys in scripts.
# ============================================================

class AliyunLLMAPI:
    """
    阿里云通义千问API封装
    """

    def __init__(
        self,
        api_key: str = None,
        endpoint: str = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation",
        model: str = "qwen-turbo"
    ):
        self.api_key = api_key or os.environ.get("ALIYUN_API_KEY", "")
        if not self.api_key:
            raise ValueError(
                "API key not provided. Set ALIYUN_API_KEY environment variable "
                "or pass api_key parameter."
            )
        self.endpoint = endpoint
        self.model = model
        self.max_retries = 3
        self.retry_delay = 2.0

    def _construct_prompt(self, question: str, schema: dict) -> str:
        """
        构造Text-to-SQL提示词
        """
        schema_str = json.dumps(schema, indent=2, ensure_ascii=False)
        return f"""
Given the database schema:
{schema_str}

Question: {question}

Generate a valid SQL query to answer this question.
Output ONLY the SQL query without any explanation.
"""

    def generate_sql_single(
        self,
        question: str,
        schema: dict,
        temperature: float = 0.7
    ) -> str:
        """
        生成单个SQL候选
        """
        prompt = self._construct_prompt(question, schema)

        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

        payload = {
            "model": self.model,
            "input": {
                "messages": [
                    {"role": "system", "content": "You are an expert SQL generator. Output only valid SQL."},
                    {"role": "user", "content": prompt}
                ]
            },
            "parameters": {
                "temperature": temperature,
                "max_tokens": 512
            }
        }

        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    self.endpoint,
                    headers=headers,
                    json=payload,
                    timeout=60
                )

                if response.status_code == 200:
                    result = response.json()
                    content = result.get('output', {}).get('choices', [{}])[0].get('message', {}).get('content', '')
                    return content.strip() if content else "SELECT 1"
                else:
                    logger.warning(f"API返回 {response.status_code}: {response.text[:200]}")
                    if attempt < self.max_retries - 1:
                        time.sleep(self.retry_delay)
            except Exception as e:
                logger.warning(f"API调用失败 (尝试 {attempt + 1}/{self.max_retries}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)

        return "SELECT 1"  # 失败时返回默认值

    def generate_candidates(
        self,
        question: str,
        schema: dict,
        n: int = 50,
        n_jobs: int = 24
    ) -> List[str]:
        """
        生成N个候选（使用不同temperature增加多样性）
        """
        temperatures = np.linspace(0.3, 1.2, n).tolist()

        if HAS_JOBLIB and n_jobs > 1:
            candidates = Parallel(n_jobs=min(n_jobs, n))(
                delayed(self.generate_sql_single)(question, schema, temp)
                for temp in temperatures
            )
        else:
            candidates = [
                self.generate_sql_single(question, schema, temp)
                for temp in temperatures
            ]

        return list(candidates)

    def _construct_step_prompt(
        self,
        question: str,
        schema: dict,
        step: int,
        previous_sql: str = ""
    ) -> str:
        """构造逐步生成的提示词"""
        schema_str = json.dumps(schema, indent=2, ensure_ascii=False)
        step_instructions = [
            "Step 1: Generate ONLY the SELECT clause (column names). Output format: SELECT col1, col2, ...",
            "Step 2: Add the FROM clause. Output format: SELECT ... FROM table_name",
            "Step 3: Add WHERE/JOIN/ON if needed. Output a complete SQL with conditions.",
            "Step 4: Add GROUP BY/ORDER BY/HAVING/LIMIT if needed. Output the final complete SQL.",
        ]
        instr = step_instructions[min(step - 1, 3)]
        if previous_sql:
            return f"""Schema: {schema_str}
Question: {question}
Previous partial SQL: {previous_sql}

{instr}
Output ONLY the SQL, no explanation."""
        return f"""Schema: {schema_str}
Question: {question}

{instr}
Output ONLY the SQL, no explanation."""

    def generate_step_by_step(
        self,
        question: str,
        schema: dict,
        n_steps: int = 4,
        n_candidates_per_step: int = 50
    ) -> List[Dict]:
        """
        逐步生成SQL（用于Phase 2/3）
        将SQL分解为4步：SELECT -> FROM -> WHERE/JOIN -> GROUP BY/ORDER BY

        返回：
        [
            {'step': 1, 'partial_sql': 'SELECT ...', 'candidates': [...]},
            ...
        ]
        """
        reasoning_chain = []
        accumulated_sql = ""

        for step_num in range(1, min(n_steps, 5)):
            # 构造步骤特定提示
            prompt = self._construct_step_prompt(
                question, schema, step_num, accumulated_sql
            )
            # 生成N个候选
            candidates = self._generate_from_prompt(
                prompt, n=n_candidates_per_step, n_jobs=8
            )
            partial_sql = candidates[0] if candidates else "SELECT 1"
            accumulated_sql = partial_sql
            reasoning_chain.append({
                'step': step_num,
                'partial_sql': partial_sql,
                'candidates': candidates
            })

        return reasoning_chain

    def _generate_from_prompt(
        self,
        prompt: str,
        n: int = 50,
        n_jobs: int = 8,
        stratified: bool = True,
    ) -> List[str]:
        """从给定提示生成N个候选（可選溫度分層 0.1/0.7/1.5）"""
        if stratified and n >= 30:
            n_each = n // 3
            temperatures = [0.1] * n_each + [0.7] * n_each + [1.5] * (n - 2 * n_each)
        else:
            temperatures = np.linspace(0.3, 1.2, n).tolist()
        if HAS_JOBLIB and n_jobs > 1:
            candidates = Parallel(n_jobs=min(n_jobs, n))(
                delayed(self._generate_single_from_messages)(
                    [{"role": "system", "content": "Output only valid SQL."},
                     {"role": "user", "content": prompt}],
                    temp
                )
                for temp in temperatures
            )
        else:
            candidates = [
                self._generate_single_from_messages(
                    [{"role": "system", "content": "Output only valid SQL."},
                     {"role": "user", "content": prompt}],
                    temp
                )
                for temp in temperatures
            ]
        return list(candidates)

    def _generate_single_from_messages(
        self,
        messages: list,
        temperature: float = 0.7
    ) -> str:
        """从消息列表生成单个响应"""
        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    self.endpoint,
                    headers={
                        'Authorization': f'Bearer {self.api_key}',
                        'Content-Type': 'application/json'
                    },
                    json={
                        "model": self.model,
                        "input": {"messages": messages},
                        "parameters": {"temperature": temperature, "max_tokens": 512}
                    },
                    timeout=60
                )
                if response.status_code == 200:
                    content = response.json().get('output', {}).get('choices', [{}])[0].get('message', {}).get('content', '')
                    return content.strip() if content else "SELECT 1"
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
            except Exception as e:
                logger.warning(f"API调用失败: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
        return "SELECT 1"
