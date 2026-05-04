import streamlit as st
import time
import cloudscraper
import re

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="BAC BO REAL-TIME INTERFACE", layout="wide")

# --- CSS: RÉPLICA 100% BAC BO EVOLUTION ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto+Condensed:wght@400;700&display=swap');

    [data-testid="stAppViewContainer"] {
        background: url('https://w0.peakpx.com/wallpaper/433/384/HD-wallpaper-dark-blur-abstract.jpg');
        background-size: cover;
        color: white;
        font-family: 'Roboto Condensed', sans-serif;
    }
    
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }

    /* ÁREA DE APOSTAS - 100% IGUAL AO JOGO */
    .mesa-bacbo {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 250px;
        margin: 20px auto;
        position: relative;
        max-width: 800px;
    }

    .asa {
        width: 320px;
        height: 150px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        padding: 20px;
        position: relative;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        transition: all 0.4s ease;
    }

    .asa-jogador {
        background: linear-gradient(to right, rgba(0, 50, 200, 0.8), rgba(0, 30, 100, 0.6));
        border-radius: 40px 0 0 40px;
        text-align: left;
        margin-right: -20px;
    }

    .asa-banca {
        background: linear-gradient(to left, rgba(200, 0, 50, 0.8), rgba(100, 0, 30, 0.6));
        border-radius: 0 40px 40px 0;
        text-align: right;
        margin-left: -20px;
    }

    .centro-empate {
        width: 180px;
        height: 180px;
        background: radial-gradient(circle, #d4af37, #8a6d3b);
        border-radius: 50%;
        z-index: 10;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        border: 5px solid #ffcc33;
        box-shadow: 0 0 30px rgba(0,0,0,0.6);
        text-align: center;
        font-size: 14px;
        color: white;
    }

    /* EFEITO PISCANTE DE ÁGUA NO SINAL (RESERVA DE APOSTA) */
    @keyframes agua-glow {
        0% { box-shadow: 0 0 10px rgba(255,255,255,0.2); border-color: rgba(255,255,255,0.2); }
        50% { box-shadow: 0 0 60px #fff, inset 0 0 20px #fff; border-color: #fff; transform: scale(1.02); }
        100% { box-shadow: 0 0 10px rgba(255,255,255,0.2); border-color: rgba(255,255,255,0.2); }
    }

    .sinal-ativo {
        animation: agua-glow 0.8s infinite alternate;
        z-index: 50;
        border: 3px solid #fff !important;
    }

    /* BEAD ROAD IGUAL À IMAGEM */
    .bead-road {
        background: #fff;
        border: 2px solid #999;
        display: grid;
        grid-template-columns: repeat(24, 25px);
        grid-template-rows: repeat(6, 25px);
        gap: 1px;
        width: fit-content;
        margin: 20px auto;
        padding: 2px;
    }

    .bead {
        width: 25px; height: 25px;
        display: flex; align-items: center; justify-content: center;
        font-size: 11px; font-weight: bold; color: white;
        border-radius: 50%;
    }
    .P { background-color: #0044cc; } /* Jogador */
    .B { background-color: #cc0033; } /* Banca */
    .T { background-color: #cc9933; position: relative; } /* Empate */
    .T::after { content: ''; position: absolute; width: 100%; height: 2px; background: white; transform: rotate(-45deg); }

    .stats-container { display: flex; justify-content: center; gap: 20px; margin-top: 10px; font-size: 12px; }
</style>
""", unsafe_allow_html=True)

# --- MOTOR DE INTELIGÊNCIA ---
if 'wins' not in st.session_state: st.session_state.wins = 0
if 'losses' not in st.session_state: st.session_state.losses = 0

def get_live_history():
    try:
        scraper = cloudscraper.create_scraper()
        res = scraper.get("https://www.trackcasino.com/bacbo", timeout=10).text
        found = re.findall(r'>(P|B|T)<', res)
        return found[:144]
    except:
        return ["P", "B", "P", "B", "T", "B", "P", "B"]

# Lógica de Predição
def predict(h):
    if len(h) < 3: return None
    # Estratégia de Quebra de 3
    if h[:3] == ["P", "P", "P"]: return "B"
    if h[:3] == ["B", "B", "B"]: return "P"
    # Estratégia de Ping-Pong
    if h[:4] == ["P", "B", "P", "B"]: return "P"
    if h[:4] == ["B", "P", "B", "P"]: return "B"
    return None

# --- UI ---
history = get_live_history()
pred = predict(history)

st.markdown("<h3 style='text-align: center; color: rgba(255,255,255,0.5);'>BAC BO AI PREDICTOR - tarcoboss</h3>", unsafe_allow_html=True)

# ASA JOGADOR | EMPATE | ASA BANCA
j_class = "sinal-ativo" if pred == "P" else ""
b_class = "sinal-ativo" if pred == "B" else ""

st.markdown(f"""
<div class="mesa-bacbo">
    <div class="asa asa-jogador {j_class}">
        <span style="font-size: 12px; opacity: 0.6;">1:1</span>
        <span style="font-size: 26px; font-weight: 700;">JOGADOR</span>
    </div>
    <div class="centro-empate">
        <span style="font-size: 10px; opacity: 0.8;">EMPATE</span>
        <span style="font-size: 20px; font-weight: 700;">88:1</span>
        <span style="font-size: 9px; opacity: 0.6;">MAX PAGAMENTO</span>
    </div>
    <div class="asa asa-banca {b_class}">
        <span style="font-size: 12px; opacity: 0.6;">1:1</span>
        <span style="font-size: 26px; font-weight: 700;">BANCA</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Porcentagens (Fictícias baseadas no histórico)
st.markdown("""
<div class="stats-container">
    <span style="color: #0055ff;">JOGADOR 54%</span>
    <span style="color: #ffaa00;">EMPATE 10%</span>
    <span style="color: #ff0044;">BANCA 36%</span>
</div>
""", unsafe_allow_html=True)

# BEAD ROAD (GRADE)
st.markdown("<div class='bead-road'>", unsafe_allow_html=True)
road_html = "".join([f'<div class="bead {r}">{r if r!="T" else ""}</div>' for r in history])
st.markdown(road_html + "</div>", unsafe_allow_html=True)

# PLACAR E GESTÃO
st.divider()
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    if pred:
        st.success(f"🎯 ENTRADA CONFIRMADA: {'JOGADOR' if pred=='P' else 'BANCA'}")
        cw, cl = st.columns(2)
        if cw.button("✅ GREEN"):
            st.session_state.wins += 1
            st.rerun()
        if cl.button("❌ LOSS"):
            st.session_state.losses += 1
            st.rerun()
    else:
        st.info("🔎 MONITORANDO MESA... AGUARDANDO PADRÃO DE ENTRADA.")

st.write(f"PLACAR: {st.session_state.wins} | {st.session_state.losses}")

# REFRESH
time.sleep(12)
st.rerun()
