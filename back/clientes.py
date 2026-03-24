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
        query = "SELECT *, CASE status WHEN 1 THEN 'Ativo' ELSE 'Inativo' END AS status_texto FROM cliente WHERE status = 1 ORDER BY id_cliente"
        df = pd.read_sql_query(query, conn)
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

def inativar_cliente(id_cliente: int) -> bool:
    """Inativa um cliente no banco de dados.
    
    Args:
        id_cliente: ID do cliente a inativar
        
    Returns:
        True se inativado com sucesso, False caso contrário
    """
    try:
        conn = sqlite3.connect(get_db_path())
        cursor = conn.cursor()
        cursor.execute("UPDATE cliente SET status = 0 WHERE id_cliente = ?", (id_cliente,))
        conn.commit()
        conn.close()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Erro ao inativar cliente: {e}")
        return False

def listar_clientes_inativos() -> pd.DataFrame:
    """Retorna um DataFrame com os clientes inativos.
    
    Returns:
        DataFrame com os dados dos clientes inativos
    """
    try:
        conn = sqlite3.connect(get_db_path())
        query = "SELECT *, CASE status WHEN 1 THEN 'Ativo' ELSE 'Inativo' END AS status_texto FROM cliente WHERE status = 0 ORDER BY id_cliente"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except sqlite3.Error as e:
        print(f"Erro ao listar clientes inativos: {e}")
        return pd.DataFrame()

def reativar_cliente(id_cliente: int) -> bool:
    """Reativa um cliente inativo no banco de dados.
    
    Args:
        id_cliente: ID do cliente a reativar
        
    Returns:
        True se reativado com sucesso, False caso contrário
    """
    try:
        conn = sqlite3.connect(get_db_path())
        cursor = conn.cursor()
        cursor.execute("UPDATE cliente SET status = 1 WHERE id_cliente = ?", (id_cliente,))
        conn.commit()
        conn.close()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Erro ao reativar cliente: {e}")
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
