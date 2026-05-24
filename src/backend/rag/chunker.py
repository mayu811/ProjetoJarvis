#chunking por parágrafo


def chunking_paragrafo(texto: str, source: str = "desconhecido", min_chars: int = 30, 
                       chunk_size: int = 500, overlap: int = 80) -> list[dict]:
    """
    Divide o texto em chunks por parágrafo, com limite de tamanho e overlap.
    - min_chars: ignora parágrafos muito curtos
    - chunk_size: tamanho máximo de cada chunk em caracteres
    - overlap: quantos caracteres do chunk anterior são repetidos no próximo
    """
    # divide por parágrafo
    paragrafos = [p.strip() for p in texto.split("\n\n")]
    paragrafos = [p for p in paragrafos if len(p) >= min_chars]

    chunks = []
    chunk_atual = ""

    for paragrafo in paragrafos:
        # se adicionar o parágrafo ultrapassar o limite
        if len(chunk_atual) + len(paragrafo) > chunk_size and chunk_atual:
            chunks.append(chunk_atual.strip())
            # overlap: começa o próximo chunk com o final do anterior
            chunk_atual = chunk_atual[-overlap:] + "\n\n" + paragrafo
        else:
            chunk_atual += "\n\n" + paragrafo if chunk_atual else paragrafo

    # adiciona o último chunk
    if chunk_atual.strip():
        chunks.append(chunk_atual.strip())

    return [
        {
            "id": f"chunk_{i:04d}",
            "texto": texto,
            "source": source
        }
        for i, texto in enumerate(chunks)
    ]