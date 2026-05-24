Integração de Métodos Paramétricos e Não-Paramétricos na Recuperação de Informação e Aprendizado de Máquina: Dos Modelos Lineares ao RAG
Resumo
Este artigo de revisão teórica examina a convergência entre abordagens paramétricas clássicas e métodos não-paramétricos de recuperação de informação (IR) no ecossistema de aprendizado de máquina contemporâneo. Analisa-se o funcionamento e as formulações matemáticas da regressão linear e logística, estabelecendo suas limitações no tratamento de dados textuais de alta dimensionalidade. Em seguida, investiga-se a transição para representações densas via embeddings e a recuperação lexical por meio do algoritmo BM25, detalhando como o framework FAISS otimiza a busca por vizinhos mais próximos. Por fim, discute-se a arquitetura de Geração Aumentada de Recuperação (RAG) como o ápice dessa integração, onde a recuperação não-paramétrica mitiga as limitações de alucinação e obsolescência dos modelos de linguagem paramétricos. O artigo conclui que a hibridização de técnicas léxicas e semânticas, operando sob estruturas de indexação eficientes, constitui o estado da arte para sistemas de IA robustos e auditáveis.
1. Introdução
O desenvolvimento do aprendizado de máquina e da recuperação de informação (IR, na sigla em inglês) tem sido historicamente marcado pela dualidade entre modelos paramétricos e não-paramétricos. Modelos paramétricos, como as regressões lineares e logísticas, condensam o conhecimento dos dados de treino em um conjunto fixo de pesos matemáticos (Hastie et al., 2009). Embora altamente interpretáveis e eficientes em dados estruturados, essas abordagens enfrentam limitações severas quando aplicadas à linguagem natural, cuja natureza é inerentemente esparsa, polissêmica e de alta dimensionalidade.
Com o advento dos modelos de linguagem baseados na arquitetura Transformer (Vaswani et al., 2017), o paradigma de processamento de texto mudou substancialmente. A representação de palavras e documentos migrou de vetores esparsos e discretos para vetores densos e contínuos, conhecidos como embeddings. Paralelamente, algoritmos tradicionais de correspondência lexical, como o BM25 (Robertson & Jones, 1976), mantiveram sua relevância devido à precisão na busca por termos específicos (palavras-chave), expondo a necessidade de combinar abordagens baseadas em léxico com buscas semânticas vetoriais de alta performance, viabilizadas por bibliotecas como o FAISS (Johnson et al., 2019).
Atualmente, a lacuna teórica e prática reside em como orquestrar esses componentes heterogêneos para mitigar os gargalos dos Grandes Modelos de Linguagem (LLMs). Embora os LLMs retenham vasto conhecimento em seus parâmetros, eles sofrem com alucinações fácticas e obsolescência temporal (Lewis et al., 2020). A arquitetura de Geração Aumentada de Recuperação (RAG) surge como a solução para este problema, unindo a recuperação não-paramétrica de documentos externos à capacidade de síntese paramétrica do modelo. O objetivo deste artigo é fornecer uma revisão conceitual, matemática e crítica dessas tecnologias, rastreando a evolução desde os modelos estatísticos básicos até os sistemas híbridos de recuperação e geração profunda.
2. Desenvolvimento
2.1 Modelos Paramétricos Clássicos: Regressão Linear e Regressão Logística
Os modelos lineares representam os fundamentos da modelagem preditiva estatística. A Regressão Linear assume que a variável dependente continua $y$ pode ser modelada como uma combinação linear de um vetor de variáveis independentes $x \in \mathbb{R}^d$ acrescida de um termo de erro estocástico $\varepsilon$. Formalmente, expressa-se como:


$$y = \beta_0 + \sum_{i=1}^{d} \beta_i x_i + \varepsilon$$
Onde $\beta_0$ é o intercepto e $\beta_i$ são os coeficientes (pesos) do modelo. O objetivo principal é estimar o vetor de parâmetros $\beta$ que minimiza a soma dos quadrados dos resíduos (Residual Sum of Squares - RSS) através do método de Mínimos Quadrados Ordinários (OLS):


$$\min_{\beta} \sum_{j=1}^{n} \left( y_j - (\beta_0 + \sum_{i=1}^{d} \beta_i x_{ji}) \right)^2$$
Apesar de sua eficiência, a regressão linear é inadequada para problemas de classificação binária, onde a variável de saída é categórica ($y \in \{0, 1\}$). Para este cenário, utiliza-se a Regressão Logística. Esta abordagem modela a probabilidade condicional $P(y=1|x)$ aplicando a função logística padrão (ou sigmóide) à combinação linear dos atributos:


$$P(y=1|x) = \sigma(\beta^T x) = \frac{1}{1 + e^{-\beta^T x}}$$
A função sigmóide $\sigma(z)$ mapeia qualquer valor real no intervalo $(0, 1)$, permitindo sua interpretação como uma probabilidade. A estimação dos parâmetros $\beta$ na regressão logística não possui solução analítica fechada, sendo realizada via Máxima Verossimilhança (Maximum Likelihood Estimation - MLE). A função de perda a ser minimizada, conhecida como entropia cruzada binária (Binary Cross-Entropy), é descrita por:


$$L(\beta) = -\frac{1}{n} \sum_{j=1}^{n} \left[ y_j \log(\sigma(\beta^T x_j)) + (1 - y_j) \log(1 - \sigma(\beta^T x_j)) \right]$$
No contexto de texto, se mapearmos um documento utilizando o modelo de Saco de Palavras (Bag-of-Words), onde cada posição do vetor representa a frequência ou a presença de uma palavra, a regressão logística pode atuar como um classificador de texto (Jurafsky & Martin, 2024). Contudo, este método falha em capturar a ordem das palavras, o contexto e as relações semânticas complexas de longo alcance.
2.2 Representações Densas: Embeddings
Para superar a esparsa e rígida representação de palavras dos modelos clássicos, a literatura de processamento de linguagem natural (PLN) introduziu o conceito de embeddings. Um embedding é uma representação vetorial densa de uma unidade textual (palavra, frase ou documento) em um espaço contínuo de baixa dimensionalidade (geralmente entre $d=384$ e $d=1536$), em contraste com as dimensões de dezenas de milhares geradas por abordagens Bag-of-Words.
Historicamente fundamentados na Hipótese Distribucional de Harris — que postula que palavras que ocorrem em contextos semelhantes tendem a ter significados semelhantes —, os embeddings evoluíram de representações estáticas como Word2Vec (Mikolov et al., 2013) para representações contextuais profundas baseadas em Transformers (Vaswani et al., 2017).
Em modelos baseados em Transformers, as representações são geradas através do mecanismo de Auto-Atenção (Self-Attention). Dada uma matriz de projeções de entrada $X$, o mecanismo calcula três matrizes: Consultas ($Q$), Chaves ($K$) e Valores ($V$). A atenção escalada por produto escalar é definida como:


$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$
Onde $d_k$ representa a dimensão das chaves. Esse cálculo permite que o embedding final de uma palavra seja modificado dinamicamente com base nas palavras adjacentes, capturando polissemia e nuances sintáticas. A similaridade semântica entre dois vetores de embedding $A$ e $B$ é comumente quantificada por meio da similaridade de cosseno:


$$\text{Sim}(A, B) = \frac{A \cdot B}{\|A\| \|B\|}$$
2.3 Recuperação Lexical: O Algoritmo BM25
Apesar do avanço das representações densas, a busca puramente semântica pode falhar ao recuperar identificadores exatos, números de série ou terminologias altamente específicas. Nesses cenários, a correspondência baseada em termos (lexical) desempenha um papel crucial. O algoritmo BM25 (Best Matching 25) é uma função de ranqueamento probabilístico não-paramétrico amplamente utilizada para avaliar a relevância de um documento $D$ em relação a uma consulta (query) $Q$ contendo os termos $q_1, q_2, \dots, q_n$ (Robertson & Jones, 1976).
A pontuação BM25 de um documento é calculada da seguinte forma:


$$\text{score}(D, Q) = \sum_{i=1}^{n} \text{IDF}(q_i) \cdot \frac{f(q_i, D) \cdot (k_1 + 1)}{f(q_i, D) + k_1 \cdot \left(1 - b + b \cdot \frac{|D|}{\text{avgdl}}\right)}$$
Onde:
* $f(q_i, D)$ é a frequência do termo $q_i$ no documento $D$.
* $|D|$ é o comprimento do documento $D$ em número de palavras, e $\text{avgdl}$ é o comprimento médio dos documentos de todo o corpus.
* $k_1$ é um parâmetro de calibração não-negativo que controla o termo de saturação da frequência da palavra (geralmente configurado entre $1.2$ e $2.0$).
* $b$ é um parâmetro entre $0$ e $1$ que dita o grau de penalização baseado no comprimento do documento (geralmente $0.75$).
O componente $\text{IDF}(q_i)$ é a Frequência Inversa do Documento para o termo $q_i$, calculada classicamente como:


$$\text{IDF}(q_i) = \ln \left( \frac{N - n(q_i) + 0.5}{n(q_i) + 0.5} + 1 \right)$$
Onde $N$ é o número total de documentos no corpus e $n(q_i)$ é o número de documentos que contêm o termo $q_i$. O BM25 destaca-se por sua robustez e por não exigir uma fase de treinamento pesado, servindo como uma linha de base estável para sistemas de busca.
2.4 Indexação e Busca Vetorial Escalável: FAISS
À medida que o volume de documentos cresce para a escala de milhões ou bilhões, calcular a similaridade de cosseno ou o produto escalar de maneira exaustiva (força bruta) entre uma query e todos os embeddings do banco de dados torna-se computacionalmente inviável, dado o custo temporal de complexidade $\mathcal{O}(N \cdot d)$. Para solucionar este gargalo, o Facebook AI Research desenvolveu a biblioteca FAISS (Facebook AI Similarity Search), focada na busca eficiente por vizinhos mais próximos aproximados (Approximate Nearest Neighbors - ANN) em espaços de alta dimensionalidade (Johnson et al., 2019).
O FAISS implementa diversas técnicas de indexação e compressão de dados, destacando-se:
1. Inverted File Index (IVF): Particiona o espaço vetorial utilizando o algoritmo de agrupamento K-Means em $k$ centroides. Durante a consulta, o vetor de busca é comparado apenas com os centroides mais próximos, reduzindo drasticamente o espaço de busca de $N$ para uma fração dos vetores pertencentes àqueles clusters.
2. Quantização Vetorial (Product Quantization - PQ): Trata-se de um processo de compressão com perda onde um vetor de dimensão $d$ é dividido em $m$ subvetores de dimensão $d/m$. Cada subvetor é quantizado independentemente em relação a um conjunto de centroides locais. Isso reduz o espaço de armazenamento na memória RAM em até 95%, permitindo que bilhões de vetores sejam mantidos em memória volátil e comparados rapidamente por meio de tabelas de distância pré-calculadas (Asymmetric Distance Computation).
Graças a essas estruturas, o FAISS viabiliza buscas semânticas em tempo submilisegundo, fornecendo a infraestrutura necessária para alimentar aplicações de tempo real.
2.5 Geração Aumentada de Recuperação (RAG)
O framework de Geração Aumentada de Recuperação (Retrieval-Augmented Generation - RAG) unifica os componentes de recuperação não-paramétricos (BM25, buscas baseadas em embeddings via FAISS) com os componentes gerativos paramétricos (LLMs) (Lewis et al., 2020).
Em vez de confiar unicamente no conhecimento estático armazenado nos pesos de um modelo de linguagem, o pipeline do RAG opera em três etapas distintas:






[Consulta do Usuário] 
      │
      ▼
[Etapa 1: Recuperação (Retrieval)] ────► Busca Semântica (FAISS/Embeddings) e/ou Lexical (BM25)
      │
      ▼
[Etapa 2: Aumentação (Augmentation)] ──► Injeção dos Documentos Recuperados no Prompt
      │
      ▼
[Etapa 3: Geração (Generation)] ───────► LLM processa o Contexto + Prompt e gera a Resposta Exata

No modelo matemático formal do RAG, dado um texto de entrada $x$ (a consulta do usuário), o sistema busca um conjunto de documentos de suporte latentes $z$ usando uma função de pontuação de recuperação $P(z|x)$. Posteriormente, o componente gerativo produz a sequência de saída $y$ token por token, condicionada tanto na entrada original $x$ quanto nos documentos recuperados $z$:


$$P(y|x) \approx \sum_{z \in \text{Top-K}(P(\cdot|x))} P(z|x) \prod_{i=1}^{m} P(y_i | x, z, y_{1:i-1})$$
A hibridização da busca (através da fusão de scores do BM25 e da busca semântica do FAISS) garante que o componente de recuperação extraia documentos que possuam tanto correspondência factual exata quanto relevância contextual abstrata. Os documentos selecionados são injetados diretamente na janela de contexto do LLM como fontes de verdade, transformando o papel do modelo de linguagem de uma "memória de fatos" para um "processador de informações em tempo real".
3. Discussão e Análise Crítica
A evolução em direção ao ecossistema RAG resolveu problemas crônicos enfrentados pela comunidade de aprendizado de máquina, mas também introduziu novos desafios teóricos e de engenharia.
A tabela abaixo sintetiza uma comparação analítica abrangente dos métodos discutidos no desenvolvimento deste artigo:
Método / Arquitetura
	Natureza do Modelo
	Representação de Dados
	Complexidade Computacional
	Vantagens Principais
	Limitações Críticas
	Regressão Linear / Logística
	Paramétrico Clássico
	Vetores densos tabulares ou esparsos (Bag-of-Words)
	Baixa: $\mathcal{O}(d^3)$ para treino analítico, linear na inferência
	Extrema interpretabilidade estatística; baixo custo computacional
	Incapaz de processar semântica contextual ou estruturas textuais complexas
	BM25
	Não-paramétrico
	Vetores esparsos baseados em contagem e frequências
	Média: Busca indexada rápida via listas invertidas
	Alta precisão para termos exatos; dispensa treinamento de pesos
	Totalmente cego a sinônimos, contexto e semântica abstrata
	Embeddings densos
	Paramétrico (Extração)
	Vetores contínuos densos (espaços latentes compactos)
	Alta: Dependente de inferências profundas em GPUs
	Captura nuances conceituais, semelhança temática e polissemia
	Alto consumo de memória; vulnerável ao problema de "out-of-vocabulary"
	FAISS
	Estrutura de Indexação
	Estruturas geométricas aproximadas (Gráfos, IVF, PQ)
	Baixa na busca: $\mathcal{O}(\log N)$ ou submilisegundo
	Escalabilidade de busca vetorial para bilhões de itens
	A aproximação (ANN) introduz uma perda marginal de revocação (recall)
	RAG
	Híbrido (Paramétrico + Não-paramétrico)
	Fluxos textuais injetados dinamicamente em LLMs
	Muito Alta: Soma custos de busca, rede e inferência generativa
	Mitigação de alucinações; atualização dinâmica sem re-treinamento
	Latência elevada; sensibilidade à ordenação dos contextos (lost in the middle)
	A literatura aponta que uma das principais discussões atuais gira em torno do equilíbrio entre a busca densa e a esparsa. Embora os embeddings capturem a semântica de forma eficaz, eles tendem a falhar em tarefas de IR industrial onde palavras-chave específicas (como códigos de produtos) ditam a relevância absoluta. Como resultado, os sistemas de ponta utilizam a "Recuperação Híbrida", combinando os scores do BM25 e da busca densa via algoritmos de fusão, como o Reciprocal Rank Fusion (RRF).
Outro desafio de pesquisa proeminente refere-se à vulnerabilidade intrínseca dos LLMs no ecossistema RAG à ordenação dos documentos fornecidos. Estudos indicam que os modelos de linguagem demonstram maior facilidade em extrair informações localizadas estritamente no início ou no fim do bloco de texto fornecido no prompt, fenômeno documentado como o efeito "lost in the middle" (Liu et al., 2024). Desse modo, o desenvolvimento de técnicas de re-ranqueamento (Re-ranking) utilizando modelos Cross-Encoder tornou-se indispensável para garantir que as informações cruciais ocupem os locais de maior atenção matemática dentro do prompt.
4. Conclusão
Este artigo revisou a trajetória de convergência entre as abordagens de aprendizado de máquina estruturadas e as modernas ferramentas de engenharia de busca. Enquanto a regressão linear e logística assentaram os alicerces teóricos dos limites paramétricos, a manipulação de dados não estruturados exigiu novos paradigmas representacionais. Os embeddings contextualizados preencheram a lacuna semântica, o algoritmo BM25 manteve a precisão lexical indispensável, e o framework FAISS viabilizou a infraestrutura matemática para que esse volume de representações contínuas operasse em larga escala.
Por fim, a arquitetura RAG consolida esses marcos tecnológicos ao criar uma simbiose eficiente: delega-se a tarefa de armazenamento de fatos a bases de conhecimento não-paramétricas indexadas e escaláveis, enquanto preserva-se o papel do Grande Modelo de Linguagem exclusivamente para raciocínio, síntese e articulação gramatical. Para trabalhos futuros, aponta-se a necessidade de investigar arquiteturas RAG totalmente ponta-a-ponta (end-to-end), onde os encoders de busca e os decoders de geração sejam treinados de forma conjunta e simultânea, reduzindo a necessidade de heurísticas intermediárias de fusão de dados.
5. Referências Bibliográficas
* HASTIE, Trevor; TIBSHIRANI, Robert; FRIEDMAN, Jerome. The Elements of Statistical Learning: Data Mining, Inference, and Prediction. 2. ed. New York: Springer, 2009.
* JOHNSON, Jeff; DOUZE, Matthijs; JÉGOU, Hervé. Billion-scale similarity search with GPUs. IEEE Transactions on Big Data, v. 7, n. 3, p. 535-547, 2019.
* JURAFSKY, Dan; MARTIN, James H. Speech and Language Processing: An Introduction to Natural Language Processing, Computational Linguistics, and Speech Recognition. 3. ed. draft. Stanford: Stanford University, 2024.
* LEWIS, Patrick et al. Retrieval-augmented generation for knowledge-intensive NLP tasks. In: Advances in Neural Information Processing Systems (NeurIPS), v. 33, p. 9459-9474, 2020.
* LIU, Nelson F. et al. Lost in the middle: How language models use long contexts. Transactions of the Association for Computational Linguistics, v. 12, p. 157-173, 2024.
* MIKOLOV, Tomas et al. Efficient estimation of word representations in vector space. arXiv preprint arXiv:1301.3781, 2013.
* ROBERTSON, Stephen E.; JONES, K. Spärck. Relevance weighting of search terms. Journal of the American Society for Information Science, v. 27, n. 3, p. 129-146, 1976.
* VASWANI, Ashish et al. Attention is all you need. In: Advances in Neural Information Processing Systems (NeurIPS), v. 30, p. 5998-6008, 2017.