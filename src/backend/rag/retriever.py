#recuperação hibrida de trecho relevantes
import numpy as np
import src.backend.rag.indexer as indexer

def normalizar(v):
    """Normaliza um vetor para o intervalo [0, 1]."""
    v = np.array(v, dtype="float32")
    delta = float(v.max() - v.min())
    if delta < 1e-9:
        return np.zeros_like(v)
    return (v - v.min()) / delta


def recuperar_hibrido(pergunta: str, k: int = 10, alpha: float = 0.6, max_por_source: int = 3) -> list:
    q = indexer.modelo_embed.encode([pergunta], normalize_embeddings=True).astype("float32")
    scores_dense, indices_faiss = indexer.indice_faiss.search(q, len(indexer.chunks_globais))

    sd = normalizar(scores_dense[0])
    sb = normalizar(indexer.indice_bm25.get_scores(indexer.tokenizar(pergunta)))

    score_final = alpha * sd + (1.0 - alpha) * sb
    idx = np.argsort(score_final)[::-1]

    # limita chunks por documento
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

    return docs_finais