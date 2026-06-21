from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
import datetime
import certifi
import os
# Importa o carregador do arquivo .env
from dotenv import load_dotenv

# Carrega as variáveis contidas no arquivo .env local
load_dotenv()

# =====================================================
# CONFIGURAÇÃO FLASK
# =====================================================

app = Flask(__name__)
app.json.ensure_ascii = False

# =====================================================
# CONFIGURAÇÃO MONGODB ATLAS
# =====================================================

# Puxa a string de conexão direto da memória da máquina.
MONGO_URI = os.getenv("MONGO_URI")

try:
    client = MongoClient(
        MONGO_URI,
        tls=True,
        tlsCAFile=certifi.where(),
        serverSelectionTimeoutMS=5000
    )

    # TESTA CONEXÃO
    client.admin.command('ping')

    print("\n====================================")
    print("MongoDB Atlas conectado com sucesso!")
    print("====================================\n")

    db = client['zap_da_vila_db']
    colecao_chamados = db['chamados_moradores']

except Exception as e:
    print("\n====================================")
    print("ERRO AO CONECTAR NO MONGODB ATLAS:")
    print(e)
    print("====================================\n")
    client = None
    db = None
    colecao_chamados = None

# =====================================================
# CONTROLE DE ESTADO DOS USUÁRIOS
# =====================================================
estados_usuarios = {}

# =====================================================
# WEBHOOK (COM TRATAMENTO DE ERROS E CANCELAMENTO)
# =====================================================
@app.route('/webhook', methods=['POST'])
def webhook():
    dados = request.get_json()
    mensagem = dados.get('mensagem', '').strip()
    usuario_id = dados.get('usuario_id', 'padrao')

    # Se o usuário digitar 'sair' ou '0' em qualquer momento, limpa o estado dele
    if mensagem.lower() in ['sair', '0', 'cancelar']:
        if usuario_id in estados_usuarios:
            del estados_usuarios[usuario_id]
        return jsonify({
            "resposta": "Atendimento cancelado com sucesso. Quando precisar, basta enviar um 'Olá' para iniciar novamente!",
            "status": "sucesso"
        })

    if usuario_id not in estados_usuarios:
        estados_usuarios[usuario_id] = {'passo': 'menu'}

    estado_atual = estados_usuarios[usuario_id]

    if estado_atual['passo'] == 'menu':
        if mensagem == '1':
            estados_usuarios[usuario_id] = {
                'passo': 'aguardando_endereco',
                'categoria': 'ODS 7 - Iluminação Pública'
            }
            return jsonify({
                "resposta": (
                    "Você selecionou: Iluminação Pública (ODS 7).\n\n"
                    "Por favor, digite o endereço exato do problema e um ponto de referência.\n"
                    "*(Se quiser cancelar, digite 0 a qualquer momento)*"
                ),
                "status": "sucesso"
            })

        elif mensagem == '2':
            estados_usuarios[usuario_id] = {
                'passo': 'aguardando_endereco',
                'categoria': 'ODS 6 - Vazamento / Saneamento'
            }
            return jsonify({
                "resposta": (
                    "Você selecionou: Vazamento / Saneamento (ODS 6).\n\n"
                    "Por favor, informe a localização aproximada e uma breve descrição do problema.\n"
                    "*(Se quiser cancelar, digite 0 a qualquer momento)*"
                ),
                "status": "sucesso"
            })
            
        # TRATAMENTO DE ERRO: Se digitar qualquer coisa diferente de 1 ou 2 no menu principal
        else:
            return jsonify({
                "resposta": (
                    "⚠️ Opção inválida!\n\n"
                    "Por favor, escolha uma opção respondendo apenas com o número:\n"
                    "1 - Relatar lâmpada queimada (ODS 7)\n"
                    "2 - Rel