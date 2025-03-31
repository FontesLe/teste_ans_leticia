import os
import sys
import subprocess
import logging
import signal
from time import sleep
from typing import Optional

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(module)s - %(message)s',
    handlers=[
        logging.FileHandler('ans_tests.log')
    ]
)
logger = logging.getLogger(__name__)

flask_process = None

def run_web_scraping() -> bool:
    try:
        print("\n" + "="*50)
        print("Executando Teste 1 - Web Scraping")
        print("="*50)
        
        from web_scraping.web_scraping import web_scraping_test
        return web_scraping_test()
    except Exception as e:
        logger.error(f"Erro no web scraping: {str(e)}", exc_info=True)
        return False

def run_data_transformation() -> bool:
    try:
        print("\n" + "="*50)
        print("Executando Teste 2 - Transformação de Dados")
        print("="*50)
        
        from data_transformation.data_transformation import transformacao_dados
        return transformacao_dados()
    except Exception as e:
        logger.error(f"Erro na transformação de dados: {str(e)}", exc_info=True)
        return False

def run_database_test() -> bool:
    try:
        print("\n" + "="*50)
        print("Executando Teste 3 - Banco de Dados")
        print("="*50)
        
        from database.database import preparar_dados, criar_banco_dados
        
        if not preparar_dados():
            print("Falha no preparo dos dados")
            return False
        
        return criar_banco_dados()
    except Exception as e:
        logger.error(f"Erro no teste de banco de dados: {str(e)}", exc_info=True)
        return False

def start_flask_server() -> Optional[subprocess.Popen]:
    try:
        process = subprocess.Popen(
            [sys.executable, "api/server.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        sleep(2)
        
        if process.poll() is not None:
            stderr = process.stderr.read()
            print(f"Falha ao iniciar servidor Flask:\n{stderr}")
            return None
        
        print("Servidor Flask iniciado com sucesso")
        return process
    except Exception as e:
        logger.error(f"Erro ao iniciar servidor Flask: {str(e)}", exc_info=True)
        return None

def run_api_test() -> bool:
    global flask_process
    
    try:
        print("\n" + "="*50)
        print("Executando Teste 4 - API")
        print("="*50)
        
        flask_process = start_flask_server()
        if not flask_process:
            return False
        
        print("Acesse a interface em http://localhost:5000/")
        print("Pressione Ctrl+C para encerrar o teste.")
        
        try:
            while flask_process.poll() is None:
                sleep(1)
            
            return True
        except KeyboardInterrupt:
            print("\nEncerrando servidor Flask...")
            return True
    except Exception as e:
        logger.error(f"Erro no teste de API: {str(e)}", exc_info=True)
        return False
    finally:
        stop_flask_server()

def stop_flask_server() -> None:
    global flask_process
    if flask_process:
        try:
            flask_process.terminate()
            flask_process.wait(timeout=5)
            print("Servidor Flask encerrado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao encerrar servidor Flask: {str(e)}")
        finally:
            flask_process = None

def criar_diretorios() -> bool:
    try:
        os.makedirs("data_transformation/data", exist_ok=True)
        os.makedirs("database/dados_ans", exist_ok=True)
        os.makedirs("api/static", exist_ok=True)
        return True
    except Exception as e:
        logger.error(f"Erro ao criar diretórios: {str(e)}", exc_info=True)
        return False

def executar_todos_testes() -> bool:
    resultados = {
        'web_scraping': run_web_scraping(),
        'data_transformation': run_data_transformation(),
        'database': run_database_test(),
        'api': run_api_test()
    }
    
    print("\n" + "="*50)
    print("Resumo da Execução")
    print("="*50)
    for teste, sucesso in resultados.items():
        status = "SUCESSO" if sucesso else "FALHA"
        print(f"{teste.replace('_', ' ').title()}: {status}")
    
    return all(resultados.values())

def main() -> None:
    try:
        signal.signal(signal.SIGINT, lambda s, f: sys.exit(0))
        
        if not criar_diretorios():
            print("Falha ao criar diretórios necessários. Verifique o log.")
            return

        print("Bem-vindo ao Sistema de Testes ANS")
        
        while True:
            print("\nMenu Principal:")
            print("1. Executar Teste Individual")
            print("2. Executar Todos os Testes")
            print("0. Sair")
            
            try:
                escolha = input("Digite sua escolha (0-2): ").strip()
                
                if escolha == "1":
                    menu_testes_individual()
                elif escolha == "2":
                    executar_todos_testes()
                elif escolha == "0":
                    print("Encerrando o programa.")
                    return
                else:
                    print("Opção inválida. Tente novamente.")
                    continue
                
            except KeyboardInterrupt:
                print("\nOperação cancelada pelo usuário.")
                return
    except Exception as e:
        logger.critical(f"Erro fatal: {str(e)}", exc_info=True)
        print("Ocorreu um erro crítico. Verifique o arquivo ans_tests.log para detalhes.")
        sys.exit(1)

def menu_testes_individual() -> None:
    while True:
        print("\nSelecione o teste a executar:")
        print("1. Web Scraping")
        print("2. Transformação de Dados")
        print("3. Banco de Dados")
        print("4. API")
        print("0. Voltar ao menu principal")
        
        try:
            choice = input("Digite sua escolha (0-4): ").strip()
            
            if choice == "1":
                run_web_scraping()
            elif choice == "2":
                run_data_transformation()
            elif choice == "3":
                run_database_test()
            elif choice == "4":
                run_api_test()
            elif choice == "0":
                return
            else:
                print("Opção inválida. Tente novamente.")
                continue
            
            continuar = input("\nDeseja executar outro teste? (s/n): ").lower()
            if continuar != 's':
                return
        
        except KeyboardInterrupt:
            print("\nOperação cancelada pelo usuário.")
            return

if __name__ == "__main__":
    main()