
# ----------------------- IMPORTAÇÕES ---------------------------
from flask import Flask, render_template, request, jsonify
from pathlib import Path
import os
import sys

from src.backend.db.database import inicializar_banco
from src.backend.rag.converter import converter_para_markdown
from src.backend.rag.chunker import chunking_paragrafo
import src.backend.rag.indexer as indexer
from src.backend.rag.indexer import indexar
from src.backend.rag.client import processar_mensagem

sys.path.insert(0, '.')

#inicialização do banco:
inicializar_banco()

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
    try:
        arquivo = request.files.get('arquivo')

        print(f"[UPLOAD] Arquivo recebido: {arquivo.filename if arquivo else 'Nenhum'}")

        if not arquivo or not arquivo.filename:
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
        try:
            markdown = converter_para_markdown(caminho)
            chunks = chunking_paragrafo(markdown, source=arquivo.filename)
            
            indexar(chunks)
            return jsonify({
                'mensagem': f'{arquivo.filename} indexado com sucesso!',
                'chunks': len(chunks),
                'arquivo': arquivo.filename
            })
        
        except Exception as e:
            print(f"[UPLOAD] ERRO ao processar: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({'erro': f'Erro ao processar arquivo: {str(e)}'}), 500
    
    except Exception as e:
        print(f"[UPLOAD] ERRO GERAL: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'erro': f'Erro no servidor: {str(e)}'}), 500


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
