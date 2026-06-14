from flask import Flask, request, jsonify
from pymongo import MongoClient
import datetime
# Importar o resolvedor de DNS para corrigir o bloqueio do roteador
import dns.resolver

app = Flask(__name__)
app.json.ensure_ascii = False

# --- AJUSTE DE DNS PARA EVITAR O ERRO 'REFUSED' ---
# Força o sistema a usar o DNS do Google (8.8.8.8) in vez do roteador local
dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ['8.8.8.8', '8.8.4.4']
# --------------------------------------------------

# --- CONFIGURAÇÃO DO MONGODB ATLAS ---
MONGO_URI = "mongodb+srv://texera09_db_user:lnee7DHq3gwCRKFG@zap-da-vila-cluster.fybtv2f.mongodb.net/?appName=Zap-da-vila-cluster"

client = MongoClient(MONGO_URI)

# Criando/Selecionando o Banco de Dados chamado 'zap_da_vila_db'
db = client['zap_da_vila_db']

# Criando/Selecionando a Coleção (tabela NoSQL) chamada 'chamados_moradores'
colecao_chamados = db['chamados_moradores']
# -------------------------------------

# Memória temporária para os passos da conversa (em qual menu o morador está)
estados_usuarios = {}

@app.route('/webhook', methods=['POST'])
def webhook():
    dados = request.get_json()
    mensagem = dados.get('mensagem', '').strip()
    usuario_id = dados.get('usuario_id', 'padrao')
    
    # Se o usuário for novo, começa no menu
    if usuario_id not in estados_usuarios:
        estados_usuarios[usuario_id] = {'passo': 'menu'}

    estado_atual = estados_usuarios[usuario_id]

    # --- FLUXO 1: USUÁRIO ESTÁ NO MENU INICIAL ---
    if estado_atual['passo'] == 'menu':
        if mensagem == '1':
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
        categoria = estado_atual['categoria']
        
        # Gerando o número do protocolo com base no total de documentos já salvos no banco
        total_documentos = colecao_chamados.count_documents({})
        novo_protocolo = total_documentos + 1
        
        # Estrutura do documento JSON que vai para a nuvem
        novo_chamado = {
            "id_protocolo": novo_protocolo,
            "usuario_id": usuario_id,
            "data_hora": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "categoria": categoria,
            "localizacao": mensagem,
            "status": "Aberto"
        }
        
        # ---- SALVANDO DE VERDADE NO MONGODB ATLAS ----
        resultado = colecao_chamados.insert_one(novo_chamado)
        print(f"\n[MONGODB ATLAS] Documento salvo com sucesso! ID: {resultado.inserted_id}\n")
        # ----------------------------------------------
        
        # Limpa o estado da memória para permitir nova conversa
        del estados_usuarios[usuario_id]
        
        resposta_final = (
            f"Obrigado! Seu relato sobre '{categoria}' foi registrado com sucesso na nuvem.\n"
            f"📍 Local informado: {mensagem}\n"
            f"🔢 Número do seu Protocolo: {novo_protocolo}\n"
            f"Nossa equipe de zeladoria comunitária já foi notificada!"
        )
        
        return jsonify({
            "resposta": resposta_final,
            "status": "sucesso"
        })

if __name__ == '__main__':
    app.run(debug=True)