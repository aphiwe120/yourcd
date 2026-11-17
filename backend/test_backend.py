"""
Tests for the backend modules.
"""

import pytest
import pandas as pd
import duckdb
import os
from ingest import ingest, normalize_column_names
from query_engine import QueryEngine
from fastapi.testclient import TestClient
from app import app


@pytest.fixture
def sample_df():
    """Create a sample DataFrame for testing."""
    return pd.DataFrame({
        'Patient ID': [1, 2, 3],
        'Diagnosis': ['Fever', 'Cough', 'Headache'],
        'Date': pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03']),
    })


@pytest.fixture
def test_db(sample_df, tmp_path):
    """Create a test database with sample data."""
    db_path = str(tmp_path / 'test.duckdb')
    conn = duckdb.connect(db_path)
    conn.register('temp_df', sample_df)
    conn.execute('CREATE TABLE records AS SELECT * FROM temp_df')
    conn.close()
    return db_path


class TestIngest:
    """Tests for data ingestion."""
    
    def test_normalize_column_names(self, sample_df):
        """Test column name normalization."""
        normalized = normalize_column_names(sample_df.copy())
        assert 'patient_id' in normalized.columns
        assert 'diagnosis' in normalized.columns
    
    def test_ingest_creates_database(self, sample_df, tmp_path):
        """Test that ingest creates DuckDB file."""
        excel_path = str(tmp_path / 'test.xlsx')
        sample_df.to_excel(excel_path, index=False)
        
        db_path = str(tmp_path / 'data.duckdb')
        result = ingest(excel_path, db_path)
        
        assert result['row_count'] == 3
        assert 'patient_id' in result['columns']
        assert os.path.exists(db_path)


class TestQueryEngine:
    """Tests for query engine."""
    
    def test_safe_sql_check(self, test_db):
        """Test SQL safety validation."""
        engine = QueryEngine(test_db)
        
        assert engine._is_safe_sql("SELECT * FROM records")
        assert not engine._is_safe_sql("DELETE FROM records")
        assert not engine._is_safe_sql("INSERT INTO records VALUES (1)")
    
    def test_empty_question_rejection(self, test_db):
        """Test rejection of empty questions."""
        engine = QueryEngine(test_db)
        result = engine.query("")
        
        assert 'error' in result
        assert result['answer'] is None


class TestFastAPIEndpoints:
    """Tests for FastAPI endpoints."""
    
    @pytest.fixture
    def client(self):
        """Create a test client."""
        return TestClient(app)
    
    def test_health_check(self, client):
        """Test health endpoint."""
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'ok'
        assert 'row_count' in data
    
    def test_schema_endpoint(self, client):
        """Test schema endpoint."""
        response = client.get("/api/schema")
        assert response.status_code == 200
        data = response.json()
        assert data['table_name'] == 'records'
        assert 'columns' in data
    
    def test_empty_query_rejection(self, client):
        """Test rejection of empty queries."""
        response = client.post("/api/query", json={"question": ""})
        assert response.status_code == 400


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
