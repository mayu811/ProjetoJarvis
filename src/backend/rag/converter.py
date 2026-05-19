from pathlib import Path
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

    return texto

def _pdf_para_texto(caminho: str) -> str:
    doc = fitz.open(caminho)
    return "\n\n".join([pagina.get_text() for pagina in doc])

def _docx_para_texto(caminho: str) -> str:
    doc = docx.Document(caminho)
    return "\n\n".join([p.text for p in doc.paragraphs if p.text.strip()])