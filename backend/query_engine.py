"""
Text-to-SQL query engine using DuckDB directly.

Converts natural language questions to SQL queries and returns results.
For now, this is a simplified version that returns curated responses
based on the question pattern.
"""

import os
import re
import duckdb
from typing import Dict, Any


class QueryEngine:
    """Text-to-SQL query engine."""
    
    DANGEROUS_KEYWORDS = ['INSERT', 'UPDATE', 'DELETE', 'DROP', 'ALTER', 'CREATE']
    
    def __init__(self, db_path='data.duckdb'):
        """
        Initialize query engine.
        
        Args:
            db_path: Path to DuckDB database file
        """
        self.db_path = db_path
        self.conn = duckdb.connect(db_path, read_only=False)
    
    def _is_safe_sql(self, sql: str) -> bool:
        """Check if SQL query is read-only."""
        for keyword in self.DANGEROUS_KEYWORDS:
            if re.search(rf'\b{keyword}\b', sql, re.IGNORECASE):
                return False
        return True
    
    def query(self, question: str) -> Dict[str, Any]:
        """
        Execute a natural language query by generating SQL.
        
        Args:
            question: Natural language question
        
        Returns:
            dict with answer, sql, and rows
        """
        if not question.strip():
            return {'error': 'Question cannot be empty', 'answer': None, 'sql': None}
        
        question_lower = question.lower()
        
        try:
            # Count queries
            if any(word in question_lower for word in ['count', 'how many', 'total']):
                sql = "SELECT COUNT(*) as total FROM records"
                result = self.conn.execute(sql).fetchall()
                answer = f"Total ICD-10 codes in database: {result[0][0]}"
                return {'answer': answer, 'sql': sql, 'rows': None}
            
            # Chapter queries
            if any(word in question_lower for word in ['chapter', 'group']):
                sql = "SELECT DISTINCT chapter_no, chapter_desc FROM records LIMIT 20"
                rows = self.conn.execute(sql).fetchall()
                answer = f"Found {len(rows)} chapters"
                return {
                    'answer': answer,
                    'sql': sql,
                    'rows': [{'chapter': r[0], 'description': r[1]} for r in rows]
                }
            
            # Extract meaningful search terms (remove common words)
            stop_words = {
                'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been',
                'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
                'should', 'may', 'might', 'must', 'can', 'find', 'search', 'code',
                'icd', 'icd10', 'icd-10', 'diagnosis', 'patient', 'with', 'without',
                'that', 'this', 'these', 'those', 'what', 'which', 'who', 'why', 'how'
            }
            
            # Extract keywords (at least 2 characters)
            words = re.findall(r'\b[a-z]+\b', question_lower)
            keywords = [w for w in words if w not in stop_words and len(w) > 2]
            
            if not keywords:
                # Fallback: try to use all words except stop words
                keywords = [w for w in words if len(w) > 2]
            
            if keywords:
                # Search multiple keywords for better matching
                search_terms = keywords[:3]  # Use up to 3 keywords
                
                # Build OR conditions for multiple keywords
                where_clauses = []
                for term in search_terms:
                    where_clauses.append(f"icd10_3_code_desc ILIKE '%{term}%'")
                    where_clauses.append(f"who_full_desc ILIKE '%{term}%'")
                
                where_condition = " OR ".join(where_clauses)
                
                sql = f"""
                SELECT DISTINCT icd10_code, icd10_3_code_desc, who_full_desc 
                FROM records 
                WHERE {where_condition}
                LIMIT 15
                """
                rows = self.conn.execute(sql).fetchall()
                
                if rows:
                    search_text = ", ".join(search_terms)
                    answer = f"Found {len(rows)} ICD-10 codes matching '{search_text}'"
                    return {
                        'answer': answer,
                        'sql': sql,
                        'rows': [{'code': r[0], 'description': r[1], 'full_desc': r[2]} for r in rows]
                    }
            
            # Fallback: return sample codes if no matches
            sql = "SELECT icd10_code, icd10_3_code_desc, who_full_desc FROM records LIMIT 5"
            rows = self.conn.execute(sql).fetchall()
            answer = "No specific matches found. Here are sample ICD-10 codes from the South African Master Industry Table"
            return {
                'answer': answer,
                'sql': sql,
                'rows': [{'code': r[0], 'description': r[1], 'full_desc': r[2]} for r in rows]
            }
        
        except Exception as e:
            return {'error': f'Query execution failed: {str(e)}', 'answer': None, 'sql': None}


def main():
    """CLI loop for interactive queries."""
    engine = QueryEngine()
    
    print("Medical Coding Assistant - Query Engine")
    print("Type 'quit' to exit\n")
    
    while True:
        question = input("Question: ").strip()
        
        if question.lower() == 'quit':
            break
        
        result = engine.query(question)
        
        if 'error' in result:
            print(f"Error: {result['error']}\n")
        else:
            print(f"\nAnswer: {result['answer']}")
            if result['sql']:
                print(f"SQL: {result['sql']}")
            if result['rows']:
                print(f"Rows: {result['rows']}")
            print()


if __name__ == '__main__':
    main()
