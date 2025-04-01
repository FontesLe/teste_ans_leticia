import os
import requests
from bs4 import BeautifulSoup
import zipfile
from urllib.parse import urljoin
import traceback
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
RAW_DIR = os.path.join(DATA_DIR, 'raw')
PROCESSED_DIR = os.path.join(DATA_DIR, 'processed')

def create_directories():
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    print(f"Diretórios criados em: {DATA_DIR}")

def download_file(url, save_path):
    try:
        print(f"Baixando {os.path.basename(save_path)}...")
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"Arquivo salvo em: {save_path}")
        return True
    except Exception as e:
        print(f"Erro ao baixar {url}: {str(e)}")
        return False

def compress_files(file_paths, zip_path):
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in file_paths:
                if os.path.exists(file):
                    arcname = os.path.basename(file)
                    zipf.write(file, arcname)
                    print(f"Compactado: {arcname}")
                else:
                    print(f"Aviso: Arquivo {file} não existe")
        
        print(f"Arquivo ZIP criado em: {zip_path}")
        return True
    except Exception as e:
        print(f"Erro ao compactar arquivos: {str(e)}")
        return False

def find_attachment(soup, keywords):
    attachments = soup.select('a[href$=".pdf"], a[href$=".xlsx"], a[href$=".csv"]')
    for a in attachments:
        href = a['href']
        text = a.get_text().strip().lower()
        if any(keyword.lower() in text for keyword in keywords):
            return urljoin(base_url, href)
    return None

def clean_filename(filename):
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename.strip()

def web_scraping_test():
    try:
        create_directories()
        
        global base_url
        base_url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
        print(f"\nAcessando o site: {base_url}")
        
        response = requests.get(base_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        print("Procurando pelos Anexos I e II...")
        
        anexo_i_url = find_attachment(soup, ['Anexo I', 'Rol de Procedimentos'])
        anexo_ii_url = find_attachment(soup, ['Anexo II', 'Diretrizes de Utilização'])
        
        if not anexo_i_url:
            print("\nAviso: Não foi possível encontrar o link do Anexo I")
        if not anexo_ii_url:
            print("Aviso: Não foi possível encontrar o link do Anexo II")
        
        if not anexo_i_url and not anexo_ii_url:
            raise Exception("Nenhum dos anexos foi encontrado")
        
        print("\nLinks encontrados:")
        if anexo_i_url:
            print(f"- Anexo I: {anexo_i_url}")
        if anexo_ii_url:
            print(f"- Anexo II: {anexo_ii_url}")
        
        downloaded_files = []
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if anexo_i_url:
            filename = clean_filename(f"Anexo_I_{timestamp}.pdf")
            anexo_i_path = os.path.join(RAW_DIR, filename)
            if download_file(anexo_i_url, anexo_i_path):
                downloaded_files.append(anexo_i_path)
                print("\nDownload do Anexo I concluído com sucesso")
        
        if anexo_ii_url:
            filename = clean_filename(f"Anexo_II_{timestamp}.pdf")
            anexo_ii_path = os.path.join(RAW_DIR, filename)
            if download_file(anexo_ii_url, anexo_ii_path):
                downloaded_files.append(anexo_ii_path)
                print("Download do Anexo II concluído com sucesso")
        
        if downloaded_files:
            zip_filename = f"Teste_leticia_{timestamp}.zip"
            zip_path = os.path.join(PROCESSED_DIR, zip_filename)
            if compress_files(downloaded_files, zip_path):
                print(f"\nProcesso concluído! Arquivos disponíveis em:")
                print(f"- PDFs: {RAW_DIR}")
                print(f"- ZIP: {zip_path}")
                return True
        
        print("\nNenhum arquivo foi baixado com sucesso")
        return False
    
    except requests.exceptions.RequestException as e:
        print(f"\nErro de conexão: {str(e)}")
        return False
    except Exception as e:
        print(f"\nErro durante o web scraping: {str(e)}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = web_scraping_test()
    if not success:
        print("\nFalha no processo de web scraping. Verifique os logs acima.")
        exit(1)