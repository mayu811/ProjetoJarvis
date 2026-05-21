# indexação hibrida: FAISS + BM25
import re
import faiss
import numpy as np
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer


# carrega o modelo uma única vez ao importar o módulo
modelo_embed = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

# variáveis globais
chunks_globais = []
indice_bm25 = None
indice_faiss = None
embeddings_globais = None

# ── Índice BM25 (lexical) ─────────────────────────────────────────────────────
# Tokeniza cada chunk em lista de palavras (tudo em minúsculo, só alfanumérico)

def tokenizar(texto: str) -> list[str]:
    return re.findall(r"\w+", texto.lower())

def indexar(novos_chunks: list[dict]):
    global chunks_globais, indice_bm25, indice_faiss, embeddings_globais

    

    chunks_globais.extend(novos_chunks)

    # debug temporário — remove depois
    print(f"\n=== CHUNKS INDEXADOS ({len(novos_chunks)} novos) ===")
    for c in novos_chunks:
        print(f"  [{c['id']}] [{c['source']}] {c['texto'][:60]}")

    # reconstrói BM25 com todos os chunks acumulados
    corpus_tokenizado = [tokenizar(c["texto"]) for c in chunks_globais]
    indice_bm25 = BM25Okapi(corpus_tokenizado)

    # reconstrói FAISS com todos os chunks acumulados
    textos = [c["texto"] for c in chunks_globais]
    matriz_emb = modelo_embed.encode(
        textos,
        normalize_embeddings=True,
        show_progress_bar=True,
    ).astype("float32")
    
    #LINHA NOVA ADICIONADA (GPT)
    embeddings_globais = matriz_emb

    dim = matriz_emb.shape[1]
    indice_faiss = faiss.IndexFlatIP(dim)
    indice_faiss.add(matriz_emb)

    print(f"Índice atualizado: {len(chunks_globais)} chunks totais.")