
# ----------------------- IMPORTAÇÕES ---------------------------
from flask import Flask, render_template, request, jsonify
from pathlib import Path
import os
import sys

# adiciona o diretório raiz do projeto ao sys.path para permitir imports relativos
sys.path.insert(0, '.')

from src.backend.db.database import inicializar_banco
from src.backend.rag.converter import converter_para_markdown
from src.backend.rag.chunker import chunking_paragrafo
from src.backend.rag.indexer import indexar
from src.backend.rag.client import processar_mensagem
import src.backend.rag.indexer as indexer  # importa o módulo para acessar valores atuais
from src.backend.tools.functions import precarregar_documentos

#inicialização do banco:
inicializar_banco()

#precarrega os documentos da pasta dataset para que já estejam disponíveis para consulta assim que o app iniciar
# se não tiver nenhum arquivo carregado no diretório, a função ignorará esse fato
precarregar_documentos('dataset')

app = Flask(__name__,
            template_folder='src/templates',
            static_folder='src/static')

# --------------- ROTAS DO FLASK ---------------

# rota para a página inicial
@app.route('/')
def index():
    return render_template("index.html")


#rota para upload de arquivos e indexação
@app.route('/upload', methods=['POST'])
def upload():
    arquivo = request.files.get('arquivo')
    if not arquivo:
        return jsonify({'erro': 'Nenhum arquivo enviado'}), 400

    # valida extensão
    extensoes_permitidas = {'.pdf', '.txt', '.docx'}
    extensao = Path(arquivo.filename).suffix.lower()

    #se a extensão do arquivo não for permitida, retorna erro
    if extensao not in extensoes_permitidas:
        return jsonify({'erro': f'Formato {extensao} não suportado'}), 400

    # salva o arquivo no diretorio certo
    caminho = f'src/uploads/{arquivo.filename}'
    # garante que a pasta de uploads exista
    os.makedirs('src/uploads', exist_ok=True)
    arquivo.save(caminho)

    # converte para markdown, gera chunks e indexa
    markdown = converter_para_markdown(caminho)
    chunks = chunking_paragrafo(markdown, source=arquivo.filename)
    indexar(chunks)

    return jsonify({
        'mensagem': f'{arquivo.filename} indexado com sucesso!',
        'chunks': len(chunks)
    })    

#rota para processar mensagens do usuário e gerar respostas
@app.route('/chat', methods=['POST'])
def chat():
    dados = request.get_json()
    mensagem = dados.get('mensagem')
    resposta = processar_mensagem(mensagem)    
    return jsonify({'resposta': resposta})

# da run no app Flask em modo debug para facilitar o desenvolvimento
if __name__ == '__main__':
    app.run(debug=True)
