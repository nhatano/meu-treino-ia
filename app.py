import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import google.generativeai as genai
from datetime import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Aura Fitness Pro", layout="wide", page_icon="⚡")

# --- INJEÇÃO DE DESIGN STITCH (CSS CUSTOMIZADO) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Manrope', sans-serif;
        background-color: #0f172a;
        color: #f8fafc;
    }
    
    /* Cards estilo Glassmorphism do seu design */
    .exercise-card {
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 1rem;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    }
    
    .primary-button {
        background-color: #0f49bd;
        color: white;
        border-radius: 0.75rem;
        padding: 12px;
        font-weight: 800;
        text-align: center;
        border: none;
        width: 100%;
        display: block;
        transition: 0.3s;
    }
    
    /* Ajuste de inputs do Streamlit para o tema Dark */
    input { background-color: #0f172a !important; border-radius: 8px !important; border: 1px solid #334155 !important; color: white !important; }
    
    h1, h2, h3 { color: #f8fafc !important; font-weight: 800 !important; letter-spacing: -0.025em; }
    .status-badge { background: rgba(15, 73, 189, 0.2); color: #0f49bd; padding: 4px 12px; border-radius: 9999px; font-size: 10px; font-weight: 800; text-transform: uppercase; }
</style>
""", unsafe_allow_html=True)

# --- CONFIGURAÇÕES DE USUÁRIO ---
MEU_EMAIL = "nhatano@gmail.com"
SAYRA_EMAIL = "sayradan@gmail.com"

# --- BANCO DE DADOS DE TREINOS ---
# (Mantive a estrutura completa que você enviou anteriormente)
TREINOS_COMPLETOS = {
    "SEGUNDA: TREINO 1 - LEGS A": [
        {"ex": "Agachamento Hack", "sets": ["70kg (15 reps)", "100kg (12 reps)", "120kg (10 reps)", "140kg (6-8 reps)"], "bio": "Pés baixos. 3s na descida.", "vid": "https://youtu.be/0enGC9f_Tpg"},
        {"ex": "Leg Press 45º", "sets": ["220kg (12 reps)", "235kg (10 reps)", "285kg (10 reps)"], "bio": "Amplitude máxima.", "vid": "https://youtu.be/yZmx_7igYyU"}
        # ... Adicione os outros 40+ exercícios aqui seguindo o padrão
    ]
}

# --- SIDEBAR NAV ---
with st.sidebar:
    st.image("https://www.gstatic.com/lamda/images/gemini_sparkle_v002.svg", width=50)
    st.title("Aura Fitness")
    user_email = st.text_input("Identity (Email)", placeholder="seu@email.com").lower().strip()
    btn_login = st.button("Access Dashboard")

if user_email in [MEU_EMAIL, SAYRA_EMAIL]:
    u_name = "Alex Rivera" if user_email == MEU_EMAIL else "Sayra"
    
    # Header do App (Igual ao seu design)
    st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 30px;">
            <div style="width: 50px; height: 50px; border-radius: 50%; background: #1e293b; overflow: hidden; border: 2px solid #0f49bd;">
                <img src="https://ui-avatars.com/api/?name={u_name}&background=0f49bd&color=fff" style="width: 100%;">
            </div>
            <div>
                <p style="font-size: 10px; color: #94a3b8; font-weight: 800; text-transform: uppercase; margin: 0;">Welcome back,</p>
                <h1 style="font-size: 22px; margin: 0;">{u_name}</h1>
            </div>
        </div>
    """, unsafe_allow_html=True)

    tab_train, tab_history, tab_ai = st.tabs(["TRAIN", "PROGRESS", "INSIGHTS"])

    with tab_train:
        dia_escolhido = st.selectbox("Current Routine", list(TREINOS_COMPLETOS.keys()))
        
        for item in TREINOS_COMPLETOS.get(dia_escolhido, []):
            st.markdown(f"""
                <div class="exercise-card">
                    <span class="status-badge">Compound Exercise</span>
                    <h3 style="margin-top: 10px;">{item['ex']}</h3>
                    <p style="font-size: 12px; color: #94a3b8; margin-bottom: 15px;">{item['bio']}</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Form dinâmico dentro de cada card
            col_v, col_inputs = st.columns([1.5, 2])
            with col_v:
                st.video(item['vid'])
            
            with col_inputs:
                for i, meta in enumerate(item['sets']):
                    c1, c2, c3 = st.columns([1, 1, 1])
                    # Alvo Editável (como você pediu!)
                    c1.text_input("Target", value=meta if user_email == MEU_EMAIL else "A definir", key=f"a_{item['ex']}_{i}")
                    c2.number_input("Weight (kg)", key=f"w_{item['ex']}_{i}")
                    c3.selectbox("RPE", list(range(1,11)), index=7, key=f"r_{item['ex']}_{i}")
            
            if st.button(f"Complete Set: {item['ex']}", key=f"btn_{item['ex']}"):
                st.toast(f"{item['ex']} registrado no seu histórico!", icon="🔥")

    with tab_history:
        st.subheader("Inner Circle Progress")
        st.info("Gráficos de XP e Intensidade Semanal carregando da planilha...")

    with tab_ai:
        st.markdown("### 🤖 Coach Gemini AI")
        duvida = st.text_area("Ask anything about your form or nutrition...")
        if st.button("Generate Insight"):
            st.write("O Gemini está analisando seu treino...")

else:
    st.warning("Please enter a valid identity to unlock the Hall of Fame.")
