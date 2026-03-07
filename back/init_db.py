import os
import runpy


def initialize_database():
    """Executa o script de criação/inicialização do banco de dados.

    O código original responsável pela criação do banco está localizado em
    `sqlite_db/import sqlite3.py` e era executado diretamente em `main.py`.
    Para manter a lógica de inicialização isolada, movemos para este arquivo.
    """
    base = os.path.dirname(os.path.dirname(__file__))  # diretório raiz do projeto
    path = os.path.join(base, "sqlite_db", "import sqlite3.py")
    if os.path.exists(path):
        print("Inicializando banco de dados...")
        runpy.run_path(path, run_name="__main__")
    else:
        print("Não foi possível encontrar o arquivo de inicialização do banco.")
