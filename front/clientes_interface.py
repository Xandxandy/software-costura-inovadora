"""Interface Streamlit para gerenciamento de clientes.

Fornece a interface para visualizar, adicionar, editar e deletar clientes.
"""

import re
import time

import streamlit as st
import pandas as pd
from back.clientes import (
    adicionar_cliente,
    inativar_cliente,
    listar_clientes,
    editar_cliente,
    deletar_cliente,
    listar_clientes_inativos,
    obter_cliente,
    reativar_cliente,
)


def mostrar_interface_clientes():
    """Exibe a interface completa de gerenciamento de clientes."""
    
    st.subheader("📋 Gerenciamento de Clientes")
    
    # Abas para diferentes operações
    tab1, tab2, tab3, tab4 = st.tabs(["Listar", "Adicionar", "Editar", "Deletar"])
    
    # TAB 1: LISTAR CLIENTES
    with tab1:
        st.write("**Lista de Clientes Cadastrados**")
        df = listar_clientes()
        
        if df.empty:
            st.info("Nenhum cliente cadastrado.")
        else:
            termo_pesquisa = st.text_input("🔍 Pesquisar por nome ou email", placeholder="Digite o nome ou email para filtrar")
            if termo_pesquisa:
                df = df[df['nome'].str.contains(termo_pesquisa, case=False) | df['email'].str.contains(termo_pesquisa, case=False)]
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.write(f"Total de clientes: {len(df)}")

        mostrar_lixeira = st.checkbox("Mostrar clientes inativos", value=False)

        if mostrar_lixeira:
            df_inativos = listar_clientes_inativos()
            if df_inativos.empty:
                st.info("Nenhum cliente inativo encontrado.")
            else:
                st.subheader("🗑️ Clientes Inativos")
                for _, row in df_inativos.iterrows():
                    col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                    with col1:
                        st.write(f"{row['id_cliente']} - {row['nome']} ({row['email']})")
                    with col2:
                        st.write(row['telefone'])
                    with col3:
                        st.write(row['status_texto'])
                    with col4:
                        if st.button("♻️ Reativar", key=f"reativar_{row['id_cliente']}"):
                            if reativar_cliente(row['id_cliente']):
                                st.success("✅ Cliente reativado com sucesso!")
                                time.sleep(1.5)  # Pequena pausa para o usuário ver a mensagem
                                st.rerun()
                            else:
                                st.error("❌ Erro ao reativar cliente!")
    
    # TAB 2: ADICIONAR CLIENTE
    with tab2:
        st.write("**Adicionar Novo Cliente**")

        if "contador_form" not in st.session_state:
            st.session_state.contador_form = 0

        with st.form(key=f"form_adicionar_cliente_{st.session_state.contador_form}"):
            nome = st.text_input("Nome", placeholder="Digite o nome do cliente")
            telefone = st.text_input("Telefone", placeholder="Digite o telefone", help="Digite o DDD seguido do número (ex: 11987654321)")
            email = st.text_input("Email", placeholder="Digite o email")
            
            submit_btn = st.form_submit_button("➕ Adicionar Cliente")
            
            if submit_btn:

                telefone_limpo = re.sub(r"\D", "", telefone)  # Remove tudo que não for número do telefone

                if not nome or not telefone or not email:
                    st.error("❌ Todos os campos são obrigatórios!")
                elif any(char.isdigit() for char in nome):
                    st.error("❌ O nome não pode conter números!")
                elif not (10 <= len(telefone_limpo) <= 11):
                    st.error("❌ Telefone inválido! Digite DDD + Número (10 ou 11 dígitos).")
                elif "@" not in email or "." not in email.split("@")[-1]:
                    st.error("❌ Email inválido!")
                else:
                    if adicionar_cliente(nome, telefone_limpo, email):
                        st.success("✅ Cliente adicionado com sucesso!")
                        st.session_state.contador_form += 1  # Incrementa o contador para criar um novo formulário único
                        time.sleep(1.5)  # Pequena pausa para o usuário ver a mensagem
                        st.rerun()
                    else:
                        st.error("❌ Erro ao adicionar cliente!")
                        
    # TAB 3: EDITAR CLIENTE
    with tab3:
        st.write("**Editar Cliente Existente**")
        
        df_clientes = listar_clientes()
        
        if df_clientes.empty:
            st.info("Nenhum cliente para editar.")
        else:
            # Criar um dicionário para facilitar a seleção
            clientes_dict = {
                f"{row['id_cliente']} - {row['nome']}": row['id_cliente']
                for _, row in df_clientes.iterrows()
            }
            
            cliente_selecionado = st.selectbox(
                "Selecione o cliente a editar:",
                options=clientes_dict.keys()
            )
            
            if cliente_selecionado:
                id_cliente = clientes_dict[cliente_selecionado]
                cliente_info = obter_cliente(id_cliente)
                
                with st.form("form_editar_cliente"):
                    nome = st.text_input("Nome", value=cliente_info.get('nome', ''))
                    telefone = st.text_input("Telefone", value=cliente_info.get('telefone', ''))
                    email = st.text_input("Email", value=cliente_info.get('email', ''))
                    
                    submit_btn = st.form_submit_button("✏️ Atualizar Cliente")
                    
                    if submit_btn:
                        if not nome or not telefone or not email:
                            st.error("❌ Todos os campos são obrigatórios!")
                        elif any(char.isdigit() for char in nome):
                            st.error("❌ O nome não pode conter números!")
                        elif any(char.isalpha() for char in telefone):
                            st.error("❌ O telefone deve conter apenas números!")
                        elif "@" not in email or "." not in email.split("@")[-1]:
                            st.error("❌ Email inválido!")
                        else:
                            if editar_cliente(id_cliente, nome, telefone, email):
                                st.success("✅ Cliente atualizado com sucesso!")
                                time.sleep(1.5)  # Pequena pausa para o usuário ver a mensagem
                                st.rerun()
                            else:
                                st.error("❌ Erro ao atualizar cliente!")
    
    # TAB 4: DESATIVAR CLIENTE
    with tab4:
        st.write("**Desativar Cliente**")
        
        df_clientes = listar_clientes()
        
        if df_clientes.empty:
            st.info("Nenhum cliente para desativar.")
        else:
            clientes_dict = {
                f"{row['id_cliente']} - {row['nome']}": row['id_cliente']
                for _, row in df_clientes.iterrows()
            }
            
            cliente_selecionado = st.selectbox(
                "Selecione o cliente a desativar:",
                options=clientes_dict.keys(),
                key="select_desativar"
            )
            
            if cliente_selecionado:
                id_cliente = clientes_dict[cliente_selecionado]
                st.warning("⚠️ Esta ação irá desativar o cliente, mas os dados permanecerão no sistema. Deseja continuar?")
                
                if st.button("🗑️ Desativar Cliente"):
                    if inativar_cliente(id_cliente):
                        st.success("✅ Cliente desativado com sucesso!")
                        time.sleep(1.5)  # Pequena pausa para o usuário ver a mensagem
                        st.rerun()
                    else:
                        st.error("❌ Erro ao desativar cliente!")