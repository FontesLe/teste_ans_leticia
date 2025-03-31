import os
import pandas as pd
import warnings
from typing import List, Union, Tuple
import zipfile

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
RAW_DIR = os.path.join(DATA_DIR, 'raw') 
PROCESSED_DIR = os.path.join(DATA_DIR, 'processed')

class PDFExtractor:
    @staticmethod
    def extract_with_tabula(pdf_path: str) -> Union[List[pd.DataFrame], None]:
        try:
            import tabula
            print("Tentando extração com tabula-py...")
            tables = tabula.read_pdf(
                pdf_path,
                pages='all',
                multiple_tables=True,
                lattice=True,
                pandas_options={'header': None},
                silent=True
            )
            return [table for table in tables if not table.empty]
        except Exception as e:
            warnings.warn(f"Falha no tabula-py: {str(e)}")
            return None

    @staticmethod
    def extract_with_pdfplumber(pdf_path: str) -> Union[List[pd.DataFrame], None]:
        try:
            import pdfplumber
            print("Tentando extração com pdfplumber...")
            tables = []
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    table = page.extract_table()
                    if table and len(table) > 1:
                        tables.append(pd.DataFrame(table[1:], columns=table[0]))
            return tables
        except Exception as e:
            warnings.warn(f"Falha no pdfplumber: {str(e)}")
            return None

    @staticmethod
    def extract_tables(pdf_path: str) -> Tuple[List[pd.DataFrame], str]:
        methods = [
            ('tabula', PDFExtractor.extract_with_tabula),
            ('pdfplumber', PDFExtractor.extract_with_pdfplumber)
        ]
        
        for method_name, method_func in methods:
            try:
                tables = method_func(pdf_path)
                if tables and any(not df.empty for df in tables):
                    return tables, method_name
            except ImportError:
                continue
                
        return [], "none"

def transformacao_dados():
    try:
        pdf_path = os.path.join(RAW_DIR, "Anexo_I.pdf")
        csv_path = os.path.join(PROCESSED_DIR, "Rol_Procedimentos.csv")
        zip_path = os.path.join(PROCESSED_DIR, "Teste_leticia.zip")
        
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(
                f"ARQUIVO NÃO ENCONTRADO: {pdf_path}\n"
                "Solução: Execute primeiro o Teste 1 (Web Scraping) para baixar o Anexo_I.pdf"
            )

        print("\nIniciando extração de tabelas do Anexo I...")
        tables, method_used = PDFExtractor.extract_tables(pdf_path)
        print(f"Extraídas {len(tables)} tabelas com {method_used}")
        
        if not tables:
            raise ValueError("Nenhuma tabela válida encontrada no PDF")

        df = pd.concat(tables, ignore_index=True)

        df.columns = [
            str(col).replace('OD', 'Odontológico')
                   .replace('AMB', 'Ambulatorial') 
            for col in df.columns
        ]

        os.makedirs(PROCESSED_DIR, exist_ok=True)
        df.to_csv(csv_path, index=False, sep=';', encoding='utf-8-sig')
        print(f"CSV salvo em: {csv_path}")

        with zipfile.ZipFile(zip_path, 'w') as zipf:
            zipf.write(csv_path, os.path.basename(csv_path))
        print(f"Arquivo ZIP criado: {zip_path}")

        return True

    except Exception as e:
        print(f"\nERRO: {str(e)}")
        print("\nSOLUÇÕES POSSÍVEIS:")
        print("1. Execute primeiro o Teste 1 (Web Scraping) para baixar os arquivos")
        print(f"2. Verifique se o arquivo 'Anexo_I.pdf' está em: {RAW_DIR}")
        print("3. Instale os requisitos: pip install tabula-py pdfplumber pandas")
        if "tabula" in str(e):
            print("4. Para tabula-py, instale Java 8+ (https://java.com/download)")
        return False

if __name__ == "__main__":
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    
    print("\n==================================================")
    print("Executando Teste 2 - Transformação de Dados")
    print("==================================================")
    
    if transformacao_dados():
        print("\n✅ Teste 2 concluído com sucesso!")
        print(f"Arquivos gerados em: {PROCESSED_DIR}")
    else:
        print("\n❌ Falha no Teste 2. Verifique as mensagens acima.")