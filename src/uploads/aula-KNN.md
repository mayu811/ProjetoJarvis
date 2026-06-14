k-Vizinhos mais Próximos

2

k-Vizinhos Mais Próximos

Aprendizado baseado em instâncias 
simplesmente armazena os exemplos de 
treinamento.
Quando um novo exemplo (caso) precisa 
ser classificado, esse exemplo é 
comparado com os exemplos 
armazenados.
A classificação é decidida a partir da 
similaridade entre o exemplo a ser 
classificado e os exemplos armazenados.

3

k-Vizinhos Mais Próximos

Aprendizado baseados em 
instâncias é chamado também de 
aprendizado “lazy”.
Isso se deve ao fato do 
processamento ser atrasado até o 
momento de classificação de um 
novo exemplo.

4

k-Vizinhos Mais Próximos

Dois métodos bastante conhecidos 
de aprendizado baseado em 
instâncias são:

k-vizinhos mais próximos;

Regressão com pesos locais.
A idéia do método k-vizinhos mais 
próximos é bastante simples...

5

K-Vizinhos mais Próximos

Inicialmente, os 
exemplos de 
treinamento são 
armazenados.

10

1
2
3
4
5
6
7
8
9 10

1
2
3
4
5
6
7
8
9

6

K-Vizinhos mais Próximos

Inicialmente, os 
exemplos de 
treinamento são 
armazenados.
Quando uma novo 
exemplo precisa 
ser classificado...

10

1
2
3
4
5
6
7
8
9 10

1
2
3
4
5
6
7
8
9

7

K-Vizinhos mais Próximos

Inicialmente, os 
exemplos de 
treinamento são 
armazenados.
Quando uma novo 
exemplo precisa 
ser classificado, é 
verificada a sua 
similaridade.

10

1
2
3
4
5
6
7
8
9 10

1
2
3
4
5
6
7
8
9

8

K-Vizinhos mais Próximos

Por fim, o novo 
exemplo é 
classificado 
segundo a sua 
proximidade com 
os exemplos de 
treinamento.

10

1
2
3
4
5
6
7
8
9 10

1
2
3
4
5
6
7
8
9

9

K-Vizinhos mais Próximos: 
Parâmetro k

O parâmetro k do k-vizinhos mais 
próximos é o número de vizinhos a 
serem considerados na classificação.
O parâmetro k é geralmente um inteiro 
pequeno e ímpar (1,3,5,7,9) para evitar 
empates (número par de classes).
Portanto, o 3-vizinhos mais próximos 
utiliza na classificação os 3 exemplos 
mais próximos do novo exemplo.

10

K-Vizinhos mais Próximos: 
Parâmetro k

Quando k = 1 (1-vizinho mais 
próximo) apenas o exemplo mais 
próximo ao exemplo a ser 
classificado é considerado.
O uso de k = 1 levar à 
classificações incorretas caso 
existam exemplos com ruído no 
conjunto de treinamento.

11

K-Vizinhos mais Próximos: 
Distância

K-vizinhos mais próximos assume 
que todos os exemplos 
correspondem a pontos no espaço 
n-dimensional n.
Os vizinhos mais próximos de um 
exemplos são definidos por uma 
medida de distância, tipicamente a 
distância euclidiana.

12

K-Vizinhos mais Próximos: 
Distância

13

K-Vizinhos mais Próximos: 
Distância

A distância euclidiana entre dois 
exemplos Ei e Ej é definida por

O k-vizinhos mais próximos pode 
ser utilizado tanto com um atributo 
classe (Y) contínuo quando 
discreto.

d( Ei,E j)=√∑

r=1

M

( xir−x jr)2

14

K-Vizinhos mais Próximos: 
Classificação

Para o caso na qual Y é discreto 
(problema de classificação), então 
deve-se encontrar os k exemplos 
mais próximos do exemplo a ser 
classificado.
Dentre os k exemplos, verifica-se a 
classe mais freqüente. Essa classe 
é atribuída ao novo exemplo.

15

K-Vizinhos mais Próximos: 
Classificação

Algoritmo de treinamento:

Armazenar todos os exemplos de

treinamento em um conjunto CT.
Algoritmo de classificação:

Dado um novo exemplo Enovo;

Sejam E’1,...E’k os k exemplos em CT

mais próximos à Enovo.

Retornar a classe que ocorre com

maior freqüência nos exemplo 
E’1,...E’k.

16

K-Vizinhos mais Próximos: 
Regressão

O k-vizinhos mais próximos pode ser 
adaptado para aproximar um atributo Y 
com valores contínuos.
Para isso, basta retornar a média dos 
valores do variável Y para os k-vizinhos 
mais próximos.
Por exemplo, pense em uma aplicação que 
precisa fornecer o salário de um 
funcionário dada a sua titulação, 
experiência, cargo, etc.

17

K-Vizinhos mais Próximos: 
Exemplo 1

Calcule a distância entre o exemplo Novo e 
os demais:

Nr.Ex.
At.1
At.2
At.3
Classe

1
5
1
90
+

2
2
3
105
-

3
1
4
120
+

Novo
3
3
100
?

18

K-Vizinhos mais Próximos: 
Normalização

Segundo a distância euclidiana, a 
distância entre os exemplos 1 e 
Novo é:

Para resultado final, 10.39, todos 
os atributos contribuíram 
igualmente?

d(1,novo)=√(5−3)2+(1−3)2+(90−100)2

=√22+(−2)2+(−10)2=√4+4+100≃10.39

19

K-Vizinhos mais Próximos: 
Normalização

Alguns atributos assumem uma 
faixa de valores mais ampla do 
que outro.
Para evitar que esses atributos 
tenham um influência maior, deve 
ser realizada uma normalização.
A normalização faz com que todos 
os atributos fiquem na mesma 
faixa de valores.

20

K-Vizinhos mais Próximos: 
Normalização

Existem diversas formas de normalização, 
uma das mais utilizadas é a normalização 
linear para o intervalo [0,1]:

Na qual:

vn é o valor normalizado;

vi é o valor não normalizado;

min e max são os valores mínimo e máximo do

atributo.

v n=

vi−min

max−min

21

K-Vizinhos mais Próximos: 
Exemplo 2

Normalize os atributos da tabela do 
exemplo 1 segundo a normalização linear:

Nr.Ex.
At.1
At.2
At.3
Classe

1
5
1
90
+

2
2
3
105
-

3
1
4
120
+

Novo
3
3
100
?

22

K-Vizinhos mais Próximos: 
Exemplo 3

Calcule a distância entre o exemplo Novo e 
o exemplo 1, dada a tabela normalizada:

Nr.Ex.
At.1
At.2
At.3
Classe

1
1
0
0
+

2
0.25
0.66
0.5
-

3
0
1
1
+

Novo
0.5
0.66
0.33
?

23

K-Vizinhos mais Próximos: 
Atributos Discretos

Um segundo problema com a distância 
euclidiana é o cálculo com atributos 
discretos.

Nr.Ex.
At.1
At.2
At.3
Classe

1
azul
novo
ford
+

2
verde
novo
gm
-

3
verde
antigo
volks
+

Novo
azul
antigo
gm
?

24

K-Vizinhos mais Próximos: 
Atributos Discretos

Uma forma simples de solucionar 
esse problema é utilizar a medida 
overlap. Nessa medida, a distância 
é zero se os valores são iguais ou 1 
se são diferentes.
Uma forma mais sofisticada é a 
Value Difference Metric (VDM) 
(Stanfil, 1986).

25

Value Difference Metric 
(VDM)

A idéia é que valores simbólicos são 
similares se eles possuem correlações 
similares com a classe.
Por exemplo, para um atributo “cor” 
que assume os valores “vermelho”, 
“verde” e “azul”, e para uma aplicação 
de identificar se um objeto é maça ou 
não, os valores “vermelho” e “verde” 
serão considerados mais próximos.

26

Value Difference Metric 
(VDM)

Na qual:

Nxir: número de exemplos com valor xir

Nxir,Cl: número exemplos com valor xir

e pertencentes a classe Cl

Ncl: número de classes

c: uma constante (tipicamente 1 ou 2)

27

Value Difference Metric 
(VDM)

VDM é uma métrica pois possui as 
propriedades de não negatividade, 
simetria e desigualdade triangular.
(Wilson & Martinez, 2000) fizeram um 
amplo estudo sobre como compor 
medidas de distâncias heterogêneas 
como a distância Euclidiana e VDM e 
Overlap.

28

K-Vizinhos mais Próximos: 
Pesos

Uma variação popular algoritmo k-
vizinhos mais próximos é utilizar 
um peso para cada vizinho 
proporcional à sua distância.

29

K-Vizinhos mais Próximos: 
Pesos

Uma sugestão é ajustar o peso do 
voto de cada vizinho pela equação:

Dessa forma, quanto mais distante 
estiver o vizinho mais próximo (Ei) 
do exemplo a ser classificado Enovo, 
menor será o seu peso.

wi=
1

d(Enovo,Ei)2

30

K-Vizinhos mais Próximos: 
Pesos

Quando se utiliza os pesos para 
decidir a classe, pode-se deixar de 
usar apenas os k vizinhos mais 
próximos, e passar a utilizar todo o 
conjunto de treinamento.
Isso porque exemplos muito 
distantes terão pouca influência na 
classificação do novo exemplo.

31

K-Vizinhos mais Próximos: 
Global e Local

Se todos os exemplos são 
utilizados para classificar um novo 
exemplo, então o método é 
chamado de global.
Se somente os vizinhos mais 
próximos são considerados, então 
o método é chamado de local.
Um método global utilizado para 
regressão é chamado de método 
de Shepard (Shepard, 1968).

32

K-Vizinhos mais Próximos: 
Observações

Algumas observações:

K-vizinhos mais próximos é uma método

bastante simples, mas que provê bons 
resultados na prática;

Ele é robusto a ruído e bastante efetivo

quando o conjunto de treinamento não é 
muito pequeno;

A melhor explicação que o método pode

prover é mostrar ao usuário os vizinhos 
mais próximos do novo exemplo quando o 
método é local;

33

K-Vizinhos mais Próximos: 
Observações

Algumas observações:

Portanto, o grau de explicação desses

método pode ser considerada inferior 
ao dos métodos simbólicos;

O k-vizinhos mais próximos considera

todos os atributos ao classificar um 
novo exemplo. Isso pode ser um sério 
problema quando existem muitos 
atributos irrelevantes;

34

K-Vizinhos mais Próximos: 
Observações

Algumas observações:

Para solucionar o problema de

atributos irrelevantes pode-se utilizar 
pesos para os atributos na medida de 
distância;

Outro problema é o desempenho (em

tempo de execução) para classificar 
novos casos quando o conjunto de 
treinamento é muito grande;

K-Vizinhos mais Próximos: 
Observações

n : número de exemplos
m : número de atributos
k: número de vizinhos
Complexidade de Treino: O(1)
Complexidade de Teste: O(nk+mn)

O(m.n) para calcular a distância de todos os 
exemplos

O(n.k) para encontrar os vizinhos mais próximos

Quando o conjunto de treinamento é muito grande, 
torna-se computacionalmente caro encontrar os 
vizinhos mais próximos.

K-Vizinhos mais Próximos: 
Observações

n : número de exemplos
m : número de atributos
k: número de vizinhos
Complexidade de Treino: O(1)
Complexidade de Teste: O(nk+mn)

O(m.n) para calcular a distância de todos os 
exemplos

O(n.k) para encontrar os vizinhos mais próximos

Quando o conjunto de treinamento é muito grande, 
torna-se computacionalmente caro encontrar os 
vizinhos mais próximos.

37

K-Vizinhos mais Próximos: 
Observações

Esse problema pode ser reduzido se 
forem armazenados apenas exemplos 
prototípicos ou quando se utiliza algum 
método de indexação como kd-trees 
(Bentley, 1975), m-trees (Ciaccia, 1997) 
ou slim-trees (Train Jr., 2000).

38

Indexação

Uma forma de indexar exemplos 
foi proposta por (Orchard, 1991);
O método de Orchard é bastante 
simples, apesar de ser pouco 
utilizado por requerer O(n2) para 
espaço.
Entretanto, (Ye et al., 2009) 
transformou esse algoritmo para 
ser da classe anyspace.

39

Indexação

(Ye et al., 2009)

40

Indexação

Dado um objeto de consulta q, e a 
sua distância calculada para um 
objeto ai (d(ai, q)), qualquer objeto 
aj que

d(ai, aj) ≥ 2 x d(ai, q)
   pode ser eliminado da busca por

similaridade.
Esse conceito é ilustrado na figura 
a seguir...

Indexação

Sabendo d(ai, q), podemos eliminar 
o objeto aj’ , mas não podemos 
eliminar aj
41

(Ye et al., 2009)

42

Indexação

(Ye et al., 2009)

Template Reduction fo 
KNN (TRKNN)

Template Reduction for 
KNN (TRKNN)

Template Reduction for 
KNN (TRKNN)

Tempo médio de execução para

3600 movimentos

Tempo(KNN) = 90,33s (3,15)
Tempo(TRKNN) = 26,45s (2,51)

KD-Tree

Índice Invertido

D1: “promoção iphone”        spam

D2: “promoção samsung”    spam

D3: “projeto ia”                    não-spam

D4: “filtro spam”                  não-spam

Novo exemplo: “projeto filtro”

palavra
documento

promoção
D1, D2

iphone
D1

samsung
D2

projeto
D3

filtro
D4

ia
D3

spam
D4

Locality-Sensitive Hashing (LSH)

o
o
o

o
o

o

o

o

o

o
o

o

Hiper-planos aleatórios h1 … hk

o

h3
h2
h1

Comparar somente
com os vizinhos que 
estiverem na
mesma partição

Tranformação do espaço

Resultados

52

Referências

Referências:

Bentley, J. Multimensional binary search trees used

for associative searching. Communications of the 
ACM, 18(9), 509-517, 1975.

Ciaccia, P.; Patella, M.; Zezula, P. M-tree: an efficient

access method for similarity search in metric spaces. 
Proceedings of VLDB, 426-435, 1997.

Mitchell, T. Machine Learning. McGraw-Hill, 1997.

Orchard, M. T. A fast nearest-neighbor search

algorithm. International Conference on Acoustics, 
Speech and Signal Processing (ICASSP), pages 2297-
2300, IEEE Computer Society Press, 1991.

Datar, Mayur, et al. "Locality-sensitive hashing

scheme based on p-stable distributions." Proceedings 
of the twentieth annual symposium on 
Computational geometry. ACM, 2004.

53

Referências

Referências:

Traina, Jr., C.; Traina, A.; Seeger, B.; Faloutsos, C.

Slim-trees: high performance metric trees minimizing 
overlap between nodes. Proceedings of ETBT, 51-65, 
2000.

Shepard, D. A two-dimensional interpolation function

for irregularly spaced data. Proceedings of the 23rd 
National Conference of the ACM, 517-523, 1968.

Stanfil, C.; Waltz, D. Towards Memory-based

reasoning. Communications of the ACM, 29, 1213-
1228, 1986.

54

Referências

Referências:

Ye, L.; Wang, X.; Keogh, E.; Mafra-Neto, A.

Autocannibalistic and Anyspace Indexing Algorithms 
with Applications to Sensor Data Mining. SIAM 
International Conference on Data Mining, 2009.

Wilson, D. R.; Martinez, T. R. Improved

heterogeneous distance functions. Journal of Artificial 
Intelligence Research (JAIR), 6:1–34, 1997.