
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


#inicialização do banco:
inicializar_banco()

'''

# função que será implementada futuramente...
from src.backend.tools.functions import precarregar_documentos

precarregar_documentos(dataset)

'''


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

@app.route('/debug/chunks', methods=['GET'])
def debug_chunks():
    """Rota para debug - ver chunks indexados"""
    chunks_info = []
    for c in indexer.chunks_globais[:10]:  # só os 10 primeiros
        chunks_info.append({
            'id': c.get('id'),
            'source': c.get('source'),
            'size': len(c.get('texto', '')),
            'preview': c.get('texto', '')[:150]
        })
    
    return jsonify({
        'total_chunks': len(indexer.chunks_globais),
        'faiss_ready': indexer.indice_faiss is not None,
        'bm25_ready': indexer.indice_bm25 is not None,
        'chunks': chunks_info
    })


# da run no app Flask em modo debug para facilitar o desenvolvimento
if __name__ == '__main__':
    app.run(debug=True)
