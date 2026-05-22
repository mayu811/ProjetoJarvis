from pathlib import Path
import os
import fitz  # pymupdf
import docx

def converter_para_markdown(caminho_arquivo: str) -> str:
    # extrai a extensão do arquivo para determinar o método de conversão
    extensao = Path(caminho_arquivo).suffix.lower()

    # converte o arquivo para markdown
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
    # escreve o texto convertido no arquivo .md
    Path(caminho_md).write_text(texto, encoding='utf-8') 

    # remove o arquivo original (em PDF) para evitar acúmulo de arquivos
    os.remove(caminho_arquivo)

    # retorna o texto convertido para que possa ser processado diretamente
    return texto


# ------------ CONVERSORES ESPECÍFICOS PARA CADA FORMATO --------------

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