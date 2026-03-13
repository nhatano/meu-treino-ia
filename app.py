import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Aura Fitness Pro", layout="wide", page_icon="⚡")

# --- DESIGN PREMIUM AURA FITNESS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700;800&display=swap');
    html, body, [data-testid="stAppViewContainer"] { font-family: 'Manrope', sans-serif; background-color: #020617; color: #f8fafc; }
    .exercise-card { background: rgba(30, 41, 59, 0.4); backdrop-filter: blur(16px); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 1rem; padding: 24px; margin-bottom: 20px; border-left: 5px solid #0f49bd; }
    .status-badge { background: rgba(15, 73, 189, 0.2); color: #3b82f6; padding: 4px 12px; border-radius: 9999px; font-size: 10px; font-weight: 800; text-transform: uppercase; }
    .stButton>button { background: #0f49bd; color: white; border-radius: 0.75rem; font-weight: 800; height: 3rem; width: 100%; border: none; }
    input { background-color: #0f172a !important; color: white !important; border: 1px solid #334155 !important; }
</style>
""", unsafe_allow_html=True)

# --- CONFIGURAÇÕES ---
MEU_EMAIL = "nhatano@gmail.com"
SAYRA_EMAIL = "sayradan@gmail.com"
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdCkxNA1WEBbuDl4VA6KKmI937zLk95BQ654KSLGzwO6TxayA/formResponse"

# --- TREINOS COMPLETOS ---
TREINOS = {
    "TREINO 1: LEGS A (QUADRÍCEPS)": [
        {"ex": "Agachamento Hack", "sets": ["70kg (15 reps)", "100kg (12 reps)", "120kg (10 reps)", "140kg (6-8 reps)"], "bio": "Pés baixos. 3s na descida.", "vid": "https://www.youtube.com/watch?v=0enGC9f_Tpg"},
        {"ex": "Leg Press 45º", "sets": ["220kg (12 reps)", "235kg (10 reps)", "285kg (10 reps)"], "bio": "Amplitude máxima.", "vid": "https://www.youtube.com/watch?v=yZmx_7igYyU"},
        {"ex": "Cadeira Adutora", "sets": ["95kg", "100kg", "100kg"], "bio": "3s abrir/fechar.", "vid": "https://www.youtube.com/watch?v=4IStG89y8i4"},
        {"ex": "Cadeira Extensora", "sets": ["47kg", "47kg", "Drop set"], "bio": "Iso 2s no topo.", "vid": "https://www.youtube.com/watch?v=m0FOpMEgero"}
    ],
    "TREINO 2: PUSH A (PEITO/OMBRO)": [
        {"ex": "Supino Inclinado Halteres", "sets": ["25kg", "27,5kg", "30kg", "32,5kg"], "bio": "Banco 30º.", "vid": "https://www.youtube.com/watch?v=8iP9S706yLw"},
        {"ex": "Chest Press Articulado", "sets": ["35kg/l", "40kg/l", "Drop"], "bio": "Altura mamilo.", "vid": "https://www.youtube.com/watch?v=l_i9I-Y8r1U"}
    ]
    # Nilson, você pode continuar adicionando os outros aqui conforme o padrão!
}

# --- INTERFACE ---
with st.sidebar:
    st.markdown("### ⚡ Aura Fitness")
    user_email = st.text_input("Identidade (E-mail)", placeholder="seu@email.com").lower().strip()

if user_email in [MEU_EMAIL, SAYRA_EMAIL]:
    u_name = "Nilson" if user_email == MEU_EMAIL else "Olá Princess Fitness"
    st.markdown(f"### Bem-vindo, **{u_name}**!")
    
    dia = st.selectbox("Rotina Atual", list(TREINOS.keys()))
    
    for item in TREINOS[dia]:
        with st.container():
            st.markdown(f"""<div class="exercise-card"><h3>{item['ex']}</h3><p>{item['bio']}</p></div>""", unsafe_allow_html=True)
            cv, cd = st.columns([1, 2])
            with cv: st.video(item['vid'])
            with cd:
                for i, meta in enumerate(item['sets']):
                    cols = st.columns([2, 1, 1])
                    alvo = cols[0].text_input("Alvo", value=meta, key=f"t_{item['ex']}_{i}")
                    carga = cols[1].number_input("Peso (kg)", key=f"w_{item['ex']}_{i}", min_value=0)
                    rpe = cols[2].selectbox("RPE", list(range(1,11)), index=7, key=f"r_{item['ex']}_{i}")
            
            if st.button(f"Salvar {item['ex']}", key=f"btn_{item['ex']}"):
                try:
                    # Envia cada série individualmente para o formulário
                    for i in range(len(item['sets'])):
                        payload = {
                            'entry.2096362736': user_email,
                            'entry.201460740': item['ex'],
                            'entry.46463683': i + 1,
                            'entry.687657200': st.session_state[f"t_{item['ex']}_{i}"],
                            'entry.906726937': st.session_state[f"w_{item['ex']}_{i}"],
                            'entry.413423792': st.session_state[f"r_{item['ex']}_{i}"]
                        }
                        requests.post(FORM_URL, data=payload)
                    
                    st.success(f"Excelente, {u_name}! {item['ex']} salvo na sua planilha!")
                    st.balloons()
                except Exception as e:
                    st.error(f"Erro ao salvar: {e}")

else:
    st.info("👋 Digite seu e-mail para carregar seu treino.")
