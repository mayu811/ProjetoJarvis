#chunking por parágrafo

def chunking_paragrafo(texto: str, min_chars: int = 30) -> list[dict]:
    """
    Usa as quebras duplas de linha (\n\n) como separadores naturais.
    Remove parágrafos muito curtos (menos que min_chars caracteres).
    """
    paragrafos = [p.strip() for p in texto.split("\n\n")]
    chunks_filtrados = [p for p in paragrafos if len(p) >= min_chars]

    return [
        {"id": f"chunk_{i:04d}", "texto": texto}
        for i, texto in enumerate(chunks_filtrados)
    ]