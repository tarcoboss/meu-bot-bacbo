import streamlit as st
import time
import cloudscraper
import re

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="BAC BO PRO", layout="wide")

# --- CSS RÉPLICA FIEL (CORRIGIDO) ---
st.markdown("""
<style>
    /* Fundo Escuro */
    [data-testid="stAppViewContainer"] {
        background-color: #060606;
        color: white;
    }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }

    /* Contentor da Mesa */
    .mesa-container {
        position: relative;
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        max-width: 500px;
        margin: 50px auto;
        height: 180px;
    }

    /* Asas (Jogador e Banca) */
    .asa {
        flex: 1;
        height: 130px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        padding: 15px;
        position: relative;
        border: 1px solid rgba(255,255,255,0.1);
        transition: all 0.3s ease;
    }

    .asa-jogador {
        background: linear-gradient(180deg, #0044cc 0%, #002266 100%);
        border-radius: 60px 0 0 60px;
        text-align: left;
        padding-left: 30px;
    }

    .asa-banca {
        background: linear-gradient(180deg, #cc0033 0%, #66001a 100%);
        border-radius: 0 60px 60px 0;
        text-align: right;
        padding-right: 30px;
    }

    /* Círculo do Empate (Ouro) */
    .centro-tie {
        position: absolute;
        width: 150px;
        height: 150px;
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
        box-shadow: 0 0 20px rgba(0,0,0,0.8);
    }

    /* Efeito de Piscada no Sinal */
    @keyframes blink-sinal {
        0% { border-color: #fff; box-shadow: 0 0 10px #fff; }
        50% { border-color: #fff; box-shadow: 0 0 60px #fff; filter: brightness(1.5); }
        100% { border-color: #fff; box-shadow: 0 0 10px #fff; }
    }
    .sinal-ativo {
        animation: blink-sinal 0.6s infinite alternate !important;
        z-index: 20;
    }

    /* Bead Road (Grade Branca) */
    .bead-road-container {
        background: white;
        border-radius: 5px;
        padding: 5px;
        width: 95%;
        max-width: 450px;
        height: 160px;
        margin: 20px auto;
        overflow-x: auto;
        border: 2px solid #333;
    }

    .grid-road {
        display: grid;
        grid-template-rows: repeat(6, 22px);
        grid-auto-flow: column;
        grid-auto-columns: 22px;
        gap: 1px;
    }

    .bead {
        width: 20px;
        height: 20px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 10px;
        font-weight: bold;
        color: white;
    }
    .bead-P { background-color: #0044cc; }
    .bead-B { background-color: #cc0033; }
    .bead-T { background-color: #cc9933; position: relative; }
    .bead-T::after { content: ''; position: absolute; width: 100%; height: 2px; background: white; transform: rotate(-45deg); }

</style>
""", unsafe_allow_html=True)

# --- ENGINE ---
if 'wins' not in st.session_state: st.session_state.wins = 0
if 'losses' not in st.session_state: st.session_state.losses = 0

def fetch_data():
    try:
        scraper = cloudscraper.create_scraper()
        res = scraper.get("https://www.trackcasino.com/bacbo", timeout=10).text
        found = re.findall(r'>(P|B|T)<', res)
        return found[:120] if found else ["P", "B", "P"]
    except:
        return ["P", "B", "T"]

history = fetch_data()

# Lógica de Estratégia
pred = None
if len(history) >= 3:
    if history[:3] == ["P", "P", "P"]: pred = "B"
    elif history[:3] == ["B", "B", "B"]: pred = "P"

# --- UI ---
st.markdown("<h4 style='text-align: center; color: #555;'>BAC BO ELITE AI</h4>", unsafe_allow_html=True)

# Mesa de Apostas
j_active = "sinal-ativo" if pred == "P" else ""
b_active = "sinal-ativo" if pred == "B" else ""

st.markdown(f"""
<div class="mesa-container">
    <div class="asa asa-jogador {j_active}">
        <span style="font-size: 10px; opacity: 0.6;">1:1</span>
        <span style="font-size: 20px; font-weight: 900;">JOGADOR</span>
    </div>
    <div class="centro-tie">
        <span style="font-size: 9px; opacity: 0.8;">EMPATE</span>
        <span style="font-size: 22px; font-weight: 900;">88:1</span>
    </div>
    <div class="asa asa-banca {b_active}">
        <span style="font-size: 10px; opacity: 0.6;">1:1</span>
        <span style="font-size: 20px; font-weight: 900;">BANCA</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Barra de Stats
st.markdown("<p style='text-align: center; font-size: 12px;'>🔵 54% | 🟡 10% | 🔴 36%</p>", unsafe_allow_html=True)

# Bead Road (Grade Branca)
road_html = '<div class="bead-road-container"><div class="grid-road">'
for r in reversed(history[:120]): # Ordem correta da esquerda para a direita
    road_html += f'<div class="bead bead-{r}">{r if r!="T" else ""}</div>'
road_html += '</div></div>'
st.markdown(road_html, unsafe_allow_html=True)

# Placar e Botões
st.divider()
if pred:
    st.success(f"ENTRADA: {'JOGADOR' if pred=='P' else 'BANCA'}")
    c1, c2 = st.columns(2)
    if c1.button("✅ GREEN"):
        st.session_state.wins += 1
        st.rerun()
    if c2.button("❌ LOSS"):
        st.session_state.losses += 1
        st.rerun()

st.write(f"PLACAR: {st.session_state.wins} - {st.session_state.losses}")

time.sleep(12)
st.rerun()
