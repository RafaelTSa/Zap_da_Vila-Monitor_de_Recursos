# Zap da Vila - Monitor de Recursos Urbanos

> **Atividade Extensionista (2026)** > **Instituição:** (UFBRA)  
> **Curso:** Ciência da Computação (5º Semestre)

O **Zap da Vila** é um protótipo de chatbot para backend focado em zeladoria urbana e engajamento comunitário. O objetivo principal do projeto é oferecer um canal simplificado e acessível para que moradores de bairros periféricos possam reportar problemas estruturais diretamente pelo celular, alinhando a gestão pública local às metas de desenvolvimento sustentável da ONU.

---

## 🎯 Objetivos de Desenvolvimento Sustentável (ODS) Atendidos

O ecossistema do chatbot foi desenhado com uma árvore de decisão estritamente focada em monitoramento de recursos essenciais:

* **🚰 ODS 6 (Água Potável e Saneamento):** Canal direcionado para o relato de vazamentos de água encanada, problemas na rede de esgoto na via pública e desperdício de recursos hidráulicos.
* **💡 ODS 7 (Energia Limpa e Acessível):** Canal voltado para a eficiência energética urbana, permitindo o mapeamento de lâmpadas queimadas ou trechos com falha na iluminação pública.

---

## 🛠️ Tecnologias e Dependências

O projeto utiliza tecnologias consolidadas no ecossistema de desenvolvimento web/backend em Python:

* **Python (v3.14+):** Linguagem interpretada base do ecossistema.
* **Flask (v3.0.3):** Microframework ágil para a criação e exposição das rotas da API/Webhook.
* **Requests (v2.32.3):** Biblioteca para envio, consumo e manipulação de requisições HTTP de forma simplificada.

---

## 📂 Estrutura de Arquivos

```text
Zap_da_Vila-Monitor_de_Recursos/
├── app.py               # Código fonte principal (Lógica em Flask, rotas e árvore de decisão)
├── requirements.txt     # Listagem oficial de dependências do projeto
└── README.md            # Documentação técnica do repositório

🚀 Como Executar o Projeto Localmente
1. Clonar o Repositório
Bash
git clone [https://github.com/SEU_USUARIO/Zap_da_Vila-Monitor_de_Recursos.git](https://github.com/SEU_USUARIO/Zap_da_Vila-Monitor_de_Recursos.git)
cd Zap_da_Vila-Monitor_de_Recursos
2. Instalar as Dependências
Utilizando o gerenciador de pacotes do Python, instale as bibliotecas necessárias declaradas no arquivo de requisitos:

Bash
python -m pip install -r requirements.txt
3. Iniciar o Servidor Flask
Execute o arquivo principal para levantar o servidor de desenvolvimento local (por padrão na porta 5000):

Bash
python app.py
🧪 Como Testar as Rotas (Webhook)
O backend expõe um endpoint do tipo POST na rota /webhook. Você pode simular interações de usuários enviando requisições JSON por ferramentas como Postman, Insomnia ou diretamente via terminal utilizando o comando curl.

Teste do Menu Inicial
Bash
curl -X POST [http://127.0.0.1:5000/webhook](http://127.0.0.1:5000/webhook) -H "Content-Type: application/json" -d '{"mensagem": "Olá"}'
Teste de Relato de Iluminação Pública (ODS 7)
Bash
curl -X POST [http://127.0.0.1:5000/webhook](http://127.0.0.1:5000/webhook) -H "Content-Type: application/json" -d '{"mensagem": "1"}'
Teste de Relato de Saneamento/Vazamento (ODS 6)
Bash
curl -X POST [http://127.0.0.1:5000/webhook](http://127.0.0.1:5000/webhook) -H "Content-Type: application/json" -d '{"mensagem": "2"}'
📈 Próximos Passos de Desenvolvimento
[ ] Migrar a simulação de persistência em memória para um banco de dados relacional ou NoSQL estável.

[ ] Integrar o Webhook à API oficial ou emulada do WhatsApp Business.

[ ] Adicionar camadas de segurança e autenticação para os dados recebidos dos usuários