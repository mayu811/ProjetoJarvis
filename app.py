from flask import Flask, render_template, request, jsonify
from pathlib import Path
import os
import sys

sys.path.insert(0, '.')

from src.backend.db.database import inicializar_banco
from src.backend.rag.converter import converter_para_markdown
from src.backend.rag.chunker import chunking_paragrafo
from src.backend.rag.indexer import indexar
from src.backend.rag.client import processar_mensagem

inicializar_banco()

app = Flask(__name__,
            template_folder='src/templates',
            static_folder='src/static')

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload():
    arquivo = request.files.get('arquivo')
    if not arquivo:
        return jsonify({'erro': 'Nenhum arquivo enviado'}), 400

    # valida extensão
    extensoes_permitidas = {'.pdf', '.txt', '.docx'}
    extensao = Path(arquivo.filename).suffix.lower()
    if extensao not in extensoes_permitidas:
        return jsonify({'erro': f'Formato {extensao} não suportado'}), 400

    # salva o arquivo
    caminho = f'uploads/{arquivo.filename}'
    os.makedirs('uploads', exist_ok=True)
    arquivo.save(caminho)

    markdown = converter_para_markdown(caminho)
    chunks = chunking_paragrafo(markdown)
    indexar(chunks)

    return jsonify({
        'mensagem': f'{arquivo.filename} indexado com sucesso!',
        'chunks': len(chunks)
    })    


@app.route('/chat', methods=['POST'])
def chat():
    dados = request.get_json()
    mensagem = dados.get('mensagem')
    resposta = processar_mensagem(mensagem)    
    return jsonify({'resposta': resposta})

if __name__ == '__main__':
    app.run(debug=True)