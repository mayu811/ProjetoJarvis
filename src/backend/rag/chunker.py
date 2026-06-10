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

    if not paragrafos:
        print(f"[CHUNKER] Aviso: nenhum parágrafo válido em '{source}'")
        return []


    # agrupamento em chunks
    chunks = []
    chunk_atual = ""
    chunk_counter = 0
    '''
    for paragrafo in paragrafos:
        if len(chunk_atual) + len(paragrafo) > chunk_size and chunk_atual:
            chunks.append(chunk_atual.strip())
            # Pega os últimos caracteres do chunk anterior para o overlap e inicia o próximo chunk com eles
            chunk_atual = chunk_atual[-overlap:] + "\n\n" + paragrafo
        else:
            chunk_atual += "\n\n" + paragrafo if chunk_atual else paragrafo
        '''
    for paragrafo in paragrafos:
        # Se adicionar este parágrafo ultrapassar o limite E já temos conteúdo
        if len(chunk_atual) + len(paragrafo) > chunk_size and chunk_atual:
            # Salva chunk atual
            chunks.append(chunk_atual.strip())
            chunk_counter += 1
            # Inicia novo chunk com overlap
            overlap_text = chunk_atual[-overlap:] if len(chunk_atual) > overlap else chunk_atual
            chunk_atual = overlap_text + "\n\n" + paragrafo
        else:
            # Adiciona parágrafo ao chunk atual
            if chunk_atual:
                chunk_atual += "\n\n" + paragrafo
            else:
                chunk_atual = paragrafo
        
    
    # se sobrou algum texto no chunk_atual após o loop, adiciona como último chunk
    if chunk_atual.strip():
        chunks.append(chunk_atual.strip())

    # criação da estrutura final de chunks com IDs e metadados
    resultado = [
        {
            "id": f"{source.replace(' ', '_')}_chunk_{i:04d}",
            "texto": chunk,
            "source": source
        }
        for i, chunk in enumerate(chunks)
    ]

    print(f"[CHUNKER] Gerados {len(resultado)}")
    # prints
    if len(resultado) <= 5:
        for r in resultado:
            print(f"  - {r['id']} | {len(r['texto'][:80])} chars")


    return resultado