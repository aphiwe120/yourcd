"""
Hybrid query engine routing between SQL and vector search.

Routes questions to the appropriate engine based on query type.
"""

from query_engine import QueryEngine


class HybridEngine:
    """Hybrid query engine combining SQL and vector search."""
    
    def __init__(self, db_path='data.duckdb'):
        """
        Initialize hybrid engine.
        
        Args:
            db_path: Path to DuckDB database
        """
        self.sql_engine = QueryEngine(db_path)
    
    def query(self, question):
        """
        Execute a hybrid query.
        
        Args:
            question: Natural language question
        
        Returns:
            dict with answer, sql, route, and rows
        """
        # For now, just route to SQL engine
        result = self.sql_engine.query(question)
        result['route'] = 'sql'
        return result


def main():
    """CLI loop for hybrid queries."""
    engine = HybridEngine()
    
    print("Medical Coding Assistant - Hybrid Engine")
    print("Type 'quit' to exit\n")
    
    while True:
        question = input("Question: ").strip()
        
        if question.lower() == 'quit':
            break
        
        result = engine.query(question)
        
        if 'error' in result:
            print(f"Error: {result['error']}\n")
        else:
            print(f"\nRoute: {result['route']}")
            print(f"Answer: {result['answer']}")
            if result['sql']:
                print(f"SQL: {result['sql']}")
            print()


if __name__ == '__main__':
    main()

