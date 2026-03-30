"""Interface Streamlit para gerenciamento de pedidos.

Fornece a interface para visualizar, adicionar, editar e deletar pedidos.
"""

import time

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
from back.servicos import listar_servicos


def mostrar_interface_pedidos():
    """Exibe a interface completa de gerenciamento de pedidos."""
    
    st.subheader("📋 Gerenciamento de Pedidos")
    
    # Abas para diferentes operações
    tab1, tab2, tab3, tab4 = st.tabs(["Listar", "Adicionar", "Editar", "Deletar"])

    if 'carrinho' not in st.session_state:
        st.session_state.carrinho = []

    # TAB 1: LISTAR PEDIDOS
    with tab1:
        st.write("**Lista de Pedidos Cadastrados**")
        df = listar_pedidos()
        
        if df.empty:
            st.info("Nenhum pedido cadastrado.")
        else:
            termo_pesquisa = st.text_input("🔍 Pesquisar por cliente ou valor", placeholder="Digite o nome do cliente ou valor para filtrar")
            if termo_pesquisa:
                df = df[df['nome_cliente'].str.contains(termo_pesquisa, case=False) | df['valor_total'].astype(str).str.contains(termo_pesquisa, case=False)]
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.write(f"Total de pedidos: {len(df)}")
    
    # TAB 2: ADICIONAR PEDIDO
    with tab2:
        st.write("**Adicionar Novo Pedido**")
        
        # Obter lista de clientes
        df_clientes = listar_clientes_para_pedido()
        
        if df_clientes.empty:
            st.error("❌ Nenhum cliente cadastrado. Adicione clientes primeiro!")
        else:
                # Criar dicionário para seleção de clientes
                clientes_dict = {f"{row['id_cliente']} - {row['nome']}": row['id_cliente'] 
                                for _, row in df_clientes.iterrows()}
                
                cliente_selecionado = st.selectbox(
                    "Selecione o cliente",
                    options=clientes_dict.keys()
                )
                
                data_pedido = st.date_input(
                    "Data do Pedido",
                    value=datetime.now()
                )
                
                df_servicos = listar_servicos()
                if not df_servicos.empty:

                    c1, c2 = st.columns([3, 1])  # Coluna maior para o selectbox e menor para o botão

                    with c1:
                        #criar um dicionário de serviços para facilitar a seleção
                        servicos_dict = {f"{row['id_servico']} - {row['nome_servico']}": row['id_servico'] 
                                        for _, row in df_servicos.iterrows()}
                        servico_selecionado = st.selectbox(
                            "Selecione o serviço",
                            options=servicos_dict.keys()
                        )

                    with c2:
                        st.write("") # Espaço para alinhar o botão
                        if st.button("➕ Adicionar Item", type="secondary"):
                            servico_escolhido = servicos_dict[servico_selecionado]

                            novo_item = {
                                "id_servico": servico_escolhido,
                                "nome_servico": df_servicos[df_servicos['id_servico'] == servico_escolhido]['nome_servico'].values[0],
                                "preco_unitario": df_servicos[df_servicos['id_servico'] == servico_escolhido]['preco_base'].values[0]
                            }

                            if "carrinho" not in st.session_state:
                                st.session_state.carrinho = []

                            st.session_state.carrinho.append(novo_item)
                            st.toast("Item adicionado ao carrinho!")
                            st.rerun()

                    if "carrinho" in st.session_state and st.session_state.carrinho:
                        st.divider()
                        st.write("**Itens no Carrinho:**")
                        df_carrinho = pd.DataFrame(st.session_state.carrinho)
                        st.dataframe(df_carrinho, use_container_width=True, hide_index=True)

                        col_t1, col_t2 = st.columns([3, 1])
                        with col_t1:
                            total_carrinho = df_carrinho['preco_unitario'].sum()
                            st.write(f"**Total do Carrinho: R${total_carrinho:.2f}**")

                        with col_t2:
                            if st.button("Limpar Carrinho", type="secondary"):
                                st.session_state.carrinho = []
                                st.toast("Carrinho limpo!")
                                st.rerun()

                valor_total = st.number_input(
                    "Valor Total (R$)",
                    value=float(total_carrinho) if "carrinho" in st.session_state and st.session_state.carrinho else 0.00,
                    min_value=0.00,
                    step=0.00,
                    format="%.2f"
                )

                st.write("**Status inicial: Pendente**")
                status = "Pendente"

                observacoes = st.text_area("Observações", placeholder="Ex: Detalhes do ajuste, tecido, etc.")
                
                if st.button("✅ Adicionar Pedido"):
                    id_cliente = clientes_dict[cliente_selecionado]
                    data_str = data_pedido.strftime("%Y-%m-%d")
                    
                    if adicionar_pedido(valor_total, data_str, status, id_cliente, observacoes):
                        st.success("✅ Pedido adicionado com sucesso!")
                        time.sleep(1.5)  # Pequena pausa para mostrar a mensagem antes de atualizar
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
                    
                    observacoes = st.text_area( 
                        "Observações", 
                        value=pedido_info.get('observacoes', ''),
                        placeholder="Ex: Detalhes do ajuste, tecido, etc."
                    )

                    submit_btn = st.form_submit_button("✏️ Atualizar Pedido")
                    
                    if submit_btn:
                        id_cliente = clientes_dict[cliente_selecionado]
                        data_str = data_pedido.strftime("%Y-%m-%d")
                        
                        if editar_pedido(id_pedido, valor_total, data_str, status, id_cliente, observacoes):
                            st.success("✅ Pedido atualizado com sucesso!")
                            time.sleep(1.5)  # Pequena pausa para mostrar a mensagem antes de atualizar
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
                        time.sleep(1.5)  # Pequena pausa para mostrar a mensagem antes de atualizar
                        st.rerun()
                    else:
                        st.error("❌ Erro ao deletar pedido!")
