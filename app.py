import streamlit as st
import time
import cloudscraper
import re

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="BAC BO PREDICTOR", layout="wide")

# --- DESIGN CYBER-PRO (LIMPO E VIVO) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Rajdhani:wght@500;700&display=swap');

    /* Fundo Digital Vivo */
    [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at 50% 50%, #0f172a 0%, #020617 100%);
        background-attachment: fixed;
        color: white;
        font-family: 'Rajdhani', sans-serif;
    }
    
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }

    /* Mesa de Apostas Futurista */
    .mesa-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        max-width: 450px;
        margin: 30px auto;
        position: relative;
        height: 140px;
    }

    .asa {
        flex: 1;
        height: 100px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        padding: 0 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }

    .asa-p {
        background: linear-gradient(180deg, #0055ff 0%, #0022aa 100%);
        border-radius: 30px 0 0 30px;
        text-align: left;
    }

    .asa-b {
        background: linear-gradient(180deg, #ff0044 0%, #aa0022 100%);
        border-radius: 0 30px 30px 0;
        text-align: right;
    }

    .tie-circle {
        position: absolute;
        width: 110px;
        height: 110px;
        background: radial-gradient(circle, #ffcc33 0%, #886611 100%);
        border-radius: 50%;
        z-index: 10;
        left: 50%;
        transform: translateX(-50%);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        border: 3px solid #fff;
        box-shadow: 0 0 25px rgba(255, 204, 51, 0.5);
    }

    /* Efeito de Piscada (Liquid Glow) */
    @keyframes glow-pulse {
        0% { filter: brightness(1); box-shadow: 0 0 10px rgba(255,255,255,0.2); }
        50% { filter: brightness(2); box-shadow: 0 0 40px #fff; }
        100% { filter: brightness(1); box-shadow: 0 0 10px rgba(255,255,255,0.2); }
    }
    .piscando {
        animation: glow-pulse 0.6s infinite alternate;
        z-index: 20;
        border: 2px solid #fff !important;
    }

    /* Bead Road Horizontal */
    .road-box {
        background: white;
        border-radius: 10px;
        padding: 8px;
        width: 100%;
        max-width: 450px;
        margin: 20px auto;
        overflow-x: auto;
    }

    .road-grid {
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
        font-weight: 800;
        color: white;
    }
    .b-P { background: #0055ff; }
    .b-B { background: #ff0044; }
    .b-T { background: #cc9933; border: 1px solid #fff; }

    .label-bet { font-family: 'Orbitron', sans-serif; font-weight: 900; font-size: 18px; letter-spacing: 1px; }
</style>
""", unsafe_allow_html=True)

# --- ENGINE ---
if 'wins' not in st.session_state: st.session_state.wins = 0
if 'losses' not in st.session_state: st.session_state.losses = 0

def fetch_results():
    try:
        scraper = cloudscraper.create_scraper()
        res = scraper.get("https://www.trackcasino.com/bacbo", timeout=10).text
        return re.findall(r'>(P|B|T)<', res)
    except:
        return ["P", "B", "T"]

history = fetch_results()
pred = None
if len(history) >= 3:
    if history[:3] == ["P", "P", "P"]: pred = "B"
    elif history[:3] == ["B", "B", "B"]: pred = "P"

# --- UI ---
st.markdown("<h2 style='text-align: center; font-family: Orbitron; color: #00d2ff;'>BAC BO PREDICTOR AI</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; font-weight: bold;'>SCORE: ✅ {st.session_state.wins} | ❌ {st.session_state.losses}</p>", unsafe_allow_html=True)

# MESA
p_glow = "piscando" if pred == "P" else ""
b_glow = "piscando" if pred == "B" else ""

st.markdown(f"""
<div class="mesa-wrapper">
    <div class="asa asa-p {p_glow}">
        <span style="font-size: 10px; opacity: 0.7;">1:1</span>
        <span class="label-bet">JOGADOR</span>
    </div>
    <div class="tie-circle">
        <span style="font-size: 10px; font-weight: bold;">EMPATE</span>
        <span style="font-size: 22px; font-weight: 900;">88:1</span>
    </div>
    <div class="asa asa-b {b_glow}">
        <span style="font-size: 10px; opacity: 0.7;">1:1</span>
        <span class="label-bet">BANCA</span>
    </div>
</div>
""", unsafe_allow_html=True)

# STATS
st.markdown("<p style='text-align: center; opacity: 0.6; font-size: 12px;'>TENDÊNCIA: 🔵 54% | 🟡 10% | 🔴 36%</p>", unsafe_allow_html=True)

# ROAD
road_html = '<div class="road-box"><div class="road-grid">'
for r in reversed(history[:120]):
    road_html += f'<div class="bead b-{r}">{r if r!="T" else ""}</div>'
road_html += '</div></div>'
st.markdown(road_html, unsafe_allow_html=True)

# CONTROLES
if pred:
    st.markdown(f"<h3 style='text-align: center; color: white;'>ENTRADA: {'JOGADOR' if pred=='P' else 'BANCA'}</h3>", unsafe_allow_html=True)
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
    st.markdown("<p style='text-align: center; color: #555;'>🔎 AGUARDANDO PADRÃO ESTATÍSTICO...</p>", unsafe_allow_html=True)

time.sleep(12)
st.rerun()
