import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import google.generativeai as genai

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="GynAI Evolution", layout="wide", initial_sidebar_state="expanded")

# --- CSS CUSTOMIZADO (VISUAL PREMIUM) ---
st.markdown("""
<style>
    .main { background-color: #0E1117; }
    .stApp { color: #FFFFFF; }
    div[data-testid="stMetricValue"] { font-size: 1.8rem; color: #00FF41; }
    .exercise-card {
        background-color: #1E2129;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 15px;
        border-left: 5px solid #00FF41;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.3);
    }
    .stButton>button {
        width: 100%;
        background-color: #00FF41;
        color: black;
        font-weight: bold;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# --- CONEXÃO COM GOOGLE SHEETS E GEMINI ---
# Nota: As chaves serão configuradas no painel do Streamlit Cloud depois
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-pro')
except:
    st.error("Configure as Secrets no Streamlit Cloud para conectar ao Banco e IA.")

# --- SIDEBAR / LOGIN ---
with st.sidebar:
    st.title("⚡ GynAI Evolution")
    user_email = st.text_input("Seu e-mail Google", placeholder="exemplo@gmail.com")
    menu = st.sidebar.radio("Navegação", ["Treino do Dia", "Meu Histórico", "Coach IA"])

# --- LÓGICA DE TREINO ---
if user_email:
    if menu == "Treino do Dia":
        st.header(f"💪 Treino de Hoje")
        
        # Exemplo de Card de Exercício
        with st.container():
            st.markdown("""<div class='exercise-card'>
                <h3>1. Supino Reto com Barra</h3>
                <p>🎯 Peitoral | 4 Séries x 10-12 Reps</p>
            </div>""", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1: carga = st.number_input("Carga (kg)", step=1, key="sup_c")
            with col2: rpe = st.slider("Percepção (RPE)", 1, 10, 7, key="sup_r")
            with col3: st.video("https://www.youtube.com/watch?v=sqOw2Y6u9as") # Exemplo
            
            if st.button("Salvar Set", key="btn_sup"):
                # Lógica para salvar no Google Sheets via conn.create()
                st.success("Set registrado no histórico!")

    elif menu == "Coach IA":
        st.header("🤖 Analista Gemini")
        if st.button("Analisar meu progresso semanal"):
            with st.spinner("O Gemini está analisando seus dados..."):
                # Aqui o código leria o DataFrame do Sheets e enviaria ao Gemini
                response = model.generate_content(f"Usuário {user_email} treinou Supino com {carga}kg e RPE {rpe}. Dê uma dica curta de progressão.")
                st.info(response.text)

else:
    st.warning("Por favor, insira seu e-mail na barra lateral para começar.")