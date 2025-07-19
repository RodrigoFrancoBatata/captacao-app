// Função para buscar o endereço via ViaCEP
document.getElementById('cep').addEventListener('blur', async function () {
    const cep = this.value.replace(/\D/g, '');
    if (cep.length === 8) {
        const response = await fetch(`https://viacep.com.br/ws/${cep}/json/`);
        const data = await response.json();
        if (!data.erro) {
            document.getElementById('endereco').value = `${data.logradouro} ${data.bairro} - ${data.localidade}`;
        } else {
            alert("CEP não encontrado.");
        }
    }
});

// Modal
function abrirModal() {
    document.getElementById('modal').style.display = 'block';
}
function fecharModal() {
    document.getElementById('modal').style.display = 'none';
}
function salvarRetorno() {
    const data = document.getElementById('data_retorno').value;
    if (data) {
        document.getElementById('proxima_visita').value = data;
        fecharModal();
    } else {
        alert("Selecione uma data.");
    }
}

// Fechar modal ao clicar fora
window.onclick = function (event) {
    const modal = document.getElementById('modal');
    if (event.target === modal) {
        modal.style.display = "none";
    }
}
