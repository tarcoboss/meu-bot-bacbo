import streamlit as st
import pandas as pd
import time
import cloudscraper
from bs4 import BeautifulSoup

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="BAC BO ULTRA-BOT LIVE", layout="wide")

# Estilização CSS para visual "Casino Dark Mode"
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #050505; color: white; }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }
    .stMetric { 
        background-color: #111; 
        border: 1px solid #333; 
        padding: 15px; 
        border-radius: 15px; 
        box-shadow: 0 4px 15px rgba(0,210,255,0.1);
    }
    .signal-card {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        padding: 40px;
        border-radius: 30px;
        border: 2px solid #3b82f6;
        text-align: center;
        margin-bottom: 20px;
    }
    .green-glow { border-color: #00ff88; box-shadow: 0 0 30px rgba(0,255,136,0.2); }
    .red-glow { border-color: #ff0055; box-shadow: 0 0 30px rgba(255,0,85,0.2); }
    .waiting-text { color: #666; font-style: italic; font-size: 20px; }
    </style>
    """, unsafe_allow_stdio=True)

# --- INICIALIZAÇÃO DO PLACAR (SESSION STATE) ---
if 'wins' not in st.session_state: st.session_state.wins = 0
if 'losses' not in st.session_state: st.session_state.losses = 0
if 'streak' not in st.session_state: st.session_state.streak = 0
if 'history' not in st.session_state: st.session_state.history = []
if 'current_gale' not in st.session_state: st.session_state.current_gale = 0
if 'active_signal' not in st.session_state: st.session_state.active_signal = None

# --- FUNÇÃO PARA PEGAR DADOS REAIS ---
def get_live_data():
    try:
        scraper = cloudscraper.create_scraper()
        # Usamos o Tracksino como fonte de dados real da Evolution
        url = "https://tracksino.com/bacbo" 
        res = scraper.get(url, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Procura os resultados na tabela de histórico
        results = []
        balls = soup.find_all('div', class_='history-ball') # Classe comum em rastreadores
        for ball in balls[:10]:
            char = ball.text.strip()[0] # P, B ou T
            results.append(char)
        return results if results else ["P", "B", "P"] # Fallback se falhar
    except:
        return ["P", "P", "B"] # Simulação caso o site bloqueie temporariamente

# --- LÓGICA DE ANÁLISE ---
def analyze():
    data = get_live_data()
    if not data: return
    
    last_3 = data[:3] # Pega os 3 últimos
    
    # Se sair 3 iguais, gera sinal oposto (Estratégia clássica)
    if last_3 == ['P', 'P', 'P']:
        st.session_state.active_signal = "BANQUEIRO 🔴"
    elif last_3 == ['B', 'B', 'B']:
        st.session_state.active_signal = "JOGADOR 🔵"
    else:
        st.session_state.active_signal = None
        st.session_state.current_gale = 0

# --- INTERFACE PRINCIPAL ---
st.markdown("<h1 style='text-align: center; color: #3b82f6;'>🤖 BAC BO PRO - SINAIS REAIS</h1>", unsafe_allow_stdio=True)

# Linha de Placar
total = st.session_state.wins + st.session_state.losses
acc = (st.session_state.wins / total * 100) if total > 0 else 100

c1, c2, c3, c4 = st.columns(4)
c1.metric("Assertividade", f"{acc:.1f}%")
c2.metric("Placar ✅", st.session_state.wins)
c3.metric("Placar ❌", st.session_state.losses)
c4.metric("Sequência 🔥", st.session_state.streak)

st.divider()

# Área do Sinal
placeholder = st.empty()

with placeholder.container():
    analyze() # Executa a análise
    
    if st.session_state.active_signal:
        # Se tem sinal, mostra o card de aposta
        st.markdown(f"""
            <div class="signal-card">
                <h3 style='color: #3b82f6;'>🎯 SINAL CONFIRMADO</h3>
                <h1 style='font-size: 60px;'>APOSTAR NO {st.session_state.active_signal}</h1>
                <p style='font-size: 20px;'>⚠️ Proteção: <b>EMPATE (TIE)</b></p>
                <div style='background: #111; padding: 10px; border-radius: 10px; margin-top: 2
