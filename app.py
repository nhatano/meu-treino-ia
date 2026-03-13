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
        background-color: #1C2128;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid #30363D;
        border-left: 5px solid #00FF41;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.5);
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #00FF41 0%, #00D136 100%);
        color: black;
        font-weight: 800;
        border-radius: 10px;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); color: white; }
    h1, h2, h3 { color: #00FF41 !important; }
</style>
""", unsafe_allow_html=True)

# --- CONEXÕES ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-pro')
except:
    st.error("Configure 'GEMINI_API_KEY' e o link da planilha nas Secrets.")

# --- DADOS DOS TREINOS (SEUS E DA SAYRA) ---
MEU_EMAIL = "nhatano@gmail.com" # <--- SUBSTITUA PELO SEU
SAYRA_EMAIL = "sayradan@gmail.com"

# Estrutura base de exercícios (A, B, C, D, E)
TREINOS_MASTER = {
    "TREINO 1: LEGS A (Quadríceps)": [
        {"ex": "Agachamento Hack", "sets": ["70kg (15reps)", "100kg (12reps)", "120kg (10reps)", "140kg (6-8reps)"], "vid": "https://youtu.be/0enGC9f_Tpg"},
        {"ex": "Leg Press 45º", "sets": ["220kg (12reps)", "235kg (10reps)", "285kg (10reps)", "Drop: 260->180->100"], "vid": "https://youtu.be/yZmx_7igYyU"},
        {"ex": "Cadeira Extensora", "sets": ["47kg (12reps)", "47kg (12reps)", "Drop: 54->33->19"], "vid": "https://youtu.be/m0FOpMEgero"}
    ],
    "TREINO 2: PUSH A (Peito/Ombro)": [
        {"ex": "Supino Inc. Halteres", "sets": ["25kg (15reps)", "27.5kg (12reps)", "30kg (10reps)", "32.5kg (6reps)"], "vid": "https://youtu.be/8iP9S706yLw"},
        {"ex": "Desenv. Articulado", "sets": ["25kg/l (12reps)", "30kg/l (10reps)", "35kg/l (10reps)"], "vid": "https://youtu.be/WvLMauqrnK8"},
        {"ex": "Elevação Lateral Halteres", "sets": ["15kg (12reps)", "15kg (12reps)", "Drop: 16->10->6"], "vid": "https://youtu.be/3VkKa2kn07w"}
    ],
    "TREINO 3: PULL A (Costas/Bíceps)": [
        {"ex": "Puxada Alta Aberta", "sets": ["55kg (15reps)", "70kg (12reps)", "77.5kg (10reps)", "84.5kg (7reps)"], "vid": "https://youtu.be/H75im9fAUMc"},
        {"ex": "Remada Baixa Triângulo", "sets": ["84.5kg (12reps)", "98.3kg (10reps)", "103kg (7reps)"], "vid": "https://youtu.be/lJ7x8S_3uMA"},
        {"ex": "Rosca Direta Barra W", "sets": ["35kg (9reps)", "35kg (7reps)", "30kg (Falha)"], "vid": "https://youtu.be/Xp0NfT_SjG0"}
    ],
    "TREINO 4: LEGS B (Posterior/Glúteo)": [
        {"ex": "Cadeira Flexora", "sets": ["54kg (15reps)", "61kg (15reps)", "68kg (12reps)", "Drop: 75kg"], "vid": "https://youtu.be/78V9XpS7F7M"},
        {"ex": "Stiff (Halteres/Hack)", "sets": ["80kg (12reps)", "100kg (10reps)", "120kg (Falha)"], "vid": "https://youtu.be/mD2f_LueIYA"},
        {"ex": "Elevação Pélvica", "sets": ["110kg (12reps)", "130kg (10reps)", "150kg (PR)"], "vid": "https://youtu.be/A8nFGuY77CE"}
    ],
    "TREINO 5: PUSH B (Ombros 3D/Peito)": [
        {"ex": "Desenv. Halteres Sentado", "sets": ["20kg (12reps)", "24kg (10reps)", "30kg (PR)"], "vid": "https://youtu.be/HzIiIn92_2M"},
        {"ex": "Supino Inc. Articulado", "sets": ["25kg/l (12reps)", "35kg/l (10reps)", "40kg/l (10reps)"], "vid": "https://youtu.be/5E6V_uT2yS8"},
        {"ex": "Tríceps Pulley Reta", "sets": ["25kg (12reps)", "30kg (10reps)", "Drop: 35->20->10"], "vid": "https://youtu.be/2-LAMcpz_OQ"}
    ]
}

# --- INTERFACE ---
with st.sidebar:
    st.title("⚡ GynAI Evolution")
    email_login = st.text_input("Login (E-mail):").lower().strip()

if email_login in [MEU_EMAIL, SAYRA_EMAIL]:
    u_nome = "VOCÊ" if email_login == MEU_EMAIL else "SAYRA"
    st.sidebar.success(f"Bem-vindo, {u_nome}")
    
    escolha_treino = st.sidebar.selectbox("Selecione o Treino", list(TREINOS_MASTER.keys()))
    modo = st.sidebar.radio("Navegação", ["👊 Treinar Agora", "📈 Histórico", "🤖 Coach IA"])

    if modo == "👊 Treinar Agora":
        st.header(f"{escolha_treino}")
        for item in TREINOS_MASTER[escolha_treino]:
            with st.container():
                st.markdown(f"""<div class='exercise-card'><h3>{item['ex']}</h3></div>""", unsafe_allow_html=True)
                col_v, col_d = st.columns([1, 2])
                with col_v: st.video(item['vid'])
                with col_d:
                    for i, meta in enumerate(item['sets']):
                        c1, c2, c3 = st.columns([2, 1, 1])
                        c1.write(f"**Série {i+1}** | Alvo: `{meta if email_login == MEU_EMAIL else 'A definir'}`")
                        cargo = c2.number_input(f"Carga", key=f"c_{item['ex']}_{i}", min_value=0)
                        rpe = c3.selectbox(f"RPE", list(range(1,11)), index=7, key=f"r_{item['ex']}_{i}")
                
                if st.button(f"Salvar {item['ex']}", key=f"btn_{item['ex']}"):
                    st.success(f"Dados de {item['ex']} salvos na planilha!")

    elif modo == "🤖 Coach IA":
        st.header("🤖 Analista Gemini PRO")
        duvida = st.text_area("Ex: 'Não bati a carga no Hack hoje, o que eu faço?'")
        if st.button("Consultar IA"):
            with st.spinner("Analisando biomecânica..."):
                resp = model.generate_content(f"Aluno {u_nome} nível avançado. Dúvida: {duvida}")
                st.info(resp.text)
else:
    st.info("👋 Por favor, digite seu e-mail para carregar seu treino personalizado.")

