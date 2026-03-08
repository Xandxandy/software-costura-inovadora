"""Interface Streamlit para gerenciamento de clientes.

Fornece a interface para visualizar, adicionar, editar e deletar clientes.
"""

import streamlit as st
import pandas as pd
from back.clientes import (
    adicionar_cliente,
    listar_clientes,
    editar_cliente,
    deletar_cliente,
    obter_cliente
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
            st.dataframe(df, use_container_width=True)
            st.write(f"Total de clientes: {len(df)}")
    
    # TAB 2: ADICIONAR CLIENTE
    with tab2:
        st.write("**Adicionar Novo Cliente**")
        
        with st.form("form_adicionar_cliente"):
            nome = st.text_input("Nome", placeholder="Digite o nome do cliente")
            telefone = st.text_input("Telefone", placeholder="Digite o telefone")
            email = st.text_input("Email", placeholder="Digite o email")
            
            submit_btn = st.form_submit_button("➕ Adicionar Cliente")
            
            if submit_btn:
                if not nome or not telefone or not email:
                    st.error("❌ Todos os campos são obrigatórios!")
                elif "@" not in email:
                    st.error("❌ Email inválido!")
                else:
                    if adicionar_cliente(nome, telefone, email):
                        st.success("✅ Cliente adicionado com sucesso!")
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
                        elif "@" not in email:
                            st.error("❌ Email inválido!")
                        else:
                            if editar_cliente(id_cliente, nome, telefone, email):
                                st.success("✅ Cliente atualizado com sucesso!")
                                st.rerun()
                            else:
                                st.error("❌ Erro ao atualizar cliente!")
    
    # TAB 4: DELETAR CLIENTE
    with tab4:
        st.write("**Deletar Cliente**")
        
        df_clientes = listar_clientes()
        
        if df_clientes.empty:
            st.info("Nenhum cliente para deletar.")
        else:
            # Criar um dicionário para facilitar a seleção
            clientes_dict = {
                f"{row['id_cliente']} - {row['nome']}": row['id_cliente']
                for _, row in df_clientes.iterrows()
            }
            
            cliente_selecionado = st.selectbox(
                "Selecione o cliente a deletar:",
                options=clientes_dict.keys()
            )
            
            if cliente_selecionado:
                id_cliente = clientes_dict[cliente_selecionado]
                cliente_info = obter_cliente(id_cliente)
                
                # Mostrar informações do cliente a deletar
                st.info(f"**Cliente a deletar:**\n- Nome: {cliente_info.get('nome')}\n- Telefone: {cliente_info.get('telefone')}\n- Email: {cliente_info.get('email')}")
                
                if st.button("🗑️ Deletar Cliente", type="secondary"):
                    if deletar_cliente(id_cliente):
                        st.success("✅ Cliente deletado com sucesso!")
                        st.rerun()
                    else:
                        st.error("❌ Erro ao deletar cliente!")
