# Zap da Vila - Monitor de Recursos Urbanos

> **Atividade Extensionista (2026)**
> **Instituição:** (UFBRA)  
> **Curso:** Ciência da Computação (5º Semestre)

O **Zap da Vila** é um protótipo de chatbot para backend focado em zeladoria urbana e engajamento comunitário. O objetivo principal do projeto é oferecer um canal simplificado e acessível para que moradores de bairros periféricos possam reportar problemas estruturais diretamente pelo celular, alinhando a gestão pública local às metas de desenvolvimento sustentável da ONU.

---

## 🎯 Objetivos de Desenvolvimento Sustentável (ODS) Atendidos

O ecossistema do chatbot foi desenhado com uma árvore de decisão estritamente focada em monitoramento de recursos essenciais:

* **🚰 ODS 6 (Água Potável e Saneamento):** Canal direcionado para o relato de vazamentos de água encanada, problemas na rede de esgoto na via pública e desperdício de recursos hidráulicos.
* **💡 ODS 7 (Energia Limpa e Acessível):** Canal voltado para a eficiência energética urbana, permitindo o mapeamento de lâmpadas queimadas ou trechos com falha na iluminação pública.

---

## 🛠️ Tecnologias e Dependências

O projeto utiliza tecnologias consolidadas no ecossistema de desenvolvimento web/backend em Python e persistência distribuída:

* **Python (v3.14+):** Linguagem interpretada base do ecossistema.
* **Flask (v3.0.3):** Microframework ágil para a criação e exposição das rotas da API/Webhook.
* **MongoDB Atlas:** Banco de dados NoSQL baseado em nuvem (hospedado na AWS - Região sa-east-1 / São Paulo) para armazenamento seguro de chamados em tempo real.
* **PyMongo:** Driver oficial do MongoDB para conexão, manipulação e persistência de dados em Python.
* **Requests (v2.32.3):** Biblioteca para envio, consumo e manipulação de requisições HTTP de forma simplificada.

---

## 📂 Estrutura de Arquivos

```text
Zap_da_Vila-Monitor_de_Recursos/
├── app.py               # Código-fonte principal (Lógica Flask, estados de usuários e conexão MongoDB Atlas)
├── requirements.txt     # Listagem oficial de dependências do projeto (incluindo pymongo)
└── README.md            # Documentação técnica do repositório
🚀 Como Executar o Projeto Localmente
1. Clonar o Repositório
Bash
git clone [https://github.com/RafaelTSa/Zap_da_Vila-Monitor_de_Recursos.git](https://github.com/RafaelTSa/Zap_da_Vila-Monitor_de_Recursos.git)
cd Zap_da_Vila-Monitor_de_Recursos

2. Instalar as Dependências
Utilizando o gerenciador de pacotes do Python, instale as bibliotecas necessárias declaradas no arquivo de requisitos:

Bash
python -m pip install -r requirements.txt
3. Iniciar o Servidor Flask
Execute o arquivo principal para levantar o servidor de desenvolvimento local (por padrão na porta 5000):

Bash
python app.py
🧪 Como Testar as Rotas (Webhook e Persistência)
O backend expõe um endpoint do tipo POST na rota /webhook. O sistema gerencia o estado da conversa baseando-se no identificador único do usuário (usuario_id). Para simular o fluxo completo de atendimento e a gravação final do documento na nuvem do MongoDB Atlas, execute a sequência de comandos curl abaixo no terminal:

Passo A: Envio de Saudação (Abertura do Menu Inicial)
Bash
curl -X POST [http://127.0.0.1:5000/webhook](http://127.0.0.1:5000/webhook) -H "Content-Type: application/json" -d '{"mensagem": "Olá", "usuario_id": "rafael_teste"}'
Passo B: Seleção da Categoria (Escolha da Opção ODS)
Para reportar iluminação pública (ODS 7), selecione 1:

Bash
curl -X POST [http://127.0.0.1:5000/webhook](http://127.0.0.1:5000/webhook) -H "Content-Type: application/json" -d '{"mensagem": "1", "usuario_id": "rafael_teste"}'
Passo C: Envio da Localização (Gravação no MongoDB Atlas)
Ao enviar o endereço, o backend altera o status para "Aberto", calcula incrementalmente o número do protocolo e persiste o registro no cluster em nuvem:

Bash
curl -X POST [http://127.0.0.1:5000/webhook](http://127.0.0.1:5000/webhook) -H "Content-Type: application/json" -d '{"mensagem": "Rua das Oliveiras, número 450, próximo ao mercado", "usuario_id": "rafael_teste"}'
📈 Próximos Passos de Desenvolvimento
[x] Migrar a simulação de persistência em memória para um banco de dados relacional ou NoSQL estável (Concluído com MongoDB Atlas).

[ ] Criar uma rota administrativa ou painel visual (Dashboard de Gestão) para listar e alterar o status dos chamados coletados.

[ ] Integrar o Webhook à API oficial ou emulada do WhatsApp Business.

[ ] Adicionar camadas de variáveis de ambiente (.env) para proteger credenciais confidenciais de conexão (MONGO_URI).