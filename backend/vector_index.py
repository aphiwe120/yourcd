"""
Vector search index for long text columns using Chroma.

Detects text columns and creates embeddings for semantic search.
"""

import os
import duckdb
from pathlib import Path
import chromadb
from chromadb.config import Settings
from llama_index.core.embeddings import OpenAIEmbedding


class VectorIndex:
    """Vector search index for semantic queries."""
    
    def __init__(self, db_path='data.duckdb', chroma_path='./chroma_db', text_threshold=100):
        """
        Initialize vector index.
        
        Args:
            db_path: Path to DuckDB database
            chroma_path: Path to Chroma collection
            text_threshold: Minimum average text length to include column (chars)
        """
        self.db_path = db_path
        self.chroma_path = chroma_path
        self.text_threshold = text_threshold
        self.conn = duckdb.connect(db_path)
        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb",
            persist_directory=chroma_path,
            anonymized_telemetry=False,
        ))
        self.text_columns = self._identify_text_columns()
        self.embedder = OpenAIEmbedding()
    
    def _identify_text_columns(self):
        """Identify columns with long text content."""
        try:
            schema = self.conn.execute("DESCRIBE records").fetchall()
        except Exception:
            return []
        
        text_columns = []
        for col_name, col_type, *_ in schema:
            if col_type.lower() in ['varchar', 'text', 'string']:
                # Calculate average text length
                result = self.conn.execute(
                    f"SELECT AVG(CAST(LENGTH({col_name}) AS FLOAT)) FROM records WHERE {col_name} IS NOT NULL"
                ).fetchone()
                avg_length = result[0] if result and result[0] else 0
                
                if avg_length >= self.text_threshold:
                    text_columns.append(col_name)
        
        return text_columns
    
    def build(self, force=False):
        """
        Build or rebuild the vector index.
        
        Args:
            force: Force rebuild even if index exists
        """
        if not self.text_columns:
            print("No long text columns found. Skipping vector index.")
            return
        
        collection_name = 'records_embeddings'
        
        # Check if rebuild is needed
        try:
            collection = self.client.get_collection(name=collection_name)
            row_count = self.conn.execute("SELECT COUNT(*) FROM records").fetchone()[0]
            if collection.count() == row_count and not force:
                print(f"Vector index up-to-date ({collection.count()} rows)")
                return
        except Exception:
            pass
        
        # Build new index
        collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        
        # Fetch data and embed
        rows = self.conn.execute(f"SELECT * FROM records").fetchall()
        columns = [desc[0] for desc in self.conn.description]
        
        ids = []
        documents = []
        
        for idx, row in enumerate(rows):
            # Combine text from identified columns
            text_content = " ".join([
                str(row[columns.index(col)])
                for col in self.text_columns
                if columns.index(col) < len(row)
            ])
            
            if text_content.strip():
                ids.append(str(idx))
                documents.append(text_content)
        
        if ids:
            collection.add(ids=ids, documents=documents)
            print(f"✓ Built vector index with {len(ids)} embeddings")
        else:
            print("No text content to index")


if __name__ == '__main__':
    index = VectorIndex()
    index.build()
