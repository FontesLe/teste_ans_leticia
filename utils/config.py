import os
from typing import Dict

class Config:
    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    WEB_SCRAPING_DIR = os.path.join(BASE_DIR, "web_scraping")
    ANEXOS_DIR = os.path.join(WEB_SCRAPING_DIR, "anexos")
    
    DATA_TRANSFORMATION_DIR = os.path.join(BASE_DIR, "data_transformation")
    DATA_DIR = os.path.join(DATA_TRANSFORMATION_DIR, "data")
    
    DATABASE_DIR = os.path.join(BASE_DIR, "database")
    DADOS_ANS_DIR = os.path.join(DATABASE_DIR, "dados_ans")
    
    API_DIR = os.path.join(BASE_DIR, "api")
    
    DB_CONFIG: Dict[str, str] = {
        'host': 'localhost',
        'user': 'root',
        'password': 'le123456',
        'database': 'ans_db',
        'charset': 'utf8mb4',
        'collation': 'utf8mb4_unicode_ci'
    }
    
    @classmethod
    def get_db_uri(cls, db_type: str = 'mysql') -> str:
        if db_type == 'mysql':
            return (f"mysql+mysqlconnector://{cls.DB_CONFIG['user']}:{cls.DB_CONFIG['password']}"
                    f"@{cls.DB_CONFIG['host']}:3306/{cls.DB_CONFIG['database']}"
                    f"?charset={cls.DB_CONFIG['charset']}")
        elif db_type == 'postgresql':
            return f"postgresql://{cls.DB_CONFIG['user']}:{cls.DB_CONFIG['password']}@{cls.DB_CONFIG['host']}:5432/{cls.DB_CONFIG['database']}"
        else:
            raise ValueError(f"Tipo de banco de dados não suportado: {db_type}")

    @classmethod
    def criar_diretorios(cls):
        os.makedirs(cls.WEB_SCRAPING_DIR, exist_ok=True)
        os.makedirs(cls.ANEXOS_DIR, exist_ok=True)
        os.makedirs(cls.DATA_TRANSFORMATION_DIR, exist_ok=True)
        os.makedirs(cls.DATA_DIR, exist_ok=True)
        os.makedirs(cls.DATABASE_DIR, exist_ok=True)
        os.makedirs(cls.DADOS_ANS_DIR, exist_ok=True)
        os.makedirs(cls.API_DIR, exist_ok=True)