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
    
    // renderiza markdown só nas mensagens recebidas
    if (tipo === 'received') {
        spanConteudo.innerHTML = marked.parse(texto);
    } else {
        spanConteudo.textContent = texto;
    }
   
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
fileInput.addEventListener('change', async () => {
    const file = fileInput.files[0];
    
    if (!file) return;

    const formData = new FormData();
    formData.append('arquivo', file);
    
    try {
        const resp = await fetch('/upload', {
            method: 'POST',
            body: formData  // FormData não usa Content-Type: application/json
        });

        const dados = await resp.json();

        if (resp.ok) {
            adicionarMensagem(dados.mensagem, 'received');
        } else {
            adicionarMensagem('Erro:' + dados.erro, 'received');
        }

    } catch (error) {
        adicionarMensagem('Erro no upload: '+ error.message, 'received');
    }

    fileInput.value = '';
});

// Variável para controlar a exibição da mensagem inicial
let primeiraVez = true;

// mensagem de boas as vindas
window.addEventListener('load', () => {
    adicionarMensagem(
        '🤖 Olá! Sou o **Jarvis**, seu assistente acadêmico inteligente!\n\n' +
        '📌 **O que posso fazer por você:**\n' +
        '• 📚 Responder perguntas sobre seus documentos\n' +
        '• ✅ Gerenciar tarefas e agenda\n' +
        '• 🎯 Criar planos de estudo personalizados\n' +
        '• 📝 Gerar exercícios sobre qualquer tema\n' +
        '• 💡 Recomendar tópicos relacionados para revisão\n\n' +
        '📎 **Envio de arquivos:**\n' +
        '• Clique no ícone 📎 para enviar **um** arquivo POR VEZ\n' +
        '• Formatos aceitos: PDF, TXT ou DOCX\n' +
        '• Aguarde a confirmação antes de enviar outro\n\n' +
        '💬 **Exemplos do que você pode digitar:**\n' +
        '• _"Gerar exercícios sobre [tema de algum documento enviado]"_\n' +
        '• _"O que tenho na agenda amanhã?"_\n' +
        '• _"Me ajuda a planejar os estudos da semana"_\n\n' +
        'Como posso te ajudar hoje? 😊',
        'received'
    );
});

// Função para enviar mensagens
async function sendMessage() {
    const texto = messageInput.value.trim();
    if (texto === '') return;

    adicionarMensagem(texto, 'sent');
    messageInput.value = '';

    
    try {// chama seu backend
    const resposta = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mensagem: texto })
    });

    const dados = await resposta.json();
    adicionarMensagem(dados.resposta, 'received');
    } catch (error) {
        adicionarMensagem('Erro: ' + error.message, 'received');
    }

}

// Envia a mensagem quando o botão de enviar 
//  é clicado ou quando a tecla Enter é pressionada
sendBtn.addEventListener('click', sendMessage);
messageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});