"""
main.py

Arquivo de entrada do programa. Ao executar este script, o restante da
aplicação deve ser inicializado (banco de dados, servidor, etc.).
"""

import os
import runpy


def initialize_database():
    """Executa o script de criação/inicialização do banco de dados.

    O código original responsável pela criação do banco está dentro de
    `sqlite_db/import sqlite3.py`. Como esse nome não é um identificador
    válido para importação, usamos `runpy.run_path` para executar o arquivo
    diretamente.
    """
    path = os.path.join(os.path.dirname(__file__), "sqlite_db", "import sqlite3.py")
    if os.path.exists(path):
        print("Inicializando banco de dados...")
        runpy.run_path(path, run_name="__main__")
    else:
        print("Não foi possível encontrar o arquivo de inicialização do banco.")


def start_frontend():
    """Inicia a aplicação Streamlit localizada em `front/app.py`.

    Antes de tentar executar, confirma se o pacote `streamlit` está
    disponível na mesma instalação de Python. Ao disparar o subprocesso
    esperamos pela abertura do `localhost:8501` usando um socket; só então
    o navegador é aberto. Isso evita o erro `ERR_CONNECTION_REFUSED` caso o
    servidor demore mais para ficar pronto.
    """
    import subprocess
    import sys
    import time
    import webbrowser
    import socket

    # verificar instalação do streamlit
    try:
        import streamlit  # noqa: F401
    except ImportError:
        print("Pacote 'streamlit' não está instalado. Rode 'pip install streamlit'.")
        return

    path = os.path.join(os.path.dirname(__file__), "front", "app.py")
    if not os.path.exists(path):
        print("Arquivo de frontend não encontrado, verifique 'front/app.py'.")
        return

    print("Iniciando frontend Streamlit...")
    # executar em modo headless para evitar que o próprio Streamlit abra o navegador
    proc = subprocess.Popen([sys.executable, "-m", "streamlit", "run", path,
                              "--server.headless", "true"])

    # aguardar servidor aceitar conexões na porta padrão
    url = "http://localhost:8501"
    timeout = 10
    deadline = time.time() + timeout
    while time.time() < deadline:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            result = sock.connect_ex(("localhost", 8501))
            if result == 0:
                break
        time.sleep(0.5)
    else:
        print(f"Servidor Streamlit não respondeu após {timeout}s; verifique logs.")
        return

    try:
        webbrowser.open(url, new=2)
        print(f"Navegador aberto em {url}")
    except Exception as exc:
        print("Não foi possível abrir o navegador automaticamente:", exc)


def main():
    print("Programa iniciado")
    # inicialização do banco de dados
    initialize_database()
    # iniciar o frontend em Streamlit
    start_frontend()
    # outras inicializações futuras podem ir aqui


if __name__ == "__main__":
    main()
