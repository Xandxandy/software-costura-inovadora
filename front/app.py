"""Front-end básico usando Streamlit.

Este arquivo servirá como ponto de entrada para a aplicação de
interface.
"""

import os
import sqlite3

import pandas as pd
import streamlit as st


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


st.title("Aplicação Streamlit")

# painel lateral com botões de navegação
st.sidebar.header("Navegação")
view = None
if st.sidebar.button("Usuários"):
    view = "usuario"
elif st.sidebar.button("Pedidos"):
    view = "pedido"
elif st.sidebar.button("Serviços"):
    view = "servico"

st.write("Bem-vindo à interface do projeto!")

if view:
    df = query_table(view)
    st.subheader(f"Tabela '{view}'")
    st.dataframe(df)
