'''
    Módulo de indexação de chunks de texto para o processo de RAG.
    Utiliza BM25 para indexação lexical e FAISS com SentenceTransformer para indexação semântica. 
    Os chunks são armazenados em uma lista global e os índices são reconstruídos a cada nova indexação.
    O processo de indexação é detalhado no docstring da função indexar, que explica passo a passo 
    como os textos são processados, tokenizados, agrupados em chunks e indexados.
'''

# ----------------------- IMPORTAÇÕES -----------------------
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

    print(f"\n[INDEXER] Entrada: {len(novos_chunks)} novos chunks")
    for c in novos_chunks:
        print(f"  [{c['id']}] [{c['source']}] {c['texto'][:60]}")

    chunks_globais.extend(novos_chunks)

    # BM25
    print(f"[INDEXER] Ferramenta: BM25Okapi | Reconstruindo índice lexical...")
    corpus_tokenizado = [tokenizar(c["texto"]) for c in chunks_globais]
    indice_bm25 = BM25Okapi(corpus_tokenizado)

    # FAISS
    print(f"[INDEXER] Ferramenta: FAISS + SentenceTransformer | Gerando embeddings...")
    textos = [c["texto"] for c in chunks_globais]
    matriz_emb = modelo_embed.encode(
        textos,
        normalize_embeddings=True,
        show_progress_bar=True,
    ).astype("float32")

    embeddings_globais = matriz_emb
    dim = matriz_emb.shape[1]
    indice_faiss = faiss.IndexFlatIP(dim)
    indice_faiss.add(matriz_emb)

    print(f"[INDEXER] Saída: índice atualizado com {len(chunks_globais)} chunks totais | dim={dim}")
