"""
Iara Bot - Assistente Jurídica em Direito da Saúde
Versão standalone - NÃO precisa de estrutura de pastas
"""

import streamlit as st
from datetime import datetime
from typing import Optional, Callable, Dict
from dataclasses import dataclass

# ============================================
# CONFIGURAÇÕES
# ============================================
CALENDLY_LINK = "https://calendly.com/dra-lethicia"
PIX_KEY = "dra.lethicia@adv.br"
L = "Dra. Lethícia Fernanda"

st.set_page_config(
    page_title="Iara Bot - Assistente Jurídica",
    page_icon="⚖️",
    layout="wide"
)

# ============================================
# CSS PERSONALIZADO
# ============================================
st.markdown("""
<style>
    .chat-message {
        padding: 1rem;
        border-radius: 0.8rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .bot-message {
        background-color: #f0f2f6;
        border-left: 4px solid #2c7be5;
        align-items: flex-start;
    }
    .user-message {
        background-color: #2c7be5;
        color: white;
        align-items: flex-end;
        margin-left: 20%;
    }
    .user-message p {
        color: white;
    }
    .chat-container {
        max-height: 550px;
        overflow-y: auto;
        padding: 1rem;
        border: 1px solid #ddd;
        border-radius: 10px;
        background-color: #fafafa;
    }
    .stButton button {
        background-color: #2c7be5;
        color: white;
        border-radius: 20px;
    }
    hr {
        margin: 1rem 0;
    }
    .info-box {
        background-color: #e8f5e9;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# FUNÇÕES AUXILIARES
# ============================================

def _n(r: str) -> str:
    return str(r).strip().lower()

def _sim(r: str) -> bool:
    return any(p in _n(r) for p in ["sim", "s", "yes", "quero", "ok", "claro", "vamos", "aceito", "topo", "1", "sozinha", "sozinho"])

def _nao(r: str) -> bool:
    return any(p in _n(r) for p in ["não", "nao", "no", "2", "depois", "sem", "agora não"])

EMENTA = "[COLE A EMENTA AQUI]"

# ============================================
# CLASSE ETAPA
# ============================================

@dataclass
class Etapa:
    nome: str
    pergunta: str
    opcoes: Optional[list] = None
    proxima: Optional[str] = None
    router: Optional[Callable] = None
    salvar_em: Optional[str] = None

ETAPAS: Dict[str, Etapa] = {}

def _r(e: Etapa):
    ETAPAS[e.nome] = e
    return e

# ══════════════════════════════════════════════════════
# ENTRADA
# ══════════════════════════════════════════════════════

_r(Etapa(
    nome="INICIO",
    pergunta=(
        "Olá, seja bem vindo(a). 🌹\n"
        "Sou a Iara, assistente jurídica do escritório da Dra Lethicia Fernanda, "
        "advogada especialista em Direito da Saúde. "
        "Fico feliz que você entrou em contato conosco. Qual o seu nome?"
    ),
    proxima="CANAL",
))

_r(Etapa(
    nome="CANAL",
    pergunta="Seu atendimento é pelo *SUS* ou por *Plano de Saúde*?",
    opcoes=["SUS", "Plano de Saúde"],
    router=lambda r: "SUS_CATEGORIA" if "sus" in _n(r) else "PS_TEMPO",
    salvar_em="canal",
))

# ══════════════════════════════════════════════════════
# BLOCO SUS
# ══════════════════════════════════════════════════════

_r(Etapa(
    nome="SUS_CATEGORIA",
    pergunta="Me diga o que você está aguardando?",
    opcoes=["Cirurgia / Tratamento", "Consultas / Exames"],
    router=lambda r: "SUS_ESPECIALIDADE" if any(p in _n(r) for p in ["cirurgia", "tratamento", "1"]) else "SUS_CONSULTA_TIPO",
    salvar_em="categoria",
))

_r(Etapa(
    nome="SUS_ESPECIALIDADE",
    pergunta="Para que eu direcione você para o protocolo de urgência correto, qual problema estamos enfrentando hoje?",
    opcoes=["Oncologia", "Neurodivergências (TEA, TDAH)", "Endometriose", "Medicamento", "Bariátrica", "Reparadora", "Neurologia", "Cardiologia", "Outros"],
    router=lambda r: (
        "POS_SUS" if any(p in _n(r) for p in ["oncologia", "câncer", "1"]) else
        "POS_SUS" if any(p in _n(r) for p in ["tea", "neuro", "2"]) else
        "POS_SUS"
    ),
    salvar_em="especialidade",
))

# ══════════════════════════════════════════════════════
# SUS — CONSULTAS / EXAMES
# ══════════════════════════════════════════════════════

_r(Etapa(
    nome="SUS_CONSULTA_TIPO",
    pergunta="Para que eu direcione você para o protocolo correto, qual problema estamos enfrentando hoje?",
    opcoes=["Consulta especializada", "Exame específico"],
    router=lambda r: "SUS_CONSULTA_PERGS" if "consulta" in _n(r) else "SUS_EXAME_PERGS",
    salvar_em="subarea",
))

_r(Etapa(
    nome="SUS_CONSULTA_PERGS",
    pergunta="Entendi que você está aguardando uma consulta especializada. Qual especialidade médica você está aguardando?",
    proxima="SUS_CONSULTA_DOC",
    salvar_em="especialidade_consulta",
))

_r(Etapa(
    nome="SUS_CONSULTA_DOC",
    pergunta="Você tem encaminhamento ou pedido médico pra essa consulta?",
    proxima="POS_SUS",
    salvar_em="tem_encaminhamento",
))

_r(Etapa(
    nome="SUS_EXAME_PERGS",
    pergunta="Qual exame o médico solicitou pra você?",
    proxima="POS_SUS",
    salvar_em="exame_solicitado",
))

# ══════════════════════════════════════════════════════
# PÓS PERGUNTAS SUS
# ══════════════════════════════════════════════════════

_r(Etapa(
    nome="POS_SUS",
    pergunta=(
        "Pelos dados que você enviou, fica claro que o seu caso não é apenas uma 'espera comum'. "
        "No SUS, o governo muitas vezes usa a fila da regulação para camuflar a falta de investimento.\n\n"
        "Para resolver isso, eu trabalho com um *Protocolo de Liberação Urgente*. "
        "Isso faria diferença na sua vida agora?"
    ),
    proxima="HONORARIOS_SUS",
))

_r(Etapa(
    nome="HONORARIOS_SUS",
    pergunta=(
        "Como é um trabalho de alta especialidade, o escritório cobra *Honorários Iniciais* "
        "para assumir o caso e protocolar o pedido de liminar.\n\n"
        "Prosseguir com esse caso faz sentido para você garantir sua saúde hoje?"
    ),
    router=lambda r: "FECHAMENTO_SIM" if _sim(r) else "FECHAMENTO_NAO",
    salvar_em="resposta_final",
))

# ══════════════════════════════════════════════════════
# BLOCO PLANO DE SAÚDE
# ══════════════════════════════════════════════════════

_r(Etapa(
    nome="PS_TEMPO",
    pergunta="Você já tem seu plano de saúde há mais de 2 anos?",
    opcoes=["Sim, mais de 2 anos", "Não, menos de 2 anos"],
    router=lambda r: "PS_SITUACAO" if _sim(r) else "PS_NAO_2ANOS",
))

_r(Etapa(nome="PS_NAO_2ANOS", proxima="PS_NAO_2ANOS_Q2",
    pergunta="Me conta, qual o tratamento que você precisa fazer?"))

_r(Etapa(nome="PS_NAO_2ANOS_Q2", proxima="POS_PS",
    pergunta="O médico comentou se isso é urgente ou pode trazer algum risco se não for feito?"))

_r(Etapa(
    nome="PS_SITUACAO",
    pergunta="Para que eu possa te direcionar corretamente, qual é a sua situação atual com o plano de saúde?",
    opcoes=["Reparadora", "Negativa de cirurgia", "Medicamento negado", "Exame negado", "Home care", "Terapias", "Reajuste", "Coparticipação", "Erro médico", "OUTRO"],
    router=lambda r: "POS_PS",
    salvar_em="tipo_negativa_plano",
))

# ══════════════════════════════════════════════════════
# PÓS PERGUNTAS PLANO DE SAÚDE
# ══════════════════════════════════════════════════════

_r(Etapa(
    nome="POS_PS",
    pergunta=(
        "Obrigado pelas informações. Agora me diz: o que você está buscando?\n\n"
        "1️⃣ Quero apenas tirar dúvidas básicas\n"
        "2️⃣ Já tenho a negativa do plano\n"
        "3️⃣ Não tenho a negativa mas sei que o plano vai negar"
    ),
    router=lambda r: (
        "POS_PS_DUVIDAS" if "1" in r else
        "POS_PS_NEGATIVA" if "2" in r else
        "POS_PS_PREVENTIVO"
    ),
))

_r(Etapa(nome="POS_PS_DUVIDAS", proxima="FECHAMENTO_SIM",
    pergunta=(
        "Ofereço uma *consulta de orientação jurídica* — você fala diretamente com a Dra.\n\n"
        f"💰 Valor: R$ 97,00\n\n"
        f"Podemos agendar um horário na agenda da {L}?"
    )))

_r(Etapa(nome="POS_PS_NEGATIVA", proxima="FECHAMENTO_SIM",
    pergunta=(
        "Você está no momento exato de agirmos judicialmente.\n\n"
        "Vou te encaminhar para a agenda da Dra. para uma reunião gratuita de diagnóstico."
    )))

_r(Etapa(nome="POS_PS_PREVENTIVO", proxima="FECHAMENTO_SIM",
    pergunta=(
        "Você é muito estratégico(a)! Vamos blindar seus laudos antes da negativa.\n\n"
        "Vou te encaminhar para a agenda da Dra."
    )))

# ══════════════════════════════════════════════════════
# FECHAMENTOS
# ══════════════════════════════════════════════════════

_r(Etapa(
    nome="FECHAMENTO_SIM",
    pergunta=(
        "Ótimo! 💙\n\n"
        "Vou encaminhar seus dados para a mesa da {lawyer} neste momento.\n\n"
        "🔗 **Agende sua reunião:** {CALENDLY_LINK}\n\n"
        "Fique atento(a)! 👀"
    ),
    proxima="FIM",
))

_r(Etapa(
    nome="FECHAMENTO_NAO",
    pergunta=(
        "Compreendo. Infelizmente, sem ação judicial, seu caso continuará na fila.\n\n"
        "Caso mude de ideia, estamos à disposição. Desejamos sorte no seu tratamento. 🙏"
    ),
    proxima="FIM",
))

_r(Etapa(nome="FIM", pergunta="", proxima=None))

# ============================================
# GERENCIAMENTO DE SESSÃO
# ============================================

def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "estado_atual" not in st.session_state:
        st.session_state.estado_atual = "INICIO"
    if "dados_coletados" not in st.session_state:
        st.session_state.dados_coletados = {}
    if "nome_usuario" not in st.session_state:
        st.session_state.nome_usuario = None

def add_bot_message(text: str):
    if not text:
        return
    text = text.replace("{nome}", st.session_state.nome_usuario or "")
    text = text.replace("{lawyer}", L)
    text = text.replace("{CALENDLY_LINK}", CALENDLY_LINK)
    st.session_state.messages.append({"role": "bot", "content": text})

def add_user_message(text: str):
    st.session_state.messages.append({"role": "user", "content": text})

def get_etapa(estado: str):
    return ETAPAS.get(estado)

def processar_resposta(resposta: str):
    estado_atual = st.session_state.estado_atual
    etapa = get_etapa(estado_atual)
    
    if not etapa:
        st.session_state.estado_atual = "INICIO"
        add_bot_message(ETAPAS["INICIO"].pergunta)
        return
    
    if estado_atual == "INICIO":
        st.session_state.nome_usuario = resposta
        st.session_state.dados_coletados["nome"] = resposta
    
    if etapa.salvar_em:
        st.session_state.dados_coletados[etapa.salvar_em] = resposta
    
    proximo = None
    if etapa.proxima and etapa.proxima != "FIM":
        proximo = etapa.proxima
    elif etapa.router:
        try:
            proximo = etapa.router(resposta)
        except:
            proximo = etapa.proxima
    
    if proximo:
        st.session_state.estado_atual = proximo
        prox_etapa = get_etapa(proximo)
        if prox_etapa and prox_etapa.pergunta:
            add_bot_message(prox_etapa.pergunta)
    elif etapa.proxima == "FIM":
        st.session_state.estado_atual = "FIM"

def reset_conversa():
    st.session_state.clear()
    init_session_state()
    add_bot_message(ETAPAS["INICIO"].pergunta)

# ============================================
# INTERFACE
# ============================================

def render_sidebar():
    with st.sidebar:
        st.markdown(f"## ⚖️ {L}")
        st.markdown("*Especialista em Direito da Saúde*")
        st.markdown("---")
        
        if st.session_state.nome_usuario:
            st.markdown(f"**Cliente:** {st.session_state.nome_usuario}")
        if st.session_state.dados_coletados.get("canal"):
            st.markdown(f"**Canal:** {st.session_state.dados_coletados['canal']}")
        if st.session_state.dados_coletados.get("categoria"):
            st.markdown(f"**Demanda:** {st.session_state.dados_coletados['categoria']}")
        
        st.markdown("---")
        if st.button("🔄 Nova Conversa", use_container_width=True):
            reset_conversa()
            st.rerun()

def render_chat():
    with st.container():
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for msg in st.session_state.messages:
            if msg["role"] == "bot":
                st.markdown(f'<div class="chat-message bot-message"><strong>🤖 Iara:</strong><br>{msg["content"]}</div>', unsafe_allow_html=True)
            else:
                nome = st.session_state.nome_usuario or "Você"
                st.markdown(f'<div class="chat-message user-message"><strong>👤 {nome}:</strong><br>{msg["content"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

def render_opcoes_rapidas():
    estado = st.session_state.estado_atual
    etapa = get_etapa(estado)
    
    if etapa and etapa.opcoes and estado not in ["FIM"]:
        st.markdown("---")
        st.markdown("**🔘 Opções rápidas:**")
        cols = st.columns(min(len(etapa.opcoes), 4))
        for i, opcao in enumerate(etapa.opcoes[:4]):
            with cols[i % 4]:
                if st.button(opcao[:25], key=f"opt_{i}", use_container_width=True):
                    add_user_message(opcao)
                    processar_resposta(opcao)
                    st.rerun()

def render_input():
    estado = st.session_state.estado_atual
    if estado == "FIM":
        st.info("✨ Atendimento finalizado. Clique em 'Nova Conversa' para recomeçar.")
        return
    
    col1, col2 = st.columns([4, 1])
    with col1:
        user_input = st.text_input("Digite sua mensagem:", key="user_input")
    with col2:
        send_button = st.button("📤 Enviar", use_container_width=True)
    
    if send_button and user_input:
        add_user_message(user_input)
        processar_resposta(user_input)
        st.rerun()

# ============================================
# MAIN
# ============================================

def main():
    st.title("⚖️ Iara Bot - Assistente Jurídica em Direito da Saúde")
    st.caption(f"{L} | Atendimento SUS e Planos de Saúde")
    
    init_session_state()
    
    col1, col2 = st.columns([3, 1])
    with col1:
        render_chat()
        render_opcoes_rapidas()
        render_input()
    with col2:
        render_sidebar()
    
    if len(st.session_state.messages) == 0:
        add_bot_message(ETAPAS["INICIO"].pergunta)
        st.rerun()

if __name__ == "__main__":
    main()
