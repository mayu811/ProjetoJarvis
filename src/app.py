from flask import Flask, render_template, request, jsonify
from pathlib import Path
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForCausalLM



app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/chat', methods=['POST'])
async def chat():
    dados = request.get_json()
    mensagem = dados.get('mensagem')
    
    #chama o RAG aqui
    # resposta = seu_rag.processar(mensagem)
    # Simulação de resposta — substitua pelo call da sua API RAG
    resposta = f"Recebi sua mensagem: {mensagem}"

    return jsonify({'resposta': resposta})

if __name__ == '__main__':
    app.run(debug=True)