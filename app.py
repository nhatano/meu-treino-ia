import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import google.generativeai as genai
from datetime import datetime

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="GynAI Evolution PRO", layout="wide")

# --- CSS CUSTOMIZADO (DESIGN DARK PREMIUM) ---
st.markdown("""
<style>
    .main { background-color: #0E1117; }
    .stApp { color: #FFFFFF; }
    .exercise-card {
        background-color: #1E2129;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 20px;
        border-left: 6px solid #00FF41;
        box-shadow: 3px 3px 15px rgba(0,0,0,0.4);
    }
    .stButton>button {
        background-color: #00FF41; color: black; font-weight: bold; border-radius: 10px; height: 3em;
    }
    .stTextInput>div>div>input { background-color: #262730; color: white; }
    h3 { color: #00FF41; margin-bottom: 5px; }
    .badge { background-color: #343541; padding: 4px 10px; border-radius: 5px; font-size: 12px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- INICIALIZAÇÃO DE CONEXÕES ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-pro')
except:
    st.error("Erro de conexão. Verifique as 'Secrets' no painel do Streamlit.")

# --- DICIONÁRIO DE TREINOS ---
TREINOS = {
    "Segunda: Legs A (Quadríceps)": [
        {"ex": "Agachamento Hack", "target": "130kg-140kg", "sets": "4", "vid": "https://www.youtube.com/watch?v=0enGC9f_Tpg"},
        {"ex": "Leg Press 45º", "target": "285kg", "sets": "4", "vid": "https://www.youtube.com/watch?v=yZmx_7igYyU"},
        {"ex": "Cadeira Extensora", "target": "54kg", "sets": "3 (Drop-set)", "vid": "https://www.youtube.com/watch?v=m0FOpMEgero"}
    ],
    "Terça: Push A (Peito/Ombro)": [
        {"ex": "Supino Inc. Halteres", "target": "32.5kg", "sets": "4", "vid": "https://www.youtube.com/watch?v=8iP9S706yLw"},
        {"ex": "Desenv. Articulado", "target": "35kg/lado", "sets": "3", "vid": "https://www.youtube.com/watch?v=WvLMauqrnK8"},
        {"ex": "Elevação Lateral", "target": "16kg", "sets": "3 (Drop-set)", "vid": "https://www.youtube.com/watch?v=3VkKa2kn07w"}
    ],
    "Quarta: Pull A (Costas/Bíceps)": [
        {"ex": "Puxada Alta Aberta", "target": "84.5kg", "sets": "4", "vid": "https://www.youtube.com/watch?v=H75im9fAUMc"},
        {"ex": "Remada Baixa Triângulo", "target": "103kg", "sets": "3", "vid": "https://www.youtube.com/watch?v=lJ7x8S_3uMA"},
        {"ex": "Rosca Direta Barra W", "target": "35kg", "sets": "3", "vid": "https://www.youtube.com/watch?v=Xp0NfT_SjG0"}
    ],
    "Sexta: Legs B (Posterior/Glúteo)": [
        {"ex": "Cadeira Flexora", "target": "75kg", "sets": "4", "vid": "https://www.youtube.com/watch?v=78V9XpS7F7M"},
        {"ex": "Stiff Halteres", "target": "120kg", "sets": "3", "vid": "https://www.youtube.com/watch?v=mD2f_LueIYA"},
        {"ex": "Elevação Pélvica", "target": "150kg", "sets": "3", "vid": "https://www.youtube.com/watch?v=A8nFGuY77CE"}
    ],
    "Sábado: Push B (Ombros 3D/Peito)": [
        {"ex": "Desenv. Halteres Sentado", "target": "30kg", "sets": "3", "vid": "https://www.youtube.com/watch?v=HzIiIn92_2M"},
        {"ex": "Supino Inc. Articulado", "target": "40kg/lado", "sets": "3", "vid": "https://www.youtube.com/watch?v=5E6V_uT2yS8"},
        {"ex": "Tríceps Pulley", "target": "35kg", "sets": "3", "vid": "https://www.youtube.com/watch?v=2-LAMcpz_OQ"}
    ]
}

# --- INTERFACE ---
st.sidebar.title("⚡ GynAI Evolution")
email = st.sidebar.text_input("Login (E-mail)")

if email:
    aba = st.sidebar.selectbox("Escolha o Treino", list(TREINOS.keys()))
    modo = st.sidebar.radio("Ir para", ["Treinar Agora", "Análise do Coach IA"])

    if modo == "Treinar Agora":
        st.header(f"🏋️ {aba}")
        for item in TREINOS[aba]:
            with st.container():
                st.markdown(f"""<div class="exercise-card">
                    <span class="badge">{item['sets']} Sets</span>
                    <h3>{item['ex']}</h3>
                    <p>Meta Anterior: <b>{item['target']}</b></p>
                </div>""", unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns([1, 1, 2])
                with col1: carga = st.number_input(f"Carga (kg)", key=f"c_{item['ex']}")
                with col2: rpe = st.select_slider(f"Esforço (RPE)", options=list(range(1,11)), value=8, key=f"r_{item['ex']}")
                with col3: st.video(item['vid'])
                
                if st.button(f"Registrar {item['ex']}"):
                    # Lógica simplificada de registro (Aqui você conectaria ao Sheets real)
                    st.toast(f"{item['ex']} Salvo com sucesso!", icon="✅")

    elif modo == "Análise do Coach IA":
        st.header("🤖 Coach Gemini Intelligence")
        pergunta = st.text_area("Dúvida técnica (ex: Posso trocar a corda pela barra reta no Pulldown?)")
        if st.button("Perguntar ao Coach"):
            with st.spinner("Analisando biomecânica..."):
                prompt = f"O aluno treina em nível avançado. Contexto: {pergunta}. Responda de forma técnica e motivadora."
                response = model.generate_content(prompt)
                st.info(response.text)
else:
    st.info("💡 Digite seu e-mail na esquerda para acessar sua planilha de treinos.")
