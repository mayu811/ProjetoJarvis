# PDF -> Marksdown converter (docling)
# ── Conversão PDF → Markdown ──────────────────────────────────────────────────

from docling.document_converter import DocumentConverter
from pathlib import Path

converter = DocumentConverter()
 #print("Convertendo PDF para Markdown...")

def converter_para_markdown(caminho_arquivo: str) -> str:
    resultado = converter.convert(caminho_arquivo)
    texto_markdown = resultado.document.export_to_markdown()

    # salva o .md gerado (opcional, mas útil para depurar)
    caminho_md = str(Path(caminho_arquivo).with_suffix('.md'))
    Path(caminho_md).write_text(texto_markdown, encoding='utf-8')

    return texto_markdown