import sqlite3

# Criação de um arquivo banco de dados (.db) no computador
import os

# garantir que o arquivo fique dentro do diretório sqlite_db em vez da raiz
db_dir = os.path.dirname(__file__)
file = os.path.join(db_dir, "Sqlite3.db")

# Método de teste e erro (try/except) para correr o código
try:
    # Conectando o banco de dados no arquivo gerado no início do código e ativando as chaves estrangeiras
    conn = sqlite3.connect(file)
    conn.execute("PRAGMA foreign_keys = ON")
    print("\n-Arquivo de banco de dados criado-\n")

    # Criação do cursos para realizar as operações sql
    cursor = conn.cursor()

    # Código para criar as tabelas
    tabela_cliente = '''
    CREATE TABLE IF NOT EXISTS cliente (
        id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL CHECK (nome NOT GLOB '*[0-9]*'),
        telefone TEXT NOT NULL UNIQUE CHECK (telefone NOT GLOB '*[a-zA-Z]*'),
        email TEXT NOT NULL UNIQUE CHECK (email LIKE '%@%.%'),
        status INTEGER DEFAULT 1
    );
    '''
    tabela_pedido = '''
    CREATE TABLE IF NOT EXISTS pedido (
        id_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
        valor_total DECIMAL(10, 2),
        data_pedido DATE,
        status TEXT,
        id_cliente INTEGER,
        observacoes TEXT,
        FOREIGN KEY (id_cliente) REFERENCES cliente (id_cliente)
    );
    '''
    tabela_servico = '''
    CREATE TABLE IF NOT EXISTS servico (
        id_servico INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_servico TEXT,
        preco_base DECIMAL(10, 2)
    );
    '''
    tabela_item_pedido = '''
    CREATE TABLE IF NOT EXISTS item_pedido (
        id_item INTEGER PRIMARY KEY AUTOINCREMENT,
        quantidade INTEGER,
        valor_unitario DECIMAL(10, 2),
        id_pedido INTEGER,
        id_servico INTEGER,
        FOREIGN KEY (id_pedido) REFERENCES pedido (id_pedido),
        FOREIGN KEY (id_servico) REFERENCES servico (id_servico)
    );
    '''
    
    # Execução do código para criar as tabelas
    cursor.execute(tabela_cliente)
    cursor.execute(tabela_pedido)
    cursor.execute(tabela_servico)
    cursor.execute(tabela_item_pedido)
    conn.commit()
    
    # Gerando código para mostrar os dados no terminal
    cursor.execute("""
    SELECT c.nome, p.data_pedido, s.nome_servico, p.valor_total
    FROM cliente c
    JOIN pedido p ON c.id_cliente = p.id_cliente
    JOIN item_pedido ip ON p.id_pedido = ip.id_pedido
    JOIN servico s ON ip.id_servico = s.id_servico
    """)

    dados = cursor.fetchall()
    for linha in dados:
        print(f"Cliente: {linha[0]} | Data: {linha[1]} | Serviço: {linha[2]} | Total: R${linha[3]}")

except sqlite3.Error as error:
    print("Erro. Arquivo de banco de dados não criado.", error)

# Encerramento do banco de dados
finally:
    if conn:
        conn.close()
        print("\n-A conexão com o banco de dados foi encerrada-\n")