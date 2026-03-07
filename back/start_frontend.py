import subprocess
import sys
import time
import webbrowser
import socket
import os


def start_frontend():
    """Inicia a aplicação Streamlit localizada em `front/app.py`.

    Essa função era originalmente definida em `main.py`; aqui ela vive no
    pacote `back` para manter o comportamento de "backend" fora do módulo
    de inicialização principal.  O código não foi alterado além de ajustar
    caminhos relativos.
    """
    # verificar instalação do streamlit
    try:
        import streamlit  # noqa: F401
    except ImportError:
        print("Pacote 'streamlit' não está instalado. Rode 'pip install streamlit'.")
        return

    base = os.path.dirname(os.path.dirname(__file__))  # diretorio raiz do projeto
    path = os.path.join(base, "front", "app.py")
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
