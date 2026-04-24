import streamlit as st
import re
import json
from datetime import datetime
from typing import Dict, Tuple
import os
from dotenv import load_dotenv

load_dotenv()

# Configuração da página
st.set_page_config(
    page_title="Iara Bot - Assistente Jurídica em Direito da Saúde",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CONFIGURAÇÕES
# ============================================
CALENDLY_LINK = os.getenv("CALENDLY_LINK", "https://calendly.com/dra-lethicia")
NOME_ESCRITORIO = os.getenv("ESCRITORIO_NOME", "Dra. Lethícia Fernanda")
TELEFONE = os.getenv("ESCRITORIO_TELEFONE", "(11) 99999-9999")

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
    .opcao-botao {
        background-color: #2c7be5;
        color: white;
        padding: 0.5rem 1rem;
        margin: 0.25rem;
        border-radius: 20px;
        display: inline-block;
        cursor: pointer;
        text-align: center;
        font-size: 0.85rem;
        border: none;
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
    
    if "ultima_pergunta" not in st.session_state:
        st.session_state.ultima_pergunta = ""

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
# LÓGICA DO FLUXO (SUS + PLANO + INSS)
# ============================================

def detectar_urgencia(dados: Dict) -> Tuple[bool, str]:
    """Detecta se o caso é urgente"""
    especialidade = dados.get("especialidade", "")
    tempo_espera = dados.get("tempo_espera", "")
    urgente = dados.get("urgente", "")
    
    # Extrair números
    numeros = re.findall(r"\d+", str(tempo_espera))
    dias = int(numeros[0]) if numeros else 0
    
    if "oncologia" in especialidade.lower() and dias >= 60:
        return True, "⚠️ **URGENTE MÁXIMA**: Câncer + 60 dias sem tratamento (descumprimento da Lei 12.732/12)"
    elif "oncologia" in especialidade.lower():
        return True, "⚠️ **URGENTE**: Caso de oncologia - prazo de 60 dias deve ser respeitado"
    elif urgente == "SIM":
        return True, "⚠️ **URGENTE**: Caso classificado como urgente pelo médico"
    elif "tea" in especialidade.lower() or "tda" in especialidade.lower() or "neurodiv" in especialidade.lower():
        return True, "⚠️ **URGENTE**: Neurodivergência - desenvolvimento não pode esperar"
    elif "cirurgia" in str(dados.get("categoria", "")).lower():
        return True, "⚠️ **ATENÇÃO**: Aguardando cirurgia - risco de agravamento"
    
    return False, "✅ Caso em análise - vamos acompanhar"

def processar_resposta(resposta: str):
    """Processa a resposta baseado no estado atual"""
    estado = st.session_state.estado
    dados = st.session_state.dados
    
    # ========== FLUXO PRINCIPAL ==========
    
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
                "🦴 **Ortopedia**\n"
                "📌 **Outro**"
            )
        elif resposta == "Consulta/Exame":
            add_bot_message(
                "Qual o objetivo do exame/consulta?\n\n"
                "🔍 **Diagnóstico** (descobrir o que tenho)\n"
                "📋 **Pré-operatório** (para cirurgia)\n"
                "✅ **Confirmação** (médico suspeita e precisa confirmar)"
            )
        elif resposta == "Medicamento":
            add_bot_message("Qual medicamento o médico indicou?")
        elif resposta == "Benefício INSS/BPC":
            add_bot_message(
                "Qual benefício você deseja solicitar?\n\n"
                "📄 **Auxílio-Doença**\n"
                "♿ **Aposentadoria por Invalidez**\n"
                "👶 **BPC Deficiência**\n"
                "👴 **BPC Idoso**\n"
                "💔 **Pensão por Morte**\n"
                "⚖️ **Recurso de negativa**"
            )
    
    elif estado == "ESPECIALIDADE":
        dados["especialidade"] = resposta
        st.session_state.estado = "DIAGNOSTICO"
        add_bot_message("Me conte mais sobre seu caso:\n\n- Qual o diagnóstico completo?\n- Há quanto tempo aguarda?\n- Já fez algum tratamento?")
    
    elif estado == "DIAGNOSTICO":
        dados["diagnostico"] = resposta
        
        # Extrair tempo de espera se mencionado
        numeros = re.findall(r"\d+", resposta)
        if numeros:
            dados["tempo_espera"] = f"{numeros[0]} dias"
        
        st.session_state.estado = "TEMPO_ESPERA" if dados["canal"] == "SUS" else "TEMPO_PLANO"
        
        if dados["canal"] == "SUS":
            add_bot_message("Há quanto tempo você está aguardando pelo SUS? (ex: 30 dias, 2 meses)")
        else:
            add_bot_message("Você tem plano de saúde há mais de 2 anos? (SIM/NÃO)")
    
    elif estado == "TEMPO_ESPERA":
        dados["tempo_espera"] = resposta
        st.session_state.estado = "LAUDO"
        add_bot_message("Você possui laudo ou relatório médico? (SIM/NÃO)")
    
    elif estado == "LAUDO":
        dados["tem_laudo"] = resposta.upper() == "SIM"
        st.session_state.estado = "COMPROVANTE"
        add_bot_message("Você possui comprovante de que está na fila do SUS?\n(SIM/NÃO)\n\nPode ser App Meu SUS Digital, SISREG ou comprovante da Secretaria.")
    
    elif estado == "COMPROVANTE":
        dados["tem_comprovante"] = resposta.upper() == "SIM"
        st.session_state.estado = "URGENCIA"
        add_bot_message("O médico falou que seu caso é URGENTE? (SIM/NÃO)")
    
    elif estado == "URGENCIA":
        dados["urgente"] = resposta.upper() == "SIM"
        
        # Verificar urgência
        eh_urgente, msg_urgencia = detectar_urgencia(dados)
        dados["nivel_urgencia"] = "URGENTE" if eh_urgente else "NORMAL"
        
        add_bot_message(msg_urgencia)
        
        st.session_state.estado = "PROPOSTA"
        
        # Mensagem da proposta
        if dados["canal"] == "SUS":
            add_bot_message(
                f"📊 **Analisando seu caso, {dados.get('nome')}...**\n\n"
                f"**Canal:** {dados['canal']}\n"
                f"**Categoria:** {dados.get('categoria')}\n"
                f"**Especialidade:** {dados.get('especialidade')}\n"
                f"**Tempo de espera:** {dados.get('tempo_espera', 'Não informado')}\n\n"
                "O SUS trata sua demanda como se pudesse esperar, mas juridicamente o tempo é seu inimigo.\n\n"
                "Trabalhamos com um **PROTOCOLO DE LIBERAÇÃO URGENTE** que força o governo a cumprir a lei.\n\n"
                "**Isso faria diferença na sua vida agora?**"
            )
        else:
            add_bot_message(
                f"📊 **Analisando seu caso, {dados.get('nome')}...**\n\n"
                f"**Canal:** {dados['canal']}\n"
                f"**Situação:** {dados.get('especialidade')}\n\n"
                "A lei é clara: se há urgência ou o procedimento está no Rol da ANS, o plano **NÃO pode negar**.\n\n"
                "A Dra. Lethícia pode entrar com ação imediata para liberar seu procedimento em **até 48h**.\n\n"
                "**Deseja encaminhar seu caso para análise?**"
            )
        
        st.session_state.estado = "AGUARDANDO_RESPOSTA"
    
    elif estado == "TEMPO_PLANO":
        dados["tempo_plano_2anos"] = resposta.upper() == "SIM"
        st.session_state.estado = "JUSTIFICATIVA"
        add_bot_message(
            "Qual foi a justificativa do plano para negar?\n\n"
            "1️⃣ **Carência** (tempo de espera)\n"
            "2️⃣ **Doença preexistente**\n"
            "3️⃣ **Fora do Rol da ANS**\n"
            "4️⃣ **Divergência médica** (querem junta)\n"
            "5️⃣ **Negaram material/prótese**"
        )
    
    elif estado == "JUSTIFICATIVA":
        dados["justificativa"] = resposta
        st.session_state.estado = "PROPOSTA"
        add_bot_message(
            "⚠️ **Atenção:** A jurisprudência é favorável em todos esses casos.\n\n"
            f"Com base na justificativa '{resposta}', podemos ingressar com ação imediata.\n\n"
            "**Deseja que a Dra. Lethícia analise seu caso gratuitamente?**"
        )
        st.session_state.estado = "AGUARDANDO_RESPOSTA"
    
    elif estado == "PROPOSTA":
        dados["aceitou_proposta"] = resposta.upper() == "SIM"
        
        if resposta.upper() == "SIM":
            # Salvar caso
            salvar_caso(dados)
            
            add_bot_message(
                f"✅ **ÓTIMO, {dados.get('nome')}!**\n\n"
                "Isso mostra que você prioriza sua saúde acima da burocracia.\n\n"
                f"Devido à complexidade do seu caso de **{dados.get('especialidade')}**, a {NOME_ESCRITORIO} "
                "definiu que é necessária uma **REUNIÃO DE VIABILIDADE POR VÍDEO (15 minutos)**.\n\n"
                "Nessa conversa, ela vai:\n"
                "✅ Validar sua documentação\n"
                "✅ Apresentar o plano de ação estratégico\n"
                "✅ Informar os valores de honorários\n\n"
                f"🔗 **Agende o melhor horário:** {CALENDLY_LINK}\n\n"
                "Em breve entraremos em contato para confirmar."
            )
            st.session_state.estado = "FINALIZADO"
        else:
            add_bot_message(
                f"Compreendo, {dados.get('nome')}.\n\n"
                "Infelizmente, sem ação judicial, seu caso continuará na fila do sistema, **sem previsão**.\n\n"
                f"Como nosso escritório foca apenas em quem deseja solução imediata, encerramos aqui.\n\n"
                "Caso mude de ideia, estamos à disposição.\n\n"
                "🙏 **Desejamos sorte no seu tratamento.**"
            )
            st.session_state.estado = "FINALIZADO"
    
    elif estado == "AGUARDANDO_RESPOSTA":
        # Já foi tratado no bloco PROPOSTA
        pass
    
    st.session_state.aguardando_resposta = False

def salvar_caso(dados: Dict):
    """Salva o caso em arquivo para análise"""
    caso = {
        "timestamp": datetime.now().isoformat(),
        "dados": dados
    }
    
    with open("casos_iara_bot.json", "a", encoding="utf-8") as f:
        json.dump(caso, f, ensure_ascii=False)
        f.write("\n")

# ============================================
# INTERFACE STREAMLIT
# ============================================

def render_sidebar():
    """Renderiza a barra lateral"""
    with st.sidebar:
        st.image("https://via.placeholder.com/300x100?text=Iara+Bot", use_container_width=True)
        
        st.markdown(f"## ⚖️ {NOME_ESCRITORIO}")
        st.markdown("**Especialista em Direito da Saúde**")
        st.markdown("---")
        
        st.markdown("### 📊 Status do Atendimento")
        
        dados = st.session_state.dados
        
        if dados.get("nome"):
            st.markdown(f"**Cliente:** {dados.get('nome')}")
        if dados.get("canal"):
            status_canal = "status-sus" if dados["canal"] == "SUS" else "status-plano"
            st.markdown(f"**Canal:** <span class='status-badge {status_canal}'>{dados['canal']}</span>", unsafe_allow_html=True)
        if dados.get("categoria"):
            st.markdown(f"**Categoria:** {dados['categoria']}")
        if dados.get("especialidade"):
            st.markdown(f"**Especialidade:** {dados['especialidade']}")
        if dados.get("nivel_urgencia") == "URGENTE":
            st.markdown(f"**🚨 Urgência:** <span class='status-badge status-urgente'>DETECTADA</span>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("### 📍 Contato")
        st.markdown(f"""
        - 📞 {TELEFONE}
        - 📧 contato@dra-lethicia.adv.br
        - 📍 São Paulo - SP
        """)
        
        st.markdown("---")
        
        if st.button("🔄 Nova Conversa", use_container_width=True):
            st.session_state.clear()
            st.rerun()
        
        st.markdown("---")
        st.caption("⚖️ **Iara Bot v1.0**")
        st.caption("Protocolo de Liberação Urgente")

def render_chat():
    """Renderiza o chat"""
    chat_container = st.container()
    
    with chat_container:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        for msg in st.session_state.messages:
            if msg["role"] == "bot":
                st.markdown(f'''
                <div class="chat-message bot-message">
                    <strong>🤖 Iara:</strong><br>{msg["content"]}
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="chat-message user-message">
                    <strong>👤 {st.session_state.dados.get("nome", "Você")}:</strong><br>{msg["content"]}
                </div>
                ''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

def render_input():
    """Renderiza o campo de input"""
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_input(
            "Digite sua mensagem:",
            key="user_input",
            disabled=st.session_state.get("estado") == "FINALIZADO",
            placeholder="Digite aqui sua resposta..."
        )
    
    with col2:
        send_button = st.button(
            "📤 Enviar",
            disabled=st.session_state.get("estado") == "FINALIZADO",
            use_container_width=True
        )
    
    # Botões rápidos
    estado_atual = st.session_state.get("estado", "")
    
    if estado_atual in ["CANAL", "CATEGORIA", "ESPECIALIDADE", "JUSTIFICATIVA"]:
        st.markdown("---")
        st.markdown("**🔘 Opções rápidas:**")
        
        opcoes = []
        
        if estado_atual == "CANAL":
            opcoes = ["SUS", "Plano de Saúde"]
        elif estado_atual == "CATEGORIA":
            opcoes = ["Cirurgia/Tratamento", "Consulta/Exame", "Medicamento", "Benefício INSS/BPC"]
        elif estado_atual == "ESPECIALIDADE":
            opcoes = ["Oncologia", "Neurodivergências (TEA/TDAH)", "Bariátrica", "Cardiologia", "Outro"]
        elif estado_atual == "JUSTIFICATIVA":
            opcoes = ["Carência", "Doença preexistente", "Fora do Rol da ANS", "Divergência médica"]
        
        cols = st.columns(min(len(opcoes), 4))
        for i, opcao in enumerate(opcoes[:4]):
            with cols[i % 4]:
                if st.button(opcao, key=f"btn_{i}", use_container_width=True):
                    add_user_message(opcao)
                    processar_resposta(opcao)
                    st.rerun()
    
    # Botões SIM/NÃO
    if estado_atual in ["URGENCIA", "LAUDO", "COMPROVANTE", "TEMPO_PLANO", "AGUARDANDO_RESPOSTA"]:
        st.markdown("---")
        st.markdown("**🔘 Responda rapidamente:**")
        
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
    
    # Mensagem inicial
    if len(st.session_state.messages) == 0:
        add_bot_message(
            f"Olá! Sou a **Iara**, assistente jurídica do escritório da {NOME_ESCRITORIO}, "
            "advogada especialista em **Direito da Saúde**.\n\n"
            "Atendemos casos de:\n"
            "🏥 **SUS** (cirurgias, consultas, exames, medicamentos)\n"
            "📋 **Planos de Saúde** (negativas, reajustes, terapias)\n"
            "📄 **INSS/BPC** (benefícios e recursos)\n\n"
            "**Qual é o seu nome?**"
        )
        st.rerun()

if __name__ == "__main__":
    main()
