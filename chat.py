"""
Iara Bot - Assistente Jurídica em Direito da Saúde
Versão com importação direta do flow.py
"""

import streamlit as st
import sys
import os
from datetime import datetime

# Adicionar o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importar do flow.py
from app.services.flow import ETAPAS, _sim, _nao
from app.config import get_settings

# Configurações
settings = get_settings()
L = settings.lawyer_name
CALENDLY_LINK = settings.calendly_link
PIX_KEY = settings.pix_key

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
    .sidebar-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .stButton button {
        background-color: #2c7be5;
        color: white;
        border-radius: 20px;
    }
    hr {
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# GERENCIAMENTO DE SESSÃO
# ============================================

def init_session_state():
    """Inicializa todas as variáveis de sessão"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "estado_atual" not in st.session_state:
        st.session_state.estado_atual = "INICIO"
    
    if "dados_coletados" not in st.session_state:
        st.session_state.dados_coletados = {}
    
    if "historico_respostas" not in st.session_state:
        st.session_state.historico_respostas = []
    
    if "nome_usuario" not in st.session_state:
        st.session_state.nome_usuario = None

def add_bot_message(text: str):
    """Adiciona mensagem do bot ao chat"""
    if not text:
        return
    
    # Substituir placeholders
    text = text.replace("{nome}", st.session_state.nome_usuario or "")
    text = text.replace("{lawyer}", L)
    text = text.replace("__PIX__", f"**Chave PIX:** `{PIX_KEY}`\n\n**Valor:** R$ {settings.consulta_valor:.2f}")
    text = text.replace("__AGUARDANDO__", "⏳ Aguardando confirmação de pagamento...")
    text = text.replace("__EMAIL__", "📧 Por favor, informe seu e-mail para envio do contrato:")
    text = text.replace("__HORARIO__", f"📅 Escolha o melhor horário na agenda:\n\n{CALENDLY_LINK}")
    
    st.session_state.messages.append({
        "role": "bot",
        "content": text,
        "timestamp": datetime.now()
    })

def add_user_message(text: str):
    """Adiciona mensagem do usuário ao chat"""
    st.session_state.messages.append({
        "role": "user",
        "content": text,
        "timestamp": datetime.now()
    })

def get_etapa(estado: str):
    """Recupera a etapa do ETAPAS"""
    return ETAPAS.get(estado)

def processar_resposta(resposta: str):
    """
    Processa a resposta do usuário e avança no fluxo
    """
    estado_atual = st.session_state.estado_atual
    etapa = get_etapa(estado_atual)
    
    if not etapa:
        # Fallback: reiniciar
        st.session_state.estado_atual = "INICIO"
        add_bot_message(ETAPAS["INICIO"].pergunta)
        return
    
    # Salvar nome se for início
    if estado_atual == "INICIO":
        st.session_state.nome_usuario = resposta
        st.session_state.dados_coletados["nome"] = resposta
    
    # Salvar resposta se tiver campo de salvamento
    if etapa.salvar_em:
        st.session_state.dados_coletados[etapa.salvar_em] = resposta
    
    # Registrar no histórico
    st.session_state.historico_respostas.append({
        "etapa": estado_atual,
        "resposta": resposta,
        "timestamp": datetime.now()
    })
    
    # Determinar próximo estado
    proximo_estado = None
    
    if etapa.proxima and etapa.proxima != "FIM":
        proximo_estado = etapa.proxima
    elif etapa.router:
        try:
            proximo_estado = etapa.router(resposta)
        except Exception as e:
            # Se router falhar, tentar proxima
            proximo_estado = etapa.proxima
    
    # Se não tem próximo e é um estado especial, apenas mostra resposta
    if not proximo_estado and etapa.pergunta in ["__PIX__", "__AGUARDANDO__", "__EMAIL__", "__HORARIO__"]:
        # Estados especiais - não mudar estado
        return
    
    # Atualizar estado
    if proximo_estado:
        st.session_state.estado_atual = proximo_estado
        proxima_etapa = get_etapa(proximo_estado)
        if proxima_etapa and proxima_etapa.pergunta:
            add_bot_message(proxima_etapa.pergunta)
    elif etapa.proxima == "FIM":
        st.session_state.estado_atual = "FIM"
    else:
        # Se não tem próximo, repetir pergunta
        add_bot_message(etapa.pergunta)

def reset_conversa():
    """Reinicia toda a conversa"""
    st.session_state.clear()
    init_session_state()
    add_bot_message(ETAPAS["INICIO"].pergunta)

# ============================================
# INTERFACE
# ============================================

def render_sidebar():
    """Renderiza a barra lateral com status"""
    with st.sidebar:
        st.markdown("## ⚖️ Iara Bot")
        st.markdown(f"**{L}**")
        st.markdown("*Especialista em Direito da Saúde*")
        st.markdown("---")
        
        st.markdown("### 📊 Status do Atendimento")
        
        if st.session_state.nome_usuario:
            st.markdown(f"**Cliente:** {st.session_state.nome_usuario}")
        
        if st.session_state.dados_coletados.get("canal"):
            st.markdown(f"**Canal:** {st.session_state.dados_coletados['canal']}")
        
        if st.session_state.dados_coletados.get("categoria"):
            st.markdown(f"**Categoria:** {st.session_state.dados_coletados['categoria']}")
        
        if st.session_state.dados_coletados.get("especialidade"):
            st.markdown(f"**Especialidade:** {st.session_state.dados_coletados['especialidade']}")
        
        if st.session_state.dados_coletados.get("resposta_final"):
            val = st.session_state.dados_coletados["resposta_final"]
            st.markdown(f"**Resposta:** {'✅ Aceitou' if 'sim' in val.lower() else '❌ Recusou'}")
        
        st.markdown("---")
        
        if len(st.session_state.dados_coletados) > 0:
            st.markdown("### 📋 Dados Coletados")
            for key, value in list(st.session_state.dados_coletados.items())[:8]:
                if key not in ["resposta_0", "resposta_1", "resposta_2", "resposta_3", "resposta_4"]:
                    if value and len(str(value)) < 50:
                        st.markdown(f"**{key}:** {str(value)[:40]}...")
        
        st.markdown("---")
        
        if st.button("🔄 Nova Conversa", use_container_width=True):
            reset_conversa()
            st.rerun()
        
        st.markdown("---")
        st.caption("💙 **Iara Bot v2.0**")
        st.caption("Protocolo de Liberação Urgente")

def render_chat():
    """Renderiza o container do chat"""
    with st.container():
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        for msg in st.session_state.messages:
            if msg["role"] == "bot":
                content = msg["content"]
                # Verificar se contém PIX ou link
                if "PIX" in content or "pix" in content:
                    st.markdown(f'<div class="chat-message bot-message"><strong>🤖 Iara:</strong></div>', unsafe_allow_html=True)
                    st.info(content)
                else:
                    st.markdown(f'''
                    <div class="chat-message bot-message">
                        <strong>🤖 Iara:</strong><br>{content}
                    </div>
                    ''', unsafe_allow_html=True)
            else:
                nome = st.session_state.nome_usuario or "Você"
                st.markdown(f'''
                <div class="chat-message user-message">
                    <strong>👤 {nome}:</strong><br>{msg["content"]}
                </div>
                ''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

def render_opcoes_rapidas():
    """Renderiza botões de opções rápidas baseado no estado atual"""
    estado_atual = st.session_state.estado_atual
    etapa = get_etapa(estado_atual)
    
    if not etapa or not etapa.opcoes:
        return
    
    # Não mostrar opções para estados especiais
    estados_especiais = ["PIX_APRESENTACAO", "AGUARDANDO_PAGAMENTO", "COLETAR_EMAIL", "ESCOLHER_HORARIO", "FIM"]
    if estado_atual in estados_especiais:
        st.markdown("---")
        if estado_atual == "PIX_APRESENTACAO":
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💰 Já paguei", use_container_width=True):
                    add_user_message("Já paguei")
                    st.session_state.estado_atual = "AGUARDANDO_PAGAMENTO"
                    add_bot_message("⏳ Aguardando confirmação de pagamento...")
                    st.rerun()
            with col2:
                if st.button("📋 Quero pagar agora", use_container_width=True):
                    add_user_message("Quero pagar")
                    st.markdown(f"""
                    <div style="background-color: #e8f5e9; padding: 1rem; border-radius: 10px; margin: 1rem 0;">
                        <strong>💳 Chave PIX:</strong><br>
                        <code style="font-size: 1.2rem;">{PIX_KEY}</code><br><br>
                        <strong>Valor:</strong> R$ {settings.consulta_valor:.2f}<br>
                        <strong>Beneficiário:</strong> {L}
                    </div>
                    """, unsafe_allow_html=True)
        
        elif estado_atual == "AGUARDANDO_PAGAMENTO":
            if st.button("✅ Confirmar pagamento", use_container_width=True):
                add_user_message("Confirmar pagamento")
                st.session_state.estado_atual = "COLETAR_EMAIL"
                add_bot_message("📧 Por favor, informe seu e-mail para envio do contrato:")
                st.rerun()
        
        elif estado_atual == "COLETAR_EMAIL":
            email = st.text_input("Digite seu e-mail:", key="email_input")
            if email and st.button("Enviar", use_container_width=True):
                add_user_message(email)
                st.session_state.dados_coletados["email"] = email
                st.session_state.estado_atual = "ESCOLHER_HORARIO"
                add_bot_message(f"📅 Escolha o melhor horário na agenda:\n\n{CALENDLY_LINK}")
                st.rerun()
        
        elif estado_atual == "ESCOLHER_HORARIO":
            st.markdown(f"[📅 Clique aqui para agendar]({CALENDLY_LINK})")
            if st.button("✅ Já agendei", use_container_width=True):
                add_user_message("Já agendei")
                st.session_state.estado_atual = "FIM"
                add_bot_message("Ótimo! Em breve a Dra. Lethícia entrará em contato. 💙")
                st.rerun()
        
        return
    
    st.markdown("---")
    st.markdown("**🔘 Opções rápidas:**")
    
    # Criar botões para as opções
    cols = st.columns(min(len(etapa.opcoes), 4))
    for i, opcao in enumerate(etapa.opcoes[:4]):
        with cols[i % 4]:
            btn_text = opcao if len(opcao) <= 25 else opcao[:22] + "..."
            if st.button(btn_text, key=f"opt_{estado_atual}_{i}", use_container_width=True):
                add_user_message(opcao)
                processar_resposta(opcao)
                st.rerun()

def render_input():
    """Renderiza o campo de input principal"""
    estado_atual = st.session_state.estado_atual
    
    if estado_atual == "FIM":
        st.info("✨ Atendimento finalizado. Clique em 'Nova Conversa' para recomeçar.")
        return
    
    if estado_atual in ["PIX_APRESENTACAO", "AGUARDANDO_PAGAMENTO", "COLETAR_EMAIL", "ESCOLHER_HORARIO"]:
        return
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_input(
            "Digite sua mensagem:",
            key="user_input",
            placeholder="Digite aqui sua resposta..."
        )
    
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
    st.caption(f"{L} | Atendimento SUS, Planos de Saúde e INSS")
    
    init_session_state()
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        render_chat()
        render_opcoes_rapidas()
        render_input()
    
    with col2:
        render_sidebar()
    
    # Mensagem inicial se não houver mensagens
    if len(st.session_state.messages) == 0:
        etapa_inicio = get_etapa("INICIO")
        if etapa_inicio:
            add_bot_message(etapa_inicio.pergunta)
            st.rerun()

if __name__ == "__main__":
    main()
