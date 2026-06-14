On The Role of Pretrained Language Models in
General-Purpose Text Embeddings: A Survey

MEISHAN ZHANG, Harbin Institute of Technology (Shenzhen), China
XIN ZHANG, Harbin Institute of Technology (Shenzhen), China
XINPING ZHAO, Harbin Institute of Technology (Shenzhen), China
SHOUZHENG HUANG, Harbin Institute of Technology (Shenzhen), China
BAOTIAN HU, Harbin Institute of Technology (Shenzhen), China
MIN ZHANG, Harbin Institute of Technology (Shenzhen), China

Text embeddings have attracted growing interest due to their effectiveness across a wide range of natural
language processing (NLP) tasks, including retrieval, classification, clustering, bitext mining, and summariza-
tion. With the emergence of pretrained language models (PLMs), general-purpose text embeddings (GPTE)
have gained significant traction for their ability to produce rich, transferable representations. The general
architecture of GPTE typically leverages PLMs to derive dense text representations, which are then optimized
through contrastive learning on large-scale pairwise datasets. In this survey, we provide a comprehensive
overview of GPTE in the era of PLMs, focusing on the roles PLMs play in driving its development. We first
examine the fundamental architecture and describe the basic roles of PLMs in GPTE, i.e., embedding extraction,
expressivity enhancement, training strategies, learning objectives, and data construction. We then describe
advanced roles enabled by PLMs, including multilingual support, multimodal integration, code understanding,
and scenario-specific adaptation. Finally, we highlight potential future research directions that move beyond
traditional improvement goals, including ranking integration, safety considerations, bias mitigation, structural
information incorporation, and the cognitive extension of embeddings. This survey aims to serve as a valuable
reference for both newcomers and established researchers seeking to understand the current state and future
potential of GPTE. 1.

CCS Concepts: • Computing methodologies →Natural language processing; • Information systems
→Information retrieval.

Additional Key Words and Phrases: Embedding Model, Large Language Models, Retriever, Retrieval-Augmented
Generation

ACM Reference Format:
Meishan Zhang, Xin Zhang, Xinping Zhao, Shouzheng Huang, Baotian Hu, and Min Zhang. 2018. On The
Role of Pretrained Language Models in General-Purpose Text Embeddings: A Survey. J. ACM 37, 4, Article 111
(August 2018), 45 pages. https://doi.org/XXXXXXX.XXXXXXX

1If you have any suggestions for improvement, please contact mason.zms@gmail.com and hubaotian@hit.edu.cn without
hesitation.

Authors’ Contact Information: Meishan Zhang, mason.zms@gmail.com, Harbin Institute of Technology (Shenzhen),
Shenzhen, China; Xin Zhang, izhx404@gmail.com, Harbin Institute of Technology (Shenzhen), Shenzhen, China; Xin-
ping Zhao, zhaoxinping@stu.hit.edu.cn, Harbin Institute of Technology (Shenzhen), Shenzhen, China; Shouzheng
Huang, huangshouzheng@stu.hit.edu.cn, Harbin Institute of Technology (Shenzhen), Shenzhen, China; Baotian Hu,
hubaotian@hit.edu.cn, Harbin Institute of Technology (Shenzhen), Shenzhen, China; Min Zhang, zhangmin2021@hit.edu.cn,
Harbin Institute of Technology (Shenzhen), Shenzhen, China.

Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee
provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the
full citation on the first page. Copyrights for components of this work owned by others than the author(s) must be honored.
Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires
prior specific permission and/or a fee. Request permissions from permissions@acm.org.
© 2018 Copyright held by the owner/author(s). Publication rights licensed to ACM.
ACM 1557-735X/2018/8-ART111
https://doi.org/XXXXXXX.XXXXXXX

J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.

arXiv:2507.20783v2  [cs.CL]  26 Nov 2025

111:2
Zhang et al.

1
Introduction

Text embeddings are continuous, dense, and fixed-size vectors used to represent discrete, variable-
length texts, enabling large-scale automated computation and analysis of textual data. It is a critical
technology widely applied in natural language processing (NLP) [221] and information retrieval
(IR) [115]. Embeddings can serve as high-level features for various text classification tasks, and
can also be exploited to calculate distances between texts, which is essential for clustering with
algorithms like K-Nearest Neighbors (KNN) [90]. By capturing the semantic meaning of texts
in a vector space, embeddings allow for direct computation of similarity measures (e.g., cosine
similarity), supporting tasks such as retrieval, reranking, semantic textual similarity (STS), and
natural Language inference (NLI). Furthermore, embedding-based retrievers are a key component
of retrieval-augmented generation (RAG) [87, 159, 387], enabling generative large language models
(LLMs) to access up-to-date external knowledge without altering their parameters.
Early works on embeddings include Latent Semantic Indexing (LSA) [66] and Latent Dirichlet
Allocation (LDA) [16]. With the advent of deep learning and word embeddings [212, 246], various
neural network models such as direct pooling, convolutional neural networks (CNNs), and recurrent
neural networks (RNNs), have been developed to generate supervised text representations in the
form of embeddings [107, 131, 142, 153]. These embeddings are typically derived as by-products, as
the primary goal of these models is aimed at a specific downstream task [57]. In parallel, learning
general-purpose text embeddings (GPTE) in an unsupervised, self-supervised, or multiple-task-
supervision manner has attracted significant attention [27, 142, 358]. Such embeddings can be
directly applied to a wide range of tasks in a universal manner, making this line of work a prominent
direction in text embedding research.
Currently, pretrained language models (PLMs) have significantly transformed natural language
processing tasks [69], without any exception for text embeddings as well. For instance, we can
obtain text embeddings by feeding a text into BERT-alike models directly, using the vectorial
representation of ⟨𝐶𝐿𝑆⟩as the full-text embedding. The derived embeddings were unprecedentedly
powerful in strength of general purpose and can be further optimized through supervised fine-
tuning (SFT) [109], following the pretrain-then-finetune paradigm. As PLMs continue to evolve,
from encoder-based [69] to encoder-decoder architectures [257], and more recently to decoder-
only large language models (LLMs) [21], the development of GPTE has also progressed rapidly.
According to the widely recognized MTEB benchmark website2, at least 150 text embedding models
have been released in recent years, reflecting the growing interest and progress in this area.
Text embeddings are conceptually straightforward, and their overall architecture has remained
largely consistent since the introduction of GPTE. Typically, a deep neural network is first initialized
to compose text representations from word embeddings [247]. Then, unsupervised, self-supervised,
or weakly supervised objectives are used to train the network parameters, resulting in GPTE [86].
Finally, task-specific SFT is applied to align the GPTE with the downstream tasks [263], which is an
almost trivial step within the PLM era. Based on the observation, a natural question arises: What
role do PLMs play in advancing GPTE models? The answer lies in examining two distinct angles: (1)
the fundamental role of PLMs in enhancing the capability of GPTE, and (2) their advanced role in
expanding the scope of GPTE applications.
In this paper, we present a comprehensive survey investigating the role of PLMs in GPTE. We
systematically review the representative GPTE models built on PLMs, which aim to offer a clear
and accessible roadmap for understanding recent developments in this field. Section 2 provides
a brief background on GPTE, describing the basic concepts of GPTE and outlining the general
learning architecture to establish a foundation for examining PLM contributions. Subsequently, we

2https://huggingface.co/spaces/mteb/leaderboard

J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.

On The Role of Pretrained Language Models in General-Purpose Text Embeddings: A Survey
111:3

categorize key works of exploring PLMs for text embedding, and describe the successive methods
within each aspect in detail, highlighting the related research efforts in terms of roles in Section 3-4.
Based on our observations and insights, we propose several promising future directions in Section
5, and finally conclude this paper in Section 6. The overall taxonomy of PLMs’ Roles in GPTE is
illustrated in Figure 1.
Several existing surveys are closely related to text embeddings. Among them, surveys on sentence
representations are particularly relevant [172, 260], with the main distinction lying in target
granularity and application scope. Sentence representations typically focus on capturing sentence-
level semantics, while text embeddings are designed for a broader range of texts and applications.
Surveys on the use of PLMs in IR also touch on text embeddings, though their emphasis remains
on IR-specific tasks [98, 314, 385]. The most directly related works include reviews of universal
text embeddings [24] and LLM-empowered text embeddings [229]. The former primarily lists top-
performing models on the MTEB benchmark, whereas the latter offers an overview of LLM-based
methods across several dimensions, which differ significantly from our approach. In contrast, our
survey adopts a unified, architecture-driven perspective, tracing the evolution of PLMs within this
framework. In particular, we give equal emphasis to GPTE models based on BERT-like architectures
since they are still important in real-application settings.

2
Background

2.1
Concept of Text Embeddings
Text is a discrete and variable-length sequence of words, sentences, or paragraphs. To make it
amenable to computation, we employ well-designed models to encode its underlying semantics into
fixed-size vector representations (real-valued vector 𝒆∈R𝑑, 𝑑is the dimension size), called text
embeddings. The embedding model can serve as the foundation of the vector space of texts [269],
enabling the calculation of quantified semantic similarities or distance measures, an essential
capability for semantic understanding and IR. Additionally, the derived embeddings can be leveraged
as high-level semantic features, making them adaptable for a wide range of downstream NLP tasks,
such as classification, clustering, STS, question-answering, and so on [61, 329, 359].

2.2
Applications of Text Embeddings
Text embedding applications can be broadly categorized into three types based on their primary
purpose: semantic similarity, semantic relevance, and semantic encoding. The first two focus on
bi-text semantic computations, where the last type involves representing individual texts as high-
level features for downstream tasks. Semantic similarity typically refers to symmetric tasks where
both texts are treated equally, while semantic relevance addresses asymmetric tasks where one text
is semantically related to another. Additionally, several hybrid cases exist within text embedding
applications. Below, we first introduce the three basic types of applications, and then provide
examples of hybrid applications, illustrated in Figure 2.

2.2.1
Semantic Similarity (SS). This type of application primarily includes STS [28, 29], NLI [20, 57]
and clustering [136, 248], which measures the similarity of semantic details between texts, em-
phasizing homogeneous symmetric relationships. STS and NLI are particularly useful in scenarios
such as detecting duplicate content, recognizing paraphrases, query rewriting, or logic reasoning.
Similarly, text clustering aims to group semantically close documents, which is critical for dis-
covering underlying themes, organizing large text collections, and more. These cases collectively
demonstrate that semantic similarity is a crucial aspect of text embeddings.

J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.

111:4
Zhang et al.

On The Role of PLMs in GPTE

Background (§2)

Concept of
Text Embeddings (§2.1)
A Vector Space Model for Automatic Indexing [269]; Downstream NLP tasks [61, 329, 359]

Applications of
Text Embeddings (§2.2)

Semantic
Similarity (§2.2.1)
STS [28, 29, 110]; NLI [20, 57, 146]; Clustering [88, 136, 248]

Semantic
Relevance (§2.2.2)

IR [98, 200]; QA [134, 150]; RAG [87, 159, 387]; LLM Memory
[241, 390]; Fact Verification [303]

Semantic
Encoding (§2.2.3)

Text Classifiers [61]; Semantic Reasoning Systems [50]; Image
Generators [268]

Hybrid
Combination (§2.2.4)
xRAG [50]; UniRAG [170]; Think-Then-Embed [60]

The General Architecture
of GPTE (§2.3)
CL [39, 143, 231, 339, 383]; Margin-based CL [383]; Momentum Smoothing [279, 340]

Training Dataset (§2.4)
Retrieval [134, 162, 180]; Classification [61, 109, 141]; STS [107, 263]; QA [99, 280]

GPTE Evaluation (§2.5)
MTEB [221]; MMTEB [71]; C-MTEB [344]; SentEval [56]; USEB [315]; SciRepEval [281]

Basic Roles (§3)

Text Embedding
Acquisition (§3.1)
Encoder-based PLMs [69]; Decoder-based PLMs [256]; Pooling [154, 227, 234, 291]

Expressibility
Improvement (§3.2)

Long-Context
Modeling (§3.2.1)

Plug-and-Play Augmentation [36, 287, 394]; Pre-Training
from Scratch [93, 251, 267, 328]

Prompt-Informed
Embedding (§3.2.2)

PromptBERT [124]; PromCSE [127]; PCoTEOL [367]; Echo
[285]; E5-mistral [317]; GritLM [220]; GEM [368]

Parameter
Optimization (§3.3)

Multi-Stage
Training (§3.3.1)

Improving the text embedding quality progressively with
weakly-supervised data and high-quality supervised data
[112, 180, 316, 381, 386]

Objectives Beyond
Contrastive Learning
(§3.3.2)

Joint Training with GPTE Objectives [13, 54, 220, 273, 335, 338];
Matryoshka Representation Learning (MRL) [149]; CoSent [289];
Knowledge distillation [36, 49, 187, 277, 316, 386] etc.

Batch Learning
(§3.3.3)

GradCache [85]; GistEmbed [284]; Activation Checkpointing
[40]; Zero Redundancy Optimizer [258]

Data Synthesis (§3.4)

Training Data
Synthesis (§3.4.1)

Training Data Synthesis [112, 154, 156, 317, 381]; Persona-based
Synthesis [112, 381, 386]; Semantically Similar Text Synthesis
[237, 302, 371]; Negative Synthesis [25, 86, 140, 370, 382, 393]

Evolving Benchmark
(§3.4.2)
AIR-bench [34]

The Choice of PLMs (§3.5)

Comparison of Model
Architectures (§3.5.1)

Encoder-based GPTE [180, 263, 316, 344]; Decoder-based GPTE
[154, 180, 317, 317, 374, 374]

Impact of Model
Scale (§3.5.2)
Scaling Effect (Figure 4); MoE-based GPTE [181, 220, 232]

Advanced Roles (§4)

Multilingualism (§4.1)
Multilingual GPTE Models [35, 78, 112, 119, 228, 318, 359, 376, 378, 381, 386] (Table 4);
Multilingual Training Data [22, 83, 88, 88, 158, 192, 222, 262, 262, 333, 350] (Table 5)

Multimodal (§4.2)
Individual Encoder [122, 165, 166, 255, 306, 361, 366]; Unified Encoder
[91, 128, 145, 152, 207, 301] (Table 6); Multimodal Training Data [33, 379, 392] (Table 7)

Programming Languages
(§4.3)

Code Embeddig Models [4, 79, 95, 96, 126, 132, 133, 151, 249, 265, 323, 327] (Table 8);
Code Training Data [5, 106, 113, 118, 194, 217, 254, 266, 294, 295, 352, 397] (Table 9)

Adaptation for
Specific Scenarios (§4.4)

Instruction-following GPTE [162, 214, 238, 270, 330]; Language-specific GPTE [202, 344];
Domain-specific Adaptation [6, 76, 157]

Expected Role (§5)

Combination with
Text Ranking (§5.1)
Jina-reranker-v3 [311]; Qwen3-Reranker [381]

Safety Considerations
(§5.2)
BadCSE [42]; GEIA [164]; ALGEN [45]; Revealer [373]; TEIA [116]

Bias of GPTE (§5.3)

Debiasing Word Embeddings [17]; Task-diverse Pretraining Regimes [381]; Domain-
adaptive Pretraining [278]; Multilingual Alignment and Language-specific Tuning
[147, 378]; Modality-invariant Representation [274]

Structure Information
(§5.4)
Tables [360]; Codes [79]; Knowledge Graphs [321]

Extending GPTE with
Reasoning (§5.5)
Think-Then-Embed [60]; O1-Embedder [351]

Fig. 1. Taxonomy of PLMs’ Roles in GPTE.
J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.

On The Role of Pretrained Language Models in General-Purpose Text Embeddings: A Survey
111:5

Fig. 2. Four typical applications of text embedding.

2.2.2
Semantic Relevance (SR). This type corresponds to IR [98, 200] and QA [134, 150] mainly,
where the goal is to search relevant documents or passages given a query, for instance, finding
a text that can answer a specific question. IR has been one of the most widely applied topics
for text embeddings. This task is typically formulated as a scoring problem, where documents
with the highest semantic relevance scores are returned as candidates for the query. Retrieval
can be employed in various scenarios, such as question answering [134], prompt retrieval [47],
RAG [87, 159, 387], LLM memory [241, 390], fact verification [303] etc.

2.2.3
Semantic Encoding (SE). This line of applications involves using text embeddings as feature
inputs for various downstream models, such as text classifiers [61], semantic reasoning systems [50],
and image generators [268]. Compared with traditional features, text embeddings are more ex-
pressive with reduced dimensions and high-level textual semantics, leading to better performance
in downstream tasks [61]. The RAG models could also benefit from text embeddings, where the
retrieved documents could be replaced with tailored embeddings as inputs for LLMs [50, 261].

2.2.4
Hybrid Combination. There are special cases where different types of applications are com-
bined [50, 60, 170]. For example, xRAG [50] suggests directly inputting the retrieved text embeddings
into the LLMs, where the embeddings are used both for text retrieval and as feature inputs. As the
capabilities of GPTE continue to evolve, we expect to see more hybrid applications in the future,
largely due to the increasingly complex real-world scenarios that we are already able to resolve.

2.3
The General Architecture of GPTE

Fig. 3. The typical architecture and train-
ing manner of GPTE models.

The task of text embedding requires a sophisticated model to
possess a deep understanding of text. A straightforward ap-
proach involves constructing a neural network from scratch
to encode the input sequence of words into a fixed-size
embedding. The central challenge then lies in effectively
learning the model parameters. Inspired by the success of
general-purpose PLM backbones in NLP, GPTE has garnered
considerable attention. These embeddings offer strong gen-
eralization for real-world, open-domain settings and can
be further fine-tuned for specific tasks, aligning with the
pretrain-then-finetune paradigm of PLMs. Consequently,
parameter learning typically involves multiple stages, where
we focus on GPTE, ignoring the last step of SFT for specific
tasks.
Figure 3 illustrates the mainstream architecture for pre-
training GPTE through a supervised approach. Typically, the textual word sequence is fed into

J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.

111:6
Zhang et al.

Table 1. Text embedding training datasets.

Quality Type
Datasets

Low

SS

Amazon Reviews [108], WikiHow [148], NLLB [104, 298], MNLI [334], SNLI [20], ArXiv-Clustering,
Biorxiv-Clustering, Medrxiv-Clustering, Reddit-Clustering [88, 262], StackExchange-Clustering [88, 286],
XL-Sum [102]

SR

MS MARCO [226], Common Crawl, ClueWeb [239], GooAQ [137], Yahoo Answers, Wikipedia [83],
Stack Exchange, PAQ [160], CC-News [100], Reddit, S2ORC, x3P [222], pubMedQA [129], arxiv_qa,
SQuAD [259], DBPedia [300]. BERRI [8], MEDI [288]

High

SS

LCSTS [110], STS12 [11], STS22 [43], STSB [28], ContractNLI [146], MultiNLI [334], Quora [65], WikiAn-
swers [74], SimCSE NLI [86], AFQMC, ATEC, BQ, CAIL2029-SCM [342], CINLID, ChineseSTS [297]

SR

FEVER [303], HotpotQA [357], Natural Questions [150], WebQA [30], SciFact [309], ChatMed-
Dataset [398], LIMA [391], T2Ranking [345], RefGPT [353], TriviaQA [130], FiQA [199], BioASQ [305],
DuReader [103], DuReaderchecklist [296]

SE

EmotionClassification [271], ToxicConversations, TweetSentimentExtraction, AmazonPolarity [206],
IMDB [198], banking77 [26], CSL [179], THUCNews [292], TNews, JDReview, IFlyTek [388], OnlineShop-
ping, Waimai

a well-established PLM backbone (the key neural network is transformers), generating hidden
contextual representations of words. Following this, a pooling step aggregates these word-level
hidden vectors into a single vector, yielding the embedding form of the input text. Once the em-
bedding network is ready, the subsequent phase involves further optimization beyond the PLM’s
initial capabilities, for which contrastive learning (CL) is the widely-accepted supervision objec-
tive [39, 143, 231, 339, 383]. This learning process can be self-supervised, weakly-supervised, or
high-quality supervised through bi-encoder semantic computation. Despite potential innovations
such as reinforcement learning that could be exploited, this supervised paradigm remains the
predominant architecture for nearly all current models.
Formally, the CL aims to optimize GPTE through text-pair similarity calibration. Given an anchor
text 𝑥(often the query text in IR), first, we provide one positive text 𝑦+ which is relevant to 𝑥. Based
on the positive pair, then we construct a set of negative (e.g., irrelevant) samples 𝑦−
𝑖(𝑖∈[1, 𝑁]) of
𝑥. Finally, the standard InfoNCE loss [236] is adopted, maximizing the agreement of positive pairs
and meanwhile minimizing that of negative pairs:

LInfoNCE = −log
𝑒𝑠(𝒙,𝒚+)/𝜏

𝑒𝑠(𝒙,𝒚+)/𝜏+ Í𝑁
𝑖=1 𝑒𝑠(𝒙,𝒚−
𝑖)/𝜏,
(1)

where 𝒙and 𝒚denote the embeddings of 𝑥and 𝑦calculated by the embedding network, 𝑠(𝒙,𝒚)
is the similarity function, normally cosine similarity or dot product, and 𝜏is the temperature. By
design, CL encourages the embedding space to bring anchor-positive pairs closer while pushing
anchor-negative pairs farther apart. Besides the above standard CL, there are also several strategies
to better CL optimization, e.g., margin-based CL [383] and momentum smoothing [279, 340]. For
these studies, we will not discuss them as they are not the main points in this survey.

2.4
Training Dataset
Previous studies often adopt multi-task supervision to train text embeddings using diverse task-
specific objectives—including classification [61, 109, 141], STS [107, 263], question answering [99,
280], and text retrieval [134, 162, 180]—spanning various GPTE-based applications with supervised
datasets available. In fact, nearly all of these datasets can be reformulated into text-pair formats,

J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.

On The Role of Pretrained Language Models in General-Purpose Text Embeddings: A Survey
111:7

enabling CL to emerge as a universal paradigm for training GPTE as mentioned in Section 2.3.
First, Semantic similarity and relevance datasets such as the manually-refined MS MARCO [226],
PQA [160], MNLI [224], SNLI [20], DBPedia [300], are naturally well-suited for CL pretraining.
Furthermore, the datasets targeting feature representation tasks can also be adapted for CL. For
instance, in text classification, texts sharing the same label can form positive pairs, and in semantic
reasoning tasks, instructionresponse pairs can serve the same purpose. In addition to these high-
quality resources, relatively lower-quality yet large-scale corpora crawled from the web are also
widely used. These include title-body pairs from regular web pages, title-abstract pairs from
academic papers, postcomment pairs from social media, questionanswer pairs from community QA
forums, text-code pairs from GitHub, and other text pairs generated via retrieval. Table 1 presents
a summary of these representative training datasets.

2.5
GPTE Evaluation

The evaluation of text embeddings is critically important, as it directly guides the development of
GPTE. In the early stage, text embeddings were evaluated independently using various benchmark
datasets. One of the earliest datasets, SentEval [56], was introduced to evaluate embeddings on
tasks such as classification, STS, and NLI. Subsequently, USEB [315] was proposed to focus on the
reranking task, and BEIR [300] was constructed for zero-shot information retrieval evaluation. Fur-
ther, SciRepEval [281] was developed for evaluating scientific document representations, covering
24 realistic tasks across classification, regression, ranking, and search.
Recently, MTEB has emerged as a unified benchmark encompassing all major types of embedding
tasks, serving as the primary framework for evaluating various GPTE models. To date, MTEB has
undergone several iterations and includes a wide array of datasets across different languages,
e.g., 56 datasets for the English language [221], 35 datasets for Chinese [344], 25 datasets for
French [55], 17 datasets for Polish [252], 12 code retrieval tasks for MTEB (code) [71], etc. Building
upon MTEB [221], MMTEB [71] extends multilingual evaluation to over 250 languages, offering a
diverse set of more than 500 systematically curated tasks for evaluating text embedding models.
The construction of MTEB and MMTEB is still ongoing, continuously expanding to include broader
task types, languages, and domains, with increasing levels of difficulty. Notably, specific efforts
for language expansion include C-MTEB [344] for Chinese, SEB [72] for Scandinavian languages,
PIRB [62] for Polish, and ruMTEB [283] for Russian, BEIR-NL [12] for Dutch, and Hindi-BEIR [2]
for Hindi.

3
The Basic Roles of PLMs

Since the introduction of ELMo [247], PLMs have remained a central focus in the NLP community
due to their remarkable performance. Models such as BERT [69] and GPT [256] have significantly
advanced the overall capabilities of NLP [313]. In the context of text embeddings, PLMs, particularly
BERT-like architectures, have become the primary approach for enhancing embedding quality
[134, 263]. Given that PLMs are inherently general-purpose and follow the pretrain-then-finetune
paradigm, text embeddings derived from them naturally inherit this generalizability [288, 316].
Here, we build upon the aforementioned general architecture in Section 2 to examine the role
of PLMs in advancing GPTE. Table 2 shows the representative GPTE models with their detailed
architecture information.
This section is organized as follows. First, we provide a detailed overview of how text embeddings
are extracted from PLMs (§3.1), which serves as the foundational step in leveraging PLMs for GPTE.
Next, we examine approaches for improving embedding expressibility in the context of different
PLMs for GPTE (§3.2). Third, we present recent advancements in optimization techniques, describing
various learning objectives to obtain better GPTE (§3.3). Fourthly, we describe the development of

J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.

111:8
Zhang et al.

Table 2. Representative open-source GPTE models (English-centered), where only models released on Hug-
gingface with detailed and clear documentation are listed. New Abbreviations: M.S. = multistage training;
MNTP = masked next token prediction training; COS = cosine objective.

Model
PLM
Release
Param.
Embed.
Max
Embed.
Learning
Series
Base
Time
Size
Dim.
Tokens
Acqui.
M.S.
Object.

GTE
(Advancing)

BERT
2023-07 [180] 33M∼335M
384∼1024
512
mean
✓
CL
GTE-MLM
2024-04 [378] 137M/434M
768/1024
8192
first
✓
CL+MRL+LEX
Qwen1.5
2024-04 [180]
7.72B
4096
32768
last
✓
CL+MRL+LEX
Qwen2
2024-06 [180] 1.78B/7.61B
1536/3584
32768
last
✓
CL+MRL+LEX
Qwen3
2025-06 [381]
0.6B∼8B
1024∼4096
32768
last
✓
CL+MRL+LEX

E5

BERT
2022-12 [316] 33M∼335M
384∼1024
512
mean
✓
CL+KD
BERT
2023-05 [316] 33M∼335M
384∼1024
512
mean
✓
CL+KD
BERT
2024-04 [394]
109M
768
4096
mean
✓
CL
Mistral
2023-12 [317]
7.11B
4096
4096
last
×
CL

BGE

BERT
2023-08 [344] 33M∼335M
384∼1024
512
first
✓
CL
BERT
2023-09 [344] 33M∼335M
384∼1024
512
first
✓
CL
Mistral
2024-07 [162]
7.11B
4096
4096
last
✓
CL+KD
Gemma
2024-07 [162]
9.24B
3584
8192
last
✓
CL+KD

Jina
T5-Enc
2023-07 [92]
14M∼335M
312∼1024
512
mean
✓
CL
JinaBERT
2023-10 [93]
33M/137M
512/768
8192
mean
✓
CL
XLM-R
2024-09 [287]
572M
1024
8192
mean
✓
CL+MRL

Nomic
NomicBERT 2024-02 [233]
137M
768
8192
first
✓
CL
NomicBERT 2024-02 [233]
137M
768
8192
first
✓
CL+MRL
XLM-R MoE 2025-02 [232]
305M
768
512
first
✓
CL+MRL

LLM2Vec
LLaMA-2
2024-04 [13]
7B
4096
4096
mean
✓
CL+MNTP
LLaMA-3
2024-04 [13]
8B
4096
8192
mean
✓
CL+MNTP
Mistral
2024-04 [13]
7B
4096
32768
mean
✓
CL+MNTP

KaLM
Qwen2
2024-12 [112]
0.49B
1024
512
last
×
CL+MRL
Qwen2
2025-06 [386]
0.49B
1024
512
last
✓
CL+MRL

ST5
T5-Enc
2021-12 [227] 110M∼4.8B
768/1024
512
mean
✓
CL
T5-EncDec
2021-12 [227]
220M∼11B
768/1024
512
Dec-first
✓
CL
BERT
2024-04 [210] 22M∼335M
384∼1024
512
first
✓
CL
snowflake
NomicBERT 2024-04 [210]
137M
768
8192
first
✓
CL
arctic
GTE-MLM
2024-12 [362]
304M
768
8192
first
✓
CL+MRL
XLM-R
2024-12 [362]
568M
1024
8192
first
✓
CL+MRL

CDE
NomicBERT 2024-10 [216]
281M
768
512
mean
✓
CL
ModernBERT 2025-01 [216]
306M
768
512
mean
✓
CL

GritLM
Mistral
2024-02 [220]
7.24B
4096
4096
mean
×
CL+NTP
Mistral
2024-02 [220] 46.7B (8x7B)
4096
32768
mean
×
CL+NTP

NV-Embed
Mistral
2024-05 [154]
7.85B
4096
4096
Latent
✓
CL
Mistral
2024-08 [154]
7.85B
4096
32768
Latent
✓
CL

DiffCSE
BERT
2022-05 [54]
110M
768
512
first
✓
CL+RTD
RoBERTa
2022-05 [54]
125M
768
512
first
✓
CL+RTD

EASE
BERT
2022-12 [231]
110M
768
512
first
✓
CL
RoBERTa
2022-12 [231]
125M
768
512
first
✓
CL
DeCLUTR
BERT
2022-08 [89]
125M
768
512
first
✓
CL+MLM
UAE
BERT
2023-12 [175]
335M
1024
512
first
✓
CL+COS+AnglE
Granite
RoBERTa
2024-12 [9]
30M∼278M
384∼768
512
first
✓
CL
GTR
T5-Enc
2021-12 [228] 110M∼4.8B
768/1024
512
mean
✓
CL
Instructor
GTR(T5-Enc) 2022-12 [288] 110M/335M
768/1024
512
mean
✓
CL
SGPT
Bloom
2022-08 [219]
7.07B
4096
512
mean
×
CL
Udever
Bloom
2023-10 [374] 560M∼7.07B 1024∼4096
512
last
×
CL
SFR-Embed
Mistral
2024-01 [208]
7.11B
4096
32768
last
✓
CL
Echo
Mistral
2024-02 [285]
7.11B
4096
32768
last
×
CL
Linq-Embed
Mistral
2024-05 [52]
7.11B
4096
32768
last
✓
CL
SPEED
Mistral
2024-11 [32]
7.11B
4096
32768
last
×
CL

J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.

On The Role of Pretrained Language Models in General-Purpose Text Embeddings: A Survey
111:9

data synthesis for the training and evaluation with the support of PLMs (§3.4). Finally, we compare
GPTE across various types of PLMs, highlighting the key factors that influence their performance
(§3.5).

3.1
Text Embedding Acquisition
To date, most PLMs adhere to a unified transformer-based architecture in which word-level rep-
resentations are interconnected through attention mechanisms, allowing each token to attend to
others within the sequence and thereby generating contextualized word representations [307].
Encoder-based PLMs employ bidirectional attention to aggregate contextual information [69], while
decoder-based PLMs utilize causal (unidirectional) attention to construct representations in an
autoregressive manner [256]. Encoder-decoder PLMs use a mixture of them. Regardless of the
underlying architecture, a pooling strategy is typically employed to produce a fixed-size vector
that serves as the embedding of the entire text: 𝒙= Í𝑛
𝑖=1 𝜶𝑖𝒙𝑖, where 𝒙𝑖is the hidden vector
representation of word 𝑤𝑖in text 𝑥. The hidden vector is often the last layer neural representation
of PLMs.
When using encoder-based PLMs, e.g., BERT [69] and RoBERTa [190], the representation of
the first token (i.e., ⟨CLS⟩, where 𝛼1 = 1 and all other 𝛼𝑖= 0) is typically adopted as the full text
representation. These models leverage bidirectional attention, allowing each token to attend to
all others in the input sequence and thereby enabling the first-token representation to capture
rich contextual information from the entire text. However, relying solely on the ⟨CLS⟩token may
introduce bias. To address this, mean pooling (i.e., 𝛼𝑖= 1

𝑛) is often employed as a more balanced
alternative. In some scenarios, max pooling is also used, and in particular, attentive pooling, e.g.,
incorporating an additional latent attention layer for representation aggregation, can further
enhance the quality of the resulting text embedding [154].
For encoder-decoder models such as T5 [257], pooling is typically performed in a manner
similar to encoder-based PLMs. By feeding the full text into the encoder component only, the same
pooling strategies, such as using the ⟨CLS⟩token or mean pooling, can be employed to obtain text
embeddings. Additionally, there are several studies that attempt to leverage the decoder component.
By using the start token in the decoder as the anchor for embedding extraction while ignoring the
remainder of the decoding process, it is feasible to produce reasonable full-text embeddings [227].
Decoder-only LLMs have revolutionized the field of NLP, achieving remarkable success across
a wide range of tasks such as machine translation, question answering, and semantic reasoning.
However, their inherent causal attention mechanism presents a unique challenge for text embedding,
which makes it challenging to derive a single comprehensive vector that fully captures the semantic
meaning of the input text. Only the final token possesses the complete contextual information,
making it the most reasonable choice for representation. As a result, last-token pooling (i.e., 𝛼𝑛= 1,
with all other weights being zero) is the most common strategy for extracting text embeddings
from decoder-only LLM models.
However, relying solely on the final token’s representation may fail to capture the exhaustive
semantic nuances of longer and more complex texts. To overcome this limitation, researchers
have begun exploring more sophisticated aggregation strategies. One natural extension involves
averaging the representations of multiple tokens from the tail of the sequence [219], i.e., 𝒙=
Í𝑛
𝑖=𝑘
1
𝑛−𝑘+1𝒙𝑖, where 𝑘marks the starting index of the tail segment used for aggregation. This
“partial pooling” approach seeks to incorporate a broader contextual window, potentially yielding
more robust and semantically expressive text embeddings.
Several studies argue that relying solely on the final-layer token representations in PLMs may be
insufficient for obtaining robust text embeddings [291]. To address this, a stack of multiple layers
(i.e., Top-K layers) can be leveraged to capture richer contextual information. A straightforward

J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.

111:10
Zhang et al.

approach to combine these layers is simple average aggregation, while more advanced methods
involve trainable multi-layer pooling modules to integrate information across layers [234]. After
this multi-layer aggregation, another token(word)-wise pooling is applied over the resulting word
representations to generate the ultimate text embeddings.

3.2
Expressibility Improvement
3.2.1
Long-Context Modeling. Early BERT-style encoder models typically support sequences of
up to 512 tokens, which falls short given the demand for longer text processing. To overcome
this limitation, many studies [220, 225, 317] have adopted PLM backbones that natively support
extended contexts such as recently-released decoder-only LLMs. Despite decoder-only models
having gained considerable traction due to their inherent capacity for long-context understanding,
substantial research continues to focus on extending the context length of existing encoder-based
models [36, 92, 233, 359, 394], since these GPTE models still remain highly practical and effective
in real-world applications. These efforts generally follow two main strategies: plug-and-play
augmentation or full-scale pre-training from scratch.
Plug-and-Play Augmentation. One quick solution for extending context length is to make low-cost
adaptations to existing models. For instance, BGE-M3 [36] significantly extends XLM-RoBERTa’s
context window to 8192 tokens. It achieves this by first replicating the learned position embeddings
multiple times, and then continues pre-training on longer sequences using RetroMAE [343]. Alterna-
tively, LongEmbed [394] and Jina-Embeddings-v3 [287] demonstrate how BERT and RoBERTa can
be enhanced for longer contexts by integrating RoPE [290] and performing contrastive pre-training.
These approaches demonstrate that even without architectural modifications, existing encoders
can be efficiently adapted to support much longer contexts.
Pre-Training from Scratch. Beyond adapting existing PLMs, many efforts have focused on
modifying the transformer architecture to develop new encoder-only models from scratch that
support longer contexts. These approaches typically build on encoder-based PLMs like BERT due to
their relatively low training costs. For instance, MosaicBERT [251] and JinaBERT [93] replace the
positional embedding of BERT with Alibi positional bias [253], enabling robust inference on longer
sequences than those seen during training3; In contrast, nomicBERT [233], GTE-MLM [359] and
ModernBERT [328] adopt Rotary Position Embeddings (RoPE) [290], which have generally shown
superior performance over Alibi. Additionally, some research has also explored non-transformer-
based models to support long contexts, like M2-BERT [267].

3.2.2
Prompt-Informed Embedding. Most methods of text embedding acquisition discussed in Sec-
tion 3.1 essentially perform a selective averaging of token-wise embeddings, effectively producing
an extractive summarization of the full text. This perspective introduces a novel paradigm for GPTE
based on text summarization or compression. The core idea is to condense the original text into a
few representative words and then use the embeddings of these words to represent the full text.
This paradigm can be effectively realized through prompt learning, a technique widely used in
PLM reasoning. PromptBERT [124] is among the earliest attempts to leverage prompts for inducing
text embeddings. With a template such as “[TEXT] means [MASK] .”, where “[TEXT]” denotes
the input text and “[MASK]” is the summarized special symbol, we can use “[MASK]” to extract
text embeddings. In addition, soft prompts are also investigated in the work of PromCSE [127],
while unlike PromptBERT, this work aims to learn better GPTE embeddings from the optimization
perspective.
The method has received great attention in the era of auto-regressive LLMs [47, 63, 332, 400]. PCo-
TEOL [367] uses a more sophisticated prompt with chain-of-thought: “After thinking step by step,

3MosaicBERT [251] explored these improvements first, but they did not develop embedding models.

J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.

On The Role of Pretrained Language Models in General-Purpose Text Embeddings: A Survey
111:11

this sentence : [TEXT] means in one word: [MASK].” Echo [285] proposes a repetition-style prompt:
“Rewrite the sentence: [TEXT], rewritten sentence: [TEXT]”, where both “[TEXT]” placeholders
contain the same text. The text embedding is obtained by averaging the token representations of
the second occurrence. In fact, the prompt can be highly flexible within this paradigm and can be
naturally extended to instruction-following text embeddings, such as E5-mistral [317].
GritLM [220] and GEM [368] further advance this line of work by adopting generalized prompt
formats to unify the prompt-based embedding acquisition. “[prefix] [special tokens] [suffix]” is
an effective example, where “[prefix]” includes the input text along with an instruction, “[special
tokens]” are a manually-defined symbol sequence used to extract the embeddings, and “[suffix]”
provides the corresponding response to the instruction. Under this paradigm, we can exploit
variable instruction-following tasks such as text reconstruction and summarization to obtain text
embeddings. Notably, even when only the “[prefix]” (i.e., the input text) and “[special tokens]” are
retained, the resulting embeddings remain strong. This approach essentially treats embedding as
a form of text compression, using a small set of “[special tokens]” to denote the semantics of the
entire text [218].

3.3
Parameter Optimization
3.3.1
Multi-Stage Training. Directly using the PLM parameters is the most initial way for GPTE
models with PLM backbones. However, it is evident that the GPTE performance can be significantly
enhanced through further parameter tuning. Before, we have introduced that supervised contrastive
learning with high-quality data is a common way for parameter tuning. As previously discussed
in Section 2, supervised CL on high-quality datasets remains a common and effective strategy
for this purpose. With the rising popularity of weakly supervised and self-supervised paradigms,
researchers have also begun to explore these approaches for GPTE, adopting multi-stage training
pipelines to refine the text embedding quality progressively [180, 316].
The core idea of multi-stage training is to train the model step-by-step, from coarse to fine, taking
full advantage of different types of data and gradually improving the model’s generalization ability
and task-specific performance. Generally, we divide the data into two types: (1) Weakly-supervised
data: with huge size (e.g., billions of pairs) and relatively low costs, these data provide extensive
semantic associations and contextual coverage, which helps models learn basic, generalized semantic
representations. However, its annotation signal is noisy, and the task definition is vague. (2) High-
quality supervised data: with thousands to millions of pairs and high cost, these data deliver precise,
high-quality task-specific signals that can directly guide the model in learning how to generate
optimal embeddings under a particular task or instruction.
The first pre-finetuning stage begins by selecting a robust pre-trained model as the starting
point and further enhancing its semantic representation abilities with massive weakly super-
vised datasets. This process enables the model to learn broad correlations across diverse textual
pairs, thereby establishing a strong basis for subsequent fine-tuning. On top of the model after
pre-finetuning, the second finetuning stage is performed using high-quality, task-specific, and
instruction-specific fine-labeled data. The core goal for the model is to generate different rep-
resentations optimized for a specific task under different instructions, and distinguish between
semantically highly similar but practically mismatched texts with fine-grained discrimination.

3.3.2
Objectives Beyond Contrastive Learning. Although the CL training has unified a number of
GPTE tasks, such as classification, STS, NLI, retrieval, question-answering, instruction-following,
etc., there are still other strategies to strengthen text embeddings. For example, the original PLM-
related objectives, such as masked language model (MLM), replaced token detection (RTD), next
token prediction (NTP), and masked nexttoken prediction (MNTP), can be adopted joint training

J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.

111:12
Zhang et al.

with the GPTE objectives [13, 54, 220, 273, 335, 338]. By the method, the GPTE can be greatly
enhanced with better generalization capability. In addition, Matryoshka Representation Learning
(MRL) [149] is one widely-adopted objective beyond CL, enabling the creation of hierarchical,
multi-scale text embeddings. The core idea is to encode coarse-grained information in the initial
dimensions of the embedding vector and progressively add finer details in subsequent dimensions.
Instead of optimizing a single loss value based on the full-sized embedding, MRL computes and
sums the losses for various truncated versions of the embedding.
There are also several other cosine-based similarity objectives [289] which differ from the CL
objective. The angle objective [175] (AnglE) is proposed to solve the saturation zone problem
of cosine-based (COS) similarity objectives. With a combination of the original objective of CL,
it can optimize the angle difference in complex space to mitigate these adverse effects. Several
studies introduce the lexicon-based sparse embeddings [81, 82] into the GPTE training, where
each dimension of the vector corresponds to the weight of a token. This lexicon-aligned, more
interpretable sparse representation (LEX) could effectively enhance the retrieval performance for
long text inputs [36, 378, 400]. Knowledge distillation (KD) from a cross-encoder (reranking) teacher
model has also been explored [36, 49, 187, 277, 316]. We could optimize the KL divergence loss
towards soft labels from the teacher model to learn more precise semantic relations.
In addition to supervised approaches, there are several methods struggling to learn GPTE without
relying on task-specific supervision. IS-BERT [380] introduces a self-supervised objective based on
mutual information maximization. BERT-flow [161] applies normalizing flows to transform the
anisotropic embeddings from BERT into a smooth and isotropic Gaussian distribution. Whiten-
ingBERT [114] employs a whitening transformation, a simple yet effective linear transformation
method, to improve embedding quality. SBERT-LP [213] enhances semantic structure preservation
by incorporating a locality-preserving loss. Meanwhile, SCD [143] proposes a joint objective that
combines self-contrastive learning with decorrelation, leveraging variations induced by differ-
ent dropout patterns. These methods collectively highlight the potential of unsupervised and
self-supervised strategies in improving the quality of text embeddings.

3.3.3
Batch Learning. Under the batch learning setting, training GPTE models with the CL objective
batch differs from standard deep learning tasks. The key reason lies in the construction of in-batch
negatives for CL. Given a batch of positive text pairs (i.e., ⟨𝑞1,𝑑1⟩, ⟨𝑞2,𝑑2⟩, · · · , ⟨𝑞𝑛,𝑑𝑛⟩), we can
randomly sampling in-batch negatives such as ⟨𝑞𝑖,𝑑𝑗⟩𝑖≠𝑗, and ⟨𝑞𝑖,𝑞𝑗⟩𝑖≠𝑗. However, this method
may introduce semantic noise, including false negatives and low-relevance samples, which can
hinder the CL training. To address this, recent work GistEmbed [284] proposes to use a small but
strong guide model to evaluate semantic similarity within a batch, enabling the selection of more
informative negatives. This guided in-batch negative selection improves training efficiency, reduces
noise, and enhances embedding quality with minimal computational overhead.
Further, according to the practice view, we prefer a large batch size in CL for training GPTE [225].
For instance, E5 [316] utilizes a batch size of 32,768. Batch sizes in the tens of thousands far exceed
the memory capacity of a single GPU. To carry out training with such large batch sizes, multi-
GPU distributed training is necessary—the more GPUs, the larger the batch size you can run.
However, due to resource constraints, one cannot always expand the number of GPUs, which
makes performance optimization techniques to increase the batch size on a single GPU essential.
Common techniques include gradient checkpointing (also known as activation checkpointing [40])
and the zero redundancy optimizer [258] of DeepSpeed 4. Sometimes one cannot use gradient
accumulation, while GradCache [85] provides similar functionality. It does this by extracting and
accumulating all embeddings in sub-batches and recomputing gradients, which delivers the same

4https://github.com/microsoft/DeepSpeed

J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.

On The Role of Pretrained Language Models in General-Purpose Text Embeddings: A Survey
111:13

loss and gradient updates. Although GradCache can execute contrastive learning with very large
batch sizes on a limited number of GPUs, it is not generally recommended as a first resort and only
explored by a few models [233]. This is because it introduces at least double the additional model
forward computation, making it a less ideal choice in a pre-training context where efficiency is
key.

3.4
Data Synthesis

The rise of PLMs has made data synthesis and augmentation increasingly popular for task-specific
optimization, which is further propelled by LLMs. GPTE has also benefited from this line [185,
319, 320, 337, 337], with numerous studies focusing on generating synthetic positive text pairs and
designing specialized negative examples to enhance CL training.

3.4.1
Training Data Synthesis. Developing text embedding models often necessitates vast amounts
of high-quality training data, particularly for supervised fine-tuning. However, acquiring large-scale,
labeled datasets can be expensive and time-consuming. To address this issue, many works [112,
154, 156, 317, 381] resort to LLMs to synthesize training data. Table 3 shows the representative
training datasets by LLM synthesis. Generally, each training entry for text embedding consists
of three parts: anchor, positive, and negative. The anchor serves as the query, the positive text is
semantically relevant or similar to the anchor, and the negative text is semantically irrelevant or
dissimilar to the anchor. Next, we discuss how LLMs synthesize data from these three parts.
Compared with traditional data construction, utilizing LLM to synthesize data is less costly
and ensures data quality and diversity, where LLM can generate data for specific tasks, languages,
and difficulties according to instructions. E5-Mistral [316] uses a two-stage prompt: the first
stage uses GPT-4 to generate diverse task descriptions (such as short text-long text matching),
and the second stage generates specific samples including queries, positives, and hard negatives.
Qwen3-embedding [381] uses Qwen3-32B to synthesize 150 million pairs covering query types,
difficulty, and 119 natural and programming languages for pre-fine-tuning, and filters out 12 million
high-quality data pairs for fine-tuning. Gemini Embedding [155] employs Gemini to filter low-
quality examples, determine relevant positive and negative passages for retrieval, and generate rich
synthetic datasets. LLM-synthesized data has become the core driving force behind text embedding
model training.
Anchor Text. The anchor text serves as the initial query from which a text embedding model
learns to identify positive and negative text. When synthesizing data using LLMs, anchors are
typically generated to diversify the input space and create challenging queries. Initial attempts [154,
156, 317] primarily involve prompting LLMs to generate anchors based on the given document or
conditions, e.g., specific task types. Furthermore, some works [112, 381] incorporate ‘persona’ and
‘difficulty’ into generation to increase the diversity and difficulty of the generated data. In short,
these synthesized anchors expand the semantic coverage and improve the robustness of learned
text embeddings.
Positive Text. Positive samples can be semantically relevant and similar to the anchor. The
semantically similar text primarily lies in STS, where the anchor and positive text are symmetric.
LLMs are extensively employed to synthesize semantically similar texts by setting conditions [371],
enriching text [237], summarizing [302], etc. Conversely, the semantically relevant text is usually
asymmetric, where the anchor and positive text are the query and document, respectively. Here,
LLMs play a role in generating either queries from documents or generating both of them simulta-
neously. Many works [19, 63, 196] leverage LLMs’ capacity to generate queries from vast document
collections. Beyond this, some works [240, 317] generate both queries and documents based on
specific instructions.

J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.

111:14
Zhang et al.

Table 3. Representative studies of GPTE data synthesis. We only include studies that regard LLM data
synthesis as one of their primary contributions.

Category
Methods
LLMs

Text Pairs (𝑥, 𝑦+/𝑦−)

Promptagator [63]
FLAN-T5
LLM4DE[196]
Alpaca/TK-instruct
SKICSE [237]
LLaMA2
SPTAR [245]
LLaMA/Vicuna
Denosent [322]
ChatGPT
CLAIF [48]
GPT3
Qwen3-Embedding [381]
Qwen3

Text Triples (𝑥, 𝑦+, 𝑦−)

SumCSE [302]
Vicuna
AdaptCL [347]
WizardLM
GenSE [46]
T5
SynCSE [371]
ChatGPT/GPT4
MultiCSR [312]
ChatGPT/FLAN-T5
NLI-GEN [272]
LLaMA2
InPars [19]
ChatGPT
InPars-v2 [121]
GPT-J

Instructed Triples (𝐼◦𝑥, 𝑦+, 𝑦−)

I3 [240]
ChatGPT
Promptriever [63]
LLaMA3/GPT4o
Gecko [156]
N/A
E5mistral [317]
ChatGPT/GPT4
FollowIR [331]
ChatGPT

Negative Text. Negative samples play a pivotal role in CL training. Initially, soft negatives,
generated through feature transformations such as representation mixing, utilizing lower-layer
representations or clustering, are considered effective for generating a large number of nega-
tives [25, 38, 68, 86, 140, 370, 382, 393]5. Recently, with the remarkable generative capabilities
of LLMs, synthetic hard negatives have gained growing interest. These hard negatives refer to
query-passage pairs that are semantically similar yet practically mismatched. In the fine-tuning
stage, deliberately mining and incorporating such challenging negative examples is key to boosting
the GPTE performance. LLM-based methods for synthesizing hard negatives generally fall into two
categories, based on the application tasks of GPTE. First, hard negatives for symmetric tasks, which
aim to generate contradictory texts to the anchor [168, 272, 347], prompt GPTE models to capture
subtle semantic distinctions beyond surface-level features. Second, hard negatives for asymmetric
tasks, which focus on generating contextually irrelevant texts based on the specific definitions of
irrelevance to the anchor [302, 332, 371], enhance the GPTE models’ capabilities in deep semantic
understanding.

3.4.2
Evolving Benchmark. As the application scenarios of embedding models expand and applica-
tion requirements increase, the benchmarks also need to be expanded in terms of task, language,
and text length. Traditional benchmarks mainly rely on manual annotation and suffer from a static
nature, a narrow scope, and a high cost, which makes it difficult to construct or expand benchmarks.
To build a unified assessment task format and fill in gaps in multilingual or task types, using LLMs
to synthesize data is a cost-effective method [374].

5Several studies explore the use of augmented positive samples; however, their underlying strategy is functionally equivalent
to that of augmented negative sampling.

J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.

On The Role of Pretrained Language Models in General-Purpose Text Embeddings: A Survey
111:15

Fig. 4. Comparisons of GPTE models with various PLM backbones, focusing on those of widely-adopted
open-source PLMs.

For example, in low-resource languages or uncommon task types such as dialogue embedding,
LLM is often used to synthesize input pairs, questions, or labels. In semantic text similarity (STS)
or question-answering tasks, LLM is also used to automatically convert formats (e.g., generating
hypothetical questions or sentence pairs) to maintain consistency in task formats. Some classification
tasks (especially multilingual ones) are constructed using data samples or label explanations
automatically generated by LLM. The AIR-bench [34] leverages LLMs to dynamically generate
retrieval evaluation data for diverse tasks, domains, and languages.

3.5
The Choice of PLMs
As the foundations of GPTE, the choice of PLMs is crucial and is influenced by the performance,
efficiency, and other advanced capabilities (e.g., multilingualism). Consequently, this choice is made
across two key factors: the model architecture and scale. Figure 4 depicts the overall trend of the
two factors.

3.5.1
Comparison of Model Architectures. The architectural design of PLMs largely impacts their
suitability for text embedding. As summarized in Table 2, the prevailing architectures for GPTE are
encoder-only and decoder-only PLMs. Encoder-only GPTE models have dominated the field for
several years [221, 359], with BERT serving as the most widely adopted backbone [180, 263, 316, 344],
alongside alternatives like XLM-R and RoBERTa. Several works also train BERT-alike models from
scratch for specific goals such as long-context modeling, e.g., GTE-MLM, JinaBERT, and NomicBERT.
For encoder-decoder PLMs, T5 is the primary choice for GPTE models. While most of them use only
the encoder component, ST5 explores the decoder as well and finds that decoder-based embeddings
perform slightly worse than their encoder-based counterparts.

J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.

111:16
Zhang et al.

With the rapid advancement of LLMs, decoder-only models have recently emerged as a popu-
lar choice for developing state-of-the-art GPTE models [317, 374]. The commonly used decoder
backbones include the Qwen series and Mistral, along with others such as Bloom, Gemma, and
MiniCPM for training GPTEs. The widely-accepted decoder backbones to train GPTE models are
Qwen series and Mistral, while Bloom, Gemma, MiniCPM and etc. are also used. Figure 4 shows
the average performance of various GPTE models, which are collected from the MTEB leadboard.
As a whole, decoder-based models can achieve top-tier performance with sufficient scale and
proper training [154, 180, 317, 374]. However, a key observation is that these models often require
a significantly larger number of parameters in order to achieve competitive results compared with
the encoder-only models.

3.5.2
Impact of Model Scale. Larger models with enormous parameters and extensive pre-training
on vast corpora tend to possess richer semantic understanding and stronger language modeling
capabilities. Consequently, when pre-trained and fine-tuned for GPTE models, increasing the model
scale also leads to more powerful text embedding generally, e.g., gte-Qwen2-7B-instruct vs. gte-
Qwen2-1.5B-instruct [180]. As shown in Figure 4, the scaling effect has demonstrated that model
capacity largely determines the quality of the resulting embedding model.
However, larger models are slower for inference, require more memory, and are more expensive
for pre-training and fine-tuning, which inflicts a heavy blow on online applications. To address this
issue, Mixture-of-Experts (MoE) models have emerged as a promising direction for efficient scaling.
Models like GritLM [220] and Nomic-Embed-MoE [232] employ a sparse MoE architecture, where
only a fraction of the model’s total parameters (the “experts”) are activated for any given input text
during inference. This allows them to maintain the representational power of large dense models
while achieving the computational efficiency of smaller ones, offering a scalable and cost-effective
pathway to scale up high-quality GPTE models without an explosion in inference costs. More
intriguingly, MoEE [181] finds that the routing weights used to decide which experts to activate
encode meaningful semantic information complementary to the hidden states commonly used as
embeddings. By combining these two sources, MoEE achieves more robust embeddings without
any additional finetuning, highlighting that MoE LLMs can serve not only as efficient generators
but also as versatile and semantically rich embedding models.

4
Advanced Roles of PLMs

In the previous section, we introduced the basic roles of GPTE in conjunction with PLMs, focusing
on standard extensions of text embeddings during the period when PLMs dominated the NLP
landscape. In this section, we explore several advanced topics that have emerged with the rise of
PLMs, including multilingual processing, multimodal learning, programming languages, safety
considerations, and task-specific adaptation. These areas have seen significant progress due to
the advent of PLMs, some of which were scarcely explored or even nonexistent prior to their
development.

4.1
Multilingualism
Multilingualism has become a central topic in NLP since the introduction of multilingual word
representations [211, 346]. The development of multilingual PLMs has significantly advanced the
ability to GPTE models across languages. By adopting multilingual PLMs such as mBERT, XLM,
and XLM-RoBERTa as the backbone, we can obtain multilingual text embeddings naturally. Nu-
merous studies have demonstrated that extending the pretraining and pre-finetuning corpora to
include multilingual unlabeled data or machine-translated corpora leads to substantial performance

J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.

On The Role of Pretrained Language Models in General-Purpose Text Embeddings: A Survey
111:17

Table 4. Representative multilingual GPTE models, where the LLM-based models are not listed as their
multilingualism is almost a standard property.

Model
Base Model
Param Size
Language Number
GTR [228]
mT5
N/A
101
LaBSE [78]
Transformer (from scratch)
471M
109
mE5 [318]
XLM-RoBERTa
118M∼560M
93
mContriever [119]
mBERT
125M
104
mDPR [376]
mBERT
125M
104
m-ST5 [359]
mT5-Enc
564M∼5.7B
101
mGTE [378]
Transformer (from scratch)
304M
75
NLLB-E5 [3]
NLLB
600M∼3.3B
200+
BGE-M3 [36]
XLM-RoBERTa
560M
194

improvements for multilingual text embedding. With the encoder-based PLMs, LaBSE [78], mCon-
triever [119], mDPR [376], mE5 [318], m-ST5 [359], mGTE [378], NLLB-E5 [3], BGE-M3 [35], and
GTR [228], have gained great successes. Table 4 provides a summary of several representative
multilingual text embedding models along with their corresponding language coverage, offering an
overview of the growing ecosystem of multilingual GPTE models. More recently, decoder-based
LLMs have shown remarkable potential in GPTE. Since nearly all LLMs inherently support multiple
languages with equally impressive effectiveness, we will not address their multilingual capabilities
here.
The pretraining of multilingual GPTE heavily depends on the breadth and quality of multilingual
corpora used in CL. Table 5 shows the representative datasets for multilingual GPTE training. First, a
straightforward yet effective approach is to aggregate monolingual corpora across various languages
(e.g., English-English and Chinese-Chinese text pairs) to construct a multilingual training set. This
strategy enables GPTE to capture rich intra-lingual semantics while laying a foundation for robust
cross-lingual generalization. To support this, diverse multilingual resources, e.g., Reddit [88, 262],
Stackexchange [88, 286], Wikipedia [83], mC4 [350], CCNet [333], and xP3 [222], can be utilized
to mine large-scale text pairs. Then standard bi-text mining, such as title-body, title-abstract,
instruction-output extraction, is applied to curate a multilingual corpus, comprising nearly one
billion text pairs across more than 200 languages. Such scale and diversity provide the semantic
coverage and linguistic variation necessary to enhance multilingual text embeddings that generalize
well across both tasks and languages.
In addition to the aforementioned data sources, the multilingual versions of high-quality, manually-
crafted text pairs from specific tasks can also be leveraged to enhance GPTE training. These tasks
are closely aligned with the GPTE objective, and several have already been adopted as benchmarks
for evaluating text embedding models. Notable examples include MFAQ [22], MLQA [158] and
MKQA [192] for multilingual question-answering, MLSUM [276], XL-Sum [102] for multilingual
text summarization, and XNLI [58] for multilingual NLI. For multilingual text retrieval, datasets
such as MIRACL [377] and Mr. TyDi [375] are widely used. Moreover, cross-lingual text pairs
originally designed for machine translation or cross-lingual IR, such as Europarl [304], NLLB [59],
CCMatrix [275] and CLIRMatrix [293], can serve as valuable resources for learning aligned text
representations across languages.
LLMs have also emerged as an affordable and scalable solution for generating synthetic data
to train multilingual text embedding models. Recent studies have demonstrated the effectiveness
of this approach [156, 381]. For example, Swim-IR [299] introduces SAP (summarize-then-ask
prompting), enabling PaLM-2 to generate informative queries in target languages, resulting in a

J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.

111:18
Zhang et al.

Table 5. Representative datasets for multilingual GPTE training.

Type
Datasets
SS
PAWS-X [356], Europarl [304], CCMatrix [275], NLLB [104, 298],XNLI [58], XL-Sum [102], MLSUM [276]

SR

Reddit, Stackexchange, Wikipedia, Multilingual CC News, mC4 [350], CLIRMatrix [293], CCNet [333], Amazon
Reviews [108], mMARCO [18], MLDR [35], MIRACL [377], Mr.TyDi [375], SWIM-IR [299], MFAQ [22], MLQA
[158], MKQA [192]

SE
AmazonCounterfactual [235], AmazonMassiveIntent [80], AmazonMassiveScenario [80], MultilingualSenti-
ment [215], MTOPIntent [163], MTOPDomaint [163]
Mixed
xP3 [222], Aya Dataset [282], MMTEB [71]

Table 6. Multimodal Embedding, where T, I, and V indicate text, image, and video, respectively.

Type
Model
Base Model
Modality

Individual
Encoder

CLIP [255]
ViT&Transformer (from scatch)
T/I
BLIP [165]
ViT&BERT
T/I
BLIP-2 [166]
ViT&OPT/Flan-T5
T/I
ALIGN [122]
EfficientNet&BERT
T/I
SigLIP [366]
ViT&Transformer (from scratch)
T/I
SigLIP-2 [306]
ViT&Transformer (from scratch)
T/I
Coca [361]
Transformer&Encoder-Decoder
T/I

Unified
Encoder

E5-V [125]
LLaVA-NeXT
T/I
VLM2VEC [128]
Qwen2-VL/LLaVA-NeXT
T/I
VLM2Vec-V2 [207]
Qwen2-VL
T/I/V
mmE5 [33]
Llama-3.2-Vision
T/I
GME [379]
Qwen2-VL
T/I
BGE-VL [392]
LLaVA-NeXT
T/I
UniME [91]
Phi3.5-V/LLaVA-NeXT
T/I
LLaVE [152]
LLaVA-OneVision/Aquila-VL
T/I
B3 [301]
Qwen2-VL
T/I
Unite [145]
Qwen2-VL
T/I/V
Jina-v4 [94]
Qwen2.5-VL
T/I/V

synthetic retrieval training dataset containing 33 languages (high to very-low resource) without
any human supervision. Similarly, JH-POLO [205] leverages GPT-3 to generate English queries for
document pairs in various target languages, producing retrieval data of diverse sizes and linguistic
coverage. mE5-Mistral [317] utilizes GPT-3.5 and GPT-4 to construct training data in 93 languages,
facilitating multilingual embedding training at scale.
While most studies on multilingual GPTE models assume that the multilingual PLM supports
the target language and that the target-language CL training data is available, several works
investigate less typical conditions. First, for a target language not covered by the multilingual PLM,
the availability of CL data can still facilitate effective GPTE training [376]. The likely reason is that
the CL objective provides strong semantic alignment signals that compensate for the lack of prior
language-specific representations. Another scenario involves the reverse: the PLM supports the
target language, but no CL data is available. In this case, several studies show that leveraging data
from other languages can still enhance the quality of target-language embeddings [316, 374, 376],
highlighting the potential of cross-lingual transfer to mitigate data scarcity.

J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.

On The Role of Pretrained Language Models in General-Purpose Text Embeddings: A Survey
111:19

Table 7. Typical datasets categorized by modalities and tasks, where T, I, VD, and V indicate text, image,
visual document, and video, respectively. The single-modal text corpora are also necessary, which is discussed
in previous sections.

Class
Task
Datasets

Single-Modal
I→I
NIGHTS[84]

Cross-Modal

T↔I
VisualNews[186],
Fashion200k[101],
MSCOCO[183],
Flickr30k[250],
ImageNet[67],
VisualDial[64], Wiki-SS-NQ[197]

T→VD TAT-DQA[395], ArxivQA[167], DocVQA[204], InfoVQA[203], VisRAG[363], Colpali[77]

T↔V
MSVD[31], Tarsier2-Recap[364], MSR-VTT[348], InternVid-FLT[325], DiDeMo[105], CaRe[349]

Fused-Modal

T→IT WebQA[30], EDIS[188]

IT→T OVEN[111], INFOSEEK[44], ReMuQ[195], OKVQA[201], LLaVA[184], VQA [7]

IT→I
FashionIQ[336], CIRR[191], Visual7W[399], RefCOCO[135]

IT→IT OVEN[111], EVQA[209], INFOSEEK[44]

VT→V WebVid-CoVR[308]

4.2
Multimodal

The advancement of PLMs has brought powerful linguistic priors and instruction-following capa-
bilities to multimodal embedding. Table 6 presents a summary of these representative multimodal
embedding models. Previous works mainly focus on learning multimodal embedding from large-
scale, weakly supervised image-text pairs [122, 165, 166, 255, 306, 361, 366], where these models
usually encode text and images separately and project them into a shared space. Pioneering break-
throughs like CLIP [255] leverage contrastive learning over 400M image-text pairs, training a vision
encoder and text encoder to maximize cross-modal alignment via a temperature-scaled cosine simi-
larity objective. Its successor, BLIP [165, 166], further optimizes efficiency by freezing pre-trained
vision encoders and introducing a lightweight querying mechanism for cross-modal interaction.
Subsequent works further advance this paradigm in data curation [122], loss design [306, 366],
training strategies [361]. Overall, these models share a common paradigm that harnesses mas-
sive weakly supervised data for cross-modal contrastive alignment while evolving architectures.
Their success has laid the foundation for integrating PLMs into multimodal embedding, while
their disjoint architecture hinders fine-grained fusion, and instruction-following capacity remains
limited.
The rapid advancement of PLMs has not only reshaped text embedding but also brought a
breakthrough in multimodal embedding. The integration of PLMs into multimodal embedding
has unlocked new potential in fusing diverse modalities and instruction-following capabilities:
(1) Powered by the contextual modeling capabilities of PLMs, multimodal embedding can fuse
textual descriptions with visual scenes seamlessly; (2) Leveraging PLMs’ instruction-following
capabilities, multimodal embedding can support various tasks, e.g., image classification, visual
question answering, multimodal retrieval, etc. Building on these advancements, models like E5-
V [125] finetune on textonly data yet outperform earlier contrastive methods on imagetext retrieval
benchmarks by leveraging the PLM’s rich semantic priors. This marks a shift towards leveraging
the powerful capabilities of PLMs for more advanced multimodal embedding.
In tandem with model advancements, training frameworks and recipes [91, 128, 145, 152, 207,
301] have evolved beyond standard contrastive learning to enhance discriminative power and
instruction-following capabilities. VLM2VEC-V1/V2 [128, 207] introduce a method to convert any
VLM into an instruction-aware embedding model. Others focus on enhancing discriminative power

J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.

111:20
Zhang et al.

through novel training objectives. For example, UniME [91] employs a two-stage approach of
knowledge distillation from an LLM teacher and hard negative enhanced instruction tuning, while
LLaVE [152] introduces a method to handle hard negatives based on their difficulty dynamically.
Further optimizing the training batch, B3 [301]introduces a novel batch construction strategy
that uses a teacher model and community detection to create batches rich in hard negatives;
UNITE [145]develops a universal framework focused on data curation and modality-aware training,
introducing modality-aware masked contrastive learning to manage the competitive relationship
between different modalities.
A significant challenge in multimodal embedding training remains the scarcity of large-scale,
high-quality labeled data. To address this, several works [33, 379, 392] have investigated data
synthesis techniques. For example, BGE-VL-MLLM [392] introduces MegaPairs, a method using
VLMs to generate a massive synthetic dataset that significantly outperforms models trained on
existing data. Similarly, GME [379] develops a pipeline to create a large-scale, fused-modal dataset
specifically for universal multimodal retrieval, where queries and candidates can be any combination
of text and images while mmE5 [33] focuses on the broad scope, cross-modal alignment, and high
fidelity for synthesizing effective data to train a powerful multilingual, multimodal embedding
model.
Beyond training techniques and data, architectural designs also play a key role. Jina-v4 [94]
introduces a flexible model that supports both single-vector and multi-vector [138] representations,
using task-specific LoRA adapters to optimize performance across diverse scenarios like visually rich
image/document retrieval. In conclusion, current developments span high-quality data synthesis
like MegaPairs, improved training techniques like B3’s hard negative-rich batch construction, and
innovative architecture designs like jina-v4’s multi-vector representation. It has moved beyond
basic cross-modal alignment to building capable, instruction-aware multimodal embeddings that
handle diverse tasks, ranging from image, video to visual document tasks.

4.3
Programming Languages

Driven by the success of PLMs in NLP, there has been growing interest in applying similar paradigms
to programming languages. Code embedding remains a central focus in the field of code representa-
tion learning. SCELMO [133] is the first work to introduce code embeddings based on ELMo, while
CodeBERT [79] and CuBERT [132] pioneer the use of BERT-style models for code embeddings.
In addition, structural information from programming languages has been leveraged to improve
code PLMs. GraphCodeBERT [96] integrates data flow structures to enhance code understanding,
while models such as SynCoBERT [323], TreeBERT [126], and UniXcoder [95] leverage syntactic
structures from abstract syntax trees (ASTs). DOBF [151] further combines both data flow and
AST information through an implicit strategy, adopting an encoder-decoder framework similar to
TransCoder [265], PLBART [4], CodeT5 [327], and CoTexT [249]. These models typically generate
code embeddings using the standard GPTE strategy for encoder-based PLMs, where the hidden
⟨CLS⟩representation is used as the code embedding.
CodeGPT6, GPT-Neo [15], GPT-J [310], and Codex [37] have sparked a new wave of research
in LLM-based code intelligence. By fine-tuning GPTs on large-scale code corpora from platforms
like GitHub, these models have demonstrated impressive performance on code generation and
related tasks. Since then, a wide array of LLMs for code have emerged, including AlphaCode [177],
CodeGen [230], PaLM-Coder [53], CodeLLaMA [264], DeepSeek-Coder [97], CodeQwen [10],
CodeGemma [384], StarCoder [169], Phi-1.5/3 [1, 176], Codestral7, among others. The process of

6https://codegpt.co/
7https://mistral.ai/news/codestral

J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.

On The Role of Pretrained Language Models in General-Purpose Text Embeddings: A Survey
111:21

Table 8. Representative PLM-based code embedding models, restricted to those that involve CL to drive
embedding-focused optimization.

Model
Base Model
Param Size
PL Number
SynCoBERT [323]
CodeBERT
125M
6
Code-MVP [324]
GraphCodeBERT
125M
6
UniXcoder [95]
RoBERTa
125M
8
C3P [242]
Transformer (from scratch)
N/A
7
CodeRetriever [173]
GraphCodeBERT
125M
6
CPT-Code [225]
GPT3 & Codex
300M∼175B
N/A
SCodeR [174]
UniXcoder
125M
8
CONCORD [70]
BERT
125M
3
FaCE [178]
RoBERTa
125M
N/A
ContraBERT [189]
CodeBERT/GraphCodeBERT
125M
6
CodeT5+ [326]
T5
220M∼16B
9

deriving code embeddings from these models typically mirrors the standard approach of LLM-based
GPTE. The typical process involves first extracting initial representations through pooling or other
advanced techniques, followed by refining these embeddings using CL. Despite the modality shift
from natural language to programming languages, the underlying methodology for embedding
remains fundamentally aligned with that of textual embeddings.
CL has been actively explored to enhance code representation learning, with numerous stud-
ies demonstrating its effectiveness [23, 120]. Table 8 shows the representative code embedding
models with CL support. Models like UniXcoder [95], Code-MVP [324], ContraFlow [51], Trans-
formCode [341] and CONCORD [70] exploit code-code pairs for CL pretraining, where these
pairs are constructed through various transformation strategies such as feature dropout, code
compression, code clone, identifier renaming, canonicalization, loop exchange, dead code insertion,
compilation-guided multiple-view expansions and etc. The multi-modal CL with both text and
code pairs has also been investigated extensively. SynCoBERT [323] pioneers the use of textcode
and codecode pairs extracted from docstrings, while the following representative studies includes
C3P [242], CodeRetriever [173], CPT-Code [225], SCodeR [174], FaCE [178], ContraBERT [189]
and CodeT5+ [326], exploiting well-mined codedocument, codecomment, code-text, and codecode
pairs.
Most recently, CODESAGE [369] demonstrates the effectiveness of multi-modal CL on large-scale
textfunction pairs, indicating the scale of training corpora plays a crucial role in code embedding
pretraining. CodeSearchNet [117] consists of 2.1 million functions paired with their natural language
documentation, while CoSQA [113] offers 20,604 high-quality, manually annotated pairs of natural
language queries and code snippets. APPS [106] provides a diverse set of programming problems
and their corresponding solutions, covering various difficulty levels. More recent datasets continue
to expand the scope and depth of textcode interaction. CodeFeedback [389] introduces 68,000
multi-turn interactions with text-code pairs, Query4Code [171] constructs 237,200 querycode pairs
from 12,300 GitHub repositories, tailored for code retrieval, and CornStack [294] presents a high-
quality filtered dataset derived from The Stack [144, 193], further enriching the landscape of clean,
large-scale code corpora for embedding and retrieval studies. Table 9 shows the representative
datasets that might be beneficial for code embeddings.

J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.

111:22
Zhang et al.

Table 9. Representative datasets for training code embeddings, where the reported scales may not be directly
comparable due to differences in measurement units.

Type
Dataset
Scale
Covered Languages

Code

CodeNet [254]
13.9M
55 languages
Codeparrot (clean)
115M
32 languages
StackV2 [294]
784.3M
86 languages

Code-Code

CodeTrans [194]
12K
Java, C#
POJ-104 [217]
52K
C, C++
Avatar [5]
57K
Java,Py
CoST [397]
132K
C++, Java, Py, C#, JS, PHP, C
CodeTransOcean [352]
270K
45 languages
TransCoder-ST [266]
437K
Java, C++, Py
BigCloneBench [295]
1.8M
Java

Code-Text
&
Text-Code

CoSQA [113]
20.6K
Py
CONCODE [118]
104K
Java
APPS [106]
232K
Py
CodeFeedback [389]
192K
Py
Query4Code [171]
237.2K
Py
XLCOST [396]
1M
C++, Java, Py, C#, JS, PHP, C
CodeSearchNet [117]
2.3M
PHP, Java, Py, Go, JS, Ruby
CornStack [294]
21.2M
PHP, Java, Py, Go, JS, Ruby
CodeT5+ [326]
37M
PHP, Java, Py, Go, JS, Ruby, C, C++, C#

4.4
Adaptation for Specific Scenarios

Although GPTE models have achieved impressive performance across a wide range of tasks, there
remains considerable room for improvement in scenario-specific settings, such as particular tasks,
languages, modalities, domains, or document types. A straightforward and effective adaptation
strategy is to perform SFT using labeled datasets tailored to the target scenario. To preserve the
strong capabilities of the original GPTE model while adapting to new scenarios, lightweight training
techniques, such as incorporating neural adapters or applying Low-Rank Adaptation (LoRA), are
often used. These approaches have proven effective in both the target-scenario performance and
the extent of model modification, and are especially popular for small-sized GPTE models when
BERT-alike or mini-type LLM models are used as backbones.
Recently, instruction-following embeddings have emerged as a promising direction for task-
specific adaptation, as the increasing interest in LLM-based GPTE models [162]. It is a natural
extension of the instruct-tuning paradigm for task-specific PLMs from general tasks into text
embeddings [214, 238, 270, 330]. GenSE [46] proposes prompt-based CL where prefix prompt
templates can be regarded as instructions. TART [8] introduces the first instruction-following
IR system by massive multi-task instruction-tuning. INSTRUCTOR [288] annotates instructions
for 330 diverse tasks and then trains a GPTE model on this with a contrastive loss, which can
achieve good performance on various (new) embedding tasks, including classification, retrieval,
and STS. LLM2Vec [13] tests the effectiveness of instruction-following text embeddings with LLM-
based GPTE models without any supervised training. INBEDDER [244] further shows that training
with questionanswer pairs can significantly enhance the instruction-following capability of GPTE
models.
Although multilingual GPTE models have achieved remarkable success, several studies still focus
on individual languages. Several studies involve training specialized BERT-based models using

J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.

On The Role of Pretrained Language Models in General-Purpose Text Embeddings: A Survey
111:23

carefully curated corpora in the target language, from which language-specific text embeddings are
derived [344]. The example attempts include FaBERT [202] for Persian, NB-BERT for Norwegian,
RuBERT for Russian, and GATE [223] for Arabic. Only models with reported results on the MTEB
leaderboard are listed here. In contrast, there are relatively few studies utilizing decoder-based LLMs
for language-specific embedding tasks. A possible reason is that recent LLMs already demonstrate
strong performance across many languages, reducing the perceived need for further specialization.
Domain-specific adaptation follows a similar trend to language-specific modeling. Most existing
studies concentrate on the clinical and biomedical domains. Improved text embeddings can be
obtained either by using specialized PLMs such as BioBERT [157] and ClinicalBERT [6], or by
pretraining on domain-specific contrastive learning corpora, such as DisEmbed [76]. A recent
study [73] shows that generalist models can outperform specialized clinical models on short-
context clinical semantic search tasks, potentially reducing the future interest in domain-specific
text embeddings.

5
Future Directions
In this section, we outline several future directions for GPTE models. While for conventional
advancements of ongoing and expected progress, such as improved text embedding acquisition
strategies [94, 154, 219], enhanced training paradigms (e.g., multi-stage curriculum learning or
reinforcement learning) [154, 381, 386], novel optimized objectives [149, 175, 386], better data
synthesis methods [155, 156, 381], stronger architectures and backbones [162, 220, 317, 381], as
well as the continued development of the advanced roles, we will not extensively elaborate on these
established areas. Instead, we aim to highlight several future research avenues that are currently
underestimated or newly emerging, yet hold significant potential as GPTE models continue to
advance.

5.1
Combination with Text Ranking
Text ranking is closely related to text embedding, and in many cases, embedding models can be
directly applied for ranking tasks [359]. In particular, bi-encoder architectures of GPTE enable
efficient deployment by independently encoding query and document representations. However,
this independent encoding limits the model’s ability to capture fine-grained interactions between
texts, which are often critical for accurate text ranking. As a result, GPTE models may fall short
in tasks that demand nuanced relevance estimation. In contrast, effective text ranking typically
benefits from models that support mutual interactions between query and document, such as
cross-encoders, which jointly process both inputs and produce a relevance score directly. Therefore,
while embedding models offer scalability and versatility, achieving high accuracy in ranking often
requires architectures that go beyond the limitations of bi-encoder designs.
Currently, the integration of text ranking into universal GPTE models has received growing
attention and is emerging as a promising direction for future development. By unifying text em-
bedding and ranking within a single general-purpose framework, the CL datasets can be fully
explored, and the strengths of GPTE models can be more effectively leveraged. Qwen3 Embed-
ding [381] leverages the instruction-following capabilities of GPTE for text ranking by framing
the task as a prompted interaction. Specifically, it uses a chat-style prompt that concatenates the
query and document, prompting the model to produce a binary output (e.g., "yes" or "no") as an
assessment of relevance for ranking purposes. This is just an initial step toward universalization,
which may further advance GPTE beyond embedding and ranking, extending its applicability to a
broad range of NLP tasks. A notable advancement along this line is Jina-reranker-v3 [311], which
exemplifies the emerging trend of integrating embedding-based retrieval with interaction-based
ranking. Instead of relying solely on independent document embeddings or late interaction after

J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.

111:24
Zhang et al.

retrieval, Jina-reranker-v3 introduces a last-but-not-late interaction mechanism that applies causal
attention between a query and its candidate documents within a shared context window. This
design effectively unifies the strengths of embedding models for efficient large-scale retrieval and
reranking models for fine-grained semantic interaction within a single framework.

5.2
Safety Considerations
Safety issues have always been a critical research focus in PLMs, and this concern is further
amplified with the rapid advancements in LLMs. While GPTE models built on PLMs demonstrate
powerful performance, the security issues they introduce must also be carefully examined. These
risks primarily stem from two aspects: inherent vulnerabilities inherited from upstream pre-trained
models, and second threats newly introduced or amplified within the embedding models’ specific
application scenarios.
The pre-training stage of large-scale models often relies on complex and diverse data sources,
creating vulnerabilities to data poisoning. A typical form of such an attack is the backdoor attack,
which embeds hidden triggers into the model. When the input contains this trigger, the model
will generate malicious output preset by the attacker. For instance, Badnl [41] demonstrates the
feasibility of backdoor attacks on large pre-trained models like BERT and highlights their high
level of stealth and effectiveness. BadCSE [42] extends this by injecting backdoors through CL,
mapping sentences with triggers to the target semantic vector region in the embedding space.
Further, backdoor injection can also be achieved by modifying the bottom neural network layers
without fine-tuning [355]. These works reflect the multiple attack surfaces of embedded models
during training, deployment, and distribution.
With the spread use of embedding models, the issue of privacy leakage has become increasingly
important. Attackers can infer some of the original input information from the generated embedding
vectors. For instance, GEIA [164] trains a generator using generative models (e.g., GPT-2 or T5)
to reverse embeddings into complete sentences, which achieves a 92% success rate when inverse
32-token sentences. ALGEN [45] uses a small scale (such as 1k) of paired data for alignment,
achieving inversion range from different fields and languages. Beyond reconstructing input texts,
inversion attacks can also target the embedding model itself. Text Revealer [373], for example,
combines public corpora and GPT-2, using model feedback from the target classifier to guide the
iterative optimization of GPT-2’s hidden states, thereby reconstructing the private text in the
original training set. Furthermore, surrogate models can be trained to mimic target embedding
models, allowing the attacker to infer sensitive information from text embeddings without direct
access [116].
Overall, the privacy and safety aspects are from the very beginning for text embeddings, which
would inevitably gain increasing attention as the growing capabilities of GPTE.

5.3
Bias of GPTE
The presence of bias in GPTE is an inevitable concern and is expected to emerge as a prominent
research focus in the field. Biases in GPTE are mainly sourced from imbalanced datasets of learn-
ing, resulting in task overrepresentation of certain tasks, insufficient linguistic diversity, domain
misalignment, and societal stereotypes [17]. These biases not only affect fairness but also limit the
robustness, generalizability, and inclusiveness of downstream applications. Moving forward, one
of the key challenges in embedding research is to develop techniques that identify, mitigate, and
evaluate these biases systematically, thereby enabling more reliable and equitable applications.
Task bias arises as current GPTE models are trained on imbalanced task distributions [86], with
semantic similarity and relevance datasets overrepresented, while feature representation tasks are
significantly underrepresented. Moreover, the semantic diversity across tasks further amplifies

J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.

On The Role of Pretrained Language Models in General-Purpose Text Embeddings: A Survey
111:25

task bias, as different tasks emphasize distinct aspects of meaning. As a result, the resulting text
embeddings tend to overfit to certain tasks, limiting their ability to handle less-represented tasks
such as complex text classification, multilabel classification, clustering, and instruction retrieval. To
address this, future research can explore task-agnostic embedding objectives, employ task-diverse
pretraining regimes [381], and develop meta-task frameworks that promote versatility across a
wider range of tasks. Reducing task bias holds the promise for enhancing generalization, improving
performance in zero-shot and compositional scenarios, and increasing flexibility for emerging
applications.
Domain, language, and modal biases represent another set of critical concerns. Domain bias
occurs as GPT models are mostly trained on general corpora, which struggle to perform effectively
in specialized areas such as biomedical or scientific texts. This might be mitigated through domain-
adaptive pretraining and in-domain contrastive learning [278]. Language bias arises from the
dominance of high-resource languages in training data, often resulting in degraded performance for
low-resource languages. Techniques such as multilingual alignment and language-specific tuning
can help bridge this gap [147, 378]. Modal bias, particularly in multimodal settings, refers to the
over-reliance on textual inputs at the expense of complementary visual, audio, or structured signals.
Balanced modality fusion, modality-invariant representations, and contrastive multimodal learning
offer promising paths forward [274]. Addressing these biases can lead to more accurate, inclusive,
and versatile embeddings across diverse linguistic, domain-specific, and multimodal contexts.
Finally, social and cultural biases such as gender, race, religion, and nationality would pose serious
ethical and societal risks. These biases often stem from stereotypes and imbalances present in large-
scale training corpora and can propagate into downstream applications [17]. Tackling such biases
requires a combination of approaches [182], including counterfactual data augmentation, fairness-
aware training objectives, post-hoc debiasing, and the development of robust bias evaluation
benchmarks. Reducing social and cultural bias not only fosters more ethical and inclusive NLP
systems but also builds user trust and aligns AI technologies with broader societal values.

5.4
Structure Information

One of the most crucial characteristics of text is its inherent structural information. While the short-
range structural dependencies are largely captured by current GPTE backbones, long-range structure
information, which is vital for comprehensive long text understanding, remains significantly under-
addressed. For example, in scientific documents like books, articles, or papers, understanding the
overall argument involves connecting concepts and logics from the introduction to the conclusion or
linking methodologies to their later results and findings. In addition to standard texts, structured data
such as tables [360], codes [79], knowledge graphs [321], and other well-organized information are
also essential for effective structural learning. Without adequately leveraging such structural cues,
GPTE models often struggle with tasks requiring global coherence, argumentation flow, or complex
multi-hop reasoning, leading to fragmented interpretations rather than holistic understanding.
In fact, structural information has already been explored in the field of information retrieval [243].
Representative PLM-based models include the subgraph retriever [372], KG-GPT [139], and Struct-
GPT [123]. However, all these studies primarily focus on improving fragment embeddings within
the structured data, rather than providing a comprehensive embedding of the entire data. It is
desirable to obtain full-data embeddings that, while being decomposable and computationally
manageable, enable a global and in-depth understanding of the structured information.
The exploitation of structural characteristics also offers a valuable avenue for task-specific GPTE
adaptation. For example, a combination of well-organized task instructions and the input text
can be naturally conceptualized as a hierarchical discourse graph, inherently forming structured
data. When global and in-depth embeddings can be derived through functional composition with

J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.

111:26
Zhang et al.

computable operators, we can then easily obtain task-specific text embeddings. This would allow
GPTE models to better align with the specific demands of diverse tasks by understanding their
underlying structural organization.
With support from structure-informed text embeddings, we can advance contrastive learning
beyond traditional pairwise texts to encompass chain and graph texts [75]. The standard pairwise
optimization paradigm, while common, exhibits limitations [86]. For instance, the aforementioned
task bias problem can be partially alleviated through fine-grained support during optimization. As a
result, the GPTE model gains a more nuanced understanding by contrasting not just individual text
snippets, but their interconnected structural components. This allows for a richer learning signal
that better captures complex relational patterns and mitigates overfitting to simplistic similarities.

5.5
Extending GPTE with Reasoning

Given the inherent variability in application contexts, GPTE models must be designed with flexibility
to accommodate the diverse requirements of downstream tasks and usage scenarios. The key
considerations often include: (1) explainability, ensuring model decisions are interpretable and
foster trustworthiness [365]; (2) privacy preservation, particularly crucial in sensitive domains such
as healthcare and finance [14]; and (3) robustness, to maintain consistent performance across noisy,
mixed-code, or domain/language-shifted inputs [381]. Consequently, future research should focus
on developing embedding models that are not only semantically rich but also inherently adaptable
to these evolving practical constraints, thereby enabling safe, effective, and responsible deployment
across a wide array of applications.
To meet the above requirements, one promising approach is to design GPTE models that are
compatible with a reasoning LLM [351]. By aligning text embeddings with the LLM reasoning
mechanisms, it becomes possible to enhance interpretability, support context-aware adaptation, and
enable controllable behavior across tasks. This compatibility allows embeddings to serve not only
as static representations but also as interfaces for dynamic reasoning, enabling applications such as
instruction following, multi-step inference, and explainable retrieval. Moreover, this integration
can facilitate modular system design, where GPTE handles efficient representation learning while
the reasoning LLM provides flexible task execution and semantic interpretation. Such a hybrid
framework could offer a practical path toward embedding systems that are both powerful and
responsive to real-world demands.
It is important to note that the above framework is not equivalent to the well-known retrieval-
augmented generation (RAG) paradigm, which belongs to one specific application of GPTE. Instead,
this framework should be viewed as a foundational component of GPTE. It enables a shift from
abstract, task-agnostic representations to more concrete, context-aware embeddings aligned with
reasoning and application needs. By coupling GPTE with a reasoning-capable LLM, the embedding
space can be made more interpretable, actionable, and adaptable, allowing for richer semantic
encoding and more precise downstream task alignment. This perspective emphasizes the role
of reasoning not merely as an add-on module but as an integral part of embedding generation,
bridging the gap between static representation and dynamic understanding.
Recent works such as Think-Then-Embed [60] and O1-Embedder [351] further demonstrate the
potential of integrating reasoning mechanisms into embedding generation. Think-Then-Embed [60]
introduces a two-stage framework where a reasoning model first produces explicit intermediate
thoughts or explanations before the embedder encodes both the original query and the generated
reasoning trace. This paradigm enhances compositional understanding, allowing the embedding
model to better capture complex semantic relationships and instruction-level nuances. Similarly,
O1 Embedder [351] brings reasoning-inspired retrieval into the text embedding, enabling retrievers
to “think before acting.” By generating internal reasoning signals before retrieval, O1 Embedder

J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.

On The Role of Pretrained Language Models in General-Purpose Text Embeddings: A Survey
111:27

achieves substantial gains in multi-task and zero-shot retrieval performance, showing that explicit
reasoning can guide embedding models toward more precise and generalizable representations.
Overall, these studies point to a promising evolution of GPTE, where embeddings are not static
outcomes of encoding, but dynamic products of deliberate reasoning.
The concept of embedding can be further extended to align with the notion of memory in cognitive
neuroscience [354], suggesting the potential for high-dimensional, dynamic representations that
evolve with ongoing textual, visual, or auditory input. Just as human memory encodes, stores,
and retrieves information to support reasoning, decision-making, and learning, GPTE serves as a
compressed representations that retain essential semantic content for downstream processing. In
this view, GPTE acts as a form of artificial memory, capable of capturing both episodic and semantic
information depending on the task and context. By the cognitive perspective, we may get a GPTE
model that not only encodes information efficiently but also supports continual learning, contextual
adaptation, and memory-augmented reasoning, which provide a more human-aligned foundation
for knowledge representation and flexible task execution in complex, real-world environments.

6
Conclusion
In this survey, we present a systematic review of GPTE in the era of PLMs, highlighting the
critical roles that PLMs play in advancing the development of GPTE. We begin by introducing
the background of GPTE, outlining the fundamental concepts and functions of text embeddings,
detailing the general training architecture, and summarizing progress in training data and evaluation
benchmarks. Next, we examine the foundational roles of PLMs in GPTE, including methods for
deriving embeddings, training strategies, diverse learning objectives, and the enrichment of high-
quality datasets. We also provide a comparative analysis of representative GPTE models with
respect to scale and backbone PLMs. Furthermore, we explore several advanced roles enabled by
PLMs, such as support for multilingual and multimodal embeddings, integration with programming
languages, and adaptation to diverse real-world scenarios. Finally, we discuss promising future
directions beyond the current scope of GPTE, including integrating text ranking, addressing safety
and bias issues in GPTE, leveraging structural information, and extending GPTE with reasoning
capabilities.
We hope this survey serves as a valuable resource for new researchers seeking to understand
recent developments in GPTE quickly, as well as for established researchers aiming to comprehen-
sively grasp the current landscape. Moreover, we expect that the insights and challenges outlined
in this survey will help to guide future research in this rapidly evolving field.

References

[1] Marah I Abdin, Sam Ade Jacobs, Ammar Ahmad Awan, Jyoti Aneja, Ahmed Awadallah, Hany Awadalla, Nguyen
Bach, Amit Bahree, Arash Bakhtiari, Harkirat S. Behl, Alon Benhaim, Misha Bilenko, Johan Bjorck, Sébastien Bubeck,
Martin Cai, Caio César Teodoro Mendes, Weizhu Chen, Vishrav Chaudhary, Parul Chopra, Allie Del Giorno, Gustavo
de Rosa, Matthew Dixon, Ronen Eldan, Dan Iter, Amit Garg, Abhishek Goswami, Suriya Gunasekar, Emman Haider,
Junheng Hao, Russell J. Hewett, Jamie Huynh, Mojan Javaheripi, Xin Jin, Piero Kauffmann, Nikos Karampatziakis,
Dongwoo Kim, Mahoud Khademi, Lev Kurilenko, James R. Lee, Yin Tat Lee, Yuanzhi Li, Chen Liang, Weishung
Liu, Eric Lin, Zeqi Lin, Piyush Madan, Arindam Mitra, Hardik Modi, Anh Nguyen, Brandon Norick, Barun Patra,
Daniel Perez-Becker, Thomas Portet, Reid Pryzant, Heyang Qin, Marko Radmilac, Corby Rosset, Sambudha Roy,
Olatunji Ruwase, Olli Saarikivi, Amin Saied, Adil Salim, Michael Santacroce, Shital Shah, Ning Shang, Hiteshi Sharma,
Xia Song, Masahiro Tanaka, Xin Wang, Rachel Ward, Guanhua Wang, Philipp A. Witte, Michael Wyatt, Can Xu,
Jiahang Xu, Sonali Yadav, Fan Yang, Ziyi Yang, Donghan Yu, Chengruidong Zhang, Cyril Zhang, Jianwen Zhang,
Li Lyna Zhang, Yi Zhang, Yue Zhang, Yunan Zhang, and Xiren Zhou. 2024. Phi-3 Technical Report: A Highly Capable
Language Model Locally on Your Phone. CoRR abs/2404.14219 (2024).
[2] Arkadeep Acharya, Rudra Murthy, Vishwajeet Kumar, and Jaydeep Sen. 2024. Hindi-BEIR : A Large Scale Retrieval
Benchmark in Hindi. CoRR abs/2408.09437 (2024).

J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.

111:28
Zhang et al.

[3] Arkadeep Acharya, Rudra Murthy, Vishwajeet Kumar, and Jaydeep Sen. 2024. NLLB-E5: A Scalable Multilingual
Retrieval Model. CoRR abs/2409.05401 (2024).
[4] Wasi Uddin Ahmad, Saikat Chakraborty, Baishakhi Ray, and Kai-Wei Chang. 2021. Unified Pre-training for Program
Understanding and Generation. In Proceedings of NAACL-HLT. 2655–2668.
[5] Wasi Uddin Ahmad, Md Golam Rahman Tushar, Saikat Chakraborty, and Kai-Wei Chang. 2021. Avatar: A parallel
corpus for java-python program translation. arXiv preprint arXiv:2108.11590 (2021).
[6] Emily Alsentzer, John R. Murphy, Willie Boag, Wei-Hung Weng, Di Jin, Tristan Naumann, and Matthew B. A.
McDermott. 2019. Publicly Available Clinical BERT Embeddings. CoRR abs/1904.03323 (2019).
[7] Stanislaw Antol, Aishwarya Agrawal, Jiasen Lu, Margaret Mitchell, Dhruv Batra, C Lawrence Zitnick, and Devi
Parikh. 2015. Vqa: Visual question answering. In Proceedings of the IEEE international conference on computer vision.
2425–2433.
[8] Akari Asai, Timo Schick, Patrick Lewis, Xilun Chen, Gautier Izacard, Sebastian Riedel, Hannaneh Hajishirzi, and
Wen-tau Yih. 2023. Task-aware Retrieval with Instructions. In Findings of ACL. 3650–3675.
[9] Parul Awasthy, Aashka Trivedi, Yulong Li, Mihaela Bornea, David Cox, Abraham Daniels, Martin Franz, Gabe
Goodhart, Bhavani Iyer, Vishwajeet Kumar, et al. 2025. Granite Embedding Models. arXiv preprint arXiv:2502.20204
(2025).
[10] Jinze Bai, Shuai Bai, Yunfei Chu, Zeyu Cui, Kai Dang, Xiaodong Deng, Yang Fan, Wenbin Ge, Yu Han, Fei Huang,
Binyuan Hui, Luo Ji, Mei Li, Junyang Lin, Runji Lin, Dayiheng Liu, Gao Liu, Chengqiang Lu, Keming Lu, Jianxin
Ma, Rui Men, Xingzhang Ren, Xuancheng Ren, Chuanqi Tan, Sinan Tan, Jianhong Tu, Peng Wang, Shijie Wang, Wei
Wang, Shengguang Wu, Benfeng Xu, Jin Xu, An Yang, Hao Yang, Jian Yang, Shusheng Yang, Yang Yao, Bowen Yu,
Hongyi Yuan, Zheng Yuan, Jianwei Zhang, Xingxuan Zhang, Yichang Zhang, Zhenru Zhang, Chang Zhou, Jingren
Zhou, Xiaohuan Zhou, and Tianhang Zhu. 2023. Qwen Technical Report. CoRR abs/2309.16609 (2023).
[11] Krisztian Balog, David Carmel, Arjen P. de Vries, Daniel M. Herzig, Peter Mika, Haggai Roitman, Ralf Schenkel, Pavel
Serdyukov, and Duc Thanh Tran. 2012. The first joint international workshop on entity-oriented and semantic search
(JIWES). SIGIR Forum 46, 2 (2012), 87–94.
[12] Nikolay Banar, Ehsan Lotfi, and Walter Daelemans. 2024. BEIR-NL: Zero-shot Information Retrieval Benchmark for
the Dutch Language. CoRR abs/2412.08329 (2024).
[13] Parishad BehnamGhader, Vaibhav Adlakha, Marius Mosbach, Dzmitry Bahdanau, Nicolas Chapados, and Siva Reddy.
2024. LLM2Vec: Large Language Models Are Secretly Powerful Text Encoders. In First Conference on Language
Modeling.
[14] Ghazaleh Beigi, Kai Shu, Ruocheng Guo, Suhang Wang, and Huan Liu. 2019. Privacy Preserving Text Representation
Learning. In HT. ACM, 275–276.
[15] Sid Black, Gao Leo, Phil Wang, Connor Leahy, and Stella Biderman. 2021. GPT-Neo: Large Scale Autoregressive
Language Modeling with Mesh-Tensorflow.
[16] David M Blei, Andrew Y Ng, and Michael I Jordan. 2003. Latent dirichlet allocation. CoRR 3, Jan (2003), 993–1022.
[17] Tolga Bolukbasi, Kai-Wei Chang, James Y. Zou, Venkatesh Saligrama, and Adam Tauman Kalai. 2016. Man is to
Computer Programmer as Woman is to Homemaker? Debiasing Word Embeddings. In NIPS. 4349–4357.
[18] Luiz Bonifacio, Vitor Jeronymo, Hugo Queiroz Abonizio, Israel Campiotti, Marzieh Fadaee, Roberto Lotufo,
and Rodrigo Nogueira. 2022. mMARCO: A Multilingual Version of the MS MARCO Passage Ranking Dataset.
arXiv:2108.13897 [cs.CL]
[19] Luiz Henrique Bonifacio, Hugo Queiroz Abonizio, Marzieh Fadaee, and Rodrigo Nogueira. 2022. InPars: Unsupervised
Dataset Generation for Information Retrieval. In SIGIR. 2387–2392.
[20] Samuel Bowman, Gabor Angeli, Christopher Potts, and Christopher D Manning. 2015. A large annotated corpus for
learning natural language inference. In Proceedings of EMNLP. 632–642.
[21] Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind Neelakantan,
Pranav Shyam, Girish Sastry, Amanda Askell, et al. 2020. Language models are few-shot learners. NeurIPS 33 (2020),
1877–1901.
[22] Maxime De Bruyn, Ehsan Lotfi, Jeska Buhmann, and Walter Daelemans. 2021. MFAQ: a Multilingual FAQ Dataset.
CoRR abs/2109.12870 (2021).
[23] Nghi DQ Bui, Yijun Yu, and Lingxiao Jiang. 2021. Self-supervised contrastive learning for code retrieval and
summarization via semantic-preserving transformations. In Proceedings of SIGIR. 511–521.
[24] Hongliu Cao. 2024. Recent advances in text embedding: A Comprehensive Review of Top-Performing Methods on
the MTEB Benchmark. arXiv preprint arXiv:2406.01607 (2024).
[25] Rui Cao, Yihao Wang, Yuxin Liang, Ling Gao, Jie Zheng, Jie Ren, and Zheng Wang. 2022. Exploring the Impact of
Negative Samples of Contrastive Learning: A Case Study of Sentence Embedding. In Findings of ACL. 3138–3152.
[26] Iñigo Casanueva, Tadas Temcinas, Daniela Gerz, Matthew Henderson, and Ivan Vulic. 2020. Efficient Intent Detection
with Dual Sentence Encoders. CoRR abs/2003.04807 (2020).

J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.

On The Role of Pretrained Language Models in General-Purpose Text Embeddings: A Survey
111:29

[27] Daniel Cer, Yinfei Yang, Sheng-yi Kong, Nan Hua, Nicole Limtiaco, Rhomni St John, Noah Constant, Mario Guajardo-
Cespedes, Steve Yuan, Chris Tar, et al. 2018. Universal sentence encoder. arXiv preprint arXiv:1803.11175 (2018).
[28] Daniel M. Cer, Mona T. Diab, Eneko Agirre, Iñigo Lopez-Gazpio, and Lucia Specia. 2017. SemEval-2017 Task 1:
Semantic Textual Similarity Multilingual and Crosslingual Focused Evaluation. In SemEval@ACL. Association for
Computational Linguistics, 1–14.
[29] Dhivya Chandrasekaran and Vijay Mago. 2021. Evolution of semantic similarity—a survey. ACM Comput. Surv. 54, 2
(2021), 1–37.
[30] Yingshan Chang, Guihong Cao, Mridu Narang, Jianfeng Gao, Hisami Suzuki, and Yonatan Bisk. 2022. WebQA:
Multihop and Multimodal QA. In CVPR. IEEE, 16474–16483.
[31] David L. Chen and William B. Dolan. 2011. Collecting Highly Parallel Data for Paraphrase Evaluation. In Proceedings
of ACL. The Association for Computer Linguistics, 190–200.
[32] Haonan Chen, Liang Wang, Nan Yang, Yutao Zhu, Ziliang Zhao, Furu Wei, and Zhicheng Dou. 2024. Little Giants:
Synthesizing High-Quality Embedding Data at Scale. arXiv preprint arXiv:2410.18634 (2024).
[33] Haonan Chen, Liang Wang, Nan Yang, Yutao Zhu, Ziliang Zhao, Furu Wei, and Zhicheng Dou. 2025. mmE5: Improving
Multimodal Multilingual Embeddings via High-quality Synthetic Data. CoRR abs/2502.08468 (2025).
[34] Jianlyu Chen, Nan Wang, Chaofan Li, Bo Wang, Shitao Xiao, Han Xiao, Hao Liao, Defu Lian, and Zheng Liu. 2024.
AIR-Bench: Automated Heterogeneous Information Retrieval Benchmark. arXiv preprint arXiv:2412.13102 (2024).
[35] Jianlv Chen, Shitao Xiao, Peitian Zhang, Kun Luo, Defu Lian, and Zheng Liu. 2024. BGE M3-Embedding: Multi-Lingual,
Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation. CoRR abs/2402.03216
(2024).
[36] Jianlyu Chen, Shitao Xiao, Peitian Zhang, Kun Luo, Defu Lian, and Zheng Liu. 2024. M3-Embedding: Multi-Linguality,
Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation. In Findings of ACL.
Bangkok, Thailand, 2318–2335.
[37] Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde De Oliveira Pinto, Jared Kaplan, Harri Edwards,
Yuri Burda, Nicholas Joseph, Greg Brockman, et al. 2021. Evaluating large language models trained on code. arXiv
preprint arXiv:2107.03374 (2021).
[38] Nuo Chen, Linjun Shou, Jian Pei, Ming Gong, Bowen Cao, Jianhui Chang, Jia Li, and Daxin Jiang. 2023. Alleviating
Over-smoothing for Unsupervised Sentence Representation. In Proceedings of ACL. 3552–3566.
[39] Shaobin Chen, Jie Zhou, Yuling Sun, and Liang He. 2022. An Information Minimization Based Contrastive Learning
Model for Unsupervised Sentence Embeddings Learning. In Proceedings of COLING. 4821–4831.
[40] Tianqi Chen, Bing Xu, Chiyuan Zhang, and Carlos Guestrin. 2016. Training deep nets with sublinear memory cost.
arXiv preprint arXiv:1604.06174 (2016).
[41] Xiaoyi Chen, Ahmed Salem, Michael Backes, Shiqing Ma, and Yang Zhang. 2020. BadNL: Backdoor Attacks Against
NLP Models. CoRR abs/2006.01043 (2020). arXiv:2006.01043
[42] Xiaoyi Chen, Baisong Xin, Shengfang Zhai, Shiqing Ma, Qingni Shen, and Zhonghai Wu. 2022. Apple of Sodom: Hidden
Backdoors in Superior Sentence Embeddings via Contrastive Learning. CoRR abs/2210.11082 (2022). arXiv:2210.11082
[43] Xi Chen, Ali Zeynali, Chico Q. Camargo, Fabian Flöck, Devin Gaffney, Przemyslaw A. Grabowicz, Scott Hale, David
Jurgens, and Mattia Samory. 2022. SemEval-2022 Task 8: Multilingual news article similarity. In SemEval@NAACL.
Association for Computational Linguistics, 1094–1106.
[44] Yang Chen, Hexiang Hu, Yi Luan, Haitian Sun, Soravit Changpinyo, Alan Ritter, and Ming-Wei Chang. 2023. Can
Pre-trained Vision and Language Models Answer Visual Information-Seeking Questions?. In Proceedings of EMNLP.
Association for Computational Linguistics, 14948–14968.
[45] Yiyi Chen, Qiongkai Xu, and Johannes Bjerva. 2025. ALGEN: Few-shot Inversion Attacks on Textual Embeddings
using Alignment and Generation. CoRR abs/2502.11308 (2025).
[46] Yiming Chen, Yan Zhang, Bin Wang, Zuozhu Liu, and Haizhou Li. 2022. Generate, Discriminate and Contrast: A
Semi-Supervised Sentence Representation Learning Framework. In EMNLP. Association for Computational Linguistics,
8150–8161.
[47] Daixuan Cheng, Shaohan Huang, Junyu Bi, Yuefeng Zhan, Jianfeng Liu, Yujing Wang, Hao Sun, Furu Wei, Weiwei
Deng, and Qi Zhang. 2023. UPRISE: Universal Prompt Retrieval for Improving Zero-Shot Evaluation. In Proceedings
of EMNLP. Singapore, 12318–12337.
[48] Qinyuan Cheng, Xiaogui Yang, Tianxiang Sun, Linyang Li, and Xipeng Qiu. 2023. Improving Contrastive Learning of
Sentence Embeddings from AI Feedback. In Findings of the ACL. 11122–11138.
[49] Xingyi Cheng. 2021. Dual-View Distilled BERT for Sentence Embedding. In SIGIR. ACM, 2151–2155.
[50] Xin Cheng, Xun Wang, Xingxing Zhang, Tao Ge, Si-Qing Chen, Furu Wei, Huishuai Zhang, and Dongyan Zhao.
2024. xRAG: Extreme Context Compression for Retrieval-augmented Generation with One Token. arXiv preprint
arXiv:2405.13792 (2024).

J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.

111:30
Zhang et al.

[51] Xiao Cheng, Guanqin Zhang, Haoyu Wang, and Yulei Sui. 2022. Path-sensitive code embedding via contrastive
learning for software vulnerability detection. In ISSTA. 519–531.
[52] Chanyeol Choi, Junseong Kim, Seolhwa Lee, Jihoon Kwon, Sangmo Gu, Yejin Kim, Minkyung Cho, and Jy-yong Sohn.
2024. Linq-Embed-Mistral Technical Report. arXiv e-prints (2024), arXiv–2412.
[53] Aakanksha Chowdhery, Sharan Narang, Jacob Devlin, Maarten Bosma, Gaurav Mishra, Adam Roberts, Paul Barham,
Hyung Won Chung, Charles Sutton, Sebastian Gehrmann, Parker Schuh, Kensen Shi, Sasha Tsvyashchenko, Joshua
Maynez, Abhishek Rao, Parker Barnes, Yi Tay, Noam Shazeer, Vinodkumar Prabhakaran, Emily Reif, Nan Du, Ben
Hutchinson, Reiner Pope, James Bradbury, Jacob Austin, Michael Isard, Guy Gur-Ari, Pengcheng Yin, Toju Duke,
Anselm Levskaya, Sanjay Ghemawat, Sunipa Dev, Henryk Michalewski, Xavier Garcia, Vedant Misra, Kevin Robinson,
Liam Fedus, Denny Zhou, Daphne Ippolito, David Luan, Hyeontaek Lim, Barret Zoph, Alexander Spiridonov, Ryan
Sepassi, David Dohan, Shivani Agrawal, Mark Omernick, Andrew M. Dai, Thanumalayan Sankaranarayana Pillai,
Marie Pellat, Aitor Lewkowycz, Erica Moreira, Rewon Child, Oleksandr Polozov, Katherine Lee, Zongwei Zhou,
Xuezhi Wang, Brennan Saeta, Mark Diaz, Orhan Firat, Michele Catasta, Jason Wei, Kathy Meier-Hellstern, Douglas
Eck, Jeff Dean, Slav Petrov, and Noah Fiedel. 2023. PaLM: Scaling Language Modeling with Pathways. J. Mach. Learn.
Res. 24 (2023), 240:1–240:113.
[54] Yung-Sung Chuang, Rumen Dangovski, Hongyin Luo, Yang Zhang, Shiyu Chang, Marin Soljacic, Shang-Wen Li, Scott
Yih, Yoon Kim, and James R. Glass. 2022. DiffCSE: Difference-based Contrastive Learning for Sentence Embeddings.
In Proceedings of NAACL-HLT. 4207–4218.
[55] Mathieu Ciancone, Imene Kerboua, Marion Schaeffer, and Wissam Siblini. 2024. Mteb-french: Resources for french
sentence embedding evaluation and analysis. arXiv preprint arXiv:2405.20468 (2024).
[56] Alexis Conneau and Douwe Kiela. 2018. SentEval: An Evaluation Toolkit for Universal Sentence Representations. In
LREC. European Language Resources Association (ELRA).
[57] Alexis Conneau, Douwe Kiela, Holger Schwenk, Loïc Barrault, and Antoine Bordes. 2017. Supervised learning of
universal sentence representations from natural language inference data. arXiv preprint arXiv:1705.02364 (2017).
[58] Alexis Conneau, Ruty Rinott, Guillaume Lample, Adina Williams, Samuel R. Bowman, Holger Schwenk, and Veselin
Stoyanov. 2018. XNLI: Evaluating Cross-lingual Sentence Representations. In Proceedings of EMNLP. 2475–2485.
[59] Marta R. Costa-jussà, James Cross, Onur Çelebi, Maha Elbayad, Kenneth Heafield, Kevin Heffernan, Elahe Kalbassi,
Janice Lam, Daniel Licht, Jean Maillard, Anna Y. Sun, Skyler Wang, Guillaume Wenzek, Al Youngblood, Bapi Akula,
Loïc Barrault, Gabriel Mejia Gonzalez, Prangthip Hansanti, John Hoffman, Semarley Jarrett, Kaushik Ram Sadagopan,
Dirk Rowe, Shannon Spruit, Chau Tran, Pierre Andrews, Necip Fazil Ayan, Shruti Bhosale, Sergey Edunov, Angela
Fan, Cynthia Gao, Vedanuj Goswami, Francisco Guzmán, Philipp Koehn, Alexandre Mourachko, Christophe Ropers,
Safiyyah Saleem, Holger Schwenk, and Jeff Wang. 2022. No Language Left Behind: Scaling Human-Centered Machine
Translation. CoRR abs/2207.04672 (2022).
[60] Xuanming Cui, Jianpeng Cheng, Hong-you Chen, Satya Narayan Shukla, Abhijeet Awasthi, Xichen Pan, Chaitanya
Ahuja, Shlok Kumar Mishra, Qi Guo, Ser-Nam Lim, et al. 2025. Think Then Embed: Generative Context Improves
Multimodal Embedding. arXiv preprint arXiv:2510.05014 (2025).
[61] Liliane Soares da Costa, Italo L Oliveira, and Renato Fileto. 2023. Text classification using embeddings: a survey.
Knowl. Inf. Syst. 65, 7 (2023), 2761–2803.
[62] Slawomir Dadas, Michal Perelkiewicz, and Rafal Poswiata. 2024. PIRB: A Comprehensive Benchmark of Polish Dense
and Hybrid Text Retrieval Methods. In Proceedings of LREC/COLING. 12761–12774.
[63] Zhuyun Dai, Vincent Y. Zhao, Ji Ma, Yi Luan, Jianmo Ni, Jing Lu, Anton Bakalov, Kelvin Guu, Keith B. Hall, and
Ming-Wei Chang. 2023. Promptagator: Few-shot Dense Retrieval From 8 Examples. In ICLR.
[64] Abhishek Das, Satwik Kottur, Khushi Gupta, Avi Singh, Deshraj Yadav, José M. F. Moura, Devi Parikh, and Dhruv
Batra. 2017. Visual Dialog. In Proceedings of CVPR. IEEE Computer Society, 1080–1089.
[65] DataCanary, hilfialkaff, Lili Jiang, Meg Risdal, Nikhil Dandekar, and tomtung. 2017. Quora Question Pairs.
[66] Scott Deerwester, Susan T Dumais, George W Furnas, Thomas K Landauer, and Richard Harshman. 1990. Indexing
by latent semantic analysis. CIVR 41, 6 (1990), 391–407.
[67] Jia Deng, Wei Dong, Richard Socher, Li-Jia Li, Kai Li, and Li Fei-Fei. 2009. ImageNet: A large-scale hierarchical image
database. In CVPR. IEEE Computer Society, 248–255.
[68] Jinghao Deng, Fanqi Wan, Tao Yang, Xiaojun Quan, and Rui Wang. 2023. Clustering-Aware Negative Sampling for
Unsupervised Sentence Representation. In Findings of ACL. 8713–8729.
[69] Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. 2019. BERT: Pre-training of Deep Bidirectional
Transformers for Language Understanding. In Proceedings of NAACL-HLT. Minneapolis, Minnesota, 4171–4186.
[70] Yangruibo Ding, Saikat Chakraborty, Luca Buratti, Saurabh Pujar, Alessandro Morari, Gail E. Kaiser, and Baishakhi
Ray. 2023. CONCORD: Clone-Aware Contrastive Learning for Source Code. In Proceedings of ISSTA. 26–38.
[71] Kenneth Enevoldsen, Isaac Chung, Imene Kerboua, Márton Kardos, Ashwin Mathur, David Stap, Jay Gala, Wissam
Siblini, Dominik Krzemiński, Genta Indra Winata, et al. 2025. Mmteb: Massive multilingual text embedding benchmark.

J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.

On The Role of Pretrained Language Models in General-Purpose Text Embeddings: A Survey
111:31

arXiv preprint arXiv:2502.13595 (2025).
[72] Kenneth C. Enevoldsen, Márton Kardos, Niklas Muennighoff, and Kristoffer L. Nielbo. 2024. The Scandinavian
Embedding Benchmarks: Comprehensive Assessment of Multilingual and Monolingual Text Embedding. In NeurIPS.
[73] Jean-Baptiste Excoffier, Tom Roehr, Alexei Figueroa, Jens-Michalis Papaioannou, Keno K. Bressem, and Matthieu
Ortala. 2024. Generalist embedding models are better at short-context clinical semantic search than specialized
embedding models. CoRR abs/2401.01943 (2024).
[74] Anthony Fader, Luke Zettlemoyer, and Oren Etzioni. 2014. Open question answering over curated and extracted
knowledge bases. In KDD. ACM, 1156–1165.
[75] Yi Fang, Dongzhe Fan, Daochen Zha, and Qiaoyu Tan. 2024. GAugLLM: Improving Graph Contrastive Learning for
Text-Attributed Graphs with Large Language Models. In KDD. ACM, 747–758.
[76] Salman Faroz. 2024. DisEmbed: Transforming Disease Understanding through Embeddings. CoRR abs/2412.15258
(2024).
[77] Manuel Faysse, Hugues Sibille, Tony Wu, Bilel Omrani, Gautier Viaud, Céline Hudelot, and Pierre Colombo. 2025.
ColPali: Efficient Document Retrieval with Vision Language Models. In ICLR. OpenReview.net.
[78] Fangxiaoyu Feng, Yinfei Yang, Daniel Cer, Naveen Arivazhagan, and Wei Wang. 2022. Language-agnostic BERT
Sentence Embedding. In Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics
(Volume 1: Long Papers). 878–891.
[79] Zhangyin Feng, Daya Guo, Duyu Tang, Nan Duan, Xiaocheng Feng, Ming Gong, Linjun Shou, Bing Qin, Ting Liu,
Daxin Jiang, and Ming Zhou. 2020. CodeBERT: A Pre-Trained Model for Programming and Natural Languages. In
EMNLP (Findings), Vol. EMNLP 2020. 1536–1547.
[80] Jack FitzGerald, Christopher Hench, Charith Peris, Scott Mackie, Kay Rottmann, Ana Sanchez, Aaron Nash, Liam
Urbach, Vishesh Kakarala, Richa Singh, Swetha Ranganath, Laurie Crist, Misha Britan, Wouter Leeuwis, Gökhan Tür,
and Prem Natarajan. 2023. MASSIVE: A 1M-Example Multilingual Natural Language Understanding Dataset with 51
Typologically-Diverse Languages. In ACL (1). Association for Computational Linguistics, 4277–4302.
[81] Thibault Formal, Carlos Lassance, Benjamin Piwowarski, and Stéphane Clinchant. 2022. From distillation to hard
negative sampling: Making sparse neural ir models more effective. In Proceedings of the 45th international ACM SIGIR
conference on research and development in information retrieval. 2353–2359.
[82] Thibault Formal, Benjamin Piwowarski, and Stéphane Clinchant. 2021. SPLADE: Sparse lexical and expansion model
for first stage ranking. In Proceedings of the 44th International ACM SIGIR Conference on Research and Development in
Information Retrieval. 2288–2292.
[83] Wikimedia Foundation. 2024. Wikimedia Downloads. https://dumps.wikimedia.org Accessed: 2024-05-01.
[84] Stephanie Fu, Netanel Tamir, Shobhita Sundaram, Lucy Chai, Richard Zhang, Tali Dekel, and Phillip Isola. 2023.
DreamSim: Learning New Dimensions of Human Visual Similarity using Synthetic Data. In NeurIPS.
[85] Luyu Gao, Yunyi Zhang, Jiawei Han, and Jamie Callan. 2021. Scaling Deep Contrastive Learning Batch Size under
Memory Limited Setup. In Proceedings of RepL4NLP@ACL-IJCNLP. Online, 316–321.
[86] Tianyu Gao, Xingcheng Yao, and Danqi Chen. 2021. SimCSE: Simple Contrastive Learning of Sentence Embeddings.
In EMNLP (1). Association for Computational Linguistics, 6894–6910.
[87] Yunfan Gao, Yun Xiong, Xinyu Gao, Kangxiang Jia, Jinliu Pan, Yuxi Bi, Yi Dai, Jiawei Sun, and Haofen Wang. 2023.
Retrieval-augmented generation for large language models: A survey. arXiv preprint arXiv:2312.10997 (2023).
[88] Gregor Geigle, Nils Reimers, Andreas Rücklé, and Iryna Gurevych. 2021. TWEAC: Transformer with Extendable QA
Agent Classifiers. CoRR abs/2104.07081 (2021).
[89] John M. Giorgi, Osvald Nitski, Bo Wang, and Gary D. Bader. 2021. DeCLUTR: Deep Contrastive Learning for
Unsupervised Textual Representations. In Proceedings of ACL/IJCNLP (1). Association for Computational Linguistics,
879–895.
[90] Maarten Grootendorst. 2022. BERTopic: Neural topic modeling with a class-based TF-IDF procedure. arXiv preprint
arXiv:2203.05794 (2022).
[91] Tiancheng Gu, Kaicheng Yang, Ziyong Feng, Xingjun Wang, Yanzhao Zhang, Dingkun Long, Yingda Chen, Weidong
Cai, and Jiankang Deng. 2025. Breaking the Modality Barrier: Universal Embedding Learning with Multimodal LLMs.
CoRR abs/2504.17432 (2025).
[92] Michael Günther, Louis Milliken, Jonathan Geuter, Georgios Mastrapas, Bo Wang, and Han Xiao. 2023. Jina Em-
beddings: A Novel Set of High-Performance Sentence Embedding Models. In Proceedings of NLP-OSS. Singapore,
8–18.
[93] Michael Günther, Jackmin Ong, Isabelle Mohr, Alaeddine Abdessalem, Tanguy Abel, Mohammad Kalim Akram, Susana
Guzman, Georgios Mastrapas, Saba Sturua, Bo Wang, et al. 2023. Jina embeddings 2: 8192-token general-purpose text
embeddings for long documents. arXiv preprint arXiv:2310.19923 (2023).
[94] Michael Günther, Saba Sturua, Mohammad Kalim Akram, Isabelle Mohr, Andrei Ungureanu, Sedigheh Eslami, Scott
Martens, Bo Wang, Nan Wang, and Han Xiao. 2025. jina-embeddings-v4: Universal Embeddings for Multimodal

J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.

111:32
Zhang et al.

Multilingual Retrieval. arXiv preprint arXiv:2506.18902 (2025).
[95] Daya Guo, Shuai Lu, Nan Duan, Yanlin Wang, Ming Zhou, and Jian Yin. 2022. UniXcoder: Unified Cross-Modal
Pre-training for Code Representation. In Proceedings of ACL (1). 7212–7225.
[96] Daya Guo, Shuo Ren, Shuai Lu, Zhangyin Feng, Duyu Tang, Shujie Liu, Long Zhou, Nan Duan, Alexey Svyatkovskiy,
Shengyu Fu, Michele Tufano, Shao Kun Deng, Colin B. Clement, Dawn Drain, Neel Sundaresan, Jian Yin, Daxin Jiang,
and Ming Zhou. 2021. GraphCodeBERT: Pre-training Code Representations with Data Flow. In ICLR.
[97] Daya Guo, Qihao Zhu, Dejian Yang, Zhenda Xie, Kai Dong, Wentao Zhang, Guanting Chen, Xiao Bi, Y. Wu, Y. K.
Li, Fuli Luo, Yingfei Xiong, and Wenfeng Liang. 2024. DeepSeek-Coder: When the Large Language Model Meets
Programming - The Rise of Code Intelligence. CoRR abs/2401.14196 (2024).
[98] Jiafeng Guo, Yinqiong Cai, Yixing Fan, Fei Sun, Ruqing Zhang, and Xueqi Cheng. 2022. Semantic Models for the
First-Stage Retrieval: A Comprehensive Review. ACM Trans. Inf. Syst. 40, 4, Article 66 (mar 2022), 42 pages.
[99] Kelvin Guu, Kenton Lee, Zora Tung, Panupong Pasupat, and Mingwei Chang. 2020. Retrieval augmented language
model pre-training. In Proceedings of ICML. PMLR, 3929–3938.
[100] Felix Hamborg, Norman Meuschke, Corinna Breitinger, and Bela Gipp. 2017. news-please - A Generic News Crawler
and Extractor. In ISI (Schriften zur Informationswissenschaft, Vol. 70). Verlag Werner Hülsbusch, 218–223.
[101] Xintong Han, Zuxuan Wu, Phoenix X. Huang, Xiao Zhang, Menglong Zhu, Yuan Li, Yang Zhao, and Larry S. Davis.
2017. Automatic Spatially-Aware Fashion Concept Discovery. In ICCV. IEEE Computer Society, 1472–1480.
[102] Tahmid Hasan, Abhik Bhattacharjee, Md. Saiful Islam, Kazi Samin Mubasshir, Yuan-Fang Li, Yong-Bin Kang, M. Sohel
Rahman, and Rifat Shahriyar. 2021. XL-Sum: Large-Scale Multilingual Abstractive Summarization for 44 Languages.
In ACL/IJCNLP (Findings) (Findings of ACL, Vol. ACL/IJCNLP 2021). 4693–4703.
[103] Wei He, Kai Liu, Jing Liu, Yajuan Lyu, Shiqi Zhao, Xinyan Xiao, Yuan Liu, Yizhong Wang, Hua Wu, Qiaoqiao She,
Xuan Liu, Tian Wu, and Haifeng Wang. 2018. DuReader: a Chinese Machine Reading Comprehension Dataset from
Real-world Applications. In QA@ACL. Association for Computational Linguistics, 37–46.
[104] Kevin Heffernan, Onur Çelebi, and Holger Schwenk. 2022. Bitext Mining Using Distilled Sentence Representations
for Low-Resource Languages. In EMNLP (Findings). 2101–2112.
[105] Lisa Anne Hendricks, Oliver Wang, Eli Shechtman, Josef Sivic, Trevor Darrell, and Bryan C. Russell. 2017. Localizing
Moments in Video with Natural Language. In ICCV. IEEE Computer Society, 5804–5813.
[106] Dan Hendrycks, Steven Basart, Saurav Kadavath, Mantas Mazeika, Akul Arora, Ethan Guo, Collin Burns, Samir
Puranik, Horace He, Dawn Song, and Jacob Steinhardt. 2021. Measuring Coding Challenge Competence With APPS.
In NeurIPS Datasets and Benchmarks.
[107] Felix Hill, Kyunghyun Cho, and Anna Korhonen. 2016. Learning distributed representations of sentences from
unlabelled data. arXiv preprint arXiv:1602.03483 (2016).
[108] Yupeng Hou, Jiacheng Li, Zhankui He, An Yan, Xiusi Chen, and Julian J. McAuley. 2024. Bridging Language and
Items for Retrieval and Recommendation. CoRR abs/2403.03952 (2024).
[109] Jeremy Howard and Sebastian Ruder. 2018. Universal language model fine-tuning for text classification. arXiv preprint
arXiv:1801.06146 (2018).
[110] Baotian Hu, Qingcai Chen, and Fangze Zhu. 2015. LCSTS: A Large Scale Chinese Short Text Summarization Dataset.
In EMNLP. The Association for Computational Linguistics, 1967–1972.
[111] Hexiang Hu, Yi Luan, Yang Chen, Urvashi Khandelwal, Mandar Joshi, Kenton Lee, Kristina Toutanova, and Ming-Wei
Chang. 2023. Open-domain Visual Entity Recognition: Towards Recognizing Millions of Wikipedia Entities. In ICCV.
IEEE, 12031–12041.
[112] Xinshuo Hu, Zifei Shan, Xinping Zhao, Zetian Sun, Zhenyu Liu, Dongfang Li, Shaolin Ye, Xinyuan Wei, Qian Chen,
Baotian Hu, et al. 2025. KaLM-Embedding: Superior Training Data Brings A Stronger Embedding Model. arXiv
preprint arXiv:2501.01028 (2025).
[113] Junjie Huang, Duyu Tang, Linjun Shou, Ming Gong, Ke Xu, Daxin Jiang, Ming Zhou, and Nan Duan. 2021. CoSQA:
20, 000+ Web Queries for Code Search and Question Answering. In Proceedings of ACL/IJCNLP (1). 5690–5700.
[114] Junjie Huang, Duyu Tang, Wanjun Zhong, Shuai Lu, Linjun Shou, Ming Gong, Daxin Jiang, and Nan Duan. 2021.
WhiteningBERT: An Easy Unsupervised Sentence Embedding Approach. In Findings of EMNLP. Association for
Computational Linguistics, 238–244.
[115] Jui-Ting Huang, Ashish Sharma, Shuying Sun, Li Xia, David Zhang, Philip Pronin, Janani Padmanabhan, Giuseppe
Ottaviano, and Linjun Yang. 2020. Embedding-based retrieval in facebook search. In Proceedings of KDD. 2553–2561.
[116] Yu-Hsiang Huang, Yu-Che Tsai, Hsiang Hsiao, Hong-Yi Lin, and Shou-De Lin. 2024. Transferable Embedding Inversion
Attack: Uncovering Privacy Risks in Text Embeddings without Model Queries. In Proceedings of ACL. 4193–4205.
[117] Hamel Husain, Ho-Hsiang Wu, Tiferet Gazit, Miltiadis Allamanis, and Marc Brockschmidt. 2019. CodeSearchNet
Challenge: Evaluating the State of Semantic Code Search. CoRR abs/1909.09436 (2019).
[118] Srinivasan Iyer, Ioannis Konstas, Alvin Cheung, and Luke Zettlemoyer. 2018. Mapping Language to Code in Pro-
grammatic Context. In Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing.

J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.

On The Role of Pretrained Language Models in General-Purpose Text Embeddings: A Survey
111:33

1643–1652.
[119] Gautier Izacard, Mathilde Caron, Lucas Hosseini, Sebastian Riedel, Piotr Bojanowski, Armand Joulin, and Edouard
Grave. 2022. Unsupervised Dense Information Retrieval with Contrastive Learning. Trans. Mach. Learn. Res. 2022
(2022).
[120] Paras Jain, Ajay Jain, Tianjun Zhang, Pieter Abbeel, Joseph E Gonzalez, and Ion Stoica. 2020. Contrastive code
representation learning. arXiv preprint arXiv:2007.04973 (2020).
[121] Vitor Jeronymo, Luiz Henrique Bonifacio, Hugo Queiroz Abonizio, Marzieh Fadaee, Roberto A. Lotufo, Jakub Zavrel,
and Rodrigo Nogueira. 2023. InPars-v2: Large Language Models as Efficient Dataset Generators for Information
Retrieval. CoRR abs/2301.01820 (2023).
[122] Chao Jia, Yinfei Yang, Ye Xia, Yi-Ting Chen, Zarana Parekh, Hieu Pham, Quoc V. Le, Yun-Hsuan Sung, Zhen Li, and
Tom Duerig. 2021. Scaling Up Visual and Vision-Language Representation Learning With Noisy Text Supervision. In
Proceedings of ICML, Vol. 139. 4904–4916.
[123] Jinhao Jiang, Kun Zhou, Zican Dong, Keming Ye, Xin Zhao, and Ji-Rong Wen. 2023. StructGPT: A General Framework
for Large Language Model to Reason over Structured Data. In EMNLP. Association for Computational Linguistics,
9237–9251.
[124] Ting Jiang, Jian Jiao, Shaohan Huang, Zihan Zhang, Deqing Wang, Fuzhen Zhuang, Furu Wei, Haizhen Huang, Denvy
Deng, and Qi Zhang. 2022. PromptBERT: Improving BERT Sentence Embeddings with Prompts. In Proceedings of
EMNLP. Abu Dhabi, United Arab Emirates, 8826–8837.
[125] Ting Jiang, Minghui Song, Zihan Zhang, Haizhen Huang, Weiwei Deng, Feng Sun, Qi Zhang, Deqing Wang, and
Fuzhen Zhuang. 2024. E5-V: Universal Embeddings with Multimodal Large Language Models. CoRR abs/2407.12580
(2024).
[126] Xue Jiang, Zhuoran Zheng, Chen Lyu, Liang Li, and Lei Lyu. 2021. TreeBERT: A tree-based pre-trained model for
programming language. In UAI (Proceedings of Machine Learning Research, Vol. 161). 54–63.
[127] Yuxin Jiang, Linhan Zhang, and Wei Wang. 2022. Improved Universal Sentence Embeddings with Prompt-based
Contrastive Learning and Energy-based Learning. In Findings of EMNLP. Association for Computational Linguistics,
3021–3035.
[128] Ziyan Jiang, Rui Meng, Xinyi Yang, Semih Yavuz, Yingbo Zhou, and Wenhu Chen. 2025. VLM2Vec: Training
Vision-Language Models for Massive Multimodal Embedding Tasks. In ICLR.
[129] Qiao Jin, Bhuwan Dhingra, Zhengping Liu, William W. Cohen, and Xinghua Lu. 2019. PubMedQA: A Dataset
for Biomedical Research Question Answering. In EMNLP/IJCNLP (1). Association for Computational Linguistics,
2567–2577.
[130] Mandar Joshi, Eunsol Choi, Daniel S. Weld, and Luke Zettlemoyer. 2017. TriviaQA: A Large Scale Distantly Supervised
Challenge Dataset for Reading Comprehension. In ACL (1). Association for Computational Linguistics, 1601–1611.
[131] Nal Kalchbrenner, Edward Grefenstette, and Phil Blunsom. 2014. A convolutional neural network for modelling
sentences. arXiv preprint arXiv:1404.2188 (2014).
[132] Aditya Kanade, Petros Maniatis, Gogul Balakrishnan, and Kensen Shi. 2020. Learning and Evaluating Contextual
Embedding of Source Code. In Proceedings of ICML (Proceedings of Machine Learning Research, Vol. 119). 5110–5121.
[133] Rafael-Michael Karampatsis and Charles Sutton. 2020. SCELMo: Source Code Embeddings from Language Models.
CoRR abs/2004.13214 (2020).
[134] Vladimir Karpukhin, Barlas Oguz, Sewon Min, Patrick Lewis, Ledell Wu, Sergey Edunov, Danqi Chen, and Wen-tau Yih.
2020. Dense Passage Retrieval for Open-Domain Question Answering. In Proceedings of EMNLP. Online, 6769–6781.
[135] Sahar Kazemzadeh, Vicente Ordonez, Mark Matten, and Tamara L. Berg. 2014. ReferItGame: Referring to Objects in
Photographs of Natural Scenes. In Proceedings of EMNLP. 787–798.
[136] Imed Keraghel, Stanislas Morbieu, and Mohamed Nadif. 2024. Beyond words: a comparative analysis of LLM
embeddings for effective clustering. In IDA. Springer, 205–216.
[137] Daniel Khashabi, Amos Ng, Tushar Khot, Ashish Sabharwal, Hannaneh Hajishirzi, and Chris Callison-Burch. 2021.
GooAQ: Open Question Answering with Diverse Answer Types. In EMNLP (Findings). Association for Computational
Linguistics, 421–433.
[138] Omar Khattab and Matei Zaharia. 2020. ColBERT: Efficient and Effective Passage Search via Contextualized Late
Interaction over BERT. In Proceedings of SIGIR. 39–48.
[139] Jiho Kim, Yeonsu Kwon, Yohan Jo, and Edward Choi. 2023. KG-GPT: A General Framework for Reasoning on
Knowledge Graphs Using Large Language Models. In EMNLP (Findings). Association for Computational Linguistics,
9410–9421.
[140] Taeuk Kim, Kang Min Yoo, and Sang-goo Lee. 2021. Self-Guided Contrastive Learning for BERT Sentence Representa-
tions. In Proceedings of the 59th ACL-IJCNLP. 2528–2540.
[141] Yoon Kim. 2014. Convolutional Neural Networks for Sentence Classification. In Proceedings of EMNLP. Doha, Qatar,
1746–1751.

J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.

111:34
Zhang et al.

[142] Ryan Kiros, Yukun Zhu, Russ R Salakhutdinov, Richard Zemel, Raquel Urtasun, Antonio Torralba, and Sanja Fidler.
2015. Skip-thought vectors. NIPS 28 (2015).
[143] Tassilo Klein and Moin Nabi. 2022. SCD: Self-Contrastive Decorrelation of Sentence Embeddings. In Proceedings of
ACL (2). Association for Computational Linguistics, 394–400.
[144] Denis Kocetkov, Raymond Li, Loubna Ben Allal, Jia Li, Chenghao Mou, Yacine Jernite, Margaret Mitchell, Carlos Muñoz
Ferrandis, Sean Hughes, Thomas Wolf, Dzmitry Bahdanau, Leandro von Werra, and Harm de Vries. 2023. The Stack:
3 TB of permissively licensed source code. Trans. Mach. Learn. Res. 2023 (2023).
[145] Fanheng Kong, Jingyuan Zhang, Yahui Liu, Hongzhi Zhang, Shi Feng, Xiaocui Yang, Daling Wang, Yu Tian, Victoria
W., Fuzheng Zhang, and Guorui Zhou. 2025. Modality Curation: Building Universal Embeddings for Advanced
Multimodal Information Retrieval. CoRR abs/2505.19650 (2025).
[146] Yuta Koreeda and Christopher D. Manning. 2021. ContractNLI: A Dataset for Document-level Natural Language
Inference for Contracts. In EMNLP (Findings). Association for Computational Linguistics, 1907–1919.
[147] Andreas Koukounas, Georgios Mastrapas, Bo Wang, Mohammad Kalim Akram, Sedigheh Eslami, Michael Günther,
Isabelle Mohr, Saba Sturua, Scott Martens, Nan Wang, and Han Xiao. 2024. jina-clip-v2: Multilingual Multimodal
Embeddings for Text and Images. CoRR abs/2412.08802 (2024).
[148] Mahnaz Koupaee and William Yang Wang. 2018. WikiHow: A Large Scale Text Summarization Dataset. CoRR
abs/1810.09305 (2018).
[149] Aditya Kusupati, Gantavya Bhatt, Aniket Rege, Matthew Wallingford, Aditya Sinha, Vivek Ramanujan, William
Howard-Snyder, Kaifeng Chen, Sham Kakade, Prateek Jain, et al. 2022. Matryoshka representation learning. CoRR 35
(2022), 30233–30249.
[150] Tom Kwiatkowski, Jennimaria Palomaki, Olivia Redfield, Michael Collins, Ankur P. Parikh, Chris Alberti, Danielle
Epstein, Illia Polosukhin, Jacob Devlin, Kenton Lee, Kristina Toutanova, Llion Jones, Matthew Kelcey, Ming-Wei
Chang, Andrew M. Dai, Jakob Uszkoreit, Quoc Le, and Slav Petrov. 2019. Natural Questions: a Benchmark for Question
Answering Research. Trans. Assoc. Comput. Linguistics 7 (2019), 452–466.
[151] Marie-Anne Lachaux, Baptiste Rozière, Marc Szafraniec, and Guillaume Lample. 2021. DOBF: A Deobfuscation
Pre-Training Objective for Programming Languages. In NeurIPS. 14967–14979.
[152] Zhibin Lan, Liqiang Niu, Fandong Meng, Jie Zhou, and Jinsong Su. 2025. LLaVE: Large Language and Vision
Embedding Models with Hardness-Weighted Contrastive Learning. CoRR abs/2503.04812 (2025).
[153] Quoc Le and Tomas Mikolov. 2014. Distributed representations of sentences and documents. In Proceedings of ICML.
PMLR, 1188–1196.
[154] Chankyu Lee, Rajarshi Roy, Mengyao Xu, Jonathan Raiman, Mohammad Shoeybi, Bryan Catanzaro, and Wei Ping.
2025. NV-Embed: Improved Techniques for Training LLMs as Generalist Embedding Models. In Proceedings of ICLR.
[155] Jinhyuk Lee, Feiyang Chen, Sahil Dua, Daniel Cer, Madhuri Shanbhogue, Iftekhar Naim, Gustavo Hernández Ábrego,
Zhe Li, Kaifeng Chen, Henrique Schechter Vera, Xiaoqi Ren, Shanfeng Zhang, Daniel Salz, Michael Boratko, Jay
Han, Blair Chen, Shuo Huang, Vikram Rao, Paul Suganthan, Feng Han, Andreas Doumanoglou, Nithi Gupta, Fedor
Moiseev, Cathy Yip, Aashi Jain, Simon Baumgartner, Shahrokh Shahi, Frank Palma Gomez, Sandeep Mariserla, Min
Choi, Parashar Shah, Sonam Goenka, Ke Chen, Ye Xia, Koert Chen, Sai Meher Karthik Duddu, Yichang Chen, Trevor
Walker, Wenlei Zhou, Rakesh Ghiya, Zach Gleicher, Karan Gill, Zhe Dong, Mojtaba Seyedhosseini, Yun-Hsuan Sung,
Raphael Hoffmann, and Tom Duerig. 2025. Gemini Embedding: Generalizable Embeddings from Gemini. CoRR
abs/2503.07891 (2025).
[156] Jinhyuk Lee, Zhuyun Dai, Xiaoqi Ren, Blair Chen, Daniel Cer, Jeremy R Cole, Kai Hui, Michael Boratko, Rajvi Kapadia,
Wen Ding, et al. 2024. Gecko: Versatile Text Embeddings Distilled from Large Language Models. arXiv preprint
arXiv:2403.20327 (2024).
[157] Jinhyuk Lee, Wonjin Yoon, Sungdong Kim, Donghyeon Kim, Sunkyu Kim, Chan Ho So, and Jaewoo Kang. 2020.
BioBERT: a pre-trained biomedical language representation model for biomedical text mining. Bioinform. 36, 4 (2020),
1234–1240.
[158] Patrick Lewis, Barlas Oguz, Ruty Rinott, Sebastian Riedel, and Holger Schwenk. 2020. MLQA: Evaluating Cross-lingual
Extractive Question Answering. In Proceedings of ACL. 7315–7330.
[159] Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Küttler,
Mike Lewis, Wen-tau Yih, Tim Rocktäschel, Sebastian Riedel, and Douwe Kiela. 2020. Retrieval-Augmented Generation
for Knowledge-Intensive NLP Tasks. In NeurIPS.
[160] Patrick Lewis, Yuxiang Wu, Linqing Liu, Pasquale Minervini, Heinrich Küttler, Aleksandra Piktus, Pontus Stenetorp,
and Sebastian Riedel. 2021. PAQ: 65 Million Probably-Asked Questions and What You Can Do With Them. Trans.
Assoc. Comput. Linguistics 9 (2021), 1098–1115.
[161] Bohan Li, Hao Zhou, Junxian He, Mingxuan Wang, Yiming Yang, and Lei Li. 2020. On the Sentence Embeddings from
Pre-trained Language Models. In Proceedings of EMNLP (1). Association for Computational Linguistics, 9119–9130.

J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.

On The Role of Pretrained Language Models in General-Purpose Text Embeddings: A Survey
111:35

[162] Chaofan Li, MingHao Qin, Shitao Xiao, Jianlyu Chen, Kun Luo, Yingxia Shao, Defu Lian, and Zheng Liu. 2025. Making
text embedders few-shot learners. In Proceedings of ICLR.
[163] Haoran Li, Abhinav Arora, Shuohui Chen, Anchit Gupta, Sonal Gupta, and Yashar Mehdad. 2021. MTOP: A Compre-
hensive Multilingual Task-Oriented Semantic Parsing Benchmark. In EACL. Association for Computational Linguistics,
2950–2962.
[164] Haoran Li, Mingshi Xu, and Yangqiu Song. 2023. Sentence Embedding Leaks More Information than You Expect:
Generative Embedding Inversion Attack to Recover the Whole Sentence. In Findings of ACL. 14022–14040.
[165] Junnan Li, Dongxu Li, Silvio Savarese, and Steven C. H. Hoi. 2023. BLIP-2: Bootstrapping Language-Image Pre-training
with Frozen Image Encoders and Large Language Models. In ICML (Proceedings of Machine Learning Research, Vol. 202).
19730–19742.
[166] Junnan Li, Dongxu Li, Caiming Xiong, and Steven C. H. Hoi. 2022. BLIP: Bootstrapping Language-Image Pre-training
for Unified Vision-Language Understanding and Generation. In ICML (Proceedings of Machine Learning Research,
Vol. 162). 12888–12900.
[167] Lei Li, Yuqi Wang, Runxin Xu, Peiyi Wang, Xiachong Feng, Lingpeng Kong, and Qi Liu. 2024. Multimodal ArXiv:
A Dataset for Improving Scientific Comprehension of Large Vision-Language Models. In Proceedings of ACL (1).
Association for Computational Linguistics, 14369–14387.
[168] Mingxin Li, Richong Zhang, Zhijie Nie, and Yongyi Mao. 2024. Narrowing the Gap between Supervised and
Unsupervised Sentence Representation Learning with Large Language Model. In AAAI. 13590–13599.
[169] Raymond Li, Loubna Ben Allal, Yangtian Zi, Niklas Muennighoff, Denis Kocetkov, Chenghao Mou, Marc Marone,
Christopher Akiki, Jia Li, Jenny Chim, Qian Liu, Evgenii Zheltonozhskii, Terry Yue Zhuo, Thomas Wang, Olivier
Dehaene, Mishig Davaadorj, Joel Lamy-Poirier, João Monteiro, Oleh Shliazhko, Nicolas Gontier, Nicholas Meade,
Armel Zebaze, Ming-Ho Yee, Logesh Kumar Umapathi, Jian Zhu, Benjamin Lipkin, Muhtasham Oblokulov, Zhiruo
Wang, Rudra Murthy V, Jason T. Stillerman, Siva Sankalp Patel, Dmitry Abulkhanov, Marco Zocca, Manan Dey,
Zhihan Zhang, Nour Fahmy, Urvashi Bhattacharyya, Wenhao Yu, Swayam Singh, Sasha Luccioni, Paulo Villegas,
Maxim Kunakov, Fedor Zhdanov, Manuel Romero, Tony Lee, Nadav Timor, Jennifer Ding, Claire Schlesinger, Hailey
Schoelkopf, Jan Ebert, Tri Dao, Mayank Mishra, Alex Gu, Jennifer Robinson, Carolyn Jane Anderson, Brendan Dolan-
Gavitt, Danish Contractor, Siva Reddy, Daniel Fried, Dzmitry Bahdanau, Yacine Jernite, Carlos Muñoz Ferrandis, Sean
Hughes, Thomas Wolf, Arjun Guha, Leandro von Werra, and Harm de Vries. 2023. StarCoder: may the source be with
you! Trans. Mach. Learn. Res. 2023 (2023).
[170] Rui Li, Liyang He, Qi Liu, Zheng Zhang, Heng Yu, Yuyang Ye, Linbo Zhu, and Yu Su. 2025. UniRAG: Unified Query
Understanding Method for Retrieval Augmented Generation. In ACL (1). Association for Computational Linguistics,
14163–14178.
[171] Rui Li, Qi Liu, Liyang He, Zheng Zhang, Hao Zhang, Shengyu Ye, Junyu Lu, and Zhenya Huang. 2024. Optimizing
Code Retrieval: High-Quality and Scalable Dataset Annotation through Large Language Models. In Proceedings of
EMNLP. 2053–2065.
[172] Ruiqi Li, Xiang Zhao, and Marie-Francine Moens. 2023. A Brief Overview of Universal Sentence Representation
Methods: A Linguistic View. ACM Comput. Surv. 55, 3 (2023), 56:1–56:42.
[173] Xiaonan Li, Yeyun Gong, Yelong Shen, Xipeng Qiu, Hang Zhang, Bolun Yao, Weizhen Qi, Daxin Jiang, Weizhu Chen,
and Nan Duan. 2022. CodeRetriever: A Large Scale Contrastive Pre-Training Method for Code Search. In Proceedings
of EMNLP. 2898–2910.
[174] Xiaonan Li, Daya Guo, Yeyun Gong, Yun Lin, Yelong Shen, Xipeng Qiu, Daxin Jiang, Weizhu Chen, and Nan Duan.
2022. Soft-Labeled Contrastive Pre-Training for Function-Level Code Representation. In EMNLP (Findings). 118–129.
[175] Xianming Li and Jing Li. 2024. AoE: Angle-optimized Embeddings for Semantic Textual Similarity. In Proceedings of
ACL (1). 1825–1839.
[176] Yuanzhi Li, Sébastien Bubeck, Ronen Eldan, Allie Del Giorno, Suriya Gunasekar, and Yin Tat Lee. 2023. Textbooks
Are All You Need II: phi-1.5 technical report. CoRR abs/2309.05463 (2023).
[177] Yujia Li, David H. Choi, Junyoung Chung, Nate Kushman, Julian Schrittwieser, Rémi Leblond, Tom Eccles, James
Keeling, Felix Gimeno, Agustin Dal Lago, Thomas Hubert, Peter Choy, Cyprien de Masson d’Autume, Igor Babuschkin,
Xinyun Chen, Po-Sen Huang, Johannes Welbl, Sven Gowal, Alexey Cherepanov, James Molloy, Daniel J. Mankowitz,
Esme Sutherland Robson, Pushmeet Kohli, Nando de Freitas, Koray Kavukcuoglu, and Oriol Vinyals. 2022. Competition-
Level Code Generation with AlphaCode. CoRR abs/2203.07814 (2022).
[178] Yiyang Li, Hongqiu Wu, and Hai Zhao. 2023. Contrastive Learning of Functionality-Aware Code Embeddings. In
ICASSP. 1–5.
[179] Yudong Li, Yuqing Zhang, Zhe Zhao, Linlin Shen, Weijie Liu, Weiquan Mao, and Hui Zhang. 2022. CSL: A Large-scale
Chinese Scientific Literature Dataset. In COLING. International Committee on Computational Linguistics, 3917–3923.
[180] Zehan Li, Xin Zhang, Yanzhao Zhang, Dingkun Long, Pengjun Xie, and Meishan Zhang. 2023. Towards general text
embeddings with multi-stage contrastive learning. arXiv preprint arXiv:2308.03281 (2023).

J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.

111:36
Zhang et al.

[181] Ziyue Li and Tianyi Zhou. 2025. Your Mixture-of-Experts LLM Is Secretly an Embedding Model for Free. In ICLR.
OpenReview.net.
[182] Paul Pu Liang, Irene Mengze Li, Emily Zheng, Yao Chong Lim, Ruslan Salakhutdinov, and Louis-Philippe Morency.
2020. Towards Debiasing Sentence Representations. In ACL. Association for Computational Linguistics, 5502–5515.
[183] Tsung-Yi Lin, Michael Maire, Serge J. Belongie, James Hays, Pietro Perona, Deva Ramanan, Piotr Dollár, and
C. Lawrence Zitnick. 2014. Microsoft COCO: Common Objects in Context. In ECCV (5) (Lecture Notes in Com-
puter Science, Vol. 8693). Springer, 740–755.
[184] Weizhe Lin, Jingbiao Mei, Jinghong Chen, and Bill Byrne. 2024. PreFLMR: Scaling Up Fine-Grained Late-Interaction
Multi-modal Retrievers. In Proceedings of ACL (1). Association for Computational Linguistics, 5294–5316.
[185] Fangyu Liu, Ivan Vulic, Anna Korhonen, and Nigel Collier. 2021. Fast, Effective, and Self-Supervised: Transforming
Masked Language Models into Universal Lexical and Sentence Encoders. In Proceedings of EMNLP (1). Association for
Computational Linguistics, 1442–1459.
[186] Fuxiao Liu, Yinghan Wang, Tianlu Wang, and Vicente Ordonez. 2021. Visual News: Benchmark and Challenges in
News Image Captioning. In Proceedings ofEMNLP (1). 6761–6771.
[187] Jiduan Liu, Jiahao Liu, Qifan Wang, Jingang Wang, Wei Wu, Yunsen Xian, Dongyan Zhao, Kai Chen, and Rui Yan.
2023. RankCSE: Unsupervised Sentence Representations Learning via Learning to Rank. In Proceedings of ACL.
13785–13802.
[188] Siqi Liu, Weixi Feng, Tsu-Jui Fu, Wenhu Chen, and William Wang. 2023. EDIS: Entity-Driven Image Search over
Multimodal Web Content. In Proceedings of EMNLP. Association for Computational Linguistics, 4877–4894.
[189] Shangqing Liu, Bozhi Wu, Xiaofei Xie, Guozhu Meng, and Yang Liu. 2023. ContraBERT: Enhancing Code Pre-trained
Models via Contrastive Learning. In ICSE. 2476–2487.
[190] Yinhan Liu, Myle Ott, Naman Goyal, Jingfei Du, Mandar Joshi, Danqi Chen, Omer Levy, Mike Lewis, Luke Zettlemoyer,
and Veselin Stoyanov. 2019. Roberta: A robustly optimized bert pretraining approach. arXiv preprint arXiv:1907.11692
(2019).
[191] Zheyuan Liu, Cristian Rodriguez Opazo, Damien Teney, and Stephen Gould. 2021. Image Retrieval on Real-life Images
with Pre-trained Vision-and-Language Models. In ICCV. IEEE, 2105–2114.
[192] Shayne Longpre, Yi Lu, and Joachim Daiber. 2021. MKQA: A Linguistically Diverse Benchmark for Multilingual Open
Domain Question Answering. Trans. Assoc. Comput. Linguistics 9 (2021), 1389–1406.
[193] Anton Lozhkov, Raymond Li, Loubna Ben Allal, Federico Cassano, Joel Lamy-Poirier, Nouamane Tazi, Ao Tang,
Dmytro Pykhtar, Jiawei Liu, Yuxiang Wei, Tianyang Liu, Max Tian, Denis Kocetkov, Arthur Zucker, Younes Belkada,
Zijian Wang, Qian Liu, Dmitry Abulkhanov, Indraneil Paul, Zhuang Li, Wen-Ding Li, Megan Risdal, Jia Li, Jian Zhu,
Terry Yue Zhuo, Evgenii Zheltonozhskii, Nii Osae Osae Dade, Wenhao Yu, Lucas Krauß, Naman Jain, Yixuan Su,
Xuanli He, Manan Dey, Edoardo Abati, Yekun Chai, Niklas Muennighoff, Xiangru Tang, Muhtasham Oblokulov,
Christopher Akiki, Marc Marone, Chenghao Mou, Mayank Mishra, Alex Gu, Binyuan Hui, Tri Dao, Armel Zebaze,
Olivier Dehaene, Nicolas Patry, Canwen Xu, Julian J. McAuley, Han Hu, Torsten Scholak, Sébastien Paquet, Jennifer
Robinson, Carolyn Jane Anderson, Nicolas Chapados, and et al. 2024. StarCoder 2 and The Stack v2: The Next
Generation. CoRR abs/2402.19173 (2024).
[194] Shuai Lu, Daya Guo, Shuo Ren, Junjie Huang, Alexey Svyatkovskiy, Ambrosio Blanco, Colin Clement, Dawn Drain,
Daxin Jiang, Duyu Tang, et al. [n. d.]. CodeXGLUE: A Machine Learning Benchmark Dataset for Code Understanding
and Generation. In Thirty-fifth Conference on Neural Information Processing Systems Datasets and Benchmarks Track
(Round 1).
[195] Man Luo, Zhiyuan Fang, Tejas Gokhale, Yezhou Yang, and Chitta Baral. 2023. End-to-end Knowledge Retrieval with
Multi-modal Queries. In Proceedings of ACL (1). Association for Computational Linguistics, 8573–8589.
[196] Guangyuan Ma, Xing Wu, Peng Wang, Zijia Lin, and Songlin Hu. 2023. Pre-training with large language model-based
document expansion for dense passage retrieval. arXiv preprint arXiv:2308.08285 (2023).
[197] Xueguang Ma, Sheng-Chieh Lin, Minghan Li, Wenhu Chen, and Jimmy Lin. 2024. Unifying Multimodal Retrieval via
Document Screenshot Embedding. In Proceedings ofEMNLP. Association for Computational Linguistics, 6492–6505.
[198] Andrew L. Maas, Raymond E. Daly, Peter T. Pham, Dan Huang, Andrew Y. Ng, and Christopher Potts. 2011. Learning
Word Vectors for Sentiment Analysis. In ACL. The Association for Computer Linguistics, 142–150.
[199] Macedo Maia, Siegfried Handschuh, André Freitas, Brian Davis, Ross McDermott, Manel Zarrouk, and Alexandra
Balahur. 2018. WWW’18 Open Challenge: Financial Opinion Mining and Question Answering. In WWW (Companion
Volume). ACM, 1941–1942.
[200] Christopher D Manning. 2009. An introduction to information retrieval.
[201] Kenneth Marino, Mohammad Rastegari, Ali Farhadi, and Roozbeh Mottaghi. 2019. OK-VQA: A Visual Question
Answering Benchmark Requiring External Knowledge. In CVPR. Computer Vision Foundation / IEEE, 3195–3204.
[202] Mostafa Masumi, Seyed Soroush Majd, Mehrnoush Shamsfard, and Hamid Beigy. 2024. FaBERT: Pre-training BERT
on Persian Blogs. CoRR abs/2402.06617 (2024).

J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.

On The Role of Pretrained Language Models in General-Purpose Text Embeddings: A Survey
111:37

[203] Minesh Mathew, Viraj Bagal, Rubèn Tito, Dimosthenis Karatzas, Ernest Valveny, and C. V. Jawahar. 2022. Infograph-
icVQA. In WACV. IEEE, 2582–2591.
[204] Minesh Mathew, Dimosthenis Karatzas, and C. V. Jawahar. 2021. DocVQA: A Dataset for VQA on Document Images.
In WACV. IEEE, 2199–2208.
[205] James Mayfield, Eugene Yang, Dawn J. Lawrie, Samuel Barham, Orion Weller, Marc Mason, Suraj Nair, and Scott
Miller. 2023. Synthetic Cross-language Information Retrieval Training Data. CoRR abs/2305.00331 (2023).
[206] Julian J. McAuley and Jure Leskovec. 2013. Hidden factors and hidden topics: understanding rating dimensions with
review text. In RecSys. ACM, 165–172.
[207] Rui Meng, Ziyan Jiang, Ye Liu, Mingyi Su, Xinyi Yang, Yuepeng Fu, Can Qin, Zeyuan Chen, Ran Xu, Caiming Xiong,
et al. 2025. VLM2Vec-V2: Advancing Multimodal Embedding for Videos, Images, and Visual Documents. arXiv
preprint arXiv:2507.04590 (2025).
[208] Rui Meng, Ye Liu, Shafiq Rayhan Joty, Caiming Xiong, Yingbo Zhou, and Semih Yavuz. 2024. SFR-Embedding-
Mistral:Enhance Text Retrieval with Transfer Learning. Salesforce AI Research Blog.
[209] Thomas Mensink, Jasper R. R. Uijlings, Lluís Castrejón, Arushi Goel, Felipe Cadar, Howard Zhou, Fei Sha, André
Araújo, and Vittorio Ferrari. 2023. Encyclopedic VQA: Visual questions about detailed properties of fine-grained
categories. In ICCV. 3090–3101.
[210] Luke Merrick, Danmei Xu, Gaurav Nuti, and Daniel Campos. 2024. Arctic-Embed: Scalable, Efficient, and Accurate
Text Embedding Models. arXiv preprint arXiv:2405.05374 (2024).
[211] Tomas Mikolov, Quoc V Le, and Ilya Sutskever. 2013. Exploiting similarities among languages for machine translation.
arXiv preprint arXiv:1309.4168 (2013).
[212] Tomáš Mikolov, Wen-tau Yih, and Geoffrey Zweig. 2013. Linguistic regularities in continuous space word representa-
tions. In Proceedings of HLT-NAACL. 746–751.
[213] Changrong Min, Yonghe Chu, Liang Yang, Bo Xu, and Hongfei Lin. [n. d.]. Locality Preserving Sentence Encoding. In
Findings of EMNLP. 3050–3060.
[214] Swaroop Mishra, Daniel Khashabi, Chitta Baral, and Hannaneh Hajishirzi. 2022. Cross-Task Generalization via
Natural Language Crowdsourcing Instructions. In Proceedings of ACL. 3470–3487.
[215] Sepideh Mollanorozy, Marc Tanti, and Malvina Nissim. 2023. Cross-lingual transfer learning with Persian. In
Proceedings of the 5th Workshop on Research in Computational Linguistic Typology and Multilingual NLP. 89–95.
[216] John X. Morris and Alexander M. Rush. 2025. Contextual Document Embeddings. In ICLR.
[217] Lili Mou, Ge Li, Lu Zhang, Tao Wang, and Zhi Jin. 2016. Convolutional neural networks over tree structures for
programming language processing. In Proceedings of the AAAI conference on artificial intelligence, Vol. 30.
[218] Jesse Mu, Xiang Lisa Li, and Noah Goodman. 2023. Learning to Compress Prompts with Gist Tokens. In NeurIPS.
[219] Niklas Muennighoff. 2022. Sgpt: Gpt sentence embeddings for semantic search. arXiv preprint arXiv:2202.08904
(2022).
[220] Niklas Muennighoff, Hongjin SU, Liang Wang, Nan Yang, Furu Wei, Tao Yu, Amanpreet Singh, and Douwe Kiela.
2025. Generative Representational Instruction Tuning. In ICLR.
[221] Niklas Muennighoff, Nouamane Tazi, Loic Magne, and Nils Reimers. 2023. MTEB: Massive Text Embedding Benchmark.
In Proceedings of EACL. Dubrovnik, Croatia, 2014–2037.
[222] Niklas Muennighoff, Thomas Wang, Lintang Sutawika, Adam Roberts, Stella Biderman, Teven Le Scao, M. Saiful Bari,
Sheng Shen, Zheng Xin Yong, Hailey Schoelkopf, Xiangru Tang, Dragomir Radev, Alham Fikri Aji, Khalid Almubarak,
Samuel Albanie, Zaid Alyafeai, Albert Webson, Edward Raff, and Colin Raffel. 2023. Crosslingual Generalization
through Multitask Finetuning. In Proceedings of ACL (1). 15991–16111.
[223] Omer Nacar, Anis Koubaa, Serry Sibaee, Yasser AlHabashi, Adel Ammar, and Wadii Boulila. 2025. GATE: General
Arabic Text Embedding for Enhanced Semantic Textual Similarity with Matryoshka Representation Learning and
Hybrid Loss Training. CoRR abs/2505.24581 (2025).
[224] Nikita Nangia, Adina Williams, Angeliki Lazaridou, and Samuel R Bowman. 2017. The repeval 2017 shared task:
Multi-genre natural language inference with sentence representations. arXiv preprint arXiv:1707.08172 (2017).
[225] Arvind Neelakantan, Tao Xu, Raul Puri, Alec Radford, Jesse Michael Han, Jerry Tworek, Qiming Yuan, Nikolas Tezak,
Jong Wook Kim, Chris Hallacy, et al. 2022. Text and code embeddings by contrastive pre-training. arXiv preprint
arXiv:2201.10005 (2022).
[226] Tri Nguyen, Mir Rosenberg, Xia Song, Jianfeng Gao, Saurabh Tiwary, Rangan Majumder, and Li Deng. 2016. MS
MARCO: A Human Generated MAchine Reading COmprehension Dataset. In CoCo@NIPS (CEUR Workshop Proceedings,
Vol. 1773). CEUR-WS.org.
[227] Jianmo Ni, Gustavo Hernandez Abrego, Noah Constant, Ji Ma, Keith Hall, Daniel Cer, and Yinfei Yang. 2022. Sentence-
T5: Scalable Sentence Encoders from Pre-trained Text-to-Text Models. In Findings of ACL. Dublin, Ireland, 1864–1874.
[228] Jianmo Ni, Chen Qu, Jing Lu, Zhuyun Dai, Gustavo Hernández Ábrego, Ji Ma, Vincent Y. Zhao, Yi Luan, Keith B. Hall,
Ming-Wei Chang, and Yinfei Yang. 2022. Large Dual Encoders Are Generalizable Retrievers. In Proceedings of EMNLP.

J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.

111:38
Zhang et al.

9844–9855.
[229] Zhijie Nie, Zhangchi Feng, Mingxin Li, Cunwang Zhang, Yanzhao Zhang, Dingkun Long, and Richong Zhang. 2024.
When Text Embedding Meets Large Language Model: A Comprehensive Survey. arXiv preprint arXiv:2412.09165
(2024).
[230] Erik Nijkamp, Bo Pang, Hiroaki Hayashi, Lifu Tu, Huan Wang, Yingbo Zhou, Silvio Savarese, and Caiming Xiong. 2023.
CodeGen: An Open Large Language Model for Code with Multi-Turn Program Synthesis. In ICLR. OpenReview.net.
[231] Sosuke Nishikawa, Ryokan Ri, Ikuya Yamada, Yoshimasa Tsuruoka, and Isao Echizen. 2022. EASE: Entity-Aware Con-
trastive Learning of Sentence Embedding. In Proceedings of NAACL-HLT. Association for Computational Linguistics,
3870–3885.
[232] Zach Nussbaum and Brandon Duderstadt. 2025. Training Sparse Mixture Of Experts Text Embedding Models. arXiv
preprint arXiv:2502.07972 (2025).
[233] Zach Nussbaum, John Xavier Morris, Andriy Mulyar, and Brandon Duderstadt. 2025. Nomic Embed: Training a
Reproducible Long Context Text Embedder. Trans. Mach. Learn. Res. (2025). Reproducibility Certification.
[234] Dongsuk Oh, Yejin Kim, Hodong Lee, H. Howie Huang, and Heuiseok Lim. 2022. Don’t Judge a Language Model
by Its Last Layer: Contrastive Learning with Layer-Wise Attention Pooling. In Proceedings of COLING. Gyeongju,
Republic of Korea, 4585–4592.
[235] James O’Neill, Polina Rozenshtein, Ryuichi Kiryo, Motoko Kubota, and Danushka Bollegala. 2021. I Wish I Would
Have Loved This One, But I Didn’t - A Multilingual Dataset for Counterfactual Detection in Product Review. In
EMNLP (1). Association for Computational Linguistics, 7092–7108.
[236] Aaron van den Oord, Yazhe Li, and Oriol Vinyals. 2018. Representation learning with contrastive predictive coding.
arXiv preprint arXiv:1807.03748 (2018).
[237] Fangwei Ou and Jinan Xu. 2024. SKICSE: Sentence Knowable Information Prompted by LLMs Improves Contrastive
Sentence Embeddings. In Proceedings of NAACL. 141–146.
[238] Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida, Carroll L. Wainwright, Pamela Mishkin, Chong Zhang, Sandhini
Agarwal, Katarina Slama, Alex Ray, John Schulman, Jacob Hilton, Fraser Kelton, Luke Miller, Maddie Simens, Amanda
Askell, Peter Welinder, Paul F. Christiano, Jan Leike, and Ryan Lowe. 2022. Training language models to follow
instructions with human feedback. In Proceedings of NeurIPS.
[239] Arnold Overwijk, Chenyan Xiong, Xiao Liu, Cameron VandenBerg, and Jamie Callan. 2022. ClueWeb22: 10 Billion
Web Documents with Visual and Semantic Information. arXiv:2211.15848
[240] Kaihang Pan, Juncheng Li, Wenjie Wang, Hao Fei, Hongye Song, Wei Ji, Jun Lin, Xiaozhong Liu, Tat-Seng Chua, and
Siliang Tang. 2024. I3: Intent-Introspective Retrieval Conditioned on Instructions. In Proceedings of SIGIR. 1839–1849.
[241] Joon Sung Park, Joseph O’Brien, Carrie Jun Cai, Meredith Ringel Morris, Percy Liang, and Michael S Bernstein. 2023.
Generative agents: Interactive simulacra of human behavior. In Proceedings of UIST. 1–22.
[242] Xiaohuan Pei, Daochang Liu, Luo Qian, and Chang Xu. 2022. Contrastive Code-Comment Pre-training. In ICDM.
398–407.
[243] Boci Peng, Yun Zhu, Yongchao Liu, Xiaohe Bo, Haizhou Shi, Chuntao Hong, Yan Zhang, and Siliang Tang. 2024.
Graph Retrieval-Augmented Generation: A Survey. CoRR abs/2408.08921 (2024).
[244] Letian Peng, Yuwei Zhang, Zilong Wang, Jayanth Srinivasa, Gaowen Liu, Zihan Wang, and Jingbo Shang. 2024. Answer
is All You Need: Instruction-following Text Embedding via Answering the Question. arXiv preprint arXiv:2402.09642
(2024).
[245] Zhiyuan Peng, Xuyang Wu, Qifan Wang, and Yi Fang. 2025. Soft prompt tuning for augmenting dense retrieval with
large language models. Knowledge-Based Systems 309 (2025), 112758.
[246] Jeffrey Pennington, Richard Socher, and Christopher D Manning. 2014. Glove: Global vectors for word representation.
In Proceedings of EMNLP. 1532–1543.
[247] Matthew E. Peters, Mark Neumann, Mohit Iyyer, Matt Gardner, Christopher Clark, Kenton Lee, and Luke Zettlemoyer.
2018. Deep Contextualized Word Representations. In Proceedings of NAACL-HLT. 2227–2237.
[248] Alina Petukhova, Joao P Matos-Carvalho, and Nuno Fachada. 2024. Text clustering with LLM embeddings. arXiv
preprint arXiv:2403.15112 (2024).
[249] Long N. Phan, Hieu Tran, Daniel Le, Hieu Nguyen, James T. Anibal, Alec Peltekian, and Yanfang Ye. 2021. CoTexT:
Multi-task Learning with Code-Text Transformer. CoRR abs/2105.08645 (2021).
[250] Bryan A. Plummer, Liwei Wang, Chris M. Cervantes, Juan C. Caicedo, Julia Hockenmaier, and Svetlana Lazebnik.
2015. Flickr30k Entities: Collecting Region-to-Phrase Correspondences for Richer Image-to-Sentence Models. In
ICCV. IEEE Computer Society, 2641–2649.
[251] Jacob Portes, Alexander Trott, Sam Havens, Daniel King, Abhinav Venigalla, Moin Nadeem, Nikhil Sardana, Daya
Khudia, and Jonathan Frankle. 2024. MosaicBERT: A Bidirectional Encoder Optimized for Fast Pretraining. NeurIPS
36 (2024).

J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.

On The Role of Pretrained Language Models in General-Purpose Text Embeddings: A Survey
111:39

[252] Rafal Poswiata, Slawomir Dadas, and Michal Perelkiewicz. 2024. PL-MTEB: Polish Massive Text Embedding Benchmark.
CoRR abs/2405.10138 (2024). arXiv:2405.10138
[253] Ofir Press, Noah Smith, and Mike Lewis. 2022. Train Short, Test Long: Attention with Linear Biases Enables Input
Length Extrapolation. In ICLR.
[254] Ruchir Puri, David S Kung, Geert Janssen, Wei Zhang, Giacomo Domeniconi, Vladimir Zolotov, Julian Dolby, Jie Chen,
Mihir Choudhury, Lindsey Decker, et al. [n. d.]. CodeNet: A Large-Scale AI for Code Dataset for Learning a Diversity
of Coding Tasks. In Thirty-fifth Conference on Neural Information Processing Systems Datasets and Benchmarks Track
(Round 2).
[255] Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry, Amanda
Askell, Pamela Mishkin, Jack Clark, Gretchen Krueger, and Ilya Sutskever. 2021. Learning Transferable Visual Models
From Natural Language Supervision. In Proceedings of ICML, Vol. 139. 8748–8763.
[256] Alec Radford, Karthik Narasimhan, Tim Salimans, Ilya Sutskever, et al. 2018. Improving language understanding by
generative pre-training. (2018).
[257] Colin Raffel, Noam Shazeer, Adam Roberts, Katherine Lee, Sharan Narang, Michael Matena, Yanqi Zhou, Wei Li, and
Peter J Liu. 2020. Exploring the limits of transfer learning with a unified text-to-text transformer. J. Mach. Learn. Res.
21, 140 (2020), 1–67.
[258] Samyam Rajbhandari, Jeff Rasley, Olatunji Ruwase, and Yuxiong He. 2020. Zero: Memory optimizations toward
training trillion parameter models. In Proceedings of SC. IEEE, 1–16.
[259] Pranav Rajpurkar, Jian Zhang, Konstantin Lopyrev, and Percy Liang. 2016. SQuAD: 100, 000+ Questions for Machine
Comprehension of Text. In EMNLP. The Association for Computational Linguistics, 2383–2392.
[260] Abhinav Ramesh Kashyap, Thanh-Tung Nguyen, Viktor Schlegel, Stefan Winkler, See-Kiong Ng, and Soujanya Poria.
2024. A Comprehensive Survey of Sentence Representations: From the BERT Epoch to the CHATGPT Era and Beyond.
In Proceedings of EACL. St. Julian’s, Malta, 1738–1751.
[261] David Rau, Shuai Wang, Hervé Déjean, and Stéphane Clinchant. 2024. Context Embeddings for Efficient Answer
Generation in RAG. arXiv preprint arXiv:2407.09252 (2024).
[262] Nils Reimers. 2021. Reddit (Title, Body) Pairs.
[263] Nils Reimers and Iryna Gurevych. 2019. Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks. In
Proceedings of EMNLP/IJCNLP (1). 3980–3990.
[264] Baptiste Rozière, Jonas Gehring, Fabian Gloeckle, Sten Sootla, Itai Gat, Xiaoqing Ellen Tan, Yossi Adi, Jingyu Liu,
Tal Remez, Jérémy Rapin, Artyom Kozhevnikov, Ivan Evtimov, Joanna Bitton, Manish Bhatt, Cristian Canton-Ferrer,
Aaron Grattafiori, Wenhan Xiong, Alexandre Défossez, Jade Copet, Faisal Azhar, Hugo Touvron, Louis Martin, Nicolas
Usunier, Thomas Scialom, and Gabriel Synnaeve. 2023. Code Llama: Open Foundation Models for Code. CoRR
abs/2308.12950 (2023).
[265] Baptiste Roziere, Marie-Anne Lachaux, Lowik Chanussot, and Guillaume Lample. 2020. Unsupervised translation of
programming languages. Advances in neural information processing systems 33 (2020), 20601–20611.
[266] Baptiste Roziere, Jie Zhang, Francois Charton, Mark Harman, Gabriel Synnaeve, and Guillaume Lample. [n. d.].
Leveraging Automated Unit Tests for Unsupervised Code Translation. In International Conference on Learning
Representations.
[267] Jon Saad-Falcon, Daniel Y Fu, Simran Arora, Neel Guha, and Christopher Ré. 2024. Benchmarking and building
long-context retrieval models with loco and m2-bert. arXiv preprint arXiv:2402.07440 (2024).
[268] Chitwan Saharia, William Chan, Saurabh Saxena, Lala Li, Jay Whang, Emily L Denton, Kamyar Ghasemipour, Raphael
Gontijo Lopes, Burcu Karagol Ayan, Tim Salimans, et al. 2022. Photorealistic text-to-image diffusion models with
deep language understanding. NeurIPS 35 (2022), 36479–36494.
[269] Gerard Salton, Anita Wong, and Chung-Shu Yang. 1975. A Vector Space Model for Automatic Indexing. Commun.
ACM 18, 11 (1975), 613–620.
[270] Victor Sanh, Albert Webson, Colin Raffel, Stephen H. Bach, Lintang Sutawika, Zaid Alyafeai, Antoine Chaffin, Arnaud
Stiegler, Arun Raja, Manan Dey, M Saiful Bari, Canwen Xu, Urmish Thakker, Shanya Sharma Sharma, Eliza Szczechla,
Taewoon Kim, Gunjan Chhablani, Nihal V. Nayak, Debajyoti Datta, Jonathan Chang, Mike Tian-Jian Jiang, Han
Wang, Matteo Manica, Sheng Shen, Zheng Xin Yong, Harshit Pandey, Rachel Bawden, Thomas Wang, Trishala Neeraj,
Jos Rozen, Abheesht Sharma, Andrea Santilli, Thibault Févry, Jason Alan Fries, Ryan Teehan, Teven Le Scao, Stella
Biderman, Leo Gao, Thomas Wolf, and Alexander M. Rush. 2022. Multitask Prompted Training Enables Zero-Shot
Task Generalization. In Proceedings of ICLR.
[271] Elvis Saravia, Hsien-Chi Toby Liu, Yen-Hao Huang, Junlin Wu, and Yi-Shin Chen. 2018. CARER: Contextualized
Affect Representations for Emotion Recognition. In EMNLP. Association for Computational Linguistics, 3687–3697.
[272] Soma Sato, Hayato Tsukagoshi, Ryohei Sasano, and Koichi Takeda. 2024. Improving Sentence Embeddings with
Automatic Generation of Training Data Using Few-shot Examples. In ACL (Student Research Workshop). 519–530.

J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.

111:40
Zhang et al.

[273] Timo Schick and Hinrich Schütze. 2021. Generating Datasets with Pretrained Language Models. In Proceedings of
EMNLP (1). Association for Computational Linguistics, 6943–6951.
[274] Simon Schrodi, David T. Hoffmann, Max Argus, Volker Fischer, and Thomas Brox. 2024. Two Effects, One Trigger: On
the Modality Gap, Object Bias, and Information Imbalance in Contrastive Vision-Language Representation Learning.
CoRR abs/2404.07983 (2024).
[275] Holger Schwenk, Guillaume Wenzek, Sergey Edunov, Edouard Grave, Armand Joulin, and Angela Fan. 2021. CCMatrix:
Mining Billions of High-Quality Parallel Sentences on the Web. In Proceedings of ACL/IJCNLP (1). 6490–6500.
[276] Thomas Scialom, Paul-Alexis Dray, Sylvain Lamprier, Benjamin Piwowarski, and Jacopo Staiano. 2020. MLSUM: The
Multilingual Summarization Corpus. In Proceedings of EMNLP (1). 8051–8067.
[277] Yeon Seonwoo, Guoyin Wang, Changmin Seo, Sajal Choudhary, Jiwei Li, Xiang Li, Puyang Xu, Sunghyun Park,
and Alice Oh. 2023. Ranking-Enhanced Unsupervised Sentence Representation Learning. In Proceedings of ACL (1).
Association for Computational Linguistics, 15783–15798.
[278] Rulin Shao, Rui Qiao, Varsha Kishore, Niklas Muennighoff, Xi Victoria Lin, Daniela Rus, Bryan Kian Hsiang Low,
Sewon Min, Wen-tau Yih, Pang Wei Koh, and Luke Zettlemoyer. 2025. ReasonIR: Training Retrievers for Reasoning
Tasks. CoRR abs/2504.20595 (2025).
[279] Ensheng Shi, Yanlin Wang, Wenchao Gu, Lun Du, Hongyu Zhang, Shi Han, Dongmei Zhang, and Hongbin Sun. 2023.
CoCoSoDa: Effective Contrastive Learning for Code Search. In ICSE. 2198–2210.
[280] Weijia Shi, Sewon Min, Michihiro Yasunaga, Minjoon Seo, Richard James, Mike Lewis, Luke Zettlemoyer, and Wen-tau
Yih. 2024. REPLUG: Retrieval-Augmented Black-Box Language Models. In Proceedings of NAACL-HLT.
[281] Amanpreet Singh, Mike D’Arcy, Arman Cohan, Doug Downey, and Sergey Feldman. 2023. SciRepEval: A Multi-
Format Benchmark for Scientific Document Representations. In EMNLP. Association for Computational Linguistics,
5548–5566.
[282] Shivalika Singh, Freddie Vargus, Daniel Dsouza, Brje F. Karlsson, Abinaya Mahendiran, Wei-Yin Ko, Herumb Shandilya,
Jay Patel, Deividas Mataciunas, Laura OMahony, Mike Zhang, Ramith Hettiarachchi, Joseph Wilson, Marina Machado,
Luisa Souza Moura, Dominik Krzemiński, Hakimeh Fadaei, Irem Ergün, Ifeoma Okoh, Aisha Alaagib, Oshan
Mudannayake, Zaid Alyafeai, Vu Minh Chien, Sebastian Ruder, Surya Guthikonda, Emad A. Alghamdi, Sebastian
Gehrmann, Niklas Muennighoff, Max Bartolo, Julia Kreutzer, Ahmet stün, Marzieh Fadaee, and Sara Hooker. 2024.
Aya Dataset: An Open-Access Collection for Multilingual Instruction Tuning. arXiv:2402.06619 [cs.CL]
[283] Artem Snegirev, Maria Tikhonova, Anna Maksimova, Alena Fenogenova, and Aleksandr Abramov. 2025. The Russian-
focused embedders’ exploration: ruMTEB benchmark and Russian embedding model design. In Proceedings of NAACL
(Long Papers). 236–254.
[284] Aivin V Solatorio. 2024. Gistembed: Guided in-sample selection of training negatives for text embedding fine-tuning.
arXiv preprint arXiv:2402.16829 (2024).
[285] Jacob Mitchell Springer, Suhas Kotha, Daniel Fried, Graham Neubig, and Aditi Raghunathan. 2025. Repetition
Improves Language Model Embeddings. In Proceedings of ICLR.
[286] Inc. Stack Exchange. 2021. StackExchange (Title, Body) Pairs.
[287] Saba Sturua, Isabelle Mohr, Mohammad Kalim Akram, Michael Günther, Bo Wang, Markus Krimmel, Feng Wang,
Georgios Mastrapas, Andreas Koukounas, Nan Wang, et al. 2024. jina-embeddings-v3: Multilingual embeddings with
task lora. arXiv preprint arXiv:2409.10173 (2024).
[288] Hongjin Su, Weijia Shi, Jungo Kasai, Yizhong Wang, Yushi Hu, Mari Ostendorf, Wen-tau Yih, Noah A. Smith, Luke
Zettlemoyer, and Tao Yu. 2023. One Embedder, Any Task: Instruction-Finetuned Text Embeddings. In Findings of
ACL. Toronto, Canada, 1102–1121.
[289] Jianlin Su. 2022. CoSENT: a more effective sentence vector scheme than Sentence BERT.
[290] Jianlin Su, Murtadha Ahmed, Yu Lu, Shengfeng Pan, Wen Bo, and Yunfeng Liu. 2024. Roformer: Enhanced transformer
with rotary position embedding. Neurocomputing 568 (2024), 127063.
[291] Jianlin Su, Jiarun Cao, Weijie Liu, and Yangyiwen Ou. 2021. Whitening sentence representations for better semantics
and faster retrieval. arXiv preprint arXiv:2103.15316 (2021).
[292] Maosong Sun, Jingyang Li, Zhipeng Guo, Yu Zhao, Yabin Zheng, Xiance Si, and Zhiyuan Liu. 2016. THUCTC: An
Efficient Chinese Text Classifier. http://thuctc.thunlp.org/
[293] Shuo Sun and Kevin Duh. 2020. CLIRMatrix: A massively large collection of bilingual and multilingual datasets for
Cross-Lingual Information Retrieval. In Proceedings of EMNLP (1). 4160–4170.
[294] Tarun Suresh, Revanth Gangi Reddy, Yifei Xu, Zach Nussbaum, Andriy Mulyar, Brandon Duderstadt, and Heng Ji.
2025. CoRNStack: High-Quality Contrastive Data for Better Code Retrieval and Reranking. In ICLR.
[295] Jeffrey Svajlenko, Judith F Islam, Iman Keivanloo, Chanchal K Roy, and Mohammad Mamun Mia. 2014. Towards a big
data curated benchmark of inter-project code clones. In 2014 IEEE international conference on software maintenance
and evolution. IEEE, 476–480.

J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.

On The Role of Pretrained Language Models in General-Purpose Text Embeddings: A Survey
111:41

[296] Hongxuan Tang, Hongyu Li, Jing Liu, Yu Hong, Hua Wu, and Haifeng Wang. 2021. DuReader_robust: A Chinese
Dataset Towards Evaluating Robustness and Generalization of Machine Reading Comprehension in Real-World
Applications. In ACL/IJCNLP (2). Association for Computational Linguistics, 955–963.
[297] Shancheng Tang, Yunyue Bai, and Fuyu Ma. 2016. Chinese Semantic Text Similarity Trainning Dataset.
https:
//github.com/IAdmireu/ChineseSTS
[298] NLLB Team, Marta R. Costa-jussà, James Cross, Onur elebi, Maha Elbayad, Kenneth Heafield, Kevin Heffernan,
Elahe Kalbassi, Janice Lam, Daniel Licht, Jean Maillard, Anna Sun, Skyler Wang, Guillaume Wenzek, Al Youngblood,
Bapi Akula, Loic Barrault, Gabriel Mejia Gonzalez, Prangthip Hansanti, John Hoffman, Semarley Jarrett, Kaushik Ram
Sadagopan, Dirk Rowe, Shannon Spruit, Chau Tran, Pierre Andrews, Necip Fazil Ayan, Shruti Bhosale, Sergey Edunov,
Angela Fan, Cynthia Gao, Vedanuj Goswami, Francisco Guzmán, Philipp Koehn, Alexandre Mourachko, Christophe
Ropers, Safiyyah Saleem, Holger Schwenk, and Jeff Wang. 2022. No Language Left Behind: Scaling Human-Centered
Machine Translation. arXiv:2207.04672
[299] Nandan Thakur, Jianmo Ni, Gustavo Hernández Ábrego, John Wieting, Jimmy Lin, and Daniel Cer. 2024. Leveraging
LLMs for Synthesizing Training Data Across Many Languages in Multilingual Dense Retrieval. In Proceedings of
NAACL-HLT. 7699–7724.
[300] Nandan Thakur, Nils Reimers, Andreas Rücklé, Abhishek Srivastava, and Iryna Gurevych. 2021. BEIR: A Heterogeneous
Benchmark for Zero-shot Evaluation of Information Retrieval Models. In NeurIPS Datasets and Benchmarks.
[301] Raghuveer Thirukovalluru, Rui Meng, Ye Liu, Karthikeyan K, Mingyi Su, Ping Nie, Semih Yavuz, Yingbo Zhou, Wenhu
Chen, and Bhuwan Dhingra. 2025. Breaking the Batch Barrier (B3) of Contrastive Learning via Smart Batch Mining.
CoRR abs/2505.11293 (2025).
[302] Raghuveer Thirukovalluru, Xiaolan Wang, Jun Chen, Shuyang Li, Jie Lei, Rong Jin, and Bhuwan Dhingra. 2024.
SumCSE: Summary as a transformation for Contrastive Learning. In Findings of NAACL-HLT. 3577–3588.
[303] James Thorne, Andreas Vlachos, Christos Christodoulopoulos, and Arpit Mittal. 2018. FEVER: a Large-scale Dataset
for Fact Extraction and VERification. In Proceedings of NAACL-HLT. Association for Computational Linguistics,
809–819.
[304] Jörg Tiedemann. 2012. Parallel Data, Tools and Interfaces in OPUS. In Proceedings of LREC. 2214–2218.
[305] George Tsatsaronis, Georgios Balikas, Prodromos Malakasiotis, Ioannis Partalas, Matthias Zschunke, Michael R.
Alvers, Dirk Weissenborn, Anastasia Krithara, Sergios Petridis, Dimitris Polychronopoulos, Yannis Almirantis, John
Pavlopoulos, Nicolas Baskiotis, Patrick Gallinari, Thierry Artières, Axel-Cyrille Ngonga Ngomo, Norman Heino, Éric
Gaussier, Liliana Barrio-Alvers, Michael Schroeder, Ion Androutsopoulos, and Georgios Paliouras. 2015. An overview
of the BIOASQ large-scale biomedical semantic indexing and question answering competition. BMC Bioinform. 16
(2015), 138:1–138:28.
[306] Michael Tschannen, Alexey A. Gritsenko, Xiao Wang, Muhammad Ferjad Naeem, Ibrahim Alabdulmohsin, Nikhil
Parthasarathy, Talfan Evans, Lucas Beyer, Ye Xia, Basil Mustafa, Olivier J. Hénaff, Jeremiah Harmsen, Andreas Steiner,
and Xiaohua Zhai. 2025. SigLIP 2: Multilingual Vision-Language Encoders with Improved Semantic Understanding,
Localization, and Dense Features. CoRR abs/2502.14786 (2025).
[307] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz Kaiser, and Illia
Polosukhin. 2017. Attention is All you Need. In NIPS. 5998–6008.
[308] Lucas Ventura, Antoine Yang, Cordelia Schmid, and Gül Varol. 2024. CoVR: Learning Composed Video Retrieval from
Web Video Captions. In Proceedings of AAAI. AAAI Press, 5270–5279.
[309] David Wadden, Shanchuan Lin, Kyle Lo, Lucy Lu Wang, Madeleine van Zuylen, Arman Cohan, and Hannaneh
Hajishirzi. 2020. Fact or Fiction: Verifying Scientific Claims. In Proceedings of EMNLP (1). Association for Computational
Linguistics, 7534–7550.
[310] Ben Wang and Aran Komatsuzaki. 2021. GPT-J-6B: A 6 Billion Parameter Autoregressive Language Model. https:
//github.com/kingoflolz/mesh-transformer-jax.
[311] Feng Wang, Yuqing Li, and Han Xiao. 2025. jina-reranker-v3: Last but Not Late Interaction for Document Reranking.
CoRR abs/2509.25085 (2025).
[312] Huiming Wang, Liying Cheng, Zhaodonghui Li, De Wen Soh, and Lidong Bing. 2023. Semantic-Aware Contrastive
Sentence Representation Learning with Large Language Models. CoRR abs/2310.10962 (2023).
[313] Haifeng Wang, Jiwei Li, Hua Wu, Eduard Hovy, and Yu Sun. 2023. Pre-Trained Language Models and Their Applications.
Engineering 25 (2023), 51–65.
[314] Jiajia Wang, Jimmy Xiangji Huang, Xinhui Tu, Junmei Wang, Angela Jennifer Huang, Md Tahmid Rahman Laskar,
and Amran Bhuiyan. 2024. Utilizing BERT for Information Retrieval: Survey, Applications, Resources, and Challenges.
ACM Comput. Surv. 56, 7, Article 185 (apr 2024), 33 pages.
[315] Kexin Wang, Nils Reimers, and Iryna Gurevych. 2021. TSDAE: Using Transformer-based Sequential Denoising
Auto-Encoder for Unsupervised Sentence Embedding Learning. CoRR abs/2104.06979 (2021).

J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.

111:42
Zhang et al.

[316] Liang Wang, Nan Yang, Xiaolong Huang, Binxing Jiao, Linjun Yang, Daxin Jiang, Rangan Majumder, and Furu Wei.
2022. Text embeddings by weakly-supervised contrastive pre-training. arXiv preprint arXiv:2212.03533 (2022).
[317] Liang Wang, Nan Yang, Xiaolong Huang, Linjun Yang, Rangan Majumder, and Furu Wei. 2024. Improving Text
Embeddings with Large Language Models. In Proceedings of ACL. Bangkok, Thailand, 11897–11916.
[318] Liang Wang, Nan Yang, Xiaolong Huang, Linjun Yang, Rangan Majumder, and Furu Wei. 2024. Multilingual e5 text
embeddings: A technical report. arXiv preprint arXiv:2402.05672 (2024).
[319] Tianduo Wang and Wei Lu. 2022. Differentiable Data Augmentation for Contrastive Sentence Representation Learning.
In Proceedings of EMNLP. 7640–7653.
[320] Wei Wang, Liangzhu Ge, Jingqiao Zhang, and Cheng Yang. 2022. Improving Contrastive Learning of Sentence
Embeddings with Case-Augmented Positives and Retrieved Negatives. In SIGIR. ACM, 2159–2165.
[321] Xiaozhi Wang, Tianyu Gao, Zhaocheng Zhu, Zhengyan Zhang, Zhiyuan Liu, Juanzi Li, and Jian Tang. 2021. KEPLER: A
Unified Model for Knowledge Embedding and Pre-trained Language Representation. Trans. Assoc. Comput. Linguistics
9 (2021), 176–194.
[322] Xinghao Wang, Junliang He, Pengyu Wang, Yunhua Zhou, Tianxiang Sun, and Xipeng Qiu. 2024. Denosent: A
denoising objective for self-supervised sentence representation learning. In Proceedings of AAAI, Vol. 38. 19180–
19188.
[323] Xin Wang, Yasheng Wang, Fei Mi, Pingyi Zhou, Yao Wan, Xiao Liu, Li Li, Hao Wu, Jin Liu, and Xin Jiang. 2021.
Syncobert: Syntax-guided multi-modal contrastive pre-training for code representation. arXiv preprint arXiv:2108.04556
(2021).
[324] Xin Wang, Yasheng Wang, Yao Wan, Jiawei Wang, Pingyi Zhou, Li Li, Hao Wu, and Jin Liu. 2022. Code-mvp: Learning
to represent source code from multiple views with contrastive pre-training. arXiv preprint arXiv:2205.02029 (2022).
[325] Yi Wang, Yinan He, Yizhuo Li, Kunchang Li, Jiashuo Yu, Xin Ma, Xinhao Li, Guo Chen, Xinyuan Chen, Yaohui Wang,
Ping Luo, Ziwei Liu, Yali Wang, Limin Wang, and Yu Qiao. 2024. InternVid: A Large-scale Video-Text Dataset for
Multimodal Understanding and Generation. In ICLR. OpenReview.net.
[326] Yue Wang, Hung Le, Akhilesh Gotmare, Nghi D. Q. Bui, Junnan Li, and Steven C. H. Hoi. 2023. CodeT5+: Open Code
Large Language Models for Code Understanding and Generation. In Proceedings of EMNLP. 1069–1088.
[327] Yue Wang, Weishi Wang, Shafiq R. Joty, and Steven C. H. Hoi. 2021. CodeT5: Identifier-aware Unified Pre-trained
Encoder-Decoder Models for Code Understanding and Generation. In Proceedings of EMNLP (1). 8696–8708.
[328] Benjamin Warner, Antoine Chaffin, Benjamin Clavié, Orion Weller, Oskar Hallström, Said Taghadouini, Alexis
Gallagher, Raja Biswas, Faisal Ladhak, Tom Aarsen, et al. 2024. Smarter, better, faster, longer: A modern bidirectional
encoder for fast, memory efficient, and long context finetuning and inference. arXiv preprint arXiv:2412.13663 (2024).
[329] Silvan Wehrli, Bert Arnrich, and Christopher Irrgang. 2023. German Text Embedding Clustering Benchmark. In
Proceedings of KONVENS. Ingolstadt, Germany, 187–201.
[330] Jason Wei, Maarten Bosma, Vincent Y. Zhao, Kelvin Guu, Adams Wei Yu, Brian Lester, Nan Du, Andrew M. Dai, and
Quoc V. Le. 2022. Finetuned Language Models are Zero-Shot Learners. In Proceedings of ICLR. OpenReview.net.
[331] Orion Weller, Benjamin Chang, Sean MacAvaney, Kyle Lo, Arman Cohan, Benjamin Van Durme, Dawn Lawrie, and
Luca Soldaini. 2024. FollowIR: Evaluating and Teaching Information Retrieval Models to Follow Instructions. arXiv
preprint arXiv:2403.15246 (2024).
[332] Orion Weller, Benjamin Van Durme, Dawn J. Lawrie, Ashwin Paranjape, Yuhao Zhang, and Jack Hessel. 2025.
Promptriever: Instruction-Trained Retrievers Can Be Prompted Like Language Models. In Proceedings of ICLR.
[333] Guillaume Wenzek, Marie-Anne Lachaux, Alexis Conneau, Vishrav Chaudhary, Francisco Guzmán, Armand Joulin,
and Edouard Grave. 2020. CCNet: Extracting High Quality Monolingual Datasets from Web Crawl Data. In Proceedings
of LREC. 4003–4012.
[334] Adina Williams, Nikita Nangia, and Samuel R. Bowman. 2018. A Broad-Coverage Challenge Corpus for Sentence
Understanding through Inference. In NAACL-HLT. Association for Computational Linguistics, 1112–1122.
[335] Bohong Wu and Hai Zhao. 2022. Sentence Representation Learning with Generative Objective rather than Contrastive
Objective. In Proceedings of EMNLP. Association for Computational Linguistics, 3356–3368.
[336] Hui Wu, Yupeng Gao, Xiaoxiao Guo, Ziad Al-Halah, Steven Rennie, Kristen Grauman, and Rogério Feris. 2021. Fashion
IQ: A New Dataset Towards Retrieving Images by Natural Language Feedback. In CVPR. Computer Vision Foundation
/ IEEE, 11307–11317.
[337] Qiyu Wu, Chongyang Tao, Tao Shen, Can Xu, Xiubo Geng, and Daxin Jiang. 2022. PCL: Peer-Contrastive Learning
with Diverse Augmentations for Unsupervised Sentence Embeddings. In Proceedings of EMNLP. Association for
Computational Linguistics, 12052–12066.
[338] Xing Wu, Chaochen Gao, Zijia Lin, Jizhong Han, Zhongyuan Wang, and Songlin Hu. 2022. InfoCSE: Information-
aggregated Contrastive Learning of Sentence Embeddings. In Findings of EMNLP. Association for Computational
Linguistics, 3060–3070.

J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.

On The Role of Pretrained Language Models in General-Purpose Text Embeddings: A Survey
111:43

[339] Xing Wu, Chaochen Gao, Yipeng Su, Jizhong Han, Zhongyuan Wang, and Songlin Hu. 2022. Smoothed Contrastive
Learning for Unsupervised Sentence Embedding. In Proceedings of COLING. International Committee on Computa-
tional Linguistics, 4902–4906.
[340] Xing Wu, Chaochen Gao, Liangjun Zang, Jizhong Han, Zhongyuan Wang, and Songlin Hu. 2022. ESimCSE: Enhanced
Sample Building Method for Contrastive Learning of Unsupervised Sentence Embedding. In Proceedings of COLING.
International Committee on Computational Linguistics, 3898–3907.
[341] Zixiang Xian, Rubing Huang, Dave Towey, Chunrong Fang, and Zhenyu Chen. 2024. TransformCode: A Contrastive
Learning Framework for Code Embedding via Subtree Transformation. IEEE Trans. Software Eng. 50, 6 (2024),
1600–1619.
[342] Chaojun Xiao, Haoxi Zhong, Zhipeng Guo, Cunchao Tu, Zhiyuan Liu, Maosong Sun, Tianyang Zhang, Xianpei Han,
Zhen Hu, Heng Wang, and Jianfeng Xu. 2019. CAIL2019-SCM: A Dataset of Similar Case Matching in Legal Domain.
CoRR abs/1911.08962 (2019).
[343] Shitao Xiao, Zheng Liu, Yingxia Shao, and Zhao Cao. 2022. RetroMAE: Pre-Training Retrieval-oriented Language
Models Via Masked Auto-Encoder. In Proceedings of EMNLP. Abu Dhabi, United Arab Emirates, 538–548.
[344] Shitao Xiao, Zheng Liu, Peitian Zhang, Niklas Muennighoff, Defu Lian, and Jian-Yun Nie. 2024. C-Pack: Packed
Resources For General Chinese Embeddings. In Proceedings of SIGIR (Washington DC, USA) (SIGIR ’24). New York,
NY, USA, 641649.
[345] Xiaohui Xie, Qian Dong, Bingning Wang, Feiyang Lv, Ting Yao, Weinan Gan, Zhijing Wu, Xiangsheng Li, Haitao Li,
Yiqun Liu, and Jin Ma. 2023. T2Ranking: A Large-scale Chinese Benchmark for Passage Ranking. In Proceedings of
SIGIR. ACM, 2681–2690.
[346] Chao Xing, Dong Wang, Chao Liu, and Yiye Lin. 2015. Normalized Word Embedding and Orthogonal Transform for
Bilingual Word Translation. In Proceedings of the 2015 Conference of the North American Chapter of the Association
for Computational Linguistics: Human Language Technologies, Rada Mihalcea, Joyce Chai, and Anoop Sarkar (Eds.).
Association for Computational Linguistics, Denver, Colorado, 1006–1011.
[347] Bo Xu, Yifei Wu, Shouang Wei, Ming Du, and Hongya Wang. 2024. Adaptive Reinforcement Tuning Language Models
as Hard Data Generators for Sentence Representation. In Proceedings of LREC/COLING. 358–371.
[348] Jun Xu, Tao Mei, Ting Yao, and Yong Rui. 2016. MSR-VTT: A Large Video Description Dataset for Bridging Video and
Language. In Proceedings of CVPR. IEEE Computer Society, 5288–5296.
[349] Yifan Xu, Xinhao Li, Yichun Yang, Rui Huang, and Limin Wang. 2025. Fine-grained Video-Text Retrieval: A New
Benchmark and Method. CoRR abs/2501.00513 (2025).
[350] Linting Xue, Noah Constant, Adam Roberts, Mihir Kale, Rami Al-Rfou, Aditya Siddhant, Aditya Barua, and Colin
Raffel. 2021. mT5: A Massively Multilingual Pre-trained Text-to-Text Transformer. In Proceedings of NAACL-HLT.
483–498.
[351] Ruiran Yan, Zheng Liu, and Defu Lian. 2025. O1 Embedder: Let Retrievers Think Before Action. CoRR abs/2502.07555
(2025).
[352] Weixiang Yan, Yuchen Tian, Yunzhe Li, Qian Chen, and Wen Wang. [n. d.]. CodeTransOcean: A Comprehensive
Multilingual Benchmark for Code Translation. In The 2023 Conference on Empirical Methods in Natural Language
Processing.
[353] Dongjie Yang, Ruifeng Yuan, Yuantao Fan, Yifei Yang, Zili Wang, Shusen Wang, and Hai Zhao. 2023. RefGPT: Dialogue
Generation of GPT, by GPT, and for GPT. In EMNLP (Findings). Association for Computational Linguistics, 2511–2535.
[354] Hongkang Yang, Zehao Lin, Wenjin Wang, Hao Wu, Zhiyu Li, Bo Tang, Wenqiang Wei, Jinbo Wang, Zeyun Tang,
Shichao Song, Chenyang Xi, Yu Yu, Kai Chen, Feiyu Xiong, Linpeng Tang, and Weinan E. 2024. Memory3: Language
Modeling with Explicit Memory. CoRR abs/2407.01178 (2024).
[355] Wenkai Yang, Lei Li, Zhiyuan Zhang, Xuancheng Ren, Xu Sun, and Bin He. 2021. Be Careful about Poisoned Word
Embeddings: Exploring the Vulnerability of the Embedding Layers in NLP Models. In Proceedings of NAACL-HLT.
2048–2058.
[356] Yinfei Yang, Yuan Zhang, Chris Tar, and Jason Baldridge. 2019. PAWS-X: A Cross-lingual Adversarial Dataset for
Paraphrase Identification. In EMNLP/IJCNLP (1). Association for Computational Linguistics, 3685–3690.
[357] Zhilin Yang, Peng Qi, Saizheng Zhang, Yoshua Bengio, William W. Cohen, Ruslan Salakhutdinov, and Christopher D.
Manning. 2018. HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering. In Proceedings of
EMNLP. Association for Computational Linguistics, 2369–2380.
[358] Ziyi Yang, Yinfei Yang, Daniel Cer, Jax Law, and Eric Darve. 2021. Universal Sentence Representation Learning
with Conditional Masked Language Model. In Proceedings of EMNLP (1). Association for Computational Linguistics,
6216–6228.
[359] Chihiro Yano, Akihiko Fukuchi, Shoko Fukasawa, Hideyuki Tachibana, and Yotaro Watanabe. 2024. Multilingual
Sentence-T5: Scalable Sentence Encoders for Multilingual Applications. In Proceedings of LREC/COLING. ELRA and
ICCL, 11849–11858.

J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.

111:44
Zhang et al.

[360] Pengcheng Yin, Graham Neubig, Wen-tau Yih, and Sebastian Riedel. 2020. TaBERT: Pretraining for Joint Understanding
of Textual and Tabular Data. In ACL. Association for Computational Linguistics, 8413–8426.
[361] Jiahui Yu, Zirui Wang, Vijay Vasudevan, Legg Yeung, Mojtaba Seyedhosseini, and Yonghui Wu. 2022. CoCa: Contrastive
Captioners are Image-Text Foundation Models. Trans. Mach. Learn. Res. 2022 (2022).
[362] Puxuan Yu, Luke Merrick, Gaurav Nuti, and Daniel Campos. 2024. Arctic-embed 2.0: Multilingual retrieval without
compromise. arXiv preprint arXiv:2412.04506 (2024).
[363] Shi Yu, Chaoyue Tang, Bokai Xu, Junbo Cui, Junhao Ran, Yukun Yan, Zhenghao Liu, Shuo Wang, Xu Han, Zhiyuan
Liu, and Maosong Sun. 2025. VisRAG: Vision-based Retrieval-augmented Generation on Multi-modality Documents.
In ICLR. OpenReview.net.
[364] Liping Yuan, Jiawei Wang, Haomiao Sun, Yuchen Zhang, and Yuan Lin. 2025. Tarsier2: Advancing Large Vision-
Language Models from Detailed Video Description to Comprehensive Video Understanding. CoRR abs/2501.07888
(2025).
[365] Mateo Espinosa Zarlenga, Pietro Barbiero, Gabriele Ciravegna, Giuseppe Marra, Francesco Giannini, Michelangelo
Diligenti, Zohreh Shams, Frédéric Precioso, Stefano Melacci, Adrian Weller, Pietro Lió, and Mateja Jamnik. 2022.
Concept Embedding Models: Beyond the Accuracy-Explainability Trade-Off. In NeurIPS.
[366] Xiaohua Zhai, Basil Mustafa, Alexander Kolesnikov, and Lucas Beyer. 2023. Sigmoid Loss for Language Image
Pre-Training. In ICCV. 11941–11952.
[367] Bowen Zhang, Kehua Chang, and Chunping Li. 2024. Simple techniques for enhancing sentence embeddings in
generative language models. In Proceedings of ICIC. Springer, 52–64.
[368] Caojin Zhang, Qiang Zhang, Ke Li, Sai Vidyaranya Nuthalapati, Benyu Zhang, Jason Liu, Serena Li, Lizhu Zhang, and
Xiangjun Fan. 2025. GEM: Empowering LLM for both Embedding Generation and Language Understanding. arXiv
preprint arXiv:2506.04344 (2025).
[369] Dejiao Zhang, Wasi Uddin Ahmad, Ming Tan, Hantian Ding, Ramesh Nallapati, Dan Roth, Xiaofei Ma, and Bing
Xiang. 2024. Code Representation Learning at Scale. In ICLR.
[370] Dejiao Zhang, Wei Xiao, Henghui Zhu, Xiaofei Ma, and Andrew Arnold. 2022. Virtual Augmentation Supported
Contrastive Learning of Sentence Representations. In Findings of the ACL. 864–876.
[371] Junlei Zhang, Zhenzhong Lan, and Junxian He. 2023. Contrastive Learning of Sentence Embeddings from Scratch. In
Proceedings of EMNLP. 3916–3932.
[372] Jing Zhang, Xiaokang Zhang, Jifan Yu, Jian Tang, Jie Tang, Cuiping Li, and Hong Chen. 2022. Subgraph Retrieval
Enhanced Model for Multi-hop Knowledge Base Question Answering. In ACL (1). Association for Computational
Linguistics, 5773–5784.
[373] Ruisi Zhang, Seira Hidano, and Farinaz Koushanfar. 2022. Text Revealer: Private Text Reconstruction via Model
Inversion Attacks against Transformers. CoRR abs/2209.10505 (2022).
[374] Xin Zhang, Zehan Li, Yanzhao Zhang, Dingkun Long, Pengjun Xie, Meishan Zhang, and Min Zhang. 2023. Language
Models are Universal Embedders. arXiv preprint arXiv:2310.08232 (2023).
[375] Xinyu Zhang, Xueguang Ma, Peng Shi, and Jimmy Lin. 2021. Mr. TyDi: A Multi-lingual Benchmark for Dense Retrieval.
CoRR abs/2108.08787 (2021).
[376] Xinyu Zhang, Kelechi Ogueji, Xueguang Ma, and Jimmy Lin. 2023. Toward best practices for training multilingual
dense retrieval models. ACM Transactions on Information Systems 42, 2 (2023), 1–33.
[377] Xinyu Zhang, Nandan Thakur, Odunayo Ogundepo, Ehsan Kamalloo, David Alfonso-Hermelo, Xiaoguang Li, Qun
Liu, Mehdi Rezagholizadeh, and Jimmy Lin. 2023. MIRACL: A Multilingual Retrieval Dataset Covering 18 Diverse
Languages. Trans. Assoc. Comput. Linguistics 11 (2023), 1114–1131.
[378] Xin Zhang, Yanzhao Zhang, Dingkun Long, Wen Xie, Ziqi Dai, Jialong Tang, Huan Lin, Baosong Yang, Pengjun Xie,
Fei Huang, Meishan Zhang, Wenjie Li, and Min Zhang. 2024. mGTE: Generalized Long-Context Text Representation
and Reranking Models for Multilingual Text Retrieval. In Proceedings of EMNLP (Industry Track). 1393–1412.
[379] Xin Zhang, Yanzhao Zhang, Wen Xie, Mingxin Li, Ziqi Dai, Dingkun Long, Pengjun Xie, Meishan Zhang, Wenjie Li,
and Min Zhang. 2024. GME: Improving Universal Multimodal Retrieval by Multimodal LLMs. CoRR abs/2412.16855
(2024).
[380] Yan Zhang, Ruidan He, Zuozhu Liu, Kwan Hui Lim, and Lidong Bing. 2020. An Unsupervised Sentence Embedding
Method by Mutual Information Maximization. In Proceedings of EMNLP (1). Association for Computational Linguistics,
1601–1610.
[381] Yanzhao Zhang, Mingxin Li, Dingkun Long, Xin Zhang, Huan Lin, Baosong Yang, Pengjun Xie, An Yang, Dayiheng
Liu, Junyang Lin, Fei Huang, and Jingren Zhou. 2025. Qwen3 Embedding: Advancing Text Embedding and Reranking
Through Foundation Models. arXiv preprint arXiv:2506.05176 (2025).
[382] Yanzhao Zhang, Richong Zhang, Samuel Mensah, Xudong Liu, and Yongyi Mao. 2022. Unsupervised sentence
representation via contrastive learning with mixing negatives. In Proceedings of AAAI, Vol. 36. 11730–11738.

J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.

On The Role of Pretrained Language Models in General-Purpose Text Embeddings: A Survey
111:45

[383] Yuhao Zhang, Hongji Zhu, Yongliang Wang, Nan Xu, Xiaobo Li, and Binqiang Zhao. 2022. A Contrastive Framework
for Learning Sentence Representations from Pairwise and Triple-wise Perspective in Angular Space. In Proceedings of
ACL (1). 4892–4903.
[384] Heri Zhao, Jeffrey Hui, Joshua Howland, Nam Nguyen, Siqi Zuo, Andrea Hu, Christopher A. Choquette-Choo, Jingyue
Shen, Joe Kelley, Kshitij Bansal, Luke Vilnis, Mateo Wirth, Paul Michel, Peter Choy, Pratik Joshi, Ravin Kumar, Sarmad
Hashmi, Shubham Agrawal, Zhitao Gong, Jane Fine, Tris Warkentin, Ale Jakse Hartman, Bin Ni, Kathy Korevec, Kelly
Schaefer, and Scott Huffman. 2024. CodeGemma: Open Code Models Based on Gemma. CoRR abs/2406.11409 (2024).
[385] Wayne Xin Zhao, Jing Liu, Ruiyang Ren, and Ji-Rong Wen. 2024. Dense Text Retrieval Based on Pretrained Language
Models: A Survey. ACM Trans. Inf. Syst. 42, 4, Article 89 (feb 2024), 60 pages.
[386] Xinping Zhao, Xinshuo Hu, Zifei Shan, Shouzheng Huang, Yao Zhou, Zetian Sun, Zhenyu Liu, Dongfang Li, Xinyuan
Wei, Qian Chen, Youcheng Pan, Yang Xiang, Meishan Zhang, Haofen Wang, Jun Yu, Baotian Hu, and Min Zhang.
2025. KaLM-Embedding-V2: Superior Training Techniques and Data Inspire A Versatile Embedding Model. CoRR
abs/2506.20923 (2025).
[387] Xinping Zhao, Yan Zhong, Zetian Sun, Xinshuo Hu, Zhenyu Liu, Dongfang Li, Baotian Hu, and Min Zhang. 2025.
FunnelRAG: A Coarse-to-Fine Progressive Retrieval Paradigm for RAG. In Findings of NAACL. 3029–3046.
[388] Zhen Zhao, Yuqiu Liu, Gang Zhang, Liang Tang, and Xiaolin Hu. 2022. The Winning Solution to the iFLYTEK
Challenge 2021 Cultivated Land Extraction from High-Resolution Remote Sensing Image. CoRR abs/2202.10974
(2022).
[389] Tianyu Zheng, Ge Zhang, Tianhao Shen, Xueling Liu, Bill Yuchen Lin, Jie Fu, Wenhu Chen, and Xiang Yue. 2024.
OpenCodeInterpreter: Integrating Code Generation with Execution and Refinement. In ACL (Findings). 12834–12859.
[390] Wanjun Zhong, Lianghong Guo, Qiqi Gao, He Ye, and Yanlin Wang. 2024. Memorybank: Enhancing large language
models with long-term memory. In Proceedings of AAAI, Vol. 38. 19724–19731.
[391] Chunting Zhou, Pengfei Liu, Puxin Xu, Srinivasan Iyer, Jiao Sun, Yuning Mao, Xuezhe Ma, Avia Efrat, Ping Yu, Lili Yu,
Susan Zhang, Gargi Ghosh, Mike Lewis, Luke Zettlemoyer, and Omer Levy. 2023. LIMA: Less Is More for Alignment.
In NeurIPS.
[392] Junjie Zhou, Zheng Liu, Ze Liu, Shitao Xiao, Yueze Wang, Bo Zhao, Chen Jason Zhang, Defu Lian, and Yongping
Xiong. 2024. MegaPairs: Massive Data Synthesis For Universal Multimodal Retrieval. CoRR abs/2412.14475 (2024).
[393] Kun Zhou, Beichen Zhang, Wayne Xin Zhao, and Ji-Rong Wen. 2022. Debiased Contrastive Learning of Unsupervised
Sentence Representations. In Proceedings of ACL. 6120–6130.
[394] Dawei Zhu, Liang Wang, Nan Yang, Yifan Song, Wenhao Wu, Furu Wei, and Sujian Li. 2024. LongEmbed: Extending
Embedding Models for Long Context Retrieval. In Proceedings of EMNLP. 802–816.
[395] Fengbin Zhu, Wenqiang Lei, Fuli Feng, Chao Wang, Haozhou Zhang, and Tat-Seng Chua. 2022. Towards Complex
Document Understanding By Discrete Reasoning. In ACM Multimedia. ACM, 4857–4866.
[396] Ming Zhu, Aneesh Jain, Karthik Suresh, Roshan Ravindran, Sindhu Tipirneni, and Chandan K Reddy. 2022. Xlcost: A
benchmark dataset for cross-lingual code intelligence. arXiv preprint arXiv:2206.08474 (2022).
[397] Ming Zhu, Karthik Suresh, and Chandan K Reddy. 2022. Multilingual code snippets training for program translation.
In Proceedings of the AAAI conference on artificial intelligence, Vol. 36. 11783–11790.
[398] Wei Zhu. 2023. ChatMed-Dataset: An GPT generated medical query-response datasets for medcial large language
models. https://github.com/michael-wzhu/ChatMed.
[399] Yuke Zhu, Oliver Groth, Michael S. Bernstein, and Li Fei-Fei. 2016. Visual7W: Grounded Question Answering in
Images. In Proceedings of CVPR. IEEE Computer Society, 4995–5004.
[400] Shengyao Zhuang, Xueguang Ma, Bevan Koopman, Jimmy Lin, and Guido Zuccon. 2024. PromptReps: Prompting Large
Language Models to Generate Dense and Sparse Representations for Zero-Shot Document Retrieval. In Proceedings of
EMNLP. 4375–4391.

Received 20 February 2007; revised 12 March 2009; accepted 5 June 2009

J. ACM, Vol. 37, No. 4, Article 111. Publication date: August 2018.