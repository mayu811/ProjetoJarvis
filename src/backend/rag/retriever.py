'''
    Módulo de recuperação de documentos relevantes para o processo de RAG.
'''

# ---------------------------- IMPORTAÇÕES ----------------------------
import numpy as np
import src.backend.rag.indexer as indexer


# ---------------------------- FUNÇÕES AUXILIARES ----------------------------

# normaliza um vetor para o intervalo [0, 1] - função sigmoide
def normalizar(v):
    """Normaliza um vetor para o intervalo [0, 1]."""
    v = np.array(v, dtype="float32")
    delta = float(v.max() - v.min())
    if delta < 1e-9:
        return np.zeros_like(v)
    return (v - v.min()) / delta

# recuperação híbrida combinando BM25 e semântico
def recuperar_hibrido(pergunta: str, k: int = 15, alpha: float = 0.6, max_por_source: int = 3) -> list:
    """
    Combina BM25 e semântico.
    alpha = peso do semântico (0 = só BM25, 1 = só semântico, 0.6 = padrão)
    max_por_source = limita quantos chunks podem vir da mesma fonte para garantir diversidade
     - pergunta: string com a pergunta do usuário
     - k: número total de chunks a recuperar
     - alpha: peso do semântico na combinação dos scores
     - max_por_source: número máximo de chunks que podem ser retornados da mesma fonte
     - Retorna: lista de dicionários com os chunks mais relevantes, cada um contendo 'id', 'texto', 'source' e 'score'
    """

    print(f"\n[RETRIEVER] Entrada: pergunta='{pergunta}' | k={k} | alpha={alpha} | max_por_source={max_por_source}")
    print(f"[RETRIEVER] Ferramenta: FAISS + BM25Okapi (híbrido)")

    q = indexer.modelo_embed.encode([pergunta], normalize_embeddings=True).astype("float32")
    scores_dense, _ = indexer.indice_faiss.search(q, len(indexer.chunks_globais))

    sd = normalizar(scores_dense[0])
    sb = normalizar(indexer.indice_bm25.get_scores(indexer.tokenizar(pergunta)))

    score_final = alpha * sd + (1.0 - alpha) * sb
    idx = np.argsort(score_final)[::-1]

    docs_finais = []
    sources_count = {}

    for i in idx:
        source = indexer.chunks_globais[i].get("source", "desconhecido")
        if sources_count.get(source, 0) >= max_por_source:
            continue
        docs_finais.append({
            "id": indexer.chunks_globais[i]["id"],
            "texto": indexer.chunks_globais[i]["texto"],
            "source": source,
            "score": float(score_final[i])
        })
        sources_count[source] = sources_count.get(source, 0) + 1
        if len(docs_finais) >= k:
            break

    #
    print(f"[RETRIEVER] {len(docs_finais)} chunks | sources: { {s: c for s, c in sources_count.items()} }")
    
    return docs_finais