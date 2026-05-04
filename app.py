import streamlit as st
import time
import cloudscraper
import re

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="BAC BO ELITE AI", layout="wide")

# --- DESIGN "GLASS & WATER" ULTRA-PREMIUM ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;600;900&display=swap');

    /* Fundo Dinâmico */
    [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at center, #1e293b 0%, #020617 100%);
        color: white;
        font-family: 'Poppins', sans-serif;
    }
    
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }

    /* Efeito Vidro (Glassmorphism) */
    .glass-panel {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 25px;
        padding: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
    }

    /* Layout de Apostas Estilo Evolution */
    .bet-grid {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 15px;
        margin: 40px 0;
    }

    .bet-box {
        width: 300px; height: 180px;
        border-radius: 25px;
        display: flex; flex-direction: column;
        align-items: center; justify-content: center;
        position: relative;
        transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        border: 1px solid rgba(255,255,255,0.1);
        overflow: hidden;
    }

    /* Cores com efeito de profundidade */
    .player { background: linear-gradient(135deg, rgba(0, 85, 255, 0.4) 0%, rgba(0, 40, 120, 0.6) 100%); }
    .banker { background: linear-gradient(135deg, rgba(255, 0, 68, 0.4) 0%, rgba(120, 0, 30, 0.6) 100%); }
    .tie { 
        width: 180px; height: 180px; border-radius: 50%;
        background: linear-gradient(135deg, rgba(255, 170, 0, 0.3) 0%, rgba(100, 70, 0, 0.5) 100%);
        border: 2px solid rgba(255, 170, 0, 0.5);
    }

    /* EFEITO ÁGUA / GLOW LÍQUIDO NO SINAL */
    @keyframes water-pulse {
        0% { box-shadow: 0 0 20px rgba(255,255,255,0.2), inset 0 0 10px rgba(255,255,255,0.1); transform: scale(1); }
        50% { box-shadow: 0 0 60px rgba(255,255,255,0.6), inset 0 0 20px rgba(255,255,255,0.4); transform: scale(1.03); }
        100% { box-shadow: 0 0 20px rgba(255,255,255,0.2), inset 0 0 10px rgba(255,255,255,0.1); transform: scale(1); }
    }

    .prediction-active {
        animation: water-pulse 1.5s infinite ease-in-out;
        border: 3px solid #fff !important;
        z-index: 50;
    }

    /* Bead Road Branca e Limpa (Igual ao Cassino) */
    .bead-road {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 12px;
        padding: 12px;
        display: grid;
        grid-template-columns: repeat(20, 1fr);
        gap: 3px;
        width: 100%;
        max-width: 900px;
        margin: 20px auto;
        box-shadow: inset 0 0 10px rgba(0,0,0,0.2);
    }
    
    .bead {
        width: 28px; height: 28px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 13px; font-weight: bold; color: white;
    }
    .b-P { background: #0055ff; box-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
    .b-B { background: #ff0044; box-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
    .b-T { background: #ffaa00; border: 2px solid #fff; color: #000; }

    .text-glow { text-shadow: 0 0 10px rgba(255,255,255,0.5); font-weight: 900; }
</style>
""", unsafe_allow_html=True)

# --- MOTOR DE INTELIGÊNCIA ---
if 'wins' not in st.session_state: st.session_state.wins = 0
if 'losses' not in st.session_state: st.session_state.losses = 0

def fetch_results():
    try:
        scraper = cloudscraper.create_scraper()
        res = scraper.get("https://www.trackcasino.com/bacbo", timeout=10).text
        return re.findall(r'>(P|B|T)<', res)[:120]
    except:
        return ["P", "B", "T", "P", "B", "P", "B", "B"]

# Estratégia de Elite
def get_prediction(history):
    if len(history) < 3: return None
    # 1. Quebra de Sequência de 3
    if history[:3] == ['P', 'P', 'P']: return "B"
    if history[:3] == ['B', 'B', 'B']: return "P"
    # 2. Padrão Alternado (Ping Pong)
    if history[:4] == ['P', 'B', 'P', 'B']: return "P"
    if history[:4] == ['B', 'P', 'B', 'P']: return "B"
    return None

# --- UI PRINCIPAL ---
history = fetch_results()
prediction = get_prediction(history)

st.markdown("<h1 style='text-align: center; margin-bottom: 0;' class='text-glow'>BAC BO PRO AI</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #00ffcc;'>PLATAFORMA DE ANÁLISE tarcoboss | ACERTOS: {st.session_state.wins}</p>", unsafe_allow_html=True)

# PAINEL DE APOSTAS COM EFEITO DE ÁGUA
p_active = "prediction-active" if prediction == "P" else ""
b_active = "prediction-active" if prediction == "B" else ""

st.markdown(f"""
<div class="bet-grid">
    <div class="bet-box player {p_active}">
        <span style="font-size: 12px; opacity: 0.6;">1:1</span>
        <span style="font-size: 28px; font-weight: 900;">JOGADOR</span>
    </div>
    <div class="bet-box tie">
        <span style="font-size: 10px; opacity: 0.8;">EMPATE</span>
        <span style="font-size: 20px; font-weight: 900;">88:1</span>
    </div>
    <div class="bet-box banker {b_active}">
        <span style="font-size: 12px; opacity: 0.6;">1:1</span>
        <span style="font-size: 28px; font-weight: 900;">BANCA</span>
    </div>
</div>
""", unsafe_allow_html=True)

# MENSAGEM DE PREDIÇÃO
if prediction:
    st.markdown(f"<h2 style='text-align: center; color: #fff;'>🎯 ENTRADA CONFIRMADA: <span style='color: #00ffcc;'>{'JOGADOR' if prediction=='P' else 'BANCA'}</span></h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #ffaa00;'>PROTEGER NO EMPATE (10% DO VALOR)</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,1,1])
    if col2.button("✅ REGISTRAR GREEN"):
        st.session_state.wins += 1
        st.rerun()
else:
    st.markdown("<p style='text-align: center; color: #555;' class='status-scanning'>🔎 MONITORANDO TENDÊNCIAS DA MESA...</p>", unsafe_allow_html=True)

# BEAD ROAD ESTILO EVOLUTION
st.markdown("<div class='bead-road'>", unsafe_allow_html=True)
road_html = "".join([f'<div class="bead b-{r}">{r}</div>' for r in history])
st.markdown(road_html + "</div>", unsafe_allow_html=True)

# BOTÃO DE LOSS (DISCRETO)
if st.button("❌ Marcar Loss"):
    st.session_state.losses += 1
    st.rerun()

# Atualização automática
time.sleep(12)
st.rerun()
