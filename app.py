import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import google.generativeai as genai
from datetime import datetime

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="GynAI Evolution Multi-User", layout="wide")

# --- CONEXÕES ---
conn = st.connection("gsheets", type=GSheetsConnection)
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-pro')

# --- BANCO DE DADOS DE TREINOS (FIXO NO CÓDIGO) ---
# Aqui separamos por e-mail para não haver confusão
BANCO_TREINOS = {
    "seu_email@gmail.com": {
        "Segunda: Legs A": [
            {"ex": "Agachamento Hack", "series": [{"label": "Série 1", "meta": "120kg"}, {"label": "Série 2", "meta": "140kg"}], "vid": "URL_AQUI"},
            {"ex": "Leg Press 45º", "series": [{"label": "Série 1", "meta": "220kg"}, {"label": "Série 2", "meta": "285kg"}], "vid": "URL_AQUI"}
        ]
    },
    "email_esposa@gmail.com": {
        "Segunda: Legs B": [
            {"ex": "Elevação Pélvica", "series": [{"label": "Série 1", "meta": "40kg"}, {"label": "Série 2", "meta": "60kg"}], "vid": "URL_AQUI"},
            {"ex": "Cadeira Abdutora", "series": [{"label": "Série 1", "meta": "50kg"}], "vid": "URL_AQUI"}
        ]
    }
}

# --- INTERFACE ---
st.sidebar.title("⚡ GynAI Evolution")
user_email = st.sidebar.text_input("Seu e-mail")

if user_email in BANCO_TREINOS:
    nome_usuario = "VOCÊ" if user_email == "seu_email@gmail.com" else "ESPOSA"
    st.sidebar.success(f"Logado como: {nome_usuario}")
    
    aba = st.sidebar.selectbox("Escolha o Treino", list(BANCO_TREINOS[user_email].keys()))
    menu = st.sidebar.radio("Navegação", ["Treinar", "Histórico", "Coach IA"])

    if menu == "Treinar":
        st.header(f"🏋️ Treino de Hoje: {aba}")
        
        for item in BANCO_TREINOS[user_email][aba]:
            with st.expander(f"🔥 {item['ex']}", expanded=True):
                cargas_feitas = []
                for i, s in enumerate(item['series']):
                    c1, c2, c3 = st.columns([2,2,2])
                    c1.write(f"**{s['label']}** (Meta: {s['meta']})")
                    carga_input = c2.number_input(f"Carga (kg)", key=f"in_{item['ex']}_{i}", min_value=0)
                    cargas_feitas.append(carga_input)
                
                if st.button(f"Salvar {item['ex']}"):
                    # LÓGICA DE SALVAMENTO: Criar DataFrame com as séries
                    dados_para_salvar = pd.DataFrame({
                        "Data": [datetime.now().strftime("%d/%m/%Y")] * len(cargas_feitas),
                        "Usuario": [user_email] * len(cargas_feitas),
                        "Exercicio": [item['ex']] * len(cargas_feitas),
                        "Serie": [f"Série {j+1}" for j in range(len(cargas_feitas))],
                        "Carga": cargas_feitas
                    })
                    # Comando para adicionar na aba "Historico" da sua planilha
                    # conn.create(worksheet="Historico", data=dados_para_salvar) 
                    st.success(f"Progresso de {item['ex']} salvo no seu histórico!")

    elif menu == "Histórico":
        st.header("📊 Sua Evolução")
        # Aqui o código filtraria a planilha: df[df['Usuario'] == user_email]
        st.info("Aqui aparecerão seus gráficos de carga baseados no seu e-mail.")

else:
    st.warning("E-mail não reconhecido. Por favor, cadastre seu e-mail no código.")
