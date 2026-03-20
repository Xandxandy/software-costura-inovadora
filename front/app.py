"""Front-end básico usando Streamlit.

Este arquivo servirá como ponto de entrada para a aplicação de
interface.
"""

import pandas as pd
import streamlit as st

from back.database import query_table
from front.clientes_interface import mostrar_interface_clientes
from front.pedidos_interface import mostrar_interface_pedidos
from front.servicos_interface import mostrar_interface_servicos
from front.orcamentos_interface import mostrar_interface_orcamentos

st.set_page_config(page_title="Painel Geral")

# Inicializar session state para armazenar a visualização atual
if "view" not in st.session_state:
    st.session_state.view = None

# painel lateral com botões de navegação

# Botão de reset para voltar à condição inicial
if st.sidebar.button("🖥️ Início"):
    st.session_state.view = None

if st.sidebar.button("🧑 Clientes"):
    st.session_state.view = "cliente"

if st.sidebar.button("👍 Orçamentos"):
    st.session_state.view = "orcamento"

if st.sidebar.button("📋 Pedidos"):
    st.session_state.view = "pedido"

if st.sidebar.button("✂️ Serviços"):
    st.session_state.view = "servico"

if st.session_state.view == "cliente":
    mostrar_interface_clientes()
elif st.session_state.view == "pedido":
    mostrar_interface_pedidos()
elif st.session_state.view == "orcamento":
    mostrar_interface_orcamentos()
elif st.session_state.view == "servico":
    mostrar_interface_servicos()
elif st.session_state.view:
    df = query_table(st.session_state.view)
    st.subheader(f"Tabela '{st.session_state.view}'")
    st.dataframe(df)
else:
    st.title("Página Inicial")
