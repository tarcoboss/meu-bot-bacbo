import streamlit as st
import time
import cloudscraper
import re
import random

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="BAC BO PREDICTOR AI - tarcoboss", layout="wide")

# --- DESIGN CSS EVOLUTION GAMING UI ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700;900&display=swap');
    [data-testid="stAppViewContainer"] { background: radial-gradient(circle, #1a1a1a 0%, #000000 100%); color: white; font-family: 'Roboto', sans-serif; }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }

    /* Painel de Apostas */
    .bet-container { display: flex; justify-content: center; align-items: center; gap: 10px; margin-top: 20px; }
    .bet-card {
        width: 260px; height: 160px; border-radius: 15px;
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        font-weight: 900; font-size: 22px; position: relative; border: 2px solid rgba(255,255,255,0.1);
        transition: all 0.4s ease-in-out;
    }
    .jogador { background: linear-gradient(180deg, #0044cc 0%, #002266 100%); }
    .banca { background: linear-gradient(180deg, #cc0033 0%, #66001a 100%); }
    .empate {
        width: 160px; height: 160px; background: radial-gradient(circle, #cc9933 0%, #664411 100%);
        border-radius: 50%; border: 3px solid #ffcc66;
        display: flex; flex-direction: column; align-items: center; justify-content: center; font-size: 16px;
    }

    /* Efeito de Prediction (Piscando) */
    @keyframes prediction-glow {
        0% { box-shadow: 0 0 5px #fff; border-color: #fff; transform: scale(1); }
        50% { box-shadow: 0 0 50px #fff; border-color: #fff; transform: scale(1.05); }
        100% { box-shadow: 0 0 5px #fff; border-color: #fff; transform: scale(1); }
    }
    .active-prediction { animation: prediction-glow 0.6s infinite !important; z-index: 100; border: 4px solid #fff !important; }

    /* Bead Road */
    .road-container {
        background: #f0f0f0; border-radius: 8px; padding: 10px;
        display: grid; grid-template-columns: repeat(20, 1fr); grid-template-rows: repeat(6, 1fr);
        gap: 3px; width: fit-content; margin: 20px auto; border: 1px solid #444;
    }
    .bead { width: 22px; height: 22px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: bold; color: white; }
    .bead-P { background-color: #0044cc; }
    .bead-B { background-color: #cc0033; }
    .bead-T { background-color: #cc9933; position: relative; border: 1px solid #fff; }

    .confidence-meter { text-align: center; font-size: 14px; color: #00ff00; margin-top: 10px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- MOTOR DE INTELIGÊNCIA ---
if 'wins' not in st.session_state: st.session_state.wins = 0
if 'losses' not in st.session_state: st.session_state.losses = 0

def fetch_data():
    try:
        scraper = cloudscraper.create_scraper()
        res = scraper.get("https://www.trackcasino.com/bacbo", timeout=10).text
        found = re.findall(r'>(P|B|T)<', res)
        return found if found else ["P", "B", "T", "P"]
    except:
        return ["P", "B", "P", "B"]

def analyze_prediction(history):
    if len(history) < 5: return None, 0
    
    score_p = 0
    score_b = 0
    last_5 = history[:5]
    
    # 1. Estratégia Anti-Clump (Quebra de 3)
    if history[:3] == ['P', 'P', 'P']: score_b += 3
    if history[:3] == ['B', 'B', 'B']: score_p += 3
    
    # 2. Estratégia Dragon (Tendência Forte)
    if history[:5] == ['B', 'B', 'B', 'B', 'B']: score_b += 4
    if history[:5] == ['P', 'P', 'P', 'P', 'P']: score_p += 4
    
    # 3. Estratégia Ping-Pong
    if history[:4] == ['P', 'B', 'P', 'B']: score_p += 3
    if history[:4] == ['B', 'P', 'B', 'P']: score_b += 3
    
    # 4. Decisão Final
    if score_p > score_b and score_p >= 3: return "P", min(score_p * 10, 98)
    if score_b > score_p and score_b >= 3: return "B", min(score_b * 10, 98)
    return None, 0

# --- EXECUÇÃO ---
history = fetch_data()
pred, confidence = analyze_prediction(history)

# --- INTERFACE ---
st.markdown(f"<h1 style='text-align: center; color: #fff; font-size: 1.5rem;'>BAC BO PREDICTOR AI - tarcoboss</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #00ff00; font-size: 0.8rem;'>PLACAR: {st.session_state.wins} ✅ | {st.session_state.losses} ❌</p>", unsafe_allow_html=True)

# Painel de Apostas
p_class = "active-prediction" if pred == "P" else ""
b_class = "active-prediction" if pred == "B" else ""

st.markdown(f"""
<div class="bet-container">
    <div class="bet-card jogador {p_class}">JOGADOR<br><span style="font-size:12px">1:1</span></div>
    <div class="empate">EMPATE<br><span style="font-size:12px">88:1</span></div>
    <div class="bet-card banca {b_class}">BANCA<br><span style="font-size:12px">1:1</span></div>
</div>
""", unsafe_allow_html=True)

if pred:
    st.markdown(f"<div class='confidence-meter'>PREDIÇÃO: ENTRAR EM { 'JOGADOR' if pred=='P' else 'BANCA' } ({confidence}% DE CONFIANÇA)</div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #ffaa00;'>🛡️ PROTEGER EMPATE (OBRIGATÓRIO)</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    if col1.button("✅ GREEN"):
        st.session_state.wins += 1
        st.rerun()
    if col2.button("❌ LOSS"):
        st.session_state.losses += 1
        st.rerun()
else:
    st.markdown("<p style='text-align: center; color: #444; margin-top: 15px;'>🔎 AGUARDANDO PADRÃO DE ALTA ASSERTIVIDADE...</p>", unsafe_allow_html=True)

# BEAD ROAD
st.markdown("<div class='road-container'>", unsafe_allow_html=True)
road_html = "".join([f'<div class="bead bead-{r}">{r}</div>' for r in history[:120]])
st.markdown(road_html + "</div>", unsafe_allow_html=True)

# Refresh
time.sleep(10)
st.rerun()
