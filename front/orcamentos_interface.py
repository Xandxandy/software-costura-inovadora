"""Interface Streamlit para gerenciamento de orçamentos.

Orçamentos são registrados na mesma tabela pedido com status 'Orçamento'.
"""

import streamlit as st
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


def mostrar_interface_orcamentos():
    st.subheader("💰 Gerenciamento de Orçamentos")

    tab1, tab2, tab3 = st.tabs(["Listar", "Adicionar Orçamento", "Confirmar Orçamento"])

    with tab1:
        st.write("**Orçamentos registrados**")
        df = listar_orcamentos()

        if df.empty:
            st.info("Nenhum orçamento cadastrado.")
        else:
            st.dataframe(df, use_container_width=True)
            st.write(f"Total de orçamentos: {len(df)}")

    with tab2:
        st.write("**Criar novo orçamento**")

        df_clientes = listar_clientes_para_pedido()

        if df_clientes.empty:
            st.error("❌ Nenhum cliente cadastrado. Adicione clientes primeiro!")
        else:
            with st.form("form_adicionar_orcamento"):
                clientes_dict = {f"{row['id_cliente']} - {row['nome']}": row['id_cliente'] for _, row in df_clientes.iterrows()}
                cliente_selecionado = st.selectbox("Selecione o cliente", options=clientes_dict.keys())

                valor_total = st.number_input(
                    "Valor Total (R$)",
                    min_value=0.01,
                    step=0.01,
                    format="%.2f"
                )

                data_orcamento = st.date_input("Data do Orçamento", value=datetime.now())

                submit_btn = st.form_submit_button("👍 Adicionar Orçamento")

                if submit_btn:
                    id_cliente = clientes_dict[cliente_selecionado]
                    data_str = data_orcamento.strftime("%Y-%m-%d")

                    if adicionar_pedido(valor_total, data_str, "Orçamento", id_cliente):
                        st.success("✅ Orçamento adicionado com sucesso!")
                        st.rerun()
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
                    st.rerun()
                else:
                    st.error("❌ Falha ao confirmar orçamento. Verifique se ainda está no status 'Orçamento'.")