GEOMETRIA COMPUTACIONAL

Esta introdu¸c˜ao foi escrita pelo professor Jos´e Coelho de Pina,
do Departamento de Ciˆencia da Computa¸c˜ao do IME-USP, que
ministrou essa disciplina em 1997, 2000, 2001, 2002 e 2004, e
apenas adaptada/atualizada para essa edi¸c˜ao da disciplina

1. Introduc¸˜ao

A procura de algoritmos para resolver problemas geom´etricos vem desde
a ´epoca da antiguidade. (Algumas motiva¸c˜oes pr´aticas para a busca por
tais algoritmos foram os impostos sobre o uso da terra e constru¸c˜oes de
ediﬁca¸c˜oes.)
S˜ao bem-conhecidas as constru¸c˜oes geom´etricas de Euclides
que usavam como instrumentos r´egua e compasso e consistiam de algumas
opera¸c˜oes primitivas que podiam ser realizadas com esses instrumentos. Um
dos problemas algor´ıtmicos1 em geometria foi o chamado Problema de Apol-
lonius (cerca de 200 A.C.) no qual trˆes circunferˆencias arbitr´arias no plano
eram dadas e pedia-se uma quarta circunferˆencia que fosse tangente `as trˆes
circunferˆencias dadas. Euclides apresentou um algoritmo que resolve este
problema.
Dentre todos os problemas algor´ıtmicos em geometria (usando constru¸c˜oes
geom´etricas de Euclides) um que atraiu grande aten¸c˜ao foi o problema da
constru¸c˜ao de um pol´ıgono regular de n lados. Para alguns valores de n (e.g.
n = 3, 4, 5, 6) a solu¸c˜ao ´e conhecida desde a antiguidade. Entretanto, para
hept´agonos regulares (n = 7) prova-se que o problema n˜ao tem solu¸c˜ao.2

Em 1902, Emile Lemoine introduziu uma medida de simplicidade para
os algoritmos que usam as constru¸c˜oes de Euclides. Esta medida ´e base-
ada no n´umero de opera¸c˜oes primitivas realizadas pelo algoritmo.
Para
Lemoine, o algoritmo mais simples ´e aquele que faz menos opera¸c˜oes pri-
mitivas. A solu¸c˜ao de Euclides para o Problema de Apollonius requer 508
dessas opera¸c˜oes enquanto que um algoritmo proposto por Lemoine requer
menos de duzentas. Estava portanto introduzido em geometria um conceito
que ´e, pelo menos em essˆencia, o que hoje chamamos de complexidade de
um algoritmo.
Em geometria computacional tamb´em estamos interessados em desenvol-
ver algoritmos eﬁcientes para resolvermos problemas geom´etricos. Pelo que

1Diremos que um problema ´e algor´ıtmico se este problema pede como resposta um
algoritmo para resolver um determinado problema. Em geometria cl´assica esses problemas
s˜ao conhecidos como Problemas de Constru¸c˜oes Geom´etricas.
2Aos 17 anos Carl Friedrich Gauss (1777-1855) mostrou que n˜ao existe um algoritmo
que usando somente as opera¸c˜oes primitivas de Euclides construa um hept´agono regular.
Na realidade Gauss mostrou mais que isso, ele mostrou que existe um algoritmo para
construir um p-gon (pol´ıgono regular com p lados), p primo se e somente se p ´e um primo
da forma 22n + 1.
1

2
Geometria Computacional

foi exposto acima vemos que n˜ao ´e algo novo. A diferen¸ca ´e que as opera¸c˜oes
primitivas usam um instrumento diferente da r´egua e do compasso: usam
um computador. Um pouco mais precisamente, em geometria computacional
estamos interessados em encontrar algoritmos eﬁcientes, ou procedimentos
computacionais, para resolver problemas geom´etricos. Muitos desses pro-
blemas tˆem sua origem em outras ´areas como computa¸c˜ao gr´aﬁca, rob´otica,
computer-aided design e processamento de imagens. No desenvolvimento
de tais algoritmos s˜ao comumente utilizados resultados em geometria eu-
clidiana, combinat´oria, teoria dos grafos, estruturas de dados e an´alise de
algoritmos.
Geometria computacional ´e um termo usado por diversos grupos3. Entre-
tanto, o termo tem sido mais utilizado para descrever a sub-´area da teoria de
algoritmos trata do projeto e an´alise de algoritmos eﬁcientes para problemas
envolvendo objetos geom´etricos, principalmente, em espa¸cos de dimens˜ao 2,
3 ou de dimens˜ao constante. As entradas para os problemas s˜ao primordial-
mente objetos simples (pontos, retas, segmentos de retas, pol´ıgonos, planos e
poliedros). ´E neste sentido que usaremos o termo geometria computacional
nesta disciplina.
Se a tese de Shamos [20] em 1978 for aceita como o in´ıcio da geometria
computacional (pelo menos da maneira como ela ser´a tratada nesta disci-
plina), ent˜ao a ´area tem apenas cerca de 30 anos. Apesar disso existem pelo
menos 7 livros na ´area, 4 revistas.
A ´area desenvolveu rapidamente nos anos 70’s, 80’s e 90’s, e ainda con-
tinua a se desenvolver. Por causa da ´area a partir da qual cresceu (desen-
volvimento de algoritmos discretos), geometria computacional tem sempre
enfatizado problemas de natureza matem´atica discreta.
Na maioria dos
problemas em geometria computacional as instˆancias dos problemas s˜ao um
conjunto ﬁnito de pontos ou outro objeto geom´etrico, e a sa´ıda exigida ´e
algum tipo de estrutura consistindo de um conjunto ﬁnito de pontos ou
segmentos de retas.
De acordo com O’Rourke [18] (p´agina xi):

“. . . Not all open problems [em geometria computacional] are ne-
cessarily diﬃcult; some are simply awaiting the requisite attention
. . . ”.

Este pode ser um bom motivo para ﬁcarmos de olhos abertos durante a
disciplina e talvez tentar fazer alguma contribui¸c˜ao para a ´area.

Divirtam-se!

[O que foi brevemente tratado nesta introdu¸c˜ao foi extra´ıdo de Cap´ıtulo 3 de Cou-
rant [4], Graham [12], Mount [15], e no Cap´ıtulo 1 de Preparata e Shamos [19].]

3O termo “geometria computacional” tem sido usado com v´arias conota¸c˜oes distintas.
Por exemplo, geometria computacional tamb´em foi usado para se referir a modelagem
geom´etrica atrav´es de splines e superf´ıcies (cf. Cap´ıtulo 1 de Preparata e Shamos [19]).

Geometria Computacional
3

2. Objetivos da disciplina

O objetivo desta disciplina ´e apresentar t´ecnicas, algoritmos e estru-
turas de dados empregados no projeto e an´alise de algoritmos eﬁcientes
para resolu¸c˜ao de problemas geom´etricos. Pretendemos mostrar estrat´egias
cl´assicas de solu¸c˜ao de problemas geom´etricos, assim como apresentar pos-
sivelmente temas de pesquisa.

3. Pr´e-requisitos

Para esta disciplina, os pr´e-requisitos s˜ao: conhecimento de t´ecnicas b´asi-
cas de projeto de algoritmos, como divis˜ao-e-consquista, algoritmo guloso,
programa¸c˜ao dinˆamica; nota¸c˜ao e t´ecnicas b´asicas de an´alise de algoritmos,
como nota¸c˜ao assint´otica, resolu¸c˜ao de somat´orios e recorrˆencias; e conhe-
cimento de estruturas de dados b´asicas, como ﬁlas de prioridades (heaps) e
´arvores balanceadas de busca bin´aria.

4. T´opicos que pretendemos cobrir

Alguns dos t´opicos que pretendemos cobrir nesta disciplina s˜ao: fechos
convexos; problemas de proximidade; parti¸c˜oes convexas; busca geom´etrica;
e problemas de intersec¸c˜ao.
Abaixo encontra-se uma breve descri¸c˜ao de alguns problemas que estuda-
remos nesta disciplina.

Problema do par mais pr´oximo (closest pair problem)
Dados n pontos, queremos encontrar dois deles que es-
tejam a distˆancia m´ınima. Uma aplica¸c˜ao pr´atica deste
problema ´e em controle de tr´afego a´ereo: os dois avi˜oes
que est˜ao em maior perigo de colis˜ao s˜ao aqueles que
est˜ao mais pr´oximos. Este problema pode ser resolvido
facilmente em O(dn2), onde d ´e a dimens˜ao do espa¸co.
O problema do par mais pr´oximo pode ser resolvido
por um algoritmo do tipo divis˜ao-e-conquista em tempo O(dn log n) (cf.
Cap´ıtulo 5 de Preparata e Shamos [19]) .

Fecho convexo de um conjunto de pontos
Convexidade ´e uma propriedade geom´etrica bastante
importante. Um conjunto de pontos ´e convexo se, para
cada par de pontos no conjunto, o segmento de reta en-
tre eles est´a inteiramente contido no conjunto. Segundo
O’Rourke (cf. O’Rourke [18], pg. 80) talvez o primeiro
artigo na ´area de geometria computacional tenha sido
sobre fechos convexos. O Problema do Fecho Convexo
consiste em, dados n pontos, encontrar o fecho convexo
desses pontos. Uma das aplica¸c˜oes pr´aticas deste problema se encontra em

4
Geometria Computacional

rob´otica. Se o fecho convexo de um robˆo n˜ao colide com obst´aculos ent˜ao o
robˆo tamb´em n˜ao colide.
Nos anos 60 uma aplica¸c˜ao da Bell Labs necessitava computar o fecho
convexo de aproximadamente 10.000 pontos no plano e os algoritmos de
complexidade de tempo O(n2) foram considerados muito lentos. Tendo essa
aplica¸c˜ao como motiva¸c˜ao, no come¸co do anos 70, Graham [11] projetou o
primeiro algoritmo de complexidade de tempo O(n log n). O fecho convexo
tamb´em pode ser constru´ıdo em O(n log n) por um algoritmo de divis˜ao-e-
conquista (cf. Cap´ıtulo 3 de Preparata e Shamos [19]).

Triangulariza¸c˜ao de pol´ıgonos
O interesse aqui ´e particionar um certo ‘dom´ınio com-
plexo’ em uma cole¸c˜ao de objetos ‘simples’. A regi˜ao
mais simples na qual podemos decompor um objeto pla-
nar ´e um triˆangulo (um tetraedro em 3-d e um ‘simplex’
em geral). Dado um pol´ıgono P, queremos adicionar a
P o maior n´umero poss´ıvel de diagonais que n˜ao se cru-
zem de tal forma que o interior de P ﬁque particionado
em triˆangulos. Chazelle [1] projetou um algoritmo linear para este problema.
Um algoritmo para triangularizar pol´ıgonos pode ser utilizado em proble-
mas do tipo Art Gallery (cf. O’Rourke [17]). Imagine que as salas de uma
galeria de arte formem um pol´ıgono. Considerando que cada guarda ﬁca
parado em um local da galeria, qual ´e o menor n´umero de guardas que s˜ao
necess´arios para tomar conta das salas?

Parti¸c˜ao de pol´ıgonos
Al´em de algoritmos eﬁcientes para particionar um pol´ı-
gono em triˆangulos, tamb´em s˜ao de interesse algoritmos
que particionem um pol´ıgono em (digamos) pol´ıgonos
mon´otonos, trapez´oides e pol´ıgonos convexos. Uma mo-
tiva¸c˜ao para particionar um pol´ıgono em pol´ıgonos con-
vexos ´e o reconhecimento de caracteres: um caractere
pode ser representado como um pol´ıgono particionado
em partes convexas.

Intersec¸c˜oes
Um dos problemas geom´etricos mais b´asicos ´e o de de-
terminar quando dois objetos se intersectam.
A de-
termina¸c˜ao se dois objetos complexos se intersectam
´e freq¨uentemente reduzida ao problema de determinar
quais pares de entidades primitivas (e.g., segmentos de
retas) se intersectam.
Veremos algoritmos eﬁcientes
para computar a intersec¸c˜ao de um conjunto de seg-
mentos de retas.

Geometria Computacional
5

Diagramas de Voronoi
Dado um conjunto S de n pontos no plano, queremos
determinar para cada ponto p em S qual ´e a regi˜ao
V (p) dos pontos do plano que est˜ao mais perto de p do
que de qualquer outro ponto em S. As n regi˜oes V (p)
formam uma parti¸c˜ao do plano chamada de Diagrama
de Voronoi.
Imagine uma vasta ﬂoresta contendo v´arios pontos
de observa¸c˜ao de incˆendio. O conjunto das ´arvores que
est˜ao mais pr´oximas de um determinado posto p determina a regi˜ao V (p)
das ´arvores que s˜ao de responsabilidade do ponto p.
O diagrama de Voronoi de um conjunto de n pontos pode ser constru´ıdo
em O(n log n) por um (complicado) algoritmo de divis˜ao-e-conquista (cf.
Shamos [21]).
Em 1985, Fortune [10] projetou um algoritmo de varre-
dura (plane-sweep algorithm) muito elegante e simples cuja complexidade
de tempo ´e O(n log n).

Triangulariza¸c˜ao de Delaunay
O dual geom´etrico (usando retas) de um diagrama de
Voronoi para um conjunto S de pontos forma uma tri-
angulariza¸c˜ao do conjunto S, chamada de triangula-
riza¸c˜ao de Delaunay. A triangulariza¸c˜ao de Delaunay
tem v´arias propriedades geom´etricas interessantes. Por
exemplo, ela cont´em todas as “´arvores geradoras m´ıni-
mas” de S (cf. Cap´ıtulo 6 de Preparata e Shamos [19]).

Arranjos e dualidade
Talvez uma das estruturas matem´aticas mais importan-
tes em geometria computacional seja um arranjo de re-
tas (e em geral, arranjos de curvas e superf´ıcies). Dadas
n retas no plano, um arranjo ´e simplesmente o grafo
que tem como v´ertices as intersec¸c˜oes das retas e como
arestas os segmentos de retas ligando estas intersec¸c˜oes.
Veremos que uma tal estrutura pode ser constru´ıda em
tempo O(n2). A raz˜ao para est´a estrutura ser t˜ao im-
portante ´e que muitos problemas envolvendo pontos podem ser transforma-
dos em problemas envolvendo retas atrav´es do m´etodo de dualidade. Por
exemplo, suponha que desejemos determinar se existem trˆes pontos colinea-
res entre um conjunto de n pontos no plano. Isto pode ser determinado por
um algoritmo do tipo for¸ca-bruta em tempo O(n3). Entretanto, se os pontos
s˜ao dualizados em retas, ent˜ao (como veremos mais tarde nesta semestre) a
quest˜ao ´e reduzida a decidir se existe um v´ertice de grau pelo menos 4 neste
arranjo de retas.

6
Geometria Computacional

5. Bibliografia

Para preparar as aulas desta disciplina tenho consultado as notas de aula
do professor Jos´e Coelho de Pina [6], os livros de O’Rourke [18] e de Berg,
van Kreveld, Overmars, e Schwarzkopf [5].
O livro de Preparata e Shamos [19] ´e um texto cl´assico em geometria com-
putacional (foi primeiro livro sobre o assunto) que coloca bastante ˆenfase na
an´alise dos algoritmos apresentados. Este livro cont´em basicamente todos
os t´opicos que ser˜ao tratados nesta disciplina. Outros livros que tamb´em
podem ser encontrados na biblioteca s˜ao: Edelsbrunner [8] (“The art of
counting and estimating is at heart of combinatorics—and it is a necessary
prerequisite for analyzing algorithms . . . ”; c´opiado da introdu¸c˜ao da Parte I
de [8]); Figueiredo e Carvalho [9] (um livro muito claro e introdut´orio); e
Resende e Stolﬁ[7] (descreve varias t´ecnicas e algoritmos em geometria com-
putacional). Outros livros sobre geometria computacional s˜ao: Laszlo [14]
(um livro que descreve v´arios algoritmos em geometria computacional e apre-
senta trechos de implementa¸c˜oes em C++); Mulmuley [16] (como o pr´oprio
t´ıtulo diz, este livro trata de algoritmos aleat´orios em geometria computa-
cional).
Cormen, Leiserson, Rivest & Stein [3] ´e um livro enciclop´edico sobre
an´alise de algoritmos que trata de geometria computacional no Cap´ıtulo 33.
Na biblioteca tamb´em podem ser encontrados alguns surveys sobre geo-
metria computacional, veja por exemplo: Chazelle [2]; Graham e Yao [12];
Guibas e Stolﬁ[13]; e Yao [22].
Artigos em geometria computacional podem ser encontrados em v´arias
revistas, incluindo ACM Transactions on Graphics, Algorithmica, Journal
of Algorithms, Journal of the ACM, e SIAM Journal on Computing. Uma
revista que ´e particularmente dedicada `a ´area ´e Discrete and Computational
Geometry e mais recentemente temos International Journal of Computa-
tional Geometry & Applications e Computational Geometry, Theory and
Applications.
Existe uma conferˆencia anual em geometria computacional, a ACM An-
nual Conference on Computational Geometry (alguns dos proceedings po-
dem ser encontrados na biblioteca; veja QA758.C S989). Al´em desta, v´arias
outras conferˆencias apresentam trabalhos em geometria computacional: por
exemplo, STOC (QA800.C S989), FOCS (QA800.C S989), SODA (QA758.C
S989), e ICALP.

6. Implementac¸˜oes de algoritmos

Algumas das implementa¸c˜oes que vocˆes ver˜ao durante as aulas foram
feitas por Cassio Polpo de Campos (cassio@ime.usp.br, http://www.ime.
usp.br/~cassio/) e por Eduardo Garcia de Freitas (freitas@ime.usp.br,
http://www.ime.usp.br/~freitas/). O Cassio fez suas implementa¸c˜oes
no Turbo C e o Eduardo fez applets em Java. Todos os programas est˜ao
dispon´ıveis no URL

Geometria Computacional
7

http://www.ime.usp.br/~freitas/gc/.

7. Geometria computacional na Internet

Existe muito material muito bom de Geometria Computacional na In-
ternet. Durante o andamento da disciplina manterei na p´agina
http://www.ime.usp.br/~cris/geocomp2007/,
uma lista de alguns s´ıtios de Geometria Computacional. Durante o anda-
mento da disciplina est´a p´agina dever´a ser atualizada e expandida. Se vocˆe
encontrar algum s´ıtio de Geometria Computacional (ou de qualquer outra
coisa) que vocˆe ache interessante, por favor, n˜ao deixe de me avisar.

8. Monitor

O monitor desta disciplina ´e Rafael Cosentino (cosen@ime.usp.br, http:
//www.ime.usp.br/~cosen/.

9. Outras informac¸˜oes

A minha sala ´e a 107-C, o n´umero do meu telefone ´e 3091-5709 e meu
endere¸co eletrˆonico ´e cris@ime.usp.br.
Manterei uma p´agina de MAC 331 / MAC 5747 no URL
http://www.ime.usp.br/~cris/geocomp2007/.
Nessa p´agina eu colocarei o material da disciplina (como, por exemplo, listas
de exerc´ıcios, notas de aula, programa¸c˜ao das aulas, etc). Por favor, dˆe uma
olhada nesta p´agina regularmente.
H´a uma lista de discuss˜ao que tem como objetivo servir de suporte para
a disciplina. Recomenda-se que vocˆe mande para esta lista suas d´uvidas,
sugest˜oes, cr´ıticas ou observa¸c˜oes sobre o andamento da disciplina. Assim,
se vocˆe pretende cursar geometria computacional, por favor, inscreva-se na
lista, que estar´a acess´ıvel a partir da p´agina da disciplina. Sinta-se a vontade
para me escrever e fazer perguntas ou coment´arios sobre a disciplina.
Outros professores do Departamento de Ciˆencia da Computa¸c˜ao que es-
tudam geometria computacional s˜ao Carlos Eduardo Ferreira (sala 108-C,
cef@ime.usp.br, http://www.ime.usp.br/~cef/), Jos´e Augusto Ramos
Soares (sala 102-C, jose@ime.usp.br, http://www.ime.usp.br/~jose/), e
Jos´e Coelho de Pina (sala 4-C, jose@ime.usp.br, http://www.ime.usp.br
/~coelho/).
Se seu interesse ´e Computa¸c˜ao Gr´aﬁca, converse com o professor Antonio
Elias Fabris (e-mail aef@ime.usp.br, http://www.ime.usp.br/~aef/). Se
vocˆe quer saber o que ´e Processamento de Imagens, Vis˜ao Computacional,
etc, ent˜ao converse com os professores Carlos Hitoshi Morimoto (sala 209-C,
hitoshi@ime.usp.br, http://www.ime.usp.br/~hitoshi/), J´unior Bar-
reira (sala 290-A, jb@ime.usp.br, http://www.ime.usp.br/~jb/), e Ro-
berto Marcondes Cesar J´unior (sala 297-A, cesar@ime.usp.br, http://www
.ime.usp.br/~cesar/).

8
Geometria Computacional

Referˆencias

1. B. Chazelle, Triangulating a simple polygon in linear time, Discrete and Computati-
onal Geometry 6 (1991), 485–524.
2.
, Computational geometry: A retrospective, Proceedings of the Twenty-Sixth
Annual ACM Symposium on Theory of Computing (Montr´eal, Qu´ebec, Canada), The
ACM Special Interest Group for Algorithms and Computation Theory, May 1994,
pp. 75–94.
3. T.H. Cormen, C.E. Leiserson, and R.L. Rivest, Introduction to algorithms, The MIT
Electrical Engineering and Computer Scienece Series, The MIT Press, MacGraw-Hill
Book Company, 1990, QA758 C811i.
4. R. Courant and H. Robbins, What is mathematics?, Oxford University Press, New
York, 1941.
5. M. de Berg, M. van Kreveld, M. Overmars, and O. Schwarzkopf, Computational geo-
metry, algorithms and applications, Springer Verlag, 1997, second edition, 2000.
6. J.C. de Pina, Geometria computacional, Notas de aula, 2000.
7. P.J. de Resende and J. Stolﬁ, Fundamentos de geometria computacional, IX Escola de
Computa¸c˜ao, 1994.
8. H. Edelsbrunner, Algorithms in combinatorial geometry, EATCS Monographs on The-
oretical Computer Science, no. 10, Springer-Verlag, Berlin, 1987, QA758 E21a.
9. L.H. Figueiredo and P.C.P. Carvalho, Introdu¸c˜ao `a geometria computacional, 18o¯
Col´oquio Brasileiro de Matem´atica, IMPA, 1991, QA758 F475i.
10. S. Fortune, A sweepline algorithm for Voronoi diagrams, Algorithmica 2 (1987), 153–
174.
11. R.L. Graham, An eﬃcient algorithm for determining the convex hull of a ﬁnite planar
set, Information Processing Letters 1 (1972), 132–133.
12. R.L. Graham and F. Yao, A whirlwind tour of computational geometry, The American
Mathematical Monthly 97 (1990), no. 8, 687–701.
13. L.J. Guibas and J. Stolﬁ, Ruler, compass and computer: The design and analysis of
geometric algorithms, Theoretical Foundations of Computer Graphics and CAD (R.A.
Earnshaw, ed.), NATO ASI Series, vol. F40, Springer-Verlag, 1988, pp. 111–165.
14. M.J. Laszlo, Computational geometry and computer graphics in C++, Prentice Hall,
Upper Saddle River, NJ, 1996.
15. D. Mount, Cmsc 754: Computational geometry, Spring 2000, Course Syllabus.
16. K. Mulmuley, Computational geometry: An introduction through randomized algo-
rithms, Prentice Hall, Englewood Cliﬀs, NJ, 1994.
17. J. O’Rourke, Art gallery theorems and algorithms, The International Series of Mo-
nographs on Computer Science, Oxford University Press, New York, 1987, QA830
O74a.
18.
, Computational geometry in C, Cambridge University Press, Cambridge, 1993.
19. F.P. Preparata and M.I. Shamos, Computational geometry: An introduction, Texts
and Monographs in Computer Science, Springer-Verlag, New York, 1985, QA758
P927c.
20. M.I. Shamos, Computacional geometry, Ph.D. thesis, Yale University, New Haven,
1978.
21. M.I. Shamos and D. Hoey, Closest point problems, Proc. 16th Annual IEEE Sympo-
sium in Foundations of Computer Science, 1975, pp. 151–162.
22. F.F. Yao, Computational geometry, Handbook of Theoretical Computer Science
(J. van Leeuwen, ed.), vol. A, The MIT Press/Elsevier, Amsterdam, 1990, QA810.C3
V259h v.1A, pp. 343–389.