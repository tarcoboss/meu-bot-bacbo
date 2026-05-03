import streamlit as st
import time
import cloudscraper
import re

# --- CONFIGURAÇÃO DE DESIGN PREMIUM ---
st.set_page_config(page_title="BAC BO PRO - 100% AUTOMÁTICO", layout="wide")

st.markdown("""
<style>
    [data-testid="stAppViewContainer"] { background-color: #050505; color: white; }
    .stMetric { background-color: #111; border: 1px solid #333; padding: 15px; border-radius: 15px; }
    .bola {
        width: 38px; height: 38px; border-radius: 50%; display: inline-flex;
        align-items: center; justify-content: center; font-weight: bold; margin: 5px;
        font-size: 14px; border: 2px solid rgba(255,255,255,0.1);
    }
    .P { background-color: #0055ff; box-shadow: 0 0 15px #0055ff; color: white; } /* PLAYER */
    .B { background-color: #ff0044; box-shadow: 0 0 15px #ff0044; color: white; } /* BANKER */
    .T { background-color: #ffaa00; color: black; } /* TIE */
    
    .card-sinal {
        background: linear-gradient(145deg, #0f172a, #1e293b);
        padding: 40px; border-radius: 30px; border: 2px solid #3b82f6;
        text-align: center; box-shadow: 0 0 40px rgba(59, 130, 246, 0.3);
    }
    .status-scanning { color: #666; font-style: italic; animation: pulse 2s infinite; }
    @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; } }
</style>
""", unsafe_allow_html=True)

# --- SISTEMA INTERNO ---
if 'wins' not in st.session_state: st.session_state.wins = 0
if 'losses' not in st.session_state: st.session_state.losses = 0
if 'last_history' not in st.session_state: st.session_state.last_history = []

def capturar_dados_automatico():
    try:
        # Criamos um rastreador que se passa por um computador real
        scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False})
        url = "https://casinoscore.com/bacbo/" 
        response = scraper.get(url, timeout=10)
        
        # Procura as letras P, B e T que representam os resultados das bolas
        html = response.text
        found = re.findall(r'result-([PBT])', html)
        if not found:
            found = re.findall(r'>(P|B|T)<', html)
            
        return found[:12] # Pega as últimas 12 rodadas
    except:
        return []

# --- CABEÇALHO ---
st.markdown("<h1 style='text-align: center; color: #3b82f6;'>🛡️ BAC BO AUTOMATIC PRO</h1>", unsafe_allow_html=True)

# Placar Automático
total = st.session_state.wins + st.session_state.losses
assertividade = (st.session_state.wins / total * 100) if total > 0 else 100

c1, c2, c3, c4 = st.columns(4)
c1.metric("ASSERTIVIDADE", f"{assertividade:.1f}%")
c2.metric("GREEN ✅", st.session_state.wins)
c3.metric("LOSS ❌", st.session_state.losses)
c4.metric("ESTADO", "LIVE", delta="ONLINE")

st.divider()

# --- LÓGICA DO ROBÔ ---
history = capturar_dados_automatico()

if not history:
    st.error("📡 AGUARDANDO CONEXÃO COM A MESA... Verificando novos dados.")
else:
    col_hist, col_sinal = st.columns([1, 2])
    
    with col_hist:
        st.subheader("📊 Histórico Real")
        html_bolas = ""
        for r in history:
            html_bolas += f'<div class="bola {r}">{r}</div>'
        st.markdown(html_bolas, unsafe_allow_html=True)
        st.caption("Atualizado em tempo real")

    with col_sinal:
        st.subheader("🎯 Inteligência de Entrada")
        
        # Pega as últimas 3 rodadas para analisar
        last_3 = history[:3]
        
        # Regra: Se sair 3 iguais, apostar no oposto
        if len(last_3) >= 3 and all(x == last_3[0] for x in last_3) and last_3[0] != 'T':
            alvo = "BANQUEIRO 🔴" if last_3[0] == 'P' else "JOGADOR 🔵"
            cor_card = "#ff0044" if "BANQUEIRO" in alvo else "#0055ff"
            
            st.markdown(f"""
                <div class="card-sinal" style="border-color: {cor_card};">
                    <h2 style="color: {cor_card};">SINAL DETECTADO!</h2>
                    <h1 style="font-size: 50px; margin: 15px 0;">ENTRAR NO {alvo}</h1>
                    <h3 style="color: #ffaa00;">🛡️ PROTEGER NO EMPATE</h3>
                    <p style="color: #666;">Padrão: 3x {last_3[0]} | Gestão: G1 e G2</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Controle de Placar
            st.write("Marque o resultado desta entrada:")
            cw, cl = st.columns(2)
            if cw.button("✅ BATEU GREEN"):
                st.session_state.wins += 1
                st.rerun()
            if cl.button("❌ DEU LOSS"):
                st.session_state.losses += 1
                st.rerun()
        else:
            st.markdown("""
                <div style='text-align: center; padding: 60px; border: 1px dashed #333; border-radius: 20px;'>
                    <h3 class="status-scanning">MONITORANDO PADRÕES...</h3>
                    <p style='color: #444;'>Aguardando repetição de 3 cores para definir entrada.</p>
                </div>
            """, unsafe_allow_html=True)

# Rodapé
st.divider()
st.markdown("<p style='text-align: center; color: #333;'>Propriedade de tarcoboss - Inteligência Analítica</p>", unsafe_allow_html=True)

# Loop de atualização automática (15 segundos)
time.sleep(15)
st.rerun()
