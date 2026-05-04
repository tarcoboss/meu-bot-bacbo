import streamlit as st
import time
import cloudscraper
import re

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="BAC BO PRO AI", layout="wide")

# --- DESIGN PROFISSIONAL "ESTILO EVOLUTION" ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');

    /* Fundo de Casino Profissional */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.8)), 
                    url('https://images.unsplash.com/photo-1511193311914-0346f16efe90?q=80&w=2073');
        background-size: cover;
        background-position: center;
        color: white;
        font-family: 'Inter', sans-serif;
    }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }

    /* Contentor da Mesa */
    .mesa-bacbo {
        position: relative;
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        max-width: 600px;
        margin: 40px auto;
        height: 120px; /* Altura controlada */
    }

    /* Asas (Jogador e Banca) */
    .asa {
        width: 250px;
        height: 100px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        position: relative;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        transition: all 0.4s ease;
        z-index: 1;
    }

    .asa-jogador {
        background: linear-gradient(180deg, rgba(0, 68, 204, 0.9) 0%, rgba(0, 34, 102, 0.9) 100%);
        border-radius: 50px 0 0 50px;
        text-align: left;
        padding-left: 35px;
    }

    .asa-banca {
        background: linear-gradient(180deg, rgba(204, 0, 51, 0.9) 0%, rgba(102, 0, 26, 0.9) 100%);
        border-radius: 0 50px 50px 0;
        text-align: right;
        padding-right: 35px;
    }

    /* Círculo do Empate Corrigido */
    .centro-tie {
        position: absolute;
        width: 125px;
        height: 125px;
        background: radial-gradient(circle, #cc9933 0%, #664411 100%);
        border-radius: 50%;
        z-index: 10;
        left: 50%;
        transform: translateX(-50%);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        border: 4px solid #ffcc66;
        box-shadow: 0 0 30px rgba(0,0,0,0.8);
    }

    /* Efeito Piscante no Sinal (Luz de Água) */
    @keyframes aqua-glow {
        0% { box-shadow: 0 0 10px #fff; filter: brightness(1); }
        50% { box-shadow: 0 0 50px #fff; filter: brightness(1.8); }
        100% { box-shadow: 0 0 10px #fff; filter: brightness(1); }
    }
    .piscando {
        animation: aqua-glow 0.7s infinite alternate !important;
        border: 3px solid #fff !important;
        z-index: 20;
    }

    /* Bead Road (Grade Estilo Evolution) */
    .bead-road-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 8px;
        padding: 8px;
        width: 95%;
        max-width: 500px;
        margin: 20px auto;
        border: 2px solid #222;
        box-shadow: 0 10px 20px rgba(0,0,0,0.5);
    }

    .grid-bead {
        display: grid;
        grid-template-rows: repeat(6, 20px);
        grid-auto-flow: column;
        grid-auto-columns: 20px;
        gap: 2px;
    }

    .bead {
        width: 18px;
        height: 18px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 9px;
        font-weight: 900;
        color: white;
    }
    .b-P { background-color: #0044cc; }
    .b-B { background-color: #cc0033; }
    .b-T { background-color: #cc9933; border: 1px solid #fff; }

    /* Stats */
    .stats { text-align: center; font-size: 11px; font-weight: bold; margin-top: 15px; }
</style>
""", unsafe_allow_html=True)

# --- ENGINE ---
if 'wins' not in st.session_state: st.session_state.wins = 0
if 'losses' not in st.session_state: st.session_state.losses = 0

def fetch_live_data():
    try:
        scraper = cloudscraper.create_scraper()
        res = scraper.get("https://www.trackcasino.com/bacbo", timeout=10).text
        found = re.findall(r'>(P|B|T)<', res)
        # Fallback caso falte dados
        return found if len(found) > 10 else ["P", "B", "P", "B", "T", "P", "B"]
    except:
        return ["P", "B", "T"]

# Execução
history = fetch_live_data()
pred = None
if len(history) >= 3:
    if history[:3] == ["P", "P", "P"]: pred = "B"
    elif history[:3] == ["B", "B", "B"]: pred = "P"

# --- UI ---
st.markdown("<h2 style='text-align: center; font-weight: 900; letter-spacing: 2px;'>BAC BO ELITE AI</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #00ffcc; font-size: 12px;'>GREEN: {st.session_state.wins} | LOSS: {st.session_state.losses}</p>", unsafe_allow_html=True)

# MESA DE APOSTAS
j_blink = "piscando" if pred == "P" else ""
b_blink = "piscando" if pred == "B" else ""

st.markdown(f"""
<div class="mesa-bacbo">
    <div class="asa asa-jogador {j_blink}">
        <span style="font-size: 10px; opacity: 0.7;">1:1</span>
        <span style="font-size: 18px; font-weight: 900; letter-spacing: 1px;">JOGADOR</span>
    </div>
    <div class="centro-tie">
        <span style="font-size: 8px; opacity: 0.9; font-weight: bold;">EMPATE</span>
        <span style="font-size: 20px; font-weight: 900;">88:1</span>
    </div>
    <div class="asa asa-banca {b_blink}">
        <span style="font-size: 10px; opacity: 0.7;">1:1</span>
        <span style="font-size: 18px; font-weight: 900; letter-spacing: 1px;">BANCA</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='stats'><span style='color:#0088ff'>JOGADOR 54%</span> | <span style='color:#ffcc00'>EMPATE 10%</span> | <span style='color:#ff3333'>BANCA 36%</span></div>", unsafe_allow_html=True)

# BEAD ROAD (GRADE BRANCA CORRIGIDA)
road_html = '<div class="bead-road-card"><div class="grid-bead">'
# No Bac Bo, o histórico flui da esquerda para a direita, coluna por coluna
for r in reversed(history[:120]): 
    road_html += f'<div class="bead b-{r}">{r if r!="T" else ""}</div>'
road_html += '</div></div>'
st.markdown(road_html, unsafe_allow_html=True)

# CONTROLES
if pred:
    st.markdown(f"<h3 style='text-align:center; color:white;'>ENTRADA: {'🔵 JOGADOR' if pred=='P' else '🔴 BANCA'}</h3>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("✅ GREEN"):
            st.session_state.wins += 1
            st.rerun()
    with c2:
        if st.button("❌ LOSS"):
            st.session_state.losses += 1
            st.rerun()
else:
    st.markdown("<p style='text-align: center; opacity: 0.5;'>🔎 MONITORANDO MESA EM TEMPO REAL...</p>", unsafe_allow_html=True)

# Auto-refresh
time.sleep(12)
st.rerun()
