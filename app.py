import streamlit as st
import time
import cloudscraper
from bs4 import BeautifulSoup

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="BAC BO REAL-TIME", layout="wide")

# Estilização Visual - CORRIGIDO: unsafe_allow_html
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] { background-color: #050505; color: white; }
    .stMetric { background-color: #111; border: 1px solid #333; padding: 15px; border-radius: 15px; }
    .card-sinal {
        background: #1e293b; padding: 30px; border-radius: 20px;
        border: 2px solid #3b82f6; text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# --- INICIALIZAÇÃO DO PLACAR ---
if 'wins' not in st.session_state: st.session_state.wins = 0
if 'losses' not in st.session_state: st.session_state.losses = 0
if 'active_signal' not in st.session_state: st.session_state.active_signal = None

# --- FUNÇÃO PARA PEGAR DADOS ---
def get_data():
    try:
        scraper = cloudscraper.create_scraper()
        url = "https://tracksino.com/bacbo"
        res = scraper.get(url, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        balls = soup.find_all('div', class_='history-ball')
        return [b.text.strip()[0] for b in balls[:10]]
    except:
        return ["?", "?", "?"]

# --- LÓGICA ---
def analyze():
    data = get_data()
    if len(data) >= 3:
        last_3 = data[:3]
        if last_3 == ['P', 'P', 'P']:
            st.session_state.active_signal = "BANQUEIRO 🔴"
        elif last_3 == ['B', 'B', 'B']:
            st.session_state.active_signal = "JOGADOR 🔵"
        else:
            st.session_state.active_signal = None

# --- INTERFACE ---
st.markdown("<h1 style='text-align: center; color: #3b82f6;'>🤖 BAC BO ULTRA-BOT</h1>", unsafe_allow_html=True)

# Placar
c1, c2, c3 = st.columns(3)
c1.metric("Placar ✅", st.session_state.wins)
c2.metric("Placar ❌", st.session_state.losses)
c3.metric("Status", "LIVE")

st.divider()

# Área do Sinal
analyze()

if st.session_state.active_signal:
    st.markdown(f"""
    <div class="card-sinal">
        <h2 style='color: #3b82f6;'>🎯 SINAL CONFIRMADO</h2>
        <h1 style='font-size: 50px;'>APOSTAR NO: {st.session_state.active_signal}</h1>
        <p>⚠️ Proteção: EMPATE (TIE)</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_w, col_l = st.columns(2)
    if col_w.button("✅ GREEN"):
        st.session_state.wins += 1
        st.session_state.active_signal = None
        st.rerun()
    if col_l.button("❌ LOSS"):
        st.session_state.losses += 1
        st.session_state.active_signal = None
        st.rerun()
else:
    st.markdown("<h3 style='text-align: center; color: #666;'>🔎 Analisando mesa em tempo real...</h3>", unsafe_allow_html=True)

# Histórico Visual
st.divider()
dados_reais = get_data()
st.write("Últimos resultados da mesa: " + " | ".join(dados_reais))

# Refresh automático
time.sleep(12)
st.rerun()
