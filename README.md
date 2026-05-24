
# ProjetoJarvis <small>

_Resolução do trabalho da disciplina de Inteligência Artificial: implementação de um assistente acadêmico inteligente._

#### Funcionalidades implementadas:
Adicionar_tarefa, listar_tarefas, listar_tarefas_concluidas,  concluir_tarefa, consultar_agenda, buscar_material_rag, adicionar_compromisso, remover_compromisso, planejar_estudos.

    Obs.:
    - Os materiais escolhidos pela equipe estão na pasta "dataset/" na raiz do projeto.
      Para utilizá-los no sistema, o usuário deve enviá-los manualmente via prompt (botão 
      de clipe no chat) — o sistema só indexa arquivos enviados dessa forma.
    - O gerenciamento de tarefas e agenda é feito via prompt e persistido no banco SQLite
      (iniciado vazio e incrementado pelo usuário).

---

## Aviso

É altamente recomendável a leitura inteira dos arquivos `README.md` disponibilizados nos diretórios do projeto, pois eles contêm informações, explicações e observações importantes sobre os respectivos módulos acessados.


---

## Desenvolvedores

- João Vitor Costa Braga
- Louise Mayumi Takigawa Pereira

---

# Como rodar a aplicação

## Pré-requisitos
- Python 3.11
- Git (opcional, para clonar o repositório)

---

## 1. Criar e ativar o ambiente virtual

```bash
python -m venv .venv
```

**Windows:**
```bash
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

---

## 2. Instalar as dependências

```bash
pip install -r requirements.txt
```


## 3. Rodar a aplicação

```bash
python app.py
```

## 4. Acessar no navegador
http://127.0.0.1:5000



---

# Tecnologias e Ferramentas Utilizadas

## Backend
- **Python 3.11** — linguagem principal
- **Flask** — framework web para criação das rotas e servidor HTTP
- **SQLite** — banco de dados local para persistência de tarefas e compromissos
- **python-dotenv** — carregamento de variáveis de ambiente (.env)

## RAG (Retrieval-Augmented Generation)
- **PyMuPDF (fitz)** — extração de texto de arquivos PDF
- **python-docx** — extração de texto de arquivos Word (.docx)
- **Sentence Transformers** — geração de embeddings semânticos dos chunks
  - Modelo: `paraphrase-multilingual-MiniLM-L12-v2`
- **FAISS** — índice vetorial para busca semântica eficiente
- **BM25Okapi (rank-bm25)** — índice lexical para busca por frequência de termos
- **Retrieval Híbrido** — combinação de FAISS (semântico) + BM25 (lexical) com fusão por score normalizado

## LLM
- **OpenAI Python SDK** — client para comunicação com a API
- **Gemma 3 12B IT** — modelo de linguagem hospedado no servidor da instituição (LIA/UFMS)
- **Tool Calling via Prompt** — decisão de chamada de funções via JSON estruturado no system prompt

## Frontend
- **HTML5 + CSS3 + JavaScript** — interface do chat
- **marked.js** — renderização de markdown nas respostas da LLM
- **Jinja2** — template engine do Flask para servir o HTML

## Arquitetura
- **Agente Roteador** (`client.py`) — decide qual função chamar com base na intenção do usuário
- **Agente RAG** (`generator.py`) — responde perguntas com base nos documentos indexados
- **Agente Planejador** (`planejar_estudos`) — combina tarefas, agenda e documentos para planejamento

---

# Modelos de IA Utilizados

## Claude

Utilizado para:

- Formatação de código
- Identificação e correção de bugs
- Refinamento estrutural
- Melhorias gerais de código

---

## Gemini

Utilizado para:

- Enriquecimento de prompts do agente
- Geração de materiais acadêmicos auxiliares
- Apoio na construção da base documental utilizada no sistema

---

## ChatGPT

Utilizado para:

- Identificação e resolução de bugs
- Explicações técnicas
- Apoio arquitetural no desenvolvimento do sistema

---

## DeepSeek

Utilizado para:

- Busca de artigos acadêmicos
- Pesquisa de conteúdos técnicos utilizados como base documental do sistema

---

## Observações de uso
- Algumas funcionalidades podem sofrer alterações ao longo das entregas dos trabalhos.
- Os materiais disponíveis para consulta estão na pasta `dataset/` — envie-os pelo chat
  usando o botão de clipe antes de fazer perguntas sobre seu conteúdo
- Arquivos aceitos: `.pdf`, `.txt`, `.docx`
- Os índices RAG são mantidos em memória — ao reiniciar o servidor, os arquivos precisam 
  ser excluídos da pasta `src/uploads/` e reenviados via chat novamente
- O banco SQLite (`jarvis.db`) persiste tarefas e compromissos entre sessões
