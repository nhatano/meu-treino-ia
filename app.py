import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import google.generativeai as genai
from datetime import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Aura Fitness Pro - Nilson & Sayra", layout="wide", page_icon="⚡")

# --- INJEÇÃO DE DESIGN PREMIUM (CSS CUSTOMIZADO) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700;800&display=swap');
    html, body, [data-testid="stAppViewContainer"] { font-family: 'Manrope', sans-serif; background-color: #020617; color: #f8fafc; }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }
    .exercise-card { background: rgba(30, 41, 59, 0.4); backdrop-filter: blur(16px); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 1rem; padding: 24px; margin-bottom: 20px; border-left: 5px solid #0f49bd; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; background-color: transparent; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: transparent; border-radius: 4px; border: none; color: #94a3b8; font-weight: 800; }
    .stTabs [aria-selected="true"] { color: #0f49bd !important; border-bottom: 2px solid #0f49bd !important; }
    .status-badge { background: rgba(15, 73, 189, 0.2); color: #3b82f6; padding: 4px 12px; border-radius: 9999px; font-size: 10px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.1em; }
    input { background-color: #0f172a !important; color: white !important; border: 1px solid #334155 !important; }
    .stButton>button { background: #0f49bd; color: white; border-radius: 0.75rem; font-weight: 800; border: none; height: 3rem; transition: 0.3s; }
    .stButton>button:hover { transform: scale(1.02); background: #1e40af; }
</style>
""", unsafe_allow_html=True)

# --- CONFIGURAÇÕES ---
MEU_EMAIL = "nhatano@gmail.com"
SAYRA_EMAIL = "sayradan@gmail.com"

# --- BANCO DE DADOS DE TREINOS ---
TREINOS_COMPLETOS = {
    "TREINO 1: LEGS A (QUADRÍCEPS)": [
        {"ex": "Agachamento Hack", "sets": ["70kg (15 reps)", "100kg (12 reps)", "120kg (10 reps)", "140kg (6-8 reps)"], "bio": "Pés baixos. 3s na descida.", "vid": "https://youtu.be/0enGC9f_Tpg"},
        {"ex": "Leg Press 45º", "sets": ["220kg (12 reps)", "235kg (10 reps)", "285kg (10 reps)", "Drop: 260->180->100"], "bio": "Amplitude máxima.", "vid": "https://youtu.be/yZmx_7igYyU"},
        {"ex": "Cadeira Adutora", "sets": ["95kg (15 reps)", "100kg (12 reps)", "100kg (Falha)"], "bio": "3s abrir/fechar.", "vid": "https://youtu.be/4IStG89y8i4"},
        {"ex": "Cadeira Extensora", "sets": ["47kg (12 reps)", "47kg (12 reps)", "Drop: 54->33->19"], "bio": "Iso 2s no topo.", "vid": "https://youtu.be/m0FOpMEgero"},
        {"ex": "Afundo com Halteres", "sets": ["17,5kg/mão", "20kg/mão", "20kg (Falha)"], "bio": "Tronco à frente.", "vid": "https://youtu.be/q7_6v6w9jXs"},
        {"ex": "Panturrilha no Leg", "sets": ["150kg (15 reps)", "150kg", "150kg (Falha)"], "bio": "Alongamento máximo.", "vid": "https://youtu.be/q_K2eW7mUqI"},
        {"ex": "Abdominal Polia Média", "sets": ["1 min", "1 min", "Falha"], "bio": "Core ativado.", "vid": "https://youtu.be/2D7N_fU7Usc"}
    ],
    "TREINO 2: PUSH A (PEITO/OMBRO)": [
        {"ex": "Supino Inclinado Halteres", "sets": ["25kg (15 reps)", "27,5kg (12 reps)", "30kg (10 reps)", "32,5kg (6 reps)"], "bio": "Banco 30º. Escápulas retraídas.", "vid": "https://youtu.be/8iP9S706yLw"},
        {"ex": "Chest Press Articulado", "sets": ["35kg/lado", "40kg/lado", "Drop: 40->25->15"], "bio": "Alça altura mamilo.", "vid": "https://youtu.be/l_i9I-Y8r1U"},
        {"ex": "Desenv. Máquina", "sets": ["25kg/lado", "30kg/lado", "35kg/lado"], "bio": "Punho alinhado.", "vid": "https://youtu.be/WvLMauqrnK8"},
        {"ex": "Voador Peck Deck", "sets": ["54kg", "61kg", "68kg (Iso 10s)"], "bio": "Esmague no centro.", "vid": "https://youtu.be/Xp0NfT_SjG0"},
        {"ex": "Elevação Lateral", "sets": ["15kg", "15kg", "Drop: 16->10->6"], "bio": "Linha do ombro.", "vid": "https://youtu.be/3VkKa2kn07w"},
        {"ex": "Tríceps Corda", "sets": ["25kg", "30kg", "Drop: 32,5->22,5->15"], "bio": "Abra embaixo.", "vid": "https://youtu.be/Yid37u14vH0"},
        {"ex": "Tríceps Francês Polia", "sets": ["15kg", "17,5kg", "20kg (Falha)"], "bio": "Cotovelos fechados.", "vid": "https://youtu.be/S_mU0G0mO-E"}
    ],
    "TREINO 3: PULL A (COSTAS/BÍCEPS)": [
        {"ex": "Puxada Alta Aberta", "sets": ["55kg", "70kg", "77,5kg", "84,5kg"], "bio": "Use STRAPS. Cotovelo guia.", "vid": "https://youtu.be/H75im9fAUMc"},
        {"ex": "Remada Baixa Triângulo", "sets": ["84,5kg", "98,3kg", "103kg"], "bio": "Segure 1s no umbigo.", "vid": "https://youtu.be/lJ7x8S_3uMA"},
        {"ex": "Remada Unilateral Polia", "sets": ["22,5kg", "25kg", "25kg"], "bio": "Tensão constante.", "vid": "https://youtu.be/fM5K60p4S8A"},
        {"ex": "Pulldown Barra/Corda", "sets": ["30kg", "35kg", "35kg (Iso 5s)"], "bio": "Cotovelo quase travado.", "vid": "https://youtu.be/8uS_w8_1I_M"},
        {"ex": "Crucifixo Inverso Máquina", "sets": ["33kg", "40kg", "40kg"], "bio": "Deltoide posterior.", "vid": "https://youtu.be/Xp0NfT_SjG0"},
        {"ex": "Rosca Martelo", "sets": ["15kg", "16kg", "18kg"], "bio": "Pegada neutra.", "vid": "https://youtu.be/zS9_3mE9L6o"},
        {"ex": "Rosca Direta Barra W", "sets": ["35kg (9 reps)", "35kg (7 reps)", "30kg"], "bio": "Mantenha cotovelo fixo.", "vid": "https://youtu.be/Xp0NfT_SjG0"},
        {"ex": "Flexão de Punho", "sets": ["14kg", "15kg", "16kg"], "bio": "Amplitude máxima.", "vid": "https://youtu.be/M_33zK08Nls"}
    ],
    "TREINO 4: LEGS B (POSTERIOR/GLÚTEO)": [
        {"ex": "Cadeira Flexora", "sets": ["54kg", "61kg", "68kg", "Drop 75kg"], "bio": "Tronco inclinado à frente.", "vid": "https://youtu.be/78V9XpS7F7M"},
        {"ex": "Stiff", "sets": ["80kg", "100kg", "120kg"], "bio": "Quadril para trás.", "vid": "https://youtu.be/mD2f_LueIYA"},
        {"ex": "Leg Press (Pés no Topo)", "sets": ["200kg", "240kg", "260kg"], "bio": "Foco no glúteo.", "vid": "https://youtu.be/yZmx_7igYyU"},
        {"ex": "Elevação Pélvica", "sets": ["110kg", "130kg", "150kg"], "bio": "Iso 3s no topo.", "vid": "https://youtu.be/A8nFGuY77CE"},
        {"ex": "Abdução Quadril", "sets": ["75kg", "82kg", "82kg"], "bio": "Tronco à frente.", "vid": "https://youtu.be/yX7t3R7p2p0"},
        {"ex": "Elevação Pernas (Infra)", "sets": ["Set 1", "Set 2", "Set 3"], "bio": "Core ativado.", "vid": "https://youtu.be/Pr1ieGZ5atk"}
    ],
    "TREINO 5: PUSH B (OMBROS 3D/PEITO)": [
        {"ex": "Desenv. Halteres Sentado", "sets": ["20kg", "24kg", "30kg"], "bio": "Banco 80º.", "vid": "https://youtu.be/HzIiIn92_2M"},
        {"ex": "Elevação Lateral Polia", "sets": ["7,5kg", "7,5kg", "10kg"], "bio": "Por trás do corpo.", "vid": "https://youtu.be/3VkKa2kn07w"},
        {"ex": "Supino Inclinado Articulado", "sets": ["25kg/l", "35kg/l", "40kg/l"], "bio": "Foco peito superior.", "vid": "https://youtu.be/5E6V_uT2yS8"},
        {"ex": "Tríceps Pulley Reta", "sets": ["25kg", "30kg", "Drop: 35->20->10"], "bio": "Punho firme.", "vid": "https://youtu.be/2-LAMcpz_OQ"},
        {"ex": "Elevação Frontal Anilha", "sets": ["12,5kg", "15kg", "15kg"], "bio": "Até linha dos olhos.", "vid": "https://youtu.be/xS9v3_S1XnE"},
        {"ex": "Abdominal Crunch Máquina", "sets": ["Set 1", "Set 2", "Set 3"], "bio": "Carga alta.", "vid": "https://youtu.be/2D7N_fU7Usc"}
    ]
}

# --- INTERFACE ---
with st.sidebar:
    st.markdown("### ⚡ Aura Fitness")
    user_email = st.text_input("Identidade (E-mail)", placeholder="seu@email.com").lower().strip()
    btn_login = st.button("Acessar Hall da Fama")

if btn_login or user_email:
    if user_email in [MEU_EMAIL, SAYRA_EMAIL]:
        u_name = "Nilson" if user_email == MEU_EMAIL else "Olá Princess Fitness"
        u_initials = "NH" if user_email == MEU_EMAIL else "SF"
        
        # Header Premium com Nome Personalizado
        st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 30px; padding: 10px;">
                <div style="width: 55px; height: 55px; border-radius: 50%; border: 2px solid #0f49bd; overflow: hidden; background: #1e293b; display: flex; align-items: center; justify-content: center; font-weight: 800; color: white; font-size: 20px;">
                    {u_initials}
                </div>
                <div>
                    <p style="font-size: 10px; color: #94a3b8; font-weight: 800; text-transform: uppercase; margin: 0; letter-spacing: 0.1em;">Bem-vindo de volta,</p>
                    <h1 style="font-size: 24px; margin: 0; font-weight: 800; color: white;">{u_name}</h1>
                </div>
            </div>
        """, unsafe_allow_html=True)

        tab1, tab2, tab3 = st.tabs(["TREINOS", "EVOLUÇÃO", "RANKING"])

        with tab1:
            dia = st.selectbox("Rotina Atual", list(TREINOS_COMPLETOS.keys()))
            for item in TREINOS_COMPLETOS[dia]:
                with st.container():
                    st.markdown(f"""
                        <div class="exercise-card">
                            <span class="status-badge">Força Avançada</span>
                            <h3 style="margin-top: 10px; font-size: 20px;">{item['ex']}</h3>
                            <p style="font-size: 12px; color: #94a3b8;">{item['bio']}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    c_vid, c_data = st.columns([1, 2])
                    with c_vid: st.video(item['vid'])
                    with c_data:
                        for i, meta in enumerate(item['sets']):
                            cols = st.columns([2, 1, 1])
                            cols[0].text_input("Alvo", value=meta if user_email == MEU_EMAIL else "A definir", key=f"t_{item['ex']}_{i}_{dia}")
                            cols[1].number_input("Carga (kg)", key=f"w_{item['ex']}_{i}_{dia}", min_value=0)
                            cols[2].selectbox("Esforço (RPE)", list(range(1,11)), index=7, key=f"r_{item['ex']}_{i}_{dia}")
                    
                    if st.button(f"Concluir {item['ex']}", key=f"btn_{item['ex']}_{dia}"):
                        st.toast(f"Ótimo trabalho! {item['ex']} salvo.", icon="🔥")

        with tab2:
            st.markdown("### 🤖 Coach Inteligente Gemini")
            st.info("O Gemini analisa seu esforço (RPE) e sugere progressão para a próxima semana.")

        with tab3:
            st.markdown("### 🏆 Hall da Fama")
            st.write("Ranking baseado no volume total de carga.")

    else:
        st.warning("Por favor, verifique seu e-mail de acesso.")
