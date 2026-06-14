
# Avaliação do Sistema

Neste arquivo são descritos os casos de teste utilizados para verificar a qualidade do sistema e analisar suas inconsistências. O documento está dividido em duas partes:

- **Avaliação do sistema:** descrição das 10 perguntas realizadas, com entradas, saídas, documentos recuperados e classificação das respostas.
- **Análise de erros:** descrição de no mínimo 3 falhas encontradas, com tipo, possível causa e solução.

---

## Avaliação do Sistema

---

### Pergunta 1

**Entrada:** "Como funciona o pipeline do RAG?"

**Resposta:** "Como funciona o pipeline do RAG?

O pipeline do RAG opera em três etapas distintas:

Recuperação (Retrieval): Realiza uma busca semântica utilizando embeddings (FAISS) e/ou uma busca lexical (BM25).
Aumentação (Augmentation): Injeta os documentos recuperados no prompt.
Geração (Generation): Um LLM (Large Language Model) processa o contexto e o prompt, gerando a resposta exata.
Fontes utilizadas:

Segundo o arquivo artigoAprendMaquinaGEMINI.txt...
"

**Documentos Recuperados:**
- `artigoAprendMaquinaGEMINI.txt`

**Classificação:**

---

### Pergunta 2

**Entrada:** "Qual a diferença entre RAG-Sequence e RAG-Token?"

**Resposta:** "O RAG-Sequence utiliza a técnica de seq2seq (sequence to sequence) para gerar respostas completas a partir de uma pergunta, enquanto o RAG-Token utiliza a técnica de tokenização para gerar respostas, onde cada palavra da resposta é gerada individualmente."
(resposta-direta)

**Documentos Recuperados:**
- Nenhum — resposta direta (falha!)

**Classificação:**

---

### Pergunta 3

**Entrada:** "Quais são os principais componentes de um sistema RAG?"

**Resposta:** "Os principais componentes de um sistema RAG (Retrieval-Augmented Generation) incluem:

Indexador de Documentos: Responsável por processar e indexar uma grande quantidade de documentos.
Buscador de Informações: Utiliza a indexação para encontrar os documentos mais relevantes à consulta.
Modelo de Geração: Gera respostas ou textos coesos baseados nos resultados da busca e outros conhecimentos pré-existentes."

**Documentos Recuperados:**
- Nenhum — resposta direta

**Classificação:**

---

### Pergunta 4

**Entrada:** "Como os embeddings são utilizados em sistemas de busca?"

**Resposta:** "Os embeddings são utilizados em sistemas de busca principalmente para representar e comparar semelhanças entre diferentes documentos ou consultas. Segundo o arquivo On The Role of Pretrained Language Models in General-Purpose Text Embeddings.pdf (Fonte 4), os embeddings gerados por modelos pré-treinados (PLMs) são usados para criar representações contextuais de palavras que são posteriormente agregadas em um único vetor, resultando na forma de embedding do texto de entrada.

Em seguida, esses embeddings são utilizados para calibrar a similaridade entre pares de textos, onde um texto é considerado o ponto de referência (anchor text) e outros textos são classificados como positivos (relevantes) ou negativos (irrelevantes) em relação ao texto de referência. Essa técnica é frequentemente aplicada em tarefas de busca de informações (IR) e respostas a perguntas (QA), conforme mencionado no mesmo arquivo (Fonte 4).

Adicionalmente, os embeddings também são utilizados em sistemas de busca para otimizar a recuperação de documentos semelhantes em cenários de aprendizado de máquina, como descrito no arquivo Driving-RAG.pdf (Fonte 5). Aqui, os embeddings precisam ser precisos e eficientes para distinguir melhor entre diferentes cenários e facilitar a busca eficiente de dados de cenários.

Referências:

Segundo o arquivo On The Role of Pretrained Language Models in General-Purpose Text Embeddings.pdf (Fonte 4).
Arquivo Driving-RAG.pdf (Fonte 5)."

**Documentos Recuperados:**
- `On The Role of Pretrained Language Models in General-Purpose Text Embeddings.pdf`
- `Driving-RAG.pdf`

**Classificação:**

---

### Pergunta 5

**Entrada:** "O que é BM25 e para que serve?"

**Resposta:** "BM25 é uma função de ranqueamento probabilístico não-paramétrico amplamente utilizada para avaliar a relevância de um documento ( D ) em relação a uma consulta ( Q ). Serve principalmente para recuperar documentos relevantes em relação a uma consulta específica, sendo útil quando se precisa encontrar documentos que contenham identificadores exatos, números de série ou terminologias altamente específicas.

Fontes Utilizadas:
Segundo o arquivo artigoAprendMaquinaGEMINI.txt (Fonte 5).
Baseado no arquivo On The Role of Pretrained Language Models in General-Purpose Text Embeddings.pdf (Fonte 4)."

**Documentos Recuperados:**
- `artigoAprendMaquinaGEMINI.txt`
- `On The Role of Pretrained Language Models in General-Purpose Text Embeddings.pdf`

**Classificação:**

---

### Pergunta 6

**Entrada:** "O que é o mecanismo de Attention e qual seu papel nos Transformers?"

**Resposta:** "Mecanismo de Attention

Segundo o arquivo AttentionIsAllYouNeed.pdf, o mecanismo de Attention é fundamental para o funcionamento do modelo Transformer. Ele substitui a recorrência usada em redes neurais recorrentes, permitindo que o modelo dependa inteiramente de um mecanismo de atenção para estabelecer relações globais entre entrada e saída.

Papel nos Transformers

No Transformer, o mecanismo de Attention é usado de três formas diferentes:

Multi-head Attention: Usado para permitir que cada posição no decodificador atenda a todas as posições na sequência de entrada. Isso é similar aos mecanismos tradicionais de atenção codificador-decodificador em modelos de seqüência-a-seqüência.
Segundo o arquivo AttentionIsAllYouNeed.pdf, o Transformer usa a atenção multi-head em três maneiras distintas, incluindo a atenção codificador-decodificador que permite que cada posição no decodificador atenda a todas as posições na sequência de entrada.

Essa abordagem permite maior paralelização e melhora a qualidade de tradução após treinamento por até 12 horas em oito GPUs P100."

**Documentos Recuperados:**
- `AttentionIsAllYouNeed.pdf`

**Classificação:**

---

### Pergunta 7

**Entrada:** "Qual a diferença entre regressão linear e regressão logística?"

**Resposta:** "A regressão linear é usada quando a variável de saída é contínua e pode assumir qualquer valor numérico. Ela ajusta uma linha aos dados para prever valores futuros. Por outro lado, a regressão logística é utilizada quando a variável de saída é categórica (geralmente binária) e o objetivo é estimar as probabilidades de que um determinado evento ocorra."

**Documentos Recuperados:**
- Nenhum — resposta direta

**Classificação:**

---

### Pergunta 8

**Entrada:** "Quais são os tipos de teste de software descritos no material?" - 'material' = VVT

**Resposta:** "Resposta:

Segundo o arquivo ConteudoP1-VVT.docx, os tipos de teste de software descritos no material são:

Teste de Sistema: Verifica se o software atende aos requisitos funcionais e atributos de qualidade (desempenho, segurança, stress, recuperação).
End-to-End (E2E): Foca na jornada completa do usuário através de todos os componentes do sistema.
Fontes utilizadas:

ConteudoP1-VVT.docx"

**Documentos Recuperados:**
- `ConteudoP1-VVT.docx`

**Classificação:**

---

### Pergunta 9

**Entrada:** "O que é uma curva poligonal fechada simples?"

**Resposta:** "Resposta:

Segundo o arquivo artgallery.pdf, uma curva poligonal fechada simples é uma curva que divide o plano em duas regiões distintas (interior e exterior da curva), conforme o famoso Teorema de Jordan. Além disso, define-se um polígono como a região fechada do plano limitada por uma curva poligonal fechada simples."

**Documentos Recuperados:**
- `artgallery.pdf`

**Classificação:**

---

### Pergunta 10

**Entrada:** "O que é o problema da galeria de arte?"

**Resposta:** "Problema da Galeria de Arte

Segundo o arquivo artgallery.pdf:

O problema da Galeria de Arte consiste em determinar a quantidade mínima de guardas necessários para cobrir completamente a planta de uma sala de uma galeria de arte, de modo que cada ponto da sala possa ser visto por pelo menos um guarda.

Victor Klee propôs esse problema em 1973.

O Teorema da Galeria de Arte (Chvátal's Art Gallery Theorem ou Watchman Theorem) afirma que ⌊n/3⌋ guardas são suficientes e às vezes necessárias para cobrir uma sala com n paredes."

**Documentos Recuperados:**
- `artgallery.pdf`

**Classificação:**

---

### Pergunta 11

**Entrada:** "com base nos documentos enviados, o que é overfitting e como evitá-lo?"

**Resposta:** "Overfitting é um fenômeno no aprendizado de máquina onde um modelo se ajusta muito bem aos dados de treinamento, incluindo ruído e detalhes específicos que não devem ser generalizados. Isso pode levar a um desempenho ruim em novos dados que o modelo não viu durante o treinamento.

Como evitar overfitting?

Segundo o arquivo AttentionIsAllYouNeed.pdf, uma técnica simples para prevenir redes neurais de overfitting é o uso de dropout. O dropout remove aleatoriamente uma fração de nós (neurônios) durante o treinamento, o que ajuda a evitar que o modelo se ajuste demais aos dados de treinamento.

Portanto, o dropout é uma técnica útil para evitar overfitting.

Referências:

Segundo o arquivo AttentionIsAllYouNeed.pdf"

**Documentos Recuperados:**
- `AttentionIsAllYouNeed.pdf`

**Classificação:**

---

### Pergunta 12

**Entrada:** "Com base nos documentos, o que é teste caixa-preta e teste caixa-branca?"

**Resposta:** "Resposta:

Segundo o arquivo Fonte 1 (ConteudoP1-VVT.docx), o conceito de teste funcional (caixa-preta) foca na especificação, baseando-se nos requisitos e no que o software deve fazer macroscopicamente, sem considerar detalhes de implementação ou o código interno.

Para o teste caixa-branca, embora não haja uma definição explícita nas fontes fornecidas, podemos inferir que este tipo de teste examina a estrutura interna do software, incluindo o código-fonte. Isso pode ser deduzido do contexto fornecido na Fonte 4 (the-art-of-software-testing-(myers)-resumo.txt), onde são mencionadas técnicas de teste de caixa branca como a cobertura de declarações.

Fontes utilizadas:

Segundo o arquivo Fonte 1 (ConteudoP1-VVT.docx)
Fonte 4 (the-art-of-software-testing-(myers)-resumo.txt)"

**Documentos Recuperados:**
- `ConteudoP1-VVT.docx`
- `the-art-of-software-testing-(myers)-resumo.txt`

**Classificação:**

---

### Pergunta 13

**Entrada:** "O que é triangulação em geometria computacional?"

**Resposta:** "Resposta: Segundo o arquivo artgallery.pdf, triangulação em geometria computacional refere-se à divisão de um polígono em triângulos. Especificamente, o Teorema 2 menciona que todo polígono pode ser triangularizado, ou seja, dividido em triângulos.

Fontes utilizadas:

Arquivo artgallery.pdf"

**Documentos Recuperados:**
- `artgallery.pdf`

**Classificação:**

---

### Pergunta 14

**Entrada:** "O que é a função sigmoide e onde ela é aplicada?"

**Resposta:** "Função Sigmoide

A função sigmoide, denotada por $\sigma(z)$, é uma função que mapeia qualquer valor real para o intervalo $(0, 1)$. Ela é frequentemente utilizada para transformar valores lineares em probabilidades, especialmente em modelos de classificação binária.

Aplicações

A função sigmoide é aplicada na Regressão Logística, onde é usada para calcular a probabilidade de um evento ocorrer dado um conjunto de atributos. Especificamente, ela é usada na seguinte equação:

$$P(y=1|x) = \sigma(\beta^T x) = \frac{1}{1 + e^{-\beta^T x}}$$

onde $x$ representa os atributos, $\beta$ são os parâmetros do modelo, e $\sigma$ é a função sigmoide.

Referências

Segundo o arquivo artigoAprendMaquinaGEMINI.txt, a função sigmoide é definida e explicada em detalhes."

**Documentos Recuperados:**
- `artigoAprendMaquinaGEMINI.txt`

**Classificação:**

---

### Pergunta 15

**Entrada:** "com base nos documentos, Como funciona o Multi-Head Attention?"

**Resposta:** "Como funciona o Multi-Head Attention?

Segundo o arquivo AttentionIsAllYouNeed.pdf, o Multi-Head Attention consiste em várias camadas de atenção funcionando em paralelo. Isso permite que o modelo atenda simultaneamente a informações de diferentes subespaços de representação em diferentes posições. Cada camada de atenção é projetada através de matrizes de pesos específicas para query, key e value, resultando em múltiplas projeções que são então concatenadas e novamente projetadas para gerar os valores finais.

No arquivo Driving-RAG.pdf, é explicado que cada cabeça de atenção calcula sua própria atenção com base nas queries, keys e values projetadas. Estas são então concatenadas e novamente projetadas para produzir o resultado final de atenção.

Em resumo, o Multi-Head Attention envolve:

Projeção das queries, keys e values através de matrizes de pesos específicas.
Cálculo da atenção para cada cabeça.
Concatenação dos resultados de todas as cabeças.
Projeção final dos resultados concatenados.
Essa abordagem permite que o modelo capture características distintas da entrada através de múltiplos espaços de representação simultaneamente.

Fontes utilizadas:

Segundo o arquivo AttentionIsAllYouNeed.pdf...
Segundo o arquivo Driving-RAG.pdf..."
"

**Documentos Recuperados:**
- `AttentionIsAllYouNeed.pdf`
- `Driving-RAG.pdf`

**Classificação:**

---

### Pergunta 16

**Entrada:** "Com base nos documentos, Como PLMs melhoram a qualidade de embeddings de propósito geral?"

**Resposta:** "PLMs melhoram a qualidade de embeddings de propósito geral através de várias estratégias:

Arquitetura de Rede: PLMs geralmente adotam uma arquitetura baseada em transformadores, onde as representações de nível de palavra são interconectadas através de mecanismos de atenção, permitindo que cada token preste atenção aos outros dentro da sequência e gere assim representações contextualizadas de palavras (Fonte 1).

Mecanismos de Atividade: Encoder-based PLMs usam atenção bidirecional para agregar informações contextuais, enquanto decoder-based PLMs utilizam atenção causal (unidirecional) para construir representações de maneira autoregressiva. Encoder-decoder PLMs combinam ambos os métodos (Fonte 1).

Pooling Strategy: Uma estratégia de agregação é empregada para produzir um vetor de tamanho fixo que serve como o embedding do texto completo, utilizando uma combinação ponderada das representações ocultas de cada palavra (Fonte 1).

Representações Contextuais: Encoder-based PLMs, como BERT e RoBERTa, usam a representação do primeiro token (⟨CLS⟩) para capturar rica informação contextual do texto inteiro (Fonte 1).

Essas estratégias permitem que os PLMs gerem embeddings de texto que capturam informações contextuais ricas e relevantes para uma variedade de tarefas, melhorando assim a qualidade dos embeddings de propósito geral."

**Documentos Recuperados:**
- `On The Role of Pretrained Language Models in General-Purpose Text Embeddings.pdf` ⚠️ *(citado com link quebrado pelo sistema)*

**Classificação:**

poderia me ajudar a completar essa analise de erros?

## Análise de Erros

### Falha 1
| Campo | Descrição |
|-------|-----------|
| **Título** | Resposta direta em vez de busca RAG |
| **Tipo** | Chamada de função |
| **Descrição** | Perguntas 2, 3 e 7 deveriam ter buscado nos documentos indexados (que contêm material sobre RAG e regressão), mas o sistema optou por responder diretamente do conhecimento do LLM sem consultar nenhum arquivo. Isso compromete a confiabilidade do sistema, já que a resposta não é rastreável a nenhuma fonte. |
| **Causa** | O system prompt não foi registrado para fazer com se prefira usar buscar_material_rag antes de mandar uma mensagem direta |
| **Solução** | Melhorar o prompt e adicionar mais condições da execução do tool calling no client.py |

### Falha 2

| Campo | Descrição |
|-------|-----------|
| **Título** | Citação com referência quebrada |
| **Tipo** | Descrição |
| **Descricao** | O sistema citou "Fonte 1" com um link quebrado em vez do nome real do arquivo (On The Role of Pretrained...). Isso indica que o modelo às vezes perde o rastreamento correto da fonte durante a geração, o que é um problema de confiabilidade nas citações. |
| **Causa** | Durante a geração, o LLM perde o mapeamento entre o índice interno da fonte (ex: "Fonte 1") e o nome real do arquivo. |
| **Solução** | Modificar o prompt do responder_rag no generator.py para instruir o modelo a sempre citar pelo nome do arquivo, nunca pelo índice numérico. Reforçar com uma regra explícita como: "Sempre cite as fontes pelo nome do arquivo, nunca por 'Fonte 1' ou similar." |

### Falha 3
| Campo | Descrição |
|-------|-----------|
| **Título** | Uma função por prompt |
| **Tipo** | Implementação |
| **Descricao** | O sistema nã consegue realizar mais que uma chamada de função ao mesmo tempo. Por exemplo, se pedirmos "Adicione duas tarefas: 'Falar com a Nina as 13 de amanhã' e 'Levar o Tob para passear no sabádo'" ele nos daria " |
| **Causa** | Não foi implementado da forma correta o código de cobertura desse comportamento. Até tentamos (com o uso de turnos - sendo o máximo até 6), mas não conseguimos deixa-lo funcional, o que fica aparente nessa falha percebida. |
| **Solução** | Implementar uma função baseada em turno para cada função percebida que invoca um método.  |

### Falha 4
| Campo | Descrição |
|-------|-----------|
| **Título** | Dificuldade de compreender intenções |
| **Tipo** | Implementação |
| **Descricao** | O sistema, quando é pedido para ele 'adicionar na agenda' ou 'marcar um compromisso', foi percebido que ele adiciona na lista de tarefas e não no calendário acadêmico. |
| **Causa** | Falha na implementação |
| **Solução** | Melhorar o prompt e verificar possiveis bugs dentro  |

