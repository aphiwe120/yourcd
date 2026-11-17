"""
Ingest Excel file into DuckDB.

Loads an Excel file, normalizes column names to snake_case,
and stores the data in a DuckDB database.
"""

import os
import sys
import pandas as pd
import duckdb
from pathlib import Path


def normalize_column_names(df):
    """Normalize column names to snake_case."""
    df.columns = (
        df.columns.str.lower()
        .str.replace(r'\s+', '_', regex=True)
        .str.replace(r'[^\w]', '', regex=True)
    )
    return df


def ingest(excel_path, db_path='data.duckdb'):
    """
    Load Excel file into DuckDB.
    
    Args:
        excel_path: Path to Excel file
        db_path: Path to DuckDB database file
    
    Returns:
        dict with row_count, columns, and dtypes
    """
    if not os.path.exists(excel_path):
        raise FileNotFoundError(f"Excel file not found: {excel_path}")
    
    # Read Excel file
    df = pd.read_excel(excel_path, engine='openpyxl')
    
    # Normalize column names
    df = normalize_column_names(df)
    
    # Infer dtypes
    df = df.infer_objects()
    
    # Connect to DuckDB and write data
    conn = duckdb.connect(db_path)
    conn.register('temp_df', df)
    conn.execute('CREATE OR REPLACE TABLE records AS SELECT * FROM temp_df')
    conn.close()
    
    # Print summary
    summary = {
        'row_count': len(df),
        'columns': df.columns.tolist(),
        'dtypes': df.dtypes.to_dict(),
    }
    
    print(f"[OK] Ingested {summary['row_count']} rows into {db_path}")
    print(f"Columns: {', '.join(summary['columns'])}")
    print(f"Dtypes: {summary['dtypes']}")
    
    return summary


if __name__ == '__main__':
    excel_path = os.getenv('EXCEL_PATH', 'data.xlsx')
    
    if len(sys.argv) > 1:
        excel_path = sys.argv[1]
    
    ingest(excel_path)
