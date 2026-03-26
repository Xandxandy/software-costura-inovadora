"""Interface Streamlit para gerenciamento de serviços.

Fornece a interface para visualizar, adicionar, editar e deletar serviços.
"""

import time

import streamlit as st
import pandas as pd
from back.servicos import (
    adicionar_servico,
    listar_servicos,
    editar_servico,
    deletar_servico,
    obter_servico
)


def mostrar_interface_servicos():
    """Exibe a interface completa de gerenciamento de serviços."""
    
    st.subheader("✂️ Gerenciamento de Serviços")
    
    # Abas para diferentes operações
    tab1, tab2, tab3, tab4 = st.tabs(["Listar", "Adicionar", "Editar", "Deletar"])
    
    # TAB 1: LISTAR SERVIÇOS
    with tab1:
        st.write("**Lista de Serviços Cadastrados**")
        df = listar_servicos()
        
        if df.empty:
            st.info("Nenhum serviço cadastrado.")
        else:
            termo_pesquisa = st.text_input("🔍 Pesquisar por nome ou preço", placeholder="Digite o nome do serviço ou preço para filtrar")
            if termo_pesquisa:
                df = df[df['nome_servico'].str.contains(termo_pesquisa, case=False) | df['preco_base'].astype(str).str.contains(termo_pesquisa, case=False)]
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.write(f"Total de tipos de serviços: {len(df)}")
    
    # TAB 2: ADICIONAR SERVIÇO
    with tab2:
        st.write("**Adicionar Novo Serviço**")
        
        with st.form("form_adicionar_servico"):
            nome_servico = st.text_input(
                "Nome do Serviço",
                placeholder="Digite o nome do serviço"
            )
            preco_base = st.number_input(
                "Preço Base (R$)",
                min_value=0.01,
                step=0.01,
                format="%.2f"
            )
            
            submit_btn = st.form_submit_button("➕ Adicionar Serviço")
            
            if submit_btn:
                if not nome_servico:
                    st.error("❌ Nome do serviço é obrigatório!")
                else:
                    if adicionar_servico(nome_servico, preco_base):
                        st.success("✅ Serviço adicionado com sucesso!")
                        time.sleep(1.5)  # Pequena pausa para mostrar a mensagem antes de atualizar
                        st.rerun()
                    else:
                        st.error("❌ Erro ao adicionar serviço!")
    
    # TAB 3: EDITAR SERVIÇO
    with tab3:
        st.write("**Editar Serviço Existente**")
        
        df_servicos = listar_servicos()
        
        if df_servicos.empty:
            st.info("Nenhum serviço para editar.")
        else:
            # Criar um dicionário para facilitar a seleção
            servicos_dict = {
                f"{row['id_servico']} - {row['nome_servico']} (R${row['preco_base']})": row['id_servico']
                for _, row in df_servicos.iterrows()
            }
            
            servico_selecionado = st.selectbox(
                "Selecione o serviço a editar:",
                options=servicos_dict.keys()
            )
            
            if servico_selecionado:
                id_servico = servicos_dict[servico_selecionado]
                servico_info = obter_servico(id_servico)
                
                with st.form("form_editar_servico"):
                    nome_servico = st.text_input(
                        "Nome do Serviço",
                        value=servico_info.get('nome_servico', '')
                    )
                    preco_base = st.number_input(
                        "Preço Base (R$)",
                        value=float(servico_info.get('preco_base', 0)),
                        min_value=0.01,
                        step=0.01,
                        format="%.2f"
                    )
                    
                    submit_btn = st.form_submit_button("✏️ Atualizar Serviço")
                    
                    if submit_btn:
                        if not nome_servico:
                            st.error("❌ Nome do serviço é obrigatório!")
                        else:
                            if editar_servico(id_servico, nome_servico, preco_base):
                                st.success("✅ Serviço atualizado com sucesso!")
                                time.sleep(1.5)  # Pequena pausa para mostrar a mensagem antes de atualizar
                                st.rerun()
                            else:
                                st.error("❌ Erro ao atualizar serviço!")
    
    # TAB 4: DELETAR SERVIÇO
    with tab4:
        st.write("**Deletar Serviço**")
        
        df_servicos = listar_servicos()
        
        if df_servicos.empty:
            st.info("Nenhum serviço para deletar.")
        else:
            # Criar um dicionário para facilitar a seleção
            servicos_dict = {
                f"{row['id_servico']} - {row['nome_servico']} (R${row['preco_base']})": row['id_servico']
                for _, row in df_servicos.iterrows()
            }
            
            servico_selecionado = st.selectbox(
                "Selecione o serviço a deletar:",
                options=servicos_dict.keys()
            )
            
            if servico_selecionado:
                id_servico = servicos_dict[servico_selecionado]
                servico_info = obter_servico(id_servico)
                
                # Mostrar informações do serviço a deletar
                st.info(f"**Serviço a deletar:**\n- ID: {servico_info.get('id_servico')}\n- Nome: {servico_info.get('nome_servico')}\n- Preço Base: R${servico_info.get('preco_base')}")
                
                if st.button("🗑️ Deletar Serviço", type="secondary"):
                    if deletar_servico(id_servico):
                        st.success("✅ Serviço deletado com sucesso!")
                        time.sleep(1.5)  # Pequena pausa para mostrar a mensagem antes de atualizar
                        st.rerun()
                    else:
                        st.error("❌ Erro ao deletar serviço!")
