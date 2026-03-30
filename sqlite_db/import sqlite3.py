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

    # Garantir que a coluna status exista em bases antigas
    cursor.execute("PRAGMA table_info(cliente)")
    columns = [row[1] for row in cursor.fetchall()]
    if 'status' not in columns:
        cursor.execute("ALTER TABLE cliente ADD COLUMN status INTEGER DEFAULT 1")
        conn.commit()
        print("Coluna 'status' adicionada à tabela 'cliente'.")

    # Garantir que a coluna observacoes exista em versões antigas do pedido
    cursor.execute("PRAGMA table_info(pedido)")
    pedido_columns = [row[1] for row in cursor.fetchall()]
    if 'observacoes' not in pedido_columns:
        cursor.execute("ALTER TABLE pedido ADD COLUMN observacoes TEXT")
        conn.commit()
        print("Coluna 'observacoes' adicionada à tabela 'pedido'.")

    # Inserir serviços padrão se ainda não existirem
    default_services = [
        ('Ajuste Cós ou Gancho', 20.00),
        ('Ajuste Lateral (inteira)', 25.00),
        ('Ajuste Lateral (pernas)', 20.00),
        ('Barra (à máquina, à mão ou original)', 20.00),
        ('Barra (com zíper lateral)', 40.00),
        ('Cerzir', 15.00),
        ('Joelheira (infantil)', 15.00),
        ('Pregar Botão', 8.00),
        ('Troca de Zíper', 20.00),
        ('Trocar Elástico', 15.00),
        ('Ajuste Altura', 25.00),
        ('Ajuste de Mangas (com zíper)', 40.00),
        ('Ajuste Mangas', 20.00),
        ('Forrar ou Trocar o Forro', 70.00),
        ('Ajuste Lateral', 25.00),
        ('Ajuste Ombro', 20.00),
        ('Barra à Máquina ou Mão (de festa)', 30.00),
        ('Barra à Máquina ou Mão (simples)', 20.00),
        ('Ajuste Lados E Cós', 25.00),
        ('Forrar (Saia Sem Forro)', 30.00),
        ('Ajustar Lados', 20.00),
        ('Barra (subir altura)', 15.00),
        ('Cerzir', 10.00),
        ('Subir Mangas', 10.00),
        ('Ajustar Mangas Com Punhos', 20.00),
        ('Ajustar Punhos Manga Com Virola', 15.00),
        ('Apertar Lados', 20.00),
        ('Barra (à máquina)', 15.00),
        ('Trocar / Colocar botões', 10.00),
        ('Virar Gola', 15.00),
        ('Barra Cortinas (pequena)', 40.00),
        ('Barra Lençol', 20.00),
        ('Capa de Edredons (não incluso tecido)', 35.00),
        ('Elástico Lençol (casal)', 25.00),
        ('Elástico Lençol (solteiro)', 20.00),
        ('Cerzir Toalhas de Mesa', 10.00),
        ('Barra Toalhas De Mesa', 10.00),
        ('Pano Americano (não incluso tecido)', 20.00)
    ]
    cursor.execute("SELECT nome_servico FROM servico")
    existing = {row[0] for row in cursor.fetchall()}
    inserted = 0
    for nome_servico, preco_base in default_services:
        if nome_servico not in existing:
            cursor.execute(
                "INSERT INTO servico (nome_servico, preco_base) VALUES (?, ?)",
                (nome_servico, preco_base)
            )
            inserted += 1
    if inserted:
        conn.commit()
        print(f"{inserted} serviços padrão inseridos na tabela 'servico'.")

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