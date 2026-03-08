"""Front-end básico usando Streamlit.

Este arquivo servirá como ponto de entrada para a aplicação de
interface.
"""

import pandas as pd
import streamlit as st

from back.database import query_table

st.set_page_config(page_title="Painel Geral")


st.title("Página Inicial")

# Inicializar session state para armazenar a visualização atual
if "view" not in st.session_state:
    st.session_state.view = None

# painel lateral com botões de navegação

# Botão de reset para voltar à condição inicial
if st.sidebar.button("🖥️ Início"):
    st.session_state.view = None

if st.sidebar.button("🧑 Clientes"):
    st.session_state.view = "usuario"

if st.sidebar.button("📋 Pedidos"):
    st.session_state.view = "pedido"

if st.sidebar.button("✂️ Serviços"):
    st.session_state.view = "servico"

if st.session_state.view:
    df = query_table(st.session_state.view)
    st.subheader(f"Tabela '{st.session_state.view}'")
    st.dataframe(df)
