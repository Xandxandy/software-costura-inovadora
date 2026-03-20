"""Lógica de orçamentos (status 'Orçamento') no banco de dados."""

import sqlite3
from back.pedidos import get_db_path
import pandas as pd


def listar_orcamentos() -> pd.DataFrame:
    """Retorna um DataFrame com todos os orçamentos."""
    try:
        conn = sqlite3.connect(get_db_path())
        df = pd.read_sql_query("""
            SELECT p.*, c.nome as nome_cliente
            FROM pedido p
            LEFT JOIN cliente c ON p.id_cliente = c.id_cliente
            WHERE p.status = 'Orçamento'
            ORDER BY p.id_pedido
        """, conn)
        conn.close()
        return df
    except sqlite3.Error as e:
        print(f"Erro ao listar orçamentos: {e}")
        return pd.DataFrame()


def confirmar_orcamento(id_pedido: int) -> bool:
    """Converte um orçamento em pedido alterando seu status para Pendente."""
    try:
        conn = sqlite3.connect(get_db_path())
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE pedido SET status = 'Pendente' WHERE id_pedido = ? AND status = 'Orçamento'",
            (id_pedido,)
        )
        conn.commit()
        updated = cursor.rowcount > 0
        conn.close()
        return updated
    except sqlite3.Error as e:
        print(f"Erro ao confirmar orçamento: {e}")
        return False
