# PDF -> Marksdown converter (docling)

# ── Conversão PDF → Markdown ──────────────────────────────────────────────────

from docling.document_converter import DocumentConverter

print("Convertendo PDF para Markdown...")
converter = DocumentConverter()
resultado = converter.convert(CAMINHO_PDF)

# O Docling retorna um objeto 'DoclingDocument'.
# O método export_to_markdown() entrega o texto estruturado.
texto_markdown = resultado.document.export_to_markdown()

# Salva o Markdown gerado para inspeção
# Usamos Path.with_suffix() para funcionar com qualquer extensão (.pdf, .PDF, etc.)
caminho_md = str(Path(CAMINHO_PDF).with_suffix(".md"))
Path(caminho_md).write_text(texto_markdown, encoding="utf-8")

print(f"Markdown salvo em: {caminho_md}")
print(f"Total de caracteres: {len(texto_markdown):,}")
print()
print("═" * 60)
print("PRÉVIA DOS PRIMEIROS 1000 CARACTERES:")
print("═" * 60)
print(texto_markdown[:1000])