import streamlit as st
import json
import re
from datetime import datetime
from typing import Dict, List, Optional

# Configuração da página
st.set_page_config(
    page_title="Lara Bot - Assistente Jurídica",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CSS PERSONALIZADO (estilo WhatsApp)
# ============================================
st.markdown("""
<style>
    /* Estilo do chat */
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
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
    .botao-opcao {
        background-color: #2c7be5;
        color: white;
        padding: 0.5rem 1rem;
        margin: 0.2rem;
        border-radius: 20px;
        display: inline-block;
        cursor: pointer;
        text-align: center;
        border: none;
        font-size: 0.9rem;
    }
    .botao-opcao:hover {
        background-color: #1c5bb5;
    }
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: bold;
    }
    .status-urgente {
        background-color: #dc3545;
        color: white;
    }
    .status-atendimento {
        background-color: #28a745;
        color: white;
    }
    .sidebar-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
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
    
    if "fluxo_atual" not in st.session_state:
        st.session_state.fluxo_atual = "boas_vindas"
    
    if "dados_usuario" not in st.session_state:
        st.session_state.dados_usuario = {}
    
    if "aguardando_resposta" not in st.session_state:
        st.session_state.aguardando_resposta = False
    
    if "ultimo_botao" not in st.session_state:
        st.session_state.ultimo_botao = None

# ============================================
# FUNÇÕES DO BOT
# ============================================

def add_bot_message(text: str):
    """Adiciona mensagem do bot ao chat"""
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

def verificar_urgencia() -> tuple[bool, str]:
    """Verifica se o caso tem urgência"""
    dados = st.session_state.dados_usuario
    tempo_espera = dados.get('tempo_espera', '')
    urgente = dados.get('urgente', '')
    especialidade = dados.get('especialidade', '')
    
    # Extrair números do tempo de espera
    numeros = re.findall(r'\d+', str(tempo_espera))
    dias_espera = int(numeros[0]) if numeros else 0
    
    if especialidade == "Oncologia" and dias_espera >= 60:
        return True, "⚠️ URGENTE: Câncer + 60 dias sem tratamento (descumprimento da lei)"
    elif urgente == "SIM":
        return True, "⚠️ URGENTE: Caso classificado como urgente pelo médico"
    elif especialidade == "Neurodivergências":
        return True, "⚠️ URGENTE: Neurodivergência - desenvolvimento não pode esperar"
    elif "cirurgia" in str(dados.get('relato', '')).lower():
        return True, "⚠️ URGENTE: Aguardando cirurgia"
    
    return False, "✅ Caso em análise - aguardando informações"

def processar_resposta(resposta: str, opcao_selecionada: str = None):
    """Processa a resposta do usuário baseado no fluxo atual"""
    fluxo = st.session_state.fluxo_atual
    dados = st.session_state.dados_usuario
    
    # Se veio de botão, usa a opção
    if opcao_selecionada:
        resposta = opcao_selecionada
    
    # ========== FLUXO 1: BOAS-VINDAS ==========
    if fluxo == "boas_vindas":
        dados['nome'] = resposta
        st.session_state.fluxo_atual = "tipo_atendimento"
        add_bot_message(f"Olá {resposta}! Seu atendimento é pelo **SUS** ou **Plano de Saúde**?")
    
    # ========== FLUXO 2: TIPO ATENDIMENTO ==========
    elif fluxo == "tipo_atendimento":
        dados['tipo_atendimento'] = resposta
        if resposta == "SUS":
            st.session_state.fluxo_atual = "especialidade_sus"
            add_bot_message("Qual problema estamos enfrentando hoje?\n\n"
                          "🔴 **Oncologia**\n"
                          "🧠 **Neurodivergências (TEA, TDAH)**\n"
                          "🩸 **Endometriose / Adenomiose**\n"
                          "💊 **Medicamento**\n"
                          "⚖️ **Bariátrica**\n"
                          "🔪 **Reparadora**\n"
                          "❤️ **Cardiologia**\n"
                          "📋 **Consultas / Exames**\n"
                          "📌 **Outros**")
        else:
            st.session_state.fluxo_atual = "tempo_plano"
            add_bot_message("Você já tem seu plano de saúde há mais de **2 anos**?\n\nResponda: **SIM** ou **NÃO**")
    
    # ========== FLUXO 3: ESPECIALIDADE SUS ==========
    elif fluxo == "especialidade_sus":
        dados['especialidade'] = resposta
        
        if resposta == "Oncologia":
            st.session_state.fluxo_atual = "coleta_oncologia"
            add_bot_message("⚠️ **ENTENDI. Vamos cuidar disso juntos.**\n\n"
                          "Precisamos de algumas informações:\n\n"
                          "1️⃣ **Qual o tipo de câncer?**\n"
                          "2️⃣ **Há quanto tempo aguarda tratamento pelo SUS?**\n"
                          "3️⃣ **O diagnóstico foi confirmado por biópsia?**\n"
                          "4️⃣ **O médico falou que é urgente?**\n\n"
                          "Por favor, me explique sua situação:")
        elif resposta == "Neurodivergências (TEA, TDAH)":
            st.session_state.fluxo_atual = "coleta_neuro"
            add_bot_message("🧠 **ENTENDI. Neurodivergências exigem atenção imediata.**\n\n"
                          "Me conte:\n"
                          "- Já tem diagnóstico fechado?\n"
                          "- Quais terapias o médico indicou?\n"
                          "- Está aguardando há quanto tempo?\n"
                          "- O médico falou sobre prejuízo no desenvolvimento?")
        elif resposta == "Consultas / Exames":
            st.session_state.fluxo_atual = "coleta_consultas"
            add_bot_message("📋 **ENTENDI. Consultas e exames no SUS.**\n\n"
                          "Me informe:\n"
                          "- Qual especialidade médica?\n"
                          "- Há quanto tempo aguarda?\n"
                          "- Tem encaminhamento médico?\n"
                          "- Já tentou marcar pelo App Meu SUS Digital?")
        else:
            st.session_state.fluxo_atual = "coleta_generica"
            add_bot_message(f"Me conte mais sobre seu caso de **{resposta}** para que eu possa ajudar:\n\n"
                          "- Qual o diagnóstico?\n"
                          "- Há quanto tempo aguarda?\n"
                          "- O médico falou em urgência?\n"
                          "- Tem laudo e comprovante de fila?")
    
    # ========== FLUXO 4: TEMPO PLANO ==========
    elif fluxo == "tempo_plano":
        dados['tempo_plano_2anos'] = resposta.upper() == "SIM"
        st.session_state.fluxo_atual = "situacao_plano"
        add_bot_message("Qual a situação com o plano de saúde?\n\n"
                      "🚫 **Negativa de cirurgia**\n"
                      "💊 **Medicamento negado**\n"
                      "🔬 **Exame negado**\n"
                      "🏠 **Home care**\n"
                      "🧠 **Terapias (fono, ABA, fisio...)**\n"
                      "📈 **Reajuste abusivo**\n\n"
                      "Digite a opção:")
    
    # ========== FLUXO 5: SITUAÇÃO PLANO ==========
    elif fluxo == "situacao_plano":
        dados['situacao_plano'] = resposta
        st.session_state.fluxo_atual = "aguardando_proposta_plano"
        
        add_bot_message("⚠️ **A lei é clara:** se há urgência ou o procedimento está no Rol da ANS, "
                      "o plano **NÃO pode negar**.\n\n"
                      "Mesmo fora do rol, com laudo médico justificando, é possível conseguir liminar.\n\n"
                      "A Dra. Lethícia pode entrar com ação imediata para liberar seu procedimento em **até 48h**.\n\n"
                      "**Deseja encaminhar seu caso para análise da Dra. Lethícia?**")
        
        st.session_state.aguardando_resposta = True
    
    # ========== COLETA ONCOLOGIA ==========
    elif fluxo == "coleta_oncologia":
        dados['relato_oncologia'] = resposta
        
        # Detectar urgência automaticamente
        if "urgente" in resposta.lower() or "60" in resposta:
            dados['urgente'] = "SIM"
        
        st.session_state.fluxo_atual = "proposta_judicial"
        
        # Verificar tempo de espera
        numeros = re.findall(r'\d+', resposta)
        if numeros and int(numeros[0]) >= 60:
            add_bot_message("⚠️ **ALERTA LEGAL:** Se o hospital não iniciou seu tratamento em 60 dias, "
                          "a lei está sendo **descumprida**.\n\n"
                          "Precisamos forçar o início imediato via Justiça.")
        
        add_bot_message("✅ **Informações recebidas!**\n\n"
                      "Agora, me diga: **você possui comprovante de que está na fila do SUS?**\n"
                      "(App Meu SUS Digital, SISREG, comprovante da Secretaria de Saúde)")
        
        st.session_state.fluxo_atual = "aguardando_comprovante"
    
    # ========== AGUARDANDO COMPROVANTE ==========
    elif fluxo == "aguardando_comprovante":
        dados['tem_comprovante'] = resposta.upper() == "SIM"
        
        eh_urgente, msg_urgencia = verificar_urgencia()
        dados['status_urgencia'] = eh_urgente
        dados['msg_urgencia'] = msg_urgencia
        
        if eh_urgente:
            add_bot_message(msg_urgencia)
        
        st.session_state.fluxo_atual = "proposta_judicial"
        
        add_bot_message(f"📊 **Analisando seu caso...**\n\n"
                      f"**Nome:** {dados.get('nome')}\n"
                      f"**Especialidade:** {dados.get('especialidade')}\n"
                      f"**Status:** {msg_urgencia}\n\n"
                      "No SUS, o governo muitas vezes usa a fila da regulação para camuflar a falta de investimento.\n\n"
                      "Para resolver isso, trabalho com um **PROTOCOLO DE LIBERAÇÃO URGENTE**.\n\n"
                      "**Isso faria diferença na sua vida agora?**")
        
        st.session_state.aguardando_resposta = True
    
    # ========== PROPOSTA JUDICIAL ==========
    elif fluxo == "proposta_judicial" or fluxo == "aguardando_proposta_plano":
        dados['aceitou_proposta'] = resposta.upper() == "SIM"
        
        if resposta.upper() == "SIM":
            add_bot_message("✅ **ÓTIMO!** Isso mostra que você prioriza sua saúde acima da burocracia do Estado.\n\n"
                          "Devido à alta complexidade do seu caso, a Dra. Lethícia definiu que é necessária uma "
                          "**REUNIÃO DE VIABILIDADE POR VÍDEO (15 minutos)**.\n\n"
                          "Nessa conversa, ela vai:\n"
                          "✅ Validar sua documentação\n"
                          "✅ Apresentar o plano de ação\n"
                          "✅ Informar os valores de honorários\n\n"
                          "🔗 **Agende o melhor horário:** [LINK DA SUA AGENDA AQUI]\n\n"
                          "Em breve entraremos em contato para confirmar.")
            
            # Salvar caso
            salvar_caso_demo()
            
            st.session_state.fluxo_atual = "finalizado"
        else:
            add_bot_message(f"Compreendo, {dados.get('nome')}.\n\n"
                          "Infelizmente, sem ação judicial, seu caso continuará na fila do SUS, **sem previsão**.\n\n"
                          "Como nosso escritório foca apenas em quem deseja solução imediata, encerramos aqui.\n\n"
                          "Caso mude de ideia, estamos à disposição.\n\n"
                          "🙏 **Desejamos sorte no seu tratamento.**")
            
            st.session_state.fluxo_atual = "finalizado"
    
    # ========== FLUXO GENÉRICO ==========
    elif fluxo == "coleta_generica" or fluxo == "coleta_neuro" or fluxo == "coleta_consultas":
        dados['relato'] = resposta
        st.session_state.fluxo_atual = "aguardando_comprovante"
        
        add_bot_message("✅ **Recebi seu relato.**\n\n"
                      "Você possui comprovante de que está aguardando na fila do SUS?\n"
                      "(App Meu SUS Digital, SISREG, comprovante da Secretaria)")
    
    elif fluxo == "finalizado":
        add_bot_message("Atendimento encerrado. Caso precise, inicie uma nova conversa recarregando a página.")
    
    # Resetar estado de aguardando resposta
    st.session_state.aguardando_resposta = False

def salvar_caso_demo():
    """Salva o caso para demonstração"""
    caso = {
        "timestamp": datetime.now().isoformat(),
        "dados": st.session_state.dados_usuario
    }
    
    # Salvar em arquivo para demonstração
    with open("casos_demo.json", "a", encoding="utf-8") as f:
        json.dump(caso, f, ensure_ascii=False)
        f.write("\n")

def render_chat():
    """Renderiza o chat com todas as mensagens"""
    chat_container = st.container()
    
    with chat_container:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        for msg in st.session_state.messages:
            if msg["role"] == "bot":
                st.markdown(f'''
                <div class="chat-message bot-message">
                    <strong>🤖 Lara:</strong><br>{msg["content"]}
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="chat-message user-message">
                    <strong>👤 Você:</strong><br>{msg["content"]}
                </div>
                ''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

def render_input():
    """Renderiza o campo de input e botões"""
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_input(
            "Digite sua mensagem:",
            key="user_input",
            disabled=st.session_state.get("fluxo_atual") == "finalizado",
            placeholder="Digite aqui sua resposta..."
        )
    
    with col2:
        send_button = st.button(
            "📤 Enviar",
            disabled=st.session_state.get("fluxo_atual") == "finalizado",
            use_container_width=True
        )
    
    # Botões rápidos para opções comuns
    if st.session_state.get("fluxo_atual") in ["tipo_atendimento", "especialidade_sus", "situacao_plano"]:
        st.markdown("---")
        st.markdown("**Opções rápidas:**")
        
        opcoes_cols = st.columns(4)
        
        if st.session_state.fluxo_atual == "tipo_atendimento":
            with opcoes_cols[0]:
                if st.button("🏥 SUS", key="btn_sus", use_container_width=True):
                    processar_resposta("", "SUS")
                    st.rerun()
            with opcoes_cols[1]:
                if st.button("📋 Plano de Saúde", key="btn_plano", use_container_width=True):
                    processar_resposta("", "Plano de Saúde")
                    st.rerun()
        
        elif st.session_state.fluxo_atual == "especialidade_sus":
            opcoes = ["Oncologia", "Neurodivergências", "Consultas/Exames", "Medicamento"]
            for i, opcao in enumerate(opcoes):
                with opcoes_cols[i]:
                    if st.button(opcao, key=f"btn_esp_{i}", use_container_width=True):
                        processar_resposta("", opcao)
                        st.rerun()
        
        elif st.session_state.fluxo_atual == "situacao_plano":
            opcoes = ["Negativa de cirurgia", "Medicamento negado", "Exame negado", "Terapias"]
            for i, opcao in enumerate(opcoes):
                with opcoes_cols[i]:
                    if st.button(opcao, key=f"btn_plan_{i}", use_container_width=True):
                        processar_resposta("", opcao)
                        st.rerun()
    
    # Botões SIM/NÃO para propostas
    if st.session_state.get("aguardando_resposta", False):
        st.markdown("---")
        st.markdown("**Escolha uma opção:**")
        
        col_sim, col_nao = st.columns(2)
        with col_sim:
            if st.button("✅ SIM, quero resolver", key="btn_sim", use_container_width=True):
                processar_resposta("", "SIM")
                st.rerun()
        with col_nao:
            if st.button("❌ NÃO, continuar na fila", key="btn_nao", use_container_width=True):
                processar_resposta("", "NÃO")
                st.rerun()
    
    if send_button and user_input:
        add_user_message(user_input)
        processar_resposta(user_input)
        st.rerun()

def render_sidebar():
    """Renderiza a barra lateral com informações"""
    with st.sidebar:
        st.image("https://via.placeholder.com/300x100?text=Dra.+Leth%C3%ADcia+Fernanda", use_container_width=True)
        
        st.markdown("## ⚖️ Dra. Lethícia Fernanda")
        st.markdown("**Especialista em Direito da Saúde**")
        st.markdown("---")
        
        # Status do atendimento
        st.markdown("### 📊 Status do Atendimento")
        
        dados = st.session_state.dados_usuario
        
        if dados.get('nome'):
            st.markdown(f"**Cliente:** {dados.get('nome')}")
        if dados.get('tipo_atendimento'):
            st.markdown(f"**Tipo:** {dados.get('tipo_atendimento')}")
        if dados.get('especialidade'):
            st.markdown(f"**Especialidade:** {dados.get('especialidade')}")
        if dados.get('status_urgencia'):
            if dados.get('status_urgencia'):
                st.markdown(f"**⚠️ Urgência detectada**")
            else:
                st.markdown(f"**✅ Sem urgência aparente**")
        
        st.markdown("---")
        
        # Informações do escritório
        st.markdown("### 📍 Contato")
        st.markdown("""
        - 📞 (11) 99999-9999
        - 📧 contato@dra-lethicia.adv.br
        - 📍 São Paulo - SP
        """)
        
        st.markdown("---")
        
        # Botão de reset
        if st.button("🔄 Nova Conversa", use_container_width=True):
            st.session_state.clear()
            st.rerun()
        
        st.markdown("---")
        st.caption("⚖️ **Protocolo de Liberação Urgente**")
        st.caption("© 2026 - Todos os direitos reservados")

# ============================================
# MAIN
# ============================================

def main():
    # Título principal
    st.title("⚖️ Lara - Assistente Jurídica em Direito da Saúde")
    st.caption("Dra. Lethícia Fernanda | Especialista em Direito da Saúde")
    
    # Inicializar sessão
    init_session_state()
    
    # Layout de duas colunas
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Chat container
        render_chat()
        
        st.markdown("---")
        
        # Input container
        render_input()
    
    with col2:
        render_sidebar()
    
    # Mensagem inicial se não houver mensagens
    if len(st.session_state.messages) == 0:
        add_bot_message("Olá! Sou a Lara, assistente jurídica do escritório da Dra. Lethícia Fernanda, advogada especialista em Direito da Saúde.\n\n"
                       "Fico feliz que você entrou em contato conosco.\n\n"
                       "**Qual é o seu nome?**")
        st.rerun()

if __name__ == "__main__":
    main()
