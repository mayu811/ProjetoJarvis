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
def recuperar_hibrido(
        pergunta: str, 
        k: int = 5, 
        alpha: float = 0.5, 
        max_por_source: int = 2) -> list:
    """
    Combina BM25 e semântico.
    alpha = peso do semântico (0 = só BM25, 1 = só semântico, 0.5 = padrão)
    max_por_source = limita quantos chunks podem vir da mesma fonte para garantir diversidade
    
     - pergunta: string com a pergunta do usuário
     - k: número total de chunks a recuperar
     - alpha: peso do semântico na combinação dos scores
     - max_por_source: número máximo de chunks que podem ser retornados da mesma fonte
     - Retorna: lista de dicionários com os chunks mais relevantes, cada um contendo 'id', 'texto', 'source' e 'score'
    """

    print(f"\n[RETRIEVER] Entrada: pergunta='{pergunta}' | k={k} | alpha={alpha} | max_por_source={max_por_source}")
    print(f"[RETRIEVER] Ferramenta: FAISS + BM25Okapi (híbrido)")

    total_chunks = len(indexer.chunks_globais)

    if total_chunks == 0:
        print("[RETRIEVER] Nenhum chunk indexado")
        return []
    
    
    if total_chunks > 200:
        k_faiss = min(100, total_chunks)  # Busca mais chunks
        k_final = min(10, total_chunks)   # Retorna mais resultados
    else:
        k_faiss = min(50, total_chunks)
        k_final = k
    
    print(f"\n[RETRIEVER] Buscando em {total_chunks} chunks | k={k} | alpha={alpha}")
 
    #Gera Embedding (para as perguntas) --------------------------
    q = indexer.modelo_embed.encode([pergunta], normalize_embeddings=True).astype("float32")
    
    # Busca FAISS --------------------------
    #k_search = min(50, len(indexer.chunks_globais))  # busca um número maior para depois filtrar
    k_faiss = min(50, total_chunks)  # busca um número maior para depois filtrar
    scores_dense, indices = indexer.indice_faiss.search(q, k_faiss)

    # Normaliza scores --------------------------
    sd = normalizar(scores_dense[0])

    #BM24 scores --------------------------
    tokens_pergunta = indexer.tokenizar(pergunta)
    scores_bm25_full = indexer.indice_bm25.get_scores(tokens_pergunta)
    sb = normalizar(scores_bm25_full)

    #Combina scores (hibrido)  --------------------------
    score_final = np.zeros(total_chunks)
    for pos, idx in enumerate(indices[0]):
        score_final[idx] = alpha * sd[pos] + (1 - alpha) * sb[idx]


    indices_ordenados = np.argsort(score_final)[::-1]


    #Contadores para prints --------------------------
    docs_finais = []
    sources_count = {}
    
    #  --------------------------
    for idx in indices_ordenados:
        if len(docs_finais) >= k_final:
            break

        chunk = indexer.chunks_globais[idx]
        source = chunk.get("source", "desconhecido")

        if sources_count.get(source, 0) >= max_por_source:
            continue

        docs_finais.append({
            "id": chunk["id"],
            "texto": chunk["texto"],
            "source": source,
            "score": float(score_final[idx])
        })

        sources_count[source] = sources_count.get(source, 0) + 1

    print(f"[RETRIEVER] {len(docs_finais)} chunks")
    for d in docs_finais:
        print(f" - {d['source']} (score: {d['score']:.3f}): {d['texto'][:60]}")
    
    return docs_finais