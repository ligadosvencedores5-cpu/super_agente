import streamlit as st
from groq import Groq
from datetime import datetime
import json
import os
import re

# ── CONFIGURAÇÃO DA PÁGINA ─────────────────────────────────────────────────
st.set_page_config(
    page_title="Super Agente IA",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
#MainMenu,footer,header,[data-testid="stToolbar"],
[data-testid="stDecoration"],[data-testid="stStatusWidget"] { visibility:hidden; }
</style>
""", unsafe_allow_html=True)

# ── CSS SISTEMA ────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* ═══ TEMA CLARO FORÇADO — sobrescreve dark mode do Streamlit ═══ */
html, body { background-color:#F8F9FA !important; color:#1A1A2E !important; }

/* Todos os containers do Streamlit */
.stApp, .stApp > *, .main, .block-container,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > *,
[data-testid="stMain"],
[data-testid="stMain"] > *,
[data-testid="block-container"],
[data-testid="block-container"] > *,
[data-testid="stVerticalBlock"],
[data-testid="stHorizontalBlock"] {
    background-color:#F8F9FA !important;
    color:#1A1A2E !important;
}

/* TEXTO — forçar escuro em absolutamente todo elemento de texto */
*, *::before, *::after {
    color:#1A1A2E !important;
    font-family:'Inter',sans-serif !important;
}

/* Exceções: botões, badges e banner do hub mantêm texto branco/claro */
.stButton > button,
.stButton > button *,
.stButton > button p,
.stButton > button span,
.badge, .badge *,
.badge-verde, .badge-verde *,
.badge-amarelo, .badge-amarelo *,
.badge-azul, .badge-azul *,
.badge-roxo, .badge-roxo * {
    color:white !important;
}

/* ═══ DOWNLOAD / UPLOAD — corrige ícone SVG encavalado ═══ */
[data-testid="stDownloadButton"] > button,
[data-testid="stDownloadButton"] > button *,
[data-testid="stDownloadButton"] > button span,
[data-testid="stDownloadButton"] > button p {
    color:white !important;
}
[data-testid="stDownloadButton"] > button svg,
[data-testid="stDownloadButton"] > button svg * {
    color:inherit !important;
    fill:white !important;
}
/* File uploader — label e ícone */
[data-testid="stFileUploader"] [data-testid="stFileUploaderDropzone"] *,
[data-testid="stFileUploader"] label,
[data-testid="stFileUploader"] small,
[data-testid="stFileUploader"] span {
    color:#495057 !important;
}
[data-testid="stFileUploader"] svg,
[data-testid="stFileUploader"] svg * {
    color:#495057 !important;
    fill:#495057 !important;
}
/* Garante que SVGs em geral não herdam color como fill */
svg text, svg tspan { fill:inherit !important; color:inherit !important; }
svg path, svg rect, svg circle, svg line, svg polyline, svg polygon {
    /* não forçar fill aqui para não quebrar ícones coloridos */
}
.hub-header h1, .hub-header h2, .hub-header h3,
.hub-header div { color:white !important; }
.hub-header p   { color:#A3E635 !important; }

/* Inputs */
.stTextInput > div > div > input,
.stTextArea > div > textarea,
.stSelectbox > div > div > div,
.stNumberInput > div > div > input {
    background-color:#FFFFFF !important;
    color:#1A1A2E !important;
    border:1px solid #CED4DA !important;
}

/* Abas */
[data-testid="stTabs"],
.stTabs [data-baseweb="tab-panel"],
.stTabs [data-baseweb="tab-list"] {
    background-color:#F8F9FA !important;
}
.stTabs [data-baseweb="tab"],
.stTabs [data-baseweb="tab"] * { color:#495057 !important; }
.stTabs [aria-selected="true"],
.stTabs [aria-selected="true"] * {
    color:#1A1A2E !important;
    border-bottom-color:#343A40 !important;
}

/* Expanders */
[data-testid="stExpander"],
.streamlit-expanderHeader,
.streamlit-expanderHeader * {
    background-color:#FFFFFF !important;
    color:#1A1A2E !important;
}

/* Métricas */
[data-testid="stMetric"] { background:#FFFFFF !important; border-radius:10px; padding:12px; border:1px solid #DEE2E6; }
[data-testid="stMetricValue"], [data-testid="stMetricLabel"],
[data-testid="stMetricDelta"] { color:#1A1A2E !important; }

/* Sidebar oculta */
[data-testid="stSidebar"] { display:none; }

/* ═══ INPUTS — fundo branco e texto escuro (BaseWeb) ═══ */
input, textarea, select,
[data-baseweb="input"] input,
[data-baseweb="textarea"] textarea,
[data-baseweb="select"] input,
[data-baseweb="input"],
[data-baseweb="input"] > div,
[data-baseweb="textarea"],
[data-baseweb="textarea"] > div,
[data-baseweb="base-input"],
[data-baseweb="base-input"] > div {
    background-color:#FFFFFF !important;
    background:#FFFFFF !important;
    color:#1A1A2E !important;
}

/* ═══ STAT-BOXES / cards escuros do Nexus English ═══ */
/* Qualquer div com background escuro dentro do stApp */
.stApp div[style*="background:#0F"],
.stApp div[style*="background: #0F"],
.stApp div[style*="background:#1A"],
.stApp div[style*="background: #1A"],
.stApp div[style*="background:#16"],
.stApp div[style*="background: #16"],
.stApp div[style*="background-color:#0F"],
.stApp div[style*="background-color: #0F"],
.stApp div[style*="background-color:#1A"],
.stApp div[style*="background-color: #1A"],
.stApp div[style*="background-color:#16"],
.stApp div[style*="background-color: #16"] {
    background-color:#F0F4FF !important;
    background:#F0F4FF !important;
    color:#1A1A2E !important;
}

/* ═══ Selectbox dropdown ═══ */
[data-baseweb="popover"] *,
[data-baseweb="menu"] *,
[role="listbox"] *,
[role="option"] {
    background-color:#FFFFFF !important;
    color:#1A1A2E !important;
}

.stTextInput>div>div>input, .stTextArea>div>textarea,
.stSelectbox>div>div>div, .stNumberInput>div>div>input {
    background-color:#FFFFFF !important; color:#1A1A2E !important;
    border:1px solid #CED4DA !important; font-family:'Inter',sans-serif !important;
}

.stButton>button {
    width:100%; border-radius:10px; height:3.2em;
    background:linear-gradient(135deg,#495057,#343A40) !important; color:white !important;
    font-weight:600; border:none; box-shadow:2px 2px 8px rgba(0,0,0,0.1);
    font-family:'Inter',sans-serif !important; transition:all 0.2s ease;
}
.stButton>button:hover { background:linear-gradient(135deg,#343A40,#212529) !important; transform:translateY(-1px); }
.stApp .stButton>button, .stApp .stButton>button p,
.stApp .stButton>button span, .stApp .stButton>button div { color:white !important; }

.stApp h1, .stApp h2, .stApp h3 { color:#1A1A2E !important; font-family:'Inter',sans-serif !important; font-weight:700 !important; }

.card { background:linear-gradient(135deg,#F1F3F5,#E9ECEF); padding:20px; border-radius:14px; border:1px solid #CED4DA; margin-bottom:14px; }
.stApp .card, .stApp .card p, .stApp .card span, .stApp .card div, .stApp .card strong { color:#1A1A2E !important; }
.card-dark { background:linear-gradient(135deg,#E9ECEF,#DEE2E6); padding:20px; border-radius:14px; border:1px solid #ADB5BD; margin-bottom:14px; }
.stApp .card-dark, .stApp .card-dark p, .stApp .card-dark span, .stApp .card-dark div { color:#1A1A2E !important; }
.card-green { background:linear-gradient(135deg,#F0FDF4,#DCFCE7); padding:20px; border-radius:14px; border:1px solid #86EFAC; margin-bottom:14px; }
.stApp .card-green, .stApp .card-green p, .stApp .card-green span, .stApp .card-green div { color:#14532D !important; }
.card-blue { background:linear-gradient(135deg,#EFF6FF,#DBEAFE); padding:20px; border-radius:14px; border:1px solid #93C5FD; margin-bottom:14px; }
.stApp .card-blue, .stApp .card-blue p, .stApp .card-blue span, .stApp .card-blue div { color:#1E3A8A !important; }
.card-red { background:linear-gradient(135deg,#FFF5F5,#FEE2E2); padding:20px; border-radius:14px; border:1px solid #FECACA; margin-bottom:14px; }
.stApp .card-red, .stApp .card-red p, .stApp .card-red span, .stApp .card-red div { color:#7F1D1D !important; }
.card-yellow { background:linear-gradient(135deg,#FFFBEB,#FEF3C7); padding:18px; border-radius:12px; border:1px solid #FCD34D; margin-bottom:12px; }
.stApp .card-yellow, .stApp .card-yellow p, .stApp .card-yellow span, .stApp .card-yellow div { color:#78350F !important; }

.stat-box { background:#FFFFFF; border-radius:12px; padding:16px; text-align:center; border:1px solid #CED4DA; }
.stApp .stat-box div, .stApp .stat-box span, .stApp .stat-box p { color:#1A1A2E !important; }
.stat-numero { font-size:2em; font-weight:700; color:#495057 !important; }

.hist-item { background:#FFFFFF; border-radius:10px; padding:12px 16px; margin-bottom:8px; border-left:4px solid #CED4DA; }
.stApp .hist-item, .stApp .hist-item p, .stApp .hist-item span, .stApp .hist-item div { color:#1A1A2E !important; }

.badge { background:#495057; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
.badge-verde { background:#059669; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
.badge-amarelo { background:#B45309; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
.badge-azul { background:#1D4ED8; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
.badge-roxo { background:#6D28D9; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }

.divider { border:none; height:1px; background:linear-gradient(to right,transparent,#CED4DA,transparent); margin:18px 0; }

.chat-user { background:#FFFFFF; border:1px solid #CED4DA; border-radius:12px 12px 4px 12px; padding:12px 16px; margin:8px 0; }
.stApp .chat-user, .stApp .chat-user p, .stApp .chat-user span, .stApp .chat-user div { color:#1A1A2E !important; }
.chat-persona { background:#F8F9FA; border:1px solid #CED4DA; border-radius:4px 12px 12px 12px; padding:12px 16px; margin:8px 0; }
.stApp .chat-persona, .stApp .chat-persona p, .stApp .chat-persona span, .stApp .chat-persona div { color:#1A1A2E !important; }

.questao-box { background:#FFFFFF; border:2px solid #CED4DA; border-radius:12px; padding:18px; margin-bottom:14px; }
.stApp .questao-box, .stApp .questao-box p, .stApp .questao-box span { color:#1A1A2E !important; }
.avaliacao-box { background:#FFFFFF; border:2px solid #CED4DA; border-radius:14px; padding:18px; margin-bottom:12px; }
.stApp .avaliacao-box, .stApp .avaliacao-box p, .stApp .avaliacao-box span { color:#1A1A2E !important; }
.meta-box { background:#FFFFFF; border:2px solid #CED4DA; border-radius:12px; padding:16px; text-align:center; margin:10px 0; }
.stApp .meta-box, .stApp .meta-box div, .stApp .meta-box span { color:#1A1A2E !important; }
.meta-numero { font-size:2em; font-weight:700; color:#495057 !important; }

.chat-scroll-container { max-height:40vh; overflow-y:auto; display:flex; flex-direction:column; scroll-behavior:smooth; padding-bottom:4px; }

.hub-header {
    background: linear-gradient(135deg, #C7D2FE 0%, #A5B4FC 100%);
    border-radius: 20px; padding: 36px 32px; margin-bottom: 32px; text-align: center;
    border: 1px solid #818CF8;
}
.hub-card {
    background: linear-gradient(135deg, #FFFFFF, #F8F9FA);
    border: 1px solid #DEE2E6; border-radius: 16px; padding: 24px 16px;
    text-align: center; margin-bottom: 12px; transition: all 0.2s ease;
    min-height: 130px; display: flex; flex-direction: column;
    align-items: center; justify-content: center;
}
.hub-card:hover { transform: translateY(-3px); box-shadow: 0 8px 24px rgba(0,0,0,0.12); border-color: #A3E635; }
.hub-emoji { font-size: 2.6em; margin-bottom: 8px; display:block; }
.hub-nome { font-size: 0.95em; font-weight: 700; color: #1A1A2E !important; margin-bottom: 3px; }
.hub-cat { font-size: 0.72em; color: #6C757D !important; letter-spacing: 0.4px; }
</style>
""", unsafe_allow_html=True)


# ── CÓDIGOS DOS AGENTES EMBUTIDOS ────────────────────────────────────────────
_CODIGOS_AGENTES = {
    "guia_viagens": """# [hub] import streamlit as st
# [hub] from groq import Groq
# [hub] from datetime import datetime
# [hub] import json

# --- CONFIGURAÇÃO DA PÁGINA ---
# set_page_config removido pelo super_agente

st.markdown(\"\"\"
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
[data-testid="stToolbar"] {visibility: hidden;}
[data-testid="stDecoration"] {visibility: hidden;}
[data-testid="stStatusWidget"] {visibility: hidden;}
</style>
\"\"\", unsafe_allow_html=True)


# --- ESTILO CSS ---
st.markdown(\"\"\"
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    .stApp { background-color:#F8F9FA; font-family:'Inter',sans-serif; }
    [data-testid="stSidebar"] { display:none; }

    .stTextInput>div>div>input, .stTextArea>div>textarea,
    .stSelectbox>div>div>div, .stNumberInput>div>div>input {
        background-color:#FFFFFF !important; color:#1A1A2E !important;
        border:1px solid #CED4DA !important; font-family:'Inter',sans-serif !important;
    }

    .stButton>button {
        width:100%; border-radius:10px; height:3.2em;
        background:linear-gradient(135deg,#495057,#343A40) !important; color:white !important;
        font-weight:600; border:none; box-shadow:2px 2px 8px rgba(0,0,0,0.1);
        font-family:'Inter',sans-serif !important; transition:all 0.2s ease;
    }
    .stButton>button:hover { background:linear-gradient(135deg,#343A40,#212529) !important; transform:translateY(-1px); }
    .stApp .stButton>button, .stApp .stButton>button p,
    .stApp .stButton>button span, .stApp .stButton>button div { color:white !important; }

    .stApp h1, .stApp h2, .stApp h3 { color:#1A1A2E !important; font-family:'Inter',sans-serif !important; font-weight:700 !important; }

    .card { background:linear-gradient(135deg,#F1F3F5,#E9ECEF); padding:20px; border-radius:14px; border:1px solid #CED4DA; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card, .stApp .card p, .stApp .card span, .stApp .card div, .stApp .card strong, .stApp .card em { color:#1A1A2E !important; }

    .card-dark { background:linear-gradient(135deg,#E9ECEF,#DEE2E6); padding:20px; border-radius:14px; border:1px solid #ADB5BD; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-dark, .stApp .card-dark p, .stApp .card-dark span, .stApp .card-dark div, .stApp .card-dark strong { color:#1A1A2E !important; }

    .card-green { background:linear-gradient(135deg,#F0FDF4,#DCFCE7); padding:20px; border-radius:14px; border:1px solid #86EFAC; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-green, .stApp .card-green p, .stApp .card-green span, .stApp .card-green div { color:#14532D !important; }

    .card-blue { background:linear-gradient(135deg,#EFF6FF,#DBEAFE); padding:20px; border-radius:14px; border:1px solid #93C5FD; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-blue, .stApp .card-blue p, .stApp .card-blue span, .stApp .card-blue div { color:#1E3A8A !important; }

    .card-red { background:linear-gradient(135deg,#FFF5F5,#FEE2E2); padding:20px; border-radius:14px; border:1px solid #FECACA; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-red, .stApp .card-red p, .stApp .card-red span, .stApp .card-red div { color:#7F1D1D !important; }

    .card-yellow { background:linear-gradient(135deg,#FFFBEB,#FEF3C7); padding:18px; border-radius:12px; border:1px solid #FCD34D; margin-bottom:12px; white-space:normal; word-wrap:break-word; }
    .stApp .card-yellow, .stApp .card-yellow p, .stApp .card-yellow span, .stApp .card-yellow div { color:#78350F !important; }

    .stat-box { background:#FFFFFF; border-radius:12px; padding:16px; text-align:center; border:1px solid #CED4DA; }
    .stApp .stat-box div, .stApp .stat-box span, .stApp .stat-box p { color:#1A1A2E !important; }
    .stApp .stat-numero, .stat-numero { font-size:2em; font-weight:700; color:#495057 !important; }

    .hist-item { background:#FFFFFF; border-radius:10px; padding:12px 16px; margin-bottom:8px; border-left:4px solid #CED4DA; }
    .stApp .hist-item, .stApp .hist-item p, .stApp .hist-item span, .stApp .hist-item div, .stApp .hist-item small { color:#1A1A2E !important; }

    .badge { background:#495057; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-verde { background:#059669; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-amarelo { background:#B45309; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-azul { background:#1D4ED8; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-roxo { background:#6D28D9; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }

    .divider { border:none; height:1px; background:linear-gradient(to right,transparent,#CED4DA,transparent); margin:18px 0; }

    .chat-user { background:#FFFFFF; border:1px solid #CED4DA; border-radius:12px 12px 4px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-user, .stApp .chat-user p, .stApp .chat-user span, .stApp .chat-user div { color:#1A1A2E !important; }

    .chat-persona { background:#F8F9FA; border:1px solid #CED4DA; border-radius:4px 12px 12px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-persona, .stApp .chat-persona p, .stApp .chat-persona span, .stApp .chat-persona div { color:#1A1A2E !important; }

    .questao-box { background:#FFFFFF; border:2px solid #CED4DA; border-radius:12px; padding:18px; margin-bottom:14px; }
    .stApp .questao-box, .stApp .questao-box p, .stApp .questao-box span, .stApp .questao-box div { color:#1A1A2E !important; }

    .avaliacao-box { background:#FFFFFF; border:2px solid #CED4DA; border-radius:14px; padding:18px; margin-bottom:12px; }
    .stApp .avaliacao-box, .stApp .avaliacao-box p, .stApp .avaliacao-box span, .stApp .avaliacao-box div { color:#1A1A2E !important; }

    .meta-box { background:#FFFFFF; border:2px solid #CED4DA; border-radius:12px; padding:16px; text-align:center; margin:10px 0; }
    .stApp .meta-box, .stApp .meta-box div, .stApp .meta-box span { color:#1A1A2E !important; }
    .stApp .meta-numero { font-size:2em; font-weight:700; color:#495057 !important; }

    .chat-scroll-container { max-height:40vh; overflow-y:auto; display:flex; flex-direction:column; scroll-behavior:smooth; padding-bottom:4px; }
    .chat-scroll-container > * { flex-shrink:0; }
    

    </style>
\"\"\", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CACHE
# ─────────────────────────────────────────────
@st.cache_resource
def get_cache_viagens():
    return {"perfis": {}}

_cache = get_cache_viagens()

# ─────────────────────────────────────────────
# PERSISTÊNCIA LOCAL (JSON)
# ─────────────────────────────────────────────
CHAVES_SALVAR = [
    'usuario', 'historico_roteiros', 'viagens_salvas',
    'cidade_origem', 'perfil_viagem', 'orcamento_padrao',
    'viagens_realizadas',
]

def gerar_json_sessao() -> str:
    dados = {k: st.session_state.get(k) for k in CHAVES_SALVAR}
    dados['salvo_em'] = datetime.now().strftime('%d/%m/%Y %H:%M')
    return json.dumps(dados, ensure_ascii=False, indent=2, default=str)

def carregar_json_sessao(dados):
    _bloq = {'api_key','etapa','nome_login','chave_login','upload_login','btn_entrar_login'}
    _pref = (
        'btn_','sel_','ul_','dl_','cad_','_sub','_sm','_tab','_bsc',
        'ativo_','rem_','sel_pet_','ev_','prof_','hig_','prev_',
        'vac_','sint_','comp_','trad_','subs_','amb_','viag_','chat_',
        'duvida_','emerg_','peso_','data_','obs_','tipo_','vet_','desc_',
        'local_','prox_','alim','sit_emerg_','tc_','oraf','siau','agmag',
        'lv','mv','pt','pi','sh','wc','rv','rp','rc',
    )
    import re as _re
    for k, v in dados.items():
        if k in _bloq: continue
        if any(k.startswith(p) for p in _pref): continue
        if _re.match(r'.+_\\d+$', k): continue
        st.session_state[k] = v

def salvar_perfil_cache(usuario: str):
    _cache["perfis"][usuario] = {k: st.session_state.get(k) for k in CHAVES_SALVAR}

def perfis_salvos() -> list:
    return list(_cache["perfis"].keys())

def carregar_perfil_cache(usuario: str) -> dict | None:
    return _cache["perfis"].get(usuario)

def salvar_roteiro(tipo: str, destino: str, conteudo: str):
    st.session_state.historico_roteiros.append({
        'data':     datetime.now().strftime('%d/%m %H:%M'),
        'tipo':     tipo,
        'destino':  destino,
        'conteudo': conteudo,
    })

# --- INICIALIZAÇÃO DE ESTADO ---
defaults = {
    'etapa':               "Login",
    'usuario':             "",
    'api_key':             "",
    'pagina':              "Home",
    'historico_roteiros':  [],
    'viagens_salvas':      [],
    'cidade_origem':       "",
    'perfil_viagem':       "Cultural e histórico",
    'orcamento_padrao':    3000,
    'viagens_realizadas':  0,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# --- NORMALIZA TABELAS DE FRASES (converte tabs em pipes, garante separador) ---
def normalizar_tabelas_frases(texto: str) -> str:
    \"\"\"
    Garante que todas as tabelas de frases usem formato pipe markdown.
    Converte linhas com tabs em linhas com pipes.
    Injeta linha separadora |---|---| quando ausente (só após cabeçalho).
    \"\"\"
    linhas = texto.split('\\n')
    resultado = []
    aguardando_separador = False
    i = 0
    while i < len(linhas):
        linha = linhas[i]

        # Linha com tabs (formato errado): converte para pipes
        if '\\t' in linha and not linha.strip().startswith('|'):
            partes = [p.strip() for p in linha.split('\\t') if p.strip()]
            if len(partes) >= 2:
                linha = '| ' + ' | '.join(partes) + ' |'

        eh_linha_tabela = linha.strip().startswith('|') and linha.strip().endswith('|')
        eh_separador = '---' in linha and linha.strip().startswith('|')

        if eh_linha_tabela and not eh_separador:
            if aguardando_separador:
                # Esta é uma linha de dados após o cabeçalho — ok, já inserimos o separador
                resultado.append(linha)
            else:
                # Este é o cabeçalho — verifica se próxima linha tem separador
                resultado.append(linha)
                prox = linhas[i+1].strip() if i+1 < len(linhas) else ''
                # Converte próxima linha se for tab
                if '\\t' in prox:
                    partes_prox = [p.strip() for p in prox.split('\\t') if p.strip()]
                    prox = '| ' + ' | '.join(partes_prox) + ' |' if len(partes_prox) >= 2 else prox
                if not (prox.startswith('|---') or prox.startswith('| ---') or '---' in prox):
                    colunas = len([c for c in linha.split('|') if c.strip()])
                    resultado.append('|' + '|'.join(['---'] * colunas) + '|')
                aguardando_separador = True
        elif eh_separador:
            resultado.append(linha)
            aguardando_separador = True
        else:
            aguardando_separador = False
            resultado.append(linha)
        i += 1

    return '\\n'.join(resultado)

# --- MOTOR DE IA ---
def viagem_ia(prompt: str, system_extra: str = "") -> str:
    try:
        client = Groq(api_key=st.session_state.api_key)
        system = f\"\"\"Você é um especialista em turismo e planejamento de viagens no Brasil e no mundo. REGRA DE OURO — CONFIABILIDADE 100%%: Forneça APENAS informações que você tem certeza absoluta que são verdadeiras. JAMAIS invente, suponha, extrapole ou preencha lacunas com dados fictícios. Se não souber algo com certeza — preço, endereço, horário, nome, estatística, lei, fato — diga EXPLICITAMENTE: 'Não tenho certeza sobre isso, recomendo verificar em [fonte].' É melhor uma resposta incompleta e honesta do que uma resposta completa e inventada. O usuário depende dessas informações para tomar decisões reais.
Usuário: {st.session_state.usuario}.
Cidade de origem: {st.session_state.cidade_origem or 'Brasil'}.
Perfil de viagem: {st.session_state.perfil_viagem}.
{system_extra}
REGRAS:
- Seja específico com nomes de lugares, restaurantes, hotéis e atrações reais
- REGRA CRÍTICA DE FORMATAÇÃO: sempre escreva R$30, R$120, R$1.500 — NUNCA escreva "R 30" ou "R 120" sem o cifrão. O símbolo correto é R$ colado ao número, sem espaço entre R e $.
- Indique horários de funcionamento quando relevante
- Dê dicas práticas que guias normais não dão
- Escreva em português brasileiro natural e animado\"\"\"
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system},
                {"role": "user",   "content": prompt},
            ],
            model="openai/gpt-oss-120b",
        )
        txt = response.choices[0].message.content
        if txt: st.session_state['res_geral_guiavi1'] = str(txt)
        if txt: st.session_state['res__guiavi1'] = txt
        # Corrige cifrão quebrado gerado pelo modelo — múltiplos padrões
        import re as _re
        # R` R' R´ R` seguido de número
        txt = _re.sub(r'R\\s*[`\\'´\\u0060]\\s*(\\d)', r'R$\\1', txt)
        txt = _re.sub(r'R\\s*[`\\'´\\u0060]\\s*([A-Z])', r'R$ \\1', txt)
        txt = txt.replace('R` ', 'R$').replace('R`', 'R$')
        txt = txt.replace("R' ", 'R$').replace("R'", 'R$')
        txt = txt.replace('R´ ', 'R$').replace('R´', 'R$')
        # "R 80" → "R$80" (R sozinho seguido de espaço e número)
        txt = _re.sub(r'\\bR\\b\\s+(\\d)', r'R$\\1', txt)
        # "R 30,50" ou "R 120.000"
        txt = _re.sub(r'\\bR\\s+(\\d[\\d.,]*)', r'R$\\1', txt)
        # Markdown bold quebrado: **R 30** → **R$30**
        txt = _re.sub(r'\\*\\*R\\s+(\\d)', r'**R$\\1', txt)
        # "R 30 50" sem cifrão (dois números juntos com R na frente)
        txt = _re.sub(r'\\bR\\b\\s*(?!\\$)(\\d)', r'R$\\1', txt)
        return txt
    except Exception as e:
        return f"⚠️ Erro na API: {e}"

# --- BARRA DE SALVAR ---
def barra_salvar():
    salvar_perfil_cache(st.session_state.usuario)
    nome_usuario = st.session_state.usuario.lower().replace(' ', '_') or 'minha_sessao'
    total  = len(st.session_state.historico_roteiros)
    salvos = len(st.session_state.viagens_salvas)

    col_info, col_btn = st.columns([4, 2])
    with col_info:
        st.markdown(
            f"<div style='background:#F0F9FF;border:1px solid #7DD3FC;border-radius:10px;"
            f"padding:10px 14px;font-size:0.84em;color:#1A1A2E;line-height:1.6;'>"
            f"💾 <strong>Antes de sair, salve seus dados no computador.</strong><br>"
            f"<span style='color:#888;font-size:0.88em;'>{total} roteiros gerados · {salvos} viagens salvas</span>"
            f"</div>",
            unsafe_allow_html=True
        )
    with col_btn:
        st.download_button(
            label="💾 SALVAR MEUS DADOS (.json)",
            data=gerar_json_sessao(),
            file_name=f"guia_viagens_{nome_usuario}.json",
            mime="application/json",
            use_container_width=True,
            key="guiaviag40"
        )
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown(\"\"\"<style>
    .dica-nav{font-size:0.72em;color:#94A3B8;text-align:center;padding:2px 0 6px;}
    .dica-mobile{display:none;}
    .dica-desktop{display:block;}
    @media(max-width:768px){.dica-mobile{display:block;}.dica-desktop{display:none;}}
    </style>
    <div class='dica-nav dica-mobile'>👆 Deslize o dedo para navegar entre as abas</div>
    <div class='dica-nav dica-desktop'>📋 Clique no ícone acima para abrir o menu completo</div>
    \"\"\", unsafe_allow_html=True)

# ============================================================
# TELA: LOGIN
# ============================================================
if 'cidade_origem' not in st.session_state: st.session_state['cidade_origem'] = None
if 'historico_roteiros' not in st.session_state: st.session_state['historico_roteiros'] = []
if 'orcamento_padrao' not in st.session_state: st.session_state['orcamento_padrao'] = None
if 'perfil_viagem' not in st.session_state: st.session_state['perfil_viagem'] = None
if 'viagens_salvas' not in st.session_state: st.session_state['viagens_salvas'] = []

if st.session_state.etapa == "Login":
    st.markdown("# 🤖 GUIA DE VIAGENS IA")
    st.markdown("<div class=\\'card\\'><b>🔒 ACESSO RESTRITO A CLIENTES DO MEUSAGENTESIA.COM.BR</b><br>🔗 <a href='https://meusagentesia.com.br' target='_blank' style='color:#4F46E5;font-weight:700;text-decoration:underline;'>meusagentesia.com.br</a></div>", unsafe_allow_html=True)
    st.info("💻 **Dica:** Pela complexidade dos agentes, no computador a experiência é mais agradável.")
    with st.container():
        nome  = st.text_input("Seu Nome:", key="nome_login")
        chave = st.text_input("🔑 Sua Chave API da Groq:", type="password", key="chave_login")
        if st.button("✨ ENTRAR", key="btn_entrar_login"):
            if len(nome.strip()) < 2:
                st.warning("Digite um nome com pelo menos 2 caracteres.")
            elif chave.strip():
                st.session_state.usuario = nome.strip()
                st.session_state.api_key = chave
                st.session_state.etapa = "App"
                st.rerun()
            else:
                st.warning("Preencha nome e chave API.")

elif st.session_state.etapa == "App":



    # TABS — navegação nativa
    _tab_Home, _tab_Roteiro, _tab_Brasil, _tab_Orcamento, _tab_Frases, _tab_Checklist, _tab_Grupo, _tab_Salvos, _tab_Destino, _tab_Mapa, _tab_Moeda, _tab_Clima, _tab_Seguranca, _tab_Historia, _tab_PDF, _tab_Economizar, _tab_Armadilha, _tab_Pessoas = st.tabs(['🏠 Home', '🗺️ Roteiro', '🇧🇷 Brasil', '💰 Orcamento', '🗣️ Frases', '🧳 Checklist', '👥 Grupo', '❤️ Salvos', '🌍 Destino', '🗺 Mapa', '💱 Moeda', '🌤️ Clima', '🛡️ Seguranca', '🏛️ Historia', '📄 PDF', '💸 Economizar', '🚫 Armadilha', '🤝 Pessoas'])

    # ── BARRA SALVAR — aparece em todas as abas ──
    with st.expander("💾 Salvar / Carregar meus dados", expanded=False):
        _bsc1, _bsc2 = st.columns(2)
        with _bsc1:
            import json as _jsv
            _dsv = {k: st.session_state.get(k) for k in list(st.session_state.keys()) if not k.startswith('_') and k not in ('api_key',)}
    with _tab_Home:
            col_u, col_r = st.columns([3, 1])
            with col_u:
                st.title(f"Bora viajar, {st.session_state.usuario}! ✈️")
                st.markdown("<span class='badge'>Explorador</span>", unsafe_allow_html=True)
            with col_r:
                if st.button("🚪 Sair", key="guiaviag3"):
                    for k in list(st.session_state.keys()):
                        del st.session_state[k]
                    st.rerun()

            # AVISO SE DADOS SUMIRAM
            if len(st.session_state.historico_roteiros) == 0 and len(st.session_state.viagens_salvas) == 0:
                st.markdown(\"\"\"<div style="background:#FEF3C7;border:2px solid #F59E0B;border-radius:12px;
                padding:12px 18px;margin-bottom:4px;color:#000;font-size:0.9em;font-weight:600;">
                ⚠️ Seus dados não estão mais no servidor.
                </div>\"\"\", unsafe_allow_html=True)
            # PERFIL DO VIAJANTE
            st.markdown("#### ⚙️ Seu perfil de viajante")
            col_a, col_b = st.columns(2)
            with col_a:
                st.session_state.cidade_origem  = st.text_input(
                    "De qual cidade você sai:", value=st.session_state.cidade_origem,
                    placeholder="ex: São Paulo, Fortaleza, Belo Horizonte...", key="guiaviag39")
                st.session_state.perfil_viagem  = st.selectbox(
                    "Seu estilo de viagem:", [
                        "Cultural e histórico","Aventura e natureza","Praia e relaxamento",
                        "Gastronomia e vinhos","Família com crianças","Casal romântico",
                        "Mochilão econômico","Luxo e conforto","Religioso e espiritual",
                    ],
                    index=["Cultural e histórico","Aventura e natureza","Praia e relaxamento",
                        "Gastronomia e vinhos","Família com crianças","Casal romântico",
                        "Mochilão econômico","Luxo e conforto","Religioso e espiritual",
                    ].index(st.session_state.perfil_viagem) if st.session_state.perfil_viagem in
                    ["Cultural e histórico","Aventura e natureza","Praia e relaxamento",
                        "Gastronomia e vinhos","Família com crianças","Casal romântico",
                        "Mochilão econômico","Luxo e conforto","Religioso e espiritual"] else 0, key="guiaviag38")
            with col_b:
                st.session_state.orcamento_padrao = st.number_input(
                    "Orçamento médio por viagem (R$):", min_value=500, max_value=100000,
                    value=st.session_state.orcamento_padrao, step=500, key="guiaviag37")


            # MÉTRICAS
            total  = len(st.session_state.historico_roteiros)
            salvos = len(st.session_state.viagens_salvas)
            tipos  = {}
            for r in st.session_state.historico_roteiros:
                tipos[r['tipo']] = tipos.get(r['tipo'], 0) + 1

            c1, c2, c3, c4 = st.columns(4)
            c1.markdown(f"<div class='stat-box'><div class='stat-numero'>{total}</div><div>Roteiros gerados</div></div>", unsafe_allow_html=True)
            c2.markdown(f"<div class='stat-box'><div class='stat-numero'>{salvos}</div><div>Viagens salvas</div></div>", unsafe_allow_html=True)
            c3.markdown(f"<div class='stat-box'><div class='stat-numero'>{tipos.get('Roteiro Completo',0)}</div><div>Roteiros completos</div></div>", unsafe_allow_html=True)
            c4.markdown(f"<div class='stat-box'><div class='stat-numero'>{tipos.get('Fim de Semana',0)}</div><div>FDS planejados</div></div>", unsafe_allow_html=True)

            st.markdown("<div class='card'>💡 <em>'O mundo é um livro e quem não viaja lê apenas uma página.'</em> — Santo Agostinho</div>", unsafe_allow_html=True)

            st.markdown("### 🗺️ O que cada aba faz")
            st.markdown("**Linha 1 — Planejamento principal:**")
            guia1 = {
                "🗺️ Roteiro Completo":       "Roteiro dia a dia completo para qualquer destino — horários, custos, restaurantes com nota, tempo de deslocamento e análise de orçamento",
                "🇧🇷 Fim de Semana no Brasil": "Destinos incríveis perto de você para viajar sem gastar muito",
                "💰 Estimativa de Custos":    "Planejamento financeiro da viagem — passagem, hotel, alimentação, passeios",
                "🗣️ Frases Essenciais":       "As frases mais importantes no idioma local — com pronúncia e dica cultural",
                "🧳 Checklist de Viagem":     "Lista completa do que levar de acordo com o destino e a estação do ano",
                "👥 Viagem em Grupo":         "Plano completo para viagem em grupo — divisão de custos e o que combinar antes",
                "❤️ Viagens Salvas":          "Seus roteiros favoritos organizados e prontos para consultar",
            }
            for aba, desc in guia1.items():
                st.markdown(f"**{aba}** — {desc}")

            st.markdown("**Linha 2 — Módulos avançados:**")
            guia2 = {
                "🌍 Guia do Destino":         "Tudo em um só lugar — clima, segurança, moeda, transporte, saúde, costumes, pratos típicos, festivais e apps",
                "🗺 Mapa dos Passeios":        "Organiza os pontos turísticos por bairro e proximidade com tempo de deslocamento entre cada um",
                "💱 Moeda e Câmbio":          "Câmbio estimado, quanto seu orçamento vale na moeda local e estratégia de pagamento (Wise, C6, espécie)",
                "🌤️ Clima no Período":         "Temperatura, chance de chuva e lista específica de roupas para aquele mês naquele destino",
                "🛡️ Segurança e Saúde":       "Nível de segurança, regiões tranquilas, vacinas, hospitais de referência e seguro viagem",
                "🏛️ Conheça o Destino":       "História, monumentos, filmes gravados, curiosidades, lendas e apps indispensáveis",
                "📄 PDF da Viagem":           "Reformata qualquer roteiro em versão compacta para imprimir ou salvar no celular",
                "💸 Economizar Mais":         "Refaz o roteiro inteiro focando em reduzir custos — atrações gratuitas, hospedagem custo-benefício e análise de orçamento",
                "🚫 Palavras Armadilha":      "Palavras normais em português que são ofensivas ou obscenas no destino — e o inverso também",
                "🤝 Como São as Pessoas":     "Cumprimentos, presentes que ofendem, o que falar e evitar, etiqueta à mesa, dinâmica social e o que os locais adoram (e não gostam) no jeito brasileiro",
            }
            for aba, desc in guia2.items():
                st.markdown(f"**{aba}** — {desc}")

            if st.session_state.historico_roteiros:
                st.markdown("### 🕐 Últimos Roteiros")
                for item in reversed(st.session_state.historico_roteiros[-4:]):
                    st.markdown(
                        f"<div class='hist-item'>"
                        f"<span class='badge'>{item['tipo']}</span> "
                        f"<span class='badge-laranja'>✈️ {item.get('destino', '')}</span> "
                        f"<small style='color:#888'>{item['data']}</small></div>",
                        unsafe_allow_html=True
                    )

        # ========================
        # ROTEIRO COMPLETO
        # ========================

    with _tab_Roteiro:
            st.header("🗺️ Roteiro Completo de Viagem")
            st.markdown("Roteiro dia a dia detalhado — do café da manhã ao jantar, com custos e dicas exclusivas.")

            col1, col2 = st.columns(2)
            with col1:
                destino   = st.text_input("✈️ Destino:", placeholder="ex: Lisboa, Cancún, Nordeste Brasileiro, Roma, Tokyo...", key="guiaviag4")
                dias      = st.slider("📅 Quantos dias:", 2, 21, 7, key="guiaviag1")
                origem    = st.text_input("🏠 Saindo de:", value=st.session_state.cidade_origem, placeholder="ex: São Paulo, Recife...", key="guiaviag5")
            with col2:
                orcamento = st.number_input("💰 Orçamento total (R$):", min_value=500, max_value=200000,
                    value=st.session_state.orcamento_padrao, step=500, key="guiaviag36")
                perfil    = st.selectbox("🎭 Estilo da viagem:", [
                    "Cultural e histórico","Aventura e natureza","Praia e relaxamento",
                    "Gastronomia","Família com crianças","Casal romântico",
                    "Mochilão econômico","Luxo e conforto",
                ], index=["Cultural e histórico","Aventura e natureza","Praia e relaxamento",
                    "Gastronomia","Família com crianças","Casal romântico",
                    "Mochilão econômico","Luxo e conforto"].index(
                    st.session_state.perfil_viagem) if st.session_state.perfil_viagem in
                    ["Cultural e histórico","Aventura e natureza","Praia e relaxamento",
                    "Gastronomia","Família com crianças","Casal romântico",
                    "Mochilão econômico","Luxo e conforto"] else 0, key="guiaviag35")
                pessoas   = st.selectbox("👥 Quantas pessoas:", ["1 pessoa","2 pessoas","3-4 pessoas","5+ pessoas"], key="guiaviag6")
                epoca     = st.text_input("📅 Período da viagem:", placeholder="ex: janeiro, carnaval, julho, qualquer época...", key="guiaviag7")

            if st.button("🗺️ GERAR ROTEIRO COMPLETO", key="guiaviag8"):
                if destino.strip():
                    with st.spinner(f"Montando seu roteiro para {destino}..."):
                        # Detecta se é destino internacional com euro
                        paises_euro = ["portugal","lisboa","porto","espanha","madrid","barcelona","frança","paris","itália","roma","milão","alemanha","berlim","grécia","atenas","holanda","amsterdam","bélgica","bruxelas","áustria","viena","irlanda","dublin"]
                        usa_euro = any(p in destino.lower() for p in paises_euro)
                        moeda_info = "O destino usa Euro (€). Mostre os preços em € e também a conversão estimada em R$ (considere câmbio de aproximadamente R$6 por €1). " if usa_euro else ""

                        prompt = (
                            f"Crie um roteiro completo de {dias} dias para {destino}.\\n"
                            f"Saindo de: {origem or 'Brasil'}. Orçamento: R${orcamento}. "
                            f"Estilo: {perfil}. Pessoas: {pessoas}. Época: {epoca or 'qualquer'}.\\n"
                            f"{moeda_info}\\n\\n"
                            f"INSTRUÇÕES IMPORTANTES:\\n"
                            f"- Todos os preços são ESTIMATIVAS e podem variar — informe isso sempre\\n"
                            f"- Inclua links para sites oficiais ou de compra de ingressos sempre que possível\\n"
                            f"- Sugira restaurantes com nota média (ex: ⭐4.5) e faixa de preço (€/R$ por pessoa)\\n"
                            f"- Informe o tempo de deslocamento entre pontos turísticos (ex: 15 min a pé, 20 min de metrô)\\n"
                            f"- Ao final, calcule o orçamento total e avise se R${orcamento} é suficiente ou não\\n"
                            f"- Inclua sugestão de restaurante por dia com nome real, prato recomendado e preço\\n\\n"
                            f"ESTRUTURA:\\n\\n"
                            f"✈️ ROTEIRO: {destino.upper()} — {dias} DIAS\\n"
                            f"Estilo: {perfil} | {pessoas} | Orçamento: R${orcamento} total\\n\\n"
                            f"📋 INFORMAÇÕES ESSENCIAIS:\\n"
                            f"• Melhor época para ir\\n"
                            f"• Como chegar (passagem estimada de {origem or 'Brasil'})\\n"
                            f"• Documentos necessários\\n"
                            f"• Moeda e câmbio estimado\\n"
                            f"• Fuso horário\\n\\n"
                            f"Para CADA dia use este formato:\\n\\n"
                            f"━━━━━━━━━━━━━━━━━━━━━\\n"
                            f"📅 DIA [N] — [TEMA DO DIA]\\n"
                            f"━━━━━━━━━━━━━━━━━━━━━\\n"
                            f"☕ Manhã ([horário]):\\n"
                            f"• [Local] — [dica exclusiva] — aprox. [preço] (⚠️ estimativa, pode variar)\\n"
                            f"  🔗 Site/ingresso: [link oficial se existir]\\n"
                            f"  🚶 Deslocamento até próximo ponto: [X min a pé / metrô / táxi]\\n\\n"
                            f"🍽️ Almoço ([horário]):\\n"
                            f"• [Nome do restaurante] ⭐[nota] — [prato recomendado] — [faixa de preço] p/pessoa\\n\\n"
                            f"🌅 Tarde ([horário]):\\n"
                            f"• [Local] — [dica] — [preço] (⚠️ estimativa)\\n"
                            f"  🔗 [link se existir]\\n"
                            f"  🚶 Deslocamento: [X min]\\n\\n"
                            f"🌙 Noite ([horário]):\\n"
                            f"• [Jantar: restaurante ⭐nota] — [preço]\\n"
                            f"• [Programa noturno opcional]\\n\\n"
                            f"💰 Gasto estimado do dia: [preço] p/pessoa (⚠️ estimativa)\\n\\n"
                            f"[Repita para todos os {dias} dias]\\n\\n"
                            f"🗺️ ORDEM SUGERIDA DOS PASSEIOS (para reduzir deslocamentos):\\n"
                            f"[Liste os pontos turísticos em ordem geográfica para minimizar trajetos, com bairro de cada um]\\n\\n"
                            f"🍽️ TOP RESTAURANTES DO ROTEIRO:\\n"
                            f"[Lista dos melhores mencionados com: nome, culinária, nota, faixa de preço, bairro]\\n\\n"
                            f"🏨 HOSPEDAGEM SUGERIDA:\\n"
                            f"[3 opções: econômico, intermediário, confortável — com bairro e preço/noite]\\n\\n"
                            f"🚗 COMO SE LOCOMOVER:\\n"
                            f"[Transporte local — app, metrô, carro, táxi — com custos e dicas]\\n\\n"
                            f"📊 RESUMO FINANCEIRO COMPLETO:\\n"
                            f"Passagem: [preço]\\n"
                            f"Hospedagem {dias} noites: [preço]\\n"
                            f"Alimentação: [preço]\\n"
                            f"Passeios e ingressos: [preço]\\n"
                            f"Transporte local: [preço]\\n"
                            f"Total estimado: [preço] p/pessoa\\n\\n"
                            f"⚠️ ANÁLISE DO ORÇAMENTO:\\n"
                            f"[Calcule se R${orcamento} é suficiente para {pessoas}. Se não for, indique quanto falta e onde cortar]\\n\\n"
                            f"💡 DICAS DE OURO:\\n"
                            f"[5 dicas que só quem conhece {destino} de verdade sabe]"
                        )
                        res = viagem_ia(prompt)
                        salvar_roteiro("Roteiro Completo", destino, res)
                        st.session_state['roteiro_temp'] = res
                        st.session_state['roteiro_destino'] = destino
                        st.session_state['roteiro_dias'] = dias
                        st.session_state['roteiro_orcamento'] = orcamento
                        st.session_state['roteiro_pessoas'] = pessoas
                        st.session_state['roteiro_epoca'] = epoca
                        st.markdown(f"<div class='card'>{res}</div>", unsafe_allow_html=True)
                else:
                    st.warning("Informe o destino da viagem.")

            if st.session_state.get('roteiro_temp'):
                col_dl, col_sv, col_novo = st.columns(3)
                with col_dl:
                    st.download_button("📋 Baixar roteiro (.txt)",
                        data=st.session_state['roteiro_temp'],
                        file_name=f"roteiro_{destino.replace(' ','_') if 'destino' in dir() else 'viagem'}.txt",
                        mime="text/plain", use_container_width=True, key="guiaviag34")
                with col_sv:
                    if st.button("❤️ Salvar viagem", use_container_width=True, key="guiaviag9"):
                        st.session_state.viagens_salvas.append({
                            'tipo': 'Roteiro Completo',
                            'destino': destino if 'destino' in dir() else '',
                            'conteudo': st.session_state['roteiro_temp'],
                            'data': datetime.now().strftime('%d/%m %H:%M'),
                        })
                        st.success("❤️ Salvo!")
                with col_novo:
                    if st.button("🔄 Gerar outro roteiro", use_container_width=True, key="guiaviag10"):
                        st.session_state.pop('roteiro_temp', None)
                        st.rerun()

        # ========================
        # FIM DE SEMANA NO BRASIL
        # ========================

    with _tab_Brasil:
            st.header("🇧🇷 Fim de Semana no Brasil")
            st.markdown("Descubra destinos incríveis perto de você — para viajar sem gastar muito.")

            col1, col2 = st.columns(2)
            with col1:
                origem_br  = st.text_input("🏠 Sua cidade:", value=st.session_state.cidade_origem,
                    placeholder="ex: São Paulo, Recife, Belo Horizonte...", key="guiaviag33")
                distancia  = st.selectbox("📍 Distância máxima:", [
                    "Até 3 horas de carro","Até 5 horas de carro","Até 2 horas de avião","Qualquer lugar do Brasil",
                ], key="guiaviag32")
                orcamento_br= st.number_input("💰 Orçamento do fim de semana (R$):",
                    min_value=200, max_value=10000, value=1500, step=200, key="guiaviag31")
            with col2:
                perfil_br  = st.selectbox("🎭 O que você quer:", [
                    "Praia e mar","Serra e natureza","Cidade histórica","Parque e ecoturismo",
                    "Gastronomia regional","Aventura e esportes","Sossego e descanso",
                ], key="guiaviag30")
                pessoas_br = st.selectbox("👥 Viajantes:", ["Só eu","Casal","Família com crianças","Grupo de amigos"], key="guiaviag11")
                carro      = st.checkbox("🚗 Tenho carro", value=True, key="guiaviag12")

            if st.button("🇧🇷 ENCONTRAR DESTINOS PERFEITOS", key="guiaviag13"):
                if origem_br.strip():
                    with st.spinner("Procurando os melhores destinos..."):
                        prompt = (
                            f"Sugira 3 destinos para fim de semana saindo de {origem_br}.\\n"
                            f"Distância: {distancia}. Orçamento: R${orcamento_br}. "
                            f"Perfil: {perfil_br}. Viajantes: {pessoas_br}. "
                            f"{'Tem carro.' if carro else 'Sem carro — vai de ônibus ou avião.'}\\n\\n"
                            f"Para CADA destino:\\n\\n"
                            f"🏖️ DESTINO [N]: [NOME DA CIDADE/LUGAR]\\n"
                            f"📍 Estado: [X] | Distância de {origem_br}: [X] horas\\n"
                            f"⭐ Por que ir: [3 motivos específicos]\\n\\n"
                            f"📅 ROTEIRO DO FIM DE SEMANA:\\n\\n"
                            f"SÁBADO:\\n"
                            f"• Manhã: [o que fazer] — R$[X]\\n"
                            f"• Almoço: [onde comer — restaurante específico] — R$[X]\\n"
                            f"• Tarde: [o que fazer] — R$[X]\\n"
                            f"• Jantar: [onde comer] — R$[X]\\n\\n"
                            f"DOMINGO:\\n"
                            f"• Manhã: [o que fazer] — R$[X]\\n"
                            f"• Almoço: [onde comer] — R$[X]\\n"
                            f"• Retorno: [horário sugerido]\\n\\n"
                            f"💰 CUSTO TOTAL ESTIMADO:\\n"
                            f"• Transporte (ida e volta): R$[X]\\n"
                            f"• Hospedagem (1 noite): R$[X]\\n"
                            f"• Alimentação: R$[X]\\n"
                            f"• Passeios: R$[X]\\n"
                            f"• TOTAL: R$[X] p/pessoa\\n\\n"
                            f"🏨 Onde ficar: [2 sugestões com preço/noite]\\n"
                            f"💡 Dica especial: [algo que poucos turistas sabem]\\n\\n"
                            f"---\\n\\n"
                            f"[Repita para os 3 destinos]\\n\\n"
                            f"🏆 NOSSA RECOMENDAÇÃO:\\n"
                            f"[Qual dos 3 é melhor para esse perfil e por quê]"
                        )
                        res = viagem_ia(prompt)
                        salvar_roteiro("Fim de Semana", f"FDS saindo de {origem_br}", res)
                        st.session_state['brasil_temp'] = res
                        st.markdown(f"<div class='card-green'>{res}</div>", unsafe_allow_html=True)
                else:
                    st.warning("Informe sua cidade de origem.")

            if st.session_state.get('brasil_temp'):
                col_dl, col_sv = st.columns(2)
                with col_dl:
                    st.download_button("📋 Baixar roteiro (.txt)", data=st.session_state['brasil_temp'],
                        file_name="fim_de_semana_brasil.txt", mime="text/plain", use_container_width=True, key="guiaviag29")
                with col_sv:
                    if st.button("❤️ Salvar", key="sv_br", use_container_width=True):
                        st.session_state.viagens_salvas.append({
                            'tipo': 'Fim de Semana', 'destino': f"FDS de {origem_br if 'origem_br' in dir() else ''}",
                            'conteudo': st.session_state['brasil_temp'],
                            'data': datetime.now().strftime('%d/%m %H:%M'),
                        })
                        st.success("❤️ Salvo!")

        # ========================
        # ESTIMATIVA DE CUSTOS
        # ========================

    with _tab_Orcamento:
            st.header("💰 Estimativa de Custos da Viagem")
            st.markdown("Planejamento financeiro completo — para não ter surpresas na viagem.")

            col1, col2 = st.columns(2)
            with col1:
                destino_o  = st.text_input("✈️ Destino:", placeholder="ex: Europa, Maldivas, Bahia...", key="guiaviag14")
                dias_o     = st.number_input("📅 Dias de viagem:", min_value=2, max_value=60, value=10, key="guiaviag15")
                pessoas_o  = st.number_input("👥 Número de pessoas:", min_value=1, max_value=20, value=2, key="guiaviag16")
            with col2:
                padrao_o   = st.selectbox("⭐ Padrão de viagem:", [
                    "Econômico (mochileiro)","Intermediário (confortável)","Superior (confortável+)","Luxo",
                ], key="guiaviag28")
                origem_o   = st.text_input("🏠 Cidade de origem:", value=st.session_state.cidade_origem, key="guiaviag17")
                tipo_o     = st.radio("Tipo:", ["Internacional","Nacional"], horizontal=True, key="guiaviag18")

            if st.button("💰 GERAR ESTIMATIVA COMPLETA", key="guiaviag19"):
                if destino_o.strip():
                    with st.spinner("Calculando custos..."):
                        prompt = (
                            f"Crie uma estimativa detalhada de custos para viagem.\\n"
                            f"Destino: {destino_o}. Dias: {dias_o}. Pessoas: {pessoas_o}.\\n"
                            f"Padrão: {padrao_o}. Saindo de: {origem_o or 'Brasil'}. Tipo: {tipo_o}.\\n\\n"
                            f"FORMATO:\\n\\n"
                            f"💰 ESTIMATIVA DE CUSTOS — {destino_o.upper()}\\n"
                            f"{dias_o} dias · {pessoas_o} pessoa(s) · Padrão {padrao_o}\\n\\n"
                            f"✈️ PASSAGENS (ida e volta por pessoa):\\n"
                            f"• Preço médio: R$[X]\\n"
                            f"• Melhor época para comprar: [X meses antes]\\n"
                            f"• Sites recomendados: [lista]\\n"
                            f"• Dica para economizar: [estratégia específica]\\n\\n"
                            f"🏨 HOSPEDAGEM (por noite — {dias_o-1} noites):\\n"
                            f"• Econômico: R$[X]/noite — exemplo: [tipo de local]\\n"
                            f"• Recomendado: R$[X]/noite — exemplo: [tipo de local]\\n"
                            f"• Confortável: R$[X]/noite — exemplo: [tipo de local]\\n"
                            f"• Total ({padrao_o}): R$[X]\\n\\n"
                            f"🍽️ ALIMENTAÇÃO (por dia por pessoa):\\n"
                            f"• Café da manhã: R$[X]\\n"
                            f"• Almoço: R$[X]\\n"
                            f"• Jantar: R$[X]\\n"
                            f"• Lanches/bebidas: R$[X]\\n"
                            f"• Total por dia: R$[X] | Total {dias_o} dias: R$[X]\\n\\n"
                            f"🎡 PASSEIOS E ATRAÇÕES:\\n"
                            f"• [Atração 1]: R$[X]\\n"
                            f"• [Atração 2]: R$[X]\\n"
                            f"• [Atração 3]: R$[X]\\n"
                            f"• Estimativa total passeios: R$[X]\\n\\n"
                            f"🚗 TRANSPORTE LOCAL:\\n"
                            f"• [modalidade]: R$[X]/dia\\n"
                            f"• Total: R$[X]\\n\\n"
                            f"🛍️ COMPRAS E SOUVENIRS: R$[X] (estimativa)\\n\\n"
                            f"🏥 SEGURO VIAGEM: R$[X] (recomendado)\\n\\n"
                            f"━━━━━━━━━━━━━━━━━━━━━\\n"
                            f"📊 RESUMO TOTAL:\\n"
                            f"• Por pessoa: R$[X]\\n"
                            f"• Total do grupo ({pessoas_o} pessoas): R$[X]\\n"
                            f"• Reserve mais 15% para imprevistos: R$[X]\\n"
                            f"━━━━━━━━━━━━━━━━━━━━━\\n\\n"
                            f"💡 3 FORMAS DE ECONOMIZAR NESSA VIAGEM:\\n"
                            f"[Dicas específicas para {destino_o} no padrão {padrao_o}]\\n\\n"
                            f"📅 MELHOR ÉPOCA PARA IR (relação custo-benefício):\\n"
                            f"[Meses ideais e por que]"
                        )
                        res = viagem_ia(prompt)
                        salvar_roteiro("Estimativa de Custos", destino_o, res)
                        st.session_state['orcamento_temp'] = res
                        st.markdown(f"<div class='card-orange'>{res}</div>", unsafe_allow_html=True)
                else:
                    st.warning("Informe o destino.")

            if st.session_state.get('orcamento_temp'):
                col_dl, col_sv = st.columns(2)
                with col_dl:
                    st.download_button("📋 Baixar estimativa (.txt)", data=st.session_state['orcamento_temp'],
                        file_name=f"custos_{destino_o.replace(' ','_') if 'destino_o' in dir() else 'viagem'}.txt",
                        mime="text/plain", use_container_width=True, key="guiaviag27")
                with col_sv:
                    if st.button("❤️ Salvar", key="sv_orc", use_container_width=True):
                        st.session_state.viagens_salvas.append({
                            'tipo': 'Estimativa de Custos', 'destino': destino_o if 'destino_o' in dir() else '',
                            'conteudo': st.session_state['orcamento_temp'],
                            'data': datetime.now().strftime('%d/%m %H:%M'),
                        })
                        st.success("❤️ Salvo!")

        # ========================
        # FRASES ESSENCIAIS
        # ========================

    with _tab_Frases:
            st.header("🗣️ Frases Essenciais no Idioma Local")
            st.markdown("As frases que você PRECISA saber para se virar em qualquer país.")

            col1, col2 = st.columns(2)
            with col1:
                pais_f   = st.text_input("🌍 País ou idioma:", placeholder="ex: França, Japão, Espanha, Italiano...", key="guiaviag20")
                contexto_f = st.multiselect("📋 Situações:", [
                    "Hotel e acomodação","Restaurante e comida","Transporte e direções",
                    "Compras e mercado","Emergências e saúde","Turismo e passeios",
                    "Aeroporto e fronteira","Social e apresentações","Números e dinheiro",
                ], default=["Restaurante e comida","Transporte e direções","Emergências e saúde"], key="guiaviag26")
            with col2:
                nivel_f  = st.radio("Nível:", ["Turista básico (sobrevivência)","Intermediário (conforto)","Avançado (fluência básica)"], horizontal=True, key="guiaviag21")
                fonetica = st.checkbox("Incluir pronúncia fonética", value=True, key="guiaviag22")

            if st.button("🗣️ GERAR FRASES ESSENCIAIS", key="guiaviag23"):
                if pais_f.strip():
                    with st.spinner(f"Preparando frases em {pais_f}..."):
                        contexts = ", ".join(contexto_f) if contexto_f else "situações gerais"
                        prompt = (
                            f"Crie um guia de frases essenciais para {pais_f}.\\n"
                            f"Situações: {contexts}. Nível: {nivel_f}.\\n"
                            f"{'Inclua pronúncia fonética entre colchetes.' if fonetica else ''}\\n\\n"
                            f"REGRAS DE FORMATAÇÃO — siga rigorosamente:\\n"
                            f"1. Use SEMPRE tabela markdown com pipes | para todas as seções\\n"
                            f"2. NUNCA use tabulações (tab) para separar colunas\\n"
                            f"3. O título da situação vai na linha imediatamente ANTES da tabela, sem linhas em branco entre eles\\n"
                            f"4. Separe as seções com apenas UMA linha em branco\\n\\n"
                            f"FORMATO EXATO (copie esta estrutura):\\n\\n"
                            f"🍴 Nome da Situação\\n"
                            f"| Português | {pais_f} | {'Pronúncia' if fonetica else ''} |\\n"
                            f"|-----------|---------|{'---------' if fonetica else ''}|\\n"
                            f"| frase em português | tradução | {'[pronúncia]' if fonetica else ''} |\\n\\n"
                            f"🚌 Próxima Situação\\n"
                            f"| Português | {pais_f} | {'Pronúncia' if fonetica else ''} |\\n"
                            f"|-----------|---------|{'---------' if fonetica else ''}|\\n"
                            f"| frase | tradução | {'[pronúncia]' if fonetica else ''} |\\n\\n"
                            f"Mínimo 6 frases por situação. Repita para todas: {contexts}\\n\\n"
                            f"🆘 FRASES DE EMERGÊNCIA\\n"
                            f"| Português | {pais_f} | {'Pronúncia' if fonetica else ''} |\\n"
                            f"|-----------|---------|{'---------' if fonetica else ''}|\\n"
                            f"[10 frases de emergência]\\n\\n"
                            f"📱 APPS DE TRADUÇÃO RECOMENDADOS:\\n"
                            f"[Os melhores apps para {pais_f} — com ou sem internet]\\n\\n"
                            f"💡 DICA CULTURAL:\\n"
                            f"[Como os locais reagem quando estrangeiros tentam falar o idioma]"
                        )
                        res = viagem_ia(prompt)
                        # Normaliza tabelas: converte tabs em pipes e garante cabeçalho separador
                        res = normalizar_tabelas_frases(res)
                        salvar_roteiro("Frases Essenciais", pais_f, res)
                        st.session_state['frases_temp'] = res
                else:
                    st.warning("Informe o país ou idioma.")

            if st.session_state.get('frases_temp'):
                # Usa st.markdown nativo para renderizar tabelas markdown corretamente
                st.markdown(\"\"\"
                <div style='background:linear-gradient(135deg,#F5F3FF,#EDE9FE);
                border:1px solid #C4B5FD;border-radius:16px;padding:20px 24px;margin-bottom:15px;'>
                </div>
                \"\"\", unsafe_allow_html=True)
                st.markdown(st.session_state['frases_temp'])
                col_dl, col_sv = st.columns(2)
                with col_dl:
                    st.download_button("📋 Baixar frases (.txt)", data=st.session_state['frases_temp'],
                        file_name=f"frases_{pais_f.replace(' ','_') if 'pais_f' in dir() else 'idioma'}.txt",
                        mime="text/plain", use_container_width=True, key="guiaviag25")
                with col_sv:
                    if st.button("❤️ Salvar", key="sv_fr", use_container_width=True):
                        st.session_state.viagens_salvas.append({
                            'tipo': 'Frases Essenciais', 'destino': pais_f if 'pais_f' in dir() else '',
                            'conteudo': st.session_state['frases_temp'],
                            'data': datetime.now().strftime('%d/%m %H:%M'),
                        })
                        st.success("❤️ Salvo!")

        # ========================
        # CHECKLIST DE VIAGEM
        # ========================

    with _tab_Checklist:
            st.header("🧳 Checklist de Viagem")
            st.markdown("Lista completa e personalizada do que levar — para não esquecer nada importante.")

            col1, col2 = st.columns(2)
            with col1:
                destino_c  = st.text_input("✈️ Destino:", placeholder="ex: Europa no inverno, praia no Nordeste, Tokyo...", key="guiaviag24")
                dias_c     = st.number_input("📅 Dias de viagem:", min_value=1, max_value=60, value=10, key="guiaviag25_d2")
                clima_c    = st.selectbox("🌡️ Clima esperado:", [
                    "Quente e úmido (tropical)","Quente e seco","Frio (abaixo de 15°C)","Muito frio (neve/geada)",
                    "Temperado (ameno)","Variado (várias estações)",
                ], key="guiaviag24_d2")
            with col2:
                tipo_c     = st.selectbox("✈️ Tipo de viagem:", [
                    "Internacional","Nacional — avião","Nacional — carro","Cruzeiro","Camping/Aventura",
                ], key="guiaviag23_d2")
                atividades = st.multiselect("🎯 Atividades planejadas:", [
                    "Praia e mar","Trilhas e montanha","Cidade e museus","Festas e baladas",
                    "Negócios","Mergulho","Esqui","Safari","Spa e relaxamento",
                ], key="guiaviag22_d2")
                mala_c     = st.radio("🧳 Tipo de mala:", ["Mala de despacho","Mochila carry-on","Ambas"], horizontal=True, key="guiaviag26_d2")

            if st.button("🧳 GERAR MEU CHECKLIST PERSONALIZADO", key="guiaviag27_d2"):
                if destino_c.strip():
                    with st.spinner("Montando seu checklist..."):
                        ativ = ", ".join(atividades) if atividades else "turismo geral"
                        prompt = (
                            f"Crie um checklist completo e personalizado de viagem.\\n"
                            f"Destino: {destino_c}. Dias: {dias_c}. Clima: {clima_c}.\\n"
                            f"Tipo: {tipo_c}. Atividades: {ativ}. Mala: {mala_c}.\\n\\n"
                            f"FORMATO:\\n\\n"
                            f"🧳 CHECKLIST — {destino_c.upper()}\\n"
                            f"{dias_c} dias · {clima_c} · {mala_c}\\n\\n"
                            f"📄 DOCUMENTOS E DINHEIRO:\\n"
                            f"[ ] [item — com observação específica]\\n\\n"
                            f"👔 ROUPAS E ACESSÓRIOS:\\n"
                            f"[ ] [item — quantidade sugerida para {dias_c} dias]\\n\\n"
                            f"🧴 HIGIENE E SAÚDE:\\n"
                            f"[ ] [item]\\n\\n"
                            f"💊 MEDICAMENTOS E PRIMEIROS SOCORROS:\\n"
                            f"[ ] [item — com para que serve]\\n\\n"
                            f"📱 TECNOLOGIA E ELETRÔNICOS:\\n"
                            f"[ ] [item — com observação]\\n\\n"
                            f"🎒 ITENS ESPECÍFICOS PARA {ativ.upper()}:\\n"
                            f"[ ] [item específico para as atividades planejadas]\\n\\n"
                            f"🔑 ANTES DE SAIR DE CASA:\\n"
                            f"[ ] [checklist do apartamento/casa]\\n\\n"
                            f"📱 APPS ESSENCIAIS PARA INSTALAR:\\n"
                            f"[ ] [app — para que serve]\\n\\n"
                            f"⚠️ NÃO LEVE NA MALA DE MÃO:\\n"
                            f"[Lista do que é proibido — específico para {tipo_c}]\\n\\n"
                            f"💡 DICA DE MALA:\\n"
                            f"[Como organizar a mala para {dias_c} dias em {mala_c}]"
                        )
                        res = viagem_ia(prompt)
                        salvar_roteiro("Checklist", destino_c, res)
                        st.session_state['check_temp'] = res
                        st.markdown(f"<div class='card-yellow'>{res}</div>", unsafe_allow_html=True)
                else:
                    st.warning("Informe o destino.")

            if st.session_state.get('check_temp'):
                col_dl, col_sv = st.columns(2)
                with col_dl:
                    st.download_button("📋 Baixar checklist (.txt)", data=st.session_state['check_temp'],
                        file_name=f"checklist_{destino_c.replace(' ','_') if 'destino_c' in dir() else 'viagem'}.txt",
                        mime="text/plain", use_container_width=True, key="guiaviag21_d2")
                with col_sv:
                    if st.button("❤️ Salvar", key="sv_ck", use_container_width=True):
                        st.session_state.viagens_salvas.append({
                            'tipo': 'Checklist', 'destino': destino_c if 'destino_c' in dir() else '',
                            'conteudo': st.session_state['check_temp'],
                            'data': datetime.now().strftime('%d/%m %H:%M'),
                        })
                        st.success("❤️ Salvo!")

        # ========================
        # VIAGEM EM GRUPO
        # ========================

    with _tab_Grupo:
            st.header("👥 Plano de Viagem em Grupo")
            st.markdown("Organize tudo antes de sair — divisão de custos, o que combinar e como evitar conflitos.")

            col1, col2 = st.columns(2)
            with col1:
                destino_g  = st.text_input("✈️ Destino:", placeholder="ex: Cartagena, Chapada Diamantina, Buenos Aires...", key="guiaviag28_d2")
                pessoas_g  = st.number_input("👥 Número de pessoas no grupo:", min_value=3, max_value=30, value=6, key="guiaviag29_d2")
                dias_g     = st.number_input("📅 Dias de viagem:", min_value=2, max_value=21, value=5, key="guiaviag30_d2")
            with col2:
                perfil_g   = st.selectbox("🎭 Perfil do grupo:", [
                    "Amigos da faculdade","Família grande","Colegas de trabalho",
                    "Casal + amigos","Grupo misto (famílias e solteiros)","Turma da empresa",
                ], key="guiaviag20_d2")
                orcamento_g= st.number_input("💰 Orçamento por pessoa (R$):", min_value=200, max_value=20000, value=2000, step=200, key="guiaviag31_d2")
                diferencias= st.text_area("⚠️ Restrições ou diferenças no grupo:", height=60,
                    placeholder="ex: 2 vegetarianos, 1 com mobilidade reduzida, crianças pequenas...", key="guiaviag19_d2")

            if st.button("👥 GERAR PLANO COMPLETO PARA GRUPO", key="guiaviag32_d2"):
                if destino_g.strip():
                    with st.spinner("Organizando a viagem em grupo..."):
                        prompt = (
                            f"Crie um plano completo de viagem em grupo.\\n"
                            f"Destino: {destino_g}. Pessoas: {pessoas_g}. Dias: {dias_g}.\\n"
                            f"Perfil: {perfil_g}. Orçamento por pessoa: R${orcamento_g}.\\n"
                            f"Particularidades: {diferencias or 'nenhuma'}.\\n\\n"
                            f"ESTRUTURA:\\n\\n"
                            f"👥 PLANO DE GRUPO — {destino_g.upper()}\\n"
                            f"{pessoas_g} pessoas · {dias_g} dias · R${orcamento_g}/pessoa\\n\\n"
                            f"📋 CHECKLIST PRÉ-VIAGEM (1 mês antes):\\n"
                            f"[O que combinar antes de sair — decisões que precisam ser tomadas em grupo]\\n\\n"
                            f"💰 DIVISÃO DE CUSTOS:\\n"
                            f"• Total estimado do grupo: R${orcamento_g * pessoas_g:,}\\n"
                            f"• Como dividir passagens: [estratégia]\\n"
                            f"• Como dividir hospedagem: [estratégia]\\n"
                            f"• Como dividir refeições: [estratégia — cada um paga o seu ou divide?]\\n"
                            f"• App recomendado para dividir contas: [nome + como usar]\\n\\n"
                            f"🏨 HOSPEDAGEM PARA GRUPO:\\n"
                            f"[Opções ideais para {pessoas_g} pessoas — casa alugada, hostels, hotéis]\\n"
                            f"[Estimativa de custo por pessoa por noite]\\n\\n"
                            f"🗓️ ROTEIRO DO GRUPO (resumido):\\n"
                            f"[Dia a dia — atividades que funcionam bem para grupos de {pessoas_g}]\\n\\n"
                            f"⚠️ REGRAS DO GRUPO (combine antes):\\n"
                            f"[As conversas difíceis que precisam acontecer antes — horários, gastos, preferências]\\n\\n"
                            f"🚗 TRANSPORTE DO GRUPO:\\n"
                            f"[Como se locomover com {pessoas_g} pessoas — van, carros, apps]\\n\\n"
                            f"😤 COMO EVITAR CONFLITOS:\\n"
                            f"[As 5 principais causas de conflito em viagens em grupo e como prevenir]\\n\\n"
                            f"👨‍💼 QUEM ORGANIZA O QUÊ:\\n"
                            f"[Sugestão de divisão de tarefas — passagens, hotel, restaurantes, passeios]\\n\\n"
                            f"💡 DICA ESPECIAL PARA {perfil_g.upper()}:\\n"
                            f"[Conselho específico para esse tipo de grupo]"
                        )
                        res = viagem_ia(prompt)
                        salvar_roteiro("Viagem em Grupo", destino_g, res)
                        st.session_state['grupo_temp'] = res
                        st.markdown(f"<div class='card-dark'>{res}</div>", unsafe_allow_html=True)
                else:
                    st.warning("Informe o destino.")

            if st.session_state.get('grupo_temp'):
                col_dl, col_sv = st.columns(2)
                with col_dl:
                    st.download_button("📋 Baixar plano (.txt)", data=st.session_state['grupo_temp'],
                        file_name=f"grupo_{destino_g.replace(' ','_') if 'destino_g' in dir() else 'viagem'}.txt",
                        mime="text/plain", use_container_width=True, key="guiaviag18_d2")
                with col_sv:
                    if st.button("❤️ Salvar", key="sv_gr", use_container_width=True):
                        st.session_state.viagens_salvas.append({
                            'tipo': 'Viagem em Grupo', 'destino': destino_g if 'destino_g' in dir() else '',
                            'conteudo': st.session_state['grupo_temp'],
                            'data': datetime.now().strftime('%d/%m %H:%M'),
                        })
                        st.success("❤️ Salvo!")

        # ========================
        # VIAGENS SALVAS
        # ========================

    with _tab_Salvos:
            st.header("❤️ Viagens Salvas e Histórico")

            total  = len(st.session_state.historico_roteiros)
            salvos = len(st.session_state.viagens_salvas)
            tipos  = {}
            for r in st.session_state.historico_roteiros:
                tipos[r['tipo']] = tipos.get(r['tipo'], 0) + 1

            c1, c2, c3, c4 = st.columns(4)
            c1.markdown(f"<div class='stat-box'><div class='stat-numero'>{total}</div><div>Roteiros gerados</div></div>", unsafe_allow_html=True)
            c2.markdown(f"<div class='stat-box'><div class='stat-numero'>{salvos}</div><div>Viagens salvas</div></div>", unsafe_allow_html=True)
            c3.markdown(f"<div class='stat-box'><div class='stat-numero'>{tipos.get('Roteiro Completo',0)}</div><div>Roteiros completos</div></div>", unsafe_allow_html=True)
            c4.markdown(f"<div class='stat-box'><div class='stat-numero'>{tipos.get('Fim de Semana',0)}</div><div>FDS planejados</div></div>", unsafe_allow_html=True)

            if st.session_state.viagens_salvas:
                st.markdown("### ❤️ Suas Viagens Favoritas")
                tipos_s = list(set(v['tipo'] for v in st.session_state.viagens_salvas))
                filtro  = st.selectbox("Filtrar:", ["Todos"] + tipos_s, key="guiaviag33_d2")

                viagens_f = [
                    v for v in st.session_state.viagens_salvas
                    if filtro == "Todos" or v['tipo'] == filtro
                ]

                for i, item in enumerate(reversed(viagens_f)):
                    idx_real = len(st.session_state.viagens_salvas) - 1 - i
                    with st.expander(f"❤️ [{item['tipo']}] ✈️ {item.get('destino', '')} — {item['data']}"):
                        st.markdown(f"<div class='card'>{item['conteudo']}</div>", unsafe_allow_html=True)
                        col_dl, col_del = st.columns([3, 1])
                        with col_dl:
                            st.download_button("📋 Baixar", data=item['conteudo'],
                                file_name=f"{item['tipo'].lower().replace(' ','_')}_{item.get('destino', '').replace(' ','_')}.txt",
                                mime="text/plain", key=f"dl_salvo_{i}")
                        with col_del:
                            if st.button("🗑️", key=f"del_salvo_{i}"):
                                st.session_state.viagens_salvas.pop(idx_real)
                                st.rerun()
            else:
                st.info("Nenhuma viagem salva ainda. Gere roteiros e salve os favoritos!")

            if st.session_state.historico_roteiros:
                st.markdown("### 📊 Histórico Completo")
                col_f, col_ex = st.columns([3, 1])
                with col_f:
                    filtro_h = st.selectbox("Filtrar histórico:", ["Todos"] + list(tipos.keys()), key="filtro_hist")
                with col_ex:
                    hist_txt = "\\n\\n".join(
                        f"[{r['data']}] {r['tipo']} — {r['destino']}\\n{r['conteudo']}\\n{'─'*40}"
                        for r in st.session_state.historico_roteiros
                    )
                    st.download_button("⬇️ Exportar TXT", data=hist_txt,
                        file_name="historico_viagens.txt", mime="text/plain", key="guiaviag17_d2")

                for i, item in enumerate(reversed(st.session_state.historico_roteiros)):
                    if filtro_h != "Todos" and item['tipo'] != filtro_h:
                        continue
                    idx_real = len(st.session_state.historico_roteiros) - 1 - i
                    with st.expander(f"[{item['tipo']}] ✈️ {item.get('destino', '')} — {item['data']}"):
                        st.markdown(f"<div class='card'>{item['conteudo']}</div>", unsafe_allow_html=True)
                        col_sv, col_del = st.columns([3, 1])
                        with col_sv:
                            if st.button("❤️ Salvar", key=f"sv_hist_{i}"):
                                st.session_state.viagens_salvas.append(item.copy())
                                st.success("Salvo!")
                        with col_del:
                            if st.button("🗑️", key=f"del_hist_{i}"):
                                st.session_state.historico_roteiros.pop(idx_real)
                                st.rerun()

                if st.button("🗑️ Limpar Todo o Histórico", key="guiaviag34_d2"):
                    st.session_state.historico_roteiros = []
                    st.rerun()

        # ========================
        # GUIA COMPLETO DO DESTINO
        # ========================

    with _tab_Destino:
            st.header("🌍 Guia Completo do Destino")
            st.markdown("Tudo que você precisa saber antes de embarcar — em um só lugar.")

            destino_d = st.text_input("✈️ Destino:", placeholder="ex: Lisboa, Tóquio, Nova York, Marrocos...", key="guiaviag35_d2")
            epoca_d = st.text_input("📅 Período da viagem:", placeholder="ex: janeiro, julho, verão europeu...", key="guiaviag36_d2")

            if st.button("🌍 GERAR GUIA COMPLETO", key="guiaviag37_d2"):
                if destino_d.strip():
                    with st.spinner(f"Reunindo tudo sobre {destino_d}..."):
                        prompt = (
                            f"Crie um guia completo e prático sobre {destino_d} para um viajante brasileiro.\\n"
                            f"Período: {epoca_d or 'geral'}.\\n\\n"
                            f"FORMATO:\\n\\n"
                            f"🌍 GUIA COMPLETO — {destino_d.upper()}\\n\\n"
                            f"🌤️ CLIMA NO PERÍODO:\\n"
                            f"• Temperatura média (máxima e mínima)\\n"
                            f"• Chance de chuva e precipitação\\n"
                            f"• Roupas recomendadas — liste peças específicas\\n\\n"
                            f"🛡️ SEGURANÇA:\\n"
                            f"• Nível geral de segurança para turistas\\n"
                            f"• Regiões mais tranquilas (onde ficar)\\n"
                            f"• Áreas para evitar e por quê\\n"
                            f"• Cuidados comuns (golpes frequentes, cuidados com pertences)\\n\\n"
                            f"💰 CUSTO DE VIDA:\\n"
                            f"• Classificação: barato / médio / caro para brasileiros\\n"
                            f"• Comparação com São Paulo\\n"
                            f"• Onde economizar vs onde vale gastar mais\\n\\n"
                            f"🏛️ IDIOMA OFICIAL E FRASES ÚTEIS:\\n"
                            f"• Idioma(s) falado(s)\\n"
                            f"• 10 frases essenciais com pronúncia\\n"
                            f"• Nível de inglês da população local\\n\\n"
                            f"💱 MOEDA, CÂMBIO E PAGAMENTO:\\n"
                            f"• Moeda oficial e câmbio estimado em R$\\n"
                            f"• Formas de pagamento aceitas\\n"
                            f"• Dicas de câmbio (onde trocar, o que evitar)\\n"
                            f"• Taxas de cartão no exterior\\n\\n"
                            f"🚖 TRANSPORTE PÚBLICO:\\n"
                            f"• Meios disponíveis (metrô, ônibus, trem, ferry)\\n"
                            f"• Apps de transporte locais\\n"
                            f"• Custo médio por trajeto\\n"
                            f"• Dicas para não errar\\n\\n"
                            f"⚡ TOMADAS E VOLTAGEM:\\n"
                            f"• Tipo de tomada (A, B, C, F, G...)\\n"
                            f"• Voltagem (110V/220V)\\n"
                            f"• Precisa de adaptador? Qual modelo?\\n\\n"
                            f"📶 INTERNET, CHIP E ESIM:\\n"
                            f"• Operadoras locais recomendadas\\n"
                            f"• Preço médio de chip turista\\n"
                            f"• eSIM — vale a pena? Quais apps usar\\n"
                            f"• Qualidade da internet local\\n\\n"
                            f"🏥 SAÚDE:\\n"
                            f"• Vacinas exigidas ou recomendadas para brasileiros\\n"
                            f"• Seguro viagem — é obrigatório? Qual contratar?\\n"
                            f"• Hospitais de referência para turistas\\n"
                            f"• Farmácias e medicamentos básicos a levar\\n\\n"
                            f"📜 COSTUMES LOCAIS:\\n"
                            f"• Etiqueta e boas maneiras locais\\n"
                            f"• O que NUNCA fazer para não ofender\\n"
                            f"• Horários culturais (almoço, jantar, lojas)\\n"
                            f"• Gorjeta — como funciona\\n\\n"
                            f"🍽️ PRATOS TÍPICOS:\\n"
                            f"• 5 pratos que valem a pena experimentar\\n"
                            f"• Onde encontrá-los (tipo de restaurante)\\n"
                            f"• Preço médio de cada prato\\n\\n"
                            f"🎉 EVENTOS E FESTIVAIS NO PERÍODO:\\n"
                            f"• Festivais, feriados ou eventos durante {epoca_d or 'o ano'}\\n"
                            f"• Impacto nos preços e disponibilidade\\n\\n"
                            f"📱 APLICATIVOS INDISPENSÁVEIS:\\n"
                            f"• Apps de transporte, mapas, tradução, reservas e pagamento específicos para {destino_d}\\n"
                            f"• Quais baixar antes de embarcar"
                        )
                        res = viagem_ia(prompt)
                        salvar_roteiro("Guia do Destino", destino_d, res)
                        st.session_state['destino_temp'] = res

            if st.session_state.get('destino_temp'):
                st.markdown(f"<div class='card'>{st.session_state['destino_temp']}</div>", unsafe_allow_html=True)
                col_dl, col_sv = st.columns(2)
                with col_dl:
                    st.download_button("📋 Baixar (.txt)", data=st.session_state['destino_temp'],
                        file_name=f"guia_{destino_d.replace(' ','_') if 'destino_d' in dir() else 'destino'}.txt",
                        mime="text/plain", use_container_width=True, key="guiaviag16_d2")
                with col_sv:
                    if st.button("❤️ Salvar", key="sv_destino", use_container_width=True):
                        st.session_state.viagens_salvas.append({'tipo':'Guia do Destino',
                            'destino': destino_d if 'destino_d' in dir() else '',
                            'conteudo': st.session_state['destino_temp'],
                            'data': datetime.now().strftime('%d/%m %H:%M')})
                        st.success("❤️ Salvo!")

        # ========================
        # MAPA DOS PASSEIOS
        # ========================

    with _tab_Mapa:
            st.header("🗺 Mapa dos Passeios")
            st.markdown("Ordem inteligente dos pontos turísticos para reduzir deslocamentos.")

            destino_m = st.text_input("✈️ Destino:", placeholder="ex: Lisboa, Paris, Roma...", key="guiaviag38_d2")
            pontos_m = st.text_area("📍 Liste os passeios que quer fazer:", height=120,
                placeholder="ex: Torre Eiffel, Louvre, Notre Dame, Montmartre, Palais Royal, Sacré-Cœur...", key="guiaviag15_d2")
            dias_m = st.number_input("📅 Quantos dias:", min_value=1, max_value=21, value=5, key="guiaviag39_d2")

            if st.button("🗺 ORGANIZAR MAPA DE PASSEIOS", key="guiaviag40_d2"):
                if destino_m.strip():
                    with st.spinner("Organizando passeios por proximidade..."):
                        prompt = (
                            f"Organize estes passeios de {destino_m} na ordem mais eficiente para reduzir deslocamentos.\\n"
                            f"Passeios: {pontos_m or 'os principais pontos turísticos'}. Dias disponíveis: {dias_m}.\\n\\n"
                            f"FORMATO:\\n\\n"
                            f"🗺 MAPA DE PASSEIOS — {destino_m.upper()}\\n\\n"
                            f"📍 DISTRIBUIÇÃO POR BAIRRO/REGIÃO:\\n"
                            f"[Agrupe os pontos por proximidade geográfica]\\n\\n"
                            f"Para cada DIA, organize assim:\\n\\n"
                            f"📅 DIA [N] — BAIRRO/REGIÃO [NOME]\\n"
                            f"• [Ponto 1] — [bairro] — [horário sugerido]\\n"
                            f"  🚶 Até próximo: [X min a pé / Y min de metrô]\\n"
                            f"• [Ponto 2] — [bairro]\\n"
                            f"  🚶 Até próximo: [X min]\\n"
                            f"[continue...]\\n\\n"
                            f"🚇 DICAS DE TRANSPORTE ENTRE OS DIAS:\\n"
                            f"[Como ir de um bairro ao outro — metrô, ônibus, táxi]\\n\\n"
                            f"⏱️ TEMPO TOTAL DE DESLOCAMENTO ESTIMADO:\\n"
                            f"[Quanto tempo por dia será gasto em transporte]\\n\\n"
                            f"💡 POR QUE ESSA ORDEM FAZ SENTIDO:\\n"
                            f"[Explique a lógica geográfica]"
                        )
                        res = viagem_ia(prompt)
                        salvar_roteiro("Mapa de Passeios", destino_m, res)
                        st.session_state['mapa_temp'] = res

            if st.session_state.get('mapa_temp'):
                st.markdown(f"<div class='card-green'>{st.session_state['mapa_temp']}</div>", unsafe_allow_html=True)
                st.download_button("📋 Baixar (.txt)", data=st.session_state['mapa_temp'],
                    file_name="mapa_passeios.txt", mime="text/plain", key="guiaviag14_d2")

        # ========================
        # MOEDA E CÂMBIO
        # ========================

    with _tab_Moeda:
            st.header("💱 Moeda e Câmbio")

            destino_mo = st.text_input("✈️ Destino:", placeholder="ex: Lisboa, Nova York, Tóquio...", key="guiaviag41")
            orcamento_mo = st.number_input("💰 Orçamento em R$:", min_value=100, max_value=200000, value=5000, step=500, key="guiaviag42")

            if st.button("💱 ANALISAR CÂMBIO E ESTRATÉGIA", key="guiaviag43"):
                if destino_mo.strip():
                    with st.spinner("Analisando..."):
                        prompt = (
                            f"Crie um guia prático de câmbio para {destino_mo} com orçamento de R${orcamento_mo}.\\n\\n"
                            f"💱 GUIA DE CÂMBIO — {destino_mo.upper()}\\n\\n"
                            f"• Moeda oficial e símbolo\\n"
                            f"• Câmbio estimado atual (R$ para a moeda local)\\n"
                            f"• Quanto R${orcamento_mo} equivale na moeda local\\n\\n"
                            f"💳 MELHORES FORMAS DE LEVAR DINHEIRO:\\n"
                            f"• Cartão de crédito internacional (vantagens e taxas)\\n"
                            f"• Cartão débito/pré-pago (Wise, Nomad, C6 — comparativo)\\n"
                            f"• Dinheiro em espécie — quanto levar\\n"
                            f"• O que NUNCA fazer (casas de câmbio no aeroporto, etc)\\n\\n"
                            f"💡 ESTRATÉGIA PARA R${orcamento_mo}:\\n"
                            f"• Como dividir entre os meios de pagamento\\n"
                            f"• Onde sacar dinheiro local sem pagar abusivo\\n"
                            f"• Gorjeta — quanto e como"
                        )
                        res = viagem_ia(prompt)
                        salvar_roteiro("Moeda e Câmbio", destino_mo, res)
                        st.session_state['moeda_temp'] = res

            if st.session_state.get('moeda_temp'):
                st.markdown(f"<div class='card-yellow'>{st.session_state['moeda_temp']}</div>", unsafe_allow_html=True)

        # ========================
        # CLIMA
        # ========================

    with _tab_Clima:
            st.header("🌤️ Clima no Período da Viagem")

            col1, col2 = st.columns(2)
            with col1:
                destino_cl = st.text_input("✈️ Destino:", placeholder="ex: Lisboa, Amsterdã, Bangkok...", key="guiaviag44")
            with col2:
                mes_cl = st.selectbox("📅 Mês da viagem:", ["Janeiro","Fevereiro","Março","Abril","Maio","Junho",
                    "Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"], key="guiaviag13_d2")

            if st.button("🌤️ VER CLIMA E ROUPAS", key="guiaviag45"):
                if destino_cl.strip():
                    with st.spinner("Consultando clima..."):
                        prompt = (
                            f"Informe o clima de {destino_cl} em {mes_cl} para um turista brasileiro.\\n\\n"
                            f"🌤️ CLIMA EM {destino_cl.upper()} — {mes_cl.upper()}\\n\\n"
                            f"🌡️ TEMPERATURA:\\n"
                            f"• Média mínima e máxima\\n"
                            f"• Temperatura da água (se litoral)\\n"
                            f"• Sensação térmica (umidade)\\n\\n"
                            f"🌧️ CHUVA:\\n"
                            f"• Chance de chuva (%)\\n"
                            f"• Tipo de chuva (pancadas rápidas, chuva contínua, neve)\\n"
                            f"• Impacto nos passeios\\n\\n"
                            f"👗 ROUPAS RECOMENDADAS — lista específica:\\n"
                            f"[Liste peças de roupa concretas: ex: calça jeans, 2 camisetas, casaco impermeável...]\\n\\n"
                            f"👟 CALÇADOS:\\n[Tipo ideal para o clima e terreno]\\n\\n"
                            f"🧴 ACESSÓRIOS ESSENCIAIS:\\n[protetor solar, guarda-chuva, óculos, etc]\\n\\n"
                            f"⚠️ CUIDADOS ESPECIAIS:\\n[o que o clima de {mes_cl} exige de atenção em {destino_cl}]"
                        )
                        res = viagem_ia(prompt)
                        salvar_roteiro("Clima", destino_cl, res)
                        st.session_state['clima_temp'] = res

            if st.session_state.get('clima_temp'):
                st.markdown(f"<div class='card-purple'>{st.session_state['clima_temp']}</div>", unsafe_allow_html=True)
                st.download_button("📋 Baixar (.txt)", data=st.session_state['clima_temp'],
                    file_name="clima_viagem.txt", mime="text/plain", key="guiaviag12_d2")

        # ========================
        # SEGURANÇA E SAÚDE
        # ========================

    with _tab_Seguranca:
            st.header("🛡️ Segurança e Saúde")

            destino_sg = st.text_input("✈️ Destino:", placeholder="ex: Lisboa, Cairo, Medellín...", key="guiaviag46")

            if st.button("🛡️ GERAR GUIA DE SEGURANÇA E SAÚDE", key="guiaviag47"):
                if destino_sg.strip():
                    with st.spinner("Analisando..."):
                        prompt = (
                            f"Crie um guia completo de segurança e saúde para turistas brasileiros em {destino_sg}.\\n\\n"
                            f"🛡️ SEGURANÇA — {destino_sg.upper()}\\n\\n"
                            f"📊 NÍVEL GERAL DE SEGURANÇA:\\n[Classificação: seguro / atenção moderada / cuidado redobrado]\\n\\n"
                            f"✅ REGIÕES MAIS TRANQUILAS:\\n[Bairros e áreas recomendadas para ficar e passear]\\n\\n"
                            f"⚠️ ÁREAS PARA EVITAR:\\n[Bairros ou regiões com mais ocorrências — sem alarmismo]\\n\\n"
                            f"🔒 CUIDADOS COMUNS:\\n"
                            f"• Golpes frequentes aplicados em turistas\\n"
                            f"• Como proteger documentos e pertences\\n"
                            f"• O que fazer em caso de roubo\\n"
                            f"• Número de emergência local\\n\\n"
                            f"🏥 SAÚDE — {destino_sg.upper()}\\n\\n"
                            f"💉 VACINAS:\\n[Exigidas, recomendadas e dispensáveis para brasileiros]\\n\\n"
                            f"🏥 HOSPITAIS DE REFERÊNCIA:\\n[Nome e localização dos melhores para turistas]\\n\\n"
                            f"📋 SEGURO VIAGEM:\\n[Obrigatório? Qual cobrir? Preço médio? Melhores empresas?]\\n\\n"
                            f"💊 MEDICAMENTOS BÁSICOS A LEVAR:\\n[Lista de itens para farmácia de viagem]"
                        )
                        res = viagem_ia(prompt)
                        salvar_roteiro("Segurança e Saúde", destino_sg, res)
                        st.session_state['seg_temp'] = res

            if st.session_state.get('seg_temp'):
                st.markdown(f"<div class='card-orange'>{st.session_state['seg_temp']}</div>", unsafe_allow_html=True)
                col_dl, col_sv = st.columns(2)
                with col_dl:
                    st.download_button("📋 Baixar (.txt)", data=st.session_state['seg_temp'],
                        file_name="seguranca_saude.txt", mime="text/plain", use_container_width=True, key="guiaviag11_d2")
                with col_sv:
                    if st.button("❤️ Salvar", key="sv_seg", use_container_width=True):
                        st.session_state.viagens_salvas.append({'tipo':'Segurança e Saúde',
                            'destino': destino_sg if 'destino_sg' in dir() else '',
                            'conteudo': st.session_state['seg_temp'],
                            'data': datetime.now().strftime('%d/%m %H:%M')})
                        st.success("❤️ Salvo!")

        # ========================
        # HISTÓRIA DO DESTINO
        # ========================

    with _tab_Historia:
            st.header("🏛️ Conheça o Destino")
            st.markdown("Descubra a história, cultura e curiosidades antes de visitar.")

            destino_h = st.text_input("✈️ Destino:", placeholder="ex: Lisboa, Roma, Machu Picchu, Kyoto...", key="guiaviag48")

            tema_h = st.multiselect("📚 O que você quer saber:", [
                "📜 Como a cidade surgiu",
                "👑 Personagens históricos importantes",
                "⚔️ Principais acontecimentos históricos",
                "🏰 Monumentos que marcaram essa história",
                "🎬 Filmes famosos gravados no local",
                "📚 Livros famosos ambientados na cidade",
                "🌟 Curiosidades que quase ninguém conhece",
                "🏆 Recordes ou títulos (Patrimônio Mundial, etc)",
                "💬 Uma lenda ou história curiosa da região",
                "📱 Aplicativos indispensáveis para esse destino",
            ], default=["📜 Como a cidade surgiu","🌟 Curiosidades que quase ninguém conhece","🏰 Monumentos que marcaram essa história"], key="guiaviag10_d2")

            if st.button("🏛️ CONHECER ESTE DESTINO", key="guiaviag49"):
                if destino_h.strip():
                    with st.spinner(f"Mergulhando na história de {destino_h}..."):
                        temas_txt = "\\n".join(f"• {t}" for t in tema_h) if tema_h else "• História geral e curiosidades"
                        prompt = (
                            f"Crie um guia histórico e cultural envolvente sobre {destino_h}.\\n"
                            f"Cubra os seguintes temas:\\n{temas_txt}\\n\\n"
                            f"FORMATO:\\n\\n"
                            f"🏛️ CONHEÇA {destino_h.upper()}\\n\\n"
                            f"[Parágrafo de introdução vibrante — 3-4 linhas que faça a pessoa querer visitar]\\n\\n"
                            f"[Para cada tema selecionado, use o emoji e o título como cabeçalho, depois o conteúdo detalhado]\\n\\n"
                            f"💡 ANTES DE VISITAR, SAIBA:\\n"
                            f"[3 fatos que vão transformar a experiência de visitar {destino_h}]"
                        )
                        res = viagem_ia(prompt)
                        salvar_roteiro("História do Destino", destino_h, res)
                        st.session_state['historia_temp'] = res

            if st.session_state.get('historia_temp'):
                st.markdown(f"<div class='card-purple'>{st.session_state['historia_temp']}</div>", unsafe_allow_html=True)
                col_dl, col_sv = st.columns(2)
                with col_dl:
                    st.download_button("📋 Baixar (.txt)", data=st.session_state['historia_temp'],
                        file_name=f"historia_{destino_h.replace(' ','_') if 'destino_h' in dir() else 'destino'}.txt",
                        mime="text/plain", use_container_width=True, key="guiaviag9_d2")
                with col_sv:
                    if st.button("❤️ Salvar", key="sv_historia", use_container_width=True):
                        st.session_state.viagens_salvas.append({'tipo':'História do Destino',
                            'destino': destino_h if 'destino_h' in dir() else '',
                            'conteudo': st.session_state['historia_temp'],
                            'data': datetime.now().strftime('%d/%m %H:%M')})
                        st.success("❤️ Salvo!")

        # ========================
        # GERAR PDF DA VIAGEM
        # ========================

    with _tab_PDF:
            st.header("📄 Gerar Resumo da Viagem para Levar")
            st.markdown("Gere um resumo compacto e organizado do seu roteiro — para imprimir ou salvar no celular.")

            if not st.session_state.historico_roteiros:
                st.info("Gere pelo menos um roteiro primeiro, depois volte aqui para criar o resumo.")
            else:
                roteiros_disponiveis = [f"{r['tipo']} — {r['destino']} ({r['data']})" for r in st.session_state.historico_roteiros[-10:]]
                roteiro_sel = st.selectbox("Escolha o roteiro:", roteiros_disponiveis, key="guiaviag50")
                idx_sel = roteiros_disponiveis.index(roteiro_sel)
                roteiro_escolhido = st.session_state.historico_roteiros[-(len(roteiros_disponiveis) - idx_sel)]

                formato_pdf = st.radio("Formato:", ["Resumo compacto (1 página)","Versão completa para imprimir","Versão para celular (compacta e visual)"], key="guiaviag51")

                if st.button("📄 GERAR RESUMO", key="guiaviag52"):
                    with st.spinner("Gerando versão para levar..."):
                        prompt = (
                            f"Reformate este roteiro de viagem no formato: {formato_pdf}.\\n"
                            f"Destino: {roteiro_escolhido['destino']}.\\n"
                            f"Roteiro original:\\n{roteiro_escolhido['conteudo'][:3000]}\\n\\n"
                            f"INSTRUÇÕES:\\n"
                            f"- Formato compacto: destaque APENAS o essencial (endereços, horários, preços, telefones)\\n"
                            f"- Use emojis como marcadores visuais para facilitar a leitura rápida\\n"
                            f"- Inclua uma seção 'EMERGÊNCIA' com números úteis e endereço do hotel\\n"
                            f"- Organize por dia de forma clara\\n"
                            f"- Adicione uma checklist rápida de itens para não esquecer no dia"
                        )
                        res = viagem_ia(prompt)
                        salvar_roteiro("Resumo PDF", roteiro_escolhido['destino'], res)
                        st.session_state['pdf_temp'] = res

            if st.session_state.get('pdf_temp'):
                st.markdown(f"<div class='card'>{st.session_state['pdf_temp']}</div>", unsafe_allow_html=True)
                col_dl, col_sv = st.columns(2)
                with col_dl:
                    st.download_button("📄 Baixar resumo (.txt)", data=st.session_state['pdf_temp'],
                        file_name="resumo_viagem.txt", mime="text/plain", use_container_width=True, key="guiaviag8_d2")
                with col_sv:
                    if st.button("❤️ Salvar", key="sv_pdf", use_container_width=True):
                        st.session_state.viagens_salvas.append({'tipo':'Resumo para Viagem',
                            'destino': roteiro_escolhido['destino'] if 'roteiro_escolhido' in dir() else '',
                            'conteudo': st.session_state['pdf_temp'],
                            'data': datetime.now().strftime('%d/%m %H:%M')})
                        st.success("❤️ Salvo!")

        # ========================
        # ECONOMIZAR MAIS
        # ========================

    with _tab_Economizar:
            st.header("💸 Economizar Mais")
            st.markdown("Refaz o roteiro reduzindo custos sem abrir mão da experiência.")

            col1, col2 = st.columns(2)
            with col1:
                destino_ec = st.text_input("✈️ Destino:", value=st.session_state.get('roteiro_destino',''), placeholder="ex: Lisboa, Paris...", key="guiaviag53")
                dias_ec = st.number_input("📅 Dias:", min_value=2, max_value=21, value=st.session_state.get('roteiro_dias', 7), key="guiaviag54")
                orcamento_ec = st.number_input("💰 Orçamento disponível (R$):", min_value=500, max_value=100000, value=st.session_state.get('roteiro_orcamento', 3000), step=500, key="guiaviag55")
            with col2:
                pessoas_ec = st.selectbox("👥 Pessoas:", ["1 pessoa","2 pessoas","3-4 pessoas","5+ pessoas"],
                    index=["1 pessoa","2 pessoas","3-4 pessoas","5+ pessoas"].index(st.session_state.get('roteiro_pessoas','1 pessoa')) if st.session_state.get('roteiro_pessoas') in ["1 pessoa","2 pessoas","3-4 pessoas","5+ pessoas"] else 0, key="guiaviag7_d2")
                epoca_ec = st.text_input("📅 Período:", value=st.session_state.get('roteiro_epoca',''), placeholder="ex: julho...", key="guiaviag56")
                prioridade_ec = st.multiselect("🎯 O que NÃO abrir mão:", ["Hospedagem boa","Restaurantes","Passeios pagos","Transporte confortável"],
                    default=["Passeios pagos"], key="guiaviag6_d2")

            if st.button("💸 GERAR ROTEIRO ECONÔMICO", key="guiaviag57"):
                if destino_ec.strip():
                    with st.spinner(f"Otimizando custos para {destino_ec}..."):
                        prompt = (
                            f"Crie um roteiro ECONÔMICO e otimizado para {destino_ec}.\\n"
                            f"Dias: {dias_ec}. Orçamento: R${orcamento_ec}. Pessoas: {pessoas_ec}. Época: {epoca_ec or 'qualquer'}.\\n"
                            f"O que não pode faltar: {', '.join(prioridade_ec) if prioridade_ec else 'flexível'}.\\n\\n"
                            f"FOCO: reduzir custos ao máximo sem perder qualidade de experiência.\\n\\n"
                            f"FORMATO:\\n\\n"
                            f"💸 ROTEIRO ECONÔMICO — {destino_ec.upper()}\\n\\n"
                            f"💡 ESTRATÉGIA DE ECONOMIA:\\n"
                            f"[As 5 principais decisões que vão economizar mais dinheiro nessa viagem]\\n\\n"
                            f"🆓 ATRAÇÕES GRATUITAS OU QUASE:\\n"
                            f"[Lista de museus gratuitos, parques, mirantes, eventos sem custo]\\n\\n"
                            f"Para cada dia:\\n\\n"
                            f"📅 DIA [N]\\n"
                            f"• Manhã: [atividade gratuita ou barata] — R$[X]\\n"
                            f"• Almoço: [opção econômica com nome real] — R$[X]/pessoa\\n"
                            f"• Tarde: [atividade] — R$[X]\\n"
                            f"• Jantar: [opção econômica] — R$[X]/pessoa\\n"
                            f"💰 Total do dia: R$[X]/pessoa\\n\\n"
                            f"🏨 HOSPEDAGEM ECONÔMICA:\\n"
                            f"[Melhores opções custo-benefício: hostels bons, apartamentos Airbnb por localização]\\n\\n"
                            f"🚇 TRANSPORTE ECONÔMICO:\\n"
                            f"[Passes de transporte, quando vale a pena, como evitar táxi]\\n\\n"
                            f"📊 ORÇAMENTO FINAL ECONOMIZADO:\\n"
                            f"Total estimado: R$[X] p/pessoa\\n"
                            f"Economia vs roteiro padrão: aprox. R$[X]\\n"
                            f"[Compare com o orçamento de R${orcamento_ec} e diga se é suficiente]\\n\\n"
                            f"⚠️ ONDE NÃO ECONOMIZAR:\\n"
                            f"[Itens que vale gastar um pouco mais — seguro, transporte no aeroporto, etc]"
                        )
                        res = viagem_ia(prompt)
                        salvar_roteiro("Roteiro Econômico", destino_ec, res)
                        st.session_state['econom_temp'] = res

            if st.session_state.get('econom_temp'):
                st.markdown(f"<div class='card-green'>{st.session_state['econom_temp']}</div>", unsafe_allow_html=True)
                col_dl, col_sv = st.columns(2)
                with col_dl:
                    st.download_button("📋 Baixar (.txt)", data=st.session_state['econom_temp'],
                        file_name="roteiro_economico.txt", mime="text/plain", use_container_width=True, key="guiaviag5_d2")
                with col_sv:
                    if st.button("❤️ Salvar", key="sv_econom", use_container_width=True):
                        st.session_state.viagens_salvas.append({'tipo':'Roteiro Econômico',
                            'destino': destino_ec if 'destino_ec' in dir() else '',
                            'conteudo': st.session_state['econom_temp'],
                            'data': datetime.now().strftime('%d/%m %H:%M')})
                        st.success("❤️ Salvo!")

        # ========================
        # PALAVRAS ARMADILHA
        # ========================

    with _tab_Armadilha:
            st.header("🚫 Palavras Armadilha")
            st.markdown("Palavras ou expressões completamente normais em português — mas ofensivas, obscenas ou constrangedoras no país de destino. Saiba antes de viajar.")

            col1, col2 = st.columns(2)
            with col1:
                pais_arm = st.text_input("🌍 País de destino:", placeholder="ex: Portugal, Espanha, EUA, Japão, Argentina...", key="guiaviag58")
            with col2:
                incluir_gestos = st.checkbox("Incluir gestos e linguagem corporal", value=True, key="guiaviag59")
                incluir_nomes = st.checkbox("Incluir nomes próprios e marcas que soam mal", value=True, key="guiaviag60")

            if st.button("🚫 DESCOBRIR AS ARMADILHAS", key="guiaviag61"):
                if pais_arm.strip():
                    with st.spinner(f"Pesquisando micos em {pais_arm}..."):
                        prompt = (
                            f"Crie um guia de ARMADILHAS LINGUÍSTICAS entre o português brasileiro e {pais_arm}.\\n\\n"
                            f"REGRA ABSOLUTA: APENAS inclua palavras que você tem CERTEZA que existem e funcionam assim no destino. "
                            f"NÃO invente, NÃO suponha, NÃO extrapole. Se não souber 7 exemplos verificáveis reais para {pais_arm}, diga quantos encontrou e explique.\\n\\n"
                            f"OBJETIVO: Mostrar palavras que causam CHOQUE ou CONFUSÃO porque têm significados OPOSTOS ou MUITO DIFERENTES nos dois lugares.\\n\\n"
                            f"DOIS TIPOS DE ARMADILHA:\\n"
                            f"1. Palavra normal no Brasil que é ofensiva/estranha em {pais_arm}\\n"
                            f"2. Palavra normal em {pais_arm} que choca ou confunde o brasileiro\\n\\n"
                            f"EXEMPLOS DO TIPO CERTO (para Portugal):\\n"
                            f"- BICHA: no Brasil = gíria pejorativa para gay | em Portugal = fila de espera (normal). Armadilha: brasileiro se choca quando português diz 'entre na bicha'\\n"
                            f"- RAPARIGA: no Brasil = prostituta | em Portugal = moça/garota (normal). Armadilha: brasileira se ofende quando chamada de rapariga\\n"
                            f"- FIXE: no Brasil = não usado | em Portugal = legal/ótimo. Armadilha: brasileiro não entende\\n\\n"
                            f"EXEMPLOS DO TIPO ERRADO (não faça isso para {pais_arm}):\\n"
                            f"- Inventar que uma palavra comum em português tem significado ofensivo numa língua que você não domina\\n"
                            f"- Usar coincidências fonéticas fracas sem contexto real de uso (ex: dizer que 'casa' soa como algo ruim em algum lugar sem prova)\\n\\n"
                            f"FORMATO para cada palavra:\\n"
                            f"🔴 **[PALAVRA]**\\n"
                            f"• No Brasil significa: [significado real atual no pt-BR]\\n"
                            f"• Em {pais_arm} significa: [significado real lá]\\n"
                            f"• A armadilha: [situação concreta onde o choque acontece]\\n"
                            f"• Nível: [leve 😅 / moderado 😬 / grave 😱]\\n"
                            f"• Como evitar: [solução prática]\\n\\n"
                            f"Inclua pelo menos 7 exemplos REAIS e VERIFICÁVEIS. Quantidade com qualidade vale mais que 15 inventados.\\n"
                            f"Destino: {pais_arm}\\n\\n"
                        )
                        if incluir_gestos:
                            prompt += (
                                f"👋 GESTOS E LINGUAGEM CORPORAL QUE ENGANAM:\\n\\n"
                                f"[Gestos comuns no Brasil que têm significado diferente ou ofensivo em {pais_arm}. "
                                f"Ex: jinha de ok, polegar, acenar, etc. Mesmo formato: gesto, o que significa aqui, o que significa lá, nível de problema.]\\n\\n"
                            )
                        if incluir_nomes:
                            prompt += (
                                f"😬 NOMES PRÓPRIOS E MARCAS QUE SOAM MAL:\\n\\n"
                                f"[Nomes comuns no Brasil — de pessoas, produtos ou lugares — que soam como algo ofensivo "
                                f"ou engraçado em {pais_arm}. Explique o porquê.]\\n\\n"
                            )
                        prompt += (
                            f"🔁 O INVERSO TAMBÉM VALE — PALAVRAS DELES QUE NOS SURPREENDEM:\\n\\n"
                            f"[Palavras comuns em {pais_arm} que soam ofensivas, engraçadas ou inadequadas para brasileiros. "
                            f"Para não se ofender à toa quando ouvir.]\\n\\n"
                            f"💡 DICA FINAL:\\n"
                            f"[Conselho prático sobre como lidar quando escapar uma palavra errada — "
                            f"como se desculpar de forma adequada na cultura de {pais_arm}]"
                        )
                        res = viagem_ia(prompt,
                            "Seja RIGOROSAMENTE preciso e honesto. Este guia existe para ajudar brasileiros a evitar situações "
                            "constrangedoras reais. Inclua APENAS exemplos verídicos, conhecidos e verificáveis. "
                            "NUNCA invente armadilhas linguísticas — se não existirem exemplos reais suficientes para o destino, "
                            "diga isso claramente em vez de fabricar coincidências fonéticas sem base real. "
                            "Qualidade e veracidade valem mais que quantidade. Não omita por pudor — "
                            "o objetivo é exatamente informar sobre o que é delicado e comprovado.")
                        salvar_roteiro("Palavras Armadilha", pais_arm, res)
                        st.session_state['armadilha_temp'] = res
                else:
                    st.warning("Informe o país de destino.")

            if st.session_state.get('armadilha_temp'):
                st.markdown(\"\"\"
                <div style='background:linear-gradient(135deg,#FFF5F5,#FFE4E4);
                border:2px solid #FC8181;border-radius:16px;padding:6px 20px;margin:12px 0;'>
                <div style='font-size:0.8em;font-weight:700;color:#C53030;margin-bottom:4px;'>
                🚫 GUIA DE ARMADILHAS LINGUÍSTICAS</div>
                </div>\"\"\", unsafe_allow_html=True)
                st.markdown(st.session_state['armadilha_temp'])
                col_dl, col_sv = st.columns(2)
                with col_dl:
                    st.download_button("📋 Baixar (.txt)",
                        data=st.session_state['armadilha_temp'],
                        file_name=f"armadilhas_{pais_arm.replace(' ','_') if 'pais_arm' in dir() else 'destino'}.txt",
                        mime="text/plain", use_container_width=True, key="guiaviag4_d2")
                with col_sv:
                    if st.button("❤️ Salvar", key="sv_armadilha", use_container_width=True):
                        st.session_state.viagens_salvas.append({
                            'tipo': 'Palavras Armadilha',
                            'destino': pais_arm if 'pais_arm' in dir() else '',
                            'conteudo': st.session_state['armadilha_temp'],
                            'data': datetime.now().strftime('%d/%m %H:%M'),
                        })
                        st.success("❤️ Salvo!")

                st.markdown(\"\"\"
                <div style='background:#FFF7ED;border:1px solid #FDBA74;border-radius:10px;
                padding:12px 16px;font-size:0.82em;color:#92400E;margin-top:8px;'>
                💡 <strong>Dica:</strong> compartilhe esse guia com todo o grupo antes de viajar.
                Um mico evitado vale mais que qualquer roteiro.
                </div>
                \"\"\", unsafe_allow_html=True)

        # ========================
        # COMO SÃO AS PESSOAS
        # ========================

    with _tab_Pessoas:
            st.header("🤝 Como São as Pessoas")
            st.markdown("Guia de relacionamento social — como cumprimentar, o que ofende, o que agrada, como funciona a dinâmica com estrangeiros.")

            col1, col2 = st.columns(2)
            with col1:
                pais_pe = st.text_input("🌍 País de destino:", placeholder="ex: Japão, Portugal, Alemanha, Marrocos...", key="guiaviag62")
                contexto_pe = st.multiselect("Situações que você vai viver:", [
                    "Ir à casa de alguém","Jantar com locais","Ambiente de trabalho/negócios",
                    "Bares e baladas","Fazer amizades na rua","Compras e mercado",
                    "Transporte público","Visitar família local","Encontros românticos",
                ], default=["Ir à casa de alguém","Jantar com locais","Fazer amizades na rua"], key="guiaviag3_d2")
            with col2:
                perfil_pe = st.selectbox("Seu perfil de viajante:", [
                    "Turista passando alguns dias","Vai visitar amigos ou conhecidos",
                    "Viagem de negócios","Vai morar ou ficar por meses",
                    "Intercâmbio ou estudo","Encontro romântico / namoro à distância",
                ], key="guiaviag2")

            if st.button("🤝 GERAR GUIA DE RELACIONAMENTO", key="guiaviag63"):
                if pais_pe.strip():
                    with st.spinner(f"Preparando guia de relacionamento para {pais_pe}..."):
                        contextos_txt = ", ".join(contexto_pe) if contexto_pe else "situações gerais"
                        prompt = (
                            f"Crie um guia completo e honesto sobre como são as pessoas de {pais_pe} "
                            f"e como um brasileiro deve se relacionar com elas.\\n"
                            f"Perfil do viajante: {perfil_pe}. Situações: {contextos_txt}.\\n\\n"
                            f"FORMATO:\\n\\n"
                            f"🤝 COMO SÃO AS PESSOAS DE {pais_pe.upper()}\\n\\n"
                            f"🧠 PERSONALIDADE GERAL:\\n"
                            f"[Como as pessoas desse país são em geral — reservadas ou abertas, formais ou informais, "
                            f"desconfiadas ou receptivas com estrangeiros, diretas ou indiretas. "
                            f"Compare com o jeito brasileiro para facilitar o entendimento.]\\n\\n"
                            f"👋 CUMPRIMENTOS — COMO SE FAZ:\\n"
                            f"• Entre homens: [aperto de mão, abraço, beijo, reverência, etc — e quando cada um é adequado]\\n"
                            f"• Entre mulheres: [idem]\\n"
                            f"• Homem cumprimentando mulher: [o que fazer e o que NUNCA fazer]\\n"
                            f"• Em ambiente formal vs informal: [diferença]\\n"
                            f"• Com idosos: [como tratar com respeito]\\n"
                            f"• Com crianças: [pode tocar, fazer carinha, etc?]\\n\\n"
                            f"🏠 IR À CASA DE ALGUÉM — REGRAS DE OURO:\\n"
                            f"• Deve-se levar algo? O quê? [seja específico — vinho, doce, o quê exatamente]\\n"
                            f"• Flores: pode? Qual tipo? Qual cor? [algumas cores são luto em certos países]\\n"
                            f"• Pontualidade: chegar no horário exato, adiantado ou atrasado?\\n"
                            f"• Ao entrar: tira o sapato? Espera ser convidado a sentar?\\n"
                            f"• À mesa: espera todos servirem? Elogia a comida? Recusa algo se não gostar?\\n"
                            f"• Quanto tempo ficar após o jantar? Quando é hora de ir embora?\\n"
                            f"• O que mandar depois: mensagem de agradecimento? É esperado?\\n\\n"
                            f"🎁 PRESENTES — O QUE OFENDE SEM QUERER:\\n"
                            f"[Lista do que NUNCA dar de presente e por quê — flores de determinada cor, faca, relógio, "
                            f"número de itens, etc. Seja específico para {pais_pe}.]\\n\\n"
                            f"💬 CONVERSAS — O QUE FALAR E O QUE EVITAR:\\n"
                            f"• Assuntos que quebram o gelo facilmente com locais de {pais_pe}\\n"
                            f"• Assuntos TABU que devem ser evitados completamente\\n"
                            f"• Perguntas que parecem inocentes mas ofendem\\n"
                            f"• Como os locais reagem quando um brasileiro fala muito ou faz muitas perguntas pessoais\\n\\n"
                            f"😊 O QUE OS LOCAIS DE {pais_pe.upper()} ADORAM NOS BRASILEIROS:\\n"
                            f"[Características do jeito brasileiro que são bem recebidas — use isso a seu favor]\\n\\n"
                            f"😬 O QUE OS LOCAIS NÃO GOSTAM NO JEITO BRASILEIRO:\\n"
                            f"[Comportamentos comuns para nós que incomodam ou causam estranheza lá — sem julgamento, só informação]\\n\\n"
                            f"🍽️ À MESA — ETIQUETA LOCAL:\\n"
                            f"• Quem paga quando saem juntos?\\n"
                            f"• Gorjeta: obrigatória, opcional ou ofensiva?\\n"
                            f"• Falar com a boca cheia, cotovelo na mesa — o que é tolerado?\\n"
                            f"• Tirar foto da comida: aceitável ou estranho?\\n\\n"
                            f"💑 RELACIONAMENTO ENTRE HOMENS E MULHERES:\\n"
                            f"[Como é a dinâmica social — olhar nos olhos, tocar no braço, piropear, "
                            f"o que é flerte e o que é assédio na cultura local]\\n\\n"
                            f"🕐 PONTUALIDADE E TEMPO:\\n"
                            f"[A cultura é pontual ou relaxada com horários? O que é insulto e o que é normal em questão de tempo?]\\n\\n"
                            f"📱 COMUNICAÇÃO DIGITAL:\\n"
                            f"[WhatsApp é usado? Como respondem mensagens — rápido, devagar? "
                            f"Ligar sem avisar é ok? Rede social favorita para se conectar com locais?]\\n\\n"
                            f"🌟 DICA FINAL DO VIAJANTE EXPERIENTE:\\n"
                            f"[1 comportamento que, se o brasileiro adotar, vai criar uma impressão muito positiva "
                            f"nos locais de {pais_pe} — algo específico e prático]"
                        )
                        res = viagem_ia(prompt,
                            "Seja honesto, específico e culturalmente preciso. Evite generalizações vagas. "
                            "O objetivo é preparar um brasileiro para interações sociais reais — não um guia turístico genérico.")
                        salvar_roteiro("Como São as Pessoas", pais_pe, res)
                        st.session_state['pessoas_temp'] = res
                else:
                    st.warning("Informe o país de destino.")

            if st.session_state.get('pessoas_temp'):
                st.markdown(\"\"\"
                <div style='background:linear-gradient(135deg,#F0FDF4,#DCFCE7);
                border:2px solid #86EFAC;border-radius:16px;padding:6px 20px;margin:12px 0;'>
                <div style='font-size:0.8em;font-weight:700;color:#166534;margin-bottom:4px;'>
                🤝 GUIA DE RELACIONAMENTO SOCIAL</div>
                </div>\"\"\", unsafe_allow_html=True)
                st.markdown(st.session_state['pessoas_temp'])
                col_dl, col_sv = st.columns(2)
                with col_dl:
                    st.download_button("📋 Baixar (.txt)",
                        data=st.session_state['pessoas_temp'],
                        file_name=f"pessoas_{pais_pe.replace(' ','_') if 'pais_pe' in dir() else 'destino'}.txt",
                        mime="text/plain", use_container_width=True, key="guiaviag1_d2")
                with col_sv:
                    if st.button("❤️ Salvar", key="sv_pessoas", use_container_width=True):
                        st.session_state.viagens_salvas.append({
                            'tipo': 'Como São as Pessoas',
                            'destino': pais_pe if 'pais_pe' in dir() else '',
                            'conteudo': st.session_state['pessoas_temp'],
                            'data': datetime.now().strftime('%d/%m %H:%M'),
                        })
                        st.success("❤️ Salvo!")

    # --- RODAPÉ ---
    st.markdown(
        "<div style='text-align:center;color:#999;font-size:0.8em;margin-top:60px;'>"
        "© 2026 Guia de Viagens IA — Roteiros Personalizados com IA · MeusAgentesIA.com.br"
        "</div>", unsafe_allow_html=True
    )

# --- RODAPÉ ---
st.markdown(
    "<div style='text-align:center;color:#999;font-size:0.8em;margin-top:60px;'>"
    "</div>", unsafe_allow_html=True
)
""",
    "chef_calorico": """# [hub] import streamlit as st
# [hub] from groq import Groq
# [hub] from datetime import datetime, date, timedelta
# [hub] import json
import random

# set_page_config removido pelo super_agente

st.markdown(\"\"\"
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
[data-testid="stToolbar"] {visibility: hidden;}
[data-testid="stDecoration"] {visibility: hidden;}
[data-testid="stStatusWidget"] {visibility: hidden;}
</style>
\"\"\", unsafe_allow_html=True)


st.markdown(\"\"\"
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    .stApp { background-color:#FDFAF6; font-family:'Inter',sans-serif; }
    [data-testid="stSidebar"] { display:none; }

    .stTextInput>div>div>input, .stTextArea>div>textarea,
    .stSelectbox>div>div>div, .stNumberInput>div>div>input {
        background-color:#FFFFFF !important; color:#1A1A2E !important;
        border:1px solid #CED4DA !important; font-family:'Inter',sans-serif !important;
    }

    .stButton>button {
        width:100%; border-radius:10px; height:3.2em;
        background:linear-gradient(135deg,#92400E,#78350F) !important; color:white !important;
        font-weight:600; border:none; box-shadow:2px 2px 8px rgba(0,0,0,0.1);
        font-family:'Inter',sans-serif !important; transition:all 0.2s ease;
    }
    .stButton>button:hover { background:linear-gradient(135deg,#78350F,#5C2D0A) !important; transform:translateY(-1px); }
    .stApp .stButton>button, .stApp .stButton>button p,
    .stApp .stButton>button span, .stApp .stButton>button div { color:white !important; }

    .stApp h1, .stApp h2, .stApp h3 { color:#3D2B1F !important; font-family:'Inter',sans-serif !important; font-weight:700 !important; }

    .card { background:linear-gradient(135deg,#FDF8F0,#FAF0E6); padding:20px; border-radius:14px; border:1px solid #D4B896; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card, .stApp .card p, .stApp .card span, .stApp .card div, .stApp .card strong, .stApp .card em { color:#3D2B1F !important; }

    .card-dark { background:linear-gradient(135deg,#FAF0E6,#F5E6D3); padding:20px; border-radius:14px; border:1px solid #C4956A; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-dark, .stApp .card-dark p, .stApp .card-dark span, .stApp .card-dark div, .stApp .card-dark strong { color:#3D2B1F !important; }

    .card-green { background:linear-gradient(135deg,#F0FDF4,#DCFCE7); padding:20px; border-radius:14px; border:1px solid #86EFAC; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-green, .stApp .card-green p, .stApp .card-green span, .stApp .card-green div { color:#14532D !important; }

    .card-blue { background:linear-gradient(135deg,#EFF6FF,#DBEAFE); padding:20px; border-radius:14px; border:1px solid #93C5FD; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-blue, .stApp .card-blue p, .stApp .card-blue span, .stApp .card-blue div { color:#1E3A8A !important; }

    .card-red { background:linear-gradient(135deg,#FFF5F5,#FEE2E2); padding:20px; border-radius:14px; border:1px solid #FECACA; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-red, .stApp .card-red p, .stApp .card-red span, .stApp .card-red div { color:#7F1D1D !important; }

    .card-yellow { background:linear-gradient(135deg,#FFFBEB,#FEF3C7); padding:18px; border-radius:12px; border:1px solid #FCD34D; margin-bottom:12px; white-space:normal; word-wrap:break-word; }
    .stApp .card-yellow, .stApp .card-yellow p, .stApp .card-yellow span, .stApp .card-yellow div { color:#78350F !important; }

    .stat-box { background:#FFFFFF; border-radius:12px; padding:16px; text-align:center; border:1px solid #D4B896; }
    .stApp .stat-box div, .stApp .stat-box span, .stApp .stat-box p { color:#3D2B1F !important; }
    .stApp .stat-numero, .stat-numero { font-size:2em; font-weight:700; color:#7C5C3E !important; }

    .hist-item { background:#FFFFFF; border-radius:10px; padding:12px 16px; margin-bottom:8px; border-left:4px solid #D4B896; }
    .stApp .hist-item, .stApp .hist-item p, .stApp .hist-item span, .stApp .hist-item div, .stApp .hist-item small { color:#3D2B1F !important; }

    .badge { background:#92400E; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-verde { background:#059669; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-amarelo { background:#B45309; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-azul { background:#1D4ED8; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-roxo { background:#6D28D9; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }

    .divider { border:none; height:1px; background:linear-gradient(to right,transparent,#D4B896,transparent); margin:18px 0; }

    .chat-user { background:#FFFFFF; border:1px solid #D4B896; border-radius:12px 12px 4px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-user, .stApp .chat-user p, .stApp .chat-user span, .stApp .chat-user div { color:#3D2B1F !important; }

    .chat-persona { background:#FDFAF6; border:1px solid #D4B896; border-radius:4px 12px 12px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-persona, .stApp .chat-persona p, .stApp .chat-persona span, .stApp .chat-persona div { color:#3D2B1F !important; }

    .questao-box { background:#FFFFFF; border:2px solid #D4B896; border-radius:12px; padding:18px; margin-bottom:14px; }
    .stApp .questao-box, .stApp .questao-box p, .stApp .questao-box span, .stApp .questao-box div { color:#3D2B1F !important; }

    .avaliacao-box { background:#FFFFFF; border:2px solid #D4B896; border-radius:14px; padding:18px; margin-bottom:12px; }
    .stApp .avaliacao-box, .stApp .avaliacao-box p, .stApp .avaliacao-box span, .stApp .avaliacao-box div { color:#3D2B1F !important; }

    .meta-box { background:#FFFFFF; border:2px solid #D4B896; border-radius:12px; padding:16px; text-align:center; margin:10px 0; }
    .stApp .meta-box, .stApp .meta-box div, .stApp .meta-box span { color:#3D2B1F !important; }
    .stApp .meta-numero { font-size:2em; font-weight:700; color:#7C5C3E !important; }

    .chat-scroll-container { max-height:40vh; overflow-y:auto; display:flex; flex-direction:column; scroll-behavior:smooth; padding-bottom:4px; }
    .chat-scroll-container > * { flex-shrink:0; }
    

    </style>
\"\"\", unsafe_allow_html=True)

# ─── CACHE ───
@st.cache_resource
def get_cache_nutri():
    return {"perfis": {}}
_cache = get_cache_nutri()

# ─── CONQUISTAS ───
CONQUISTAS_DEF = [
    ("hidratacao",    "🏆 Mestre da Hidratação",  "7 dias seguidos atingindo meta de água"),
    ("proteina",      "🥇 Rei das Proteínas",      "7 dias seguidos batendo meta de proteína"),
    ("detox",         "🌿 Detox Master",            "Completou o desafio 7 dias sem refrigerante"),
    ("streak_100",    "🔥 100 Dias Seguidos",       "100 dias consecutivos seguindo o plano"),
    ("perfeita",      "🍎 Alimentação Perfeita",    "Saúde nutricional acima de 90 por 7 dias"),
    ("chef",          "👨‍🍳 Chef Iniciante",          "Gerou 10 receitas saudáveis"),
    ("planejador",    "📅 Planejador Master",        "Criou plano de 30 dias"),
    ("explorador",    "🌍 Explorador Culinário",     "Experimentou 5 culinárias diferentes"),
]

CULINÁRIAS = [
    "🇧🇷 Brasileira","🇮🇹 Italiana","🇯🇵 Japonesa","🇲🇽 Mexicana","🇫🇷 Francesa",
    "🇬🇷 Mediterrânea","🇹🇭 Tailandesa","🇮🇳 Indiana","🇨🇳 Chinesa","🇱🇧 Árabe",
    "🇵🇪 Peruana","🇰🇷 Coreana","🇲🇦 Marroquina","🇪🇸 Espanhola","🇻🇳 Vietnamita",
]

DICAS_IA = [
    "💡 Adicionar proteína no café da manhã reduz a fome em até 30% ao longo do dia.",
    "🥗 Comer fibras antes do prato principal diminui o índice glicêmico da refeição.",
    "💧 Beber 500ml de água 30 minutos antes das refeições ajuda a controlar as porções.",
    "🍳 Ovos mexidos com vegetais têm mais saciedade do que cereais industrializados.",
    "🥑 Gorduras boas no almoço ajudam a absorver vitaminas lipossolúveis da salada.",
    "🌙 Refeições leves à noite melhoram a qualidade do sono e a recuperação muscular.",
    "🍋 Vitamina C junto com ferro não-heme (feijão, lentilha) aumenta a absorção em até 3x.",
    "🫐 Antioxidantes de frutas escuras combatem inflamação causada por exercício intenso.",
]

FRASES_DIA = [
    "Seu corpo é o reflexo das escolhas que você faz todos os dias.",
    "Alimentação não é dieta — é estilo de vida.",
    "Cada refeição é uma oportunidade de se cuidar.",
    "Comer bem não precisa ser chato — precisa ser inteligente.",
    "A consistência vence a perfeição.",
]

# ─── PERSISTÊNCIA ───
CHAVES_SALVAR = [
    'usuario','historico_cardapios','receitas_salvas',
    'calorias_padrao','culinaria_favorita','restricoes',
    'objetivo','refeicoes_geradas','proteina_meta','carboidrato_meta',
    'gordura_meta','peso_atual','altura','idade','sexo',
    'nivel_atividade','alergias','estilo_alimentar','agua_meta',
    'streak_atual','maior_streak','dias_plano','conquistas',
    'desafio_ativo','xp_total','evolucao_peso','historico_agua',
    'checkins_nutri',
]

def gerar_json():
    dados = {k: st.session_state.get(k) for k in CHAVES_SALVAR}
    dados['salvo_em'] = datetime.now().strftime('%d/%m/%Y %H:%M')
    return json.dumps(dados, ensure_ascii=False, indent=2, default=str)

def carregar_json(dados):
    for k in CHAVES_SALVAR:
        if k in dados:
            st.session_state[k] = dados[k]

def salvar_cache(u):
    _cache["perfis"][u] = {k: st.session_state.get(k) for k in CHAVES_SALVAR}

def perfis_salvos():
    return list(_cache["perfis"].keys())

def carregar_cache(u):
    return _cache["perfis"].get(u)

def salvar_receita(tipo, nome, conteudo):
    st.session_state.historico_cardapios.append({
        'data': datetime.now().strftime('%d/%m %H:%M'),
        'tipo': tipo, 'nome': nome, 'conteudo': conteudo,
    })
    st.session_state.refeicoes_geradas += 1

def calcular_imc():
    peso = st.session_state.get('peso_atual', 0)
    altura = st.session_state.get('altura', 0)
    if peso and altura:
        return round(peso / ((altura/100)**2), 1)
    return 0

def calcular_saude_nutri():
    score = 50
    streak = st.session_state.get('streak_atual', 0)
    xp = st.session_state.get('xp_total', 0)
    receitas = st.session_state.get('refeicoes_geradas', 0)
    score += min(streak * 2, 20)
    score += min(xp / 100, 15)
    score += min(receitas * 0.5, 15)
    return min(int(score), 100)

defaults = {
    'etapa':'Login','usuario':'','api_key':'','pagina':'Home',
    'historico_cardapios':[],'receitas_salvas':[],
    'calorias_padrao':1500,'culinaria_favorita':'Brasileira',
    'restricoes':'','objetivo':'Perder gordura',
    'refeicoes_geradas':0,'proteina_meta':120,
    'carboidrato_meta':150,'gordura_meta':50,
    'peso_atual':0,'altura':0,'idade':30,'sexo':'Feminino',
    'nivel_atividade':'Moderado','alergias':'',
    'estilo_alimentar':'Sem restrições','agua_meta':2.5,
    'streak_atual':0,'maior_streak':0,'dias_plano':0,
    'conquistas':[],'desafio_ativo':None,'xp_total':0,
    'evolucao_peso':[],'historico_agua':[],'checkins_nutri':[],

    'dist_cul': None,
    'dist_kcal': None,
    'dist_nref': None,
    'dist_res': None,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─── IA ───
def nutri_ia(prompt, system_extra=""):
    try:
        client = Groq(api_key=st.session_state.api_key)
        perfil = (
            f"Usuário: {st.session_state.get('usuario','Usuário')}. "
            f"Objetivo: {st.session_state.get('objetivo','Manter peso')}. "
            f"Meta calórica: {st.session_state.get('calorias_padrao',2000)} kcal. "
            f"Proteína: {st.session_state.get('proteina_meta',50)}g. "
            f"Estilo: {st.session_state.get('estilo_alimentar','Brasileira')}. "
            f"Restrições: {st.session_state.get('restricoes','nenhuma') or 'nenhuma'}. "
            f"Alergias: {st.session_state.get('alergias','nenhuma') or 'nenhuma'}. "
            f"Culinária favorita: {st.session_state.get('culinaria_favorita','Brasileira')}. "
            f"IMC: {calcular_imc()}. Nível de atividade: {st.session_state.get('nivel_atividade','Moderado')}."
        )
        system = (
            f"Você é o NutriMind AI — nutricionista, chef e coach de hábitos alimentares em um só lugar.  REGRA DE OURO — CONFIABILIDADE 100%%: Forneça APENAS informações que você tem certeza absoluta que são verdadeiras. JAMAIS invente, suponha, extrapole ou preencha lacunas com dados fictícios. Se não souber algo com certeza — preço, endereço, horário, nome, estatística, lei, fato — diga EXPLICITAMENTE: 'Não tenho certeza sobre isso, recomendo verificar em [fonte].' É melhor uma resposta incompleta e honesta do que uma resposta completa e inventada. O usuário depende dessas informações para tomar decisões reais. "
            f"Você cria planos alimentares personalizados, sugere receitas saudáveis sem abrir mão do sabor, "
            f"e adapta o cardápio automaticamente quando há imprevistos ou desvios. "
            f"Sempre considera o perfil real do usuário. Nunca é genérico. "
            f"Inclui calorias e macronutrientes em TODAS as refeições. "
            f"Português do Brasil. {perfil} {system_extra}"
        )
        response = client.chat.completions.create(
            messages=[{"role":"system","content":system},{"role":"user","content":prompt}],
            model="openai/gpt-oss-120b",
            max_tokens=4096,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Erro na API: {e}"

def barra_salvar():
    salvar_cache(st.session_state.usuario)
    nome_u = st.session_state.usuario.lower().replace(' ','_') or 'sessao'
    xp = st.session_state.get('xp_total', 0)
    streak = st.session_state.get('streak_atual', 0)
    col_i, col_b = st.columns([4, 2])
    with col_i:
        st.markdown(
            f"<div style='background:#FFF7ED;border:1px solid #FDBA74;border-radius:10px;"
            f"padding:10px 14px;font-size:0.84em;color:#1A1A2E;line-height:1.6;'>"
            f"💾 <strong>Salve seus dados antes de sair.</strong><br>"
            f"<span style='color:#EA580C;font-size:0.88em;'>"
            f"🔥 {streak} dias seguidos · ⭐ {xp} XP · 🍽️ {st.session_state.refeicoes_geradas} refeições geradas"
            f"</span></div>", unsafe_allow_html=True)
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown(\"\"\"<style>
    .dica-nav{font-size:0.72em;color:#94A3B8;text-align:center;padding:2px 0 6px;}
    .dica-mobile{display:none;}
    .dica-desktop{display:block;}
    @media(max-width:768px){.dica-mobile{display:block;}.dica-desktop{display:none;}}
    </style>
    <div class='dica-nav dica-mobile'>👆 Deslize o dedo para navegar entre as abas</div>
    <div class='dica-nav dica-desktop'>📋 Clique no ícone acima para abrir o menu completo</div>
    \"\"\", unsafe_allow_html=True)

# ============================================================
# LOGIN
# ============================================================
def carregar_json_sessao(dados):
    _bloq = {'api_key','etapa','nome_login','chave_login','upload_login','btn_entrar_login'}
    _pref = (
        'btn_','sel_','ul_','dl_','cad_','_sub','_sm','_tab','_bsc',
        'ativo_','rem_','sel_pet_','ev_','prof_','hig_','prev_',
        'vac_','sint_','comp_','trad_','subs_','amb_','viag_','chat_',
        'duvida_','emerg_','peso_','data_','obs_','tipo_','vet_','desc_',
        'local_','prox_','alim','sit_emerg_','tc_','oraf','siau','agmag',
        'lv','mv','pt','pi','sh','wc','rv','rp','rc',
    )
    import re as _re
    for k, v in dados.items():
        if k in _bloq: continue
        if any(k.startswith(p) for p in _pref): continue
        if _re.match(r'.+_\\d+$', k): continue
        st.session_state[k] = v

if st.session_state.etapa == "Login":
    st.markdown("# 🍽️ NutriMind AI")
    st.markdown("<div class=\\'card\\'><b>🔒 ACESSO RESTRITO A CLIENTES DO MEUSAGENTESIA.COM.BR</b><br>🔗 <a href='https://meusagentesia.com.br' target='_blank' style='color:#4F46E5;font-weight:700;text-decoration:underline;'>meusagentesia.com.br</a></div>", unsafe_allow_html=True)
    st.info("💻 **Dica:** Pela complexidade dos agentes, no computador a experiência é mais agradável.")
    with st.container():
        nome  = st.text_input("Seu Nome:", key="nome_login")
        chave = st.text_input("🔑 Sua Chave API da Groq:", type="password", key="chave_login")
        if st.button("✨ ENTRAR", key="btn_entrar_login"):
            if len(nome.strip()) < 2:
                st.warning("Digite um nome com pelo menos 2 caracteres.")
            elif chave.strip():
                st.session_state.usuario = nome.strip()
                st.session_state.api_key = chave
                st.session_state.etapa = "App"
                st.rerun()
            else:
                st.warning("Preencha nome e chave API.")

elif st.session_state.etapa == "App":



    # TABS — navegação nativa com scroll horizontal
    _tab_Home, _tab_Perfil, _tab_DiaCompleto, _tab_Planejamento, _tab_Chef, _tab_Compras, _tab_Culinarias, _tab_Favoritos, _tab_Evolucao, _tab_Nutricionista, _tab_Fitness, _tab_Desafios, _tab_Conquistas, _tab_FotoPrato, _tab_Restaurante, _tab_IAPreventiva, _tab_Historico, _tab_Salvos, _tab_Distribuicao, _tab_NutricaoInt = st.tabs(['🏠 Painel', '📋 Perfil', '🍽️ Plano do Dia', '📅 Planejamento', '👨\\u200d🍳 Chef IA', '🛒 Compras', '🌍 Culinárias', '❤️ Favoritos', '📊 Evolução', '💬 Nutricionista', '🏃 Fitness', '🏆 Desafios', '🎖️ Conquistas', '📷 Foto Prato', '🏪 Restaurante', '🧠 IA Preventiva', '📖 Histórico', '❤️ Salvos', '🧮 Distribuição', '🥗 Nutrição'])

    # ── BARRA SALVAR — aparece em todas as abas ──
    with st.expander("💾 Salvar / Carregar meus dados", expanded=False):
        _bsc1, _bsc2 = st.columns(2)
        with _bsc1:
            import json as _jsv
            _dsv = {k: st.session_state.get(k) for k in list(st.session_state.keys()) if not k.startswith('_') and k not in ('api_key',)}
    with _tab_Home:
            col_u, col_r = st.columns([3,1])
            with col_u:
                st.title(f"🍽️ Olá, {st.session_state.usuario}!")
                st.markdown(f"<span class='badge'>🎯 {st.session_state.objetivo}</span> "
                    f"<span class='badge-verde'>🍴 {st.session_state.estilo_alimentar}</span>", unsafe_allow_html=True)
            with col_r:
                if st.button("🚪 Sair", key="chefcalo3"):
                    for k in list(st.session_state.keys()):
                        del st.session_state[k]
                    st.rerun()

            if not st.session_state.objetivo or not st.session_state.peso_atual:
                st.markdown(\"\"\"<div style="background:#FFF7ED;border:2px solid #F97316;border-radius:12px;
                padding:16px 20px;margin-bottom:16px;">
                <span style='font-size:1em;font-weight:600;color:#C2410C;'>
                ⚡ Configure seu 📋 Perfil Nutricional para ativar todos os recursos personalizados.
                </span></div>\"\"\", unsafe_allow_html=True)

            # PAINEL PRINCIPAL
            saude = calcular_saude_nutri()
            imc = calcular_imc()
            streak = st.session_state.get('streak_atual', 0)
            xp = st.session_state.get('xp_total', 0)
            dias = st.session_state.get('dias_plano', 0)

            st.markdown(f\"\"\"
            <div class='painel-nutri'>
                <div style='font-size:0.85em;opacity:0.7;letter-spacing:2px;margin-bottom:12px;'>🍽️ NUTRIMIND AI — PAINEL DE SAÚDE</div>
                <div style='display:grid;grid-template-columns:repeat(5,1fr);gap:14px;'>
                    <div style='text-align:center;background:rgba(255,255,255,0.06);border-radius:12px;padding:14px;'>
                        <div style='font-size:0.7em;opacity:0.6;'>🔥 META CALÓRICA</div>
                        <div style='font-size:1.6em;font-weight:700;'>{st.session_state.calorias_padrao} kcal</div>
                    </div>
                    <div style='text-align:center;background:rgba(255,255,255,0.06);border-radius:12px;padding:14px;'>
                        <div style='font-size:0.7em;opacity:0.6;'>❤️ SAÚDE NUTRI</div>
                        <div style='font-size:1.6em;font-weight:700;'>{saude}/100</div>
                    </div>
                    <div style='text-align:center;background:rgba(255,255,255,0.06);border-radius:12px;padding:14px;'>
                        <div style='font-size:0.7em;opacity:0.6;'>🔥 SEQUÊNCIA</div>
                        <div style='font-size:1.6em;font-weight:700;'>{streak} dias</div>
                    </div>
                    <div style='text-align:center;background:rgba(255,255,255,0.06);border-radius:12px;padding:14px;'>
                        <div style='font-size:0.7em;opacity:0.6;'>⭐ XP TOTAL</div>
                        <div style='font-size:1.6em;font-weight:700;'>{xp}</div>
                    </div>
                    <div style='text-align:center;background:rgba(255,255,255,0.06);border-radius:12px;padding:14px;'>
                        <div style='font-size:0.7em;opacity:0.6;'>📅 DIAS NO PLANO</div>
                        <div style='font-size:1.6em;font-weight:700;'>{dias}</div>
                    </div>
                </div>
            </div>
            \"\"\", unsafe_allow_html=True)

            # DASHBOARD
            st.markdown("### 📊 Dashboard")
            c1,c2,c3,c4,c5,c6 = st.columns(6)
            c1.markdown(f"<div class='stat-box'><div class='stat-numero'>{streak}</div><div>Dias seguidos</div></div>", unsafe_allow_html=True)
            c2.markdown(f"<div class='stat-box'><div class='stat-numero'>{st.session_state.get('maior_streak',0)}</div><div>Recorde</div></div>", unsafe_allow_html=True)
            c3.markdown(f"<div class='stat-box'><div class='stat-numero'>{saude}</div><div>Saúde /100</div></div>", unsafe_allow_html=True)
            c4.markdown(f"<div class='stat-box'><div class='stat-numero'>{imc or '—'}</div><div>IMC</div></div>", unsafe_allow_html=True)
            c5.markdown(f"<div class='stat-box'><div class='stat-numero'>{st.session_state.refeicoes_geradas}</div><div>Refeições</div></div>", unsafe_allow_html=True)
            c6.markdown(f"<div class='stat-box'><div class='stat-numero'>{len(st.session_state.receitas_salvas)}</div><div>Salvas</div></div>", unsafe_allow_html=True)

            # IA PREVENTIVA — alerta automático
            st.markdown("<hr class='divider'>", unsafe_allow_html=True)
            dica = random.choice(DICAS_IA)
            frase = random.choice(FRASES_DIA)
            st.markdown(f"<div class='ia-preventiva'>🤖 <strong>IA Preventiva:</strong> {dica}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='card'><em>💬 \\"{frase}\\"</em></div>", unsafe_allow_html=True)

            # COACH DIÁRIO
            st.markdown("### 🎯 Coach do Dia")
            col_coach, col_checkin = st.columns(2)
            with col_coach:
                if st.button("💡 DICA + MISSÃO DO DIA", key="chefcalo4"):
                    with st.spinner("Preparando seu coach..."):
                        prompt = (
                            f"Crie o coaching nutricional diário para {st.session_state.usuario}.\\n"
                            f"Objetivo: {st.session_state.objetivo}. Meta: {st.session_state.calorias_padrao} kcal.\\n\\n"
                            f"FORMATO:\\n\\n"
                            f"💡 DICA NUTRICIONAL DO DIA:\\n[dica específica e baseada em ciência]\\n\\n"
                            f"🥗 RECEITA EXCLUSIVA DE HOJE:\\n[1 receita rápida com macro e calorias]\\n\\n"
                            f"🎯 MISSÃO DO DIA:\\n[1 hábito alimentar para praticar hoje]\\n\\n"
                            f"🔥 MOTIVAÇÃO PERSONALIZADA:\\n[mensagem baseada no objetivo da pessoa]"
                        )
                        res = nutri_ia(prompt)
                        salvar_receita("Coach Diário", "Coaching do dia", res)
                        st.session_state.xp_total += 10
                        st.session_state['coach_temp'] = res

                if st.session_state.get('coach_temp'):
                    st.markdown(f"<div class='card'>{st.session_state['coach_temp']}</div>", unsafe_allow_html=True)

            with col_checkin:
                st.markdown("#### ✅ Check-in do Dia")
                agua_hoje = st.number_input("💧 Água bebida hoje (L):", min_value=0.0, max_value=10.0, value=0.0, step=0.1, key="agua_hoje_input")
                seguiu_plano = st.radio("Seguiu o plano alimentar?", ["✅ Sim","⚠️ Parcialmente","❌ Não"], key="seguiu_plano")
                if st.button("✅ FAZER CHECK-IN", key="chefcalo5"):
                    checkin = {'data': datetime.now().strftime('%d/%m %H:%M'), 'agua': agua_hoje, 'plano': seguiu_plano}
                    st.session_state.checkins_nutri.append(checkin)
                    st.session_state.historico_agua.append({'data': date.today().isoformat(), 'litros': agua_hoje})
                    if "Sim" in seguiu_plano:
                        st.session_state.streak_atual += 1
                        st.session_state.xp_total += 20
                        st.session_state.dias_plano += 1
                        if st.session_state.streak_atual > st.session_state.get('maior_streak', 0):
                            st.session_state.maior_streak = st.session_state.streak_atual
                        st.success(f"🏆 +20 XP! Streak: {st.session_state.streak_atual} dias!")
                    else:
                        st.info("📖 Registrado. Amanhã é uma nova chance!")
                    st.rerun()

            # ÚLTIMAS REFEIÇÕES
            if st.session_state.historico_cardapios:
                st.markdown("<hr class='divider'>", unsafe_allow_html=True)
                st.markdown("### 🕐 Últimas Refeições")
                for item in reversed(st.session_state.historico_cardapios[-4:]):
                    st.markdown(f"<div class='hist-item'><span class='badge'>{item['tipo']}</span> <small style='color:#888'>{item['data']}</small><br><small>{item['nome'][:80]}</small></div>", unsafe_allow_html=True)

        # ──────────────────────────────────────────
        # PERFIL NUTRICIONAL
        # ──────────────────────────────────────────

    with _tab_Perfil:
            st.header("📋 Meu Perfil Nutricional")

            with st.form("form_perfil_nutri"):
                st.markdown("#### 👤 Dados Pessoais")
                col1, col2, col3 = st.columns(3)
                with col1:
                    p_peso = st.number_input("⚖️ Peso atual (kg):", min_value=30.0, max_value=300.0, value=float(st.session_state.get('peso_atual',70) or 70), step=0.5, key="chefcalo6")
                    p_altura = st.number_input("📏 Altura (cm):", min_value=100, max_value=220, value=int(st.session_state.get('altura',170) or 170), key="chefcalo7")
                    p_idade = st.number_input("🎂 Idade:", min_value=10, max_value=100, value=int(st.session_state.get('idade',30)), key="chefcalo8")
                with col2:
                    p_sexo = st.selectbox("⚧ Sexo biológico:", ["Feminino","Masculino"],
                        index=0 if st.session_state.get('sexo','Feminino')=='Feminino' else 1, key="chefcalo11")
                    p_atividade = st.selectbox("🏃 Nível de atividade:", ["Sedentário","Levemente ativo","Moderado","Muito ativo","Atleta"],
                        index=["Sedentário","Levemente ativo","Moderado","Muito ativo","Atleta"].index(st.session_state.get('nivel_atividade','Moderado')), key="chefcalo10")
                    p_objetivo = st.selectbox("🎯 Objetivo:", ["Perder gordura","Ganhar massa muscular","Manutenção","Saúde geral","Performance esportiva"],
                        index=["Perder gordura","Ganhar massa muscular","Manutenção","Saúde geral","Performance esportiva"].index(st.session_state.get('objetivo','Perder gordura')), key="chefcalo9")
                with col3:
                    p_calorias = st.number_input("🔥 Meta calórica diária (kcal):", min_value=800, max_value=5000, value=max(800, int(st.session_state.get("calorias_padrao", 1500) or 800)), step=50, key="chefcalo9_d2")
                    p_proteina = st.number_input("💪 Meta de proteína (g):", min_value=20, max_value=300, value=max(20, int(st.session_state.get("proteina_meta", 120) or 20)), step=5, key="chefcalo10_d2")
                    p_agua = st.number_input("💧 Meta de água (L):", min_value=1.0, max_value=8.0, value=max(1.0, float(st.session_state.get("agua_meta", 2.5) or 1.0)), step=0.25, key="chefcalo11_d2")

                st.markdown("#### 🍴 Preferências Alimentares")
                col4, col5 = st.columns(2)
                with col4:
                    p_estilo = st.selectbox("🥗 Estilo alimentar:", ["Sem restrições","Mediterrânea","Low Carb","Cetogênica","Vegetariano","Vegano","Paleolítica","Flexitariano"],
                        index=["Sem restrições","Mediterrânea","Low Carb","Cetogênica","Vegetariano","Vegano","Paleolítica","Flexitariano"].index(st.session_state.estilo_alimentar) if st.session_state.estilo_alimentar in ["Sem restrições","Mediterrânea","Low Carb","Cetogênica","Vegetariano","Vegano","Paleolítica","Flexitariano"] else 0, key="chefcalo8_d2")
                    p_culinaria = st.selectbox("🌍 Culinária favorita:", [c.split(" ",1)[1] if " " in c else c for c in CULINÁRIAS],
                        index=0, key="chefcalo7_d2")
                with col5:
                    p_restricoes = st.text_area("🚫 Restrições alimentares:", value=st.session_state.restricoes, height=80, placeholder="ex: sem lactose, sem glúten, não como peixe...", key="chefcalo12")
                    p_alergias = st.text_area("🥜 Alergias:", value=st.session_state.alergias, height=80, placeholder="ex: amendoim, frutos do mar, ovo...", key="chefcalo13")

                sub = st.form_submit_button("💾 SALVAR PERFIL", key="chefcalofsb501")
                if sub:
                    st.session_state.peso_atual = p_peso
                    st.session_state.altura = p_altura
                    st.session_state.idade = p_idade
                    st.session_state.sexo = p_sexo
                    st.session_state.nivel_atividade = p_atividade
                    st.session_state.objetivo = p_objetivo
                    st.session_state.calorias_padrao = p_calorias
                    st.session_state.proteina_meta = p_proteina
                    st.session_state.agua_meta = p_agua
                    st.session_state.estilo_alimentar = p_estilo
                    st.session_state.culinaria_favorita = p_culinaria
                    st.session_state.restricoes = p_restricoes
                    st.session_state.alergias = p_alergias
                    salvar_cache(st.session_state.usuario)
                    st.success("✅ Perfil salvo! O NutriMind agora conhece você de verdade.")

            if st.session_state.peso_atual:
                imc = calcular_imc()
                classificacao = "Abaixo do peso" if imc < 18.5 else ("Normal" if imc < 25 else ("Sobrepeso" if imc < 30 else "Obesidade"))
                cor_imc = "#059669" if 18.5 <= imc < 25 else "#D97706"
                st.markdown(f"<div style='background:#FFF7ED;border:1px solid #FDBA74;border-radius:12px;padding:16px;margin-top:12px;'>",unsafe_allow_html=True)
                col_imc, col_obj = st.columns(2)
                col_imc.markdown(f"**IMC:** {imc} — {classificacao}")
                col_obj.markdown(f"**Objetivo:** {st.session_state.objetivo} · **Meta:** {st.session_state.calorias_padrao} kcal")
                st.markdown("</div>", unsafe_allow_html=True)

        # ──────────────────────────────────────────
        # PLANO DO DIA
        # ──────────────────────────────────────────

    with _tab_DiaCompleto:
            st.header("🍽️ Plano Alimentar do Dia")

            col1, col2 = st.columns(2)
            with col1:
                refeicoes_dia = st.multiselect("Refeições do dia:", ["☕ Café da manhã","🥪 Lanche da manhã","🍽️ Almoço","🍎 Lanche da tarde","🌙 Jantar","🥛 Ceia"],
                    default=["☕ Café da manhã","🍽️ Almoço","🍎 Lanche da tarde","🌙 Jantar"], key="chefcalo6_d2")
            with col2:
                contexto_dia = st.text_input("Algo especial hoje?", placeholder="ex: vou malhar, vou a um churrasco, preciso de algo rápido...", key="ti_chef_cal_101")
                culinaria_dia = st.selectbox("Estilo do dia:", [c.split(" ",1)[1] if " " in c else c for c in CULINÁRIAS], key="chefcalo14")

            if st.button("🍽️ GERAR PLANO DO DIA COMPLETO", key="chefcalo15"):
                with st.spinner("Montando seu dia alimentar perfeito..."):
                    prompt = (
                        f"Crie um plano alimentar completo e detalhado para hoje.\\n"
                        f"Refeições: {', '.join(refeicoes_dia)}. Contexto: {contexto_dia or 'dia normal'}. "
                        f"Culinária: {culinaria_dia}.\\n\\n"
                        f"Para CADA refeição use este formato:\\n\\n"
                        f"[EMOJI] [NOME DA REFEIÇÃO] · [HORÁRIO SUGERIDO]\\n"
                        f"[Prato principal com ingredientes]\\n"
                        f"🔥 [X] kcal · 💪 [X]g proteína · 🍞 [X]g carbo · 🥑 [X]g gordura\\n"
                        f"👨‍🍳 Preparo rápido: [como fazer em poucos passos]\\n\\n"
                        f"[repita para todas as refeições]\\n\\n"
                        f"📊 TOTAL DO DIA:\\n"
                        f"🔥 Total: [X] kcal (meta: {st.session_state.calorias_padrao} kcal)\\n"
                        f"💪 Proteína: [X]g (meta: {st.session_state.proteina_meta}g)\\n"
                        f"🍞 Carboidrato: [X]g · 🥑 Gordura: [X]g\\n\\n"
                        f"⚖️ ANÁLISE: [como esse dia se compara à meta — está dentro? acima? como ajustar se necessário]\\n\\n"
                        f"💡 DICA DO DIA: [1 orientação específica para o contexto de hoje]"
                    )
                    res = nutri_ia(prompt)
                    salvar_receita("Plano do Dia", f"Dia completo — {culinaria_dia}", res)
                    st.session_state.xp_total += 15
                    st.session_state['dia_temp'] = res

            if st.session_state.get('dia_temp'):
                st.markdown(f"<div class='card'>{st.session_state['dia_temp']}</div>", unsafe_allow_html=True)
                col_dl, col_sv = st.columns(2)
                with col_dl:
                    st.download_button("📋 Baixar (.txt)", data=st.session_state['dia_temp'], file_name="plano_dia.txt", mime="text/plain", use_container_width=True,
        key="dl_chef_cal_2"
    )
                with col_sv:
                    if st.button("❤️ Salvar", key="sv_dia", use_container_width=True):
                        st.session_state.receitas_salvas.append({'tipo':'Plano do Dia','nome':f"Dia — {culinaria_dia}",'conteudo':st.session_state['dia_temp'],'data':datetime.now().strftime('%d/%m %H:%M'),'favorito':False})
                        st.success("❤️ Salvo!")

        # ──────────────────────────────────────────
        # PLANEJAMENTO 7-90 DIAS
        # ──────────────────────────────────────────

    with _tab_Planejamento:
            st.header("📅 Planejamento Premium")
            st.markdown("A IA varia as receitas para evitar repetição e manter a motivação.")

            col1, col2 = st.columns(2)
            with col1:
                dias_plan = st.selectbox("Duração do planejamento:", ["7 dias","15 dias","30 dias","90 dias"], key="chefcalo16")
                foco_plan = st.selectbox("Foco desta semana:", ["Balanceado","Alta proteína","Detox e leveza","Ganho de massa","Anti-inflamatório","Low carb"], key="chefcalo17")
            with col2:
                incluir_lista = st.checkbox("Incluir lista de compras", value=True, key="chefcalo18")
                incluir_dicas = st.checkbox("Incluir dicas nutricionais por dia", value=True, key="chefcalo19")

            if st.button("📅 GERAR PLANEJAMENTO COMPLETO", key="chefcalo20"):
                with st.spinner(f"Criando {dias_plan} de alimentação variada e personalizada..."):
                    dias_num = int(dias_plan.split()[0])
                    prompt = (
                        f"Crie um planejamento alimentar completo de {dias_plan} com foco em {foco_plan}.\\n"
                        f"Varie as receitas para evitar repetição. Cada dia deve ter cardápio diferente.\\n\\n"
                        f"Para cada dia use:\\n\\n"
                        f"📅 DIA [N] — [TEMA DO DIA]\\n"
                        f"☕ Café: [prato] ([X] kcal)\\n"
                        f"🍽️ Almoço: [prato] ([X] kcal)\\n"
                        f"🍎 Lanche: [prato] ([X] kcal)\\n"
                        f"🌙 Jantar: [prato] ([X] kcal)\\n"
                        f"🔥 Total: [X] kcal · 💪 [X]g prot\\n\\n"
                        f"[repita para todos os {dias_num} dias]\\n\\n"
                    )
                    if incluir_lista:
                        prompt += f"🛒 LISTA DE COMPRAS CONSOLIDADA:\\n[itens organizados por setor]\\n\\n"
                    if incluir_dicas:
                        prompt += f"💡 DICAS NUTRICIONAIS DA SEMANA:\\n[3-5 dicas práticas]"

                    res = nutri_ia(prompt)
                    salvar_receita("Planejamento", f"{dias_plan} — {foco_plan}", res)
                    st.session_state.xp_total += 30
                    if "30" in dias_plan or "90" in dias_plan:
                        if "planejador" not in st.session_state.get('conquistas', []):
                            st.session_state.conquistas.append("planejador")
                            st.success("🏆 Conquista desbloqueada: Planejador Master!")
                    st.session_state['plan_temp'] = res

            if st.session_state.get('plan_temp'):
                st.markdown(f"<div class='card'>{st.session_state['plan_temp']}</div>", unsafe_allow_html=True)
                col_dl, col_sv = st.columns(2)
                with col_dl:
                    st.download_button("📋 Baixar (.txt)", data=st.session_state['plan_temp'], file_name=f"planejamento_{dias_plan.replace(' ','_')}.txt", mime="text/plain", use_container_width=True,
        key="dl_chef_cal_3"
    )
                with col_sv:
                    if st.button("❤️ Salvar", key="sv_plan", use_container_width=True):
                        st.session_state.receitas_salvas.append({'tipo':'Planejamento','nome':f"{dias_plan} — {foco_plan}",'conteudo':st.session_state['plan_temp'],'data':datetime.now().strftime('%d/%m %H:%M'),'favorito':False})
                        st.success("❤️ Salvo!")

        # ──────────────────────────────────────────
        # CHEF IA
        # ──────────────────────────────────────────

    with _tab_Chef:
            st.header("👨‍🍳 Chef IA — Versão Saudável")
            st.markdown("Digite qualquer prato — a IA cria uma versão mais saudável mantendo o sabor.")

            prato_chef = st.text_input("🍽️ Qual prato você quer transformar?", placeholder="ex: Lasanha, Hambúrguer, Feijoada, Pizza, Açaí...", key="ti_chef_cal_102")
            col1, col2 = st.columns(2)
            with col1:
                tipo_chef = st.selectbox("Tipo de adaptação:", ["Mais saudável (menos calorias)","Alta proteína","Low carb","Sem glúten","Sem lactose","Vegano","Anti-inflamatório"], key="chefcalo21")
            with col2:
                porcoes_chef = st.number_input("Porções:", min_value=1, max_value=20, value=2, key="chefcalo22")

            if st.button("👨‍🍳 CRIAR VERSÃO SAUDÁVEL", key="chefcalo23"):
                if prato_chef.strip():
                    with st.spinner(f"O Chef IA está reinventando {prato_chef}..."):
                        prompt = (
                            f"Crie uma versão saudável de {prato_chef} com adaptação: {tipo_chef}. Porções: {porcoes_chef}.\\n\\n"
                            f"FORMATO:\\n\\n"
                            f"👨‍🍳 {prato_chef.upper()} — VERSÃO {tipo_chef.upper()}\\n\\n"
                            f"📊 COMPARAÇÃO NUTRICIONAL:\\n"
                            f"| | Versão Original | Versão Saudável |\\n"
                            f"|---|---|---|\\n"
                            f"| Calorias | [X] kcal | [X] kcal |\\n"
                            f"| Proteína | [X]g | [X]g |\\n"
                            f"| Gordura | [X]g | [X]g |\\n\\n"
                            f"🥘 INGREDIENTES SUBSTITUÍDOS:\\n[o que mudou e por quê — explique os benefícios]\\n\\n"
                            f"📋 INGREDIENTES (para {porcoes_chef} porções):\\n[lista completa]\\n\\n"
                            f"👨‍🍳 MODO DE PREPARO:\\n[passo a passo]\\n\\n"
                            f"⏱️ Tempo: [X] min · 🔥 [X] kcal/porção · 💪 [X]g proteína/porção\\n\\n"
                            f"💡 DICA DO CHEF: [1 truque para manter o sabor original]"
                        )
                        res = nutri_ia(prompt)
                        salvar_receita("Chef IA", prato_chef, res)
                        st.session_state.xp_total += 15
                        if st.session_state.refeicoes_geradas >= 10:
                            if "chef" not in st.session_state.get('conquistas', []):
                                st.session_state.conquistas.append("chef")
                                st.success("🏆 Conquista: Chef Iniciante!")
                        st.session_state['chef_temp'] = res
                else:
                    st.warning("Digite o prato que quer transformar.")

            if st.session_state.get('chef_temp'):
                st.markdown(f"<div class='card-green'>{st.session_state['chef_temp']}</div>", unsafe_allow_html=True)
                col_dl, col_sv = st.columns(2)
                with col_dl:
                    st.download_button("📋 Baixar receita (.txt)", data=st.session_state['chef_temp'], file_name=f"receita_{prato_chef.replace(' ','_') if 'prato_chef' in dir() else 'chef'}.txt", mime="text/plain", use_container_width=True,
        key="dl_chef_cal_4"
    )
                with col_sv:
                    if st.button("❤️ Salvar receita", key="sv_chef", use_container_width=True):
                        st.session_state.receitas_salvas.append({'tipo':'Chef IA','nome':prato_chef if 'prato_chef' in dir() else '','conteudo':st.session_state['chef_temp'],'data':datetime.now().strftime('%d/%m %H:%M'),'favorito':False})
                        st.success("❤️ Salvo!")

        # ──────────────────────────────────────────
        # LISTA DE COMPRAS
        # ──────────────────────────────────────────

    with _tab_Compras:
            st.header("🛒 Compras Inteligentes")

            col1, col2 = st.columns(2)
            with col1:
                pessoas_compras = st.selectbox("Para quantas pessoas:", ["1 pessoa","2 pessoas","3-4 pessoas (família)","5+ pessoas"], key="chefcalo24")
                dias_compras = st.selectbox("Duração:", ["3 dias","1 semana","2 semanas","1 mês"], key="chefcalo25")
            with col2:
                orcamento_compras = st.number_input("Orçamento (R$, opcional):", min_value=0, value=0, step=50, key="chefcalo26")
                foco_compras = st.selectbox("Foco:", ["Alimentação balanceada","Alta proteína","Low carb","Detox","Economia"], key="chefcalo27")

            if st.button("🛒 GERAR LISTA DE COMPRAS", key="chefcalo28"):
                with st.spinner("Montando sua lista inteligente..."):
                    orcamento_txt = f"Orçamento: R${orcamento_compras}." if orcamento_compras > 0 else ""
                    prompt = (
                        f"Crie uma lista de compras inteligente e organizada.\\n"
                        f"Pessoas: {pessoas_compras}. Duração: {dias_compras}. Foco: {foco_compras}. {orcamento_txt}\\n\\n"
                        f"FORMATO:\\n\\n"
                        f"🛒 LISTA DE COMPRAS — {dias_compras.upper()} para {pessoas_compras.upper()}\\n\\n"
                        f"🥩 CARNES E PROTEÍNAS:\\n[item — quantidade — preço estimado]\\n\\n"
                        f"🥬 HORTIFRUTI:\\n[item — quantidade — preço estimado]\\n\\n"
                        f"🥛 LATICÍNIOS E OVOS:\\n[item — quantidade — preço estimado]\\n\\n"
                        f"🌾 GRÃOS E CEREAIS:\\n[item — quantidade — preço estimado]\\n\\n"
                        f"🧂 TEMPEROS E CONDIMENTOS:\\n[item — quantidade — preço estimado]\\n\\n"
                        f"🧃 BEBIDAS:\\n[item — quantidade — preço estimado]\\n\\n"
                        f"🍫 OUTROS:\\n[item — quantidade — preço estimado]\\n\\n"
                        f"💰 TOTAL ESTIMADO: R$[X]\\n\\n"
                        f"💡 DICA DE ECONOMIA: [como economizar sem abrir mão da qualidade nutricional]"
                    )
                    res = nutri_ia(prompt)
                    salvar_receita("Lista de Compras", f"{dias_compras} — {pessoas_compras}", res)
                    st.session_state.xp_total += 10
                    st.session_state['compras_temp'] = res

            if st.session_state.get('compras_temp'):
                st.markdown(f"<div class='card-blue'>{st.session_state['compras_temp']}</div>", unsafe_allow_html=True)
                st.download_button("📋 Baixar lista (.txt)", data=st.session_state['compras_temp'], file_name="lista_compras.txt", mime="text/plain",
        key="dl_chef_cal_5"
    )

        # ──────────────────────────────────────────
        # CULINÁRIAS DO MUNDO
        # ──────────────────────────────────────────

    with _tab_Culinarias:
            st.header("🌍 Descobrir Culinárias")
            st.markdown("Mais de 15 culinárias. A IA cria receitas autênticas e saudáveis de qualquer país.")

            culinaria_sel = st.selectbox("Escolha a culinária:", CULINÁRIAS, key="chefcalo29")
            col1, col2 = st.columns(2)
            with col1:
                tipo_refeicao_cul = st.selectbox("Tipo de refeição:", ["Qualquer","Café da manhã","Almoço/Jantar","Lanche","Sobremesa"], key="chefcalo30")
            with col2:
                dificuldade_cul = st.selectbox("Dificuldade:", ["Fácil (até 20 min)","Médio (20-40 min)","Chef (40+ min)"], key="chefcalo31")

            if st.button("🌍 DESCOBRIR RECEITA", key="chefcalo32"):
                with st.spinner(f"Buscando inspiração na culinária {culinaria_sel}..."):
                    prompt = (
                        f"Crie uma receita autêntica da culinária {culinaria_sel}, adaptada para ser saudável.\\n"
                        f"Tipo: {tipo_refeicao_cul}. Dificuldade: {dificuldade_cul}.\\n\\n"
                        f"FORMATO:\\n\\n"
                        f"🌍 [NOME DO PRATO] — {culinaria_sel.upper()}\\n\\n"
                        f"🗺️ ORIGEM E HISTÓRIA:\\n[2-3 linhas sobre o prato e sua origem cultural]\\n\\n"
                        f"📊 INFORMAÇÕES NUTRICIONAIS:\\n🔥 [X] kcal · 💪 [X]g prot · 🍞 [X]g carbo · 🥑 [X]g gord\\n\\n"
                        f"📋 INGREDIENTES:\\n[lista]\\n\\n"
                        f"👨‍🍳 PREPARO:\\n[passo a passo]\\n\\n"
                        f"⏱️ Tempo: [X] min · Porções: [X]\\n\\n"
                        f"🥗 VERSÃO MAIS SAUDÁVEL:\\n[adaptações para reduzir calorias ou aumentar proteína]"
                    )
                    res = nutri_ia(prompt)
                    salvar_receita("Culinária", culinaria_sel, res)
                    st.session_state.xp_total += 10
                    st.session_state['culinaria_temp'] = res

            if st.session_state.get('culinaria_temp'):
                st.markdown(f"<div class='card-purple'>{st.session_state['culinaria_temp']}</div>", unsafe_allow_html=True)
                col_dl, col_sv = st.columns(2)
                with col_dl:
                    st.download_button("📋 Baixar (.txt)", data=st.session_state['culinaria_temp'], file_name="receita_mundial.txt", mime="text/plain", use_container_width=True,
        key="dl_chef_cal_6"
    )
                with col_sv:
                    if st.button("❤️ Salvar", key="sv_culinaria", use_container_width=True):
                        st.session_state.receitas_salvas.append({'tipo':'Culinária','nome':culinaria_sel if 'culinaria_sel' in dir() else '','conteudo':st.session_state['culinaria_temp'],'data':datetime.now().strftime('%d/%m %H:%M'),'favorito':False})
                        st.success("❤️ Salvo!")

        # ──────────────────────────────────────────
        # FAVORITOS
        # ──────────────────────────────────────────

    with _tab_Favoritos:
            st.header("❤️ Receitas Favoritas")

            categorias = ["Todas","Café da manhã","Almoço","Jantar","Lanche","Sobremesas","Fitness","Vegetariano","Chef IA","Culinária","Planejamento"]
            filtro = st.selectbox("Filtrar por categoria:", categorias, key="filtro_favoritos")

            receitas = st.session_state.receitas_salvas
            if filtro != "Todas":
                receitas = [r for r in receitas if filtro.lower() in r.get('tipo','').lower() or filtro.lower() in r.get('nome','').lower()]

            if not receitas:
                st.info("Nenhuma receita salva nesta categoria. Gere receitas e salve suas favoritas!")
            else:
                st.markdown(f"**{len(receitas)} receita(s) encontrada(s)**")
                for i, item in enumerate(reversed(receitas)):
                    idx_real = len(st.session_state.receitas_salvas) - 1 - i
                    with st.expander(f"[{item['tipo']}] {item['nome'][:60]} — {item['data']}"):
                        st.markdown(f"<div class='card'>{item['conteudo']}</div>", unsafe_allow_html=True)
                        col_dl, col_del = st.columns([3,1])
                        with col_dl:
                            st.download_button("📋 Baixar", data=item['conteudo'], file_name=f"{item['tipo'].lower().replace(' ','_')}.txt", mime="text/plain", key=f"dl_fav_{i}")
                        with col_del:
                            if st.button("🗑️", key=f"del_fav_{i}"):
                                st.session_state.receitas_salvas.pop(idx_real)
                                st.rerun()

        # ──────────────────────────────────────────
        # EVOLUÇÃO E PROGRESSO
        # ──────────────────────────────────────────

    with _tab_Evolucao:
            st.header("📊 Evolução e Progresso")

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### ⚖️ Registrar Peso")
                novo_peso = st.number_input("Peso de hoje (kg):", min_value=30.0, max_value=300.0, value=float(st.session_state.get('peso_atual',70) or 70), step=0.1, key="chefcalo33")
                if st.button("✅ Registrar peso", key="chefcalo34"):
                    st.session_state.peso_atual = novo_peso
                    if 'evolucao_peso' not in st.session_state:
                        st.session_state.evolucao_peso = []
                    st.session_state.evolucao_peso.append({'data': date.today().isoformat(), 'peso': novo_peso})
                    st.session_state.xp_total += 5
                    st.success(f"✅ Peso registrado: {novo_peso} kg")
                    st.rerun()
            with col2:
                st.markdown("#### 📏 Seus Indicadores")
                imc = calcular_imc()
                saude = calcular_saude_nutri()
                xp = st.session_state.get('xp_total', 0)
                st.markdown(f"**IMC:** {imc} | **Saúde:** {saude}/100 | **XP:** {xp}")

            if st.session_state.get('evolucao_peso'):
                st.markdown("#### 📈 Histórico de Peso")
                pesos = st.session_state.evolucao_peso[-10:]
                for p in reversed(pesos):
                    st.markdown(f"<div class='hist-item'>{p['data']} — <strong>{p['peso']} kg</strong></div>", unsafe_allow_html=True)

            if st.button("📊 ANÁLISE DE EVOLUÇÃO PELA IA", key="chefcalo35"):
                with st.spinner("Analisando sua evolução..."):
                    hist = st.session_state.get('evolucao_peso', [])
                    agua_hist = st.session_state.get('historico_agua', [])
                    prompt = (
                        f"Analise a evolução nutricional deste usuário.\\n"
                        f"Objetivo: {st.session_state.objetivo}. Peso atual: {st.session_state.peso_atual}kg. "
                        f"Altura: {st.session_state.altura}cm. IMC: {imc}. "
                        f"Histórico de peso: {hist[-5:] if hist else 'não registrado'}. "
                        f"Saúde nutricional: {saude}/100. Streak: {st.session_state.streak_atual} dias.\\n\\n"
                        f"FORMATO:\\n\\n"
                        f"📊 ANÁLISE DE EVOLUÇÃO\\n\\n"
                        f"📈 O QUE ESTÁ FUNCIONANDO:\\n[pontos positivos]\\n\\n"
                        f"⚠️ O QUE AJUSTAR:\\n[pontos a melhorar]\\n\\n"
                        f"🎯 META PARA AS PRÓXIMAS 2 SEMANAS:\\n[objetivo específico e realista]\\n\\n"
                        f"💡 RECOMENDAÇÃO DA IA:\\n[ajuste no plano alimentar baseado nos dados]"
                    )
                    res = nutri_ia(prompt)
                    salvar_receita("Análise", "Evolução nutricional", res)
                    st.session_state['evolucao_temp'] = res

            if st.session_state.get('evolucao_temp'):
                st.markdown(f"<div class='card'>{st.session_state['evolucao_temp']}</div>", unsafe_allow_html=True)

        # ──────────────────────────────────────────
        # NUTRICIONISTA IA
        # ──────────────────────────────────────────

    with _tab_Nutricionista:
            st.header("💬 Nutricionista IA")
            st.markdown("Converse naturalmente. A IA reorganiza seu plano quando há imprevistos.")

            st.markdown(\"\"\"
            <div class='ia-preventiva'>
            💡 <strong>Exemplos:</strong> "Vou viajar essa semana" · "Hoje comi pizza no almoço, como compenso?"
            · "Não gosto de peixe" · "Quero incluir mais fibras" · "Tenho um churrasco amanhã"
            </div>
            \"\"\", unsafe_allow_html=True)

            if 'chat_nutri' not in st.session_state:
                st.session_state.chat_nutri = []
            if 'nutri_key' not in st.session_state:
                st.session_state.nutri_key = 0

            for msg in st.session_state.chat_nutri:
                if msg['role'] == 'user':
                    st.markdown(f"<div style='background:#FFF7ED;border:1px solid #FDBA74;border-radius:12px 12px 4px 12px;padding:12px 16px;margin:8px 0;'><b style='color:#C2410C'>Você:</b> <span style='color:#1A1A2E'>{msg['content']}</span></div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='card' style='margin:8px 0;'><b>🍽️ NutriMind:</b><br>{msg['content']}</div>", unsafe_allow_html=True)

            if not st.session_state.chat_nutri:
                st.markdown("<div class='card' style='text-align:center;'>🍽️ <strong>Olá! Sou seu nutricionista pessoal.</strong><br>Me conte o que está acontecendo com sua alimentação hoje.</div>", unsafe_allow_html=True)

            pergunta = st.text_input("Mensagem:", key=f"nutri_input_{st.session_state.nutri_key}", placeholder="Hoje comi pizza, o que faço no jantar?", label_visibility="collapsed")

            col_env, col_lim = st.columns([4,1])
            with col_env:
                if st.button("📤 ENVIAR", key="chefcalo36"):
                    if pergunta.strip():
                        historico_msgs = [{"role":m["role"],"content":m["content"]} for m in st.session_state.chat_nutri[-8:]]
                        with st.spinner("..."):
                            try:
                                client = Groq(api_key=st.session_state.api_key)
                                perfil_txt = (f"Usuário: {st.session_state.usuario}. Objetivo: {st.session_state.objetivo}. "
                                    f"Meta: {st.session_state.calorias_padrao} kcal. Restrições: {st.session_state.restricoes or 'nenhuma'}.")
                                msgs = [{"role":"system","content":f"Você é o NutriMind AI, nutricionista pessoal. {perfil_txt} Responda de forma prática e adaptativa — reorganize o plano quando necessário, nunca culpe o usuário por desvios."}] + historico_msgs + [{"role":"user","content":pergunta}]
                                response = client.chat.completions.create(messages=msgs, model="openai/gpt-oss-120b")
                                resp = response.choices[0].message.content
                                if resp: st.session_state['res_nutricionist_chefca1'] = str(resp)
                                if resp: st.session_state['res_nutricioni_chefca1'] = resp
                            except Exception as e:
                                resp = f"⚠️ Erro: {e}"
                        st.session_state.chat_nutri.append({"role":"user","content":pergunta})
                        st.session_state.chat_nutri.append({"role":"assistant","content":resp})
                        st.session_state.nutri_key += 1
                        salvar_receita("Nutricionista IA", pergunta[:60], resp)
                        st.rerun()
            with col_lim:
                if st.button("🗑️", key="chefcalo37"):
                    st.session_state.chat_nutri = []
                    st.rerun()

        # ──────────────────────────────────────────
        # ÁREA FITNESS
        # ──────────────────────────────────────────

    with _tab_Fitness:
            st.header("🏃 Área Fitness")
            st.markdown("A IA recalcula suas calorias com base na atividade física do dia.")

            col1, col2 = st.columns(2)
            with col1:
                atividade_fit = st.selectbox("Atividade física hoje:", ["Caminhada 🚶","Corrida 🏃","Bicicleta 🚴","Musculação 🏋️","Natação 🏊","HIIT","Yoga","Futebol","Sem atividade"], key="chefcalo38")
                duracao_fit = st.number_input("Duração (minutos):", min_value=0, max_value=300, value=45, key="chefcalo39")
            with col2:
                intensidade_fit = st.selectbox("Intensidade:", ["Leve","Moderada","Intensa","Muito intensa"], key="chefcalo40")
                peso_fit = float(st.session_state.get('peso_atual', 70) or 70)

            if st.button("🏃 CALCULAR E AJUSTAR CARDÁPIO", key="chefcalo41"):
                with st.spinner("Calculando gasto calórico e ajustando cardápio..."):
                    prompt = (
                        f"Calcule o gasto calórico e ajuste o cardápio do dia.\\n"
                        f"Atividade: {atividade_fit}. Duração: {duracao_fit} min. Intensidade: {intensidade_fit}. "
                        f"Peso: {peso_fit}kg. Meta base: {st.session_state.calorias_padrao} kcal.\\n\\n"
                        f"FORMATO:\\n\\n"
                        f"🏃 ANÁLISE FITNESS DO DIA\\n\\n"
                        f"🔥 GASTO CALÓRICO ESTIMADO: [X] kcal\\n\\n"
                        f"📊 META CALÓRICA AJUSTADA:\\n"
                        f"Base: {st.session_state.calorias_padrao} kcal\\n"
                        f"+ Exercício: [X] kcal\\n"
                        f"= Total de hoje: [X] kcal\\n\\n"
                        f"🍽️ AJUSTE NO CARDÁPIO:\\n[o que adicionar ou remover para compensar o gasto]\\n\\n"
                        f"💪 REFEIÇÃO PÓS-TREINO IDEAL:\\n[receita específica com macros — foco em recuperação]\\n\\n"
                        f"💧 HIDRATAÇÃO RECOMENDADA:\\n[quantos litros para hoje com esse exercício]"
                    )
                    res = nutri_ia(prompt)
                    salvar_receita("Fitness", f"{atividade_fit} — {duracao_fit}min", res)
                    st.session_state.xp_total += 15
                    st.session_state['fitness_temp'] = res

            if st.session_state.get('fitness_temp'):
                st.markdown(f"<div class='card-green'>{st.session_state['fitness_temp']}</div>", unsafe_allow_html=True)

        # ──────────────────────────────────────────
        # DESAFIOS
        # ──────────────────────────────────────────

    with _tab_Desafios:
            st.header("🏆 Desafios Nutricionais")

            DESAFIOS_LIST = [
                ("desafio_7_refri",   "🥤 7 dias sem refrigerante",      7,  "Elimina açúcar e melhora hidratação"),
                ("desafio_21_acucar", "🍬 21 dias sem açúcar refinado",  21, "Reset do paladar e estabiliza insulina"),
                ("desafio_30_limpa",  "🥗 30 dias de alimentação limpa", 30, "Transforma hábitos alimentares"),
                ("desafio_mediterra", "🇬🇷 Desafio Mediterrâneo",        21, "Rica em gorduras boas e antioxidantes"),
                ("desafio_anti",      "🌿 Desafio Anti-inflamatório",    14, "Reduz inflamação e melhora energia"),
                ("desafio_7_legumes", "🥦 7 dias comendo legumes diário",  7, "Aumenta fibras e micronutrientes"),
            ]

            if not st.session_state.get('desafio_ativo'):
                st.markdown("### Escolha seu desafio")
                for chave, nome, dias, desc in DESAFIOS_LIST:
                    col_d, col_b = st.columns([4,1])
                    with col_d:
                        st.markdown(f"<div class='desafio-box'><strong>{nome}</strong> — {dias} dias<br><small>{desc}</small></div>", unsafe_allow_html=True)
                    with col_b:
                        if st.button("🚀 Iniciar", key=f"des_{chave}"):
                            with st.spinner("Preparando seu desafio..."):
                                prompt = (
                                    f"Crie um guia completo para o desafio: {nome} ({dias} dias).\\n\\n"
                                    f"Inclua: o que esperar dia a dia, dicas para não desistir, "
                                    f"o que comer no lugar do item eliminado, e os benefícios científicos."
                                )
                                res = nutri_ia(prompt)
                                st.session_state.desafio_ativo = {'chave': chave, 'nome': nome, 'dias': dias, 'inicio': date.today().isoformat(), 'guia': res, 'dia_atual': 1}
                                salvar_receita("Desafio", nome, res)
                                st.rerun()
            else:
                des = st.session_state.desafio_ativo
                dia_atual = des.get('dia_atual', 1)
                total = des['dias']
                pct = min(int(dia_atual / total * 100), 100)

                st.markdown(f"### 🔥 {des['nome']}")
                st.markdown(f"**Dia {dia_atual} de {total}** — Iniciado em {des['inicio']}")
                st.progress(pct / 100)
                st.markdown(f"**{pct}% concluído** · +{dia_atual * 10} XP acumulados")

                with st.expander("📖 Ver guia do desafio"):
                    st.markdown(f"<div class='card'>{des['guia']}</div>", unsafe_allow_html=True)

                col_ok, col_enc = st.columns(2)
                with col_ok:
                    if st.button("✅ CONCLUÍ O DIA DE HOJE", key="chefcalo42"):
                        st.session_state.desafio_ativo['dia_atual'] = dia_atual + 1
                        st.session_state.xp_total += 10
                        if dia_atual + 1 > total:
                            if des['chave'] not in st.session_state.get('conquistas', []):
                                st.session_state.conquistas.append(des['chave'])
                            st.success(f"🏆 Desafio {des['nome']} CONCLUÍDO! Conquista desbloqueada!")
                            st.session_state.desafio_ativo = None
                        else:
                            st.success(f"✅ Dia {dia_atual} concluído! +10 XP")
                        st.rerun()
                with col_enc:
                    if st.button("🔄 Encerrar desafio", key="chefcalo43"):
                        st.session_state.desafio_ativo = None
                        st.rerun()

        # ──────────────────────────────────────────
        # CONQUISTAS
        # ──────────────────────────────────────────

    with _tab_Conquistas:
            st.header("🎖️ Minhas Conquistas")
            conquistadas = st.session_state.get('conquistas', [])
            obtidas = len(conquistadas)
            total = len(CONQUISTAS_DEF)
            st.markdown(f"**{obtidas} de {total} conquistas desbloqueadas**")
            st.progress(obtidas / total if total > 0 else 0)

            cols_c = st.columns(3)
            for i, (chave, nome, desc) in enumerate(CONQUISTAS_DEF):
                obtida = chave in conquistadas
                estilo = "border:2px solid #EA580C;" if obtida else "opacity:0.4;border:1px solid #E2E8F0;"
                icon = "🏆" if obtida else "🔒"
                with cols_c[i % 3]:
                    st.markdown(f"<div class='conquista-box' style='{estilo}'>"
                        f"<div style='font-size:1.4em;'>{icon}</div>"
                        f"<div style='font-weight:700;font-size:0.9em;'>{nome}</div>"
                        f"<div style='font-size:0.78em;color:#6B7280;'>{desc}</div>"
                        f"</div>", unsafe_allow_html=True)

            st.markdown(f"### ⭐ XP Total: {st.session_state.get('xp_total', 0)}")

        # ──────────────────────────────────────────
        # FOTO DO PRATO
        # ──────────────────────────────────────────

    with _tab_FotoPrato:
            st.header("📷 Analisar Foto do Prato")
            st.markdown("Descreva o que está no seu prato — a IA estima os macros e dá uma nota nutricional.")

            descricao_prato = st.text_area("📝 Descreva o prato detalhadamente:", height=120,
                placeholder="ex: Prato com arroz branco (4 colheres), feijão caldo (1 concha), frango grelhado (1 filé médio), salada de alface e tomate com azeite...", key="chefcalo5_d2")
            porcao_prato = st.selectbox("Tamanho da porção:", ["Pequena","Média","Grande","Muito grande"], key="chefcalo44")

            if st.button("📷 ANALISAR PRATO", key="chefcalo45"):
                if descricao_prato.strip():
                    with st.spinner("Analisando os nutrientes..."):
                        prompt = (
                            f"Analise os macronutrientes e calorias deste prato.\\n"
                            f"Descrição: {descricao_prato}. Porção: {porcao_prato}.\\n\\n"
                            f"FORMATO:\\n\\n"
                            f"📷 ANÁLISE NUTRICIONAL DO PRATO\\n\\n"
                            f"📊 ESTIMATIVA NUTRICIONAL:\\n"
                            f"🔥 Calorias: [X] kcal\\n"
                            f"💪 Proteína: [X]g\\n"
                            f"🍞 Carboidratos: [X]g\\n"
                            f"🥑 Gorduras: [X]g\\n"
                            f"🌾 Fibras: [X]g\\n\\n"
                            f"⭐ NOTA NUTRICIONAL: [0-100]\\n[justificativa da nota]\\n\\n"
                            f"✅ PONTOS POSITIVOS:\\n[o que está bom neste prato]\\n\\n"
                            f"💡 COMO MELHORAR:\\n[1-2 sugestões simples para tornar mais nutritivo]\\n\\n"
                            f"📋 COMO SE ENCAIXA NA SUA META:\\n"
                            f"[Comparação com a meta de {st.session_state.calorias_padrao} kcal — sobrou ou gastou quanto?]\\n\\n"
                            f"⚠️ Aviso: estas são estimativas — os valores reais podem variar conforme preparo e ingredientes exatos."
                        )
                        res = nutri_ia(prompt)
                        salvar_receita("Análise de Prato", descricao_prato[:60], res)
                        st.session_state.xp_total += 5
                        st.session_state['foto_temp'] = res
                else:
                    st.warning("Descreva o prato para análise.")

            if st.session_state.get('foto_temp'):
                st.markdown(f"<div class='card-green'>{st.session_state['foto_temp']}</div>", unsafe_allow_html=True)
                st.markdown("<div class='card-red' style='font-size:0.82em;padding:12px 16px;'>⚠️ Aviso: estimativas nutricionais por descrição podem ter variações de 15-25%. Para dados precisos, utilize um aplicativo com base de dados alimentar verificada.</div>", unsafe_allow_html=True)

        # ──────────────────────────────────────────
        # ASSISTENTE DE RESTAURANTE
        # ──────────────────────────────────────────

    with _tab_Restaurante:
            st.header("🏪 Assistente de Restaurante")
            st.markdown("A IA recomenda os melhores pratos do cardápio para o seu objetivo.")

            col1, col2 = st.columns(2)
            with col1:
                restaurante_nome = st.text_input("🍽️ Nome do restaurante ou tipo de culinária:", placeholder="ex: Outback, pizzaria italiana, japonês, churrascaria...", key="ti_chef_cal_103")
            with col2:
                situacao_rest = st.selectbox("Situação:", ["Almoço de trabalho","Jantar especial","Comida rápida","Celebração","Data especial"], key="chefcalo46")

            cardapio_rest = st.text_area("📋 Cole o cardápio (opcional):", height=120, placeholder="Se tiver o cardápio, cole aqui para recomendações mais precisas...", key="chefcalo47")

            if st.button("🏪 RECOMENDAR PRATOS", key="chefcalo48"):
                if restaurante_nome.strip():
                    with st.spinner(f"Analisando o {restaurante_nome}..."):
                        cardapio_txt = f"Cardápio disponível:\\n{cardapio_rest}" if cardapio_rest.strip() else "Cardápio não informado — baseie-se no tipo de restaurante."
                        prompt = (
                            f"Recomende os melhores pratos para comer em {restaurante_nome} ({situacao_rest}).\\n"
                            f"{cardapio_txt}\\n\\n"
                            f"FORMATO:\\n\\n"
                            f"🏪 {restaurante_nome.upper()} — GUIA DE PEDIDO\\n\\n"
                            f"✅ MELHOR OPÇÃO (mais alinhada ao objetivo):\\n[prato, por quê, estimativa calórica]\\n\\n"
                            f"🥈 SEGUNDA OPÇÃO:\\n[prato alternativo com justificativa]\\n\\n"
                            f"❌ EVITAR:\\n[o que NÃO pedir e por quê]\\n\\n"
                            f"💡 DICAS INTELIGENTES:\\n"
                            f"• Como pedir modificações no prato\\n"
                            f"• Acompanhamentos a pedir ou evitar\\n"
                            f"• Como compensar no restante do dia"
                        )
                        res = nutri_ia(prompt)
                        salvar_receita("Restaurante", restaurante_nome, res)
                        st.session_state['rest_temp'] = res
                else:
                    st.warning("Informe o nome ou tipo do restaurante.")

            if st.session_state.get('rest_temp'):
                st.markdown(f"<div class='card-blue'>{st.session_state['rest_temp']}</div>", unsafe_allow_html=True)

        # ──────────────────────────────────────────
        # IA PREVENTIVA E COACH
        # ──────────────────────────────────────────

    with _tab_IAPreventiva:
            st.header("🧠 IA Preventiva e Coach")
            st.markdown("Antes de você pedir, a IA analisa seus padrões e sugere.")

            if st.button("🧠 ANÁLISE PREVENTIVA COMPLETA", key="chefcalo49"):
                with st.spinner("Analisando seus padrões alimentares..."):
                    checkins = st.session_state.get('checkins_nutri', [])
                    agua_hist = st.session_state.get('historico_agua', [])
                    agua_media = sum(a.get('litros',0) for a in agua_hist[-7:]) / max(len(agua_hist[-7:]),1)
                    streak = st.session_state.get('streak_atual', 0)

                    prompt = (
                        f"Faça uma análise preventiva completa dos hábitos nutricionais.\\n"
                        f"Média de água/dia (7 dias): {agua_media:.1f}L (meta: {st.session_state.agua_meta}L). "
                        f"Streak atual: {streak} dias. Objetivo: {st.session_state.objetivo}. "
                        f"Refeições geradas: {st.session_state.refeicoes_geradas}. "
                        f"Check-ins: {len(checkins)}.\\n\\n"
                        f"FORMATO:\\n\\n"
                        f"🧠 ANÁLISE PREVENTIVA — {st.session_state.usuario.upper()}\\n\\n"
                        f"🔍 O QUE IDENTIFIQUEI NOS SEUS PADRÕES:\\n[análise honesta dos dados disponíveis]\\n\\n"
                        f"⚠️ ALERTAS PREVENTIVOS:\\n[o que pode estar acontecendo que a pessoa não percebe]\\n\\n"
                        f"💧 HIDRATAÇÃO:\\n[avaliação e recomendação]\\n\\n"
                        f"💡 3 SUGESTÕES IMEDIATAS:\\n[ações concretas para os próximos 7 dias]\\n\\n"
                        f"🎯 MISSÃO DA SEMANA:\\n[1 hábito para implementar]"
                    )
                    res = nutri_ia(prompt)
                    salvar_receita("IA Preventiva", "Análise automática", res)
                    st.session_state['preventiva_temp'] = res

            if st.session_state.get('preventiva_temp'):
                st.markdown(f"<div class='card'>{st.session_state['preventiva_temp']}</div>", unsafe_allow_html=True)

            st.markdown("<hr class='divider'>", unsafe_allow_html=True)
            st.markdown("### 💬 Pergunte ao Coach")
            coach_pergunta = st.text_area("Relate algo sobre sua alimentação:", height=100,
                placeholder="ex: Estou há 3 dias sem conseguir seguir o plano. Tenho sentido muita fome à noite...", key="chefcalo4_d2")
            if st.button("💬 ORIENTAÇÃO DO COACH", key="chefcalo50"):
                if coach_pergunta.strip():
                    with st.spinner("..."):
                        res = nutri_ia(coach_pergunta, "Responda como um coach nutricional empático — sem culpar, reorganizando o plano de forma prática.")
                        salvar_receita("Coach", coach_pergunta[:60], res)
                        st.session_state['coach_consult_temp'] = res
            if st.session_state.get('coach_consult_temp'):
                st.markdown(f"<div class='ia-preventiva'>{st.session_state['coach_consult_temp']}</div>", unsafe_allow_html=True)

        # ──────────────────────────────────────────
        # HISTÓRICO
        # ──────────────────────────────────────────

    with _tab_Historico:
            st.header("📖 Histórico de Cardápios")

            if not st.session_state.historico_cardapios:
                st.info("Nenhum cardápio gerado ainda.")
            else:
                tipos = list(set(e['tipo'] for e in st.session_state.historico_cardapios))
                filtro = st.selectbox("Filtrar:", ["Todos"] + tipos, key="filtro_hist")
                hist_f = [e for e in st.session_state.historico_cardapios if filtro == "Todos" or e['tipo'] == filtro]
                st.markdown(f"**{len(hist_f)} registros**")
                for i, item in enumerate(reversed(hist_f[-20:])):
                    with st.expander(f"[{item['tipo']}] {item['nome'][:60]} — {item['data']}"):
                        st.markdown(f"<div class='card'>{item['conteudo']}</div>", unsafe_allow_html=True)
                        col_dl, col_sv = st.columns([3,1])
                        with col_dl:
                            st.download_button("📋 Baixar", data=item['conteudo'], file_name=f"{item['tipo'].lower().replace(' ','_')}.txt", mime="text/plain", key=f"dl_hist_{i}")
                        with col_sv:
                            if st.button("❤️ Salvar", key=f"sv_hist_{i}"):
                                st.session_state.receitas_salvas.append({**item, 'favorito': False})
                                st.success("❤️ Salvo!")

                hist_txt = "\\n\\n".join(f"[{e['data']}] {e['tipo']} — {e['nome']}\\n{e['conteudo']}\\n{'─'*40}" for e in st.session_state.historico_cardapios)
                st.download_button("⬇️ Exportar histórico completo (.txt)", data=hist_txt, file_name="historico_nutrimind.txt", mime="text/plain",
        key="dl_chef_cal_7"
    )
                if st.button("🗑️ Limpar histórico", key="chefcalo51"):
                    st.session_state.historico_cardapios = []
                    st.rerun()

        # ──────────────────────────────────────────
        # RECEITAS SALVAS
        # ──────────────────────────────────────────

    with _tab_Salvos:
            st.header("❤️ Receitas Salvas")
            if not st.session_state.receitas_salvas:
                st.info("Nenhuma receita salva ainda.")
            else:
                filtro_s = st.selectbox("Filtrar:", ["Todas"] + list(set(r['tipo'] for r in st.session_state.receitas_salvas)), key="filtro_salvos")
                salvos_f = [r for r in st.session_state.receitas_salvas if filtro_s == "Todas" or r['tipo'] == filtro_s]
                st.markdown(f"**{len(salvos_f)} receita(s)**")
                for i, item in enumerate(reversed(salvos_f)):
                    idx_real = len(st.session_state.receitas_salvas) - 1 - i
                    with st.expander(f"[{item['tipo']}] {item['nome'][:60]} — {item['data']}"):
                        st.markdown(f"<div class='card'>{item['conteudo']}</div>", unsafe_allow_html=True)
                        col_dl, col_del = st.columns([3,1])
                        with col_dl:
                            st.download_button("📋 Baixar", data=item['conteudo'], file_name=f"{item['tipo'].lower().replace(' ','_')}.txt", mime="text/plain", key=f"dl_salvo_{i}")
                        with col_del:
                            if st.button("🗑️", key=f"del_salvo_{i}"):
                                st.session_state.receitas_salvas.pop(idx_real)
                                st.rerun()

        # ──────────────────────────────────────────
        # DISTRIBUIÇÃO CALÓRICA INTELIGENTE
        # ──────────────────────────────────────────

    with _tab_Distribuicao:
            st.header("🧮 Distribuição Calórica Inteligente")

            c1, c2, c3 = st.columns(3)
            with c1:
                cul = st.selectbox("🍽️ Culinária",
                    ["🇧🇷 Brasileira","🌵 Nordestina","🇯🇵 Japonesa",
                     "🇮🇹 Italiana","🥗 Saudável","🌱 Vegetariana","🍖 Carnívora"],
                    key="dist_cul")
            with c2:
                nref = st.selectbox("🍴 Refeições",
                    ["2","3","4","5","6"], key="dist_nref")
            with c3:
                kcal = st.number_input("🔥 Calorias/dia",
                    min_value=800, max_value=5000, value=1500, step=100,
                    key="dist_kcal")

            cul_val  = st.session_state.dist_cul
            nref_val = st.session_state.dist_nref
            kcal_val = int(st.session_state.get("dist_kcal") or 1500)

            nomes_ref = {
                "2": ["Almoço","Jantar"],
                "3": ["Café da manhã","Almoço","Jantar"],
                "4": ["Café da manhã","Almoço","Lanche","Jantar"],
                "5": ["Café da manhã","Lanche manhã","Almoço","Lanche tarde","Jantar"],
                "6": ["Café da manhã","Lanche manhã","Almoço","Lanche tarde","Jantar","Ceia"],
            }
            lista = nomes_ref.get(nref_val, nomes_ref["3"])
            n = len(lista)

            defaults_pct = {
                "Café da manhã":25,"Lanche manhã":10,"Almoço":35,
                "Lanche tarde":10,"Lanche":10,"Jantar":25,"Ceia":5,
            }

            st.markdown("### 📊 Distribua as calorias")
            st.caption("O total deve somar 100% — a última refeição recebe o restante automaticamente.")

            pcts = {}
            usado = 0

            for i, ref in enumerate(lista[:-1]):
                reserva = n - 1 - i  # mínimo 1% para cada refeição restante
                max_disp = 100 - usado - reserva
                max_disp = max(max_disp, 1)
                def_val  = min(defaults_pct.get(ref, 20), max_disp)

                key = f"dist_n_{nref_val}_{i}"
                # Garantir que o valor salvo não excede o máximo disponível
                if key not in st.session_state:
                    st.session_state[key] = def_val
                if st.session_state[key] > max_disp:
                    st.session_state[key] = max_disp

                col_a, col_b = st.columns([3, 1])
                with col_a:
                    # Barra visual de progresso
                    st.markdown(
                        f"<div style='margin-bottom:4px;font-weight:600;font-size:0.9em;'>{ref}</div>"
                        f"<div style='background:#F1F5F9;border-radius:999px;height:10px;'>"
                        f"<div style='background:#EA580C;border-radius:999px;height:100%;"
                        f"width:{st.session_state[key]}%;'></div></div>",
                        unsafe_allow_html=True
                    )
                with col_b:
                    pct = st.number_input(
                        f"% {ref}",
                        min_value=1,
                        max_value=max_disp,
                        value=st.session_state[key],
                        step=1,
                        key=key,
                        label_visibility="collapsed"
                    )

                kcal_ref = round(kcal_val * pct / 100)
                st.caption(f"→ {kcal_ref} kcal  |  disponível para o resto: {max_disp - pct}%")
                pcts[ref] = pct
                usado += pct

            # Última refeição = restante automático
            ultima    = lista[-1]
            pct_ult   = 100 - usado
            kcal_ult  = round(kcal_val * pct_ult / 100)
            pcts[ultima] = pct_ult

            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.markdown(
                    f"<div style='margin-bottom:4px;font-weight:600;font-size:0.9em;'>{ultima} <span style='color:#059669;font-size:0.8em;'>(automático)</span></div>"
                    f"<div style='background:#F1F5F9;border-radius:999px;height:10px;'>"
                    f"<div style='background:#059669;border-radius:999px;height:100%;width:{pct_ult}%;'></div></div>",
                    unsafe_allow_html=True
                )
            with col_b:
                st.markdown(f"<div style='padding-top:4px;font-weight:700;color:#059669;'>{pct_ult}%</div>",
                            unsafe_allow_html=True)
            st.caption(f"→ {kcal_ult} kcal  |  Total: 100% = {kcal_val} kcal ✅")

            st.markdown("---")

            if st.button("🤖 GERAR PLANO", use_container_width=True, key="chefcalo52"):
                refs_txt = " | ".join(
                    f"{r} ({pcts[r]}% = {round(kcal_val*pcts[r]/100)} kcal)"
                    for r in lista
                )
                prompt = (
                    f"Plano: {cul_val}, {kcal_val} kcal/dia, {nref_val} refeições.\\n"
                    f"Distribuição: {refs_txt}\\n\\n"
                    f"Para cada refeição:\\n"
                    f"**[Nome] — [kcal]**\\n"
                    f"Prato: [nome]\\n"
                    f"Ingredientes: [lista curta]\\n"
                    f"Preparo: [1 linha]\\n\\n"
                    f"Gere TODAS as {nref_val} refeições. Seja breve. Português brasileiro."
                )
                with st.spinner(f"Gerando {nref_val} refeições — {kcal_val} kcal..."):
                    res = nutri_ia(prompt,
                        system_extra=f"Use EXATAMENTE {kcal_val} kcal divididas conforme: {refs_txt}. Ignore qualquer outra meta calórica.")
                st.session_state.dist_res = res

            if st.session_state.get("dist_res"):
                st.markdown("---")
                st.markdown(st.session_state.dist_res)
                st.download_button("📋 Baixar", data=st.session_state.dist_res,
                    file_name="plano.txt", mime="text/plain", key="dist_dl")

    with _tab_NutricaoInt:
            st.header("🥗 Nutrição Inteligente")
            st.markdown("Análise nutricional profunda, carências, suplementação e recomendações personalizadas.")

            tab_analise, tab_carencias, tab_supl, tab_hidra = st.tabs([
                "🔬 Analisar Minha Dieta","⚠️ Carências Nutricionais","💊 Suplementação","💧 Hidratação"
            ])

            with tab_analise:
                st.markdown("### 🔬 Análise Nutricional Completa")
                dieta_desc = st.text_area("Descreva o que você costuma comer num dia típico:", height=180,
                    placeholder="Ex: Café: pão com manteiga e café com leite. Almoço: arroz, feijão, frango e salada. Lanche: fruta. Jantar: sopa...", key="chefcalo3_d2")
                col1, col2 = st.columns(2)
                with col1:
                    peso_n = st.number_input("⚖️ Peso (kg):", value=float(st.session_state.get('peso_atual',70) or 70), step=0.5, key="chefcalo53")
                    objetivo_n = st.selectbox("🎯 Objetivo:", ["Emagrecer","Ganhar massa","Manutenção","Saúde geral","Performance"], key="chefcalo54")
                with col2:
                    idade_n = st.number_input("🎂 Idade:", value=int(st.session_state.get('idade',30)), step=1, key="chefcalo55")
                    atividade_n = st.selectbox("🏃 Atividade:", ["Sedentário","Levemente ativo","Moderado","Muito ativo","Atleta"], key="chefcalo56")

                if st.button("🔬 ANALISAR MINHA DIETA", key="chefcalo57"):
                    if dieta_desc.strip():
                        with st.spinner("Analisando nutricionalmente..."):
                            prompt = (
                                f"Faça uma análise nutricional completa da dieta descrita.\\n"
                                f"Dieta: {dieta_desc}\\n"
                                f"Peso: {peso_n}kg. Idade: {idade_n}. Objetivo: {objetivo_n}. Atividade: {atividade_n}.\\n\\n"
                                f"FORMATO:\\n\\n"
                                f"🔬 ANÁLISE NUTRICIONAL COMPLETA\\n\\n"
                                f"📊 ESTIMATIVA DE MACROS DIÁRIOS:\\n"
                                f"🔥 Calorias: ~[X] kcal (necessidade estimada: [X] kcal)\\n"
                                f"💪 Proteína: ~[X]g (recomendado: [X]g)\\n"
                                f"🍞 Carboidratos: ~[X]g (recomendado: [X]g)\\n"
                                f"🥑 Gorduras: ~[X]g (recomendado: [X]g)\\n"
                                f"🌾 Fibras: ~[X]g (recomendado: 25-35g)\\n\\n"
                                f"✅ O QUE ESTÁ BOM:\\n[pontos positivos da dieta]\\n\\n"
                                f"⚠️ O QUE PRECISA MELHORAR:\\n[deficiências e problemas]\\n\\n"
                                f"🎯 ADEQUAÇÃO AO OBJETIVO '{objetivo_n}':\\n[análise específica]\\n\\n"
                                f"💡 3 MUDANÇAS SIMPLES QUE FARIAM GRANDE DIFERENÇA:\\n[sugestões práticas e realistas]"
                            )
                            res = nutri_ia(prompt)
                            salvar_receita("Análise Nutricional", "Dieta do dia", res)
                            st.session_state['nutrint_analise'] = res
                    else:
                        st.warning("Descreva sua dieta antes de analisar.")

                if st.session_state.get('nutrint_analise'):
                    st.markdown(f"<div class='card'>{st.session_state['nutrint_analise']}</div>", unsafe_allow_html=True)

            with tab_carencias:
                st.markdown("### ⚠️ Identificar Carências Nutricionais")
                st.markdown("*Descreva seus sintomas e a IA identifica possíveis deficiências.*")
                sintomas = st.text_area("🩺 Seus sintomas ou queixas:", height=120,
                    placeholder="ex: cansaço frequente, queda de cabelo, unhas fracas, dificuldade de concentração, cãibras...", key="chefcalo2")
                dieta_car = st.text_area("🍽️ O que você costuma comer:", height=100,
                    placeholder="ex: pouca carne vermelha, não como peixe, vegetariano...", key="chefcalo1")

                if st.button("⚠️ IDENTIFICAR POSSÍVEIS CARÊNCIAS", key="chefcalo58"):
                    if sintomas.strip():
                        with st.spinner("Analisando..."):
                            prompt = (
                                f"Com base nos sintomas e dieta, identifique possíveis carências nutricionais.\\n"
                                f"Sintomas: {sintomas}\\nDieta: {dieta_car or 'não informada'}\\n\\n"
                                f"FORMATO:\\n\\n"
                                f"⚠️ POSSÍVEIS CARÊNCIAS IDENTIFICADAS\\n\\n"
                                f"⚠️ IMPORTANTE: Esta análise é educacional e não substitui avaliação médica.\\n\\n"
                                f"Para cada carência suspeita:\\n\\n"
                                f"🔴 [NUTRIENTE]\\n"
                                f"Sintomas compatíveis: [quais sintomas relatados]\\n"
                                f"Fontes alimentares: [alimentos ricos nesse nutriente]\\n"
                                f"Como incluir na dieta: [sugestão prática]\\n"
                                f"Quando buscar médico: [sinais de alerta]\\n\\n"
                                f"[Repita para cada carência]\\n\\n"
                                f"🥗 ALIMENTOS PARA INCLUIR NA ROTINA:\\n[lista com os mais importantes]\\n\\n"
                                f"⚕️ RECOMENDAÇÃO: Consulte um nutricionista ou médico para exames e diagnóstico preciso."
                            )
                            res = nutri_ia(prompt)
                            salvar_receita("Carências", sintomas[:60], res)
                            st.session_state['nutrint_carencias'] = res
                    else:
                        st.warning("Descreva seus sintomas.")

                if st.session_state.get('nutrint_carencias'):
                    st.markdown(f"<div class='card-yellow'>{st.session_state['nutrint_carencias']}</div>", unsafe_allow_html=True)

            with tab_supl:
                st.markdown("### 💊 Guia de Suplementação")
                obj_supl = st.selectbox("Objetivo:", ["Emagrecer","Ganhar massa muscular","Energia e disposição","Saúde geral","Performance esportiva","Sono e recuperação"], key="chefcalo59")
                nivel_supl = st.selectbox("Nível de atividade:", ["Sedentário","Praticante casual","Praticante regular","Atleta"], key="chefcalo60")
                restricoes_supl = st.text_input("Restrições (alergias, medicamentos):", placeholder="ex: lactose, anticoagulante...", key="ti_chef_cal_104")

                if st.button("💊 GERAR GUIA DE SUPLEMENTAÇÃO", key="chefcalo61"):
                    with st.spinner("Analisando..."):
                        prompt = (
                            f"Crie um guia de suplementação para:\\nObjetivo: {obj_supl}\\nNível: {nivel_supl}\\nRestrições: {restricoes_supl or 'nenhuma'}\\n\\n"
                            f"FORMATO:\\n\\n"
                            f"💊 GUIA DE SUPLEMENTAÇÃO — {obj_supl.upper()}\\n\\n"
                            f"⚠️ AVISO: Consulte um profissional de saúde antes de iniciar suplementação.\\n\\n"
                            f"✅ SUPLEMENTOS RECOMENDADOS:\\n\\n"
                            f"Para cada suplemento:\\n"
                            f"[Nome] — [benefício principal]\\n"
                            f"• Quando tomar: [horário e momento]\\n"
                            f"• Dosagem sugerida: [quantidade]\\n"
                            f"• Custo estimado: [faixa de preço]\\n"
                            f"• Prioridade: [essencial / recomendado / opcional]\\n\\n"
                            f"🚫 O QUE EVITAR:\\n[suplementos desnecessários ou com riscos]\\n\\n"
                            f"🥗 ANTES DOS SUPLEMENTOS, PRIORIZE:\\n[ajustes alimentares que substituem suplementos]"
                        )
                        res = nutri_ia(prompt)
                        salvar_receita("Suplementação", obj_supl, res)
                        st.session_state['nutrint_supl'] = res

                if st.session_state.get('nutrint_supl'):
                    st.markdown(f"<div class='card-blue'>{st.session_state['nutrint_supl']}</div>", unsafe_allow_html=True)

            with tab_hidra:
                st.markdown("### 💧 Hidratação Inteligente")
                col1, col2 = st.columns(2)
                with col1:
                    peso_h = st.number_input("⚖️ Peso (kg):", value=float(st.session_state.get('peso_atual',70) or 70), step=0.5, key="hidra_peso")
                    ativ_h = st.selectbox("🏃 Atividade física:", ["Sedentário","Levemente ativo","Moderado","Muito ativo","Atleta"], key="hidra_ativ")
                with col2:
                    clima_h = st.selectbox("🌡️ Clima:", ["Frio","Temperado","Quente","Muito quente/Úmido"], key="hidra_clima")
                    saude_h = st.text_input("💊 Condições de saúde:", placeholder="ex: hipertensão, diabetes, grávida...", key="hidra_saude")

                # Cálculo rápido
                base = peso_h * 35  # ml
                if ativ_h in ["Moderado"]: base += 300
                elif ativ_h in ["Muito ativo"]: base += 600
                elif ativ_h == "Atleta": base += 1000
                if clima_h == "Quente": base += 300
                elif clima_h == "Muito quente/Úmido": base += 600
                meta_agua = base / 1000

                st.markdown(f\"\"\"
                <div class='meta-box' style='margin:12px 0;'>
                    <div style='font-size:0.82em;color:#C2410C;'>💧 SUA META DIÁRIA DE ÁGUA</div>
                    <div class='meta-numero'>{meta_agua:.1f} L</div>
                    <div style='font-size:0.85em;color:#C2410C;'>({int(meta_agua/0.25)} copos de 250ml)</div>
                </div>
                \"\"\", unsafe_allow_html=True)

                if st.button("💧 GUIA COMPLETO DE HIDRATAÇÃO", key="chefcalo62"):
                    with st.spinner("..."):
                        prompt = (
                            f"Crie um guia completo de hidratação personalizado.\\n"
                            f"Peso: {peso_h}kg. Atividade: {ativ_h}. Clima: {clima_h}. Saúde: {saude_h or 'sem restrições'}.\\n"
                            f"Meta calculada: {meta_agua:.1f}L/dia.\\n\\n"
                            f"💧 GUIA DE HIDRATAÇÃO\\n\\n"
                            f"Meta diária: {meta_agua:.1f}L\\n\\n"
                            f"⏰ DISTRIBUIÇÃO AO LONGO DO DIA:\\n[horários sugeridos para beber água]\\n\\n"
                            f"✅ ALÉM DA ÁGUA — outras fontes de hidratação:\\n[alimentos e bebidas que contribuem]\\n\\n"
                            f"🚨 SINAIS DE DESIDRATAÇÃO:\\n[o que observar]\\n\\n"
                            f"💡 DICAS PARA BEBER MAIS ÁGUA:\\n[estratégias práticas e realistas]"
                        )
                        res = nutri_ia(prompt)
                        salvar_receita("Hidratação", f"{meta_agua:.1f}L", res)
                        st.session_state['nutrint_hidra'] = res

                if st.session_state.get('nutrint_hidra'):
                    st.markdown(f"<div class='card-blue'>{st.session_state['nutrint_hidra']}</div>", unsafe_allow_html=True)

    # --- RODAPÉ ---
    st.markdown(
        "<div style='text-align:center;color:#999;font-size:0.8em;margin-top:60px;'>"
        "© 2026 NutriMind AI — Nutricionista, Chef e Coach em um só lugar · MeusAgentesIA.com.br"
        "</div>", unsafe_allow_html=True
    )

# --- RODAPÉ ---
st.markdown(
    "<div style='text-align:center;color:#999;font-size:0.8em;margin-top:60px;'>"
    "</div>", unsafe_allow_html=True
)
""",
    "personal_trainer": """# [hub] import streamlit as st
# [hub] from groq import Groq
# [hub] from datetime import datetime
# [hub] import json

# --- CONFIGURAÇÃO DA PÁGINA ---
# set_page_config removido pelo super_agente

st.markdown(\"\"\"
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
[data-testid="stToolbar"] {visibility: hidden;}
[data-testid="stDecoration"] {visibility: hidden;}
[data-testid="stStatusWidget"] {visibility: hidden;}
</style>
\"\"\", unsafe_allow_html=True)


# --- ESTILO CSS ---
st.markdown(\"\"\"
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    .stApp { background-color:#F8F9FA; font-family:'Inter',sans-serif; }
    [data-testid="stSidebar"] { display:none; }

    .stTextInput>div>div>input, .stTextArea>div>textarea,
    .stSelectbox>div>div>div, .stNumberInput>div>div>input {
        background-color:#FFFFFF !important; color:#1A1A2E !important;
        border:1px solid #CED4DA !important; font-family:'Inter',sans-serif !important;
    }

    .stButton>button {
        width:100%; border-radius:10px; height:3.2em;
        background:linear-gradient(135deg,#495057,#343A40) !important; color:white !important;
        font-weight:600; border:none; box-shadow:2px 2px 8px rgba(0,0,0,0.1);
        font-family:'Inter',sans-serif !important; transition:all 0.2s ease;
    }
    .stButton>button:hover { background:linear-gradient(135deg,#343A40,#212529) !important; transform:translateY(-1px); }
    .stApp .stButton>button, .stApp .stButton>button p,
    .stApp .stButton>button span, .stApp .stButton>button div { color:white !important; }

    .stApp h1, .stApp h2, .stApp h3 { color:#1A1A2E !important; font-family:'Inter',sans-serif !important; font-weight:700 !important; }

    .card { background:linear-gradient(135deg,#F1F3F5,#E9ECEF); padding:20px; border-radius:14px; border:1px solid #CED4DA; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card, .stApp .card p, .stApp .card span, .stApp .card div, .stApp .card strong, .stApp .card em { color:#1A1A2E !important; }

    .card-dark { background:linear-gradient(135deg,#E9ECEF,#DEE2E6); padding:20px; border-radius:14px; border:1px solid #ADB5BD; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-dark, .stApp .card-dark p, .stApp .card-dark span, .stApp .card-dark div, .stApp .card-dark strong { color:#1A1A2E !important; }

    .card-green { background:linear-gradient(135deg,#F0FDF4,#DCFCE7); padding:20px; border-radius:14px; border:1px solid #86EFAC; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-green, .stApp .card-green p, .stApp .card-green span, .stApp .card-green div { color:#14532D !important; }

    .card-blue { background:linear-gradient(135deg,#EFF6FF,#DBEAFE); padding:20px; border-radius:14px; border:1px solid #93C5FD; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-blue, .stApp .card-blue p, .stApp .card-blue span, .stApp .card-blue div { color:#1E3A8A !important; }

    .card-red { background:linear-gradient(135deg,#FFF5F5,#FEE2E2); padding:20px; border-radius:14px; border:1px solid #FECACA; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-red, .stApp .card-red p, .stApp .card-red span, .stApp .card-red div { color:#7F1D1D !important; }

    .card-yellow { background:linear-gradient(135deg,#FFFBEB,#FEF3C7); padding:18px; border-radius:12px; border:1px solid #FCD34D; margin-bottom:12px; white-space:normal; word-wrap:break-word; }
    .stApp .card-yellow, .stApp .card-yellow p, .stApp .card-yellow span, .stApp .card-yellow div { color:#78350F !important; }

    .stat-box { background:#FFFFFF; border-radius:12px; padding:16px; text-align:center; border:1px solid #CED4DA; }
    .stApp .stat-box div, .stApp .stat-box span, .stApp .stat-box p { color:#1A1A2E !important; }
    .stApp .stat-numero, .stat-numero { font-size:2em; font-weight:700; color:#495057 !important; }

    .hist-item { background:#FFFFFF; border-radius:10px; padding:12px 16px; margin-bottom:8px; border-left:4px solid #CED4DA; }
    .stApp .hist-item, .stApp .hist-item p, .stApp .hist-item span, .stApp .hist-item div, .stApp .hist-item small { color:#1A1A2E !important; }

    .badge { background:#495057; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-verde { background:#059669; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-amarelo { background:#B45309; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-azul { background:#1D4ED8; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-roxo { background:#6D28D9; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }

    .divider { border:none; height:1px; background:linear-gradient(to right,transparent,#CED4DA,transparent); margin:18px 0; }

    .chat-user { background:#FFFFFF; border:1px solid #CED4DA; border-radius:12px 12px 4px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-user, .stApp .chat-user p, .stApp .chat-user span, .stApp .chat-user div { color:#1A1A2E !important; }

    .chat-persona { background:#F8F9FA; border:1px solid #CED4DA; border-radius:4px 12px 12px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-persona, .stApp .chat-persona p, .stApp .chat-persona span, .stApp .chat-persona div { color:#1A1A2E !important; }

    .questao-box { background:#FFFFFF; border:2px solid #CED4DA; border-radius:12px; padding:18px; margin-bottom:14px; }
    .stApp .questao-box, .stApp .questao-box p, .stApp .questao-box span, .stApp .questao-box div { color:#1A1A2E !important; }

    .avaliacao-box { background:#FFFFFF; border:2px solid #CED4DA; border-radius:14px; padding:18px; margin-bottom:12px; }
    .stApp .avaliacao-box, .stApp .avaliacao-box p, .stApp .avaliacao-box span, .stApp .avaliacao-box div { color:#1A1A2E !important; }

    .meta-box { background:#FFFFFF; border:2px solid #CED4DA; border-radius:12px; padding:16px; text-align:center; margin:10px 0; }
    .stApp .meta-box, .stApp .meta-box div, .stApp .meta-box span { color:#1A1A2E !important; }
    .stApp .meta-numero { font-size:2em; font-weight:700; color:#495057 !important; }

    .chat-scroll-container { max-height:40vh; overflow-y:auto; display:flex; flex-direction:column; scroll-behavior:smooth; padding-bottom:4px; }
    .chat-scroll-container > * { flex-shrink:0; }
    

    </style>
\"\"\", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CACHE
# ─────────────────────────────────────────────
@st.cache_resource
def get_cache_personal():
    return {"perfis": {}}

_cache = get_cache_personal()

# ─────────────────────────────────────────────
# PERSISTÊNCIA LOCAL (JSON)
# ─────────────────────────────────────────────
CHAVES_SALVAR = [
    'usuario', 'historico_treinos', 'treinos_salvos',
    'objetivo_treino', 'local_treino', 'nivel_treino',
    'dias_semana', 'limitacoes', 'tempo_treino',
    'peso', 'altura', 'treinos_realizados',
]

def gerar_json_sessao() -> str:
    dados = {k: st.session_state.get(k) for k in CHAVES_SALVAR}
    dados['salvo_em'] = datetime.now().strftime('%d/%m/%Y %H:%M')
    return json.dumps(dados, ensure_ascii=False, indent=2, default=str)

def carregar_json_sessao(dados):
    _bloq = {'api_key','etapa','nome_login','chave_login','upload_login','btn_entrar_login'}
    _pref = (
        'btn_','sel_','ul_','dl_','cad_','_sub','_sm','_tab','_bsc',
        'ativo_','rem_','sel_pet_','ev_','prof_','hig_','prev_',
        'vac_','sint_','comp_','trad_','subs_','amb_','viag_','chat_',
        'duvida_','emerg_','peso_','data_','obs_','tipo_','vet_','desc_',
        'local_','prox_','alim','sit_emerg_','tc_','oraf','siau','agmag',
        'lv','mv','pt','pi','sh','wc','rv','rp','rc',
    )
    import re as _re
    for k, v in dados.items():
        if k in _bloq: continue
        if any(k.startswith(p) for p in _pref): continue
        if _re.match(r'.+_\\d+$', k): continue
        st.session_state[k] = v

def salvar_perfil_cache(usuario: str):
    _cache["perfis"][usuario] = {k: st.session_state.get(k) for k in CHAVES_SALVAR}

def perfis_salvos() -> list:
    return list(_cache["perfis"].keys())

def carregar_perfil_cache(usuario: str) -> dict | None:
    return _cache["perfis"].get(usuario)

def salvar_treino(tipo: str, foco: str, conteudo: str):
    st.session_state.historico_treinos.append({
        'data':    datetime.now().strftime('%d/%m %H:%M'),
        'tipo':    tipo,
        'foco':    foco,
        'conteudo': conteudo,
    })

# --- INICIALIZAÇÃO DE ESTADO ---
defaults = {
    'etapa':            "Login",
    'usuario':          "",
    'api_key':          "",
    'pagina':           "Home",
    'historico_treinos':[],
    'treinos_salvos':   [],
    'objetivo_treino':  "Emagrecer",
    'local_treino':     "Academia",
    'nivel_treino':     "Iniciante",
    'dias_semana':      3,
    'limitacoes':       "",
    'tempo_treino':     "60 minutos",
    'peso':             "",
    'altura':           "",
    'treinos_realizados': 0,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# --- MOTOR DE IA ---
def personal_ia(prompt: str, system_extra: str = "") -> str:
    try:
        client = Groq(api_key=st.session_state.api_key)
        system = f\"\"\"Você é um Personal Trainer profissional especialista em treinamento físico. REGRA DE OURO — CONFIABILIDADE 100%%: Forneça APENAS informações que você tem certeza absoluta que são verdadeiras. JAMAIS invente, suponha, extrapole ou preencha lacunas com dados fictícios. Se não souber algo com certeza — preço, endereço, horário, nome, estatística, lei, fato — diga EXPLICITAMENTE: 'Não tenho certeza sobre isso, recomendo verificar em [fonte].' É melhor uma resposta incompleta e honesta do que uma resposta completa e inventada. O usuário depende dessas informações para tomar decisões reais.
Usuário: {st.session_state.usuario}.
Objetivo: {st.session_state.objetivo_treino}.
Local de treino: {st.session_state.local_treino}.
Nível: {st.session_state.nivel_treino}.
Limitações físicas: {st.session_state.limitacoes or 'nenhuma'}.
Tempo disponível: {st.session_state.tempo_treino}.
{system_extra}
REGRAS:
- Sempre indique séries, repetições e tempo de descanso
- Adapte ao nível e limitações do usuário
- Explique brevemente como executar cada exercício
- Use emojis para deixar visual e motivador
- Escreva em português brasileiro\"\"\"
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system},
                {"role": "user",   "content": prompt},
            ],
            model="openai/gpt-oss-120b",
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Erro na API: {e}"

# --- BARRA DE SALVAR ---
def barra_salvar():
    salvar_perfil_cache(st.session_state.usuario)
    nome_usuario = st.session_state.usuario.lower().replace(' ', '_') or 'minha_sessao'
    total  = len(st.session_state.historico_treinos)
    salvos = len(st.session_state.treinos_salvos)
    realizados = st.session_state.treinos_realizados

    col_info, col_btn = st.columns([4, 2])
    with col_info:
        st.markdown(
            f"<div style='background:#FFF1F2;border:1px solid #FDA4AF;border-radius:10px;"
            f"padding:10px 14px;font-size:0.84em;color:#1A1A2E;line-height:1.6;'>"
            f"💾 <strong>Antes de sair, salve seus dados no computador.</strong><br>"
            f"<span style='color:#888;font-size:0.88em;'>{total} treinos gerados · "
            f"{realizados} treinos concluídos · {salvos} salvos</span>"
            f"</div>",
            unsafe_allow_html=True
        )
    with col_btn:
        st.download_button(
            label="💾 SALVAR MEUS DADOS (.json)",
            data=gerar_json_sessao(),
            file_name=f"personal_trainer_{nome_usuario}.json",
            mime="application/json",
            use_container_width=True,
            key="pt50"
        )
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown(\"\"\"<style>
    .dica-nav{font-size:0.72em;color:#94A3B8;text-align:center;padding:2px 0 6px;}
    .dica-mobile{display:none;}
    .dica-desktop{display:block;}
    @media(max-width:768px){.dica-mobile{display:block;}.dica-desktop{display:none;}}
    </style>
    <div class='dica-nav dica-mobile'>👆 Deslize o dedo para navegar entre as abas</div>
    <div class='dica-nav dica-desktop'>📋 Clique no ícone acima para abrir o menu completo</div>
    \"\"\", unsafe_allow_html=True)

# ============================================================
# TELA: LOGIN
# ============================================================
if 'altura' not in st.session_state: st.session_state['altura'] = None
if 'dias_semana' not in st.session_state: st.session_state['dias_semana'] = 0
if 'historico_treinos' not in st.session_state: st.session_state['historico_treinos'] = []
if 'limitacoes' not in st.session_state: st.session_state['limitacoes'] = None
if 'local_treino' not in st.session_state: st.session_state['local_treino'] = None
if 'nivel_treino' not in st.session_state: st.session_state['nivel_treino'] = None
if 'objetivo_treino' not in st.session_state: st.session_state['objetivo_treino'] = None
if 'peso' not in st.session_state: st.session_state['peso'] = None
if 'tempo_treino' not in st.session_state: st.session_state['tempo_treino'] = None
if 'treinos_realizados' not in st.session_state: st.session_state['treinos_realizados'] = None
if 'treinos_salvos' not in st.session_state: st.session_state['treinos_salvos'] = None

if st.session_state.etapa == "Login":
    st.markdown("# 🤖 PERSONAL TRAINER IA")
    st.markdown("<div class=\\'card\\'><b>🔒 ACESSO RESTRITO A CLIENTES DO MEUSAGENTESIA.COM.BR</b><br>🔗 <a href='https://meusagentesia.com.br' target='_blank' style='color:#4F46E5;font-weight:700;text-decoration:underline;'>meusagentesia.com.br</a></div>", unsafe_allow_html=True)
    st.info("💻 **Dica:** Pela complexidade dos agentes, no computador a experiência é mais agradável.")
    with st.container():
        nome  = st.text_input("Seu Nome:", key="nome_login")
        chave = st.text_input("🔑 Sua Chave API da Groq:", type="password", key="chave_login")
        if st.button("✨ ENTRAR", key="btn_entrar_login"):
            if len(nome.strip()) < 2:
                st.warning("Digite um nome com pelo menos 2 caracteres.")
            elif chave.strip():
                st.session_state.usuario = nome.strip()
                st.session_state.api_key = chave
                st.session_state.etapa = "App"
                st.rerun()
            else:
                st.warning("Preencha nome e chave API.")

elif st.session_state.etapa == "App":



    # TABS — navegação nativa
    (_tab_Home, _tab_TreinoDia, _tab_Semana, _tab_Casa, _tab_Evolucao, _tab_Alongamento, _tab_Salvos, _tab_Progresso, _tab_Anamnese, _tab_Suplementacao, _tab_Fadiga, _tab_Macros, _tab_Recuperacao, _tab_Mental, _tab_Biblioteca, _tab_Desafio) = st.tabs(['🏠 Painel', '💪 Treino do Dia', '📅 Semana', '🏡 Treino Casa', '📈 Progressão', '🧘 Alongamento', '❤️ Salvos', '📊 Progresso', '📋 Anamnese', '💊 Suplementação', '🔥 Energia', '🍽️ Macros', '😴 Recuperação', '🧠 Mentalidade', '📚 Biblioteca', '🏆 Desafio'])

    # ── BARRA SALVAR — aparece em todas as abas ──
    with st.expander("💾 Salvar / Carregar meus dados", expanded=False):
        _bsc1, _bsc2 = st.columns(2)
        with _bsc1:
            import json as _jsv
            _dsv = {k: st.session_state.get(k) for k in list(st.session_state.keys()) if not k.startswith('_') and k not in ('api_key',)}
    with _tab_Home:
        col_u, col_r = st.columns([3, 1])
        with col_u:
            st.title(f"Bora treinar, {st.session_state.usuario}! 💪")
            st.markdown("<span class='badge'>Modo Personal</span>", unsafe_allow_html=True)
        with col_r:
            if st.button("🚪 Sair", key="personal3"):
                for k in list(st.session_state.keys()):
                    del st.session_state[k]
                st.rerun()

        # AVISO SE DADOS SUMIRAM
        if len(st.session_state.historico_treinos) == 0 and st.session_state.treinos_realizados == 0:
            st.markdown(\"\"\"<div style="background:#FEF3C7;border:2px solid #F59E0B;border-radius:12px;
            padding:12px 18px;margin-bottom:4px;color:#000;font-size:0.9em;font-weight:600;">
            ⚠️ Seus dados não estão mais no servidor.
            </div>\"\"\", unsafe_allow_html=True)
        # PERFIL DO ATLETA
        st.markdown("#### ⚙️ Seu perfil de treino")
        col_a, col_b = st.columns(2)
        with col_a:
            st.session_state.objetivo_treino = st.selectbox(
                "Objetivo:", ["Emagrecer","Ganhar massa","Definir","Condicionamento físico","Saúde e bem-estar","Reabilitação"],
                index=["Emagrecer","Ganhar massa","Definir","Condicionamento físico","Saúde e bem-estar","Reabilitação"].index(
                    st.session_state.objetivo_treino) if st.session_state.objetivo_treino in
                    ["Emagrecer","Ganhar massa","Definir","Condicionamento físico","Saúde e bem-estar","Reabilitação"] else 0, key="pt49")
            st.session_state.local_treino = st.selectbox(
                "Onde treina:", ["Academia","Casa com equipamentos","Casa sem equipamentos","Ar livre","Misto"],
                index=["Academia","Casa com equipamentos","Casa sem equipamentos","Ar livre","Misto"].index(
                    st.session_state.local_treino) if st.session_state.local_treino in
                    ["Academia","Casa com equipamentos","Casa sem equipamentos","Ar livre","Misto"] else 0, key="pt48")
            st.session_state.nivel_treino = st.selectbox(
                "Nível:", ["Iniciante","Intermediário","Avançado"],
                index=["Iniciante","Intermediário","Avançado"].index(
                    st.session_state.nivel_treino) if st.session_state.nivel_treino in
                    ["Iniciante","Intermediário","Avançado"] else 0, key="pt47")
        with col_b:
            st.session_state.dias_semana  = st.slider("Dias por semana:", 1, 7, st.session_state.dias_semana, key="personal1")
            st.session_state.tempo_treino = st.selectbox(
                "Tempo por treino:", ["30 minutos","45 minutos","60 minutos","90 minutos","2 horas"],
                index=["30 minutos","45 minutos","60 minutos","90 minutos","2 horas"].index(
                    st.session_state.tempo_treino) if st.session_state.tempo_treino in
                    ["30 minutos","45 minutos","60 minutos","90 minutos","2 horas"] else 2, key="pt46")
            st.session_state.limitacoes   = st.text_input(
                "Limitações físicas:", value=st.session_state.limitacoes,
                placeholder="ex: dor no joelho, hérnia de disco, ombro operado...", key="pt45")
            col_p, col_a2 = st.columns(2)
            with col_p:
                st.session_state.peso   = st.text_input("Peso (kg):", value=st.session_state.peso, placeholder="ex: 75", key="personal4")
            with col_a2:
                st.session_state.altura = st.text_input("Altura (cm):", value=st.session_state.altura, placeholder="ex: 170", key="personal5")


        # IMC rápido
        try:
            peso_f   = float(st.session_state.peso.replace(',','.'))
            altura_f = float(st.session_state.altura.replace(',','.')) / 100
            imc      = round(peso_f / (altura_f ** 2), 1)
            if imc < 18.5:    cat_imc = "Abaixo do peso"
            elif imc < 25:    cat_imc = "Peso normal ✅"
            elif imc < 30:    cat_imc = "Sobrepeso"
            else:             cat_imc = "Obesidade"
        except:
            imc, cat_imc = None, None

        # MÉTRICAS
        total      = len(st.session_state.historico_treinos)
        realizados = st.session_state.treinos_realizados
        salvos     = len(st.session_state.treinos_salvos)

        c1, c2, c3, c4, c5 = st.columns(5)
        c1.markdown(f"<div class='stat-box'><div class='stat-numero'>{total}</div><div>Treinos gerados</div></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='stat-box'><div class='stat-numero'>{realizados}</div><div>Treinos concluídos</div></div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='stat-box'><div class='stat-numero'>{salvos}</div><div>Treinos salvos</div></div>", unsafe_allow_html=True)
        c4.markdown(f"<div class='stat-box'><div class='stat-numero'>{st.session_state.dias_semana}x</div><div>Dias/semana</div></div>", unsafe_allow_html=True)
        c5.markdown(f"<div class='stat-box'><div class='stat-numero'>{imc or '--'}</div><div>IMC {('· ' + cat_imc) if cat_imc else ''}</div></div>", unsafe_allow_html=True)

        st.markdown("<div class='card'>💡 <em>'O melhor treino é o que você consegue fazer com consistência. Não o mais difícil — o mais regular.'</em></div>", unsafe_allow_html=True)

        st.markdown("### 🗺️ O que cada aba faz")
        guia = {
            "💪 Treino do Dia":        "Gera o treino completo do dia com exercícios, séries, repetições e descanso",
            "📅 Planilha da Semana":   "Planilha completa de treinos para a semana — cada dia com foco diferente",
            "🏠 Treino em Casa":       "Treinos sem equipamento — só com o peso do corpo, em qualquer espaço",
            "📈 Progressão de Cargas": "Como aumentar a intensidade semana a semana para continuar evoluindo",
            "🧘 Aquecimento/Alongamento": "Aquecimento antes e alongamento depois — específico para cada treino",
            "❤️ Treinos Salvos":       "Seus treinos favoritos organizados e prontos para usar",
            "📊 Progresso":            "Histórico completo de todos os treinos gerados",
        }
        for aba, desc in guia.items():
            st.markdown(f"**{aba}** — {desc}")

        if st.session_state.historico_treinos:
            st.markdown("### 🕐 Últimos Treinos")
            for item in reversed(st.session_state.historico_treinos[-4:]):
                st.markdown(
                    f"<div class='hist-item'>"
                    f"<span class='badge'>{item['tipo']}</span> "
                    f"<span class='badge-laranja'>{item.get('foco', '')}</span> "
                    f"<small style='color:#888'>{item['data']}</small></div>",
                    unsafe_allow_html=True
                )

        # ========================
        # TREINO DO DIA
        # ========================

        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        st.markdown("### 💾 Salvar e Carregar Dados")
        _csl1, _csl2 = st.columns(2)
        with _csl1:
            import json as _json_sv
            _dados_sv = {k: st.session_state.get(k) for k in list(st.session_state.keys()) if not k.startswith('_')}
    with _tab_TreinoDia:
        st.header("💪 Treino do Dia")
        st.markdown("Treino completo personalizado — exercícios, séries, repetições e como executar.")

        col1, col2 = st.columns(2)
        with col1:
            foco_dia   = st.selectbox("🎯 Foco de hoje:", [
                "Peito e Tríceps", "Costas e Bíceps", "Pernas e Glúteos",
                "Ombros e Trapézio", "Abdômen e Core", "Corpo inteiro (Full Body)",
                "Cardio e Queima de Gordura", "Funcional", "Livre (IA decide pelo objetivo)",
            ], key="pt44")
            local_d    = st.selectbox("📍 Local:", ["Academia","Casa com equipamentos","Casa sem equipamentos","Ar livre"],
                index=["Academia","Casa com equipamentos","Casa sem equipamentos","Ar livre"].index(
                    st.session_state.local_treino) if st.session_state.local_treino in
                    ["Academia","Casa com equipamentos","Casa sem equipamentos","Ar livre"] else 0, key="pt43")
        with col2:
            nivel_d    = st.selectbox("📊 Nível:", ["Iniciante","Intermediário","Avançado"],
                index=["Iniciante","Intermediário","Avançado"].index(
                    st.session_state.nivel_treino) if st.session_state.nivel_treino in
                    ["Iniciante","Intermediário","Avançado"] else 0, key="pt42")
            tempo_d    = st.selectbox("⏱️ Tempo:", ["30 minutos","45 minutos","60 minutos","90 minutos"],
                index=["30 minutos","45 minutos","60 minutos","90 minutos"].index(
                    st.session_state.tempo_treino) if st.session_state.tempo_treino in
                    ["30 minutos","45 minutos","60 minutos","90 minutos"] else 2, key="pt41")
            limitacoes_d = st.text_input("⚠️ Limitações:", value=st.session_state.limitacoes,
                placeholder="ex: joelho, lombar...", key="pt40")

        if st.button("💪 GERAR TREINO DO DIA", key="personal6"):
            with st.spinner("Seu personal montando o treino..."):
                prompt = (
                    f"Monte um treino completo do dia.\\n"
                    f"Foco: {foco_dia}. Local: {local_d}. Nível: {nivel_d}.\\n"
                    f"Tempo: {tempo_d}. Objetivo: {st.session_state.objetivo_treino}.\\n"
                    f"Limitações: {limitacoes_d or 'nenhuma'}.\\n\\n"
                    f"FORMATO OBRIGATÓRIO:\\n\\n"
                    f"💪 TREINO DE {foco_dia.upper()}\\n"
                    f"Nível: {nivel_d} | Local: {local_d} | Tempo: {tempo_d}\\n\\n"
                    f"🔥 AQUECIMENTO (5-10 min):\\n"
                    f"[3-4 exercícios de aquecimento específicos para esse foco]\\n\\n"
                    f"📋 TREINO PRINCIPAL:\\n\\n"
                    f"Para cada exercício use este formato:\\n"
                    f"[NÚMERO]. [NOME DO EXERCÍCIO] 💪\\n"
                    f"   • Séries: [X] | Repetições: [X] | Descanso: [X] segundos\\n"
                    f"   • Como executar: [instrução clara em 2 linhas]\\n"
                    f"   • Dica: [erro mais comum e como evitar]\\n\\n"
                    f"[Mínimo 6 exercícios para o foco principal]\\n\\n"
                    f"🧘 VOLTA À CALMA (5 min):\\n"
                    f"[3-4 alongamentos específicos para os músculos trabalhados]\\n\\n"
                    f"📊 RESUMO DO TREINO:\\n"
                    f"Total de exercícios: [X]\\n"
                    f"Volume total (séries x rep): [X]\\n"
                    f"Calorias estimadas: [X] cal\\n"
                    f"Músculos trabalhados: [lista]\\n\\n"
                    f"💡 DICA DO PERSONAL:\\n"
                    f"[1 dica específica para maximizar esse treino]\\n\\n"
                    f"⚡ PRÓXIMO TREINO SUGERIDO:\\n"
                    f"[O que trabalhar na próxima sessão para equilíbrio muscular]"
                )
                res = personal_ia(prompt)
                if res: st.session_state['res_treinodia_person1'] = str(res)
                salvar_treino("Treino do Dia", foco_dia, res)
                st.session_state['treino_dia_temp'] = res
                st.markdown(f"<div class='card'>{res}</div>", unsafe_allow_html=True)

        if st.session_state.get('treino_dia_temp'):
            col_dl, col_sv, col_ok = st.columns(3)
            with col_dl:
                st.download_button("📋 Baixar treino (.txt)",
                    data=st.session_state['treino_dia_temp'],
                    file_name=f"treino_{foco_dia.replace(' ','_') if 'foco_dia' in dir() else 'dia'}.txt",
                    mime="text/plain", use_container_width=True, key="pt39")
            with col_sv:
                if st.button("❤️ Salvar treino", use_container_width=True, key="personal7"):
                    st.session_state.treinos_salvos.append({
                        'tipo': 'Treino do Dia', 'foco': foco_dia if 'foco_dia' in dir() else '',
                        'conteudo': st.session_state['treino_dia_temp'],
                        'data': datetime.now().strftime('%d/%m %H:%M'),
                    })
                    st.success("❤️ Salvo!")
            with col_ok:
                if st.button("✅ Treino concluído!", use_container_width=True, key="personal8"):
                    st.session_state.treinos_realizados += 1
                    st.success(f"🎉 Parabéns! {st.session_state.treinos_realizados} treinos no total!")
                    st.rerun()

        # ========================
        # PLANILHA DA SEMANA
        # ========================

    with _tab_Semana:
        st.header("📅 Planilha de Treino Semanal")
        st.markdown("Planilha completa para a semana — cada dia com foco e objetivo diferentes.")

        col1, col2 = st.columns(2)
        with col1:
            dias_s   = st.slider("Dias de treino na semana:", 2, 6, st.session_state.dias_semana, key="personal2")
            local_s  = st.selectbox("Local:", ["Academia","Casa com equipamentos","Casa sem equipamentos","Misto"],
                index=0, key="pt38")
            nivel_s  = st.selectbox("Nível:", ["Iniciante","Intermediário","Avançado"],
                index=["Iniciante","Intermediário","Avançado"].index(
                    st.session_state.nivel_treino) if st.session_state.nivel_treino in
                    ["Iniciante","Intermediário","Avançado"] else 0, key="pt37")
        with col2:
            objetivo_s   = st.selectbox("Objetivo principal:", [
                "Emagrecer","Ganhar massa","Definir","Condicionamento","Saúde geral"],
                index=["Emagrecer","Ganhar massa","Definir","Condicionamento","Saúde geral"].index(
                    st.session_state.objetivo_treino) if st.session_state.objetivo_treino in
                    ["Emagrecer","Ganhar massa","Definir","Condicionamento","Saúde geral"] else 0, key="pt36")
            tempo_s      = st.selectbox("Tempo por treino:", ["30 minutos","45 minutos","60 minutos","90 minutos"],
                index=2, key="pt35")
            limitacoes_s = st.text_input("Limitações:", value=st.session_state.limitacoes, key="personal9")

        if st.button("📅 GERAR PLANILHA DA SEMANA", key="personal10"):
            with st.spinner("Montando sua planilha semanal..."):
                prompt = (
                    f"Monte uma planilha de treino para {dias_s} dias na semana.\\n"
                    f"Objetivo: {objetivo_s}. Local: {local_s}. Nível: {nivel_s}.\\n"
                    f"Tempo por sessão: {tempo_s}. Limitações: {limitacoes_s or 'nenhuma'}.\\n\\n"
                    f"ESTRUTURA:\\n\\n"
                    f"📅 PLANILHA SEMANAL — {objetivo_s.upper()}\\n"
                    f"{dias_s} dias de treino · {tempo_s} por sessão · {nivel_s}\\n\\n"
                    f"Para cada dia de treino use:\\n\\n"
                    f"━━━━━━━━━━━━━━━━━━━━━\\n"
                    f"💪 DIA [N] — [GRUPO MUSCULAR / FOCO]\\n"
                    f"━━━━━━━━━━━━━━━━━━━━━\\n"
                    f"Exercício 1: [nome] — [X] séries x [X] rep — descanso [X]s\\n"
                    f"Exercício 2: [nome] — [X] séries x [X] rep — descanso [X]s\\n"
                    f"Exercício 3: [nome] — [X] séries x [X] rep — descanso [X]s\\n"
                    f"Exercício 4: [nome] — [X] séries x [X] rep — descanso [X]s\\n"
                    f"Exercício 5: [nome] — [X] séries x [X] rep — descanso [X]s\\n"
                    f"🔥 Finalizador: [exercício cardio/metabólico]\\n\\n"
                    f"[Para os dias de descanso: indique recuperação ativa]\\n\\n"
                    f"📊 VISÃO GERAL DA SEMANA:\\n"
                    f"[Tabela resumida: Dia | Foco | Volume | Intensidade]\\n\\n"
                    f"📈 PROGRESSÃO NAS PRÓXIMAS SEMANAS:\\n"
                    f"Semana 2: [como aumentar]\\n"
                    f"Semana 3: [como aumentar]\\n"
                    f"Semana 4: [deload — semana de recuperação]\\n\\n"
                    f"💡 DICA DA SEMANA:\\n"
                    f"[1 estratégia para maximizar os resultados dessa divisão]"
                )
                res = personal_ia(prompt)
                if res: st.session_state['res_semana_person2'] = str(res)
                salvar_treino("Planilha Semanal", f"{dias_s} dias", res)
                st.session_state['semana_temp'] = res
                st.markdown(f"<div class='card-dark'>{res}</div>", unsafe_allow_html=True)

        if st.session_state.get('semana_temp'):
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar planilha (.txt)",
                    data=st.session_state['semana_temp'],
                    file_name="planilha_semanal.txt", mime="text/plain", use_container_width=True, key="pt34")
            with col_sv:
                if st.button("❤️ Salvar planilha", key="sv_sem", use_container_width=True):
                    st.session_state.treinos_salvos.append({
                        'tipo': 'Planilha Semanal',
                        'foco': f"{dias_s} dias — {objetivo_s}",
                        'conteudo': st.session_state['semana_temp'],
                        'data': datetime.now().strftime('%d/%m %H:%M'),
                    })
                    st.success("❤️ Salvo!")

        # ========================
        # TREINO EM CASA
        # ========================

    with _tab_Casa:
        st.header("🏠 Treino em Casa")
        st.markdown("Sem academia, sem desculpa — treinos com o peso do corpo em qualquer espaço.")

        col1, col2 = st.columns(2)
        with col1:
            foco_casa    = st.selectbox("Foco:", [
                "Corpo inteiro (Full Body)","Pernas e Glúteos","Abdômen e Core",
                "Peito e Braços","Cardio e Queima de Gordura","Funcional","Yoga e Mobilidade",
            ], key="pt33")
            espaco       = st.selectbox("Espaço disponível:", [
                "Sala/quarto pequeno (2x2m)","Sala maior (3x3m+)","Quintal/área externa","Qualquer espaço",
            ], key="pt32")
        with col2:
            equipamentos = st.multiselect("Equipamentos que tem em casa:", [
                "Nenhum (só peso do corpo)","Halteres","Elásticos/faixas","Barra fixa",
                "Corda de pular","Banco/cadeira","Garrafa d'água como peso",
            ], default=["Nenhum (só peso do corpo)"], key="pt31")
            nivel_c      = st.selectbox("Nível:", ["Iniciante","Intermediário","Avançado"],
                index=["Iniciante","Intermediário","Avançado"].index(
                    st.session_state.nivel_treino) if st.session_state.nivel_treino in
                    ["Iniciante","Intermediário","Avançado"] else 0, key="pt30")
            tempo_c      = st.selectbox("Tempo:", ["20 minutos","30 minutos","45 minutos","60 minutos"], key="personal11")

        if st.button("🏠 GERAR TREINO EM CASA", key="personal12"):
            with st.spinner("Montando treino em casa..."):
                equip = ", ".join(equipamentos) if equipamentos else "só peso do corpo"
                prompt = (
                    f"Monte um treino em casa completo.\\n"
                    f"Foco: {foco_casa}. Espaço: {espaco}. Equipamentos: {equip}.\\n"
                    f"Nível: {nivel_c}. Tempo: {tempo_c}. Objetivo: {st.session_state.objetivo_treino}.\\n"
                    f"Limitações: {st.session_state.limitacoes or 'nenhuma'}.\\n\\n"
                    f"FORMATO:\\n\\n"
                    f"🏠 TREINO EM CASA — {foco_casa.upper()}\\n"
                    f"Sem academia · {equip} · {tempo_c}\\n\\n"
                    f"🔥 AQUECIMENTO (3-5 min):\\n"
                    f"[Aquecimento sem equipamento, em espaço pequeno]\\n\\n"
                    f"💪 CIRCUITO PRINCIPAL:\\n"
                    f"[Organize em blocos/circuitos de 3-4 exercícios]\\n\\n"
                    f"BLOCO 1 — [nome do bloco]:\\n"
                    f"• [Exercício 1]: [X] séries x [X] rep (ou [X] segundos)\\n"
                    f"  Como fazer: [instrução simples]\\n"
                    f"• [Exercício 2]: ...\\n"
                    f"• [Exercício 3]: ...\\n"
                    f"Descanso entre blocos: [X] segundos\\n\\n"
                    f"[Repita para todos os blocos]\\n\\n"
                    f"🧘 ALONGAMENTO FINAL (5 min):\\n"
                    f"[Alongamentos no chão/em pé]\\n\\n"
                    f"📊 RESUMO:\\n"
                    f"Calorias estimadas: [X] cal\\n"
                    f"Músculos trabalhados: [lista]\\n\\n"
                    f"💡 VERSÃO MAIS DIFÍCIL:\\n"
                    f"[Como tornar esse treino mais intenso quando ficar fácil]\\n\\n"
                    f"📱 TIMER SUGERIDO:\\n"
                    f"[Como usar o cronômetro para esse treino — Tabata, EMOM, AMRAP...]"
                )
                res = personal_ia(prompt)
                if res: st.session_state['res_casa_person3'] = str(res)
                salvar_treino("Treino em Casa", foco_casa, res)
                st.session_state['casa_temp'] = res
                st.markdown(f"<div class='card-green'>{res}</div>", unsafe_allow_html=True)

        if st.session_state.get('casa_temp'):
            col_dl, col_sv, col_ok = st.columns(3)
            with col_dl:
                st.download_button("📋 Baixar treino (.txt)",
                    data=st.session_state['casa_temp'],
                    file_name="treino_casa.txt", mime="text/plain", use_container_width=True, key="pt29")
            with col_sv:
                if st.button("❤️ Salvar", key="sv_casa", use_container_width=True):
                    st.session_state.treinos_salvos.append({
                        'tipo': 'Treino em Casa', 'foco': foco_casa,
                        'conteudo': st.session_state['casa_temp'],
                        'data': datetime.now().strftime('%d/%m %H:%M'),
                    })
                    st.success("❤️ Salvo!")
            with col_ok:
                if st.button("✅ Concluído!", key="ok_casa", use_container_width=True):
                    st.session_state.treinos_realizados += 1
                    st.success(f"🎉 Treino {st.session_state.treinos_realizados} concluído!")
                    st.rerun()

        # ========================
        # PROGRESSÃO DE CARGAS
        # ========================

    with _tab_Evolucao:
        st.header("📈 Progressão de Cargas e Evolução")
        st.markdown("Como aumentar a intensidade semana a semana para nunca parar de evoluir.")

        col1, col2 = st.columns(2)
        with col1:
            semanas_atual= st.number_input("Há quantas semanas está treinando:", min_value=1, max_value=104, value=4, key="personal13")
            treino_atual = st.text_area("Seu treino atual (exercícios e cargas):", height=120,
                placeholder="ex: Supino reto: 3x10 com 30kg\\nAgachamento: 4x12 com 40kg\\nRosca direta: 3x12 com 10kg...", key="pt28")
        with col2:
            objetivo_e   = st.selectbox("Objetivo da progressão:", [
                "Ganhar força (menos rep, mais carga)",
                "Ganhar massa (hipertrofia)",
                "Resistência (mais rep, menos carga)",
                "Misto equilibrado",
            ], key="pt27")
            nivel_e      = st.selectbox("Nível:", ["Iniciante","Intermediário","Avançado"],
                index=["Iniciante","Intermediário","Avançado"].index(
                    st.session_state.nivel_treino) if st.session_state.nivel_treino in
                    ["Iniciante","Intermediário","Avançado"] else 0, key="pt26")

        if st.button("📈 GERAR PLANO DE PROGRESSÃO", key="personal14"):
            if treino_atual.strip():
                with st.spinner("Calculando sua progressão..."):
                    prompt = (
                        f"Crie um plano de progressão de cargas para 8 semanas.\\n"
                        f"Semanas treinando: {semanas_atual}. Nível: {nivel_e}.\\n"
                        f"Objetivo: {objetivo_e}.\\n"
                        f"Treino atual:\\n{treino_atual}\\n\\n"
                        f"ESTRUTURA:\\n\\n"
                        f"📈 PLANO DE PROGRESSÃO — 8 SEMANAS\\n"
                        f"Objetivo: {objetivo_e}\\n\\n"
                        f"📊 ANÁLISE DO TREINO ATUAL:\\n"
                        f"[Avaliação honesta do volume e intensidade atual]\\n\\n"
                        f"🗓️ PROGRESSÃO SEMANA A SEMANA:\\n\\n"
                        f"Para cada semana:\\n"
                        f"Semana [N]:\\n"
                        f"• [Exercício]: [séries]x[rep] com [carga] kg\\n"
                        f"  Mudança: [o que aumentou e por quê]\\n\\n"
                        f"[Semana 4: deload — redução de 40% do volume]\\n"
                        f"[Semana 8: teste de força máxima]\\n\\n"
                        f"📏 REGRAS DE PROGRESSÃO:\\n"
                        f"[Quando aumentar carga, quando manter, quando recuar]\\n\\n"
                        f"🚨 SINAIS DE ALERTA:\\n"
                        f"[Quando parar de progredir significa que algo está errado]\\n\\n"
                        f"💡 PERIODIZAÇÃO:\\n"
                        f"[Como organizar os ciclos após as 8 semanas]"
                    )
                    res = personal_ia(prompt)
                    if res: st.session_state['res_evolucao_person4'] = str(res)
                    salvar_treino("Progressão de Cargas", objetivo_e, res)
                    st.session_state['evolucao_temp'] = res
                    st.markdown(f"<div class='card-blue'>{res}</div>", unsafe_allow_html=True)
            else:
                st.warning("Informe seu treino atual com as cargas.")

        if st.session_state.get('evolucao_temp'):
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar plano (.txt)",
                    data=st.session_state['evolucao_temp'],
                    file_name="progressao_cargas.txt", mime="text/plain", use_container_width=True, key="pt25")
            with col_sv:
                if st.button("❤️ Salvar", key="sv_ev", use_container_width=True):
                    st.session_state.treinos_salvos.append({
                        'tipo': 'Progressão', 'foco': objetivo_e,
                        'conteudo': st.session_state['evolucao_temp'],
                        'data': datetime.now().strftime('%d/%m %H:%M'),
                    })
                    st.success("❤️ Salvo!")

        # ========================
        # AQUECIMENTO E ALONGAMENTO
        # ========================

    with _tab_Alongamento:
        st.header("🧘 Aquecimento e Alongamento")
        st.markdown("Prepare o corpo antes e recupere depois — para treinar sem lesões.")

        tab1, tab2 = st.tabs(["🔥 Aquecimento", "🧘 Alongamento"])

        with tab1:
            col1, col2 = st.columns(2)
            with col1:
                musculo_aq = st.selectbox("Grupo muscular do treino:", [
                    "Peito e Tríceps","Costas e Bíceps","Pernas e Glúteos",
                    "Ombros","Abdômen","Corpo inteiro",
                ], key="pt24")
                tempo_aq   = st.selectbox("Tempo para aquecimento:", ["5 minutos","8 minutos","10 minutos","15 minutos"], key="personal15")
            with col2:
                local_aq   = st.selectbox("Local:", ["Academia","Casa","Ar livre"], key="personal16")
                nivel_aq   = st.selectbox("Nível:", ["Iniciante","Intermediário","Avançado"],
                    index=["Iniciante","Intermediário","Avançado"].index(
                        st.session_state.nivel_treino) if st.session_state.nivel_treino in
                        ["Iniciante","Intermediário","Avançado"] else 0, key="pt23")

            if st.button("🔥 GERAR AQUECIMENTO", key="personal17"):
                with st.spinner("Preparando aquecimento..."):
                    prompt = (
                        f"Crie um protocolo de aquecimento completo para treino de {musculo_aq}.\\n"
                        f"Tempo: {tempo_aq}. Local: {local_aq}. Nível: {nivel_aq}.\\n\\n"
                        f"FORMATO:\\n\\n"
                        f"🔥 AQUECIMENTO — {musculo_aq.upper()}\\n"
                        f"Duração: {tempo_aq}\\n\\n"
                        f"FASE 1 — Ativação geral (2-3 min):\\n"
                        f"[Exercícios para elevar temperatura corporal]\\n\\n"
                        f"FASE 2 — Mobilização articular (2-3 min):\\n"
                        f"[Movimentos para as articulações envolvidas no treino]\\n\\n"
                        f"FASE 3 — Ativação específica (2-3 min):\\n"
                        f"[Exercícios leves dos músculos que vão ser treinados]\\n\\n"
                        f"Para cada exercício:\\n"
                        f"• [Nome]: [X] repetições ou [X] segundos\\n"
                        f"  Como fazer: [instrução rápida]\\n\\n"
                        f"✅ VOCÊ ESTÁ PRONTO PARA TREINAR QUANDO:\\n"
                        f"[Sinais de que o corpo está aquecido corretamente]"
                    )
                    res = personal_ia(prompt)
                    if res: st.session_state['res_alongamento_person5'] = str(res)
                    salvar_treino("Aquecimento", musculo_aq, res)
                    st.session_state['aquec_temp'] = res
                    st.markdown(f"<div class='card-orange'>{res}</div>", unsafe_allow_html=True)

            if st.session_state.get('aquec_temp'):
                st.download_button("📋 Baixar aquecimento (.txt)",
                    data=st.session_state['aquec_temp'],
                    file_name="aquecimento.txt", mime="text/plain", key="pt22")

        with tab2:
            col1, col2 = st.columns(2)
            with col1:
                musculo_al = st.selectbox("Músculo trabalhado no treino:", [
                    "Peito e Tríceps","Costas e Bíceps","Pernas e Glúteos",
                    "Ombros","Abdômen","Corpo inteiro",
                ], key="musc_al")
                tempo_al   = st.selectbox("Tempo para alongamento:", ["5 minutos","10 minutos","15 minutos","20 minutos"], key="tempo_al")
            with col2:
                objetivo_al= st.radio("Objetivo:", ["Recuperação pós-treino","Flexibilidade","Relaxamento"], horizontal=True, key="personal18")
                limitacoes_al = st.text_input("Limitações:", value=st.session_state.limitacoes, key="lim_al")

            if st.button("🧘 GERAR ALONGAMENTO", key="personal19"):
                with st.spinner("Preparando alongamento..."):
                    prompt = (
                        f"Crie um protocolo de alongamento após treino de {musculo_al}.\\n"
                        f"Tempo: {tempo_al}. Objetivo: {objetivo_al}.\\n"
                        f"Limitações: {limitacoes_al or 'nenhuma'}.\\n\\n"
                        f"FORMATO:\\n\\n"
                        f"🧘 ALONGAMENTO — {musculo_al.upper()}\\n"
                        f"Duração: {tempo_al} | Foco: {objetivo_al}\\n\\n"
                        f"Para cada alongamento:\\n"
                        f"[NÚMERO]. [NOME DO ALONGAMENTO]\\n"
                        f"   • Duração: [X] segundos por lado\\n"
                        f"   • Como fazer: [instrução clara]\\n"
                        f"   • Músculo alongado: [qual músculo]\\n"
                        f"   • Respiração: [como respirar durante]\\n\\n"
                        f"[Mínimo 6 alongamentos]\\n\\n"
                        f"💡 DICA DE RECUPERAÇÃO:\\n"
                        f"[O que mais fazer para recuperar bem após esse treino]\\n\\n"
                        f"🥤 NUTRIÇÃO PÓS-TREINO:\\n"
                        f"[O que comer/beber nas próximas 2 horas para maximizar a recuperação]"
                    )
                    res = personal_ia(prompt)
                    if res: st.session_state['res_alongamento_person6'] = str(res)
                    salvar_treino("Alongamento", musculo_al, res)
                    st.session_state['along_temp'] = res
                    st.markdown(f"<div class='card-purple'>{res}</div>", unsafe_allow_html=True)

            if st.session_state.get('along_temp'):
                st.download_button("📋 Baixar alongamento (.txt)",
                    data=st.session_state['along_temp'],
                    file_name="alongamento.txt", mime="text/plain", key="pt21")

        # ========================
        # TREINOS SALVOS
        # ========================

    with _tab_Salvos:
        st.header("❤️ Treinos Salvos")
        st.markdown("Seus treinos favoritos — organizados e prontos para usar a qualquer hora.")

        if not st.session_state.treinos_salvos:
            st.info("Nenhum treino salvo ainda. Gere treinos e salve os favoritos!")
        else:
            tipos_s = list(set(t['tipo'] for t in st.session_state.treinos_salvos))
            filtro  = st.selectbox("Filtrar por tipo:", ["Todos"] + tipos_s, key="personal20")

            treinos_f = [
                t for t in st.session_state.treinos_salvos
                if filtro == "Todos" or t['tipo'] == filtro
            ]

            st.markdown(f"**{len(treinos_f)} treino(s) encontrado(s)**")

            for i, item in enumerate(reversed(treinos_f)):
                idx_real = len(st.session_state.treinos_salvos) - 1 - i
                with st.expander(f"❤️ [{item['tipo']}] {item.get('foco', '')} — {item['data']}"):
                    st.markdown(f"<div class='card'>{item['conteudo']}</div>", unsafe_allow_html=True)
                    col_dl, col_ok, col_del = st.columns([2, 2, 1])
                    with col_dl:
                        st.download_button("📋 Baixar", data=item['conteudo'],
                            file_name=f"{item['tipo'].lower().replace(' ','_')}.txt",
                            mime="text/plain", key=f"dl_salvo_{i}")
                    with col_ok:
                        if st.button("✅ Marcar como feito", key=f"ok_salvo_{i}"):
                            st.session_state.treinos_realizados += 1
                            st.success(f"🎉 +1 treino! Total: {st.session_state.treinos_realizados}")
                            st.rerun()
                    with col_del:
                        if st.button("🗑️", key=f"del_salvo_{i}"):
                            st.session_state.treinos_salvos.pop(idx_real)
                            st.rerun()

        # ========================
        # PROGRESSO
        # ========================

    with _tab_Progresso:
        st.header("📊 Meu Progresso")

        total      = len(st.session_state.historico_treinos)
        realizados = st.session_state.treinos_realizados
        salvos     = len(st.session_state.treinos_salvos)
        tipos = {}
        for t in st.session_state.historico_treinos:
            tipos[t['tipo']] = tipos.get(t['tipo'], 0) + 1

        c1, c2, c3, c4, c5 = st.columns(5)
        c1.markdown(f"<div class='stat-box'><div class='stat-numero'>{total}</div><div>Treinos gerados</div></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='stat-box'><div class='stat-numero'>{realizados}</div><div>Treinos concluídos 🏆</div></div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='stat-box'><div class='stat-numero'>{salvos}</div><div>Treinos salvos</div></div>", unsafe_allow_html=True)
        c4.markdown(f"<div class='stat-box'><div class='stat-numero'>{tipos.get('Treino do Dia',0)}</div><div>Treinos do dia</div></div>", unsafe_allow_html=True)
        c5.markdown(f"<div class='stat-box'><div class='stat-numero'>{tipos.get('Planilha Semanal',0)}</div><div>Planilhas</div></div>", unsafe_allow_html=True)

        # Ajuste manual de treinos realizados
        with st.expander("✏️ Ajustar treinos concluídos"):
            novo_r = st.number_input("Total de treinos concluídos:", min_value=0, value=realizados, key="personal21")
            if st.button("Salvar", key="personal22"):
                st.session_state.treinos_realizados = novo_r
                st.success("✅ Atualizado!")
                st.rerun()

        if st.session_state.historico_treinos:
            col_f, col_ex = st.columns([3, 1])
            with col_f:
                filtro = st.selectbox("Filtrar:", ["Todos"] + list(tipos.keys()), key="personal23")
            with col_ex:
                hist_txt = "\\n\\n".join(
                    f"[{t['data']}] {t['tipo']} — {t['foco']}\\n{t['conteudo']}\\n{'─'*40}"
                    for t in st.session_state.historico_treinos
                )
                st.download_button("⬇️ Exportar TXT", data=hist_txt,
                    file_name="historico_treinos.txt", mime="text/plain", key="pt20")

            for i, item in enumerate(reversed(st.session_state.historico_treinos)):
                if filtro != "Todos" and item['tipo'] != filtro:
                    continue

        # ========================
        # ANAMNESE
        # ========================

    with _tab_Anamnese:
        st.header("📋 Minha Anamnese Completa")
        st.markdown("Preencha uma vez — a IA usa tudo isso em todos os módulos para personalizar cada resposta.")

        with st.form("form_anamnese"):
            st.markdown("#### 👤 Dados Básicos")
            col1, col2, col3 = st.columns(3)
            with col1:
                an_idade = st.number_input("Idade:", min_value=12, max_value=90, value=st.session_state.get('an_idade', 30), key="personal24")
                an_peso = st.number_input("Peso atual (kg):", min_value=30.0, max_value=250.0, value=st.session_state.get('an_peso', 70.0), step=0.5, key="personal25")
            with col2:
                an_altura = st.number_input("Altura (cm):", min_value=120, max_value=220, value=st.session_state.get('an_altura', 170), key="personal26")
                an_sexo = st.selectbox("Sexo biológico:", ["Masculino","Feminino"], index=0 if st.session_state.get('an_sexo','Masculino')=='Masculino' else 1, key="personal27")
            with col3:
                an_objetivo = st.selectbox("Objetivo principal:", ["Perder gordura","Ganhar massa muscular","Manutenção","Condicionamento físico","Saúde geral","Desempenho esportivo"],
                    index=["Perder gordura","Ganhar massa muscular","Manutenção","Condicionamento físico","Saúde geral","Desempenho esportivo"].index(st.session_state.get('an_objetivo','Perder gordura')), key="pt19")
                an_nivel = st.selectbox("Nível de experiência:", ["Iniciante (menos de 6 meses)","Intermediário (6m-2 anos)","Avançado (2+ anos)","Atleta"],
                    index=["Iniciante (menos de 6 meses)","Intermediário (6m-2 anos)","Avançado (2+ anos)","Atleta"].index(st.session_state.get('an_nivel','Iniciante (menos de 6 meses)')), key="pt18")

            st.markdown("#### 🏋️ Treino")
            col4, col5 = st.columns(2)
            with col4:
                an_dias = st.slider("Dias disponíveis por semana:", 1, 7, st.session_state.get('an_dias', 3), key="personal3_x2")
                an_duracao = st.selectbox("Duração por sessão:", ["30 min","45 min","60 min","75 min","90 min+"],
                    index=["30 min","45 min","60 min","75 min","90 min+"].index(st.session_state.get('an_duracao','60 min')), key="pt17")
            with col5:
                an_local = st.selectbox("Local de treino:", ["Academia completa","Academia básica","Em casa com equipamentos","Em casa sem equipamentos","Ao ar livre","Híbrido"],
                    index=["Academia completa","Academia básica","Em casa com equipamentos","Em casa sem equipamentos","Ao ar livre","Híbrido"].index(st.session_state.get('an_local','Academia completa')), key="pt16")
                an_equipamentos = st.text_input("Equipamentos disponíveis:", value=st.session_state.get('an_equipamentos',''), placeholder="ex: halteres, barra, elásticos...", key="personal28")

            st.markdown("#### 🩺 Saúde e Limitações")
            col6, col7 = st.columns(2)
            with col6:
                an_lesoes = st.text_area("Lesões ou limitações físicas:", height=80, value=st.session_state.get('an_lesoes',''), placeholder="ex: dor lombar, joelho operado, tendinite no ombro...", key="personal29")
                an_doencas = st.text_area("Condições de saúde relevantes:", height=80, value=st.session_state.get('an_doencas',''), placeholder="ex: hipertensão, diabetes, hipotireoidismo...", key="personal30")
            with col7:
                an_medicamentos = st.text_input("Medicamentos em uso:", value=st.session_state.get('an_medicamentos',''), placeholder="ex: metformina, losartana...", key="personal31")
                an_historico = st.text_area("Histórico de atividade física:", height=80, value=st.session_state.get('an_historico',''), placeholder="ex: pratiquei musculação por 2 anos, parei há 6 meses...", key="personal32")

            st.markdown("#### 🍽️ Alimentação e Rotina")
            col8, col9 = st.columns(2)
            with col8:
                an_dieta = st.selectbox("Tipo de alimentação:", ["Onívoro","Vegetariano","Vegano","Low carb","Cetogênica","Sem restrições"],
                    index=["Onívoro","Vegetariano","Vegano","Low carb","Cetogênica","Sem restrições"].index(st.session_state.get('an_dieta','Onívoro')), key="pt15")
                an_sono = st.selectbox("Horas de sono por noite:", ["Menos de 5h","5-6h","6-7h","7-8h","8h+"],
                    index=["Menos de 5h","5-6h","6-7h","7-8h","8h+"].index(st.session_state.get('an_sono','7-8h')), key="pt14")
            with col9:
                an_trabalho = st.selectbox("Nível de atividade no trabalho:", ["Sedentário (escritório)","Levemente ativo","Moderadamente ativo","Muito ativo (trabalho físico)"],
                    index=["Sedentário (escritório)","Levemente ativo","Moderadamente ativo","Muito ativo (trabalho físico)"].index(st.session_state.get('an_trabalho','Sedentário (escritório)')), key="pt13")
                an_estresse = st.selectbox("Nível de estresse geral:", ["Baixo","Moderado","Alto","Muito alto"],
                    index=["Baixo","Moderado","Alto","Muito alto"].index(st.session_state.get('an_estresse','Moderado')), key="pt12")

            an_obs = st.text_area("Outras informações importantes:", height=80, value=st.session_state.get('an_obs',''),
                placeholder="qualquer coisa que seu personal precisaria saber...", key="pt11")

            submitted = st.form_submit_button("💾 SALVAR ANAMNESE COMPLETA", key="personalfsb501")
            if submitted:
                for k, v in [('an_idade',an_idade),('an_peso',an_peso),('an_altura',an_altura),
                              ('an_sexo',an_sexo),('an_objetivo',an_objetivo),('an_nivel',an_nivel),
                              ('an_dias',an_dias),('an_duracao',an_duracao),('an_local',an_local),
                              ('an_equipamentos',an_equipamentos),('an_lesoes',an_lesoes),
                              ('an_doencas',an_doencas),('an_medicamentos',an_medicamentos),
                              ('an_historico',an_historico),('an_dieta',an_dieta),('an_sono',an_sono),
                              ('an_trabalho',an_trabalho),('an_estresse',an_estresse),('an_obs',an_obs)]:
                    st.session_state[k] = v
                st.success("✅ Anamnese salva! Todos os módulos agora usarão essas informações.")

        if st.session_state.get('an_objetivo'):
            imc = st.session_state.get('an_peso',70) / ((st.session_state.get('an_altura',170)/100)**2)
            c1,c2,c3 = st.columns(3)
            c1.markdown(f"<div class='stat-box'><div class='stat-numero'>{imc:.1f}</div><div>IMC</div></div>", unsafe_allow_html=True)
            c2.markdown(f"<div class='stat-box'><div class='stat-numero'>{st.session_state.get('an_objetivo','—')}</div><div>Objetivo</div></div>", unsafe_allow_html=True)
            c3.markdown(f"<div class='stat-box'><div class='stat-numero'>{st.session_state.get('an_nivel','—').split(' ')[0]}</div><div>Nível</div></div>", unsafe_allow_html=True)

        # ========================
        # SUPLEMENTAÇÃO
        # ========================

    with _tab_Suplementacao:
        st.header("💊 Suplementação Inteligente")

        def contexto_anamnese():
            if st.session_state.get('an_objetivo'):
                return (f"Perfil do aluno: {st.session_state.get('an_sexo','')}, {st.session_state.get('an_idade','')} anos, "
                        f"{st.session_state.get('an_peso','')}kg, objetivo: {st.session_state.get('an_objetivo','')}, "
                        f"nível: {st.session_state.get('an_nivel','')}, dieta: {st.session_state.get('an_dieta','')}, "
                        f"lesões: {st.session_state.get('an_lesoes','nenhuma')}, "
                        f"doenças: {st.session_state.get('an_doencas','nenhuma')}.")
            return "Perfil não preenchido — responda de forma geral."

        tab_s1, tab_s2, tab_s3 = st.tabs(["🎯 Recomendação Personalizada","📚 Guia de Suplementos","⚠️ O que EVITAR"])

        with tab_s1:
            col1, col2 = st.columns(2)
            with col1:
                orcamento_sup = st.selectbox("💰 Orçamento mensal:", ["Sem orçamento (só o essencial)","Até R$100","R$100-300","R$300-600","Acima de R$600"], key="personal33")
                fase_sup = st.selectbox("📊 Fase atual:", ["Perda de gordura","Ganho de massa","Manutenção","Cutting","Bulking"], key="personal34")
            with col2:
                restricoes_sup = st.multiselect("🚫 Restrições:", ["Vegano","Intolerante à lactose","Sem glúten","Alergia a soja","Sem cafeína"], key="personal4_x2")
                experiencia_sup = st.selectbox("🎓 Experiência com suplementos:", ["Nunca usei","Uso básico (só proteína)","Uso intermediário","Uso avançado"], key="personal35")

            if st.button("💊 GERAR RECOMENDAÇÃO PERSONALIZADA", key="personal36"):
                with st.spinner("Analisando seu perfil..."):
                    prompt = (
                        f"Crie uma recomendação completa e honesta de suplementação.\\n"
                        f"{contexto_anamnese()}\\n"
                        f"Orçamento: {orcamento_sup}. Fase: {fase_sup}. Restrições: {', '.join(restricoes_sup) or 'nenhuma'}. "
                        f"Experiência: {experiencia_sup}.\\n\\n"
                        f"FORMATO:\\n\\n"
                        f"💊 SUPLEMENTAÇÃO RECOMENDADA\\n\\n"
                        f"⭐ ESSENCIAIS (maior evidência científica para seu objetivo):\\n"
                        f"[Para cada: nome, dose, momento ideal, por que para ESTE perfil, custo estimado]\\n\\n"
                        f"➕ OPCIONAIS (benefício real mas secundário):\\n[mesma estrutura]\\n\\n"
                        f"❌ NÃO NECESSÁRIOS PARA VOCÊ AGORA:\\n[o que o marketing vende mas não faz sentido para esse perfil]\\n\\n"
                        f"📅 PROTOCOLO DIÁRIO:\\n[como encaixar cada suplemento na rotina do dia]\\n\\n"
                        f"⚠️ IMPORTANTE:\\n[interações com medicamentos se houver, contraindicações pelo perfil de saúde]"
                    )
                    res = personal_ia(prompt, "Seja honesto sobre evidências científicas. Não exagere benefícios. Sempre considere as condições de saúde reportadas.")
                    if res: st.session_state['res_suplementaca_person7'] = str(res)
                    salvar_treino("Suplementacao", "Recomendação personalizada", res)
                    st.session_state['sup_rec_temp'] = res

            if st.session_state.get('sup_rec_temp'):
                st.markdown(f"<div class='card-green'>{st.session_state['sup_rec_temp']}</div>", unsafe_allow_html=True)
                st.download_button("📋 Baixar (.txt)", data=st.session_state['sup_rec_temp'], file_name="suplementacao.txt", mime="text/plain", key="personal37")

        with tab_s2:
            supl_escolhido = st.selectbox("Escolha um suplemento:", [
                "Whey Protein","Creatina","BCAA","Glutamina","Cafeína/Pré-treino",
                "Ômega-3","Vitamina D","ZMA","Beta-Alanina","Albumina",
                "Proteína Vegetal (pea, arroz)","Colágeno","Multivitamínico","HMB","Ashwagandha"
            ], key="pt10")
            if st.button("📚 GUIA COMPLETO DESTE SUPLEMENTO", key="personal38"):
                with st.spinner("Preparando guia..."):
                    prompt = (
                        f"Crie um guia completo e científicamente embasado sobre: {supl_escolhido}.\\n\\n"
                        f"FORMATO:\\n\\n"
                        f"📚 {supl_escolhido.upper()}\\n\\n"
                        f"🔬 O QUE É E COMO FUNCIONA:\\n[mecanismo real no corpo]\\n\\n"
                        f"✅ PARA QUEM FAZ SENTIDO:\\n[perfis que mais se beneficiam]\\n\\n"
                        f"📊 DOSAGEM BASEADA EM EVIDÊNCIA:\\n[dose, timing, forma de uso]\\n\\n"
                        f"⚡ O QUE A CIÊNCIA DIZ:\\n[nível de evidência — forte, moderada ou fraca]\\n\\n"
                        f"💰 CUSTO-BENEFÍCIO:\\n[vale o investimento para a maioria das pessoas?]\\n\\n"
                        f"⚠️ CUIDADOS E CONTRAINDICAÇÕES:\\n[quem deve evitar ou consultar médico antes]"
                    )
                    res = personal_ia(prompt)
                    if res: st.session_state['res_suplementaca_person8'] = str(res)
                    st.session_state['sup_guia_temp'] = res

            if st.session_state.get('sup_guia_temp'):
                st.markdown(f"<div class='card-blue'>{st.session_state['sup_guia_temp']}</div>", unsafe_allow_html=True)

        with tab_s3:
            if st.button("⚠️ O QUE EVITAR E POR QUÊ", key="personal39"):
                with st.spinner("Preparando lista crítica..."):
                    prompt = (
                        f"Liste suplementos e produtos que devem ser evitados ou têm evidência fraca.\\n\\n"
                        f"FORMATO:\\n\\n"
                        f"⚠️ SUPLEMENTOS QUE NÃO VALEM O DINHEIRO\\n\\n"
                        f"[Para cada: nome, por que é vendido, o que a ciência realmente diz, veredicto]\\n\\n"
                        f"🚨 PRODUTOS PERIGOSOS OU SUSPEITOS:\\n[substâncias que oferecem risco real]\\n\\n"
                        f"💡 REGRA DE OURO:\\n[como avaliar qualquer novo suplemento antes de comprar]"
                    )
                    res = personal_ia(prompt)
                    if res: st.session_state['res_suplementaca_person9'] = str(res)
                    st.session_state['sup_evitar_temp'] = res

            if st.session_state.get('sup_evitar_temp'):
                st.markdown(f"<div class='card-orange'>{st.session_state['sup_evitar_temp']}</div>", unsafe_allow_html=True)

        # ========================
        # TREINO POR FADIGA
        # ========================

    with _tab_Fadiga:
        st.header("🔥 Treino por Nível de Energia")
        st.markdown("A IA adapta o treino de hoje ao seu nível real de disposição.")

        col1, col2 = st.columns(2)
        with col1:
            energia_pct = st.slider("⚡ Seu nível de energia hoje (%):", 10, 100, 70, step=10, key="personal5_x2")
            sono_noite = st.selectbox("😴 Como foi o sono ontem:", ["Ótimo (7h+)","Razoável (5-6h)","Ruim (menos de 5h)","Não dormi bem"], key="personal40")
        with col2:
            dores_hoje = st.multiselect("💢 Dores ou desconforto hoje:", ["Sem dores","Lombar","Pernas cansadas","Ombros","Braços","Dor de cabeça","Mal-estar geral"], key="personal6_x2")
            ultimo_treino = st.selectbox("📅 Último treino foi:", ["Hoje cedo","Ontem","2 dias atrás","3+ dias atrás","Não lembro"], key="personal41")

        foco_fadiga = st.text_input("🎯 Qual grupo muscular você gostaria de treinar (opcional):", placeholder="ex: pernas, costas, peito...", key="personal42")

        if st.button("🔥 GERAR TREINO ADAPTADO", key="personal43"):
            with st.spinner("Calibrando para seu nível de hoje..."):
                nivel_txt = "BAIXO" if energia_pct <= 30 else ("MÉDIO" if energia_pct <= 60 else "ALTO")
                perfil = (f"Perfil: {st.session_state.get('an_sexo','')}, {st.session_state.get('an_nivel','intermediário')}, "
                         f"objetivo: {st.session_state.get('an_objetivo','melhora geral')}, "
                         f"local: {st.session_state.get('an_local','academia')}, "
                         f"lesões: {st.session_state.get('an_lesoes','nenhuma')}." if st.session_state.get('an_objetivo') else "")
                prompt = (
                    f"Crie um treino adaptado ao nível de energia atual.\\n"
                    f"{perfil}\\n"
                    f"Energia: {energia_pct}% (nível {nivel_txt}). Sono: {sono_noite}. "
                    f"Dores: {', '.join(dores_hoje) or 'nenhuma'}. Último treino: {ultimo_treino}. "
                    f"Foco desejado: {foco_fadiga or 'livre'}.\\n\\n"
                    f"FORMATO:\\n\\n"
                    f"🔥 TREINO DE HOJE — NÍVEL {nivel_txt} ({energia_pct}%)\\n\\n"
                    f"🎯 ESTRATÉGIA DO DIA:\\n[por que esse tipo de treino faz sentido hoje com essa energia]\\n\\n"
                    f"⚡ AQUECIMENTO ({5 if energia_pct < 50 else 10} min):\\n[adaptado ao nível de energia]\\n\\n"
                    f"💪 TREINO PRINCIPAL:\\n[exercícios com séries, repetições e descanso — "
                    f"mais leve e menos volume se energia baixa, normal/intenso se alta]\\n\\n"
                    f"🔄 ADAPTAÇÕES PARA AS DORES REPORTADAS:\\n[como modificar exercícios]\\n\\n"
                    f"🧘 FINALIZAÇÃO:\\n[volta à calma adequada ao estado de hoje]\\n\\n"
                    f"💡 CONSELHO DO DIA:\\n[1 orientação sobre treinar com esse nível de energia]"
                )
                res = personal_ia(prompt)
                if res: st.session_state['res_fadiga_person10'] = str(res)
                salvar_treino("Fadiga", f"Energia {energia_pct}%", res)
                st.session_state['fadiga_temp'] = res

        if st.session_state.get('fadiga_temp'):
            cor = "card-red" if energia_pct <= 30 else ("card-orange" if energia_pct <= 60 else "card-green")
            st.markdown(f"<div class='{cor}'>{st.session_state['fadiga_temp']}</div>", unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['fadiga_temp'], file_name="treino_fadiga.txt", mime="text/plain", use_container_width=True, key="personal44")
            with col_sv:
                if st.button("✅ Treino Concluído!", key="concluir_fadiga", use_container_width=True):
                    st.session_state.treinos_realizados += 1
                    st.success("🏆 +1 treino concluído!")

        # ========================
        # CALCULADORA DE MACROS
        # ========================

    with _tab_Macros:
        st.header("🍽️ Calculadora de Macros")

        col1, col2, col3 = st.columns(3)
        with col1:
            peso_mac = st.number_input("Peso (kg):", min_value=30.0, max_value=250.0,
                value=float(st.session_state.get('an_peso', 70)), step=0.5, key="pt9")
            altura_mac = st.number_input("Altura (cm):", min_value=120, max_value=220,
                value=int(st.session_state.get('an_altura', 170)), key="pt8")
            idade_mac = st.number_input("Idade:", min_value=12, max_value=90,
                value=int(st.session_state.get('an_idade', 30)), key="pt7")
        with col2:
            sexo_mac = st.selectbox("Sexo biológico:", ["Masculino","Feminino"],
                index=0 if st.session_state.get('an_sexo','Masculino')=='Masculino' else 1, key="pt6")
            atividade_mac = st.selectbox("Nível de atividade:", [
                "Sedentário (sem exercício)","Levemente ativo (1-2x/sem)",
                "Moderadamente ativo (3-4x/sem)","Muito ativo (5-6x/sem)","Extremamente ativo (2x/dia)"], key="pt5")
        with col3:
            objetivo_mac = st.selectbox("Objetivo:", ["Perder gordura","Manutenção","Ganhar massa"], key="personal45")
            dieta_mac = st.selectbox("Preferência alimentar:", ["Onívoro","Vegetariano","Vegano","Low carb","Cetogênica"], key="personal46")

        if st.button("🍽️ CALCULAR MEUS MACROS", key="personal47"):
            with st.spinner("Calculando..."):
                # TMB pelo método Harris-Benedict
                if sexo_mac == "Masculino":
                    tmb = 88.36 + (13.4 * peso_mac) + (4.8 * altura_mac) - (5.7 * idade_mac)
                else:
                    tmb = 447.6 + (9.2 * peso_mac) + (3.1 * altura_mac) - (4.3 * idade_mac)

                fat = {"Sedentário (sem exercício)":1.2,"Levemente ativo (1-2x/sem)":1.375,
                       "Moderadamente ativo (3-4x/sem)":1.55,"Muito ativo (5-6x/sem)":1.725,
                       "Extremamente ativo (2x/dia)":1.9}
                tdee = tmb * fat.get(atividade_mac, 1.55)
                cal_alvo = tdee - 400 if objetivo_mac == "Perder gordura" else (tdee + 300 if objetivo_mac == "Ganhar massa" else tdee)

                prompt = (
                    f"Crie um plano completo de macros para esta pessoa.\\n"
                    f"TMB calculada: {tmb:.0f} kcal. TDEE: {tdee:.0f} kcal. Calorias alvo: {cal_alvo:.0f} kcal.\\n"
                    f"Perfil: {sexo_mac}, {idade_mac} anos, {peso_mac}kg, {altura_mac}cm, "
                    f"objetivo: {objetivo_mac}, dieta: {dieta_mac}.\\n\\n"
                    f"FORMATO:\\n\\n"
                    f"🍽️ SEU PLANO DE MACROS\\n\\n"
                    f"📊 CALORIAS DIÁRIAS: {cal_alvo:.0f} kcal\\n"
                    f"(TMB: {tmb:.0f} | TDEE: {tdee:.0f})\\n\\n"
                    f"🥩 PROTEÍNA: [X]g/dia ([X] kcal)\\n[justificativa e fontes recomendadas para {dieta_mac}]\\n\\n"
                    f"🍞 CARBOIDRATO: [X]g/dia ([X] kcal)\\n[timing e melhores fontes]\\n\\n"
                    f"🥑 GORDURA: [X]g/dia ([X] kcal)\\n[melhores fontes]\\n\\n"
                    f"📅 DISTRIBUIÇÃO NAS REFEIÇÕES:\\n[como dividir os macros ao longo do dia — 4-6 refeições]\\n\\n"
                    f"🍱 EXEMPLOS DE REFEIÇÕES:\\n[3 exemplos práticos que batem os macros do dia, respeitando {dieta_mac}]\\n\\n"
                    f"💡 DICA PRINCIPAL:\\n[1 ajuste que mais impacta o resultado para esse objetivo]"
                )
                res = personal_ia(prompt)
                if res: st.session_state['res_macros_person11'] = str(res)
                salvar_treino("Macros", f"{objetivo_mac} — {cal_alvo:.0f}kcal", res)
                st.session_state['macros_temp'] = res

        if st.session_state.get('macros_temp'):
            st.markdown(f"<div class='card-green'>{st.session_state['macros_temp']}</div>", unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['macros_temp'], file_name="plano_macros.txt", mime="text/plain", use_container_width=True, key="personal48")
            with col_sv:
                if st.button("❤️ Salvar", key="sv_macros", use_container_width=True):
                    st.session_state.treinos_salvos.append({'tipo':'Macros','foco':f"{objetivo_mac}",'conteudo':st.session_state['macros_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

        # ========================
        # RECUPERAÇÃO E SONO
        # ========================

    with _tab_Recuperacao:
        st.header("😴 Recuperação e Sono")

        tab_r1, tab_r2, tab_r3 = st.tabs(["😴 Sono e Recuperação","🧊 Recuperação Ativa","🚨 Overtraining"])

        with tab_r1:
            horas_sono = st.selectbox("Quantas horas você dorme por noite:", ["Menos de 5h","5-6h","6-7h","7-8h","8h+"], key="personal49")
            qualidade_sono = st.selectbox("Qualidade do sono:", ["Ótima (acordo descansado)","Boa","Regular","Ruim (acordo cansado)","Péssima (insônia)"], key="personal50")

            if st.button("😴 ANALISAR MEU SONO E RECUPERAÇÃO", key="personal51"):
                with st.spinner("Analisando..."):
                    prompt = (
                        f"Analise o padrão de sono e crie um guia de recuperação personalizado.\\n"
                        f"Sono: {horas_sono} por noite. Qualidade: {qualidade_sono}.\\n"
                        f"Objetivo: {st.session_state.get('an_objetivo','melhora geral')}. "
                        f"Nível: {st.session_state.get('an_nivel','intermediário')}. "
                        f"Estresse: {st.session_state.get('an_estresse','moderado')}.\\n\\n"
                        f"FORMATO:\\n\\n"
                        f"😴 ANÁLISE DO SEU SONO\\n\\n"
                        f"📊 O IMPACTO NO SEU TREINO:\\n[como esse padrão de sono afeta seus resultados especificamente]\\n\\n"
                        f"🧠 POR QUE O SONO É O SUPLEMENTO MAIS PODEROSO:\\n[mecanismos fisiológicos — GH, testosterona, recuperação muscular]\\n\\n"
                        f"✅ PROTOCOLO DE HIGIENE DO SONO:\\n[ações específicas para melhorar, em ordem de impacto]\\n\\n"
                        f"⏰ ROTINA IDEAL PRÉ-SONO:\\n[o que fazer nas 2 horas antes de dormir]\\n\\n"
                        f"💊 SUPLEMENTOS QUE PODEM AJUDAR:\\n[com base em evidência — melatonina, magnésio, etc]\\n\\n"
                        f"🎯 META DESTA SEMANA:\\n[1 mudança concreta para começar hoje]"
                    )
                    res = personal_ia(prompt)
                    if res: st.session_state['res_recuperacao_person12'] = str(res)
                    st.session_state['sono_temp'] = res

            if st.session_state.get('sono_temp'):
                st.markdown(f"<div class='card-purple'>{st.session_state['sono_temp']}</div>", unsafe_allow_html=True)

        with tab_r2:
            dias_sem_treino = st.number_input("Dias seguidos treinando sem descanso:", min_value=0, max_value=30, value=3, key="personal52")
            tipo_dor = st.multiselect("Onde você sente dor muscular agora:", ["Sem dores","Pernas","Costas","Peito","Ombros","Braços","Abdômen"], key="personal7_x2")

            if st.button("🧊 PROTOCOLO DE RECUPERAÇÃO ATIVA", key="personal53"):
                with st.spinner("Preparando protocolo..."):
                    prompt = (
                        f"Crie um protocolo de recuperação ativa.\\n"
                        f"Dias consecutivos treinando: {dias_sem_treino}. Dores: {', '.join(tipo_dor) or 'nenhuma'}.\\n\\n"
                        f"FORMATO:\\n\\n"
                        f"🧊 PROTOCOLO DE RECUPERAÇÃO ATIVA\\n\\n"
                        f"🎯 DIAGNÓSTICO:\\n[avaliação do estado de recuperação]\\n\\n"
                        f"✅ ATIVIDADES DE RECUPERAÇÃO RECOMENDADAS HOJE:\\n[o que fazer — caminhada leve, mobilidade, natação leve, etc]\\n\\n"
                        f"🧊 TÉCNICAS DE RECUPERAÇÃO FÍSICA:\\n[banho frio, contraste, foam roller, compressão — o que ajuda e como]\\n\\n"
                        f"🍽️ NUTRIÇÃO PARA RECUPERAÇÃO:\\n[o que comer para acelerar a recuperação muscular]\\n\\n"
                        f"⏳ QUANDO VOLTAR AO TREINO INTENSO:\\n[guia de timing baseado no estado atual]"
                    )
                    res = personal_ia(prompt)
                    if res: st.session_state['res_recuperacao_person13'] = str(res)
                    st.session_state['rec_ativa_temp'] = res

            if st.session_state.get('rec_ativa_temp'):
                st.markdown(f"<div class='card-blue'>{st.session_state['rec_ativa_temp']}</div>", unsafe_allow_html=True)

        with tab_r3:
            sintomas_over = st.multiselect("Você está sentindo:", [
                "Queda de desempenho nos treinos","Fadiga persistente mesmo com descanso",
                "Irritabilidade e mudanças de humor","Insônia ou sono ruim",
                "Dores articulares frequentes","Perda de motivação para treinar",
                "Infecções frequentes (gripes, resfriados)","Frequência cardíaca em repouso elevada"], key="pt4")

            if st.button("🚨 AVALIAR RISCO DE OVERTRAINING", key="personal54"):
                if sintomas_over:
                    with st.spinner("Analisando..."):
                        prompt = (
                            f"Avalie o risco de overtraining com base nos sintomas.\\n"
                            f"Sintomas: {', '.join(sintomas_over)}.\\n"
                            f"Frequência de treino: {st.session_state.get('an_dias',3)} dias/semana. "
                            f"Nível: {st.session_state.get('an_nivel','intermediário')}.\\n\\n"
                            f"FORMATO:\\n\\n"
                            f"🚨 AVALIAÇÃO DE OVERTRAINING\\n\\n"
                            f"📊 NÍVEL DE RISCO: [Baixo/Moderado/Alto/Crítico]\\n[justificativa]\\n\\n"
                            f"🔬 O QUE ESTÁ ACONTECENDO NO SEU CORPO:\\n[fisiologia do overtraining]\\n\\n"
                            f"🛑 O QUE FAZER AGORA:\\n[protocolo de ação baseado no nível de risco]\\n\\n"
                            f"📅 PLANO DE DELOAD:\\n[como estruturar a semana de recuperação]\\n\\n"
                            f"✅ COMO PREVENIR NO FUTURO:\\n[periodização e sinais de alerta precoces]"
                        )
                        res = personal_ia(prompt, "Seja conservador nas recomendações de saúde. Se os sintomas forem graves, recomende avaliação médica.")
                        if res: st.session_state['res_recuperacao_person14'] = str(res)
                        st.session_state['over_temp'] = res
                else:
                    st.info("Selecione os sintomas que está sentindo.")

            if st.session_state.get('over_temp'):
                st.markdown(f"<div class='card-orange'>{st.session_state['over_temp']}</div>", unsafe_allow_html=True)

        # ========================
        # MÓDULO MENTAL
        # ========================

    with _tab_Mental:
        st.header("🧠 Mentalidade e Consistência")

        tema_mental = st.selectbox("O que você está enfrentando:", [
            "Falta de motivação para treinar","Procrastinação — fico adiando o treino",
            "Abandonei os treinos e quero recomeçar","Sabotagem — começo bem e travejo no meio",
            "Como criar um hábito de treino duradouro","Ansiedade com resultados lentos",
            "Como lidar com a semana que fugiu do plano","Mentalidade de atleta para vida real",
        ], key="pt3")
        contexto_mental = st.text_area("Conte mais sobre o que está acontecendo:", height=100,
            placeholder="ex: Sei que devo treinar mas quando chega a hora invento desculpas...", key="pt2")

        if st.button("🧠 ORIENTAÇÃO MENTAL", key="personal55"):
            with st.spinner("Preparando orientação..."):
                prompt = (
                    f"Ofereça orientação sobre mentalidade e consistência no treino.\\n"
                    f"Tema: {tema_mental}. Contexto: {contexto_mental or 'não detalhado'}.\\n"
                    f"Perfil: objetivo {st.session_state.get('an_objetivo','melhora geral')}, "
                    f"nível {st.session_state.get('an_nivel','iniciante')}.\\n\\n"
                    f"FORMATO:\\n\\n"
                    f"🧠 {tema_mental.upper()}\\n\\n"
                    f"🎯 O QUE REALMENTE ESTÁ ACONTECENDO:\\n[a raiz psicológica do problema, sem julgamento]\\n\\n"
                    f"🔬 A CIÊNCIA POR TRÁS:\\n[o que a psicologia do comportamento e neurociência diz sobre isso]\\n\\n"
                    f"⚙️ ESTRATÉGIAS PRÁTICAS:\\n[3-5 ações concretas e replicáveis]\\n\\n"
                    f"📅 O QUE FAZER HOJE:\\n[1 ação imediata para quebrar o padrão]\\n\\n"
                    f"💪 REFRAME:\\n[uma perspectiva diferente que muda como você vê a situação]"
                )
                res = personal_ia(prompt, "Seja direto, empático e prático. Evite clichês motivacionais vazios. Fale de igual para igual.")
                if res: st.session_state['res_mental_person15'] = str(res)
                salvar_treino("Mental", tema_mental, res)
                st.session_state['mental_temp'] = res

        if st.session_state.get('mental_temp'):
            st.markdown(f"<div class='card-dark'>{st.session_state['mental_temp']}</div>", unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['mental_temp'], file_name="mentalidade.txt", mime="text/plain", use_container_width=True, key="personal56")
            with col_sv:
                if st.button("❤️ Salvar", key="sv_mental", use_container_width=True):
                    st.session_state.treinos_salvos.append({'tipo':'Mental','foco':tema_mental,'conteudo':st.session_state['mental_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

        # ========================
        # BIBLIOTECA DE EXERCÍCIOS
        # ========================

    with _tab_Biblioteca:
        st.header("📚 Biblioteca de Exercícios")

        tab_b1, tab_b2, tab_b3 = st.tabs(["🔄 Substituições","📖 Guia do Exercício","💢 Adaptações para Lesão"])

        with tab_b1:
            col1, col2 = st.columns(2)
            with col1:
                exercicio_orig = st.text_input("Exercício que você NÃO pode fazer:", placeholder="ex: agachamento, supino, barra fixa...", key="personal57")
            with col2:
                motivo_subst = st.selectbox("Motivo:", ["Não tenho o equipamento","Lesão ou dor","Iniciante — muito difícil","Prefiro variar"], key="personal58")

            if st.button("🔄 ENCONTRAR SUBSTITUIÇÕES", key="personal59"):
                if exercicio_orig.strip():
                    with st.spinner("Buscando alternativas..."):
                        prompt = (
                            f"Sugira substituições para o exercício: {exercicio_orig}.\\n"
                            f"Motivo: {motivo_subst}.\\n"
                            f"Equipamentos disponíveis: {st.session_state.get('an_equipamentos','não informado')}. "
                            f"Local: {st.session_state.get('an_local','academia')}. "
                            f"Lesões: {st.session_state.get('an_lesoes','nenhuma')}.\\n\\n"
                            f"FORMATO:\\n\\n"
                            f"🔄 SUBSTITUIÇÕES PARA: {exercicio_orig.upper()}\\n\\n"
                            f"✅ SUBSTITUTO PRINCIPAL (mais similar em recrutamento muscular):\\n[nome, como fazer, por que é equivalente]\\n\\n"
                            f"✅ SUBSTITUTO ALTERNATIVO 1:\\n[nome, como fazer]\\n\\n"
                            f"✅ SUBSTITUTO ALTERNATIVO 2:\\n[nome, como fazer]\\n\\n"
                            f"💡 DICA DE TRANSIÇÃO:\\n[como adaptar a carga/série ao mudar de exercício]"
                        )
                        res = personal_ia(prompt)
                        if res: st.session_state['res_biblioteca_person16'] = str(res)
                        st.session_state['subst_temp'] = res

            if st.session_state.get('subst_temp'):
                st.markdown(f"<div class='card-green'>{st.session_state['subst_temp']}</div>", unsafe_allow_html=True)

        with tab_b2:
            exercicio_guia = st.text_input("Exercício para estudar:", placeholder="ex: levantamento terra, elevação lateral...", key="personal60")

            if st.button("📖 GUIA COMPLETO", key="personal61"):
                if exercicio_guia.strip():
                    with st.spinner("Preparando guia..."):
                        prompt = (
                            f"Crie um guia completo e técnico sobre o exercício: {exercicio_guia}.\\n\\n"
                            f"FORMATO:\\n\\n"
                            f"📖 {exercicio_guia.upper()}\\n\\n"
                            f"🏋️ MÚSCULOS TRABALHADOS:\\n[principal e secundários]\\n\\n"
                            f"⚙️ EXECUÇÃO CORRETA (passo a passo):\\n[técnica detalhada]\\n\\n"
                            f"❌ ERROS MAIS COMUNS:\\n[e como corrigir cada um]\\n\\n"
                            f"📊 VARIAÇÕES:\\n[versões mais fáceis, mais difíceis e alternativas]\\n\\n"
                            f"💡 DICAS DE PERFORMANCE:\\n[o que muda para iniciantes vs avançados]\\n\\n"
                            f"⚠️ CUIDADOS E CONTRAINDICAÇÕES:\\n[quando evitar ou ter cuidado especial]"
                        )
                        res = personal_ia(prompt)
                        if res: st.session_state['res_biblioteca_person17'] = str(res)
                        st.session_state['guia_ex_temp'] = res

            if st.session_state.get('guia_ex_temp'):
                st.markdown(f"<div class='card-blue'>{st.session_state['guia_ex_temp']}</div>", unsafe_allow_html=True)

        with tab_b3:
            lesao_adapt = st.text_input("Sua lesão ou limitação:", placeholder="ex: dor no joelho, tendinite no ombro, hérnia lombar...", key="personal62")
            grupo_adapt = st.selectbox("Grupo muscular que quer treinar:", ["Pernas","Costas","Peito","Ombros","Bíceps","Tríceps","Abdômen","Full body"], key="personal63")

            if st.button("💢 TREINO ADAPTADO PARA MINHA LESÃO", key="personal64"):
                if lesao_adapt.strip():
                    with st.spinner("Adaptando treino..."):
                        prompt = (
                            f"Crie um protocolo de treino adaptado para treinar {grupo_adapt} com a limitação: {lesao_adapt}.\\n\\n"
                            f"FORMATO:\\n\\n"
                            f"💢 TREINO DE {grupo_adapt.upper()} COM {lesao_adapt.upper()}\\n\\n"
                            f"⚠️ EXERCÍCIOS A EVITAR COMPLETAMENTE:\\n[e por que causam risco]\\n\\n"
                            f"✅ EXERCÍCIOS SEGUROS:\\n[lista com séries, repetições e cuidados específicos]\\n\\n"
                            f"🔧 ADAPTAÇÕES TÉCNICAS:\\n[modificações na execução para proteger a lesão]\\n\\n"
                            f"🩺 QUANDO CONSULTAR UM PROFISSIONAL:\\n[sinais de alerta que indicam necessidade de avaliação médica]"
                        )
                        res = personal_ia(prompt, "IMPORTANTE: sempre recomende avaliação médica ou fisioterapêutica antes de treinar com lesões. Não faça diagnóstico — apenas oriente sobre adaptações gerais.")
                        if res: st.session_state['res_biblioteca_person18'] = str(res)
                        st.session_state['adapt_lesao_temp'] = res

            if st.session_state.get('adapt_lesao_temp'):
                st.markdown(f"<div class='card-orange'>{st.session_state['adapt_lesao_temp']}</div>", unsafe_allow_html=True)
                st.markdown("<div class='disclaimer' style='background:#FFF7ED;border:1px solid #FDE68A;border-radius:10px;padding:12px;font-size:0.82em;color:#92400E;margin-top:8px;'>⚠️ Este conteúdo é educativo. Sempre consulte um médico ou fisioterapeuta antes de treinar com lesões.</div>", unsafe_allow_html=True)

        # ========================
        # DESAFIO 30/60/90 DIAS
        # ========================

    with _tab_Desafio:
        st.header("🏆 Desafio 30/60/90 Dias")

        if 'desafio_ativo' not in st.session_state:
            st.session_state.desafio_ativo = None
        if 'desafio_checkins' not in st.session_state:
            st.session_state.desafio_checkins = []
        if 'desafio_pontos' not in st.session_state:
            st.session_state.desafio_pontos = 0

        if st.session_state.desafio_ativo is None:
            st.markdown("### 🎯 Crie seu Desafio")
            col1, col2 = st.columns(2)
            with col1:
                duracao_des = st.selectbox("Duração:", ["30 dias","60 dias","90 dias"], key="personal65")
                objetivo_des = st.selectbox("Objetivo do desafio:", [
                    "Perder gordura","Ganhar massa","Criar hábito de treino",
                    "Melhorar condicionamento","Definição muscular","Força"], key="pt1")
            with col2:
                dias_semana_des = st.slider("Dias de treino por semana:", 2, 6, 3, key="personal8_x2")
                nivel_des = st.selectbox("Intensidade:", ["Leve (foco no hábito)","Moderada","Intensa"], key="personal66")

            if st.button("🏆 CRIAR MEU DESAFIO", key="personal67"):
                with st.spinner("Montando seu desafio..."):
                    prompt = (
                        f"Crie um programa de desafio completo.\\n"
                        f"Duração: {duracao_des}. Objetivo: {objetivo_des}. "
                        f"Treinos/semana: {dias_semana_des}. Intensidade: {nivel_des}.\\n"
                        f"Perfil: {st.session_state.get('an_nivel','iniciante')}, "
                        f"local: {st.session_state.get('an_local','academia')}.\\n\\n"
                        f"FORMATO:\\n\\n"
                        f"🏆 DESAFIO {duracao_des.upper()} — {objetivo_des.upper()}\\n\\n"
                        f"🎯 O QUE VOCÊ VAI CONQUISTAR:\\n[resultados esperados realistas]\\n\\n"
                        f"📅 ESTRUTURA DO PROGRAMA:\\n[como as semanas se organizam — progressão]\\n\\n"
                        f"💪 TREINOS DA SEMANA 1:\\n[treinos completos para começar]\\n\\n"
                        f"📊 COMO MEDIR SEU PROGRESSO:\\n[métricas semanais para acompanhar]\\n\\n"
                        f"🔥 REGRAS DO DESAFIO:\\n[compromissos claros e não-negociáveis]\\n\\n"
                        f"💡 MISSÃO DO DIA 1:\\n[o que fazer hoje para começar com força]"
                    )
                    res = personal_ia(prompt)
                    if res: st.session_state['res_desafio_person19'] = str(res)
                    st.session_state.desafio_ativo = {
                        'duracao': duracao_des, 'objetivo': objetivo_des,
                        'inicio': datetime.now().strftime('%d/%m/%Y'),
                        'programa': res, 'dias_semana': dias_semana_des
                    }
                    st.session_state.desafio_pontos = 0
                    st.session_state.desafio_checkins = []
                    st.rerun()
        else:
            des = st.session_state.desafio_ativo
            dias_passados = len(st.session_state.desafio_checkins)
            total_dias = int(des['duracao'].split()[0])
            pct = min(int(dias_passados / total_dias * 100), 100)

            col1, col2, col3, col4 = st.columns(4)
            col1.markdown(f"<div class='stat-box'><div class='stat-numero'>{dias_passados}</div><div>Dias concluídos</div></div>", unsafe_allow_html=True)
            col2.markdown(f"<div class='stat-box'><div class='stat-numero'>{total_dias - dias_passados}</div><div>Dias restantes</div></div>", unsafe_allow_html=True)
            col3.markdown(f"<div class='stat-box'><div class='stat-numero'>{st.session_state.desafio_pontos}</div><div>Pontos</div></div>", unsafe_allow_html=True)
            col4.markdown(f"<div class='stat-box'><div class='stat-numero'>{pct}%</div><div>Concluído</div></div>", unsafe_allow_html=True)

            st.progress(pct / 100)
            st.markdown(f"<br>**🏆 {des['duracao']} de {des['objetivo']}** — iniciado em {des['inicio']}", unsafe_allow_html=True)

            with st.expander("📋 Ver programa completo"):
                st.markdown(f"<div class='card'>{des['programa']}</div>", unsafe_allow_html=True)

            st.markdown("### ✅ Check-in do Dia")
            col_c1, col_c2 = st.columns(2)
            with col_c1:
                treinou_hoje = st.radio("Você treinou hoje?", ["✅ Sim, treinei!","❌ Não treinei"], key="treinou_radio")
                nota_treino = st.slider("Como foi o treino (1-10):", 1, 10, 7, key="personal9_x2") if "Sim" in treinou_hoje else None
            with col_c2:
                comeu_bem = st.radio("Seguiu a alimentação?", ["✅ Sim","Parcialmente","❌ Não"], key="personal68")
                obs_dia = st.text_input("Observação do dia:", placeholder="ex: Senti evolução no supino...", key="personal69")

            if st.button("📝 FAZER CHECK-IN DE HOJE", key="personal70"):
                checkin = {
                    'data': datetime.now().strftime('%d/%m/%Y'),
                    'treinou': "Sim" in treinou_hoje,
                    'nota': nota_treino,
                    'alimentacao': comeu_bem,
                    'obs': obs_dia
                }
                st.session_state.desafio_checkins.append(checkin)
                pontos = 10 if "Sim" in treinou_hoje else 2
                pontos += 5 if comeu_bem == "✅ Sim" else (2 if comeu_bem == "Parcialmente" else 0)
                st.session_state.desafio_pontos += pontos
                st.success(f"✅ Check-in registrado! +{pontos} pontos 🔥")
                st.rerun()

            if st.session_state.desafio_checkins:
                with st.expander(f"📊 Histórico de check-ins ({len(st.session_state.desafio_checkins)} dias)"):
                    for c in reversed(st.session_state.desafio_checkins[-10:]):
                        status = "✅" if c['treinou'] else "❌"
                        st.markdown(f"**{c['data']}** — {status} Treino | Alimentação: {c['alimentacao']} {('| Nota: ' + str(c['nota'])) if c['nota'] else ''} {('| ' + c['obs']) if c['obs'] else ''}")

            st.markdown("<hr>", unsafe_allow_html=True)
            if st.button("🔄 Encerrar e criar novo desafio", key="encerrar_desafio"):
                st.session_state.desafio_ativo = None
                st.rerun()


        # --- RODAPÉ ---
        st.markdown(
        "<div style='text-align:center;color:#999;font-size:0.8em;margin-top:60px;'>"
        "© 2026 Personal Trainer IA — Treinos Personalizados com IA · MeusAgentesIA.com.br"
        "</div>", unsafe_allow_html=True
        )

# --- RODAPÉ ---
st.markdown(
    "<div style='text-align:center;color:#999;font-size:0.8em;margin-top:60px;'>"
    "© 2026 Personal Trainer IA — Treinos Personalizados com IA · MeusAgentesIA.com.br"
    "</div>", unsafe_allow_html=True
)
""",
    "tutor_concursos": """# [hub] import streamlit as st
# [hub] from groq import Groq
# [hub] from datetime import datetime, date, timedelta
# [hub] import json
import random

# set_page_config removido pelo super_agente

st.markdown(\"\"\"
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
[data-testid="stToolbar"] {visibility: hidden;}
[data-testid="stDecoration"] {visibility: hidden;}
[data-testid="stStatusWidget"] {visibility: hidden;}
</style>
\"\"\", unsafe_allow_html=True)


st.markdown(\"\"\"
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    .stApp { background-color:#FDFAF6; font-family:'Inter',sans-serif; }
    [data-testid="stSidebar"] { display:none; }

    .stTextInput>div>div>input, .stTextArea>div>textarea,
    .stSelectbox>div>div>div, .stNumberInput>div>div>input {
        background-color:#FFFFFF !important; color:#1A1A2E !important;
        border:1px solid #CED4DA !important; font-family:'Inter',sans-serif !important;
    }

    .stButton>button {
        width:100%; border-radius:10px; height:3.2em;
        background:linear-gradient(135deg,#92400E,#78350F) !important; color:white !important;
        font-weight:600; border:none; box-shadow:2px 2px 8px rgba(0,0,0,0.1);
        font-family:'Inter',sans-serif !important; transition:all 0.2s ease;
    }
    .stButton>button:hover { background:linear-gradient(135deg,#78350F,#5C2D0A) !important; transform:translateY(-1px); }
    .stApp .stButton>button, .stApp .stButton>button p,
    .stApp .stButton>button span, .stApp .stButton>button div { color:white !important; }

    .stApp h1, .stApp h2, .stApp h3 { color:#3D2B1F !important; font-family:'Inter',sans-serif !important; font-weight:700 !important; }

    .card { background:linear-gradient(135deg,#FDF8F0,#FAF0E6); padding:20px; border-radius:14px; border:1px solid #D4B896; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card, .stApp .card p, .stApp .card span, .stApp .card div, .stApp .card strong, .stApp .card em { color:#3D2B1F !important; }

    .card-dark { background:linear-gradient(135deg,#FAF0E6,#F5E6D3); padding:20px; border-radius:14px; border:1px solid #C4956A; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-dark, .stApp .card-dark p, .stApp .card-dark span, .stApp .card-dark div, .stApp .card-dark strong { color:#3D2B1F !important; }

    .card-green { background:linear-gradient(135deg,#F0FDF4,#DCFCE7); padding:20px; border-radius:14px; border:1px solid #86EFAC; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-green, .stApp .card-green p, .stApp .card-green span, .stApp .card-green div { color:#14532D !important; }

    .card-blue { background:linear-gradient(135deg,#EFF6FF,#DBEAFE); padding:20px; border-radius:14px; border:1px solid #93C5FD; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-blue, .stApp .card-blue p, .stApp .card-blue span, .stApp .card-blue div { color:#1E3A8A !important; }

    .card-red { background:linear-gradient(135deg,#FFF5F5,#FEE2E2); padding:20px; border-radius:14px; border:1px solid #FECACA; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-red, .stApp .card-red p, .stApp .card-red span, .stApp .card-red div { color:#7F1D1D !important; }

    .card-yellow { background:linear-gradient(135deg,#FFFBEB,#FEF3C7); padding:18px; border-radius:12px; border:1px solid #FCD34D; margin-bottom:12px; white-space:normal; word-wrap:break-word; }
    .stApp .card-yellow, .stApp .card-yellow p, .stApp .card-yellow span, .stApp .card-yellow div { color:#78350F !important; }

    .stat-box { background:#FFFFFF; border-radius:12px; padding:16px; text-align:center; border:1px solid #D4B896; }
    .stApp .stat-box div, .stApp .stat-box span, .stApp .stat-box p { color:#3D2B1F !important; }
    .stApp .stat-numero, .stat-numero { font-size:2em; font-weight:700; color:#7C5C3E !important; }

    .hist-item { background:#FFFFFF; border-radius:10px; padding:12px 16px; margin-bottom:8px; border-left:4px solid #D4B896; }
    .stApp .hist-item, .stApp .hist-item p, .stApp .hist-item span, .stApp .hist-item div, .stApp .hist-item small { color:#3D2B1F !important; }

    .badge { background:#92400E; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-verde { background:#059669; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-amarelo { background:#B45309; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-azul { background:#1D4ED8; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-roxo { background:#6D28D9; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }

    .divider { border:none; height:1px; background:linear-gradient(to right,transparent,#D4B896,transparent); margin:18px 0; }

    .chat-user { background:#FFFFFF; border:1px solid #D4B896; border-radius:12px 12px 4px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-user, .stApp .chat-user p, .stApp .chat-user span, .stApp .chat-user div { color:#3D2B1F !important; }

    .chat-persona { background:#FDFAF6; border:1px solid #D4B896; border-radius:4px 12px 12px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-persona, .stApp .chat-persona p, .stApp .chat-persona span, .stApp .chat-persona div { color:#3D2B1F !important; }

    .questao-box { background:#FFFFFF; border:2px solid #D4B896; border-radius:12px; padding:18px; margin-bottom:14px; }
    .stApp .questao-box, .stApp .questao-box p, .stApp .questao-box span, .stApp .questao-box div { color:#3D2B1F !important; }

    .avaliacao-box { background:#FFFFFF; border:2px solid #D4B896; border-radius:14px; padding:18px; margin-bottom:12px; }
    .stApp .avaliacao-box, .stApp .avaliacao-box p, .stApp .avaliacao-box span, .stApp .avaliacao-box div { color:#3D2B1F !important; }

    .meta-box { background:#FFFFFF; border:2px solid #D4B896; border-radius:12px; padding:16px; text-align:center; margin:10px 0; }
    .stApp .meta-box, .stApp .meta-box div, .stApp .meta-box span { color:#3D2B1F !important; }
    .stApp .meta-numero { font-size:2em; font-weight:700; color:#7C5C3E !important; }

    .chat-scroll-container { max-height:40vh; overflow-y:auto; display:flex; flex-direction:column; scroll-behavior:smooth; padding-bottom:4px; }
    .chat-scroll-container > * { flex-shrink:0; }
    

    </style>
\"\"\", unsafe_allow_html=True)

# ─── CACHE ───
@st.cache_resource
def get_cache_tutor():
    return {"perfis": {}}
_cache = get_cache_tutor()

# ─── NÍVEIS E XP ───
NIVEIS = [
    (0,    "Iniciante",   "🌱"),
    (100,  "Aprendiz",    "📚"),
    (300,  "Persistente", "💪"),
    (600,  "Estudioso",   "🎯"),
    (1000, "Especialista","⭐"),
    (1500, "Elite",       "🏆"),
    (2500, "Aprovado",    "🎓"),
]
XP_ATIVIDADES = {
    'questao_certa': 10, 'questao_errada': 2, 'resumo': 20,
    'flashcard': 15, 'simulado': 50, 'revisao': 15,
    'plano': 25, 'mapa_mental': 20, 'missao_dia': 30,
}

def calcular_nivel(xp: int):
    nivel_atual = NIVEIS[0]
    for req_xp, nome, emoji in NIVEIS:
        if xp >= req_xp:
            nivel_atual = (req_xp, nome, emoji)
    return nivel_atual

def xp_proximo_nivel(xp: int):
    for i, (req_xp, nome, emoji) in enumerate(NIVEIS):
        if xp < req_xp:
            return req_xp
    return NIVEIS[-1][0]

# ─── CONQUISTAS ───
CONQUISTAS_DEF = [
    ("primeira_questao",   "🎯 Primeira Questão",      "Respondeu sua primeira questão"),
    ("questoes_100",       "💯 Centenário",             "100 questões respondidas"),
    ("questoes_1000",      "🏆 Guerreiro",              "1.000 questões respondidas"),
    ("primeiro_resumo",    "📝 Primeiro Resumo",        "Criou seu primeiro resumo"),
    ("primeiro_plano",     "📅 Planejador",             "Criou seu primeiro plano de estudos"),
    ("primeiro_simulado",  "📊 Simulador",              "Realizou seu primeiro simulado"),
    ("streak_7",           "🔥 7 Dias",                 "7 dias consecutivos de estudo"),
    ("streak_30",          "⚡ 30 Dias",                "30 dias consecutivos de estudo"),
    ("horas_100",          "⏱️ 100 Horas",              "100 horas de estudo acumuladas"),
    ("acerto_90",          "🎯 Mira Certeira",          "Taxa de acerto acima de 90%"),
    ("especialista_mat",   "🔢 Especialista em Matemática", "Acerto >80% em Matemática"),
    ("especialista_port",  "📖 Especialista em Português",  "Acerto >80% em Português"),
    ("especialista_dir",   "⚖️ Especialista em Direito",    "Acerto >80% em Direito"),
    ("nivel_elite",        "🌟 Elite",                  "Atingiu o nível Elite"),
    ("aprovado",           "🎓 Aprovado",               "Atingiu o nível Aprovado"),
]

def verificar_conquistas():
    conquistadas = st.session_state.get('conquistas', [])
    novas = []
    q = st.session_state.questoes_respondidas
    xp = st.session_state.pontuacao_total
    streak = st.session_state.get('streak_atual', 0)
    horas = st.session_state.get('horas_acumuladas', 0)
    taxa = (st.session_state.questoes_certas / max(q,1)) * 100

    checks = [
        ("primeira_questao", q >= 1),
        ("questoes_100", q >= 100),
        ("questoes_1000", q >= 1000),
        ("primeiro_resumo", any(e['tipo']=='Resumo' for e in st.session_state.historico_estudos)),
        ("primeiro_plano", any(e['tipo']=='Plano' for e in st.session_state.historico_estudos)),
        ("primeiro_simulado", any(e['tipo']=='Simulado' for e in st.session_state.historico_estudos)),
        ("streak_7", streak >= 7),
        ("streak_30", streak >= 30),
        ("horas_100", horas >= 100),
        ("acerto_90", taxa >= 90 and q >= 20),
        ("nivel_elite", xp >= 1500),
        ("aprovado", xp >= 2500),
    ]
    for chave, condicao in checks:
        if condicao and chave not in conquistadas:
            conquistadas.append(chave)
            novas.append(chave)
    st.session_state['conquistas'] = conquistadas
    return novas

def calcular_indice_preparacao():
    q = st.session_state.questoes_respondidas
    xp = st.session_state.pontuacao_total
    streak = st.session_state.get('streak_atual', 0)
    horas = st.session_state.get('horas_acumuladas', 0)
    taxa = (st.session_state.questoes_certas / max(q,1)) * 100 if q > 0 else 0

    score = 0
    score += min(taxa * 0.35, 35)
    score += min((q / 500) * 25, 25)
    score += min((horas / 200) * 20, 20)
    score += min((streak / 30) * 10, 10)
    score += min((xp / 2000) * 10, 10)
    return int(min(score, 100))

def classificar_indice(idx):
    if idx >= 85: return "Elite", "Muito Alta", "#059669"
    if idx >= 70: return "Avançado", "Alta", "#16A34A"
    if idx >= 55: return "Intermediário", "Moderada", "#D97706"
    if idx >= 40: return "Básico", "Baixa", "#EA580C"
    return "Iniciante", "Muito Baixa", "#DC2626"

MOTIVACOES = [
    "Cada questão respondida hoje é um passo que seu concorrente não deu.",
    "A aprovação não acontece em um dia — ela acontece em cada dia.",
    "Disciplina é escolher, repetidamente, o que importa sobre o que é fácil.",
    "O estudo de hoje é o cargo de amanhã.",
    "Você não está competindo com os outros — está competindo com quem você era ontem.",
    "Consistência vence talento quando o talento não é consistente.",
    "Cada hora estudada reduz a distância entre você e a aprovação.",
    "A banca não mede esforço — mede domínio. Domine.",
    "O candidato que estuda agora é o servidor que comemora depois.",
    "Cansaço é temporário. Aprovação é permanente.",
]

# ─── PERSISTÊNCIA ───
CHAVES_SALVAR = [
    'usuario','historico_estudos','biblioteca_materiais',
    'concurso_foco','materias_foco','horas_disponiveis',
    'nivel_conhecimento','data_prova','cargo_foco','nota_necessaria',
    'dias_disponiveis','experiencia_anterior','maior_dificuldade',
    'maior_facilidade','metodo_preferido','instituicao',
    'pontuacao_total','questoes_respondidas','questoes_certas',
    'streak_atual','maior_streak','horas_acumuladas',
    'ultima_atividade','dias_estudo','conquistas',
    'radar_materias','missao_hoje','meta_semanal_h',
    'meta_semanal_q','horas_semana','questoes_semana',
    'historico_simulados',
]

def gerar_json_sessao():
    dados = {k: st.session_state.get(k) for k in CHAVES_SALVAR}
    dados['salvo_em'] = datetime.now().strftime('%d/%m/%Y %H:%M')
    return json.dumps(dados, ensure_ascii=False, indent=2, default=str)

def carregar_json_sessao(dados):
    _bloq = {'api_key','etapa','nome_login','chave_login','upload_login','btn_entrar_login'}
    _pref = (
        'btn_','sel_','ul_','dl_','cad_','_sub','_sm','_tab','_bsc',
        'ativo_','rem_','sel_pet_','ev_','prof_','hig_','prev_',
        'vac_','sint_','comp_','trad_','subs_','amb_','viag_','chat_',
        'duvida_','emerg_','peso_','data_','obs_','tipo_','vet_','desc_',
        'local_','prox_','alim','sit_emerg_','tc_','oraf','siau','agmag',
        'lv','mv','pt','pi','sh','wc','rv','rp','rc',
    )
    import re as _re
    for k, v in dados.items():
        if k in _bloq: continue
        if any(k.startswith(p) for p in _pref): continue
        if _re.match(r'.+_\\d+$', k): continue
        st.session_state[k] = v

def salvar_perfil_cache(u):
    _cache["perfis"][u] = {k: st.session_state.get(k) for k in CHAVES_SALVAR}

def perfis_salvos():
    return list(_cache["perfis"].keys())

def carregar_perfil_cache(u):
    return _cache["perfis"].get(u)

def salvar_estudo(tipo, materia, conteudo):
    st.session_state.historico_estudos.append({
        'data': datetime.now().strftime('%d/%m %H:%M'),
        'tipo': tipo, 'materia': materia, 'conteudo': conteudo,
    })
    st.session_state['ultima_atividade'] = f"{tipo} — {materia}"
    st.session_state['dias_estudo'] = st.session_state.get('dias_estudo', 0) + 1

def ganhar_xp(atividade: str, quantidade: int = 1):
    xp = XP_ATIVIDADES.get(atividade, 10) * quantidade
    st.session_state.pontuacao_total = st.session_state.get('pontuacao_total', 0) + xp
    novas = verificar_conquistas()
    return xp, novas

def atualizar_streak():
    hoje = date.today().isoformat()
    ultimo_dia = st.session_state.get('ultimo_dia_estudo', '')
    if ultimo_dia == hoje:
        return
    ontem = (date.today() - timedelta(days=1)).isoformat()
    if ultimo_dia == ontem:
        st.session_state.streak_atual = st.session_state.get('streak_atual', 0) + 1
    else:
        st.session_state.streak_atual = 1
    if st.session_state.streak_atual > st.session_state.get('maior_streak', 0):
        st.session_state.maior_streak = st.session_state.streak_atual
    st.session_state['ultimo_dia_estudo'] = hoje

# ─── DEFAULTS ───
defaults = {
    'etapa': "Login", 'usuario': "", 'api_key': "", 'pagina': "Home",
    'historico_estudos': [], 'biblioteca_materiais': [],
    'concurso_foco': "", 'materias_foco': "", 'horas_disponiveis': "2",
    'nivel_conhecimento': "Iniciante", 'data_prova': "", 'cargo_foco': "",
    'nota_necessaria': "", 'dias_disponiveis': "5", 'experiencia_anterior': "Nenhuma",
    'maior_dificuldade': "", 'maior_facilidade': "", 'metodo_preferido': "Misto",
    'instituicao': "",
    'pontuacao_total': 0, 'questoes_respondidas': 0, 'questoes_certas': 0,
    'streak_atual': 0, 'maior_streak': 0, 'horas_acumuladas': 0,
    'ultima_atividade': "Nenhuma", 'dias_estudo': 0, 'conquistas': [],
    'radar_materias': {}, 'missao_hoje': None, 'ultimo_dia_estudo': '',
    'meta_semanal_h': 10, 'meta_semanal_q': 100,
    'horas_semana': 0, 'questoes_semana': 0,
    'questoes_ativas': [], 'respondendo_idx': 0, 'respostas_sessao': [],
    'historico_simulados': [],
    'relampago_historico': [],
    'relampago_fase': 'menu',
    'relampago_tema': '',
    'relampago_modo': 'Desafio',
    'relampago_planejamento': {},
    'relampago_redacao': '',
    'relampago_aval_plano': '',
    'relampago_aval_redacao': '',
    'smc_fase': 'menu',
    'smc_questoes': [],
    'smc_respostas': {},
    'smc_inicio': 0,
    'smc_duracao': 3600,
    'smc_materia': '',
    'smc_n': 10,
    'smc_resultado': None,
    'smc_historico': [],

    'relampago_duracao': 0,
    'relampago_inicio': None,
    'simulado_ativo': False,
    'smc_escolha': None,
    'smc_idx': 0,
    'smc_vistas': None,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─── MOTOR DE IA ───
def tutor_ia(prompt: str, system_extra: str = "") -> str:
    try:
        client = Groq(api_key=st.session_state.api_key)
        perfil = (
            f"Aluno: {st.session_state.usuario}. "
            f"Concurso: {st.session_state.concurso_foco or 'não definido'}. "
            f"Cargo: {st.session_state.cargo_foco or 'não definido'}. "
            f"Nível: {st.session_state.nivel_conhecimento}. "
            f"Matérias foco: {st.session_state.materias_foco or 'não definidas'}. "
            f"Maior dificuldade: {st.session_state.maior_dificuldade or 'não informada'}. "
            f"Método preferido: {st.session_state.metodo_preferido}. "
            f"Índice de preparação: {calcular_indice_preparacao()}%. "
            f"XP: {st.session_state.pontuacao_total}. "
            f"Taxa de acerto: {int(st.session_state.questoes_certas/max(st.session_state.questoes_respondidas,1)*100)}%."
        )
        system = (
            f"Você é o Tutor de Concursos IA — um mentor estratégico de preparação para concursos públicos brasileiros.  REGRA DE OURO — CONFIABILIDADE 100%%: Forneça APENAS informações que você tem certeza absoluta que são verdadeiras. JAMAIS invente, suponha, extrapole ou preencha lacunas com dados fictícios. Se não souber algo com certeza — preço, endereço, horário, nome, estatística, lei, fato — diga EXPLICITAMENTE: 'Não tenho certeza sobre isso, recomendo verificar em [fonte].' É melhor uma resposta incompleta e honesta do que uma resposta completa e inventada. O usuário depende dessas informações para tomar decisões reais. "
            f"Você acompanha toda a jornada do aluno, identifica padrões, explica o raciocínio por trás de cada decisão "
            f"e mantém o foco no objetivo final: a aprovação. "
            f"Sempre baseie conselhos no perfil real do aluno. Nunca seja genérico. "
            f"Português do Brasil. {perfil} {system_extra}"
        )
        response = client.chat.completions.create(
            messages=[{"role":"system","content":system},{"role":"user","content":prompt}],
            model="openai/gpt-oss-120b",
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Erro na API: {e}"

# ─── BARRA SALVAR ───
def barra_salvar():
    salvar_perfil_cache(st.session_state.usuario)
    nome_u = st.session_state.usuario.lower().replace(' ','_') or 'sessao'
    col_info, col_btn = st.columns([4, 2])
    with col_info:
        xp = st.session_state.pontuacao_total
        _, nivel_nome, nivel_emoji = calcular_nivel(xp)
        concurso = st.session_state.concurso_foco or "—"
        st.markdown(
            f"<div style='background:#FFFBEB;border:1px solid #FCD34D;border-radius:10px;"
            f"padding:10px 14px;font-size:0.84em;color:#1A1A2E;line-height:1.6;'>"
            f"💾 <strong>Salve seus dados antes de sair.</strong><br>"
            f"<span style='color:#D97706;font-size:0.88em;'>{nivel_emoji} {nivel_nome} · "
            f"{xp} XP · {concurso}</span>"
            f"</div>", unsafe_allow_html=True)
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown(\"\"\"<style>
    .dica-nav{font-size:0.72em;color:#94A3B8;text-align:center;padding:2px 0 6px;}
    .dica-mobile{display:none;}
    .dica-desktop{display:block;}
    @media(max-width:768px){.dica-mobile{display:block;}.dica-desktop{display:none;}}
    </style>
    <div class='dica-nav dica-mobile'>👆 Deslize o dedo para navegar entre as abas</div>
    <div class='dica-nav dica-desktop'>📋 Clique no ícone acima para abrir o menu completo</div>
    \"\"\", unsafe_allow_html=True)


# ============================================================
# LOGIN
# ============================================================
if 'biblioteca_materiais' not in st.session_state: st.session_state['biblioteca_materiais'] = None
if 'cargo_foco' not in st.session_state: st.session_state['cargo_foco'] = None
if 'concurso_foco' not in st.session_state: st.session_state['concurso_foco'] = None
if 'data_prova' not in st.session_state: st.session_state['data_prova'] = None
if 'dias_disponiveis' not in st.session_state: st.session_state['dias_disponiveis'] = 0
if 'experiencia_anterior' not in st.session_state: st.session_state['experiencia_anterior'] = None
if 'historico_estudos' not in st.session_state: st.session_state['historico_estudos'] = []
if 'horas_acumuladas' not in st.session_state: st.session_state['horas_acumuladas'] = None
if 'horas_disponiveis' not in st.session_state: st.session_state['horas_disponiveis'] = None
if 'horas_semana' not in st.session_state: st.session_state['horas_semana'] = 0
if 'instituicao' not in st.session_state: st.session_state['instituicao'] = None
if 'maior_dificuldade' not in st.session_state: st.session_state['maior_dificuldade'] = None
if 'maior_facilidade' not in st.session_state: st.session_state['maior_facilidade'] = None
if 'maior_streak' not in st.session_state: st.session_state['maior_streak'] = None
if 'materias_foco' not in st.session_state: st.session_state['materias_foco'] = None
if 'meta_semanal_h' not in st.session_state: st.session_state['meta_semanal_h'] = 0
if 'metodo_preferido' not in st.session_state: st.session_state['metodo_preferido'] = None
if 'missao_hoje' not in st.session_state: st.session_state['missao_hoje'] = None
if 'nivel_conhecimento' not in st.session_state: st.session_state['nivel_conhecimento'] = None
if 'nota_necessaria' not in st.session_state: st.session_state['nota_necessaria'] = None
if 'pontuacao_total' not in st.session_state: st.session_state['pontuacao_total'] = 0
if 'questoes_certas' not in st.session_state: st.session_state['questoes_certas'] = []
if 'questoes_respondidas' not in st.session_state: st.session_state['questoes_respondidas'] = []
if 'questoes_semana' not in st.session_state: st.session_state['questoes_semana'] = []
if 'radar_materias' not in st.session_state: st.session_state['radar_materias'] = None
if 'relampago_aval_redacao' not in st.session_state: st.session_state['relampago_aval_redacao'] = None
if 'relampago_duracao' not in st.session_state: st.session_state['relampago_duracao'] = None
if 'relampago_fase' not in st.session_state: st.session_state['relampago_fase'] = None
if 'relampago_inicio' not in st.session_state: st.session_state['relampago_inicio'] = None
if 'relampago_redacao' not in st.session_state: st.session_state['relampago_redacao'] = None
if 'relampago_tema' not in st.session_state: st.session_state['relampago_tema'] = None
if 'simulado_ativo' not in st.session_state: st.session_state['simulado_ativo'] = False
if 'smc_duracao' not in st.session_state: st.session_state['smc_duracao'] = None
if 'smc_escolha' not in st.session_state: st.session_state['smc_escolha'] = None
if 'smc_fase' not in st.session_state: st.session_state['smc_fase'] = None
if 'smc_historico' not in st.session_state: st.session_state['smc_historico'] = []
if 'smc_idx' not in st.session_state: st.session_state['smc_idx'] = 0
if 'smc_inicio' not in st.session_state: st.session_state['smc_inicio'] = None
if 'smc_materia' not in st.session_state: st.session_state['smc_materia'] = None
if 'smc_questoes' not in st.session_state: st.session_state['smc_questoes'] = []
if 'smc_respostas' not in st.session_state: st.session_state['smc_respostas'] = {}
if 'smc_resultado' not in st.session_state: st.session_state['smc_resultado'] = None
if 'smc_vistas' not in st.session_state: st.session_state['smc_vistas'] = None
if 'streak_atual' not in st.session_state: st.session_state['streak_atual'] = None

if 'historico_redacoes' not in st.session_state: st.session_state['historico_redacoes'] = []
if 'quiz_banco' not in st.session_state: st.session_state['quiz_banco'] = []
if 'quiz_idx' not in st.session_state: st.session_state['quiz_idx'] = 0
if 'quiz_acertos' not in st.session_state: st.session_state['quiz_acertos'] = 0
if 'quiz_erros' not in st.session_state: st.session_state['quiz_erros'] = []
if 'quiz_respondida' not in st.session_state: st.session_state['quiz_respondida'] = False
if 'quiz_resposta_atual' not in st.session_state: st.session_state['quiz_resposta_atual'] = None
if 'historico_simulados' not in st.session_state: st.session_state['historico_simulados'] = []
if 'red_ativo' not in st.session_state: st.session_state['red_ativo'] = False

if st.session_state.etapa == "Login":
    st.markdown("# 🤖 TUTOR DE CONCURSOS IA")
    st.markdown("<div class=\\'card\\'><b>🔒 ACESSO RESTRITO A CLIENTES DO MEUSAGENTESIA.COM.BR</b><br>🔗 <a href='https://meusagentesia.com.br' target='_blank' style='color:#4F46E5;font-weight:700;text-decoration:underline;'>meusagentesia.com.br</a></div>", unsafe_allow_html=True)
    st.info("💻 **Dica:** Pela complexidade dos agentes, no computador a experiência é mais agradável.")
    with st.container():
        nome  = st.text_input("Seu Nome:", key="nome_login")
        chave = st.text_input("🔑 Sua Chave API da Groq:", type="password", key="chave_login")
        if st.button("✨ ENTRAR", key="btn_entrar_login"):
            if len(nome.strip()) < 2:
                st.warning("Digite um nome com pelo menos 2 caracteres.")
            elif chave.strip():
                st.session_state.usuario = nome.strip()
                st.session_state.api_key = chave
                st.session_state.etapa = "App"
                st.rerun()
            else:
                st.warning("Preencha nome e chave API.")

elif st.session_state.etapa == "App":

    atualizar_streak()


    # TABS — navegação nativa
    (_tab_Home, _tab_Questoes, _tab_Redacao, _tab_Simulado, _tab_Cronograma, _tab_Flashcards, _tab_Progresso, _tab_Legislacao, _tab_Informatica, _tab_Portugues, _tab_Matematica, _tab_Atualidades, _tab_DirConst, _tab_DirAdmin, _tab_Logico, _tab_DirPenal, _tab_DirProc, _tab_Bancario, _tab_Contabil, _tab_Geo, _tab_Hist, _tab_Especifico) = st.tabs(['🏠 Painel', '📝 Questões', '✍️ Redação', '🎯 Simulado', '📅 Cronograma', '🃏 Flashcards', '📈 Progresso', '⚖️ Legislação', '💻 Informática', '📖 Português', '🔢 Matemática', '📰 Atualidades', '📜 Dir. Constitucional', '🏛️ Dir. Administrativo', '🧠 Raciocínio Lógico', '🚔 Dir. Penal', '⚖️ Dir. Processual', '💰 Conh. Bancários', '📊 Contabilidade', '🌍 Geografia', '🕰️ História', '🎯 Conh. Específicos'])

    # ── BARRA SALVAR — aparece em todas as abas ──
    with st.expander("💾 Salvar / Carregar meus dados", expanded=False):
        _bsc1, _bsc2 = st.columns(2)
        with _bsc1:
            import json as _jsv
            _dsv = {k: st.session_state.get(k) for k in list(st.session_state.keys()) if not k.startswith('_') and k not in ('api_key',)}
    with _tab_Home:
        col_u, col_r = st.columns([3,1])
        with col_u:
            st.title(f"🎓 Olá, {st.session_state.usuario}!")
            concurso = st.session_state.concurso_foco or "Não definido"
            xp = st.session_state.pontuacao_total
            _, nivel_nome, nivel_emoji = calcular_nivel(xp)
            st.markdown(f"<span class='badge'>{nivel_emoji} {nivel_nome}</span> <span class='badge-azul'>🎯 {concurso}</span>", unsafe_allow_html=True)
        with col_r:
            if st.button("🚪 Sair", key="tutorcon3"):
                for k in list(st.session_state.keys()):
                    del st.session_state[k]
                st.rerun()

        if not st.session_state.concurso_foco:
            st.markdown(\"\"\"<div style="background:#FFFBEB;border:2px solid #F59E0B;border-radius:12px;
            padding:16px 20px;margin-bottom:16px;">
            <span style='font-size:1em;font-weight:600;color:#92400E;'>
            ⚡ Comece pelo 📋 Perfil — configure seu concurso, matérias e data da prova para ativar todos os recursos.
            </span></div>\"\"\", unsafe_allow_html=True)
        else:
            pass
            # RECUPERAR BACKUP
        # CABEÇALHO INSTITUCIONAL
        dias_restantes = "—"
        if st.session_state.data_prova:
            try:
                dp = datetime.strptime(st.session_state.data_prova, "%Y-%m-%d").date()
                dias_restantes = (dp - date.today()).days
                if dias_restantes < 0:
                    dias_restantes = "Prova passada"
            except Exception:
                dias_restantes = "—"

        ultima = st.session_state.get('ultima_atividade', 'Nenhuma')
        st.markdown(f\"\"\"
        <div class='painel-exec'>
            <div style='font-size:0.85em;opacity:0.7;letter-spacing:2px;margin-bottom:8px;'>🎓 MENTOR INTELIGENTE DE ESTUDOS</div>
            <div style='font-size:1.1em;opacity:0.7;margin-bottom:16px;'>Seu treinador pessoal com Inteligência Artificial · <span style='color:#22C55E;'>🟢 IA Online</span></div>
            <div style='display:flex;flex-wrap:wrap;gap:20px;'>
                <div><div style='font-size:0.75em;opacity:0.6;'>🎯 OBJETIVO</div><div style='font-size:1.1em;font-weight:700;'>{st.session_state.concurso_foco or "—"} {("— " + st.session_state.cargo_foco) if st.session_state.cargo_foco else ""}</div></div>
                <div><div style='font-size:0.75em;opacity:0.6;'>📅 DIAS RESTANTES</div><div style='font-size:1.1em;font-weight:700;'>{dias_restantes}</div></div>
                <div><div style='font-size:0.75em;opacity:0.6;'>🔥 SEQUÊNCIA</div><div style='font-size:1.1em;font-weight:700;'>{st.session_state.get("streak_atual",0)} dias</div></div>
                <div><div style='font-size:0.75em;opacity:0.6;'>📖 ÚLTIMA ATIVIDADE</div><div style='font-size:1.1em;font-weight:700;'>{ultima}</div></div>
            </div>
        </div>
        \"\"\", unsafe_allow_html=True)

        # ÍNDICE DE PREPARAÇÃO
        idx = calcular_indice_preparacao()
        nivel_idx, prob, cor = classificar_indice(idx)
        col_idx, col_mot = st.columns([1, 2])
        with col_idx:
            st.markdown(f\"\"\"
            <div class='indice-box'>
                <div style='font-size:0.85em;opacity:0.8;'>ÍNDICE DE PREPARAÇÃO</div>
                <div class='indice-numero'>{idx}%</div>
                <div style='font-size:0.9em;'>Nível: <strong>{nivel_idx}</strong></div>
                <div style='font-size:0.85em;opacity:0.8;'>Prob. estimada: {prob}</div>
            </div>
            \"\"\", unsafe_allow_html=True)
        with col_mot:
            frase_mot = random.choice(MOTIVACOES)
            streak = st.session_state.get('streak_atual', 0)
            if streak > 0:
                frase_mot = f"Você está há {streak} dias consecutivos estudando. {frase_mot}"
            st.markdown(f"<div class='card' style='height:120px;display:flex;align-items:center;'><em>💡 {frase_mot}</em></div>", unsafe_allow_html=True)

        # DASHBOARD
        st.markdown("### 📊 Dashboard")
        q = st.session_state.questoes_respondidas
        c_q = st.session_state.questoes_certas
        e_q = q - c_q
        taxa = int(c_q/max(q,1)*100)
        xp = st.session_state.pontuacao_total
        horas = st.session_state.get('horas_acumuladas', 0)
        resumos = sum(1 for e in st.session_state.historico_estudos if e['tipo']=='Resumo')
        flashcards = sum(1 for e in st.session_state.historico_estudos if e['tipo']=='Flashcard')
        simulados = sum(1 for e in st.session_state.historico_estudos if e['tipo']=='Simulado')
        cronogramas = sum(1 for e in st.session_state.historico_estudos if e['tipo']=='Plano')

        d1,d2,d3,d4,d5,d6 = st.columns(6)
        d1.markdown(f"<div class='stat-box'><div class='stat-numero'>{st.session_state.get('streak_atual',0)}</div><div>Dias seguidos</div></div>", unsafe_allow_html=True)
        d2.markdown(f"<div class='stat-box'><div class='stat-numero'>{horas:.0f}h</div><div>Horas acumuladas</div></div>", unsafe_allow_html=True)
        d3.markdown(f"<div class='stat-box'><div class='stat-numero'>{q}</div><div>Questões</div></div>", unsafe_allow_html=True)
        d4.markdown(f"<div class='stat-box'><div class='stat-numero'>{taxa}%</div><div>Acertos</div></div>", unsafe_allow_html=True)
        d5.markdown(f"<div class='stat-box'><div class='stat-numero'>{resumos}</div><div>Resumos</div></div>", unsafe_allow_html=True)
        d6.markdown(f"<div class='stat-box'><div class='stat-numero'>{xp}</div><div>XP Total</div></div>", unsafe_allow_html=True)

        d7,d8,d9,d10,d11,d12 = st.columns(6)
        d7.markdown(f"<div class='stat-box'><div class='stat-numero'>{flashcards}</div><div>Flashcards</div></div>", unsafe_allow_html=True)
        d8.markdown(f"<div class='stat-box'><div class='stat-numero'>{simulados}</div><div>Simulados</div></div>", unsafe_allow_html=True)
        d9.markdown(f"<div class='stat-box'><div class='stat-numero'>{cronogramas}</div><div>Planos</div></div>", unsafe_allow_html=True)
        d10.markdown(f"<div class='stat-box'><div class='stat-numero'>{c_q}</div><div>Certas</div></div>", unsafe_allow_html=True)
        d11.markdown(f"<div class='stat-box'><div class='stat-numero'>{e_q}</div><div>Erradas</div></div>", unsafe_allow_html=True)
        d12.markdown(f"<div class='stat-box'><div class='stat-numero'>{st.session_state.get('maior_streak',0)}</div><div>Recorde dias</div></div>", unsafe_allow_html=True)

        # MISSÃO DO DIA
        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        col_miss, col_meta = st.columns(2)
        with col_miss:
            st.markdown("### ⚡ Missão do Dia")
            if not st.session_state.get('missao_hoje'):
                if st.button("⚡ GERAR MISSÃO DO DIA", key="tutorcon4"):
                    with st.spinner("Gerando missão personalizada..."):
                        materia_critica = st.session_state.maior_dificuldade or st.session_state.materias_foco or "a matéria mais importante do seu concurso"
                        missao_prompt = (
                            f"Crie uma missão de estudo para hoje para o aluno preparando {st.session_state.concurso_foco or 'concurso público'}.\\n"
                            f"Horas disponíveis: {st.session_state.horas_disponiveis}h. Maior dificuldade: {materia_critica}.\\n"
                            f"Formato:\\n\\n"
                            f"⚡ MISSÃO DO DIA\\n\\n"
                            f"[3-4 tarefas específicas com tempo estimado cada]\\n\\n"
                            f"⏱️ Tempo total previsto: [X]h[Y]min\\n"
                            f"🏆 Recompensa: +[XP] XP\\n\\n"
                            f"💡 Por que essa missão hoje: [1 linha explicando a estratégia]"
                        )
                        missao = tutor_ia(missao_prompt)
                        if missao: st.session_state['res_home_tutorc1'] = str(missao)
                        st.session_state.missao_hoje = missao
                        st.rerun()
            else:
                st.markdown(f"<div class='missao-box'>{st.session_state.missao_hoje}</div>", unsafe_allow_html=True)
                col_ok, col_re = st.columns(2)
                with col_ok:
                    if st.button("✅ MISSÃO CONCLUÍDA!", key="missao_ok"):
                        xp_g, novas = ganhar_xp('missao_dia')
                        st.success(f"🏆 +{xp_g} XP! Excelente trabalho!")
                        st.session_state.missao_hoje = None
                        st.rerun()
                with col_re:
                    if st.button("🔄 Nova missão", key="missao_re"):
                        st.session_state.missao_hoje = None
                        st.rerun()

        with col_meta:
            st.markdown("### 📆 Meta Semanal")
            h_prev = st.session_state.get('meta_semanal_h', 10)
            h_feito = st.session_state.get('horas_semana', 0)
            q_prev = st.session_state.get('meta_semanal_q', 100)
            q_feito = st.session_state.get('questoes_semana', 0)
            pct_h = min(int(h_feito/max(h_prev,1)*100), 100)
            pct_q = min(int(q_feito/max(q_prev,1)*100), 100)
            st.markdown(f"**⏱️ Horas:** {h_feito}/{h_prev}h ({pct_h}%)")
            st.progress(pct_h/100)
            st.markdown(f"**❓ Questões:** {q_feito}/{q_prev} ({pct_q}%)")
            st.progress(pct_q/100)
            col_ma, col_mb = st.columns(2)
            with col_ma:
                if st.button("➕ +1h estudada", key="tutorcon5"):
                    st.session_state.horas_semana = h_feito + 1
                    st.session_state.horas_acumuladas = st.session_state.get('horas_acumuladas',0) + 1
                    st.rerun()
            with col_mb:
                if st.button("⚙️ Definir metas", key="def_metas"):
                    st.session_state.pagina = "Progresso"; st.rerun()

        # ÚLTIMAS ATIVIDADES
        if st.session_state.historico_estudos:
            st.markdown("<hr class='divider'>", unsafe_allow_html=True)
            st.markdown("### 🕐 Últimas Atividades")
            for item in reversed(st.session_state.historico_estudos[-4:]):
                st.markdown(f"<div class='hist-item'><span class='badge'>{item['tipo']}</span> <small style='color:#888'>{item['data']}</small><br><small>{item.get('materia', '')[:80]}</small></div>", unsafe_allow_html=True)


        # ──────────────────────────────────────────
        # PAINEL EXECUTIVO
        # ──────────────────────────────────────────

        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        st.markdown("### 💾 Salvar e Carregar Dados")
        _csl1, _csl2 = st.columns(2)
        with _csl1:
            import json as _json_sv
            _dados_sv = {k: st.session_state.get(k) for k in list(st.session_state.keys()) if not k.startswith('_')}
    with _tab_Questoes:
        st.header("❓ Simulado de Questões")
        st.markdown("Questões no estilo da banca — com gabarito comentado e explicação detalhada.")

        col1, col2 = st.columns(2)
        with col1:
            materia_q  = st.text_input("Matéria:", placeholder="ex: Português, Matemática, Direito...", key="tutorcon30")
            tema_q     = st.text_input("Tema:", placeholder="ex: Análise Sintática, Regra de Três, CF/88...", key="tutorcon31")
            concurso_q = st.text_input("Estilo de banca:", value=st.session_state.concurso_foco,
                placeholder="ex: CESPE, FCC, Vunesp, ENEM...", key="tutorcon14_d2")
        with col2:
            qtd_q   = st.slider("Quantidade de questões:", 3, 10, 5, key="tutorcon1")
            nivel_q = st.selectbox("Nível de dificuldade:", ["Fácil","Médio","Difícil","Misto"], key="tutorcon32")
            tipo_q  = st.radio("Tipo:", ["Múltipla escolha (A-E)","Certo ou Errado"], horizontal=True, key="tutorcon33")

        if st.button("❓ GERAR SIMULADO", key="tutorcon34"):
            if materia_q.strip():
                with st.spinner("Gerando suas questões..."):
                    estilo = "no estilo CERTO ou ERRADO" if "Certo" in tipo_q else "de múltipla escolha com 5 alternativas (A, B, C, D, E)"
                    prompt = (
                        f"Crie {qtd_q} questões {estilo} sobre '{tema_q or materia_q}' da matéria {materia_q}.\\n"
                        f"Banca/estilo: {concurso_q}. Nível: {nivel_q}.\\n\\n"
                        f"Para CADA questão use EXATAMENTE este formato:\\n\\n"
                        f"QUESTÃO [N]\\n"
                        f"[Enunciado da questão]\\n"
                        + ("[A) opção\\nB) opção\\nC) opção\\nD) opção\\nE) opção\\n" if "múltipla" in tipo_q else "[  ] CERTO  [  ] ERRADO\\n")
                        + f"GABARITO: [letra ou CERTO/ERRADO]\\n"
                        f"EXPLICAÇÃO: [resolução detalhada — por que o gabarito está certo e por que as outras estão erradas]\\n"
                        f"DICA: [macete para não errar esse tipo de questão]\\n\\n"
                        f"---\\n\\n"
                        f"REGRAS:\\n"
                        f"- Questões realistas, no estilo de provas reais\\n"
                        f"- Varie os assuntos dentro do tema\\n"
                        f"- Inclua pelo menos 1 pegadinha típica de banca\\n"
                        f"- Explicações claras e educativas"
                    )
                    res = tutor_ia(prompt)
                    if res: st.session_state['res_questoes_tutorc2'] = str(res)
                    salvar_estudo("Simulado", f"{materia_q} — {tema_q}", res)
                    st.session_state.questoes_respondidas += qtd_q
                    st.session_state['simulado_temp'] = res
                    st.markdown(f"<div class='card-purple'>{res}</div>", unsafe_allow_html=True)
            else:
                st.warning("Preencha a matéria antes de gerar o simulado.")

        if st.session_state.get('simulado_temp'):
            col_acerto, col_dl, col_sv = st.columns(3)
            with col_acerto:
                acertos_input = st.number_input("Quantas você acertou?", min_value=0, max_value=qtd_q if 'qtd_q' in dir() else 10, value=0, key="tutorcon35")
                if st.button("✅ Registrar acertos", key="tutorcon36"):
                    st.session_state.questoes_certas += acertos_input
                    st.success(f"✅ {acertos_input} acertos registrados! Taxa geral: {round(st.session_state.questoes_certas/max(1,st.session_state.questoes_respondidas)*100)}%")
            with col_dl:
                st.download_button("📋 Baixar simulado (.txt)", data=st.session_state['simulado_temp'],
                    file_name="simulado.txt", mime="text/plain", use_container_width=True, key="tutorcon13_d2")
            with col_sv:
                if st.button("💾 Salvar na Biblioteca", key="sv_sim", use_container_width=True):
                    st.session_state.biblioteca_materiais.append({
                        'tipo': 'Simulado', 'materia': f"{materia_q} — {tema_q}",
                        'conteudo': st.session_state['simulado_temp'],
                        'data': datetime.now().strftime('%d/%m %H:%M'),
                    })
                    st.success("✅ Salvo!")

        # ========================
        # TÉCNICAS DE MEMORIZAÇÃO
        # ========================

    with _tab_Redacao:
        st.header("✍️ Redação para Concursos")
        _aba_r1, _aba_r2 = st.tabs(["📚 Como Fazer", "⏱️ Prática Cronometrada"])

        with _aba_r1:
            st.markdown("### 📚 Guia de Redação para Concursos")
            _tipo_guia = st.selectbox("Tipo:", ["Dissertativo-argumentativa","Carta argumentativa","Redação administrativa"], key="tc_tipo_guia")
            if st.button("📚 GERAR GUIA", key="tc_btn_guia", use_container_width=True):
                with st.spinner("Gerando guia..."):
                    try:
                        from groq import Groq as _Gr1
                        _r1 = _Gr1(api_key=st.session_state.api_key).chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[{"role":"user","content":f"Crie um guia completo de redação {_tipo_guia} para concursos públicos. Inclua: estrutura, técnicas de argumentação, critérios das bancas, erros comuns e exemplo comentado."}],
                            max_tokens=2500
                        )
                        st.markdown(f"<div class='card'>{_r1.choices[0].message.content}</div>", unsafe_allow_html=True)
                    except Exception as _e1: st.error(f"Erro: {_e1}")

        with _aba_r2:
            import time as _tm

            # ── ETAPA 1: Gerar tema ──
            if not st.session_state.get('red_ativo') and not st.session_state.get('red_entregue'):
                st.markdown("### 🎯 Prática Cronometrada")
                st.markdown("A IA sorteia um tema de concurso. Escreva sua redação e clique em **Finalizar** quando terminar — a IA analisa o texto e o tempo que você levou.")
                _banca = st.selectbox("Banca:", ["CESPE/CEBRASPE","FCC","VUNESP","FGV","Qualquer"], key="tc_banca_red")
                if st.button("🎲 GERAR TEMA E INICIAR", key="tc_iniciar_red", use_container_width=True):
                    with st.spinner("Sorteando tema..."):
                        try:
                            from groq import Groq as _Gr2
                            import random as _rnd
                            _area = _rnd.choice(['segurança pública','meio ambiente','educação','saúde',
                                'tecnologia e sociedade','desigualdade social','mobilidade urbana',
                                'trabalho e emprego','direitos humanos','sustentabilidade',
                                'cultura e identidade','economia digital','envelhecimento populacional',
                                'violência doméstica','acesso à justiça'])
                            _r2 = _Gr2(api_key=st.session_state.api_key).chat.completions.create(
                                model="openai/gpt-oss-120b",
                                messages=[{"role":"user","content":f"Gere um tema inédito de redação para concurso público banca {_banca} sobre {_area}. Inclua: TEMA (1 linha em negrito), CONTEXTO (2-3 linhas) e PROPOSTA DE REDAÇÃO (o que o candidato deve escrever). Seja objetivo."}],
                                max_tokens=500
                            )
                            st.session_state['red_tema']     = _r2.choices[0].message.content
                            st.session_state['red_inicio']   = _tm.time()
                            st.session_state['red_ativo']    = True
                            st.session_state['red_entregue'] = False
                            st.session_state['red_texto']    = ''
                            st.session_state['red_correcao'] = ''
                            st.rerun()
                        except Exception as _e2: st.error(f"Erro: {_e2}")

            # ── ETAPA 2: Escrever ──
            elif st.session_state.get('red_ativo') and not st.session_state.get('red_entregue'):
                # Timer via JS usando components — roda no browser sem rerun
                import streamlit.components.v1 as _comp
                _inicio_ts = int(st.session_state.get('red_inicio', _tm.time()) * 1000)
                _comp.html(f\"\"\"
                <div style="text-align:center;font-size:2em;font-weight:700;color:#64748B;
                     background:#F8F9FA;border-radius:10px;padding:8px;margin-bottom:4px;
                     font-family:monospace;">
                  ⏱️ <span id="tv">00:00</span>
                </div>
                <script>
                var s0 = {_inicio_ts};
                function tick(){{
                    var e = Math.floor((Date.now()-s0)/1000);
                    var m = Math.floor(e/60), ss = e%60;
                    var el = document.getElementById('tv');
                    if(el) el.textContent=(m<10?'0':'')+m+':'+(ss<10?'0':'')+ss;
                }}
                tick(); setInterval(tick,500);
                </script>
                \"\"\", height=70)
                _elapsed = int(_tm.time() - st.session_state.get('red_inicio', _tm.time()))

                with st.expander("📋 Tema", expanded=True):
                    st.markdown(st.session_state.get('red_tema',''))

                _texto = st.text_area(
                    "✍️ Escreva sua redação:",
                    height=380,
                    value=st.session_state.get('red_texto',''),
                    key="tc_texto_red",
                    placeholder="Escreva aqui sua redação..."
                )
                st.session_state['red_texto'] = _texto

                # Contador de palavras em tempo real via JS
                st.markdown(\"\"\"<div id="wc-bar" style="font-size:0.83em;color:#64748B;margin:-8px 0 12px 2px;">📝 <span id="wc-n">0</span> palavras</div>
                <script>(function(){function cnt(){var a=window.parent.document.querySelectorAll('textarea'),t=null;
                for(var i=0;i<a.length;i++){if(a[i].value.length>5){t=a[i];break;}}
                if(!t)t=a[a.length-1];if(t){var v=t.value.trim();
                var n=v===''?0:v.split(/[ \\t\\n\\r]+/).filter(function(w){return w.length>0;}).length;
                var el=document.getElementById('wc-n');if(el)el.textContent=n;}}
                setInterval(cnt,300);window.parent.document.addEventListener('input',cnt);})();
                </script>\"\"\", unsafe_allow_html=True)

                st.markdown("<hr style='margin:8px 0'>", unsafe_allow_html=True)

                if st.button("✅ FINALIZAR E RECEBER NOTA", key="tc_finalizar_red", use_container_width=True):
                    if _texto.strip():
                        st.session_state['red_tempo_total'] = _elapsed
                        st.session_state['red_ativo']       = False
                        st.session_state['red_entregue']    = True
                        st.rerun()
                    else:
                        st.warning("Escreva algo antes de finalizar.")

            # ── ETAPA 3: Nota e análise ──
            elif st.session_state.get('red_entregue'):
                _texto_final = st.session_state.get('red_texto','').strip()
                _tema_final  = st.session_state.get('red_tema','')
                _tempo_seg   = st.session_state.get('red_tempo_total', 0)
                _mins_f      = _tempo_seg // 60
                _segs_f      = _tempo_seg % 60

                st.success(f"✅ Redação finalizada em **{_mins_f}min {_segs_f}s**")

                if not st.session_state.get('red_correcao'):
                    with st.spinner("📊 Analisando sua redação..."):
                        try:
                            from groq import Groq as _Gr3
                            _palavras = len(_texto_final.split())
                            _corr = _Gr3(api_key=st.session_state.api_key).chat.completions.create(
                                model="openai/gpt-oss-120b",
                                messages=[{"role":"user","content":f\"\"\"Você é corretor oficial de concurso público. Avalie a redação abaixo.

TEMA:
{_tema_final}

REDAÇÃO ({_palavras} palavras, tempo: {_mins_f}min {_segs_f}s):
{_texto_final}

Forneça a análise completa:

📊 NOTA FINAL: __/100

Critérios (0-20 cada):
• Adequação ao tema: __/20
• Estrutura e coesão: __/20  
• Qualidade dos argumentos: __/20
• Domínio da norma culta: __/20
• Proposta de intervenção: __/20

⏱️ ANÁLISE DO TEMPO: Comente se {_mins_f} minutos foi adequado para {_palavras} palavras e o nível de elaboração apresentado.

✅ PONTOS FORTES: (liste 2-3)

❌ ERROS: (cite trechos exatos e corrija)

💡 RECOMENDAÇÕES: (3 dicas práticas para próxima redação)

📈 PARECER FINAL: (1 parágrafo honesto e motivador)\"\"\"}],
                                max_tokens=2000
                            ).choices[0].message.content
                            st.session_state['red_correcao'] = _corr
                            if 'historico_redacoes' not in st.session_state:
                                st.session_state['historico_redacoes'] = []
                            import datetime as _dt
                            st.session_state['historico_redacoes'].append({
                                'data':    _dt.datetime.now().strftime('%d/%m %H:%M'),
                                'tema':    _tema_final[:80],
                                'tempo':   f"{_mins_f}min {_segs_f}s",
                                'palavras': _palavras,
                                'correcao': _corr
                            })
                            st.rerun()
                        except Exception as _e3: st.error(f"Erro: {_e3}")
                else:
                    st.markdown(f"<div class='card'>{st.session_state['red_correcao']}</div>", unsafe_allow_html=True)
                    st.download_button("📥 Baixar correção", data=st.session_state['red_correcao'], file_name="correcao_redacao.txt", key="tc_dl_corr")

                if st.button("🔄 Nova Redação", key="tc_nova_red", use_container_width=True):
                    for _k in ['red_ativo','red_entregue','red_tema','red_inicio','red_texto','red_correcao','red_tempo_total']:
                        st.session_state.pop(_k, None)
                    st.rerun()

                if st.session_state.get('historico_redacoes'):
                    with st.expander(f"📊 Histórico ({len(st.session_state['historico_redacoes'])} redações)"):
                        for _item in reversed(st.session_state['historico_redacoes'][-5:]):
                            st.markdown(f"**{_item.get('data','')}** — {_item.get('tema','')[:50]}... — {_item.get('tempo','')} — {_item.get('palavras',0)} palavras")

    with _tab_Simulado:
        st.header("🎯 Simulado — Quiz de Concurso")
        st.markdown("*Questões no estilo de banca, com placar e histórico de acertos.*")

        if 'quiz_banco' not in st.session_state: st.session_state['quiz_banco'] = []
        if 'quiz_idx' not in st.session_state: st.session_state['quiz_idx'] = 0
        if 'quiz_acertos' not in st.session_state: st.session_state['quiz_acertos'] = 0
        if 'quiz_erros' not in st.session_state: st.session_state['quiz_erros'] = []
        if 'quiz_respondida' not in st.session_state: st.session_state['quiz_respondida'] = False
        if 'quiz_resposta_atual' not in st.session_state: st.session_state['quiz_resposta_atual'] = None
        if 'historico_simulados' not in st.session_state: st.session_state['historico_simulados'] = []

        _tab_quiz1, _tab_quiz2 = st.tabs(["🎯 Simulado", "📊 Meu Desempenho"])

        with _tab_quiz1:
            if not st.session_state['quiz_banco']:
                # Configurar simulado
                _col1, _col2 = st.columns(2)
                with _col1:
                    _mat_quiz = st.text_input("Matéria:", placeholder="ex: Português, Direito Constitucional...", key="tc_quiz_mat")
                    _banca_quiz = st.selectbox("Banca:", ["CESPE/CEBRASPE","FCC","VUNESP","FGV","IBFC","Qualquer"], key="tc_quiz_banca")
                with _col2:
                    _qtd_quiz = st.selectbox("Quantidade de questões:", [5, 10, 15, 20], index=1, key="tc_quiz_qtd")
                    _nivel_quiz = st.selectbox("Nível:", ["Fácil","Médio","Difícil","Misto"], index=1, key="tc_quiz_nivel")

                if st.button("🚀 INICIAR SIMULADO", key="tc_quiz_iniciar", use_container_width=True):
                    if _mat_quiz.strip():
                        with st.spinner(f"Gerando {_qtd_quiz} questões de {_mat_quiz}..."):
                            try:
                                from groq import Groq as _GrQ
                                _cli = _GrQ(api_key=st.session_state.api_key)
                                _r = _cli.chat.completions.create(
                                    model="openai/gpt-oss-120b",
                                    messages=[{"role":"user","content":f\"\"\"Gere exatamente {_qtd_quiz} questões de {_mat_quiz} no estilo {_banca_quiz}, nível {_nivel_quiz}.

Responda APENAS em JSON válido, sem texto extra:
{{"questoes": [{{"enunciado": "texto da questão", "alternativas": {{"A": "texto A", "B": "texto B", "C": "texto C", "D": "texto D", "E": "texto E"}}, "gabarito": "A", "explicacao": "Por que A está correta..."}}]}}\"\"\"}],
                                    max_tokens=4000
                                )
                                import json as _json
                                _raw = _r.choices[0].message.content
                                _s = _raw.find('{'); _e = _raw.rfind('}')
                                _dados = _json.loads(_raw[_s:_e+1])
                                st.session_state['quiz_banco'] = _dados['questoes']
                                st.session_state['quiz_idx'] = 0
                                st.session_state['quiz_acertos'] = 0
                                st.session_state['quiz_erros'] = []
                                st.session_state['quiz_respondida'] = False
                                st.session_state['quiz_resposta_atual'] = None
                                st.rerun()
                            except Exception as _e2:
                                st.error(f"Erro ao gerar questões: {_e2}")
                    else:
                        st.warning("Informe a matéria.")
            else:
                _banco = st.session_state['quiz_banco']
                _idx = st.session_state['quiz_idx']
                _total = len(_banco)

                if _idx >= _total:
                    # Resultado final
                    _acertos = st.session_state['quiz_acertos']
                    _pct = round(_acertos/_total*100)
                    _cor = "#22C55E" if _pct >= 70 else ("#F59E0B" if _pct >= 50 else "#EF4444")
                    st.markdown(f"<h2 style='text-align:center;color:{_cor};'>✅ Simulado Concluído!</h2>", unsafe_allow_html=True)
                    st.markdown(f"<h1 style='text-align:center;font-size:3em;color:{_cor};'>{_acertos}/{_total} — {_pct}%</h1>", unsafe_allow_html=True)

                    _c1,_c2,_c3 = st.columns(3)
                    _c1.metric("✅ Acertos", _acertos)
                    _c2.metric("❌ Erros", _total-_acertos)
                    _c3.metric("📊 Aproveitamento", f"{_pct}%")

                    if st.session_state['quiz_erros']:
                        st.markdown("### ❌ Questões que você errou — Revise:")
                        for _err in st.session_state['quiz_erros']:
                            with st.expander(f"Q{_err['num']}: {_err['enunciado'][:60]}..."):
                                st.markdown(f"**Sua resposta:** {_err['sua']} — **Gabarito:** {_err['gabarito']}")
                                st.markdown(f"**Explicação:** {_err['explicacao']}")

                    # Salvar no histórico
                    import datetime as _dt
                    st.session_state['historico_simulados'].append({
                        'data': _dt.datetime.now().strftime('%d/%m %H:%M'),
                        'acertos': _acertos,
                        'total': _total,
                        'pct': _pct
                    })

                    if st.button("🔄 Novo Simulado", key="tc_quiz_novo_final", use_container_width=True):
                        st.session_state['quiz_banco'] = []
                        st.rerun()
                else:
                    # Questão atual
                    _q = _banco[_idx]
                    st.markdown(f"**Questão {_idx+1} de {_total}** | ✅ {st.session_state['quiz_acertos']} acertos")

                    # Barra de progresso
                    st.progress(_idx/_total)

                    st.markdown(f"<div class='card'>{_q.get('enunciado','')}</div>", unsafe_allow_html=True)

                    _alts = _q.get('alternativas', {})
                    _gabarito = _q.get('gabarito','A')

                    if not st.session_state['quiz_respondida']:
                        for _letra, _texto in _alts.items():
                            if st.button(f"{_letra}) {_texto}", key=f"tc_quiz_alt_{_idx}_{_letra}", use_container_width=True):
                                st.session_state['quiz_resposta_atual'] = _letra
                                st.session_state['quiz_respondida'] = True
                                if _letra == _gabarito:
                                    st.session_state['quiz_acertos'] += 1
                                else:
                                    st.session_state['quiz_erros'].append({
                                        'num': _idx+1,
                                        'enunciado': _q.get('enunciado',''),
                                        'sua': _letra,
                                        'gabarito': _gabarito,
                                        'explicacao': _q.get('explicacao','')
                                    })
                                st.rerun()
                    else:
                        _resp = st.session_state['quiz_resposta_atual']
                        for _letra, _texto in _alts.items():
                            if _letra == _gabarito:
                                st.success(f"✅ {_letra}) {_texto}")
                            elif _letra == _resp and _resp != _gabarito:
                                st.error(f"❌ {_letra}) {_texto} ← sua resposta")
                            else:
                                st.markdown(f"&nbsp;&nbsp;{_letra}) {_texto}")

                        st.markdown(f"**💡 Explicação:** {_q.get('explicacao','')}")

                        if st.button("➡️ PRÓXIMA QUESTÃO" if _idx+1 < _total else "🏁 VER RESULTADO", key=f"tc_quiz_prox_{_idx}", use_container_width=True):
                            st.session_state['quiz_idx'] += 1
                            st.session_state['quiz_respondida'] = False
                            st.session_state['quiz_resposta_atual'] = None
                            st.rerun()

        with _tab_quiz2:
            st.markdown("### 📊 Meu Histórico de Simulados")
            if st.session_state['historico_simulados']:
                for i, _item in enumerate(reversed(st.session_state['historico_simulados'][-10:])):
                    _pct2 = _item.get('pct',0)
                    _cor2 = "#22C55E" if _pct2>=70 else ("#F59E0B" if _pct2>=50 else "#EF4444")
                    st.markdown(f"<div class='hist-item'><b>{_item.get('data','')}</b> — {_item.get('acertos',0)}/{_item.get('total',0)} questões — <span style='color:{_cor2};font-weight:700;'>{_pct2}%</span></div>", unsafe_allow_html=True)

                _total_sim = len(st.session_state['historico_simulados'])
                _media_pct = sum(s.get('pct',0) for s in st.session_state['historico_simulados']) / _total_sim
                st.markdown(f"**📈 Média geral:** {_media_pct:.0f}% em {_total_sim} simulados")
            else:
                st.info("Faça seu primeiro simulado para ver o histórico aqui.")

    with _tab_Cronograma:
        st.header("📅 Cronograma de Estudos")
        st.markdown("*Monte seu cronograma personalizado para o concurso.*")
        _prompt_cronograma = st.text_area("Descreva sua situação ou dúvida:", height=120, key="tutorc_cronograma_in", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="tutorc_cronograma_btn", use_container_width=True):
            if _prompt_cronograma.strip():
                with st.spinner("Analisando..."):
                    try:
                        from groq import Groq as _GrT
                        _cli = _GrT(api_key=st.session_state.api_key)
                        _r = _cli.chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[{"role":"user","content":_prompt_cronograma}],
                            max_tokens=2048
                        )
                        st.markdown(f"<div class='card'>{_r.choices[0].message.content}</div>", unsafe_allow_html=True)
                    except Exception as _e:
                        st.error(f"Erro: {_e}")
            else:
                st.warning("Preencha o campo acima.")


    with _tab_Flashcards:
        st.header("🃏 Flashcards Inteligentes")
        st.markdown("*Estude com flashcards gerados pela IA.*")
        _prompt_flashcards = st.text_area("Descreva sua situação ou dúvida:", height=120, key="tutorc_flashcards_in", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="tutorc_flashcards_btn", use_container_width=True):
            if _prompt_flashcards.strip():
                with st.spinner("Analisando..."):
                    try:
                        from groq import Groq as _GrT
                        _cli = _GrT(api_key=st.session_state.api_key)
                        _r = _cli.chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[{"role":"user","content":_prompt_flashcards}],
                            max_tokens=2048
                        )
                        st.markdown(f"<div class='card'>{_r.choices[0].message.content}</div>", unsafe_allow_html=True)
                    except Exception as _e:
                        st.error(f"Erro: {_e}")
            else:
                st.warning("Preencha o campo acima.")


    with _tab_Progresso:
        st.header("📈 Meu Progresso de Estudos")

        total       = len(st.session_state.historico_estudos)
        bib         = len(st.session_state.biblioteca_materiais)
        respondidas = st.session_state.questoes_respondidas
        certas      = st.session_state.questoes_certas
        taxa        = round(certas / respondidas * 100) if respondidas > 0 else 0
        tipos = {}
        for e in st.session_state.historico_estudos:
            tipos[e['tipo']] = tipos.get(e['tipo'], 0) + 1

        # Cor da taxa de acerto
        cor_taxa = "#059669" if taxa >= 70 else ("#B45309" if taxa >= 50 else "#B91C1C")
        msg_taxa = "🟢 Ótimo!" if taxa >= 70 else ("🟡 Melhorando..." if taxa >= 50 else "🔴 Precisa praticar mais")

        c1, c2, c3, c4, c5 = st.columns(5)
        c1.markdown(f"<div class='stat-box'><div class='stat-numero'>{total}</div><div>Materiais gerados</div></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='stat-box'><div class='stat-numero'>{respondidas}</div><div>Questões feitas</div></div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='stat-box'><div class='stat-numero' style='color:{cor_taxa} !important;'>{taxa}%</div><div>Taxa de acerto {msg_taxa}</div></div>", unsafe_allow_html=True)
        c4.markdown(f"<div class='stat-box'><div class='stat-numero'>{tipos.get('Resumo',0)}</div><div>Resumos</div></div>", unsafe_allow_html=True)
        c5.markdown(f"<div class='stat-box'><div class='stat-numero'>{bib}</div><div>Na biblioteca</div></div>", unsafe_allow_html=True)

        # Ajuste manual de questões
        with st.expander("✏️ Ajustar contagem de questões"):
            col_r, col_c = st.columns(2)
            with col_r:
                nova_r = st.number_input("Total de questões respondidas:", min_value=0, value=respondidas, key="tutorcon46")
            with col_c:
                nova_c = st.number_input("Total de acertos:", min_value=0, max_value=nova_r, value=min(certas, nova_r), key="tutorcon47")
            if st.button("Salvar contagem", key="tutorcon48"):
                st.session_state.questoes_respondidas = nova_r
                st.session_state.questoes_certas      = nova_c
                st.success("✅ Contagem atualizada!")
                st.rerun()

        if st.session_state.historico_estudos:
            col_f, col_ex = st.columns([3, 1])
            with col_f:
                filtro = st.selectbox("Filtrar:", ["Todos"] + list(tipos.keys()), key="tutorcon49")
            with col_ex:
                historico_txt = "\\n\\n".join(
                    f"[{e['data']}] {e['tipo']} — {e['materia']}\\n{e['conteudo']}\\n{'─'*40}"
                    for e in st.session_state.historico_estudos
                )
                st.download_button("⬇️ Exportar TXT", data=historico_txt,
                    file_name="historico_estudos.txt", mime="text/plain", key="tutorcon6_d2")

            for i, item in enumerate(reversed(st.session_state.historico_estudos)):
                if filtro != "Todos" and item['tipo'] != filtro:
                    continue
                idx_real = len(st.session_state.historico_estudos) - 1 - i
                with st.expander(f"[{item['tipo']}] {item.get('materia', '')} — {item['data']}"):
                    st.markdown(f"<div class='card'>{item['conteudo']}</div>", unsafe_allow_html=True)
                    col_sv, col_del = st.columns([3, 1])
                    with col_sv:
                        if st.button("💾 Salvar na Biblioteca", key=f"sv_hist_{i}"):
                            st.session_state.biblioteca_materiais.append(item.copy())
                            st.success("Salvo!")
                    with col_del:
                        if st.button("🗑️", key=f"del_hist_{i}"):
                            st.session_state.historico_estudos.pop(idx_real)
                            st.rerun()

            if st.button("🗑️ Limpar Todo o Histórico", key="tutorcon50"):
                st.session_state.historico_estudos = []
                st.rerun()
        else:
            st.info("Nenhum material gerado ainda. Comece pelo Plano de Estudos!")


        # ──────────────────────────────────────────
        # SIMULADO INTELIGENTE
        # ──────────────────────────────────────────

    with _tab_Legislacao:
        st.header("⚖️ Legislação")
        st.markdown("*Estude a legislação específica do seu concurso.*")
        _prompt_legislacao = st.text_area("Descreva sua situação ou dúvida:", height=120, key="tutorc_legislacao_in", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="tutorc_legislacao_btn", use_container_width=True):
            if _prompt_legislacao.strip():
                with st.spinner("Analisando..."):
                    try:
                        from groq import Groq as _GrT
                        _cli = _GrT(api_key=st.session_state.api_key)
                        _r = _cli.chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[{"role":"user","content":_prompt_legislacao}],
                            max_tokens=2048
                        )
                        st.markdown(f"<div class='card'>{_r.choices[0].message.content}</div>", unsafe_allow_html=True)
                    except Exception as _e:
                        st.error(f"Erro: {_e}")
            else:
                st.warning("Preencha o campo acima.")


    with _tab_Informatica:
        st.header("💻 Informática")
        st.markdown("*Questões e teoria de informática para concursos.*")
        _prompt_informatica = st.text_area("Descreva sua situação ou dúvida:", height=120, key="tutorc_informatica_in", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="tutorc_informatica_btn", use_container_width=True):
            if _prompt_informatica.strip():
                with st.spinner("Analisando..."):
                    try:
                        from groq import Groq as _GrT
                        _cli = _GrT(api_key=st.session_state.api_key)
                        _r = _cli.chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[{"role":"user","content":_prompt_informatica}],
                            max_tokens=2048
                        )
                        st.markdown(f"<div class='card'>{_r.choices[0].message.content}</div>", unsafe_allow_html=True)
                    except Exception as _e:
                        st.error(f"Erro: {_e}")
            else:
                st.warning("Preencha o campo acima.")


    with _tab_Portugues:
        st.header("📖 Português")
        st.markdown("*Gramática, interpretação e redação em português.*")
        _prompt_portugues = st.text_area("Descreva sua situação ou dúvida:", height=120, key="tutorc_portugues_in", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="tutorc_portugues_btn", use_container_width=True):
            if _prompt_portugues.strip():
                with st.spinner("Analisando..."):
                    try:
                        from groq import Groq as _GrT
                        _cli = _GrT(api_key=st.session_state.api_key)
                        _r = _cli.chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[{"role":"user","content":_prompt_portugues}],
                            max_tokens=2048
                        )
                        st.markdown(f"<div class='card'>{_r.choices[0].message.content}</div>", unsafe_allow_html=True)
                    except Exception as _e:
                        st.error(f"Erro: {_e}")
            else:
                st.warning("Preencha o campo acima.")


    with _tab_Matematica:
        st.header("🔢 Matemática/Raciocínio")
        st.markdown("*Matemática e raciocínio lógico para concursos.*")
        _prompt_matematica = st.text_area("Descreva sua situação ou dúvida:", height=120, key="tutorc_matematica_in", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="tutorc_matematica_btn", use_container_width=True):
            if _prompt_matematica.strip():
                with st.spinner("Analisando..."):
                    try:
                        from groq import Groq as _GrT
                        _cli = _GrT(api_key=st.session_state.api_key)
                        _r = _cli.chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[{"role":"user","content":_prompt_matematica}],
                            max_tokens=2048
                        )
                        st.markdown(f"<div class='card'>{_r.choices[0].message.content}</div>", unsafe_allow_html=True)
                    except Exception as _e:
                        st.error(f"Erro: {_e}")
            else:
                st.warning("Preencha o campo acima.")


    with _tab_Atualidades:
        st.header("📰 Atualidades")
        st.markdown("*Fique por dentro dos principais fatos nacionais e internacionais cobrados em concursos.*")
        _prompt_atual = st.text_area("Descreva o tema ou peça um resumo de atualidades:", height=120, key="tutorc_atual_in", placeholder="Ex: Resumo das principais notícias de 2024, eventos geopolíticos recentes, reformas legislativas...")
        if st.button("🤖 GERAR COM IA", key="tutorc_atual_btn", use_container_width=True):
            if _prompt_atual.strip():
                with st.spinner("Analisando..."):
                    try:
                        from groq import Groq as _GrT
                        _cli = _GrT(api_key=st.session_state.api_key)
                        _r = _cli.chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[{"role":"user","content":_prompt_atual}],
                            max_tokens=2048
                        )
                        st.markdown(f"<div class='card'>{_r.choices[0].message.content}</div>", unsafe_allow_html=True)
                    except Exception as _e:
                        st.error(f"Erro: {_e}")
            else:
                st.warning("Preencha o campo acima.")

    with _tab_DirConst:
        st.header("📜 Direito Constitucional")
        st.markdown("*Estude a Constituição Federal, direitos fundamentais, organização do Estado e controle de constitucionalidade.*")
        _prompt_dirconst = st.text_area("Descreva sua dúvida ou peça explicação sobre o tema:", height=120, key="tutorc_dirconst_in", placeholder="Ex: Explique os princípios fundamentais da CF/88, direitos e garantias fundamentais, processo legislativo...")
        if st.button("🤖 GERAR COM IA", key="tutorc_dirconst_btn", use_container_width=True):
            if _prompt_dirconst.strip():
                with st.spinner("Analisando..."):
                    try:
                        from groq import Groq as _GrT
                        _cli = _GrT(api_key=st.session_state.api_key)
                        _r = _cli.chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[{"role":"user","content":_prompt_dirconst}],
                            max_tokens=2048
                        )
                        st.markdown(f"<div class='card'>{_r.choices[0].message.content}</div>", unsafe_allow_html=True)
                    except Exception as _e:
                        st.error(f"Erro: {_e}")
            else:
                st.warning("Preencha o campo acima.")

    with _tab_DirAdmin:
        st.header("🏛️ Direito Administrativo")
        st.markdown("*Domine os princípios da administração pública, atos administrativos, licitações, contratos e responsabilidade civil do Estado.*")
        _prompt_diradm = st.text_area("Descreva sua dúvida ou peça explicação sobre o tema:", height=120, key="tutorc_diradm_in", placeholder="Ex: Princípios da administração pública (LIMPE), licitações Lei 14.133/21, contratos administrativos...")
        if st.button("🤖 GERAR COM IA", key="tutorc_diradm_btn", use_container_width=True):
            if _prompt_diradm.strip():
                with st.spinner("Analisando..."):
                    try:
                        from groq import Groq as _GrT
                        _cli = _GrT(api_key=st.session_state.api_key)
                        _r = _cli.chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[{"role":"user","content":_prompt_diradm}],
                            max_tokens=2048
                        )
                        st.markdown(f"<div class='card'>{_r.choices[0].message.content}</div>", unsafe_allow_html=True)
                    except Exception as _e:
                        st.error(f"Erro: {_e}")
            else:
                st.warning("Preencha o campo acima.")

    with _tab_Logico:
        st.header("🧠 Raciocínio Lógico")
        st.markdown("*Treine lógica proposicional, argumentativa, analítica, sequências, diagramas e raciocínio quantitativo.*")
        _prompt_logico = st.text_area("Descreva sua dúvida ou peça exercícios:", height=120, key="tutorc_logico_in", placeholder="Ex: Me explique lógica proposicional, resolva sequências numéricas, tabela verdade, silogismos...")
        if st.button("🤖 GERAR COM IA", key="tutorc_logico_btn", use_container_width=True):
            if _prompt_logico.strip():
                with st.spinner("Analisando..."):
                    try:
                        from groq import Groq as _GrT
                        _cli = _GrT(api_key=st.session_state.api_key)
                        _r = _cli.chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[{"role":"user","content":_prompt_logico}],
                            max_tokens=2048
                        )
                        st.markdown(f"<div class='card'>{_r.choices[0].message.content}</div>", unsafe_allow_html=True)
                    except Exception as _e:
                        st.error(f"Erro: {_e}")
            else:
                st.warning("Preencha o campo acima.")

    with _tab_DirPenal:
        st.header("🚔 Direito Penal")
        st.markdown("*Estude os princípios do direito penal, crimes em espécie, penas, extinção da punibilidade e legislação especial.*")
        _prompt_dirpenal = st.text_area("Descreva sua dúvida ou peça explicação sobre o tema:", height=120, key="tutorc_dirpenal_in", placeholder="Ex: Princípios do direito penal, crimes contra a administração pública, lei de drogas, estatuto do desarmamento...")
        if st.button("🤖 GERAR COM IA", key="tutorc_dirpenal_btn", use_container_width=True):
            if _prompt_dirpenal.strip():
                with st.spinner("Analisando..."):
                    try:
                        from groq import Groq as _GrT
                        _cli = _GrT(api_key=st.session_state.api_key)
                        _r = _cli.chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[{"role":"user","content":_prompt_dirpenal}],
                            max_tokens=2048
                        )
                        st.markdown(f"<div class='card'>{_r.choices[0].message.content}</div>", unsafe_allow_html=True)
                    except Exception as _e:
                        st.error(f"Erro: {_e}")
            else:
                st.warning("Preencha o campo acima.")

    with _tab_DirProc:
        st.header("⚖️ Direito Processual")
        st.markdown("*Domine o processo civil e penal: princípios, competência, recursos, execução e procedimentos especiais.*")
        _prompt_dirproc = st.text_area("Descreva sua dúvida ou peça explicação sobre o tema:", height=120, key="tutorc_dirproc_in", placeholder="Ex: Processo civil (CPC), processo penal (CPP), recursos, execução, tutela de urgência...")
        if st.button("🤖 GERAR COM IA", key="tutorc_dirproc_btn", use_container_width=True):
            if _prompt_dirproc.strip():
                with st.spinner("Analisando..."):
                    try:
                        from groq import Groq as _GrT
                        _cli = _GrT(api_key=st.session_state.api_key)
                        _r = _cli.chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[{"role":"user","content":_prompt_dirproc}],
                            max_tokens=2048
                        )
                        st.markdown(f"<div class='card'>{_r.choices[0].message.content}</div>", unsafe_allow_html=True)
                    except Exception as _e:
                        st.error(f"Erro: {_e}")
            else:
                st.warning("Preencha o campo acima.")

    with _tab_Bancario:
        st.header("💰 Conhecimentos Bancários e Financeiros")
        st.markdown("*Estude o sistema financeiro nacional, produtos bancários, mercado de capitais e matemática financeira.*")
        _prompt_banc = st.text_area("Descreva sua dúvida ou peça explicação sobre o tema:", height=120, key="tutorc_banc_in", placeholder="Ex: Sistema Financeiro Nacional, Banco Central, mercado de câmbio, produtos bancários, matemática financeira...")
        if st.button("🤖 GERAR COM IA", key="tutorc_banc_btn", use_container_width=True):
            if _prompt_banc.strip():
                with st.spinner("Analisando..."):
                    try:
                        from groq import Groq as _GrT
                        _cli = _GrT(api_key=st.session_state.api_key)
                        _r = _cli.chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[{"role":"user","content":_prompt_banc}],
                            max_tokens=2048
                        )
                        st.markdown(f"<div class='card'>{_r.choices[0].message.content}</div>", unsafe_allow_html=True)
                    except Exception as _e:
                        st.error(f"Erro: {_e}")
            else:
                st.warning("Preencha o campo acima.")

    with _tab_Contabil:
        st.header("📊 Contabilidade")
        st.markdown("*Estude contabilidade geral e pública: balanço patrimonial, DRE, escrituração e orçamento público.*")
        _prompt_cont = st.text_area("Descreva sua dúvida ou peça explicação sobre o tema:", height=120, key="tutorc_cont_in", placeholder="Ex: Balanço patrimonial, DRE, plano de contas, contabilidade pública, orçamento federal...")
        if st.button("🤖 GERAR COM IA", key="tutorc_cont_btn", use_container_width=True):
            if _prompt_cont.strip():
                with st.spinner("Analisando..."):
                    try:
                        from groq import Groq as _GrT
                        _cli = _GrT(api_key=st.session_state.api_key)
                        _r = _cli.chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[{"role":"user","content":_prompt_cont}],
                            max_tokens=2048
                        )
                        st.markdown(f"<div class='card'>{_r.choices[0].message.content}</div>", unsafe_allow_html=True)
                    except Exception as _e:
                        st.error(f"Erro: {_e}")
            else:
                st.warning("Preencha o campo acima.")

    with _tab_Geo:
        st.header("🌍 Geografia")
        st.markdown("*Estude geografia do Brasil e do mundo: regiões, clima, relevo, hidrografia, geopolítica e meio ambiente.*")
        _prompt_geo = st.text_area("Descreva sua dúvida ou peça explicação sobre o tema:", height=120, key="tutorc_geo_in", placeholder="Ex: Regiões brasileiras, biomas, hidrografia, geopolítica mundial, questões ambientais...")
        if st.button("🤖 GERAR COM IA", key="tutorc_geo_btn", use_container_width=True):
            if _prompt_geo.strip():
                with st.spinner("Analisando..."):
                    try:
                        from groq import Groq as _GrT
                        _cli = _GrT(api_key=st.session_state.api_key)
                        _r = _cli.chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[{"role":"user","content":_prompt_geo}],
                            max_tokens=2048
                        )
                        st.markdown(f"<div class='card'>{_r.choices[0].message.content}</div>", unsafe_allow_html=True)
                    except Exception as _e:
                        st.error(f"Erro: {_e}")
            else:
                st.warning("Preencha o campo acima.")

    with _tab_Hist:
        st.header("🕰️ História")
        st.markdown("*Estude história do Brasil e geral: períodos coloniais, império, república, história contemporânea e eventos mundiais.*")
        _prompt_hist = st.text_area("Descreva sua dúvida ou peça explicação sobre o tema:", height=120, key="tutorc_hist_in", placeholder="Ex: História do Brasil colonial, período imperial, república velha, Segunda Guerra Mundial, Guerra Fria...")
        if st.button("🤖 GERAR COM IA", key="tutorc_hist_btn", use_container_width=True):
            if _prompt_hist.strip():
                with st.spinner("Analisando..."):
                    try:
                        from groq import Groq as _GrT
                        _cli = _GrT(api_key=st.session_state.api_key)
                        _r = _cli.chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[{"role":"user","content":_prompt_hist}],
                            max_tokens=2048
                        )
                        st.markdown(f"<div class='card'>{_r.choices[0].message.content}</div>", unsafe_allow_html=True)
                    except Exception as _e:
                        st.error(f"Erro: {_e}")
            else:
                st.warning("Preencha o campo acima.")

    with _tab_Especifico:
        st.header("🎯 Conhecimentos Específicos")
        st.markdown("*Área específica do cargo: administração, economia, engenharia, medicina, direito, tecnologia e outros. Diga qual é sua área!*")
        _prompt_espec = st.text_area("Informe sua área e a dúvida:", height=120, key="tutorc_espec_in", placeholder="Ex: Sou candidato para auditor fiscal — me explique crédito tributário. / Área: TI — explique redes de computadores para concurso...")
        if st.button("🤖 GERAR COM IA", key="tutorc_espec_btn", use_container_width=True):
            if _prompt_espec.strip():
                with st.spinner("Analisando..."):
                    try:
                        from groq import Groq as _GrT
                        _cli = _GrT(api_key=st.session_state.api_key)
                        _r = _cli.chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[{"role":"user","content":_prompt_espec}],
                            max_tokens=2048
                        )
                        st.markdown(f"<div class='card'>{_r.choices[0].message.content}</div>", unsafe_allow_html=True)
                    except Exception as _e:
                        st.error(f"Erro: {_e}")
            else:
                st.warning("Preencha o campo acima.")

# --- RODAPÉ ---
st.markdown(
    "<div style='text-align:center;color:#999;font-size:0.8em;margin-top:60px;'>"
    "© 2026 Tutor de Concursos IA — Mentor Estratégico · MeusAgentesIA.com.br"
    "</div>", unsafe_allow_html=True
)
""",
    "nexus_english": """# [hub] import streamlit as st
# [hub] from groq import Groq
# [hub] from datetime import datetime, date, timedelta
# [hub] import json
import random

# set_page_config removido pelo super_agente

st.markdown(\"\"\"
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
[data-testid="stToolbar"] {visibility: hidden;}
[data-testid="stDecoration"] {visibility: hidden;}
[data-testid="stStatusWidget"] {visibility: hidden;}
</style>
\"\"\", unsafe_allow_html=True)

st.markdown(\"\"\"
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp { background-color:#F8FAFC; font-family:'Inter',sans-serif; }
[data-testid="stSidebar"] { display:none; }

.stTextInput>div>div>input, .stTextArea>div>textarea,
.stSelectbox>div>div>div, .stNumberInput>div>div>input {
    background-color:#FFFFFF !important; color:#1E293B !important;
    border:1px solid #CBD5E1 !important; font-family:'Inter',sans-serif !important;
}
.stTextArea>div>textarea { color:#1E293B !important; }

.stButton>button {
    width:100%; border-radius:10px; height:3.2em;
    background:linear-gradient(135deg,#6366F1,#4F46E5) !important; color:white !important;
    font-weight:600; border:none; box-shadow:0 4px 15px rgba(99,102,241,0.3);
    font-family:'Inter',sans-serif !important; transition:all 0.2s ease;
}
.stButton>button:hover { background:linear-gradient(135deg,#4F46E5,#4338CA) !important; transform:translateY(-1px); box-shadow:0 6px 20px rgba(99,102,241,0.4); }
.stApp .stButton>button, .stApp .stButton>button p,
.stApp .stButton>button span, .stApp .stButton>button div { color:white !important; }

.stApp h1, .stApp h2, .stApp h3 { color:#1E293B !important; font-family:'Inter',sans-serif !important; font-weight:700 !important; }
.stApp p, .stApp label, .stApp .stMarkdown { color:#475569 !important; }

/* Cards */
.card {
    background:#FFFFFF; padding:20px; border-radius:14px;
    border:1px solid #CBD5E1; margin-bottom:14px;
    white-space:normal; word-wrap:break-word;
}
.stApp .card, .stApp .card p, .stApp .card span,
.stApp .card div, .stApp .card strong, .stApp .card em { color:#1E293B !important; }

.card-professor {
    background:linear-gradient(135deg,#EEF2FF,#FFFFFF);
    padding:18px; border-radius:14px;
    border-left:4px solid #6366F1; margin-bottom:10px;
}
.stApp .card-professor, .stApp .card-professor * { color:#1E293B !important; }

.card-aluno {
    background:#F8FAFC; padding:14px; border-radius:14px;
    border:1px solid #CBD5E1; border-right:4px solid #10B981; margin-bottom:10px; margin-left:30px;
}
.stApp .card-aluno, .stApp .card-aluno * { color:#475569 !important; }

.card-success {
    background:linear-gradient(135deg,#064E3B,#065F46);
    padding:16px; border-radius:14px; border:1px solid #10B981; margin-bottom:10px;
}
.stApp .card-success, .stApp .card-success * { color:#065F46 !important; }

.card-erro {
    background:linear-gradient(135deg,#450A0A,#7F1D1D);
    padding:16px; border-radius:14px; border:1px solid #EF4444; margin-bottom:10px;
}
.stApp .card-erro, .stApp .card-erro * { color:#7F1D1D !important; }

.card-revisao {
    background:linear-gradient(135deg,#F5F5F4,#E7E5E4);
    padding:16px; border-radius:14px; border:1px solid #F59E0B; margin-bottom:10px;
}
.stApp .card-revisao, .stApp .card-revisao * { color:#78350F !important; }

/* Badge */
.badge { display:inline-block; background:#6366F122; color:#4F46E5;
         border:1px solid #6366F144; padding:3px 12px; border-radius:20px;
         font-size:0.75em; font-weight:600; margin-bottom:8px; }

.nivel-tag { display:inline-block; padding:4px 14px; border-radius:20px;
             font-size:0.85em; font-weight:700; }
.nivel-A1 { background:#CCFBF1; color:#0F766E; border:1px solid #2DD4BF; }
.nivel-A2 { background:#DBEAFE; color:#1D4ED8; border:1px solid #60A5FA; }
.nivel-B1 { background:#FEF3C7; color:#92400E; border:1px solid #FBBF24; }
.nivel-B2 { background:#FFEDD5; color:#9A3412; border:1px solid #F97316; }
.nivel-C1 { background:#EDE9FE; color:#5B21B6; border:1px solid #A78BFA; }
.nivel-C2 { background:#FCE7F3; color:#9D174D; border:1px solid #F472B6; }

/* Progresso */
.prog-bar-bg { background:#FFFFFF; border-radius:8px; height:10px; overflow:hidden; margin:4px 0 12px; }
.prog-bar-fill { height:10px; border-radius:8px; background:linear-gradient(90deg,#6366F1,#4F46E5); transition:width 0.4s ease; }

/* Stat tiles */
.stat-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(100px,1fr)); gap:10px; margin-bottom:16px; }
.stat-tile { background:#FFFFFF; border:1px solid #CBD5E1; border-radius:12px; padding:14px; text-align:center; }
.stat-num { font-size:1.7em; font-weight:800; color:#4F46E5; }
.stat-label { font-size:0.72em; color:#475569; margin-top:2px; }

.streak-tile { border-color:#F59E0B !important; }
.streak-tile .stat-num { color:#B45309 !important; }
</style>
\"\"\", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# PROMPT MESTRE — NEXUS ENGLISH
# ═══════════════════════════════════════════════════════════
PROMPT_MESTRE = \"\"\"
IDENTIDADE
Você é o NEXUS ENGLISH, um professor particular de inglês especializado em aprendizagem adaptativa,  REGRA DE OURO — CONFIABILIDADE 100%%: Forneça APENAS informações que você tem certeza absoluta que são verdadeiras. JAMAIS invente, suponha, extrapole ou preencha lacunas com dados fictícios. Se não souber algo com certeza — preço, endereço, horário, nome, estatística, lei, fato — diga EXPLICITAMENTE: 'Não tenho certeza sobre isso, recomendo verificar em [fonte].' É melhor uma resposta incompleta e honesta do que uma resposta completa e inventada. O usuário depende dessas informações para tomar decisões reais. conversação prática, gramática contextualizada, aquisição de vocabulário e correção pedagógica.

Seu objetivo é ajudar o aluno a compreender, lembrar e utilizar o inglês de maneira progressiva, desde o nível iniciante até o avançado.

Você não é apenas um tradutor nem um chatbot de perguntas e respostas. Você conduz sessões de aprendizagem, verifica o conhecimento, identifica dificuldades e adapta as atividades ao desempenho do aluno.

REGRAS FUNDAMENTAIS
1. Personalize o ensino ao nível, aos objetivos e às dificuldades registradas do aluno.
2. Ensine UMA habilidade principal por vez. Não sobrecarregue o iniciante.
3. Apresente exemplos claros, contextualizados e naturais.
4. Sempre que possível, peça ao aluno que tente responder ANTES de revelar a resposta.
5. Nunca confunda reconhecer uma resposta com saber produzi-la.
6. Corrija os erros com respeito, clareza e objetividade. Explique o motivo e ofereça outra oportunidade.
7. Não aceite automaticamente uma resposta como errada apenas porque ela difere do exemplo esperado. Considere alternativas gramaticalmente corretas e naturais.
8. Não invente regras gramaticais, traduções ou explicações.
9. Não avance apenas porque o aluno acertou uma única pergunta.
10. Evite repetir conteúdos que o aluno já domina, mas mantenha revisões periódicas.
11. Use português para explicar quando isso facilitar o entendimento. Aumente gradualmente o uso do inglês.
12. Nunca humilhe, pressione ou desestimule. Transforme erros em oportunidades.

PROTOCOLO DE CORREÇÃO
Quando o aluno cometer um erro:
1. Identifique a parte incorreta.
2. Mostre a forma correta e natural.
3. Explique a regra em linguagem compatível com seu nível.
4. Dê um exemplo adicional.
5. Peça que o aluno aplique a regra em outra frase.

MODO CONVERSAÇÃO
Simule situações reais (apresentações, viagens, restaurantes, entrevistas, reuniões, cotidiano).
Mantenha o diálogo natural. Não interrompa para corrigir cada detalhe irrelevante.
Depois de um trecho de conversa, ofereça correções relevantes e convide o aluno a continuar.

FORMATO
Seja didático, natural, motivador e objetivo. Em exercícios, apresente UMA pergunta por vez e aguarde a resposta.
\"\"\"

# ═══════════════════════════════════════════════════════════
# CURRÍCULO A1 → C2
# ═══════════════════════════════════════════════════════════
CURRICULO = {
    "A1": [
        ("A1_U01", "Alfabeto e sons básicos", "Fundamentos"),
        ("A1_U02", "Cumprimentos e apresentação pessoal", "Fundamentos"),
        ("A1_U03", "Números, dias e meses", "Fundamentos"),
        ("A1_U04", "Pronomes e verbo To Be", "Gramática"),
        ("A1_U05", "Artigos (a, an, the) e plurais", "Gramática"),
        ("A1_U06", "Vocabulário cotidiano (cores, família, objetos)", "Vocabulário"),
        ("A1_U07", "Perguntas simples (What, Who, Where)", "Gramática"),
        ("A1_U08", "Horas e rotina diária", "Vocabulário"),
        ("A1_U09", "Números grandes e preços", "Vocabulário"),
        ("A1_U10", "Mini-conversação: apresentação completa", "Conversação"),
    ],
    "A2": [
        ("A2_U01", "Present Simple — rotinas e fatos", "Gramática"),
        ("A2_U02", "Present Continuous — agora e futuro próximo", "Gramática"),
        ("A2_U03", "Past Simple — verbos regulares e irregulares", "Gramática"),
        ("A2_U04", "Futuro básico: will e going to", "Gramática"),
        ("A2_U05", "Vocabulário de compras e dinheiro", "Vocabulário"),
        ("A2_U06", "No restaurante e pedindo comida", "Conversação"),
        ("A2_U07", "Direções e transporte", "Conversação"),
        ("A2_U08", "Descrição de pessoas e lugares", "Vocabulário"),
        ("A2_U09", "Planejando uma viagem", "Conversação"),
        ("A2_U10", "Conversação: cotidiano completo", "Conversação"),
    ],
    "B1": [
        ("B1_U01", "Present Perfect — experiências e resultados", "Gramática"),
        ("B1_U02", "Condicionais básicas (If type 1 e 2)", "Gramática"),
        ("B1_U03", "Modal verbs completos", "Gramática"),
        ("B1_U04", "Expressando opiniões e sentimentos", "Conversação"),
        ("B1_U05", "Leitura e interpretação de textos", "Compreensão"),
        ("B1_U06", "Vocabulário de trabalho e carreira", "Vocabulário"),
        ("B1_U07", "Resolvendo problemas e situações inesperadas", "Conversação"),
        ("B1_U08", "Phrasal verbs essenciais", "Vocabulário"),
        ("B1_U09", "Escrita formal e informal", "Escrita"),
        ("B1_U10", "Conversação: debate e opinião", "Conversação"),
    ],
    "B2": [
        ("B2_U01", "Passive voice e estruturas avançadas", "Gramática"),
        ("B2_U02", "Reported speech", "Gramática"),
        ("B2_U03", "Condicionais avançadas (type 3 e mistas)", "Gramática"),
        ("B2_U04", "Idioms e expressões idiomáticas", "Vocabulário"),
        ("B2_U05", "Inglês para negócios e ambiente profissional", "Conversação"),
        ("B2_U06", "Textos complexos e argumentação", "Compreensão"),
        ("B2_U07", "Vocabulário acadêmico e formal", "Vocabulário"),
        ("B2_U08", "Nuances e registros", "Gramática"),
        ("B2_U09", "Apresentações e debates avançados", "Conversação"),
        ("B2_U10", "Preparação para exames (IELTS/TOEFL B2)", "Avaliação"),
    ],
    "C1": [
        ("C1_U01", "Gramática avançada e exceções", "Gramática"),
        ("C1_U02", "Linguagem especializada por área", "Vocabulário"),
        ("C1_U03", "Argumentação complexa e sofisticada", "Conversação"),
        ("C1_U04", "Compreensão de textos exigentes", "Compreensão"),
        ("C1_U05", "Escrita acadêmica e profissional avançada", "Escrita"),
        ("C1_U06", "Expressão precisa e registro formal", "Conversação"),
        ("C1_U07", "Leitura crítica e análise", "Compreensão"),
        ("C1_U08", "Preparação Cambridge C1 Advanced", "Avaliação"),
    ],
    "C2": [
        ("C2_U01", "Precisão e sofisticação linguística", "Gramática"),
        ("C2_U02", "Textos literários e técnicos", "Compreensão"),
        ("C2_U03", "Expressão espontânea e nativa", "Conversação"),
        ("C2_U04", "Cambridge C2 Proficiency", "Avaliação"),
    ]
}

NIVEIS_ORDEM = ["A1", "A2", "B1", "B2", "C1", "C2"]

NIVEL_DESC = {
    "A1": "Iniciante",
    "A2": "Básico",
    "B1": "Intermediário",
    "B2": "Interm. Avançado",
    "C1": "Avançado",
    "C2": "Fluente"
}

# ═══════════════════════════════════════════════════════════
# DIAGNÓSTICO — perguntas adaptativas
# ═══════════════════════════════════════════════════════════
DIAGNOSTICO_PERGUNTAS = [
    # (id, pergunta, resposta_correta, alternativas, nivel_alvo)
    ("D01", "Complete: 'My name ___ John.'", "is", ["is","are","am","be"], "A1"),
    ("D02", "Qual é o plural de 'child'?", "children", ["childs","childrens","children","child's"], "A1"),
    ("D03", "Complete: 'She ___ to school every day.'", "goes", ["go","goes","going","gone"], "A2"),
    ("D04", "Qual tempo verbal é este: 'I am eating lunch.'", "Present Continuous", ["Present Simple","Present Continuous","Past Simple","Future"], "A2"),
    ("D05", "Complete: 'I ___ never been to Japan.'", "have", ["have","has","had","am"], "B1"),
    ("D06", "Se eu dissesse 'If I had more money, I ___ buy a car.' — qual forma está correta?", "would buy", ["will buy","would buy","buy","bought"], "B1"),
    ("D07", "'The report was written by the manager.' Esta frase está na voz:", "passiva", ["ativa","passiva","indireta","condicional"], "B2"),
    ("D08", "'Break a leg' significa:", "Boa sorte", ["Quebre uma perna","Boa sorte","Tenha cuidado","Seja rápido"], "B2"),
    ("D09", "Em 'Had she known, she would have acted differently.' — qual é o tipo de condicional?", "Tipo 3 (hipótese no passado)", ["Tipo 1","Tipo 2","Tipo 3 (hipótese no passado)","Zero conditional"], "C1"),
    ("D10", "Qual palavra completa corretamente: 'The government's ___ to tackle climate change has been criticized.'", "endeavour", ["try","attempt","endeavour","effort"] , "C1"),
]

# ═══════════════════════════════════════════════════════════
# HELPERS — repetição espaçada
# ═══════════════════════════════════════════════════════════
def intervalo_revisao(resultado: str) -> int:
    \"\"\"Retorna dias até próxima revisão baseado no resultado.\"\"\"
    return {"errou": 0, "dificil": 1, "hesitante": 3, "seguro": 7, "dominado": 14, "excelente": 30}.get(resultado, 1)

def calcular_dominio(habilidade: dict) -> float:
    \"\"\"Calcula domínio entre 0 e 1.\"\"\"
    if not habilidade.get("tentativas"): return 0.0
    t = habilidade["tentativas"]
    e = habilidade.get("erros", 0)
    taxa = max(0, (t - e) / t)
    revisoes_ok = habilidade.get("revisoes_ok", 0)
    bonus = min(0.2, revisoes_ok * 0.05)
    return min(1.0, taxa * 0.8 + bonus)

def habilidade_vencida(habilidade: dict) -> bool:
    \"\"\"Verifica se a habilidade precisa de revisão hoje.\"\"\"
    proxima = habilidade.get("proxima_revisao")
    if not proxima: return False
    try:
        return date.fromisoformat(proxima) <= date.today()
    except Exception:
        return False

def inicializar_perfil(nome, nivel_est, objetivo, api_key):
    \"\"\"Cria perfil inicial do aluno.\"\"\"
    return {
        "nome": nome,
        "nivel_estimado": nivel_est,
        "objetivo": objetivo,
        "api_key": api_key,
        "unidade_atual": f"{nivel_est}_U01",
        "streak_dias": 0,
        "ultima_aula": None,
        "habilidades": {},
        "vocabulario": [],
        "erros_recorrentes": [],
        "sessoes": [],
        "historico_chat": [],
        "historico_conv": [],
        "diagnostico_feito": False,
        "pontos": 0,
    }

def registrar_tentativa(habilidade_id: str, acertou: bool, resultado: str = "hesitante"):
    \"\"\"Atualiza habilidade no perfil após tentativa.\"\"\"
    p = st.session_state.perfil
    if habilidade_id not in p["habilidades"]:
        p["habilidades"][habilidade_id] = {"tentativas": 0, "erros": 0, "revisoes_ok": 0, "proxima_revisao": None}
    h = p["habilidades"][habilidade_id]
    h["tentativas"] = h.get("tentativas", 0) + 1
    if not acertou:
        h["erros"] = h.get("erros", 0) + 1
        h["proxima_revisao"] = str(date.today() + timedelta(days=intervalo_revisao("errou")))
        if habilidade_id not in p.get("erros_recorrentes", []):
            p["erros_recorrentes"].append(habilidade_id)
    else:
        h["revisoes_ok"] = h.get("revisoes_ok", 0) + 1
        dias = intervalo_revisao(resultado)
        h["proxima_revisao"] = str(date.today() + timedelta(days=dias))
        p["pontos"] = p.get("pontos", 0) + 10
    h["dominio"] = calcular_dominio(h)
    h["ultima_pratica"] = str(date.today())

def unidade_atual_info():
    \"\"\"Retorna info da unidade atual.\"\"\"
    uid = st.session_state.perfil.get("unidade_atual", "A1_U01")
    nivel = uid[:2]
    unidades = CURRICULO.get(nivel, [])
    for u in unidades:
        if u[0] == uid:
            return u
    return unidades[0] if unidades else ("A1_U01", "Fundamentos", "Gramática")

def revisoes_pendentes():
    \"\"\"Retorna lista de habilidades vencidas para revisão.\"\"\"
    p = st.session_state.perfil
    return [hid for hid, h in p.get("habilidades", {}).items() if habilidade_vencida(h) and h.get("dominio", 0) < 0.85]

def atualizar_streak():
    p = st.session_state.perfil
    hoje = str(date.today())
    if p.get("ultima_aula") == str(date.today() - timedelta(days=1)):
        p["streak_dias"] = p.get("streak_dias", 0) + 1
    elif p.get("ultima_aula") != hoje:
        p["streak_dias"] = 1
    p["ultima_aula"] = hoje

def chamar_ia(mensagens: list, max_tokens: int = 1024) -> str:
    \"\"\"Chama a API com o prompt mestre.\"\"\"
    try:
        _cli = Groq(api_key=st.session_state.perfil["api_key"])
        _sys = [{"role": "system", "content": PROMPT_MESTRE}]
        _sys[0]["content"] += f"\\n\\nPERFIL DO ALUNO:\\nNome: {st.session_state.perfil['nome']}\\nNível estimado: {st.session_state.perfil['nivel_estimado']}\\nObjetivo: {st.session_state.perfil['objetivo']}\\nErros recorrentes: {', '.join(st.session_state.perfil.get('erros_recorrentes', [])[:5]) or 'nenhum registrado'}\\nStreak: {st.session_state.perfil.get('streak_dias', 0)} dias"
        _r = _cli.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=_sys + mensagens,
            max_tokens=max_tokens
        )
        return _r.choices[0].message.content
    except Exception as e:
        return f"❌ Erro na API: {e}"

# ═══════════════════════════════════════════════════════════
# SESSION STATE
# ═══════════════════════════════════════════════════════════
if "etapa" not in st.session_state: st.session_state.etapa = "login"
if "perfil" not in st.session_state: st.session_state.perfil = {}
if "diag_idx" not in st.session_state: st.session_state.diag_idx = 0
if "diag_acertos" not in st.session_state: st.session_state.diag_acertos = 0
if "diag_nivel" not in st.session_state: st.session_state.diag_nivel = "A1"
if "diag_resp" not in st.session_state: st.session_state.diag_resp = None
if "diag_confirmado" not in st.session_state: st.session_state.diag_confirmado = False
if "aula_historico" not in st.session_state: st.session_state.aula_historico = []

# ═══════════════════════════════════════════════════════════
# TELA LOGIN
# ═══════════════════════════════════════════════════════════
if st.session_state.etapa == "login":
    st.markdown("<h1 style='text-align:center;font-size:2.4em;margin-bottom:4px'>🧠 Nexus English</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#4F46E5;font-size:1.1em;margin-bottom:4px'>Seu professor particular adaptativo de inglês</p>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center'><span class='badge'>MeusAgentesIA.com.br</span></div>", unsafe_allow_html=True)
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        _nome = st.text_input("Seu nome", placeholder="Como posso te chamar?", key="l_nome")
        _obj = st.selectbox("Seu objetivo com inglês", [
            "Conversação geral",
            "Trabalho e negócios",
            "Viagem e turismo",
            "Estudos e intercâmbio",
            "Exames (IELTS, TOEFL, Cambridge)",
            "Inglês para tecnologia/programação",
            "Quero aprender do zero"
        ], key="l_obj")
        _api = st.text_input("Chave API Groq", type="password", placeholder="gsk_...", key="l_api")
        st.markdown("<small style='color:#475569'>Obtenha grátis em <b>console.groq.com</b></small>", unsafe_allow_html=True)
        st.markdown("")
        if st.button("🚀 COMEÇAR DIAGNÓSTICO", key="l_btn"):
            if _nome.strip() and _api.strip():
                st.session_state.perfil = inicializar_perfil(_nome.strip(), "A1", _obj, _api.strip())
                st.session_state.etapa = "diagnostico"
                st.session_state.diag_idx = 0
                st.session_state.diag_acertos = 0
                st.session_state.diag_nivel = "A1"
                st.rerun()
            else:
                st.warning("Informe seu nome e a chave API.")

# ═══════════════════════════════════════════════════════════
# DIAGNÓSTICO ADAPTATIVO
# ═══════════════════════════════════════════════════════════
elif st.session_state.etapa == "diagnostico":
    st.markdown("<h2 style='text-align:center'>📊 Diagnóstico Inicial</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#475569'>Vamos descobrir seu nível real — sem pressa, sem julgamento!</p>", unsafe_allow_html=True)

    _idx = st.session_state.diag_idx
    _total = len(DIAGNOSTICO_PERGUNTAS)

    # Progresso
    _prog = _idx / _total
    st.markdown(f"<div class='prog-bar-bg'><div class='prog-bar-fill' style='width:{int(_prog*100)}%'></div></div>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center;color:#475569;font-size:0.85em'>Questão {_idx + 1} de {_total}</p>", unsafe_allow_html=True)

    if _idx < _total:
        _qid, _q, _correta, _alts, _nivel_q = DIAGNOSTICO_PERGUNTAS[_idx]
        _alts_embaralhadas = _alts.copy()
        random.shuffle(_alts_embaralhadas)

        st.markdown(f"<div class='card'><b>❓ {_q}</b></div>", unsafe_allow_html=True)
        _resp = st.radio("Escolha a resposta:", _alts_embaralhadas, key=f"diag_{_idx}", index=None)

        if _resp and not st.session_state.diag_confirmado:
            if st.button("✅ Confirmar resposta", key=f"diag_conf_{_idx}"):
                st.session_state.diag_resp = _resp
                st.session_state.diag_confirmado = True
                st.rerun()

        if st.session_state.diag_confirmado and st.session_state.diag_resp:
            _acertou = st.session_state.diag_resp.lower() == _correta.lower()
            if _acertou:
                st.markdown("<div class='card-success'>✅ <b>Correto!</b></div>", unsafe_allow_html=True)
                st.session_state.diag_acertos += 1
                # Subir nível estimado
                if _nivel_q in NIVEIS_ORDEM:
                    _idx_nivel = NIVEIS_ORDEM.index(_nivel_q)
                    if _idx_nivel + 1 < len(NIVEIS_ORDEM):
                        st.session_state.diag_nivel = NIVEIS_ORDEM[min(_idx_nivel + 1, len(NIVEIS_ORDEM)-1)]
            else:
                st.markdown(f"<div class='card-erro'>❌ <b>Resposta esperada:</b> {_correta}</div>", unsafe_allow_html=True)
                # Manter ou baixar nível
                if _nivel_q in NIVEIS_ORDEM:
                    _idx_nivel = NIVEIS_ORDEM.index(_nivel_q)
                    st.session_state.diag_nivel = NIVEIS_ORDEM[max(0, _idx_nivel - 1)]

            if st.button("➡️ Próxima questão", key=f"diag_prox_{_idx}"):
                st.session_state.diag_idx += 1
                st.session_state.diag_confirmado = False
                st.session_state.diag_resp = None
                st.rerun()
    else:
        # Diagnóstico concluído
        _nivel_final = st.session_state.diag_nivel
        _acertos = st.session_state.diag_acertos
        st.markdown(f\"\"\"
        <div class='card-professor'>
            <h3>🎉 Diagnóstico concluído!</h3>
            <p>Você acertou <b>{_acertos} de {_total}</b> questões.</p>
            <p>Seu nível estimado: <span class='nivel-tag nivel-{_nivel_final}'>{_nivel_final} — {NIVEL_DESC.get(_nivel_final,'')}</span></p>
            <p style='color:#475569;font-size:0.9em'>Este diagnóstico textual é uma estimativa inicial. O professor irá ajustar conforme você pratica.</p>
        </div>
        \"\"\", unsafe_allow_html=True)

        if st.button("🚀 COMEÇAR MINHA TRILHA PERSONALIZADA", key="diag_fim"):
            st.session_state.perfil["nivel_estimado"] = _nivel_final
            st.session_state.perfil["unidade_atual"] = f"{_nivel_final}_U01"
            st.session_state.perfil["diagnostico_feito"] = True
            atualizar_streak()
            st.session_state.etapa = "app"
            st.rerun()

# ═══════════════════════════════════════════════════════════
# APP PRINCIPAL
# ═══════════════════════════════════════════════════════════
elif st.session_state.etapa == "app":
    p = st.session_state.perfil
    atualizar_streak()

    _nivel = p.get("nivel_estimado", "A1")
    _unidade = unidade_atual_info()
    _revisoes = revisoes_pendentes()
    _dominio_medio = 0
    if p["habilidades"]:
        _vals = [h.get("dominio", 0) for h in p["habilidades"].values()]
        _dominio_medio = int(sum(_vals) / len(_vals) * 100)

    # Header
    st.markdown(
        f"<h1 style='margin-bottom:2px'>🧠 Nexus English</h1>"
        f"<p style='color:#4F46E5;margin-bottom:6px'>Olá, <b>{p['nome']}</b>! "
        f"<span class='nivel-tag nivel-{_nivel}'>{_nivel} — {NIVEL_DESC.get(_nivel,'')}</span></p>",
        unsafe_allow_html=True
    )
    st.markdown("<div style='margin-bottom:10px'><span class='badge'>MeusAgentesIA.com.br</span></div>", unsafe_allow_html=True)

    # Stats
    st.markdown(f\"\"\"
    <div class='stat-grid'>
        <div class='stat-tile streak-tile'>
            <div class='stat-num'>🔥 {p.get('streak_dias',0)}</div>
            <div class='stat-label'>Dias seguidos</div>
        </div>
        <div class='stat-tile'>
            <div class='stat-num'>{p.get('pontos',0)}</div>
            <div class='stat-label'>Pontos</div>
        </div>
        <div class='stat-tile'>
            <div class='stat-num'>{len(p.get('habilidades',{}))}</div>
            <div class='stat-label'>Habilidades</div>
        </div>
        <div class='stat-tile'>
            <div class='stat-num'>{_dominio_medio}%</div>
            <div class='stat-label'>Domínio médio</div>
        </div>
        <div class='stat-tile'>
            <div class='stat-num'>{len(_revisoes)}</div>
            <div class='stat-label'>Revisões pendentes</div>
        </div>
    </div>
    \"\"\", unsafe_allow_html=True)

    # Alerta de revisões
    if _revisoes:
        st.markdown(f"<div class='card-revisao'>⏰ <b>Você tem {len(_revisoes)} revisão(ões) pendente(s)!</b> Acesse a aba <b>Revisão</b> para não perder o que aprendeu.</div>", unsafe_allow_html=True)

    # TABS
    (_tab_aula, _tab_conv, _tab_revisao, _tab_exercicios, _tab_vocab, _tab_progresso, _tab_explorar) = st.tabs([
        "📚 Minha Aula", "💬 Conversação", "🔄 Revisão", "🎯 Exercícios", "📖 Vocabulário", "📈 Progresso", "🗺️ Explorar"
    ])

    # ── ABA: MINHA AULA ──
    with _tab_aula:
        st.header("📚 Minha Aula de Hoje")

        # Info da unidade atual
        _uid, _utitulo, _utipo = _unidade
        st.markdown(f\"\"\"
        <div class='card-professor'>
            <div style='font-size:0.8em;color:#4F46E5;margin-bottom:6px'>UNIDADE ATUAL · {_utipo.upper()}</div>
            <h3 style='margin:0 0 8px 0'>{_utitulo}</h3>
            <p style='color:#475569;margin:0'>Trilha: <b>{_nivel}</b> — {NIVEL_DESC.get(_nivel,'')}</p>
        </div>
        \"\"\", unsafe_allow_html=True)

        # Histórico da aula
        _hist = st.session_state.aula_historico
        if _hist:
            st.markdown("**Sessão atual:**")
            for _msg in _hist[-10:]:
                if _msg["role"] == "user":
                    st.markdown(f"<div class='card-aluno'>🧑 <b>Você:</b> {_msg['content']}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='card-professor'>🎓 <b>Nexus:</b> {_msg['content']}</div>", unsafe_allow_html=True)

        _col_btn1, _col_btn2 = st.columns(2)
        with _col_btn1:
            if st.button("▶️ INICIAR / CONTINUAR AULA", key="aula_start", use_container_width=True):
                with st.spinner("Preparando sua aula..."):
                    _contexto = f"O aluno está na unidade '{_utitulo}' (tipo: {_utipo}). Nível: {_nivel}. Objetivo: {p['objetivo']}."
                    if _hist:
                        _prompt = f"{_contexto} Continue a aula do ponto onde paramos. Proponha a próxima atividade ou exercício."
                    else:
                        _prompt = f"{_contexto} Inicie a aula seguindo a estrutura: 1) revisão rápida se houver conteúdo anterior, 2) explique o conteúdo novo de forma didática com exemplos, 3) proponha o primeiro exercício interativo. Apresente UMA pergunta e aguarde a resposta."
                    _msgs = st.session_state.aula_historico[-6:] + [{"role": "user", "content": _prompt}]
                    _resp = chamar_ia(_msgs, max_tokens=1500)
                    st.session_state.aula_historico.append({"role": "user", "content": _prompt})
                    st.session_state.aula_historico.append({"role": "assistant", "content": _resp})
                    st.rerun()

        with _col_btn2:
            if st.button("🔄 Nova aula (próxima unidade)", key="aula_nova", use_container_width=True):
                # Avançar unidade
                _uid_atual = p.get("unidade_atual", "A1_U01")
                _nivel_atual = _uid_atual[:2]
                _unidades = CURRICULO.get(_nivel_atual, [])
                _ids = [u[0] for u in _unidades]
                if _uid_atual in _ids:
                    _pos = _ids.index(_uid_atual)
                    if _pos + 1 < len(_ids):
                        p["unidade_atual"] = _ids[_pos + 1]
                    else:
                        # Subir de nível
                        _idx_n = NIVEIS_ORDEM.index(_nivel_atual)
                        if _idx_n + 1 < len(NIVEIS_ORDEM):
                            _proximo_nivel = NIVEIS_ORDEM[_idx_n + 1]
                            p["nivel_estimado"] = _proximo_nivel
                            p["unidade_atual"] = f"{_proximo_nivel}_U01"
                            st.success(f"🎉 Parabéns! Você avançou para o nível {_proximo_nivel}!")
                st.session_state.aula_historico = []
                st.rerun()

        # Campo de resposta
        st.markdown("---")
        _resp_aluno = st.text_area("Sua resposta para o professor:", height=100, key="aula_resp_in", placeholder="Digite sua resposta em inglês (ou em português se tiver dúvida)...")
        _c1, _c2 = st.columns(2)
        with _c1:
            if st.button("📩 ENVIAR RESPOSTA", key="aula_resp_btn", use_container_width=True):
                if _resp_aluno.strip():
                    with st.spinner("Analisando sua resposta..."):
                        _hist_atual = st.session_state.aula_historico[-8:]
                        _hist_atual.append({"role": "user", "content": _resp_aluno})
                        _r = chamar_ia(_hist_atual, max_tokens=1200)
                        st.session_state.aula_historico.append({"role": "user", "content": _resp_aluno})
                        st.session_state.aula_historico.append({"role": "assistant", "content": _r})
                        # Tentativa registrada genericamente
                        registrar_tentativa(_uid, True, "hesitante")
                        st.rerun()
                else:
                    st.warning("Escreva sua resposta antes de enviar.")
        with _c2:
            if st.button("🗑️ Limpar sessão", key="aula_clear", use_container_width=True):
                st.session_state.aula_historico = []
                st.rerun()

    # ── ABA: CONVERSAÇÃO ──
    with _tab_conv:
        st.header("💬 Conversação em Inglês")
        st.markdown("*Pratique situações reais. O professor mantém o diálogo natural e corrige ao longo da conversa.*")

        _situacoes = [
            "Livre — escolha o assunto",
            "Apresentação pessoal (primeiro contato)",
            "No restaurante (pedir, pagar, reclamar)",
            "Entrevista de emprego",
            "No hotel (check-in, pedidos)",
            "Discussão de notícias / atualidades",
            "Reunião de trabalho",
            "No aeroporto e alfândega",
            "Compras em loja / shopping",
            "Pedindo informações na rua",
            "Telefone / videochamada profissional",
            "Situação de emergência",
        ]
        _situacao = st.selectbox("Situação para praticar:", _situacoes, key="conv_sit")
        _tema_livre = ""
        if _situacao == "Livre — escolha o assunto":
            _tema_livre = st.text_input("Tema livre:", placeholder="Ex: minha família, meu trabalho, filmes...", key="conv_tema")

        _hist_conv = p.get("historico_conv", [])
        if _hist_conv:
            for _m in _hist_conv:
                if _m["role"] == "user":
                    st.markdown(f"<div class='card-aluno'>🧑 {_m['content']}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='card-professor'>🎓 <b>Nexus:</b> {_m['content']}</div>", unsafe_allow_html=True)

        _fala = st.text_area("Fale em inglês (ou português se quiser ajuda):", height=90, key="conv_in", placeholder="Go ahead and speak...")
        _cc1, _cc2 = st.columns(2)
        with _cc1:
            if st.button("💬 ENVIAR", key="conv_btn", use_container_width=True):
                if _fala.strip():
                    with st.spinner("Conversando..."):
                        _tema_conv = _tema_livre if _tema_livre else _situacao
                        _intro = f"Situação de conversação: {_tema_conv}. Nível do aluno: {_nivel}. Objetivo: {p['objetivo']}. Mantenha a conversa fluindo naturalmente. Corrija apenas erros relevantes e ao final de cada turno de fala."
                        _msgs_conv = [{"role": "system", "content": PROMPT_MESTRE + "\\n\\n" + _intro}]
                        _msgs_conv += _hist_conv  # histórico completo
                        _msgs_conv.append({"role": "user", "content": _fala})
                        try:
                            _cli = Groq(api_key=p["api_key"])
                            _r = _cli.chat.completions.create(model="openai/gpt-oss-120b", messages=_msgs_conv, max_tokens=800)
                            _resp_conv = _r.choices[0].message.content
                            p["historico_conv"].append({"role": "user", "content": _fala})
                            p["historico_conv"].append({"role": "assistant", "content": _resp_conv})
                            st.rerun()
                        except Exception as _e:
                            st.error(f"Erro: {_e}")
                else:
                    st.warning("Escreva algo para conversar.")
        with _cc2:
            if st.button("🗑️ Limpar conversa", key="conv_clear", use_container_width=True):
                p["historico_conv"] = []
                st.rerun()

    # ── ABA: REVISÃO ──
    with _tab_revisao:
        st.header("🔄 Revisão Espaçada")
        st.markdown("*O sistema identifica o que você precisa revisar para não esquecer.*")

        if not _revisoes:
            st.markdown("<div class='card-success'>✅ <b>Nenhuma revisão pendente!</b> Você está em dia com o conteúdo aprendido.</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='card-revisao'>⏰ <b>{len(_revisoes)} habilidade(s) para revisar hoje.</b></div>", unsafe_allow_html=True)
            for _hid in _revisoes[:3]:
                st.markdown(f"- **{_hid.replace('_',' ')}** — domínio atual: {int(p['habilidades'][_hid].get('dominio',0)*100)}%")

        _rev_pedido = st.text_area("Ou peça uma revisão específica:", height=90, key="rev_in", placeholder="Ex: quero revisar present perfect, phrasal verbs, vocabulário de viagem...")
        if st.button("🤖 GERAR REVISÃO PERSONALIZADA", key="rev_btn", use_container_width=True):
            _conteudo_rev = _rev_pedido.strip()
            if not _conteudo_rev and _revisoes:
                _conteudo_rev = f"Revisão das habilidades: {', '.join(_revisoes[:3])}"
            elif not _conteudo_rev:
                _conteudo_rev = f"Revisão geral do nível {_nivel}"
            with st.spinner("Preparando revisão..."):
                _r = chamar_ia([{"role": "user", "content": f"Faça uma revisão de: {_conteudo_rev}. Use o método Nexus: apresente a explicação, pergunte primeiro, corrija com clareza. Uma pergunta por vez para começar."}], max_tokens=1200)
                st.markdown(f"<div class='card-professor'>🎓 <b>Nexus:</b> {_r}</div>", unsafe_allow_html=True)

        _resp_rev = st.text_area("Sua resposta:", height=80, key="rev_resp_in", placeholder="Responda o exercício de revisão...")
        if st.button("📩 ENVIAR RESPOSTA", key="rev_resp_btn", use_container_width=True):
            if _resp_rev.strip():
                with st.spinner("Corrigindo..."):
                    _r2 = chamar_ia([{"role": "user", "content": f"Avalie minha resposta nesta revisão: '{_resp_rev}'. Corrija com o protocolo completo: resposta original, resposta esperada, explicação, nova tentativa."}], max_tokens=800)
                    st.markdown(f"<div class='card-professor'>🎓 <b>Nexus:</b> {_r2}</div>", unsafe_allow_html=True)

    # ── ABA: EXERCÍCIOS ──
    with _tab_exercicios:
        st.header("🎯 Exercícios Interativos")
        st.markdown("*Pratique com exercícios gerados pelo professor para o seu nível.*")

        _tipo_ex = st.selectbox("Tipo de exercício:", [
            "Fill in the blanks (complete as lacunas)",
            "Multiple choice (múltipla escolha)",
            "Tradução de frases (PT → EN)",
            "Tradução de frases (EN → PT)",
            "Corrija o erro na frase",
            "Ordene as palavras para formar a frase",
            "Transformação de frase (ativo → passivo / etc.)",
            "Perguntas e respostas em inglês",
            "Diálogo incompleto para completar",
        ], key="ex_tipo")
        _tema_ex = st.text_input("Tema ou conteúdo (opcional):", placeholder=f"Ex: present perfect, vocabulário de trabalho... (padrão: nível {_nivel})", key="ex_tema")
        _qtd_ex = st.slider("Questões:", 3, 10, 5, key="ex_qtd")

        if st.button("🎯 GERAR EXERCÍCIOS", key="ex_gerar", use_container_width=True):
            with st.spinner("Criando exercícios personalizados..."):
                _tema_str = _tema_ex.strip() if _tema_ex.strip() else f"conteúdo do nível {_nivel}"
                _r = chamar_ia([{"role": "user", "content": f"Crie {_qtd_ex} exercícios do tipo '{_tipo_ex}' sobre {_tema_str}, adaptados ao nível {_nivel}. Apresente os exercícios primeiro. Ao final, coloque o GABARITO completo com explicações em português. Seja didático."}], max_tokens=2048)
                st.markdown(f"<div class='card'>{_r}</div>", unsafe_allow_html=True)

        st.markdown("---")
        _resp_ex = st.text_area("Suas respostas:", height=100, key="ex_resp_in", placeholder="Digite suas respostas aqui para o professor corrigir...")
        if st.button("📩 ENVIAR PARA CORREÇÃO", key="ex_corr_btn", use_container_width=True):
            if _resp_ex.strip():
                with st.spinner("Corrigindo..."):
                    _r2 = chamar_ia([{"role": "user", "content": f"O aluno (nível {_nivel}) enviou as seguintes respostas para correção: '{_resp_ex}'. Corrija cada uma, mostre a resposta certa, explique o erro e dê uma nova oportunidade de praticar."}], max_tokens=1200)
                    st.markdown(f"<div class='card-professor'>🎓 <b>Nexus:</b> {_r2}</div>", unsafe_allow_html=True)
                    registrar_tentativa("exercicios_gerais", True, "hesitante")

    # ── ABA: VOCABULÁRIO ──
    with _tab_vocab:
        st.header("📖 Vocabulário")
        st.markdown("*Aprenda palavras novas e revise as que você está estudando.*")

        # Vocabulário do aluno
        _vocab_aluno = p.get("vocabulario", [])
        if _vocab_aluno:
            st.markdown(f"**Seu vocabulário pessoal ({len(_vocab_aluno)} palavra(s)):**")
            for _v in _vocab_aluno[-10:]:
                _dom_v = int(_v.get("dominio", 0) * 100)
                st.markdown(f"- **{_v['word']}** — {_v.get('meaning_pt','?')} &nbsp; `{_dom_v}% domínio`")
            st.markdown("---")

        _tipo_v = st.selectbox("O que você quer aprender?", [
            "Lista de vocabulário essencial para meu nível",
            "Palavras sobre um tema específico",
            "Família de palavras (word family)",
            "Sinônimos e antônimos",
            "Phrasal verbs",
            "Idioms e expressões",
            "Vocabulário de negócios",
            "Palavras mais cobradas em IELTS/TOEFL",
        ], key="vocab_tipo")
        _tema_v = st.text_input("Tema específico (opcional):", placeholder="Ex: tecnologia, saúde, família...", key="vocab_tema")

        if st.button("📖 GERAR LISTA", key="vocab_gerar", use_container_width=True):
            with st.spinner("Montando vocabulário..."):
                _tema_vstr = f"tema '{_tema_v}'" if _tema_v.strip() else f"nível {_nivel}"
                _r = chamar_ia([{"role": "user", "content": f"Crie uma lista de vocabulário para {_tema_vstr}. Tipo: {_tipo_v}. Nível: {_nivel}. Formato: palavra em inglês | tradução | exemplo de frase. Inclua 15 itens e uma dica de memorização ao final."}], max_tokens=1500)
                st.markdown(f"<div class='card'>{_r}</div>", unsafe_allow_html=True)

        st.markdown("---")
        _nova_palavra = st.text_input("Adicionar palavra ao meu vocabulário:", placeholder="Ex: although", key="vocab_add_word")
        _nova_trad = st.text_input("Tradução:", placeholder="Ex: embora, apesar de", key="vocab_add_trad")
        if st.button("➕ ADICIONAR", key="vocab_add_btn", use_container_width=True):
            if _nova_palavra.strip():
                p["vocabulario"].append({
                    "word": _nova_palavra.strip(),
                    "meaning_pt": _nova_trad.strip(),
                    "dominio": 0.0,
                    "next_review": str(date.today() + timedelta(days=1))
                })
                st.success(f"✅ '{_nova_palavra}' adicionada ao seu vocabulário!")
                st.rerun()

    # ── ABA: PROGRESSO ──
    with _tab_progresso:
        st.header("📈 Meu Progresso")

        _nivel_idx = NIVEIS_ORDEM.index(_nivel) if _nivel in NIVEIS_ORDEM else 0
        _prog_nivel = (_nivel_idx / (len(NIVEIS_ORDEM) - 1)) * 100

        st.markdown(f"**Nível atual:** <span class='nivel-tag nivel-{_nivel}'>{_nivel} — {NIVEL_DESC.get(_nivel,'')}</span>", unsafe_allow_html=True)
        st.markdown(f"<div class='prog-bar-bg'><div class='prog-bar-fill' style='width:{int(_prog_nivel)}%'></div></div>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:#475569;font-size:0.85em'>A1 ──── A2 ──── B1 ──── B2 ──── C1 ──── C2</p>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("**Unidade atual:**")
        _uid2, _utit2, _utip2 = _unidade
        st.markdown(f"📌 **{_utit2}** ({_utip2})")

        if p["habilidades"]:
            st.markdown("---")
            st.markdown("**Habilidades praticadas:**")
            for _hid, _h in list(p["habilidades"].items())[:15]:
                _dom = int(_h.get("dominio", 0) * 100)
                _bar_color = "#10B981" if _dom >= 85 else "#6366F1" if _dom >= 50 else "#F59E0B"
                st.markdown(f\"\"\"
                <div style='margin-bottom:10px'>
                    <div style='display:flex;justify-content:space-between;font-size:0.85em;color:#475569'>
                        <span>{_hid.replace('_',' ')}</span><span>{_dom}%</span>
                    </div>
                    <div class='prog-bar-bg'>
                        <div style='height:10px;border-radius:8px;background:{_bar_color};width:{_dom}%'></div>
                    </div>
                </div>
                \"\"\", unsafe_allow_html=True)

        if p.get("erros_recorrentes"):
            st.markdown("---")
            st.markdown("**⚠️ Pontos de atenção (erros recorrentes):**")
            for _e in p["erros_recorrentes"][:5]:
                st.markdown(f"- {_e.replace('_',' ')}")

    # ── ABA: EXPLORAR ──
    with _tab_explorar:
        st.header("🗺️ Explorar Conteúdo")
        st.markdown("*Explore o currículo completo ou peça aulas sobre qualquer tema.*")

        # Currículo completo
        for _n in NIVEIS_ORDEM:
            _cor = "#6366F1" if _n == _nivel else "#CBD5E1"
            _label = f"{'✅ ' if _n < _nivel else '📌 ' if _n == _nivel else '🔒 '}{_n} — {NIVEL_DESC.get(_n,'')}"
            with st.expander(_label):
                for _u in CURRICULO.get(_n, []):
                    _uid_u, _titulo_u, _tipo_u = _u
                    _praticado = _uid_u in p.get("habilidades", {})
                    _icon = "✅" if _praticado and p["habilidades"][_uid_u].get("dominio",0) >= 0.85 else "🔵" if _praticado else "⬜"
                    st.markdown(f"{_icon} **{_titulo_u}** — _{_tipo_u}_")

        st.markdown("---")
        st.markdown("**Aula livre — explore qualquer tema:**")
        _tema_livre_exp = st.text_area("O que você quer aprender agora?", height=90, key="exp_tema", placeholder="Ex: me ensine os tempos verbais do passado, quero aprender sobre business english, explique conditional sentences...")
        if st.button("🤖 PEDIR AULA ESPECÍFICA", key="exp_btn", use_container_width=True):
            if _tema_livre_exp.strip():
                with st.spinner("Preparando aula..."):
                    _r = chamar_ia([{"role": "user", "content": f"O aluno (nível {_nivel}, objetivo: {p['objetivo']}) quer aprender: {_tema_livre_exp}. Inicie a aula com explicação clara, exemplos e proponha o primeiro exercício interativo."}], max_tokens=1500)
                    st.markdown(f"<div class='card-professor'>🎓 <b>Nexus:</b> {_r}</div>", unsafe_allow_html=True)
            else:
                st.warning("Descreva o que você quer aprender.")

# --- RODAPÉ ---
st.markdown(
    "<div style='text-align:center;color:#CBD5E1;font-size:0.8em;margin-top:60px;'>"
    "© 2026 Nexus English — Professor Adaptativo de Inglês · MeusAgentesIA.com.br"
    "</div>", unsafe_allow_html=True
)
""",
    "sherlock_ia": """# [hub] import streamlit as st
# [hub] from groq import Groq
# [hub] from datetime import datetime
# [hub] import json
# [hub] import re

# --- CONFIGURAÇÃO DA PÁGINA ---
# set_page_config removido pelo super_agente

st.markdown(\"\"\"
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
[data-testid="stToolbar"] {visibility: hidden;}
[data-testid="stDecoration"] {visibility: hidden;}
[data-testid="stStatusWidget"] {visibility: hidden;}
</style>
\"\"\", unsafe_allow_html=True)


# --- ESTILO CSS ---
st.markdown(\"\"\"
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    .stApp { background-color:#F8F9FA; font-family:'Inter',sans-serif; }
    [data-testid="stSidebar"] { display:none; }

    .stTextInput>div>div>input, .stTextArea>div>textarea,
    .stSelectbox>div>div>div, .stNumberInput>div>div>input {
        background-color:#FFFFFF !important; color:#1A1A2E !important;
        border:1px solid #CED4DA !important; font-family:'Inter',sans-serif !important;
    }

    .stButton>button {
        width:100%; border-radius:10px; height:3.2em;
        background:linear-gradient(135deg,#495057,#343A40) !important; color:white !important;
        font-weight:600; border:none; box-shadow:2px 2px 8px rgba(0,0,0,0.1);
        font-family:'Inter',sans-serif !important; transition:all 0.2s ease;
    }
    .stButton>button:hover { background:linear-gradient(135deg,#343A40,#212529) !important; transform:translateY(-1px); }
    .stApp .stButton>button, .stApp .stButton>button p,
    .stApp .stButton>button span, .stApp .stButton>button div { color:white !important; }

    .stApp h1, .stApp h2, .stApp h3 { color:#1A1A2E !important; font-family:'Inter',sans-serif !important; font-weight:700 !important; }

    .card { background:linear-gradient(135deg,#F1F3F5,#E9ECEF); padding:20px; border-radius:14px; border:1px solid #CED4DA; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card, .stApp .card p, .stApp .card span, .stApp .card div, .stApp .card strong, .stApp .card em { color:#1A1A2E !important; }

    .card-dark { background:linear-gradient(135deg,#E9ECEF,#DEE2E6); padding:20px; border-radius:14px; border:1px solid #ADB5BD; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-dark, .stApp .card-dark p, .stApp .card-dark span, .stApp .card-dark div, .stApp .card-dark strong { color:#1A1A2E !important; }

    .card-green { background:linear-gradient(135deg,#F0FDF4,#DCFCE7); padding:20px; border-radius:14px; border:1px solid #86EFAC; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-green, .stApp .card-green p, .stApp .card-green span, .stApp .card-green div { color:#14532D !important; }

    .card-blue { background:linear-gradient(135deg,#EFF6FF,#DBEAFE); padding:20px; border-radius:14px; border:1px solid #93C5FD; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-blue, .stApp .card-blue p, .stApp .card-blue span, .stApp .card-blue div { color:#1E3A8A !important; }

    .card-red { background:linear-gradient(135deg,#FFF5F5,#FEE2E2); padding:20px; border-radius:14px; border:1px solid #FECACA; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-red, .stApp .card-red p, .stApp .card-red span, .stApp .card-red div { color:#7F1D1D !important; }

    .card-yellow { background:linear-gradient(135deg,#FFFBEB,#FEF3C7); padding:18px; border-radius:12px; border:1px solid #FCD34D; margin-bottom:12px; white-space:normal; word-wrap:break-word; }
    .stApp .card-yellow, .stApp .card-yellow p, .stApp .card-yellow span, .stApp .card-yellow div { color:#78350F !important; }

    .stat-box { background:#FFFFFF; border-radius:12px; padding:16px; text-align:center; border:1px solid #CED4DA; }
    .stApp .stat-box div, .stApp .stat-box span, .stApp .stat-box p { color:#1A1A2E !important; }
    .stApp .stat-numero, .stat-numero { font-size:2em; font-weight:700; color:#495057 !important; }

    .hist-item { background:#FFFFFF; border-radius:10px; padding:12px 16px; margin-bottom:8px; border-left:4px solid #CED4DA; }
    .stApp .hist-item, .stApp .hist-item p, .stApp .hist-item span, .stApp .hist-item div, .stApp .hist-item small { color:#1A1A2E !important; }

    .badge { background:#495057; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-verde { background:#059669; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-amarelo { background:#B45309; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-azul { background:#1D4ED8; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-roxo { background:#6D28D9; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }

    .divider { border:none; height:1px; background:linear-gradient(to right,transparent,#CED4DA,transparent); margin:18px 0; }

    .chat-user { background:#FFFFFF; border:1px solid #CED4DA; border-radius:12px 12px 4px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-user, .stApp .chat-user p, .stApp .chat-user span, .stApp .chat-user div { color:#1A1A2E !important; }

    .chat-persona { background:#F8F9FA; border:1px solid #CED4DA; border-radius:4px 12px 12px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-persona, .stApp .chat-persona p, .stApp .chat-persona span, .stApp .chat-persona div { color:#1A1A2E !important; }

    .questao-box { background:#FFFFFF; border:2px solid #CED4DA; border-radius:12px; padding:18px; margin-bottom:14px; }
    .stApp .questao-box, .stApp .questao-box p, .stApp .questao-box span, .stApp .questao-box div { color:#1A1A2E !important; }

    .avaliacao-box { background:#FFFFFF; border:2px solid #CED4DA; border-radius:14px; padding:18px; margin-bottom:12px; }
    .stApp .avaliacao-box, .stApp .avaliacao-box p, .stApp .avaliacao-box span, .stApp .avaliacao-box div { color:#1A1A2E !important; }

    .meta-box { background:#FFFFFF; border:2px solid #CED4DA; border-radius:12px; padding:16px; text-align:center; margin:10px 0; }
    .stApp .meta-box, .stApp .meta-box div, .stApp .meta-box span { color:#1A1A2E !important; }
    .stApp .meta-numero { font-size:2em; font-weight:700; color:#495057 !important; }

    .chat-scroll-container { max-height:40vh; overflow-y:auto; display:flex; flex-direction:column; scroll-behavior:smooth; padding-bottom:4px; }
    .chat-scroll-container > * { flex-shrink:0; }
    

    </style>
\"\"\", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CACHE
# ─────────────────────────────────────────────
@st.cache_resource
def get_cache_sherlock():
    return {"perfis": {}}

_cache = get_cache_sherlock()

# ─────────────────────────────────────────────
# PERSISTÊNCIA LOCAL (JSON)
# ─────────────────────────────────────────────
CHAVES_SALVAR = [
    'usuario', 'historico_casos', 'casos_salvos',
    'caso_padrao', 'diario_investigador', 'desafio_pontuacao', 'desafio_nivel_atual',
    'casos_resolvidos_count', 'evidencias_cadastradas_count',
]

def gerar_json_sessao() -> str:
    dados = {k: st.session_state.get(k) for k in CHAVES_SALVAR}
    dados['salvo_em'] = datetime.now().strftime('%d/%m/%Y %H:%M')
    return json.dumps(dados, ensure_ascii=False, indent=2, default=str)

def carregar_json_sessao(dados):
    _bloq = {'api_key','etapa','nome_login','chave_login','upload_login','btn_entrar_login'}
    _pref = (
        'btn_','sel_','ul_','dl_','cad_','_sub','_sm','_tab','_bsc',
        'ativo_','rem_','sel_pet_','ev_','prof_','hig_','prev_',
        'vac_','sint_','comp_','trad_','subs_','amb_','viag_','chat_',
        'duvida_','emerg_','peso_','data_','obs_','tipo_','vet_','desc_',
        'local_','prox_','alim','sit_emerg_','tc_','oraf','siau','agmag',
        'lv','mv','pt','pi','sh','wc','rv','rp','rc',
    )
    import re as _re
    for k, v in dados.items():
        if k in _bloq: continue
        if any(k.startswith(p) for p in _pref): continue
        if _re.match(r'.+_\\d+$', k): continue
        st.session_state[k] = v

def salvar_perfil_cache(usuario: str):
    _cache["perfis"][usuario] = {k: st.session_state.get(k) for k in CHAVES_SALVAR}

def perfis_salvos() -> list:
    return list(_cache["perfis"].keys())

def carregar_perfil_cache(usuario: str) -> dict | None:
    return _cache["perfis"].get(usuario)

def salvar_caso(modulo: str, tema: str, conteudo: str):
    st.session_state.historico_casos.append({
        'data': datetime.now().strftime('%d/%m %H:%M'), 'modulo': modulo, 'tema': tema, 'conteudo': conteudo,
    })

# --- INICIALIZAÇÃO DE ESTADO ---
defaults = {
    'etapa': "Login", 'usuario': "", 'api_key': "", 'pagina': "Home",
    'historico_casos': [], 'casos_salvos': [],
    'caso_padrao': "", 'diario_investigador': [], 'desafio_pontuacao': 0, 'desafio_nivel_atual': "Iniciante",
    'casos_resolvidos_count': 0, 'evidencias_cadastradas_count': 0,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

NIVEIS_DESAFIO = ["Iniciante", "Investigador", "Inspetor", "Mestre", "Sherlock"]
CLASSES_NIVEL = {"Iniciante":"badge-nivel-iniciante","Investigador":"badge-nivel-investigador","Inspetor":"badge-nivel-inspetor","Mestre":"badge-nivel-mestre","Sherlock":"badge-nivel-sherlock"}

# --- PRINCÍPIO DE RIGOR LÓGICO E RESPONSABILIDADE — compartilhado ---
PRINCIPIO_RIGOR = \"\"\"
PRINCÍPIO OBRIGATÓRIO DE RIGOR LÓGICO E RESPONSABILIDADE — siga isso em TODA resposta:
- Você é um consultor de raciocínio lógico e investigação, inspirado no método de observação, dedução e eliminação
  de hipóteses — mas você NÃO é perito forense oficial, detetive licenciado, psicólogo ou advogado
- Trabalhe SEMPRE a partir do que foi descrito em texto pela pessoa — você não recebe fotos, vídeos ou áudios reais,
  então para "análise de imagem" trabalhe com a descrição detalhada que a pessoa fornecer
- NUNCA afirme com certeza absoluta que algo é verdade sobre uma pessoa real e terceira (ex: "ele está mentindo",
  "ela está tendo um caso") — use sempre linguagem de hipótese: "isso poderia indicar", "um padrão possível seria",
  "vale considerar, mas não é conclusivo"
- Para Perfil Comportamental e Análise de Conversas envolvendo pessoas reais: trate tudo como HIPÓTESES para reflexão
  do próprio usuário, nunca como diagnóstico ou prova. Lembre, quando relevante, que ler demais nas entrelinhas de
  mensagens reais tem limites — más interpretações são comuns e a melhor fonte de verdade é conversar diretamente
  com a pessoa envolvida
- Para o Laboratório Forense Educativo: explique COMO a ciência forense funciona em princípio (conceitos, método,
  cadeia de custódia) — isso é educativo. NUNCA forneça instruções operacionais sobre como evitar, burlar ou enganar
  uma perícia real (remover vestígios, burlar coleta de DNA, etc) — se a pergunta pedir isso, redirecione para o
  aspecto educativo de como a perícia funciona, sem fornecer o "como evitar ser detectado"
- Para Fraudes e Golpes / Investigação Digital: foco é proteção e reconhecimento, nunca como executar um golpe
- Casos, mistérios e desafios do Simulador, Sala de Casos Impossíveis e Academia Sherlock são sempre FICTÍCIOS —
  invente livremente, com boa qualidade narrativa e lógica consistente
- Você pode e deve ser envolvente, dramático e didático no tom — isso é parte da experiência — mas a responsabilidade
  com fatos reais e pessoas reais é inegociável
- Português do Brasil
\"\"\"

DISCLAIMER_PADRAO = \"\"\"
<div class="disclaimer">
⚠️ <strong>Importante:</strong> esta análise é um exercício de raciocínio lógico para apoiar sua reflexão — não é uma
prova, diagnóstico ou conclusão definitiva. Hipóteses geradas por IA podem estar erradas; a melhor fonte de verdade
sobre uma situação real é sempre investigação cuidadosa e, quando envolve outra pessoa, conversa direta com ela.
</div>
\"\"\"

DISCLAIMER_COMPORTAMENTAL = \"\"\"
<div class="disclaimer-comportamental">
🧠 <strong>Sobre esta análise comportamental:</strong> isso é uma hipótese especulativa para reflexão, nunca um
diagnóstico psicológico ou prova de intenção. Comportamentos têm múltiplas explicações possíveis, e interpretações
à distância são frequentemente erradas. Use isso como ponto de partida para pensar, não como conclusão.
</div>
\"\"\"

DISCLAIMER_FORENSE = \"\"\"
<div class="disclaimer-forense">
🧪 <strong>Conteúdo educativo:</strong> esta seção explica princípios gerais de ciência forense para fins de
aprendizado — não é um manual operacional, não substitui peritos reais, e não deve ser usada para interferir em
investigações ou evidências reais.
</div>
\"\"\"

# --- MOTOR DE IA ---
def sherlock_ia(prompt: str, system_extra: str = "") -> str:
    try:
        client = Groq(api_key=st.session_state.api_key)
        system = f\"\"\"Você é Sherlock IA — um consultor de investigação lógica, raciocínio dedutivo e pensamento REGRA DE OURO — CONFIABILIDADE 100%%: Forneça APENAS informações que você tem certeza absoluta que são verdadeiras. JAMAIS invente, suponha, extrapole ou preencha lacunas com dados fictícios. Se não souber algo com certeza — preço, endereço, horário, nome, estatística, lei, fato — diga EXPLICITAMENTE: 'Não tenho certeza sobre isso, recomendo verificar em [fonte].' É melhor uma resposta incompleta e honesta do que uma resposta completa e inventada. O usuário depende dessas informações para tomar decisões reais.
crítico, inspirado nos grandes métodos investigativos clássicos.
Usuário: {st.session_state.usuario}. Caso atual: {st.session_state.caso_padrao or 'não informado'}.
{PRINCIPIO_RIGOR}
{system_extra}\"\"\"
        response = client.chat.completions.create(
            messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}],
            model="openai/gpt-oss-120b",
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Erro na API: {e}"

def renderizar_indice(texto: str, titulo_indice: str = "CONSISTÊNCIA"):
    percentuais = re.findall(r'(\\d+)\\s*/\\s*100|(\\d+)%', texto)
    valores = [int(a or b) for a, b in percentuais if a or b]
    indice = valores[0] if valores else 50

    if indice >= 70:
        classe, emoji, label = "indice-alto", "🟢", "ALTA"
    elif indice >= 40:
        classe, emoji, label = "indice-medio", "🟡", "MÉDIA"
    else:
        classe, emoji, label = "indice-baixo", "🔴", "BAIXA"

    st.markdown(f\"\"\"
    <div class="indice-box {classe}">
        <div style="font-size:2.2em;">{emoji}</div>
        <div class="indice-titulo">{titulo_indice}: {indice}/100</div>
        <div style="font-size:0.95em;color:#444;font-weight:600;">Nível: {label}</div>
        <div style="font-size:0.82em;color:#555;margin-top:6px;">Estimativa baseada nas informações fornecidas</div>
    </div>
    \"\"\", unsafe_allow_html=True)

# --- BARRA DE SALVAR ---
def barra_salvar():
    salvar_perfil_cache(st.session_state.usuario)
    nome_usuario = st.session_state.usuario.lower().replace(' ', '_') or 'minha_sessao'
    total = len(st.session_state.historico_casos)
    diario = len(st.session_state.diario_investigador)

    col_info, col_btn = st.columns([4, 2])
    with col_info:
        st.markdown(
            f"<div style='background:#F1F5F9;border:1px solid #334155;border-radius:10px;"
            f"padding:10px 14px;font-size:0.84em;color:#1A1A2E;line-height:1.6;'>"
            f"💾 <strong>Antes de sair, salve seus dados no computador.</strong><br>"
            f"<span style='color:#888;font-size:0.88em;'>{total} análises geradas · {diario} casos no diário</span>"
            f"</div>", unsafe_allow_html=True
        )
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown(\"\"\"<style>
    .dica-nav{font-size:0.72em;color:#94A3B8;text-align:center;padding:2px 0 6px;}
    .dica-mobile{display:none;}
    .dica-desktop{display:block;}
    @media(max-width:768px){.dica-mobile{display:block;}.dica-desktop{display:none;}}
    </style>
    <div class='dica-nav dica-mobile'>👆 Deslize o dedo para navegar entre as abas</div>
    <div class='dica-nav dica-desktop'>📋 Clique no ícone acima para abrir o menu completo</div>
    \"\"\", unsafe_allow_html=True)

# ============================================================
# TELA: LOGIN
# ============================================================
if 'caso_padrao' not in st.session_state: st.session_state['caso_padrao'] = None
if 'casos_resolvidos_count' not in st.session_state: st.session_state['casos_resolvidos_count'] = None
if 'casos_salvos' not in st.session_state: st.session_state['casos_salvos'] = None
if 'desafio_nivel_atual' not in st.session_state: st.session_state['desafio_nivel_atual'] = None
if 'desafio_pontuacao' not in st.session_state: st.session_state['desafio_pontuacao'] = None
if 'diario_investigador' not in st.session_state: st.session_state['diario_investigador'] = None
if 'evidencias_cadastradas_count' not in st.session_state: st.session_state['evidencias_cadastradas_count'] = None
if 'historico_casos' not in st.session_state: st.session_state['historico_casos'] = []

if st.session_state.etapa == "Login":
    st.markdown("# 🤖 SHERLOCK IA")
    st.markdown("<div class=\\'card\\'><b>🔒 ACESSO RESTRITO A CLIENTES DO MEUSAGENTESIA.COM.BR</b><br>🔗 <a href='https://meusagentesia.com.br' target='_blank' style='color:#4F46E5;font-weight:700;text-decoration:underline;'>meusagentesia.com.br</a></div>", unsafe_allow_html=True)
    st.info("💻 **Dica:** Pela complexidade dos agentes, no computador a experiência é mais agradável.")
    with st.container():
        nome  = st.text_input("Seu Nome:", key="nome_login")
        chave = st.text_input("🔑 Sua Chave API da Groq:", type="password", key="chave_login")
        if st.button("✨ ENTRAR", key="btn_entrar_login"):
            if len(nome.strip()) < 2:
                st.warning("Digite um nome com pelo menos 2 caracteres.")
            elif chave.strip():
                st.session_state.usuario = nome.strip()
                st.session_state.api_key = chave
                st.session_state.etapa = "App"
                st.rerun()
            else:
                st.warning("Preencha nome e chave API.")

elif st.session_state.etapa == "App":



    # TABS
    _tab_Home, _tab_Investigacao, _tab_Hipoteses, _tab_Evidencias, _tab_Timeline, _tab_Contradicoes, _tab_Perfil, _tab_Conversas, _tab_Imagens, _tab_Domestica, _tab_Digital, _tab_Fraudes, _tab_Padroes, _tab_Probabilidades, _tab_Perguntas, _tab_Critico, _tab_Metodo, _tab_Forense, _tab_Casos, _tab_Simulador, _tab_Diario, _tab_Painel, _tab_Academia, _tab_Desafio, _tab_Sherlock24, _tab_CasosImpossiveis, _tab_Biblioteca = st.tabs(['🏠 Painel Principal', '🔎 Investigação Geral', '🧩 Construção de Hipó', '📋 Organizador de Evi', '📄 Timeline', '📄 Contradicoes', '📄 Perfil', '📄 Conversas', '📄 Imagens', '📄 Domestica', '📄 Digital', '📄 Fraudes', '📄 Padroes', '📄 Probabilidades', '📄 Perguntas', '📄 Critico', '📄 Metodo', '📄 Forense', '📄 Casos', '📄 Simulador', '📄 Diario', '📄 Painel', '📄 Academia', '📄 Desafio', '📄 Sherlock24', '📄 CasosImpossiveis', '📄 Biblioteca'])

    # ── BARRA SALVAR — aparece em todas as abas ──
    with st.expander("💾 Salvar / Carregar meus dados", expanded=False):
        _bsc1, _bsc2 = st.columns(2)
        with _bsc1:
            import json as _jsv
            _dsv = {k: st.session_state.get(k) for k in list(st.session_state.keys()) if not k.startswith('_') and k not in ('api_key',)}
    # TABS — navegação nativa (16 + Ferramentas)
    (_tab_Home, _tab_Investigacao, _tab_Hipoteses, _tab_Evidencias, _tab_Timeline, _tab_Simulador, _tab_Diario, _tab_Painel, _tab_Academia, _tab_Desafio, _tab_Sherlock24, _tab_CasosImpossiveis, _tab_Biblioteca, _tab_Forense, _tab_Casos, _tab_Ferramentas) = st.tabs(['🏠 Home', '🔍 Investigação', '💡 Hipóteses', '🔬 Evidências', '⏱️ Timeline', '🎯 Simulador', '📖 Diário', '📈 Painel', '🎓 Academia', '🏆 Desafio', '🤖 Sherlock 24h', '💎 Casos Impossíveis', '📚 Biblioteca', '🧪 Lab Forense', '📋 Casos Históricos', '🛠️ Ferramentas'])

    with _tab_Home:
        col_u, col_r = st.columns([3, 1])
        with col_u:
            st.title(f"Olá, {st.session_state.usuario}! 🕵️")
            nivel_atual = st.session_state.desafio_nivel_atual
            st.markdown(f"<span class='{CLASSES_NIVEL.get(nivel_atual,'badge')}'>{nivel_atual}</span>", unsafe_allow_html=True)
        with col_r:
            if st.button("🚪 Sair", key="sherlock3"):
                for k in list(st.session_state.keys()):
                    del st.session_state[k]
                st.rerun()

        if len(st.session_state.historico_casos) == 0:
            st.markdown(\"\"\"<div style="background:#FEF3C7;border:2px solid #F59E0B;border-radius:12px;
            padding:12px 18px;margin-bottom:4px;color:#000;font-size:0.9em;font-weight:600;">
            ⚠️ Seus dados não estão mais no servidor.
            </div>\"\"\", unsafe_allow_html=True)
        st.session_state.caso_padrao = st.text_area("🔎 Caso/situação que você está investigando:",
            value=st.session_state.caso_padrao, height=80,
            placeholder="ex: Estou tentando entender um problema estranho que aconteceu no trabalho...", key="sherlock15")


        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f"<div class='stat-box'><div class='stat-numero'>{len(st.session_state.historico_casos)}</div><div>Análises geradas</div></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='stat-box'><div class='stat-numero'>{st.session_state.casos_resolvidos_count}</div><div>Casos resolvidos</div></div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='stat-box'><div class='stat-numero'>{st.session_state.evidencias_cadastradas_count}</div><div>Evidências cadastradas</div></div>", unsafe_allow_html=True)
        c4.markdown(f"<div class='stat-box'><div class='stat-numero'>{st.session_state.desafio_pontuacao}</div><div>Pontos no Desafio</div></div>", unsafe_allow_html=True)

        st.markdown("<div class='card'>🕵️ <em>'Quando você elimina o impossível, o que restar, ainda que improvável, deve ser a verdade.'</em></div>", unsafe_allow_html=True)

        st.markdown("### 🗺️ O que cada módulo faz")
        guia = {
            "🔎 Investigação Geral": "Descreva qualquer situação — fatos, pessoas, linha do tempo e hipóteses organizados",
            "🧩 Construção de Hipóteses": "Cenários possíveis com probabilidade, pontos a favor e contra",
            "📋 Organizador de Evidências": "Cadastre fotos, documentos, locais, datas e pessoas de um caso",
            "⏳ Linha do Tempo": "Reconstrói a sequência dos acontecimentos e identifica lacunas",
            "🎭 Detector de Contradições": "Cole relatos e identifique mudanças de versão e conflitos",
            "👤 Perfil Comportamental": "Hipóteses sobre padrões de comportamento — nunca diagnóstico",
            "💬 Análise de Conversas": "Tom, contradições, assuntos evitados em conversas que você já tem",
            "📸 Análise de Imagens": "Descreva uma cena em detalhes para análise investigativa",
            "🏠 Investigação Doméstica": "Vazamentos, ruídos, cheiros, infiltrações — descubra a causa",
            "💻 Investigação Digital": "Sites suspeitos, perfis falsos, engenharia social",
            "💰 Fraudes e Golpes": "Como funcionam, como identificar e como se proteger",
            "🔍 Detector de Padrões": "Relações escondidas entre datas, pessoas, lugares e eventos",
            "📊 Análise de Probabilidades": "Quais hipóteses são mais consistentes com as evidências",
            "❓ Perguntas Inteligentes": "As perguntas que um investigador faria e você talvez não pensou",
            "⚖️ Pensamento Crítico": "Identifique vieses, generalizações e julgamentos precipitados",
            "🧠 Método Sherlock": "Dedução, indução, abdução e eliminação de hipóteses",
            "🧪 Laboratório Forense": "Como funcionam impressões digitais, DNA, balística — educativo",
            "📚 Casos Históricos": "Investigações famosas e o raciocínio usado para resolvê-las",
            "🎯 Simulador de Investigação": "Casos fictícios por categoria e nível de dificuldade",
            "📖 Diário do Investigador": "Salve casos, hipóteses e conclusões",
            "📈 Painel Investigativo": "Acompanhe sua evolução como investigador",
            "🎓 Academia Sherlock": "30 aulas práticas de raciocínio investigativo",
            "🏆 Desafio Sherlock": "5 níveis de dificuldade — de Iniciante a Sherlock",
            "🤖 Sherlock 24h": "Converse livremente sobre qualquer investigação",
            "💎 Sala de Casos Impossíveis": "Dossiês complexos que se revelam por etapas",
        }
        for aba, desc in guia.items():
            st.markdown(f"**{aba}** — {desc}")

        if st.session_state.historico_casos:
            st.markdown("### 🕐 Últimas Análises")
            for item in reversed(st.session_state.historico_casos[-4:]):
                st.markdown(f"<div class='hist-item'><span class='badge'>{item.get('modulo', '')}</span> <small style='color:#888'>{item['data']}</small><br><small>{item.get('tema', '')[:80]}</small></div>", unsafe_allow_html=True)

        # ========================
        # INVESTIGAÇÃO GERAL
        # ========================

        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        st.markdown("### 💾 Salvar e Carregar Dados")
        _csl1, _csl2 = st.columns(2)
        with _csl1:
            import json as _json_sv
            _dados_sv = {k: st.session_state.get(k) for k in list(st.session_state.keys()) if not k.startswith('_')}
    with _tab_Investigacao:
        st.header("🔎 Investigação Geral")
        st.markdown("Descreva a situação. A IA organiza fatos, hipóteses e próximos passos.")

        situacao_inv = st.text_area("📝 Descreva a situação:", height=180, value=st.session_state.caso_padrao,
            placeholder="ex: Notei que um objeto da minha casa desapareceu, e três pessoas estiveram aqui na última semana...", key="sherlock14")

        if st.button("🔎 INVESTIGAR", key="sherlock4"):
            if situacao_inv.strip():
                with st.spinner("Organizando a investigação..."):
                    prompt = (
                        f"Organize uma investigação completa para esta situação.\\n"
                        f"Situação: {situacao_inv}\\n\\n"
                        f"FORMATO:\\n\\n"
                        f"🔎 INVESTIGAÇÃO — {situacao_inv[:50].upper()}\\n\\n"
                        f"✅ FATOS CONHECIDOS:\\n[liste o que é certo, com base no que foi descrito]\\n\\n"
                        f"❓ FATOS DESCONHECIDOS:\\n[o que ainda não se sabe]\\n\\n"
                        f"👥 PESSOAS ENVOLVIDAS:\\n[liste com o papel de cada uma na situação, se mencionadas]\\n\\n"
                        f"📅 LINHA DO TEMPO PRELIMINAR:\\n[ordene os eventos descritos]\\n\\n"
                        f"🔍 EVIDÊNCIAS DISPONÍVEIS:\\n[o que já se tem para analisar]\\n\\n"
                        f"🧩 HIPÓTESES INICIAIS:\\n[2-4 possibilidades, todas como hipóteses, não conclusões]\\n\\n"
                        f"❓ PERGUNTAS IMPORTANTES:\\n[o que precisa ser perguntado/descoberto a seguir]\\n\\n"
                        f"✅ PRÓXIMOS PASSOS DA INVESTIGAÇÃO:\\n[ações concretas para avançar]"
                    )
                    res = sherlock_ia(prompt)
                    if res: st.session_state['res_investigacao_sherlo1'] = str(res)
                    salvar_caso("Investigacao", situacao_inv[:60], res)
                    st.session_state['inv_temp'] = res
                    st.session_state.caso_padrao = situacao_inv
            else:
                st.warning("Descreva a situação.")

        if st.session_state.get('inv_temp'):
            st.markdown(f"<div class='card'>{st.session_state['inv_temp']}</div>", unsafe_allow_html=True)
            st.markdown(DISCLAIMER_PADRAO, unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['inv_temp'], file_name="investigacao.txt", mime="text/plain", use_container_width=True, key="sherlock5")
            with col_sv:
                if st.button("❤️ Salvar", key="sv_inv", use_container_width=True):
                    st.session_state.casos_salvos.append({'modulo':'Investigacao','tema':situacao_inv[:60] if 'situacao_inv' in dir() else '','conteudo':st.session_state['inv_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

        # ========================
        # CONSTRUÇÃO DE HIPÓTESES
        # ========================

    with _tab_Hipoteses:
        st.header("🧩 Construção de Hipóteses")

        situacao_hip = st.text_area("📝 Descreva a situação:", height=120, value=st.session_state.caso_padrao, key="situacao_hip")
        qtd_hip = st.slider("Quantas hipóteses gerar:", 2, 6, 3, key="sherlock1")

        if st.button("🧩 GERAR HIPÓTESES", key="sherlock6"):
            if situacao_hip.strip():
                with st.spinner("Construindo hipóteses..."):
                    prompt = (
                        f"Crie {qtd_hip} hipóteses distintas para explicar esta situação.\\n"
                        f"Situação: {situacao_hip}\\n\\n"
                        f"Para CADA hipótese:\\n\\n"
                        f"🧩 HIPÓTESE [N]: [nome curto]\\n"
                        f"[Descrição da hipótese]\\n"
                        f"📊 Probabilidade estimada: [Baixa/Média/Alta]\\n"
                        f"✔ Pontos favoráveis: [o que sustenta essa hipótese]\\n"
                        f"✘ Pontos contrários: [o que a contradiz ou fragiliza]\\n"
                        f"🔍 Evidências necessárias para confirmar: [o que ajudaria a provar isso]\\n"
                        f"❓ O que ainda precisa ser descoberto:\\n\\n"
                        f"[Repita para as {qtd_hip} hipóteses]\\n\\n"
                        f"🎯 HIPÓTESE MAIS CONSISTENTE ATÉ AGORA:\\n[qual parece mais provável com base no que foi descrito, e por quê — sem afirmar certeza]"
                    )
                    res = sherlock_ia(prompt)
                    if res: st.session_state['res_hipoteses_sherlo2'] = str(res)
                    salvar_caso("Hipoteses", situacao_hip[:60], res)
                    st.session_state['hip_temp'] = res
            else:
                st.warning("Descreva a situação.")

        if st.session_state.get('hip_temp'):
            st.markdown(f"<div class='card'>{st.session_state['hip_temp']}</div>", unsafe_allow_html=True)
            st.markdown(DISCLAIMER_PADRAO, unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['hip_temp'], file_name="hipoteses.txt", mime="text/plain", use_container_width=True, key="sherlock7")
            with col_sv:
                if st.button("❤️ Salvar", key="sv_hip", use_container_width=True):
                    st.session_state.casos_salvos.append({'modulo':'Hipoteses','tema':situacao_hip[:60] if 'situacao_hip' in dir() else '','conteudo':st.session_state['hip_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

        # ========================
        # ORGANIZADOR DE EVIDÊNCIAS
        # ========================

    with _tab_Evidencias:
        st.header("📋 Organizador de Evidências")
        st.markdown("Cadastre evidências do seu caso — tudo fica organizado automaticamente.")

        col1, col2 = st.columns(2)
        with col1:
            tipo_evid = st.selectbox("Tipo de evidência:", ["📸 Foto (descrição)","🎥 Vídeo (descrição)","🎙 Áudio (descrição)","📄 Documento","💬 Conversa","📍 Local","📅 Data/Horário","👥 Pessoa"], key="sherlock8")
            descricao_evid = st.text_area("📝 Descrição da evidência:", height=100, placeholder="ex: Mensagem recebida às 14h32 dizendo que estava no trabalho...", key="sherlock9")
        with col2:
            relevancia_evid = st.selectbox("Relevância:", ["Alta","Média","Baixa","A determinar"], key="sherlock10")
            notas_evid = st.text_input("Notas adicionais (opcional):", placeholder="ex: confirmar com testemunha...", key="sherlock11")

        if st.button("📋 ADICIONAR EVIDÊNCIA", key="sherlock12"):
            if descricao_evid.strip():
                if 'evidencias_lista' not in st.session_state:
                    st.session_state.evidencias_lista = []
                st.session_state.evidencias_lista.append({
                    'tipo': tipo_evid, 'descricao': descricao_evid, 'relevancia': relevancia_evid,
                    'notas': notas_evid, 'data': datetime.now().strftime('%d/%m/%Y %H:%M'),
                })
                st.session_state.evidencias_cadastradas_count += 1
                st.success("✅ Evidência cadastrada!")
                st.rerun()
            else:
                st.warning("Descreva a evidência.")

        if st.session_state.get('evidencias_lista'):
            st.markdown("<hr class='divider'>", unsafe_allow_html=True)
            st.markdown(f"### 📂 Evidências Cadastradas ({len(st.session_state.evidencias_lista)})")
            for i, ev in enumerate(reversed(st.session_state.evidencias_lista)):
                idx_real = len(st.session_state.evidencias_lista) - 1 - i
                cor_rel = "badge-vermelho" if ev.get('relevancia', 0)=="Alta" else ("badge-amarelo" if ev.get('relevancia', 0)=="Média" else "badge")
                with st.expander(f"{ev['tipo']} — {ev['descricao'][:50]} — {ev['data']}"):
                    st.markdown(f"<span class='{cor_rel}'>Relevância: {ev.get('relevancia', 0)}</span>", unsafe_allow_html=True)
                    st.markdown(f"**Descrição:** {ev['descricao']}")
                    if ev.get('notas'):
                        st.markdown(f"**Notas:** {ev.get('notas', 0)}")
                    if st.button("🗑️ Remover", key=f"del_evid_{i}"):
                        st.session_state.evidencias_lista.pop(idx_real)
                        st.session_state.evidencias_cadastradas_count = max(0, st.session_state.evidencias_cadastradas_count - 1)
                        st.rerun()

            if st.button("🤖 ANALISAR TODAS AS EVIDÊNCIAS JUNTAS", key="sherlock13"):
                with st.spinner("Analisando o conjunto..."):
                    evid_txt = "\\n".join([f"- [{e['tipo']}] {e['descricao']} (relevância: {e['relevancia']})" for e in st.session_state.evidencias_lista])
                    prompt = (
                        f"Analise este conjunto de evidências de forma integrada.\\n"
                        f"Evidências:\\n{evid_txt}\\n\\n"
                        f"FORMATO:\\n\\n"
                        f"📋 ANÁLISE DO CONJUNTO DE EVIDÊNCIAS\\n\\n"
                        f"🔗 CONEXÕES ENTRE AS EVIDÊNCIAS:\\n[como elas se relacionam]\\n\\n"
                        f"🧩 O QUE O CONJUNTO SUGERE:\\n[hipóteses que emergem ao olhar tudo junto]\\n\\n"
                        f"⚠️ LACUNAS:\\n[que tipo de evidência ainda falta]\\n\\n"
                        f"🎯 EVIDÊNCIA MAIS DECISIVA:\\n[qual delas mais pesa, e por quê]"
                    )
                    res = sherlock_ia(prompt)
                    if res: st.session_state['res_evidencias_sherlo3'] = str(res)
                    st.session_state['evid_analise_temp'] = res

            if st.session_state.get('evid_analise_temp'):
                st.markdown(f"<div class='card-dark'>{st.session_state['evid_analise_temp']}</div>", unsafe_allow_html=True)

        # ========================
        # LINHA DO TEMPO INTELIGENTE
        # ========================

    with _tab_Timeline:
        st.header("⏳ Linha do Tempo Inteligente")

        eventos_time = st.text_area("📝 Liste os eventos que você conhece (com horários/datas se possível):", height=180,
            placeholder="ex: 14h - mensagem enviada\\n15h30 - chegou em casa\\n16h - notou o problema\\n...", key="sherlock13_d2")

        if st.button("⏳ RECONSTRUIR LINHA DO TEMPO", key="sherlock14_d2"):
            if eventos_time.strip():
                with st.spinner("Reconstruindo..."):
                    prompt = (
                        f"Reconstrua e analise esta linha do tempo.\\n"
                        f"Eventos: {eventos_time}\\n\\n"
                        f"FORMATO:\\n\\n"
                        f"⏳ LINHA DO TEMPO RECONSTRUÍDA\\n\\n"
                        f"📅 SEQUÊNCIA ORDENADA:\\n[eventos em ordem cronológica clara]\\n\\n"
                        f"⏱️ INTERVALOS DE TEMPO:\\n[tempo entre eventos relevantes]\\n\\n"
                        f"⚠️ POSSÍVEIS LACUNAS:\\n[períodos sem informação que merecem atenção]\\n\\n"
                        f"🎭 CONTRADIÇÕES CRONOLÓGICAS:\\n[se houver algo que não bate na sequência temporal]\\n\\n"
                        f"🎯 PONTO MAIS CRÍTICO DA LINHA DO TEMPO:\\n[o momento que merece mais investigação]"
                    )
                    res = sherlock_ia(prompt)
                    if res: st.session_state['res_timeline_sherlo4'] = str(res)
                    salvar_caso("Timeline", "Linha do tempo", res)
                    st.session_state['time_temp'] = res
            else:
                st.warning("Liste os eventos.")

        if st.session_state.get('time_temp'):
            st.markdown(f"<div class='card-blue'>{st.session_state['time_temp']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar (.txt)", data=st.session_state['time_temp'], file_name="linha_do_tempo.txt", mime="text/plain", key="sherlock15_d2")

        # ========================
        # DETECTOR DE CONTRADIÇÕES
        # ========================

    with _tab_Simulador:
        st.header("🎯 Simulador de Investigação")
        st.markdown("Casos fictícios para você resolver.")

        col1, col2 = st.columns(2)
        with col1:
            categoria_sim = st.selectbox("Categoria:", ["🏠 Mistérios domésticos","💰 Fraudes","🏢 Empresas","🔐 Segurança","🧩 Mistérios clássicos"], key="sherlock49")
        with col2:
            dificuldade_sim = st.selectbox("Dificuldade:", ["Fácil","Médio","Difícil","Muito difícil"], key="sherlock50")

        if st.button("🎯 GERAR CASO", key="sherlock51"):
            with st.spinner("Criando o caso..."):
                prompt = (
                    f"Crie um caso investigativo FICTÍCIO para o usuário resolver.\\n"
                    f"Categoria: {categoria_sim}. Dificuldade: {dificuldade_sim}\\n\\n"
                    f"FORMATO:\\n\\n"
                    f"🎯 CASO: [NOME DRAMÁTICO DO CASO]\\n"
                    f"Categoria: {categoria_sim} | Dificuldade: {dificuldade_sim}\\n\\n"
                    f"📖 SITUAÇÃO:\\n[contexto do mistério, envolvente e bem narrado]\\n\\n"
                    f"🔍 PISTAS DISPONÍVEIS:\\n[3-6 pistas, com nível de detalhe proporcional à dificuldade]\\n\\n"
                    f"👥 PERSONAGENS ENVOLVIDOS:\\n[breve descrição de cada um]\\n\\n"
                    f"❓ A PERGUNTA QUE VOCÊ PRECISA RESPONDER:\\n[o que o jogador precisa descobrir]\\n\\n"
                    f"🔒 [NÃO REVELE A SOLUÇÃO AINDA — isso vem só se o usuário pedir a resposta depois]"
                )
                res = sherlock_ia(prompt)
                if res: st.session_state['res_simulador_sherlo5'] = str(res)
                st.session_state['sim_caso_temp'] = res
                st.session_state['sim_caso_categoria'] = categoria_sim
                st.session_state['sim_solucao_revelada'] = False

        if st.session_state.get('sim_caso_temp'):
            st.markdown(f"<div class='dossie-box'>{st.session_state['sim_caso_temp']}</div>", unsafe_allow_html=True)

            if not st.session_state.get('sim_solucao_revelada'):
                sua_solucao = st.text_area("🕵️ Sua solução para o caso:", height=100, key="input_solucao_sim")
                if st.button("🔓 VER A SOLUÇÃO E COMPARAR", key="sherlock52"):
                    with st.spinner("Revelando a solução..."):
                        prompt_solucao = (
                            f"Aqui está o caso que você criou antes:\\n{st.session_state['sim_caso_temp']}\\n\\n"
                            f"O usuário propôs esta solução: {sua_solucao or 'não informou uma solução'}\\n\\n"
                            f"Revele a solução completa do caso e compare com a tentativa do usuário.\\n\\n"
                            f"FORMATO:\\n\\n"
                            f"🔓 SOLUÇÃO DO CASO\\n\\n"
                            f"✅ O QUE REALMENTE ACONTECEU:\\n[solução completa e lógica]\\n\\n"
                            f"🧩 RACIOCÍNIO CORRETO:\\n[como as pistas levavam à solução]\\n\\n"
                            f"📊 SUA TENTATIVA:\\n[comentário sobre a proposta do usuário, reconhecendo acertos]\\n\\n"
                            f"🎯 NOTA: [X]/10\\n[avaliação do raciocínio do usuário]"
                        )
                        res_sol = sherlock_ia(prompt_solucao)
                        if res_sol: st.session_state['res_simulador_sherlo6'] = str(res_sol)
                        st.session_state['sim_solucao_temp'] = res_sol
                        st.session_state['sim_solucao_revelada'] = True
                        st.session_state.casos_resolvidos_count += 1
                        st.rerun()

            if st.session_state.get('sim_solucao_temp'):
                st.markdown(f"<div class='card-gold'>{st.session_state['sim_solucao_temp']}</div>", unsafe_allow_html=True)
                if st.button("🔄 Novo caso", key="sherlock53"):
                    for k in ['sim_caso_temp','sim_solucao_temp','sim_solucao_revelada','sim_caso_categoria']:
                        st.session_state.pop(k, None)
                    st.rerun()

        # ========================
        # DIÁRIO DO INVESTIGADOR
        # ========================

    with _tab_Diario:
        st.header("📖 Diário do Investigador")

        col1, col2 = st.columns(2)
        with col1:
            nome_caso_diario = st.text_input("🔍 Nome do caso:", placeholder="ex: O Mistério do Objeto Desaparecido", key="sherlock54")
            status_diario = st.selectbox("Status:", ["Em andamento","Resolvido","Arquivado","Aguardando mais informações"], key="sherlock55")
        with col2:
            hipotese_diario = st.text_input("🧩 Hipótese principal atual:", placeholder="ex: Alguém pegou por engano...", key="sherlock56")

        conclusao_diario = st.text_area("📝 Notas/conclusões:", height=120, placeholder="ex: Conversei com todos, a evidência mais forte aponta para...", key="sherlock57")

        if st.button("📖 SALVAR NO DIÁRIO", key="sherlock58"):
            if nome_caso_diario.strip():
                st.session_state.diario_investigador.append({
                    'data': datetime.now().strftime('%d/%m/%Y'),
                    'caso': nome_caso_diario, 'status': status_diario,
                    'hipotese': hipotese_diario, 'conclusao': conclusao_diario,
                })
                if status_diario == "Resolvido":
                    st.session_state.casos_resolvidos_count += 1
                st.success("✅ Registrado no diário!")
                st.rerun()
            else:
                st.warning("Nomeie o caso.")

        if st.session_state.diario_investigador:
            st.markdown("<hr class='divider'>", unsafe_allow_html=True)
            st.markdown(f"### 📚 Seus Casos ({len(st.session_state.diario_investigador)})")
            for i, caso in enumerate(reversed(st.session_state.diario_investigador)):
                idx_real = len(st.session_state.diario_investigador) - 1 - i
                cor_status = "badge-verde" if caso['status']=="Resolvido" else ("badge-amarelo" if caso['status']=="Em andamento" else "badge")
                with st.expander(f"🔍 {caso['caso']} — {caso['data']}"):
                    st.markdown(f"<span class='{cor_status}'>{caso['status']}</span>", unsafe_allow_html=True)
                    if caso.get('hipotese'): st.markdown(f"**Hipótese:** {caso['hipotese']}")
                    if caso.get('conclusao'): st.markdown(f"**Notas:** {caso['conclusao']}")
                    if st.button("🗑️ Remover", key=f"del_diario_{i}"):
                        st.session_state.diario_investigador.pop(idx_real)
                        st.rerun()

        # ========================
        # PAINEL INVESTIGATIVO
        # ========================

    with _tab_Painel:
        st.header("📈 Painel Investigativo")

        total_casos = len(st.session_state.historico_casos)
        modulos_count = {}
        for c in st.session_state.historico_casos:
            modulos_count[c['modulo']] = modulos_count.get(c['modulo'], 0) + 1

        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f"<div class='stat-box'><div class='stat-numero'>{st.session_state.casos_resolvidos_count}</div><div>Casos resolvidos</div></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='stat-box'><div class='stat-numero'>{st.session_state.evidencias_cadastradas_count}</div><div>Evidências cadastradas</div></div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='stat-box'><div class='stat-numero'>{total_casos}</div><div>Análises totais</div></div>", unsafe_allow_html=True)
        c4.markdown(f"<div class='stat-box'><div class='stat-numero'>{len(st.session_state.diario_investigador)}</div><div>Casos no diário</div></div>", unsafe_allow_html=True)

        if modulos_count:
            st.markdown("### 📊 Áreas onde você mais investigou")
            ranking = sorted(modulos_count.items(), key=lambda x: x[1], reverse=True)
            for i, (modulo, count) in enumerate(ranking[:8]):
                pct = round(count / total_casos * 100) if total_casos else 0
                st.markdown(f\"\"\"
                <div style="margin-bottom:10px;">
                    <div style="display:flex;justify-content:space-between;font-size:0.85em;font-weight:600;"><span>{i+1}. {modulo}</span><span>{count}x</span></div>
                    <div style="background:#E2E8F0;border-radius:999px;height:10px;overflow:hidden;"><div style="height:100%;border-radius:999px;background:#0F172A;width:{pct}%;"></div></div>
                </div>
                \"\"\", unsafe_allow_html=True)

        # ========================
        # ACADEMIA SHERLOCK
        # ========================

    with _tab_Academia:
        st.header("🎓 Academia Sherlock")
        st.markdown("30 aulas de aprofundamento real — observação, dedução e método investigativo aplicado.")

        aulas = [
            "Aula 1 — O Poder da Observação", "Aula 2 — A Arte da Dedução", "Aula 3 — Fato x Opinião x Evidência",
            "Aula 4 — Como Pensam os Grandes Investigadores", "Aula 5 — Psicologia do Comportamento",
            "Aula 6 — Como Fazer Perguntas Inteligentes", "Aula 7 — Montando o Quebra-Cabeça",
            "Aula 8 — Encontrando Padrões", "Aula 9 — Os Maiores Erros da Mente", "Aula 10 — Organização Profissional",
            "Aula 11 — Memória de Investigador", "Aula 12 — Atenção aos Pequenos Detalhes",
            "Aula 13 — Como Observar Fotografias", "Aula 14 — Investigação no Dia a Dia",
            "Aula 15 — Investigação Digital", "Aula 16 — Introdução à Ciência Forense",
            "Aula 17 — Grandes Casos da História", "Aula 18 — Desafios de Lógica", "Aula 19 — Caça aos Detalhes",
            "Aula 20 — Método Sherlock Holmes",
        ]
        aulas += [
            "Aula 21 — Linguagem Corporal e Microexpressões (com cautela)", "Aula 22 — Investigação de Ausências (o que NÃO está lá)",
            "Aula 23 — Raciocínio Probabilístico no Dia a Dia", "Aula 24 — Como Documentar uma Investigação",
            "Aula 25 — Entrevistas e Como Conduzir Conversas Investigativas", "Aula 26 — Cadeia de Custódia e Preservação de Evidências",
            "Aula 27 — Investigação Colaborativa (trabalhando em equipe)", "Aula 28 — Ética na Investigação",
            "Aula 29 — Quando Parar de Investigar", "Aula 30 — Construindo seu Próprio Método",
        ]

        col_aula, col_nivel = st.columns([3, 1])
        with col_aula:
            aula_escolhida = st.selectbox("Escolha a aula:", aulas, key="select_aula_academia")
        with col_nivel:
            profundidade_aula = st.selectbox("Profundidade:", ["Padrão", "Aprofundada"], key="select_profundidade_aula")

        if st.button("🎓 INICIAR AULA", key="sherlock59"):
            with st.spinner("Preparando uma aula de verdade, com profundidade..."):
                nivel_instrucao = (
                    "Esta deve ser uma aula EXTENSA e densa, no nível de um curso universitário de elite ou de um seminário "
                    "avançado de investigação — não um resumo de blog."
                    if profundidade_aula == "Aprofundada" else
                    "Esta deve ser uma aula completa e rica, mas objetiva."
                )
                prompt = (
                    f"Você está escrevendo uma aula para a Academia Sherlock — um curso de altíssimo nível sobre raciocínio "
                    f"investigativo, no espírito do método de observação e dedução de Sherlock Holmes, mas aplicado a contextos "
                    f"reais e modernos. {nivel_instrucao}\\n\\n"
                    f"Tema da aula: {aula_escolhida}\\n\\n"
                    f"EXIGÊNCIAS DE QUALIDADE — leia com atenção antes de escrever:\\n"
                    f"- PROIBIDO ser superficial, genérico ou usar frases de efeito vazias. Cada afirmação deve ser sustentada "
                    f"por um exemplo concreto, um mecanismo explicado, ou um caso ilustrativo.\\n"
                    f"- Use pelo menos 2 exemplos NARRADOS EM DETALHE (não apenas citados de passagem) — podem ser cenários "
                    f"fictícios elaborados, casos históricos genéricos (sem inventar fatos verificáveis específicos que você não "
                    f"tenha certeza), ou situações do cotidiano levadas a um nível de análise que a maioria das pessoas não faz.\\n"
                    f"- Demonstre o RACIOCÍNIO PASSO A PASSO, não apenas a conclusão. Mostre o 'como se pensa', não só o 'o que pensar'.\\n"
                    f"- Inclua nuances, contra-exemplos e limites do método ensinado — uma aula de elite reconhece onde a técnica falha.\\n"
                    f"- O exercício final deve ser desafiador, específico e ter um gabarito comentado explicando o raciocínio "
                    f"correto, não apenas a resposta.\\n\\n"
                    f"FORMATO OBRIGATÓRIO:\\n\\n"
                    f"🎓 {aula_escolhida.upper()}\\n\\n"
                    f"📖 ABERTURA — POR QUE ISSO IMPORTA:\\n"
                    f"[3-5 linhas que conectem o tema a uma situação real e mostrem por que dominar isso muda a qualidade do "
                    f"raciocínio de quem está aprendendo. Evite frases motivacionais genéricas — seja específico sobre a vantagem prática.]\\n\\n"
                    f"💡 OS CONCEITOS FUNDAMENTAIS:\\n"
                    f"[3-5 conceitos centrais, cada um com: definição precisa, por que costuma ser mal compreendido ou ignorado, "
                    f"e um exemplo curto que fixe a ideia]\\n\\n"
                    f"🔍 ESTUDO DE CASO 1 — NARRATIVA COMPLETA:\\n"
                    f"[Narre uma situação (fictícia ou genérica, bem construída) onde o conceito da aula é aplicado do início ao fim. "
                    f"Mostre as observações feitas, o raciocínio encadeado, e a conclusão. Pelo menos 8-10 linhas de narrativa real, "
                    f"não um resumo de 2 linhas.]\\n\\n"
                    f"🔍 ESTUDO DE CASO 2 — UM ÂNGULO DIFERENTE:\\n"
                    f"[Um segundo exemplo que mostre uma faceta diferente do mesmo conceito — outro contexto, outra complexidade, "
                    f"ou um caso em que a aplicação ingênua do método levaria a erro, e como corrigir isso]\\n\\n"
                    f"⚙️ O MÉTODO PASSO A PASSO:\\n"
                    f"[Decomponha a técnica em etapas concretas e replicáveis — numeradas, específicas, sem vagueza. "
                    f"Esta é a parte 'manual de instruções' da aula]\\n\\n"
                    f"⚠️ ARMADILHAS E LIMITES DO MÉTODO:\\n"
                    f"[Onde essa técnica costuma ser usada mal, que erros ela não resolve, e quando confiar demais nela é perigoso. "
                    f"Uma aula de elite é honesta sobre os limites do que está ensinando]\\n\\n"
                    f"🧠 CONEXÃO COM OUTRAS AULAS/CONCEITOS:\\n"
                    f"[Como esse tema se conecta com outros princípios investigativos — mostre que o conhecimento é uma rede, não peças isoladas]\\n\\n"
                    f"🏋️ EXERCÍCIO PRÁTICO DESAFIADOR:\\n"
                    f"[Um exercício elaborado e específico — um mini-caso, um cenário com dados reais para analisar, ou um "
                    f"desafio de observação. Deve exigir aplicação real do conceito, não só recordação]\\n\\n"
                    f"✅ GABARITO COMENTADO:\\n"
                    f"[A resposta esperada do exercício, COM o raciocínio explicado passo a passo — não apenas 'a resposta é X', "
                    f"mas 'a resposta é X porque, ao observar Y, deduzimos Z, e isso elimina a hipótese W']\\n\\n"
                    f"📚 SÍNTESE MAGISTRAL:\\n"
                    f"[2-4 linhas que cristalizem a essência da aula em uma ideia memorável e aplicável — a frase que o aluno "
                    f"deveria lembrar meses depois]"
                )
                res = sherlock_ia(prompt, "Você está escrevendo a melhor aula possível sobre este tema. Imagine que está escrevendo para uma pessoa inteligente e exigente que vai notar e se decepcionar com qualquer superficialidade, clichê vazio, ou exemplo fraco. Densidade e precisão acima de tudo — mas sem perder a clareza didática.")
                if res: st.session_state['res_academia_sherlo7'] = str(res)
                salvar_caso("Academia", aula_escolhida, res)
                st.session_state['aula_temp'] = res

        if st.session_state.get('aula_temp'):
            try:
                st.markdown(f"<div class='card'>{st.session_state['aula_temp']}</div>", unsafe_allow_html=True)
            except:
                st.markdown(st.session_state['aula_temp'])
            st.download_button("📋 Baixar aula (.txt)", data=st.session_state['aula_temp'], file_name="aula_academia.txt", mime="text/plain", key="sherlock60")

        # ========================
        # DESAFIO SHERLOCK
        # ========================

    with _tab_Desafio:
        st.header("🏆 Desafio Sherlock")
        nivel_atual = st.session_state.desafio_nivel_atual
        st.markdown(f"Pontuação: **{st.session_state.desafio_pontuacao} pontos** | Nível atual: <span class='{CLASSES_NIVEL.get(nivel_atual)}'>{nivel_atual}</span>", unsafe_allow_html=True)

        nivel_desafio = st.selectbox("Escolha o nível do desafio:", NIVEIS_DESAFIO, key="select_nivel_desafio")

        if st.button("🏆 GERAR DESAFIO", key="sherlock61"):
            with st.spinner("Criando o desafio..."):
                prompt = (
                    f"Crie um mini-desafio de lógica/investigação no nível: {nivel_desafio}\\n\\n"
                    f"FORMATO:\\n\\n"
                    f"🏆 DESAFIO {nivel_desafio.upper()}\\n\\n"
                    f"📖 SITUAÇÃO:\\n[um mini-mistério ou quebra-cabeça lógico, complexidade adequada ao nível]\\n\\n"
                    f"❓ O QUE VOCÊ PRECISA DESCOBRIR:\\n[a pergunta do desafio]\\n\\n"
                    f"💡 DICA (opcional, oculta até pedir):\\n[uma dica que ajuda sem entregar a resposta]\\n\\n"
                    f"✅ RESPOSTA: [a solução, mas marque claramente como RESPOSTA para o app esconder até o usuário clicar]"
                )
                res = sherlock_ia(prompt)
                if res: st.session_state['res_desafio_sherlo8'] = str(res)
                st.session_state['desafio_temp'] = res
                st.session_state['desafio_revelado'] = False
                st.session_state['desafio_nivel_jogado'] = nivel_desafio

        if st.session_state.get('desafio_temp'):
            partes_desafio = st.session_state['desafio_temp'].split('✅ RESPOSTA')
            st.markdown(f"<div class='dossie-box'>{partes_desafio[0]}</div>", unsafe_allow_html=True)

            if not st.session_state.get('desafio_revelado'):
                if st.button("👁️ VER RESPOSTA", key="sherlock62"):
                    st.session_state['desafio_revelado'] = True
                    st.rerun()
            else:
                st.markdown(f"<div class='card-gold'>✅ RESPOSTA{partes_desafio[1] if len(partes_desafio)>1 else ''}</div>", unsafe_allow_html=True)
                col_acertei, col_errei = st.columns(2)
                with col_acertei:
                    if st.button("✅ Acertei!", key="sherlock63"):
                        pontos = {"Iniciante":5,"Investigador":10,"Inspetor":15,"Mestre":20,"Sherlock":30}
                        nivel_jogado = st.session_state.get('desafio_nivel_jogado', nivel_desafio)
                        st.session_state.desafio_pontuacao += pontos.get(nivel_jogado, 10)
                        st.session_state.desafio_nivel_atual = nivel_jogado
                        st.session_state.casos_resolvidos_count += 1
                        st.success(f"🎉 +{pontos.get(nivel_jogado,10)} pontos!")
                with col_errei:
                    if st.button("❌ Errei", key="sherlock64"):
                        st.info("Sem problema, a prática leva à perfeição. Próximo desafio!")

        # ========================
        # SHERLOCK 24 HORAS
        # ========================

    with _tab_Sherlock24:
        st.header("🤖 Sherlock 24 Horas")
        st.markdown("Converse livremente sobre qualquer investigação.")

        if 'chat_sherlock' not in st.session_state:
            st.session_state.chat_sherlock = []
        if 'sherlock_key' not in st.session_state:
            st.session_state.sherlock_key = 0

        if st.session_state.chat_sherlock:
            for msg in st.session_state.chat_sherlock:
                if msg['role'] == 'user':
                    st.markdown(f"<div style='background:#F1F5F9;border:1px solid #334155;border-radius:12px 12px 4px 12px;padding:12px 16px;margin:8px 0;'><b>Você:</b> {msg['content']}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='card-dark' style='margin:8px 0;'><b>🕵️ Sherlock:</b><br>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(\"\"\"<div style="background:#F1F5F9;border:1px dashed #334155;border-radius:12px;padding:16px;text-align:center;">
            🤖 <strong>Pergunte qualquer coisa!</strong> Ex: "Como eu organizaria uma investigação sobre X?",
            "Quais perguntas eu deveria fazer nessa situação?"
            </div>\"\"\", unsafe_allow_html=True)

        pergunta_sherlock = st.text_input("Sua pergunta:", key=f"sherlock_input_{st.session_state.sherlock_key}", placeholder="Pergunte qualquer coisa sobre investigação...")

        col_env, col_limpar = st.columns([3, 1])
        with col_env:
            if st.button("📤 PERGUNTAR", key="sherlock65"):
                if pergunta_sherlock.strip():
                    with st.spinner("Investigando..."):
                        resp = sherlock_ia(pergunta_sherlock, "Responda como um detetive consultor experiente, lógico e didático.")
                        if resp: st.session_state['res_sherlock24_sherlo9'] = str(resp)
                    st.session_state.chat_sherlock.append({"role": "user", "content": pergunta_sherlock})
                    st.session_state.chat_sherlock.append({"role": "assistant", "content": resp})
                    st.session_state.sherlock_key += 1
                    salvar_caso("Sherlock24", pergunta_sherlock[:60], resp)
                    st.rerun()
                else:
                    st.warning("Digite sua pergunta.")
        with col_limpar:
            if st.button("🗑️ Limpar", key="sherlock66"):
                st.session_state.chat_sherlock = []
                st.rerun()

        # ========================
        # SALA DE CASOS IMPOSSÍVEIS
        # ========================

    with _tab_CasosImpossiveis:
        st.header("💎 Sala de Casos Impossíveis")
        st.markdown("Mistérios complexos que se revelam por etapas. A IA é sua mentora — não entrega a resposta.")

        if 'dossie_etapa' not in st.session_state:
            st.session_state.dossie_etapa = 0

        if st.session_state.dossie_etapa == 0:
            dificuldade_dossie = st.selectbox("Nível de complexidade:", ["Inspetor","Mestre","Sherlock"], key="sherlock67")
            if st.button("💎 ABRIR NOVO DOSSIÊ", key="sherlock68"):
                with st.spinner("Montando o dossiê..."):
                    prompt = (
                        f"Crie um caso investigativo complexo e envolvente, nível {dificuldade_dossie}, "
                        f"para ser revelado em etapas (dossiê).\\n\\n"
                        f"FORMATO:\\n\\n"
                        f"💎 DOSSIÊ: [NOME DRAMÁTICO DO CASO]\\n"
                        f"Nível: {dificuldade_dossie}\\n\\n"
                        f"📖 CONTEXTO INICIAL:\\n[a situação inicial, intrigante]\\n\\n"
                        f"📸 ELEMENTOS DISPONÍVEIS NESTA ETAPA:\\n[2-3 evidências/depoimentos iniciais]\\n\\n"
                        f"❓ SUA MISSÃO:\\n[o que o investigador precisa descobrir]\\n\\n"
                        f"[NÃO REVELE MAIS NADA AINDA — isso é só a primeira etapa do dossiê]"
                    )
                    res = sherlock_ia(prompt)
                    if res: st.session_state['res_casosimpossi_sherlo10'] = str(res)
                    st.session_state['dossie_conteudo'] = [res]
                    st.session_state['dossie_dificuldade'] = dificuldade_dossie
                    st.session_state.dossie_etapa = 1
                    st.rerun()
        else:
            for i, parte in enumerate(st.session_state.get('dossie_conteudo', [])):
                st.markdown(f"<div class='dossie-box'>{parte}</div>", unsafe_allow_html=True)

            st.markdown("#### 🧩 Sua análise / próxima pergunta para a mentora:")
            analise_dossie = st.text_area("Escreva sua hipótese atual ou pergunta:", height=100, key="input_analise_dossie")

            col_continuar, col_revelar = st.columns(2)
            with col_continuar:
                if st.button("➡️ DESBLOQUEAR PRÓXIMO ELEMENTO", key="sherlock69"):
                    if analise_dossie.strip():
                        with st.spinner("A mentora está analisando..."):
                            historico_dossie = "\\n\\n".join(st.session_state['dossie_conteudo'])
                            prompt = (
                                f"Você é a mentora de um caso investigativo em andamento (dossiê nível {st.session_state.get('dossie_dificuldade','Inspetor')}).\\n"
                                f"Conteúdo já revelado:\\n{historico_dossie}\\n\\n"
                                f"O investigador (usuário) disse: {analise_dossie}\\n\\n"
                                f"Responda como mentora: faça uma pergunta estratégica sobre o raciocínio dele, aponte SUTILMENTE "
                                f"se algo parece incompleto (sem entregar a resposta), e então revele UM novo elemento do dossiê "
                                f"(uma nova evidência, depoimento ou pista) que avança a investigação.\\n\\n"
                                f"FORMATO:\\n\\n"
                                f"🕵️ COMENTÁRIO DA MENTORA:\\n[reação ao raciocínio do investigador — perguntas estratégicas, sem entregar a resposta]\\n\\n"
                                f"📂 NOVO ELEMENTO DESBLOQUEADO:\\n[uma nova peça do dossiê — evidência, depoimento, documento]"
                            )
                            res = sherlock_ia(prompt)
                            if res: st.session_state['res_casosimpossi_sherlo11'] = str(res)
                            st.session_state['dossie_conteudo'].append(res)
                            st.rerun()
                    else:
                        st.warning("Escreva sua hipótese ou pergunta antes de avançar.")
            with col_revelar:
                if st.button("🔓 REVELAR SOLUÇÃO COMPLETA", key="sherlock70"):
                    with st.spinner("Revelando a lógica completa..."):
                        historico_dossie = "\\n\\n".join(st.session_state['dossie_conteudo'])
                        prompt = (
                            f"Revele a solução completa deste caso investigativo, explicando toda a lógica.\\n"
                            f"Conteúdo do dossiê até agora:\\n{historico_dossie}\\n\\n"
                            f"FORMATO:\\n\\n"
                            f"🔓 SOLUÇÃO COMPLETA DO CASO\\n\\n"
                            f"✅ O QUE REALMENTE ACONTECEU:\\n[a solução completa]\\n\\n"
                            f"🧩 LÓGICA UTILIZADA:\\n[como cada pista levava à solução, passo a passo]\\n\\n"
                            f"🎯 A PISTA MAIS DECISIVA:\\n[qual elemento foi crucial]\\n\\n"
                            f"🏆 PARABÉNS POR INVESTIGAR ATÉ O FIM!"
                        )
                        res_final = sherlock_ia(prompt)
                        if res_final: st.session_state['res_casosimpossi_sherlo12'] = str(res_final)
                        st.session_state['dossie_solucao'] = res_final
                        st.session_state.casos_resolvidos_count += 1
                        st.rerun()

            if st.session_state.get('dossie_solucao'):
                st.markdown(f"<div class='card-gold'>{st.session_state['dossie_solucao']}</div>", unsafe_allow_html=True)
                if st.button("🔄 Abrir novo dossiê", key="sherlock71"):
                    for k in ['dossie_etapa','dossie_conteudo','dossie_dificuldade','dossie_solucao']:
                        st.session_state.pop(k, None)
                    st.rerun()

        # ========================
        # BIBLIOTECA
        # ========================

    with _tab_Biblioteca:
        st.header("📚 Biblioteca de Casos")

        if not st.session_state.casos_salvos:
            st.info("Biblioteca vazia. Gere análises nos módulos e salve as importantes aqui!")
        else:
            modulos_bib = list(set(c['modulo'] for c in st.session_state.casos_salvos))
            filtro = st.selectbox("Filtrar por módulo:", ["Todos"] + modulos_bib, key="select_filtro_bib")
            consultas_f = [c for c in st.session_state.casos_salvos if filtro == "Todos" or c['modulo'] == filtro]

            st.markdown(f"**{len(consultas_f)} análise(s) encontrada(s)**")
            for i, item in enumerate(reversed(consultas_f)):
                idx_real = len(st.session_state.casos_salvos) - 1 - i
                with st.expander(f"[{item.get('modulo', '')}] {item.get('tema', '')[:60]} — {item['data']}"):
                    st.markdown(f"<div class='card'>{item['conteudo']}</div>", unsafe_allow_html=True)
                    col_dl, col_del = st.columns([3, 1])
                    with col_dl:
                        st.download_button("📋 Baixar", data=item['conteudo'], file_name=f"{item.get('modulo', '').lower()}.txt", mime="text/plain", key=f"dl_bib_{i}")
                    with col_del:
                        if st.button("🗑️ Remover", key=f"del_bib_{i}"):
                            st.session_state.casos_salvos.pop(idx_real)
                            st.rerun()

        if st.session_state.historico_casos:
            st.markdown("<hr class='divider'>", unsafe_allow_html=True)
            historico_txt = "\\n\\n".join(f"[{c['data']}] {c['modulo']} — {c['tema']}\\n{c['conteudo']}\\n{'─'*40}" for c in st.session_state.historico_casos)
            st.download_button("⬇️ Exportar todo o histórico (.txt)", data=historico_txt, file_name="historico_sherlock.txt", mime="text/plain", key="sherlock72")
            if st.button("🗑️ Limpar Todo o Histórico", key="sherlock73"):
                st.session_state.historico_casos = []
                st.rerun()

        # --- RODAPÉ ---
        st.markdown(
        "<div style='text-align:center;color:#999;font-size:0.8em;margin-top:60px;'>"
        "© 2026 Sherlock IA — Consultor de Investigação Lógica com IA · MeusAgentesIA.com.br"
        "</div>", unsafe_allow_html=True
        )


        # --- RODAPÉ ---
        st.markdown(
        "<div style='text-align:center;color:#999;font-size:0.8em;margin-top:60px;'>"
        "</div>", unsafe_allow_html=True
        )

    with _tab_Forense:
        st.header("🧪 Laboratório Forense (Educativo)")
        st.markdown(DISCLAIMER_FORENSE, unsafe_allow_html=True)

        tema_forense = st.selectbox("Tema:", [
            "Impressões digitais", "DNA forense", "Análise de pegadas", "Vestígios e indícios",
            "Cadeia de custódia", "Balística", "Documentoscopia", "Perícia digital",
        ], key="sherlock1_d2")

        if st.button("🧪 APRENDER", key="sherlock44"):
            with st.spinner("Preparando conteúdo..."):
                prompt = (
                    f"Explique de forma educativa: {tema_forense}\\n\\n"
                    f"FORMATO:\\n\\n"
                    f"🧪 {tema_forense.upper()}\\n\\n"
                    f"📖 O QUE É E COMO FUNCIONA:\\n[explicação científica acessível]\\n\\n"
                    f"🔬 PRINCÍPIOS CIENTÍFICOS ENVOLVIDOS:\\n[a base científica/lógica do método]\\n\\n"
                    f"📋 COMO É USADO EM INVESTIGAÇÕES REAIS:\\n[contexto de uso pela perícia oficial]\\n\\n"
                    f"💡 CURIOSIDADE HISTÓRICA:\\n[1 fato interessante sobre a evolução dessa técnica]"
                )
                res = sherlock_ia(prompt, "Mantenha o conteúdo estritamente educativo e conceitual — nunca forneça instruções de como evitar ou burlar essa técnica forense.")
                if res: st.session_state['res_forense_sherlo13'] = str(res)
                salvar_caso("Forense", tema_forense, res)
                st.session_state['for_temp'] = res

        if st.session_state.get('for_temp'):
            st.markdown(f"<div class='card-blue'>{st.session_state['for_temp']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar (.txt)", data=st.session_state['for_temp'], file_name="forense.txt", mime="text/plain", key="sherlock45")

        # ========================
        # CASOS HISTÓRICOS
        # ========================

    with _tab_Casos:
        st.header("📚 Casos Históricos")

        caso_hist = st.text_input("🔍 Caso de interesse (ou deixe vazio para sugestão):", placeholder="ex: um caso famoso de fraude, um mistério clássico resolvido por perícia...", key="sherlock46")

        if st.button("📚 EXPLORAR CASO", key="sherlock47"):
            with st.spinner("Buscando o caso..."):
                topico_caso = caso_hist if caso_hist.strip() else "um caso histórico famoso de investigação bem documentado"
                prompt = (
                    f"Apresente um caso investigativo histórico relevante relacionado a: {topico_caso}\\n\\n"
                    f"FORMATO:\\n\\n"
                    f"📚 CASO: [NOME DO CASO]\\n\\n"
                    f"📖 CONTEXTO:\\n[o que aconteceu]\\n\\n"
                    f"🔍 COMO FOI INVESTIGADO:\\n[método usado pelos investigadores]\\n\\n"
                    f"🎯 EVIDÊNCIAS DECISIVAS:\\n[o que resolveu o caso]\\n\\n"
                    f"⚠️ ERROS COMETIDOS NA INVESTIGAÇÃO:\\n[se houver, o que poderia ter sido feito melhor]\\n\\n"
                    f"💡 LIÇÃO PARA INVESTIGADORES:\\n[o que esse caso ensina]\\n\\n"
                    f"⚠️ NOTA: se não tiver certeza de detalhes específicos e verificáveis sobre um caso real, "
                    f"diga isso claramente em vez de inventar fatos."
                )
                res = sherlock_ia(prompt)
                if res: st.session_state['res_casos_sherlo14'] = str(res)
                salvar_caso("Casos", topico_caso, res)
                st.session_state['caso_hist_temp'] = res

        if st.session_state.get('caso_hist_temp'):
            st.markdown(f"<div class='card-dark'>{st.session_state['caso_hist_temp']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar (.txt)", data=st.session_state['caso_hist_temp'], file_name="caso_historico.txt", mime="text/plain", key="sherlock48")

        # ========================
        # SIMULADOR DE INVESTIGAÇÃO
        # ========================

    with _tab_Ferramentas:
        st.header("🛠️ Ferramentas Avançadas")
        st.markdown("*Ferramentas especializadas de investigação criminal e análise.*")
        (_sContradicoes, _sPerfil, _sConversas, _sImagens, _sDomestica, _sDigital, _sFraudes, _sPadroes, _sProbabilidades, _sPerguntas, _sCritico, _sMetodo) = st.tabs(['❌ Contradições', '👤 Perfil', '💬 Conversas', '🖼️ Imagens', '🏠 Crimes Dom.', '💻 Crimes Digitais', '💸 Fraudes', '🔗 Padrões', '📊 Probabilidades', '❓ Perguntas', '🧠 Pens. Crítico', '🔬 Método'])

        with _sContradicoes:
            st.header("🎭 Detector de Contradições")
            st.markdown("Cole relatos, mensagens ou depoimentos para identificar inconsistências.")

            relatos_contra = st.text_area("📝 Cole os relatos/depoimentos (identifique quem disse o quê):", height=200,
                placeholder="ex: Pessoa A disse: 'Eu não estava lá às 14h'. Mais tarde, Pessoa A disse: 'Cheguei por volta de 14h e já tinha gente lá'...", key="sherlock12_d2")

            if st.button("🎭 DETECTAR CONTRADIÇÕES", key="sherlock16_d2"):
                if relatos_contra.strip():
                    with st.spinner("Analisando..."):
                        prompt = (
                            f"Analise estes relatos identificando contradições e inconsistências.\\n"
                            f"Relatos: {relatos_contra}\\n\\n"
                            f"FORMATO:\\n\\n"
                            f"🎭 ANÁLISE DE CONTRADIÇÕES\\n\\n"
                            f"🔄 MUDANÇAS DE VERSÃO:\\n[onde a mesma pessoa disse coisas diferentes]\\n\\n"
                            f"⚠️ CONTRADIÇÕES ENTRE RELATOS:\\n[onde diferentes pessoas se contradizem]\\n\\n"
                            f"❓ INFORMAÇÕES CONFLITANTES:\\n[dados que não se encaixam]\\n\\n"
                            f"❓ PERGUNTAS AINDA NÃO RESPONDIDAS:\\n[o que precisa ser esclarecido]\\n\\n"
                            f"🎯 CONTRADIÇÃO MAIS SIGNIFICATIVA:\\n[qual merece mais atenção, e por quê]"
                        )
                        res = sherlock_ia(prompt)
                        if res: st.session_state['res_scontradicoe_sherlo15'] = str(res)
                        salvar_caso("Contradicoes", relatos_contra[:60], res)
                        st.session_state['contra_temp'] = res
                else:
                    st.warning("Cole os relatos.")

            if st.session_state.get('contra_temp'):
                st.markdown(f"<div class='card-red'>{st.session_state['contra_temp']}</div>", unsafe_allow_html=True)
                st.markdown(DISCLAIMER_PADRAO, unsafe_allow_html=True)
                st.download_button("📋 Baixar (.txt)", data=st.session_state['contra_temp'], file_name="contradicoes.txt", mime="text/plain", key="sherlock17")

            # ========================
            # PERFIL COMPORTAMENTAL
            # ========================

        with _sPerfil:
            st.header("👤 Perfil Comportamental")
            st.markdown(DISCLAIMER_COMPORTAMENTAL, unsafe_allow_html=True)

            comportamento_perfil = st.text_area("📝 Descreva os comportamentos observados:", height=150,
                placeholder="ex: A pessoa começou a chegar mais tarde no trabalho, ficou mais quieta nas reuniões, e parou de almoçar com a equipe...", key="sherlock11_d2")

            if st.button("👤 ANALISAR PADRÕES", key="sherlock18"):
                if comportamento_perfil.strip():
                    with st.spinner("Analisando padrões..."):
                        prompt = (
                            f"Analise estes comportamentos descritos, gerando hipóteses (nunca diagnósticos).\\n"
                            f"Comportamentos: {comportamento_perfil}\\n\\n"
                            f"FORMATO:\\n\\n"
                            f"👤 ANÁLISE DE PADRÕES COMPORTAMENTAIS\\n\\n"
                            f"🔄 MUDANÇAS IDENTIFICADAS:\\n[o que mudou, com base no relato]\\n\\n"
                            f"💭 POSSÍVEIS MOTIVAÇÕES (hipóteses, não certezas):\\n[3-4 explicações possíveis, incluindo motivos benignos e neutros]\\n\\n"
                            f"📊 PADRÕES E HÁBITOS:\\n[o que parece ser recorrente]\\n\\n"
                            f"❤️ FATORES EMOCIONAIS POSSÍVEIS:\\n[hipóteses sobre estado emocional, com cautela]\\n\\n"
                            f"❓ O QUE AINDA NÃO SE SABE:\\n[informação que falta para entender melhor]\\n\\n"
                            f"💬 SUGESTÃO:\\n[1 frase recomendando, quando aplicável, conversar diretamente com a pessoa em vez de apenas inferir]"
                        )
                        res = sherlock_ia(prompt, "Gere hipóteses variadas, incluindo explicações neutras e benignas — não foque só em explicações negativas ou suspeitas.")
                        if res: st.session_state['res_sperfil_sherlo16'] = str(res)
                        salvar_caso("Perfil", comportamento_perfil[:60], res)
                        st.session_state['perfil_temp'] = res
                else:
                    st.warning("Descreva os comportamentos.")

            if st.session_state.get('perfil_temp'):
                st.markdown(f"<div class='card-purple'>{st.session_state['perfil_temp']}</div>", unsafe_allow_html=True)
                st.download_button("📋 Baixar (.txt)", data=st.session_state['perfil_temp'], file_name="perfil_comportamental.txt", mime="text/plain", key="sherlock19")

            # ========================
            # ANÁLISE DE CONVERSAS
            # ========================

        with _sConversas:
            st.header("💬 Análise de Conversas")
            st.markdown(DISCLAIMER_COMPORTAMENTAL, unsafe_allow_html=True)

            conversa_analise = st.text_area("📝 Cole a conversa que você quer analisar:", height=200,
                placeholder="Cole aqui a conversa, identificando quem disse cada parte...", key="sherlock10_d2")

            if st.button("💬 ANALISAR CONVERSA", key="sherlock20"):
                if conversa_analise.strip():
                    with st.spinner("Analisando..."):
                        prompt = (
                            f"Analise esta conversa.\\n"
                            f"Conversa: {conversa_analise}\\n\\n"
                            f"FORMATO:\\n\\n"
                            f"💬 ANÁLISE DA CONVERSA\\n\\n"
                            f"🎭 MUDANÇAS DE TOM:\\n[onde o tom muda e o que isso pode sugerir]\\n\\n"
                            f"⚠️ POSSÍVEIS CONTRADIÇÕES:\\n[inconsistências no que foi dito]\\n\\n"
                            f"🙈 ASSUNTOS EVITADOS:\\n[temas que parecem ser desviados ou evitados]\\n\\n"
                            f"🔄 COMUNICAÇÃO INDIRETA:\\n[onde algo parece estar sendo dito sem ser dito diretamente]\\n\\n"
                            f"❓ PERGUNTAS SEM RESPOSTA:\\n[o que foi perguntado mas não respondido claramente]\\n\\n"
                            f"✅ COERÊNCIA GERAL: [Alta/Média/Baixa]\\n[avaliação geral de quão consistente é a conversa]"
                        )
                        res = sherlock_ia(prompt)
                        if res: st.session_state['res_sconversas_sherlo17'] = str(res)
                        salvar_caso("Conversas", conversa_analise[:60], res)
                        st.session_state['conv_temp'] = res
                else:
                    st.warning("Cole a conversa.")

            if st.session_state.get('conv_temp'):
                st.markdown(f"<div class='card-purple'>{st.session_state['conv_temp']}</div>", unsafe_allow_html=True)
                st.download_button("📋 Baixar (.txt)", data=st.session_state['conv_temp'], file_name="analise_conversa.txt", mime="text/plain", key="sherlock21")

            # ========================
            # ANÁLISE DE IMAGENS (DESCRITIVA)
            # ========================

        with _sImagens:
            st.header("📸 Análise de Imagens")
            st.info("📝 Este app trabalha por descrição em texto — descreva a cena com o máximo de detalhes possível.")

            descricao_imagem = st.text_area("📝 Descreva detalhadamente o que você vê na imagem/cena:", height=180,
                placeholder="ex: Sala com a janela aberta, uma cadeira fora do lugar normal, papéis no chão perto da mesa, luz apagada...", key="sherlock9_d2")

            if st.button("📸 ANALISAR DESCRIÇÃO", key="sherlock22"):
                if descricao_imagem.strip():
                    with st.spinner("Analisando os detalhes..."):
                        prompt = (
                            f"Analise esta descrição de cena/imagem com olhar investigativo.\\n"
                            f"Descrição: {descricao_imagem}\\n\\n"
                            f"FORMATO:\\n\\n"
                            f"📸 ANÁLISE DA CENA DESCRITA\\n\\n"
                            f"🔍 OBJETOS RELEVANTES:\\n[itens mencionados que podem ter importância]\\n\\n"
                            f"🏠 AMBIENTE E ORGANIZAÇÃO:\\n[o que o estado do ambiente sugere]\\n\\n"
                            f"👣 POSSÍVEIS VESTÍGIOS:\\n[sinais que indicam o que pode ter acontecido]\\n\\n"
                            f"⚠️ ELEMENTOS QUE CHAMAM ATENÇÃO:\\n[o que parece fora do normal ou inconsistente]\\n\\n"
                            f"👀 DETALHES QUE PODEM TER SIDO IGNORADOS:\\n[perguntas sobre o que mais observar]\\n\\n"
                            f"🧩 O QUE ESSA CENA PODE SUGERIR:\\n[hipóteses, sempre como possibilidades]"
                        )
                        res = sherlock_ia(prompt)
                        if res: st.session_state['res_simagens_sherlo18'] = str(res)
                        salvar_caso("Imagens", descricao_imagem[:60], res)
                        st.session_state['img_temp'] = res
                else:
                    st.warning("Descreva a cena.")

            if st.session_state.get('img_temp'):
                st.markdown(f"<div class='card'>{st.session_state['img_temp']}</div>", unsafe_allow_html=True)
                st.markdown(DISCLAIMER_PADRAO, unsafe_allow_html=True)
                st.download_button("📋 Baixar (.txt)", data=st.session_state['img_temp'], file_name="analise_imagem.txt", mime="text/plain", key="sherlock23")

            # ========================
            # INVESTIGAÇÃO DOMÉSTICA
            # ========================

        with _sDomestica:
            st.header("🏠 Investigação Doméstica")

            tipo_dom = st.selectbox("Tipo de problema:", ["Vazamento de água","Ruído estranho","Cheiro incomum","Infiltração","Defeito elétrico","Outro"], key="sherlock24")
            descricao_dom = st.text_area("📝 Descreva o problema com detalhes:", height=150,
                placeholder="ex: Aparece uma mancha de umidade no canto do teto da sala, principalmente depois de chover...", key="sherlock8_d2")

            if st.button("🏠 INVESTIGAR PROBLEMA", key="sherlock25"):
                if descricao_dom.strip():
                    with st.spinner("Investigando..."):
                        prompt = (
                            f"Investigue este problema doméstico.\\n"
                            f"Tipo: {tipo_dom}. Descrição: {descricao_dom}\\n\\n"
                            f"FORMATO:\\n\\n"
                            f"🏠 INVESTIGAÇÃO — {tipo_dom.upper()}\\n\\n"
                            f"🔍 POSSÍVEIS CAUSAS (da mais para a menos provável):\\n[liste com lógica]\\n\\n"
                            f"🧪 TESTES QUE VOCÊ PODE FAZER:\\n[ações simples para isolar a causa]\\n\\n"
                            f"⚠️ SINAIS DE URGÊNCIA:\\n[quando isso indica um problema que precisa de atenção rápida]\\n\\n"
                            f"🔧 QUANDO CHAMAR UM PROFISSIONAL:\\n[a partir de que ponto vale a pena]"
                        )
                        res = sherlock_ia(prompt)
                        if res: st.session_state['res_sdomestica_sherlo19'] = str(res)
                        salvar_caso("Domestica", f"{tipo_dom}: {descricao_dom[:40]}", res)
                        st.session_state['dom_temp'] = res
                else:
                    st.warning("Descreva o problema.")

            if st.session_state.get('dom_temp'):
                st.markdown(f"<div class='card-green'>{st.session_state['dom_temp']}</div>", unsafe_allow_html=True)
                st.download_button("📋 Baixar (.txt)", data=st.session_state['dom_temp'], file_name="investigacao_domestica.txt", mime="text/plain", key="sherlock26")

            # ========================
            # INVESTIGAÇÃO DIGITAL
            # ========================

        with _sDigital:
            st.header("💻 Investigação Digital")

            tipo_dig = st.selectbox("O que você quer investigar:", ["Site suspeito","Mensagem/e-mail estranho","Perfil possivelmente falso","Link suspeito","Possível engenharia social","Outro"], key="sherlock27")
            descricao_dig = st.text_area("📝 Descreva o que você está vendo:", height=150,
                placeholder="ex: Recebi uma mensagem dizendo que ganhei um prêmio e pedindo para clicar em um link...", key="sherlock7_d2")

            if st.button("💻 ANALISAR", key="sherlock28"):
                if descricao_dig.strip():
                    with st.spinner("Analisando..."):
                        prompt = (
                            f"Analise esta situação digital suspeita.\\n"
                            f"Tipo: {tipo_dig}. Descrição: {descricao_dig}\\n\\n"
                            f"FORMATO:\\n\\n"
                            f"💻 ANÁLISE DIGITAL — {tipo_dig.upper()}\\n\\n"
                            f"🚩 SINAIS DE ALERTA IDENTIFICADOS:\\n[com base na descrição]\\n\\n"
                            f"🎭 TÉCNICA PROVÁVEL UTILIZADA:\\n[se for um golpe, qual técnica é essa]\\n\\n"
                            f"📊 NÍVEL DE SUSPEITA: [Baixo/Médio/Alto]\\n[justificativa]\\n\\n"
                            f"🛡️ O QUE FAZER:\\n[ações recomendadas — não clicar, verificar, bloquear, etc]\\n\\n"
                            f"📚 COMO RECONHECER ISSO NO FUTURO:\\n[padrão geral para identificar esse tipo de ameaça]"
                        )
                        res = sherlock_ia(prompt)
                        if res: st.session_state['res_sdigital_sherlo20'] = str(res)
                        salvar_caso("Digital", f"{tipo_dig}: {descricao_dig[:40]}", res)
                        st.session_state['dig_temp'] = res
                else:
                    st.warning("Descreva a situação.")

            if st.session_state.get('dig_temp'):
                st.markdown(f"<div class='card-red'>{st.session_state['dig_temp']}</div>", unsafe_allow_html=True)
                st.download_button("📋 Baixar (.txt)", data=st.session_state['dig_temp'], file_name="investigacao_digital.txt", mime="text/plain", key="sherlock29")

            # ========================
            # FRAUDES E GOLPES
            # ========================

        with _sFraudes:
            st.header("💰 Fraudes e Golpes")

            golpe_select = st.selectbox("Golpe que você quer entender:", [
                "Golpe do Pix", "Golpe da falsa central bancária", "Golpe do falso boleto",
                "Golpe do amor (romance scam)", "Pirâmide financeira", "Golpe do falso emprego",
                "Investimento fraudulento", "Outro (descrever)",
            ], key="sherlock6_d2")
            descricao_golpe = ""
            if golpe_select == "Outro (descrever)":
                descricao_golpe = st.text_input("Descreva a situação:", key="sherlock30")

            if st.button("💰 ENTENDER ESSE GOLPE", key="sherlock31"):
                topico = descricao_golpe if golpe_select == "Outro (descrever)" and descricao_golpe.strip() else golpe_select
                if topico.strip():
                    with st.spinner("Preparando explicação..."):
                        prompt = (
                            f"Explique detalhadamente: {topico}\\n\\n"
                            f"FORMATO:\\n\\n"
                            f"💰 {topico.upper()}\\n\\n"
                            f"🎭 COMO FUNCIONA:\\n[passo a passo de como os criminosos aplicam isso]\\n\\n"
                            f"🚩 SINAIS DE ALERTA:\\n[como reconhecer]\\n\\n"
                            f"🛡️ COMO SE PROTEGER:\\n[ações preventivas]\\n\\n"
                            f"⚡ COMO AGIR SE JÁ CAIU NESSE GOLPE:\\n[passos imediatos]\\n\\n"
                            f"📂 INFORMAÇÕES IMPORTANTES A REUNIR:\\n[o que documentar para denúncia/recuperação]"
                        )
                        res = sherlock_ia(prompt)
                        if res: st.session_state['res_sfraudes_sherlo21'] = str(res)
                        salvar_caso("Fraudes", topico, res)
                        st.session_state['fraude_temp'] = res
                else:
                    st.warning("Escolha ou descreva o golpe.")

            if st.session_state.get('fraude_temp'):
                st.markdown(f"<div class='card-dark'>{st.session_state['fraude_temp']}</div>", unsafe_allow_html=True)
                st.download_button("📋 Baixar (.txt)", data=st.session_state['fraude_temp'], file_name="fraudes_golpes.txt", mime="text/plain", key="sherlock32")

            # ========================
            # DETECTOR DE PADRÕES
            # ========================

        with _sPadroes:
            st.header("🔍 Detector de Padrões")

            dados_padroes = st.text_area("📝 Liste os dados (datas, pessoas, lugares, eventos):", height=180,
                placeholder="ex: Segunda - encontro com João no café X\\nQuarta - mensagem de Maria sobre o mesmo assunto\\n...", key="sherlock5_d2")

            if st.button("🔍 ENCONTRAR PADRÕES", key="sherlock33"):
                if dados_padroes.strip():
                    with st.spinner("Procurando padrões..."):
                        prompt = (
                            f"Analise estes dados procurando padrões e relações escondidas.\\n"
                            f"Dados: {dados_padroes}\\n\\n"
                            f"FORMATO:\\n\\n"
                            f"🔍 PADRÕES IDENTIFICADOS\\n\\n"
                            f"🔗 RELAÇÕES ENTRE OS ELEMENTOS:\\n[conexões encontradas entre datas, pessoas, lugares]\\n\\n"
                            f"📊 PADRÕES DE FREQUÊNCIA:\\n[o que se repete e com que regularidade]\\n\\n"
                            f"⏰ PADRÕES TEMPORAIS:\\n[horários ou dias que se destacam]\\n\\n"
                            f"🎯 PADRÃO MAIS SIGNIFICATIVO:\\n[o que mais chama atenção, e por quê]\\n\\n"
                            f"❓ O QUE ISSO PODE SUGERIR:\\n[hipóteses derivadas do padrão]"
                        )
                        res = sherlock_ia(prompt)
                        if res: st.session_state['res_spadroes_sherlo22'] = str(res)
                        salvar_caso("Padroes", "Detecção de padrões", res)
                        st.session_state['pad_temp'] = res
                else:
                    st.warning("Liste os dados.")

            if st.session_state.get('pad_temp'):
                st.markdown(f"<div class='card-teal'>{st.session_state['pad_temp']}</div>", unsafe_allow_html=True)
                st.download_button("📋 Baixar (.txt)", data=st.session_state['pad_temp'], file_name="padroes.txt", mime="text/plain", key="sherlock34")

            # ========================
            # ANÁLISE DE PROBABILIDADES
            # ========================

        with _sProbabilidades:
            st.header("📊 Análise de Probabilidades")

            hipoteses_prob = st.text_area("📝 Liste as hipóteses que você já tem (uma por linha):", height=150,
                placeholder="ex: A pessoa esqueceu o compromisso\\nA pessoa teve um imprevisto\\nA pessoa evitou de propósito...", key="sherlock4_d2")
            evidencias_prob = st.text_area("📝 Evidências disponíveis:", height=100,
                placeholder="ex: Ela respondeu mensagens normalmente outras vezes...", key="sherlock3_d2")

            if st.button("📊 ANALISAR PROBABILIDADES", key="sherlock35"):
                if hipoteses_prob.strip():
                    with st.spinner("Calculando consistência..."):
                        prompt = (
                            f"Analise a consistência destas hipóteses com as evidências.\\n"
                            f"Hipóteses: {hipoteses_prob}\\n"
                            f"Evidências: {evidencias_prob or 'não informadas'}\\n\\n"
                            f"FORMATO:\\n\\n"
                            f"📊 ANÁLISE DE PROBABILIDADES\\n\\n"
                            f"[Para cada hipótese listada:]\\n"
                            f"🧩 [HIPÓTESE]\\n"
                            f"Consistência com as evidências: [X]/100\\n"
                            f"Justificativa: [por quê]\\n\\n"
                            f"🎯 HIPÓTESE MAIS CONSISTENTE:\\n[qual tem maior consistência com as evidências, e por quê — sem afirmar certeza absoluta]\\n\\n"
                            f"⚠️ LIMITAÇÃO DESTA ANÁLISE:\\n[o que ainda impede uma conclusão definitiva]"
                        )
                        res = sherlock_ia(prompt)
                        if res: st.session_state['res_sprobabilida_sherlo23'] = str(res)
                        salvar_caso("Probabilidades", "Análise de probabilidades", res)
                        st.session_state['prob_temp'] = res
                else:
                    st.warning("Liste as hipóteses.")

            if st.session_state.get('prob_temp'):
                renderizar_indice(st.session_state['prob_temp'], "CONSISTÊNCIA GERAL")
                st.markdown(f"<div class='card'>{st.session_state['prob_temp']}</div>", unsafe_allow_html=True)
                st.markdown(DISCLAIMER_PADRAO, unsafe_allow_html=True)
                st.download_button("📋 Baixar (.txt)", data=st.session_state['prob_temp'], file_name="probabilidades.txt", mime="text/plain", key="sherlock36")

            # ========================
            # PERGUNTAS INTELIGENTES
            # ========================

        with _sPerguntas:
            st.header("❓ Perguntas Inteligentes")

            situacao_perg = st.text_area("📝 Descreva a situação:", height=150, value=st.session_state.caso_padrao, key="situacao_perg")

            if st.button("❓ GERAR PERGUNTAS", key="sherlock37"):
                if situacao_perg.strip():
                    with st.spinner("Pensando nas perguntas certas..."):
                        prompt = (
                            f"Gere as perguntas que um investigador experiente faria sobre esta situação.\\n"
                            f"Situação: {situacao_perg}\\n\\n"
                            f"FORMATO:\\n\\n"
                            f"❓ PERGUNTAS QUE UM INVESTIGADOR FARIA\\n\\n"
                            f"🎯 PERGUNTAS FUNDAMENTAIS:\\n[5-7 perguntas essenciais que ainda não foram respondidas]\\n\\n"
                            f"🔍 PERGUNTAS QUE NINGUÉM PENSOU EM FAZER:\\n[2-3 perguntas não óbvias mas potencialmente decisivas]\\n\\n"
                            f"💡 POR QUE ESSAS PERGUNTAS IMPORTAM:\\n[explicação de como cada uma pode destravar a investigação]"
                        )
                        res = sherlock_ia(prompt)
                        if res: st.session_state['res_sperguntas_sherlo24'] = str(res)
                        salvar_caso("Perguntas", situacao_perg[:60], res)
                        st.session_state['perg_temp'] = res
                else:
                    st.warning("Descreva a situação.")

            if st.session_state.get('perg_temp'):
                st.markdown(f"<div class='card-gold'>{st.session_state['perg_temp']}</div>", unsafe_allow_html=True)
                st.download_button("📋 Baixar (.txt)", data=st.session_state['perg_temp'], file_name="perguntas.txt", mime="text/plain", key="sherlock38")

            # ========================
            # PENSAMENTO CRÍTICO
            # ========================

        with _sCritico:
            st.header("⚖️ Pensamento Crítico")

            raciocinio_critico = st.text_area("📝 Cole seu raciocínio ou conclusão sobre algo:", height=150,
                placeholder="ex: Acho que ela está escondendo algo porque ficou nervosa quando perguntei sobre o fim de semana...", key="sherlock2")

            if st.button("⚖️ ANALISAR MEU RACIOCÍNIO", key="sherlock39"):
                if raciocinio_critico.strip():
                    with st.spinner("Analisando..."):
                        prompt = (
                            f"Analise este raciocínio identificando possíveis vieses e erros de interpretação.\\n"
                            f"Raciocínio: {raciocinio_critico}\\n\\n"
                            f"FORMATO:\\n\\n"
                            f"⚖️ ANÁLISE DO RACIOCÍNIO\\n\\n"
                            f"🧠 VIESES POSSÍVEIS IDENTIFICADOS:\\n[viés de confirmação, ancoragem, etc — se aplicável]\\n\\n"
                            f"⚠️ POSSÍVEIS ERROS DE INTERPRETAÇÃO:\\n[onde a conclusão pode estar pulando etapas]\\n\\n"
                            f"📊 GENERALIZAÇÕES:\\n[se há generalização apressada]\\n\\n"
                            f"❓ FALTA DE EVIDÊNCIAS:\\n[onde a conclusão se apoia em suposição, não fato]\\n\\n"
                            f"✅ COMO FORTALECER ESSE RACIOCÍNIO:\\n[o que ajudaria a confirmar ou refutar com mais solidez]"
                        )
                        res = sherlock_ia(prompt)
                        if res: st.session_state['res_scritico_sherlo25'] = str(res)
                        salvar_caso("Critico", raciocinio_critico[:60], res)
                        st.session_state['crit_temp'] = res
                else:
                    st.warning("Cole seu raciocínio.")

            if st.session_state.get('crit_temp'):
                st.markdown(f"<div class='card-dark'>{st.session_state['crit_temp']}</div>", unsafe_allow_html=True)
                st.download_button("📋 Baixar (.txt)", data=st.session_state['crit_temp'], file_name="pensamento_critico.txt", mime="text/plain", key="sherlock40")

            # ========================
            # MÉTODO SHERLOCK
            # ========================

        with _sMetodo:
            st.header("🧠 Método Sherlock")

            tecnica_metodo = st.selectbox("Técnica:", ["Dedução","Indução","Abdução","Observação","Eliminação de hipóteses","Raciocínio lógico","Investigação científica"], key="sherlock41")

            if st.button("🧠 APRENDER", key="sherlock42"):
                with st.spinner("Preparando explicação..."):
                    prompt = (
                        f"Explique de forma didática a técnica: {tecnica_metodo}\\n\\n"
                        f"FORMATO:\\n\\n"
                        f"🧠 {tecnica_metodo.upper()}\\n\\n"
                        f"📖 O QUE É:\\n[definição clara]\\n\\n"
                        f"🔍 COMO FUNCIONA:\\n[mecanismo passo a passo]\\n\\n"
                        f"💡 EXEMPLO PRÁTICO:\\n[exemplo ilustrativo, fictício]\\n\\n"
                        f"🎯 QUANDO USAR:\\n[situações onde essa técnica é mais útil]\\n\\n"
                        f"🏋️ EXERCÍCIO PARA TREINAR:\\n[1 exercício prático]"
                    )
                    res = sherlock_ia(prompt)
                    if res: st.session_state['res_smetodo_sherlo26'] = str(res)
                    salvar_caso("Metodo", tecnica_metodo, res)
                    st.session_state['metodo_temp'] = res

            if st.session_state.get('metodo_temp'):
                st.markdown(f"<div class='card'>{st.session_state['metodo_temp']}</div>", unsafe_allow_html=True)
                st.download_button("📋 Baixar (.txt)", data=st.session_state['metodo_temp'], file_name="metodo.txt", mime="text/plain", key="sherlock43")

            # ========================
            # LABORATÓRIO FORENSE (EDUCATIVO)
            # ========================

# --- RODAPÉ ---
st.markdown(
    "<div style='text-align:center;color:#999;font-size:0.8em;margin-top:60px;'>"
    "</div>", unsafe_allow_html=True
)
""",
    "oraculo_financeiro": """# [hub] import streamlit as st
# [hub] from groq import Groq
import pandas as pd
# [hub] from datetime import datetime, date
# [hub] import json
import math

# ─────────────────────────────────────────────
# CONFIG PÁGINA
# ─────────────────────────────────────────────
# set_page_config removido pelo super_agente

st.markdown(\"\"\"
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
[data-testid="stToolbar"] {visibility: hidden;}
[data-testid="stDecoration"] {visibility: hidden;}
[data-testid="stStatusWidget"] {visibility: hidden;}
</style>
\"\"\", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# DESIGN
# ─────────────────────────────────────────────
st.markdown(\"\"\"
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    .stApp { background-color:#F6FBF4; font-family:'Inter',sans-serif; }
    [data-testid="stSidebar"] { display:none; }

    .stTextInput>div>div>input, .stTextArea>div>textarea,
    .stSelectbox>div>div>div, .stNumberInput>div>div>input {
        background-color:#FFFFFF !important; color:#1A1A2E !important;
        border:1px solid #CED4DA !important; font-family:'Inter',sans-serif !important;
    }

    .stButton>button {
        width:100%; border-radius:10px; height:3.2em;
        background:linear-gradient(135deg,#16A34A,#15803D) !important; color:white !important;
        font-weight:600; border:none; box-shadow:2px 2px 8px rgba(0,0,0,0.1);
        font-family:'Inter',sans-serif !important; transition:all 0.2s ease;
    }
    .stButton>button:hover { background:linear-gradient(135deg,#15803D,#166534) !important; transform:translateY(-1px); }
    .stApp .stButton>button, .stApp .stButton>button p,
    .stApp .stButton>button span, .stApp .stButton>button div { color:white !important; }

    .stApp h1, .stApp h2, .stApp h3 { color:#14532D !important; font-family:'Inter',sans-serif !important; font-weight:700 !important; }

    .card { background:linear-gradient(135deg,#F0FDF4,#DCFCE7); padding:20px; border-radius:14px; border:1px solid #86EFAC; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card, .stApp .card p, .stApp .card span, .stApp .card div, .stApp .card strong, .stApp .card em { color:#14532D !important; }

    .card-dark { background:linear-gradient(135deg,#DCFCE7,#D1FAE5); padding:20px; border-radius:14px; border:1px solid #6EE7B7; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-dark, .stApp .card-dark p, .stApp .card-dark span, .stApp .card-dark div, .stApp .card-dark strong { color:#14532D !important; }

    .card-green { background:linear-gradient(135deg,#DCFCE7,#BBF7D0); padding:20px; border-radius:14px; border:1px solid #4ADE80; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-green, .stApp .card-green p, .stApp .card-green span, .stApp .card-green div { color:#14532D !important; }

    .card-blue { background:linear-gradient(135deg,#EFF6FF,#DBEAFE); padding:20px; border-radius:14px; border:1px solid #93C5FD; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-blue, .stApp .card-blue p, .stApp .card-blue span, .stApp .card-blue div { color:#1E3A8A !important; }

    .card-red { background:linear-gradient(135deg,#FFF5F5,#FEE2E2); padding:20px; border-radius:14px; border:1px solid #FECACA; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-red, .stApp .card-red p, .stApp .card-red span, .stApp .card-red div { color:#7F1D1D !important; }

    .card-yellow { background:linear-gradient(135deg,#FFFBEB,#FEF3C7); padding:18px; border-radius:12px; border:1px solid #FCD34D; margin-bottom:12px; white-space:normal; word-wrap:break-word; }
    .stApp .card-yellow, .stApp .card-yellow p, .stApp .card-yellow span, .stApp .card-yellow div { color:#78350F !important; }

    .stat-box { background:#FFFFFF; border-radius:12px; padding:16px; text-align:center; border:1px solid #86EFAC; }
    .stApp .stat-box div, .stApp .stat-box span, .stApp .stat-box p { color:#14532D !important; }
    .stApp .stat-numero, .stat-numero { font-size:2em; font-weight:700; color:#166534 !important; }

    .hist-item { background:#FFFFFF; border-radius:10px; padding:12px 16px; margin-bottom:8px; border-left:4px solid #86EFAC; }
    .stApp .hist-item, .stApp .hist-item p, .stApp .hist-item span, .stApp .hist-item div, .stApp .hist-item small { color:#14532D !important; }

    .badge { background:#166534; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-verde { background:#059669; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-amarelo { background:#B45309; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-azul { background:#1D4ED8; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-roxo { background:#6D28D9; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }

    .divider { border:none; height:1px; background:linear-gradient(to right,transparent,#86EFAC,transparent); margin:18px 0; }

    .chat-user { background:#FFFFFF; border:1px solid #86EFAC; border-radius:12px 12px 4px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-user, .stApp .chat-user p, .stApp .chat-user span, .stApp .chat-user div { color:#14532D !important; }

    .chat-persona { background:#F6FBF4; border:1px solid #86EFAC; border-radius:4px 12px 12px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-persona, .stApp .chat-persona p, .stApp .chat-persona span, .stApp .chat-persona div { color:#14532D !important; }

    .questao-box { background:#FFFFFF; border:2px solid #86EFAC; border-radius:12px; padding:18px; margin-bottom:14px; }
    .stApp .questao-box, .stApp .questao-box p, .stApp .questao-box span, .stApp .questao-box div { color:#14532D !important; }

    .avaliacao-box { background:#FFFFFF; border:2px solid #86EFAC; border-radius:14px; padding:18px; margin-bottom:12px; }
    .stApp .avaliacao-box, .stApp .avaliacao-box p, .stApp .avaliacao-box span, .stApp .avaliacao-box div { color:#14532D !important; }

    .meta-box { background:#FFFFFF; border:2px solid #86EFAC; border-radius:12px; padding:16px; text-align:center; margin:10px 0; }
    .stApp .meta-box, .stApp .meta-box div, .stApp .meta-box span { color:#14532D !important; }
    .stApp .meta-numero { font-size:2em; font-weight:700; color:#166534 !important; }

    .chat-scroll-container { max-height:40vh; overflow-y:auto; display:flex; flex-direction:column; scroll-behavior:smooth; padding-bottom:4px; }
    .chat-scroll-container > * { flex-shrink:0; }

    /* ── CLASSES USADAS NO APP ── */
    .card-purple { background:linear-gradient(135deg,#F5F3FF,#EDE9FE); padding:20px; border-radius:14px; border:1px solid #C4B5FD; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-purple, .stApp .card-purple p, .stApp .card-purple span, .stApp .card-purple div { color:#3B0764 !important; }

    .card-gold { background:linear-gradient(135deg,#FFFBEB,#FEF3C7); padding:20px; border-radius:14px; border:1px solid #FCD34D; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-gold, .stApp .card-gold p, .stApp .card-gold span, .stApp .card-gold div { color:#78350F !important; }

    .alert-info { background:#EFF6FF; border:1px solid #93C5FD; border-radius:8px; padding:10px 14px; font-size:13px; color:#1E40AF !important; margin-bottom:8px; }
    .alert-warn { background:#FFFBEB; border:1px solid #FCD34D; border-radius:8px; padding:10px 14px; font-size:13px; color:#92400E !important; margin-bottom:8px; }
    .alert-danger { background:#FFF5F5; border:1px solid #FECACA; border-radius:8px; padding:10px 14px; font-size:13px; color:#991B1B !important; margin-bottom:8px; }
    .alert-success { background:#F0FDF4; border:1px solid #86EFAC; border-radius:8px; padding:10px 14px; font-size:13px; color:#166534 !important; margin-bottom:8px; }

    .metric-box { background:#FFFFFF; border-radius:12px; padding:14px 10px; text-align:center; border:1px solid #E5E7EB; }
    .metric-label { font-size:11px; color:#6B7280; margin-bottom:4px; font-weight:600; text-transform:uppercase; letter-spacing:0.5px; }
    .metric-value { font-size:20px; font-weight:700; color:#1A1A2E; }
    .metric-sub { font-size:11px; color:#9CA3AF; margin-top:2px; }

    .prog-wrap { background:#E5E7EB; border-radius:999px; height:7px; overflow:hidden; margin:5px 0; }
    .prog-fill { height:100%; border-radius:999px; transition:width 0.4s ease; }

    .badge-green  { background:#059669; color:white !important; padding:3px 10px; border-radius:20px; font-size:11px; font-weight:600; display:inline-block; }
    .badge-gold   { background:#B45309; color:white !important; padding:3px 10px; border-radius:20px; font-size:11px; font-weight:600; display:inline-block; }
    .badge-red    { background:#DC2626; color:white !important; padding:3px 10px; border-radius:20px; font-size:11px; font-weight:600; display:inline-block; }
    .badge-purple { background:#7C3AED; color:white !important; padding:3px 10px; border-radius:20px; font-size:11px; font-weight:600; display:inline-block; }

    .list-item { display:flex; justify-content:space-between; align-items:center; padding:8px 0; border-bottom:1px solid #F3F4F6; font-size:13px; }
    .list-item:last-child { border-bottom:none; }

    .chat-ai { background:#F6FBF4; border:1px solid #86EFAC; border-radius:4px 12px 12px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-ai, .stApp .chat-ai p, .stApp .chat-ai span, .stApp .chat-ai div { color:#14532D !important; }

    </style>
\"\"\", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PERSISTÊNCIA LOCAL (JSON)
# ─────────────────────────────────────────────
CHAVES_SALVAR = [
    "nome_user", "renda_total", "outras_rendas", "gastos", "metas",
    "contas_fixas", "dividas", "historico_chat", "categorias_gastos",
    "reserva_emergencia", "patrimonio_itens", "config_meta_reserva",
    "taxa_invest_anual", "aporte_inv_salvo", "cap_ini_inv_salvo",
]

# ── CACHE — persiste enquanto servidor não reiniciar ──────────
@st.cache_resource
def get_cache_oraculo():
    return {"perfis": {}}   # {nome_user: dados}

_cache = get_cache_oraculo()

def gerar_json_sessao() -> str:
    dados = {k: st.session_state.get(k) for k in CHAVES_SALVAR}
    dados["salvo_em"] = str(datetime.now())
    return json.dumps(dados, ensure_ascii=False, indent=2, default=str)

def carregar_json_sessao(dados):
    _bloq = {'api_key','etapa','nome_login','chave_login','upload_login','btn_entrar_login',
             'input_nome_login','input_chave_login','autenticado'}
    _pref = (
        'btn_','sel_','ul_','dl_','cad_','_sub','_sm','_tab','_bsc',
        'ativo_','rem_','sel_pet_','ev_','prof_','hig_','prev_',
        'vac_','sint_','comp_','trad_','subs_','amb_','viag_','chat_',
        'duvida_','emerg_','peso_','data_','obs_','tipo_','vet_','desc_',
        'local_','prox_','alim','sit_emerg_','tc_','oraf','siau','agmag',
        'lv','mv','pt','pi','sh','wc','rv','rp','rc',
        'input_','upload_','oraculof',
    )
    import re as _re
    for k, v in dados.items():
        if k in _bloq: continue
        if any(k.startswith(p) for p in _pref): continue
        if _re.match(r'.+_?\\d+$', k): continue
        st.session_state[k] = v
    # Forçar ressincronização dos widgets de investimento após carregar JSON
    for _wk in ('inv_aporte_mensal', 'inv_capital_ini'):
        if _wk in st.session_state:
            del st.session_state[_wk]
def salvar_perfil_cache(nome: str, dados: dict):
    \"\"\"Salva no cache enquanto servidor estiver vivo.\"\"\"
    _cache["perfis"][nome] = dados.copy()

def carregar_perfil_cache(nome: str) -> dict | None:
    return _cache["perfis"].get(nome)

def perfis_salvos() -> list:
    return list(_cache["perfis"].keys())

# ─────────────────────────────────────────────
# INICIALIZAÇÃO DE ESTADOS
# ─────────────────────────────────────────────
def init():
    defaults = {
        "autenticado": False,
        "nome_user": "",
        "api_key": "",
        "renda_total": 0.0,
        "outras_rendas": [],
        "gastos": [],
        "metas": [],
        "contas_fixas": [],
        "dividas": [],
        "historico_chat": [],
        "categorias_gastos": ["Alimentação","Transporte","Moradia","Saúde","Lazer","Educação","Vestuário","Tecnologia","Outros"],
        "nivel_evolucao": "Nível 1: Iniciante",
        "perfil_decisao": "Não Identificado",
        "reserva_emergencia": 0.0,
        "patrimonio_itens": [],
        "config_meta_reserva": 6,
        "taxa_invest_anual": 10.0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init()

# ─────────────────────────────────────────────
# UTILITÁRIOS
# ─────────────────────────────────────────────
def fmt(v):
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def pct(v, total):
    return round(v / total * 100, 1) if total > 0 else 0.0

def barra(valor_pct, cor="#7C6FFF"):
    p = max(0, min(100, valor_pct))
    return f'<div class="prog-wrap"><div class="prog-fill" style="width:{p}%;background:{cor};"></div></div>'

def get_totais():
    renda  = st.session_state.renda_total + sum(x["valor"] for x in st.session_state.outras_rendas)
    gv     = sum(x["valor"] for x in st.session_state.gastos)
    gf     = sum(x["valor"] for x in st.session_state.contas_fixas if x.get("ativa", True))
    gm     = sum(x["mensal"] for x in st.session_state.metas)
    div_m  = sum(x["parcela_mensal"] for x in st.session_state.dividas)
    saldo  = renda - gv - gf - gm - div_m
    if renda > 0:
        r = saldo / renda
        if r >= 0.4:    st.session_state.nivel_evolucao = "Nível 5: Independente 🏆"
        elif r >= 0.25: st.session_state.nivel_evolucao = "Nível 4: Estratégico 🎯"
        elif r >= 0.1:  st.session_state.nivel_evolucao = "Nível 3: Organizado ✅"
        elif r >= 0:    st.session_state.nivel_evolucao = "Nível 2: Equilibrado ⚖️"
        else:           st.session_state.nivel_evolucao = "Nível 1: Déficit 🚨"
    return renda, gv, gf, gm, div_m, saldo

# ─────────────────────────────────────────────
# IA — CONSULTOR
# ─────────────────────────────────────────────
def contexto_financeiro():
    renda, gv, gf, gm, div_m, saldo = get_totais()
    meta_res = gf * st.session_state.config_meta_reserva
    cats = {}
    for g in st.session_state.gastos:
        cats[g["tipo"]] = cats.get(g["tipo"], 0) + g["valor"]
    cats_txt    = "\\n".join(f"  • {c}: R${v:.2f} ({pct(v, renda)}%)" for c, v in cats.items()) or "  Nenhum"
    dividas_txt = "\\n".join(f"  • {d['nome']}: saldo R${d['valor_total']-d['valor_pago']:.2f}, juros {d['juros_mensal']}%/mês" for d in st.session_state.dividas) or "  Nenhuma"
    metas_txt   = "\\n".join(f"  • {m['nome']}: {fmt(m.get('atual',0))}/{fmt(m['valor'])}" for m in st.session_state.metas) or "  Nenhuma"
    return f\"\"\"
DADOS DO USUÁRIO:
Renda total: R${renda:.2f}
Despesas fixas: R${gf:.2f} ({pct(gf,renda)}%)
Gastos variáveis: R${gv:.2f} ({pct(gv,renda)}%)
Parcelas de dívidas: R${div_m:.2f}
Metas mensais: R${gm:.2f} ({pct(gm,renda)}%)
Saldo livre: R${saldo:.2f} ({pct(saldo,renda)}%)
Reserva atual: R${st.session_state.reserva_emergencia:.2f} (meta: R${meta_res:.2f})
Gastos por categoria:\\n{cats_txt}
Dívidas:\\n{dividas_txt}
Metas:\\n{metas_txt}
\"\"\"

def consultor(prompt, historico):
    try:
        client = Groq(api_key=st.session_state.api_key)
        sys_msg = f\"\"\"Você é o Oráculo Financeiro — mentor de decisões financeiras pessoais. REGRA DE OURO — CONFIABILIDADE 100%%: Forneça APENAS informações que você tem certeza absoluta que são verdadeiras. JAMAIS invente, suponha, extrapole ou preencha lacunas com dados fictícios. Se não souber algo com certeza — preço, endereço, horário, nome, estatística, lei, fato — diga EXPLICITAMENTE: 'Não tenho certeza sobre isso, recomendo verificar em [fonte].' É melhor uma resposta incompleta e honesta do que uma resposta completa e inventada. O usuário depende dessas informações para tomar decisões reais.
Filosofia: direto, estratégico, sem rodeios. Aponta problemas sem medo.
Nomenclatura: Blindagem = fixas+reserva | Expansão = metas/investimentos | Estabilidade = saldo livre.
Regra 50/30/20: 50% necessidades, 30% desejos, 20% poupança.
{contexto_financeiro()}
Nível: {st.session_state.nivel_evolucao} | Perfil: {st.session_state.perfil_decisao}
Responda em no máximo 4 parágrafos curtos. Sugira 1 ação concreta ao final.
Termine sempre com: "⚠️ Análise baseada nos seus dados. Consulte um profissional certificado para decisões de grande impacto."
\"\"\"
        msgs = [{"role": "system", "content": sys_msg}]
        for m in historico[-10:]:
            msgs.append(m)
        msgs.append({"role": "user", "content": prompt})
        r = client.chat.completions.create(messages=msgs, model="openai/gpt-oss-120b", max_tokens=700, temperature=0.7)
        return r.choices[0].message.content
    except Exception as e:
        return f"⚠️ Oráculo indisponível. Verifique sua chave API. Erro: {str(e)[:80]}"

# ─────────────────────────────────────────────
# TELA DE LOGIN
# ─────────────────────────────────────────────
# Garantia extra: init() já rodou acima, mas asseguramos valores padrão corretos
if 'aporte_inv_salvo' not in st.session_state or st.session_state['aporte_inv_salvo'] is None:
    st.session_state['aporte_inv_salvo'] = 0.0
else:
    st.session_state['aporte_inv_salvo'] = float(st.session_state['aporte_inv_salvo'])
if 'cap_ini_inv_salvo' not in st.session_state or st.session_state['cap_ini_inv_salvo'] is None:
    st.session_state['cap_ini_inv_salvo'] = 0.0
else:
    st.session_state['cap_ini_inv_salvo'] = float(st.session_state['cap_ini_inv_salvo'])
if 'outras_rendas' not in st.session_state or st.session_state['outras_rendas'] is None:
    st.session_state['outras_rendas'] = []
if 'patrimonio_itens' not in st.session_state or st.session_state['patrimonio_itens'] is None:
    st.session_state['patrimonio_itens'] = []
if 'reserva_emergencia' not in st.session_state or st.session_state['reserva_emergencia'] is None:
    st.session_state['reserva_emergencia'] = 0.0
if 'config_meta_reserva' not in st.session_state or st.session_state['config_meta_reserva'] is None:
    st.session_state['config_meta_reserva'] = 6
if 'taxa_invest_anual' not in st.session_state or st.session_state['taxa_invest_anual'] is None:
    st.session_state['taxa_invest_anual'] = 10.0
if 'nivel_evolucao' not in st.session_state or st.session_state['nivel_evolucao'] is None:
    st.session_state['nivel_evolucao'] = "Nível 1: Iniciante"
if 'perfil_decisao' not in st.session_state or st.session_state['perfil_decisao'] is None:
    st.session_state['perfil_decisao'] = "Não Identificado"

if not st.session_state.autenticado:
    st.markdown(\"\"\"
    <div style="text-align:center; padding:30px 20px 20px 20px;">
      <div style="font-size:56px; margin-bottom:8px;">💰</div>
      <h1 style="font-size:28px; margin:0; color:#1A1A2E;">Oráculo Financeiro</h1>
      <p style="font-size:13px; color:#4B5563; letter-spacing:2px; margin-top:6px;">ECONOMIZE • GERENCIE • INVISTA • CRESÇA</p>
    </div>
    \"\"\", unsafe_allow_html=True)

    st.markdown("<div class='card'><b>🔒 ACESSO RESTRITO A ASSOCIADOS DO MEUSAGENTESIA.COM.BR</b><br>🔗 <a href='https://meusagentesia.com.br' target='_blank' style='color:#4F46E5;font-weight:700;text-decoration:underline;'>meusagentesia.com.br</a></div>", unsafe_allow_html=True)
    st.info("💻 **Dica:** Pela complexidade dos agentes, no computador a experiência é mais agradável.")

    with st.form("login"):
        nome  = st.text_input("👤 Seu nome", key="input_nome_login")
        chave = st.text_input("🔑 Chave Groq API", type="password", key="input_chave_login")

        # ── UPLOADER ─────────────────────
        st.markdown(\"\"\"<div style="background:#FFFBEB;border:1px solid #FDE68A;border-radius:8px;
        padding:10px 14px;font-size:0.85em;color:#92400E;line-height:1.6;margin-top:8px;">
        📥 <strong>Seus dados sumiram?</strong> Isso acontece quando o servidor reinicia.<br>
        Selecione abaixo o arquivo <strong>.json</strong> que você salvou antes — tudo volta como era.
        </div>\"\"\", unsafe_allow_html=True)

        if st.form_submit_button("🚀 ENTRAR NO SISTEMA", key="oraculoffsb501"):
            if nome and chave:
                st.session_state.nome_user   = nome
                st.session_state.api_key     = chave
                st.session_state.autenticado = True
                st.rerun()
            else:
                st.error("Preencha nome e chave API.")

    st.markdown("🔑 Não tem chave Groq? Crie grátis em <a href='https://console.groq.com/keys' target='_blank' style='color:#5B50E8;font-weight:600;'>console.groq.com/keys</a>", unsafe_allow_html=True)
    st.stop()

# ─────────────────────────────────────────────
# SISTEMA LOGADO
# ─────────────────────────────────────────────
renda, gv, gf, gm, div_m, saldo = get_totais()

# HEADER
c1, c2, c3 = st.columns([3, 2, 1])
with c1:
    st.markdown(f"<h1 style='margin:0;font-size:24px;color:#1A1A2E;'>💰 Oráculo de {st.session_state.nome_user}</h1>", unsafe_allow_html=True)
with c2:
    nivel = st.session_state.nivel_evolucao
    cls   = "badge-green" if ("5" in nivel or "4" in nivel) else ("badge-gold" if ("3" in nivel or "2" in nivel) else "badge-red")
    st.markdown(f"<div style='padding:14px 0;text-align:right;'><span class='{cls}' style='padding:6px 14px;font-size:12px;'>{nivel}</span></div>", unsafe_allow_html=True)
with c3:
    if st.button("🚪 Sair", key="oraculof1"):
        st.session_state.autenticado = False
        st.rerun()

# ── SALVAR NO CACHE AUTOMATICAMENTE ──────────────────────────
nome_arquivo = st.session_state.nome_user.lower().replace(" ", "_") or "meus_dados"
json_sessao  = gerar_json_sessao()
dados_atuais = {k: st.session_state.get(k) for k in CHAVES_SALVAR}
salvar_perfil_cache(st.session_state.nome_user, dados_atuais)

# ── BARRA DE SALVAR NO COMPUTADOR ────────────────────────────
tem_dados_logado = (
    len(st.session_state.gastos) > 0 or
    len(st.session_state.contas_fixas) > 0 or
    st.session_state.renda_total > 0
)
col_av, col_btn = st.columns([4, 2])
with col_av:
    if tem_dados_logado:
        st.markdown(\"\"\"<div style="background:#FFFBEB;border:1px solid #FDE68A;border-radius:10px;
        padding:10px 14px;font-size:0.84em;color:#92400E;line-height:1.6;">
        💾 <strong>Antes de sair, salve seus dados no computador</strong> — se o servidor reiniciar, faça o upload do arquivo para recuperar tudo.
        </div>\"\"\", unsafe_allow_html=True)
with col_btn:
    st.download_button(
        label="💾 SALVAR MEUS DADOS (.json)",
        data=json_sessao,
        file_name=f"oraculo_{nome_arquivo}.json",
        mime="application/json",
        use_container_width=True,
    
        key="oraf3001",
    )

st.markdown("<hr>", unsafe_allow_html=True)

# TABS
tabs = st.tabs([
    "🏠 Dashboard", "🧠 Consultor IA", "💵 Renda",
    "💸 Gastos", "🎯 Metas", "🛡️ Fixas",
    "💳 Dívidas", "🏦 Reserva", "📈 Investimentos",
    "⚖️ Patrimônio", "📊 Relatório", "⚙️ Config"
])

# ── BARRA SALVAR — visível em todas as abas ──
with st.expander("💾 Salvar / Carregar meus dados", expanded=False):
    _bsc1, _bsc2 = st.columns(2)
    with _bsc1:
        _dsv_or = {k: st.session_state.get(k) for k in list(st.session_state.keys()) if not k.startswith('_') and k not in ('api_key','input_nome_login','input_chave_login','upload_login')}
(tab_dash, tab_ia, tab_renda, tab_gastos, tab_metas,
 tab_fixas, tab_div, tab_res, tab_inv,
 tab_pat, tab_rel, tab_cfg) = tabs

# ══════════════════════════════════════════════
# 1. DASHBOARD
# ══════════════════════════════════════════════
with tab_dash:

    # ── AVISO SE DADOS SUMIRAM ────────────────────────────────
    tem_dados_dash = (
        len(st.session_state.gastos) > 0 or
        len(st.session_state.contas_fixas) > 0 or
        st.session_state.renda_total > 0
    )
    if not tem_dados_dash:
        st.markdown(\"\"\"<div style="background:#FFFBEB;border:2px solid #F59E0B;border-radius:12px;
        padding:12px 18px;margin-bottom:4px;color:#92400E;font-size:0.9em;font-weight:600;">
        ⚠️ Seus dados não estão mais no servidor.
        </div>\"\"\", unsafe_allow_html=True)


    # Alerta de situação
    if renda == 0:
        st.markdown('<div class="alert-info">ℹ️ Comece cadastrando sua renda na aba <b>Renda</b>.</div>', unsafe_allow_html=True)
    elif saldo < 0:
        st.markdown(f'<div class="alert-danger">🚨 <b>Déficit de {fmt(abs(saldo))}!</b> Você gasta mais do que ganha. Ação imediata necessária.</div>', unsafe_allow_html=True)
    elif saldo < renda * 0.1:
        st.markdown(f'<div class="alert-warn">⚠️ Margem muito baixa ({pct(saldo,renda)}%). Recomendado: mínimo 20% livre.</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="alert-success">✅ Sistema saudável. {fmt(saldo)} livres para expandir.</div>', unsafe_allow_html=True)

    # MÉTRICAS PRINCIPAIS
    c1, c2, c3, c4, c5 = st.columns(5)
    def metrica(col, label, val, cor, sub=""):
        col.markdown(f'<div class="metric-box"><div class="metric-label">{label}</div><div class="metric-value" style="color:{cor};">{fmt(val)}</div><div class="metric-sub">{sub}</div></div>', unsafe_allow_html=True)

    metrica(c1, "💰 Renda",            renda,            "#6EE7B7", "total/mês")
    metrica(c2, "🛡️ Blindagem",        gf,               "#7DD3FC", f"{pct(gf,renda)}% da renda")
    metrica(c3, "💸 Gastos Variáveis",  gv,               "#FCD34D", f"{pct(gv,renda)}% da renda")
    metrica(c4, "🚀 Metas/Mês",         gm,               "#6D28D9", f"{pct(gm,renda)}% da renda")
    cor_s = "#6EE7B7" if saldo >= 0 else "#FCA5A5"
    metrica(c5, "⚖️ Estabilidade",     saldo,            cor_s,     f"{pct(saldo,renda)}% livre")


    # ── GUIA DAS ABAS ────────────────────────────────────────
    st.markdown("### 🗺️ O que cada aba faz")
    guia = {
        "🏠 Dashboard":        "Visão geral da sua saúde financeira com alertas e diagnóstico automático",
        "🧠 Consultor IA":     "Mentor financeiro que conhece seus números e responde perguntas diretas",
        "💵 Renda":            "Cadastre seu salário e outras fontes de renda",
        "💸 Gastos":           "Registre e categorize seus gastos variáveis",
        "🎯 Metas":            "Crie e acompanhe metas de economia e investimento",
        "🛡️ Fixas":            "Gerencie suas contas fixas mensais",
        "💳 Dívidas":          "Controle dívidas com estratégia avalanche ou bola de neve",
        "🏦 Reserva":          "Acompanhe sua reserva de emergência",
        "📈 Investimentos":    "Simulações e estratégias de investimento por perfil",
        "⚖️ Patrimônio":       "Balanço entre ativos e passivos — seu patrimônio líquido",
        "📊 Relatório":        "Relatório completo com fluxo de caixa e exportação",
        "⚙️ Config":           "Ajuste metas e configurações do sistema",
    }
    for aba, desc in guia.items():
        st.markdown(f"**{aba}** — {desc}")

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<b style='color:#1A1A2E;'>📊 Distribuição da Renda</b>", unsafe_allow_html=True)
        if renda > 0:
            for nome_d, val_d, cor_d in [
                ("🛡️ Fixas",       gf,              "#38BDF8"),
                ("💸 Variáveis",   gv,              "#FCD34D"),
                ("💳 Dívidas",     div_m,           "#FCA5A5"),
                ("🚀 Metas",       gm,              "#6D28D9"),
                ("✅ Livre",       max(0, saldo),   "#6EE7B7"),
            ]:
                pct_d = pct(val_d, renda)
                st.markdown(f\"\"\"
                <div style="display:flex;justify-content:space-between;margin-bottom:3px;">
                  <span style="font-size:13px;color:#555577;">{nome_d}</span>
                  <span style="font-size:13px;color:#1A1A2E;">{fmt(val_d)} <span style="color:#4B5563;">({pct_d}%)</span></span>
                </div>{barra(pct_d, cor_d)}\"\"\", unsafe_allow_html=True)
        else:
            st.markdown("<p>Cadastre sua renda para ver a distribuição.</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<b style='color:#1A1A2E;'>📐 Regra 50/30/20</b>", unsafe_allow_html=True)
        if renda > 0:
            cats_nec = ["Moradia","Alimentação","Saúde","Transporte"]
            cats_des = ["Lazer","Vestuário","Tecnologia"]
            nec = gf + sum(g["valor"] for g in st.session_state.gastos if g["tipo"] in cats_nec)
            des = sum(g["valor"] for g in st.session_state.gastos if g["tipo"] in cats_des)
            pou = gm
            for rotulo_r, valor_r, ideal_r, cor_r in [
                ("🏠 Necessidades (ideal 50%)", nec, 50, "#38BDF8"),
                ("🎮 Desejos     (ideal 30%)",  des, 30, "#FCD34D"),
                ("📈 Poupança    (ideal 20%)",  pou, 20, "#6EE7B7"),
            ]:
                real_r = pct(valor_r, renda)
                ok_r   = "✅" if abs(real_r - ideal_r) <= 10 else "⚠️"
                st.markdown(f\"\"\"
                <div style="display:flex;justify-content:space-between;margin-bottom:3px;">
                  <span style="font-size:13px;color:#555577;">{rotulo_r}</span>
                  <span style="font-size:13px;color:#1A1A2E;">{ok_r} {real_r:.1f}%</span>
                </div>{barra(real_r, cor_r)}\"\"\", unsafe_allow_html=True)
        else:
            st.markdown("<p>Cadastre sua renda para ver a análise.</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_b:
        meta_res_d = gf * st.session_state.config_meta_reserva
        pct_res_d  = pct(st.session_state.reserva_emergencia, meta_res_d) if meta_res_d > 0 else 0
        st.markdown(f\"\"\"<div class="card-green">
        <b style='color:#1A1A2E;'>🛡️ Reserva de Emergência</b><br>
        <span style='font-size:13px;color:#555577;'>{fmt(st.session_state.reserva_emergencia)} de {fmt(meta_res_d)} ({st.session_state.config_meta_reserva} meses)</span>
        {barra(pct_res_d, "#10B981")}
        <span style='font-size:12px;color:#4B5563;'>{'✅ Completa!' if pct_res_d >= 100 else f'Faltam {fmt(max(0, meta_res_d - st.session_state.reserva_emergencia))}'}</span>
        </div>\"\"\", unsafe_allow_html=True)

        if st.session_state.metas:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("<b style='color:#1A1A2E;'>🎯 Metas em Andamento</b>", unsafe_allow_html=True)
            for m in st.session_state.metas[:4]:
                p_m   = pct(m.get("atual", 0), m["valor"])
                rest  = round((m["valor"] - m.get("atual", 0)) / m["mensal"]) if m["mensal"] > 0 else "∞"
                st.markdown(f\"\"\"
                <div style="margin-bottom:10px;">
                  <div style="display:flex;justify-content:space-between;">
                    <span style="font-size:13px;color:#1A1A2E;">{m['nome']}</span>
                    <span style="font-size:12px;color:#4B5563;">{p_m:.0f}% · {rest} meses</span>
                  </div>{barra(p_m, "#7C6FFF")}
                  <span style="font-size:11px;color:#4B5563;">{fmt(m.get('atual',0))} / {fmt(m['valor'])} · {fmt(m['mensal'])}/mês</span>
                </div>\"\"\", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        if st.session_state.dividas:
            total_div_d = sum(d["valor_total"] - d["valor_pago"] for d in st.session_state.dividas)
            st.markdown(f\"\"\"<div class="card-red">
            <b style='color:#1A1A2E;'>💳 Dívidas em Aberto</b><br>
            <span style='font-size:22px;font-weight:700;color:#991B1B;'>{fmt(total_div_d)}</span>
            <span style='font-size:12px;color:#4B5563;'> saldo total · {fmt(div_m)}/mês</span><br>
            <span style='font-size:12px;color:#4B5563;'>{len(st.session_state.dividas)} dívida(s) ativa(s)</span>
            </div>\"\"\", unsafe_allow_html=True)

        st.markdown('<div class="card-purple">', unsafe_allow_html=True)
        st.markdown("<b style='color:#1A1A2E;'>💡 Diagnóstico Automático</b>", unsafe_allow_html=True)
        dicas = []
        if renda > 0:
            if pct(gf, renda) > 50:    dicas.append(("⚠️", "Fixas acima de 50% da renda. Revise contratos e assinaturas.", "warn"))
            if pct(gv, renda) > 30:    dicas.append(("💸", "Variáveis acima de 30%. Identifique onde cortar.", "warn"))
            if pct(gm, renda) < 10:    dicas.append(("🎯", "Menos de 10% alocado em metas. Aumente gradualmente.", "info"))
            if pct_res_d < 100:        dicas.append(("🛡️", "Reserva incompleta. Priorize antes de investir.", "warn"))
            if st.session_state.dividas: dicas.append(("💳", "Quite dívidas com juros altos primeiro (estratégia avalanche).", "warn"))
            if saldo < 0:              dicas.append(("🚨", "DÉFICIT! Você gasta mais do que ganha. Corte imediato necessário.", "danger"))
            if saldo > renda * 0.3 and pct_res_d >= 100:
                                        dicas.append(("🚀", "Ótima saúde financeira! Hora de acelerar os investimentos.", "success"))
        if not dicas:
            dicas = [("ℹ️", "Preencha seus dados para receber o diagnóstico completo.", "info")]
        cls_map = {"warn":"alert-warn","info":"alert-info","danger":"alert-danger","success":"alert-success"}
        for ic, tx, tp in dicas:
            st.markdown(f'<div class="{cls_map[tp]}" style="margin-bottom:6px;">{ic} {tx}</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# 2. CONSULTOR IA
# ══════════════════════════════════════════════
with tab_ia:
    col_d, col_c = st.columns([1, 1.5])

    with col_d:
        st.markdown('<div class="card-purple">', unsafe_allow_html=True)
        st.markdown("<b style='color:#1A1A2E;'>🧬 Perfil de Decisão</b>", unsafe_allow_html=True)
        d1 = st.select_slider("Sem renda, sobreviveria:", ["< 1 mês","1-3 meses","3-6 meses","6-12 meses","1 ano+"], key="oraf1001")
        d2 = st.radio("Maior medo:", ["Perder o que tenho","Deixar de ganhar","Dívidas"], horizontal=True, key="oraculof2")
        d3 = st.radio("Objetivo:", ["Liberdade financeira","Estabilidade","Crescimento"], horizontal=True, key="oraculof3")
        d4 = st.radio("Tolerância ao risco:", ["Conservador","Moderado","Arrojado"], horizontal=True, key="oraculof4")
        if st.button("🔍 MAPEAR MEU PERFIL", key="oraculof5"):
            st.session_state.perfil_decisao = f"{d3} | Risco: {d4} | Reserva: {d1}"
            st.success(f"Perfil mapeado: {d3}, {d4}")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="card-gold">', unsafe_allow_html=True)
        st.markdown("<b style='color:#1A1A2E;'>📈 Simulador de Investimento</b>", unsafe_allow_html=True)
        v_inv   = st.number_input("Aporte mensal (R$):", value=500.0, min_value=0.0, step=50.0, key="oraculof6")
        t_inv   = st.slider("Prazo (anos):", 1, 40, 10, key="oraf1002")
        cap_ini = st.number_input("Capital inicial (R$):", value=0.0, min_value=0.0, step=100.0, key="oraculof7")
        taxa_a  = st.session_state.taxa_invest_anual
        taxa_m  = (1 + taxa_a / 100) ** (1/12) - 1
        if taxa_m > 0:
            montante = cap_ini*(1+taxa_m)**(t_inv*12) + v_inv*(((1+taxa_m)**(t_inv*12)-1)/taxa_m)
        else:
            montante = cap_ini + v_inv*t_inv*12
        investido = cap_ini + v_inv*t_inv*12
        lucro     = montante - investido
        st.markdown(f\"\"\"
        <div style="display:flex;gap:10px;margin:10px 0;">
          <div style="flex:1;background:#F0F0FA;border-radius:9px;padding:12px;text-align:center;">
            <div style="font-size:11px;color:#4B5563;">Montante Final</div>
            <div style="font-size:17px;font-weight:700;color:#065F46;">{fmt(montante)}</div>
          </div>
          <div style="flex:1;background:#F0F0FA;border-radius:9px;padding:12px;text-align:center;">
            <div style="font-size:11px;color:#4B5563;">Lucro</div>
            <div style="font-size:17px;font-weight:700;color:#6D28D9;">{fmt(lucro)}</div>
          </div>
        </div>
        <span style="font-size:11px;color:#4B5563;">Taxa: {taxa_a}% a.a. | Total investido: {fmt(investido)}</span>
        \"\"\", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<b style='color:#1A1A2E;font-size:13px;'>⚡ Perguntas Rápidas</b>", unsafe_allow_html=True)
        for q in [
            "Analise minha saúde financeira completa",
            "Como priorizar meus objetivos agora?",
            "Onde posso cortar gastos sem sofrimento?",
            "Quanto devo investir com meu saldo atual?",
            "Como quitar minhas dívidas mais rápido?",
        ]:
            if st.button(f"→ {q}", key=f"qr_{q[:18]}"):
                with st.spinner("Consultando o Oráculo..."):
                    resp = consultor(q, st.session_state.historico_chat)
                    if resp: st.session_state['res_bsc2_oraf1'] = str(resp)
                st.session_state.historico_chat.append({"role":"user","content":q})
                st.session_state.historico_chat.append({"role":"assistant","content":resp})
                st.rerun()

    with col_c:
        st.markdown("<b style='color:#1A1A2E;font-size:16px;'>💼 Mentor de Decisão</b>", unsafe_allow_html=True)
        if not st.session_state.historico_chat:
            st.markdown('<div class="alert-info" style="text-align:center;">💰 Faça sua primeira pergunta. O Oráculo conhece seus números e vai ser direto ao ponto.</div>', unsafe_allow_html=True)
        for msg in st.session_state.historico_chat:
            if msg["role"] == "user":
                st.markdown(f'<div class="chat-user"><span style="font-size:11px;color:#4B5563;">👤 {st.session_state.nome_user}</span><br><span style="color:#1A1A2E;">{msg["content"]}</span></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-ai"><span style="font-size:11px;color:#5B50E8;">💰 Oráculo</span><br><span style="color:#333355;">{msg["content"]}</span></div>', unsafe_allow_html=True)

        if p := st.chat_input("Qual é sua dúvida ou decisão financeira?", key="oraf1003"):
            with st.spinner("O Oráculo está analisando..."):
                resp = consultor(p, st.session_state.historico_chat)
                if resp: st.session_state['res_bsc2_oraf2'] = str(resp)
            st.session_state.historico_chat.append({"role":"user","content":p})
            st.session_state.historico_chat.append({"role":"assistant","content":resp})
            st.rerun()

        if st.session_state.historico_chat:
            if st.button("🗑️ Limpar conversa", key="oraculof8"):
                st.session_state.historico_chat = []
                st.rerun()

# ══════════════════════════════════════════════
# 3. RENDA
# ══════════════════════════════════════════════
with tab_renda:
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        st.markdown('<div class="card-green">', unsafe_allow_html=True)
        st.markdown("<b style='color:#1A1A2E;'>💵 Renda Principal</b>", unsafe_allow_html=True)
        with st.form("renda_principal"):
            nr = st.number_input("Salário / Renda Mensal (R$)", min_value=0.0, value=st.session_state.renda_total, step=100.0, key="oraculof9")
            if st.form_submit_button("💾 SALVAR", key="oraculoffsb502"):
                st.session_state.renda_total = nr
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<b style='color:#1A1A2E;'>➕ Outras Fontes de Renda</b>", unsafe_allow_html=True)
        with st.form("outras_rendas_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1: nr_nome = st.text_input("Fonte", placeholder="Freela, aluguel...", key="oraculof10")
            with c2: nr_val  = st.number_input("Valor (R$)", min_value=0.0, step=50.0, key="oraculof11")
            nr_rec = st.checkbox("Recorrente todo mês?", value=True, key="oraculof12")
            if st.form_submit_button("ADICIONAR", key="oraculoffsb503"):
                if nr_nome and nr_val > 0:
                    st.session_state.outras_rendas.append({"nome":nr_nome,"valor":nr_val,"recorrente":nr_rec})
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col_r2:
        total_r = st.session_state.renda_total + sum(x["valor"] for x in st.session_state.outras_rendas)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f"<b style='color:#1A1A2E;'>📋 Todas as Fontes — Total: {fmt(total_r)}/mês</b>", unsafe_allow_html=True)
        st.markdown(f'<div class="list-item"><span style="color:#1A1A2E;">💼 Salário principal</span><span style="color:#065F46;font-weight:600;">{fmt(st.session_state.renda_total)}</span></div>', unsafe_allow_html=True)
        for i, r in enumerate(st.session_state.outras_rendas):
            rec = "🔄" if r["recorrente"] else "1️⃣"
            col_rx, col_rd = st.columns([4, 1])
            with col_rx:
                st.markdown(f'<div class="list-item"><span style="color:#1A1A2E;">{rec} {r["nome"]}</span><span style="color:#065F46;">{fmt(r["valor"])}</span></div>', unsafe_allow_html=True)
            with col_rd:
                if st.button("✕", key=f"del_or_{i}"):
                    st.session_state.outras_rendas.pop(i); st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# 4. GASTOS VARIÁVEIS
# ══════════════════════════════════════════════
with tab_gastos:
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<b style='color:#1A1A2E;'>💸 Registrar Gasto</b>", unsafe_allow_html=True)
        with st.expander("⚙️ Gerenciar categorias"):
            nova_c = st.text_input("Nova categoria:", key="oraculof13")
            if st.button("Adicionar categoria", key="oraculof14"):
                if nova_c and nova_c not in st.session_state.categorias_gastos:
                    st.session_state.categorias_gastos.append(nova_c); st.rerun()
            cat_rem = st.selectbox("Remover categoria:", ["—"] + st.session_state.categorias_gastos, key="oraculof15")
            if st.button("Remover", key="oraculof16") and cat_rem != "—":
                st.session_state.categorias_gastos.remove(cat_rem); st.rerun()
        with st.form("gasto_form", clear_on_submit=True):
            g_cat  = st.selectbox("Categoria", st.session_state.categorias_gastos, key="oraculof17")
            g_desc = st.text_input("Descrição", placeholder="Ex: Supermercado extra", key="oraculof18")
            c1, c2 = st.columns(2)
            with c1: g_val  = st.number_input("Valor (R$)", min_value=0.0, step=10.0, key="oraculof19")
            with c2: g_data = st.date_input("Data", value=date.today())
            g_parc = st.checkbox("É parcelado?", key="oraculof20")
            g_np   = st.number_input("Nº parcelas", min_value=1, max_value=48, value=1, key="oraculof21") if g_parc else 1
            if st.form_submit_button("💾 REGISTRAR", key="oraculoffsb504"):
                if g_val > 0:
                    st.session_state.gastos.append({"tipo":g_cat,"descricao":g_desc,"valor":g_val,"data":str(g_data),"parcelado":g_parc,"parcelas":g_np})
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col_g2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f"<b style='color:#1A1A2E;'>📋 Gastos Registrados — Total: {fmt(gv)}</b>", unsafe_allow_html=True)
        if not st.session_state.gastos:
            st.markdown("<p>Nenhum gasto registrado ainda.</p>", unsafe_allow_html=True)
        else:
            cats_p  = list(set(g["tipo"] for g in st.session_state.gastos))
            filtro  = st.multiselect("Filtrar por categoria:", cats_p, default=cats_p, key="oraf1004")
            gastos_f = [g for g in st.session_state.gastos if g["tipo"] in filtro]
            for i, g in enumerate(gastos_f):
                parc_t = f" ({g['parcelas']}x)" if g.get("parcelado") else ""
                desc_t = f'<br><span style="font-size:11px;color:#4B5563;">{g["descricao"]}</span>' if g.get("descricao") else ""
                col_gi, col_gd = st.columns([5, 1])
                with col_gi:
                    st.markdown(f'<div class="list-item"><div><span style="color:#1A1A2E;">{g["tipo"]}{parc_t}</span>{desc_t}<br><span style="font-size:11px;color:#4B5563;">{g.get("data","")}</span></div><span style="color:#92400E;font-weight:600;">{fmt(g["valor"])}</span></div>', unsafe_allow_html=True)
                with col_gd:
                    idx = st.session_state.gastos.index(g)
                    if st.button("✕", key=f"del_g_{i}"):
                        st.session_state.gastos.pop(idx); st.rerun()
            if gastos_f:
                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown("<b style='color:#1A1A2E;font-size:13px;'>Por categoria:</b>", unsafe_allow_html=True)
                df_cat = pd.DataFrame(gastos_f).groupby("tipo")["valor"].sum().sort_values(ascending=False)
                for cat_n, val_c in df_cat.items():
                    p_c = pct(val_c, gv)
                    st.markdown(f\"\"\"
                    <div style="display:flex;justify-content:space-between;margin-bottom:3px;">
                      <span style="font-size:12px;color:#555577;">{cat_n}</span>
                      <span style="font-size:12px;color:#1A1A2E;">{fmt(val_c)} ({p_c}%)</span>
                    </div>{barra(p_c, "#FCD34D")}\"\"\", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# 5. METAS
# ══════════════════════════════════════════════
with tab_metas:
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.markdown('<div class="card-purple">', unsafe_allow_html=True)
        st.markdown("<b style='color:#1A1A2E;'>🎯 Criar Nova Meta</b>", unsafe_allow_html=True)
        with st.form("meta_form", clear_on_submit=True):
            m_nome  = st.text_input("Nome da meta", placeholder="Ex: Viagem Europa", key="oraculof22")
            m_cat   = st.selectbox("Categoria", ["Viagem","Carro","Casa","Educação","Investimento","Reserva","Emergência","Outro"], key="oraculof23")
            c1, c2  = st.columns(2)
            with c1: m_val   = st.number_input("Valor total (R$)", min_value=1.0, step=100.0, key="oraculof24")
            with c2: m_prazo = st.number_input("Prazo (meses)", min_value=1, max_value=360, value=12, key="oraculof25")
            m_atual = st.number_input("Já guardei (R$)", min_value=0.0, step=100.0, key="oraculof26")
            if st.form_submit_button("🚀 CRIAR META", key="oraculoffsb505"):
                if m_nome and m_val:
                    mensal = (m_val - m_atual) / m_prazo if m_prazo > 0 else m_val
                    st.session_state.metas.append({"nome":m_nome,"categoria":m_cat,"valor":m_val,"mensal":mensal,"prazo":m_prazo,"atual":m_atual,"criada":str(date.today())})
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col_m2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f"<b style='color:#1A1A2E;'>📋 Metas Ativas — {fmt(gm)}/mês alocados</b>", unsafe_allow_html=True)
        if not st.session_state.metas:
            st.markdown("<p>Nenhuma meta criada ainda.</p>", unsafe_allow_html=True)
        else:
            for i, m in enumerate(st.session_state.metas):
                p_m  = pct(m.get("atual", 0), m["valor"])
                rest = max(0, round((m["valor"]-m.get("atual",0))/m["mensal"])) if m["mensal"] > 0 else "∞"
                st.markdown(f\"\"\"<div class="card-purple" style="padding:12px;margin-bottom:8px;">
                <div style="display:flex;justify-content:space-between;">
                  <b style="color:#1A1A2E;">{m['nome']}</b>
                  <span class="badge-purple">{m.get('categoria','')}</span>
                </div>
                <span style="font-size:12px;color:#555577;">{fmt(m.get('atual',0))} / {fmt(m['valor'])} · {fmt(m['mensal'])}/mês · {rest} meses</span>
                {barra(p_m, "#7C6FFF")}
                <span style="font-size:11px;color:#5B50E8;">{p_m:.1f}% concluído</span>
                </div>\"\"\", unsafe_allow_html=True)
                _mk = f"meta_atual_{i}"
                if _mk not in st.session_state:
                    st.session_state[_mk] = float(m.get("atual", 0))
                col_mi, col_md = st.columns([4, 1])
                with col_mi:
                    st.number_input("Valor já guardado (R$):", min_value=0.0, max_value=float(m["valor"]), step=50.0, key=_mk)
                    if st.button("✅ Atualizar", key=f"upd_m_{i}"):
                        novo_a = st.session_state[_mk]
                        st.session_state.metas[i]["atual"]  = novo_a
                        st.session_state.metas[i]["mensal"] = (m["valor"]-novo_a)/m["prazo"] if m["prazo"] > 0 else 0
                        st.rerun()
                with col_md:
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("✕", key=f"del_m_{i}"):
                        if _mk in st.session_state: del st.session_state[_mk]
                        st.session_state.metas.pop(i); st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# 6. CONTAS FIXAS
# ══════════════════════════════════════════════
with tab_fixas:
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<b style='color:#1A1A2E;'>🛡️ Adicionar Conta Fixa</b>", unsafe_allow_html=True)
        with st.form("fixa_form", clear_on_submit=True):
            f_nome = st.text_input("Nome", placeholder="Ex: Aluguel, Netflix...", key="oraculof27")
            f_cat  = st.selectbox("Categoria", ["Moradia","Transporte","Alimentação","Saúde","Educação","Lazer","Serviços","Seguros","Outros"], key="oraculof28")
            c1, c2 = st.columns(2)
            with c1: f_val = st.number_input("Valor mensal (R$)", min_value=0.0, step=10.0, key="oraculof29")
            with c2: f_dia = st.number_input("Dia do vencimento", min_value=1, max_value=31, value=10, key="oraculof30")
            if st.form_submit_button("ADICIONAR", key="oraculoffsb506"):
                if f_nome and f_val > 0:
                    st.session_state.contas_fixas.append({"nome":f_nome,"valor":f_val,"dia_venc":f_dia,"categoria":f_cat,"ativa":True})
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col_f2:
        total_fixas_ativas = sum(x["valor"] for x in st.session_state.contas_fixas if x.get("ativa", True))
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f"<b style='color:#1A1A2E;'>🔒 Contas Fixas — {fmt(total_fixas_ativas)}/mês</b>", unsafe_allow_html=True)
        if not st.session_state.contas_fixas:
            st.markdown("<p>Nenhuma conta fixa cadastrada.</p>", unsafe_allow_html=True)
        else:
            fixas_ord = sorted(st.session_state.contas_fixas, key=lambda x: x.get("dia_venc", 99))
            for i, f in enumerate(fixas_ord):
                idx   = st.session_state.contas_fixas.index(f)
                ativa = f.get("ativa", True)
                col_fi, col_ft, col_fd = st.columns([4, 1, 1])
                with col_fi:
                    op = "1" if ativa else "0.4"
                    st.markdown(f'<div class="list-item" style="opacity:{op};"><div><span style="color:#1A1A2E;">{f["nome"]}</span><br><span style="font-size:11px;color:#4B5563;">Dia {f.get("dia_venc","?")} · {f.get("categoria","")}</span></div><span style="color:#0369A1;font-weight:600;">{fmt(f["valor"])}</span></div>', unsafe_allow_html=True)
                with col_ft:
                    if st.button("⏸" if ativa else "▶", key=f"tog_f_{i}"):
                        st.session_state.contas_fixas[idx]["ativa"] = not ativa; st.rerun()
                with col_fd:
                    if st.button("✕", key=f"del_f_{i}"):
                        st.session_state.contas_fixas.pop(idx); st.rerun()
            st.markdown("<hr>", unsafe_allow_html=True)
            cats_f = {}
            for f in st.session_state.contas_fixas:
                if f.get("ativa", True):
                    cats_f[f["categoria"]] = cats_f.get(f["categoria"], 0) + f["valor"]
            for cat_f, val_f in sorted(cats_f.items(), key=lambda x: -x[1]):
                p_f = pct(val_f, total_fixas_ativas)
                st.markdown(f\"\"\"
                <div style="display:flex;justify-content:space-between;margin-bottom:3px;">
                  <span style="font-size:12px;color:#555577;">{cat_f}</span>
                  <span style="font-size:12px;color:#1A1A2E;">{fmt(val_f)}</span>
                </div>{barra(p_f, "#38BDF8")}\"\"\", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# 7. DÍVIDAS
# ══════════════════════════════════════════════
with tab_div:
    st.markdown('<div class="alert-info">💡 <b>Avalanche:</b> quite a dívida de maior juros primeiro. <b>Bola de Neve:</b> quite a menor primeiro.</div>', unsafe_allow_html=True)
    col_dv1, col_dv2 = st.columns(2)
    with col_dv1:
        st.markdown('<div class="card-red">', unsafe_allow_html=True)
        st.markdown("<b style='color:#1A1A2E;'>💳 Cadastrar Dívida</b>", unsafe_allow_html=True)
        with st.form("div_form", clear_on_submit=True):
            d_nome    = st.text_input("Nome", placeholder="Ex: Cartão Nubank, Financiamento Carro", key="oraculof31")
            c1, c2    = st.columns(2)
            with c1: d_total   = st.number_input("Valor total da dívida (R$)", min_value=0.0, step=100.0, key="oraculof32")
            with c2: d_pago    = st.number_input("Já paguei (R$)", min_value=0.0, step=100.0, key="oraculof33")
            c3, c4    = st.columns(2)
            with c3: d_juros   = st.number_input("Juros ao mês (%)", min_value=0.0, max_value=100.0, step=0.1, key="oraculof34")
            with c4: d_parcela = st.number_input("Parcela mensal (R$)", min_value=0.0, step=50.0, key="oraculof35")
            if st.form_submit_button("REGISTRAR DÍVIDA", key="oraculoffsb507"):
                if d_nome and d_total > 0:
                    st.session_state.dividas.append({"nome":d_nome,"valor_total":d_total,"valor_pago":d_pago,"juros_mensal":d_juros,"parcela_mensal":d_parcela})
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col_dv2:
        total_div = sum(d["valor_total"] - d["valor_pago"] for d in st.session_state.dividas)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f"<b style='color:#1A1A2E;'>📋 Dívidas — Saldo Total: {fmt(total_div)}</b>", unsafe_allow_html=True)
        if not st.session_state.dividas:
            st.markdown('<div class="alert-success">✅ Nenhuma dívida cadastrada. Parabéns!</div>', unsafe_allow_html=True)
        else:
            dividas_ord = sorted(st.session_state.dividas, key=lambda x: -x["juros_mensal"])
            for i, d in enumerate(dividas_ord):
                saldo_d = d["valor_total"] - d["valor_pago"]
                p_d     = pct(d["valor_pago"], d["valor_total"])
                idx     = st.session_state.dividas.index(d)
                col_di, col_dd = st.columns([5, 1])
                with col_di:
                    st.markdown(f\"\"\"<div class="card-red" style="padding:12px;margin-bottom:8px;">
                    <div style="display:flex;justify-content:space-between;">
                      <b style="color:#1A1A2E;">{d['nome']}</b>
                      <span class="badge-red">{d['juros_mensal']}%/mês</span>
                    </div>
                    <span style="font-size:12px;color:#555577;">Saldo: {fmt(saldo_d)} · Parcela: {fmt(d['parcela_mensal'])}/mês</span>
                    {barra(p_d, "#B91C1C")}
                    <span style="font-size:11px;color:#991B1B;">{p_d:.1f}% quitado</span>
                    </div>\"\"\", unsafe_allow_html=True)
                    _dk = f"div_pago_{i}"
                    if _dk not in st.session_state:
                        st.session_state[_dk] = float(d["valor_pago"])
                    st.number_input("Valor já pago (R$):", min_value=0.0, max_value=float(d["valor_total"]), step=50.0, key=_dk)
                    if st.button("Atualizar pagamento", key=f"upd_d_{i}"):
                        novo_pago = st.session_state[_dk]
                        st.session_state.dividas[idx]["valor_pago"] = novo_pago
                        if novo_pago >= d["valor_total"]:
                            st.session_state.dividas.pop(idx)
                            st.success("🎉 Dívida quitada!")
                        st.rerun()
                with col_dd:
                    if st.button("✕", key=f"del_d_{i}"):
                        st.session_state.dividas.pop(idx); st.rerun()

            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown("<b style='color:#1A1A2E;font-size:13px;'>⏱️ Previsão de Quitação</b>", unsafe_allow_html=True)
            for d in dividas_ord:
                saldo_d = d["valor_total"] - d["valor_pago"]
                try:
                    if d["parcela_mensal"] > 0 and d["juros_mensal"] > 0:
                        taxa_md  = d["juros_mensal"] / 100
                        meses_d  = math.ceil(math.log(d["parcela_mensal"] / (d["parcela_mensal"] - saldo_d*taxa_md)) / math.log(1+taxa_md)) if d["parcela_mensal"] > saldo_d*taxa_md else 999
                    elif d["parcela_mensal"] > 0:
                        meses_d  = math.ceil(saldo_d / d["parcela_mensal"])
                    else:
                        meses_d  = 999
                except:
                    meses_d = 999
                txt_m = f"{meses_d} meses" if meses_d < 999 else "Revise a parcela"
                st.markdown(f'<div class="list-item"><span style="color:#1A1A2E;">{d["nome"]}</span><span style="color:#991B1B;">{txt_m}</span></div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# 8. RESERVA DE EMERGÊNCIA
# ══════════════════════════════════════════════
with tab_res:
    meta_res = gf * st.session_state.config_meta_reserva
    pct_res  = pct(st.session_state.reserva_emergencia, meta_res) if meta_res > 0 else 0
    falta_res = max(0, meta_res - st.session_state.reserva_emergencia)
    col_rv1, col_rv2 = st.columns(2)

    with col_rv1:
        st.markdown('<div class="card-green">', unsafe_allow_html=True)
        st.markdown("<b style='color:#1A1A2E;'>🛡️ Reserva de Emergência</b>", unsafe_allow_html=True)
        st.markdown(f"<p>Ideal: <b style='color:#065F46;'>{st.session_state.config_meta_reserva} meses</b> de despesas fixas = <b style='color:#065F46;'>{fmt(meta_res)}</b></p>", unsafe_allow_html=True)
        with st.form("reserva_form"):
            novo_res = st.number_input("Valor atual da sua reserva (R$)", min_value=0.0, value=st.session_state.reserva_emergencia, step=100.0, key="oraculof36")
            if st.form_submit_button("💾 SALVAR", key="oraculoffsb508"):
                st.session_state.reserva_emergencia = novo_res; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<b style='color:#1A1A2E;'>🏦 Onde Guardar a Reserva</b>", unsafe_allow_html=True)
        for nm_r, desc_r, st_r, cor_r in [
            ("Tesouro Selic",     "Seguro, liquidez diária, rende ~CDI",   "✅ Ideal",   "#6EE7B7"),
            ("CDB 100%+ CDI",     "Bancos digitais, FGC até R$250k",       "✅ Ótimo",   "#6EE7B7"),
            ("Conta Remunerada",  "Nubank, Inter — resgate imediato",      "✅ Prático", "#6EE7B7"),
            ("Poupança",          "Rende menos que a inflação",            "⚠️ Evite",   "#FCD34D"),
            ("Debaixo do colchão","Zero rendimento, risco físico",         "❌ Não",     "#FCA5A5"),
        ]:
            st.markdown(f'<div class="list-item"><div><span style="color:#1A1A2E;">{nm_r}</span><br><span style="font-size:11px;color:#4B5563;">{desc_r}</span></div><span style="color:{cor_r};font-size:12px;">{st_r}</span></div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_rv2:
        cor_rv = "#6EE7B7" if pct_res >= 100 else "#FCA5A5"
        st.markdown(f\"\"\"<div class="card">
        <div style="text-align:center;margin-bottom:16px;">
          <div style="font-size:34px;font-weight:700;color:{cor_rv};">{fmt(st.session_state.reserva_emergencia)}</div>
          <div style="font-size:13px;color:#4B5563;">de {fmt(meta_res)}</div>
        </div>
        {barra(pct_res, "#10B981")}
        <div style="display:flex;gap:10px;margin:16px 0;">
          <div style="flex:1;background:#F0F0FA;border-radius:9px;padding:10px;text-align:center;">
            <div style="font-size:11px;color:#4B5563;">Meses cobertos</div>
            <div style="font-size:20px;font-weight:700;color:#10B981;">{round(st.session_state.reserva_emergencia/gf, 1) if gf > 0 else "∞"}</div>
          </div>
          <div style="flex:1;background:#F0F0FA;border-radius:9px;padding:10px;text-align:center;">
            <div style="font-size:11px;color:#4B5563;">Meta (meses)</div>
            <div style="font-size:20px;font-weight:700;color:#1A1A2E;">{st.session_state.config_meta_reserva}</div>
          </div>
          <div style="flex:1;background:#F0F0FA;border-radius:9px;padding:10px;text-align:center;">
            <div style="font-size:11px;color:#4B5563;">Concluído</div>
            <div style="font-size:20px;font-weight:700;color:#5B50E8;">{min(100, pct_res):.0f}%</div>
          </div>
        </div>
        </div>\"\"\", unsafe_allow_html=True)
        if pct_res >= 100:
            st.markdown('<div class="alert-success">✅ Reserva completa! Use o excedente para investimentos.</div>', unsafe_allow_html=True)
        else:
            m_comp = math.ceil(falta_res / max(1, saldo)) if saldo > 0 else "∞"
            st.markdown(f'<div class="alert-warn">⚠️ Faltam {fmt(falta_res)}. Com seu saldo atual, ~{m_comp} meses para completar.</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════
# 9. INVESTIMENTOS
# ══════════════════════════════════════════════
with tab_inv:
    st.markdown('<div class="card-gold">', unsafe_allow_html=True)
    st.markdown("<b style='color:#1A1A2E;'>📈 Planejamento de Investimentos</b>", unsafe_allow_html=True)
    ci1, ci2, ci3 = st.columns(3)
    with ci1:
        taxa_a_inv = st.number_input("Taxa anual esperada (%)", min_value=1.0, max_value=30.0, value=st.session_state.taxa_invest_anual, step=0.5, key="oraculof37")
        st.session_state.taxa_invest_anual = taxa_a_inv
    with ci2:
        if "inv_aporte_mensal" not in st.session_state:
            st.session_state["inv_aporte_mensal"] = float(st.session_state.aporte_inv_salvo)
        aporte_inv = st.number_input("Aporte mensal (R$)", min_value=0.0, step=50.0, key="inv_aporte_mensal")
        st.session_state.aporte_inv_salvo = aporte_inv
    with ci3:
        if "inv_capital_ini" not in st.session_state:
            st.session_state["inv_capital_ini"] = float(st.session_state.cap_ini_inv_salvo)
        cap_ini_inv = st.number_input("Capital inicial (R$)", min_value=0.0, step=500.0, key="inv_capital_ini")
        st.session_state.cap_ini_inv_salvo = cap_ini_inv
    st.markdown("</div>", unsafe_allow_html=True)

    taxa_m_inv = (1 + taxa_a_inv/100)**(1/12) - 1
    st.markdown("<br><b style='color:#1A1A2E;'>🗓️ Projeções de Crescimento</b>", unsafe_allow_html=True)
    prazos_inv = [1, 2, 5, 10, 20, 30]
    cols_inv   = st.columns(len(prazos_inv))
    dados_proj = []
    for i, anos in enumerate(prazos_inv):
        n = anos * 12
        if taxa_m_inv > 0:
            mont = cap_ini_inv*(1+taxa_m_inv)**n + aporte_inv*(((1+taxa_m_inv)**n-1)/taxa_m_inv)
        else:
            mont = cap_ini_inv + aporte_inv*n
        inv_t  = cap_ini_inv + aporte_inv*n
        lucro_i = mont - inv_t
        dados_proj.append((anos, mont, lucro_i))
        with cols_inv[i]:
            st.markdown(f\"\"\"<div class="card-gold" style="text-align:center;padding:12px;">
            <div style="font-size:13px;color:#92400E;font-weight:600;">{anos} ano{'s' if anos>1 else ''}</div>
            <div style="font-size:15px;font-weight:700;color:#1A1A2E;margin:4px 0;">{fmt(mont)}</div>
            <div style="font-size:11px;color:#4B5563;">+{fmt(lucro_i)}</div>
            </div>\"\"\", unsafe_allow_html=True)

    col_inv_a, col_inv_b = st.columns(2)

    with col_inv_a:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<b style='color:#1A1A2E;'>📊 Crescimento Visual</b>", unsafe_allow_html=True)
        max_m = max(d[1] for d in dados_proj) if dados_proj else 1
        for anos, mont, lucro_i in dados_proj:
            p_i = pct(mont, max_m)
            st.markdown(f\"\"\"
            <div style="display:flex;justify-content:space-between;margin-bottom:3px;">
              <span style="font-size:12px;color:#555577;">{anos} ano{'s' if anos>1 else ''}</span>
              <span style="font-size:12px;color:#1A1A2E;">{fmt(mont)}</span>
            </div>{barra(p_i, "#10B981")}\"\"\", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_inv_b:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<b style='color:#1A1A2E;'>🎓 Onde Investir — Por Perfil</b>", unsafe_allow_html=True)
        perfil_inv = st.radio("Perfil de risco:", ["Conservador","Moderado","Arrojado"], horizontal=True, key="oraculof40")
        inv_map = {
            "Conservador": [
                ("Tesouro Selic",    "Liquidez diária, ~CDI",               "✅"),
                ("CDB 100%+ CDI",    "FGC até R$250k, bancos digitais",     "✅"),
                ("LCI / LCA",        "Isento de IR, ótimo custo-benefício", "✅"),
                ("Fundo DI",         "Gestão profissional, renda fixa",     "✅"),
            ],
            "Moderado": [
                ("Tesouro IPCA+",    "Protege da inflação, longo prazo",    "📈"),
                ("Fundos Multimercado","Mix renda fixa + variável",         "📈"),
                ("FIIs",             "Renda passiva mensal em imóveis",     "📈"),
                ("ETF Renda Fixa",   "Diversificação automática",           "📈"),
            ],
            "Arrojado": [
                ("Ações (Buy&Hold)", "Empresas sólidas, foco longo prazo",  "🚀"),
                ("ETFs de Ações",    "BOVA11, IVVB11 (S&P 500 em R$)",     "🚀"),
                ("FIIs + Ações",     "Renda passiva + crescimento",         "🚀"),
                ("BDRs",             "Empresas internacionais em R$",       "🚀"),
            ]
        }
        for nm_i, desc_i, st_i in inv_map[perfil_inv]:
            st.markdown(f'<div class="list-item"><div><b style="color:#1A1A2E;">{nm_i}</b><br><span style="font-size:11px;color:#4B5563;">{desc_i}</span></div><span style="color:#065F46;">{st_i}</span></div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# 10. PATRIMÔNIO
# ══════════════════════════════════════════════
with tab_pat:
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<b style='color:#1A1A2E;'>📦 Registrar Item Patrimonial</b>", unsafe_allow_html=True)
        with st.form("patr_form", clear_on_submit=True):
            p_nome = st.text_input("Nome", placeholder="Apartamento, Carro, FGTS...", key="oraculof41")
            p_tipo = st.radio("Tipo:", ["Ativo (tenho)","Passivo (devo)"], horizontal=True, key="oraculof42")
            p_cat  = st.selectbox("Categoria", ["Imóveis","Veículos","Investimentos","Poupança","FGTS","Dívidas","Outros"], key="oraculof43")
            p_val  = st.number_input("Valor (R$)", min_value=0.0, step=1000.0, key="oraculof44")
            if st.form_submit_button("ADICIONAR", key="oraculoffsb509"):
                if p_nome and p_val > 0:
                    st.session_state.patrimonio_itens.append({"nome":p_nome,"valor":p_val,"tipo":p_tipo,"categoria":p_cat})
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col_p2:
        ativos   = [x for x in st.session_state.patrimonio_itens if "Ativo"   in x["tipo"]]
        passivos = [x for x in st.session_state.patrimonio_itens if "Passivo" in x["tipo"]]
        total_a  = sum(x["valor"] for x in ativos)
        total_p  = sum(x["valor"] for x in passivos)
        pat_liq  = total_a - total_p
        cor_pl   = "#6EE7B7" if pat_liq >= 0 else "#FCA5A5"

        st.markdown(f\"\"\"<div class="card">
        <b style='color:#1A1A2E;'>⚖️ Balanço Patrimonial</b>
        <div style="display:flex;gap:10px;margin:14px 0;">
          <div style="flex:1;background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.2);border-radius:9px;padding:12px;text-align:center;">
            <div style="font-size:11px;color:#4B5563;">Ativos</div>
            <div style="font-size:18px;font-weight:700;color:#065F46;">{fmt(total_a)}</div>
          </div>
          <div style="flex:1;background:rgba(239,68,68,0.1);border:1px solid rgba(239,68,68,0.2);border-radius:9px;padding:12px;text-align:center;">
            <div style="font-size:11px;color:#4B5563;">Passivos</div>
            <div style="font-size:18px;font-weight:700;color:#991B1B;">{fmt(total_p)}</div>
          </div>
          <div style="flex:1;background:#F0F0FA;border-radius:9px;padding:12px;text-align:center;">
            <div style="font-size:11px;color:#4B5563;">Patrimônio Líquido</div>
            <div style="font-size:18px;font-weight:700;color:{cor_pl};">{fmt(pat_liq)}</div>
          </div>
        </div>\"\"\", unsafe_allow_html=True)
        for rotulo_p, lista_p, cor_p in [("✅ Ativos", ativos, "#6EE7B7"), ("❌ Passivos", passivos, "#FCA5A5")]:
            if lista_p:
                st.markdown(f"<b style='color:#1A1A2E;font-size:13px;'>{rotulo_p}:</b>", unsafe_allow_html=True)
                for i, item in enumerate(lista_p):
                    idx = st.session_state.patrimonio_itens.index(item)
                    col_pi, col_pd = st.columns([5, 1])
                    with col_pi:
                        st.markdown(f'<div class="list-item"><span style="color:#1A1A2E;">{item["nome"]} <span style="color:#4B5563;font-size:11px;">({item["categoria"]})</span></span><span style="color:{cor_p};font-weight:600;">{fmt(item["valor"])}</span></div>', unsafe_allow_html=True)
                    with col_pd:
                        if st.button("✕", key=f"del_pat_{rotulo_p}_{i}"):
                            st.session_state.patrimonio_itens.pop(idx); st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# 11. RELATÓRIO
# ══════════════════════════════════════════════
with tab_rel:
    st.markdown("<b style='color:#1A1A2E;font-size:18px;'>📊 Relatório Financeiro Completo</b>", unsafe_allow_html=True)
    col_rl1, col_rl2 = st.columns(2)

    with col_rl1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<b style='color:#1A1A2E;'>📋 Resumo Executivo</b>", unsafe_allow_html=True)
        total_div_r = sum(d["valor_total"]-d["valor_pago"] for d in st.session_state.dividas)
        pat_liq_r   = sum(x["valor"] for x in st.session_state.patrimonio_itens if "Ativo" in x["tipo"]) - sum(x["valor"] for x in st.session_state.patrimonio_itens if "Passivo" in x["tipo"])
        for lbl, val_r, cor_r in [
            ("💰 Renda Total",           fmt(renda),                                  "#6EE7B7"),
            ("🛡️ Despesas Fixas",         fmt(gf),                                     "#7DD3FC"),
            ("💸 Gastos Variáveis",       fmt(gv),                                     "#FCD34D"),
            ("💳 Parcelas de Dívidas",    fmt(div_m),                                  "#FCA5A5"),
            ("🚀 Alocação em Metas",      fmt(gm),                                     "#6D28D9"),
            ("⚖️ Saldo Livre",            fmt(saldo),                                  "#6EE7B7" if saldo>=0 else "#FCA5A5"),
            ("🛡️ Reserva de Emergência",  fmt(st.session_state.reserva_emergencia),    "#6EE7B7"),
            ("💳 Total de Dívidas",       fmt(total_div_r),                            "#FCA5A5"),
            ("⚖️ Patrimônio Líquido",     fmt(pat_liq_r),                              "#FCD34D"),
            ("📊 % Renda Comprometida",   f"{pct(gf+gv+gm+div_m, renda):.1f}%",      "#A0A0C0"),
        ]:
            st.markdown(f'<div class="list-item"><span style="color:#555577;">{lbl}</span><span style="color:{cor_r};font-weight:600;">{val_r}</span></div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_rl2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<b style='color:#1A1A2E;'>💹 Fluxo de Caixa</b>", unsafe_allow_html=True)
        if renda > 0:
            for nome_f, val_f, cor_f in [
                ("💰 Renda",          renda,           "#6EE7B7"),
                ("🛡️ Fixas",          gf,              "#38BDF8"),
                ("💸 Variáveis",      gv,              "#FCD34D"),
                ("💳 Dívidas",        div_m,           "#FCA5A5"),
                ("🚀 Metas",          gm,              "#6D28D9"),
                ("✅ Saldo Livre",    max(0, saldo),   "#6EE7B7"),
            ]:
                pct_f = pct(val_f, renda)
                st.markdown(f\"\"\"
                <div style="display:flex;justify-content:space-between;margin-bottom:3px;">
                  <span style="font-size:13px;color:#555577;">{nome_f}</span>
                  <span style="font-size:13px;color:#1A1A2E;">{fmt(val_f)} <span style="color:#4B5563;">({pct_f}%)</span></span>
                </div>{barra(pct_f, cor_f)}\"\"\", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        if st.session_state.gastos:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("<b style='color:#1A1A2E;'>💸 Gastos por Categoria</b>", unsafe_allow_html=True)
            df_rel = pd.DataFrame(st.session_state.gastos).groupby("tipo")["valor"].sum().sort_values(ascending=False)
            st.bar_chart(df_rel)
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<b style='color:#1A1A2E;'>💾 Exportar Dados</b>", unsafe_allow_html=True)
    col_exp1, col_exp2 = st.columns(2)
    with col_exp1:
        st.download_button(
            "💾 SALVAR MEUS DADOS (.json)",
            data=gerar_json_sessao(),
            file_name=f"oraculo_{st.session_state.nome_user.lower().replace(' ','_')}_{date.today()}.json",
            mime="application/json",
            use_container_width=True,
        
        key="oraf3002",
    )
    with col_exp2:
        dados_exp = {
            "usuario": st.session_state.nome_user,
            "exportado_em": str(datetime.now()),
            "renda": renda, "gastos": st.session_state.gastos,
            "contas_fixas": st.session_state.contas_fixas,
            "metas": st.session_state.metas, "dividas": st.session_state.dividas,
            "reserva": st.session_state.reserva_emergencia,
            "patrimonio": st.session_state.patrimonio_itens,
        }
        st.download_button(
            "📥 Exportar relatório (.json)",
            data=json.dumps(dados_exp, indent=2, ensure_ascii=False, default=str),
            file_name=f"relatorio_{st.session_state.nome_user}_{date.today()}.json",
            mime="application/json",
            use_container_width=True,
        
        key="oraf3003",
    )

# ══════════════════════════════════════════════
# 12. CONFIGURAÇÕES
# ══════════════════════════════════════════════
with tab_cfg:
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<b style='color:#1A1A2E;'>⚙️ Configurações do Sistema</b>", unsafe_allow_html=True)
        meses_cfg = st.slider("Meta de reserva (meses de despesas fixas):", 1, 12, st.session_state.config_meta_reserva, key="oraf1005")
        st.session_state.config_meta_reserva = meses_cfg
        taxa_cfg  = st.number_input("Taxa de retorno padrão para simulações (% a.a.):", min_value=1.0, max_value=30.0, value=st.session_state.taxa_invest_anual, step=0.5, key="oraculof45")
        st.session_state.taxa_invest_anual = taxa_cfg
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<b style='color:#1A1A2E;'>ℹ️ Sobre o Oráculo</b>", unsafe_allow_html=True)
        st.markdown(\"\"\"
        <p style="font-size:13px;line-height:1.7;">
        O <b style="color:#1A1A2E;">Oráculo Financeiro</b> é um sistema pessoal de organização e educação financeira.
        </p>
        <p style="font-size:12px;color:#4B5563;">⚠️ Este sistema não é um serviço regulamentado. As análises são educativas e não substituem um consultor financeiro certificado (CFP/CEA).</p>
        \"\"\", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_c2:
        st.markdown('<div class="card-red">', unsafe_allow_html=True)
        st.markdown("<b style='color:#1A1A2E;'>🗑️ Zona de Perigo</b>", unsafe_allow_html=True)
        st.markdown("<p>Apaga permanentemente todos os dados inseridos nesta sessão.</p>", unsafe_allow_html=True)
        confirmar = st.checkbox("Confirmo que quero apagar tudo", key="oraculof46")
        if confirmar:
            if st.button("🗑️ APAGAR TODOS OS DADOS", key="oraculof47"):
                for k in ["gastos","metas","contas_fixas","outras_rendas","patrimonio_itens","historico_chat","dividas"]:
                    st.session_state[k] = []
                st.session_state.renda_total        = 0.0
                st.session_state.reserva_emergencia = 0.0
                st.success("Dados apagados com sucesso.")
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# --- RODAPÉ ---
st.markdown(
    "<div style='text-align:center;color:#999;font-size:0.8em;margin-top:60px;padding-bottom:20px;'>"
    "© 2026 Oráculo Financeiro IA — Gestão Financeira Inteligente · MeusAgentesIA.com.br"
    "</div>", unsafe_allow_html=True
)
""",
    "conexao_magnetica": """# [hub] import streamlit as st
# [hub] from groq import Groq
# [hub] from datetime import datetime, date
# [hub] import json
import random

# set_page_config removido pelo super_agente

st.markdown(\"\"\"
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
[data-testid="stToolbar"] {visibility: hidden;}
[data-testid="stDecoration"] {visibility: hidden;}
[data-testid="stStatusWidget"] {visibility: hidden;}
</style>
\"\"\", unsafe_allow_html=True)


st.markdown(\"\"\"
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    .stApp { background-color:#F8F9FA; font-family:'Inter',sans-serif; }
    [data-testid="stSidebar"] { display:none; }

    .stTextInput>div>div>input, .stTextArea>div>textarea,
    .stSelectbox>div>div>div, .stNumberInput>div>div>input {
        background-color:#FFFFFF !important; color:#1A1A2E !important;
        border:1px solid #CED4DA !important; font-family:'Inter',sans-serif !important;
    }

    .stButton>button {
        width:100%; border-radius:10px; height:3.2em;
        background:linear-gradient(135deg,#495057,#343A40) !important; color:white !important;
        font-weight:600; border:none; box-shadow:2px 2px 8px rgba(0,0,0,0.1);
        font-family:'Inter',sans-serif !important; transition:all 0.2s ease;
    }
    .stButton>button:hover { background:linear-gradient(135deg,#343A40,#212529) !important; transform:translateY(-1px); }
    .stApp .stButton>button, .stApp .stButton>button p,
    .stApp .stButton>button span, .stApp .stButton>button div { color:white !important; }

    .stApp h1, .stApp h2, .stApp h3 { color:#1A1A2E !important; font-family:'Inter',sans-serif !important; font-weight:700 !important; }

    .card { background:linear-gradient(135deg,#F1F3F5,#E9ECEF); padding:20px; border-radius:14px; border:1px solid #CED4DA; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card, .stApp .card p, .stApp .card span, .stApp .card div, .stApp .card strong, .stApp .card em { color:#1A1A2E !important; }

    .card-dark { background:linear-gradient(135deg,#E9ECEF,#DEE2E6); padding:20px; border-radius:14px; border:1px solid #ADB5BD; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-dark, .stApp .card-dark p, .stApp .card-dark span, .stApp .card-dark div, .stApp .card-dark strong { color:#1A1A2E !important; }

    .card-green { background:linear-gradient(135deg,#F0FDF4,#DCFCE7); padding:20px; border-radius:14px; border:1px solid #86EFAC; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-green, .stApp .card-green p, .stApp .card-green span, .stApp .card-green div { color:#14532D !important; }

    .card-blue { background:linear-gradient(135deg,#EFF6FF,#DBEAFE); padding:20px; border-radius:14px; border:1px solid #93C5FD; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-blue, .stApp .card-blue p, .stApp .card-blue span, .stApp .card-blue div { color:#1E3A8A !important; }

    .card-red { background:linear-gradient(135deg,#FFF5F5,#FEE2E2); padding:20px; border-radius:14px; border:1px solid #FECACA; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-red, .stApp .card-red p, .stApp .card-red span, .stApp .card-red div { color:#7F1D1D !important; }

    .card-yellow { background:linear-gradient(135deg,#FFFBEB,#FEF3C7); padding:18px; border-radius:12px; border:1px solid #FCD34D; margin-bottom:12px; white-space:normal; word-wrap:break-word; }
    .stApp .card-yellow, .stApp .card-yellow p, .stApp .card-yellow span, .stApp .card-yellow div { color:#78350F !important; }

    .stat-box { background:#FFFFFF; border-radius:12px; padding:16px; text-align:center; border:1px solid #CED4DA; }
    .stApp .stat-box div, .stApp .stat-box span, .stApp .stat-box p { color:#1A1A2E !important; }
    .stApp .stat-numero, .stat-numero { font-size:2em; font-weight:700; color:#495057 !important; }

    .hist-item { background:#FFFFFF; border-radius:10px; padding:12px 16px; margin-bottom:8px; border-left:4px solid #CED4DA; }
    .stApp .hist-item, .stApp .hist-item p, .stApp .hist-item span, .stApp .hist-item div, .stApp .hist-item small { color:#1A1A2E !important; }

    .badge { background:#495057; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-verde { background:#059669; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-amarelo { background:#B45309; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-azul { background:#1D4ED8; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-roxo { background:#6D28D9; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }

    .divider { border:none; height:1px; background:linear-gradient(to right,transparent,#CED4DA,transparent); margin:18px 0; }

    .chat-user { background:#FFFFFF; border:1px solid #CED4DA; border-radius:12px 12px 4px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-user, .stApp .chat-user p, .stApp .chat-user span, .stApp .chat-user div { color:#1A1A2E !important; }

    .chat-persona { background:#F8F9FA; border:1px solid #CED4DA; border-radius:4px 12px 12px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-persona, .stApp .chat-persona p, .stApp .chat-persona span, .stApp .chat-persona div { color:#1A1A2E !important; }

    .questao-box { background:#FFFFFF; border:2px solid #CED4DA; border-radius:12px; padding:18px; margin-bottom:14px; }
    .stApp .questao-box, .stApp .questao-box p, .stApp .questao-box span, .stApp .questao-box div { color:#1A1A2E !important; }

    .avaliacao-box { background:#FFFFFF; border:2px solid #CED4DA; border-radius:14px; padding:18px; margin-bottom:12px; }
    .stApp .avaliacao-box, .stApp .avaliacao-box p, .stApp .avaliacao-box span, .stApp .avaliacao-box div { color:#1A1A2E !important; }

    .meta-box { background:#FFFFFF; border:2px solid #CED4DA; border-radius:12px; padding:16px; text-align:center; margin:10px 0; }
    .stApp .meta-box, .stApp .meta-box div, .stApp .meta-box span { color:#1A1A2E !important; }
    .stApp .meta-numero { font-size:2em; font-weight:700; color:#495057 !important; }

    .chat-scroll-container { max-height:40vh; overflow-y:auto; display:flex; flex-direction:column; scroll-behavior:smooth; padding-bottom:4px; }
    .chat-scroll-container > * { flex-shrink:0; }
    

    </style>
\"\"\", unsafe_allow_html=True)

# ─── CACHE ───
@st.cache_resource
def get_cache():
    return {"perfis": {}}
_cache = get_cache()

# ─── FAIXAS DA ARTE DA LÁBIA ───
FAIXAS = [
    (1, "⚪ Faixa Branca",  "🌱 O Invisível",    "Recebe ajuda direta. Personagem facilitador."),
    (2, "🟡 Faixa Amarela", "🟢 O Quebra-Gelo",  "Aprende a captar ganchos. Ajuda reduzida."),
    (3, "🟠 Faixa Laranja", "🟡 O Interessante", "Lida com silêncio e improvisação. Sem ajuda direta."),
    (4, "🟢 Faixa Verde",   "🟠 O Inabalável",   "Provocações e pressão social."),
    (5, "🔵 Faixa Azul",    "🔴 O Desafiador",   "Respostas frias e pouca reciprocidade."),
    (6, "🟤 Faixa Marrom",  "⚫ O Sedutor",       "Oscilação e imprevisibilidade."),
    (7, "⚫ Faixa Preta",   "👑 Don Juan",        "Conversa livre. Zero rede de proteção."),
]

CONQUISTAS_DEF = [
    ("primeira_analise",   "🔍 Primeira Análise",        "Realizou sua primeira análise de conversa"),
    ("primeiro_treino",    "🎭 Primeiro Treino",          "Completou o primeiro roleplay"),
    ("cinco_analises",     "📊 5 Conversas",              "5 conversas analisadas"),
    ("dez_mensagens",      "✨ 10 Mensagens",             "10 mensagens aprimoradas"),
    ("primeira_carta",     "🃏 Primeira Carta",           "Usou a Carta na Manga pela primeira vez"),
    ("cinco_cartas",       "🎴 5 Cartas",                 "5 Cartas na Manga utilizadas"),
    ("plano_7dias",        "🗓️ Plano 7 Dias",            "Concluiu o plano de 7 dias"),
    ("primeiro_passo",     "🌱 Primeiro Passo",           "Concluiu a primeira conversa na Arte da Lábia"),
    ("cacador_ganchos",    "🧩 Caçador de Ganchos",      "Aproveitou 10 ganchos em conversas"),
    ("resposta_relampago", "⚡ Resposta Relâmpago",       "Respondeu 10 situações dentro do tempo"),
    ("sem_roteiro",        "🧠 Sem Roteiro",              "Completou uma conversa sem ajuda"),
    ("inabalavel",         "🛡️ Inabalável",              "Superou 5 provocações com naturalidade"),
    ("resgatador",         "🔥 Resgatador",               "Recuperou 5 conversas esfriando"),
    ("camaleao",           "🦎 Camaleão",                 "Adaptou-se a 10 personalidades diferentes"),
    ("don_juan",           "👑 Don Juan",                 "Concluiu o Nível 7 — Don Juan"),
]

CHAVES_SALVAR = [
    'usuario', 'historico', 'biblioteca', 'resumo_semanal',
    'plano_conquista', 'plano_pessoa',
    'conversas_analisadas', 'mensagens_aprimoradas', 'analises_realizadas',
    'cartas_usadas', 'treinos_realizados', 'favoritos_total',
    'clareza', 'naturalidade', 'reciprocidade', 'confianca', 'escuta',
    'conquistas', 'faixa_atual', 'historico_personagens',
    'labia_nivel', 'labia_chat', 'labia_personagem', 'labia_falha_anterior',
    'objetivos_usuario',
]

def gerar_json():
    dados = {k: st.session_state.get(k) for k in CHAVES_SALVAR}
    dados['salvo_em'] = datetime.now().strftime('%d/%m/%Y %H:%M')
    return json.dumps(dados, ensure_ascii=False, indent=2, default=str)

def carregar_json(dados):
    for k in CHAVES_SALVAR:
        if k in dados:
            st.session_state[k] = dados[k]

def salvar_cache(u):
    _cache["perfis"][u] = {k: st.session_state.get(k) for k in CHAVES_SALVAR}

def perfis_salvos():
    return list(_cache["perfis"].keys())

def carregar_cache(u):
    return _cache["perfis"].get(u)

def salvar_historico(tipo, tema, conteudo):
    st.session_state.historico.append({
        'data': datetime.now().strftime('%d/%m %H:%M'),
        'tipo': tipo, 'tema': tema, 'conteudo': conteudo,
    })

def verificar_conquistas():
    c = st.session_state.get('conquistas', [])
    novas = []
    checks = [
        ("primeira_analise",   st.session_state.analises_realizadas >= 1),
        ("primeiro_treino",    st.session_state.treinos_realizados >= 1),
        ("cinco_analises",     st.session_state.conversas_analisadas >= 5),
        ("dez_mensagens",      st.session_state.mensagens_aprimoradas >= 10),
        ("primeira_carta",     st.session_state.cartas_usadas >= 1),
        ("cinco_cartas",       st.session_state.cartas_usadas >= 5),
    ]
    for chave, cond in checks:
        if cond and chave not in c:
            c.append(chave); novas.append(chave)
    st.session_state['conquistas'] = c
    return novas

defaults = {
    'etapa': 'Login', 'usuario': '', 'api_key': '', 'pagina': 'Home',
    'historico': [], 'biblioteca': [], 'resumo_semanal': '',
    'plano_conquista': '', 'plano_pessoa': '',
    'conversas_analisadas': 0, 'mensagens_aprimoradas': 0,
    'analises_realizadas': 0, 'cartas_usadas': 0,
    'treinos_realizados': 0, 'favoritos_total': 0,
    'clareza': 0, 'naturalidade': 0, 'reciprocidade': 0,
    'confianca': 0, 'escuta': 0,
    'conquistas': [], 'faixa_atual': 1,
    'historico_personagens': [],
    'labia_nivel': 1, 'labia_chat': [], 'labia_personagem': None,
    'labia_falha_anterior': None, 'objetivos_usuario': [],
    'labia_inicio': 0, 'labia_duracao': 180, 'labia_encerrado': False,
    # Mestre da Lábia
    'lj_fase': 1, 'lj_personagem_sel': 'Rafaela',
    'lj_ativo': False, 'lj_chat': [], 'lj_conexo': 100,
    'lj_atributos': {'interesse':50,'atracao':50,'conexao':50,'confianca':50,'naturalidade':50,'curiosidade':50,'tensao':20},
    'lj_inicio': 0, 'lj_duracao': 300,
    'lj_missao': '', 'lj_missao_cumprida': False,
    'lj_aval': None, 'lj_arranques': [],
    'lj_historico_cenarios': [], 'lj_historico_aberturas': [],
    'lj_ts_persona': 0, 'lj_ts_usuario': 0, 'lj_silencio_total': 0,
    'lj_combo': 0,
    'lj_fases_concluidas': 0,
    'lj_titulo': 'Paquerador',
    'lj_personagens_desbloqueadas': ['Rafaela'],
    'lj_perfil_estilo': None,
    'lj_historico_partidas': [],
    'lj_desbloqueado': False,
    'lj_ficha': {}, 'lj_ficha_resumo': '',
    'lj_nome_persona': '', 'lj_dados_persona': {},
    'lj_cenario': '', 'lj_cenario_label': '',

    'lj_fases_ok': '',
    'lj_hist_partidas': [],
    'lj_personagens_ok': None,
    'ml_aberturas_usadas': None,
    'ml_cenario': '',
    'ml_character': None,
    'ml_connexometer': None,
    'ml_current_rank': None,
    'ml_estagio': None,
    'ml_historico': [],
    'ml_interaction_scores': None,
    'ml_last_result': None,
    'ml_messages': None,
    'ml_phase_coachings': None,
    'ml_phase_index': None,
    'ml_phase_message_start': None,
    'ml_phase_results': None,
    'ml_phase_start': None,
    'ml_response_since': None,
    'roleplay_cenario': '',
    'roleplay_system': None,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─── IA ───
def conexa_ia(prompt, system_extra=""):
    try:
        client = Groq(api_key=st.session_state.api_key)
        system = (
            "Você é o Conexão Magnética 2026 — sistema de inteligência para comunicação e conexões humanas.  REGRA DE OURO — CONFIABILIDADE 100%%: Forneça APENAS informações que você tem certeza absoluta que são verdadeiras. JAMAIS invente, suponha, extrapole ou preencha lacunas com dados fictícios. Se não souber algo com certeza — preço, endereço, horário, nome, estatística, lei, fato — diga EXPLICITAMENTE: 'Não tenho certeza sobre isso, recomendo verificar em [fonte].' É melhor uma resposta incompleta e honesta do que uma resposta completa e inventada. O usuário depende dessas informações para tomar decisões reais. "
            "Você ajuda pessoas a entender conversas, melhorar mensagens e desenvolver habilidades sociais. "
            "NUNCA afirme intenções ou sentimentos que não podem ser conhecidos. "
            "Trabalhe apenas com padrões observáveis. "
            "Seja direto, prático e baseado no contexto fornecido. "
            "Português do Brasil. " + system_extra
        )
        resp = client.chat.completions.create(
            messages=[{"role":"system","content":system},{"role":"user","content":prompt}],
            model="openai/gpt-oss-120b",
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"⚠️ Erro na API: {e}"

# ============================================================
# LOGIN
# ============================================================
# ── CONSTANTES GLOBAIS ──
FASES_DEF_G = [
    # (num, nome,             mins, titulo,          min_conexao, min_natural, min_interesse)
    (1, "ATRACAO",           5,  "Paquerador",      70, 60, 65),
    (2, "CONEXAO EMOCIONAL", 7,  "Galanteador",     75, 70, 65),
    (3, "SEDUCAO",           10, "Mestre da Labia", 80, 75, 70),
]
# Índices: [0]=num [1]=nome [2]=mins [3]=titulo [4]=min_conexao [5]=min_natural [6]=min_interesse

def estado_conexo_g(val):
    if val >= 80: return "CONEXAO FORTE", "#DC2626"
    if val >= 60: return "BOA QUIMICA", "#F59E0B"
    if val >= 40: return "NEUTRO", "#64748B"
    if val >= 20: return "INTERESSE CAINDO", "#EA580C"
    if val >= 1:  return "ULTIMA CHANCE", "#7F1D1D"
    return "ELIMINADA", "#000000"

PERSONAGENS = {
    "Rafaela": {
        "emoji": "😊", "dificuldade": 2, "estrelas": "⭐⭐",
        "desc": "Simpática, inteligente, bem-humorada. Conversa naturalmente mas não demonstra interesse imediatamente.",
        "personalidade": "simpatica, inteligente, bem-humorada, curiosa, fala de forma leve e natural",
        "humor": 80, "receptividade": 70, "provocacao": 30, "exigencia": 40, "bloqueada": False,
    },
    "Camila": {
        "emoji": "😏", "dificuldade": 4, "estrelas": "⭐⭐⭐⭐",
        "desc": "Segura, provocadora, responde com ironia e testa a confiança do usuário.",
        "personalidade": "segura, ironica, provocadora, testa confianca, nao facilita",
        "humor": 70, "receptividade": 45, "provocacao": 80, "exigencia": 70, "bloqueada": True,
    },
    "Helena": {
        "emoji": "🧐", "dificuldade": 5, "estrelas": "⭐⭐⭐⭐⭐",
        "desc": "Sofisticada, seletiva, difícil de impressionar. Exige conversa mais inteligente.",
        "personalidade": "sofisticada, seletiva, intelectual, dificil de impressionar, exige profundidade",
        "humor": 55, "receptividade": 30, "provocacao": 60, "exigencia": 90, "bloqueada": True,
    },
}

MISSOES_POR_FASE = {
    1: ["Fazer ela fazer uma pergunta espontânea sobre você","Conseguir que ela demonstre curiosidade","Criar um momento de humor","Fazer ela contar algo pessoal"],
    2: ["Fazer ela lembrar algo que você disse antes","Conseguir que ela compartilhe um sonho","Criar um momento de empatia genuína","Fazer ela admitir algo que normalmente não diria"],
    3: ["Criar um momento de flerte natural","Fazer ela brincar com você","Criar uma brincadeira interna entre vocês","Fazer ela perguntar algo pessoal espontaneamente"],
}

CENARIOS_TODOS = [
    "cafeteria","parque","livraria","fila de evento","shopping","feira",
    "exposicao de arte","aeroporto","praca","academia","show de musica",
    "festa de aniversario","mercado","galeria","coworking","food court",
    "banca de jornal","pet shop","sebo de livros","farmacia","bancada de bar",
    "fila de banco","salao de beleza","loja de discos","jardim botanico",
    "estacao de metro","calcadao","praia","aluguel de bicicletas","museu"
]

PERFIS_ESTILO = {
    "O Confiante":     "Fala com segurança, mas às vezes avança rápido demais.",
    "O Estrategista":  "Faz boas perguntas e lê bem os sinais.",
    "O Divertido":     "Usa humor para criar conexão.",
    "O Conquistador":  "Cria conexão emocional rapidamente.",
    "O Reservado":     "Tem boas respostas, mas demonstra pouco interesse.",
}

def carregar_json_sessao(dados):
    _bloq = {'api_key','etapa','nome_login','chave_login','upload_login','btn_entrar_login'}
    _pref = (
        'btn_','sel_','ul_','dl_','cad_','_sub','_sm','_tab','_bsc',
        'ativo_','rem_','sel_pet_','ev_','prof_','hig_','prev_',
        'vac_','sint_','comp_','trad_','subs_','amb_','viag_','chat_',
        'duvida_','emerg_','peso_','data_','obs_','tipo_','vet_','desc_',
        'local_','prox_','alim','sit_emerg_','tc_','oraf','siau','agmag',
        'lv','mv','pt','pi','sh','wc','rv','rp','rc',
    )
    import re as _re
    for k, v in dados.items():
        if k in _bloq: continue
        if any(k.startswith(p) for p in _pref): continue
        if _re.match(r'.+_\\d+$', k): continue
        st.session_state[k] = v

if 'lj_arranques' not in st.session_state: st.session_state['lj_arranques'] = []
if 'lj_cenario' not in st.session_state: st.session_state['lj_cenario'] = None
if 'lj_dados_persona' not in st.session_state: st.session_state['lj_dados_persona'] = {}
if 'lj_ficha' not in st.session_state: st.session_state['lj_ficha'] = {}
if 'lj_hist_partidas' not in st.session_state: st.session_state['lj_hist_partidas'] = []
if 'lj_inicio' not in st.session_state: st.session_state['lj_inicio'] = None

if 'lj_missao' not in st.session_state: st.session_state['lj_missao'] = ''
if 'lj_nome_persona' not in st.session_state: st.session_state['lj_nome_persona'] = ''
if 'lj_personagens_ok' not in st.session_state: st.session_state['lj_personagens_ok'] = []

if st.session_state.etapa == "Login":
    st.markdown("# 🧠 Conexão Magnética 2026")
    st.markdown("<div class=\\'card\\'><b>🔒 ACESSO RESTRITO A CLIENTES DO MEUSAGENTESIA.COM.BR</b><br>🔗 <a href='https://meusagentesia.com.br' target='_blank' style='color:#4F46E5;font-weight:700;text-decoration:underline;'>meusagentesia.com.br</a></div>", unsafe_allow_html=True)
    st.info("💻 **Dica:** Pela complexidade dos agentes, no computador a experiência é mais agradável.")
    with st.container():
        nome  = st.text_input("Seu Nome:", key="nome_login")
        chave = st.text_input("🔑 Sua Chave API da Groq:", type="password", key="chave_login")
        if st.button("✨ ENTRAR", key="btn_entrar_login"):
            if len(nome.strip()) < 2:
                st.warning("Digite um nome com pelo menos 2 caracteres.")
            elif chave.strip():
                st.session_state.usuario = nome.strip()
                st.session_state.api_key = chave
                st.session_state.etapa = "App"
                st.rerun()
            else:
                st.warning("Preencha nome e chave API.")

elif st.session_state.etapa == "App":
    faixa = FAIXAS[min(st.session_state.faixa_atual-1, 6)]
    em_partida = st.session_state.get('pagina') == 'Dialogo'

    if not em_partida:
        pass
        # ── NAVBAR ──
        # NAVBAR
    _nav_pgs = ['Home', 'Rapida', 'Carta', 'Turbinar', 'Analisar', 'Roleplay', 'Labia', 'Biblioteca', 'Perfil', 'Comparar', 'Plano', 'Progresso', 'Resumo', 'Conquistas']
    _nav_ics = ['🏠', '⚡', '🃏', '💬', '🧠', '🎭', '💋', '📚', '📸', '⚔️', '🗓️', '📈', '📋', '🏆']
    _nav_lbs = ['Dashboard', 'Resposta Rápida', 'Carta na Manga', 'Turbinar Mensagem', 'Raio-X da Conversa', 'Simulador de Conversa', '💋 Mestre da Lábia ⭐', 'Biblioteca Inteligente', 'Leitor de Perfil', 'Comparar Conversas', 'Plano 7 Dias', 'Minha Evolução', 'Relatório Semanal', 'Conquistas']
    _nav_idx = _nav_pgs.index(st.session_state.pagina) if st.session_state.pagina in _nav_pgs else 0

    # ── NAVEGAÇÃO: selectbox limpo ──
    _opcoes_nav = [f"{ic} {lb}" for ic, lb in zip(_nav_ics, _nav_lbs)]
    _sel_nav = st.selectbox("📍 Navegar para:", _opcoes_nav,
        index=_nav_idx, key="nav_select", label_visibility="collapsed")
    _pg_escolhida = _nav_pgs[_opcoes_nav.index(_sel_nav)]
    if _pg_escolhida != st.session_state.pagina:
        st.session_state.pagina = _pg_escolhida; st.rerun()

    st.markdown(f"<div style='text-align:center;font-weight:700;font-size:1.1em;color:#1A1A2E;padding:4px 0;'>{_nav_ics[_nav_idx]} {_nav_lbs[_nav_idx]}</div>", unsafe_allow_html=True)
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)



    if st.session_state.pagina == "Dialogo":
        import time as _t, json as _j, re as _r

        # Esconde TUDO do Streamlit — só o diálogo
        st.markdown(\"\"\"
        <style>
        header[data-testid="stHeader"]{display:none!important;}
        #MainMenu{display:none!important;}
        [data-testid="stToolbar"]{display:none!important;}
        footer{display:none!important;}
        .block-container{padding:0.5rem 1rem!important;}
        [data-testid="stSidebar"]{display:none!important;}

        .chat-wrap{
            display:flex;flex-direction:column;
            height:calc(100vh - 180px);
            min-height:300px;
        }
        .chat-msgs{
            flex:1;overflow-y:auto;
            padding:10px 4px;
            display:flex;flex-direction:column;
            scroll-behavior:smooth;
        }
        .msg-p{
            background:#FFF0F5;border:1px solid #FFB6C1;
            border-radius:4px 16px 16px 16px;
            padding:10px 14px;margin:6px 0;
            font-size:0.95em;color:#1A1A2E;
            max-width:80%;align-self:flex-start;
        }
        .msg-u{
            background:#F0F4FF;border:1px solid #C7D2FE;
            border-radius:16px 16px 4px 16px;
            padding:10px 14px;margin:6px 0;
            font-size:0.95em;color:#1A1A2E;
            max-width:80%;align-self:flex-end;
        }
        .msg-arr{
            font-size:0.72em;color:#22C55E;font-weight:700;
            text-align:right;margin-bottom:2px;
        }
        .bar-wrap{
            background:#fff;border:2px solid #22C55E;
            border-radius:10px;padding:6px 12px;
            display:flex;align-items:center;gap:8px;
            margin-bottom:6px;
        }
        .input-wrap{
            display:flex;gap:8px;align-items:center;
            padding:6px 0;
        }
        </style>\"\"\", unsafe_allow_html=True)

        # Redireciona se não há partida
        if not st.session_state.get('lj_ativo') or not st.session_state.get('lj_nome_persona') or st.session_state.get('lj_inicio',0)==0:
            st.session_state.pagina="Labia"; st.rerun()

        chat     = st.session_state.lj_chat
        conexo   = st.session_state.lj_conexo
        fase_n   = st.session_state.lj_fase
        nome_p   = st.session_state.lj_nome_persona
        dados_p  = st.session_state.lj_dados_persona
        cenario  = st.session_state.lj_cenario
        ficha    = st.session_state.lj_ficha
        atribs   = st.session_state.lj_atributos

        FASES_D  = {1:(5,70,60,65,"🥉 Paquerador"),2:(7,75,70,65,"🥈 Galanteador"),3:(10,80,75,70,"👑 Mestre da Lábia")}
        fi       = FASES_D[fase_n]
        duracao  = fi[0]*60
        inicio   = st.session_state.lj_inicio
        decorrido= _t.time() - inicio
        restante = max(0, duracao - decorrido)
        mins_r   = int(restante//60); segs_r = int(restante%60)
        pct_t    = max(0.0, 1-decorrido/duracao)
        cor_c    = "#22C55E" if conexo>70 else ("#84CC16" if conexo>50 else ("#F59E0B" if conexo>30 else ("#EF4444" if conexo>10 else "#7F1D1D")))
        pulso    = "animation:pulso 0.8s ease-in-out infinite;" if conexo<=20 else ""
        cor_t    = "#22C55E" if pct_t>0.5 else ("#F59E0B" if pct_t>0.2 else "#EF4444")

        def estado(v):
            if v>=80: return "🔥 CONEXÃO FORTE"
            if v>=60: return "❤️ BOA QUÍMICA"
            if v>=40: return "😐 NEUTRO"
            if v>=20: return "⚠️ CAINDO"
            return "🚨 ÚLTIMA CHANCE"

        # ── CENÁRIO ──
        st.markdown(
            f"<div style='background:#FFF0F5;border:1px solid #FFB6C1;border-radius:8px;"
            f"padding:4px 14px;margin-bottom:4px;font-size:0.82em;color:#5C0F30;'>"
            f"📍 <b>{cenario.capitalize()}</b> — Você acaba de conhecer alguém.</div>",
            unsafe_allow_html=True)

        # ── CONEXÔMETRO + TIMER (numa linha) ──
        st.markdown(
            f"<style>@keyframes pulso{{0%,100%{{opacity:1}}50%{{opacity:.4}}}}</style>"
            f"<div class='bar-wrap'>"
            f"<span style='font-size:0.7em;color:#64748B;font-weight:600;white-space:nowrap;'>❤️ CONEXÔMETRO</span>"
            f"<div style='flex:1;background:#F1F5F9;border-radius:999px;height:10px;overflow:hidden;'>"
            f"<div style='height:100%;border-radius:999px;background:{cor_c};width:{conexo}%;transition:width 0.4s;{pulso}'></div></div>"
            f"<span style='font-size:0.9em;font-weight:700;color:{cor_c};white-space:nowrap;'>{conexo} {estado(conexo)}</span>"
            f"<span style='border-left:1px solid #E2E8F0;padding-left:10px;font-size:0.7em;color:#94A3B8;'>⏱️</span>"
            f"<span style='font-size:1em;font-weight:700;color:{cor_t};'>{mins_r:02d}:{segs_r:02d}</span>"
            f"</div>", unsafe_allow_html=True)

        # ── ALERTAS ──
        if 0 < conexo <= 20:
            st.markdown("<div style='color:#B91C1C;font-weight:700;font-size:0.85em;text-align:center;'>🚨 ÚLTIMA CHANCE</div>", unsafe_allow_html=True)
        if st.session_state.lj_missao_cumprida:
            st.markdown("<div style='color:#22C55E;font-weight:700;font-size:0.8em;text-align:center;'>🎯 MISSÃO CUMPRIDA!</div>", unsafe_allow_html=True)
        # Alerta de silêncio
        if ts_p > 0 and ts_u < ts_p:
            inat_alerta = _t.time() - ts_p
            if inat_alerta > 25:
                emoji_alerta = "🔴" if inat_alerta > 45 else "🟡"
                st.markdown(f"<div style='color:#B45309;font-weight:700;font-size:0.82em;text-align:center;'>{emoji_alerta} {'RESPONDA AGORA — conexômetro caindo!' if inat_alerta>45 else 'Silêncio detectado — responda logo!'}</div>", unsafe_allow_html=True)

        # ── CHAT (ocupa toda a altura disponível) ──
        msgs_html = ""
        for msg in chat:
            if msg['role']=='user':
                msgs_html += f"<div class='msg-u'><b style='color:#7C3AED;'>Você:</b> {msg['content']}</div>"
            else:
                arr = msg.get('arranque','')
                if arr: msgs_html += f"<div class='msg-arr'>{arr}</div>"
                msgs_html += f"<div class='msg-p'><b style='color:#C2185B;'>😊 {nome_p}:</b> {msg['content']}</div>"

        turno_u = sum(1 for m in chat if m['role']=='user')
        if fase_n==1 and turno_u==0:
            msgs_html += f"<div style='font-size:0.75em;color:#94A3B8;border-left:2px solid #FFB6C1;padding:4px 10px;margin:4px 0;'>💡 Comente o que {nome_p} disse.</div>"

        st.markdown(
            f"<div class='chat-msgs' id='chat-c'>{msgs_html}<div id='cb'></div></div>"
            f"<script>setTimeout(()=>{{var c=document.getElementById('chat-c');if(c)c.scrollTop=c.scrollHeight;}},80);</script>",
            unsafe_allow_html=True)

        # ── INATIVIDADE — 25s calado = -25% fixo ──
        ts_p = st.session_state.lj_ts_persona; ts_u = st.session_state.lj_ts_usuario
        if ts_p > 0 and ts_u < ts_p:
            inat = _t.time() - ts_p
            # A cada 25s completos de silêncio, aplica -25%
            blocos = int(inat // 25)
            if blocos > st.session_state.get('lj_blocos_silencio', 0):
                st.session_state['lj_blocos_silencio'] = blocos
                novo_c = max(0, conexo - 25)
                st.session_state.lj_conexo = novo_c
                if novo_c!=conexo: st.session_state.lj_conexo=novo_c

        # ── FIM DE PARTIDA ──
        if restante<=0 or conexo<=0:
            hist_txt = "\\n".join(f"{'Você' if m['role']=='user' else nome_p}: {m['content']}" for m in chat)
            n_arr = len(st.session_state.lj_arranques)
            mc,mn,mi,_,titulo_fase = fi[1],fi[2],fi[3],fi[0],fi[4]
            passou = (conexo>=mc and atribs.get('naturalidade',0)>=mn and atribs.get('interesse',0)>=mi and turno_u>=4 and restante<=0)
            prompt_av = (
                f"Avalie conversa — Fase {fase_n}.\\n"
                f"Personagem:{nome_p}. Conexao:{conexo}. Arranques:{n_arr}. Turnos:{turno_u}.\\n"
                f"Missao:'{st.session_state.lj_missao}' — cumprida:{st.session_state.lj_missao_cumprida}\\n"
                f"Conversa:\\n{hist_txt}\\n\\n"
                f"JSON sem markdown:\\n"
                + '{"aprovado":false,"ponto_forte":"1 frase","melhorar":"1 frase","perfil":"O Confiante","missao_ok":false}'
            )
            with st.spinner("Avaliando..."):
                try:
                    from groq import Groq as _Groq
                    _cl = _Groq(api_key=st.session_state.api_key)
                    _r2 = _cl.chat.completions.create(messages=[{"role":"user","content":prompt_av}],model="openai/gpt-oss-120b",max_tokens=200)
                    jm = _r.search(r'\\{.*\\}',_r2.choices[0].message.content,_r.DOTALL)
                    av_d = _j.loads(jm.group(0)) if jm else {}
                except: av_d = {}
            aprovado = passou and av_d.get('aprovado',passou)
            if aprovado:
                st.session_state.lj_fases_ok = max(st.session_state.lj_fases_ok, fase_n)
                nomes_pers = ["Rafaela","Camila","Helena"]
                for i2 in range(min(fase_n,3)):
                    if nomes_pers[i2] not in st.session_state.lj_personagens_ok:
                        st.session_state.lj_personagens_ok.append(nomes_pers[i2])
                TITULOS = {1:"🥉 Paquerador",2:"🥈 Galanteador",3:"👑 Mestre da Lábia"}
                st.session_state.lj_titulo = TITULOS[fase_n]
            st.session_state.lj_aval = {
                'aprovado':aprovado,
                'titulo': f"FASE {fase_n} CONCLUÍDA! 🎉" if aprovado else "CONEXÃO PERDIDA 💥",
                'conexo_final':conexo,'n_arranques':n_arr,
                'missao_cumprida':av_d.get('missao_ok',False),
                'ponto_forte':av_d.get('ponto_forte','—'),
                'melhorar':av_d.get('melhorar','—'),
            }
            st.session_state.lj_hist_partidas.append({
                'fase':fase_n,'personagem':nome_p,'conexo_final':conexo,
                'aprovado':aprovado,'data':datetime.now().strftime('%d/%m %H:%M'),
                'ficha_resumo':st.session_state.get('lj_ficha_resumo',''),
            })
            st.session_state.lj_ativo=False; st.session_state.lj_chat=[]
            st.session_state.pagina="Labia"; st.rerun()

        else:
            # ── INPUT + BOTÕES ──
            msg_in = st.text_input("",key=f"lj_in_{len(chat)}",
                placeholder="O que você diz?",label_visibility="collapsed")
            col_e, col_s = st.columns([4,1])
            with col_e:
                if st.button("📤 ENVIAR",key="lj_env",use_container_width=True):
                    if msg_in.strip():
                        st.session_state.lj_ts_usuario = _t.time()
                        st.session_state['lj_blocos_silencio'] = 0  # reset silêncio
                        f2 = ficha
                        aviso_pes = ""
                        kws = ['aniversario','cidade','mora','trabalha','profissao','musica','hobby','medo','sonho']
                        if any(k in msg_in.lower() for k in kws):
                            aviso_pes = f"\\nAVISO: Aniversario={f2.get('aniversario','?')}, Cidade={f2.get('cidade','?')}, Profissao={f2.get('profissao','?')}."
                        ultima = chat[-1]['content'] if chat else ''
                        sys_p = (
                            f"Você é {nome_p}, {f2.get('profissao','')}, {f2.get('cidade','')}.\\n"
                            f"Personalidade: {dados_p.get('personalidade','')}.\\n"
                            f"Cenário: {cenario}. Hoje: {f2.get('hoje','')}.\\n"
                            f"Você disse '{ultima}', pessoa respondeu '{msg_in}'.\\n"
                            f"Reaja a ISSO. Máximo 10 palavras. Estilo WhatsApp.\\n"
                            f"Zero filosofia. Só reaja. NUNCA revele que é IA."
                            + aviso_pes
                        )
                        hist = [{"role":m["role"],"content":m["content"]} for m in chat[-6:]]
                        with st.spinner(""):
                            try:
                                from groq import Groq as _Groq2
                                _cl2 = _Groq2(api_key=st.session_state.api_key)
                                msgs_l = [{"role":"system","content":sys_p.encode("utf-8","ignore").decode("utf-8")}]+hist+[{"role":"user","content":msg_in}]
                                resp_l = _cl2.chat.completions.create(messages=msgs_l,model="openai/gpt-oss-120b",max_tokens=40)
                                resp_bruto = resp_l.choices[0].message.content.strip().split('\\n')[0]
                                mc2 = _r.search(r'[.!?]',resp_bruto)
                                resp_txt = resp_bruto[:mc2.end()].strip() if mc2 else ' '.join(resp_bruto.split()[:10])
                                if not resp_txt.strip():
                                    resp_txt = "Interessante..."
                            except Exception as e:
                                resp_txt = "Hm, é mesmo?"
                        CRIT = {
                            1:"Fase 1: avalie curiosidade,humor,originalidade. Generoso. delta -15 a +20",
                            2:"Fase 2: avalie escuta,empatia,profundidade. Moderado. delta -15 a +18",
                            3:"Fase 3: avalie timing,tensao,confianca. Exigente. delta -15 a +20",
                        }
                        prompt_ev = (
                            f"Avaliador. Fase {fase_n}.\\n"
                            f"Ela:'{ultima}' Usuario:'{msg_in}'\\n"
                            f"{CRIT.get(fase_n,CRIT[1])}\\n"
                            f"Missao:'{st.session_state.lj_missao}'\\n"
                            f"JSON: {{\\"delta\\":0,\\"interesse\\":50,\\"atracao\\":50,\\"conexao\\":50,\\"confianca\\":50,\\"naturalidade\\":50,\\"arranque\\":\\"\\",\\"missao_cumprida\\":false}}"
                        )
                        with st.spinner(""):
                            try:
                                from groq import Groq as _Groq3
                                _cl3 = _Groq3(api_key=st.session_state.api_key)
                                ev_txt = _cl3.chat.completions.create(messages=[{"role":"user","content":prompt_ev.encode("utf-8","ignore").decode("utf-8")}],model="openai/gpt-oss-120b",max_tokens=150).choices[0].message.content
                                jm2 = _r.search(r'\\{.*\\}',ev_txt,_r.DOTALL)
                                ev_d = _j.loads(jm2.group(0)) if jm2 else {}
                            except: ev_d = {}
                        delta = ev_d.get('delta',0)
                        arranque = f"🚀 {ev_d.get('arranque', '')}" if ev_d.get('arranque') else ""
                        for k in ['interesse','atracao','conexao','confianca','naturalidade']:
                            if k in ev_d: atribs[k]=max(0,min(100,ev_d[k]))
                        st.session_state.lj_atributos = atribs
                        st.session_state.lj_conexo = max(0,min(100,conexo+delta))
                        if ev_d.get('missao_cumprida'): st.session_state.lj_missao_cumprida=True
                        st.session_state.lj_combo = st.session_state.lj_combo+1 if delta>5 else 0
                        if arranque: st.session_state.lj_arranques.append(arranque)
                        ph = st.empty()
                        palavras = resp_txt.split()
                        txt_ac = ""
                        for p_w in palavras:
                            txt_ac += ("" if txt_ac=="" else " ")+p_w
                            ph.markdown(f"<div class='msg-p'><b style='color:#C2185B;'>😊 {nome_p}:</b> {txt_ac}▌</div>",unsafe_allow_html=True)
                            _t.sleep(0.07)
                        ph.empty()
                        chat.append({"role":"user","content":msg_in,"ts":_t.time()})
                        chat.append({"role":"assistant","content":resp_txt,"ts":_t.time(),"arranque":arranque})
                        st.session_state.lj_chat=chat
                        st.session_state.lj_ts_persona=_t.time()
                        st.rerun()
            with col_s:
                if st.button("🚩 Sair",key="lj_sair",use_container_width=True):
                    st.session_state.lj_ativo=False; st.session_state.lj_chat=[]
                    st.session_state.pagina="Labia"; st.rerun()
            _t.sleep(0.8); st.rerun()

    # Bloco abaixo só executa quando NÃO está no Dialogo
    if em_partida:
        st.stop()

    if not em_partida:
        if st.session_state.pagina == "Home":
            col_u, col_r = st.columns([3,1])
            with col_u:
                st.title(f"💋 Olá, {st.session_state.usuario}!")
                st.markdown(f"<span class='badge-roxo'>{faixa[0]} {faixa[2]}</span>", unsafe_allow_html=True)
            with col_r:
                if st.button("🚪 Sair", key="conexaom3"):
                    for k in list(st.session_state.keys()): del st.session_state[k]
                    st.rerun()

        # PAINEL PRINCIPAL
        st.markdown(f\"\"\"
        <div class='painel-conexa'>
            <div style='font-size:0.82em;opacity:0.7;letter-spacing:2px;margin-bottom:12px;'>🧠 Conexão Magnética 2026 — PAINEL DE INTELIGÊNCIA</div>
            <div style='font-size:1.1em;opacity:0.6;margin-bottom:16px;'>A IA que ajuda você a entender a conversa — e saber o próximo passo.</div>
            <div style='display:grid;grid-template-columns:repeat(3,1fr);gap:14px;'>
                <div style='text-align:center;background:rgba(255,255,255,0.06);border-radius:12px;padding:14px;'>
                    <div style='font-size:0.7em;opacity:0.6;'>⚡ NÍVEL ATUAL</div>
                    <div style='font-size:1.3em;font-weight:700;'>{faixa[2]}</div>
                </div>
                <div style='text-align:center;background:rgba(255,255,255,0.06);border-radius:12px;padding:14px;'>
                    <div style='font-size:0.7em;opacity:0.6;'>💬 CONVERSAS</div>
                    <div style='font-size:1.6em;font-weight:700;'>{st.session_state.conversas_analisadas}</div>
                </div>
                <div style='text-align:center;background:rgba(255,255,255,0.06);border-radius:12px;padding:14px;'>
                    <div style='font-size:0.7em;opacity:0.6;'>🃏 CARTAS USADAS</div>
                    <div style='font-size:1.6em;font-weight:700;'>{st.session_state.cartas_usadas}</div>
                </div>
            </div>
        </div>
        \"\"\", unsafe_allow_html=True)

        # DASHBOARD MÉTRICAS
        st.markdown("### 📊 Seu Desempenho")
        c1,c2,c3,c4,c5,c6 = st.columns(6)
        c1.markdown(f"<div class='stat-box'><div class='stat-numero'>{st.session_state.conversas_analisadas}</div><div>Conversas</div></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='stat-box'><div class='stat-numero'>{st.session_state.mensagens_aprimoradas}</div><div>Turbinadas</div></div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='stat-box'><div class='stat-numero'>{st.session_state.analises_realizadas}</div><div>Análises</div></div>", unsafe_allow_html=True)
        c4.markdown(f"<div class='stat-box'><div class='stat-numero'>{st.session_state.cartas_usadas}</div><div>Cartas</div></div>", unsafe_allow_html=True)
        c5.markdown(f"<div class='stat-box'><div class='stat-numero'>{st.session_state.treinos_realizados}</div><div>Treinos</div></div>", unsafe_allow_html=True)
        c6.markdown(f"<div class='stat-box'><div class='stat-numero'>{st.session_state.favoritos_total}</div><div>Favoritos</div></div>", unsafe_allow_html=True)

        # EVOLUÇÃO
        st.markdown("### 📈 Evolução")
        metricas = [
            ("Clareza", st.session_state.clareza),
            ("Naturalidade", st.session_state.naturalidade),
            ("Reciprocidade", st.session_state.reciprocidade),
            ("Confiança", st.session_state.confianca),
            ("Escuta", st.session_state.escuta),
        ]
        for nome_m, val in metricas:
            cor = "#22C55E" if val >= 7 else ("#B45309" if val >= 4 else "#B91C1C")
            st.markdown(f\"\"\"
            <div style='margin-bottom:10px;'>
                <div style='display:flex;justify-content:space-between;font-size:0.88em;font-weight:600;color:#1A1A2E;'>
                    <span>{nome_m}</span><span style='color:{cor};'>{val}/10</span>
                </div>
                <div style='background:#F1F5F9;border-radius:999px;height:8px;overflow:hidden;margin-top:4px;'>
                    <div style='height:100%;border-radius:999px;background:{cor};width:{val*10}%;'></div>
                </div>
            </div>
            \"\"\", unsafe_allow_html=True)

        # GUIA DE ABAS
        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        st.markdown("### 🗺️ O que cada aba faz")
        guia = {
            "⚡ Resposta Rápida": "Cole uma mensagem e receba 3 opções de resposta com estratégia",
            "🃏 Carta na Manga": "Quando você não sabe o que dizer — a IA encontra uma nova possibilidade",
            "💬 Turbinar": "Melhore qualquer mensagem — clareza, tom e naturalidade",
            "🧠 Raio-X": "Análise completa de uma conversa — fluidez, reciprocidade e oportunidades",
            "🎭 Roleplay": "Simule conversas e receba avaliação detalhada",
            "🎭 Arte da Lábia": "Treinamento adaptativo em 7 faixas — do iniciante ao Don Juan",
            "📚 Biblioteca": "Suas melhores respostas organizadas por categoria",
            "📸 Leitor de Perfil": "Analisa informações públicas e sugere assuntos de conversa",
            "⚔️ Comparar": "Compare duas conversas e descubra qual tem melhor dinâmica",
            "🗓️ Plano 7 Dias": "Plano de desenvolvimento de comunicação personalizado",
            "📈 Progresso": "Sua evolução ao longo do tempo em todas as métricas",
            "📋 Relatório": "Resumo semanal gerado automaticamente pela IA",
        }
        for aba, desc in guia.items():
            st.markdown(f"**{aba}** — <span style='color:#4B5563;'>{desc}</span>", unsafe_allow_html=True)

        if st.session_state.historico:
            st.markdown("<hr class='divider'>", unsafe_allow_html=True)
            st.markdown("### 🕐 Últimas Atividades")
            for item in reversed(st.session_state.historico[-4:]):
                st.markdown(f"<div class='hist-item'><span class='badge'>{item['tipo']}</span> <small style='color:#888'>{item['data']}</small><br><small>{item.get('tema', '')[:80]}</small></div>", unsafe_allow_html=True)

        # ──────────────────────────────────────────
        # RESPOSTA RÁPIDA
        # ──────────────────────────────────────────
        elif st.session_state.pagina == "Rapida":
            st.header("⚡ Resposta Inteligente")
            st.markdown("Cole a mensagem recebida e receba 3 opções estratégicas de resposta.")

            msg_recebida = st.text_area("💬 Mensagem recebida:", height=100, placeholder="Cole a mensagem aqui...", key="conexaom4")
            col1, col2 = st.columns(2)
            with col1:
                quem = st.selectbox("Quem é essa pessoa?", ["Colega","Amigo","Pessoa nova","Interesse romântico","Familiar","Outro"], key="conexaom5")
            with col2:
                objetivo = st.selectbox("O que você quer fazer?", ["Continuar a conversa","Responder de forma natural","Esclarecer algo","Iniciar um assunto novo","Dar um passo à frente"], key="conexaom6")

        contexto_extra = st.text_input("Contexto adicional (opcional):", placeholder="ex: acabamos de nos conhecer, faz 2 dias que não falamos...", key="conexaom7")

        if st.button("⚡ ANALISAR E RESPONDER", key="conexaom8"):
            if msg_recebida.strip():
                with st.spinner("Analisando o contexto..."):
                    prompt = (
                        f"Analise esta mensagem e gere 3 opções estratégicas de resposta.\\n"
                        f"Mensagem recebida: '{msg_recebida}'\\n"
                        f"Quem enviou: {quem}. Objetivo: {objetivo}. Contexto: {contexto_extra or 'não informado'}.\\n\\n"
                        f"REGRAS:\\n"
                        f"- NÃO afirme intenções ou sentimentos que não podem ser conhecidos\\n"
                        f"- Trabalhe apenas com padrões observáveis na mensagem\\n"
                        f"- Respostas devem soar naturais, não robóticas\\n\\n"
                        f"FORMATO:\\n\\n"
                        f"📊 LEITURA DO CONTEXTO:\\n[O que é observável nessa mensagem — tom, abertura, oportunidades]\\n\\n"
                        f"💬 OPÇÃO 1 — NATURAL\\n[resposta]\\nPor quê: [explicação curta]\\n\\n"
                        f"💡 OPÇÃO 2 — INTERESSANTE\\n[resposta]\\nPor quê: [explicação curta]\\n\\n"
                        f"🎯 OPÇÃO 3 — DIRETA\\n[resposta]\\nPor quê: [explicação curta]\\n\\n"
                        f"⭐ RECOMENDAÇÃO:\\n[qual das 3 é mais adequada para esse contexto e por quê]"
                    )
                    res = conexa_ia(prompt)
                    st.session_state.analises_realizadas += 1
                    st.session_state.conversas_analisadas += 1
                    verificar_conquistas()
                    salvar_historico("Resposta Rápida", msg_recebida[:60], res)
                    st.session_state['rapida_temp'] = res
            else:
                st.warning("Cole a mensagem antes de analisar.")

        if st.session_state.get('rapida_temp'):
            st.markdown(f"<div class='card'>{st.session_state['rapida_temp']}</div>", unsafe_allow_html=True)
            col_cp, col_fv, col_sv = st.columns(3)
            with col_cp:
                st.download_button("📋 Copiar (.txt)", data=st.session_state['rapida_temp'], file_name="resposta.txt", mime="text/plain", use_container_width=True, key="dl_conexa_3")
            with col_fv:
                if st.button("⭐ Favoritar", key="fav_rapida", use_container_width=True):
                    st.session_state.biblioteca.append({'categoria':'Respostas','conteudo':st.session_state['rapida_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.session_state.favoritos_total += 1
                    st.success("⭐ Salvo na biblioteca!")
            with col_sv:
                if st.button("🃏 Carta na Manga", key="carta_rapida", use_container_width=True):
                    st.session_state.pagina = "Carta"; st.rerun()

        # ──────────────────────────────────────────
        # CARTA NA MANGA
        # ──────────────────────────────────────────
        elif st.session_state.pagina == "Carta":
            st.header("🃏 Carta na Manga")
            st.markdown("Quando você não sabe mais o que dizer — a IA encontra uma nova possibilidade.")

            conversa_carta = st.text_area("💬 Cole a conversa completa:", height=180, placeholder="Cole aqui toda a conversa...", key="conexaom9")
            contexto_carta = st.text_input("Contexto (opcional):", placeholder="ex: amigo, interesse romântico, colega de trabalho...", key="conexaom10")

            if st.button("🃏 GERAR CARTAS NA MANGA", key="conexaom11"):
                if conversa_carta.strip():
                    with st.spinner("A IA está procurando novas possibilidades..."):
                        prompt = (
                        f"Analise esta conversa e gere 5 cartas na manga — novas possibilidades de interação.\\n"
                        f"Conversa:\\n{conversa_carta}\\n"
                        f"Contexto: {contexto_carta or 'não informado'}\\n\\n"
                        f"REGRAS:\\n"
                        f"- Trabalhe APENAS com o que está na conversa\\n"
                        f"- NÃO fabrique fatos, interesses ou sentimentos\\n"
                        f"- Cada carta deve ser genuinamente diferente das outras\\n\\n"
                        f"FORMATO:\\n\\n"
                        f"🃏 CARTA #01 — RESGATAR UM ASSUNTO\\n"
                        f"[mensagem sugerida]\\n"
                        f"Por que essa carta: [explicação]\\n\\n"
                        f"🃏 CARTA #02 — MUDAR O RUMO\\n"
                        f"[mensagem sugerida]\\n"
                        f"Por que essa carta: [explicação]\\n\\n"
                        f"🃏 CARTA #03 — PERGUNTA-CHAVE\\n"
                        f"[pergunta aberta]\\n"
                        f"Por que essa carta: [explicação]\\n\\n"
                        f"🃏 CARTA #04 — LEVEZA\\n"
                        f"[abordagem descontraída]\\n"
                        f"Por que essa carta: [explicação]\\n\\n"
                        f"🛡️ CARTA #05 — DAR ESPAÇO\\n"
                        f"[avaliação de quando não insistir é o melhor caminho]\\n\\n"
                        f"⭐ CARTA RECOMENDADA: [número e por quê é a melhor agora]"
                    )
                    res = conexa_ia(prompt)
                    st.session_state.cartas_usadas += 1
                    verificar_conquistas()
                    salvar_historico("Carta na Manga", conversa_carta[:60], res)
                    st.session_state['carta_temp'] = res
            else:
                st.warning("Cole a conversa antes de gerar.")

        if st.session_state.get('carta_temp'):
            st.markdown(f"<div class='carta-box'>{st.session_state['carta_temp']}</div>", unsafe_allow_html=True)
            col_cp, col_fv = st.columns(2)
            with col_cp:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['carta_temp'], file_name="carta_manga.txt", mime="text/plain", use_container_width=True, key="dl_conexa_4")
            with col_fv:
                if st.button("⭐ Favoritar cartas", key="fav_carta", use_container_width=True):
                    st.session_state.biblioteca.append({'categoria':'Cartas na Manga','conteudo':st.session_state['carta_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.session_state.favoritos_total += 1
                    st.success("⭐ Salvo!")

        # ──────────────────────────────────────────
        # TURBINAR
        # ──────────────────────────────────────────
        elif st.session_state.pagina == "Turbinar":
            st.header("💬 Turbinar Mensagem")
            st.markdown("Cole sua mensagem e a IA a aprimora — clareza, tom e naturalidade.")

            msg_orig = st.text_area("✍️ Sua mensagem:", height=100, placeholder="Cole sua mensagem aqui...", key="conexaom12")
            col1, col2 = st.columns(2)
            with col1:
                estilo = st.selectbox("Estilo desejado:", ["Natural","Leve","Confiante","Divertido","Direto","Empático"], key="conexaom13")
            with col2:
                contexto_turb = st.text_input("Contexto:", placeholder="ex: primeira mensagem, resposta após sumiço...", key="conexaom14")

        if st.button("💬 TURBINAR MENSAGEM", key="conexaom15"):
            if msg_orig.strip():
                with st.spinner("Aprimorando..."):
                    prompt = (
                        f"Avalie e melhore esta mensagem.\\n"
                        f"Mensagem original: '{msg_orig}'\\n"
                        f"Estilo desejado: {estilo}. Contexto: {contexto_turb or 'não informado'}.\\n\\n"
                        f"FORMATO:\\n\\n"
                        f"📊 AVALIAÇÃO DA MENSAGEM ORIGINAL:\\n"
                        f"• Clareza: [nota]/10\\n"
                        f"• Naturalidade: [nota]/10\\n"
                        f"• Tom: [análise]\\n"
                        f"• Reciprocidade: [abre espaço para o outro?]\\n"
                        f"• Pressão: [há pressão excessiva?]\\n\\n"
                        f"❌ ANTES:\\n{msg_orig}\\n\\n"
                        f"✅ DEPOIS — ESTILO {estilo.upper()}:\\n[mensagem aprimorada]\\n\\n"
                        f"🧠 POR QUE MELHOROU:\\n[explicação objetiva das mudanças]\\n\\n"
                        f"💡 VARIAÇÃO ALTERNATIVA:\\n[outra versão em estilo diferente]"
                    )
                    res = conexa_ia(prompt)
                    st.session_state.mensagens_aprimoradas += 1
                    verificar_conquistas()
                    salvar_historico("Turbinar", msg_orig[:60], res)
                    st.session_state['turb_temp'] = res
            else:
                st.warning("Cole a mensagem antes de turbinar.")

        if st.session_state.get('turb_temp'):
            st.markdown(f"<div class='card'>{st.session_state['turb_temp']}</div>", unsafe_allow_html=True)
            if st.button("⭐ Favoritar", key="fav_turb"):
                st.session_state.biblioteca.append({'categoria':'Mensagens Turbinadas','conteudo':st.session_state['turb_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                st.session_state.favoritos_total += 1
                st.success("⭐ Salvo!")

        # ──────────────────────────────────────────
        # RAIO-X DA CONVERSA
        # ──────────────────────────────────────────
        elif st.session_state.pagina == "Analisar":
            st.header("🧠 Raio-X da Conversa")
            st.markdown("Análise completa — fluidez, reciprocidade, qualidade e oportunidades.")

            conversa_rx = st.text_area("💬 Cole a conversa completa:", height=200, placeholder="Cole a conversa aqui...", key="conexaom16")

            if st.button("🧠 ANALISAR CONVERSA", key="conexaom17"):
                if conversa_rx.strip():
                    with st.spinner("Fazendo o raio-X..."):
                        prompt = (
                        f"Faça uma análise completa desta conversa.\\n\\n"
                        f"IMPORTANTE: NÃO afirme sentimentos ou intenções. Apresente APENAS padrões observáveis.\\n\\n"
                        f"Conversa:\\n{conversa_rx}\\n\\n"
                        f"FORMATO:\\n\\n"
                        f"📊 01 — FLUIDEZ\\n"
                        f"Status: [🟢 Fluindo / 🟡 Perdendo ritmo / 🔴 Travada]\\n"
                        f"[análise observável]\\n\\n"
                        f"🤝 02 — RECIPROCIDADE\\n"
                        f"[Quem inicia, tamanho das respostas, perguntas feitas, equilíbrio — sem afirmar sentimentos]\\n\\n"
                        f"💬 03 — QUALIDADE DA COMUNICAÇÃO\\n"
                        f"• Clareza: [nota]/10\\n• Naturalidade: [nota]/10\\n• Escuta: [nota]/10\\n"
                        f"• Perguntas: [quantidade e qualidade]\\n• Pressão: [há?]\\n\\n"
                        f"🎯 04 — ASSUNTOS\\n"
                        f"✅ Que funcionaram: [lista]\\n"
                        f"💡 Que podem ser explorados: [lista]\\n"
                        f"📉 Que perderam força: [lista]\\n\\n"
                        f"🚦 05 — RADAR\\n"
                        f"[🟢 / 🟡 / 🔴 com justificativa baseada em padrões observáveis]\\n\\n"
                        f"🎯 06 — PRÓXIMO PASSO RECOMENDADO:\\n[ação concreta]"
                    )
                    res = conexa_ia(prompt)
                    st.session_state.analises_realizadas += 1
                    st.session_state.conversas_analisadas += 1
                    verificar_conquistas()
                    salvar_historico("Raio-X", conversa_rx[:60], res)
                    st.session_state['rx_temp'] = res
            else:
                st.warning("Cole a conversa antes de analisar.")

        if st.session_state.get('rx_temp'):
            st.markdown(f"<div class='card'>{st.session_state['rx_temp']}</div>", unsafe_allow_html=True)
            col_dl, col_fv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['rx_temp'], file_name="raio_x.txt", mime="text/plain", use_container_width=True, key="dl_conexa_5")
            with col_fv:
                if st.button("⭐ Favoritar", key="fav_rx", use_container_width=True):
                    st.session_state.biblioteca.append({'categoria':'Análises','conteudo':st.session_state['rx_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.session_state.favoritos_total += 1; st.success("⭐ Salvo!")

        # ──────────────────────────────────────────
        # ROLEPLAY
        # ──────────────────────────────────────────
        elif st.session_state.pagina == "Roleplay":
            st.header("🎭 Simulador de Conversa")
            st.markdown("Treine antes de enviar. A IA simula uma pessoa real em um cenário.")

            if 'roleplay_chat' not in st.session_state:
                st.session_state.roleplay_chat = []
        if 'roleplay_ativo' not in st.session_state:
            st.session_state.roleplay_ativo = False
        if 'roleplay_key' not in st.session_state:
            st.session_state.roleplay_key = 0

        if not st.session_state.roleplay_ativo:
            cenario = st.selectbox("Escolha o cenário:", [
                "🤝 Conhecer alguém novo","👥 Fazer amizade","🏫 Conversar com colega",
                "💼 Networking","🗣️ Conversa difícil","😬 Situação que causa nervosismo"])
            nivel_role = st.selectbox("Dificuldade:", ["Fácil — pessoa receptiva","Médio — pessoa neutra","Difícil — pessoa reservada"], key="conexaom18")

            if st.button("🎭 INICIAR SIMULAÇÃO", key="conexaom19"):
                with st.spinner("Criando o cenário..."):
                    system_role = (
                        f"Você é uma pessoa num simulador de conversa para treino de comunicação. "
                        f"Cenário: {cenario}. Dificuldade: {nivel_role}. "
                        f"Seja realista — não force perguntas, não salve a conversa artificialmente. "
                        f"Mantenha personalidade consistente. Responda como essa pessoa responderia, "
                        f"não como um assistente. Primeira mensagem: apresente o cenário brevemente e comece a interação."
                    )
                    resp = conexa_ia("Inicie o cenário com uma fala natural da personagem.", system_role)
                    st.session_state.roleplay_chat = [{"role":"assistant","content":resp,"system":system_role}]
                    st.session_state.roleplay_ativo = True
                    st.session_state.roleplay_cenario = cenario
                    st.session_state.roleplay_system = system_role
                    st.rerun()
        else:
            st.markdown(f"**Cenário:** {st.session_state.get('roleplay_cenario','')}")
            for msg in st.session_state.roleplay_chat:
                if msg['role'] == 'user':
                    st.markdown(f"<div class='chat-user'><b style='color:#C2185B;'>Você:</b> {msg['content']}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='chat-persona'><b style='color:#1D4ED8;'>🎭 Personagem:</b> {msg['content']}</div>", unsafe_allow_html=True)

            msg_role = st.text_input("Sua resposta:", key=f"role_input_{st.session_state.roleplay_key}", placeholder="O que você diria?")

            col_e, col_f = st.columns([4,1])
            with col_e:
                if st.button("📤 ENVIAR", key="conexaom20"):
                    if msg_role.strip():
                        historico_msgs = [{"role":m["role"],"content":m["content"]} for m in st.session_state.roleplay_chat]
                        with st.spinner("..."):
                            try:
                                client = Groq(api_key=st.session_state.api_key)
                                msgs = [{"role":"system","content":st.session_state.roleplay_system}] + historico_msgs + [{"role":"user","content":msg_role}]
                                resp = client.chat.completions.create(messages=msgs, model="openai/gpt-oss-120b")
                                resp_txt = resp.choices[0].message.content
                                if resp_txt: st.session_state['res_cm_conexa1'] = str(resp_txt)
                            except Exception as e:
                                resp_txt = f"⚠️ Erro: {e}"
                        st.session_state.roleplay_chat.append({"role":"user","content":msg_role})
                        st.session_state.roleplay_chat.append({"role":"assistant","content":resp_txt})
                        st.session_state.roleplay_key += 1
                        st.rerun()
            with col_f:
                if st.button("🏁 Finalizar", key="conexaom21"):
                    with st.spinner("Avaliando sua performance..."):
                        hist_txt = "\\n".join(f"{'Usuário' if m['role']=='user' else 'Personagem'}: {m['content']}" for m in st.session_state.roleplay_chat)
                        prompt_aval = (
                            f"Avalie a performance deste usuário na simulação de conversa.\\n"
                            f"Cenário: {st.session_state.get('roleplay_cenario','')}\\n\\n"
                            f"Conversa:\\n{hist_txt}\\n\\n"
                            f"FORMATO:\\n\\n"
                            f"🏆 AVALIAÇÃO DA SIMULAÇÃO\\n\\n"
                            f"| Competência | Nota |\\n|---|---|\\n"
                            f"| 🗣️ Naturalidade | [X]/10 |\\n"
                            f"| 👂 Escuta | [X]/10 |\\n"
                            f"| ❓ Qualidade das perguntas | [X]/10 |\\n"
                            f"| 🔄 Adaptação | [X]/10 |\\n"
                            f"| 🤝 Reciprocidade | [X]/10 |\\n\\n"
                            f"⭐ NOTA GERAL: [X]/10\\n\\n"
                            f"🟢 O QUE VOCÊ FEZ BEM:\\n[feedback específico]\\n\\n"
                            f"🟡 O QUE PODE MELHORAR:\\n[feedback específico]\\n\\n"
                            f"🎯 PRÓXIMO DESAFIO:\\n[o que trabalhar na próxima simulação]"
                        )
                        aval = conexa_ia(prompt_aval)
                        st.session_state.treinos_realizados += 1
                        verificar_conquistas()
                        salvar_historico("Roleplay", st.session_state.get('roleplay_cenario',''), aval)
                        st.session_state['role_aval'] = aval
                        st.session_state.roleplay_ativo = False
                        st.session_state.roleplay_chat = []
                        st.rerun()

        if st.session_state.get('role_aval'):
            st.markdown(f"<div class='avaliacao-box'>{st.session_state['role_aval']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar avaliação (.txt)", data=st.session_state['role_aval'], file_name="avaliacao_roleplay.txt", mime="text/plain", key="dl_conexa_6")


        # ──────────────────────────────────────────
        # A ARTE DA LÁBIA — SISTEMA COMPLETO
        # ──────────────────────────────────────────
        elif st.session_state.pagina == "Labia":
            import time as _t, random as _rand, re as _re2

            PHASES_L = ["Atração", "Conexão", "Sedução"]
            PHASE_EMOJI_L = {"Atração":"🔥","Conexão":"💫","Sedução":"❤️"}
            PHASE_DIFFICULTY_L = {"Atração":"Paquerador","Conexão":"Galanteador","Sedução":"Mestre da Lábia"}
            RANK_ORDER_L = ["Aspirante","Paquerador","Galanteador","Mestre da Lábia"]
            RANK_AFTER_L = {"Atração":"Paquerador","Conexão":"Galanteador","Sedução":"Mestre da Lábia"}
            PASS_THRESHOLD_L = 60
            PHASE_SECONDS_L = 300
            CRITERIA_W = {"naturalidade":0.20,"confianca":0.20,"criatividade":0.15,"conexao":0.20,"humor":0.10,"conducao":0.15}
            CRITERIA_LBL = {"naturalidade":"🗣️ Naturalidade","confianca":"😎 Confiança","criatividade":"🎯 Criatividade","conexao":"🧲 Conexão","humor":"😂 Humor","conducao":"🧭 Condução"}

            CHARACTERS_L = {
                "Rafaela":{"emoji":"👩","estrelas":2,"unlock_rank":None,"pronome":"ela","descricao":"Inteligente, espontânea e seletiva.","bio":"31 anos, designer. Curte cerâmica, filme de terror e café coado. Irônica, direta."},
                "Camila":{"emoji":"👩‍🦰","estrelas":3,"unlock_rank":"Paquerador","pronome":"ela","descricao":"Segura, provocadora, testa confiança.","bio":"27 anos, advogada. Corre 10km, joga xadrez. Detecta puxa-saquismo na hora."},
                "Helena":{"emoji":"👩‍💼","estrelas":5,"unlock_rank":"Galanteador","pronome":"ela","descricao":"Sofisticada, só se abre com quem conquista.","bio":"34 anos, sommelier. Fala 3 idiomas. Fecha se sentir técnica de paquera."},
                "André":{"emoji":"👨","estrelas":2,"unlock_rank":None,"pronome":"ele","descricao":"Comunicativo, reage bem ao humor.","bio":"29 anos, fisioterapeuta. Nota quando alguém é forçado e esfria."},
                "Lucas":{"emoji":"🧑‍🎤","estrelas":3,"unlock_rank":"Paquerador","pronome":"ele","descricao":"Confiante, sarcástico — testa se aguenta provocação.","bio":"26 anos, baixista. Faz cara de tédio se sentir cantada decorada."},
                "Diego":{"emoji":"🕴️","estrelas":5,"unlock_rank":"Galanteador","pronome":"ele","descricao":"Extremamente seletivo, fala pouco mas repara em tudo.","bio":"33 anos, chef. Só reage a quem traz algo genuíno."},
            }

            CENARIOS_L = ["fila de um café badalado","festa de aniversário","sala de espera de workshop","parque","corredor de livraria","show ao ar livre","loja de discos","cozinha de workshop","elevador","mesa comunitária de bar"]

            RANK_STYLE_L = {"Aspirante":{"emoji":"⚪","badge":"badge"},"Paquerador":{"emoji":"🟢","badge":"badge-verde"},"Galanteador":{"emoji":"🟡","badge":"badge-amarelo"},"Mestre da Lábia":{"emoji":"🔴","badge":"badge-roxo"}}

            for k,v in [
                ('ml_estagio','home'),('ml_character',None),('ml_phase_index',0),
                ('ml_phase_start',None),('ml_connexometer',100),('ml_messages',[]),
                ('ml_interaction_scores',[]),('ml_phase_results',{}),
                ('ml_phase_message_start',0),('ml_phase_coachings',{}),
                ('ml_current_rank',"Aspirante"),('ml_cenario',None),
                ('ml_aberturas_usadas',[]),('ml_historico',[]),('ml_last_result',None),
                ('ml_response_since',None),
            ]:
                if k not in st.session_state: st.session_state[k] = v

            def ml_reset(keep_char=False):
                for k in ['ml_phase_index','ml_phase_start','ml_connexometer','ml_messages',
                          'ml_interaction_scores','ml_phase_results','ml_phase_message_start',
                          'ml_phase_coachings','ml_cenario','ml_last_result','ml_response_since']:
                    st.session_state[k] = {'ml_phase_index':0,'ml_phase_start':None,'ml_connexometer':100,
                        'ml_messages':[],'ml_interaction_scores':[],'ml_phase_results':{},
                        'ml_phase_message_start':0,'ml_phase_coachings':{},'ml_cenario':None,
                        'ml_last_result':None,'ml_response_since':None}[k]
                st.session_state.ml_current_rank = "Aspirante"
                if not keep_char: st.session_state.ml_character = None
                st.session_state.ml_estagio = "home"

            def ml_maior_rank():
                melhor = 0
                for h in st.session_state.ml_historico:
                    rk = h.get("rank_final","Aspirante")
                    if rk in RANK_ORDER_L: melhor = max(melhor, RANK_ORDER_L.index(rk))
                return RANK_ORDER_L[melhor]

            def ml_desbloqueado(nome):
                info = CHARACTERS_L[nome]
                if info["unlock_rank"] is None: return True
                return RANK_ORDER_L.index(ml_maior_rank()) >= RANK_ORDER_L.index(info["unlock_rank"])

            def ml_weighted(av):
                return sum(av[k]*CRITERIA_W[k] for k in CRITERIA_W)

            def ml_avg(lista):
                if not lista: return {k:60 for k in CRITERIA_W}
                return {k: sum(a[k] for a in lista)/len(lista) for k in CRITERIA_W}

            def ml_build_system(character, difficulty, phase):
                char = CHARACTERS_L[character]
                cenario = st.session_state.ml_cenario or "situação social casual"
                phase_ctx = {"Atração":f"FASE 1 — ATRAÇÃO. Vocês se conheceram em: {cenario}. Desperte interesse com leveza.","Conexão":"FASE 2 — CONEXÃO. Aprofunde: histórias, valores, personalidade.","Sedução":"FASE 3 — SEDUÇÃO. Tensão romântica sutil. Se grosseiro, recue."}[phase]
                diff_ctx = {"Paquerador":"Nível fácil: seja receptivo, ajude a conversa.","Galanteador":"Nível médio: seja seletivo, responda curto às vezes.","Mestre da Lábia":"Nível difícil: não facilite, teste a confiança."}[difficulty]
                return f\"\"\"Você é {character}. {char['descricao']}
BIOGRAFIA: {char['bio']}
{phase_ctx}
{diff_ctx}
REGRAS: Respostas CURTAS (1 frase). Use detalhes específicos da bio. NUNCA revele que é IA.
Após sua fala, avalie 0-100: naturalidade, confianca, criatividade, conexao, humor, conducao. Delta -15 a 15.
JSON: {{"resposta":"fala","avaliacao":{{"naturalidade":0,"confianca":0,"criatividade":0,"conexao":0,"humor":0,"conducao":0}},"delta_conexometro":0}}\"\"\"

            def ml_call_ai(character, difficulty, phase, history, user_msg=None, opening=False):
                from groq import Groq as _GrML
                client = _GrML(api_key=st.session_state.api_key)
                system = ml_build_system(character, difficulty, phase)
                cenario = st.session_state.ml_cenario or "situação social casual"
                bloq = ""
                if opening and st.session_state.ml_aberturas_usadas:
                    lista = " | ".join(f'"{a}"' for a in st.session_state.ml_aberturas_usadas[-5:])
                    bloq = f"NÃO repita: {lista}."
                opening_prompt = f"Gere sua fala de abertura no cenário: {cenario}. Curta, com personalidade. {bloq} JSON de sempre com zeros."
                msgs = [{"role":"system","content":system}]
                for m in history:
                    msgs.append({"role":"assistant" if m["role"]=="assistant" else "user","content":m["content"]})
                msgs.append({"role":"user","content":opening_prompt if opening else user_msg})
                for attempt in range(3):
                    try:
                        kwargs = dict(model="openai/gpt-oss-120b",messages=msgs,temperature=0.9,max_tokens=350)
                        if attempt==0: kwargs["response_format"]={"type":"json_object"}
                        resp = client.chat.completions.create(**kwargs)
                        raw = resp.choices[0].message.content
                        if raw: st.session_state['res_cm_conexa2'] = str(raw)
                        try: data = import_json_ml(raw)
                        except:
                            s,e2 = raw.find("{"),raw.rfind("}")
                            data = import_json_ml(raw[s:e2+1]) if s!=-1 and e2>s else {}
                        resposta = (data.get("resposta") or "").strip()
                        av = data.get("avaliacao",{})
                        for k in CRITERIA_W: av[k] = max(0,min(100,int(av.get(k,50))))
                        delta = max(-15,min(15,int(data.get("delta_conexometro",0))))
                        if len(resposta.strip(".\\n"))<2: raise ValueError("vazia")
                        return resposta, av, delta
                    except: continue
                return "Opa, o que você ia dizer?", {k:50 for k in CRITERIA_W}, 0

            import json as import_json_ml_mod
            def import_json_ml(s): return import_json_ml_mod.loads(s)

            def ml_coaching(character, phase, phase_msgs, scores):
                if not phase_msgs: return "Você não respondeu nesta fase."
                conv = "\\n".join(f"{'Você' if m['role']=='user' else character}: {m['content']}" for m in phase_msgs)
                fracos = ", ".join(f"{CRITERIA_LBL[k]} ({int(v)}/100)" for k,v in sorted(scores.items(),key=lambda x:x[1])[:3] if v<70)
                fortes = ", ".join(f"{CRITERIA_LBL[k]} ({int(v)}/100)" for k,v in sorted(scores.items(),key=lambda x:x[1],reverse=True)[:2])
                try:
                    from groq import Groq as _GrCo
                    client = _GrCo(api_key=st.session_state.api_key)
                    prompt = (f"Coach — fase '{phase}' com {character}.\\nConversa:\\n{conv}\\n\\nFracos:{fracos or 'nenhum'}\\nFortes:{fortes}\\n\\n"
                             f"Feedback direto citando exemplos REAIS. Máx 180 palavras.\\n🔴 O QUE NÃO FUNCIONOU:\\n🟢 O QUE FUNCIONOU:\\n💡 PARA SUBIR DE NÍVEL:")
                    r = client.chat.completions.create(model="openai/gpt-oss-120b",messages=[{"role":"user","content":prompt}],temperature=0.6,max_tokens=600)
                    return r.choices[0].message.content.strip()
                except: return "Não foi possível gerar feedback."

            estagio_l = st.session_state.ml_estagio

            # ── HOME ──
            if estagio_l == "home":
                st.markdown("## 👑 Mestre da Lábia")
                st.markdown("*Você não vai aprender o que dizer — vai aprender a conversar.*")
                st.markdown(\"\"\"<div class='card'>
                🔥 <strong>Fase 1 — Atração</strong> → <span class='badge-verde'>🟢 Paquerador</span><br>
                💫 <strong>Fase 2 — Conexão</strong> → <span class='badge-amarelo'>🟡 Galanteador</span><br>
                ❤️ <strong>Fase 3 — Sedução</strong> → <span class='badge-roxo'>🔴 Mestre da Lábia</span>
                </div>\"\"\", unsafe_allow_html=True)
                if st.session_state.ml_historico:
                    st.markdown("### 🕐 Últimos treinos")
                    for item in reversed(st.session_state.ml_historico[-4:]):
                        rk2 = RANK_STYLE_L.get(item.get("rank_final","Aspirante"),RANK_STYLE_L["Aspirante"])
                        _rk2b = rk2["badge"]; _rk2e = rk2['emoji']
                        st.markdown(f"<div class='card'><span class='badge'>{item['personagem']}</span> <span class='{_rk2b}'>{_rk2e} {item.get('rank_final','Aspirante')}</span> <small style='color:#888'>{item['data']}</small> — <strong>{item.get('overall', 0)}/100</strong></div>",unsafe_allow_html=True)
                col_c = st.columns([1,2,1])[1]
                with col_c:
                    if st.button("🔥 COMEÇAR TREINAMENTO", use_container_width=True, key="ml_iniciar"):
                        ml_reset(); st.session_state.ml_estagio="character"; st.rerun()

            # ── ESCOLHA DE PERSONAGEM ──
            elif estagio_l == "character":
                st.markdown("### 🎭 Escolha sua personagem")
                rank_at = ml_maior_rank()
                rk_at = RANK_STYLE_L[rank_at]
                _rkat_b = rk_at["badge"]; _rkat_e = rk_at['emoji']
                st.markdown(f"Seu maior rank: <span class='{_rkat_b}'>{_rkat_e} {rank_at}</span>",unsafe_allow_html=True)
                cols_p = st.columns(3)
                for i,(nome_p2,info_p) in enumerate(CHARACTERS_L.items()):
                    col_p = cols_p[i%3]
                    desbloq = ml_desbloqueado(nome_p2)
                    estrelas = "⭐"*info_p["estrelas"]+"☆"*(5-info_p["estrelas"])
                    with col_p:
                        if desbloq:
                            st.markdown(f"<div class='card' style='text-align:center;'><div style='font-size:2em;'>{info_p['emoji']}</div><div style='font-weight:700;'>{nome_p2}</div><div style='color:#F5C542;'>{estrelas}</div><div style='font-size:0.8em;'>{info_p['descricao']}</div></div>",unsafe_allow_html=True)
                            if st.button(f"Escolher {nome_p2}", key=f"ml_char_{nome_p2}", use_container_width=True):
                                st.session_state.ml_character = nome_p2
                                ml_reset(keep_char=True)
                                st.session_state.ml_cenario = _rand.choice(CENARIOS_L)
                                st.session_state.ml_estagio = "training"
                                st.rerun()
                        else:
                            unlock_rk2 = RANK_STYLE_L[info_p["unlock_rank"]]
                            _urk2b = unlock_rk2["badge"]; _urk2e = unlock_rk2['emoji']
                            st.markdown(f"<div class='card' style='text-align:center;opacity:.5;'><div style='font-size:2em;'>🔒</div><div style='font-weight:700;'>{nome_p2}</div><div style='color:#F5C542;'>{estrelas}</div><div style='font-size:0.8em;'>{info_p['descricao']}</div><div style='font-size:0.75em;'>Desbloqueia com <span class='{_urk2b}'>{_urk2e} {info_p['unlock_rank']}</span></div></div>",unsafe_allow_html=True)
                            st.button("🔒 Bloqueada", key=f"ml_locked_{nome_p2}", use_container_width=True, disabled=True)

            # ── TREINAMENTO ──
            elif estagio_l == "training":
                phase = PHASES_L[st.session_state.ml_phase_index]
                character = st.session_state.ml_character
                difficulty = PHASE_DIFFICULTY_L[phase]

                if st.session_state.ml_phase_start is None:
                    st.session_state.ml_phase_start = _t.time()
                    if phase=="Atração" and not st.session_state.ml_messages:
                        with st.spinner(f"{character} está chegando..."):
                            resp_op,_av_op,_d_op = ml_call_ai(character,difficulty,phase,[],opening=True)
                        st.session_state.ml_messages.append({"role":"assistant","content":resp_op})
                        st.session_state.ml_aberturas_usadas = (st.session_state.ml_aberturas_usadas+[resp_op])[-10:]
                        st.session_state.ml_response_since = _t.time()

                elapsed  = _t.time()-st.session_state.ml_phase_start
                remaining= max(0,PHASE_SECONDS_L-elapsed)
                mins_r   = int(remaining//60); segs_r=int(remaining%60)
                rk2 = RANK_STYLE_L[st.session_state.ml_current_rank]
                st.markdown(f"<h4>{PHASE_EMOJI_L[phase]} FASE {st.session_state.ml_phase_index+1} — {phase.upper()}</h4>",unsafe_allow_html=True)
                _rk2b2 = rk2["badge"]; _rk2e2 = rk2['emoji']
                st.markdown(f"<span class='{_rk2b2}'>{_rk2e2} {st.session_state.ml_current_rank}</span> <span class='badge'>{CHARACTERS_L[character]['emoji']} {character}</span>",unsafe_allow_html=True)

                cx = st.session_state.ml_connexometer
                cor_cx = "#22C55E" if cx>70 else ("#84CC16" if cx>50 else ("#F59E0B" if cx>30 else "#EF4444"))
                pulso = "animation:pulso 0.8s ease-in-out infinite;" if cx<=20 else ""
                cor_t2 = "#22C55E" if remaining>60 else ("#F59E0B" if remaining>20 else "#EF4444")
                st.markdown(f"<style>@keyframes pulso{{0%,100%{{opacity:1}}50%{{opacity:.4}}}}</style><div style='display:flex;align-items:center;gap:10px;padding:8px 12px;background:#fff;border:2px solid #22C55E;border-radius:10px;margin-bottom:8px;'><span style='font-size:0.7em;color:#64748B;font-weight:600;'>❤️ CONEXÔMETRO</span><div style='flex:1;background:#F1F5F9;border-radius:999px;height:10px;'><div style='height:100%;border-radius:999px;background:{cor_cx};width:{cx}%;{pulso}'></div></div><span style='font-weight:700;color:{cor_cx};'>{cx}%</span><span style='border-left:1px solid #E2E8F0;padding-left:10px;font-weight:700;color:{cor_t2};'>⏱️ {mins_r:02d}:{segs_r:02d}</span></div>",unsafe_allow_html=True)

                for m in st.session_state.ml_messages:
                    css = "chat-persona" if m["role"]=="assistant" else "chat-user"
                    autor = f"{CHARACTERS_L[character]['emoji']} {character}" if m["role"]=="assistant" else "🙂 Você"
                    st.markdown(f"<div class='{css}'><strong>{autor}:</strong><br>{m['content']}</div>",unsafe_allow_html=True)

                if remaining<=0:
                    scores = st.session_state.ml_interaction_scores
                    avg = ml_avg(scores)
                    score = round(ml_weighted(avg))
                    passou = score>=PASS_THRESHOLD_L
                    st.session_state.ml_phase_results[phase]={"score":score,"scores":avg,"passou":passou}
                    phase_msgs = st.session_state.ml_messages[st.session_state.ml_phase_message_start:]
                    with st.spinner("Analisando..."):
                        coaching = ml_coaching(character,phase,phase_msgs,avg)
                    st.session_state.ml_phase_coachings[phase]=coaching
                    st.session_state.ml_interaction_scores=[]
                    st.session_state.ml_estagio="phase_end"; st.rerun()
                else:
                    msg_in = st.text_input("",key=f"ml_in_{len(st.session_state.ml_messages)}",placeholder="Digite sua resposta...",label_visibility="collapsed")
                    col_env2,col_sair2 = st.columns([4,1])
                    with col_env2:
                        if st.button("📤 ENVIAR", key="ml_env", use_container_width=True):
                            if msg_in.strip():
                                st.session_state.ml_messages.append({"role":"user","content":msg_in})
                                with st.spinner(f"{character} está digitando..."):
                                    resp2,av2,delta2 = ml_call_ai(character,difficulty,phase,st.session_state.ml_messages[:-1],user_msg=msg_in)
                                st.session_state.ml_messages.append({"role":"assistant","content":resp2})
                                st.session_state.ml_interaction_scores.append(av2)
                                resp_t = (_t.time()-st.session_state.ml_response_since) if st.session_state.ml_response_since else 0
                                pen = 12 if resp_t>45 else (8 if resp_t>30 else (4 if resp_t>15 else 0))
                                st.session_state.ml_connexometer = max(0,min(100,cx+delta2-pen))
                                # Penalidade de silêncio
                                blocos = int(resp_t//25) if resp_t else 0
                                if blocos>0:
                                    queda_sil = blocos*25
                                    st.session_state.ml_connexometer = max(0,st.session_state.ml_connexometer-queda_sil)
                                st.session_state.ml_response_since = _t.time()
                                st.rerun()
                    with col_sair2:
                        if st.button("🚩 Sair",key="ml_sair",use_container_width=True):
                            ml_reset(); st.rerun()
                    _t.sleep(1); st.rerun()

            # ── FIM DE FASE ──
            elif estagio_l == "phase_end":
                phase = PHASES_L[st.session_state.ml_phase_index]
                result = st.session_state.ml_phase_results.get(phase,{"score":0,"scores":{},"passou":False})
                score2,scores2,passou2 = result["score"],result["scores"],result["passou"]
                coaching2 = st.session_state.ml_phase_coachings.get(phase,"")
                st.markdown(f"<h3 style='text-align:center;'>{PHASE_EMOJI_L[phase]} {phase.upper()} — CONCLUÍDA</h3>",unsafe_allow_html=True)
                st.markdown(f"<h1 style='text-align:center;'>{score2}/100</h1>",unsafe_allow_html=True)
                st.caption(f"Nota de corte: {PASS_THRESHOLD_L}/100")
                if passou2:
                    novo_rank2 = RANK_AFTER_L[phase]
                    st.session_state.ml_current_rank = novo_rank2
                    rk3 = RANK_STYLE_L[novo_rank2]
                    _rk3b = rk3["badge"]; _rk3e = rk3['emoji']
                    st.markdown(f"<div class='card' style='text-align:center;'><h3>🎉 VOCÊ PASSOU!</h3><h2><span class='{_rk3b}'>{_rk3e} {novo_rank2.upper()}</span></h2></div>",unsafe_allow_html=True)
                else:
                    rk_at2 = RANK_STYLE_L[st.session_state.ml_current_rank]
                    _rkat2b = rk_at2["badge"]; _rkat2e = rk_at2['emoji']
                    st.markdown(f"<div class='card' style='text-align:center;'><h3>❌ NÃO PASSOU DESTA VEZ</h3><p>Você continua <span class='{_rkat2b}'>{_rkat2e} {st.session_state.ml_current_rank}</span></p></div>",unsafe_allow_html=True)
                if coaching2:
                    st.markdown(f"<div class='card'>{coaching2}</div>",unsafe_allow_html=True)
                st.markdown("<hr class='divider'>",unsafe_allow_html=True)
                is_last = st.session_state.ml_phase_index>=len(PHASES_L)-1
                encerrar = (not passou2) or is_last
                label_btn = "🏆 VER RESULTADO FINAL" if encerrar else f"{PHASE_EMOJI_L[PHASES_L[st.session_state.ml_phase_index+1]]} PRÓXIMA FASE"
                if st.button(label_btn, use_container_width=True, key="ml_prox"):
                    if encerrar:
                        all_scores2 = [r["scores"] for r in st.session_state.ml_phase_results.values()]
                        avg2 = ml_avg(all_scores2)
                        overall2 = round(ml_weighted(avg2))
                        entry2 = {"data":datetime.now().strftime("%d/%m/%Y %H:%M"),"personagem":st.session_state.ml_character,"rank_final":st.session_state.ml_current_rank,"treino_completo":passou2 and is_last,"overall":overall2,"fases":{p2:r2["score"] for p2,r2 in st.session_state.ml_phase_results.items()},"criterios":avg2}
                        st.session_state.ml_historico.append(entry2)
                        st.session_state.ml_last_result = entry2
                        st.session_state.ml_estagio = "final"
                    else:
                        st.session_state.ml_phase_index += 1
                        st.session_state.ml_phase_start = None
                        st.session_state.ml_phase_message_start = len(st.session_state.ml_messages)
                        st.session_state.ml_estagio = "training"
                    st.rerun()

            # ── RESULTADO FINAL ──
            elif estagio_l == "final":
                entry3 = st.session_state.ml_last_result
                if not entry3:
                    st.session_state.ml_estagio="home"; st.rerun()
                else:
                    rk4 = RANK_STYLE_L.get(entry3.get("rank_final","Aspirante"),RANK_STYLE_L["Aspirante"])
                    st.markdown(f"<h2 style='text-align:center;'>{'🏆 TREINO COMPLETO!' if entry3.get('treino_completo') else 'Resultado'}</h2>",unsafe_allow_html=True)
                    st.markdown(f"<h1 style='text-align:center;font-size:4em;'>{entry3['overall']}</h1>",unsafe_allow_html=True)
                    _rk4b = rk4["badge"]; _rk4e = rk4['emoji']
                    st.markdown(f"<h3 style='text-align:center;'><span class='{_rk4b}'>{_rk4e} {entry3['rank_final'].upper()}</span></h3>",unsafe_allow_html=True)
                    st.markdown("<hr class='divider'>",unsafe_allow_html=True)
                    c1f,c2f,c3f = st.columns(3)
                    c1f.metric("🔥 Atração",entry3["fases"].get("Atração","—"))
                    c2f.metric("💫 Conexão",entry3["fases"].get("Conexão","—"))
                    c3f.metric("❤️ Sedução",entry3["fases"].get("Sedução","—"))
                    col_r1,col_r2 = st.columns(2)
                    with col_r1:
                        if st.button("🔄 Jogar Novamente",use_container_width=True,key="ml_replay"):
                            ml_reset(); st.session_state.ml_estagio="character"; st.rerun()
                    with col_r2:
                        if st.button("🏠 Voltar",use_container_width=True,key="ml_home_final"):
                            ml_reset(); st.rerun()

        elif st.session_state.pagina == "Biblioteca":
            st.header("📚 Biblioteca Inteligente")
            categorias = ["Todas","Respostas","Cartas na Manga","Mensagens Turbinadas","Análises","Primeiras conversas","Amizade","Networking","Perguntas"]
            filtro = st.selectbox("Filtrar:", categorias, key="filtro_bib")
            bib = st.session_state.biblioteca
            if filtro != "Todas":
                bib = [b for b in bib if b.get('categoria','') == filtro]
            if not bib:
                st.info("Nenhum item salvo nesta categoria ainda.")
            else:
                st.markdown(f"**{len(bib)} item(ns) encontrado(s)**")
                for i, item in enumerate(reversed(bib)):
                    idx = len(st.session_state.biblioteca) - 1 - i
                    with st.expander(f"[{item.get('categoria','')}] {item['conteudo'][:60]}... — {item['data']}"):
                        st.markdown(f"<div class='card'>{item['conteudo']}</div>", unsafe_allow_html=True)
                        col_dl, col_del = st.columns([3,1])
                        with col_dl:
                            st.download_button("📋 Baixar", data=item['conteudo'], file_name="item_biblioteca.txt", mime="text/plain", key=f"dl_bib_{i}")
                        with col_del:
                            if st.button("🗑️", key=f"del_bib_{i}"):
                                st.session_state.biblioteca.pop(idx); st.rerun()

        # ──────────────────────────────────────────
        # LEITOR DE PERFIL
        # ──────────────────────────────────────────
        elif st.session_state.pagina == "Perfil":
            st.header("📸 Leitor de Perfil")
            st.markdown("*Analisa informações públicas e sugere assuntos de conversa.*")
            st.markdown(\"\"\"<div class='card-yellow'>⚠️ <strong>Limite ético:</strong> A IA trabalha APENAS com informações fornecidas por você.
            Não determina personalidade por aparência. Não afirma intenções. Não diagnostica.
            Use apenas informações públicas.</div>\"\"\", unsafe_allow_html=True)

            bio_perfil = st.text_area("📋 Informações do perfil (bio, posts, interesses):", height=150, placeholder="ex: 'Viajante apaixonada. Fotógrafa nas horas vagas. Amo trilhas e café ☕'", key="conexaom22")
            nome_perfil = st.text_input("Nome (opcional):", placeholder="ex: Marina", key="conexaom23")
            contexto_perfil = st.text_input("Como vocês se conheceram:", placeholder="ex: seguimos um ao outro, colega de trabalho, amigo em comum...", key="conexaom24")

            if st.button("📸 ANALISAR PERFIL", key="conexaom25"):
                if bio_perfil.strip():
                    with st.spinner("Analisando..."):
                        prompt = (
                            f"Analise as informações públicas deste perfil e sugira assuntos para conversa.\\n"
                            f"Nome: {nome_perfil or 'não informado'}. Bio/informações: {bio_perfil}. Contexto: {contexto_perfil or 'não informado'}.\\n\\n"
                            f"REGRAS ABSOLUTAS:\\n"
                            f"- NÃO determine personalidade por aparência\\n- NÃO afirme intenções ou sentimentos\\n"
                            f"- Trabalhe APENAS com informações fornecidas\\n\\n"
                            f"FORMATO:\\n\\n"
                            f"🎯 INTERESSES IDENTIFICADOS:\\n[o que é explicitamente visível nas informações]\\n\\n"
                            f"💬 ASSUNTOS PARA CONVERSA:\\n[lista de 5-7 assuntos com base nos interesses]\\n\\n"
                            f"❓ PERGUNTAS NATURAIS:\\n[3-5 perguntas abertas relacionadas aos interesses]\\n\\n"
                            f"🧩 ELEMENTOS DA BIO QUE PODEM GERAR ASSUNTO:\\n[análise dos elementos específicos]\\n\\n"
                            f"💡 COMO INICIAR A CONVERSA:\\n[2-3 aberturas naturais baseadas no perfil]"
                        )
                        res = conexa_ia(prompt)
                        salvar_historico("Leitor de Perfil", bio_perfil[:60], res)
                        st.session_state['perfil_temp'] = res
                else:
                    st.warning("Cole as informações do perfil.")

            if st.session_state.get('perfil_temp'):
                st.markdown(f"<div class='card'>{st.session_state['perfil_temp']}</div>", unsafe_allow_html=True)

        # ──────────────────────────────────────────
        # COMPARAR CONVERSAS
        # ──────────────────────────────────────────
        elif st.session_state.pagina == "Comparar":
            st.header("⚔️ Comparar Duas Conversas")
            col1, col2 = st.columns(2)
            with col1:
                conv_a = st.text_area("💬 Conversa A:", height=180, placeholder="Cole a primeira conversa...", key="conexaom26")
            with col2:
                conv_b = st.text_area("💬 Conversa B:", height=180, placeholder="Cole a segunda conversa...", key="conexaom27")

            if st.button("⚔️ COMPARAR", key="conexaom28"):
                if conv_a.strip() and conv_b.strip():
                    with st.spinner("Comparando..."):
                        prompt = (
                            f"Compare estas duas conversas.\\n\\nConversa A:\\n{conv_a}\\n\\nConversa B:\\n{conv_b}\\n\\n"
                            f"FORMATO:\\n\\n"
                            f"🧠 COMPARAÇÃO\\n\\n"
                            f"| Critério | A | B |\\n|---|---|---|\\n"
                            f"| Clareza | [nota] | [nota] |\\n"
                            f"| Naturalidade | [nota] | [nota] |\\n"
                            f"| Reciprocidade | [nota] | [nota] |\\n"
                            f"| Fluidez | [nota] | [nota] |\\n"
                            f"| Qualidade das perguntas | [nota] | [nota] |\\n\\n"
                            f"🏆 MELHOR DINÂMICA:\\n[qual e por quê — baseado em padrões observáveis]\\n\\n"
                            f"💡 O QUE A MELHOR CONVERSA FEZ DIFERENTE:\\n[lições práticas]"
                        )
                        res = conexa_ia(prompt)
                        salvar_historico("Comparação", "Conversa A vs B", res)
                        st.session_state['comp_temp'] = res
                else:
                    st.warning("Cole as duas conversas.")

            if st.session_state.get('comp_temp'):
                st.markdown(st.session_state['comp_temp'])

        # ──────────────────────────────────────────
        # PLANO 7 DIAS
        # ──────────────────────────────────────────
        elif st.session_state.pagina == "Plano":
            st.header("🗓️ Plano de Evolução — 7 Dias")

            foco_plano = st.text_input("Qual aspecto da comunicação você mais quer desenvolver?",
                placeholder="ex: fazer perguntas melhores, não travar no início da conversa, lidar com silêncio...")

            if st.button("🗓️ GERAR MEU PLANO", key="conexaom29"):
                with st.spinner("Criando seu plano personalizado..."):
                    prompt = (
                        f"Crie um plano de desenvolvimento de comunicação de 7 dias.\\n"
                        f"Foco principal: {foco_plano or 'desenvolvimento geral'}.\\n\\n"
                        f"Para cada dia:\\n\\n"
                        f"📅 DIA [N] — [TEMA]\\n"
                        f"🎯 Objetivo do dia: [o que desenvolver]\\n"
                        f"📖 Conceito: [explicação simples]\\n"
                        f"💪 Exercício prático: [tarefa concreta que pode ser feita hoje]\\n"
                        f"⭐ Critério de sucesso: [como saber se conseguiu]\\n\\n"
                        f"[repita para 7 dias]\\n\\n"
                        f"🏆 DIA 7 — DESAFIO FINAL:\\n[simulação completa integrando tudo]"
                    )
                    res = conexa_ia(prompt)
                    st.session_state.plano_conquista = res
                    salvar_historico("Plano 7 Dias", foco_plano[:60] if foco_plano else "Geral", res)
                    st.session_state['plano_temp'] = res

            if st.session_state.get('plano_temp'):
                st.markdown(f"<div class='card'>{st.session_state['plano_temp']}</div>", unsafe_allow_html=True)
                st.download_button("📋 Baixar plano (.txt)", data=st.session_state['plano_temp'], file_name="plano_7dias.txt", mime="text/plain", key="dl_conexa_7")

        # ──────────────────────────────────────────
        # PROGRESSO
        # ──────────────────────────────────────────
        elif st.session_state.pagina == "Progresso":
            st.header("📈 Minha Evolução")

            # Atualizar métricas manualmente
            st.markdown("### 📊 Atualizar Evolução")
            st.markdown("*Após cada sessão de treino, atualize suas métricas.*")
            col1, col2 = st.columns(2)
            with col1:
                nova_clareza = st.slider("Clareza:", 0, 10, st.session_state.clareza)
                nova_naturalidade = st.slider("Naturalidade:", 0, 10, st.session_state.naturalidade)
                nova_reciprocidade = st.slider("Reciprocidade:", 0, 10, st.session_state.reciprocidade)
            with col2:
                nova_confianca = st.slider("Confiança:", 0, 10, st.session_state.confianca)
                nova_escuta = st.slider("Escuta:", 0, 10, st.session_state.escuta)

            if st.button("💾 SALVAR EVOLUÇÃO", key="conexaom30"):
                st.session_state.clareza = nova_clareza
                st.session_state.naturalidade = nova_naturalidade
                st.session_state.reciprocidade = nova_reciprocidade
                st.session_state.confianca = nova_confianca
                st.session_state.escuta = nova_escuta
                salvar_cache(st.session_state.usuario)
                st.success("✅ Evolução salva!")

            st.markdown("<hr class='divider'>", unsafe_allow_html=True)
            st.markdown("### 📊 Desempenho Geral")
            c1,c2,c3,c4,c5 = st.columns(5)
            for col, nome_m, val in [(c1,"Clareza",st.session_state.clareza),(c2,"Naturalidade",st.session_state.naturalidade),(c3,"Reciprocidade",st.session_state.reciprocidade),(c4,"Confiança",st.session_state.confianca),(c5,"Escuta",st.session_state.escuta)]:
                col.markdown(f"<div class='stat-box'><div class='stat-numero'>{val}</div><div>{nome_m}</div></div>", unsafe_allow_html=True)

            st.markdown("<hr class='divider'>", unsafe_allow_html=True)
            col_a, col_b, col_c = st.columns(3)
            col_a.markdown(f"<div class='stat-box'><div class='stat-numero'>{st.session_state.conversas_analisadas}</div><div>Conversas analisadas</div></div>", unsafe_allow_html=True)
            col_b.markdown(f"<div class='stat-box'><div class='stat-numero'>{st.session_state.treinos_realizados}</div><div>Treinos realizados</div></div>", unsafe_allow_html=True)
            col_c.markdown(f"<div class='stat-box'><div class='stat-numero'>{st.session_state.labia_nivel}</div><div>Nível Arte da Lábia</div></div>", unsafe_allow_html=True)

        # ──────────────────────────────────────────
        # RESUMO SEMANAL
        # ──────────────────────────────────────────
        elif st.session_state.pagina == "Resumo":
            st.header("📋 Relatório Semanal")

            if st.button("📋 GERAR RELATÓRIO", key="conexaom31"):
                with st.spinner("Gerando relatório..."):
                    prompt = (
                        f"Crie um relatório semanal de evolução em comunicação.\\n"
                        f"Dados: {st.session_state.conversas_analisadas} conversas analisadas, "
                        f"{st.session_state.mensagens_aprimoradas} mensagens turbinadas, "
                        f"{st.session_state.treinos_realizados} treinos, "
                        f"{st.session_state.cartas_usadas} cartas usadas.\\n"
                        f"Métricas: Clareza {st.session_state.clareza}/10, Naturalidade {st.session_state.naturalidade}/10, "
                        f"Reciprocidade {st.session_state.reciprocidade}/10, Confiança {st.session_state.confianca}/10, Escuta {st.session_state.escuta}/10.\\n"
                        f"Nível Arte da Lábia: {st.session_state.labia_nivel}/7.\\n\\n"
                        f"FORMATO:\\n\\n"
                        f"📋 RELATÓRIO SEMANAL — {st.session_state.usuario.upper()}\\n\\n"
                        f"🧠 O QUE A IA PERCEBEU:\\n"
                        f"Maior avanço: [gerado automaticamente]\\n"
                        f"Ponto de atenção: [gerado automaticamente]\\n"
                        f"Comportamento funcionando: [gerado automaticamente]\\n"
                        f"Próximo desafio: [gerado automaticamente]\\n\\n"
                        f"💡 INSIGHT DA SEMANA:\\n[frase personalizada baseada nos dados]\\n\\n"
                        f"🎯 OBJETIVOS PARA A PRÓXIMA SEMANA:\\n[3 metas específicas]"
                    )
                    res = conexa_ia(prompt)
                    st.session_state.resumo_semanal = res
                    salvar_historico("Resumo Semanal", "Relatório automático", res)
                    st.session_state['resumo_temp'] = res

            if st.session_state.get('resumo_temp') or st.session_state.resumo_semanal:
                txt = st.session_state.get('resumo_temp') or st.session_state.resumo_semanal
                st.markdown(f"<div class='card'>{txt}</div>", unsafe_allow_html=True)
                st.download_button("📋 Baixar relatório (.txt)", data=txt, file_name="relatorio_semanal.txt", mime="text/plain", key="dl_conexa_10")

        # ──────────────────────────────────────────
        # CONQUISTAS
        # ──────────────────────────────────────────
        elif st.session_state.pagina == "Conquistas":
            st.header("🏆 Conquistas")
            conquistadas = st.session_state.get('conquistas', [], key="dl_conexa_12")
            total = len(CONQUISTAS_DEF, key="dl_conexa_13")
            obtidas = len(conquistadas, key="dl_conexa_14")
            st.markdown(f"**{obtidas} de {total} conquistas desbloqueadas**")
            st.progress(obtidas / total if total > 0 else 0)

            novas = verificar_conquistas()
            if novas:
                for nc in novas:
                    nome_c = next((n for ch,n,_ in CONQUISTAS_DEF if ch==nc), nc)
                    st.success(f"🏆 Nova conquista: {nome_c}!")

            cols_c = st.columns(3)
            for i, (chave, nome, desc) in enumerate(CONQUISTAS_DEF):
                obtida = chave in conquistadas
                estilo = "border:2px solid #FF69B4;" if obtida else "opacity:0.4;border:1px solid #E2E8F0;"
                icon = "🏆" if obtida else "🔒"
                with cols_c[i % 3]:
                    st.markdown(f"<div class='conquista-item' style='{estilo}'>"
                        f"<div style='font-size:1.3em;'>{icon}</div>"
                        f"<div style='font-weight:700;font-size:0.88em;color:#1A1A2E;'>{nome}</div>"
                        f"<div style='font-size:0.75em;color:#6B7280;'>{desc}</div>"
                        f"</div>", unsafe_allow_html=True)

# --- RODAPÉ ---
st.markdown(
    "<div style='text-align:center;color:#999;font-size:0.8em;margin-top:60px;'>"
    "© 2026 Conexão Magnética 2026 — Inteligência para Conversas · MeusAgentesIA.com.br"
    "</div>", unsafe_allow_html=True
)

# --- RODAPÉ ---
st.markdown(
    "<div style='text-align:center;color:#999;font-size:0.8em;margin-top:60px;'>"
    "</div>", unsafe_allow_html=True
)

# --- RODAPÉ ---
st.markdown(
    "<div style='text-align:center;color:#999;font-size:0.8em;margin-top:60px;'>"
    "</div>", unsafe_allow_html=True
)

# --- RODAPÉ ---
st.markdown(
    "<div style='text-align:center;color:#999;font-size:0.8em;margin-top:60px;'>"
    "</div>", unsafe_allow_html=True
)
""",
    "invencoes_ia": """# [hub] import streamlit as st
# [hub] from groq import Groq
# [hub] from datetime import datetime
# [hub] import json
# [hub] import re

# --- CONFIGURAÇÃO DA PÁGINA ---
# set_page_config removido pelo super_agente

st.markdown(\"\"\"
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
[data-testid="stToolbar"] {visibility: hidden;}
[data-testid="stDecoration"] {visibility: hidden;}
[data-testid="stStatusWidget"] {visibility: hidden;}
</style>
\"\"\", unsafe_allow_html=True)


# --- ESTILO CSS ---
st.markdown(\"\"\"
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    .stApp { background-color:#F6FBF4; font-family:'Inter',sans-serif; }
    [data-testid="stSidebar"] { display:none; }

    .stTextInput>div>div>input, .stTextArea>div>textarea,
    .stSelectbox>div>div>div, .stNumberInput>div>div>input {
        background-color:#FFFFFF !important; color:#1A1A2E !important;
        border:1px solid #CED4DA !important; font-family:'Inter',sans-serif !important;
    }

    .stButton>button {
        width:100%; border-radius:10px; height:3.2em;
        background:linear-gradient(135deg,#16A34A,#15803D) !important; color:white !important;
        font-weight:600; border:none; box-shadow:2px 2px 8px rgba(0,0,0,0.1);
        font-family:'Inter',sans-serif !important; transition:all 0.2s ease;
    }
    .stButton>button:hover { background:linear-gradient(135deg,#15803D,#166534) !important; transform:translateY(-1px); }
    .stApp .stButton>button, .stApp .stButton>button p,
    .stApp .stButton>button span, .stApp .stButton>button div { color:white !important; }

    .stApp h1, .stApp h2, .stApp h3 { color:#14532D !important; font-family:'Inter',sans-serif !important; font-weight:700 !important; }

    .card { background:linear-gradient(135deg,#F0FDF4,#DCFCE7); padding:20px; border-radius:14px; border:1px solid #86EFAC; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card, .stApp .card p, .stApp .card span, .stApp .card div, .stApp .card strong, .stApp .card em { color:#14532D !important; }

    .card-dark { background:linear-gradient(135deg,#DCFCE7,#D1FAE5); padding:20px; border-radius:14px; border:1px solid #6EE7B7; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-dark, .stApp .card-dark p, .stApp .card-dark span, .stApp .card-dark div, .stApp .card-dark strong { color:#14532D !important; }

    .card-green { background:linear-gradient(135deg,#DCFCE7,#BBF7D0); padding:20px; border-radius:14px; border:1px solid #4ADE80; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-green, .stApp .card-green p, .stApp .card-green span, .stApp .card-green div { color:#14532D !important; }

    .card-blue { background:linear-gradient(135deg,#EFF6FF,#DBEAFE); padding:20px; border-radius:14px; border:1px solid #93C5FD; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-blue, .stApp .card-blue p, .stApp .card-blue span, .stApp .card-blue div { color:#1E3A8A !important; }

    .card-red { background:linear-gradient(135deg,#FFF5F5,#FEE2E2); padding:20px; border-radius:14px; border:1px solid #FECACA; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-red, .stApp .card-red p, .stApp .card-red span, .stApp .card-red div { color:#7F1D1D !important; }

    .card-yellow { background:linear-gradient(135deg,#FFFBEB,#FEF3C7); padding:18px; border-radius:12px; border:1px solid #FCD34D; margin-bottom:12px; white-space:normal; word-wrap:break-word; }
    .stApp .card-yellow, .stApp .card-yellow p, .stApp .card-yellow span, .stApp .card-yellow div { color:#78350F !important; }

    .stat-box { background:#FFFFFF; border-radius:12px; padding:16px; text-align:center; border:1px solid #86EFAC; }
    .stApp .stat-box div, .stApp .stat-box span, .stApp .stat-box p { color:#14532D !important; }
    .stApp .stat-numero, .stat-numero { font-size:2em; font-weight:700; color:#166534 !important; }

    .hist-item { background:#FFFFFF; border-radius:10px; padding:12px 16px; margin-bottom:8px; border-left:4px solid #86EFAC; }
    .stApp .hist-item, .stApp .hist-item p, .stApp .hist-item span, .stApp .hist-item div, .stApp .hist-item small { color:#14532D !important; }

    .badge { background:#166534; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-verde { background:#059669; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-amarelo { background:#B45309; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-azul { background:#1D4ED8; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-roxo { background:#6D28D9; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }

    .divider { border:none; height:1px; background:linear-gradient(to right,transparent,#86EFAC,transparent); margin:18px 0; }

    .chat-user { background:#FFFFFF; border:1px solid #86EFAC; border-radius:12px 12px 4px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-user, .stApp .chat-user p, .stApp .chat-user span, .stApp .chat-user div { color:#14532D !important; }

    .chat-persona { background:#F6FBF4; border:1px solid #86EFAC; border-radius:4px 12px 12px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-persona, .stApp .chat-persona p, .stApp .chat-persona span, .stApp .chat-persona div { color:#14532D !important; }

    .questao-box { background:#FFFFFF; border:2px solid #86EFAC; border-radius:12px; padding:18px; margin-bottom:14px; }
    .stApp .questao-box, .stApp .questao-box p, .stApp .questao-box span, .stApp .questao-box div { color:#14532D !important; }

    .avaliacao-box { background:#FFFFFF; border:2px solid #86EFAC; border-radius:14px; padding:18px; margin-bottom:12px; }
    .stApp .avaliacao-box, .stApp .avaliacao-box p, .stApp .avaliacao-box span, .stApp .avaliacao-box div { color:#14532D !important; }

    .meta-box { background:#FFFFFF; border:2px solid #86EFAC; border-radius:12px; padding:16px; text-align:center; margin:10px 0; }
    .stApp .meta-box, .stApp .meta-box div, .stApp .meta-box span { color:#14532D !important; }
    .stApp .meta-numero { font-size:2em; font-weight:700; color:#166534 !important; }

    .chat-scroll-container { max-height:40vh; overflow-y:auto; display:flex; flex-direction:column; scroll-behavior:smooth; padding-bottom:4px; }
    .chat-scroll-container > * { flex-shrink:0; }
    

    </style>
\"\"\", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CACHE
# ─────────────────────────────────────────────
@st.cache_resource
def get_cache_invencoes():
    return {"perfis": {}}

_cache = get_cache_invencoes()

# ─────────────────────────────────────────────
# PERSISTÊNCIA LOCAL (JSON)
# ─────────────────────────────────────────────
CHAVES_SALVAR = [
    'usuario', 'historico_projetos', 'projetos_salvos',
    'ideia_padrao', 'projetos_ativos', 'banco_ideias_geradas',
]

def gerar_json_sessao() -> str:
    dados = {k: st.session_state.get(k) for k in CHAVES_SALVAR}
    dados['salvo_em'] = datetime.now().strftime('%d/%m/%Y %H:%M')
    return json.dumps(dados, ensure_ascii=False, indent=2, default=str)

def carregar_json_sessao(dados):
    _bloq = {'api_key','etapa','nome_login','chave_login','upload_login','btn_entrar_login'}
    _pref = (
        'btn_','sel_','ul_','dl_','cad_','_sub','_sm','_tab','_bsc',
        'ativo_','rem_','sel_pet_','ev_','prof_','hig_','prev_',
        'vac_','sint_','comp_','trad_','subs_','amb_','viag_','chat_',
        'duvida_','emerg_','peso_','data_','obs_','tipo_','vet_','desc_',
        'local_','prox_','alim','sit_emerg_','tc_','oraf','siau','agmag',
        'lv','mv','pt','pi','sh','wc','rv','rp','rc',
    )
    import re as _re
    for k, v in dados.items():
        if k in _bloq: continue
        if any(k.startswith(p) for p in _pref): continue
        if _re.match(r'.+_\\d+$', k): continue
        st.session_state[k] = v

def salvar_perfil_cache(usuario: str):
    _cache["perfis"][usuario] = {k: st.session_state.get(k) for k in CHAVES_SALVAR}

def perfis_salvos() -> list:
    return list(_cache["perfis"].keys())

def carregar_perfil_cache(usuario: str) -> dict | None:
    return _cache["perfis"].get(usuario)

def salvar_projeto(modulo: str, tema: str, conteudo: str):
    st.session_state.historico_projetos.append({
        'data': datetime.now().strftime('%d/%m %H:%M'), 'modulo': modulo, 'tema': tema, 'conteudo': conteudo,
    })

# --- INICIALIZAÇÃO DE ESTADO ---
defaults = {
    'etapa': "Login", 'usuario': "", 'api_key': "", 'pagina': "Home",
    'historico_projetos': [], 'projetos_salvos': [],
    'ideia_padrao': "", 'projetos_ativos': [], 'banco_ideias_geradas': [],
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# --- PRINCÍPIO DE HONESTIDADE ESTRATÉGICA — compartilhado ---
PRINCIPIO_HONESTIDADE = \"\"\"
PRINCÍPIO OBRIGATÓRIO DE HONESTIDADE ESTRATÉGICA — siga isso em TODA resposta:
- Você é um consultor de inovação e estratégia de negócios, mas NÃO tem acesso a dados de mercado em tempo real,
  buscas na internet, ou bancos de dados de concorrentes atualizados
- Para pesquisa de mercado, análise de concorrência e tendências: baseie-se em padrões gerais de mercado e
  conhecimento estabelecido até sua atualização de conhecimento — sempre recomende validar com pesquisa real
  (entrevistas com clientes potenciais, análise de concorrentes reais, dados de associações do setor) antes de investir
- Para viabilidade financeira, precificação e simulações: apresente sempre como ESTIMATIVAS para planejamento,
  nunca como garantias de resultado — os números reais dependem de execução, mercado real e fatores não previsíveis
- Para Patentes e Propriedade Intelectual: explique os conceitos gerais (diferença entre patente, marca, desenho
  industrial), mas sempre recomende um especialista em propriedade intelectual ou o INPI para o registro real —
  nunca dê certeza sobre se algo é patenteável sem análise profissional
- Seja honesto sobre os desafios e riscos reais de qualquer ideia — não infle expectativas para agradar. Inovação de
  verdade envolve riscos reais, e seu papel é ajudar a pessoa a vê-los claramente, não escondê-los
- Seja criativo, estratégico e entusiasmado — você é um consultor que genuinamente quer ver a ideia da pessoa
  prosperar, combinando otimismo com realismo
- Português do Brasil
\"\"\"

DISCLAIMER_MERCADO = \"\"\"
<div class="disclaimer-mercado">
🔍 <strong>Sobre esta análise:</strong> esta é uma análise estratégica educativa baseada em padrões gerais de mercado —
não substitui pesquisa de mercado real (entrevistas com clientes, análise de concorrentes reais, dados atualizados
do setor). Antes de investir, valide essas hipóteses com o mercado real.
</div>
\"\"\"

DISCLAIMER_PADRAO = \"\"\"
<div class="disclaimer">
⚠️ <strong>Importante:</strong> esta é uma análise estratégica para apoiar seu planejamento — os resultados reais
dependem de execução, mercado e fatores não previsíveis. Use como ponto de partida, não como garantia.
</div>
\"\"\"

# --- MOTOR DE IA ---
def invencoes_ia(prompt: str, system_extra: str = "") -> str:
    try:
        client = Groq(api_key=st.session_state.api_key)
        system = f\"\"\"Você é um consultor de inovação completo — um misto de inventor, estrategista de negócios, REGRA DE OURO — CONFIABILIDADE 100%%: Forneça APENAS informações que você tem certeza absoluta que são verdadeiras. JAMAIS invente, suponha, extrapole ou preencha lacunas com dados fictícios. Se não souber algo com certeza — preço, endereço, horário, nome, estatística, lei, fato — diga EXPLICITAMENTE: 'Não tenho certeza sobre isso, recomendo verificar em [fonte].' É melhor uma resposta incompleta e honesta do que uma resposta completa e inventada. O usuário depende dessas informações para tomar decisões reais.
pesquisador de mercado, designer de produtos e mentor de startups.
Usuário: {st.session_state.usuario}. Ideia/projeto principal: {st.session_state.ideia_padrao or 'não informado'}.
{PRINCIPIO_HONESTIDADE}
{system_extra}\"\"\"
        response = client.chat.completions.create(
            messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}],
            model="openai/gpt-oss-120b",
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Erro na API: {e}"

def renderizar_indice(texto: str, titulo_indice: str = "ÍNDICE"):
    percentuais = re.findall(r'(\\d+)\\s*/\\s*100|(\\d+)%', texto)
    valores = [int(a or b) for a, b in percentuais if a or b]
    indice = valores[0] if valores else 50

    if indice >= 70:
        classe, emoji, label = "indice-alto", "🟢", "ALTO"
    elif indice >= 40:
        classe, emoji, label = "indice-medio", "🟡", "MÉDIO"
    else:
        classe, emoji, label = "indice-baixo", "🔴", "BAIXO"

    st.markdown(f\"\"\"
    <div class="indice-box {classe}">
        <div style="font-size:2.2em;">{emoji}</div>
        <div class="indice-titulo">{titulo_indice}: {indice}/100</div>
        <div style="font-size:0.95em;color:#444;font-weight:600;">Nível: {label}</div>
        <div style="font-size:0.82em;color:#555;margin-top:6px;">Estimativa estratégica baseada nas informações fornecidas</div>
    </div>
    \"\"\", unsafe_allow_html=True)

# --- BARRA DE SALVAR ---
def barra_salvar():
    salvar_perfil_cache(st.session_state.usuario)
    nome_usuario = st.session_state.usuario.lower().replace(' ', '_') or 'minha_sessao'
    total = len(st.session_state.historico_projetos)
    ativos = len(st.session_state.projetos_ativos)

    col_info, col_btn = st.columns([4, 2])
    with col_info:
        st.markdown(
            f"<div style='background:#FFFBEB;border:1px solid #D97706;border-radius:10px;"
            f"padding:10px 14px;font-size:0.84em;color:#1A1A2E;line-height:1.6;'>"
            f"💾 <strong>Antes de sair, salve seus dados no computador.</strong><br>"
            f"<span style='color:#888;font-size:0.88em;'>{total} análises geradas · {ativos} projetos ativos</span>"
            f"</div>", unsafe_allow_html=True
        )
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown(\"\"\"<style>
    .dica-nav{font-size:0.72em;color:#94A3B8;text-align:center;padding:2px 0 6px;}
    .dica-mobile{display:none;}
    .dica-desktop{display:block;}
    @media(max-width:768px){.dica-mobile{display:block;}.dica-desktop{display:none;}}
    </style>
    <div class='dica-nav dica-mobile'>👆 Deslize o dedo para navegar entre as abas</div>
    <div class='dica-nav dica-desktop'>📋 Clique no ícone acima para abrir o menu completo</div>
    \"\"\", unsafe_allow_html=True)

# ============================================================
# TELA: LOGIN
# ============================================================
if 'banco_ideias_geradas' not in st.session_state: st.session_state['banco_ideias_geradas'] = None
if 'historico_projetos' not in st.session_state: st.session_state['historico_projetos'] = []
if 'ideia_padrao' not in st.session_state: st.session_state['ideia_padrao'] = None
if 'projetos_ativos' not in st.session_state: st.session_state['projetos_ativos'] = []
if 'projetos_salvos' not in st.session_state: st.session_state['projetos_salvos'] = []

if st.session_state.etapa == "Login":
    st.markdown("# 🤖 INVENÇÕES IA")
    st.markdown("<div class=\\'card\\'><b>🔒 ACESSO RESTRITO A CLIENTES DO MEUSAGENTESIA.COM.BR</b><br>🔗 <a href='https://meusagentesia.com.br' target='_blank' style='color:#4F46E5;font-weight:700;text-decoration:underline;'>meusagentesia.com.br</a></div>", unsafe_allow_html=True)
    st.info("💻 **Dica:** Pela complexidade dos agentes, no computador a experiência é mais agradável.")
    with st.container():
        nome  = st.text_input("Seu Nome:", key="nome_login")
        chave = st.text_input("🔑 Sua Chave API da Groq:", type="password", key="chave_login")
        if st.button("✨ ENTRAR", key="btn_entrar_login"):
            if len(nome.strip()) < 2:
                st.warning("Digite um nome com pelo menos 2 caracteres.")
            elif chave.strip():
                st.session_state.usuario = nome.strip()
                st.session_state.api_key = chave
                st.session_state.etapa = "App"
                st.rerun()
            else:
                st.warning("Preencha nome e chave API.")

elif st.session_state.etapa == "App":



    # TABS
    _tab_Home, _tab_Transformador, _tab_Pesquisa, _tab_Concorrencia, _tab_Validacao, _tab_Melhorias, _tab_Publico, _tab_Viabilidade, _tab_Precificacao, _tab_Escala, _tab_Lancamento, _tab_Branding, _tab_Visual, _tab_Produto, _tab_Tendencias, _tab_Patentes, _tab_PlanoNegocios, _tab_Marketing, _tab_Simulador, _tab_Riscos, _tab_BancoIdeias, _tab_Investidor, _tab_Pitch, _tab_Cronograma, _tab_Mentor, _tab_Laboratorio, _tab_Biblioteca = st.tabs(['🏠 Painel Principal', '💡 Transformador de I', '🔍 Pesquisa de Mercad', '⚔️ Concorrência Intel', '🧠 Validação da Ideia', '📄 Melhorias', '📄 Publico', '📄 Viabilidade', '📄 Precificacao', '📄 Escala', '📄 Lancamento', '📄 Branding', '📄 Visual', '📄 Produto', '📄 Tendencias', '📄 Patentes', '📄 PlanoNegocios', '📄 Marketing', '📄 Simulador', '📄 Riscos', '📄 BancoIdeias', '📄 Investidor', '📄 Pitch', '📄 Cronograma', '📄 Mentor', '📄 Laboratorio', '📄 Biblioteca'])

    # ── BARRA SALVAR — aparece em todas as abas ──
    with st.expander("💾 Salvar / Carregar meus dados", expanded=False):
        _bsc1, _bsc2 = st.columns(2)
        with _bsc1:
            import json as _jsv
            _dsv = {k: st.session_state.get(k) for k in list(st.session_state.keys()) if not k.startswith('_') and k not in ('api_key',)}
    with _tab_Home:
        col_u, col_r = st.columns([3, 1])
        with col_u:
            st.title(f"Olá, {st.session_state.usuario}! 💡")
            st.markdown("<span class='badge'>Laboratório Aberto</span>", unsafe_allow_html=True)
        with col_r:
            if st.button("🚪 Sair", key="invencoe3"):
                for k in list(st.session_state.keys()):
                    del st.session_state[k]
                st.rerun()

        if len(st.session_state.historico_projetos) == 0:
            st.markdown(\"\"\"<div style="background:#FEF3C7;border:2px solid #F59E0B;border-radius:12px;
            padding:12px 18px;margin-bottom:4px;color:#000;font-size:0.9em;font-weight:600;">
            ⚠️ Seus dados não estão mais no servidor.
            </div>\"\"\", unsafe_allow_html=True)
        st.session_state.ideia_padrao = st.text_area("💡 Sua ideia/projeto principal:",
            value=st.session_state.ideia_padrao, height=80,
            placeholder="ex: Um app que conecta idosos a jovens para ajudar com tecnologia em troca de companhia...", key="invencoe7")


        modulos_count = {}
        for c in st.session_state.historico_projetos:
            modulos_count[c['modulo']] = modulos_count.get(c['modulo'], 0) + 1

        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f"<div class='stat-box'><div class='stat-numero'>{len(st.session_state.historico_projetos)}</div><div>Análises geradas</div></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='stat-box'><div class='stat-numero'>{len(st.session_state.projetos_ativos)}</div><div>Projetos ativos</div></div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='stat-box'><div class='stat-numero'>{len(st.session_state.projetos_salvos)}</div><div>Salvas</div></div>", unsafe_allow_html=True)
        c4.markdown(f"<div class='stat-box'><div class='stat-numero'>{len(st.session_state.banco_ideias_geradas)}</div><div>Ideias no banco</div></div>", unsafe_allow_html=True)

        st.markdown("<div class='card'>💡 <em>'Toda grande invenção começou como uma pergunta simples que ninguém tinha respondido ainda.'</em></div>", unsafe_allow_html=True)

        st.markdown("### 🗺️ O que cada módulo faz")
        guia = {
            "💡 Transformador de Ideias": "Descreva sua ideia em poucas palavras e receba um projeto estruturado completo",
            "🔍 Pesquisa de Mercado": "Demanda, crescimento, tendências e nichos pouco explorados",
            "⚔️ Concorrência": "Principais concorrentes, pontos fortes/fracos e oportunidades de diferenciação",
            "🧠 Validação da Ideia": "Originalidade, potencial comercial, escalabilidade e barreiras de entrada",
            "🚀 Melhorias Automáticas": "Sugestões de funcionalidades, simplificações e versões futuras",
            "🎯 Público-Alvo": "Perfil completo do cliente ideal — dores, gatilhos e comportamentos",
            "💰 Viabilidade Financeira": "Custos, investimento mínimo, margem e ponto de equilíbrio",
            "💲 Precificação": "Melhor preço, faixa competitiva e estratégias de versão econômica/premium",
            "📈 Potencial de Escala": "Do mercado local ao internacional — franquias, licenciamento, assinaturas",
            "📢 Plano de Lançamento": "Roteiro completo do pré-lançamento à escala",
            "🎨 Branding": "Nome, slogan, posicionamento e personalidade da marca",
            "🖌️ Identidade Visual": "Cores, tipografia, conceito de logo e embalagem",
            "📦 Produto Final": "Como fabricar, entregar, vender e apresentar ao cliente",
            "🌎 Tendências": "Tecnologias relacionadas e oportunidades futuras",
            "⚖️ Patentes": "Quando vale patentear e como proteger sua criação",
            "📄 Plano de Negócios": "Documento completo — resumo executivo, mercado, financeiro, crescimento",
            "📣 Marketing Inteligente": "Campanhas, headlines, anúncios e estratégias de lançamento",
            "🧪 Simulador de Mercado": "Simule cenários — e se vender 100 unidades? E se entrar concorrência?",
            "📊 Painel de Riscos": "Principais riscos, obstáculos e como reduzir cada um",
            "💎 Banco de Ideias": "Quando faltar inspiração — centenas de ideias por área",
            "🤝 Investidor IA": "Veja se sua ideia atrairia investidores e quais objeções esperar",
            "🎤 Pitch Perfeito": "Apresentações de 30s a 10 minutos para qualquer audiência",
            "📅 Cronograma": "O que fazer hoje, amanhã e nas próximas semanas",
            "🤖 Mentor 24h": "Converse livremente sobre seu projeto, do início às primeiras vendas",
            "⭐ Laboratório do Futuro": "Descreva um problema — receba soluções multidisciplinares inovadoras",
        }
        for aba, desc in guia.items():
            st.markdown(f"**{aba}** — {desc}")

        if st.session_state.historico_projetos:
            st.markdown("### 🕐 Últimas Análises")
            for item in reversed(st.session_state.historico_projetos[-4:]):
                st.markdown(f"<div class='hist-item'><span class='badge'>{item.get('modulo', '')}</span> <small style='color:#888'>{item['data']}</small><br><small>{item.get('tema', '')[:80]}</small></div>", unsafe_allow_html=True)

        # ========================
        # TRANSFORMADOR DE IDEIAS
        # ========================

        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        st.markdown("### 💾 Salvar e Carregar Dados")
        _csl1, _csl2 = st.columns(2)
        with _csl1:
            import json as _json_sv
            _dados_sv = {k: st.session_state.get(k) for k in list(st.session_state.keys()) if not k.startswith('_')}
    with _tab_Transformador:
        st.header("💡 Transformador de Ideias")
        st.markdown("Descreva sua ideia em poucas palavras — a IA estrutura tudo.")

        ideia_transf = st.text_area("💭 Sua ideia:", height=120, value=st.session_state.ideia_padrao,
            placeholder="ex: Quero criar um aplicativo que ajuda pessoas a economizar água em casa de forma gamificada...", key="invencoe6")

        if st.button("💡 TRANSFORMAR EM PROJETO", key="invencoe4"):
            if ideia_transf.strip():
                with st.spinner("Estruturando sua ideia..."):
                    prompt = (
                        f"Transforme esta ideia em um projeto estruturado.\\n"
                        f"Ideia: {ideia_transf}\\n\\n"
                        f"FORMATO:\\n\\n"
                        f"💡 PROJETO: [nome sugestivo para o projeto]\\n\\n"
                        f"🎯 OBJETIVO:\\n[o que o projeto busca alcançar]\\n\\n"
                        f"❓ PROBLEMA QUE RESOLVE:\\n[a dor real que essa ideia ataca]\\n\\n"
                        f"👥 PÚBLICO BENEFICIADO:\\n[quem ganha com isso]\\n\\n"
                        f"⭐ DIFERENCIAIS:\\n[o que torna essa ideia única ou interessante]\\n\\n"
                        f"🔄 POSSÍVEIS APLICAÇÕES:\\n[outros usos ou mercados onde isso poderia funcionar]\\n\\n"
                        f"✅ PRÓXIMOS PASSOS:\\n[3-5 ações concretas para sair do papel]"
                    )
                    res = invencoes_ia(prompt)
                    if res: st.session_state['res_transformado_invenc1'] = str(res)
                    salvar_projeto("Transformador", ideia_transf[:60], res)
                    st.session_state['transf_temp'] = res
                    st.session_state.ideia_padrao = ideia_transf
            else:
                st.warning("Descreva sua ideia.")

        if st.session_state.get('transf_temp'):
            st.markdown(f"<div class='card'>{st.session_state['transf_temp']}</div>", unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['transf_temp'], file_name="projeto_estruturado.txt", mime="text/plain", use_container_width=True, key="invencoe5")
            with col_sv:
                if st.button("❤️ Salvar como projeto ativo", use_container_width=True, key="invencoe6_d2"):
                    nome_proj = ideia_transf[:40] if 'ideia_transf' in dir() else 'Novo projeto'
                    if nome_proj not in st.session_state.projetos_ativos:
                        st.session_state.projetos_ativos.append(nome_proj)
                    st.session_state.projetos_salvos.append({'modulo':'Transformador','tema':nome_proj,'conteudo':st.session_state['transf_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo como projeto ativo!")

        # ========================
        # PESQUISA DE MERCADO
        # ========================

    with _tab_Pesquisa:
        st.header("🔍 Pesquisa de Mercado")
        st.markdown(DISCLAIMER_MERCADO, unsafe_allow_html=True)

        ideia_pesq = st.text_area("💡 Ideia/produto:", height=80, value=st.session_state.ideia_padrao, key="invencoe7_d2")
        regiao_pesq = st.text_input("📍 Mercado de interesse:", placeholder="ex: Brasil, São Paulo, mercado global...", key="invencoe8_d2")

        if st.button("🔍 PESQUISAR MERCADO", key="invencoe9"):
            if ideia_pesq.strip():
                with st.spinner("Analisando o mercado..."):
                    prompt = (
                        f"Faça uma análise de mercado para esta ideia.\\n"
                        f"Ideia: {ideia_pesq}. Mercado: {regiao_pesq or 'geral'}\\n\\n"
                        f"FORMATO:\\n\\n"
                        f"🔍 PESQUISA DE MERCADO — {ideia_pesq[:50].upper()}\\n\\n"
                        f"📊 EXISTE DEMANDA?\\n[análise baseada em padrões conhecidos — dores similares já resolvidas no mercado, sinais de interesse]\\n\\n"
                        f"👥 QUEM COMPRARIA:\\n[perfil geral do comprador potencial]\\n\\n"
                        f"📈 O MERCADO ESTÁ CRESCENDO?\\n[tendência geral do setor relacionado, com base em conhecimento estabelecido]\\n\\n"
                        f"🌍 TENDÊNCIAS NACIONAIS E INTERNACIONAIS:\\n[movimentos relevantes do setor]\\n\\n"
                        f"💎 NICHOS POUCO EXPLORADOS:\\n[oportunidades dentro dessa área]\\n\\n"
                        f"🎯 OPORTUNIDADES ESCONDIDAS:\\n[ângulos que poucos competidores costumam explorar]\\n\\n"
                        f"✅ COMO VALIDAR ISSO NA PRÁTICA:\\n[passos reais para confirmar essas hipóteses com o mercado de verdade]"
                    )
                    res = invencoes_ia(prompt)
                    if res: st.session_state['res_pesquisa_invenc2'] = str(res)
                    salvar_projeto("Pesquisa", ideia_pesq[:60], res)
                    st.session_state['pesq_temp'] = res
            else:
                st.warning("Descreva a ideia/produto.")

        if st.session_state.get('pesq_temp'):
            st.markdown(f"<div class='card-blue'>{st.session_state['pesq_temp']}</div>", unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['pesq_temp'], file_name="pesquisa_mercado.txt", mime="text/plain", use_container_width=True, key="invencoe10")
            with col_sv:
                if st.button("❤️ Salvar", key="sv_pesq", use_container_width=True):
                    st.session_state.projetos_salvos.append({'modulo':'Pesquisa','tema':ideia_pesq[:60] if 'ideia_pesq' in dir() else '','conteudo':st.session_state['pesq_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

        # ========================
        # CONCORRÊNCIA INTELIGENTE
        # ========================

    with _tab_Concorrencia:
        st.header("⚔️ Concorrência Inteligente")
        st.markdown(DISCLAIMER_MERCADO, unsafe_allow_html=True)

        ideia_conc = st.text_area("💡 Ideia/produto:", height=80, value=st.session_state.ideia_padrao, key="ideia_conc")
        concorrentes_conhecidos = st.text_input("🏢 Concorrentes que você já conhece (opcional):", placeholder="ex: empresa X, app Y...", key="invencoe11")

        if st.button("⚔️ ANALISAR CONCORRÊNCIA", key="invencoe12"):
            if ideia_conc.strip():
                with st.spinner("Mapeando concorrência..."):
                    prompt = (
                        f"Analise a concorrência para esta ideia.\\n"
                        f"Ideia: {ideia_conc}. Concorrentes conhecidos: {concorrentes_conhecidos or 'nenhum informado'}\\n\\n"
                        f"FORMATO:\\n\\n"
                        f"⚔️ ANÁLISE DE CONCORRÊNCIA — {ideia_conc[:50].upper()}\\n\\n"
                        f"🏢 TIPOS DE CONCORRENTES NESSE MERCADO:\\n[categorias de concorrentes — direto, indireto, substitutos]\\n\\n"
                        f"✅ PONTOS FORTES TÍPICOS DA CONCORRÊNCIA:\\n[o que esse tipo de negócio geralmente faz bem]\\n\\n"
                        f"⚠️ PONTOS FRACOS TÍPICOS:\\n[onde esse tipo de negócio geralmente falha ou frustra clientes]\\n\\n"
                        f"💰 FAIXA DE PREÇO TÍPICA DO MERCADO:\\n[estimativa geral]\\n\\n"
                        f"🎯 OPORTUNIDADES PARA SUPERAR A CONCORRÊNCIA:\\n[onde sua ideia pode se diferenciar]\\n\\n"
                        f"💎 ESPAÇOS AINDA NÃO EXPLORADOS:\\n[lacunas que a concorrência típica não cobre]\\n\\n"
                        f"✅ COMO PESQUISAR CONCORRENTES REAIS:\\n[método prático para mapear concorrentes reais nesse mercado]"
                    )
                    res = invencoes_ia(prompt)
                    if res: st.session_state['res_concorrencia_invenc3'] = str(res)
                    salvar_projeto("Concorrencia", ideia_conc[:60], res)
                    st.session_state['conc_temp'] = res
            else:
                st.warning("Descreva a ideia/produto.")

        if st.session_state.get('conc_temp'):
            st.markdown(f"<div class='card-red'>{st.session_state['conc_temp']}</div>", unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['conc_temp'], file_name="concorrencia.txt", mime="text/plain", use_container_width=True, key="invencoe13")
            with col_sv:
                if st.button("❤️ Salvar", key="sv_conc", use_container_width=True):
                    st.session_state.projetos_salvos.append({'modulo':'Concorrencia','tema':ideia_conc[:60] if 'ideia_conc' in dir() else '','conteudo':st.session_state['conc_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

        # ========================
        # VALIDAÇÃO DA IDEIA
        # ========================

    with _tab_Validacao:
        st.header("🧠 Validação da Ideia")

        ideia_val = st.text_area("💡 Ideia/produto:", height=80, value=st.session_state.ideia_padrao, key="ideia_val")
        contexto_val = st.text_area("📝 Contexto adicional (opcional):", height=80,
            placeholder="ex: já tenho um protótipo, é para um nicho B2B, vai ser um app...", key="contexto_val_input")

        if st.button("🧠 VALIDAR IDEIA", key="invencoe14"):
            if ideia_val.strip():
                with st.spinner("Analisando..."):
                    prompt = (
                        f"Faça um diagnóstico completo de validação para esta ideia.\\n"
                        f"Ideia: {ideia_val}. Contexto: {contexto_val or 'não informado'}\\n\\n"
                        f"FORMATO:\\n\\n"
                        f"🧠 ÍNDICE DE VALIDAÇÃO: [X]/100\\n"
                        f"[1-2 linhas explicando a estimativa geral]\\n\\n"
                        f"✨ ORIGINALIDADE: [X]/10 — [comentário]\\n"
                        f"💰 POTENCIAL COMERCIAL: [X]/10 — [comentário]\\n"
                        f"📈 ESCALABILIDADE: [X]/10 — [comentário]\\n"
                        f"🔧 COMPLEXIDADE: [Baixa/Média/Alta] — [comentário sobre dificuldade de execução]\\n"
                        f"🚧 BARREIRAS DE ENTRADA: [Baixas/Médias/Altas] — [o que dificultaria competidores entrarem, ou você entrar]\\n"
                        f"🎯 GRAU DE INOVAÇÃO: [Incremental/Disruptivo/Já existe similar] — [comentário honesto]\\n"
                        f"✅ CHANCES DE ACEITAÇÃO: [X]/10 — [comentário]\\n\\n"
                        f"⚠️ MAIOR RISCO DESSA IDEIA:\\n[seja honesto sobre o ponto mais fraco]\\n\\n"
                        f"💡 O QUE FORTALECERIA MAIS A IDEIA AGORA:\\n[1-2 ações prioritárias]"
                    )
                    res = invencoes_ia(prompt)
                    if res: st.session_state['res_validacao_invenc4'] = str(res)
                    salvar_projeto("Validacao", ideia_val[:60], res)
                    st.session_state['val_temp'] = res
            else:
                st.warning("Descreva a ideia.")

        if st.session_state.get('val_temp'):
            renderizar_indice(st.session_state['val_temp'], "ÍNDICE DE VALIDAÇÃO")
            st.markdown(f"<div class='card'>{st.session_state['val_temp']}</div>", unsafe_allow_html=True)
            st.markdown(DISCLAIMER_PADRAO, unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['val_temp'], file_name="validacao_ideia.txt", mime="text/plain", use_container_width=True, key="invencoe15")
            with col_sv:
                if st.button("❤️ Salvar", key="sv_val", use_container_width=True):
                    st.session_state.projetos_salvos.append({'modulo':'Validacao','tema':ideia_val[:60] if 'ideia_val' in dir() else '','conteudo':st.session_state['val_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

        # ========================
        # MELHORIAS AUTOMÁTICAS
        # ========================

    with _tab_Melhorias:
        st.header("🚀 Melhorias Automáticas")

        ideia_mel = st.text_area("💡 Ideia/produto atual:", height=80, value=st.session_state.ideia_padrao, key="ideia_mel")

        if st.button("🚀 SUGERIR MELHORIAS", key="invencoe16"):
            if ideia_mel.strip():
                with st.spinner("Pensando em melhorias..."):
                    prompt = (
                        f"Sugira melhorias criativas e estratégicas para esta ideia.\\n"
                        f"Ideia: {ideia_mel}\\n\\n"
                        f"FORMATO:\\n\\n"
                        f"🚀 MELHORIAS PARA: {ideia_mel[:50].upper()}\\n\\n"
                        f"⚙️ NOVAS FUNCIONALIDADES:\\n[3-5 funcionalidades que agregariam valor]\\n\\n"
                        f"👥 MUDANÇAS NO PÚBLICO:\\n[outros públicos que poderiam se beneficiar, ou ajustes no foco]\\n\\n"
                        f"🔄 NOVAS APLICAÇÕES:\\n[outros contextos onde essa ideia poderia ser usada]\\n\\n"
                        f"✂️ SIMPLIFICAÇÕES:\\n[o que poderia ser removido/simplificado para tornar mais fácil de usar/vender]\\n\\n"
                        f"💎 RECURSOS PREMIUM:\\n[funcionalidades que poderiam ser parte de uma versão paga]\\n\\n"
                        f"🔮 VERSÕES FUTURAS:\\n[para onde essa ideia poderia evoluir no longo prazo]"
                    )
                    res = invencoes_ia(prompt)
                    if res: st.session_state['res_melhorias_invenc5'] = str(res)
                    salvar_projeto("Melhorias", ideia_mel[:60], res)
                    st.session_state['mel_temp'] = res
            else:
                st.warning("Descreva a ideia.")

        if st.session_state.get('mel_temp'):
            st.markdown(f"<div class='card-teal'>{st.session_state['mel_temp']}</div>", unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['mel_temp'], file_name="melhorias.txt", mime="text/plain", use_container_width=True, key="invencoe17")
            with col_sv:
                if st.button("❤️ Salvar", key="sv_mel", use_container_width=True):
                    st.session_state.projetos_salvos.append({'modulo':'Melhorias','tema':ideia_mel[:60] if 'ideia_mel' in dir() else '','conteudo':st.session_state['mel_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

        # ========================
        # PÚBLICO-ALVO INTELIGENTE
        # ========================

    with _tab_Publico:
        st.header("🎯 Público-Alvo Inteligente")

        ideia_pub = st.text_area("💡 Ideia/produto:", height=80, value=st.session_state.ideia_padrao, key="ideia_pub")

        if st.button("🎯 DESCOBRIR PÚBLICO-ALVO", key="invencoe18"):
            if ideia_pub.strip():
                with st.spinner("Traçando o perfil..."):
                    prompt = (
                        f"Crie um perfil detalhado do cliente ideal para esta ideia.\\n"
                        f"Ideia: {ideia_pub}\\n\\n"
                        f"FORMATO:\\n\\n"
                        f"🎯 PÚBLICO-ALVO — {ideia_pub[:50].upper()}\\n\\n"
                        f"👤 PERFIL DO CLIENTE:\\n[nome fictício, descrição geral]\\n\\n"
                        f"🎂 FAIXA ETÁRIA:\\n[idade típica]\\n\\n"
                        f"💰 PODER AQUISITIVO:\\n[faixa de renda]\\n\\n"
                        f"❤️ INTERESSES:\\n[o que esse perfil gosta/consome]\\n\\n"
                        f"🧠 COMPORTAMENTOS:\\n[hábitos relevantes — como pesquisa, como compra]\\n\\n"
                        f"😰 PRINCIPAIS DORES:\\n[problemas reais que essa ideia resolve para esse perfil]\\n\\n"
                        f"💥 GATILHOS EMOCIONAIS:\\n[o que realmente convenceria essa pessoa a comprar/usar]\\n\\n"
                        f"📱 ONDE ENCONTRAR ESSE PÚBLICO:\\n[canais e locais onde esse perfil está presente]"
                    )
                    res = invencoes_ia(prompt)
                    if res: st.session_state['res_publico_invenc6'] = str(res)
                    salvar_projeto("Publico", ideia_pub[:60], res)
                    st.session_state['pub_temp'] = res
            else:
                st.warning("Descreva a ideia.")

        if st.session_state.get('pub_temp'):
            st.markdown(f"<div class='card-pink'>{st.session_state['pub_temp']}</div>", unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['pub_temp'], file_name="publico_alvo.txt", mime="text/plain", use_container_width=True, key="invencoe19")
            with col_sv:
                if st.button("❤️ Salvar", key="sv_pub", use_container_width=True):
                    st.session_state.projetos_salvos.append({'modulo':'Publico','tema':ideia_pub[:60] if 'ideia_pub' in dir() else '','conteudo':st.session_state['pub_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

        # ========================
        # VIABILIDADE FINANCEIRA
        # ========================

    with _tab_Viabilidade:
        st.header("💰 Viabilidade Financeira")
        st.markdown(DISCLAIMER_MERCADO, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            ideia_via = st.text_area("💡 Ideia/produto:", height=80, value=st.session_state.ideia_padrao, key="ideia_via")
            capital_via = st.number_input("💰 Capital disponível para investir (R$):", min_value=0.0, value=5000.0, step=500.0, key="invencoe20")
        with col2:
            tipo_via = st.selectbox("📦 Tipo de negócio:", ["Produto físico","Serviço","App/Software","Plataforma digital","Conteúdo/Educação","Outro"], key="invencoe21")
            meta_via = st.text_input("🎯 Meta de receita mensal (opcional):", placeholder="ex: R$5.000/mês", key="invencoe22")

        if st.button("💰 ANALISAR VIABILIDADE", key="invencoe23"):
            if ideia_via.strip():
                with st.spinner("Calculando viabilidade..."):
                    prompt = (
                        f"Analise a viabilidade financeira desta ideia.\\n"
                        f"Ideia: {ideia_via}. Tipo: {tipo_via}. Capital disponível: R${capital_via}. Meta: {meta_via or 'não definida'}\\n\\n"
                        f"FORMATO:\\n\\n"
                        f"💰 VIABILIDADE FINANCEIRA — {ideia_via[:50].upper()}\\n\\n"
                        f"💸 CUSTOS INICIAIS ESTIMADOS:\\n[lista com faixas de valores]\\n\\n"
                        f"📅 CUSTOS MENSAIS ESTIMADOS:\\n[lista com faixas de valores]\\n\\n"
                        f"💰 INVESTIMENTO MÍNIMO PARA COMEÇAR:\\n[valor estimado]\\n\\n"
                        f"📊 ANÁLISE DO SEU CAPITAL (R${capital_via}):\\n[é suficiente? o que fazer se não for?]\\n\\n"
                        f"📈 MARGEM POSSÍVEL:\\n[estimativa de margem para esse tipo de negócio]\\n\\n"
                        f"⚖️ PONTO DE EQUILÍBRIO ESTIMADO:\\n[quantas vendas/clientes para cobrir custos]\\n\\n"
                        f"⏱️ TEMPO ESTIMADO PARA RETORNO:\\n[estimativa realista]\\n\\n"
                        f"⚠️ MAIOR RISCO FINANCEIRO:\\n[seja honesto sobre o que pode dar errado financeiramente]"
                    )
                    res = invencoes_ia(prompt)
                    if res: st.session_state['res_viabilidade_invenc7'] = str(res)
                    salvar_projeto("Viabilidade", ideia_via[:60], res)
                    st.session_state['via_temp'] = res
            else:
                st.warning("Descreva a ideia.")

        if st.session_state.get('via_temp'):
            st.markdown(f"<div class='card-green'>{st.session_state['via_temp']}</div>", unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['via_temp'], file_name="viabilidade.txt", mime="text/plain", use_container_width=True, key="invencoe24")
            with col_sv:
                if st.button("❤️ Salvar", key="sv_via", use_container_width=True):
                    st.session_state.projetos_salvos.append({'modulo':'Viabilidade','tema':ideia_via[:60] if 'ideia_via' in dir() else '','conteudo':st.session_state['via_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

        # ========================
        # PRECIFICAÇÃO
        # ========================

    with _tab_Precificacao:
        st.header("💲 Precificação")

        col1, col2 = st.columns(2)
        with col1:
            ideia_prec = st.text_area("💡 Produto/serviço:", height=80, value=st.session_state.ideia_padrao, key="ideia_prec")
            custo_prec = st.number_input("💸 Custo unitário/de entrega (R$):", min_value=0.0, value=0.0, step=10.0, key="invencoe25")
        with col2:
            publico_prec = st.selectbox("🎯 Público:", ["Classe A/B (premium)","Classe B/C (intermediário)","Classe C/D (popular)","B2B (empresas)","Misto"], key="invencoe26")
            concorrencia_preco = st.text_input("💰 Preço de referência da concorrência (opcional):", placeholder="ex: R$50-100", key="invencoe27")

        if st.button("💲 CALCULAR PRECIFICAÇÃO", key="invencoe28"):
            if ideia_prec.strip():
                with st.spinner("Calculando..."):
                    prompt = (
                        f"Crie uma estratégia de precificação completa.\\n"
                        f"Produto/serviço: {ideia_prec}. Custo: R${custo_prec}. Público: {publico_prec}.\\n"
                        f"Referência de concorrência: {concorrencia_preco or 'não informada'}\\n\\n"
                        f"FORMATO:\\n\\n"
                        f"💲 ESTRATÉGIA DE PREÇO — {ideia_prec[:50].upper()}\\n\\n"
                        f"🎯 MELHOR PREÇO SUGERIDO: R$[X]\\n"
                        f"[justificativa]\\n\\n"
                        f"📊 FAIXA COMPETITIVA: R$[X] a R$[X]\\n\\n"
                        f"📈 MARGEM IDEAL: [X]%\\n"
                        f"[com base no custo de R${custo_prec}]\\n\\n"
                        f"💡 ESTRATÉGIAS DE PREÇO:\\n[psicológico, ancoragem, etc — específico para esse produto]\\n\\n"
                        f"💰 VERSÃO ECONÔMICA: R$[X]\\n[o que ela incluiria]\\n\\n"
                        f"💎 VERSÃO PREMIUM: R$[X]\\n[o que ela incluiria a mais]"
                    )
                    res = invencoes_ia(prompt)
                    if res: st.session_state['res_precificacao_invenc8'] = str(res)
                    salvar_projeto("Precificacao", ideia_prec[:60], res)
                    st.session_state['prec_temp'] = res
            else:
                st.warning("Descreva o produto/serviço.")

        if st.session_state.get('prec_temp'):
            st.markdown(f"<div class='card-gold' style='background:linear-gradient(135deg,#FFFBEB,#FEF3C7);border:2px solid #D97706;padding:22px;border-radius:16px;'>{st.session_state['prec_temp']}</div>", unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['prec_temp'], file_name="precificacao.txt", mime="text/plain", use_container_width=True, key="invencoe29")
            with col_sv:
                if st.button("❤️ Salvar", key="sv_prec", use_container_width=True):
                    st.session_state.projetos_salvos.append({'modulo':'Precificacao','tema':ideia_prec[:60] if 'ideia_prec' in dir() else '','conteudo':st.session_state['prec_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

        # ========================
        # POTENCIAL DE ESCALA
        # ========================

    with _tab_Escala:
        st.header("📈 Potencial de Escala")

        ideia_esc = st.text_area("💡 Ideia/produto:", height=80, value=st.session_state.ideia_padrao, key="ideia_esc")

        if st.button("📈 ANALISAR POTENCIAL DE ESCALA", key="invencoe30"):
            if ideia_esc.strip():
                with st.spinner("Analisando escala..."):
                    prompt = (
                        f"Analise até onde esta ideia pode crescer.\\n"
                        f"Ideia: {ideia_esc}\\n\\n"
                        f"FORMATO:\\n\\n"
                        f"📈 POTENCIAL DE ESCALA — {ideia_esc[:50].upper()}\\n\\n"
                        f"🏘️ MERCADO LOCAL:\\n[viabilidade e tamanho aproximado]\\n\\n"
                        f"🇧🇷 MERCADO NACIONAL:\\n[o que seria necessário para expandir]\\n\\n"
                        f"🌍 MERCADO INTERNACIONAL:\\n[viabilidade e desafios — idioma, regulação, logística]\\n\\n"
                        f"🏪 POSSIBILIDADE DE FRANQUIAS:\\n[faz sentido para esse tipo de negócio?]\\n\\n"
                        f"📜 LICENCIAMENTO:\\n[a ideia poderia ser licenciada para terceiros?]\\n\\n"
                        f"🔄 MODELO DE ASSINATURA:\\n[seria viável transformar em recorrência?]\\n\\n"
                        f"💻 EXPANSÃO DIGITAL:\\n[como a digitalização poderia acelerar o crescimento]\\n\\n"
                        f"🎯 TETO REALISTA DE CRESCIMENTO:\\n[seja honesto sobre limitações reais dessa ideia]"
                    )
                    res = invencoes_ia(prompt)
                    if res: st.session_state['res_escala_invenc9'] = str(res)
                    salvar_projeto("Escala", ideia_esc[:60], res)
                    st.session_state['esc_temp'] = res
            else:
                st.warning("Descreva a ideia.")

        if st.session_state.get('esc_temp'):
            st.markdown(f"<div class='card-blue'>{st.session_state['esc_temp']}</div>", unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['esc_temp'], file_name="potencial_escala.txt", mime="text/plain", use_container_width=True, key="invencoe31")
            with col_sv:
                if st.button("❤️ Salvar", key="sv_esc", use_container_width=True):
                    st.session_state.projetos_salvos.append({'modulo':'Escala','tema':ideia_esc[:60] if 'ideia_esc' in dir() else '','conteudo':st.session_state['esc_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

        # ========================
        # PLANO DE LANÇAMENTO
        # ========================

    with _tab_Lancamento:
        st.header("📢 Plano de Lançamento")

        col1, col2 = st.columns(2)
        with col1:
            ideia_lanc = st.text_area("💡 Ideia/produto:", height=80, value=st.session_state.ideia_padrao, key="ideia_lanc")
        with col2:
            prazo_lanc = st.text_input("📅 Prazo desejado para lançar:", placeholder="ex: 2 meses, 6 meses...", key="invencoe32")
            orcamento_lanc = st.number_input("💰 Orçamento para lançamento (R$):", min_value=0.0, value=1000.0, step=200.0, key="invencoe33")

        if st.button("📢 CRIAR PLANO DE LANÇAMENTO", key="invencoe34"):
            if ideia_lanc.strip():
                with st.spinner("Montando o roteiro..."):
                    prompt = (
                        f"Crie um plano completo de lançamento.\\n"
                        f"Ideia: {ideia_lanc}. Prazo: {prazo_lanc or 'flexível'}. Orçamento: R${orcamento_lanc}\\n\\n"
                        f"FORMATO:\\n\\n"
                        f"📢 PLANO DE LANÇAMENTO — {ideia_lanc[:50].upper()}\\n\\n"
                        f"📋 FASE 1 — PRÉ-LANÇAMENTO:\\n[ações antes de lançar — construir audiência, validar, preparar]\\n\\n"
                        f"🧪 FASE 2 — VALIDAÇÃO:\\n[como testar com público real antes de escalar]\\n\\n"
                        f"🚀 FASE 3 — PRIMEIRAS VENDAS:\\n[estratégia para as primeiras conversões]\\n\\n"
                        f"📣 FASE 4 — DIVULGAÇÃO:\\n[canais e táticas considerando o orçamento de R${orcamento_lanc}]\\n\\n"
                        f"📈 FASE 5 — CRESCIMENTO:\\n[como ganhar tração após a validação inicial]\\n\\n"
                        f"🏆 FASE 6 — ESCALA:\\n[próximos passos quando o modelo estiver funcionando]\\n\\n"
                        f"📅 CRONOGRAMA RESUMIDO:\\n[timeline considerando o prazo de {prazo_lanc or 'médio prazo'}]"
                    )
                    res = invencoes_ia(prompt)
                    if res: st.session_state['res_lancamento_invenc10'] = str(res)
                    salvar_projeto("Lancamento", ideia_lanc[:60], res)
                    st.session_state['lanc_temp'] = res
            else:
                st.warning("Descreva a ideia.")

        if st.session_state.get('lanc_temp'):
            st.markdown(f"<div class='card-purple'>{st.session_state['lanc_temp']}</div>", unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['lanc_temp'], file_name="plano_lancamento.txt", mime="text/plain", use_container_width=True, key="invencoe35")
            with col_sv:
                if st.button("❤️ Salvar", key="sv_lanc", use_container_width=True):
                    st.session_state.projetos_salvos.append({'modulo':'Lancamento','tema':ideia_lanc[:60] if 'ideia_lanc' in dir() else '','conteudo':st.session_state['lanc_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

        # ========================
        # BRANDING
        # ========================

    with _tab_Branding:
        st.header("🎨 Branding")

        ideia_brand = st.text_area("💡 Ideia/produto:", height=80, value=st.session_state.ideia_padrao, key="ideia_brand")
        valores_brand = st.text_input("💎 Valores que você quer transmitir (opcional):", placeholder="ex: sustentabilidade, inovação, acessibilidade...", key="invencoe36")

        if st.button("🎨 CRIAR BRANDING", key="invencoe37"):
            if ideia_brand.strip():
                with st.spinner("Criando a marca..."):
                    prompt = (
                        f"Crie um branding completo para esta ideia.\\n"
                        f"Ideia: {ideia_brand}. Valores desejados: {valores_brand or 'a definir'}\\n\\n"
                        f"FORMATO:\\n\\n"
                        f"🎨 BRANDING — {ideia_brand[:50].upper()}\\n\\n"
                        f"🏷️ OPÇÕES DE NOME (5):\\n[nome — significado/por que funciona]\\n\\n"
                        f"🎯 SLOGAN (3 opções):\\n[slogan 1]\\n[slogan 2]\\n[slogan 3]\\n\\n"
                        f"📍 POSICIONAMENTO:\\n[frase: Para [público], a [marca] é a [categoria] que [benefício único]]\\n\\n"
                        f"🗣️ PERSONALIDADE DA MARCA:\\n[como a marca se comporta — adjetivos]\\n\\n"
                        f"💬 IDENTIDADE VERBAL:\\n[como a marca fala — tom de voz, vocabulário]\\n\\n"
                        f"💎 VALORES DA MARCA:\\n[3-5 valores centrais]"
                    )
                    res = invencoes_ia(prompt)
                    if res: st.session_state['res_branding_invenc11'] = str(res)
                    salvar_projeto("Branding", ideia_brand[:60], res)
                    st.session_state['brand_temp'] = res
            else:
                st.warning("Descreva a ideia.")

        if st.session_state.get('brand_temp'):
            st.markdown(f"<div class='card-pink'>{st.session_state['brand_temp']}</div>", unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['brand_temp'], file_name="branding.txt", mime="text/plain", use_container_width=True, key="invencoe38")
            with col_sv:
                if st.button("❤️ Salvar", key="sv_brand", use_container_width=True):
                    st.session_state.projetos_salvos.append({'modulo':'Branding','tema':ideia_brand[:60] if 'ideia_brand' in dir() else '','conteudo':st.session_state['brand_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

        # ========================
        # IDENTIDADE VISUAL
        # ========================

    with _tab_Visual:
        st.header("🖌️ Identidade Visual")

        ideia_vis = st.text_area("💡 Ideia/produto:", height=80, value=st.session_state.ideia_padrao, key="ideia_vis")
        estilo_vis = st.selectbox("🎨 Estilo desejado:", ["Moderno/minimalista","Divertido/colorido","Sofisticado/premium","Rústico/artesanal","Tecnológico/futurista","Não sei, sugira"], key="invencoe39")

        if st.button("🖌️ SUGERIR IDENTIDADE VISUAL", key="invencoe40"):
            if ideia_vis.strip():
                with st.spinner("Criando conceito visual..."):
                    prompt = (
                        f"Sugira uma identidade visual completa.\\n"
                        f"Ideia: {ideia_vis}. Estilo desejado: {estilo_vis}\\n\\n"
                        f"FORMATO:\\n\\n"
                        f"🖌️ IDENTIDADE VISUAL — {ideia_vis[:50].upper()}\\n\\n"
                        f"🎨 PALETA DE CORES:\\n[2-3 cores principais com código hex sugerido + o que cada uma transmite]\\n\\n"
                        f"🔤 TIPOGRAFIA:\\n[estilo de fonte recomendado — serifada/sem serifa, e por quê]\\n\\n"
                        f"💡 CONCEITO DO LOGOTIPO:\\n[ideia de símbolo/conceito visual que represente a marca]\\n\\n"
                        f"📦 EMBALAGEM/APRESENTAÇÃO:\\n[se aplicável, como deveria parecer fisicamente ou digitalmente]\\n\\n"
                        f"🎭 REFERÊNCIAS DE ESTILO:\\n[tipo de marcas/design que servem de inspiração visual, sem citar marcas registradas específicas]"
                    )
                    res = invencoes_ia(prompt)
                    if res: st.session_state['res_visual_invenc12'] = str(res)
                    salvar_projeto("Visual", ideia_vis[:60], res)
                    st.session_state['vis_temp'] = res
            else:
                st.warning("Descreva a ideia.")

        if st.session_state.get('vis_temp'):
            st.markdown(f"<div class='card-purple'>{st.session_state['vis_temp']}</div>", unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['vis_temp'], file_name="identidade_visual.txt", mime="text/plain", use_container_width=True, key="invencoe41")
            with col_sv:
                if st.button("❤️ Salvar", key="sv_vis", use_container_width=True):
                    st.session_state.projetos_salvos.append({'modulo':'Visual','tema':ideia_vis[:60] if 'ideia_vis' in dir() else '','conteudo':st.session_state['vis_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

        # ========================
        # PRODUTO FINAL
        # ========================

    with _tab_Produto:
        st.header("📦 Produto Final")

        ideia_prod = st.text_area("💡 Ideia/produto:", height=80, value=st.session_state.ideia_padrao, key="ideia_prod")

        if st.button("📦 TRANSFORMAR EM PRODUTO REAL", key="invencoe42"):
            if ideia_prod.strip():
                with st.spinner("Estruturando o produto final..."):
                    prompt = (
                        f"Mostre como transformar esta ideia em um produto real e entregável.\\n"
                        f"Ideia: {ideia_prod}\\n\\n"
                        f"FORMATO:\\n\\n"
                        f"📦 PRODUTO FINAL — {ideia_prod[:50].upper()}\\n\\n"
                        f"🏭 COMO FABRICAR/CRIAR:\\n[processo geral de produção/desenvolvimento]\\n\\n"
                        f"🚚 COMO ENTREGAR:\\n[logística — física ou digital]\\n\\n"
                        f"💰 COMO VENDER:\\n[canais de venda recomendados]\\n\\n"
                        f"🎤 COMO APRESENTAR AO CLIENTE:\\n[script ou estrutura de apresentação do produto]\\n\\n"
                        f"✅ CHECKLIST PARA O PRODUTO ESTAR PRONTO:\\n[itens essenciais antes de vender]"
                    )
                    res = invencoes_ia(prompt)
                    if res: st.session_state['res_produto_invenc13'] = str(res)
                    salvar_projeto("Produto", ideia_prod[:60], res)
                    st.session_state['prod_temp'] = res
            else:
                st.warning("Descreva a ideia.")

        if st.session_state.get('prod_temp'):
            st.markdown(f"<div class='card-teal'>{st.session_state['prod_temp']}</div>", unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['prod_temp'], file_name="produto_final.txt", mime="text/plain", use_container_width=True, key="invencoe43")
            with col_sv:
                if st.button("❤️ Salvar", key="sv_prod", use_container_width=True):
                    st.session_state.projetos_salvos.append({'modulo':'Produto','tema':ideia_prod[:60] if 'ideia_prod' in dir() else '','conteudo':st.session_state['prod_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

        # ========================
        # TENDÊNCIAS
        # ========================

    with _tab_Tendencias:
        st.header("🌎 Tendências")
        st.markdown(DISCLAIMER_MERCADO, unsafe_allow_html=True)

        area_tend = st.selectbox("Área de interesse:", [
            "Tecnologia e IA", "Saúde e bem-estar", "Educação", "Sustentabilidade",
            "Alimentação", "Serviços financeiros", "Mobilidade", "Entretenimento", "Outra (descrever)",
        ], key="invencoe5_d2")
        area_custom = ""
        if area_tend == "Outra (descrever)":
            area_custom = st.text_input("Descreva a área:", key="invencoe44")

        if st.button("🌎 EXPLORAR TENDÊNCIAS", key="invencoe45"):
            area_final = area_custom if area_tend == "Outra (descrever)" and area_custom.strip() else area_tend
            if area_final.strip():
                with st.spinner("Explorando tendências..."):
                    prompt = (
                        f"Explore as tendências da área: {area_final}\\n\\n"
                        f"FORMATO:\\n\\n"
                        f"🌎 TENDÊNCIAS — {area_final.upper()}\\n\\n"
                        f"💻 TECNOLOGIAS RELACIONADAS:\\n[tecnologias relevantes para essa área]\\n\\n"
                        f"✨ INOVAÇÕES RECENTES:\\n[movimentos recentes conhecidos nessa área]\\n\\n"
                        f"📈 MERCADOS EM CRESCIMENTO:\\n[sub-segmentos em expansão]\\n\\n"
                        f"🔄 MUDANÇAS DE COMPORTAMENTO:\\n[como o consumidor está mudando nessa área]\\n\\n"
                        f"🚀 OPORTUNIDADES FUTURAS:\\n[onde os próximos movimentos provavelmente estarão]"
                    )
                    res = invencoes_ia(prompt)
                    if res: st.session_state['res_tendencias_invenc14'] = str(res)
                    salvar_projeto("Tendencias", area_final, res)
                    st.session_state['tend_temp'] = res
            else:
                st.warning("Escolha ou descreva a área.")

        if st.session_state.get('tend_temp'):
            st.markdown(f"<div class='card-blue'>{st.session_state['tend_temp']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar (.txt)", data=st.session_state['tend_temp'], file_name="tendencias.txt", mime="text/plain", key="invencoe46")

        # ========================
        # PATENTES E PROPRIEDADE INTELECTUAL
        # ========================

    with _tab_Patentes:
        st.header("⚖️ Patentes e Propriedade Intelectual")

        st.markdown(\"\"\"<div class="disclaimer-mercado">
        ⚖️ <strong>Importante:</strong> esta seção é educativa. Para registro real de patente, marca ou desenho
        industrial, consulte um especialista em propriedade intelectual ou o INPI (Instituto Nacional da Propriedade Industrial).
        </div>\"\"\", unsafe_allow_html=True)

        tema_pat = st.selectbox("Tema:", [
            "Quando vale a pena patentear", "Diferença entre patente, marca e desenho industrial",
            "Como proteger minha ideia antes de divulgar", "Como funciona o registro de marca",
            "Direitos de autor vs patente", "Cuidados ao buscar investidores/parceiros",
        ], key="invencoe4_d2")

        if st.button("⚖️ EXPLICAR", key="invencoe47"):
            with st.spinner("Preparando explicação..."):
                prompt = (
                    f"Explique de forma clara e prática: {tema_pat}, no contexto de proteção de ideias e inovação no Brasil.\\n\\n"
                    f"FORMATO:\\n\\n"
                    f"⚖️ {tema_pat.upper()}\\n\\n"
                    f"📖 EXPLICAÇÃO:\\n[explicação didática]\\n\\n"
                    f"✅ QUANDO ISSO SE APLICA:\\n[situações práticas]\\n\\n"
                    f"📋 PASSO A PASSO GERAL:\\n[processo típico, sempre indicando que detalhes devem ser confirmados com especialista/INPI]\\n\\n"
                    f"⚠️ CUIDADOS COMUNS:\\n[erros frequentes que pessoas cometem nessa área]\\n\\n"
                    f"💡 DICA PRÁTICA:\\n[1 dica de proteção imediata e de baixo custo]"
                )
                res = invencoes_ia(prompt)
                if res: st.session_state['res_patentes_invenc15'] = str(res)
                salvar_projeto("Patentes", tema_pat, res)
                st.session_state['pat_temp'] = res

        if st.session_state.get('pat_temp'):
            st.markdown(f"<div class='card'>{st.session_state['pat_temp']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar (.txt)", data=st.session_state['pat_temp'], file_name="patentes.txt", mime="text/plain", key="invencoe48")

        # ========================
        # PLANO DE NEGÓCIOS AUTOMÁTICO
        # ========================

    with _tab_PlanoNegocios:
        st.header("📄 Plano de Negócios Automático")

        ideia_plano = st.text_area("💡 Ideia/produto:", height=100, value=st.session_state.ideia_padrao, key="ideia_plano")
        contexto_plano = st.text_area("📝 Contexto adicional (opcional):", height=80,
            placeholder="ex: capital disponível, experiência prévia, equipe...", key="contexto_plano_input")

        if st.button("📄 GERAR PLANO DE NEGÓCIOS COMPLETO", key="invencoe49"):
            if ideia_plano.strip():
                with st.spinner("Montando o plano de negócios..."):
                    prompt = (
                        f"Crie um plano de negócios completo.\\n"
                        f"Ideia: {ideia_plano}. Contexto: {contexto_plano or 'não informado'}\\n\\n"
                        f"FORMATO:\\n\\n"
                        f"📄 PLANO DE NEGÓCIOS — {ideia_plano[:50].upper()}\\n\\n"
                        f"📋 RESUMO EXECUTIVO:\\n[visão geral em 3-4 linhas]\\n\\n"
                        f"💼 MODELO DE NEGÓCIO:\\n[como o negócio gera valor e receita]\\n\\n"
                        f"📊 MERCADO:\\n[tamanho e características gerais do mercado-alvo]\\n\\n"
                        f"📣 MARKETING:\\n[estratégia geral de aquisição de clientes]\\n\\n"
                        f"⚙️ OPERAÇÃO:\\n[como o negócio funciona no dia a dia]\\n\\n"
                        f"💰 FINANCEIRO:\\n[estrutura de custos e receita esperada]\\n\\n"
                        f"📈 CRESCIMENTO:\\n[plano para os próximos passos de expansão]"
                    )
                    res = invencoes_ia(prompt)
                    if res: st.session_state['res_planonegocio_invenc16'] = str(res)
                    salvar_projeto("PlanoNegocios", ideia_plano[:60], res)
                    st.session_state['plano_neg_temp'] = res
            else:
                st.warning("Descreva a ideia.")

        if st.session_state.get('plano_neg_temp'):
            st.markdown(f"<div class='card-dark'>{st.session_state['plano_neg_temp']}</div>", unsafe_allow_html=True)
            st.markdown(DISCLAIMER_PADRAO, unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar plano completo (.txt)", data=st.session_state['plano_neg_temp'], file_name="plano_de_negocios.txt", mime="text/plain", use_container_width=True, key="invencoe50")
            with col_sv:
                if st.button("❤️ Salvar", key="sv_plano_neg", use_container_width=True):
                    st.session_state.projetos_salvos.append({'modulo':'PlanoNegocios','tema':ideia_plano[:60] if 'ideia_plano' in dir() else '','conteudo':st.session_state['plano_neg_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

        # ========================
        # MARKETING INTELIGENTE
        # ========================

    with _tab_Marketing:
        st.header("📣 Marketing Inteligente")

        ideia_mkt = st.text_area("💡 Ideia/produto:", height=80, value=st.session_state.ideia_padrao, key="ideia_mkt")
        canal_mkt = st.multiselect("📱 Canais de interesse:", ["Instagram","TikTok","Facebook","Google Ads","E-mail","WhatsApp"], default=["Instagram"], key="invencoe1")

        if st.button("📣 CRIAR MATERIAL DE MARKETING", key="invencoe51"):
            if ideia_mkt.strip():
                with st.spinner("Criando materiais..."):
                    canais_txt = ", ".join(canal_mkt) if canal_mkt else "redes sociais em geral"
                    prompt = (
                        f"Crie materiais de marketing para esta ideia.\\n"
                        f"Ideia: {ideia_mkt}. Canais: {canais_txt}\\n\\n"
                        f"FORMATO:\\n\\n"
                        f"📣 MARKETING — {ideia_mkt[:50].upper()}\\n\\n"
                        f"🎯 CAMPANHA PRINCIPAL (conceito):\\n[ideia central da campanha de lançamento]\\n\\n"
                        f"📰 3 HEADLINES PARA TESTAR:\\n[headline 1]\\n[headline 2]\\n[headline 3]\\n\\n"
                        f"📢 IDEIA DE ANÚNCIO PAGO:\\n[estrutura de anúncio — gancho, corpo, CTA]\\n\\n"
                        f"📱 3 IDEIAS DE POSTS:\\n[post 1]\\n[post 2]\\n[post 3]\\n\\n"
                        f"🎥 IDEIA DE VÍDEO CURTO:\\n[roteiro resumido para Reels/TikTok]\\n\\n"
                        f"🚀 ESTRATÉGIA DE LANÇAMENTO NOS CANAIS ({canais_txt}):\\n[como sequenciar o conteúdo nos primeiros 30 dias]"
                    )
                    res = invencoes_ia(prompt)
                    if res: st.session_state['res_marketing_invenc17'] = str(res)
                    salvar_projeto("Marketing", ideia_mkt[:60], res)
                    st.session_state['mkt_temp'] = res
            else:
                st.warning("Descreva a ideia.")

        if st.session_state.get('mkt_temp'):
            st.markdown(f"<div class='card-pink'>{st.session_state['mkt_temp']}</div>", unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['mkt_temp'], file_name="marketing.txt", mime="text/plain", use_container_width=True, key="invencoe52")
            with col_sv:
                if st.button("❤️ Salvar", key="sv_mkt", use_container_width=True):
                    st.session_state.projetos_salvos.append({'modulo':'Marketing','tema':ideia_mkt[:60] if 'ideia_mkt' in dir() else '','conteudo':st.session_state['mkt_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

        # ========================
        # SIMULADOR DE MERCADO
        # ========================

    with _tab_Simulador:
        st.header("🧪 Simulador de Mercado")
        st.markdown(DISCLAIMER_PADRAO, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            ideia_sim = st.text_area("💡 Ideia/produto:", height=80, value=st.session_state.ideia_padrao, key="ideia_sim")
            preco_sim = st.number_input("💰 Preço de venda (R$):", min_value=0.0, value=50.0, step=5.0, key="invencoe53")
        with col2:
            custo_sim = st.number_input("💸 Custo unitário (R$):", min_value=0.0, value=20.0, step=5.0, key="invencoe54")
            cenario_sim = st.selectbox("🧪 Cenário a simular:", [
                "Vender 100 unidades/mês", "Vender 1.000 unidades/mês", "Dobrar o preço",
                "Reduzir o preço em 30%", "Entrada de um concorrente forte", "Reduzir custos em 20%",
                "Cenário customizado (descrever)",
            ], key="invencoe3_d2")
            cenario_custom = ""
            if cenario_sim == "Cenário customizado (descrever)":
                cenario_custom = st.text_input("Descreva o cenário:", key="invencoe55")

        if st.button("🧪 SIMULAR CENÁRIO", key="invencoe56"):
            if ideia_sim.strip():
                with st.spinner("Simulando..."):
                    cenario_final = cenario_custom if cenario_sim == "Cenário customizado (descrever)" and cenario_custom.strip() else cenario_sim
                    margem_unit = preco_sim - custo_sim
                    prompt = (
                        f"Simule este cenário de mercado.\\n"
                        f"Ideia: {ideia_sim}. Preço: R${preco_sim}. Custo: R${custo_sim}. Margem unitária: R${margem_unit:.2f}\\n"
                        f"Cenário a simular: {cenario_final}\\n\\n"
                        f"FORMATO:\\n\\n"
                        f"🧪 SIMULAÇÃO: {cenario_final.upper()}\\n\\n"
                        f"📊 PROJEÇÃO NUMÉRICA:\\n[calcule receita, custo total e lucro estimado para esse cenário]\\n\\n"
                        f"📈 IMPACTO NO NEGÓCIO:\\n[o que isso significa na prática]\\n\\n"
                        f"⚠️ RISCOS DESSE CENÁRIO:\\n[o que pode dar errado]\\n\\n"
                        f"✅ COMO SE PREPARAR:\\n[ações para aproveitar ou se proteger desse cenário]"
                    )
                    res = invencoes_ia(prompt)
                    if res: st.session_state['res_simulador_invenc18'] = str(res)
                    salvar_projeto("Simulador", cenario_final, res)
                    st.session_state['sim_temp'] = res
            else:
                st.warning("Descreva a ideia.")

        if st.session_state.get('sim_temp'):
            st.markdown(f"<div class='card-dark'>{st.session_state['sim_temp']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar (.txt)", data=st.session_state['sim_temp'], file_name="simulacao.txt", mime="text/plain", key="invencoe57")

        # ========================
        # PAINEL DE RISCOS
        # ========================

    with _tab_Riscos:
        st.header("📊 Painel de Riscos")

        ideia_risco = st.text_area("💡 Ideia/produto:", height=80, value=st.session_state.ideia_padrao, key="ideia_risco")

        if st.button("📊 MAPEAR RISCOS", key="invencoe58"):
            if ideia_risco.strip():
                with st.spinner("Mapeando riscos..."):
                    prompt = (
                        f"Mapeie os riscos completos desta ideia, com honestidade.\\n"
                        f"Ideia: {ideia_risco}\\n\\n"
                        f"FORMATO:\\n\\n"
                        f"📊 PAINEL DE RISCOS — {ideia_risco[:50].upper()}\\n\\n"
                        f"⚠️ PRINCIPAIS RISCOS:\\n[liste 4-6 riscos reais, do mais para o menos crítico]\\n\\n"
                        f"🚧 OBSTÁCULOS:\\n[barreiras práticas para executar essa ideia]\\n\\n"
                        f"🎯 PONTOS CRÍTICOS:\\n[os momentos/decisões que mais podem fazer a ideia falhar]\\n\\n"
                        f"🛡️ COMO REDUZIR CADA RISCO:\\n[para cada risco listado, uma ação de mitigação]"
                    )
                    res = invencoes_ia(prompt)
                    if res: st.session_state['res_riscos_invenc19'] = str(res)
                    salvar_projeto("Riscos", ideia_risco[:60], res)
                    st.session_state['risco_temp'] = res
            else:
                st.warning("Descreva a ideia.")

        if st.session_state.get('risco_temp'):
            st.markdown(f"<div class='card-red'>{st.session_state['risco_temp']}</div>", unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['risco_temp'], file_name="painel_riscos.txt", mime="text/plain", use_container_width=True, key="invencoe59")
            with col_sv:
                if st.button("❤️ Salvar", key="sv_risco", use_container_width=True):
                    st.session_state.projetos_salvos.append({'modulo':'Riscos','tema':ideia_risco[:60] if 'ideia_risco' in dir() else '','conteudo':st.session_state['risco_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

        # ========================
        # BANCO DE IDEIAS
        # ========================

    with _tab_BancoIdeias:
        st.header("💎 Banco de Ideias")
        st.markdown("Quando faltar inspiração, gere ideias novas em qualquer área.")

        area_banco = st.selectbox("Área:", [
            "Tecnologia","Saúde","Educação","Agricultura","Indústria","Alimentação",
            "Meio Ambiente","Serviços","Aplicativos","Inteligência Artificial","Qualquer área (surpreenda-me)",
        ], key="invencoe2")
        qtd_ideias = st.slider("Quantas ideias gerar:", 3, 15, 5, key="invencoe2_d2")

        if st.button("💎 GERAR IDEIAS", key="invencoe60"):
            with st.spinner("Gerando ideias..."):
                prompt = (
                    f"Gere {qtd_ideias} ideias de produtos/negócios/invenções na área: {area_banco}\\n\\n"
                    f"FORMATO — para cada ideia:\\n\\n"
                    f"💡 [NOME DA IDEIA]\\n"
                    f"[Descrição em 2-3 linhas: o que é e que problema resolve]\\n"
                    f"Potencial: [Baixo/Médio/Alto]\\n\\n"
                    f"[Repita para as {qtd_ideias} ideias, todas diferentes entre si]"
                )
                res = invencoes_ia(prompt)
                if res: st.session_state['res_bancoideias_invenc20'] = str(res)
                salvar_projeto("BancoIdeias", area_banco, res)
                st.session_state['banco_temp'] = res
                st.session_state.banco_ideias_geradas.append({'area': area_banco, 'data': datetime.now().strftime('%d/%m/%Y')})

        if st.session_state.get('banco_temp'):
            st.markdown(f"<div class='card'>{st.session_state['banco_temp']}</div>", unsafe_allow_html=True)
            st.download_button("📋 Baixar ideias (.txt)", data=st.session_state['banco_temp'], file_name="banco_de_ideias.txt", mime="text/plain", key="invencoe61")

        # ========================
        # INVESTIDOR IA
        # ========================

    with _tab_Investidor:
        st.header("🤝 Investidor IA")
        st.markdown("Veja como sua ideia seria avaliada por um investidor.")

        ideia_inv = st.text_area("💡 Ideia/produto:", height=100, value=st.session_state.ideia_padrao, key="ideia_inv")
        estagio_inv = st.selectbox("📊 Estágio atual:", ["Apenas ideia","Protótipo","MVP funcionando","Já vendendo","Negócio estabelecido buscando expansão"], key="invencoe62")

        if st.button("🤝 ANALISAR COMO INVESTIDOR", key="invencoe63"):
            if ideia_inv.strip():
                with st.spinner("Analisando como investidor..."):
                    prompt = (
                        f"Analise esta ideia do ponto de vista de um investidor.\\n"
                        f"Ideia: {ideia_inv}. Estágio: {estagio_inv}\\n\\n"
                        f"FORMATO:\\n\\n"
                        f"🤝 ANÁLISE DO INVESTIDOR — {ideia_inv[:50].upper()}\\n\\n"
                        f"📈 POTENCIAL DE CRESCIMENTO: [Baixo/Médio/Alto] — [justificativa honesta]\\n\\n"
                        f"📊 ESCALABILIDADE: [Baixa/Média/Alta] — [justificativa]\\n\\n"
                        f"⭐ DIFERENCIAL COMPETITIVO: [comentário honesto sobre o quão defensável é a ideia]\\n\\n"
                        f"🎯 ATRATIVIDADE PARA INVESTIMENTO: [Baixa/Média/Alta] — [no estágio atual: {estagio_inv}]\\n\\n"
                        f"❓ PRINCIPAIS OBJEÇÕES QUE UM INVESTIDOR FARIA:\\n[3-4 perguntas difíceis reais]\\n\\n"
                        f"✅ O QUE FORTALECERIA A IDEIA PARA INVESTIDORES:\\n[1-2 ações prioritárias antes de buscar investimento]"
                    )
                    res = invencoes_ia(prompt, "Seja honesto como um investidor real seria — investidores fazem perguntas difíceis e não se impressionam facilmente. Não infle a avaliação para agradar.")
                    if res: st.session_state['res_investidor_invenc21'] = str(res)
                    salvar_projeto("Investidor", ideia_inv[:60], res)
                    st.session_state['investidor_temp'] = res
            else:
                st.warning("Descreva a ideia.")

        if st.session_state.get('investidor_temp'):
            st.markdown(f"<div class='card-dark'>{st.session_state['investidor_temp']}</div>", unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['investidor_temp'], file_name="analise_investidor.txt", mime="text/plain", use_container_width=True, key="invencoe64")
            with col_sv:
                if st.button("❤️ Salvar", key="sv_investidor", use_container_width=True):
                    st.session_state.projetos_salvos.append({'modulo':'Investidor','tema':ideia_inv[:60] if 'ideia_inv' in dir() else '','conteudo':st.session_state['investidor_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

        # ========================
        # PITCH PERFEITO
        # ========================

    with _tab_Pitch:
        st.header("🎤 Pitch Perfeito")

        col1, col2 = st.columns(2)
        with col1:
            ideia_pitch = st.text_area("💡 Ideia/produto:", height=80, value=st.session_state.ideia_padrao, key="ideia_pitch")
        with col2:
            duracao_pitch = st.selectbox("⏱️ Duração:", ["30 segundos","1 minuto","3 minutos","10 minutos"], key="invencoe65")
            audiencia_pitch = st.selectbox("🎯 Audiência:", ["Investidores","Clientes","Parceiros/Sócios","Banco/Crédito"], key="invencoe66")

        if st.button("🎤 CRIAR PITCH", key="invencoe67"):
            if ideia_pitch.strip():
                with st.spinner("Criando o pitch..."):
                    prompt = (
                        f"Crie um pitch de {duracao_pitch} para {audiencia_pitch}.\\n"
                        f"Ideia: {ideia_pitch}\\n\\n"
                        f"FORMATO:\\n\\n"
                        f"🎤 PITCH DE {duracao_pitch.upper()} — PARA {audiencia_pitch.upper()}\\n\\n"
                        f"[Script completo, palavra por palavra, adequado à duração e à audiência — "
                        f"para investidores foque em números/escala, para clientes foque no benefício, "
                        f"para parceiros foque na visão compartilhada, para banco foque em solidez/garantias]\\n\\n"
                        f"🎯 GANCHO DE ABERTURA:\\n[a frase que precisa capturar atenção nos primeiros segundos]\\n\\n"
                        f"💡 DICA DE ENTREGA:\\n[como falar — tom, postura, ritmo para essa duração e audiência]"
                    )
                    res = invencoes_ia(prompt)
                    if res: st.session_state['res_pitch_invenc22'] = str(res)
                    salvar_projeto("Pitch", f"{duracao_pitch} — {audiencia_pitch}", res)
                    st.session_state['pitch_temp'] = res
            else:
                st.warning("Descreva a ideia.")

        if st.session_state.get('pitch_temp'):
            st.markdown(f"<div class='card-green'>{st.session_state['pitch_temp']}</div>", unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['pitch_temp'], file_name="pitch.txt", mime="text/plain", use_container_width=True, key="invencoe68")
            with col_sv:
                if st.button("❤️ Salvar", key="sv_pitch", use_container_width=True):
                    st.session_state.projetos_salvos.append({'modulo':'Pitch','tema':ideia_pitch[:60] if 'ideia_pitch' in dir() else '','conteudo':st.session_state['pitch_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

        # ========================
        # CRONOGRAMA INTELIGENTE
        # ========================

    with _tab_Cronograma:
        st.header("📅 Cronograma Inteligente")

        ideia_cron = st.text_area("💡 Ideia/produto:", height=80, value=st.session_state.ideia_padrao, key="ideia_cron")
        prazo_cron = st.text_input("📅 Prazo total do projeto:", placeholder="ex: 3 meses, 1 ano...", key="invencoe69")

        if st.button("📅 GERAR CRONOGRAMA", key="invencoe70"):
            if ideia_cron.strip():
                with st.spinner("Montando cronograma..."):
                    prompt = (
                        f"Crie um cronograma detalhado para este projeto.\\n"
                        f"Ideia: {ideia_cron}. Prazo total: {prazo_cron or 'a definir'}\\n\\n"
                        f"FORMATO:\\n\\n"
                        f"📅 CRONOGRAMA — {ideia_cron[:50].upper()}\\n\\n"
                        f"☀️ HOJE (próximas 24h):\\n[ação imediata e concreta]\\n\\n"
                        f"📆 ESTA SEMANA:\\n[3-5 ações]\\n\\n"
                        f"📅 PRÓXIMO MÊS:\\n[principais marcos]\\n\\n"
                        f"🗓️ PRÓXIMOS {prazo_cron or '3 meses'}:\\n[etapas principais até o prazo final]\\n\\n"
                        f"🏁 MARCO FINAL:\\n[o que define que o projeto atingiu esse objetivo de prazo]"
                    )
                    res = invencoes_ia(prompt)
                    if res: st.session_state['res_cronograma_invenc23'] = str(res)
                    salvar_projeto("Cronograma", ideia_cron[:60], res)
                    st.session_state['cron_temp'] = res
            else:
                st.warning("Descreva a ideia.")

        if st.session_state.get('cron_temp'):
            st.markdown(f"<div class='card-teal'>{st.session_state['cron_temp']}</div>", unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['cron_temp'], file_name="cronograma.txt", mime="text/plain", use_container_width=True, key="invencoe71")
            with col_sv:
                if st.button("❤️ Salvar", key="sv_cron", use_container_width=True):
                    st.session_state.projetos_salvos.append({'modulo':'Cronograma','tema':ideia_cron[:60] if 'ideia_cron' in dir() else '','conteudo':st.session_state['cron_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

        # ========================
        # MENTOR 24 HORAS
        # ========================

    with _tab_Mentor:
        st.header("🤖 Mentor 24 Horas")
        st.markdown("Converse livremente sobre seu projeto.")

        if 'chat_mentor' not in st.session_state:
            st.session_state.chat_mentor = []
        if 'mentor_key' not in st.session_state:
            st.session_state.mentor_key = 0

        if st.session_state.chat_mentor:
            for msg in st.session_state.chat_mentor:
                if msg['role'] == 'user':
                    st.markdown(f"<div style='background:#FFFBEB;border:1px solid #D97706;border-radius:12px 12px 4px 12px;padding:12px 16px;margin:8px 0;'><b>Você:</b> {msg['content']}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='card-dark' style='margin:8px 0;'><b>💡 Mentor:</b><br>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(\"\"\"<div style="background:#FFFBEB;border:1px dashed #D97706;border-radius:12px;padding:16px;text-align:center;">
            🤖 <strong>Pergunte qualquer coisa sobre seu projeto!</strong> Ex: "Devo focar em B2B ou B2C primeiro?",
            "Como conseguir os primeiros 10 clientes sem dinheiro para anúncios?"
            </div>\"\"\", unsafe_allow_html=True)

        pergunta_mentor = st.text_input("Sua pergunta:", key=f"mentor_input_{st.session_state.mentor_key}", placeholder="Pergunte qualquer coisa sobre seu projeto...")

        col_env, col_limpar = st.columns([3, 1])
        with col_env:
            if st.button("📤 PERGUNTAR", key="invencoe72"):
                if pergunta_mentor.strip():
                    with st.spinner("Pensando..."):
                        historico_msgs = [{"role": m["role"], "content": m["content"]} for m in st.session_state.chat_mentor[-10:]]
                        resp = invencoes_ia(pergunta_mentor, "Você é um mentor de startups e inovação experiente, direto e estratégico. Responda com profundidade mas sem rodeios.")
                        if resp: st.session_state['res_mentor_invenc24'] = str(resp)
                    st.session_state.chat_mentor.append({"role": "user", "content": pergunta_mentor})
                    st.session_state.chat_mentor.append({"role": "assistant", "content": resp})
                    st.session_state.mentor_key += 1
                    salvar_projeto("Mentor", pergunta_mentor[:60], resp)
                    st.rerun()
                else:
                    st.warning("Digite sua pergunta.")
        with col_limpar:
            if st.button("🗑️ Limpar", key="invencoe73"):
                st.session_state.chat_mentor = []
                st.rerun()

        # ========================
        # LABORATÓRIO DE INVENÇÕES DO FUTURO
        # ========================

    with _tab_Laboratorio:
        st.header("⭐ Laboratório de Invenções do Futuro")
        st.markdown("Informe um problema real — a IA combina múltiplas áreas para propor soluções inovadoras.")

        st.markdown(\"\"\"<div class="ideia-icon-box">
        <div style="font-size:2.5em;">⭐</div>
        <div style="font-size:1.1em;font-weight:600;">Equipe Multidisciplinar de Inovação</div>
        <div style="font-size:0.85em;margin-top:6px;">Engenharia · Tecnologia · Design · Psicologia · Logística · Negócios</div>
        </div>\"\"\", unsafe_allow_html=True)

        problema_lab = st.text_area("❓ Qual problema você quer resolver?", height=100,
            placeholder="ex: Como reduzir acidentes de bicicleta? Como economizar água em casa? Como diminuir filas em hospitais?", key="invencoe1_d2")

        if st.button("⭐ GERAR SOLUÇÕES MULTIDISCIPLINARES", key="invencoe74"):
            if problema_lab.strip():
                with st.spinner("Combinando conhecimentos de múltiplas áreas..."):
                    prompt = (
                        f"Combine conhecimentos de engenharia, tecnologia, design, psicologia, logística e negócios "
                        f"para propor soluções inovadoras para este problema.\\n"
                        f"Problema: {problema_lab}\\n\\n"
                        f"FORMATO:\\n\\n"
                        f"⭐ SOLUÇÕES PARA: {problema_lab.upper()}\\n\\n"
                        f"💡 SOLUÇÃO 1 — [nome]:\\n"
                        f"[Descrição da solução]\\n"
                        f"Áreas combinadas: [quais disciplinas essa solução usa]\\n"
                        f"Por que funciona: [lógica por trás]\\n\\n"
                        f"💡 SOLUÇÃO 2 — [nome]:\\n"
                        f"[mesma estrutura]\\n\\n"
                        f"💡 SOLUÇÃO 3 — [nome, mais não-convencional/criativa]:\\n"
                        f"[mesma estrutura]\\n\\n"
                        f"🔧 SOLUÇÃO 4 — [adaptação de tecnologia existente]:\\n"
                        f"[uma tecnologia que já existe em outro contexto, adaptada para esse problema]\\n\\n"
                        f"🚀 CONCEITO MAIS PROMISSOR:\\n"
                        f"[qual das soluções acima parece ter mais potencial e por quê]\\n\\n"
                        f"⚠️ MAIOR DESAFIO PARA IMPLEMENTAR:\\n"
                        f"[seja honesto sobre a dificuldade real de execução]"
                    )
                    res = invencoes_ia(prompt, "Seja genuinamente criativo e multidisciplinar. Combine perspectivas de diferentes áreas de forma real, não superficial. Inclua pelo menos uma ideia pouco convencional.")
                    if res: st.session_state['res_laboratorio_invenc25'] = str(res)
                    salvar_projeto("Laboratorio", problema_lab[:60], res)
                    st.session_state['lab_temp'] = res
            else:
                st.warning("Descreva o problema que você quer resolver.")

        if st.session_state.get('lab_temp'):
            st.markdown(f"<div class='card-dark'>{st.session_state['lab_temp']}</div>", unsafe_allow_html=True)
            st.markdown(DISCLAIMER_PADRAO, unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['lab_temp'], file_name="laboratorio_invencoes.txt", mime="text/plain", use_container_width=True, key="invencoe75")
            with col_sv:
                if st.button("❤️ Salvar", key="sv_lab", use_container_width=True):
                    st.session_state.projetos_salvos.append({'modulo':'Laboratorio','tema':problema_lab[:60] if 'problema_lab' in dir() else '','conteudo':st.session_state['lab_temp'],'data':datetime.now().strftime('%d/%m %H:%M')})
                    st.success("❤️ Salvo!")

        # ========================
        # BIBLIOTECA
        # ========================

    with _tab_Biblioteca:
        st.header("📚 Biblioteca de Projetos")

        if not st.session_state.projetos_salvos:
            st.info("Biblioteca vazia. Gere análises nos módulos e salve as importantes aqui!")
        else:
            modulos_bib = list(set(c['modulo'] for c in st.session_state.projetos_salvos))
            filtro = st.selectbox("Filtrar por módulo:", ["Todos"] + modulos_bib, key="select_filtro_bib")
            consultas_f = [c for c in st.session_state.projetos_salvos if filtro == "Todos" or c['modulo'] == filtro]

            st.markdown(f"**{len(consultas_f)} análise(s) encontrada(s)**")
            for i, item in enumerate(reversed(consultas_f)):
                idx_real = len(st.session_state.projetos_salvos) - 1 - i
                with st.expander(f"[{item.get('modulo', '')}] {item.get('tema', '')[:60]} — {item['data']}"):
                    st.markdown(f"<div class='card'>{item['conteudo']}</div>", unsafe_allow_html=True)
                    col_dl, col_del = st.columns([3, 1])
                    with col_dl:
                        st.download_button("📋 Baixar", data=item['conteudo'], file_name=f"{item.get('modulo', '').lower()}.txt", mime="text/plain", key=f"dl_bib_{i}")
                    with col_del:
                        if st.button("🗑️ Remover", key=f"del_bib_{i}"):
                            st.session_state.projetos_salvos.pop(idx_real)
                            st.rerun()

        if st.session_state.projetos_ativos:
            st.markdown("<hr class='divider'>", unsafe_allow_html=True)
            st.markdown("### 📂 Seus Projetos Ativos")
            for p in st.session_state.projetos_ativos:
                st.markdown(f"<span class='badge'>💡 {p}</span>", unsafe_allow_html=True)

        if st.session_state.historico_projetos:
            st.markdown("<hr class='divider'>", unsafe_allow_html=True)
            historico_txt = "\\n\\n".join(f"[{c['data']}] {c['modulo']} — {c['tema']}\\n{c['conteudo']}\\n{'─'*40}" for c in st.session_state.historico_projetos)
            st.download_button("⬇️ Exportar todo o histórico (.txt)", data=historico_txt, file_name="historico_invencoes.txt", mime="text/plain", key="invencoe76")
            if st.button("🗑️ Limpar Todo o Histórico", key="invencoe77"):
                st.session_state.historico_projetos = []
                st.rerun()

        # --- RODAPÉ ---
        st.markdown(
        "<div style='text-align:center;color:#999;font-size:0.8em;margin-top:60px;'>"
        "© 2026 Invenções IA — Laboratório de Inovação com IA · MeusAgentesIA.com.br"
        "</div>", unsafe_allow_html=True
        )


# --- RODAPÉ ---
st.markdown(
    "<div style='text-align:center;color:#999;font-size:0.8em;margin-top:60px;'>"
    "</div>", unsafe_allow_html=True
)
""",
    "nexus_launcher": """# [hub] import json
# [hub] import streamlit as st
# [hub] from groq import Groq
# [hub] from datetime import timedelta, date, datetime
# [hub] import re

# --- CONFIGURAÇÃO DA PÁGINA ---
# set_page_config removido pelo super_agente

st.markdown(\"\"\"
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
[data-testid="stToolbar"] {visibility: hidden;}
[data-testid="stDecoration"] {visibility: hidden;}
[data-testid="stStatusWidget"] {visibility: hidden;}
</style>
\"\"\", unsafe_allow_html=True)


# --- ESTILO CSS ---
st.markdown(\"\"\"
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    .stApp { background-color:#F6FBF4; font-family:'Inter',sans-serif; }
    [data-testid="stSidebar"] { display:none; }

    .stTextInput>div>div>input, .stTextArea>div>textarea,
    .stSelectbox>div>div>div, .stNumberInput>div>div>input {
        background-color:#FFFFFF !important; color:#1A1A2E !important;
        border:1px solid #CED4DA !important; font-family:'Inter',sans-serif !important;
    }

    .stButton>button {
        width:100%; border-radius:10px; height:3.2em;
        background:linear-gradient(135deg,#16A34A,#15803D) !important; color:white !important;
        font-weight:600; border:none; box-shadow:2px 2px 8px rgba(0,0,0,0.1);
        font-family:'Inter',sans-serif !important; transition:all 0.2s ease;
    }
    .stButton>button:hover { background:linear-gradient(135deg,#15803D,#166534) !important; transform:translateY(-1px); }
    .stApp .stButton>button, .stApp .stButton>button p,
    .stApp .stButton>button span, .stApp .stButton>button div { color:white !important; }

    .stApp h1, .stApp h2, .stApp h3 { color:#14532D !important; font-family:'Inter',sans-serif !important; font-weight:700 !important; }

    .card { background:linear-gradient(135deg,#F0FDF4,#DCFCE7); padding:20px; border-radius:14px; border:1px solid #86EFAC; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card, .stApp .card p, .stApp .card span, .stApp .card div, .stApp .card strong, .stApp .card em { color:#14532D !important; }

    .card-dark { background:linear-gradient(135deg,#DCFCE7,#D1FAE5); padding:20px; border-radius:14px; border:1px solid #6EE7B7; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-dark, .stApp .card-dark p, .stApp .card-dark span, .stApp .card-dark div, .stApp .card-dark strong { color:#14532D !important; }

    .card-green { background:linear-gradient(135deg,#DCFCE7,#BBF7D0); padding:20px; border-radius:14px; border:1px solid #4ADE80; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-green, .stApp .card-green p, .stApp .card-green span, .stApp .card-green div { color:#14532D !important; }

    .card-blue { background:linear-gradient(135deg,#EFF6FF,#DBEAFE); padding:20px; border-radius:14px; border:1px solid #93C5FD; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-blue, .stApp .card-blue p, .stApp .card-blue span, .stApp .card-blue div { color:#1E3A8A !important; }

    .card-red { background:linear-gradient(135deg,#FFF5F5,#FEE2E2); padding:20px; border-radius:14px; border:1px solid #FECACA; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-red, .stApp .card-red p, .stApp .card-red span, .stApp .card-red div { color:#7F1D1D !important; }

    .card-yellow { background:linear-gradient(135deg,#FFFBEB,#FEF3C7); padding:18px; border-radius:12px; border:1px solid #FCD34D; margin-bottom:12px; white-space:normal; word-wrap:break-word; }
    .stApp .card-yellow, .stApp .card-yellow p, .stApp .card-yellow span, .stApp .card-yellow div { color:#78350F !important; }

    .stat-box { background:#FFFFFF; border-radius:12px; padding:16px; text-align:center; border:1px solid #86EFAC; }
    .stApp .stat-box div, .stApp .stat-box span, .stApp .stat-box p { color:#14532D !important; }
    .stApp .stat-numero, .stat-numero { font-size:2em; font-weight:700; color:#166534 !important; }

    .hist-item { background:#FFFFFF; border-radius:10px; padding:12px 16px; margin-bottom:8px; border-left:4px solid #86EFAC; }
    .stApp .hist-item, .stApp .hist-item p, .stApp .hist-item span, .stApp .hist-item div, .stApp .hist-item small { color:#14532D !important; }

    .badge { background:#166534; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-verde { background:#059669; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-amarelo { background:#B45309; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-azul { background:#1D4ED8; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-roxo { background:#6D28D9; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }

    .divider { border:none; height:1px; background:linear-gradient(to right,transparent,#86EFAC,transparent); margin:18px 0; }

    .chat-user { background:#FFFFFF; border:1px solid #86EFAC; border-radius:12px 12px 4px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-user, .stApp .chat-user p, .stApp .chat-user span, .stApp .chat-user div { color:#14532D !important; }

    .chat-persona { background:#F6FBF4; border:1px solid #86EFAC; border-radius:4px 12px 12px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-persona, .stApp .chat-persona p, .stApp .chat-persona span, .stApp .chat-persona div { color:#14532D !important; }

    .questao-box { background:#FFFFFF; border:2px solid #86EFAC; border-radius:12px; padding:18px; margin-bottom:14px; }
    .stApp .questao-box, .stApp .questao-box p, .stApp .questao-box span, .stApp .questao-box div { color:#14532D !important; }

    .avaliacao-box { background:#FFFFFF; border:2px solid #86EFAC; border-radius:14px; padding:18px; margin-bottom:12px; }
    .stApp .avaliacao-box, .stApp .avaliacao-box p, .stApp .avaliacao-box span, .stApp .avaliacao-box div { color:#14532D !important; }

    .meta-box { background:#FFFFFF; border:2px solid #86EFAC; border-radius:12px; padding:16px; text-align:center; margin:10px 0; }
    .stApp .meta-box, .stApp .meta-box div, .stApp .meta-box span { color:#14532D !important; }
    .stApp .meta-numero { font-size:2em; font-weight:700; color:#166534 !important; }

    .chat-scroll-container { max-height:40vh; overflow-y:auto; display:flex; flex-direction:column; scroll-behavior:smooth; padding-bottom:4px; }
    .chat-scroll-container > * { flex-shrink:0; }
    

    </style>
\"\"\", unsafe_allow_html=True)

# --- PERSISTÊNCIA: SUPABASE → GOOGLE SHEETS → MEMÓRIA ---
import os, json

# ── SUPABASE ──────────────────────────────────────────────────
def _get_supabase():
    try:
        url = os.environ.get("SUPABASE_URL","").strip()
        key = os.environ.get("SUPABASE_KEY","").strip()
        if not url or not key: return None
        from supabase import create_client
        return create_client(url, key)
    except Exception:
        return None

def sb_carregar(sb):
    try:
        res = sb.table("projetos").select("nome, dados").execute()
        return {r["nome"]: json.loads(r["dados"]) for r in (res.data or [])}
    except Exception: return {}

def sb_salvar(sb, nome, dados):
    try:
        sb.table("projetos").upsert({"nome": nome, "dados": json.dumps(dados, default=str)}, on_conflict="nome").execute()
        return True
    except Exception: return False

def sb_deletar(sb, nome):
    try:
        sb.table("projetos").delete().eq("nome", nome).execute()
        return True
    except Exception: return False

# ── GOOGLE SHEETS ─────────────────────────────────────────────
def _get_sheets():
    try:
        sheet_id = os.environ.get("GSHEET_ID","").strip()
        creds_json = os.environ.get("GSHEET_CREDS","").strip()
        if not sheet_id or not creds_json: return None
        import gspread
        from google.oauth2.service_account import Credentials
        scopes = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]
        creds_dict = json.loads(creds_json)
        creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
        gc = gspread.authorize(creds)
        sh = gc.open_by_key(sheet_id)
        try:
            ws = sh.worksheet("projetos")
        except Exception:
            ws = sh.add_worksheet(title="projetos", rows=1000, cols=3)
            ws.append_row(["nome","dados","criado_em"])
        return ws
    except Exception:
        return None

def gs_carregar(ws):
    try:
        rows = ws.get_all_records()
        result = {}
        for r in rows:
            if r.get("nome") and r.get("dados"):
                try: result[r["nome"]] = json.loads(r["dados"])
                except: pass
        return result
    except Exception: return {}

def gs_salvar(ws, nome, dados):
    try:
        dados_str = json.dumps(dados, default=str)
        from datetime import datetime as _dt
        agora = _dt.now().strftime("%Y-%m-%d %H:%M")
        cell = None
        try: cell = ws.find(nome, in_column=1)
        except: pass
        if cell:
            ws.update(f"B{cell.row}", [[dados_str]])
        else:
            ws.append_row([nome, dados_str, agora])
        return True
    except Exception as e:
        return False

def gs_deletar(ws, nome):
    try:
        cell = ws.find(nome, in_column=1)
        if cell: ws.delete_rows(cell.row)
        return True
    except Exception: return False

# ── CACHE FALLBACK ────────────────────────────────────────────
@st.cache_resource
def get_cache_store():
    return {"projetos": {}}

_cache = get_cache_store()
_sb   = _get_supabase()
_gs   = _get_sheets() if not _sb else None

def _backend():
    if _sb:   return "supabase"
    if _gs:   return "sheets"
    return "memoria"

# ── INICIALIZAÇÃO DE ESTADO ───────────────────────────────────
_defaults = {'etapa': "Login", 'dados': {}, 'chat_hist': [],
    'chat_input_key': 0,
             'usuario': '', 'api_key': '', 'chat_input_key': 0,
             'projetos': {}, '_db_carregado': False}
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

if not st.session_state._db_carregado:
    if _sb:
        st.session_state.projetos = sb_carregar(_sb)
    elif _gs:
        st.session_state.projetos = gs_carregar(_gs)
    else:
        st.session_state.projetos = _cache["projetos"]
    _cache["projetos"] = st.session_state.projetos
    st.session_state._db_carregado = True

def salvar_projeto(nome, dados):
    dados_copy = dados.copy()
    if _sb:
        sb_salvar(_sb, nome, dados_copy)
    elif _gs:
        gs_salvar(_gs, nome, dados_copy)
    st.session_state.projetos[nome] = dados_copy
    _cache["projetos"][nome] = dados_copy

def deletar_projeto(nome):
    if _sb:   sb_deletar(_sb, nome)
    elif _gs: gs_deletar(_gs, nome)
    st.session_state.projetos.pop(nome, None)
    _cache["projetos"].pop(nome, None)

# ── SALVAR LOCALMENTE (download automático via botão) ─────────
def gerar_json_projeto(dados: dict) -> str:
    \"\"\"Serializa o projeto inteiro em JSON para download local.\"\"\"
    return json.dumps(dados, ensure_ascii=False, indent=2, default=str)


# --- ETAPAS ---
ETAPAS_LABELS = {
    "Formulario":      "1. Formulário",
    "Potencial_Nicho": "2. Potencial",
    "Gerar_Ebook":     "3. E-book",
    "Gerar_Bonus":     "4. Bônus",
    "Copy_Face":       "5. Anúncio",
    "Copy_LP":         "6. Landing Page",
    "Mensagens_Grupo": "7. Mensagens",
    "Visualizacao":    "8. Projeto Final",
}

# --- EXEMPLOS ---
EXEMPLOS = {
    "Emagrecimento": {
        "nicho": "emagrecimento", "publico": "mulheres de 30 a 50 anos que querem emagrecer",
        "nome_eb": "Barriga Zero em 30 Dias", "dor": "não consigo perder peso mesmo fazendo dieta e exercício",
        "atual": "A pessoa está acima do peso, frustrada com dietas que não funcionam e sem energia no dia a dia",
        "desejada": "Ter um corpo mais saudável, se sentir bonita, ter disposição e autoestima elevada",
        "promessa": "Emagrecer até 7kg em 30 dias com um método simples e sem passar fome",
        "diferencial": "Método baseado em refeições rápidas de até 15 minutos, sem academia",
    },
    "Criptomoedas": {
        "nicho": "criptomoedas", "publico": "iniciantes que querem investir em cripto mas têm medo de perder dinheiro",
        "nome_eb": "Cripto do Zero: Como Começar a Investir com Segurança",
        "dor": "medo de perder dinheiro por falta de conhecimento sobre o mercado cripto",
        "atual": "A pessoa ouve falar de cripto mas não entende nada, fica de fora e vê outros lucrando",
        "desejada": "Entender como funciona o mercado, fazer os primeiros investimentos com segurança e confiança",
        "promessa": "Aprender a investir em criptomoedas do zero, com segurança, mesmo sem experiência",
        "diferencial": "Linguagem simples, sem jargões técnicos, com passo a passo prático para iniciantes",
    },
    "Renda Extra": {
        "nicho": "renda extra", "publico": "pessoas que trabalham com carteira assinada e querem ganhar dinheiro extra online",
        "nome_eb": "Renda Extra Digital: Ganhe R$1.000 por Mês Trabalhando 1 Hora por Dia",
        "dor": "salário não cobre todas as despesas e não há tempo para um segundo emprego",
        "atual": "A pessoa está endividada ou no limite financeiro, sem tempo livre e sem saber por onde começar",
        "desejada": "Ter uma renda extra de pelo menos R$1.000 por mês trabalhando no celular nas horas vagas",
        "promessa": "Gerar R$1.000 extras por mês pelo celular em apenas 1 hora por dia",
        "diferencial": "Estratégias testadas que não exigem investimento inicial nem experiência prévia",
    },
    "Relacionamentos": {
        "nicho": "relacionamentos", "publico": "mulheres de 25 a 45 anos que querem reconquistar ou melhorar seu relacionamento",
        "nome_eb": "Amor de Volta: Como Reconquistar Quem Você Ama em 21 Dias",
        "dor": "terminou um relacionamento e não sabe como reconquistar ou se deve tentar",
        "atual": "A pessoa está sofrendo após um término, se sentindo perdida e sem esperança de reconciliação",
        "desejada": "Reconquistar a pessoa amada ou ter clareza para seguir em frente com autoestima elevada",
        "promessa": "Reconquistar o ex em 21 dias usando técnicas de psicologia comportamental",
        "diferencial": "Método com base em psicologia aplicada, sem joguinhos ou manipulação",
    },
}

# --- FUNÇÃO DE IA ---
def chamar_ia(prompt: str, system_prompt: str) -> str:
    try:
        client = Groq(api_key=st.session_state.api_key)
        response = client.chat.completions.create(
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}],
            model="openai/gpt-oss-120b",
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Erro na API: {e}"

def limpar_html(texto: str) -> str:
    limpo = re.sub(r'<[^>]+>', '', texto)
    return limpo.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').strip()


def corrigir_texto(texto: str) -> str:
    prompt = (
        f"Corrija o texto abaixo. Corrija: ortografia, acentuação, concordância verbal e nominal, "
        f"pontuação e erros de digitação. Mantenha o tom, estilo e estrutura originais. "
        f"Não reescreva — apenas corrija os erros. Retorne SOMENTE o texto corrigido, sem comentários.\\n\\n"
        f"TEXTO:\\n{texto}"
    )
    system = "Você é um revisor gramatical especialista em português brasileiro. Corrija apenas o necessário. REGRA DE OURO — CONFIABILIDADE 100%%: Forneça APENAS informações que você tem certeza absoluta que são verdadeiras. JAMAIS invente, suponha, extrapole ou preencha lacunas com dados fictícios. Se não souber algo com certeza — preço, endereço, horário, nome, estatística, lei, fato — diga EXPLICITAMENTE: 'Não tenho certeza sobre isso, recomendo verificar em [fonte].' É melhor uma resposta incompleta e honesta do que uma resposta completa e inventada. O usuário depende dessas informações para tomar decisões reais."
    try:
        client = Groq(api_key=st.session_state.api_key)
        resp = client.chat.completions.create(
            messages=[{"role":"system","content":system},{"role":"user","content":prompt}],
            model="openai/gpt-oss-120b"
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Erro: {e}"

def gerar_ics(eventos: list) -> str:
    linhas = [
        'BEGIN:VCALENDAR',
        'VERSION:2.0',
        'PRODID:-//Nexus Launcher//Agendador//PT',
        'CALSCALE:GREGORIAN',
        'METHOD:PUBLISH',
    ]
    for ev in eventos:
        try:
            h, m = map(int, ev['hora'].split(':'))
        except Exception:
            h, m = 9, 0
        dt_start = datetime(ev['data'].year, ev['data'].month, ev['data'].day, h, m, 0)
        dt_end   = datetime(ev['data'].year, ev['data'].month, ev['data'].day, h, m + 30 if m <= 29 else m, 0)
        uid = f"{ev['data'].strftime('%Y%m%d')}-{ev['chave']}@nexuslauncher"
        desc = ev['descricao'].replace('\\n', '\\\\n').replace(',', r'\\,').replace(';', r'\\;')[:500]
        linhas += [
            'BEGIN:VEVENT',
            f"UID:{uid}",
            f"DTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}",
            f"DTSTART:{dt_start.strftime('%Y%m%dT%H%M%S')}",
            f"DTEND:{dt_end.strftime('%Y%m%dT%H%M%S')}",
            f"SUMMARY:{ev['titulo']}",
            f"DESCRIPTION:{desc}",
            'BEGIN:VALARM',
            'TRIGGER:-PT30M',
            'ACTION:DISPLAY',
            f"DESCRIPTION:Lembrete: {ev['titulo']}",
            'END:VALARM',
            'END:VEVENT',
        ]
    linhas.append('END:VCALENDAR')
    return '\\r\\n'.join(linhas)

def normalizar_markdown(texto: str) -> str:
    linhas = texto.split('\\n')
    resultado = []
    for linha in linhas:
        if linha.startswith('#### '): linha = f"<h4>{linha[5:]}</h4>"
        elif linha.startswith('### '): linha = f"<h3>{linha[4:]}</h3>"
        elif linha.startswith('## '): linha = f"<h2>{linha[3:]}</h2>"
        elif linha.startswith('# '): linha = f"<h2>{linha[2:]}</h2>"
        linha = re.sub(r'\\*\\*(.+?)\\*\\*', r'<strong>\\1</strong>', linha)
        linha = re.sub(r'\\*(.+?)\\*', r'<em>\\1</em>', linha)
        resultado.append(linha)
    return '\\n'.join(resultado)

# --- PARSERS ---
def _linha_e_marcador_bonus(linha):
    l = linha.strip().replace("🎁", "").strip()
    lu = l.upper()
    for num in ("1", "2", "3"):
        for pref in (f"BONUS {num}:", f"BONUS{num}:", f"BONUS {num} -", f"BONUS{num} -"):
            if lu.startswith(pref):
                return num, l[len(pref):].strip(" :-")
        for pref in (f"BÔNUS {num}:", f"BÔNUS{num}:", f"BÔNUS {num} -"):
            if lu.startswith(pref.upper()):
                return num, l[len(pref):].strip(" :-")
    return None, None

def parsear_bonus(texto: str) -> list:
    linhas = texto.split("\\n")
    marcadores = []
    for idx, linha in enumerate(linhas):
        num, nome = _linha_e_marcador_bonus(linha)
        if num is not None: marcadores.append((idx, num, nome))
    if not marcadores: return [{"titulo": "🎁 Bônus", "descricao": "", "conteudo": texto.strip()}]
    bonus_list = []
    for i, (idx_ini, num, nome_bonus) in enumerate(marcadores):
        idx_fim = marcadores[i+1][0] if i+1 < len(marcadores) else len(linhas)
        bloco = linhas[idx_ini+1:idx_fim]
        descricao_partes, conteudo_partes, estado = [], [], "cabecalho"
        for linha in bloco:
            ls = linha.strip(); lu = ls.upper()
            if estado == "cabecalho" and not ls: continue
            if lu.startswith("DESCRI") and ":" in ls:
                estado = "descricao"
                parte = ls[ls.index(":")+1:].strip()
                if parte: descricao_partes.append(parte)
                continue
            if lu.startswith("CONTE") and ":" in ls:
                estado = "conteudo"
                parte = ls[ls.index(":")+1:].strip()
                if parte: conteudo_partes.append(parte)
                continue
            if estado == "descricao": descricao_partes.append(ls)
            elif estado == "conteudo": conteudo_partes.append(linha)
            else: conteudo_partes.append(linha)
        descricao = "\\n".join(descricao_partes).strip()
        conteudo = "\\n".join(conteudo_partes).strip()
        if not conteudo and not descricao: conteudo = "\\n".join(bloco).strip()
        bonus_list.append({"titulo": "🎁 BÔNUS " + num + (": " + nome_bonus if nome_bonus else ""), "descricao": descricao, "conteudo": conteudo})
    return bonus_list

def parsear_mensagens(texto: str) -> list:
    SECOES = ["DESCRICAO_GRUPO","BOAS_VINDAS","DIA_7","DIA_6","DIA_5","DIA_4","DIA_3","VESPERA","VENDA_MANHA","VENDA_NOITE"]
    LABELS = {
        "DESCRICAO_GRUPO": "📋 Descrição do grupo (bio)",
        "BOAS_VINDAS":  "💬 D-8 — Boas-vindas (mensagem automática)",
        "DIA_7":        "📅 D-9 — Abertura do programa",
        "DIA_6":        "🎯 D-10 — Enquete interativa",
        "DIA_5":        "🔥 D-11 — Dica prática",
        "DIA_4":        "📌 D-12 — Atividade interativa",
        "DIA_3":        "💡 D-13 — Conteúdo de valor / prova social",
        "VESPERA":      "⏳ D-14 — Véspera da venda",
        "VENDA_MANHA":  "🚀 Dia do lançamento — Manhã",
        "VENDA_NOITE":  "⏰ Dia do lançamento — Lembrete noturno (19h)",
    }
    linhas = texto.split('\\n')
    secoes, atual_label, atual_linhas = [], None, []
    for linha in linhas:
        ls = linha.strip(); lu = ls.upper()
        achou = False
        for chave in SECOES:
            if lu.startswith(chave + ":") or lu.startswith(chave.replace("_"," ") + ":"):
                if atual_label:
                    secoes.append({"label": LABELS.get(atual_label, atual_label), "chave": atual_label, "conteudo": '\\n'.join(atual_linhas).strip()})
                atual_label = chave
                resto = ls[ls.index(":")+1:].strip()
                atual_linhas = [resto] if resto else []
                achou = True
                break
        if not achou and atual_label:
            atual_linhas.append(linha)
    if atual_label:
        secoes.append({"label": LABELS.get(atual_label, atual_label), "chave": atual_label, "conteudo": '\\n'.join(atual_linhas).strip()})
    if not secoes:
        secoes = [{"label": "Mensagens", "chave": "RAW", "conteudo": texto.strip()}]
    return secoes

# --- BLOCO DE CONTEÚDO ---
def bloco_conteudo(chave: str, titulo: str, prompt_fn=None, system_fn=None):
    conteudo = st.session_state.dados.get(chave, '')
    if not conteudo:
        st.info(f"{titulo} ainda não foi gerado.")
        return

    if chave == 'bonus_cont':
        for b in parsear_bonus(conteudo):
            st.markdown(f"<div class='bonus-card-header'>{b['titulo']}</div>", unsafe_allow_html=True)
            if b['descricao']:
                st.markdown(f"<div class='bonus-descricao'><strong>Descrição:</strong><br>{b['descricao']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='bonus-conteudo'>{normalizar_markdown(b['conteudo'])}</div>", unsafe_allow_html=True)

    elif chave == 'msg_grupo':
        secoes = parsear_mensagens(conteudo)
        for i, s in enumerate(secoes):
            st.markdown(f"<div class='msg-dia-header'>{s['label']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='msg-conteudo'>{normalizar_markdown(s['conteudo'])}</div>", unsafe_allow_html=True)
            texto_limpo = limpar_html(s['conteudo'])
            st.download_button(
                label="📋 Copiar esta mensagem",
                data=texto_limpo,
                file_name=f"{s['chave'].lower()}.txt",
                mime="text/plain",
                key=f"copy_msg_{i}_{chave}",
                use_container_width=False,
            )

    else:
        st.markdown(f"<div class='caixa-texto'>{normalizar_markdown(conteudo)}</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.download_button(label="📋 Copiar como .txt", data=limpar_html(conteudo), file_name=f"{chave}.txt", mime="text/plain", key=f"copy_{chave}", use_container_width=True)
    with col2:
        if prompt_fn and system_fn:
            st.markdown('<div class="btn-secundario">', unsafe_allow_html=True)
            if st.button(f"🔄 Regenerar {titulo}", key=f"regen_{chave}", use_container_width=True):
                with st.spinner(f"Regenerando {titulo}..."):
                    st.session_state.dados[chave] = chamar_ia(prompt_fn(), system_fn())
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="btn-secundario">', unsafe_allow_html=True)
        if st.button(f"✍️ Corrigir gramática", key=f"gram_{chave}", use_container_width=True):
            with st.spinner("Revisando gramática e concordâncias..."):
                st.session_state.dados[chave] = corrigir_texto(limpar_html(conteudo))
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


# --- NAVEGAÇÃO ---
def mostrar_progresso():
    etapa_atual = st.session_state.etapa
    badges = ""
    for chave, label in ETAPAS_LABELS.items():
        cls = "ativo" if chave == etapa_atual else ""
        badges += f'<span class="step-badge {cls}">{label}</span>'
    st.markdown(f'<div class="step-indicator">{badges}</div>', unsafe_allow_html=True)

def barra_navegacao():
    mostrar_progresso()
    col1, col2, col3 = st.columns([2,2,2])
    with col1:
        if st.button("➕ INICIAR NOVO PROJETO", key="nx76"):
            st.session_state.dados = {}; st.session_state.chat_hist = []; st.session_state.etapa = "Formulario"; st.rerun()
    with col3:
        if st.session_state.dados and st.session_state.dados.get('nome_eb'):
            _nome_arq = st.session_state.dados.get('nome_eb','projeto').replace(' ','_').lower()
    with col2:
        with st.expander("📂 MEUS PROJETOS"):
            # ── PROJETOS SALVOS NA SESSÃO ─────────────────────
            if st.session_state.projetos:
                for nome in list(st.session_state.projetos.keys()):
                    c_abrir, c_deletar = st.columns([4,1])
                    if c_abrir.button(f"📄 {nome}", key=f"abrir_{nome}"):
                        st.session_state.dados = st.session_state.projetos[nome].copy()
                        st.session_state.etapa = "Visualizacao"; st.rerun()
                    st.markdown('<div class="btn-perigo">', unsafe_allow_html=True)
                    if c_deletar.button("🗑️", key=f"del_{nome}", help="Excluir projeto"):
                        deletar_projeto(nome); st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown(\"\"\"<div style="background:#FEF9C3;border:1px solid #FDE047;border-radius:8px;padding:10px 12px;font-size:0.82em;color:#713F12;margin-bottom:8px;">
                Nenhum projeto na memória.<br>Carregue seu arquivo .json abaixo.
                </div>\"\"\", unsafe_allow_html=True)

            # ── CARREGAR DO COMPUTADOR ────────────────────────
            st.divider()
            st.markdown("**📥 Carregar projeto do computador**")
            st.caption("Selecione o arquivo .json que você salvou antes.")
# =============================================================
# PROMPTS
# =============================================================

def prompt_ebook():
    d = st.session_state.dados
    return (f"Gere 60 cartões educativos numerados para o e-book '{d['nome_eb']}'. "
            f"Público-alvo: {d.get('publico', '')}. Dor principal: {d.get('dor', '')}. "
            f"Diferencial: {d.get('diferencial', '')}. Cada cartão deve ter título e conteúdo útil.")

def system_ebook():
    return "Você é um especialista em conteúdo digital educativo. Seja objetivo e prático."

def prompt_bonus():
    d = st.session_state.dados
    return (
        f"Crie 3 ebooks bônus complementares para quem comprou o ebook principal sobre {d.get('nicho')}. "
        f"Ebook principal: {d.get('nome_eb')}. Publico-alvo: {d.get('publico')}. "
        f"Dor principal: {d.get('dor')}. Promessa: {d.get('promessa')}. "
        f"Para cada ebook bonus, gere EXATAMENTE neste formato:\\n\\n"
        f"BONUS 1: [Nome]\\nDescricao: [2 linhas]\\nConteudo: [20 cartoes educativos numerados]\\n\\n"
        f"BONUS 2: [Nome]\\nDescricao: [2 linhas]\\nConteudo: [20 cartoes educativos numerados]\\n\\n"
        f"BONUS 3: [Nome]\\nDescricao: [2 linhas]\\nConteudo: [20 cartoes educativos numerados]"
    )

def system_bonus():
    return "Você é um especialista em conteúdo digital educativo. Crie ebooks bônus práticos que agreguem valor real ao produto principal."

def prompt_fb():
    d = st.session_state.dados
    return (
        f"Crie UM anúncio completo para Facebook Ads convidando pessoas para um grupo gratuito.\\n\\n"
        f"CONTEXTO:\\n"
        f"- Nicho: {d['nicho']}\\n- Público: {d.get('publico', '')}\\n- Dor principal: {d.get('dor', '')}\\n\\n"
        f"CONCEITO OBRIGATÓRIO: O anúncio convida para um PROGRAMA GRATUITO DE 15 DIAS sobre {d['nicho']}. "
        f"Use um nome atrativo para o programa baseado no tema — ex: 'Programa 15 Dias para [objetivo]'. "
        f"NUNCA mencione ebook, produto pago, lançamento, preço ou qualquer venda. "
        f"O grupo é gratuito, com dicas e atividades práticas durante 15 dias. Só isso.\\n\\n"
        f"ESTRUTURA OBRIGATÓRIA:\\n"
        f"1. Título chamativo em <strong>negrito HTML</strong> — centrado no programa gratuito\\n"
        f"2. Texto principal (máx 5 linhas) — foca na dor do público e no que vão receber grátis\\n"
        f"3. Lista rápida: ✅ Gratuito ✅ Grupo fechado ✅ Dicas diárias ✅ Vagas limitadas\\n"
        f"4. Sugestão de criativo visual (1 linha)\\n"
        f"5. CTA: ⬇️ Clique abaixo e garanta sua vaga\\n\\n"
        f"REGRAS: Deixe BEM EXPLÍCITO que o programa é 100% GRATUITO — use essa palavra em destaque. Sem exageros. Tom humano. Parece um convite, não um anúncio de produto.\\n"
        f"No CTA final, use: ⬇️ Clique no link abaixo e garanta sua vaga gratuitamente"
    )

def system_fb():
    return ("Você é um copywriter especialista em Facebook Ads. "
            "O anúncio deve convidar para um grupo gratuito — sem mencionar produto pago, ebook ou lançamento. "
            "A oferta é o programa gratuito em si. Use tags HTML <strong> para negrito, nunca asteriscos.")

def prompt_lp():
    d = st.session_state.dados
    secao_autor = ''
    if d.get('autor_nome') or d.get('autor_experiencia'):
        secao_autor = (f"Autor: {d.get('autor_nome','')}, Experiência: {d.get('autor_experiencia','')}, "
                       f"Credenciais: {d.get('autor_credenciais','')}.  ")
    return (
        f"Crie UMA landing page com abordagem de DIAGNÓSTICO para capturar leads.\\n\\n"
        f"CONTEXTO:\\n"
        f"- Nicho: {d.get('nicho')}\\n- Público: {d.get('publico')}\\n"
        f"- Dor principal: {d.get('dor', '')}\\n- Situação atual: {d['atual']}\\n"
        f"- Objetivo: {d['desejada']}\\n"
        f"- {secao_autor}\\n\\n"
        f"CONCEITO CENTRAL — DIAGNÓSTICO:\\n"
        f"A LP não vende nada. Ela convida para um programa gratuito que vai DIAGNOSTICAR o problema real "
        f"da pessoa em {d.get('nicho')} e mostrar o que está travando o resultado dela.\\n"
        f"Tom: 'Você sabe que algo está errado, mas não sabe exatamente o quê. "
        f"Nesses 15 dias vamos descobrir juntos — e eu vou te mostrar o caminho.'\\n"
        f"NUNCA mencione ebook, produto pago, lançamento ou preço.\\n\\n"
        f"ESTRUTURA OBRIGATÓRIA:\\n"
        f"1. Headline: promessa de diagnóstico — ex: 'Descubra o que está travando seu resultado em {d.get('nicho')}' \\n"
        f"2. Subtítulo: 'Em 15 dias gratuitos, você vai entender exatamente o que está errado — e o que fazer'\\n"
        f"3. Seção de dor — 3 bullets: situações que a pessoa vive e não entende por quê\\n"
        f"4. O que o programa faz: diagnostica, identifica os erros, mostra o caminho — tudo grátis\\n"
        f"5. Quem sou eu (autor, 2-3 linhas de credibilidade)\\n"
        f"6. 4 benefícios com ✔ — focados em clareza, diagnóstico e direção\\n"
        f"7. Sugestão de elemento visual\\n"
        f"8. CTA: [ QUERO DESCOBRIR O QUE ESTÁ ERRADO ]\\n\\n"
        f"REGRAS: Tom de quem vai ajudar a pessoa a entender, não de quem vai vender. "
        f"A solução (ebook) aparece só depois, na venda. Aqui só existe o diagnóstico."
    )

def system_lp():
    return ("Você é um especialista em Landing Pages de diagnóstico. "
            "Gere o TEXTO da landing page — não gere código HTML. "
            "Use formatação simples em markdown: **negrito**, títulos com ##, bullets com -. "
            "A LP cria curiosidade sobre o problema real da pessoa e posiciona o grupo gratuito "
            "como o lugar onde ela vai descobrir o que está travando seus resultados. "
            "Tom humano e direto. Não mencione código, HTML ou programação.")

def prompt_msg():
    d = st.session_state.dados
    data_lancto = d.get('data_lancto')
    data_fmt = data_lancto.strftime('%d/%m/%Y') if data_lancto else 'em breve'
    preco = d.get('preco', 47)
    nome_eb = d.get('nome_eb', '')
    nicho = d.get('nicho', '')
    dor = d.get('dor', '')
    publico = d.get('publico', '')
    whatsapp_num = d.get('whatsapp_contato', 'SEU NÚMERO AQUI')
    link_venda = d.get('link_monetizze', '').strip() or '[LINK MONETIZZE]'

    # ── MODIFICAÇÃO: pede revisão dos nomes dos bônus ──────────
    bonus_resumo = d.get('bonus_resumo', '')
    if bonus_resumo:
        nomes_bonus = [b.strip() for b in bonus_resumo.split(',') if b.strip()]
        bonus_lista = '\\n'.join([f'🎁 Bônus {i+1} – {nome}' for i, nome in enumerate(nomes_bonus)])
    else:
        bonus_lista = '🎁 Bônus 1\\n🎁 Bônus 2\\n🎁 Bônus 3'

    return (
        f"Gere as mensagens do funil de WhatsApp para o lançamento sobre {nicho}.\\n"
        f"Ebook: {nome_eb}. Preço: R${preco}. WhatsApp: {whatsapp_num}. Dor: {dor}.\\n\\n"
        f"REGRA DE OURO — TOM DE WHATSAPP REAL:\\n"
        f"- Escreva como uma pessoa real escreveria pra um grupo de amigos\\n"
        f"- Saudações vivas e naturais: Bom dia, grupo! Como vocês estão? / Boa tarde, pessoal! / E aí, tudo bem?\\n"
        f"- Frases curtas, uma por linha, sem parágrafos longos\\n"
        f"- Reticências naturais... pausas... como na fala\\n"
        f"- Emojis onde cabem de forma natural, sem exagero\\n"
        f"- ZERO texto corporativo, ZERO linguagem de robô, ZERO formalidade\\n"
        f"- Parece que foi digitado agora, não copiado de um template\\n\\n"
        f"Textos entre === FIXO === e === FIM === copie PALAVRA POR PALAVRA.\\n"
        f"Blocos [IA] devem ser criados com o mesmo tom humano de WhatsApp.\\n\\n"

        f"DESCRICAO_GRUPO:\\n"
        f"=== FIXO ===\\n"
        f"Seja muito bem-vindo ao nosso grupo de [adapte: nome do programa sobre {nicho}]!\\n"
        f"Esse não é apenas um grupo com conteúdos soltos.\\n"
        f"Nos próximos dias, você vai passar por um processo simples, mas muito poderoso:\\n"
        f"Primeiro, eu vou entender você.\\n"
        f"Depois, vou te mostrar pequenos ajustes que já podem fazer diferença no seu dia a dia.\\n"
        f"E no momento certo… eu vou te apresentar algo mais completo.\\n"
        f"Tudo isso de forma leve, prática e aplicável.\\n"
        f"Nosso objetivo aqui é um só: te ajudar a sair do mesmo lugar.\\n"
        f"⚠️ Para manter a melhor experiência, o grupo permanecerá silencioso.\\n"
        f"Assim, você recebe apenas o que realmente importa.\\n"
        f"Fica atento…\\n"
        f"Porque, se você acompanhar até o final, pode enxergar {nicho} de uma forma completamente diferente.\\n"
        f"=== FIM ===\\n\\n"

        f"BOAS_VINDAS:\\n"
        f"=== FIXO ===\\n"
        f"Seja muito bem-vindo ao nosso grupo de [adapte: nome do programa sobre {nicho}]!\\n"
        f"Se você está aqui… provavelmente já tentou melhorar em {nicho} — e não conseguiu manter.\\n"
        f"E não é por falta de esforço.\\n"
        f"Nos próximos dias, você vai entender exatamente o porquê.\\n"
        f"Aqui, você não vai receber conteúdo aleatório.\\n"
        f"Você vai receber algo simples… mas que pode destravar algo que você vem tentando há muito tempo.\\n"
        f"⚠️ O grupo permanecerá silencioso\\n"
        f"Pra você receber só o que realmente importa.\\n"
        f"Fica atento… porque o que vem pode te surpreender.\\n"
        f"=== FIM ===\\n\\n"

        # ── MODIFICAÇÃO D-9: "amanhã" em vez de "nas próximas horas" ──
        f"DIA_7:\\n"
        f"=== FIXO ===\\n"
        f"Bom dia, grupo! ☀️\\n"
        f"Como vocês estão?\\n"
        f"Espero que bem!\\n\\n"
        f"Antes de começarmos os conteúdos sobre {nicho}...\\n"
        f"Eu quero fazer algo diferente.\\n\\n"
        f"Quero te entender de verdade.\\n\\n"
        f"A maioria dos conteúdos por aí são genéricos demais.\\n"
        f"E eu não quero fazer isso com vocês.\\n\\n"
        f"Então amanhã vou mandar um diagnóstico aqui no grupo.\\n"
        f"Ele vai me ajudar a entender exatamente onde você tá travado em {nicho}.\\n\\n"
        f"Fica de olho amanhã 👇\\n"
        f"=== FIM ===\\n\\n"

        f"DIA_6:\\n"
        f"[IA] Saudação viva e natural de grupo de WhatsApp (ex: Bom dia, pessoal! Tudo bem por aí? 🌿)\\n"
        f"Segunda linha em branco.\\n"
        f"Próxima linha: Preciso muito da ajuda de vocês aqui...\\n"
        f"Próxima: Quero entender melhor a situação de cada um pra poder ajudar de verdade.\\n"
        f"Linha em branco.\\n"
        f"Uma pergunta central de diagnóstico sobre a dor {dor} no nicho {nicho}.\\n"
        f"Linha em branco.\\n"
        f"4 opções A) B) C) D) — cada uma em sua própria linha, curtas e diretas.\\n"
        f"Linha em branco.\\n"
        f"Me manda sua resposta no WhatsApp: {whatsapp_num} 📲\\n"
        f"Vou ler todas... prometo!\\n"
        f"Linha em branco.\\n"
        f"E em {data_fmt} eu entrego a solução detalhada, passo a passo, pra cada perfil.\\n\\n"

        f"DIA_5:\\n"
        f"[IA] Saudação animada e diferente das anteriores (ex: Boa tarde, galera! 👋 / E aí, pessoal, tudo certo?)\\n"
        f"Linha em branco.\\n"
        f"Próxima linha: Deixa eu compartilhar algo que pouca gente fala sobre {nicho}...\\n"
        f"Linha em branco.\\n"
        f"Crie 3 dicas surpreendentes e contra-intuitivas sobre {nicho}.\\n"
        f"Cada dica: *Dica X: [título impactante]* (negrito estilo WhatsApp) + 2 linhas explicando.\\n"
        f"Tom: Que massa, nunca pensei nisso antes!\\n"
        f"Linha em branco entre cada dica.\\n"
        f"Finalize com: Aplica uma dessas e me conta o que achou 😊\\n\\n"

        f"DIA_4:\\n"
        f"[IA] Saudação descontraída (ex: Bom dia! Acordei pensando em vocês 😄 / Boa tarde, grupo!)\\n"
        f"Linha em branco.\\n"
        f"Proponha uma atividade de OBSERVAÇÃO simples sobre {nicho} ligada à dor {dor}.\\n"
        f"NÃO explique o motivo — mantenha o mistério.\\n"
        f"Linha em branco.\\n"
        f"Peça pra responder no WhatsApp {whatsapp_num} o que observaram.\\n"
        f"Tom curioso e leve. Máximo 8 linhas no total.\\n\\n"

        f"DIA_3:\\n"
        f"[IA] Saudação direta (ex: Bom dia! 👊 / Boa tarde, pessoal!)\\n"
        f"Linha em branco.\\n"
        f"Escreva naturalmente assim:\\n"
        f"Existe um erro simples que pode estar travando o resultado em {nicho}...\\n"
        f"Linha em branco.\\n"
        f"Mas o problema é:\\n"
        f"👉 ele não é óbvio\\n"
        f"👉 e quase ninguém percebe\\n"
        f"Linha em branco.\\n"
        f"Por isso muita gente continua tentando... ajustando... mas sem sair do lugar.\\n"
        f"Linha em branco.\\n"
        f"Hoje, só faz isso:\\n"
        f"[crie 1 ação de observação simples sobre {nicho} — SEM revelar a causa]\\n"
        f"Linha em branco.\\n"
        f"Sem mudar nada ainda.\\n"
        f"Depois me conta como foi 📲\\n\\n"

        f"VESPERA:\\n"
        f"=== FIXO ===\\n"
        f"Eu preciso ser sincero com você.\\n"
        f"Depois de tudo que vocês me enviaram no meu WhatsApp…\\n"
        f"Eu percebi algo que eu não esperava.\\n\\n"
        f"Existe um padrão.\\n"
        f"E não é pequeno.\\n\\n"
        f"Mais de 80% das pessoas aqui estão presas exatamente nos mesmos pontos…\\n"
        f"Mesmo tentando caminhos diferentes.\\n\\n"
        f"E isso me fez chegar a uma conclusão:\\n"
        f"O problema não está no esforço.\\n"
        f"Está no caminho que foi mostrado até hoje.\\n\\n"
        f"Foi por isso que eu decidi fazer algo diferente.\\n"
        f"Algo único… pensado pra resolver isso de forma direta.\\n\\n"
        f"Mas não é só sobre entender.\\n"
        f"É sobre saber exatamente o que fazer — sem dúvidas, sem excesso, sem confusão.\\n\\n"
        f"Eu organizei tudo de um jeito que praticamente qualquer pessoa aqui consiga aplicar.\\n\\n"
        f"Amanhã, eu vou te mostrar.\\n\\n"
        f"Mas já te adianto:\\n"
        f"Se você ignorar… provavelmente vai continuar no mesmo lugar.\\n\\n"
        f"Fica atento.\\n"
        f"=== FIM ===\\n\\n"

        # ── MODIFICAÇÃO: pede revisão dos nomes dos bônus na venda ──
        f"VENDA_MANHA:\\n"
        f"=== FIXO ===\\n"
        f"Hoje é o dia. 🚀\\n\\n"
        f"Durante esses dias, eu analisei tudo que vocês me enviaram…\\n"
        f"e encontrei padrões que explicam exatamente por que a maioria não consegue evoluir em {nicho}.\\n\\n"
        f"E como eu te disse ontem:\\n"
        f"👉 isso não é óbvio\\n"
        f"👉 e quase ninguém percebe sozinho\\n\\n"
        f"Foi por isso que eu organizei tudo em um método simples:\\n\\n"
        f"📘 *{nome_eb}*\\n\\n"
        f"Esse material é a continuação direta do que você começou aqui.\\n"
        f"Aqui dentro, você vai entender:\\n"
        f"👉 o que realmente está travando seu resultado\\n"
        f"👉 e exatamente o que fazer pra corrigir\\n\\n"
        f"Sem tentativa e erro. Sem perder tempo.\\n\\n"
        f"E vem com 3 bônus exclusivos:\\n"
        f"{bonus_lista}\\n\\n"
        f"⚠️ ATENÇÃO: Antes de enviar, revise se os nomes dos bônus acima estão corretos — confira com os ebooks que você criou!\\n\\n"
        f"Tudo isso por apenas *R$ {preco}.*\\n\\n"
        f"👉 {link_venda}\\n\\n"
        f"⏰ Só hoje até 23:59\\n"
        f"✅ Garantia de 7 dias\\n\\n"
        f"Você pode continuar tentando ajustar sozinho…\\n"
        f"ou seguir um caminho que já está organizado.\\n\\n"
        f"A decisão é sua.\\n"
        f"=== FIM ===\\n\\n"

        f"VENDA_NOITE:\\n"
        f"=== FIXO ===\\n"
        f"Boa noite, pessoal! 👋\\n\\n"
        f"Passando aqui rapidinho pra não deixar vocês esquecerem...\\n\\n"
        f"Hoje de manhã eu compartilhei aqui algo que preparei com muito carinho pra vocês.\\n\\n"
        f"📘 Conteúdo direto, sem enrolação\\n"
        f"🎁 Com 3 bônus práticos\\n\\n"
        f"Se você viu e ficou na dúvida, tudo bem.\\n"
        f"Mas a verdade é:\\n"
        f"Quem aplica o método certo, evolui muito mais rápido.\\n\\n"
        f"Ainda dá tempo hoje:\\n\\n"
        f"👉 {link_venda}\\n\\n"
        f"⏰ Só até 23:59\\n"
        f"✅ Garantia de 7 dias\\n\\n"
        f"Dá uma olhada com calma… e decide com consciência. 🙏\\n"
        f"=== FIM ===\\n"
    )

def system_msg():
    return (
        "Você é um especialista em copywriting para lançamentos no WhatsApp e Telegram. "
        "Os textos fixos devem ser reproduzidos EXATAMENTE como fornecidos — sem alterar uma vírgula. "
        "Apenas os blocos com instruções entre colchetes devem ser gerados pela IA. "
        "Respeite o formato com os rótulos exatos. Tom humano e direto em tudo que gerar."
    )

# =============================================================
# TELAS
# =============================================================

# ── LOGIN ─────────────────────────────────────────────────────
if st.session_state.etapa == "Login":
    st.info("💻 **Dica:** Pela complexidade dos agentes, no computador a experiência é mais agradável.")
    st.title("NEXUS LAUNCHER")
    st.subheader("ACESSO RESTRITO A ASSOCIADOS DO MEUSAGENTESIA.COM.BR")
    st.markdown('<p style="margin-top:-8px;margin-bottom:20px;font-size:0.95em;">🔗 <a href="https://meusagentesia.com.br" target="_blank" style="color:#0369A1;text-decoration:none;font-weight:600;">meusagentesia.com.br</a></p>', unsafe_allow_html=True)
    st.session_state.usuario = st.text_input("Nome", key="nx75")
    st.session_state.api_key = st.text_input("Chave Groq", type="password", key="nx74")
    with st.expander("🚀 Primeira vez aqui? Veja como funciona em 3 passos"):
        st.markdown(\"\"\"
<div style="display:flex;gap:16px;flex-wrap:wrap;">
<div style="flex:1;min-width:180px;background:#EFF6FF;border-radius:10px;padding:16px;text-align:center;">
<div style="font-size:2em;">1️⃣</div>
<div style="font-weight:700;margin:8px 0 4px;font-family:Rajdhani,sans-serif;">Preencha o formulário</div>
<div style="font-size:0.82em;color:#64748B;">Nicho, público, dor, promessa. A IA preenche automaticamente se quiser.</div>
</div>
<div style="flex:1;min-width:180px;background:#F0FDF4;border-radius:10px;padding:16px;text-align:center;">
<div style="font-size:2em;">2️⃣</div>
<div style="font-weight:700;margin:8px 0 4px;font-family:Rajdhani,sans-serif;">Gere tudo com 1 clique</div>
<div style="font-size:0.82em;color:#64748B;">E-book, bônus, anúncio, landing page e funil completo de mensagens.</div>
</div>
<div style="flex:1;min-width:180px;background:#FDF4FF;border-radius:10px;padding:16px;text-align:center;">
<div style="font-size:2em;">3️⃣</div>
<div style="font-weight:700;margin:8px 0 4px;font-family:Rajdhani,sans-serif;">Salve e lance</div>
<div style="font-size:0.82em;color:#64748B;">Projetos salvos ficam disponíveis sempre. Exporte o calendário de envios.</div>
</div>
</div>
<div style="margin-top:14px;background:#FEF9C3;border-radius:8px;padding:10px 14px;font-size:0.82em;color:#713F12;">
💡 <strong>Você precisará de uma chave Groq gratuita</strong> em <a href="https://console.groq.com/keys" target="_blank">console.groq.com/keys</a> — cria conta, gera a chave e cola aqui.
</div>
        \"\"\", unsafe_allow_html=True)

    st.markdown("#### Status da API")
    col_groq, _ = st.columns(2)
    with col_groq:
        if st.session_state.api_key.strip():
            try:
                _gc = Groq(api_key=st.session_state.api_key)
                _gc.chat.completions.create(
                    messages=[{"role":"user","content":"ok"}],
                    model="openai/gpt-oss-120b", max_tokens=1
                )
                st.markdown(\"\"\"<div style="background:#ECFDF5;border:1px solid #6EE7B7;border-radius:8px;
                padding:10px 14px;font-size:0.82em;color:#064E3B;">
                🟢 <strong>Groq API:</strong> conectada<br>
                <span style="font-size:0.9em;">Chave válida. Geração de conteúdo ativa.</span>
                </div>\"\"\", unsafe_allow_html=True)
            except Exception as _e:
                err_msg = str(_e)
                if "401" in err_msg or "invalid" in err_msg.lower():
                    msg = "Chave inválida ou expirada."
                elif "rate" in err_msg.lower():
                    msg = "Limite de requisições atingido."
                else:
                    msg = err_msg[:80]
                st.markdown(f\"\"\"<div style="background:#FEF2F2;border:1px solid #FECACA;border-radius:8px;
                padding:10px 14px;font-size:0.82em;color:#7F1D1D;">
                🔴 <strong>Groq API:</strong> erro<br>
                <span style="font-size:0.9em;">{msg}</span>
                </div>\"\"\", unsafe_allow_html=True)
        else:
            st.markdown(\"\"\"<div style="background:#F1F5F9;border:1px solid #CBD5E1;border-radius:8px;
            padding:10px 14px;font-size:0.82em;color:#64748B;">
            ⚪ <strong>Groq API:</strong> aguardando chave
            </div>\"\"\", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**📂 Já tem um projeto salvo?** Carregue o arquivo .json para continuar de onde parou:")
    st.markdown("")

    if st.button("ENTRAR", key="nx73"):
        if not st.session_state.usuario.strip(): st.error("Informe seu nome.")
        elif not st.session_state.api_key.strip(): st.error("Informe sua chave de API.")
        else: st.session_state.etapa = "Escolha_Tipo"; st.rerun()

# ── ESCOLHA DO TIPO DE LANÇAMENTO ─────────────────────────────
elif st.session_state.etapa == "Escolha_Tipo":
    st.title("NEXUS LAUNCHER")
    st.markdown(f"### Olá, {st.session_state.usuario}! O que você vai lançar?")

    st.markdown("### 🗺️ Como funciona o Nexus Launcher")
    guia_nx = {
        "📚 Lançamento de E-book":    "Programa gratuito 15 dias → aquecimento no grupo → venda do e-book com funil completo de mensagens",
        "🎬 Lançamento de Videoaulas":"Método CPL: 3 vídeos estratégicos de pré-lançamento → abertura de carrinho → fechamento com urgência",
    }
    for etapa, desc in guia_nx.items():
        st.markdown(f"**{etapa}** — {desc}")
    st.markdown("**O que é gerado automaticamente:**")
    st.markdown("📚 E-book com 60 cartões · 🎁 3 Bônus · 📣 Anúncio · 🌐 Landing Page · 💬 Funil de Mensagens completo")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(\"\"\"<div style="background:#EFF6FF;border:2px solid #3B82F6;border-radius:16px;padding:30px;text-align:center;min-height:220px;">
        <div style="font-size:3em;">📚</div>
        <div style="font-family:Rajdhani,sans-serif;font-size:1.4em;font-weight:700;color:#1E3A5F;margin:10px 0 8px;">Lançamento de E-book</div>
        <div style="font-size:0.88em;color:#64748B;line-height:1.5;">Programa gratuito de 15 dias → aquecimento → venda do e-book no grupo do WhatsApp</div>
        </div>\"\"\", unsafe_allow_html=True)
        if st.button("📚 LANÇAR E-BOOK", use_container_width=True, key="nx72"):
            st.session_state.dados['tipo_lancamento'] = 'ebook'
            st.session_state.etapa = "Formulario"; st.rerun()
    with col2:
        st.markdown(\"\"\"<div style="background:#FDF4FF;border:2px solid #A855F7;border-radius:16px;padding:30px;text-align:center;min-height:220px;">
        <div style="font-size:3em;">🎬</div>
        <div style="font-family:Rajdhani,sans-serif;font-size:1.4em;font-weight:700;color:#4A1D7A;margin:10px 0 8px;">Lançamento de Videoaulas</div>
        <div style="font-size:0.88em;color:#64748B;line-height:1.5;">Método CPL: pré-lançamento com 3 vídeos estratégicos → abertura de carrinho → fechamento com urgência</div>
        </div>\"\"\", unsafe_allow_html=True)
        if st.button("🎬 LANÇAR VIDEOAULAS", use_container_width=True, key="nx71"):
            st.session_state.dados['tipo_lancamento'] = 'video'
            st.session_state.etapa = "Video_Formulario"; st.rerun()

# ── FORMULÁRIO ───────────────────────────────────────────────
elif st.session_state.etapa == "Formulario":
    barra_navegacao()
    st.title("PREENCHA O FORMULÁRIO")
    d = st.session_state.dados

    st.markdown("#### Começar com um exemplo pronto")
    st.caption("Escolha um nicho de exemplo e preencha tudo automaticamente.")
    cols = st.columns(len(EXEMPLOS))
    for i, (nome_ex, vals) in enumerate(EXEMPLOS.items()):
        with cols[i]:
            st.markdown('<div class="exemplo-btn">', unsafe_allow_html=True)
            if st.button(f"📋 {nome_ex}", key=f"ex_{nome_ex}", use_container_width=True):
                for k, v in vals.items(): st.session_state.dados[k] = v
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    st.divider()
    st.markdown("#### Preencha os dados do seu lançamento")
    d['nicho']       = st.text_input("Nicho:", value=d.get('nicho',''), help="ex: emagrecimento, renda extra", key="nx68")
    d['publico']     = st.text_input("Público-alvo:", value=d.get('publico',''), key="nx67")
    d['nome_eb']     = st.text_input("Nome do e-book:", value=d.get('nome_eb',''), key="nx66")
    d['dor']         = st.text_input("Principal dor que resolve:", value=d.get('dor',''), key="nx65")
    d['atual']       = st.text_area("Situação atual da pessoa:", value=d.get('atual',''), key="nx64")
    d['desejada']    = st.text_area("Situação desejada:", value=d.get('desejada',''), key="nx63")
    d['promessa']    = st.text_input("Transformação do programa:", value=d.get('promessa',''), key="nx62")
    d['diferencial'] = st.text_input("Diferencial:", value=d.get('diferencial',''), key="nx61")
    d['preco']       = st.number_input("Preço do e-book (R$):", min_value=9, max_value=997, value=int(d.get('preco',47)), step=1, key="nx60")

    st.divider()
    st.markdown("#### Suas credenciais como autor")
    d['autor_nome']        = st.text_input("Seu nome:", value=d.get('autor_nome',''), key="nx59")
    d['autor_experiencia'] = st.text_area("Sua experiência com o tema:", value=d.get('autor_experiencia',''), key="nx58")
    d['autor_credenciais'] = st.text_area("Resultados ou conquistas:", value=d.get('autor_credenciais',''), key="nx57")

    st.divider()
    st.markdown("#### WhatsApp para receber respostas da enquete")
    st.markdown(\"\"\"<div style="background:#FEF9C3;border:1px solid #FDE047;border-radius:8px;padding:12px 16px;margin-bottom:12px;color:#713F12;font-size:0.88em;line-height:1.6;">
    ⚠️ <strong>ATENÇÃO: use um número DIFERENTE do grupo.</strong><br>
    O grupo ficará fechado para mensagens — os membros não conseguem responder lá dentro.<br>
    Por isso, as respostas da enquete e dúvidas devem ir para um número pessoal ou comercial separado.
    </div>\"\"\", unsafe_allow_html=True)
    d['whatsapp_contato'] = st.text_input("Número para receber respostas:", value=d.get('whatsapp_contato',''), placeholder="ex: (11) 99999-9999", key="nx56")

    data_sugerida = d.get('data_lancto', date.today() + timedelta(days=15))
    d['data_lancto'] = st.date_input("Data de lançamento", value=data_sugerida, min_value=date.today(), key="nx55")
    st.caption("💡 Dica: Use os primeiros 7 dias para encher o grupo e os próximos 7 para aquecer. Lance no 15º dia.")

    st.divider()
    st.markdown("#### Calculadora de faturamento")
    col_a, col_b, col_c = st.columns(3)
    with col_a: leads = st.number_input("Pessoas no grupo:", min_value=100, max_value=100000, value=1000, step=100, key="nx54")
    with col_b: conversao = st.slider("Taxa de conversão (%):", min_value=1, max_value=30, value=10, key="nx53")
    with col_c: st.metric("Preço definido", f"R${d.get('preco',47)}")
    vendas = int(leads * conversao / 100)
    faturamento = vendas * d.get('preco', 47)
    lucro = faturamento - int(leads * 1.5)
    col1, col2, col3 = st.columns(3)
    col1.metric("Vendas estimadas", f"{vendas}")
    col2.metric("Faturamento bruto", f"R${faturamento:,.0f}".replace(',','.'))
    col3.metric("Lucro estimado", f"R${lucro:,.0f}".replace(',','.'), delta="após tráfego ~R$1,50/lead")

    campos_obrigatorios = ['nicho','publico','nome_eb','dor','atual','desejada','promessa','diferencial']
    tudo_preenchido = all(d.get(c,'').strip() for c in campos_obrigatorios)

    if tudo_preenchido:
        st.divider()
        st.markdown("#### Resumo do que será gerado")
        st.markdown(f\"\"\"<div class="preview-box">
        📚 <strong>E-book:</strong> {d.get('nome_eb')} — 60 cartões educativos<br>
        🎁 <strong>3 E-books Bônus</strong> complementares<br>
        📣 <strong>1 Anúncio</strong> alinhado com a landing page<br>
        🌐 <strong>1 Landing Page</strong> alinhada com o anúncio<br>
        💬 <strong>Funil completo de Mensagens</strong> — boas-vindas + aquecimento + véspera + venda<br>
        🚀 <strong>Lançamento:</strong> {d['data_lancto'].strftime('%d/%m/%Y') if hasattr(d.get('data_lancto'), 'strftime') else str(d.get('data_lancto', 'a definir'))}
        </div>\"\"\", unsafe_allow_html=True)

    if st.button("AVANÇAR →", key="nx52"):
        faltando = [c for c in campos_obrigatorios if not d.get(c,'').strip()]
        if faltando: st.warning("Preencha todos os campos antes de avançar.")
        else: st.session_state.etapa = "Potencial_Nicho"; st.rerun()

# ── POTENCIAL DO NICHO ───────────────────────────────────────
elif st.session_state.etapa == "Potencial_Nicho":
    barra_navegacao()
    st.title("📊 POTENCIAL DO NICHO")
    d = st.session_state.dados

    if st.button("🔍 ANALISAR POTENCIAL DO NICHO", key="nx51"):
        with st.spinner("Analisando potencial de mercado..."):
            prompt_pot = (
                f"Analise o potencial de mercado para lançamento digital no nicho: {d.get('nicho')}.\\n"
                f"Público-alvo: {d.get('publico')}.\\n"
                f"Dor principal: {d.get('dor')}.\\n\\n"
                f"Responda EXATAMENTE neste formato:\\n\\n"
                f"NIVEL_DEMANDA: [Alta / Média / Baixa] — justifique em 1 frase\\n\\n"
                f"NIVEL_CONCORRENCIA: [Alta / Média / Baixa] — justifique em 1 frase\\n\\n"
                f"TICKET_IDEAL: [faixa de preço recomendada para ebook nesse nicho] — justifique\\n\\n"
                f"PUBLICO_ESTIMADO: [estimativa do tamanho do público online no Brasil]\\n\\n"
                f"PONTOS_FORTES: [3 vantagens desse nicho para lançamento digital]\\n\\n"
                f"PONTOS_ATENCAO: [3 riscos ou desafios desse nicho]\\n\\n"
                f"ANGULOS_VIRAIS: [3 ângulos de comunicação que tendem a performar bem nesse nicho]\\n\\n"
                f"VEREDICTO: [Avaliação geral em 2-3 frases — vale lançar? Por quê?]\\n\\n"
                f"NOTA_GERAL: [nota de 1 a 10 para o potencial desse nicho]"
            )
            system_pot = "Você é um analista de marketing digital especialista em lançamentos no Brasil. Seja direto, realista e baseado em dados de mercado."
            st.session_state.dados['potencial_nicho'] = chamar_ia(prompt_pot, system_pot)

    if st.session_state.dados.get('potencial_nicho'):
        raw = st.session_state.dados['potencial_nicho']
        import re as _re
        def pegar(chave, texto):
            pat = rf"{chave}:\\s*(.+?)(?=\\n[A-Z_]{{3,}}:|$)"
            m = _re.search(pat, texto, _re.DOTALL)
            return m.group(1).strip() if m else ""

        nivel_dem  = pegar("NIVEL_DEMANDA", raw)
        nivel_con  = pegar("NIVEL_CONCORRENCIA", raw)
        ticket     = pegar("TICKET_IDEAL", raw)
        pub_est    = pegar("PUBLICO_ESTIMADO", raw)
        fortes     = pegar("PONTOS_FORTES", raw)
        atencao    = pegar("PONTOS_ATENCAO", raw)
        virais     = pegar("ANGULOS_VIRAIS", raw)
        veredicto  = pegar("VEREDICTO", raw)
        nota_raw   = pegar("NOTA_GERAL", raw)
        try:
            nota = float(_re.search(r"\\d+[.,]?\\d*", nota_raw).group().replace(",","."))
        except:
            nota = 0

        cor_nota = "#22C55E" if nota >= 7 else "#B45309" if nota >= 5 else "#B91C1C"
        st.markdown(
            f"<div style='display:flex;align-items:center;gap:20px;background:#F8FAFC;"
            f"border:2px solid {cor_nota};border-radius:12px;padding:18px 24px;margin-bottom:20px;'>"
            f"<div style='font-size:3em;font-weight:900;color:{cor_nota};font-family:Rajdhani,sans-serif;'>{nota:.0f}<span style='font-size:0.4em;color:#475569;'>/10</span></div>"
            f"<div><div style='font-size:1.1em;font-weight:700;color:#1E293B;'>Potencial geral do nicho</div>"
            f"<div style='font-size:0.88em;color:#64748B;margin-top:4px;'>{veredicto}</div></div>"
            f"</div>", unsafe_allow_html=True
        )

        def nivel_badge(txt):
            txt = txt.split("—")[0].strip().split()[0].strip()
            cor = {"Alta":"#22C55E","Média":"#B45309","Baixa":"#B91C1C"}.get(txt, "#475569")
            return f"<span style='background:{cor};color:white;padding:2px 10px;border-radius:999px;font-size:0.8em;font-weight:700;'>{txt}</span>"

        c1, c2, c3 = st.columns(3)
        c1.markdown(f"**Demanda**<br>{nivel_badge(nivel_dem)}", unsafe_allow_html=True)
        c2.markdown(f"**Concorrência**<br>{nivel_badge(nivel_con)}", unsafe_allow_html=True)
        c3.markdown(f"**Ticket ideal**<br><span style='font-size:0.9em;color:#1E293B;'>{ticket.split('—')[0].strip()[:40]}</span>", unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("**✅ Pontos fortes**")
            for linha in fortes.split("\\n"):
                if linha.strip(): st.markdown(f"- {linha.strip().lstrip('123.-)')}")
            st.markdown("**🎯 Ângulos virais**")
            for linha in virais.split("\\n"):
                if linha.strip(): st.markdown(f"- {linha.strip().lstrip('123.-)')}")
        with col_b:
            st.markdown("**⚠️ Pontos de atenção**")
            for linha in atencao.split("\\n"):
                if linha.strip(): st.markdown(f"- {linha.strip().lstrip('123.-)')}")
            st.markdown(f"**👥 Público estimado:** {pub_est}")

        st.divider()
        if st.button("AVANÇAR → GERAR E-BOOK", key="nx50"): st.session_state.etapa = "Gerar_Ebook"; st.rerun()

# ── E-BOOK ───────────────────────────────────────────────────
elif st.session_state.etapa == "Gerar_Ebook":
    barra_navegacao()
    st.title("📚 GERAR E-BOOK PROFISSIONAL")
    if st.button("GERAR E-BOOK – 60 CARTÕES", key="nx49"):
        with st.spinner("Gerando e-book com IA..."):
            st.session_state.dados['ebook_cont'] = chamar_ia(prompt_ebook(), system_ebook())
    if 'ebook_cont' in st.session_state.dados:
        bloco_conteudo('ebook_cont', 'E-book', prompt_ebook, system_ebook)
        if st.button("AVANÇAR →", key="nx48"): st.session_state.etapa = "Gerar_Bonus"; st.rerun()

# ── BÔNUS ────────────────────────────────────────────────────
elif st.session_state.etapa == "Gerar_Bonus":
    barra_navegacao()
    st.title("🎁 GERAR 3 E-BOOKS BÔNUS")
    st.caption("Os bônus serão complementares ao ebook principal e incluídos automaticamente na Mensagem de Lançamento.")
    if st.button("GERAR 3 EBOOKS BÔNUS", key="nx47"):
        with st.spinner("Gerando ebooks bônus com IA..."):
            st.session_state.dados['bonus_cont'] = chamar_ia(prompt_bonus(), system_bonus())
            nomes = []
            for linha in st.session_state.dados['bonus_cont'].split('\\n'):
                num, nome_b = _linha_e_marcador_bonus(linha)
                if num is not None and nome_b: nomes.append(nome_b)
            if nomes: st.session_state.dados['bonus_resumo'] = ', '.join(nomes)
            st.rerun()
    if 'bonus_cont' in st.session_state.dados:
        bloco_conteudo('bonus_cont', 'Bônus', prompt_bonus, system_bonus)

        st.divider()
        st.markdown("#### 🔗 Link da Monetizze")
        st.markdown(\"\"\"<div style="background:#F0FDF4;border:1px solid #86EFAC;border-radius:8px;padding:12px 16px;margin-bottom:12px;color:#14532D;font-size:0.87em;line-height:1.6;">
        ✅ <strong>Agora é o momento certo.</strong> Seu e-book e bônus estão prontos.<br>
        Cadastre-os na Monetizze, copie o link de venda e cole abaixo.<br>
        Ele entrará automaticamente nas mensagens de venda.
        </div>\"\"\", unsafe_allow_html=True)
        col_lnk, col_lbtn = st.columns([4,1])
        with col_lnk:
            lnk = st.text_input("Link da Monetizze:", value=st.session_state.dados.get('link_monetizze',''),
                placeholder="https://go.monetizze.com.br/...", label_visibility="collapsed", key="nx46")
        with col_lbtn:
            if st.button("💾 Salvar link", use_container_width=True, key="nx45"):
                if lnk.strip():
                    st.session_state.dados['link_monetizze'] = lnk.strip()
                    st.success("Link salvo!")
                else:
                    st.warning("Cole o link antes de salvar.")
        if st.session_state.dados.get('link_monetizze'):
            st.caption(f"✅ Link salvo: {st.session_state.dados['link_monetizze']}")

        st.divider()
        if st.button("AVANÇAR →", key="nx44"): st.session_state.etapa = "Copy_Face"; st.rerun()

# ── ANÚNCIO ───────────────────────────────────────────────────
elif st.session_state.etapa == "Copy_Face":
    barra_navegacao()
    st.title("📣 ANÚNCIO")
    st.caption("Um anúncio completo e alinhado com a landing page — mesma promessa, mesmo tom, mesma linguagem.")

    # Link da LP
    st.markdown("#### 🔗 Link da sua Landing Page")
    col_lp, col_lp_btn = st.columns([4,1])
    with col_lp:
        lp_link = st.text_input("Link da Landing Page:", value=st.session_state.dados.get('link_lp',''),
            placeholder="https://sualandingpage.com.br", label_visibility="collapsed", key="nx43")
    with col_lp_btn:
        if st.button("💾 Salvar", key="salvar_lp_link", use_container_width=True):
            if lp_link.strip():
                st.session_state.dados['link_lp'] = lp_link.strip()
                st.success("Salvo!")
    if st.session_state.dados.get('link_lp'):
        st.caption(f"✅ Link salvo: {st.session_state.dados['link_lp']}")

    st.divider()
    if st.button("GERAR ANÚNCIO", key="nx42"):
        with st.spinner("Gerando anúncio com IA..."):
            st.session_state.dados['fb_copy'] = chamar_ia(prompt_fb(), system_fb())

    if 'fb_copy' in st.session_state.dados:
        bloco_conteudo('fb_copy', 'Anúncio', prompt_fb, system_fb)

        # ── MODIFICAÇÃO: segundo texto com instruções completas ──
        link_lp_atual = st.session_state.dados.get('link_lp','')
        if link_lp_atual:
            st.markdown(f\"\"\"<div style="background:#ECFDF5;border:1px solid #6EE7B7;border-radius:8px;padding:12px 16px;font-size:0.85em;color:#064E3B;margin-bottom:10px;">
            ✅ <strong>Link salvo:</strong> ao subir esse anúncio no Facebook Ads, coloque <strong>{link_lp_atual}</strong> como URL de destino do botão.
            </div>\"\"\", unsafe_allow_html=True)
        else:
            st.markdown(\"\"\"<div style="background:#FEF3C7;border:1px solid #FCD34D;border-radius:8px;padding:12px 16px;font-size:0.85em;color:#78350F;margin-bottom:10px;">
            ⚠️ <strong>Importante:</strong> ao subir esse anúncio no Facebook Ads, insira o link da sua landing page como URL de destino do botão CTA.
            </div>\"\"\", unsafe_allow_html=True)

        # ── NOVO: segundo bloco com workflow ChatGPT + Gamma ──
        st.markdown(\"\"\"<div class="dica-ferramenta">
        <strong>📋 Próximo passo — publicar o anúncio:</strong><br><br>
        <strong>1. Copie o texto</strong> com o botão acima (Copiar como .txt)<br><br>
        <strong>2. Crie a imagem do anúncio no ChatGPT:</strong><br>
        &nbsp;&nbsp;&nbsp;• Acesse <a href="https://chat.openai.com" target="_blank" style="color:#92400E;">chat.openai.com</a> e abra uma conversa nova<br>
        &nbsp;&nbsp;&nbsp;• Cole o texto do anúncio e peça: <em>"Crie uma imagem para esse anúncio de Facebook Ads, formato quadrado 1080x1080px, visual chamativo e profissional"</em><br>
        &nbsp;&nbsp;&nbsp;• Baixe a imagem gerada<br><br>
        <strong>3. Suba no Facebook Ads Manager:</strong><br>
        &nbsp;&nbsp;&nbsp;• Cole o texto copiado no campo de texto principal<br>
        &nbsp;&nbsp;&nbsp;• Faça upload da imagem gerada pelo ChatGPT<br>
        &nbsp;&nbsp;&nbsp;• No campo de URL de destino, cole o link da sua landing page<br>
        &nbsp;&nbsp;&nbsp;• Escolha o botão CTA: <em>"Saiba mais"</em> ou <em>"Inscreva-se"</em>
        </div>\"\"\", unsafe_allow_html=True)

        # Tutorial Facebook
        st.divider()
        with st.expander("📘 TUTORIAL — Como anunciar no Facebook Ads passo a passo"):
            st.markdown(\"\"\"
<div style="font-size:0.88em;line-height:1.8;color:#1E293B;">

<div style="background:#1877F2;color:white;border-radius:8px;padding:10px 16px;margin-bottom:16px;font-family:Rajdhani,sans-serif;font-size:1.05em;font-weight:700;">
📘 PASSO A PASSO — FACEBOOK ADS
</div>

**PASSO 1 — Acesse o Gerenciador de Anúncios**
Acesse: [business.facebook.com/adsmanager](https://business.facebook.com/adsmanager)

**PASSO 2 — Crie uma nova campanha**
Clique em **+ Criar** → Objetivo: **Tráfego** (direciona para sua LP)

**PASSO 3 — Configure o público**
- Localização: Brasil · Idade: seu público-alvo · Interesses: termos do nicho
- Tamanho ideal: 500 mil a 3 milhões

**PASSO 4 — Defina o orçamento**
- Orçamento diário: R$ 10 a R$ 20/dia

**PASSO 5 — Crie o anúncio**
- Formato: imagem única
- Texto principal: cole o texto gerado
- Imagem: use a gerada pelo ChatGPT (1080x1080px)
- URL de destino: link da sua landing page
- Botão CTA: "Saiba mais" ou "Inscreva-se"

**PASSO 6 — Publicar**
Revise todos os campos → **Publicar** → Facebook revisa em até 24h

**PASSO 7 — Métricas**
- CPL (Custo por Lead): meta até R$ 2,00
- CTR: meta acima de 1,5%
- CPC: meta abaixo de R$ 1,50

</div>
            \"\"\", unsafe_allow_html=True)

        if st.button("AVANÇAR →", key="nx41"): st.session_state.etapa = "Copy_LP"; st.rerun()

# ── LANDING PAGE ──────────────────────────────────────────────
elif st.session_state.etapa == "Copy_LP":
    barra_navegacao()
    st.title("🌐 LANDING PAGE")
    st.caption("Diagnóstico: mostra que o grupo vai descobrir o que está travando o resultado — a solução vem na venda.")

    st.markdown("#### 🔗 Link de convite do grupo (WhatsApp ou Telegram)")
    st.markdown(\"\"\"<div style="background:#F0FDF4;border:1px solid #86EFAC;border-radius:8px;padding:10px 16px;margin-bottom:12px;color:#14532D;font-size:0.86em;line-height:1.6;">
    O botão CTA da landing page deve levar direto para o grupo.<br>
    Cole abaixo o link de convite do seu grupo.
    </div>\"\"\", unsafe_allow_html=True)
    col_gr, col_gr_btn = st.columns([4,1])
    with col_gr:
        grupo_link = st.text_input("Link de convite do grupo:", value=st.session_state.dados.get('link_grupo',''),
            placeholder="https://chat.whatsapp.com/...", label_visibility="collapsed", key="nx40")
    with col_gr_btn:
        if st.button("💾 Salvar", key="salvar_grupo_link", use_container_width=True):
            if grupo_link.strip():
                st.session_state.dados['link_grupo'] = grupo_link.strip()
                st.success("Salvo!")
    if st.session_state.dados.get('link_grupo'):
        st.caption(f"✅ Link salvo: {st.session_state.dados['link_grupo']}")

    st.divider()
    if st.button("GERAR LANDING PAGE", key="nx39"):
        with st.spinner("Gerando landing page com IA..."):
            st.session_state.dados['lp_copy'] = chamar_ia(prompt_lp(), system_lp())

    if 'lp_copy' in st.session_state.dados:
        bloco_conteudo('lp_copy', 'Landing Page', prompt_lp, system_lp)

        st.markdown(\"\"\"
        <div style="background:#EFF6FF;border:1px solid #93C5FD;border-radius:10px;padding:14px 18px;margin-top:16px;">
        <strong style="color:#1E3A8A;">🎨 Como criar sua Landing Page gratuitamente</strong><br><br>
        Use o <strong>Gamma.app</strong> ou <strong>Carrd.co</strong> para montar sua página em minutos:<br><br>
        <strong>No Gamma.app:</strong><br>
        1. Acesse <a href="https://gamma.app" target="_blank">gamma.app</a> e crie uma conta gratuita<br>
        2. Clique em <strong>New → Paste in text</strong><br>
        3. Cole o texto gerado acima<br>
        4. Escolha um tema visual e clique em <strong>Generate</strong><br>
        5. Adicione uma imagem sua ou do nicho na seção do autor<br>
        6. Configure o botão CTA com o link do seu grupo<br>
        7. Publique e copie o link gerado<br><br>
        <strong>💡 Dica:</strong> No Gamma, você pode adicionar imagens, mudar cores e personalizar tudo visualmente sem saber programar.
        </div>
        \"\"\", unsafe_allow_html=True)

        link_grupo_atual = st.session_state.dados.get('link_grupo','')
        if link_grupo_atual:
            st.markdown(f\"\"\"<div style="background:#ECFDF5;border:1px solid #6EE7B7;border-radius:8px;padding:12px 16px;font-size:0.85em;color:#064E3B;margin-bottom:10px;">
            ✅ <strong>Lembre-se:</strong> configure o botão CTA da sua landing page apontando para <strong>{link_grupo_atual}</strong>
            </div>\"\"\", unsafe_allow_html=True)
        else:
            st.markdown(\"\"\"<div style="background:#FEF3C7;border:1px solid #FCD34D;border-radius:8px;padding:12px 16px;font-size:0.85em;color:#78350F;margin-bottom:10px;">
            ⚠️ <strong>Importante:</strong> configure o botão CTA da landing page apontando para o link de convite do seu grupo.
            </div>\"\"\", unsafe_allow_html=True)

        # ── NOVO: segundo bloco com workflow Gamma ──
        st.markdown(f\"\"\"<div class="dica-ferramenta">
        <strong>🌐 Próximo passo — transformar em site com Gamma AI:</strong><br><br>
        <strong>1. Copie o texto</strong> com o botão acima (Copiar como .txt)<br><br>
        <strong>2. Acesse o Gamma AI:</strong><br>
        &nbsp;&nbsp;&nbsp;• Abra <a href="https://gamma.app" target="_blank" style="color:#92400E;">gamma.app</a> e crie uma conta gratuita<br>
        &nbsp;&nbsp;&nbsp;• Clique em <strong>New → Page (site/landing page)</strong><br>
        &nbsp;&nbsp;&nbsp;• Cole o texto copiado no campo de geração<br>
        &nbsp;&nbsp;&nbsp;• Escolha o tema visual que combine com seu nicho<br>
        &nbsp;&nbsp;&nbsp;• Clique em <strong>Generate</strong> — o Gamma criará o site automaticamente<br><br>
        <strong>3. Configure o botão CTA:</strong><br>
        &nbsp;&nbsp;&nbsp;• No editor do Gamma, clique no botão CTA gerado<br>
        &nbsp;&nbsp;&nbsp;• Insira o link do grupo: <strong>{link_grupo_atual if link_grupo_atual else '[link do seu grupo aqui]'}</strong><br>
        &nbsp;&nbsp;&nbsp;• Clique em <strong>Publish</strong> para obter o link público do site<br><br>
        <strong>4. Use o link do site</strong> como URL de destino do seu anúncio no Facebook Ads
        </div>\"\"\", unsafe_allow_html=True)

        if st.button("AVANÇAR →", key="nx38"): st.session_state.etapa = "Mensagens_Grupo"; st.rerun()

# ── MENSAGENS DO GRUPO ────────────────────────────────────────
elif st.session_state.etapa == "Mensagens_Grupo":
    barra_navegacao()
    st.title("💬 MENSAGENS DO GRUPO")

    st.markdown(\"\"\"<div class="preview-box">
    <strong>10 mensagens prontas — use uma por dia no grupo:</strong><br><br>
    📋 <strong>Descrição</strong> — texto da bio do grupo (configurar uma vez só)<br>
    💬 <strong>D-8</strong> — Boas-vindas automática ao entrar<br>
    📅 <strong>D-9</strong> — Abertura: cria expectativa para o diagnóstico do dia seguinte<br>
    🎯 <strong>D-10</strong> — Diagnóstico: pergunta interativa<br>
    🔥 <strong>D-11</strong> — 3 dicas surpreendentes sobre o nicho<br>
    📌 <strong>D-12</strong> — Atividade de observação (mantém mistério)<br>
    💡 <strong>D-13</strong> — Padrão oculto (sem revelar a causa)<br>
    ⏳ <strong>D-14</strong> — Véspera: texto fixo aprovado<br>
    🚀 <strong>Manhã</strong> — Lançamento: copy de venda com link<br>
    ⏰ <strong>Noite</strong> — Lembrete 19h: última chance
    </div>\"\"\", unsafe_allow_html=True)

    # ── AVISO REVISÃO BÔNUS ───────────────────────────────────
    bonus_resumo = st.session_state.dados.get('bonus_resumo','')
    if bonus_resumo:
        st.markdown(f\"\"\"<div style="background:#FEF9C3;border:1px solid #FDE047;border-radius:8px;padding:12px 16px;margin-bottom:8px;color:#713F12;font-size:0.88em;line-height:1.6;">
        ⚠️ <strong>Confira os nomes dos seus bônus antes de gerar:</strong><br>
        {bonus_resumo}<br>
        <em>Eles aparecerão na mensagem de venda. Se quiser alterar, volte em Bônus e regenere.</em>
        </div>\"\"\", unsafe_allow_html=True)

    st.markdown(\"\"\"<div style="background:#FEF3C7;border:1px solid #FCD34D;border-radius:8px;padding:10px 16px;margin-bottom:8px;color:#78350F;font-size:0.85em;line-height:1.6;">
    ⚠️ <strong>Antes de enviar, revise:</strong>
    D-10 (diagnóstico) · D-11 (dicas) · D-12 (atividade) · D-13 (prova social) — gerados pela IA, os demais são texto fixo aprovado.
    </div>\"\"\", unsafe_allow_html=True)

    if not st.session_state.dados.get('whatsapp_contato'):
        st.warning("⚠️ Você não preencheu o WhatsApp de contato no formulário.")

    st.markdown('<div class="btn-verde15">', unsafe_allow_html=True)
    gerar_msg = st.button("💬 GERAR FUNIL COMPLETO DE MENSAGENS", key="nx37")
    st.markdown('</div>', unsafe_allow_html=True)

    if gerar_msg:
        with st.spinner("Gerando o funil completo de mensagens..."):
            st.session_state.dados['msg_grupo'] = chamar_ia(prompt_msg(), system_msg())
            st.rerun()

    if 'msg_grupo' in st.session_state.dados:
        st.divider()
        st.markdown("#### Suas mensagens prontas para enviar")
        bloco_conteudo('msg_grupo', 'Mensagens', prompt_msg, system_msg)

        st.divider()
        st.markdown("#### 🔗 Inserir link da Monetizze")
        col_link, col_btn = st.columns([4, 1])
        with col_link:
            link_input = st.text_input(
                "Link:", value=st.session_state.dados.get('link_monetizze', ''),
                placeholder="https://go.monetizze.com.br/...", label_visibility="collapsed",
                             key="nx36"
                         )
        with col_btn:
            if st.button("✅ Aplicar", use_container_width=True, key="nx35"):
                if link_input.strip():
                    st.session_state.dados['link_monetizze'] = link_input.strip()
                    st.session_state.dados['msg_grupo'] = st.session_state.dados['msg_grupo'].replace('[LINK MONETIZZE]', link_input.strip())
                    st.rerun()
                else:
                    st.warning("Cole o link antes de aplicar.")

        st.divider()

        # ── SALVAR NO COMPUTADOR ───────────────────────────────
        nome_projeto = st.session_state.dados.get('nome_eb', 'meu_projeto')
        nome_arquivo = nome_projeto.replace(' ', '_').lower()
        json_projeto = gerar_json_projeto(st.session_state.dados)
        salvar_projeto(nome_projeto, st.session_state.dados)

        st.markdown(\"\"\"<div style="background:#F0FDF4;border:2px solid #22C55E;border-radius:12px;padding:18px 20px;margin-bottom:14px;color:#14532D;font-size:0.92em;line-height:1.8;">
        💾 <strong>Projeto pronto! Salve agora no seu computador.</strong><br>
        <span style="font-size:0.88em;">Clique no botão abaixo para baixar o arquivo. Da próxima vez que acessar o app, faça o upload do arquivo em <strong>📂 Meus Projetos → Carregar projeto (.json)</strong> e tudo estará lá do jeito que você deixou.</span>
        </div>\"\"\", unsafe_allow_html=True)

        st.markdown('<div class="btn-verde15">', unsafe_allow_html=True)
        st.download_button(
            label="💾 SALVAR PROJETO NO COMPUTADOR (.json)",
            data=json_projeto,
            file_name=f"{nome_arquivo}_nexus.json",
            mime="application/json",
            use_container_width=True,
            key="nx34"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        st.caption("📌 Guarde esse arquivo em um lugar seguro — ele contém todo o seu projeto de lançamento.")
        st.session_state.etapa = "Visualizacao"

# ── VISUALIZAÇÃO FINAL ────────────────────────────────────────
elif st.session_state.etapa == "Visualizacao":
    barra_navegacao()
    nome_projeto = st.session_state.dados.get('nome_eb', 'Projeto')
    st.title(f"PROJETO: {nome_projeto}")
    d = st.session_state.dados

    texto_completo = f\"\"\"NEXUS LAUNCHER — PROJETO COMPLETO
{'='*50}
E-BOOK: {d.get('nome_eb','')}
NICHO: {d.get('nicho','')}
PÚBLICO: {d.get('publico','')}
DATA DE LANÇAMENTO: {d.get('data_lancto','')}
PREÇO: R${d.get('preco',47)}
{'='*50}

📚 E-BOOK PRINCIPAL
{'-'*40}
{limpar_html(d.get('ebook_cont','Não gerado.'))}

🎁 E-BOOKS BÔNUS
{'-'*40}
{limpar_html(d.get('bonus_cont','Não gerado.'))}

📣 ANÚNCIO
{'-'*40}
{limpar_html(d.get('fb_copy','Não gerado.'))}

🌐 LANDING PAGE
{'-'*40}
{limpar_html(d.get('lp_copy','Não gerado.'))}

💬 MENSAGENS DO GRUPO (FUNIL COMPLETO)
{'-'*40}
{limpar_html(d.get('msg_grupo','Não gerado.'))}\"\"\".strip()

    # ── SALVAR LOCAL (botão prominente no topo da visualização) ──
    nome_arquivo = nome_projeto.replace(' ', '_').lower()
    json_projeto = gerar_json_projeto(d)

    # ── BOTÃO PRINCIPAL — SALVAR NO COMPUTADOR ────────────────
    st.markdown(\"\"\"<div style="background:#F0FDF4;border:2px solid #22C55E;border-radius:12px;padding:16px 20px;margin-bottom:14px;color:#14532D;font-size:0.9em;line-height:1.7;">
    💾 <strong>Salve seu projeto no computador</strong> — é a forma mais segura de guardar tudo.<br>
    <span style="font-size:0.88em;">Da próxima vez que acessar, vá em <strong>📂 Meus Projetos → Carregar projeto (.json)</strong> e continue de onde parou.</span>
    </div>\"\"\", unsafe_allow_html=True)

    st.markdown('<div class="btn-verde15">', unsafe_allow_html=True)
    st.download_button(
        label="💾 SALVAR PROJETO NO COMPUTADOR (.json)",
        data=json_projeto,
        file_name=f"{nome_arquivo}_nexus.json",
        mime="application/json",
        use_container_width=True,
        key="nx33"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="btn-secundario">', unsafe_allow_html=True)
    st.download_button(
        label="⬇️ Baixar projeto completo em texto (.txt)",
        data=texto_completo,
        file_name=f"{nome_arquivo}_lancamento.txt",
        mime="text/plain",
        use_container_width=True,
        key="nx32"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # ── CARREGAR PROJETO LOCAL ────────────────────────────────
    with st.expander("📂 Meus Projetos — Carregar projeto (.json)"):
        st.caption("Selecione o arquivo .json salvo anteriormente para continuar de onde parou.")
    st.divider()
    with st.expander("📚 E-BOOK"):
        bloco_conteudo('ebook_cont','E-book',prompt_ebook,system_ebook)
    with st.expander("🎁 E-BOOKS BÔNUS"):
        bloco_conteudo('bonus_cont','Bônus',prompt_bonus,system_bonus)
    with st.expander("📣 ANÚNCIO"):
        bloco_conteudo('fb_copy','Anúncio',prompt_fb,system_fb)
    with st.expander("🌐 LANDING PAGE"):
        bloco_conteudo('lp_copy','Landing Page',prompt_lp,system_lp)
    with st.expander("💬 MENSAGENS DO GRUPO — FUNIL COMPLETO"):
        st.caption("Boas-vindas → D-7 a D-1 → Venda manhã → Lembrete noturno")
        bloco_conteudo('msg_grupo','Mensagens',prompt_msg,system_msg)

    # ── AGENDADOR DE MENSAGENS ───────────────────────────────
    st.divider()
    with st.expander("📅 AGENDADOR — Calendário de envio das mensagens"):
        data_lancto = d.get('data_lancto')
        # Corrigir: ao carregar JSON, data pode vir como string
        if isinstance(data_lancto, str):
            try:
                from datetime import date as _date
                data_lancto = _date.fromisoformat(data_lancto)
                d['data_lancto'] = data_lancto
            except: data_lancto = None

        if not data_lancto:
            st.warning("Defina a data de lançamento no formulário para usar o agendador.")
        elif not d.get('msg_grupo'):
            st.info("Gere as mensagens primeiro para usar o agendador.")
        else:
            AGENDA_DEF = [
                {"chave": "DESCRICAO_GRUPO", "label": "📋 Descrição do grupo (bio)",          "emoji": "📋", "offset": -15, "hora_pad": "08:00", "cor": "#64748B", "quando": "15 dias antes do lançamento"},
                {"chave": "BOAS_VINDAS",     "label": "💬 Boas-vindas ao grupo",              "emoji": "💬", "offset": -8,  "hora_pad": "08:00", "cor": "#0EA5E9", "quando": "8 dias antes do lançamento"},
                {"chave": "DIA_7",           "label": "📅 Abertura — 7 dias antes",           "emoji": "📅", "offset": -7,  "hora_pad": "08:00", "cor": "#0EA5E9", "quando": "7 dias antes do lançamento"},
                {"chave": "DIA_6",           "label": "🎯 Enquete — 6 dias antes",            "emoji": "🎯", "offset": -6,  "hora_pad": "08:00", "cor": "#8B5CF6", "quando": "6 dias antes do lançamento"},
                {"chave": "DIA_5",           "label": "🔥 Dica — 5 dias antes",              "emoji": "🔥", "offset": -5,  "hora_pad": "08:00", "cor": "#8B5CF6", "quando": "5 dias antes do lançamento"},
                {"chave": "DIA_4",           "label": "📌 Atividade — 4 dias antes",          "emoji": "\\U0001F4CC", "offset": -4,  "hora_pad": "08:00", "cor": "#8B5CF6", "quando": "4 dias antes do lançamento"},
                {"chave": "DIA_3",           "label": "💡 Prova social — 3 dias antes",       "emoji": "💡", "offset": -3,  "hora_pad": "08:00", "cor": "#8B5CF6", "quando": "3 dias antes do lançamento"},
                {"chave": "VESPERA",         "label": "⏳ Véspera do lançamento",             "emoji": "⏳", "offset": -1,  "hora_pad": "08:00", "cor": "#B45309", "quando": "Véspera — 1 dia antes"},
                {"chave": "VENDA_MANHA",     "label": "🚀 Dia do lançamento — manhã",        "emoji": "🚀", "offset":  0,  "hora_pad": "08:00", "cor": "#22C55E", "quando": "Dia do lançamento (manhã)"},
                {"chave": "VENDA_NOITE",     "label": "⏰ Dia do lançamento — noite",        "emoji": "⏰", "offset":  0,  "hora_pad": "19:00", "cor": "#22C55E", "quando": "Dia do lançamento (noite)"},
            ]

            secoes_map = {s['chave']: limpar_html(s['conteudo']) for s in parsear_mensagens(d['msg_grupo'])}
            horas_config = st.session_state.dados.get('agenda_horas', {})

            st.markdown("#### Horários de envio")
            for item in AGENDA_DEF:
                chave = item['chave']
                data_msg = data_lancto + timedelta(days=item.get('offset', 0))
                data_str = data_msg.strftime('%d/%m')
                quando = item.get('quando', item['label'])
                col_label, col_hora = st.columns([4, 1])
                with col_label:
                    st.markdown(
                        f"<div style='padding:5px 0;font-size:0.87em;color:#1E293B;'>"
                        f"<span style='display:inline-block;width:14px;height:14px;"
                        f"border-radius:3px;background:{item.get('cor', '#888')};margin-right:6px;"
                        f"vertical-align:middle;'></span>"
                        f"<strong>{quando}</strong> <span style='color:#94A3B8;'>({data_str})</span>"
                        f"</div>",
                        unsafe_allow_html=True
                    )
                with col_hora:
                    hora_val = horas_config.get(chave, item.get('hora_pad', ""))
                    hora_input = st.text_input(
                        "h", value=hora_val, key=f"hora_{chave}",
                        label_visibility="collapsed", placeholder="HH:MM"
                    )
                    horas_config[chave] = hora_input

            st.session_state.dados['agenda_horas'] = horas_config

            if st.button("📅 EXPORTAR CALENDÁRIO (.ics)", use_container_width=True, key="nx30"):
                eventos = []
                for item in AGENDA_DEF:
                    chave    = item['chave']
                    data_msg = data_lancto + timedelta(days=item.get('offset', 0))
                    hora     = horas_config.get(chave, item.get('hora_pad', ""))
                    texto    = secoes_map.get(chave, '')
                    if not texto: continue
                    eventos.append({
                        'chave':     chave,
                        'titulo':    f"[Nexus] {item.get('emoji', chr(0x1F4CC))} {item['label']}",
                        'data':      data_msg,
                        'hora':      hora,
                        'descricao': texto,
                    })
                ics_content = gerar_ics(eventos)
                st.download_button(
                    label="⬇️ Baixar arquivo .ics",
                    data=ics_content.encode('utf-8'),
                    file_name=f"lancamento_{d.get('nome_eb','').replace(' ','_')}.ics",
                    mime="text/calendar",
                    use_container_width=True,
                    key="nx29"
                )
                st.success("Pronto! Importe no Google Calendar, Apple Calendar ou Outlook.")

            st.markdown(\"\"\"<div style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:8px;padding:10px 14px;margin-top:10px;color:#64748B;font-size:0.78em;line-height:1.7;">
            💡 <strong>Como importar:</strong>
            Google Calendar → Configurações → Importar → selecione o .ics &nbsp;|&nbsp;
            Apple Calendar → Arquivo → Importar &nbsp;|&nbsp;
            Outlook → Arquivo → Abrir e Exportar → Importar
            </div>\"\"\", unsafe_allow_html=True)

    # ── DICA MESTRE ──────────────────────────────────────────
    st.divider()
    with st.expander("🧠 DICA MESTRE — O QUE FAZER DEPOIS DO LANÇAMENTO"):
        st.markdown(\"\"\"<div style="background:#F0FDF4;border:2px solid #22C55E;border-radius:12px;padding:22px 26px;color:#14532D;line-height:1.7;font-size:0.92em;">
        <strong style="font-size:1.05em;">Não apague esse grupo.</strong><br><br>
        Aqui dentro, você construiu algo extremamente valioso: atenção e interesse de pessoas reais.
        Esse grupo é um ativo. Se bem utilizado, ele pode gerar novos resultados sem investimento em tráfego.<br><br>
        <strong>Mas existe um ponto importante: evite excesso.</strong><br>
        O ideal é realizar novos lançamentos com equilíbrio — aproximadamente 1 vez por mês.
        </div>\"\"\", unsafe_allow_html=True)

    st.divider()
    with st.expander("✅ CHECKLIST DE LANÇAMENTO — O QUE FAZER AGORA"):
        data_lancto = d.get('data_lancto', date.today())
        dlf  = data_lancto.strftime('%d/%m/%Y') if hasattr(data_lancto,'strftime') else str(data_lancto)
        dm1  = (data_lancto - timedelta(days=1)).strftime('%d/%m/%Y') if hasattr(data_lancto,'strftime') else ''
        d7   = (data_lancto - timedelta(days=7)).strftime('%d/%m/%Y') if hasattr(data_lancto,'strftime') else ''
        d6   = (data_lancto - timedelta(days=6)).strftime('%d/%m/%Y') if hasattr(data_lancto,'strftime') else ''
        d5   = (data_lancto - timedelta(days=5)).strftime('%d/%m/%Y') if hasattr(data_lancto,'strftime') else ''
        d4   = (data_lancto - timedelta(days=4)).strftime('%d/%m/%Y') if hasattr(data_lancto,'strftime') else ''
        d3   = (data_lancto - timedelta(days=3)).strftime('%d/%m/%Y') if hasattr(data_lancto,'strftime') else ''
        d2   = (data_lancto - timedelta(days=2)).strftime('%d/%m/%Y') if hasattr(data_lancto,'strftime') else ''

        fases = [
            {"fase":"FASE 1 — HOJE: Preparação","cor":"#0EA5E9","items":[
                ("Hoje","Baixe o projeto completo (.json e .txt)"),
                ("Hoje","Cadastre o e-book + 3 bônus na Monetizze — configure o checkout"),
                (f"Hoje",f"Preço: R${d.get('preco',47)} — salve o link de venda"),
                ("Hoje","Crie o grupo: 'Programa [X] Dias para [Objetivo]'"),
                ("Hoje","Cole a DESCRIÇÃO DO GRUPO no campo de informações do WhatsApp/Telegram"),
                ("Hoje","Configure a mensagem de BOAS-VINDAS automática ao entrar"),
                ("Hoje","Gere a imagem do anúncio no ChatGPT e suba no Facebook Ads"),
                ("Hoje","Configure a LANDING PAGE no Gamma AI com CTA apontando para o grupo"),
            ]},
            {"fase":"FASE 2 — SEMANA 1: Encher o grupo","cor":"#8B5CF6","items":[
                ("Dias 1 a 8","Anúncios rodando — objetivo: 500 a 1.000 pessoas no grupo"),
                ("Diariamente","Monitore custo por lead — meta: até R$2,00 por pessoa"),
            ]},
            {"fase":"FASE 3 — SEMANA 2: Aquecimento","cor":"#059669","items":[
                (f"{d7} — D-7","Envie: Abertura do programa"),
                (f"{d6} — D-6","Envie: Enquete — respostas no WhatsApp de contato"),
                (f"{d5} — D-5","Envie: Dica prática"),
                (f"{d4} — D-4","Envie: Atividade rápida"),
                (f"{d3} — D-3","Envie: Relato de resultado"),
                (f"{dm1} — D-1","Envie: Véspera da venda"),
                (f"{dm1}","Confirme se o link da Monetizze está funcionando"),
            ]},
            {"fase":f"FASE 4 — {dlf}: Dia da venda","cor":"#22C55E","items":[
                (f"{dlf} — manhã","Envie a mensagem de lançamento com o link"),
                (f"{dlf}","Fique disponível no WhatsApp para responder dúvidas"),
                (f"{dlf} — 19h","Envie o lembrete noturno"),
            ]},
            {"fase":"FASE 5 — PÓS-LANÇAMENTO","cor":"#64748B","items":[
                ("Após","Registre: pessoas no grupo, vendas, taxa de conversão, ROI"),
                ("Após","Verifique na Monetizze se os acessos foram entregues"),
                ("Próximo mês","Use o mesmo grupo para relançar"),
            ]},
        ]
        for fase in fases:
            st.markdown(f'<div style="margin:18px 0 8px 0;padding:8px 14px;background:{fase["cor"]};border-radius:8px;color:white;font-weight:600;font-size:0.85em;letter-spacing:0.5px">{fase["fase"]}</div>', unsafe_allow_html=True)
            for quando, acao in fase['items']:
                st.markdown(f'<div class="checklist-item"><div style="width:10px;height:10px;border-radius:50%;background:{fase["cor"]};margin-top:5px;flex-shrink:0"></div><div><div style="font-size:0.72em;color:#64748B;font-weight:600;text-transform:uppercase;letter-spacing:0.5px">{quando}</div><div style="font-size:0.92em;color:#1E293B">{acao}</div></div></div>', unsafe_allow_html=True)

    st.divider()
    with st.expander("📈 MÉTRICAS PÓS-LANÇAMENTO"):
        m = st.session_state.dados.get('metricas_pos', {})
        col1, col2, col3 = st.columns(3)
        with col1:
            m['grupo_pessoas']  = st.number_input("Pessoas no grupo", min_value=0, value=int(m.get('grupo_pessoas',0)), key="mp1")
            m['cliques_link']   = st.number_input("Cliques no link de venda", min_value=0, value=int(m.get('cliques_link',0)), key="mp2")
        with col2:
            m['vendas_reais']   = st.number_input("Vendas realizadas", min_value=0, value=int(m.get('vendas_reais',0)), key="mp3")
            m['custo_trafego']  = st.number_input("Custo de tráfego (R$)", min_value=0.0, value=float(m.get('custo_trafego',0)), key="mp4")
        with col3:
            m['reembolsos']     = st.number_input("Reembolsos / estornos", min_value=0, value=int(m.get('reembolsos',0)), key="mp5")
            m['preco_real']     = st.number_input("Preço vendido (R$)", min_value=0.0, value=float(m.get('preco_real', d.get('preco',47))), key="mp6")

        st.session_state.dados['metricas_pos'] = m

        vendas_liq   = max(0, int(m.get('vendas_reais',0)) - int(m.get('reembolsos',0)))
        faturamento  = vendas_liq * float(m.get('preco_real', d.get('preco',47)))
        custo        = float(m.get('custo_trafego',0))
        lucro        = faturamento - custo
        grupo        = int(m.get('grupo_pessoas',1)) or 1
        tx_conv      = (vendas_liq / grupo * 100) if grupo else 0
        roi          = ((lucro / custo) * 100) if custo else 0
        cpl          = (custo / grupo) if grupo else 0

        if vendas_liq > 0 or faturamento > 0:
            r1, r2, r3, r4 = st.columns(4)
            r1.metric("Faturamento líquido", f"R${faturamento:,.0f}".replace(',','.'))
            r2.metric("Lucro real", f"R${lucro:,.0f}".replace(',','.'))
            r3.metric("ROI", f"{roi:.0f}%")
            r4.metric("CPL", f"R${cpl:.2f}")
            if tx_conv < 1:
                st.info("⚠️ Abaixo de 1% — revise a mensagem de venda e o aquecimento.")
            elif tx_conv < 3:
                st.info("✅ Entre 1-3% — resultado esperado para primeiro lançamento.")
            else:
                st.info("🔥 Acima de 3% — excelente! Escale o tráfego no próximo.")

    st.divider()
    with st.expander("📊 CALCULADORA PRÉ-LANÇAMENTO"):
        col_a, col_b = st.columns(2)
        with col_a:
            leads_v = st.number_input("Pessoas no grupo:", min_value=100, max_value=100000, value=1000, step=100, key="leads_vis")
            conv_v  = st.slider("Taxa de conversão (%):", 1, 30, 10, key="conv_vis")
        with col_b:
            preco_v = st.number_input("Preço (R$):", min_value=9, max_value=997, value=int(d.get('preco',47)), key="preco_vis")
            custo_v = st.number_input("Custo de tráfego (R$):", min_value=0, max_value=50000, value=int(leads_v*1.5), key="custo_vis")
        vendas_v = int(leads_v * conv_v / 100)
        fat_v = vendas_v * preco_v
        lucro_v = fat_v - custo_v
        c1, c2, c3 = st.columns(3)
        c1.metric("Vendas", f"{vendas_v}")
        c2.metric("Faturamento", f"R${fat_v:,.0f}".replace(',','.'))
        c3.metric("Lucro", f"R${lucro_v:,.0f}".replace(',','.'))

    st.divider()
    st.markdown("### 🤖 Launcerbot")
    if st.session_state.chat_hist:
        for q, r in st.session_state.chat_hist:
            st.markdown(f"**Você:** {q}")
            st.markdown(f"<div class='chat-bubble'>{r}</div>", unsafe_allow_html=True)

    pergunta = st.text_input("Sua pergunta:", key=f"chat_input_{st.session_state.chat_input_key}", label_visibility="collapsed", placeholder="Digite sua pergunta aqui...")
    if st.button("ENVIAR", key="nx28"):
        if pergunta.strip():
            with st.spinner("Launcerbot pensando..."):
                system = (f"Você é o Launcerbot, assistente especialista em lançamentos digitais. "
                          f"Usuário: {st.session_state.usuario}. "
                          f"Projeto: nicho={d.get('nicho')}, ebook={d.get('nome_eb')}, público={d.get('publico')}.")
                try:
                    client = Groq(api_key=st.session_state.api_key)
                    messages = [{"role": "system", "content": system}]
                    for q_hist, r_hist in st.session_state.chat_hist:
                        messages.append({"role": "user", "content": q_hist})
                        messages.append({"role": "assistant", "content": r_hist})
                    messages.append({"role": "user", "content": pergunta})
                    response = client.chat.completions.create(messages=messages, model="openai/gpt-oss-120b")
                    resp = response.choices[0].message.content
                    if resp: st.session_state['res_geral_nexusl1'] = str(resp)
                except Exception as e:
                    resp = f"⚠️ Erro na API: {e}"
                st.session_state.chat_hist.append((pergunta, resp))
                st.session_state.chat_input_key += 1
                st.rerun()
        else: st.warning("Digite uma pergunta antes de enviar.")

# ── LANÇAMENTO DE VIDEOAULAS ─────────────────────────────────

elif st.session_state.etapa == "Video_Formulario":
    st.title("🎬 LANÇAMENTO DE VIDEOAULAS")
    st.markdown(\"\"\"<div class="preview-box">
    <strong>Método CPL — Como funciona:</strong><br>
    📣 Pré-pré-lançamento → 🎬 CPL 1 (Oportunidade) → 🎬 CPL 2 (Transformação) →
    🎬 CPL 3 (Objeções) → 🛒 Abertura de carrinho → ⏰ Fechamento com urgência
    </div>\"\"\", unsafe_allow_html=True)
    d = st.session_state.dados

    st.markdown("#### Dados do produto")
    d['v_nicho']    = st.text_input("Nicho:", value=d.get('v_nicho',''), key="nx27")
    d['v_publico']  = st.text_input("Público-alvo:", value=d.get('v_publico',''), key="nx26")
    d['v_produto']  = st.text_input("Nome do curso/videoaulas:", value=d.get('v_produto',''), key="nx25")
    d['v_dor']      = st.text_input("Principal dor que resolve:", value=d.get('v_dor',''), key="nx24")
    d['v_promessa'] = st.text_input("Promessa de transformação:", value=d.get('v_promessa',''), key="nx23")
    d['v_preco']    = st.number_input("Preço do curso (R$):", min_value=47, max_value=9997, value=int(d.get('v_preco',497)), step=10, key="nx22")
    d['v_garantia'] = st.selectbox("Garantia:", ["7 dias","14 dias","30 dias"], index=["7 dias","14 dias","30 dias"].index(d.get('v_garantia','7 dias')), key="nx21")
    d['v_bonus']    = st.text_input("Bônus inclusos (separe por vírgula):", value=d.get('v_bonus',''), key="nx20")
    d['v_autor']    = st.text_input("Seu nome:", value=d.get('v_autor',''), key="nx19")
    d['v_cred']     = st.text_area("Sua credencial/experiência:", value=d.get('v_cred',''), key="nx18")

    st.divider()
    st.markdown("#### Datas do lançamento")
    col1, col2 = st.columns(2)
    with col1:
        d['v_data_cpl1'] = st.date_input("CPL 1 — 1º vídeo:", value=d.get('v_data_cpl1', date.today() + timedelta(days=7)), key="nx17")
        d['v_data_cpl2'] = st.date_input("CPL 2 — 2º vídeo:", value=d.get('v_data_cpl2', date.today() + timedelta(days=11)), key="nx16")
        d['v_data_cpl3'] = st.date_input("CPL 3 — 3º vídeo:", value=d.get('v_data_cpl3', date.today() + timedelta(days=15)), key="nx15")
    with col2:
        d['v_data_abertura'] = st.date_input("Abertura do carrinho:", value=d.get('v_data_abertura', date.today() + timedelta(days=18)), key="nx14")
        d['v_data_fechamento'] = st.date_input("Fechamento do carrinho:", value=d.get('v_data_fechamento', date.today() + timedelta(days=21)), key="nx13")

    st.divider()
    if st.button("AVANÇAR → GERAR LANÇAMENTO COMPLETO", key="nx12"):
        if not d.get('v_nicho') or not d.get('v_produto'):
            st.warning("Preencha pelo menos nicho e nome do produto.")
        else:
            st.session_state.etapa = "Video_Gerar"; st.rerun()

elif st.session_state.etapa == "Video_Gerar":
    st.title("🎬 GERANDO SEU LANÇAMENTO DE VIDEOAULAS")
    barra_video = {"Video_Formulario":"1. Dados","Video_Gerar":"2. Conteúdo","Video_Final":"3. Projeto"}
    badges = ""
    for k,v in barra_video.items():
        cls = "ativo" if k == "Video_Gerar" else ""
        badges += f'<span class="step-badge {cls}">{v}</span>'
    st.markdown(f'<div class="step-indicator">{badges}</div>', unsafe_allow_html=True)

    d = st.session_state.dados
    n = d.get('v_nicho',''); pub = d.get('v_publico',''); prod = d.get('v_produto','')
    dor = d.get('v_dor',''); prom = d.get('v_promessa',''); preco = d.get('v_preco',497)
    garantia = d.get('v_garantia','7 dias'); bonus = d.get('v_bonus','')
    autor = d.get('v_autor',''); cred = d.get('v_cred','')
    d1 = d.get('v_data_cpl1', date.today()).strftime('%d/%m')
    d2 = d.get('v_data_cpl2', date.today()).strftime('%d/%m')
    d3 = d.get('v_data_cpl3', date.today()).strftime('%d/%m')
    da = d.get('v_data_abertura', date.today()).strftime('%d/%m/%Y')
    df = d.get('v_data_fechamento', date.today()).strftime('%d/%m/%Y')

    # PRÉ-PRÉ-LANÇAMENTO
    if not d.get('v_pre_pre'):
        if st.button("🔥 1. GERAR PRÉ-PRÉ-LANÇAMENTO (stories + posts de bastidores)", key="nx11"):
            with st.spinner("Gerando conteúdo de antecipação..."):
                p = (f"Crie o conteúdo de pré-pré-lançamento para o curso '{prod}' sobre {n}.\\n"
                     f"Público: {pub}. Dor: {dor}.\\n\\n"
                     f"Gere:\\n"
                     f"1. 7 STORIES progressivos (um por dia) que criam antecipação crescente.\\n\\n"
                     f"2. 3 POSTS para feed com bastidores.\\n\\n"
                     f"REGRAS: Gatilhos de antecipação, autoridade e curiosidade. Zero venda.")
                d['v_pre_pre'] = chamar_ia(p, "Você é especialista em lançamentos digitais e copywriting.")
                st.rerun()
    else:
        with st.expander("🔥 Pré-pré-lançamento — Stories e bastidores", expanded=True):
            st.markdown(f"<div class='caixa-texto'>{normalizar_markdown(d.get('v_pre_pre', ''))}</div>", unsafe_allow_html=True)
            col1,col2,col3 = st.columns(3)
            col1.download_button("📋 Copiar", data=limpar_html(d.get('v_pre_pre', '')), file_name="pre_pre.txt", mime="text/plain", key="dl_prepre")
            if col2.button("🔄 Regenerar"): d.pop('v_pre_pre'); st.rerun()
            if col3.button("✍️ Corrigir gramática", key="gr_prepre"):
                with st.spinner("Revisando..."): d['v_pre_pre'] = corrigir_texto(limpar_html(d.get('v_pre_pre', ''))); st.rerun()

    # CPL 1
    if d.get('v_pre_pre') and not d.get('v_cpl1'):
        if st.button(f"🎬 2. GERAR CPL 1 — Oportunidade ({d1})", key="nx10"):
            with st.spinner("Gerando roteiro CPL 1..."):
                p = (f"Crie o CPL 1 — OPORTUNIDADE — para o curso '{prod}' sobre {n}.\\n"
                     f"Público: {pub}. Dor: {dor}. Promessa: {prom}.\\n\\n"
                     f"ROTEIRO DO VÍDEO CPL 1 (8-12 min):\\n"
                     f"- Hook · Problema · Oportunidade · Prova rápida · Teaser CPL2 · CTA\\n\\n"
                     f"SEQUÊNCIA DE WHATSAPP PÓS-CPL1 (3 mensagens).")
                d['v_cpl1'] = chamar_ia(p, "Você é especialista em lançamentos CPL.")
                st.rerun()
    elif d.get('v_cpl1'):
        with st.expander(f"🎬 CPL 1 — Oportunidade ({d1})", expanded=True):
            st.markdown(f"<div class='caixa-texto'>{normalizar_markdown(d['v_cpl1'])}</div>", unsafe_allow_html=True)
            col1,col2,col3 = st.columns(3)
            col1.download_button("📋 Copiar", data=limpar_html(d['v_cpl1']), file_name="cpl1.txt", mime="text/plain", key="dl_cpl1")
            if col2.button("🔄 Regenerar"): d.pop('v_cpl1'); st.rerun()
            if col3.button("✍️ Corrigir gramática", key="gr_cpl1"):
                with st.spinner("Revisando..."): d['v_cpl1'] = corrigir_texto(limpar_html(d['v_cpl1'])); st.rerun()

    # CPL 2
    if d.get('v_cpl1') and not d.get('v_cpl2'):
        if st.button(f"🎬 3. GERAR CPL 2 — Transformação ({d2})", key="nx9"):
            with st.spinner("Gerando roteiro CPL 2..."):
                p = (f"Crie o CPL 2 — TRANSFORMAÇÃO — para '{prod}' sobre {n}.\\n"
                     f"Público: {pub}. Credencial: {cred}.\\n\\n"
                     f"ROTEIRO (8-12 min): Recap · Prova social · O método · Credencial do autor · Teaser CPL3 · CTA\\n\\n"
                     f"SEQUÊNCIA DE WHATSAPP PÓS-CPL2 (3 mensagens).")
                d['v_cpl2'] = chamar_ia(p, "Você é especialista em lançamentos CPL.")
                st.rerun()
    elif d.get('v_cpl2'):
        with st.expander(f"🎬 CPL 2 — Transformação ({d2})", expanded=True):
            st.markdown(f"<div class='caixa-texto'>{normalizar_markdown(d.get('v_cpl2', ''))}</div>", unsafe_allow_html=True)
            col1,col2,col3 = st.columns(3)
            col1.download_button("📋 Copiar", data=limpar_html(d.get('v_cpl2', '')), file_name="cpl2.txt", mime="text/plain", key="dl_cpl2")
            if col2.button("🔄 Regenerar"): d.pop('v_cpl2'); st.rerun()
            if col3.button("✍️ Corrigir gramática", key="gr_cpl2"):
                with st.spinner("Revisando..."): d['v_cpl2'] = corrigir_texto(limpar_html(d.get('v_cpl2', ''))); st.rerun()

    # CPL 3
    if d.get('v_cpl2') and not d.get('v_cpl3'):
        if st.button(f"🎬 4. GERAR CPL 3 — Quebra de objeções ({d3})", key="nx8"):
            with st.spinner("Gerando roteiro CPL 3..."):
                p = (f"Crie o CPL 3 — QUEBRA DE OBJEÇÕES — para '{prod}' sobre {n}.\\n"
                     f"Preço: R${preco}. Data abertura: {da}.\\n\\n"
                     f"ROTEIRO (10-15 min): Abertura forte · 5 objeções respondidas · FAQ · Antecipação · CTA\\n\\n"
                     f"SEQUÊNCIA DE WHATSAPP (3 mensagens de antecipação pré-abertura).")
                d['v_cpl3'] = chamar_ia(p, "Você é especialista em quebra de objeções.")
                st.rerun()
    elif d.get('v_cpl3'):
        with st.expander(f"🎬 CPL 3 — Quebra de objeções ({d3})", expanded=True):
            st.markdown(f"<div class='caixa-texto'>{normalizar_markdown(d.get('v_cpl3', ''))}</div>", unsafe_allow_html=True)
            col1,col2,col3 = st.columns(3)
            col1.download_button("📋 Copiar", data=limpar_html(d.get('v_cpl3', '')), file_name="cpl3.txt", mime="text/plain", key="dl_cpl3")
            if col2.button("🔄 Regenerar"): d.pop('v_cpl3'); st.rerun()
            if col3.button("✍️ Corrigir gramática", key="gr_cpl3"):
                with st.spinner("Revisando..."): d['v_cpl3'] = corrigir_texto(limpar_html(d.get('v_cpl3', ''))); st.rerun()

    # ABERTURA DE CARRINHO
    if d.get('v_cpl3') and not d.get('v_abertura'):
        if st.button(f"🛒 5. GERAR ABERTURA DE CARRINHO ({da})", key="nx7"):
            with st.spinner("Gerando copy de abertura..."):
                bonus_lista = '\\n'.join([f'🎁 {b.strip()}' for b in bonus.split(',') if b.strip()]) if bonus else '🎁 Bônus exclusivos'
                p = (f"Crie a copy completa de ABERTURA DE CARRINHO para '{prod}' sobre {n}.\\n"
                     f"Preço: R${preco}. Garantia: {garantia}.\\n\\n"
                     f"Gere: E-mail de abertura · Mensagem WhatsApp manhã · Post feed · Story (3 frames)\\n\\n"
                     f"Bônus:\\n{bonus_lista}")
                d['v_abertura'] = chamar_ia(p, "Você é especialista em copy de abertura de carrinho.")
                st.rerun()
    elif d.get('v_abertura'):
        with st.expander(f"🛒 Abertura de carrinho ({da})", expanded=True):
            st.markdown(f"<div class='caixa-texto'>{normalizar_markdown(d.get('v_abertura', ''))}</div>", unsafe_allow_html=True)
            col1,col2,col3 = st.columns(3)
            col1.download_button("📋 Copiar", data=limpar_html(d.get('v_abertura', '')), file_name="abertura_carrinho.txt", mime="text/plain", key="dl_aber")
            if col2.button("🔄 Regenerar"): d.pop('v_abertura'); st.rerun()
            if col3.button("✍️ Corrigir gramática", key="gr_aber"):
                with st.spinner("Revisando..."): d['v_abertura'] = corrigir_texto(limpar_html(d.get('v_abertura', ''))); st.rerun()

    # FECHAMENTO
    if d.get('v_abertura') and not d.get('v_fechamento'):
        if st.button(f"⏰ 6. GERAR FECHAMENTO — Urgência máxima ({df})", key="nx6"):
            with st.spinner("Gerando copy de fechamento..."):
                p = (f"Crie a copy de FECHAMENTO DE CARRINHO para '{prod}' sobre {n}.\\n"
                     f"Carrinho fecha em {df}. Preço: R${preco}. Garantia: {garantia}.\\n\\n"
                     f"Gere: WhatsApp 24h antes · WhatsApp manhã do fechamento · WhatsApp 2h antes · E-mail última chance · Story contagem regressiva")
                d['v_fechamento'] = chamar_ia(p, "Você é especialista em copy de fechamento e urgência.")
                st.rerun()
    elif d.get('v_fechamento'):
        with st.expander(f"⏰ Fechamento — Urgência máxima ({df})", expanded=True):
            st.markdown(f"<div class='caixa-texto'>{normalizar_markdown(d['v_fechamento'])}</div>", unsafe_allow_html=True)
            col1,col2,col3 = st.columns(3)
            col1.download_button("📋 Copiar", data=limpar_html(d['v_fechamento']), file_name="fechamento.txt", mime="text/plain", key="dl_fech")
            if col2.button("🔄 Regenerar"): d.pop('v_fechamento'); st.rerun()
            if col3.button("✍️ Corrigir gramática", key="gr_fech"):
                with st.spinner("Revisando..."): d['v_fechamento'] = corrigir_texto(limpar_html(d['v_fechamento'])); st.rerun()

    if d.get('v_fechamento'):
        st.divider()
        st.success("✅ Lançamento CPL completo gerado!")
        nome_v = d.get('v_produto','curso').replace(' ','_')
        texto_v = f\"\"\"NEXUS LAUNCHER — LANÇAMENTO DE VIDEOAULAS
{'='*50}
CURSO: {d.get('v_produto','')}
NICHO: {d.get('v_nicho','')}
{'='*50}

PRÉ-PRÉ-LANÇAMENTO\\n{'-'*40}\\n{limpar_html(d.get('v_pre_pre',''))}
CPL 1\\n{'-'*40}\\n{limpar_html(d.get('v_cpl1',''))}
CPL 2\\n{'-'*40}\\n{limpar_html(d.get('v_cpl2',''))}
CPL 3\\n{'-'*40}\\n{limpar_html(d.get('v_cpl3',''))}
ABERTURA\\n{'-'*40}\\n{limpar_html(d.get('v_abertura',''))}
FECHAMENTO\\n{'-'*40}\\n{limpar_html(d.get('v_fechamento',''))}\"\"\"

        col_txt_v, col_json_v = st.columns(2)
        with col_txt_v:
            st.markdown('<div class="btn-verde">', unsafe_allow_html=True)
            st.download_button("⬇️ BAIXAR COMPLETO (.txt)", data=texto_v,
                file_name=f"{nome_v}_lancamento_video.txt", mime="text/plain", use_container_width=True, key="nx5")
            st.markdown('</div>', unsafe_allow_html=True)
        with col_json_v:
            st.markdown('<div class="btn-verde">', unsafe_allow_html=True)
            st.download_button("💾 SALVAR NO COMPUTADOR (.json)", data=gerar_json_projeto(d),
                file_name=f"{nome_v}_nexus.json", mime="application/json", use_container_width=True, key="nx4")
            st.markdown('</div>', unsafe_allow_html=True)

        # Agendador CPL
        st.divider()
        with st.expander("📅 AGENDADOR CPL — Calendário de envio"):
            CPL_AGENDA = [
                {"chave":"v_pre_pre",    "label":"🔥 Pré-pré-lançamento",   "data_key":"v_data_cpl1",      "offset":-7, "hora":"09:00", "cor":"#64748B"},
                {"chave":"v_cpl1",       "label":"🎬 CPL 1 — Oportunidade", "data_key":"v_data_cpl1",      "offset":0,  "hora":"10:00", "cor":"#1D4ED8"},
                {"chave":"v_cpl2",       "label":"🎬 CPL 2 — Transformação","data_key":"v_data_cpl2",      "offset":0,  "hora":"10:00", "cor":"#8B5CF6"},
                {"chave":"v_cpl3",       "label":"🎬 CPL 3 — Objeções",     "data_key":"v_data_cpl3",      "offset":0,  "hora":"10:00", "cor":"#B45309"},
                {"chave":"v_abertura",   "label":"🛒 Abertura do carrinho", "data_key":"v_data_abertura",  "offset":0,  "hora":"08:00", "cor":"#22C55E"},
                {"chave":"v_fechamento", "label":"⏰ Fechamento",            "data_key":"v_data_fechamento","offset":0,  "hora":"08:00", "cor":"#B91C1C"},
            ]
            horas_cpl = d.get('agenda_horas_cpl', {})
            for item in CPL_AGENDA:
                data_base = d.get(item.get("data_key", ""), date.today())
                data_ev = data_base + timedelta(days=item.get("offset", 0))
                col_l, col_h = st.columns([4,1])
                with col_l:
                    st.markdown(
                        f"<div style='padding:5px 0;font-size:0.87em;'>"
                        f"<span style='display:inline-block;width:12px;height:12px;border-radius:3px;"
                        f"background:{item.get('cor', '#888')};margin-right:6px;vertical-align:middle;'></span>"
                        f"<span style='color:#64748B;font-size:0.8em;font-weight:600;margin-right:6px;'>{data_ev.strftime('%d/%m')}</span>"
                        f"{item['label']}</div>", unsafe_allow_html=True)
                with col_h:
                    horas_cpl[item["chave"]] = st.text_input("h", value=horas_cpl.get(item["chave"], item.get("hora", "")),
                        key=f"hcpl_{item['chave']}", label_visibility="collapsed")
            d['agenda_horas_cpl'] = horas_cpl

            if st.button("📅 EXPORTAR CALENDÁRIO CPL (.ics)", use_container_width=True, key="nx3"):
                eventos_cpl = []
                for item in CPL_AGENDA:
                    data_base = d.get(item.get("data_key", ""), date.today())
                    data_ev = data_base + timedelta(days=item.get("offset", 0))
                    texto = limpar_html(d.get(item["chave"], ""))
                    if not texto: continue
                    eventos_cpl.append({"chave": item["chave"], "titulo": f"[Nexus CPL] {item['label']}",
                        "data": data_ev, "hora": horas_cpl.get(item["chave"], item.get("hora", "")), "descricao": texto})
                ics = gerar_ics(eventos_cpl)
                st.download_button("⬇️ Baixar .ics", data=ics.encode('utf-8'),
                    file_name=f"{nome_v}_cpl.ics", mime="text/calendar", use_container_width=True, key="nx2")
                st.success("Importe no Google Calendar, Apple Calendar ou Outlook.")

        if st.button("🔙 Voltar à escolha de lançamento", key="nx1"):
            st.session_state.etapa = "Escolha_Tipo"; st.rerun()


# --- RODAPÉ ---
st.markdown("<div class='footer'>© 2026 Nexus Launcher – Lançamento digital inteligente</div>", unsafe_allow_html=True)
""",
}
AGENTES = [
    {"id": "viagens",        "emoji": "🗺️",  "nome": "Guia de Viagens",    "categoria": "Viagens · Lazer",        "codigo": "guia_viagens",       "auth_key": "etapa",       "etapa_app": "App"},
    {"id": "nutricao",       "emoji": "🍽️",  "nome": "NutriMind AI",       "categoria": "Nutrição · Dieta",       "codigo": "chef_calorico",      "auth_key": "etapa",       "etapa_app": "App"},
    {"id": "personal",       "emoji": "💪",   "nome": "Personal Trainer",   "categoria": "Fitness · Saúde",        "codigo": "personal_trainer",   "auth_key": "etapa",       "etapa_app": "App"},
    {"id": "concursos",      "emoji": "🎓",   "nome": "Tutor Concursos",    "categoria": "Concursos · Carreira",   "codigo": "tutor_concursos",    "auth_key": "etapa",       "etapa_app": "App"},
    {"id": "ingles",         "emoji": "🇺🇸", "nome": "Nexus English",      "categoria": "Inglês · Idiomas",       "codigo": "nexus_english",      "auth_key": "etapa",       "etapa_app": "app"},
    {"id": "investigacao",   "emoji": "🔍",   "nome": "Sherlock IA",        "categoria": "Investigação · Análise", "codigo": "sherlock_ia",        "auth_key": "etapa",       "etapa_app": "App"},
    {"id": "financeiro",     "emoji": "💰",   "nome": "Oráculo Financeiro", "categoria": "Finanças · Dinheiro",    "codigo": "oraculo_financeiro", "auth_key": "autenticado", "etapa_app": True},
    {"id": "relacionamentos","emoji": "💘",   "nome": "Conexão Magnética",  "categoria": "Relacionamentos · Amor", "codigo": "conexao_magnetica",  "auth_key": "etapa",       "etapa_app": "App"},
    {"id": "invencoes",      "emoji": "💡",   "nome": "Invenções IA",       "categoria": "Inovação · Criatividade","codigo": "invencoes_ia",       "auth_key": "etapa",       "etapa_app": "App"},
    {"id": "nexus",          "emoji": "🚀",   "nome": "Nexus Launch",       "categoria": "Startups · Negócios",    "codigo": "nexus_launcher",     "auth_key": "etapa",       "etapa_app": "Escolha_Tipo"},
]


# ── INICIALIZAÇÃO DE ESTADO ───────────────────────────────────────────────
_defaults = {
    "sa_etapa":   "Login",
    "sa_agente":  None,
    "sa_usuario": "",
    "sa_api_key": "",
}
for _k, _v in _defaults.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v

# ── HELPER: EXECUTAR AGENTE EMBUTIDO ─────────────────────────────────────
def _executar_agente(agente: dict):
    import math, random, pandas as pd
    from datetime import datetime, date, timedelta

    codigo_key = agente["codigo"]
    if codigo_key not in _CODIGOS_AGENTES:
        st.error(f"❌ Código do agente '{agente['nome']}' não encontrado.")
        return

    codigo = _CODIGOS_AGENTES[codigo_key]

    # Propaga credenciais do hub
    st.session_state["usuario"] = st.session_state.sa_usuario
    st.session_state["api_key"] = st.session_state.sa_api_key
    st.session_state["nome"]    = st.session_state.sa_usuario

    # Bypass de autenticação
    auth_key  = agente["auth_key"]
    etapa_app = agente["etapa_app"]

    if auth_key == "autenticado":
        st.session_state["autenticado"] = True
        st.session_state["nome_user"]   = st.session_state.sa_usuario
    else:
        estados_login = {"Login", "login", "", None, "diagnostico"}
        if st.session_state.get("etapa", "") in estados_login:
            st.session_state["etapa"] = etapa_app

    # Nexus English: perfil precisa existir com chaves corretas ao pular login
    if codigo_key == "nexus_english":
        if not st.session_state.get("perfil") or "habilidades" not in st.session_state.get("perfil", {}):
            st.session_state["perfil"] = {
                "nome": st.session_state.sa_usuario,
                "nivel_estimado": "A1",
                "objetivo": "Aprender inglês",
                "api_key": st.session_state.sa_api_key,
                "unidade_atual": "A1_U01",
                "streak_dias": 0,
                "ultima_aula": None,
                "habilidades": {},
                "vocabulario": [],
                "erros_recorrentes": [],
                "sessoes": [],
                "historico_chat": [],
                "historico_conv": [],
                "diagnostico_feito": False,
                "pontos": 0,
            }
            st.session_state["etapa"] = "app"

    # Namespace de módulo limpo — simula execução independente de um .py
    # Inclui todos os imports que os agentes usam no nível de módulo
    _ns = {
        "__file__":   f"<{codigo_key}>",
        "__name__":   "__main__",
        "__builtins__": __builtins__,
        # bibliotecas usadas pelos agentes
        "st":         st,
        "Groq":       Groq,
        "json":       json,
        "os":         os,
        "re":         re,
        "math":       math,
        "random":     random,
        "pd":         pd,
        "datetime":   datetime,
        "date":       date,
        "timedelta":  timedelta,
    }
    exec(compile(codigo, f"<{codigo_key}>", "exec"), _ns)

    # CSS de reforço — aplicado DEPOIS do agente para sobrescrever estilos inline
    st.markdown("""<style>
input, textarea,
[data-baseweb="input"] input,
[data-baseweb="textarea"] textarea,
[data-baseweb="base-input"] input,
[data-baseweb="base-input"] > div {
    background:#FFFFFF !important;
    background-color:#FFFFFF !important;
    color:#1A1A2E !important;
}
[data-baseweb="input"] > div,
[data-baseweb="input"],
[data-baseweb="textarea"],
[data-baseweb="base-input"] {
    background:#FFFFFF !important;
    background-color:#FFFFFF !important;
}
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="block-container"],
.stApp { background-color:#F8F9FA !important; }
p, span, label, div, li, td, th, h1, h2, h3, h4, h5, h6,
[data-testid="stMarkdownContainer"] * { color:#1A1A2E !important; }
.stButton > button, .stButton > button * { color:white !important; }
[data-testid="stDownloadButton"] > button,
[data-testid="stDownloadButton"] > button * { color:white !important; }
[data-testid="stDownloadButton"] > button svg,
[data-testid="stDownloadButton"] > button svg * { fill:white !important; }
[data-testid="stFileUploader"] svg,
[data-testid="stFileUploader"] svg * { fill:#495057 !important; color:#495057 !important; }
</style>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════
# TELA: LOGIN
# ══════════════════════════════════════════════════════════════════════════
if st.session_state.sa_etapa == "Login":

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown("""
        <div style="text-align:center; padding: 20px 0 10px 0;">
            <div style="font-size:4em;">🤖</div>
            <h1 style="margin:0; font-size:2em; color:#1A1A2E;">Super Agente IA</h1>
            <p style="color:#6C757D; margin-top:6px;">10 agentes especializados em um só lugar</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card" style="text-align:center;">
            <b>🔒 ACESSO RESTRITO A CLIENTES</b><br>
            <a href="https://meusagentesia.com.br" target="_blank"
               style="color:#16A34A; font-weight:700; text-decoration:underline;">
               meusagentesia.com.br
            </a>
        </div>
        """, unsafe_allow_html=True)

        nome  = st.text_input("👤 Seu Nome:", key="sa_inp_nome",  placeholder="Como quer ser chamado?")
        chave = st.text_input("🔑 Chave API da Groq:", type="password", key="sa_inp_chave", placeholder="gsk_...")

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("✨ ENTRAR NO SUPER AGENTE", key="sa_btn_login"):
            if len(nome.strip()) < 2:
                st.warning("⚠️ Digite um nome com pelo menos 2 letras.")
            elif not chave.strip():
                st.warning("⚠️ Insira sua chave API da Groq.")
            else:
                st.session_state.sa_usuario = nome.strip()
                st.session_state.sa_api_key = chave.strip()
                st.session_state.sa_etapa = "Hub"
                st.rerun()

        st.markdown("""
        <p style="text-align:center; color:#9CA3AF; font-size:0.78em; margin-top:16px;">
            💻 Melhor experiência no computador
        </p>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════
# TELA: HUB
# ══════════════════════════════════════════════════════════════════════════
elif st.session_state.sa_etapa == "Hub":

    col_t, col_s = st.columns([5, 1])
    with col_t:
        st.markdown(f"""
        <div class="hub-header">
            <div style="font-size:3em; margin-bottom:8px;">🤖</div>
            <h1 style="color:#1E1B4B !important; margin:0; font-size:1.8em;">Super Agente IA</h1>
            <p style="margin:6px 0 0 0; font-size:1em;">
                <span style="color:#1E1B4B !important; font-weight:400;">Olá,</span>
                <span style="color:#1E1B4B !important; font-weight:700;">{st.session_state.sa_usuario}</span>
                <span style="color:#1E1B4B !important; font-weight:400;">· Escolha seu agente</span>
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col_s:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        if st.button("🚪 Sair", key="sa_btn_sair"):
            for _k in list(st.session_state.keys()):
                del st.session_state[_k]
            st.rerun()

    cols_por_linha = 3
    for i in range(0, len(AGENTES), cols_por_linha):
        linha = AGENTES[i:i + cols_por_linha]
        colunas = st.columns(cols_por_linha)
        for col, agente in zip(colunas, linha):
            with col:
                st.markdown(f"""
                <div class="hub-card">
                    <span class="hub-emoji">{agente['emoji']}</span>
                    <div class="hub-nome">{agente['nome']}</div>
                    <div class="hub-cat">{agente['categoria']}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("▶ Abrir", key=f"sa_hub_{agente['id']}", use_container_width=True):
                    for _k in ["etapa", "autenticado", "nome_user"]:
                        if _k in st.session_state:
                            del st.session_state[_k]
                    st.session_state.sa_agente = agente["id"]
                    st.session_state.sa_etapa  = "Agente"
                    st.rerun()

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center; color:#9CA3AF; font-size:0.78em;">
        10 agentes especializados · meusagentesia.com.br
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════
# TELA: AGENTE
# ══════════════════════════════════════════════════════════════════════════
elif st.session_state.sa_etapa == "Agente":

    agente_ativo = next(
        (a for a in AGENTES if a["id"] == st.session_state.sa_agente), None
    )

    if agente_ativo is None:
        st.error("Agente não encontrado.")
        if st.button("← Voltar ao Hub", key="sa_back_404"):
            st.session_state.sa_etapa = "Hub"
            st.rerun()
    else:
        col_back, col_titulo = st.columns([1, 6])
        with col_back:
            if st.button("⬅ Hub", key="sa_btn_back", use_container_width=True):
                for _k in ["etapa", "autenticado", "nome_user"]:
                    if _k in st.session_state:
                        del st.session_state[_k]
                st.session_state.sa_etapa  = "Hub"
                st.session_state.sa_agente = None
                st.rerun()
        with col_titulo:
            st.markdown(f"""
            <div style="padding:8px 0; color:#6C757D; font-size:0.88em; line-height:2;">
                {agente_ativo['emoji']} <strong style="color:#1A1A2E;">{agente_ativo['nome']}</strong>
                &nbsp;·&nbsp; {agente_ativo['categoria']}
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<hr class='divider'>", unsafe_allow_html=True)

        _executar_agente(agente_ativo)
