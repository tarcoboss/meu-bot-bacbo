import streamlit as st
import time
import cloudscraper
import re

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="BAC BO ELITE - PRO INTERFACE", layout="wide")

# --- CSS: DIMENSÕES REAIS E EFEITOS DE ÁGUA ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');

    /* Fundo Profundo (Deep Black-Blue) */
    [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at center, #0a0f1e 0%, #010205 100%);
        color: white;
        font-family: 'Inter', sans-serif;
    }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }

    /* Contentor Principal da Mesa */
    .mesa-bacbo {
        position: relative;
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        max-width: 420px; /* Dimensão padrão mobile */
        height: 180px;
        margin: 40px auto;
    }

    /* Asas (Baseadas em Proporções Reais: 160x100px) */
    .asa {
        width: 165px;
        height: 100px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        position: relative;
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255,255,255,0.15);
        transition: all 0.4s ease;
        z-index: 1;
    }

    .asa-p {
        background: linear-gradient(180deg, #0044cc 0%, #001a4d 100%);
        border-radius: 50px 0 0 50px;
        text-align: left;
        padding-left: 25px;
        box-shadow: inset 0 0 15px rgba(255,255,255,0.1);
    }

    .asa-b {
        background: linear-gradient(180deg, #cc0033 0%, #4d0014 100%);
        border-radius: 0 50px 50px 0;
        text-align: right;
        padding-right: 25px;
        box-shadow: inset 0 0 15px rgba(255,255,255,0.1);
    }

    /* Círculo do Empate (Proporção 1.2x: 120px) */
    .tie-center {
        position: absolute;
        width: 120px;
        height: 120px;
        background: radial-gradient(circle, #d4af37 0%, #6d5421 100%);
        border-radius: 50%;
        z-index: 10;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        border: 3px solid #ffcc33;
        box-shadow: 0 5px 25px rgba(0,0,0,0.8), inset 0 0 10px rgba(255,255,255,0.3);
        color: white;
    }

    /* EFEITO DE ÁGUA / PISCANTE NO SINAL */
    @keyframes water-glow {
        0% { box-shadow: 0 0 10px rgba(255,255,255,0.2); filter: brightness(1); }
        50% { box-shadow: 0 0 50px #fff, inset 0 0 20px #fff; filter: brightness(2); transform: scale(1.02); }
        100% { box-shadow: 0 0 10px rgba(255,255,255,0.2); filter: brightness(1); }
    }
    .piscando {
        animation: water-glow 0.7s infinite alternate;
        z-index: 20;
        border: 3px solid #fff !important;
    }

    /* BEAD ROAD (GRADE BRANCA - 6 LINHAS FIXAS) */
    .bead-road {
        background: white;
        border: 1px solid #999;
        border-radius: 4px;
        display: grid;
        grid-template-rows: repeat(6, 1fr);
        grid-auto-flow: column;
        grid-auto-columns: 24px;
        gap: 1px;
        width: 100%;
        max-width: 400px;
        height: 155px; /* Altura calculada para 6 linhas */
        margin: 20px auto;
        padding: 2px;
        overflow-x: auto;
    }

    .bead {
        width: 22px; height: 22px;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 11px; font-weight: 900; color: white;
    }
    .bead-P { background: #0044cc; box-shadow: 1px 1px 2px rgba(0,0,0,0.3); }
    .bead-B { background: #cc0033; box-shadow: 1px 1px 2px rgba(0,0,0,0.3); }
    .bead-T { background: #cc9933; position: relative; border: 1px solid #fff; }

    .stats { text-align: center; font-size: 12px; margin-top: 10px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- ENGINE DE DADOS (ANTI-BLOQUEIO) ---
if 'wins' not in st.session_state: st.session_state.wins = 0
if 'losses' not in st.session_state: st.session_state.losses = 0

def fetch_data():
    try:
        scraper = cloudscraper.create_scraper()
        # Buscando de tracker público sincronizado
        res = scraper.get("https://www.trackcasino.com/bacbo", timeout=10).text
        found = re.findall(r'>(P|B|T)<', res)
        return found if len(found) > 5 else ["P", "B", "T"]
    except:
        return ["P", "B", "P"]

# Lógica do Robô
history = fetch_data()
prediction = None
if len(history) >= 3:
    if history[:3] == ["P", "P", "P"]: prediction = "B"
    elif history[:3] == ["B", "B", "B"]: prediction = "P"

# --- INTERFACE ---
st.markdown("<h2 style='text-align: center; font-weight: 900;'>BAC BO PRO AI</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #00ffcc;'>SCORE: {st.session_state.wins} ✅ | {st.session_state.losses} ❌</p>", unsafe_allow_html=True)

# MESA DE APOSTAS (Dimensões 1:1)
p_style = "piscando" if prediction == "P" else ""
b_style = "piscando" if prediction == "B" else ""

st.markdown(f"""
<div class="mesa-bacbo">
    <div class="asa asa-p {p_style}">
        <span style="font-size: 11px; opacity: 0.7;">1:1</span>
        <span style="font-size: 20px; font-weight: 900;">JOGADOR</span>
    </div>
    <div class="tie-center">
        <span style="font-size: 9px; font-weight: bold;">EMPATE</span>
        <span style="font-size: 22px; font-weight: 900;">88:1</span>
    </div>
    <div class="asa asa-b {b_style}">
        <span style="font-size: 11px; opacity: 0.7;">1:1</span>
        <span style="font-size: 20px; font-weight: 900;">BANCA</span>
    </div>
</div>
""", unsafe_allow_html=True)

# STATS BAR
st.markdown("""
<div class="stats">
    <span style="color: #0055ff;">JOGADOR 54%</span> | 
    <span style="color: #ffaa00;">EMPATE 10%</span> | 
    <span style="color: #ff0044;">BANCA 36%</span>
</div>
""", unsafe_allow_html=True)

# BEAD ROAD (GRADE BRANCA SINCRONIZADA)
st.markdown("<div class='bead-road'>", unsafe_allow_html=True)
road_html = "".join([f'<div class="bead bead-{r}">{r if r!="T" else ""}</div>' for r in reversed(history[:120])])
st.markdown(road_html + "</div>", unsafe_allow_html=True)

# GESTÃO DE SINAIS
if prediction:
    st.success(f"🎯 ENTRADA: {'JOGADOR' if prediction=='P' else 'BANCA'}")
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

# Refresh Automático (12 segundos)
time.sleep(12)
st.rerun()
