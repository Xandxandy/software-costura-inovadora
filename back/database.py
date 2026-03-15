"""Módulo para operações de banco de dados.

Este arquivo contém funções para acessar e manipular dados do banco de dados SQLite.
"""

import os
import sqlite3

import pandas as pd


def query_table(table_name: str) -> pd.DataFrame:
    """Retorna um DataFrame contendo todos os registros da tabela especificada."""
    # caminho relativo para o arquivo de banco na raiz do projeto
    base = os.path.dirname(os.path.dirname(__file__))
    db_path = os.path.join(base, "sqlite_db", "Sqlite3.db")
    conn = sqlite3.connect(db_path)
    try:
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    finally:
        conn.close()
    return df
