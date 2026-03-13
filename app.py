import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import google.generativeai as genai
from datetime import datetime

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="GynAI Evolution - Family Edition", layout="wide")

# --- CONEXÕES ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-pro')
except:
    st.error("Erro nas conexões. Verifique as Secrets.")

# --- BANCO DE DADOS DE TREINOS ---
# Substitua 'seu_email@gmail.com' pelo seu e-mail real
MEU_EMAIL = "seu_email@gmail.com" 
EMAIL_SAYRA = "sayradan@gmail.com"

TREINOS_DADOS = {
    MEU_EMAIL: {
        "Segunda: Legs A (Quadríceps)": [
            {"ex": "Agachamento Hack", "series": [{"l": "Série 1", "m": "70kg"}, {"l": "Série 2", "m": "100kg"}, {"l": "Série 3", "m": "120kg"}, {"l": "Série 4", "m": "140kg"}], "v": "https://www.youtube.com/watch?v=0enGC9f_Tpg"},
            {"ex": "Leg Press 45º", "series": [{"l": "Série 1", "m": "220kg"}, {"l": "Série 2", "m": "235kg"}, {"l": "Série 3", "m": "285kg"}], "v": "https://www.youtube.com/watch?v=yZmx_7igYyU"}
        ],
        "Terça: Push A (Peito/Ombro)": [
            {"ex": "Supino Inc. Halteres", "series": [{"l": "Série 1", "m": "25kg"}, {"l": "Série 2", "m": "27,5kg"}, {"l": "Série 3", "m": "32,5kg"}], "v": "https://www.youtube.com/watch?v=8iP9S706yLw"}
        ]
    },
    EMAIL_SAYRA: {
        "Segunda: Legs A (Quadríceps)": [
            {"ex": "Agachamento Hack", "series": [{"l": "Série 1", "m": "A definir"}, {"l": "Série 2", "m": "A definir"}], "v": "https://www.youtube.com/watch?v=0enGC9f_Tpg"},
            {"ex": "Leg Press 45º", "series": [{"l": "Série 1", "m": "A definir"}], "v": "https://www.youtube.com/watch?v=yZmx_7igYyU"}
        ]
    }
}

# --- INTERFACE ---
st.sidebar.title("⚡ GynAI Evolution")
email_login = st.sidebar.text_input("Digite seu e-mail para treinar:").lower().strip()

if email_login in [MEU_EMAIL, EMAIL_SAYRA]:
    usuario_nome = "CAMPEÃO" if email_login == MEU_EMAIL else "SAYRA"
    st.sidebar.success(f"Logado como: {usuario_nome}")
    
    # Seletor de Treino baseado no usuário
    treinos_disponiveis = TREINOS_DADOS[email_login]
    aba_treino = st.sidebar.selectbox("Selecione o Treino", list(treinos_disponiveis.keys()))
    
    menu = st.sidebar.radio("Navegação", ["Treinar Agora", "Coach IA"])

    if menu == "Treinar Agora":
        st.header(f"🏋️ {aba_treino}")
        
        for item in treinos_disponiveis[aba_treino]:
            with st.expander(f"🔥 {item['ex']}", expanded=True):
                st.video(item['v'])
                cargas_lista = []
                
                for i, s in enumerate(item['series']):
                    col1, col2, col3 = st.columns([2,1,1])
                    col1.write(f"**{s['l']}** | Meta: `{s['m']}`")
                    c_real = col2.number_input(f"Carga Feita", key=f"{email_login}_{item['ex']}_{i}")
                    cargas_lista.append(c_real)
                
                if st.button(f"Salvar {item['ex']}", key=f"btn_{item['ex']}"):
                    # Lógica para salvar cada série individualmente
                    # Para salvar no Sheets real, use: conn.create(worksheet="Historico", data=df)
                    st.success(f"Treino de {item['ex']} registrado para {usuario_nome}!")

    elif menu == "Coach IA":
        st.header("🤖 Coach Gemini")
        duvida = st.text_input("Qual sua dúvida sobre o treino de hoje?")
        if st.button("Analisar"):
            res = model.generate_content(f"Usuário {usuario_nome} perguntou: {duvida}. Responda como um personal trainer.")
            st.info(res.text)
else:
    st.warning("E-mail não autorizado. Adicione seu e-mail no código do GitHub.")
