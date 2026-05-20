Conteúdo p1: 
vai cair camada de apĺicação a partir do slide 84!

Comutação de pacotes e Segmentação de 
Mensagens

Sem segmentação

-​
Desperdício de banda larga

Com segmentação

●​ Melhor uso da largura de banda (Multiplexação Estatística): Pacotes de diferentes 
fontes podem compartilhar o mesmo link simultaneamente. Se uma fonte parar, 
outra ocupa seu lugar instantaneamente, evitando desperdício de banda. 
●​ Transmissão Paralela e Roteamento Dinâmico: Os pacotes podem seguir caminhos 
diferentes para evitar congestionamentos. Enquanto um pacote aguarda na fila de 
um roteador, outros já podem estar avançando por outros caminhos. 
●​ Menor Latência de "Store-and-Forward": Em vez de esperar uma mensagem de 1GB 
ser enviada por completo para começar a processar a próxima, um roteador pode 
encaminhar o primeiro pacote assim que ele chega, processando o resto enquanto 
isso. 
●​ Recuperação de Erros Rápida: Se um pacote for corrompido, apenas ele precisa ser 
retransmitido, e não todo o arquivo.

Comutação por circuito

-​
Reserva e transmissão de dados por enlace; 
-​

Comutação por pacote

-​
Não precisa estabelecer conexão (onde cada pacote de dados é tratado como uma 
unidade independente contendo todas as informações necessárias para chegar ao 
destino). Porém pode existir entre as pontas! 
-​
Congestionamento excessivo, estouramento da memória do buffer, podendo 
ocorrer perda de dados; recebe mais pacote do que consegue lidar. Dado isso, é 
necessário de protocolos para garantir transferências confiáveis;

Sistema Autônomo (AS)

Ex: Internet da UFMS; ISP não pode controlar como essa internet vai ser usada aqui dentro, 
porém, ela fornece os serviços que provém o acesso a internet. 
 
ISP (Internet Service Provider)

-​
Organizações que provêm acesso à internet; possuem níveis. 
-​
ISP nível 1: cobertura nacional/internacional; 
 
IXP (Ponto de troca de internet)

-​
Interconexão entre provedores de nível 1;

Medidas de desempenho

Latência

-​
ou atraso, em unidades de tempo; 
-​
Tempo para enviar uma mensagem do ponto A para o ponto B;

Vazão

-​
throughput) em bits por segundo; 
-​
é taxa de bits efetivamente transportadas; 
-​
Largura de banda é a taxa mínima de bits que um meio físico pode transmitir em 
uma unidade de tempo (taxa de transmissão)

Quanto vale um Mega

Relacionado ao tempo: As taxas de transmissão serão com potências de 10. 
Relacionado ao armazenamento: potências de 2.

Atrasos em comutação por pacotes

-​
Processamento no nó (verificação de bits com erro) 
-​
Enfileiramento (dependente do congestionamento do roteador) 
-​
Atraso de transmissão ()

-​
Atraso de propagação ()

Atraso de transmissão X Atraso de propagação (RTT)

-​
RTT = ida + volta = 2 * propagação 
 
Produto: retardo X largura de banda - qtde máx. de dados em “voo” ou na “tubulação”; 
normalmente relativo ao RTT

Ex: 100ms x 45Mbps = ~549KB

Modelo OSI

Comunicação entre processos

Funcionalidade da rede 
Comunicação entre processos

●​ Transforma conectividade host-a-host em comunicação processo-a-processo;

Programação com sockets

Uma interface (uma “porta”), local ao hospedeiro, criada por e pertencente à aplicação, e 
controlado pelo SO. Um ponto de acesso, que através de uma biblioteca, permitisse a 
entrada e como saída de mensagens para/de outro processo de aplicação (remoto ou 
local). É a criação de conexões de rede entre softwares, permitindo a troca de dados 
entre um cliente e um servidor. Ela utiliza uma API que funciona como uma ponte para 
enviar e receber informações em tempo real, baseando-se em protocolos como TCP ou 
UDP para estabelecer essa comunicação.

●​ são explicitamente criados, usados e liberados por APIs; 
●​ paradigma cliente/servidor; 
●​ dois tipos de transporte via API Sockets; 
○​ datagrama, não confiável 
○​ fluxo de bytes, confiável 
●​ Meta: aprender a construir aplicações cliente/servidor que se comunicam usando 
sockets (API Sockets);

API Sockets

●​ elemento de ligação entre a aplicação e um sistema de mais baixo nível (diretamente 
com o hardware);

O que é um socket?

●​ Interface padrão do sistema Unix; 
●​ Na camada de transporte, os sockets suporta os protocolos: 
○​ TCP 
■​ entrega confiável e em ordem; orientado à conexão (conexão

contínua entre o par de comunicação); bidirecional. 
○​ UDP 
■​ não há noção de conexão - aplicação indica destinatário para/ cada

datagrama; envio e recebimento. 
○​ SCTP 
○​ Obs: ela não fica presa a somente estes protocolos, no entanto. 
 
Visão Socket da Internet

●​ Ao chamar uma função que cria um socket, a função cria uma interface, que é 
acessível via um manipulador (file descriptor em C); 
●​ Além de precisar saber o IP, precisamos saber do número da porta (16 bits), estes 
podem variar de 0 a 65535.

○​ Esse espaço de numeração é considerado separadamente em cada 
protocolo de transporte. Isto é, cada protocolo pode usar cada tipo de 
faixa, onde as faixas podem se repetir.

Portas

Associações (bind)

●​ Um processo precisa associar um socket a um endereço para “avisar” ao sistema 
operacional que deseja receber dados que chegam ao host com o endereço de 
destino especificado; 
●​ Um socket provê uma interface para enviar/receber dados para/da rede através de 
uma porta

○​ Um endereço IP indica um pacote para uma máquina, enquanto que a porta 
permite a máq​uina decidir para que processo/serviço (se tiver algum) 
direcioná-lo.

Entendendo a comunicação via socket:

Cliente-Servidor

Os passos que envolvem escrever uma aplicação cliente diferem superficialmente entre 
TCP  e UDP.

*perceba que os passos 2 e 6 estão em vermelho, pois só na o TCP que ele estabelece a 
conexão primária com o servidor

Servidor

●​ Basicamente, existem dois aspectos em um servidor: 
○​ Escutar por conexões de clientes 
○​ Manipular cada conexão de clientes 
■​ enviar e receber mensagens do cliente 
○​ Obs: tanto o lado do cliente quanto o lado do servidor têm portas próprias 
na comunicação por sockets, mas elas funcionam de maneiras diferentes. 
○​ Pode-se separar o manipulador de uma conexão em uma função de suporte; 
e ser executada em thread separada.

*unidade de transmissão = 8 bits = 1 byte

Funcionamento em Python

A criação de um socket é realizada via chamada à função socket com dois parâmetros

●​ AF_INET (para indicar que o endereço IP é IPv4) 
●​ SOCK_DGRAM (UDP) ou SOCK_STREMA (TCP) 
Salientamos que, mesmo em Python, há muitos outros parâmetros para a criação de um 
socket. Consulte a documentação do Python para detalhes adicionais 
https://docs.python.org/3/library/socket.html#module-socket)

Programação com sockets:

Usando UDP

UDP: Não tem “conexão” entre cliente e servidor.

●​ não tem “handshaking”; 
●​ remetente coloca explicitamente endereço IP e porta do destino 
●​ servidor deve extrair endereço IP, porta do remetente do datagrama recebido 
●​ O cliente sabe para qual porta do servidor enviar, pois, esta, foi definida pelo 
desenvolvedor (dentro da aplicação) na configuração do servidor. Agora, do lado do 
cliente, o SO escolhe uma porta livre (para o cliente) na hora e a envia dentro do 
pacote para o servidor.

Usando TCP

Cliente deve contatar servidor

●​ processo servidor deve antes estar em execução 
●​ servidor deve antes ter criado socket (porta) que aguarda contato do cliente 
Cliente:

●​ cria socket TCP local ao cliente 
●​ especifica endereço IP, número de porta do processo servidor 
●​ quando cliente cria socket: TCP cliente deve criar conexão com TCP do servidor 
●​

** A porta do lado do servidor vai ser SEMPRE a mesma. O que difere uma conexão 
cliente-servidor é o IP e a porta do cliente!

** O socket de entrada vai ser um software sempre ativo. Quando o servidor recebe uma 
nova conexão com um cliente, ele cria um novo “software” socket de conexão. 
Ou seja, inicialmente, o servidor tem apenas um socket. Quando acha uma nova conexão

com o cliente, ele cria um socket de conexão com ele. Acabada esta conexão, ele fecha

este socket de conexão. 
 
Cada conexão aceita corresponde a uma 4-upla única: (IP cliente, porta cliente, IP servidor, 
porta servidor). Isso permite que milhares de clientes diferentes conversem 
simultaneamente com o mesmo serviço, todos usando a mesma porta do lado do servidor.

Cuidado com a armadilha!

As funções:

podem retornar menos bytes, e nenhuma mensagem de erro é retornada neste caso! 
Solução: ao usar as funções recv, recvfrom, send e sendto pode-se passar como 
parâmetro a flag MSG_WAITALL.

Ordem de bytes para endereços e portas

●​ Endereços e portas são armazenados como inteiros 
●​ Problema: 
○​ máquina SOs diferentes usam diferentes ordens: 
■​ little-endian: lower bytes first 
■​ big-endian: higher bytes first 
○​ essas máquinas podem se comunicar em uma rede 
●​ Solução: 
○​ Definições: 
■​ Host Byte-Ordering: a ordem utiliza por um host (big ou little) 
■​ Network BYte-Ordering: a ordem utilizada pela rede - sempre

big-endian.

Lidando com chamadas bloqueantes

[não vai ser cobrado isso na prova]

Noções de Segurança (EAD)

Pilares da Segurança

●​ Confidencialidade (esconder de quem não deve vê-la) 
○​ Por meio de criptografia. 
○​ No TLS: usa criptografia simétrica (AES, ChaCha 20) após o handshake - fase 
inicial 
○​ Exemplo: HTTPS protege senhas e cartões 
●​ Integridade (garantir o envio de informações) 
○​ garante que os dados não foram alterados em trânsito 
○​ TLS usa modos AEAD 
○​ funções de hash como SHA-256 sustentam a consistência 
●​ Autenticação (provar quem dizer ser) 
○​ Confirma a identidade do servidor (e opcionalmente do cliente) 
○​ Validação: hostname precisa corresponder ao CN/SAN do certificado 
○​ Proteção contra spoofing e Man-in-the-middle 
●​ Não repúdio (garante que uma mensagem não negue seu autor) 
○​ Impede que o emissor negue a autoridade da mensagem 
○​ baseado em assinaturas digitais  
○​ observação: não repúdio dos dados de aplicação não é garantido 
diretamente por TLS.

Criptografia Simétrica

Mesma chave para cifrar e decifrar 
Muito rápida; ideal para grandes volumes. 
No TLS: usada após negociar a chave de sessão no handshake

Criptografia Assimétrica

Usa par de chaves pública/privada

Firewalls

Isola a rede interna da organização da internet, permitindo que alguns pacotes passem e 
outros pacotes sejam bloqueados. 
 
Por quê?

●​ impedir ataques de negação de serviço 
●​ impedir modificação e acesso ilegal a dados internos 
●​ permitir que apenas acesso autorizado ocorra dentro da rede 
●​ três tipos de firewalls 
○​ filtros de pacotes stateless 
○​ filtros de pacotes stateful 
○​ gateways de aplicação

Filtragem de pacotes Stateless

●​ A rede interna é conectada à internet via um roteador firewall 
●​ Filtra pacote-a-pacote, e a decisão em repassar ou descarte pacote é baseada em: 
○​ endereço IP de origem 
○​ números de portas 
○​ tipo de mensagem ICMP 
○​ bits TCP SYN, ACK 
●​ Ferramenta rudimentar: admite pacotes que não fazem sentido algum, por exemplo, 
porta de destino = 80, bit ACK setado, mesmo com nenhuma conexão TCP 
estabelecida

Filtragem de pacotes Stateful

●​ Rastreia o estado de cada conexão TCP 
●​ Rastrear configuração de conexão (SYN), encerramento de conexão em que 
ambas as partes estão cientes do encerramento (FIN): determinar se os pacotes que 
chegam e saem possuem sentido. Limpa tabela 
●​ conexões inativas por timeout no firewall: não admitir mais pacotes

Gateways de Aplicação

Camada de Transporte

(FALTA ANOTAR AS INFORMAÇÕES ANTES DESSA PARTE - CHEGUEI ATRASADA) 
 
pag 23

UDP

Formato do Datagrama UDP

-​
32 bits

-​
octeto = bytes 
-​
ipv4 é um protocolo de rede! uma camada abaixo da de transporte!! 
-​
No cálculo do Checksum é utilizado:

-​
Pseudo-cabeçalho IP +  
-​
cabeçalho UDP +  
-​
dados

Soma de verificação (checksum) UDP

Objetivo: detectar “erros” (ex: bits trocados) no segmento transmitido; 
 
O checksum não informa onde exatamente está o erro, só que existe um erro. Além disso, 
ele pode dar um falso negativo, em alguns casos, probabilidade baixa, mas ainda existe, 
onde ocorre um erro no endereçamento mas ele dá como sem erros ou vice-versa. 
 
Transmissor:

●​ trata contéudo do segmento como sequência de inteiros de 16-bits 
●​ checksum: soma (adição usando complemento de 1) do conteúdo segmento 
●​ transmissor coloca complemento do valor da soma no campo checksum do UDP 
 
Receptor:

●​ calcula checksum do segmento recebido 
●​ verifica se o checksum calculado é 0xFFFF (ou em decimal, -1): 
○​ NÃO - erro detectado 
○​ SIM - nenhum erro detectado 
■​ mas ainda pode ter erros… 
 
Mais detalhadamente…..

Exemplo de cálculos (revisar mais como é feito o cálculo, suspeito de cair isso na prova)

Observação: esse cálculo de checksum que ocorre no UDP acontece o mesmo em TCP!

TCP

Características:

●​ ponto a ponto: um transmissor, um receptor 
●​ baseado em stream: 
○​ sequências de bytes não estruturada 
●​ conexão com circuito virtual (orientado a conexão): 
○​ estabelecimento, transmissão e encerramento de conexão 
●​ confiável (detecção e correção de erros) 
●​ buffers de envio e recebimento: 
○​ buffer de retransmissão com controle automático de envio 
●​ fluxo de dados full duplex (bidirecional) 
●​ controle de fluxo por janela deslizante: 
○​ evita que emissor ultrapasse a capacidade do receptor 
●​ controle de congestionamento 
○​ evita que o emissor inunde a rede 
 
Segmentos: é o fluxo de bytes que estou enviando 
Número de sequência: é o número do byte que inicia qual trecho do fluxo que estou 
enviando. Exemplo: [0,1] [2,8,9], [6,7,9] –então→ [0], [2] e [6]. Isso ocorre para esperar os 
dados faltantes até conseguir mandar todos, tornando a conexão confiável.

-​
Esse ACK ele se refere ao próximo segmento em relação ao segmento que ele já 
recebeu. Exemplo: recebi o segmento 1, então meu ACK indica o segmento 
seguinte, o 2, e assim por diante. Esse mecanismo garante a ordem certa do 
recebimento dos dados,objetivo central do TCP.

-​
Nos 9 bits, temos de ficar ligados no CWR e ECE

-​
Nos 6 bits, temos de ficar ligados nos: ACK, PSH, RST, SYN e FIN.

Window Size

Sliding Window

Urgent Pointer

Options

-​
Tamanho de segmento máximo que cabe dentro de um IP, e consequentemente, em 
um quadro.

Padding