"""Módulo para operações CRUD de serviços no banco de dados.

Este arquivo contém funções para adicionar, editar, deletar e listar serviços.
"""

import os
import sqlite3
import pandas as pd


def get_db_path():
    """Retorna o caminho do arquivo do banco de dados."""
    base = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(base, "sqlite_db", "Sqlite3.db")


def adicionar_servico(nome_servico: str, preco_base: float) -> bool:
    """Adiciona um novo serviço ao banco de dados.
    
    Args:
        nome_servico: Nome do serviço
        preco_base: Preço base do serviço
        
    Returns:
        True se adicionado com sucesso, False caso contrário
    """
    try:
        conn = sqlite3.connect(get_db_path())
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO servico (nome_servico, preco_base) VALUES (?, ?)",
            (nome_servico, preco_base)
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Erro ao adicionar serviço: {e}")
        return False


def listar_servicos() -> pd.DataFrame:
    """Retorna um DataFrame com todos os serviços.
    
    Returns:
        DataFrame com os dados dos serviços
    """
    try:
        conn = sqlite3.connect(get_db_path())
        df = pd.read_sql_query("SELECT * FROM servico ORDER BY id_servico", conn)
        conn.close()
        return df
    except sqlite3.Error as e:
        print(f"Erro ao listar serviços: {e}")
        return pd.DataFrame()


def editar_servico(id_servico: int, nome_servico: str, preco_base: float) -> bool:
    """Edita um serviço existente.
    
    Args:
        id_servico: ID do serviço
        nome_servico: Novo nome do serviço
        preco_base: Novo preço base
        
    Returns:
        True se editado com sucesso, False caso contrário
    """
    try:
        conn = sqlite3.connect(get_db_path())
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE servico SET nome_servico = ?, preco_base = ? WHERE id_servico = ?",
            (nome_servico, preco_base, id_servico)
        )
        conn.commit()
        conn.close()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Erro ao editar serviço: {e}")
        return False


def deletar_servico(id_servico: int) -> bool:
    """Deleta um serviço do banco de dados.
    
    Args:
        id_servico: ID do serviço a deletar
        
    Returns:
        True se deletado com sucesso, False caso contrário
    """
    try:
        conn = sqlite3.connect(get_db_path())
        cursor = conn.cursor()
        cursor.execute("DELETE FROM servico WHERE id_servico = ?", (id_servico,))
        conn.commit()
        conn.close()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Erro ao deletar serviço: {e}")
        return False


def obter_servico(id_servico: int) -> dict:
    """Obtém os dados de um serviço específico.
    
    Args:
        id_servico: ID do serviço
        
    Returns:
        Dicionário com os dados do serviço ou vazio se não encontrado
    """
    try:
        conn = sqlite3.connect(get_db_path())
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM servico WHERE id_servico = ?", (id_servico,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                "id_servico": row[0],
                "nome_servico": row[1],
                "preco_base": row[2]
            }
        return {}
    except sqlite3.Error as e:
        print(f"Erro ao obter serviço: {e}")
        return {}
