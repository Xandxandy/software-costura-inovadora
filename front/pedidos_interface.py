"""Interface Streamlit para gerenciamento de pedidos.

Fornece a interface para visualizar, adicionar, editar e deletar pedidos.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from back.pedidos import (
    adicionar_pedido,
    listar_pedidos,
    editar_pedido,
    deletar_pedido,
    obter_pedido,
    listar_clientes_para_pedido
)


def mostrar_interface_pedidos():
    """Exibe a interface completa de gerenciamento de pedidos."""
    
    st.subheader("📋 Gerenciamento de Pedidos")
    
    # Abas para diferentes operações
    tab1, tab2, tab3, tab4 = st.tabs(["Listar", "Adicionar", "Editar", "Deletar"])
    
    # TAB 1: LISTAR PEDIDOS
    with tab1:
        st.write("**Lista de Pedidos Cadastrados**")
        df = listar_pedidos()
        
        if df.empty:
            st.info("Nenhum pedido cadastrado.")
        else:
            st.dataframe(df, use_container_width=True)
            st.write(f"Total de pedidos: {len(df)}")
    
    # TAB 2: ADICIONAR PEDIDO
    with tab2:
        st.write("**Adicionar Novo Pedido**")
        
        # Obter lista de clientes
        df_clientes = listar_clientes_para_pedido()
        
        if df_clientes.empty:
            st.error("❌ Nenhum cliente cadastrado. Adicione clientes primeiro!")
        else:
            with st.form("form_adicionar_pedido"):
                # Criar dicionário para seleção de clientes
                clientes_dict = {f"{row['id_cliente']} - {row['nome']}": row['id_cliente'] 
                                for _, row in df_clientes.iterrows()}
                
                cliente_selecionado = st.selectbox(
                    "Selecione o cliente",
                    options=clientes_dict.keys()
                )
                
                valor_total = st.number_input(
                    "Valor Total (R$)",
                    min_value=0.01,
                    step=0.01,
                    format="%.2f"
                )
                
                data_pedido = st.date_input(
                    "Data do Pedido",
                    value=datetime.now()
                )
                
                status_options = ["Pendente", "Processando", "Finalizado", "Cancelado"]
                status = st.selectbox("Status", options=status_options)
                
                submit_btn = st.form_submit_button("➕ Adicionar Pedido")
                
                if submit_btn:
                    id_cliente = clientes_dict[cliente_selecionado]
                    data_str = data_pedido.strftime("%Y-%m-%d")
                    
                    if adicionar_pedido(valor_total, data_str, status, id_cliente):
                        st.success("✅ Pedido adicionado com sucesso!")
                        st.rerun()
                    else:
                        st.error("❌ Erro ao adicionar pedido!")
    
    # TAB 3: EDITAR PEDIDO
    with tab3:
        st.write("**Editar Pedido Existente**")
        
        df_pedidos = listar_pedidos()
        df_clientes = listar_clientes_para_pedido()
        
        if df_pedidos.empty:
            st.info("Nenhum pedido para editar.")
        else:
            # Criar um dicionário para facilitar a seleção
            pedidos_dict = {
                f"{row['id_pedido']} - Cliente: {row['nome_cliente']} - R${row['valor_total']}": row['id_pedido']
                for _, row in df_pedidos.iterrows()
            }
            
            pedido_selecionado = st.selectbox(
                "Selecione o pedido a editar:",
                options=pedidos_dict.keys()
            )
            
            if pedido_selecionado:
                id_pedido = pedidos_dict[pedido_selecionado]
                pedido_info = obter_pedido(id_pedido)
                
                # Criar dicionário de clientes
                clientes_dict = {f"{row['id_cliente']} - {row['nome']}": row['id_cliente'] 
                                for _, row in df_clientes.iterrows()}
                
                with st.form("form_editar_pedido"):
                    # 1. Busca o nome do cliente de forma segura (sem travar se não achar)
                    encontrados = [k for k, v in clientes_dict.items() if v == pedido_info.get('id_cliente')]
                    cliente_atual = encontrados[0] if encontrados else "Cliente não encontrado"

                    # 2. Prepara a lista de opções para o seletor
                    opcoes_clientes = list(clientes_dict.keys())

                    # 3. Tenta achar a posição do cliente_atual na lista para o seletor começar nele
                    try:
                        indice_cliente = opcoes_clientes.index(cliente_atual)
                    except ValueError:
                        # Se o cliente não existir no dicionário, seleciona o primeiro da lista
                        indice_cliente = 0

                    # 4. Cria o seletor de cliente
                    cliente_selecionado = st.selectbox(
                        "Cliente",
                        options=opcoes_clientes,
                        index=indice_cliente
                    )
                    
                    valor_total = st.number_input(
                        "Valor Total (R$)",
                        value=float(pedido_info.get('valor_total', 0)),
                        min_value=0.01,
                        step=0.01,
                        format="%.2f"
                    )
                    
                    # Converter string de data
                    data_pedido_str = pedido_info.get('data_pedido', '')
                    if data_pedido_str:
                        data_pedido = datetime.strptime(data_pedido_str, "%Y-%m-%d").date()
                    else:
                        data_pedido = datetime.now().date()
                    
                    data_pedido = st.date_input("Data do Pedido", value=data_pedido)
                    
                    status_options = ["Pendente", "Processando", "Finalizado", "Cancelado"]
                    status_atual = pedido_info.get('status', 'Pendente')
                    status_index = status_options.index(status_atual) if status_atual in status_options else 0
                    
                    status = st.selectbox(
                        "Status",
                        options=status_options,
                        index=status_index
                    )
                    
                    submit_btn = st.form_submit_button("✏️ Atualizar Pedido")
                    
                    if submit_btn:
                        id_cliente = clientes_dict[cliente_selecionado]
                        data_str = data_pedido.strftime("%Y-%m-%d")
                        
                        if editar_pedido(id_pedido, valor_total, data_str, status, id_cliente):
                            st.success("✅ Pedido atualizado com sucesso!")
                            st.rerun()
                        else:
                            st.error("❌ Erro ao atualizar pedido!")
    
    # TAB 4: DELETAR PEDIDO
    with tab4:
        st.write("**Deletar Pedido**")
        
        df_pedidos = listar_pedidos()
        
        if df_pedidos.empty:
            st.info("Nenhum pedido para deletar.")
        else:
            # Criar um dicionário para facilitar a seleção
            pedidos_dict = {
                f"{row['id_pedido']} - Cliente: {row['nome_cliente']} - R${row['valor_total']}": row['id_pedido']
                for _, row in df_pedidos.iterrows()
            }
            
            pedido_selecionado = st.selectbox(
                "Selecione o pedido a deletar:",
                options=pedidos_dict.keys()
            )
            
            if pedido_selecionado:
                id_pedido = pedidos_dict[pedido_selecionado]
                pedido_info = obter_pedido(id_pedido)
                
                # Mostrar informações do pedido a deletar
                st.info(f"**Pedido a deletar:**\n- ID: {pedido_info.get('id_pedido')}\n- Valor: R${pedido_info.get('valor_total')}\n- Data: {pedido_info.get('data_pedido')}\n- Status: {pedido_info.get('status')}")
                
                if st.button("🗑️ Deletar Pedido", type="secondary"):
                    if deletar_pedido(id_pedido):
                        st.success("✅ Pedido deletado com sucesso!")
                        st.rerun()
                    else:
                        st.error("❌ Erro ao deletar pedido!")
