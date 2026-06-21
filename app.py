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
                    "2 - Relatar vazamento de água/esgoto (ODS 6)"
                ),
                "status": "sucesso"
            })

    elif estado_atual['passo'] == 'aguardando_endereco':
        if colecao_chamados is None:
            return jsonify({
                "resposta": "Erro: O banco de dados está indisponível no momento.",
                "status": "erro"
            })

        # Validação simples de endereço muito curto
        if len(mensagem) < 5:
            return jsonify({
                "resposta": (
                    "⚠️ O endereço informado parece muito curto.\n"
                    "Por favor, digite o nome da rua e o número para que a equipe possa localizar o problema."
                ),
                "status": "sucesso"
            })

        categoria = estado_atual['categoria']

        try:
            total_documentos = colecao_chamados.count_documents({})
            novo_protocolo = total_documentos + 1

            novo_chamado = {
                "id_protocolo": novo_protocolo,
                "usuario_id": usuario_id,
                "data_hora": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "categoria": categoria,
                "localizacao": mensagem,
                "status": "Aberto"
            }

            resultado = colecao_chamados.insert_one(novo_chamado)

            print("\n====================================")
            print("DOCUMENTO SALVO NO MONGODB!")
            print(f"ID: {resultado.inserted_id}")
            print("====================================\n")

            del estados_usuarios[usuario_id]

            resposta_final = (
                f"✅ Obrigado! Seu relato foi registrado com sucesso.\n\n"
                f"📋 Protocolo: #{novo_protocolo}\n"
                f"📍 Categoria: {categoria}\n"
                f"🏠 Local: {mensagem}\n\n"
                f"Nossa equipe de zeladoria comunitária já recebeu o alerta!"
            )

            return jsonify({
                "resposta": resposta_final,
                "status": "sucesso"
            })

        except Exception as e:
            print(f"ERRO AO SALVAR DOCUMENTO: {e}")
            return jsonify({
                "resposta": "Erro ao salvar chamado no MongoDB.",
                "status": "erro"
            })
        
# =====================================================
# PAINEL ADMINISTRATIVO
# =====================================================
@app.route('/admin', methods=['GET'])
def admin_dashboard():
    if colecao_chamados is None:
        return """
        <h1>Erro de conexão com MongoDB Atlas</h1>
        <p>Verifique a URI, senha e Network Access.</p>
        """
    try:
        chamados_do_banco = list(
            colecao_chamados.find().sort("id_protocolo", -1)
        )
        return render_template(
            'admin.html',
            chamados=chamados_do_banco
        )
    except Exception as e:
        return f"<h1>Erro ao buscar dados do MongoDB</h1><pre>{e}</pre>"

# =====================================================
# ROTA DE TESTE
# =====================================================
@app.route('/teste')
def teste():
    if colecao_chamados is None:
        return "<h1>Banco de dados indisponível</h1>"

    teste_doc = {
        "id_protocolo": 999,
        "usuario_id": "teste",
        "data_hora": "2026-06-15",
        "categoria": "Teste",
        "localizacao": "Rua Teste",
        "status": "Aberto"
    }
    try:
        resultado = colecao_chamados.insert_one(teste_doc)
        return f"<h1>Documento inserido!</h1><p>ID: {resultado.inserted_id}</p>"
    except Exception as e:
        return f"<h1>Erro ao inserir documento</h1><pre>{e}</pre>"

# =====================================================
# ROTA PARA ATUALIZAR STATUS DO CHAMADO
# =====================================================
@app.route('/admin/atualizar_status/<int:id_protocolo>', methods=['POST'])
def atualizar_status(id_protocolo):
    if colecao_chamados is None:
        return "Banco de dados indisponível", 500

    # Pega o novo status vindo do botão do painel
    novo_status = request.form.get('novo_status')

    try:
        # Atualiza o documento baseado no id_protocolo numérico
        colecao_chamados.update_one(
            {"id_protocolo": id_protocolo},
            {"$set": {"status": novo_status}}
        )
        print(f"\n[MONGODB] Protocolo #{id_protocolo} atualizado para {novo_status}!\n")
        
        # Redireciona de volta para o painel atualizado
        from flask import redirect, url_for
        return redirect(url_for('admin_dashboard'))
        
    except Exception as e:
        print(f"Erro ao atualizar status: {e}")
        return f"Erro ao atualizar: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)