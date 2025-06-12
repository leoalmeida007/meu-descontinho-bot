import requests
import json
from flask import Flask

app = Flask(__name__)

BOT_TOKEN = "8190307226:AAGQESFLL5HId2Spl_dRHYnGLWF3fBSxyBI"
CHAT_ID = "@meudescontinho"

def carregar_ofertas(caminho='ofertas-amazon.json'):
    try:
        with open(caminho, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def enviar_mensagem_telegram(mensagem):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensagem, "parse_mode": "HTML"}
    response = requests.post(url, json=payload)
    return response

@app.route("/")
def home():
    return "✅ Servidor do bot do Meu Descontinho está rodando!"

@app.route("/enviar-ofertas")
def enviar_ofertas():
    ofertas = carregar_ofertas()
    if not ofertas:
        return "ℹ️ Sem ofertas novas."

    enviadas = 0
    for oferta in ofertas:
        titulo = oferta.get("titulo", "Sem título")
        preco = oferta.get("preco", "Preço não informado")
        link = oferta.get("url", "#")
        loja = oferta.get("loja", "Amazon")
        imagem = oferta.get("imagem", "")

        mensagem = f"<b>{titulo}</b>\n"
        mensagem += f"🛒 <b>Loja:</b> {loja}\n💰 <b>Preço:</b> {preco}\n🔗 <a href='{link}'>Clique para aproveitar</a>"
        enviar_mensagem_telegram(mensagem)
        enviadas += 1

    return f"✅ {enviadas} ofertas enviadas!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)