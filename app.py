import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import google.generativeai as genai
from datetime import datetime

# --- DESIGN E CONFIGURAÇÃO ---
st.set_page_config(page_title="GynAI Evolution PRO", layout="wide")

st.markdown("""
<style>
    .main { background-color: #0E1117; }
    .exercise-card {
        background-color: #1E2129; border-radius: 15px; padding: 20px;
        margin-bottom: 10px; border-left: 6px solid #00FF41;
    }
    .set-row {
        background-color: #262730; padding: 10px; border-radius: 8px;
        margin-bottom: 5px; border: 1px solid #444;
    }
    .stCheckbox { font-size: 18px; }
</style>
""", unsafe_allow_html=True)

# --- CONEXÃO ---
conn = st.connection("gsheets", type=GSheetsConnection)

# --- BASE DE DADOS DE TREINO (DETALHADO SÉRIE POR SÉRIE) ---
# Exemplo com os dados que você enviou
TREINOS_DETALHADOS = {
    "Segunda: Legs A (Quadríceps)": [
        {
            "ex": "Agachamento Hack",
            "series": [
                {"label": "Série 1: Aquecimento", "carga": "70kg", "reps": "15"},
                {"label": "Série 2: Calibragem", "carga": "100kg", "reps": "12"},
                {"label": "Série 3: Consolidar PR", "carga": "120kg", "reps": "10"},
                {"label": "Série 4: NOVO DEPLOY", "carga": "140kg", "reps": "6-8"}
            ],
            "vid": "https://www.youtube.com/watch?v=0enGC9f_Tpg"
        },
        {
            "ex": "Leg Press 45º",
            "series": [
                {"label": "Série 1", "carga": "220kg", "reps": "12"},
                {"label": "Série 2", "carga": "235kg", "reps": "10"},
                {"label": "Série 3: Evolução", "carga": "285kg", "reps": "10"},
                {"label": "Série 4: Drop-set", "carga": "260kg -> 100kg", "reps": "Falha"}
            ],
            "vid": "https://www.youtube.com/watch?v=yZmx_7igYyU"
        }
    ],
    "Terça: Push A (Peito/Ombro)": [
        {
            "ex": "Supino Inclinado Halteres",
            "series": [
                {"label": "Série 1", "carga": "25kg", "reps": "15"},
                {"label": "Série 2", "carga": "27,5kg", "reps": "12"},
                {"label": "Série 3: Consolidação", "carga": "30kg", "reps": "10-12"},
                {"label": "Série 4: Falha Total", "carga": "32,5kg", "reps": "6"}
            ],
            "vid": "https://www.youtube.com/watch?v=8iP9S706yLw"
        }
    ]
    # Adicione os outros treinos seguindo este mesmo padrão
}

# --- INTERFACE ---
st.sidebar.title("⚡ GynAI Evolution")
email = st.sidebar.text_input("Login (E-mail)")

if email:
    aba = st.sidebar.selectbox("Escolha o Treino", list(TREINOS_DETALHADOS.keys()))
    
    st.header(f"🏋️ {aba}")
    
    for item in TREINOS_DETALHADOS[aba]:
        with st.expander(f"🔥 {item['ex']}", expanded=True):
            st.video(item['vid'])
            
            st.write("---")
            # Loop pelas séries específicas do exercício
            for i, s in enumerate(item['series']):
                col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
                with col1:
                    st.markdown(f"**{s['label']}**")
                with col2:
                    st.markdown(f"🎯 Alvo: `{s['carga']}`")
                with col3:
                    real = st.number_input(f"Carga Feita (kg)", key=f"real_{item['ex']}_{i}")
                with col4:
                    check = st.checkbox("OK", key=f"check_{item['ex']}_{i}")
            
            if st.button(f"Salvar Treino de {item['ex']}"):
                st.success(f"Dados de {item['ex']} enviados para a planilha!")

else:
    st.info("Digite seu e-mail para carregar seu plano de séries.")
