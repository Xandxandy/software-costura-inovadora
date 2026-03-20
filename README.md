# Python-backend

Este repositório contém a parte backend de uma aplicação com Streamlit para gerenciamento de clientes, pedidos e serviços.

## Estrutura

- `main.py`: ponto de entrada que inicializa o banco e o frontend.
- `back/`: pacote com funções CRUD e auxiliares
  - `clientes.py`: operações CRUD para clientes
  - `pedidos.py`: operações CRUD para pedidos
  - `orcamentos.py`: operações CRUD para orçamentos
  - `servicos.py`: operações CRUD para serviços
  - `database.py`: funções gerais de banco de dados
  - `init_db.py`: inicialização do banco de dados
  - `start_frontend.py`: inicialização do Streamlit
- `front/`: código da aplicação Streamlit
  - `app.py`: página principal e navegação
  - `clientes_interface.py`: interface CRUD de clientes
  - `pedidos_interface.py`: interface CRUD de pedidos
  - `orcamentos_interface.py`: interface CRUD de orçamentos
  - `servicos_interface.py`: interface CRUD de serviços
- `sqlite_db/`: script de criação e inicialização do banco de dados SQLite

## Dependências

Além da biblioteca padrão do Python (como `sqlite3`, `os`, `subprocess` etc.),
este projeto usa os seguintes pacotes de terceiros:

- `streamlit` – framework de interface web;
- `pandas` – manipulação e exibição de tabelas;

Instale-os com:

```bash
pip install streamlit pandas
```

Em sistemas com múltiplos ambientes de Python, certifique-se de usar o mesmo
ambiente ao rodar `main.py`.

## Uso

1. Inicie o programa:

   ```bash
   python main.py
   ```

2. A página será aberta automaticamente em `http://localhost:8501`.

## Interface do Frontend

O frontend, implementado com Streamlit, apresenta uma **barra lateral à esquerda**
com cinco botões de navegação:

- **🖥️ Início**: Exibe a página inicial
- **🧑 Clientes**: Gerenciamento completo de clientes (CRUD)
- **👍 Orçamentos**: Gerenciamento de orçamentos com conversão para pedidos
- **📋 Pedidos**: Gerenciamento completo de pedidos (CRUD)
- **✂️ Serviços**: Gerenciamento completo de serviços (CRUD)

### Telas de Gerenciamento

Cada seção possui 3-4 abas de funcionalidade:

1. **Listar**: Visualiza todos os registros em formato de tabela
2. **Adicionar**: Formulário para inserir novos registros
3. **Editar**: Seleciona e atualiza um registro existente (não disponível em Orçamentos)
4. **Deletar**: Seleciona e remove um registro (não disponível em Orçamentos)

#### Clientes
- Campos: Nome, Telefone, Email
- Validação básica de email

#### Orçamentos
- Campos: Cliente (seleção), Valor Total (R$), Data do Orçamento
- Funcionalidades:
  - **Listar**: Visualizar todos os orçamentos registrados
  - **Adicionar Orçamento**: Criar novo orçamento com status `Orçamento`
  - **Confirmar Orçamento**: Converter orçamento em pedido (muda status para `Pendente`)
- Orçamentos são armazenados na mesma tabela de pedidos com status diferenciado

#### Pedidos
- Campos: Cliente (seleção), Valor Total, Data do Pedido, Status
- Status disponíveis: Pendente, Processando, Finalizado, Cancelado, Orçamento
- Exibe nome do cliente na listagem

#### Serviços
- Campos: Nome do Serviço, Preço Base
- Interface simples para gerenciar serviços

## Banco de Dados SQLite

O projeto usa um banco de dados SQLite localizado em `sqlite_db/Sqlite3.db`.
A primeira vez que o script roda, o arquivo é criado automaticamente e as tabelas
são (re)criados pelo script `sqlite_db/import sqlite3.py`. Por padrão o processo
apaga tabelas existentes sempre que o programa é executado — isso facilita testes
repetidos, mas não deve ser usado em ambiente de produção.

### Tabelas

- **cliente**: Armazena informações de clientes (id_cliente, nome, telefone, email)
- **pedido**: Armazena pedidos (id_pedido, valor_total, data_pedido, status, id_cliente)
- **servico**: Armazena serviços (id_servico, nome_servico, preco_base)
- **item_pedido**: Armazena itens de pedidos (id_item, quantidade, valor_unitario, id_pedido, id_servico)

Além disso:

- Chaves estrangeiras são ativadas usando `PRAGMA foreign_keys = ON`
- Relacionamento: Pedidos → Clientes e Items de Pedido → Pedidos/Serviços

## Notas

- A inicialização do banco remove e recria tabelas a cada execução (uso para testes).
- As operações CRUD validam dados antes de inserir/atualizar no banco.
- A página inicial só é exibida quando o botão "🖥️ Início" é clicado
- Configurações do Streamlit podem ser definidas em `~/.streamlit/config.toml`.
