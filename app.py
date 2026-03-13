import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Aura Fitness Pro", layout="wide", page_icon="⚡")

# --- DESIGN PREMIUM AURA FITNESS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700;800&display=swap');
    html, body, [data-testid="stAppViewContainer"] { font-family: 'Manrope', sans-serif; background-color: #020617; color: #f8fafc; }
    .exercise-card { background: rgba(30, 41, 59, 0.4); backdrop-filter: blur(16px); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 1rem; padding: 24px; margin-bottom: 20px; border-left: 5px solid #0f49bd; }
    .stButton>button { background: #0f49bd; color: white; border-radius: 0.75rem; font-weight: 800; height: 3rem; width: 100%; border: none; }
    input { background-color: #0f172a !important; color: white !important; border: 1px solid #334155 !important; }
</style>
""", unsafe_allow_html=True)

# --- CONFIGURAÇÕES ---
MEU_EMAIL = "nhatano@gmail.com"
SAYRA_EMAIL = "sayradan@gmail.com"
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdCkxNA1WEBbuDl4VA6KKmI937zLk95BQ654KSLGzwO6TxayA/formResponse"

# --- BANCO DE DADOS DE TREINOS COMPLETO (7+ EXERCÍCIOS POR DIA) ---
TREINOS = {
    "TREINO A: LEGS A (QUADRÍCEPS)": [
        {"ex": "Agachamento Hack", "sets": ["70kg (15 reps)", "100kg (12 reps)", "120kg (10 reps)", "140kg (6-8 reps)"], "bio": "Pés baixos. 3s na descida.", "vid": "https://www.youtube.com/watch?v=0enGC9f_Tpg"},
        {"ex": "Leg Press 45º", "sets": ["220kg (12 reps)", "235kg (10 reps)", "285kg (10 reps)", "Drop: 260->180->100"], "bio": "Amplitude máxima.", "vid": "https://www.youtube.com/watch?v=yZmx_7igYyU"},
        {"ex": "Cadeira Adutora", "sets": ["95kg (15 reps)", "100kg (12 reps)", "100kg (Falha)"], "bio": "3s abrir/fechar.", "vid": "https://www.youtube.com/watch?v=4IStG89y8i4"},
        {"ex": "Cadeira Extensora", "sets": ["47kg (12 reps)", "47kg (12 reps)", "Drop: 54->33->19"], "bio": "Iso 2s no topo.", "vid": "https://www.youtube.com/watch?v=m0FOpMEgero"},
        {"ex": "Afundo com Halteres", "sets": ["17,5kg/mão", "20kg/mão", "20kg (Falha)"], "bio": "Tronco à frente.", "vid": "https://www.youtube.com/watch?v=q7_6v6w9jXs"},
        {"ex": "Panturrilha no Leg", "sets": ["150kg", "150kg", "150kg"], "bio": "Alongamento máximo.", "vid": "https://www.youtube.com/watch?v=q_K2eW7mUqI"},
        {"ex": "Abdominal Polia Média", "sets": ["1 min", "1 min", "Falha"], "bio": "Foco na contração.", "vid": "https://www.youtube.com/watch?v=2D7N_fU7Usc"}
    ],
    "TREINO B: PUSH A (PEITO/OMBRO)": [
        {"ex": "Supino Inclinado Halteres", "sets": ["25kg", "27,5kg", "30kg", "32,5kg"], "bio": "Banco 30º. Escápulas retraídas.", "vid": "https://www.youtube.com/watch?v=8iP9S706yLw"},
        {"ex": "Chest Press Articulado", "sets": ["35kg/lado", "40kg/lado", "Drop: 40->25->15"], "bio": "Alça altura mamilo.", "vid": "https://www.youtube.com/watch?v=l_i9I-Y8r1U"},
        {"ex": "Desenv. Máquina", "sets": ["25kg/l", "30kg/l", "35kg/l"], "bio": "Punho alinhado com cotovelo.", "vid": "https://www.youtube.com/watch?v=WvLMauqrnK8"},
        {"ex": "Voador Peck Deck", "sets": ["54kg", "61kg", "68kg"], "bio": "Esmague o peito no centro.", "vid": "https://www.youtube.com/watch?v=Xp0NfT_SjG0"},
        {"ex": "Elevação Lateral Halteres", "sets": ["15kg", "15kg", "Drop: 16->10->6"], "bio": "Não suba além da linha do ombro.", "vid": "https://www.youtube.com/watch?v=3VkKa2kn07w"},
        {"ex": "Tríceps Corda", "sets": ["25kg", "30kg", "Drop: 32,5->22,5->15"], "bio": "Abra a corda embaixo.", "vid": "https://www.youtube.com/watch?v=Yid37u14vH0"},
        {"ex": "Tríceps Francês Polia", "sets": ["15kg", "17,5kg", "20kg"], "bio": "Cotovelos bem fechados.", "vid": "https://www.youtube.com/watch?v=S_mU0G0mO-E"}
    ],
    "TREINO C: PULL A (COSTAS/BÍCEPS)": [
        {"ex": "Puxada Alta Aberta", "sets": ["55kg", "70kg", "77,5kg", "84,5kg"], "bio": "Use Straps. Puxe pelo cotovelo.", "vid": "https://www.youtube.com/watch?v=H75im9fAUMc"},
        {"ex": "Remada Baixa Triângulo", "sets": ["84kg", "98kg", "103kg"], "bio": "Segure 1s no umbigo.", "vid": "https://www.youtube.com/watch?v=lJ7x8S_3uMA"},
        {"ex": "Remada Unilateral Polia", "sets": ["22kg", "25kg", "25kg"], "bio": "Tensão constante.", "vid": "https://www.youtube.com/watch?v=fM5K60p4S8A"},
        {"ex": "Pulldown Barra ou Corda", "sets": ["30kg", "35kg", "35kg"], "bio": "Cotovelo quase travado.", "vid": "https://www.youtube.com/watch?v=8uS_w8_1I_M"},
        {"ex": "Crucifixo Inverso Máquina", "sets": ["33kg", "40kg", "40kg"], "bio": "Deltoide posterior.", "vid": "https://www.youtube.com/watch?v=Xp0NfT_SjG0"},
        {"ex": "Rosca Martelo", "sets": ["15kg", "16kg", "18kg"], "bio": "Pegada neutra.", "vid": "https://www.youtube.com/watch?v=zS9_3mE9L6o"},
        {"ex": "Rosca Direta Barra W", "sets": ["35kg", "35kg", "30kg"], "bio": "Mantenha cotovelo fixo.", "vid": "https://www.youtube.com/watch?v=Xp0NfT_SjG0"},
        {"ex": "Flexão de Punho", "sets": ["14kg", "15kg", "16kg"], "bio": "Amplitude máxima.", "vid": "https://www.youtube.com/watch?v=M_33zK08Nls"},
        {"ex": "Abdominal na Polia", "sets": ["25kg", "27,5kg", "27,5kg"], "bio": "Enrole a coluna.", "vid": "https://www.youtube.com/watch?v=2D7N_fU7Usc"}
    ],
    "TREINO D: LEGS B (POSTERIOR/GLÚTEO)": [
        {"ex": "Cadeira Flexora", "sets": ["54kg", "61kg", "68kg", "Drop 75kg"], "bio": "Tronco inclinado à frente.", "vid": "https://www.youtube.com/watch?v=78V9XpS7F7M"},
        {"ex": "Stiff com Halteres ou Hack", "sets": ["80kg", "100kg", "120kg"], "bio": "Quadril para trás. Raspe na perna.", "vid": "https://www.youtube.com/watch?v=mD2f_LueIYA"},
        {"ex": "Leg Press (Pés no Topo)", "sets": ["200kg", "240kg", "260kg"], "bio": "Foco glúteo. Empurre pelo calcanhar.", "vid": "https://www.youtube.com/watch?v=yZmx_7igYyU"},
        {"ex": "Elevação Pélvica", "sets": ["110kg", "130kg", "150kg"], "bio": "Iso 3s no topo.", "vid": "https://www.youtube.com/watch?v=A8nFGuY77CE"},
        {"ex": "Abdução de Quadril", "sets": ["75kg", "82kg", "82kg"], "bio": "Tronco à frente.", "vid": "https://www.youtube.com/watch?v=yX7t3R7p2p0"},
        {"ex": "Panturrilha no Leg", "sets": ["240kg", "240kg", "240kg"], "bio": "Alongamento máximo.", "vid": "https://www.youtube.com/watch?v=q_K2eW7mUqI"},
        {"ex": "Elevação de Pernas (Infra)", "sets": ["Set 1", "Set 2", "Set 3"], "bio": "Core ativado.", "vid": "https://www.youtube.com/watch?v=Pr1ieGZ5atk"}
    ],
    "TREINO E: PUSH B (OMBROS 3D/PEITO)": [
        {"ex": "Desenv. Halteres Sentado", "sets": ["20kg", "24kg", "30kg"], "bio": "Banco 80º.", "vid": "https://www.youtube.com/watch?v=HzIiIn92_2M"},
        {"ex": "Elevação Lateral Polia", "sets": ["7,5kg", "10kg", "12kg"], "bio": "Por trás do corpo. Tensão constante.", "vid": "https://www.youtube.com/watch?v=3VkKa2kn07w"},
        {"ex": "Supino Inc. Articulado", "sets": ["25kg/l", "35kg/l", "40kg/l"], "bio": "Foco no peito superior.", "vid": "https://www.youtube.com/watch?v=5E6V_uT2yS8"},
        {"ex": "Crucifixo Inverso Máquina", "sets": ["33kg", "40kg", "40kg"], "bio": "Deltoide posterior.", "vid": "https://www.youtube.com/watch?v=Xp0NfT_SjG0"},
        {"ex": "Elevação Frontal com Anilha", "sets": ["12,5kg", "15kg", "15kg"], "bio": "Suba até a linha dos olhos.", "vid": "https://www.youtube.com/watch?v=xS9v3_S1XnE"},
        {"ex": "Tríceps Pulley Reta", "sets": ["25kg", "30kg", "Drop"], "bio": "Punho firme.", "vid": "https://www.youtube.com/watch?v=2-LAMcpz_OQ"},
        {"ex": "Tríceps Francês Polia (Média)", "sets": ["15kg", "17,5kg", "20kg"], "bio": "Cuidado com o ombro.", "vid": "https://www.youtube.com/watch?v=S_mU0G0mO-E"},
        {"ex": "Tríceps Francês Polia (Baixa)", "sets": ["15kg", "17,5kg", "20kg"], "bio": "Extensão total.", "vid": "https://www.youtube.com/watch?v=S_mU0G0mO-E"},
        {"ex": "Abdominal Crunch Máquina", "sets": ["Set 1", "Set 2", "Set 3"], "bio": "Carga alta. Enrole o abdômen.", "vid": "https://www.youtube.com/watch?v=2D7N_fU7Usc"}
    ]
}

# --- INTERFACE ---
with st.sidebar:
    st.markdown("### ⚡ Aura Fitness")
    user_email = st.text_input("Identidade (E-mail)", placeholder="seu@email.com").lower().strip()
    if user_email in [MEU_EMAIL, SAYRA_EMAIL]:
        dia = st.selectbox("Selecione sua Rotina", list(TREINOS.keys()))
    btn_login = st.button("Acessar Treino")

if user_email in [MEU_EMAIL, SAYRA_EMAIL]:
    u_name = "Nilson" if user_email == MEU_EMAIL else "Olá Princess Fitness"
    u_initials = "NH" if user_email == MEU_EMAIL else "SF"
    
    st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 30px; padding: 10px;">
            <div style="width: 55px; height: 55px; border-radius: 50%; border: 2px solid #0f49bd; overflow: hidden; background: #1e293b; display: flex; align-items: center; justify-content: center; font-weight: 800; color: white; font-size: 20px;">{u_initials}</div>
            <div>
                <p style="font-size: 10px; color: #94a3b8; font-weight: 800; text-transform: uppercase; margin: 0; letter-spacing: 0.1em;">Bem-vindo de volta,</p>
                <h1 style="font-size: 24px; margin: 0; font-weight: 800; color: white;">{u_name}</h1>
            </div>
        </div>
    """, unsafe_allow_html=True)

    for item in TREINOS[dia]:
        with st.container():
            st.markdown(f"""<div class="exercise-card"><h3>{item['ex']}</h3><p>{item['bio']}</p></div>""", unsafe_allow_html=True)
            cv, cd = st.columns([1, 2])
            with cv:
                try:
                    st.video(item['vid'])
                except:
                    st.warning("Vídeo indisponível no momento.")
            with cd:
                for i, meta in enumerate(item['sets']):
                    cols = st.columns([2, 1, 1])
                    # Alvos preenchidos para ambos, mas editáveis
                    alvo = cols[0].text_input("Alvo", value=meta, key=f"t_{item['ex']}_{i}_{dia}")
                    carga = cols[1].number_input("Peso (kg)", key=f"w_{item['ex']}_{i}_{dia}", min_value=0)
                    rpe = cols[2].selectbox("Esforço (RPE)", list(range(1,11)), index=7, key=f"r_{item['ex']}_{i}_{dia}")
            
            if st.button(f"Salvar {item['ex']}", key=f"btn_{item['ex']}_{dia}"):
                try:
                    for i in range(len(item['sets'])):
                        payload = {
                            'entry.2096362736': user_email,
                            'entry.201460740': item['ex'],
                            'entry.46463683': i + 1,
                            'entry.687657200': st.session_state[f"t_{item['ex']}_{i}_{dia}"],
                            'entry.906726937': st.session_state[f"w_{item['ex']}_{i}_{dia}"],
                            'entry.413423792': st.session_state[f"r_{item['ex']}_{i}_{dia}"]
                        }
                        requests.post(FORM_URL, data=payload)
                    st.success(f"{item['ex']} salvo com sucesso!")
                    st.balloons()
                except Exception as e:
                    st.error(f"Erro ao salvar: {e}")
else:
    st.info("👋 Digite seu e-mail na barra lateral para carregar seu treino.")
