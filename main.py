"""
main.py

Arquivo de entrada do programa. Ao executar este script, o restante da
aplicação deve ser inicializado (banco de dados, servidor, etc.).
"""

from back.init_db import initialize_database
from back.start_frontend import start_frontend




def main():
    print("Programa iniciado")
    # inicialização do banco de dados
    initialize_database()
    # iniciar o frontend em Streamlit
    start_frontend()
    # outras inicializações futuras podem ir aqui


if __name__ == "__main__":
    main()
