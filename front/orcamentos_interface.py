"""Interface Streamlit para gerenciamento de orçamentos.

Orçamentos são registrados na mesma tabela pedido com status 'Orçamento'.
"""

import time

import streamlit as st
import pandas as pd
from datetime import datetime
from back.pedidos import (
    adicionar_pedido,
    listar_clientes_para_pedido,
    obter_pedido
)
from back.orcamentos import (
    listar_orcamentos,
    confirmar_orcamento
)
from back.servicos import listar_servicos


def mostrar_interface_orcamentos():
    st.subheader("💰 Gerenciamento de Orçamentos")

    if 'orcamento_carrinho' not in st.session_state:
        st.session_state.orcamento_carrinho = []

    tab1, tab2, tab3 = st.tabs(["Listar", "Adicionar Orçamento", "Confirmar Orçamento"])

    with tab1:
        st.write("**Orçamentos registrados**")
        df = listar_orcamentos()

        if df.empty:
            st.info("Nenhum orçamento cadastrado.")
        else:
            termo_pesquisa = st.text_input("🔍 Pesquisar por cliente ou valor", placeholder="Digite o nome do cliente ou valor para filtrar")
            if termo_pesquisa:
                df = df[df['nome_cliente'].str.contains(termo_pesquisa, case=False) | df['valor_total'].astype(str).str.contains(termo_pesquisa, case=False)]
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.write(f"Total de orçamentos: {len(df)}")

    with tab2:
        st.write("**Adicionar Novo Orçamento**")

        df_clientes = listar_clientes_para_pedido()

        if df_clientes.empty:
            st.error("❌ Nenhum cliente cadastrado. Adicione clientes primeiro!")
        else:
            df_servicos = listar_servicos()
            clientes_dict = {f"{row['id_cliente']} - {row['nome']}": row['id_cliente'] for _, row in df_clientes.iterrows()}
            cliente_selecionado = st.selectbox("Selecione o cliente", options=clientes_dict.keys())

            if df_servicos.empty:
                st.warning("Nenhum serviço cadastrado. Vá em Serviços e cadastre ao menos um serviço.")
            else:
                c1, c2 = st.columns([3, 1])
                with c1:
                    servicos_dict = {f"{row['id_servico']} - {row['nome_servico']}": row['id_servico'] for _, row in df_servicos.iterrows()}
                    servico_selecionado = st.selectbox("Selecione o serviço", options=servicos_dict.keys())
                with c2:
                    st.write("")
                    if st.button("➕ Adicionar Item", type="secondary"):
                        servico_escolhido = servicos_dict[servico_selecionado]
                        novo_item = {
                            "id_servico": servico_escolhido,
                            "nome_servico": df_servicos[df_servicos['id_servico'] == servico_escolhido]['nome_servico'].values[0],
                            "preco_unitario": df_servicos[df_servicos['id_servico'] == servico_escolhido]['preco_base'].values[0]
                        }
                        st.session_state.orcamento_carrinho.append(novo_item)
                        st.toast("Item adicionado ao orçamento!")
                        st.rerun()

            if st.session_state.orcamento_carrinho:
                st.divider()
                st.write("**Itens no Orçamento:**")
                df_carrinho = pd.DataFrame(st.session_state.orcamento_carrinho)
                st.dataframe(df_carrinho, use_container_width=True, hide_index=True)

                total_carrinho = df_carrinho['preco_unitario'].sum()
                col_t1, col_t2 = st.columns([3, 1])
                with col_t1:
                    st.write(f"**Total do Orçamento: R${total_carrinho:.2f}**")
                with col_t2:
                    if st.button("Limpar Orçamento", type="secondary"):
                        st.session_state.orcamento_carrinho = []
                        st.toast("Orçamento limpo!")
                        st.rerun()
            else:
                total_carrinho = 0.00

            valor_total = st.number_input(
                "Valor Total (R$)",
                value=float(total_carrinho),
                min_value=0.00,
                step=0.00,
                format="%.2f"
            )

            data_orcamento = st.date_input("Data do Orçamento", value=datetime.now())
            observacoes = st.text_area("Observações", placeholder="Detalhes do orçamento, tecido, etc.")

            if st.button("✅ Adicionar Orçamento"):
                id_cliente = clientes_dict[cliente_selecionado]
                data_str = data_orcamento.strftime("%Y-%m-%d")

                if adicionar_pedido(valor_total, data_str, "Orçamento", id_cliente, observacoes):
                    st.success("✅ Orçamento adicionado com sucesso!")
                    st.session_state.orcamento_carrinho = []
                    time.sleep(1.5)  # Pequena pausa para o usuário ver a mensagem
                    st.rerun()  # Recarrega a página para mostrar o novo orçamento na lista
                else:
                    st.error("❌ Erro ao adicionar orçamento!")

    with tab3:
        st.write("**Confirmar orçamento**")

        df_orcamentos = listar_orcamentos()

        if df_orcamentos.empty:
            st.info("Nenhum orçamento disponível para confirmação.")
        else:
            orcamentos_dict = {
                f"{row['id_pedido']} - Cliente: {row['nome_cliente']} - R${row['valor_total']}": row['id_pedido']
                for _, row in df_orcamentos.iterrows()
            }
            selecionado = st.selectbox("Selecione orçamento", options=orcamentos_dict.keys())
            id_orcamento = orcamentos_dict[selecionado]

            orcamento_info = obter_pedido(id_orcamento)
            st.info(
                f"**Orçamento selecionado**\n- ID: {orcamento_info.get('id_pedido')}\n- Cliente: {orcamento_info.get('id_cliente')}\n- Valor: R${orcamento_info.get('valor_total')}\n- Data: {orcamento_info.get('data_pedido')}\n- Status: {orcamento_info.get('status')}"
            )

            if st.button("✅ Confirmar orçamento como pedido"):
                if confirmar_orcamento(id_orcamento):
                    st.success("✅ Orçamento confirmado e convertido em pedido (status: Pendente).")
                    time.sleep(1.5)  # Pequena pausa para o usuário ver a mensagem
                    st.rerun()  # Recarrega a página para mostrar o novo orçamento na lista
                else:
                    st.error("❌ Falha ao confirmar orçamento. Verifique se ainda está no status 'Orçamento'.")