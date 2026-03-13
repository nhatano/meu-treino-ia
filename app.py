import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Lindos Shape Pro", layout="wide", page_icon="⚡")

# --- DESIGN PREMIUM MOBILE-FIRST ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700;800&display=swap');
    html, body, [data-testid="stAppViewContainer"] { font-family: 'Manrope', sans-serif; background-color: #020617; color: #f8fafc; }
    
    .exercise-card { 
        background: rgba(30, 41, 59, 0.4); 
        backdrop-filter: blur(16px); 
        border: 1px solid rgba(255, 255, 255, 0.05); 
        border-radius: 1.2rem; 
        padding: 1.2rem; 
        margin-bottom: 1rem; 
        border-left: 6px solid #0f49bd; 
    }

    /* Botão de Salvar (Azul Forte) */
    .stButton>button { 
        background: #0f49bd !important; 
        color: white !important; 
        border-radius: 0.8rem !important; 
        font-weight: 800 !important; 
        height: 3.5rem !important; 
        width: 100% !important; 
        border: none !important; 
    }

    /* Botão de Vídeo (Estilo Outline Premium) */
    .stLinkButton>a {
        background-color: transparent !important;
        color: #3b82f6 !important;
        border: 2px solid #3b82f6 !important;
        border-radius: 0.8rem !important;
        font-weight: 700 !important;
        height: 3rem !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-decoration: none !important;
        margin-bottom: 15px !important;
    }

    input { height: 3.5rem !important; background-color: #0f172a !important; color: white !important; border: 1px solid #334155 !important; font-size: 1.1rem !important; }
    .main-title { text-align: center; color: #f8fafc; font-weight: 800; margin-bottom: 1rem; }
</style>
""", unsafe_allow_html=True)

# --- CONFIGURAÇÕES ---
MEU_EMAIL = "nhatano@gmail.com"
SAYRA_EMAIL = "sayradan@gmail.com"
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdCkxNA1WEBbuDl4VA6KKmI937zLk95BQ654KSLGzwO6TxayA/formResponse"

# --- BANCO DE DADOS DE TREINOS (A AO F) ---
TREINOS = {
    "TREINO A: LEGS A (QUADRÍCEPS)": [
        {"ex": "Agachamento Hack", "sets": ["70kg (15 reps)", "100kg (12 reps)", "120kg (10 reps)", "140kg (6-8 reps)"], "bio": "Pés baixos. 3s na descida.", "vid": "https://www.youtube.com/watch?v=0v8rKNcmMFM"},
        {"ex": "Leg Press 45º", "sets": ["220kg (12 reps)", "235kg (10 reps)", "285kg (10 reps)", "Drop: 260->180->100"], "bio": "Amplitude máxima.", "vid": "https://www.youtube.com/watch?v=adPY6cd4h58"},
        {"ex": "Cadeira Adutora", "sets": ["95kg", "100kg", "100kg"], "bio": "3s abrir/fechar.", "vid": "https://www.youtube.com/watch?v=Wf602gn_9zU"},
        {"ex": "Cadeira Extensora", "sets": ["47kg", "47kg", "Drop set"], "bio": "Iso 2s no topo.", "vid": "https://www.youtube.com/watch?v=H6UoiaP9_38"},
        {"ex": "Afundo com Halteres", "sets": ["17,5kg", "20kg", "20kg"], "bio": "Tronco à frente.", "vid": "https://www.youtube.com/watch?v=QOVaHwm-Q6U"},
        {"ex": "Panturrilha no Leg", "sets": ["150kg", "150kg", "150kg"], "bio": "Alongamento máximo.", "vid": "https://www.youtube.com/watch?v=q_K2eW7mUqI"},
        {"ex": "Abdominal Polia Média", "sets": ["1 min", "1 min", "Falha"], "bio": "Core ativado.", "vid": "https://www.youtube.com/watch?v=2D7N_fU7Usc"}
    ],
    "TREINO B: PUSH A (PEITO/OMBRO)": [
        {"ex": "Supino Inclinado Halteres", "sets": ["25kg", "27,5kg", "30kg", "32,5kg"], "bio": "Banco 30º.", "vid": "https://www.youtube.com/watch?v=0G2_XV7slIs"},
        {"ex": "Chest Press Articulado", "sets": ["35kg/lado", "40kg/lado", "Drop set"], "bio": "Alça altura mamilo.", "vid": "https://www.youtube.com/watch?v=l_i9I-Y8r1U"},
        {"ex": "Desenv. Máquina", "sets": ["25kg", "30kg", "35kg"], "bio": "Punho alinhado.", "vid": "https://www.youtube.com/watch?v=WvLMauqrnK8"},
        {"ex": "Voador Peck Deck", "sets": ["54kg", "61kg", "68kg"], "bio": "Esmague no centro.", "vid": "https://www.youtube.com/watch?v=Xp0NfT_SjG0"},
        {"ex": "Elevação Lateral Halteres", "sets": ["15kg", "15kg", "Drop set"], "bio": "Linha do ombro.", "vid": "https://www.youtube.com/watch?v=3VkKa2kn07w"},
        {"ex": "Tríceps Corda", "sets": ["25kg", "30kg", "Drop set"], "bio": "Abra embaixo.", "vid": "https://www.youtube.com/watch?v=Yid37u14vH0"},
        {"ex": "Tríceps Francês Polia", "sets": ["15kg", "17,5kg", "20kg"], "bio": "Cotovelos fechados.", "vid": "https://www.youtube.com/watch?v=S_mU0G0mO-E"}
    ],
    "TREINO C: PULL A (COSTAS/BÍCEPS)": [
        {"ex": "Puxada Alta Aberta", "sets": ["55kg", "70kg", "77kg", "84kg"], "bio": "Puxe pelo cotovelo.", "vid": "https://www.youtube.com/watch?v=H75im9fAUMc"},
        {"ex": "Remada Baixa Triângulo", "sets": ["84kg", "98kg", "103kg"], "bio": "Segure 1s no umbigo.", "vid": "https://www.youtube.com/watch?v=lJ7x8S_3uMA"},
        {"ex": "Remada Unilateral Polia", "sets": ["22kg", "25kg", "25kg"], "bio": "Tensão constante.", "vid": "https://www.youtube.com/watch?v=fM5K60p4S8A"},
        {"ex": "Pulldown Barra/Corda", "sets": ["30kg", "35kg", "35kg"], "bio": "Braços quase retos.", "vid": "https://www.youtube.com/watch?v=8uS_w8_1I_M"},
        {"ex": "Crucifixo Inverso Máquina", "sets": ["33kg", "40kg", "40kg"], "bio": "Deltoide posterior.", "vid": "https://www.youtube.com/watch?v=Xp0NfT_SjG0"},
        {"ex": "Rosca Martelo", "sets": ["15kg", "16kg", "18kg"], "bio": "Pegada neutra.", "vid": "https://www.youtube.com/watch?v=zS9_3mE9L6o"},
        {"ex": "Rosca Direta Barra W", "sets": ["35kg", "35kg", "30kg"], "bio": "Mantenha cotovelo fixo.", "vid": "https://www.youtube.com/watch?v=Xp0NfT_SjG0"},
        {"ex": "Flexão de Punho", "sets": ["14kg", "15kg", "16kg"], "bio": "Carga moderada.", "vid": "https://www.youtube.com/watch?v=M_33zK08Nls"},
        {"ex": "Abdominal na Polia", "sets": ["25kg", "27,5kg", "30kg"], "bio": "Enrole a coluna.", "vid": "https://www.youtube.com/watch?v=2D7N_fU7Usc"}
    ],
    "TREINO D: LEGS B (POSTERIOR/GLÚTEO)": [
        {"ex": "Cadeira Flexora", "sets": ["54kg", "61kg", "68kg", "Drop 75kg"], "bio": "Tronco à frente.", "vid": "https://www.youtube.com/watch?v=78V9XpS7F7M"},
        {"ex": "Stiff", "sets": ["80kg", "100kg", "120kg"], "bio": "Quadril para trás.", "vid": "https://www.youtube.com/watch?v=mD2f_LueIYA"},
        {"ex": "Leg Press (Pés no Topo)", "sets": ["200kg", "240kg", "260kg"], "bio": "Foco no glúteo.", "vid": "https://www.youtube.com/watch?v=yZmx_7igYyU"},
        {"ex": "Elevação Pélvica", "sets": ["110kg", "130kg", "150kg"], "bio": "Iso 3s no topo.", "vid": "https://www.youtube.com/watch?v=A8nFGuY77CE"},
        {"ex": "Abdução Quadril", "sets": ["75kg", "82kg", "82kg"], "bio": "Tronco à frente.", "vid": "https://www.youtube.com/watch?v=yX7t3R7p2p0"},
        {"ex": "Panturrilha no Leg", "sets": ["240kg", "240kg", "240kg"], "bio": "Ponta dos pés.", "vid": "https://www.youtube.com/watch?v=q_K2eW7mUqI"},
        {"ex": "Elevação Pernas Infra", "sets": ["Set 1", "Set 2", "Set 3"], "bio": "Foco infra.", "vid": "https://www.youtube.com/watch?v=Pr1ieGZ5atk"}
    ],
    "TREINO E: PUSH B (OMBROS 3D/PEITO)": [
        {"ex": "Desenv. Halteres Sentado", "sets": ["20kg", "24kg", "30kg"], "bio": "Banco 80º.", "vid": "https://www.youtube.com/watch?v=HzIiIn92_2M"},
        {"ex": "Elevação Lateral Polia", "sets": ["7,5kg", "7,5kg", "10kg"], "bio": "Tensão constante.", "vid": "https://www.youtube.com/watch?v=3VkKa2kn07w"},
        {"ex": "Supino Inc. Articulado", "sets": ["25kg", "35kg", "40kg"], "bio": "Peito superior.", "vid": "https://www.youtube.com/watch?v=5E6V_uT2yS8"},
        {"ex": "Crucifixo Inverso Máquina", "sets": ["33kg", "40kg", "40kg"], "bio": "Deltoide post.", "vid": "https://www.youtube.com/watch?v=Xp0NfT_SjG0"},
        {"ex": "Elevação Frontal Anilha", "sets": ["12,5kg", "15kg", "15kg"], "bio": "Até os olhos.", "vid": "https://www.youtube.com/watch?v=xS9v3_S1XnE"},
        {"ex": "Tríceps Pulley Reta", "sets": ["25kg", "30kg", "35kg"], "bio": "Punho firme.", "vid": "https://www.youtube.com/watch?v=2-LAMcpz_OQ"},
        {"ex": "Tríceps Francês Polia", "sets": ["15kg", "17,5kg", "20kg"], "bio": "Extensão total.", "vid": "https://www.youtube.com/watch?v=S_mU0G0mO-E"},
        {"ex": "Abdominal Crunch", "sets": ["Set 1", "Set 2", "Set 3"], "bio": "Carga alta.", "vid": "https://www.youtube.com/watch?v=2D7N_fU7Usc"}
    ],
    "TREINO F: PULL B (COSTAS/BÍCEPS)": [
        {"ex": "Remada Curvada Barra", "sets": ["Set 1", "Set 2", "Set 3", "Set 4"], "bio": "Tronco paralelo.", "vid": "https://www.youtube.com/watch?v=68T080S09Wk"},
        {"ex": "Remada Cavalinho", "sets": ["Set 1", "Set 2", "Set 3"], "bio": "Cotovelo rente.", "vid": "https://www.youtube.com/watch?v=FmS_XzIByK4"},
        {"ex": "Puxada Triângulo", "sets": ["Set 1", "Set 2", "Set 3"], "bio": "Latíssimo.", "vid": "https://www.youtube.com/watch?v=lJ7x8S_3uMA"},
        {"ex": "Puxada Unilateral", "sets": ["Set 1", "Set 2", "Set 3"], "bio": "Conexão mente.", "vid": "https://www.youtube.com/watch?v=fM5K60p4S8A"},
        {"ex": "Encolhimento Halteres", "sets": ["Set 1", "Set 2", "Set 3"], "bio": "Trapézio.", "vid": "https://www.youtube.com/watch?v=mE9n-W7S8Yg"},
        {"ex": "Rosca Inclinada", "sets": ["Set 1", "Set 2", "Set 3"], "bio": "Alongamento bíceps.", "vid": "https://www.youtube.com/watch?v=K3S2G_9vS0I"},
        {"ex": "Rosca Scott", "sets": ["Set 1", "Set 2", "Set 3"], "bio": "Isolamento.", "vid": "https://www.youtube.com/watch?v=f_Vp_7i0N_E"},
        {"ex": "Prancha", "sets": ["1 min", "1 min", "1 min"], "bio": "Estabilização.", "vid": "https://www.youtube.com/watch?v=pSHjTRCQxIw"}
    ]
}

# --- CONTROLE DE LOGIN ---
if 'logado' not in st.session_state:
    st.session_state.logado = False

if not st.session_state.logado:
    st.markdown("<h1 class='main-title'>⚡ Lindos Shape Pro</h1>", unsafe_allow_html=True)
    email_login = st.text_input("Seu e-mail", placeholder="exemplo@gmail.com").lower().strip()
    if st.button("Acessar"):
        if email_login in [MEU_EMAIL, SAYRA_EMAIL]:
            st.session_state.logado = True
            st.session_state.email = email_login
            st.rerun()
        else:
            st.error("E-mail não autorizado.")
else:
    # --- INTERFACE PRINCIPAL ---
    email = st.session_state.email
    u_name = "Nilson" if email == MEU_EMAIL else "Olá Princess Fitness"
    saudacao = "Bem-vindo, Lindo!" if email == MEU_EMAIL else "Olá, Linda!"
    
    st.markdown(f"### {saudacao}")
    dia = st.selectbox("Escolha seu Treino", list(TREINOS.keys()))
    
    st.divider()

    for item in TREINOS[dia]:
        with st.container():
            st.markdown(f"""<div class="exercise-card"><h3>{item['ex']}</h3><p>{item['bio']}</p></div>""", unsafe_allow_html=True)
            
            # BOTÃO DE VÍDEO NOVO (ABRE NO YOUTUBE)
            st.link_button("🎥 Ver Execução no YouTube", item['vid'])
            
            for i, meta in enumerate(item['sets']):
                st.write(f"**Série {i+1}**")
                c1, c2, c3 = st.columns([1, 1, 1])
                c1.text_input("Alvo", value=meta, key=f"t_{item['ex']}_{i}_{dia}")
                c2.number_input("Peso", key=f"w_{item['ex']}_{i}_{dia}", min_value=0)
                c3.selectbox("RPE", list(range(1,11)), index=7, key=f"r_{item['ex']}_{i}_{dia}")
            
            if st.button(f"Salvar {item['ex']}", key=f"btn_{item['ex']}_{dia}"):
                try:
                    for i in range(len(item['sets'])):
                        payload = {
                            'entry.2096362736': email,
                            'entry.201460740': item['ex'],
                            'entry.46463683': i + 1,
                            'entry.687657200': st.session_state[f"t_{item['ex']}_{i}_{dia}"],
                            'entry.906726937': st.session_state[f"w_{item['ex']}_{i}_{dia}"],
                            'entry.413423792': st.session_state[f"r_{item['ex']}_{i}_{dia}"]
                        }
                        requests.post(FORM_URL, data=payload)
                    st.success("Salvo com sucesso!")
                    st.balloons()
                except:
                    st.error("Erro ao salvar.")

    if st.button("Sair"):
        st.session_state.logado = False
        st.rerun()


