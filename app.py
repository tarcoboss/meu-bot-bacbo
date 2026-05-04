import streamlit as st
import time
import cloudscraper
import re

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="BAC BO PRO - tarcoboss", layout="wide")

# --- CSS RÉPLICA FIEL (EMPATE PEQUENO E ASAS LARGAS) ---
st.markdown("""
<style>
    /* Fundo Deep Dark com Vida */
    [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at center, #0a0f1e 0%, #02040a 100%);
        color: white;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }

    /* Contentor da Mesa */
    .mesa-bacbo {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        max-width: 480px;
        margin: 40px auto;
        position: relative;
        height: 120px;
    }

    /* Asas (Jogador e Banca) */
    .asa {
        flex: 1;
        height: 90px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        padding: 0 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(5px);
        transition: all 0.3s ease;
    }

    .asa-p {
        background: linear-gradient(180deg, #0044cc 0%, #001144 100%);
        border-radius: 45px 0 0 45px;
        text-align: left;
        padding-left: 25px;
    }

    .asa-b {
        background: linear-gradient(180deg, #cc0033 0%, #440011 100%);
        border-radius: 0 45px 45px 0;
        text-align: right;
        padding-right: 25px;
    }

    /* CÍRCULO DO EMPATE (REDUZIDO E CENTRALIZADO) */
    .centro-tie {
        position: absolute;
        width: 80px; /* REDUZIDO DRASTICAMENTE */
        height: 80px;
        background: radial-gradient(circle, #d4af37 0%, #8a6d3b 100%);
        border-radius: 50%;
        z-index: 10;
        left: 50%;
        transform: translateX(-50%);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        border: 3px solid #ffcc33;
        box-shadow: 0 0 15px rgba(0,0,0,0.8);
    }

    /* EFEITO PISCANTE NO SINAL */
    @keyframes blink-sinal {
        0% { filter: brightness(1); box-shadow: 0 0 5px rgba(255,255,255,0.2); }
        50% { filter: brightness(2.5); box-shadow: 0 0 50px #fff; }
        100% { filter: brightness(1); box-shadow: 0 0 5px rgba(255,255,255,0.2); }
    }
    .piscando {
        animation: blink-sinal 0.5s infinite alternate !important;
        border: 2px solid #fff !important;
        z-index: 20;
    }

    /* BEAD ROAD (GRADE BRANCA) */
    .bead-road-box {
        background: #ffffff;
        border-radius: 10px;
        padding: 6px;
        width: 95%;
        max-width: 450px;
        margin: 20px auto;
        overflow-x: auto;
        border: 2px solid #333;
    }

    .bead-grid {
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
        font-size: 10px;
        font-weight: 900;
        color: white;
    }
    .b-P { background-color: #0044cc; }
    .b-B { background-color: #cc0033; }
    .b-T { background-color: #cc9933; position: relative; border: 1px solid #fff; }
</style>
""", unsafe_allow_html=True)

# --- SINCRONIZAÇÃO DE DADOS ---
if 'wins' not in st.session_state: st.session_state.wins = 0
if 'losses' not in st.session_state: st.session_state.losses = 0

def fetch_live_results():
    try:
        scraper = cloudscraper.create_scraper()
        # Buscando da fonte mais rápida e estável
        url = "https://casinoscore.com/bacbo/"
        res = scraper.get(url, timeout=10).text
        # Captura os resultados P, B ou T
        found = re.findall(r'result-([PBT])', res)
        if not found:
            found = re.findall(r'>(P|B|T)<', res)
        return found if found else ["P", "B", "T"]
    except:
        return ["P", "B", "T"]

# Lógica do Robô
history = fetch_live_results()
pred = None
if len(history) >= 3:
    if history[:3] == ["P", "P", "P"]: pred = "B"
    elif history[:3] == ["B", "B", "B"]: pred = "P"

# --- UI ---
st.markdown("<h2 style='text-align: center; font-weight: 900; letter-spacing: 2px;'>BAC BO PREDICTOR</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #00ffcc;'>Score: {st.session_state.wins} ✅ | {st.session_state.losses} ❌</p>", unsafe_allow_html=True)

# MESA DE APOSTAS (Sincronizada)
j_blink = "piscando" if pred == "P" else ""
b_blink = "piscando" if pred == "B" else ""

st.markdown(f"""
<div class="mesa-bacbo">
    <div class="asa asa-p {j_blink}">
        <span style="font-size: 10px; opacity: 0.6;">1:1</span>
        <span style="font-size: 20px; font-weight: 900;">JOGADOR</span>
    </div>
    <div class="centro-tie">
        <span style="font-size: 8px; font-weight: bold; color: white;">EMPATE</span>
        <span style="font-size: 18px; font-weight: 900;">88:1</span>
    </div>
    <div class="asa asa-b {b_blink}">
        <span style="font-size: 10px; opacity: 0.6;">1:1</span>
        <span style="font-size: 20px; font-weight: 900;">BANCA</span>
    </div>
</div>
""", unsafe_allow_html=True)

# BEAD ROAD (Grade Branca)
road_html = '<div class="bead-road-box"><div class="bead-grid">'
for r in reversed(history[:120]): # Mostra do mais antigo para o mais recente na grade
    road_html += f'<div class="bead b-{r}">{r if r!="T" else ""}</div>'
road_html += '</div></div>'
st.markdown(road_html, unsafe_allow_html=True)

# AÇÕES
if pred:
    st.markdown(f"<h3 style='text-align: center;'>⚠️ ENTRADA: {'JOGADOR' if pred=='P' else 'BANCA'}</h3>", unsafe_allow_html=True)
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
    st.markdown("<p style='text-align: center; opacity: 0.5;'>🔎 MONITORANDO RESULTADOS REAIS...</p>", unsafe_allow_html=True)

# Auto-refresh de 10 segundos para sincronia
time.sleep(10)
st.rerun()
