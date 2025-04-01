import psycopg2
from dotenv import load_dotenv
import os
import time

load_dotenv()

def testar_conexao():
    print("🔍 Iniciando teste de conexão com o PostgreSQL no Render...")
    
    config = {
        'host': os.getenv('DB_HOST'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'dbname': os.getenv('DB_NAME'),
        'port': os.getenv('DB_PORT'),
        'connect_timeout': 5,
        'sslmode': 'require'
    }

    print("\n🔧 Configuração usada:")
    print(f"Host: {config['host']}")
    print(f"User: {config['user']}")
    print(f"Database: {config['dbname']}")
    print(f"Port: {config['port']}")
    print(f"SSL: {config['sslmode']}")

    try:
        print("\n🔄 Tentando conectar...")
        inicio = time.time()
        
        conn = psycopg2.connect(**config)
        cursor = conn.cursor()
        
        cursor.execute("SELECT 1")
        resultado = cursor.fetchone()
        
        tempo = time.time() - inicio
        print(f"✅ Conexão bem-sucedida! (Tempo: {tempo:.2f}s)")
        print(f"Resposta do banco: {resultado[0]}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print("\n❌ Falha na conexão:")
        print(f"Tipo do erro: {type(e).__name__}")
        print(f"Mensagem: {str(e)}")
        
        print("\n🔧 Possíveis soluções:")
        if "connection timeout" in str(e):
            print("1. Aumente o 'connect_timeout' para 30")
            print("2. Verifique se o IP está liberado no Render")
        elif "password authentication" in str(e):
            print("1. Verifique usuário/senha no painel do Render")
            print("2. Confira se a senha tem caracteres especiais")
        elif "does not exist" in str(e):
            print("1. O nome do banco está correto?")
            print("2. Verifique em 'Database Info' no Render")
        else:
            print("1. Teste manualmente com:")
            print(f"   psql -h {config['host']} -U {config['user']} -d {config['dbname']}")
        
        return False

if __name__ == "__main__":
    testar_conexao()