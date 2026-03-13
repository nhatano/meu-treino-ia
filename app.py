import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import google.generativeai as genai
from datetime import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="GynAI Evolution Pro", layout="wide", page_icon="⚡")

# --- CSS PARA LAYOUT PREMIUM ---
st.markdown("""
<style>
    .main { background-color: #0E1117; }
    .stApp { color: #FFFFFF; }
    [data-testid="stSidebar"] { background-color: #161B22; border-right: 1px solid #30363D; }
    .exercise-card {
        background-color: #1C2128; border-radius: 15px; padding: 20px;
        margin-bottom: 20px; border: 1px solid #30363D; border-left: 5px solid #00FF41;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.5);
    }
    .stButton>button { width: 100%; background: linear-gradient(90deg, #00FF41 0%, #00D136 100%); color: black; font-weight: 800; border-radius: 10px; border: none; }
    h1, h2, h3 { color: #00FF41 !important; margin-bottom: 0px; }
    .meta-text { color: #8B949E; font-size: 0.9rem; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

# --- CONEXÕES ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-pro')
except:
    st.error("Erro nas conexões. Verifique as 'Secrets' no Streamlit Cloud.")

# --- BANCO DE DADOS DE USUÁRIOS ---
MEU_EMAIL = "nhatano@gmail.com" 
SAYRA_EMAIL = "sayradan@gmail.com"

# --- ESTRUTURA COMPLETA DE TREINOS ---
TREINOS_COMPLETOS = {
    "SEGUNDA: TREINO 1 - LEGS A (QUADRÍCEPS)": [
        {"ex": "Agachamento Hack", "sets": ["70kg (15 reps)", "100kg (12 reps)", "120kg (10 reps)", "140kg (6-8 reps)"], "bio": "Pés baixos na plataforma. 3s na descida.", "vid": "https://youtu.be/0enGC9f_Tpg"},
        {"ex": "Leg Press 45º", "sets": ["220kg (12 reps)", "235kg (10 reps)", "285kg (10 reps)", "Drop: 260->180->100"], "bio": "Amplitude máxima. Empurre com o calcanhar.", "vid": "https://youtu.be/yZmx_7igYyU"},
        {"ex": "Cadeira Adutora", "sets": ["95kg (15 reps)", "100kg (12 reps)", "100kg (Falha Total)"], "bio": "3s para abrir, 3s para fechar.", "vid": "https://youtu.be/4IStG89y8i4"},
        {"ex": "Cadeira Extensora", "sets": ["47kg (12 reps)", "47kg (12 reps)", "Drop: 54->33->19"], "bio": "Isometria de 2s no topo.", "vid": "https://youtu.be/m0FOpMEgero"},
        {"ex": "Afundo com Halteres", "sets": ["17,5kg/mão (12 passos)", "20kg/mão (10 passos)", "20kg (Limite cardio)"], "bio": "Tronco ligeiramente à frente.", "vid": "https://youtu.be/q7_6v6w9jXs"},
        {"ex": "Panturrilha no Leg (Unilateral)", "sets": ["150kg (15 reps)", "150kg", "150kg (Falha)"], "bio": "Alongamento máximo na descida.", "vid": "https://youtu.be/q_K2eW7mUqI"},
        {"ex": "Abdominal na Polia Média", "sets": ["Set 1 (1 min)", "Set 2 (1 min)", "Set 3 (Falha)"], "bio": "Foco na contração do core.", "vid": "https://youtu.be/2D7N_fU7Usc"}
    ],
    "TERÇA: TREINO 2 - PUSH A (PEITO & OMBRO ANT)": [
        {"ex": "Supino Inc. Halteres", "sets": ["25kg (15 reps)", "27,5kg (12 reps)", "30kg (10-12 reps)", "32,5kg (6 reps)"], "bio": "Banco a 30º. Escápulas retraídas.", "vid": "https://youtu.be/8iP9S706yLw"},
        {"ex": "Chest Press Articulado", "sets": ["35kg/lado (8 reps)", "40kg/lado (10 reps)", "Drop: 40->25->15"], "bio": "Alça na altura do mamilo.", "vid": "https://youtu.be/l_i9I-Y8r1U"},
        {"ex": "Desenv. Máquina Articulado", "sets": ["25kg/lado (12 reps)", "30kg/lado (10 reps)", "35kg/lado (10 reps)"], "bio": "Punho alinhado com cotovelo.", "vid": "https://youtu.be/WvLMauqrnK8"},
        {"ex": "Voador Peck Deck", "sets": ["54kg (15 reps)", "61kg (12 reps)", "68kg (Falha + 10s isometria)"], "bio": "Esmague o peito no centro.", "vid": "https://youtu.be/Xp0NfT_SjG0"},
        {"ex": "Elevação Lateral Halteres", "sets": ["15kg (12 reps)", "15kg", "Drop: 16->10->6"], "bio": "Não suba além da linha do ombro.", "vid": "https://youtu.be/3VkKa2kn07w"},
        {"ex": "Tríceps Corda", "sets": ["25kg (15 reps)", "30kg (12 reps)", "Drop: 32,5->22,5->15"], "bio": "Abra a corda embaixo.", "vid": "https://youtu.be/Yid37u14vH0"},
        {"ex": "Tríceps Francês Polia (Média)", "sets": ["15kg (12 reps)", "17,5kg (10 reps)", "20kg (7 reps)"], "bio": "Cotovelos fechados.", "vid": "
