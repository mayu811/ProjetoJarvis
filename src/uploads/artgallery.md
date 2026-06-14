GEOMETRIA COMPUTACIONAL

TEOREMA DA GALERIA DE ARTE

1. Introduc¸˜ao

O t´opico que iremos estudar pertence `a ´area de geome-
tria combinat´oria (combinatorial gemeotry), uma sub-
´area de matem´atica e geometria computacional (ciˆencia
da computa¸c˜ao). Em 1973, Victor Klee propˆos o pro-
blema de determinar-se o menor n´umero de guardas su-
ﬁcientes para ‘guardar’ o interior de uma sala de uma
galeria de arte com n paredes.
Informalmente, cada guarda ´e considerado como um ponto ﬁxo que en-
xerga (ou vˆe) tudo a sua volta. Um conjunto de guardas cobre uma sala
se cada ponto da sala pode ser visto por algum guarda. A ﬁgura ao lado
representa a planta de uma sala de uma galeria de arte com 12 paredes, 4
guardas s˜ao suﬁcientes para cobrir a sala (podemos cobrir a sala com menos
guardas?).
Estudaremos a seguir o chamado Teorema da Galeria de Arte (Chv´atal’s
Art Gallery Theorem ou Watchman Theorem) que diz que ⌊n/3⌋guardas
s˜ao ocasionalmente necess´arios e sempre suﬁcientes para cobrir uma sala
com n paredes. Este teorema simples tem sido estendido por matem´aticos
em v´arias dire¸c˜oes (cf. [7]) e tem sido desenvolvido por cientistas da com-
puta¸c˜ao no estudo de algoritmos de parti¸c˜ao de pol´ıgonos (que veremos mais
adiante durante esta disciplina).

O fragmento de texto a seguir foi extra´ıdo de How many guards in the
Gallery de Ian Steawart [10].

State-of-the-art Gallery houses the Sandy Warthog col-
lection. . . .
“Naturally the Warthog Collection will be ﬁtted with all the
latest electronic surveillance gear,” said Harry Sams, chief of secu-
rity. “An individual micro-camera will face every painting—”
“No, I want something special for the Warthog Collection,” in-
terrupted Parrot.
“Uh—how special?”
“Real special, Harry. I want guards. Human guards.”
“Boss, let’s not get too ambitius, huh? Do you realize the cost
in positive security vetting alone? Not to mention medical insu-
rance, severance pay, coﬀee-break tokens. Real people cost real
money, Boss. No, what I suggest is the latest sniﬀer robots from
Notsobitchi and maybe a couple–”
“I want guards, Harry.”

Date: 19 de agosto de 2014.
1

2
TEOREMA DA GALERIA DE ARTE

“Boss. Guards. Uh—how many?”
“Enough to make sure that every square inch of the building
can be seen by at least one guard. I want each guard stationed
on a swivel chair, so that in eﬀect each one has all-around vision.
Hire as many as the job needs—but not a single guard extra, you
understand? Human guards cost real money, you know.”
. . .

Observa¸c˜ao.
Os t´opicos que cobriremos a seguir foram extra´ıdos do livro de
O’Rourke [7], Cap´ıtulo 1 de O’Rourke [8] e das notas de aula de Mount [6]. Veja
tamb´em Steawart [10].

2. Definic¸˜oes e convenc¸˜oes

Uma curva poligonal ´e uma sequˆencia ﬁnita (v0, e0, v1, . . . , en−2, vn−1)
onde v0, . . . , vn−1 s˜ao pontos em R2 e ei ´e um segmento de reta com ex-
tremidades vi e vi+1 (i = 0, . . . , n −2).
Os pontos v0, . . . , vn−1 tamb´em
s˜ao chamados de v´ertices e os segmentos e0, . . . , en−2 de arestas. (Nota¸c˜ao:
os ´ındices ser˜ao considerados ciclicamente, assim, por exemplo, vn = v0,
en−1 = e0, . . . )
Uma curva poligonal ´e fechada se o ´ultimo ponto da
sequˆencia ´e igual ao primeiro, ou seja, v0 = vn.
Uma curva pol´ıgonal ´e
simples se ela n˜ao se autointersecta. Mais precisamente, isto signiﬁca que
o segmento ei s´o intersecta (possivelmente) o segmento ei+1 no ponto vi+1
(i = 0, . . . , n −2). Veja Figura 1.

v0

v1

v2

v3

v4

v5

v6

v7

curva poligonal
fechada simples
fechada n˜ao-simples

Figura 1.
Curvas poligonais.

O famoso Teorema de Jordan diz que toda curva plana fechada simples
divide o plano em duas regi˜oes (o interior e o exterior da curva). Deﬁnimos
um pol´ıgono como sendo a regi˜ao fechada do plano (no sentido topol´ogico)
limitada por uma curva poligonal fechada simples. O termo pol´ıgono simples
tamb´em ´e frequentemente usado com este mesmo sentido. Convencionare-
mos que os v´ertices de um pol´ıgono ser˜ao sempre listados na ordem em
que eles aparecem ao percorrermos a fronteira do pol´ıgono no sentido anti-
hor´ario, veja a Figura 2. A fronteira de um pol´ıgono P ser´a denotada por
∂P. Da nossa deﬁni¸c˜ao temos que ∂P ⊂P.

GEOMETRIA COMPUTACIONAL
3

curvanaosimples
poligono

v0
v0

v1
v1

v2

v2
v3

v3
v4
v4

v5 v6

v7
v8

v9
v10

v11

v12

v13

v14
v15

v16

Figura 2.
Uma curva poligonal fechada que n˜ao forma um
pol´ıgono e uma que forma um pol´ıgono.

3. Problema da Galeria de Arte

Diremos que dois pontos p e q de um pol´ıgono P vˆeem ou enxergam um
ao outro se o segmento que liga p e q, denotado por pq, est´a inteiramente
contido no pol´ıgono P.
A planta de uma sala, com n paredes, de uma galeria de arte pode ser vista
como sendo um pol´ıgono formado por n v´ertices (ou arestas). Considere
o problema de determinar onde devemos dispor guardas na galeria de tal
modo que cada ponto da sala possa ser visto por pelo menos um guarda.
Pensaremos em um guarda como sendo um ponto e diremos que um conjunto
de guardas guardam ou cobrem um pol´ıgono se cada ponto do pol´ıgono pode
ser visto por pelo menos um guarda. Victor Klee propˆos o seguinte problema.

Problema 1. Dado n, determinar, como uma fun¸c˜ao de n, o n´umero
m´ınimo de guardas suﬁcientes para cobrir um pol´ıgono com n vertices.

Observemos que a ´unica informa¸c˜ao que temos sobre o pol´ıgono ´e o seu
n´umero de lados (ou arestas).
N˜ao sabemos nada sobre a estrutura do
pol´ıgono. O problema pergunta pelo menor n´umero de guardas suﬁcientes
para cobrir qualquer pol´ıgono com n lados. Na Figura 3 vemos um pol´ıgono
onde 3 guardas s˜ao suﬁciente e um onde 4 guardas s˜ao suﬁcientes.
Se denotarmos por g(P) o menor n´umero de guardas necess´arios para
cobrirmos um pol´ıgono P e por G(n) o menor n´umero de guardas necess´arios
para cobrirmos um pol´ıgono com n v´ertices, ent˜ao temos que

G(n) = max{g(P) | P ´e um pol´ıgono com n v´ertices}.

N˜ao ´e dif´ıcil vermos que G(n) ´e menor do que n. Podemos colocar um
guarda em cada v´ertice do pol´ıgono. Apesar deste fato ser trivial ´e interes-
sante notar que a generaliza¸c˜ao para o espa¸co tridimensional ´e falsa (!).

Exerc´ıcio.
Encontre um poliedro no R3 tal que mesmo colocando um
guarda em cada v´ertice teremos pontos no interior do poliedro que n˜ao s˜ao
visto por nenhum dos guardas. (Este poliedro ´e certamente n˜ao-convexo.)

Salas que tˆem o formato de um pol´ıgono convexo, com qualquer n´umero de
v´ertices, podem ser cobertas por apenas um guarda, colocado em qualquer

4
TEOREMA DA GALERIA DE ARTE

Figura 3.
Um pol´ıgono coberto por 3 guardas e um outro
coberto por 4 guardas. ´E poss´ıvel usarmos menos guardas?

ponto da sala. Todo pol´ıgono com trˆes v´ertices ´e convexo, logo G(3) = 1.
Existem pol´ıgonos com quatro v´ertices que n˜ao s˜ao convexos. Diremos que
um v´ertice de um pol´ıgono ´e reﬂexo ou concavo se o seu ˆangulo interior ´e
maior do que π. J´a se o ˆangulo interior do v´ertice de um pol´ıgono for no
m´aximo π, diremos que o v´ertice ´e convexo (veja Figura 4).

R = reﬂexo e C = convexo

R
R

R

C

C

C
C

C

C

C

C

Figura 4.
Um pol´ıgono e seus v´ertices reﬂexos e convexos.

Um pol´ıgono com quatro v´ertices (um quadril´atero) pode ter no m´aximo
um ˆangulo reﬂexo, mas mesmo assim ´e poss´ıvel cobrirmos o pol´ıgono com
apenas um guarda, assim G(4) = 1. Um pol´ıgono com cinco v´ertices pode
ter 0, 1 ou 2 v´ertices reﬂexos. Fazendo alguns experimentos podemos ver
que pol´ıgonos com 5 v´ertices podem ser cobertos por apenas um guarda,
ou seja, G(5) = 1. Existem pol´ıgonos com 6 v´ertices que necessitam de 2
guardas para serem cobertos. A situa¸c˜ao est´a ilustrada na Figura 5.
Uma quest˜ao interessante em geometria combinat´oria ´e saber como o
n´umero de guardas necess´arios para cobrir um pol´ıgono cresce como uma
fun¸c˜ao de n. O pol´ıgono ‘pente’ da Figura 6 mostra que G(n) ≥⌊n/3⌋.
Veremos na pr´oxima se¸c˜ao que este n´umero ´e sempre suﬁciente, ou seja, um
pol´ıgono com n v´ertices pode ser sempre guardado por no m´aximo ⌊n/3⌋
guardas.

GEOMETRIA COMPUTACIONAL
5

G(3) = 1

G(4) = 1

G(5) = 1

G(6) = 2

Figura 5.
Pol´ıgonos como no m´aximo 5 v´ertices podem ser
cobertos com apenas 1 guarda, mas alguns pol´ıgonos com 6
v´ertices necessitam 2 guardas.

Figura 6.
Exemplo de pol´ıgonos onde ⌊n/3⌋guardas s˜ao necess´arios.

4. Teorema da galeria de arte

Estudaremos agora um resultado muito bacana em geometria combi-
nat´oria, o chamado Chv´atal’s Art Gallery Theorem.

Teorema 2 (Teorema da Galeria de Arte). Dado um pol´ıgono com n v´er-
tices, existe uma maneira de dispormos no m´aximo ⌊n/3⌋guardas neste
pol´ıgono de modo que cada ponto do pol´ıgono seja coberto por pelo menos
um guarda.

A primeira demonstra¸c˜ao do teorema acima deve-se naturalmente a Chv´atal [2].
Trˆes anos mais tarde, Fisk [3] apresentou uma prova muito simples deste te-
orema. ´E esta a prova que veremos a seguir.
A demonstra¸c˜ao de Fisk ´e baseada em dois conceitos: triangula¸c˜ao de
pol´ıgonos e colora¸c˜ao de v´ertices de um grafo.

4.1. Diagonais e triangula¸c˜ao. Dois v´ertices u e v de um pol´ıgono P
se vˆeem ou enxergam claramente se o segmento uv com extremos u e v
est´a inteiramente contido em P e se, al´em disso, a intersec¸c˜ao de uv com a
fronteira ∂P de P ´e igual a {u, v}. Ou seja u e v se vˆeem claramente se
(i) uv ⊂P; e
(ii) uv ∩∂P = {u, v}.
Uma diagonal de um pol´ıgono P ´e um segmento de reta entre dois v´ertices
de P que se vˆeem claramente. Duas diagonais distintas uv e wx de P se
cruzam se uv ∩wx ̸⊂{u, v, w, x}. Se colocarmos em um pol´ıgono P o maior

6
TEOREMA DA GALERIA DE ARTE

n´umero poss´ıvel de diagonais que duas-a-duas n˜ao se cruzam obteremos uma
triangula¸c˜ao do pol´ıgono P. Uma triangula¸c˜ao de P pode ser vista como a
uni˜ao das arestas de P e um conjunto maximal de diagonais de P que duas-a-
duas n˜ao se intersectam, a n˜ao ser, eventualmente, nos seus extremos. Uma
outra maneira de pensarmos em uma triangula¸c˜ao de um pol´ıgono P (e as
vezes ser´a mais conveniente pensarmos desta maneira) ´e como um conjunto
de triˆangulos que cobrem o pol´ıgono P e que se intersectam apenas em
v´ertices e diagonais de P.
A Figura 7 mostra uma triangula¸c˜ao de um
pol´ıgono.

Figura 7.
Triangula¸c˜ao de um pol´ıgono.

Teorema 3 (Triangula¸c˜ao). Todo pol´ıgono pode ser particionado em triˆan-
gulos atrav´es da inclus˜ao de diagonais (zero ou mais).

Demonstraremos o Teorema 3 na pr´oxima se¸c˜ao. A demonstra¸c˜ao ´e ba-
seada no fato de que todo pol´ıgono com pelo menos 4 v´ertices possui uma
diagonal. Este fato pode parecer trivial, entretanto, teremos um pouco de
trabalho em veriﬁc´a-lo.

4.2. Colora¸c˜ao de v´ertices de um grafo. Um grafo G = (V, E) ´e k-
color´ıvel se for poss´ıvel colorirmos os v´ertices de G de tal forma que se u
e v s˜ao v´ertices adjacentes em G ent˜ao a cor atribu´ıda a u ´e diferente da cor
atribu´ıda a v.
Associaremos um grafo (planar) GT = (V, E) `a triangula¸c˜ao T de um
pol´ıgono P da seguinte maneira. O conjunto de v´ertices V de GP ser´a o
conjunto dos v´ertices de P e existir´a uma aresta em E ligando v´ertices u e v
de GT se o segmento uv faz parte da triangula¸c˜ao T. Veja a Figura 8.
´E um fato conhecido que todo grafo planar pode ser 4-colorido (o famoso
Teorema das 4 Cores).
Com grafos associados a triangula¸c˜oes, que s˜ao
planares, podemos fazer melhor que isto.

Teorema 4. Se GT ´e um grafo associado a uma triangula¸c˜ao de um pol´ıgono,
ent˜ao GT ´e 3-color´ıvel.

O teorema anterior tamb´em ser´a demonstrado na pr´oxima se¸c˜ao.

4.3. Demonstra¸c˜ao do Teorema da Galeria de Arte. Seja P um pol´ı-
gono com n v´ertices. Mostraremos que P pode ser coberto por ⌊n/3⌋guar-
das.
Pelo Teorema 3, sabemos que todo pol´ıgono ´e triangulariz´avel, em

GEOMETRIA COMPUTACIONAL
7

1

1

1
1

1

1

2

2

2

2

2
2
2

3
3

3

3

3

Figura 8.
Grafo associado `a triangula¸c˜ao da Figura 7 e
uma 3-colora¸c˜ao deste grafo. As cores s˜ao 1, 2 e 3.

particular seja T uma triangula¸c˜ao de P. Do Teorema 4, sabemos que o
grafo GT associado a T ´e 3-color´ıvel. Considere uma tal 3-colora¸c˜ao e supo-
nha que as cores usadas foram, digamos, azul, verde e amarela. Observemos
que cada triˆangulo de T tem pelo menos um v´ertice de cada uma dessas
cores. Como a cole¸c˜ao de triˆangulos de T cobre P e cada triˆangulo tem
um v´ertice de cor amarela (ou qualquer outra cor), guardas colocados nos
v´ertices amarelos cobrem P. Analogamente, guardas colocados em v´ertices
de cor azul cobrem P e guardas colocado em v´ertices de cor verde cobrem
P. Pelo menos uma dessas 3 cores ´e usada em n˜ao mais do que n/3 v´ertices.
Como o n´umero de v´ertices com uma determinada cor ´e um n´umero in-
teiro, podemos trocar n/3 por ⌊n/3⌋. Logo, ⌊n/3⌋guardas s˜ao suﬁciente e
eventualmente necess´arios para cobrirmos um pol´ıgono com n v´ertices.

5. Teoria de triangulac¸˜oes

Neste se¸c˜ao provaremos alguns resultados relacionados com triangula¸c˜ao
de pol´ıgonos. Tamb´em mostraremos os Teoremas 3 e 4, que deixamos de
provar na se¸c˜ao anterior. Para estudarmos os aspectos algor´ıtmicos de tri-
angula¸c˜ao e parti¸c˜ao de pol´ıgono ainda teremos que esperar um pouco.

Lema 5. Todo pol´ıgono tem um v´ertice estritamente convexo.

Demonstra¸c˜ao. Seja P um pol´ıgono. Oriente as arestas de P no sentido
anti-hor´ario. Um transeunte andando sobre ∂P, e seguindo a orienta¸c˜ao, te-
ria o interior do pol´ıgono `a sua esquerda. Assim, em um v´ertice estritamente
convexo o nosso transeunte virar´a `a esquerda e em um v´ertice estritamente
reﬂexo ele virar´a `a direita.
Seja v o v´ertice de P com
(i) y-coordenada m´ınima; e
(ii) x-coordenada m´axima, respeitando (i).
Seja l a reta horizontal passando sobre v. A aresta seguindo v deve estar
acima de l (veja Figura 9). Logo, nosso transeunte deve virar `a esquerda
em v. Portanto, v ´e um v´ertice estritamente convexo.

Lema 6 (Meister [5]). Todo pol´ıgono com pelo menos 4 v´ertices possui uma
diagonal.

8
TEOREMA DA GALERIA DE ARTE

v
l

Figura 9.
Ilustra¸c˜ao da prova do Lema 5.

Demonstra¸c˜ao.
Seja P um pol´ıgono com n ≥4 v´ertices e seja u um
v´ertice estritamente convexo de P. Sejam v e w v´ertices adjacentes a u.
Se vw ´e uma diagonal do pol´ıgono ent˜ao n˜ao h´a o que demonstrar. Logo,
suponhamos que vw n˜ao ´e uma diagonal de P, ou seja,
• ou vw ̸⊂P;
• ou vw ⊂P e vw ∩∂P ̸⊂{v, w}.
Como n ≥4, o triˆangulo de v´ertices u, v, w, denotado por △(u, v, w),
cont´em pelo menos um v´ertice de P distinto de u, v e w. Seja t um v´ertice
de P em △(u, v, w) mais pr´oximo de u, onde a distˆancia ´e medida ortogo-
nalmente `a reta passando pelo segmento vw. Logo, t ´e o primeiro v´ertice
de P atingido quando movemos a reta ℓparalela a vw de u na dire¸c˜ao de
vw (veja Figura 10).
Aﬁrmamos que ut ´e uma diagonal de P. De fato, seja L a reta passando
por t e paralela ao segmento vw. Notemos que a intersec¸c˜ao do semiplano
determinado por L contendo o v´ertice u com o triˆangulo △(u, v, w) ´e um
triˆangulo que n˜ao tem nenhum ponto de ∂P no seu interior. Logo, o v´ertice u
vˆe t claramente. Portanto, ut ´e uma diagonal de P.

u
ℓ

v
w

t
L

Figura 10.
Ilustra¸c˜ao da prova do Lema 6.

Estamos prontos para provar o Teorema 3. Abaixo repetimos o seu enun-
ciado.

Teorema 3 (Triangula¸c˜ao). Todo pol´ıgono pode ser particionado em triˆan-
gulos atrav´es da inclus˜ao de diagonais (zero ou mais).

Demonstra¸c˜ao. Seja P um pol´ıgono. A prova ´e por indu¸c˜ao no n´umero n
de v´ertices do pol´ıgono P. Se n = 3, o pol´ıgono ´e um triˆangulo e o te-
orema vale, j´a que n˜ao precisamos adicionar nenhuma diagonal.
Agora,
suponha que n ≥4. Pelo Lema 6, sabemos que P possui uma diagonal d.
O segmento d particiona P em dois pol´ıgonos com menos do que n v´ertices;

GEOMETRIA COMPUTACIONAL
9

cada um tendo d como aresta. Aplicando a hip´otese de indu¸c˜ao, temos que
cada um desses (sub)pol´ıgonos pode ser triangularizado. Logo, combinando
as triangula¸c˜oes de cada um dos pol´ıgonos e d, obtemos uma triangula¸c˜ao
de P. (A situa¸c˜ao est´a ilustrada na Figura 11.)

d

d

d

Figura 11.
Ilustra¸c˜ao da prova do Teorema 6.

Lema 7 (N´umero de diagonais). Toda triangula¸c˜ao de um pol´ıgono de n
v´ertices consiste de n −3 diagonais e n −2 triˆangulos.

Demonstra¸c˜ao. Seja P um pol´ıgono. Provaremos o lema por indu¸c˜ao no
n´umero n de v´ertices de P. Ambas as aﬁrma¸c˜oes s˜ao verdadeiras para n = 3,
ou seja, para um triˆangulo.
Suponhamos que n ≥4.
Particionemos P em dois pol´ıgonos P1 e P2
atrav´es de uma diagonal arbitr´aria d. Suponhamos que P1 tenha n1 v´ertices
e P2 tenha n2 v´ertices. Assim, temos que n1 + n2 = n + 2.
Aplicando a hip´otese de indu¸c˜ao ao pol´ıgono P1 e ao pol´ıgono P2, temos
que toda triangula¸c˜ao de P1 possui n1 −3 diagonais e toda triangula¸c˜ao
de P2 possui n2 −3 diagonais. Toda triangula¸c˜ao de P que possui d induz
triangula¸c˜oes de P1 e P2. Assim, toda triangula¸c˜ao de P que possui d tem

(n1 −3) + (n2 −3) + 1 = n1 + n2 −5 = n + 2 −5 = n −3

diagonais. Como a escolha de d foi arbitr´aria conclu´ımos que toda trian-
gula¸c˜ao de P possui n −3 diagonais. O n´umero de triˆangulos ´e claramente
um a mais que o n´umero de diagonais.

Lema 8 (Soma dos ˆangulos). A soma dos ˆangulos internos de um pol´ıgono
de n v´ertices ´e (n −2)π.

Demonstra¸c˜ao. Pelo Lema 7, existem n−2 triˆangulos em uma triangula¸c˜ao
de um pol´ıgono com n v´ertices e cada triˆangulo contribui com π para a soma
dos ˆangulos internos.

Diremos que 3 v´ertices consecutivos u, v, w de um pol´ıgono formam uma
orelha se uw ´e uma diagonal. Duas orelhas n˜ao se sobrep˜oem se os seus
interiores s˜ao disjuntos.

Teorema 9 (Meister’s Two Ears Theorem). Todo pol´ıgono com pelo me-
nos 4 v´ertices possui pelo menos duas orelhas.

10
TEOREMA DA GALERIA DE ARTE

O teorema acima segue imediatamente do seguinte teorema.

Teorema 10. Seja P um pol´ıgono com pelo menos 4 v´ertices e T uma
triangula¸c˜ao de P. Pelo menos dois triˆangulos de T formam orelhas de P.

Demonstra¸c˜ao. A demonstra¸c˜ao ´e por indu¸c˜ao no n´umero de v´ertices n de
P. Se n = 4 ent˜ao P ´e um quadril´atero e os dois triˆangulos de T s˜ao orelhas
de P. Suponhamos que n ≥5. Particionemos P em dois pol´ıgonos P1 e P2
atrav´es de uma diagonal arbitr´aria d de T. Sejam T1 e T2 as triangula¸c˜oes
de P1 e P2, respectivamente, obtidas atrav´es da restri¸c˜ao da triangula¸c˜ao T
a P1 e P2. Pela hip´otese de indu¸c˜ao, cada um dos (sub)pol´ıgonos P1 e P2
´e um triˆangulo ou, pela hip´otese de indu¸c˜ao, possui duas orelhas formadas
por triˆangulos em T1 e T2, respectivamente. Pelo menos um desses (possivel-
mente dois) triˆangulos de T1 ´e uma orelha de P. Analogamente, pelo menos
um desses (possivelmente dois) dos triˆangulos de T2 ´e uma orelha de P.
Como estes triˆangulos s˜ao disjuntos, a prova do teorema est´a completa.

Estamos agora preparados para demonstrar o Teorema 4 da se¸c˜ao ante-
rior.

Teorema 4. Se GT ´e um grafo associado a uma triangula¸c˜ao T de um
pol´ıgono P, ent˜ao GT ´e 3-color´ıvel.

Demonstra¸c˜ao. A prova ´e por indu¸c˜ao no n´umero de v´ertices n de GT .
Claramente um triˆangulo ´e 3-color´ıvel.
Logo, podemos supor que n ≥4.
Pelo Teorema 10, sabemos que P tem uma orelha (na realidade pelo menos
duas) que ´e formada por um triˆangulo △(u, v, w) de T. Seja P ′ o pol´ıgono
obtido a partir de P atrav´es da remo¸c˜ao desta orelha (isto ´e, troque a sub-
sequˆencia . . . , u, v, w, . . . na fronteira ∂P pela subsequˆencia . . . , u, w, . . .) e
seja T ′ a triangula¸c˜ao de P ′ obtida a partir de T, simplesmente removendo-
se △(u, v, w). Ent˜ao P ′ tem n −1 v´ertices e, pela hip´otese de indu¸c˜ao, o
grafo GT ′ associado `a triangula¸c˜ao T ′ ´e 3-color´ıvel. O grafo GT pode ser
obtido a partir de GT ′ simplesmente adicionando o v´ertice v e as arestas
uv e vw. Logo, existe (um ´unica!) maneira de estendermos a 3-colora¸c˜ao
de GT ′ a uma 3-colora¸c˜ao de GT (‘pinte’ v com a cor que n˜ao pintamos u
nem w).

6. Exercicios

1. (Exerc´ıcio 1.1.4.6 de [8] — guardando a parede) Construa um pol´ıgono P
e disponha guardas em P de tal forma que os guardas vˆeem todos os
pontos em ∂P, mas existem pontos em P que n˜ao s˜ao vistos/cobertos
pelos guardas.
2. (Exerc´ıcio 1.1.4.6 de [8] — guardas em poliedros) Descreva um poliedro
em R3 que mesmo colocando-se guardas em todos os v´ertices existim
pontos do poliedro que n˜ao s˜ao cobertos pelos guardas.
Sugest˜ao. Veja o Cap´ıtulo 9 O’Rourke [7].
3. (‘Tetraedriza¸c˜ao’ de poliedros) Descreva um politopo (um politopo ´e um
poliedro limitado) de genus zero (ou seja o politopo n˜ao tem ‘buracos’)
em R3 que n˜ao pode ser particionado em tetrahedros tendo v´ertices sele-
cionados dentre os v´ertices do politopo.
Sugest˜ao. Veja o Cap´ıtulo 10 O’Rourke [7].

GEOMETRIA COMPUTACIONAL
11

Observa¸c˜ao. Ruppert e Seidel [9] mostraram que o seguinte problema ´e NP-
completo: dado um politopo P em R3, decidir se P pode ou n˜ao ser tetrae-
drizado. Below, De Loera e Richter-Gebert [1] provaram que o problema de
minimizar o n´umero de tetraedros em uma tetraedriza¸c˜ao de um politopo con-
vexo em R3 ´e NP-dif´ıcil. (Note que isto, em particular, signiﬁca que politopos
convexos possuem tetraedriza¸c˜oes com um n´umero diferente de tetraedros. Em
dimens˜ao 2, n˜ao temos um fato semelhante.)
4. Pelo Teorema da Galeria de Arte sabemos que ⌊n/3⌋guardas s˜ao ocasi-
onalmente necess´arios e sempre suﬁcientes para cobrir qualquer pol´ıgono
com n v´ertices. Tendo este teorema em mente, o professor Maqui Sperto
fez a seguinte aﬁrma¸c˜ao: Seja P = (v0, v1, . . . , vn) um pol´ıgono (v´ertices
em ordem anti-hor´ario a medida que eles ocorrem quando percorremos ∂P)
e seja Vk := {vi | i mod 3 = k} (k = 0, 1, 2). Ent˜ao guardas colocados
nos v´ertices em Vk cobrem o pol´ıgono P para algum k ∈{0, 1, 2}. Apre-
sente um exemplo que mostra que o professor Sperto est´a enganado.
5. (Exerc´ıcio 1.1.4.2 de [8] — Visibilidade clara) Seja G′(n) o menor n´umero
de guardas suﬁcientes para verem claramente cada ponto de um pol´ıgono
com n v´ertices. Qual ´e a rela¸c˜ao entre G(n) e G′(n)? A prova de Fisk
estabelece que G′(n) ≤⌊n/3⌋? Tente determinar G′(n) exatamente.
6. (Exerc´ıcio 1.1.4.3 de [8] — Guardas nos v´ertices) Tente resolver o exerc´ıcio
anterior com a restri¸c˜ao que os guardas s´o podem ser colocados em
v´ertices do pol´ıgono.
7. (Exerc´ıcio 1.2.5.1 de [8] — Soma dos ˆangulos externos) Qual ´e a soma
dos ˆangulos externos de um pol´ıgono com n v´ertices.
8. O dual de uma triangula¸c˜ao T de um pol´ıgono P ´e um grafo com um
v´ertice associado a cada triˆangulo de T e uma aresta ligando dois v´ertices
se e somente se os triˆangulos correspondentes tˆem um lado (diagonal) em
comum. Prove que o dual D de uma triangula¸c˜ao ´e uma ´arvore (uma
´arvore ´e um grafo conexo sem ciclos).
9. Prove ou de um contra-exemplo: Toda ´arvore bin´aria ´e dual de uma
triangula¸c˜ao de algum pol´ıgono.
10. (Exerc´ıcio 1.2.5.3 de [8] — triangula¸c˜oes extremais) Quais pol´ıgonos tem o
menor n´umero de triangula¸c˜oes (em fun¸c˜ao do n´umero de v´ertices n)? Um
pol´ıgono de n v´ertices pode ter uma ´unica triangula¸c˜ao? Quais pol´ıgonos
de n v´ertices tem o maior n´umero de triˆangula¸c˜oes distintas?
11. (Exerc´ıcio 1.2.5.4 de [8] — n´umero de triangula¸c˜oes) Qual o n´umero de
triangula¸c˜oes distintas de um pol´ıgono convexo com n v´ertices?
Sugest˜ao. Veja o Cap´ıtulo 10, p´aginas 505–508, de [4].
12. (Exerc´ıcio 1.2.5.7 de [8] — rota¸c˜oes em ´arvores) Para aqueles que conhe-
cem a opera¸c˜ao de rota¸c~ao para mander o balanceamento de ´arvores
bin´arias de busca.
Interprete a orepara¸c˜ao de rota¸c~ao em termos de
triangula¸c˜ao de pol´ıgonos.
13. O professor Maqui Sperto (novamente) propˆos uma altera¸c˜ao para a prova
do Lema 6 Ele sugeriu que o v´ertice t, escolhido na demonstra¸c˜ao, fosse
um v´ertice tal que a distˆancia entre v e t fosse m´ınima e aﬁrmou que
escolhendo t dessa maneira vt ´e uma diagonal do pol´ıgono P. O pro-
fessor conseguiu dar um palpite correto desta vez? (Vocˆe precisa ver a
demonstra¸c˜ao do lema para fazer este exerc´ıcio.)

12
TEOREMA DA GALERIA DE ARTE

14. (Minimizar o n´umero de guardas est´a em NP) Descreva um algoritmo de
complexidade de tempo polinomial que resolve o seguinte problema de
decis˜ao: dados um pol´ıgono P e pontos p1, . . . , pk, guardas colocados nos
pontos p1, . . . , pk cobrem P?
15. (Minimizar o n´umero de guardas ´e NP-d´ıﬁcil) Considere o problema de
decis˜ao: dados: um pol´ıgono P e um inteiro positivo k; quest˜ao: P pode
ser coberto por k guardas? Mostre que este problema ´e NP-completo.
Sugest˜ao. Veja o Cap´ıtulo 9 O’Rourke [7].

Referˆencias

[1] A. Below, J.A. De Loera e J. Richter-Gebert, Finding minimal triangulations of con-
vex 3-polytopes is NP-hard, Proceedings of the Eleventh Annual ACM-SIAM Sympo-
sium on Discrete Algorithms, ACM-SIAM, 2000, pp. 65–66.
[2] V. Chv´atal, A combinatorial theorem in plane geometry, Journal of Combinatorial,
Series B 18 (1975), 39–41.
[3] S. Fisk, A short proof of Chv´atal’s watchman theoreom, Journal of Combinatorial
Theory, series B 24 (1978), 374.
[4] R.P. Grimaldi, Discrete and combinatorial mathematics, Addison-Wesley, 1994,
QA832 G861d.
[5] G.H. Meister, Polygons have ears, American Mathematical Monthly 82 (1975), 648.
[6] D. Mount, CMSC 754: Computational geometry, Spring 2000, Course Syllabus.
[7] J. O’Rourke, Art gallery theorems and algorithms, The International Series of Mo-
nographs on Computer Science, Oxford University Press, New York, 1987, QA830
O74a.
[8]
, Computational geometry in C, Cambridge University Press, Cambridge,
1993, Second Edition, 1998.
[9] J. Ruppert e R. Seidel, On the diﬃcult of triangulating three-dimensional non-convex
polyhedra, Discrete and Computational Geometry 7 (1992), 227–253.
[10] I. Stewart, How many guards in the gallery, Scientiﬁc American (1994), 88–90,
Mathematical Recreations.