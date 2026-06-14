# Base de Materiais Acadêmicos Utilizados no Sistema

Este README tem como objetivo detalhar os documentos acadêmicos utilizados pelo sistema antes de sua conversão para o formato `.md`. Esses materiais serão consultados principalmente pela função `buscar_material_rag`.

Os temas abordados incluem:

- Aprendizado de Máquina
- RAG (Retrieval-Augmented Generation)
- Embeddings
- BM25
- FAISS
- Regressão Linear e Logística
- Verificação, Validação e Teste de Software (VVT)
- Geometria Computacional
- Boas práticas de desenvolvimento

Além disso, como não foi especificada a obrigatoriedade de um dataset definitivo para a entrega do Trabalho 1 — considerando a existência de uma segunda entrega (Trabalho 2) — alguns materiais presentes neste diretório poderão sofrer modificações futuras.

---

# Materiais

---

## 1. `aula-KNN`

- **ORIGEM:** material (slides) disponibilizado pelo próprio professor Takashi no AVA.
- **TEMA:** KNN
- **TIPO:** `.pdf`
- **LIMITAÇÕES:** uso de imagens no material, dificultando a compreensão completa pelo agente do sistema.

---

## 2. `ConteudoP1-VVT`

- **ORIGEM:** resumo gerado pelo GEMINI a partir dos slides da disciplina de VVT, ministrada pelo professor Awdren. O material foi utilizado pelos próprios estudantes para estudo da P1.
- **TEMA:** Verificação, Validação e Teste de Software
- **TIPO:** `.docx`
- **LIMITAÇÕES:** nenhuma identificada até o momento.

---

## 3. `RAG-for-Knowledge-Intensive-Lewis-2020`

- **ORIGEM:** disponível em https://arxiv.org/abs/2005.11401
- **TEMA:** RAG (Retrieval-Augmented Generation)
- **TIPO:** `.pdf`
- **LIMITAÇÕES:** presença de imagens e elementos gráficos que dificultam a interpretação integral pelo agente.

---

## 4. `AttentionIsAllYouNeed`

- **ORIGEM:** disponível em https://arxiv.org/abs/1706.03762
- **TEMA:** Transformers e mecanismo de Attention
- **TIPO:** `.pdf`
- **LIMITAÇÕES:** uso de imagens e diagramas que podem dificultar a extração semântica do conteúdo.

---

## 5. `the-art-of-software-testing-(myers)-resumo`

- **ORIGEM:** disponível em https://medium.com/@JSobral/the-art-of-software-testing-from-glenford-myers-871ac1073264
- **TEMA:** Teste de Software
- **TIPO:** `.txt`
- **LIMITAÇÕES:** nenhuma identificada até o momento.

---

## 6. `Driving-RAG`

- **ORIGEM:** disponível em https://arxiv.org/pdf/2504.04419
- **TEMA:** RAG
- **TIPO:** `.pdf`
- **LIMITAÇÕES:** uso de imagens no artigo dificulta a interpretação completa pelo agente.

---

## 7. `artigoAprendMaquinaGEMINI`

- **ORIGEM:** material gerado pelo GEMINI a partir de um prompt acadêmico voltado para revisão teórica aprofundada sobre:
  - RAG
  - Embeddings
  - Regressão Logística
  - Regressão Linear
  - BM25
  - FAISS

- **TIPO:** `.txt`

- **TEMA:**  
  RAG, embeddings, regressão logística e linear, BM25 e FAISS.

- **LIMITAÇÕES:**  
  Algumas fórmulas presentes no material sofreram perdas durante o processo de conversão, resultando em resíduos de símbolos e caracteres que podem dificultar parcialmente a compreensão do conteúdo pelo agente.

---

## 8. `artgallery`

- **ORIGEM:** disponível em https://share.google/4sCjQX2OoL2RnNWeW
- **TEMA:** Geometria Computacional
- **TIPO:** `.pdf`
- **LIMITAÇÕES:** uso de imagens e elementos gráficos dificulta parte da interpretação automatizada.

---

## 9. `intro-geo-comp`

- **ORIGEM:** disponível em https://www.ime.usp.br/~cris/aulas/07_2_331/intro.pdf
- **TEMA:** Geometria Computacional
- **TIPO:** `.pdf`
- **LIMITAÇÕES:** presença de imagens e diagramas pode dificultar a compreensão completa pelo agente.

---

## 10. `On The Role of Pretrained Language Models in General-Purpose Text Embeddings`

- **ORIGEM:** disponivel em https://arxiv.org/abs/2507.20783
- **TEMA:** Aborda modelos de Linguagem Pré-treinados (PLMs) no desenvolvimento de Embeddings de Texto de Propósito Geral (GPTE).
- **TIPO:** `.pdf`
- **LIMITAÇÕES:** presença de imagens e diagramas pode dificultar a compreensão completa pelo agente.

---

# Observações Gerais

- Alguns documentos possuem grande quantidade de imagens, gráficos e fórmulas matemáticas complexas.
- Durante o processo de conversão para Markdown (`.md`), parte dessas estruturas pode sofrer perdas semânticas.
- O objetivo principal desses materiais é servir como base documental para mecanismos de recuperação semântica utilizados pelo sistema RAG.