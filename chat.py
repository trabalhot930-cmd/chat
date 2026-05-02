"""
Iara Bot - Streamlit App
Versão que utiliza o flow.py como motor de estado
"""

import streamlit as st
import sys
import os
from datetime import datetime
from typing import Dict, Any

# Adicionar o diretório atual ao path para importar o app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importar o flow.py
from app.services.flow import ETAPAS, _sim, _nao, L

# ============================================
# CONFIGURAÇÕES
# ============================================
CALENDLY_LINK = "https://calendly.com/dra-lethicia"
PIX_KEY = "dra.lethicia@adv.br"  # Substituir pelo PIX real

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
    option-select {
        background-color: #2c7be5;
        color: white;
        padding: 0.5rem;
        border-radius: 5px;
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
    # Substituir placeholders
    text = text.replace("{nome}", st.session_state.nome_usuario or "")
    text = text.replace("{lawyer}", L)
    text = text.replace("__PIX__", f"**Chave PIX:** `{PIX_KEY}`")
    text = text.replace("__AGUARDANDO__", "⏳ Aguardando confirmação de pagamento...")
    text = text.replace("__EMAIL__", "📧 Por favor, informe seu e-mail para envio do contrato:")
    text = text.replace("__HORARIO__", "📅 Escolha o melhor horário na agenda:\n\n" + CALENDLY_LINK)
    
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

def processar_resposta(resposta: str, opcao_selecionada: str = None):
    """
    Processa a resposta do usuário e avança no fluxo
    """
    estado_atual = st.session_state.estado_atual
    etapa = get_etapa(estado_atual)
    
    if not etapa:
        # Fallback: reiniciar
        st.session_state.estado_atual = "INICIO"
        st.session_state.dados_coletados = {}
        add_bot_message("Vamos recomeçar? Qual o seu nome?")
        return
    
    # Usar opção selecionada se disponível
    if opcao_selecionada:
        resposta = opcao_selecionada
    
    # Salvar resposta se tiver campo de salvamento
    if etapa.salvar_em:
        st.session_state.dados_coletados[etapa.salvar_em] = resposta
    
    # Registrar no histórico
    st.session_state.historico_respostas.append({
        "etapa": estado_atual,
        "resposta": resposta,
        "timestamp": datetime.now()
    })
    
    # Caso especial: INICIO salva nome
    if estado_atual == "INICIO":
        st.session_state.nome_usuario = resposta
    
    # Determinar próximo estado
    proximo_estado = None
    
    if etapa.proxima:
        proximo_estado = etapa.proxima
    elif etapa.router:
        proximo_estado = etapa.router(resposta)
    elif etapa.opcoes:
        # Se tem opções mas não router, procurar match
        for i, opcao in enumerate(etapa.opcoes):
            if resposta == opcao or resposta == str(i+1):
                # Tentar encontrar próximo baseado no índice
                pass
        if not proximo_estado:
            proximo_estado = None
    
    # Atualizar estado
    if proximo_estado:
        st.session_state.estado_atual = proximo_estado
        proxima_etapa = get_etapa(proximo_estado)
        if proxima_etapa:
            add_bot_message(proxima_etapa.pergunta)
    else:
        # Se não tem próximo, está finalizado
        if estado_atual == "FIM":
            pass  # Já finalizado
        elif etapa.pergunta and etapa.pergunta not in ["__PIX__", "__AGUARDANDO__", "__EMAIL__", "__HORARIO__"]:
            # Repetir a pergunta
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
        st.image("https://via.placeholder.com/300x80?text=Iara+Bot", use_container_width=True)
        
        st.markdown("## ⚖️ Assistente Jurídica")
        st.markdown(f"**{L}**")
        st.markdown("*Especialista em Direito da Saúde*")
        st.markdown("---")
        
        st.markdown("### 📊 Status do Atendimento")
        
        if st.session_state.nome_usuario:
            st.markdown(f"**Cliente:** {st.session_state.nome_usuario}")
        
        if st.session_state.dados_coletados.get("canal"):
            canal = st.session_state.dados_coletados["canal"]
            st.markdown(f"**Canal:** {canal}")
        
        if st.session_state.dados_coletados.get("categoria"):
            st.markdown(f"**Categoria:** {st.session_state.dados_coletados['categoria']}")
        
        if st.session_state.dados_coletados.get("especialidade"):
            st.markdown(f"**Especialidade:** {st.session_state.dados_coletados['especialidade']}")
        
        if st.session_state.dados_coletados.get("resposta_final"):
            st.markdown(f"**Resposta Final:** {st.session_state.dados_coletados['resposta_final']}")
        
        st.markdown("---")
        
        # Informações coletadas (resumo)
        st.markdown("### 📋 Dados Coletados")
        dados = st.session_state.dados_coletados
        if dados:
            for key, value in list(dados.items())[:5]:  # Mostrar apenas 5 primeiros
                if value and key not in ["resposta_0", "resposta_1", "resposta_2", "resposta_3", "resposta_4"]:
                    st.markdown(f"**{key}:** {str(value)[:50]}...")
        
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
                # Verificar se é mensagem especial
                content = msg["content"]
                if "__PIX__" in content or "__HORARIO__" in content or "__EMAIL__" in content:
                    # Mensagem formatada
                    st.markdown(f'''
                    <div class="chat-message bot-message">
                        <strong>🤖 Iara:</strong>
                    </div>
                    ''', unsafe_allow_html=True)
                    st.markdown(content)
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
    if estado_atual in ["AGUARDANDO_PAGAMENTO", "FIM", "PIX_APRESENTACAO", "COLETAR_EMAIL", "ESCOLHER_HORARIO"]:
        return
    
    st.markdown("---")
    st.markdown("**🔘 Opções rápidas:**")
    
    # Criar botões para as opções
    cols = st.columns(min(len(etapa.opcoes), 4))
    for i, opcao in enumerate(etapa.opcoes[:4]):
        with cols[i % 4]:
            # Limpar texto da opção para botão
            btn_text = opcao
            if len(btn_text) > 25:
                btn_text = btn_text[:22] + "..."
            
            if st.button(btn_text, key=f"opt_{estado_atual}_{i}", use_container_width=True):
                add_user_message(opcao)
                processar_resposta(opcao)
                st.rerun()

def render_input():
    """Renderiza o campo de input principal"""
    estado_atual = st.session_state.estado_atual
    etapa = get_etapa(estado_atual)
    
    # Verificar se é um estado final
    if estado_atual in ["FIM", "AGUARDANDO_PAGAMENTO"]:
        st.info("✨ Atendimento finalizado. Clique em 'Nova Conversa' para recomeçar.")
        return
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_input(
            "Digite sua mensagem:",
            key="user_input",
            placeholder="Digite aqui sua resposta..." if not etapa or not etapa.opcoes else "Ou clique nas opções acima...",
            disabled=estado_atual == "FIM"
        )
    
    with col2:
        send_button = st.button("📤 Enviar", disabled=estado_atual == "FIM", use_container_width=True)
    
    # Botões SIM/NÃO para estados que precisam
    if etapa and etapa.opcoes and len(etapa.opcoes) == 2 and \
       any(p in str(etapa.opcoes).lower() for p in ["sim", "não", "nao"]):
        st.markdown("---")
        col_sim, col_nao = st.columns(2)
        with col_sim:
            if st.button("✅ SIM", key="btn_sim", use_container_width=True):
                add_user_message("Sim")
                processar_resposta("Sim")
                st.rerun()
        with col_nao:
            if st.button("❌ NÃO", key="btn_nao", use_container_width=True):
                add_user_message("Não")
                processar_resposta("Não")
                st.rerun()
    
    # Botões de resposta específicos para PIX e agendamento
    if estado_atual == "PIX_APRESENTACAO":
        st.markdown("---")
        col_pago, col_pagar = st.columns(2)
        with col_pago:
            if st.button("💰 Já paguei", use_container_width=True):
                add_user_message("Já paguei")
                st.session_state.estado_atual = "AGUARDANDO_PAGAMENTO"
                st.rerun()
        with col_pagar:
            if st.button("🏦 Quero pagar agora", use_container_width=True):
                add_user_message("Quero pagar")
                st.markdown(f"""
                <div style="background-color: #e8f5e9; padding: 1rem; border-radius: 10px; margin: 1rem 0;">
                    <strong>💳 Chave PIX:</strong><br>
                    <code style="font-size: 1.2rem;">{PIX_KEY}</code><br><br>
                    <strong>Valor:</strong> R$ 97,00<br>
                    <strong>Beneficiário:</strong> {L}
                </div>
                """, unsafe_allow_html=True)
    
    if estado_atual == "AGUARDANDO_PAGAMENTO":
        st.markdown("---")
        if st.button("✅ Confirmar pagamento", use_container_width=True):
            add_user_message("Confirmar pagamento")
            st.session_state.estado_atual = "COLETAR_EMAIL"
            add_bot_message(ETAPAS["COLETAR_EMAIL"].pergunta)
            st.rerun()
    
    if estado_atual == "COLETAR_EMAIL":
        email_input = st.text_input("Digite seu e-mail:", key="email_input")
        if email_input and st.button("Enviar e-mail", use_container_width=True):
            add_user_message(email_input)
            st.session_state.dados_coletados["email"] = email_input
            st.session_state.estado_atual = "ESCOLHER_HORARIO"
            add_bot_message(ETAPAS["ESCOLHER_HORARIO"].pergunta)
            st.rerun()
    
    if estado_atual == "ESCOLHER_HORARIO":
        st.markdown(f"""
        <div style="background-color: #e3f2fd; padding: 1rem; border-radius: 10px; margin: 1rem 0;">
            <strong>📅 Agende sua reunião:</strong><br>
            <a href="{CALENDLY_LINK}" target="_blank" style="background-color: #2c7be5; color: white; 
            padding: 0.5rem 1rem; text-decoration: none; border-radius: 5px; display: inline-block;">
                Clique aqui para agendar
            </a>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("✅ Já agendei", use_container_width=True):
            add_user_message("Já agendei")
            st.session_state.estado_atual = "FIM"
            add_bot_message("Ótimo! Em breve a Dra. Lethícia entrará em contato. 💙")
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
