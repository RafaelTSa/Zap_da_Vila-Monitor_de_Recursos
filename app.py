from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)
app.json.ensure_ascii = False

# Memória temporária para saber em qual passo o morador está
# Estrutura: {'id_do_usuario': {'passo': 'menu', 'categoria': '...'} }
estados_usuarios = {}

# Simulação do banco de dados (enquanto não ligamos o MongoDB no próximo passo)
banco_simulado = []
contador_protocolo = 0

@app.route('/webhook', methods=['POST'])
def webhook():
    global contador_protocolo
    
    dados = request.get_json()
    # Pegamos a mensagem e o ID do usuário (se não vier ID, usamos 'padrao')
    mensagem = dados.get('mensagem', '').strip()
    usuario_id = dados.get('usuario_id', 'padrao')
    
    # Se o usuário for novo, ele começa no passo do 'menu'
    if usuario_id not in estados_usuarios:
        estados_usuarios[usuario_id] = {'passo': 'menu'}

    estado_atual = estados_usuarios[usuario_id]

    # --- FLUXO 1: USUÁRIO ESTÁ NO MENU INICIAL ---
    if estado_atual['passo'] == 'menu':
        if mensagem == '1':
            estado_current_step = 'aguardando_endereco'
            estados_usuarios[usuario_id] = {
                'passo': 'aguardando_endereco',
                'categoria': 'ODS 7 - Iluminação Pública'
            }
            return jsonify({
                "resposta": "Você selecionou: Iluminação Pública (ODS 7).\nPor favor, digite o endereço exato e um ponto de referência da lâmpada queimada.",
                "status": "sucesso"
            })
            
        elif mensagem == '2':
            estados_usuarios[usuario_id] = {
                'passo': 'aguardando_endereco',
                'categoria': 'ODS 6 - Vazamento / Saneamento'
            }
            return jsonify({
                "resposta": "Você selecionou: Vazamento de Água / Saneamento (ODS 6).\nPor favor, informe a localização e uma breve descrição do vazamento observado.",
                "status": "sucesso"
            })
            
        else:
            return jsonify({
                "resposta": "Olá! Bem-vindo ao Zap da Vila - Monitor de Recursos Urbanos.\nPara reportar um problema no bairro, digite apenas o número da opção:\n\n1 - Relatar lâmpada queimada / falta de iluminação (ODS 7)\n2 - Relatar vazamento de água ou esgoto na via (ODS 6)",
                "status": "sucesso"
            })

    # --- FLUXO 2: USUÁRIO ESTÁ ENVIANDO O ENDEREÇO ---
    elif estado_atual['passo'] == 'aguardando_endereco':
        contador_protocolo += 1
        categoria = estado_atual['categoria']
        
        # Estrutura JSON idêntica ao que salvaremos no MongoDB depois
        novo_chamado = {
            "id_protocolo": contador_protocolo,
            "data_hora": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "categoria": categoria,
            "localizacao": mensagem,
            "status": "Aberto"
        }
        
        # Guarda no nosso banco simulado por enquanto
        banco_simulado.append(novo_chamado)
        
        print(f"\n[BANCO DE DADOS SIMULADO] Novo documento JSON gerado:\n{novo_chamado}\n")
        
        # Reseta o estado do usuário para que ele possa começar de novo se mandar mensagem depois
        del estados_usuarios[usuario_id]
        
        resposta_final = (
            f"Obrigado! Seu relato sobre '{categoria}' foi registrado.\n"
            f"📍 Local informado: {mensagem}\n"
            f"🔢 Número do seu Protocolo: {contador_protocolo}\n"
            f"Nossa equipe de zeladoria comunitária já foi notificada!"
        )
        
        return jsonify({
            "resposta": resposta_final,
            "status": "sucesso"
        })

if __name__ == '__main__':
    app.run(debug=True)