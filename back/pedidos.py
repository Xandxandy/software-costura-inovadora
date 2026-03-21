"""Módulo para operações CRUD de pedidos no banco de dados.

Este arquivo contém funções para adicionar, editar, deletar e listar pedidos.
"""

import os
import sqlite3
import pandas as pd
from datetime import datetime


def get_db_path():
    """Retorna o caminho do arquivo do banco de dados."""
    base = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(base, "sqlite_db", "Sqlite3.db")


def adicionar_pedido(valor_total: float, data_pedido: str, status: str, id_cliente: int, observacoes: str = None) -> bool:
    """Adiciona um novo pedido ao banco de dados.
    
    Args:
        valor_total: Valor total do pedido
        data_pedido: Data do pedido (formato YYYY-MM-DD)
        status: Status do pedido
        id_cliente: ID do cliente
        observacoes: Observações sobre o pedido (opcional)
        
    Returns:
        True se adicionado com sucesso, False caso contrário
    """
    try:
        conn = sqlite3.connect(get_db_path())
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO pedido (valor_total, data_pedido, status, id_cliente, observacoes) VALUES (?, ?, ?, ?, ?)",
            (valor_total, data_pedido, status, id_cliente, observacoes)
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Erro ao adicionar pedido: {e}")
        return False


def listar_pedidos() -> pd.DataFrame:
    """Retorna um DataFrame com todos os pedidos.
    
    Returns:
        DataFrame com os dados dos pedidos
    """
    try:
        conn = sqlite3.connect(get_db_path())
        df = pd.read_sql_query("""
            SELECT p.*, c.nome as nome_cliente 
            FROM pedido p
            LEFT JOIN cliente c ON p.id_cliente = c.id_cliente
            ORDER BY p.id_pedido
        """, conn)
        conn.close()
        return df
    except sqlite3.Error as e:
        print(f"Erro ao listar pedidos: {e}")
        return pd.DataFrame()


def editar_pedido(id_pedido: int, valor_total: float, data_pedido: str, status: str, id_cliente: int, observacoes: str = None) -> bool:
    """Edita um pedido existente.
    
    Args:
        id_pedido: ID do pedido
        valor_total: Novo valor total
        data_pedido: Nova data
        status: Novo status
        id_cliente: Novo ID do cliente
        observacoes: Novas observações sobre o pedido (opcional)
        
    Returns:
        True se editado com sucesso, False caso contrário
    """
    try:
        conn = sqlite3.connect(get_db_path())
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE pedido SET valor_total = ?, data_pedido = ?, status = ?, id_cliente = ?, observacoes = ? WHERE id_pedido = ?",
            (valor_total, data_pedido, status, id_cliente, observacoes, id_pedido)
        )
        conn.commit()
        conn.close()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Erro ao editar pedido: {e}")
        return False


def deletar_pedido(id_pedido: int) -> bool:
    """Deleta um pedido do banco de dados.
    
    Args:
        id_pedido: ID do pedido a deletar
        
    Returns:
        True se deletado com sucesso, False caso contrário
    """
    try:
        conn = sqlite3.connect(get_db_path())
        cursor = conn.cursor()
        cursor.execute("DELETE FROM pedido WHERE id_pedido = ?", (id_pedido,))
        conn.commit()
        conn.close()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Erro ao deletar pedido: {e}")
        return False


def obter_pedido(id_pedido: int) -> dict:
    """Obtém os dados de um pedido específico.
    
    Args:
        id_pedido: ID do pedido
        
    Returns:
        Dicionário com os dados do pedido ou vazio se não encontrado
    """
    try:
        conn = sqlite3.connect(get_db_path())
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pedido WHERE id_pedido = ?", (id_pedido,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                "id_pedido": row[0],
                "valor_total": row[1],
                "data_pedido": row[2],
                "status": row[3],
                "id_cliente": row[4]
            }
        return {}
    except sqlite3.Error as e:
        print(f"Erro ao obter pedido: {e}")
        return {}


def listar_clientes_para_pedido() -> pd.DataFrame:
    """Retorna uma lista de clientes para seleção ao criar/editar pedidos."""
    try:
        conn = sqlite3.connect(get_db_path())
        df = pd.read_sql_query("SELECT id_cliente, nome FROM cliente ORDER BY nome", conn)
        conn.close()
        return df
    except sqlite3.Error as e:
        print(f"Erro ao listar clientes: {e}")
        return pd.DataFrame()
