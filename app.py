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
    h1, h2, h3 { color: #00FF41 !important; margin-bottom: 5px; }
    .meta-label { color: #8B949E; font-size: 0.85rem; }
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
        {"ex": "Tríceps Francês Polia (Média)", "sets": ["15kg (12 reps)", "17,5kg (10 reps)", "20kg (7 reps)"], "bio": "Cotovelos fechados.", "vid": "https://youtu.be/S_mU0G0mO-E"},
        {"ex": "Tríceps Francês Polia (Baixa)", "sets": ["15kg", "17,5kg", "17,5kg (Falha)"], "bio": "Extensão total acima da cabeça.", "vid": "https://youtu.be/S_mU0G0mO-E"}
    ],
    "QUARTA: TREINO 3 - PULL A (COSTAS & BÍCEPS)": [
        {"ex": "Puxada Alta Aberta", "sets": ["55kg (15 reps)", "70kg (12 reps)", "77,5kg (10 reps)", "84,5kg (7 reps)"], "bio": "Use STRAPS. Puxe pelo cotovelo.", "vid": "https://youtu.be/H75im9fAUMc"},
        {"ex": "Remada Baixa Triângulo", "sets": ["84,5kg (12 reps)", "98,3kg (10 reps)", "103kg (7 reps)"], "bio": "Segure 1s no umbigo. Tronco estático.", "vid": "https://youtu.be/lJ7x8S_3uMA"},
        {"ex": "Remada Unilateral Polia Baixa", "sets": ["22,5kg (12 reps)", "25kg", "25kg (Falha)"], "bio": "Tensão constante.", "vid": "https://youtu.be/fM5K60p4S8A"},
        {"ex": "Pulldown (Barra ou Corda)", "sets": ["30kg (15 reps)", "35kg (12 reps)", "35kg (Falha + 5s iso)"], "bio": "Cotovelo quase travado.", "vid": "https://youtu.be/8uS_w8_1I_M"},
        {"ex": "Crucifixo Inverso Máquina", "sets": ["33kg (15 reps)", "40kg (12 reps)", "40kg (Falha)"], "bio": "Foco no deltoide posterior.", "vid": "https://youtu.be/Xp0NfT_SjG0"},
        {"ex": "Rosca Martelo", "sets": ["15kg (12 reps)", "16kg (12 reps)", "18kg (8 reps)"], "bio": "Pegada neutra.", "vid": "https://youtu.be/zS9_3mE9L6o"},
        {"ex": "Rosca Direta Barra W", "sets": ["35kg (9 reps)", "35kg (7 reps)", "30kg (Falha)"], "bio": "Mantenha o cotovelo fixo.", "vid": "https://youtu.be/Xp0NfT_SjG0"},
        {"ex": "Flexão de Punho", "sets": ["14kg (12 reps)", "15kg (10 reps)", "16kg (Falha)"], "bio": "Amplitude máxima de punho.", "vid": "https://youtu.be/M_33zK08Nls"},
        {"ex": "Abdominal na Polia", "sets": ["25kg", "27,5kg", "27,5kg (Falha)"], "bio": "Enrole a coluna.", "vid": "https://youtu.be/2D7N_fU7Usc"}
    ],
    "SEXTA: TREINO 4 - LEGS B (POSTERIOR & GLÚTEO)": [
        {"ex": "Cadeira Flexora", "sets": ["54kg (15 reps)", "61kg (15 reps)", "68kg (12 reps)", "Drop 75kg"], "bio": "Tronco inclinado à frente.", "vid": "https://youtu.be/78V9XpS7F7M"},
        {"ex": "Stiff (Halteres ou Hack)", "sets": ["80kg (12 reps)", "100kg (10 reps)", "120kg (Falha)"], "bio": "Quadril para trás. Raspe na perna.", "vid": "https://youtu.be/mD2f_LueIYA"},
        {"ex": "Leg Press (Pés no Topo)", "sets": ["200kg (15 reps)", "240kg (12 reps)", "260kg (Falha)"], "bio": "Foco total em glúteo. Empurre pelo calcanhar.", "vid": "https://youtu.be/yZmx_7igYyU"},
        {"ex": "Elevação Pélvica", "sets": ["110kg (12 reps)", "130kg (10 reps)", "150kg (PR)"], "bio": "Isometria de 3s no topo.", "vid": "https://youtu.be/A8nFGuY77CE"},
        {"ex": "Abdução de Quadril", "sets": ["75kg (15 reps)", "82kg (12 reps)", "82kg (Falha)"], "bio": "Tronco à frente.", "vid": "https://youtu.be/yX7t3R7p2p0"},
        {"ex": "Panturrilha no Leg", "sets": ["240kg (15 reps)", "240kg (18 reps)", "240kg (Falha)"], "bio": "Ponta dos pés.", "vid": "https://youtu.be/q_K2eW7mUqI"},
        {"ex": "Elevação de Pernas (Infra)", "sets": ["3 Sets até a falha"], "bio": "Core ativado.", "vid": "https://youtu.be/Pr1ieGZ5atk"}
    ],
    "SÁBADO: TREINO 5 - PUSH B (OMBROS 3D & PEITO)": [
        {"ex": "Desenv. Halteres (Sentado)", "sets": ["20kg (12 reps)", "24kg (10 reps)", "30kg (PR)"], "bio": "Banco a 80º.", "vid": "https://youtu.be/HzIiIn92_2M"},
        {"ex": "Elevação Lateral Polia (Por trás)", "sets": ["7,5kg (15 reps)", "7,5kg (12 reps)", "10kg (Falha)"], "bio": "Tensão constante.", "vid": "https://youtu.be/3VkKa2kn07w"},
        {"ex": "Supino Inclinado Articulado", "sets": ["25kg/lado (12 reps)", "35kg/lado (10 reps)", "40kg/lado (10 reps)"], "bio": "Foco no peito superior.", "vid": "https://youtu.be/5E6V_uT2yS8"},
        {"ex": "Crucifixo Inverso Máquina", "sets": ["33kg (15 reps)", "40kg (12 reps)", "40kg (Falha)"], "bio": "Deltoide posterior.", "vid": "https://youtu.be/Xp0NfT_SjG0"},
        {"ex": "Elevação Frontal com Anilha", "sets": ["12,5kg (12 reps)", "15kg", "15kg (Falha)"], "bio": "Suba até a linha do olho.", "vid": "https://youtu.be/xS9v3_S1XnE"},
        {"ex": "Tríceps Pulley Barra Reta", "sets": ["25kg (12 reps)", "30kg (10 reps)", "Drop: 35->20->10"], "bio": "Punho firme.", "vid": "https://youtu.be/2-LAMcpz_OQ"},
        {"ex": "Tríceps Francês Polia (Média)", "sets": ["15kg", "17,5kg", "20kg (Falha)"], "bio": "Cuidado com o ombro.", "vid": "https://youtu.be/S_mU0G0mO-E"},
        {"ex": "Tríceps Francês Polia (Baixa)", "sets": ["15kg", "17,5kg", "20kg (Falha)"], "bio": "Extensão vertical.", "vid": "https://youtu.be/S_mU0G0mO-E"},
        {"ex": "Abdominal Crunch Máquina", "sets": ["3 Sets até a falha (Carga alta)"], "bio": "Enrole o abdômen.", "vid": "https://youtu.be/2D7N_fU7Usc"}
    ]
}

# --- INTERFACE ---
with st.sidebar:
    st.title("⚡ GynAI Evolution")
    email_login = st.text_input("Login (E-mail):").lower().strip()
    btn_login = st.button("Carregar Treino")

if email_login in [MEU_EMAIL, SAYRA_EMAIL]:
    u_nome = "NHATANO" if email_login == MEU_EMAIL else "SAYRA"
    st.sidebar.success(f"Logado como: {u_nome}")
    
    escolha = st.sidebar.selectbox("Escolha o Dia", list(TREINOS_COMPLETOS.keys()))
    modo = st.sidebar.radio("Navegação", ["👊 Treinar Agora", "📈 Exportar Dados", "🤖 Coach IA"])

    if modo == "👊 Treinar Agora":
        st.header(f"{escolha}")
        for item in TREINOS_COMPLETOS[escolha]:
            with st.expander(f"🔥 {item['ex']}", expanded=False):
                st.markdown(f"**Biomecânica:** {item['bio']}")
                col_v, col_d = st.columns([1, 2])
                with col_v: st.video(item['vid'])
                with col_d:
                    for i, meta in enumerate(item['sets']):
                        c1, c2, c3 = st.columns([1.5, 1, 1])
                        # CAMPO EDITÁVEL PARA CARGA ALVO
                        c1.text_input(f"Alvo Série {i+1}", value=meta if email_login == MEU_EMAIL else "A definir", key=f"alvo_{item['ex']}_{i}_{escolha}")
                        # CAMPO PARA REGISTRO REAL
                        c2.number_input(f"Fiz com (kg)", key=f"c_{item['ex']}_{i}_{escolha}", min_value=0)
                        # RPE
                        c3.selectbox(f"RPE", list(range(1,11)), index=7, key=f"r_{item['ex']}_{i}_{escolha}")
                if st.button(f"Salvar {item['ex']}", key=f"btn_{item['ex']}_{escolha}"):
                    st.success(f"Registro de {item['ex']} realizado!")

    elif modo == "📈 Exportar Dados":
        st.header("📊 Exportação de Dados")
        try:
            df = conn.read(worksheet="Historico")
            user_df = df[df['Usuario'] == email_login]
            csv = user_df.to_csv(index=False).encode('utf-8')
            st.download_button("Baixar Histórico CSV", csv, "treino.csv", "text/csv")
        except:
            st.warning("Sem dados históricos.")

    elif modo == "🤖 Coach IA":
        st.header("🤖 Coach Gemini")
        duvida = st.text_area("Dúvida técnica:")
        if st.button("Consultar"):
            resp = model.generate_content(f"Aluno {u_nome}. {duvida}")
            st.info(resp.text)
else:
    st.info("👋 Digite seu e-mail e clique em 'Carregar Treino'.")
