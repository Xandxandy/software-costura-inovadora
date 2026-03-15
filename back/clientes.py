"""Módulo para operações CRUD de clientes no banco de dados.

Este arquivo contém funções para adicionar, editar, deletar e listar clientes.
"""

import os
import sqlite3
import pandas as pd


def get_db_path():
    """Retorna o caminho do arquivo do banco de dados."""
    base = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(base, "sqlite_db", "Sqlite3.db")


def adicionar_cliente(nome: str, telefone: str, email: str) -> bool:
    """Adiciona um novo cliente ao banco de dados.
    
    Args:
        nome: Nome do cliente
        telefone: Telefone do cliente
        email: Email do cliente
        
    Returns:
        True se adicionado com sucesso, False caso contrário
    """
    try:
        conn = sqlite3.connect(get_db_path())
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO cliente (nome, telefone, email) VALUES (?, ?, ?)",
            (nome, telefone, email)
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Erro ao adicionar cliente: {e}")
        return False


def listar_clientes() -> pd.DataFrame:
    """Retorna um DataFrame com todos os clientes.
    
    Returns:
        DataFrame com os dados dos clientes
    """
    try:
        conn = sqlite3.connect(get_db_path())
        df = pd.read_sql_query("SELECT * FROM cliente ORDER BY id_cliente", conn)
        conn.close()
        return df
    except sqlite3.Error as e:
        print(f"Erro ao listar clientes: {e}")
        return pd.DataFrame()


def editar_cliente(id_cliente: int, nome: str, telefone: str, email: str) -> bool:
    """Edita um cliente existente.
    
    Args:
        id_cliente: ID do cliente
        nome: Novo nome
        telefone: Novo telefone
        email: Novo email
        
    Returns:
        True se editado com sucesso, False caso contrário
    """
    try:
        conn = sqlite3.connect(get_db_path())
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE cliente SET nome = ?, telefone = ?, email = ? WHERE id_cliente = ?",
            (nome, telefone, email, id_cliente)
        )
        conn.commit()
        conn.close()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Erro ao editar cliente: {e}")
        return False


def deletar_cliente(id_cliente: int) -> bool:
    """Deleta um cliente do banco de dados.
    
    Args:
        id_cliente: ID do cliente a deletar
        
    Returns:
        True se deletado com sucesso, False caso contrário
    """
    try:
        conn = sqlite3.connect(get_db_path())
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cliente WHERE id_cliente = ?", (id_cliente,))
        conn.commit()
        conn.close()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Erro ao deletar cliente: {e}")
        return False


def obter_cliente(id_cliente: int) -> dict:
    """Obtém os dados de um cliente específico.
    
    Args:
        id_cliente: ID do cliente
        
    Returns:
        Dicionário com os dados do cliente ou vazio se não encontrado
    """
    try:
        conn = sqlite3.connect(get_db_path())
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cliente WHERE id_cliente = ?", (id_cliente,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                "id_cliente": row[0],
                "nome": row[1],
                "telefone": row[2],
                "email": row[3]
            }
        return {}
    except sqlite3.Error as e:
        print(f"Erro ao obter cliente: {e}")
        return {}
