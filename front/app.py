import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu # Precisa instalar: pip install streamlit-option-menu

from back.database import query_table
from front.clientes_interface import mostrar_interface_clientes
from front.pedidos_interface import mostrar_interface_pedidos
from front.servicos_interface import mostrar_interface_servicos
from front.orcamentos_interface import mostrar_interface_orcamentos

# 1. Configuração da Página
st.set_page_config(page_title="Painel Geral", layout="wide")

# 2. Injeção de CSS
st.markdown("""
    <style>
        /* Fundo da página cinza claro */
        .main {
            background-color: #f8f9fa;
        }
        /* Estilo dos Cards de indicadores */
        .st-emotion-cache-12w0qpk { 
            background-color: white;
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #eee;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.02);
        }
        /* Ajuste do título */
        h1, h2, h3 {
            color: #1f2937;
            font-weight: 700;
        }
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar
with st.sidebar:
    st.markdown("### ✂️ Costura Inovadora")
    selected = option_menu(
        menu_title=None, # Título opcional
        options=["Início", "Clientes", "Orçamentos", "Pedidos", "Serviços"],
        icons=["house", "people", "file-earmark-text", "box", "scissors"],
        menu_icon="cast", 
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#6b7280", "font-size": "18px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"5px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#B31552", "color": "white"}, # Cor Magenta
        }
    )

# 4. Lógica de Navegação
if selected == "Clientes":
    mostrar_interface_clientes()

elif selected == "Pedidos":
    mostrar_interface_pedidos()

elif selected == "Orçamentos":
    mostrar_interface_orcamentos()

elif selected == "Serviços":
    mostrar_interface_servicos()

else: # Caso seja "Início"
    st.title("Painel Geral")
    st.caption("Bem-vindo ao sistema de gerenciamento de costura")
    
    # Criando os 4 Cards da imagem
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label="Clientes Ativos", value="1")
    with col2:
        st.metric(label="Pedidos", value="0")
    with col3:
        st.metric(label="Orçamentos", value="0")
    with col4:
        st.metric(label="Serviços", value="0")
    
    st.write("---")