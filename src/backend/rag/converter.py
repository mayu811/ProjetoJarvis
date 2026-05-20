from pathlib import Path
import os
import fitz  # pymupdf
import docx

def converter_para_markdown(caminho_arquivo: str) -> str:
    extensao = Path(caminho_arquivo).suffix.lower()

    if extensao == '.pdf':
        texto = _pdf_para_texto(caminho_arquivo)
    elif extensao == '.txt':
        texto = Path(caminho_arquivo).read_text(encoding='utf-8')
    elif extensao == '.docx':
        texto = _docx_para_texto(caminho_arquivo)
    else:
        raise ValueError(f'Formato {extensao} não suportado')

    # salva o .md gerado
    caminho_md = str(Path(caminho_arquivo).with_suffix('.md'))
    Path(caminho_md).write_text(texto, encoding='utf-8')

    os.remove(caminho_arquivo)

    return texto

def _pdf_para_texto(caminho: str) -> str:
    doc = fitz.open(caminho)
    blocos = []
    for pagina in doc:
        # extrai blocos de texto individualmente
        for bloco in pagina.get_text("blocks"):
            texto = bloco[4].strip()  # índice 4 é o texto do bloco
            if texto:
                blocos.append(texto)
    return "\n\n".join(blocos)

def _docx_para_texto(caminho: str) -> str:
    doc = docx.Document(caminho)
    return "\n\n".join([p.text for p in doc.paragraphs if p.text.strip()])