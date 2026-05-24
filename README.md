# ProjetoJarvis

> Sistema de assistente acadêmico inteligente desenvolvido para a disciplina de Inteligência Artificial, utilizando RAG (Retrieval-Augmented Generation), busca semântica e tool calling.

---

# Objetivo do Projeto

O ProjetoJarvis tem como objetivo desenvolver um assistente acadêmico inteligente capaz de combinar:

- Recuperação de informação via RAG
- Busca semântica híbrida
- Gerenciamento de tarefas acadêmicas
- Planejamento de estudos
- Consulta contextualizada de materiais

Tudo isso integrado em uma interface conversacional semelhante a um chatbot.

---

# Funcionalidades Implementadas

- Adicionar tarefas
- Listar tarefas
- Listar tarefas concluídas
- Concluir tarefas
- Consultar agenda
- Buscar materiais acadêmicos via RAG
- Adicionar compromissos
- Remover compromissos
- Planejamento de estudos

---

## Observações Importantes

> - Os materiais selecionados pela equipe estão disponíveis na pasta `dataset/`, localizada na raiz do projeto.
> - Para que os documentos sejam utilizados pelo sistema RAG, eles devem ser enviados manualmente pelo usuário através da interface do chat (botão de clipe).
> - O sistema realiza indexação apenas dos arquivos enviados via prompt.
> - O gerenciamento de tarefas e compromissos é persistido em banco SQLite, iniciado vazio e alimentado dinamicamente pelo usuário.

---

# Aviso

É altamente recomendável a leitura completa dos arquivos `README.md` disponibilizados nos diretórios do projeto, pois eles contêm informações, explicações e observações importantes sobre os respectivos módulos.

---

# Desenvolvedores

- João Vitor Costa Braga
- Louise Mayumi Takigawa Pereira

---

# Como Funciona a Aplicação

O sistema funciona como um chatbot conversacional, no qual o usuário interage através de prompts em linguagem natural.

A partir dessas interações, o agente inteligente identifica a intenção do usuário e decide dinamicamente quais funções devem ser executadas.

As funcionalidades relacionadas à análise documental, como:

- `buscar_material_rag`
- `planejar_estudos`

dependem do envio manual de arquivos pelo usuário através do botão de clipe presente na interface do chat.

---

## Funcionamento dos Materiais Acadêmicos

O diretório `src/dataset/` serve apenas como armazenamento local dos materiais previamente selecionados pela equipe.

Os arquivos presentes nesse diretório **não são carregados automaticamente** pelo sistema.

Para que possam ser analisados pelo pipeline RAG, os documentos devem:

1. Ser baixados/localizados pelo usuário
2. Ser enviados manualmente via interface do chat
3. Passar pelo processo de indexação semântica

---

# Pipeline RAG

O fluxo utilizado pelo sistema para recuperação semântica funciona da seguinte forma:

1. Upload do documento pelo usuário
2. Extração textual do arquivo
3. Chunking por parágrafos
4. Geração de embeddings semânticos
5. Indexação híbrida (FAISS + BM25)
6. Recuperação contextual dos chunks mais relevantes
7. Geração da resposta pela LLM

---

## Persistência e Reinicialização

Os índices RAG são mantidos apenas em memória durante a execução da aplicação.

Portanto, ao reiniciar o servidor:

- os arquivos presentes em `src/uploads/` devem ser removidos;
- os documentos precisam ser enviados novamente via chat para que sejam reindexados e serem interpretados pelo RAG do sistema.

O banco SQLite (`jarvis.db`) permanece persistido entre execuções, mantendo:

- tarefas;
- compromissos;
- dados relacionados à agenda.

---

# Como Rodar a Aplicação

### 1. Clonar o Repositório

```bash
git clone URL-DO-REPOSITORIO
```

### 2. Criar e Ativar o Ambiente Virtual

```bash
python -m venv .venv
```

#### Windows

```bash
.venv\Scripts\activate
```

#### Linux/Mac

```bash
source .venv/bin/activate
```


### 3. Instalar as Dependências

```bash
pip install -r requirements.txt
```


### 4. Executar a Aplicação

```bash
python app.py
```


### 5. Acessar no Navegador

Abrir o link exibido no terminal:

```text
http://127.0.0.1:5000
```

---

# Tecnologias e Ferramentas Utilizadas

## Backend

- **Python 3.11** — linguagem principal do projeto
- **Flask** — framework web responsável pelas rotas e servidor HTTP
- **SQLite** — persistência local de tarefas e compromissos

---

## RAG (Retrieval-Augmented Generation)

- **PyMuPDF (`fitz`)** — extração de texto de arquivos PDF
- **python-docx** — leitura de arquivos `.docx`
- **Sentence Transformers** — geração de embeddings semânticos
  - Modelo utilizado:
    - `paraphrase-multilingual-MiniLM-L12-v2`
- **FAISS** — indexação vetorial para busca semântica
- **BM25Okapi (`rank-bm25`)** — busca lexical baseada em frequência de termos
- **Recuperação híbrida** — combinação entre FAISS (semântico) e BM25 (lexical)

---

## LLM

- **OpenAI Python SDK** — cliente de comunicação com APIs de modelos
- **Gemma 3 12B IT** — modelo hospedado no servidor institucional (LIA/UFMS)
- **Tool Calling baseado em prompting** — seleção dinâmica de funções através de respostas estruturadas em JSON produzidas pela LLM

---

# Modelos de IA Utilizados

## Claude

Utilizado para:

- formatação de código;
- identificação e correção de bugs;
- refinamento estrutural;
- melhorias gerais de código.

---

## Gemini

Utilizado para:

- enriquecimento de prompts;
- geração de materiais acadêmicos auxiliares;
- apoio na construção da base documental do sistema.

---

## ChatGPT

Utilizado para:

- identificação e resolução de bugs;
- explicações técnicas;
- apoio arquitetural no desenvolvimento do sistema.

---

## DeepSeek

Utilizado para:

- busca de artigos acadêmicos;
- pesquisa de conteúdos técnicos utilizados como base documental.

---

# Observações Gerais

- Algumas funcionalidades podem sofrer alterações ao longo das entregas da disciplina.
- Arquivos suportados:
  - `.pdf`
  - `.txt`
  - `.docx`
- O sistema depende do envio manual dos documentos para indexação.
- Parte dos materiais utilizados pode sofrer pequenas perdas semânticas durante processos de conversão textual.
- O projeto encontra-se em evolução contínua.