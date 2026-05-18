const sendBtn = document.getElementById('sendBtn');
const messageInput = document.getElementById('messageInput');
const chatBox = document.getElementById('chatBox');
const clipBtn = document.getElementById('clipBtn');
const fileInput = document.getElementById('fileInput');


// Abre a seleção de arquivos quando o ícone de clipe é clicado
clipBtn.addEventListener('click', () => {
    fileInput.click();
});

// Função para adicionar mensagens ao chat
function adicionarMensagem(texto, tipo) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', tipo);

    const ul = document.createElement('ul');

    const spanConteudo = document.createElement('span');
    spanConteudo.classList.add(tipo === 'sent' ? 'sent-content' : 'received-content');
    spanConteudo.textContent = texto;

    const spanHora = document.createElement('span');
    spanHora.classList.add(tipo === 'sent' ? 'sent-time' : 'received-time');
    spanHora.textContent = new Date().toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });

    ul.appendChild(spanConteudo);
    ul.appendChild(spanHora);
    messageDiv.appendChild(ul);
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Adiciona a mensagem de arquivo enviado ao chat quando 
// um arquivo é selecionado
fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        adicionarMensagem(`Arquivo enviado: ${file.name}`, 'sent');
        
        
        setTimeout(() => {
            adicionarMensagem('Recebi seu arquivo!', 'received');
        }, 1000);
    }
});

// Variável para controlar a exibição da mensagem inicial
let primeiraVez = true;

window.addEventListener('load', () => {
    adicionarMensagem('Olá! Como posso ajudar você hoje?', 'received');
});

// Função para enviar mensagens
async function sendMessage() {
    const texto = messageInput.value.trim();
    if (texto === '') return;

    adicionarMensagem(texto, 'sent');
    messageInput.value = '';

    /*
    // chama seu backend
    const resposta = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mensagem: texto })
    });

    const dados = await resposta.json();
    adicionarMensagem(dados.resposta, 'received');
    */
   
    // simulação de resposta — substitua pelo call da sua API RAG
    setTimeout(() => {
        adicionarMensagem('Recebi sua mensagem!', 'received');
    }, 1000);
}

// Envia a mensagem quando o botão de enviar 
//  é clicado ou quando a tecla Enter é pressionada
sendBtn.addEventListener('click', sendMessage);
messageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});