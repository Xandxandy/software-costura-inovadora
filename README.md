# Python-backend

Este repositório contém a parte backend de uma aplicação com Streamlit.

## Estrutura

- `main.py`: ponto de entrada que inicializa o banco e o frontend.
- `back/`: pacote com funções auxiliares (inicialização de banco e frontend).
- `front/`: código do aplicativo Streamlit.
- `sqlite_db/`: script de criação e inicialização do banco de dados SQLite.

## Uso

1. Instale as dependências, por exemplo:

   ```bash
   pip install streamlit
   ```

2. Execute:

   ```bash
   python main.py
   ```

3. A página será aberta automaticamente em `http://localhost:8501`.

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
