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

    # Excluindo as tabelas. OBS: Fiz isso para ficar resetando as tabelas com finalidade de testar o código várias vezes
    cursor.execute("DROP TABLE IF EXISTS item_pedido")
    cursor.execute("DROP TABLE IF EXISTS pedido")
    cursor.execute("DROP TABLE IF EXISTS servico")
    cursor.execute("DROP TABLE IF EXISTS usuario")

    # Código para criar as tabelas
    tabela_usuario = '''
    CREATE TABLE IF NOT EXISTS usuario (
        id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        telefone TEXT NOT NULL,
        email TEXT NOT NULL
    );
    '''
    tabela_pedido = '''
    CREATE TABLE IF NOT EXISTS pedido (
        id_pedido INTEGER PRIMARY KEY AUTOINCREMENT,
        valor_total DECIMAL(10, 2),
        data_pedido DATE,
        status TEXT,
        id_usuario INTEGER,
        FOREIGN KEY (id_usuario) REFERENCES usuario (id_usuario)
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
    cursor.execute(tabela_usuario)
    cursor.execute(tabela_pedido)
    cursor.execute(tabela_servico)
    cursor.execute(tabela_item_pedido)
    conn.commit()

    # Inserindo dados para teste das tabelas
    cursor.execute('''
    INSERT INTO usuario (nome, telefone, email) VALUES ('Alexandre Uihara', '11913767838', 'emailalexandre@gmail.com')
    ''')
    # Criando uma variável para guardar o id do usuario
    id_alexandre = cursor.lastrowid

    cursor.execute('''
    INSERT INTO servico (nome_servico, preco_base) VALUES ('Troca de Zíper', 35.00)
    ''')
    # Criando uma variável para guardar o id do servico
    id_servico = cursor.lastrowid

    cursor.execute('''
        INSERT INTO pedido (valor_total, data_pedido, status, id_usuario) VALUES (35.00, '2026-03-15', 'Finalizado', ?)
    ''', (id_alexandre,))
    # Criando uma variável para guardar o id do pedido
    id_pedido = cursor.lastrowid

    cursor.execute('''
    INSERT INTO item_pedido (quantidade, valor_unitario, id_pedido, id_servico) VALUES (1, 35.00, ?, ?)
    ''', (id_pedido, id_servico))

    conn.commit()

    # Gerando código para mostrar os dados no terminal
    cursor.execute("""
    SELECT u.nome, p.data_pedido, s.nome_servico, p.valor_total
    FROM usuario u
    JOIN pedido p ON u.id_usuario = p.id_usuario
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