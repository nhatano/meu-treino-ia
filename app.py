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
    h1, h2, h3 { color: #00FF41 !important; }
</style>
""", unsafe_allow_html=True)

# --- CONEXÕES ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-pro')
except:
    st.error("Configure as Secrets no Streamlit Cloud.")

# --- BANCO DE DADOS DE USUÁRIOS ---
MEU_EMAIL = "nhatano@gmail.com" # <--- MUDE PARA O SEU E-MAIL
SAYRA_EMAIL = "sayradan@gmail.com"

# --- ESTRUTURA COMPLETA DE TREINOS ---
TREINOS_COMPLETOS = {
    "SEGUNDA: TREINO 1 - LEGS A (QUADRÍCEPS)": [
        {"ex": "Agachamento Hack", "sets": ["70kg (15 reps)", "100kg (12 reps)", "120kg (10 reps)", "140kg (6-8 reps)"], "vid": "https://youtu.be/0enGC9f_Tpg"},
        {"ex": "Leg Press 45º", "sets": ["220kg (12 reps)", "235kg (10 reps)", "285kg (10 reps)", "Drop: 260->180->100"], "vid": "https://youtu.be/yZmx_7igYyU"},
        {"ex": "Cadeira Adutora", "sets": ["95kg (15 reps)", "100kg (12 reps)", "100kg (Falha)"], "vid": "https://youtu.be/4IStG89y8i4"},
        {"ex": "Cadeira Extensora", "sets": ["47kg (12 reps)", "47kg (12 reps)", "Drop: 54->33->19"], "vid": "https://youtu.be/m0FOpMEgero"},
        {"ex": "Afundo com Halteres", "sets": ["17,5kg/mão (12 passos)", "20kg/mão", "20kg (Até o limite)"], "vid": "https://youtu.be/q7_6v6w9jXs"},
        {"ex": "Panturrilha no Leg (Unilateral)", "sets": ["150kg (15 reps)", "150kg", "150kg (Falha)"], "vid": "https://youtu.be/q_K2eW7mUqI"}
    ],
    "TERÇA: TREINO 2 - PUSH A (PEITO & OMBRO ANT)": [
        {"ex": "Supino Inc. Halteres", "sets": ["25kg (15 reps)", "27,5kg (12 reps)", "30kg (10-12 reps)", "32,5kg (6 reps)"], "vid": "https://youtu.be/8iP9S706yLw"},
        {"ex": "Chest Press Máquina", "sets": ["35kg/lado (8 reps)", "40kg/lado (10 reps)", "Drop: 40->25->15"], "vid": "https://youtu.be/l_i9I-Y8r1U"},
        {"ex": "Desenv. Máquina Articulado", "sets": ["25kg/lado (12 reps)", "30kg/lado (10 reps)", "35kg/lado (10 reps)"], "vid": "https://youtu.be/WvLMauqrnK8"},
        {"ex": "Voador Peck Deck", "sets": ["54kg (15 reps)", "61kg (12 reps)", "68kg (Falha + Isometria)"], "vid": "https://youtu.be/Xp0NfT_SjG0"},
        {"ex": "Elevação Lateral Halteres", "sets": ["15kg (12 reps)", "15kg", "Drop: 16->10->6"], "vid": "https://youtu.be/3VkKa2kn07w"},
        {"ex": "Tríceps Corda", "sets": ["25kg (15 reps)", "30kg (12 reps)", "Drop: 32,5->22,5->15"], "vid": "https://youtu.be/Yid37u14vH0"},
        {"ex": "Tríceps Francês Polia", "sets": ["15kg (12 reps)", "17,5kg", "20kg (7 reps)"], "vid": "https://youtu.be/S_mU0G0mO-E"}
    ],
    "QUARTA: TREINO 3 - PULL A (COSTAS & BÍCEPS)": [
        {"ex": "Puxada Alta Aberta", "sets": ["55kg (15 reps)", "70kg (12 reps)", "77,5kg (10 reps)", "84,5kg (7 reps)"], "vid": "https://youtu.be/H75im9fAUMc"},
        {"ex": "Remada Baixa Triângulo", "sets": ["84,5kg (12 reps)", "98,3kg (10 reps)", "103kg (7 reps)"], "vid": "https://youtu.be/lJ7x8S_3uMA"},
        {"ex": "Remada Unilateral Polia", "sets": ["22,5kg", "25kg", "25kg (Falha)"], "vid": "https://youtu.be/fM5K60p4S8A"},
        {"ex": "Pulldown Barra/Corda", "sets": ["30kg (15 reps)", "35kg", "35kg (Isometria 5s)"], "vid": "https://youtu.be/8uS_w8_1I_M"},
        {"ex": "Rosca Martelo", "sets": ["15kg (12 reps)", "16kg (12 reps)", "18kg (8 reps)"], "vid": "https://youtu.be/zS9_3mE9L6o"},
        {"ex": "Rosca Direta Barra W", "sets": ["35kg (9 reps)", "35kg (7 reps)", "30kg (Falha)"], "vid": "https://youtu.be/Xp0NfT_SjG0"}
    ],
    "SEXTA: TREINO 4 - LEGS B (POSTERIOR & GLÚTEO)": [
        {"ex": "Cadeira Flexora", "sets": ["54kg (15 reps)", "61kg (15 reps)", "68kg (12 reps)", "Drop 75kg"], "vid": "https://youtu.be/78V9XpS7F7M"},
        {"ex": "Stiff", "sets": ["80kg (12 reps)", "100kg (10 reps)", "120kg (Falha)"], "vid": "https://youtu.be/mD2f_LueIYA"},
        {"ex": "Leg Press (Pés no Topo)", "sets": ["200kg (15 reps)", "240kg (12 reps)", "260kg (Falha)"], "vid": "https://youtu.be/yZmx_7igYyU"},
        {"ex": "Elevação Pélvica", "sets": ["110kg (12 reps)", "130kg (10 reps)", "150kg (PR)"], "vid": "https://youtu.be/A8nFGuY77CE"},
        {"ex": "Panturrilha Sentado", "sets": ["240kg (15 reps)", "240kg (18 reps)", "240kg (Falha)"], "vid": "https://youtu.be/q_K2eW7mUqI"}
    ],
    "SÁBADO: TREINO 5 - PUSH B (OMBROS 3D & PEITO)": [
        {"ex": "Desenvolvimento Halteres", "sets": ["20kg (12 reps)", "24kg (10 reps)", "30kg (PR)"], "vid": "https://youtu.be/HzIiIn92_2M"},
        {"ex": "Elevação Lateral Polia", "sets": ["7,5kg (15 reps)", "7,5kg (12 reps)", "10kg (Falha)"], "vid": "https://youtu.be/3VkKa2kn07w"},
        {"ex": "Supino Inclinado Articulado", "sets": ["25kg/lado (12 reps)", "35kg/lado (10 reps)", "40kg/lado (10 reps)"], "vid": "https://youtu.be/5E6V_uT2yS8"},
        {"ex": "Tríceps Pulley Barra Reta", "sets": ["25kg (12 reps)", "30kg (10 reps)", "Drop: 35->20->10"], "vid": "https://youtu.be/2-LAMcpz_OQ"}
    ]
}

# --- INTERFACE ---
with st.sidebar:
    st.title("⚡ GynAI Evolution")
    email_login = st.text_input("Login (E-mail):").lower().strip()
    btn_login = st.button("Carregar Treino")

if email_login in [MEU_EMAIL, SAYRA_EMAIL]:
    u_nome = "CAMPEÃO" if email_login == MEU_EMAIL else "SAYRA"
    st.sidebar.success(f"Logado como: {u_nome}")
    
    escolha = st.sidebar.selectbox("Escolha o Dia", list(TREINOS_COMPLETOS.keys()))
    modo = st.sidebar.radio("Navegação", ["👊 Treinar", "🤖 Coach IA"])

    if modo == "👊 Treinar":
        st.header(f"{escolha}")
        for item in TREINOS_COMPLETOS[escolha]:
            with st.expander(f"🔥 {item['ex']}", expanded=False):
                col_v, col_d = st.columns([1, 2])
                with col_v: st.video(item['vid'])
                with col_d:
                    for i, meta in enumerate(item['sets']):
                        c1, c2, c3 = st.columns([2, 1, 1])
                        c1.write(f"**Série {i+1}** | Alvo: `{meta if email_login == MEU_EMAIL else 'A definir'}`")
                        c2.number_input(f"Carga", key=f"c_{item['ex']}_{i}_{escolha}")
                        c3.selectbox(f"RPE", list(range(1,11)), index=7, key=f"r_{item['ex']}_{i}_{escolha}")
                if st.button(f"Salvar {item['ex']}", key=f"btn_{item['ex']}_{escolha}"):
                    st.success("Registrado!")

    elif modo == "🤖 Coach IA":
        st.header("🤖 Analista Gemini")
        duvida = st.text_area("Dúvida técnica?")
        if st.button("Consultar"):
            resp = model.generate_content(f"Aluno avançado {u_nome}. Dúvida: {duvida}")
            st.info(resp.text)
else:
    st.info("👋 Digite seu e-mail e clique em 'Carregar Treino'.")
