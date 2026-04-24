import streamlit as st
import re
import json
from datetime import datetime
from typing import Dict, Tuple

# ============================================
# CONFIGURAÇÕES DIRETAS (sem .env)
# ============================================
CALENDLY_LINK = "https://calendly.com/dra-lethicia"
NOME_ESCRITORIO = "Dra. Lethícia Fernanda"
TELEFONE = "(11) 99999-9999"
EMAIL = "contato@dra-lethicia.adv.br"

# ============================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================
st.set_page_config(
    page_title="Iara Bot - Assistente Jurídica em Direito da Saúde",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
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
        max-height: 500px;
        overflow-y: auto;
        padding: 1rem;
        border: 1px solid #ddd;
        border-radius: 10px;
        background-color: #fafafa;
    }
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: bold;
    }
    .status-sus {
        background-color: #17a2b8;
        color: white;
    }
    .status-plano {
        background-color: #28a745;
        color: white;
    }
    .status-urgente {
        background-color: #dc3545;
        color: white;
    }
    .sidebar-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    hr {
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# GERENCIAMENTO DE ESTADO
# ============================================

def init_session_state():
    """Inicializa todas as variáveis de sessão"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "estado" not in st.session_state:
        st.session_state.estado = "INICIO"
    
    if "dados" not in st.session_state:
        st.session_state.dados = {}
    
    if "aguardando_resposta" not in st.session_state:
        st.session_state.aguardando_resposta = False

def add_bot_message(text: str):
    st.session_state.messages.append({
        "role": "bot",
        "content": text,
        "timestamp": datetime.now()
    })

def add_user_message(text: str):
    st.session_state.messages.append({
        "role": "user",
        "content": text,
        "timestamp": datetime.now()
    })

# ============================================
# LÓGICA DO FLUXO
# ============================================

def detectar_urgencia(dados: Dict) -> tuple:
    """Detecta se o caso é urgente"""
    especialidade = dados.get("especialidade", "")
    tempo_espera = dados.get("tempo_espera", "")
    urgente = dados.get("urgente", "")
    
    numeros = re.findall(r"\d+", str(tempo_espera))
    dias = int(numeros[0]) if numeros else 0
    
    if "oncologia" in especialidade.lower() and dias >= 60:
        return True, "⚠️ **URGENTE MÁXIMA**: Câncer + 60 dias sem tratamento (descumprimento da Lei 12.732/12)"
    elif "oncologia" in especialidade.lower():
        return True, "⚠️ **URGENTE**: Caso de oncologia - prazo de 60 dias deve ser respeitado"
    elif urgente == "SIM":
        return True, "⚠️ **URGENTE**: Caso classificado como urgente pelo médico"
    elif "tea" in especialidade.lower() or "tdah" in especialidade.lower():
        return True, "⚠️ **URGENTE**: Neurodivergência - desenvolvimento não pode esperar"
    
    return False, "✅ Caso em análise - vamos acompanhar"

def processar_resposta(resposta: str):
    """Processa a resposta baseado no estado atual"""
    estado = st.session_state.estado
    dados = st.session_state.dados
    
    if estado == "INICIO":
        dados["nome"] = resposta
        st.session_state.estado = "CANAL"
        add_bot_message(f"Prazer em conhecê-lo(a), {resposta}!\n\nSeu atendimento é pelo **SUS** ou **Plano de Saúde**?")
    
    elif estado == "CANAL":
        dados["canal"] = resposta.upper()
        st.session_state.estado = "CATEGORIA"
        add_bot_message(
            "Qual o tipo de demanda?\n\n"
            "🔴 **Cirurgia/Tratamento**\n"
            "📋 **Consulta/Exame**\n"
            "💊 **Medicamento**\n"
            "📄 **Benefício INSS/BPC**"
        )
    
    elif estado == "CATEGORIA":
        dados["categoria"] = resposta
        st.session_state.estado = "ESPECIALIDADE"
        
        if resposta == "Cirurgia/Tratamento":
            add_bot_message(
                "Qual especialidade?\n\n"
                "🔴 **Oncologia**\n"
                "🧠 **Neurodivergências (TEA/TDAH)**\n"
                "🩸 **Endometriose**\n"
                "⚖️ **Bariátrica**\n"
                "🔪 **Reparadora**\n"
                "❤️ **Cardiologia**\n"
                "📌 **Outro**"
            )
        elif resposta == "Consulta/Exame":
            add_bot_message(
                "Qual o objetivo?\n\n"
                "🔍 **Diagnóstico**\n"
                "📋 **Pré-operatório**\n"
                "✅ **Confirmação**"
            )
        elif resposta == "Medicamento":
            add_bot_message("Qual medicamento o médico indicou?")
        elif resposta == "Benefício INSS/BPC":
            add_bot_message(
                "Qual benefício?\n\n"
                "📄 **Auxílio-Doença**\n"
                "♿ **Aposentadoria Invalidez**\n"
                "👶 **BPC Deficiência**\n"
                "👴 **BPC Idoso**\n"
                "⚖️ **Recurso**"
            )
    
    elif estado == "ESPECIALIDADE":
        dados["especialidade"] = resposta
        st.session_state.estado = "DIAGNOSTICO"
        add_bot_message("Me conte mais sobre seu caso:\n\n- Diagnóstico?\n- Há quanto tempo aguarda?")
    
    elif estado == "DIAGNOSTICO":
        dados["diagnostico"] = resposta
        numeros = re.findall(r"\d+", resposta)
        if numeros:
            dados["tempo_espera"] = f"{numeros[0]} dias"
        
        if dados["canal"] == "SUS":
            st.session_state.estado = "TEMPO_ESPERA"
            add_bot_message("Há quanto tempo você está aguardando? (ex: 30 dias, 2 meses)")
        else:
            st.session_state.estado = "TEMPO_PLANO"
            add_bot_message("Você tem plano de saúde há mais de 2 anos? (SIM/NÃO)")
    
    elif estado == "TEMPO_ESPERA":
        dados["tempo_espera"] = resposta
        st.session_state.estado = "URGENCIA_MEDICA"
        add_bot_message("O médico falou que seu caso é URGENTE? (SIM/NÃO)")
    
    elif estado == "URGENCIA_MEDICA":
        dados["urgente"] = resposta.upper() == "SIM"
        eh_urgente, msg = detectar_urgencia(dados)
        dados["nivel_urgencia"] = "URGENTE" if eh_urgente else "NORMAL"
        
        add_bot_message(msg)
        st.session_state.estado = "PROPOSTA"
        
        add_bot_message(
            f"📊 **Analisando seu caso, {dados.get('nome')}...**\n\n"
            f"**Canal:** {dados['canal']}\n"
            f"**Categoria:** {dados.get('categoria')}\n"
            f"**Especialidade:** {dados.get('especialidade')}\n\n"
            "Trabalhamos com um **PROTOCOLO DE LIBERAÇÃO URGENTE**.\n\n"
            "**Deseja encaminhar seu caso para análise da Dra. Lethícia?**"
        )
        st.session_state.estado = "AGUARDANDO_RESPOSTA"
    
    elif estado == "TEMPO_PLANO":
        dados["tempo_plano"] = resposta
        st.session_state.estado = "PROPOSTA"
        add_bot_message(
            "⚠️ A lei é clara: planos de saúde não podem negar procedimentos urgentes.\n\n"
            "**Deseja que a Dra. Lethícia analise seu caso?**"
        )
        st.session_state.estado = "AGUARDANDO_RESPOSTA"
    
    elif estado == "AGUARDANDO_RESPOSTA":
        if resposta.upper() == "SIM":
            salvar_caso(dados)
            add_bot_message(
                f"✅ **ÓTIMO, {dados.get('nome')}!**\n\n"
                f"Devido à complexidade do seu caso, é necessária uma **REUNIÃO DE VIABILIDADE (15 min)**.\n\n"
                f"🔗 **Agende aqui:** {CALENDLY_LINK}\n\n"
                "Em breve entraremos em contato."
            )
            st.session_state.estado = "FINALIZADO"
        else:
            add_bot_message(
                f"Compreendo, {dados.get('nome')}.\n\n"
                "Infelizmente, sem ação judicial, seu caso continuará na fila.\n\n"
                "🙏 **Desejamos sorte no seu tratamento.**"
            )
            st.session_state.estado = "FINALIZADO"

def salvar_caso(dados: Dict):
    """Salva o caso em arquivo"""
    caso = {
        "timestamp": datetime.now().isoformat(),
        "dados": {k: str(v) for k, v in dados.items()}
    }
    try:
        with open("casos_iara_bot.json", "a", encoding="utf-8") as f:
            json.dump(caso, f, ensure_ascii=False)
            f.write("\n")
    except:
        pass  # Não crítico para o funcionamento

# ============================================
# INTERFACE
# ============================================

def render_sidebar():
    with st.sidebar:
        st.markdown(f"## ⚖️ {NOME_ESCRITORIO}")
        st.markdown("**Especialista em Direito da Saúde**")
        st.markdown("---")
        
        dados = st.session_state.dados
        
        if dados.get("nome"):
            st.markdown(f"**Cliente:** {dados['nome']}")
        if dados.get("canal"):
            st.markdown(f"**Canal:** {dados['canal']}")
        if dados.get("categoria"):
            st.markdown(f"**Categoria:** {dados['categoria']}")
        if dados.get("especialidade"):
            st.markdown(f"**Especialidade:** {dados['especialidade']}")
        if dados.get("nivel_urgencia") == "URGENTE":
            st.markdown("🚨 **Urgência Detectada**")
        
        st.markdown("---")
        st.markdown(f"📞 {TELEFONE}")
        st.markdown(f"📧 {EMAIL}")
        st.markdown("---")
        
        if st.button("🔄 Nova Conversa", use_container_width=True):
            st.session_state.clear()
            st.rerun()

def render_chat():
    with st.container():
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        for msg in st.session_state.messages:
            if msg["role"] == "bot":
                st.markdown(f'''
                <div class="chat-message bot-message">
                    <strong>🤖 Iara:</strong><br>{msg["content"]}
                </div>
                ''', unsafe_allow_html=True)
            else:
                nome = st.session_state.dados.get("nome", "Você")
                st.markdown(f'''
                <div class="chat-message user-message">
                    <strong>👤 {nome}:</strong><br>{msg["content"]}
                </div>
                ''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

def render_input():
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_input(
            "Digite sua mensagem:",
            key="user_input",
            disabled=st.session_state.get("estado") == "FINALIZADO",
            placeholder="Digite aqui sua resposta..."
        )
    
    with col2:
        send_button = st.button("📤 Enviar", disabled=st.session_state.get("estado") == "FINALIZADO", use_container_width=True)
    
    estado_atual = st.session_state.get("estado", "")
    
    if estado_atual in ["CANAL", "CATEGORIA", "ESPECIALIDADE"]:
        st.markdown("---")
        st.markdown("**🔘 Opções rápidas:**")
        
        opcoes = []
        if estado_atual == "CANAL":
            opcoes = ["SUS", "Plano de Saúde"]
        elif estado_atual == "CATEGORIA":
            opcoes = ["Cirurgia/Tratamento", "Consulta/Exame", "Medicamento", "Benefício INSS/BPC"]
        elif estado_atual == "ESPECIALIDADE":
            opcoes = ["Oncologia", "Neurodivergências (TEA/TDAH)", "Cardiologia", "Outro"]
        
        cols = st.columns(min(len(opcoes), 4))
        for i, opcao in enumerate(opcoes[:4]):
            with cols[i % 4]:
                if st.button(opcao, key=f"btn_{i}", use_container_width=True):
                    add_user_message(opcao)
                    processar_resposta(opcao)
                    st.rerun()
    
    if estado_atual in ["URGENCIA_MEDICA", "TEMPO_PLANO", "AGUARDANDO_RESPOSTA"]:
        st.markdown("---")
        col_sim, col_nao = st.columns(2)
        with col_sim:
            if st.button("✅ SIM", key="btn_sim", use_container_width=True):
                add_user_message("SIM")
                processar_resposta("SIM")
                st.rerun()
        with col_nao:
            if st.button("❌ NÃO", key="btn_nao", use_container_width=True):
                add_user_message("NÃO")
                processar_resposta("NÃO")
                st.rerun()
    
    if send_button and user_input:
        add_user_message(user_input)
        processar_resposta(user_input)
        st.rerun()

# ============================================
# MAIN
# ============================================

def main():
    st.title("⚖️ Iara Bot - Assistente Jurídica em Direito da Saúde")
    st.caption(f"{NOME_ESCRITORIO} | Atendimento SUS, Planos de Saúde e INSS")
    
    init_session_state()
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        render_chat()
        st.markdown("---")
        render_input()
    
    with col2:
        render_sidebar()
    
    if len(st.session_state.messages) == 0:
        add_bot_message(
            f"Olá! Sou a **Iara**, assistente jurídica do escritório da {NOME_ESCRITORIO}.\n\n"
            "Atendemos:\n"
            "🏥 **SUS** (cirurgias, consultas, exames, medicamentos)\n"
            "📋 **Planos de Saúde** (negativas, reajustes)\n"
            "📄 **INSS/BPC** (benefícios)\n\n"
            "**Qual é o seu nome?**"
        )
        st.rerun()

if __name__ == "__main__":
    main()
