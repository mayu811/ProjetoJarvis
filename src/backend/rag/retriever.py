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

def recuperar_hibrido(pergunta, k=3, alpha=0.6):
    """
    Combina BM25 e semântico.
    alpha = peso do semântico (0 = só BM25, 1 = só semântico, 0.6 = padrão)
    """
    sb = normalizar(indexer.indice_bm25.get_scores(indexer.tokenizar(pergunta)))

    q = indexer.modelo_embed.encode([pergunta], normalize_embeddings=True).astype("float32")

    # matriz_emb reconstruída a partir dos chunks indexados
    matriz_emb = indexer.modelo_embed.encode(
        [c["texto"] for c in indexer.chunks_globais],
        normalize_embeddings=True
    ).astype("float32")

    sd = normalizar(np.dot(matriz_emb, q[0]))
    score_final = alpha * sd + (1.0 - alpha) * sb
    idx = np.argsort(score_final)[::-1][:k]

    return [
        {"id": indexer.chunks_globais[i]["id"], "texto": indexer.chunks_globais[i]["texto"], "score": float(score_final[i])}
        for i in idx
    ]
