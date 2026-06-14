from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)
# Linha nova: garante que os acentos apareçam corretamente em português
app.json.ensure_ascii = False

# Banco de dados simulado na memória do servidor para registrar os atendimentos
logs_atendimento = []

@app.route('/webhook', methods=['POST'])
def webhook_chatbot():
    """
    Rota principal que recebe as interações do usuário.
    Simula uma árvore de decisão para zeladoria urbana (ODS 6 e 7).
    """
    # Captura os dados enviados na requisição simulada
    dados_recebidos = request.json or {}
    mensagem_usuario = dados_recebidos.get('mensagem', '').strip()
    
    # 1. Fluxo Lógico: Opção 1 - Iluminação Pública (ODS 7)
    if mensagem_usuario == "1":
        resposta_bot = (
            "Você selecionou: Iluminação Pública (ODS 7).\n"
            "Por favor, digite o endereço exato e um ponto de referência da lâmpada queimada."
        )
        registrar_no_banco("ODS 7 - Iluminação Pública")
        
    # 2. Fluxo Lógico: Opção 2 - Vazamento de Água / Saneamento (ODS 6)
    elif mensagem_usuario == "2":
        resposta_bot = (
            "Você selecionou: Vazamento de Água / Saneamento (ODS 6).\n"
            "Por favor, informe a localização e uma breve descrição do vazamento observado."
        )
        registrar_no_banco("ODS 6 - Vazamento / Saneamento")
        
    # 3. Fluxo Lógico: Finalização do contato
    elif mensagem_usuario.lower() in ['fim', 'obrigado', 'obrigada', 'encerrar']:
        resposta_bot = "Atendimento concluído. O Monitor de Recursos agradece seu relato!"
        
    # 4. Fluxo Lógico: Menu Inicial (Qualquer outro texto digitado)
    else:
        resposta_bot = (
            "Olá! Bem-vindo ao Zap da Vila - Monitor de Recursos Urbanos.\n"
            "Para reportar um problema no bairro, digite apenas o número da opção:\n\n"
            "1 - Relatar lâmpada queimada / falta de iluminação (ODS 7)\n"
            "2 - Relatar vazamento de água ou esgoto na via (ODS 6)"
        )
        
    # Retorna o JSON estruturado com a resposta do bot
    return jsonify({
        "status": "sucesso",
        "resposta": resposta_bot
    })

def registrar_no_banco(categoria_ods):
    """Função interna para simular a persistência de dados e logs."""
    novo_log = {
        "id_protocolo": len(logs_atendimento) + 1,
        "data_hora": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "categoria": categoria_ods,
        "status": "Aguardando detalhamento técnico"
    }
    logs_atendimento.append(novo_log)
    print(f"\n[BANCO DE DADOS] Novo log registrado com sucesso: {novo_log}\n")

if __name__ == '__main__':
    print("==================================================")
    print(" Servidor do 'Zap da Vila' Iniciado com Sucesso! ")
    print(" Executando árvore de decisão local em Flask...    ")
    print("==================================================")
    # Roda o servidor local na porta 5000
    app.run(port=5000, debug=True)