#chunking por parágrafo para impedir que informações sofram de cortes abruptos perdendo o contexto da mensagem

def chunking_paragrafo(texto: str, source: str = "desconhecido", min_chars: int = 30,
                       chunk_size: int = 500, overlap: int = 80) -> list[dict]:
    """
    Divide o texto em chunks por parágrafo, com limite de tamanho e overlap.
    - min_chars: ignora parágrafos muito curtos
    - chunk_size: tamanho máximo de cada chunk em caracteres
    - overlap: quantos caracteres do chunk anterior são repetidos no próximo

    Passos ========================================================:
        Texto original
                ↓
        Separação por parágrafos
                ↓
        Remoção de parágrafos curtos
                ↓
        Agrupamento até chunk_size
                ↓
        Aplicação de overlap
                ↓
        Criação de IDs e metadados
                ↓
        Lista final de chunks
    ================================================================
    """
    print(f"\n[CHUNKER] Entrada: source='{source}' | min_chars={min_chars} | chunk_size={chunk_size} | overlap={overlap}")

    #separação de paragrafos, removendo espaços em branco e ignorando os muito curtos
    paragrafos = [p.strip() for p in texto.split("\n\n")]
    paragrafos = [p for p in paragrafos if len(p) >= min_chars]


    # agrupamento dos parágrafos em chunks respeitando o limite de tamanho e aplicando overlap
    chunks = []
    chunk_atual = ""

    for paragrafo in paragrafos:
        if len(chunk_atual) + len(paragrafo) > chunk_size and chunk_atual:
            chunks.append(chunk_atual.strip())
            # Pega os últimos caracteres do chunk anterior para o overlap e inicia o próximo chunk com eles
            chunk_atual = chunk_atual[-overlap:] + "\n\n" + paragrafo
        else:
            chunk_atual += "\n\n" + paragrafo if chunk_atual else paragrafo

    # se sobrou algum texto no chunk_atual após o loop, adiciona como último chunk
    if chunk_atual.strip():
        chunks.append(chunk_atual.strip())

    # criação da estrutura final de chunks com IDs e metadados
    resultado = [
        {
            "id": f"chunk_{i:04d}",
            "texto": texto,
            "source": source
        }
        for i, texto in enumerate(chunks)
    ]

    print(f"[CHUNKER] Saída: {len(resultado)} chunks gerados de '{source}'")

    return resultado