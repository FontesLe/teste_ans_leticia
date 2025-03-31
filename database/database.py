import os
import requests
import pandas as pd
from sqlalchemy import create_engine, text, exc
import mysql.connector
from mysql.connector import Error
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging
from tqdm import tqdm
import zipfile
from io import BytesIO

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ans_import.log'),
        logging.StreamHandler()
    ]
)

class DatabaseManager:
    def __init__(self):
        self.base_url = "https://dadosabertos.ans.gov.br/FTP/PDA/"
        self.selected_years = ['2023', '2024']
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'ans_dados')
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'le123456',
            'database': 'ans_dados_abertos',
            'auth_plugin': 'mysql_native_password',
            'connect_timeout': 600,
            'charset': 'utf8mb4'
        }
        self.batch_size = 5000
        self.engine = self._create_engine()

    def _create_database_if_not_exists(self):
        try:
            conn = mysql.connector.connect(
                host=self.db_config['host'],
                user=self.db_config['user'],
                password=self.db_config['password']
            )
            cursor = conn.cursor()
            
            cursor.execute(f"SHOW DATABASES LIKE '{self.db_config['database']}'")
            result = cursor.fetchone()
            
            if not result:
                cursor.execute(f"CREATE DATABASE {self.db_config['database']} "
                              f"CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                conn.commit()
                logging.info(f"Banco de dados {self.db_config['database']} criado com sucesso")
            
            cursor.close()
            conn.close()
        except Error as e:
            logging.error(f"Erro ao verificar/criar banco de dados: {str(e)}")
            raise

    def _create_engine(self):
        try:
            self._create_database_if_not_exists()
            
            engine = create_engine(
                f"mysql+mysqlconnector://{self.db_config['user']}:{self.db_config['password']}@"
                f"{self.db_config['host']}/{self.db_config['database']}?"
                f"charset={self.db_config['charset']}",
                connect_args={
                    'auth_plugin': self.db_config['auth_plugin'],
                    'connect_timeout': self.db_config['connect_timeout']
                },
                pool_size=5,
                pool_recycle=3600,
                echo=True 
            )
            
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            return engine
        except Exception as e:
            logging.error(f"Erro ao criar engine do banco de dados: {str(e)}")
            raise

    def preparar_dados(self):
        try:
            self._setup_directories()
            
            operadoras_url = f"{self.base_url}operadoras_de_plano_de_saude_ativas/Relatorio_cadop.csv"
            operadoras_path = os.path.join(self.data_dir, "operadoras.csv")
            
            if not self._download_file(operadoras_url, operadoras_path):
                logging.error("Falha ao baixar dados das operadoras")
                return False
            
            success_count = 0
            for year in self.selected_years:
                available_files = self._get_available_files(year)
                for file_url in available_files:
                    filename = file_url.split('/')[-1]
                    save_path = os.path.join(self.data_dir, filename)
                    if self._download_file(file_url, save_path):
                        success_count += 1
            
            logging.info(f"Download concluído: {success_count} arquivos baixados")
            return success_count > 0
            
        except Exception as e:
            logging.error(f"Erro ao preparar dados: {str(e)}")
            return False

    def _setup_directories(self):
        os.makedirs(self.data_dir, exist_ok=True)
        logging.info(f"Diretório de dados: {self.data_dir}")

    def _download_file(self, url, save_path):
        try:
            logging.info(f"Baixando {url.split('/')[-1]}...")
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, stream=True, timeout=30)
            response.raise_for_status()
            
            if url.endswith('.zip'):
                with zipfile.ZipFile(BytesIO(response.content)) as zip_ref:
                    zip_ref.extractall(os.path.dirname(save_path))
                logging.info(f"Arquivo ZIP extraído em: {os.path.dirname(save_path)}")
            else:
                with open(save_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                logging.info(f"Arquivo salvo em: {save_path}")
            
            return True
        except Exception as e:
            logging.error(f"Erro ao baixar arquivo: {str(e)}")
            return False

    def _get_available_files(self, year):
        available_files = []
        year_url = f"{self.base_url}demonstracoes_contabeis/{year}/"
        
        try:
            logging.info(f"Buscando arquivos para {year}...")
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(year_url, headers=headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            for link in soup.find_all('a'):
                href = link.get('href')
                if href and href.endswith('.zip') and any(q in href for q in ['1T', '2T', '3T', '4T']):
                    full_url = urljoin(year_url, href)
                    available_files.append(full_url)
                    logging.info(f"Encontrado: {href}")
        
        except Exception as e:
            logging.error(f"Erro ao buscar arquivos: {str(e)}")
        
        return available_files

    def criar_banco_dados(self):
        try:
            logging.info("Iniciando criação do banco de dados...")
            
            if not self._criar_estrutura():
                return False

            if not self._importar_operadoras():
                return False
   
            if not self._importar_demonstracoes():
                return False
                
            logging.info("Banco de dados criado com sucesso!")
            return True
            
        except Exception as e:
            logging.error(f"Erro ao criar banco de dados: {str(e)}")
            return False

    def _criar_estrutura(self):
        try:
            with self.engine.begin() as conn:
                existing_tables = conn.execute(text(
                    "SHOW TABLES LIKE 'operadoras'"
                )).fetchone()
                
                if existing_tables:
                    logging.warning("Tabelas já existem no banco de dados")
                    return True

                conn.execute(text("SET FOREIGN_KEY_CHECKS=0"))

                conn.execute(text("""
                CREATE TABLE IF NOT EXISTS operadoras (
                    registro_ans VARCHAR(20) PRIMARY KEY,
                    cnpj VARCHAR(20),
                    razao_social VARCHAR(255) NOT NULL,
                    nome_fantasia VARCHAR(255),
                    modalidade VARCHAR(100),
                    logradouro VARCHAR(255),
                    numero VARCHAR(20),
                    complemento VARCHAR(100),
                    bairro VARCHAR(100),
                    cidade VARCHAR(100),
                    uf CHAR(2),
                    cep VARCHAR(10),
                    ddd VARCHAR(5),
                    telefone VARCHAR(20),
                    fax VARCHAR(20),
                    endereco_eletronico VARCHAR(100),
                    representante VARCHAR(255),
                    cargo_representante VARCHAR(100),
                    regiao_de_comercializacao VARCHAR(20),
                    data_registro_ans DATE
                ) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
                """))
                
                conn.execute(text("""
                CREATE TABLE IF NOT EXISTS demonstracoes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    registro_ans VARCHAR(20) NOT NULL,
                    data DATE NOT NULL,
                    cd_conta_contabil VARCHAR(50) NOT NULL,
                    descricao VARCHAR(255),
                    vl_saldo_inicial DECIMAL(15,2),
                    vl_saldo_final DECIMAL(15,2),
                    periodo VARCHAR(10) NOT NULL,
                    FOREIGN KEY (registro_ans) REFERENCES operadoras(registro_ans),
                    INDEX idx_periodo (periodo),
                    INDEX idx_conta (cd_conta_contabil)
                ) ENGINE=InnoDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
                """))
                
                conn.execute(text("SET FOREIGN_KEY_CHECKS=1"))
            
            logging.info("Estrutura do banco criada com sucesso")
            return True
        except Exception as e:
            logging.error(f"Erro ao criar estrutura: {str(e)}")
            return False

    def _importar_operadoras(self):
        operadoras_path = os.path.join(self.data_dir, "operadoras.csv")
        if not os.path.exists(operadoras_path):
            logging.error("Arquivo de operadoras não encontrado!")
            return False

        try:
            df = pd.read_csv(
                operadoras_path,
                encoding='latin1',
                sep=';',
                dtype=str
            )
            
            df.columns = [col.lower().replace(' ', '_') for col in df.columns]
            
            if 'data_registro_ans' in df.columns:
                df['data_registro_ans'] = pd.to_datetime(
                    df['data_registro_ans'],
                    format='%d/%m/%Y',
                    errors='coerce'
                )
            
            df = df.drop_duplicates(subset=['registro_ans'])
            
            with self.engine.begin() as conn:
                df.to_sql(
                    'operadoras',
                    conn,
                    if_exists='append',
                    index=False,
                    method='multi',
                    chunksize=self.batch_size
                )
            
            logging.info(f"Operadoras importadas: {len(df)} registros")
            return True
            
        except Exception as e:
            logging.error(f"Erro ao importar operadoras: {str(e)}")
            return False

    def _importar_demonstracoes(self):
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT registro_ans FROM operadoras"))
                operadoras_validas = {row[0] for row in result}
 
            arquivos = [
                os.path.join(root, file)
                for root, _, files in os.walk(self.data_dir)
                for file in files 
                if file.endswith('.csv') and any(q in file for q in ['1T', '2T', '3T', '4T'])
            ]
            
            total_importados = 0
            
            for arquivo in tqdm(arquivos, desc="Processando arquivos"):
                try:
                    periodo = self._extrair_periodo(os.path.basename(arquivo))
                    
                    for chunk in pd.read_csv(
                        arquivo,
                        encoding='latin1',
                        sep=';',
                        dtype={'REG_ANS': str, 'CD_CONTA_CONTABIL': str},
                        chunksize=self.batch_size
                    ):
                        chunk.columns = [col.lower().replace(' ', '_') for col in chunk.columns]
                        
                        chunk = chunk[chunk['reg_ans'].isin(operadoras_validas)]
                        
                        if chunk.empty:
                            continue
                            
                        chunk['periodo'] = periodo
                        chunk['data'] = pd.to_datetime(chunk['data'], format='%d/%m/%Y', errors='coerce')
                        chunk = chunk.dropna(subset=['data'])

                        for col in ['vl_saldo_inicial', 'vl_saldo_final']:
                            chunk[col] = (
                                chunk[col].astype(str)
                                .str.replace(r'\.', '', regex=True)
                                .str.replace(',', '.')
                                .replace('', '0')
                                .astype(float)
                            )

                        cols = ['reg_ans', 'data', 'cd_conta_contabil', 
                               'descricao', 'vl_saldo_inicial', 'vl_saldo_final', 'periodo']
                        chunk = chunk[cols].rename(columns={'reg_ans': 'registro_ans'})

                        with self.engine.begin() as conn:
                            chunk.to_sql(
                                'demonstracoes',
                                conn,
                                if_exists='append',
                                index=False,
                                method='multi'
                            )
                        total_importados += len(chunk)
                        
                except Exception as e:
                    logging.error(f"Erro ao processar {arquivo}: {str(e)}")
                    continue
            
            logging.info(f"Demonstrações importadas: {total_importados} registros")
            return True
            
        except Exception as e:
            logging.error(f"Erro ao importar demonstrações: {str(e)}")
            return False

    def _extrair_periodo(self, filename):
        try:
            if '1T' in filename:
                return filename.split('_')[-2] + '_1T'
            elif '2T' in filename:
                return filename.split('_')[-2] + '_2T'
            elif '3T' in filename:
                return filename.split('_')[-2] + '_3T'
            elif '4T' in filename:
                return filename.split('_')[-2] + '_4T'
            return 'desconhecido'
        except:
            return 'desconhecido'

def preparar_dados():
    db = DatabaseManager()
    return db.preparar_dados()

def criar_banco_dados():
    db = DatabaseManager()
    return db.criar_banco_dados()

if __name__ == "__main__":
    logging.info("Iniciando processo de importação...")
    if preparar_dados() and criar_banco_dados():
        logging.info("Processo concluído com sucesso!")
    else:
        logging.error("Ocorreu um erro durante o processo")