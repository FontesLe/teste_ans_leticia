🏥 Buscador de Operadoras ANS - Documentação Completa
<div style="background-color: #f0f8ff; padding: 20px; border-radius: 10px; border-left: 5px solid #2c3e50; margin-bottom: 20px;"> <h2 style="color: #2c3e50; margin-top: 0;">🌟 Tecnologias Utilizadas</h2>
🔧 Backend
<div style="margin-left: 20px; margin-bottom: 15px;"> <div style="display: flex; align-items: center; margin-bottom: 8px;"> <img src="https://img.icons8.com/color/48/000000/python.png" width="20" style="margin-right: 10px;"/> <span><strong>Python 3.8+</strong> - Linguagem principal</span> </div> <div style="display: flex; align-items: center; margin-bottom: 8px;"> <img src="https://img.icons8.com/ios/50/000000/flask.png" width="20" style="margin-right: 10px;"/> <span><strong>Flask 2.0+</strong> - Framework web</span> </div> <div style="display: flex; align-items: center; margin-bottom: 8px;"> <img src="https://img.icons8.com/color/48/000000/postgresql.png" width="20" style="margin-right: 10px;"/> <span><strong>PostgreSQL 12+</strong> - Banco de dados</span> </div> <div style="margin-left: 30px; margin-bottom: 8px;"> • <strong>SQLAlchemy 1.4+</strong> - ORM para banco de dados </div> <div style="margin-left: 30px; margin-bottom: 8px;"> • <strong>Psycopg2 2.9+</strong> - Adaptador PostgreSQL </div> </div>
🎨 Frontend
<div style="margin-left: 20px; margin-bottom: 15px;"> <div style="display: flex; align-items: center; margin-bottom: 8px;"> <img src="https://img.icons8.com/color/48/000000/html-5.png" width="20" style="margin-right: 10px;"/> <span><strong>HTML5</strong> - Estrutura da página</span> </div> <div style="display: flex; align-items: center; margin-bottom: 8px;"> <img src="https://img.icons8.com/color/48/000000/css3.png" width="20" style="margin-right: 10px;"/> <span><strong>CSS3</strong> - Estilização</span> </div> <div style="display: flex; align-items: center; margin-bottom: 8px;"> <img src="https://img.icons8.com/color/48/000000/javascript.png" width="20" style="margin-right: 10px;"/> <span><strong>JavaScript ES6+</strong> - Interatividade</span> </div> <div style="display: flex; align-items: center; margin-bottom: 8px;"> <img src="https://img.icons8.com/color/48/000000/vue-js.png" width="20" style="margin-right: 10px;"/> <span><strong>Vue.js 3.x</strong> - Framework frontend</span> </div> </div>
☁️ Infraestrutura
<div style="margin-left: 20px;"> <div style="display: flex; align-items: center; margin-bottom: 8px;"> <img src="https://img.icons8.com/nolan/64/render.png" width="20" style="margin-right: 10px;"/> <span><strong>Render</strong> - Hospedagem do banco/app</span> </div> <div style="display: flex; align-items: center;"> <img src="https://img.icons8.com/color/48/000000/git.png" width="20" style="margin-right: 10px;"/> <span><strong>Git</strong> - Controle de versão</span> </div> </div> </div>
🚀 Como Executar o Projeto Localmente
📋 Pré-requisitos
<div style="margin-left: 20px; margin-bottom: 15px;"> <div style="display: flex; align-items: center; margin-bottom: 8px;"> <img src="https://img.icons8.com/color/48/000000/python.png" width="20" style="margin-right: 10px;"/> <span>Python 3.8 ou superior</span> </div> <div style="display: flex; align-items: center; margin-bottom: 8px;"> <img src="https://img.icons8.com/color/48/000000/postgresql.png" width="20" style="margin-right: 10px;"/> <span>PostgreSQL 12+ (acesso à instância remota no Render)</span> </div> <div style="display: flex; align-items: center; margin-bottom: 8px;"> <img src="https://img.icons8.com/color/48/000000/nodejs.png" width="20" style="margin-right: 10px;"/> <span>Node.js 14+ (para desenvolvimento frontend)</span> </div> <div style="display: flex; align-items: center; margin-bottom: 8px;"> <img src="https://img.icons8.com/color/48/000000/java-coffee-cup-logo.png" width="20" style="margin-right: 10px;"/> <span>Java JDK 11+ instalado</span> </div> <div style="display: flex; align-items: center;"> <img src="https://img.icons8.com/color/48/000000/git.png" width="20" style="margin-right: 10px;"/> <span>Git instalado</span> </div> </div>
🔧 Configuração do Ambiente
bash
Copy
# 1. Clonar repositório
git clone https://github.com/FontesLe/teste_ans_leticia
cd teste_ans_leticia

# 2. Criar ambiente virtual (Obrigatório)
python -m venv venv

# Ativação:
source venv/bin/activate       # Linux/Mac
.\venv\Scripts\activate       # Windows

# 3. Instalar dependências
pip install -r requirements.txt
🗃️ Configuração do Banco de Dados
O banco já está configurado no Render

Verifique as variáveis de conexão no arquivo .env

🖥️ Executando a Aplicação
bash
Copy
# Iniciar servidor backend
python main.py

# Em outro terminal (para frontend)
cd frontend
npm install
npm run serve
Acesse:

Backend: http://localhost:5000

Frontend: http://localhost:8080

📌 Dicas Importantes
✔ Sempre ative o ambiente virtual antes de trabalhar no projeto
✔ Verifique as variáveis de ambiente no arquivo .env
✔ Para desenvolvimento, use:

bash
Copy
export FLASK_ENV=development  # Linux/Mac
set FLASK_ENV=development    # Windows
📄 Licença
Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.

<div style="text-align: center; margin-top: 30px; padding: 15px; background-color: #f5f5f5; border-radius: 8px;"> <p style="margin-bottom: 10px;">Desenvolvido com ❤️ por <strong>Leticia Fontes</strong></p> <div style="display: flex; justify-content: center; gap: 15px;"> <a href="https://github.com/FontesLe" style="display: flex; align-items: center;"> <img src="https://img.icons8.com/nolan/64/github.png" width="30" style="margin-right: 5px;"/> GitHub </a> <a href="#" style="display: flex; align-items: center;"> <img src="https://img.icons8.com/color/48/000000/linkedin.png" width="30" style="margin-right: 5px;"/> LinkedIn </a> </div> </div>
