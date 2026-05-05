import requests
import hashlib
import json
import time
import pytz
import os
from datetime import datetime
from Crypto.Cipher import AES
from flask import Flask
from threading import Thread

# --- SERVIDOR WEB PARA O RENDER ---
app = Flask('')

@app.route('/')
def home():
    return "Big Boss Online"

def run_web():
    # O Render fornece a porta na variável de ambiente PORT
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- CONFIGURAÇÕES DO BOSS ---
API_KEY = "bcf9516418d71b89256137381b1169ea98ec4bdd4684ea8b2c33f818d7b5af8e"
TOKEN = "8338485800:AAGarC1l4CZBfS68lPIMntpu4e2l8v63Las"
CHAT_ID = "-1003990778863"
AFF_LINK = "https://tracker.afiliado.com/visit/?bta=35222&nci=5432&afid=p6104p6845p4b2d"

WINS = {'Direto': 0, 'G1': 0, 'G2': 0}
LOSSES = 0
STREAK = 0 
ANALYZING_MSG_ID = None
LAST_SIGNAL_TIME = 0 

def decrypt_engine(encrypted_data):
    try:
        key_hash = hashlib.sha256(API_KEY.encode()).digest()
        iv = encrypted_data[:12]; tag = encrypted_data[-16:]; ciphertext = encrypted_data[12:-16]
        cipher = AES.new(key_hash, AES.MODE_GCM, iv)
        return json.loads(cipher.decrypt_and_verify(ciphertext, tag).decode('utf-8'))
    except: return None

def enviar_msg(texto, reply_markup=None):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": texto, "parse_mode": "Markdown", "disable_web_page_preview": True}
    if reply_markup: payload["reply_markup"] = json.dumps(reply_markup)
    try:
        r = requests.post(url, data=payload)
        return r.json().get('result', {}).get('message_id')
    except: return None

def deletar_msg(msg_id):
    if msg_id: requests.post(f"https://api.telegram.org/bot{TOKEN}/deleteMessage", data={"chat_id": CHAT_ID, "message_id": msg_id})

def get_placar_boss():
    total = sum(WINS.values())
    return f"🤵‍♂️ **RELATÓRIO DO BOSS**\n✅ Lucros: {total} | ❌ Erros: {LOSSES}\n🔥 **STREAK: {STREAK}**"

def boss_engine():
    global ANALYZING_MSG_ID, LOSSES, STREAK, LAST_SIGNAL_TIME
    print("Iniciando Engine...")
    while True:
        try:
            tz = pytz.timezone('Europe/Lisbon')
            agora = datetime.now(tz)
            if agora.hour == 0 and agora.minute == 0:
                WINS.update({'Direto': 0, 'G1': 0, 'G2': 0}); LOSSES = 0; STREAK = 0
                enviar_msg("🎩 **NOVO DIA OPERACIONAL**\nO Boss resetou o placar. Vamos faturar! 🚀")
                time.sleep(60)

            if time.time() - LAST_SIGNAL_TIME < 160:
                if ANALYZING_MSG_ID is None:
                    ANALYZING_MSG_ID = enviar_msg("📡 **BIG BOSS MONITORANDO...**\n\n🤵‍♂️ *O Chefe está analisando o mercado.*")
                time.sleep(20); continue

            res = requests.get("https://betmind.org/api/results?game=bacbo&limit=10", headers={"X-API-Key": API_KEY})
            dados = decrypt_engine(res.json().get('e'))
            if not dados: continue

            historico = [r['result'] for r in dados[:4]]
            entrada = None
            if historico == ['P', 'P', 'P', 'P']: entrada = "BANKER (Vermelho)"
            if historico == ['B', 'B', 'B', 'B']: entrada = "PLAYER (Azul)"
            
            if entrada:
                deletar_msg(ANALYZING_MSG_ID); ANALYZING_MSG_ID = None
                msg_sinal = (f"🎩 **BIG BOSS - ORDEM DE ENTRADA**\n\n🎯 **APOSTAR NO: {entrada}**\n🟡 **COBERTURA NO EMPATE**\n\n🔄 Até Gale 2")
                btn = {"inline_keyboard": [[{"text": "🏢 ENTRAR NA MESA", "url": AFF_LINK}]]}
                sinal_id = enviar_msg(msg_sinal, reply_markup=btn)

                venceu = False
                for g in range(3):
                    time.sleep(45)
                    check = decrypt_engine(requests.get("https://betmind.org/api/results?game=bacbo&limit=1", headers={"X-API-Key": API_KEY}).json().get('e'))[0]
                    cor_venceu = "PLAYER (Azul)" if check['result'] == 'P' else "BANKER (Vermelho)"
                    if cor_venceu == entrada or check['result'] == 'T':
                        venceu = True; STREAK += 1
                        if g == 0: WINS['Direto'] += 1
                        elif g == 1: WINS['G1'] += 1
                        else: WINS['G2'] += 1
                        deletar_msg(sinal_id)
                        enviar_msg(f"✅ **LUCRO NO BOLSO!**\n\n{get_placar_boss()}\n🤵‍♂️ *O Boss mandou, a mesa pagou.*")
                        break
                
                if not venceu:
                    LOSSES += 1; STREAK = 0
                    deletar_msg(sinal_id)
                    enviar_msg(f"❌ **RED**\n\n{get_placar_boss()}")
                
                LAST_SIGNAL_TIME = time.time()
            time.sleep(20)
        except Exception as e: 
            print(f"Erro: {e}")
            time.sleep(10)

if __name__ == "__main__":
    # Inicia o servidor web
    t = Thread(target=run_web)
    t.start()
    # Inicia o robô
    boss_engine()
