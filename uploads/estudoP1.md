RAG - Retrieval-Augmented Generation

-​
Geração por recuperação aumentada; Fornecer a LLM informações (arquivos, seja: 
texto, vídeo, áudio, etc) que antes ele não tinha. 
-​
 
 
Janela de contexto (limite de arquivo por tokens):

-​
Criação de chunks: pega um documento e o transforma em vários documentos 
menores (k-chunks).

-​
 
-​
Como saber qual k-chunk representa o contexto esperado? Este é o objetivo do 
RAG. 
-​
Primeiro buscamos qual contexto possui a semântica mais próxima do esperado, por 
vector-embedding. 
-​
Como armazenamos essas chunks? Em Vector Database, para guardar os vetores 
(nas representações semânticas numéricas) 
 
Vector-embedding:

-​
criação de um vetor entre as k-chunks para mapear qual é a frase mais próxima 
semanticamente do esperado, retornando os vetores mais próximos. 
-​
Como representar essas frases? O vector-embedding transforma uma 
frase/documento em embeddings (numérica) :

O que é? 
 
Knowledge cut-off: quando a LLM não sabe responder com a base de dados que ela tem. 
A insistência para exigir respostas sobre, ele irá alucinar.