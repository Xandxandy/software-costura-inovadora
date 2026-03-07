# Python-backend

Este repositório contém a parte backend de uma aplicação com Streamlit.

## Estrutura

- `main.py`: ponto de entrada que inicializa o banco e o frontend.
- `back/`: pacote com funções auxiliares (inicialização de banco e frontend).
- `front/`: código do aplicativo Streamlit.
- `sqlite_db/`: script de criação e inicialização do banco de dados SQLite.

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
com três botões de navegação: *Usuários*, *Pedidos* e *Serviços*. Ao clicar em um
dos botões, a aplicação carrega a tabela correspondente do banco de dados e mostra
os registros em uma grade (`st.dataframe`).

Os dados são consultados diretamente no arquivo `sqlite_db/Sqlite3.db` usando uma
função auxiliar (`query_table`) localizada em `front/app.py`.

## Banco de Dados SQLite

O projeto usa um banco de dados SQLite localizado em `sqlite_db/Sqlite3.db`.
A primeira vez que o script roda, o arquivo é criado automaticamente e as tabelas
são (re)criados pelo script `sqlite_db/import sqlite3.py`. Por padrão o processo
apaga tabelas existentes sempre que o programa é executado — isso facilita testes
repetidos, mas não deve ser usado em ambiente de produção.

Além disso:

- a coluna `email` da tabela `usuario` não possui coerção de unicidade;
- chaves estrangeiras são ativadas usando `PRAGMA foreign_keys = ON` no início
do script.

## Notas

- A inicialização do banco remove e recria tabelas a cada execução (uso para testes).
- A restrição `UNIQUE` no campo `email` foi removida propositalmente.
- Configurações do Streamlit podem ser definidas em `~/.streamlit/config.toml`.
