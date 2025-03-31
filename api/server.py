import os
import sys
from flask import Flask, request, jsonify, send_from_directory
import pandas as pd

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from utils.config import Config

static_folder_path = os.path.join(project_root, 'api', 'static')
app = Flask(__name__, static_folder=static_folder_path)

def carregar_dados_operadoras():
    try:
        filepath = os.path.join(project_root, 'data', 'ans_dados', 'operadoras.csv')
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Arquivo {filepath} não encontrado")
        
        df = pd.read_csv(
            filepath, 
            encoding='latin1', 
            sep=';',
            dtype=str,
            na_values=['', ' '],
            keep_default_na=False
        )
        
        df.columns = (
            df.columns
            .str.strip()
            .str.lower()
            .str.replace(' ', '_')
            .str.normalize('NFKD')
            .str.encode('ascii', errors='ignore')
            .str.decode('utf-8')
        )
        
        df = df.rename(columns={
            'registro_ans': 'registro_ans',
            'razao_social': 'razao_social',
            'nome_fantasia': 'nome_fantasia',
            'cnpj': 'cnpj',
            'modalidade': 'modalidade',
            'uf': 'uf',
            'cidade': 'municipio'
        })

        df = df.dropna(how='all')
        
        return df
    
    except Exception as e:
        print(f"Erro ao carregar dados: {str(e)}")
        raise

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/buscar_operadoras', methods=['GET'])
def buscar_operadoras():
    try:
        termo = request.args.get('termo', '').strip()
        print(f"\n[DEBUG] Recebida requisição de busca. Termo: '{termo}'")
        
        if not termo or len(termo) < 3:
            print("[DEBUG] Termo muito curto ou vazio")
            return jsonify({
                "error": "Termo de busca deve ter pelo menos 3 caracteres",
                "termo_recebido": termo
            }), 400

        df_operadoras = carregar_dados_operadoras()

        print("\nColunas disponíveis no DataFrame:")
        print(df_operadoras.columns.tolist())
        
        colunas_busca = [
            'razao_social',
            'nome_fantasia',
            'cnpj',
            'municipio',
            'uf',
            'modalidade'
        ]

        colunas_busca = [col for col in colunas_busca if col in df_operadoras.columns]

        mask = pd.Series(False, index=df_operadoras.index)
        for col in colunas_busca:
            mask = mask | df_operadoras[col].str.contains(termo, case=False, na=False)
        
        resultados = df_operadoras[mask]

        colunas_relevantes = [
            'registro_ans', 
            'razao_social', 
            'nome_fantasia', 
            'cnpj', 
            'modalidade', 
            'uf', 
            'municipio'
        ]
        
        colunas_relevantes = [col for col in colunas_relevantes if col in resultados.columns]

        resultados = resultados.sort_values(by='razao_social')

        resultados = resultados.head(100)
        
        resultados = resultados.fillna('')
        
        print(f"\nTotal de resultados encontrados: {len(resultados)}")
        if len(resultados) > 0:
            print("\nPrimeiros 3 resultados:")
            print(resultados[colunas_relevantes].head(3).to_string())
        
        resultados_json = resultados[colunas_relevantes].to_dict(orient='records')
        
        return jsonify({
            "total_resultados": len(resultados),
            "resultados": resultados_json,
            "termo_busca": termo
        })
        
    except FileNotFoundError as e:
        return jsonify({"error": "Dados não disponíveis. Arquivo não encontrado."}), 503
    except Exception as e:
        print(f"Erro na busca: {str(e)}")
        return jsonify({
            "error": "Ocorreu um erro interno no servidor",
            "detalhes": str(e)
        }), 500

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    print(f"Static folder path: {static_folder_path}")
    print(f"Contents of static folder: {os.listdir(static_folder_path)}")
    
    try:
        df = carregar_dados_operadoras()
        print(f"\nDados carregados com sucesso. Total de operadoras: {len(df)}")
        print("\nExemplo de dados carregados:")
        print(df[['registro_ans', 'razao_social', 'uf']].head(3).to_string())
    except Exception as e:
        print(f"\nAVISO: Problema ao carregar dados - {str(e)}")
    
    app.run(host='0.0.0.0', port=5000, debug=True)