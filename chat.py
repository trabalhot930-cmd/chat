"""
Aurora Bot - Assistente Jurídica em Direito da Saúde
VERSÃO CORRIGIDA E COMPLETA COM NOVAS FUNCIONALIDADES
"""

import streamlit as st
import streamlit.components.v1 as components
import time
import re

# ============================================
# CONFIGURAÇÕES
# ============================================
CALENDLY_LINK = "https://calendly.com/lethiciafernanda-adv-lxev/30min"
L = "Dra. Lethicia Fernanda"

LINK_CARTAO_97  = "https://www.asaas.com/c/oilhnffc7xyvc4n6"
LINK_PIX_97     = "https://www.asaas.com/c/9025wgqkpuziono4"
LINK_CARTAO_500 = "https://www.asaas.com/c/apigp8m45tileghw"
LINK_PIX_500    = "https://www.asaas.com/c/x1dfvyoajxnlgpp2"

st.set_page_config(
    page_title="Aurora Bot - Assistente Jurídica",
    page_icon="⚖️",
    layout="wide"
)

# ============================================
# CSS
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
</style>
""", unsafe_allow_html=True)

# ============================================
# FUNÇÕES AUXILIARES
# ============================================

def _n(r: str) -> str:
    return str(r).strip().lower()

def _sim(r: str) -> bool:
    return any(p in _n(r) for p in ["sim", "s", "yes", "quero", "ok", "claro", "vamos", "aceito", "topo"])

def _opcao_numero(r: str):
    """Extrai opção numérica escolhida por botão/texto.

    A tela principal de Plano de Saúde agora usa opções de 0 a 9:
    0=Reparadora, 1=Negativa de cirurgia, ..., 9=OUTRO.
    """
    texto = _n(r)
    # botão do Streamlit envia exatamente '0', '1', ..., '9'
    if texto in {str(i) for i in range(0, 10)}:
        return texto
    # aceita emojis/formatos como 0️⃣, 9️⃣, opção 9
    if "outro" in texto or re.search(r"\b9\b", texto) or "9️⃣" in texto:
        return "9"
    m = re.search(r"(?:^|\b)([0-8])(?:\b|️⃣)", texto)
    return m.group(1) if m else None

def init_session():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "estado" not in st.session_state:
        st.session_state.estado = "INICIO"
    if "dados" not in st.session_state:
        st.session_state.dados = {}
    if "nome" not in st.session_state:
        st.session_state.nome = None
    if "pergunta_idx" not in st.session_state:
        st.session_state.pergunta_idx = 0
    if "perguntas_ativas" not in st.session_state:
        st.session_state.perguntas_ativas = []
    if "followup_time" not in st.session_state:
        st.session_state.followup_time = None
    if "finalizacao_time" not in st.session_state:
        st.session_state.finalizacao_time = None
    if "followup_sent" not in st.session_state:
        st.session_state.followup_sent = False
    if "finalizacao_sent" not in st.session_state:
        st.session_state.finalizacao_sent = False
    if "aguardando_resposta_desde" not in st.session_state:
        st.session_state.aguardando_resposta_desde = None
    if "estado_antes_pergunta" not in st.session_state:
        st.session_state.estado_antes_pergunta = None
    if "dados_antes_pergunta" not in st.session_state:
        st.session_state.dados_antes_pergunta = None
    if "mensagem_antes_pergunta_resultados" not in st.session_state:
        st.session_state.mensagem_antes_pergunta_resultados = None
    # Para mensagens de 24h
    if "ultimo_contato_24h_idx" not in st.session_state:
        st.session_state.ultimo_contato_24h_idx = 0
    if "proxima_mensagem_24h_time" not in st.session_state:
        st.session_state.proxima_mensagem_24h_time = None
    if "agendamento_reuniao_data" not in st.session_state:
        st.session_state.agendamento_reuniao_data = None

def add_bot(msg, delay=5):
    if msg:
        msg = msg.replace("{nome}", st.session_state.nome or "")
        msg = msg.replace("{lawyer}", L)
        msg = msg.replace("{CALENDLY_LINK}", CALENDLY_LINK)
        # Remove ** para negrito (substitui por tags HTML)
        msg = msg.replace("**", "<strong>").replace("**", "</strong>", 1) if "**" in msg else msg
        # Corrige dupla substituição
        if "<strong>" in msg and "**" in msg:
            msg = msg.replace("**", "")
        time.sleep(delay)
        st.session_state.messages.append({"role": "bot", "content": msg})
        # inicia/renova o contador para enviar "Ainda está por aqui?"
        # caso o cliente não responda em até 5 minutos após a última mensagem do robô
        st.session_state.aguardando_resposta_desde = time.time()

def add_user(msg):
    st.session_state.messages.append({"role": "user", "content": msg})

def reset():
    st.session_state.clear()
    init_session()
    add_bot(MSG_BOAS_VINDAS)

# Função para verificar e enviar mensagem de 5 min sem resposta
def check_no_response_timeout():
    """Envia automaticamente “Ainda está por aqui?” quando o cliente fica 5 minutos sem responder.

    A mensagem não depende de clique, botão ou nova resposta do usuário.
    O contador é iniciado/renovado sempre que o robô envia uma mensagem via add_bot().
    """
    if st.session_state.get("aguardando_resposta_desde"):
        elapsed = time.time() - st.session_state.aguardando_resposta_desde
        if elapsed >= 300:  # 5 minutos
            # Evita duplicar a mensagem caso o Streamlit rode novamente no mesmo instante.
            if not st.session_state.messages or st.session_state.messages[-1].get("content") != "Ainda está por aqui?":
                st.session_state.messages.append({"role": "bot", "content": "Ainda está por aqui?"})
            st.session_state.aguardando_resposta_desde = None
            return True
    return False

def schedule_no_response_autorefresh():
    """Agenda uma atualização automática da tela para o exato momento do timeout.

    Sem isso, o Streamlit só verificaria os 5 minutos quando alguém clicasse em algo
    ou enviasse uma nova mensagem.
    """
    inicio = st.session_state.get("aguardando_resposta_desde")
    if not inicio:
        return
    remaining = max(1, int((300 - (time.time() - inicio)) * 1000) + 750)
    components.html(
        f"""
        <script>
            setTimeout(function() {{
                window.parent.location.reload();
            }}, {remaining});
        </script>
        """,
        height=0,
        width=0,
    )

# Função para mensagens de followup de 24h
def check_24h_messages():
    if st.session_state.proxima_mensagem_24h_time and not st.session_state.followup_sent:
        if time.time() >= st.session_state.proxima_mensagem_24h_time:
            mensagens_24h = [
                f"Oi {st.session_state.nome or ''}, vi que a minha mensagem chegou mas você não respondeu, acredito que seja por conta da correria do dia a dia, você prefere que eu retorne o contato posteriormente, ou podemos continuar agora?",
                f"Olá, {st.session_state.nome or ''}, tudo bem? Estou organizando o relatório de atendimentos da Dra. Lethicia para esta semana e notei que ainda não finalizamos a análise do seu caso. Como nossa pauta de reuniões para garantir liberações de atendimentos é limitada, gostaria de um posicionamento seu. Conseguimos avançar com a sua ajuda ainda esta semana ou prefere que eu libere o horário para o próximo da fila?",
                f"Oi, {st.session_state.nome or ''}! Percebi que você ainda não respondeu. Está tudo bem? Se precisar de mais algum detalhe ou tiver alguma dúvida, estou por aqui para te ajudar. 😊",
                f"Oi, {st.session_state.nome or ''}! Tudo certo por aí? Vi que ainda não tivemos um retorno. Gostaria de saber se você ainda tem interesse em seguir com nosso acompanhamento jurídico ou se há algo específico que você gostaria de ajustar."
            ]
            if st.session_state.ultimo_contato_24h_idx < len(mensagens_24h):
                st.session_state.messages.append({"role": "bot", "content": mensagens_24h[st.session_state.ultimo_contato_24h_idx]})
                st.session_state.ultimo_contato_24h_idx += 1
                st.session_state.proxima_mensagem_24h_time = time.time() + 86400  # +24h
                st.session_state.followup_sent = True
                return True
    return False

# Função para enviar link do Meet 5 min antes da reunião
def check_meet_link():
    if st.session_state.agendamento_reuniao_data:
        agora = time.time()
        hora_reuniao = st.session_state.agendamento_reuniao_data
        if hora_reuniao - 300 <= agora < hora_reuniao and not getattr(st.session_state, 'meet_link_enviado', False):
            # Link do Meet gerado pelo Calendly - normalmente é o mesmo do calendly
            st.session_state.messages.append({"role": "bot", "content": f"🔔 Lembrando que sua reunião com a {L} começa em 5 minutos! Aqui está o link para a videochamada: {CALENDLY_LINK}"})
            st.session_state.meet_link_enviado = True
            return True
    return False

# Função para verificar perguntas sobre resultados
def verificar_pergunta_resultados(resposta: str) -> bool:
    palavras_chave = [
        "já ganhou", "ja ganhou", "algum caso", "resultado", "tem algum resultado",
        "se eu perder", "e se eu perder", "risco", "tem risco",
        "não dar certo", "nao dar certo", "risco de não dar certo", "risco de nao dar certo",
        "garantido", "garantia", "é garantido", "e garantido",
        "certeza", "é certeza", "e certeza", "alguém já conseguiu", "alguem ja conseguiu",
        "cases reais", "possibilidade de não conseguir", "possibilidade de nao conseguir",
        "existe a possibilidade de não conseguir", "existe a possibilidade de nao conseguir",
        "casos reais de pessoas que conseguiram", "existem casos reais de pessoas que conseguiram",
        "vocês possuem cases reais", "voces possuem cases reais",
        "vocês já ganharam", "voces ja ganharam", "vocês já ganharam causas", "voces ja ganharam causas",
        "causas assim", "casos assim", "tenho medo de perder",
        "medo de perder", "tenho medo de gastar", "tenho medo de investir",
        "tenho medo de pagar", "gastar e perder", "investir e perder", "pagar e perder"
    ]
    return any(palavra in _n(resposta) for palavra in palavras_chave)

# Função para processar resposta de resultados (será chamada antes do processamento normal)
def processar_pergunta_resultados(resposta: str):
    if verificar_pergunta_resultados(resposta):
        # Salva estado atual para voltar depois
        st.session_state.estado_antes_pergunta = st.session_state.estado
        st.session_state.dados_antes_pergunta = st.session_state.dados.copy()
        # Guarda a última pergunta do robô para retomar o fluxo sem exigir nova mensagem digitada
        st.session_state.mensagem_antes_pergunta_resultados = next(
            (m.get("content") for m in reversed(st.session_state.messages) if m.get("role") == "bot"),
            None
        )
        st.session_state.estado = "PERGUNTA_RESULTADOS"
        if st.session_state.dados.get("canal") == "SUS":
            add_bot("Compreendo perfeitamente sua dúvida. No Direito à Saúde, lidamos com vidas, e resultados reais são o que validam nosso trabalho. A Dra. Lethicia Fernanda já ajudou diversos pacientes a saírem da demora ou da negativa do SUS para a mesa de cirurgia ou para o início de um tratamento.")
        else:
            add_bot("Compreendo perfeitamente sua dúvida. No Direito à Saúde, lidamos com vidas, e resultados reais são o que validam nosso trabalho. A Dra. Lethicia Fernanda já ajudou diversos pacientes a saírem do 'não' do plano para a mesa de cirurgia ou para o início de um tratamento.")
        add_bot("Como advogada, nós não podemos prometer ganhos de causa, isso fere a ética da profissão. Mas os casos do escritório sempre têm êxito, por algumas questões: somos especialistas em direito da saúde, atuamos somente com isso diariamente, antes de entrarmos com a ação, preparamos toda a documentação do cliente com as orientações corretas a ter em laudos e relatórios médicos. Não entregamos apenas um processo, entregamos uma estratégia de excelência desenhada para que o seu direito seja reconhecido de forma completa. É esse tipo de atuação que você busca?")
        return True
    return False

def voltar_apos_pergunta_resultados(resposta: str):
    if _sim(resposta):
        # Volta para o estado anterior e reapresenta a pergunta em que a conversa estava,
        # para o cliente continuar imediatamente pelo botão/resposta correta, sem precisar digitar outra mensagem.
        estado_anterior = st.session_state.estado_antes_pergunta
        mensagem_anterior = st.session_state.mensagem_antes_pergunta_resultados
        st.session_state.estado = estado_anterior
        if st.session_state.dados_antes_pergunta:
            st.session_state.dados = st.session_state.dados_antes_pergunta.copy()
        st.session_state.estado_antes_pergunta = None
        st.session_state.dados_antes_pergunta = None
        st.session_state.mensagem_antes_pergunta_resultados = None
        if mensagem_anterior:
            add_bot(mensagem_anterior, delay=0)
        return True
    else:
        add_bot(PS_ENCERRAMENTO)
        st.session_state.estado = "FIM"
        st.session_state.estado_antes_pergunta = None
        st.session_state.dados_antes_pergunta = None
        st.session_state.mensagem_antes_pergunta_resultados = None
        return False

# ============================================
# MENSAGENS PRINCIPAIS (com rosa 🌹)
# ============================================

MSG_BOAS_VINDAS = (
    "Olá, seja bem vindo(a). 🌹\n\n"
    "Sou a Aurora, assistente jurídica do escritório da Dra Lethicia Fernanda, "
    "advogada especialista em Direito da Saúde.\n\n"
    "Fico feliz que você entrou em contato conosco.\n\n"
    "Qual o seu nome?"
)

MSG_CANAL = "Olá, {nome}! Seu atendimento é pelo SUS ou por Plano de Saúde?"

# ============================================
# MENSAGENS DE VALORES (INTERCEPTAÇÃO) - ATUALIZADAS
# ============================================
MSG_VALORES_CIRURGIA = (
    "Eu entendo que o valor é importante, mas deixe-me te fazer uma pergunta: quanto vale uma estratégia jurídica que realmente garante o seu tratamento contra um sistema que quer te ver desistir?\n\n"
    "O seu caso exige uma estratégia jurídica personalizada e de alto nível. A Dra. Lethicia Fernanda entende que casos de alta complexidade, que envolvem o seu bem-estar e o seu futuro, devem ser tratados de forma personalizada.\n\n"
    "Precisamos de uma Reunião de Viabilização Jurídica rápida, de 20 minutos, via vídeo. É o momento onde ela vai alinhar o investimento necessário e, principalmente, te mostrar como vamos fazer pra você ter um atendimento correto para sua saúde.\n\n"
    "Fique tranquilo(a), esse primeiro contato é gratuito. Pra você marcar essa reunião, basta seguir com a nossa conversa, certo?"
)

MSG_VALORES_CONSULTA = (
    "Eu entendo que o valor é importante, mas deixe-me te fazer uma pergunta: quanto vale uma estratégia jurídica que realmente garante o seu exame contra um sistema que quer te ver desistir?\n\n"
    "O seu caso exige uma estratégia jurídica personalizada e de alto nível. A Dra. Lethicia Fernanda entende que casos de alta complexidade, que envolvem o seu bem-estar e o seu futuro, devem ser tratados de forma personalizada.\n\n"
    "Precisamos de uma Reunião de Viabilização Jurídica rápida, de 20 minutos, via vídeo. É o momento onde ela vai alinhar o investimento necessário e, principalmente, te mostrar como vamos fazer pra você ter um atendimento correto para sua saúde.\n\n"
    "Fique tranquilo(a), esse primeiro contato é gratuito. Pra você marcar essa reunião, basta seguir com a nossa conversa, certo?"
)

MSG_VALORES_REAJUSTE = (
    "Eu entendo que o valor é importante, mas deixe-me te fazer uma pergunta: quanto vale uma estratégia jurídica que realmente garante o reequilíbrio do seu plano contra reajustes abusivos?\n\n"
    "O seu caso exige uma estratégia jurídica personalizada e de alto nível. A Dra. Lethicia Fernanda entende que questões contratuais de alta complexidade devem ser tratadas de forma personalizada.\n\n"
    "Precisamos de uma Reunião de Viabilização Jurídica rápida, de 20 minutos, via vídeo. É o momento onde ela vai alinhar o investimento necessário e, principalmente, te mostrar como vamos fazer pra você ter o reequilíbrio do seu plano.\n\n"
    "Fique tranquilo(a), esse primeiro contato é gratuito. Pra você marcar essa reunião, basta seguir com a nossa conversa, certo?"
)

MSG_VALORES_ANALISE_INICIAL = (
    "Eu entendo que o valor é um ponto importante para você, mas antes de falarmos de números, precisamos falar de segurança: "
    "quanto vale uma estratégia jurídica personalizada para garantir o seu direito contra um sistema que espera que você desista?\n\n"
    "Aqui no escritório, prezamos por estratégias personalizadas. Por isso, os valores de investimento são passados diretamente pela Dra. Lethicia após essa análise inicial.\n\n"
    "Basta continuar nossa conversa por aqui para que os detalhes do seu caso cheguem à mesa dela. Assim que você finalizar, ela terá acesso às suas informações para te dar o direcionamento correto.\n\n"
    "Podemos seguir para a análise do seu caso?"
)

# ============================================
# SUS - FLUXO CIRURGIA (Mensagem do câncer apenas para maligno)
# ============================================

MSG_SUS_DEMANDA = "Me diga o que você está aguardando?\n\n🔪 Cirurgia / Tratamento\n\n📋 Consultas / Exames"

MSG_SUS_ESPECIALIDADE = (
    "Para que eu direcione você para o protocolo de urgência correto, "
    "qual problema estamos enfrentando hoje?\n\n"
    "1️⃣ Oncologia\n2️⃣ Neurodivergências (TEA, TDAH)\n3️⃣ Endometriose / Adenomiose\n"
    "4️⃣ Medicamento\n5️⃣ Bariátrica\n6️⃣ Neurologia / Neurocirurgia\n"
    "7️⃣ Cardiologia\n8️⃣ Outros"
)

# Perguntas SUS por especialidade (CIRURGIA) - ATUALIZADAS
PERGUNTAS_ONCOLOGIA = [
    "Entendi... vamos cuidar disso juntos 💙\n\nVocê consegue me contar qual é o tipo de câncer?",
    "O câncer que você está é benigno ou maligno?",
    "Você está aguardando atendimento ou tratamento pelo SUS? Se sim, há quanto tempo mais ou menos?",
    "Só pra eu entender melhor seu caso:\n\nO diagnóstico já foi confirmado por biópsia? E você tem esse laudo em mãos?",
    "Entendi...\n\nVocê já foi encaminhado para um hospital especializado em câncer (oncologia) pelo SUS ou ainda nem conseguiu passar com um especialista?",
    "Infelizmente, a fila do SUS não respeita o avanço da doença. Em casos de câncer, se o hospital não iniciou seu tratamento em 60 dias, a lei está sendo descumprida e precisamos forçar o início imediato via Justiça. Já tem mais que 60 dias que você está aguardando?",
    "Você possui um relatório médico explicando o tratamento que precisa fazer?",
    "Última perguntinha, que é bem importante:\n\nO médico falou se o seu caso é urgente?",
    "Você possui o comprovante de que está aguardando na fila?\n\nPode ser o print da tela do App Meu SUS Digital, o comprovante de agendamento da Secretaria de Saúde ou o papel da regulação (SISREG) com o número do seu protocolo."
]

# MENSAGEM DO CÂNCER (60 dias) - será usada condicionalmente
MSG_CANCER_60_DIAS = "Infelizmente, a fila do SUS não respeita o avanço da doença. Em casos de câncer, se o hospital não iniciou seu tratamento em 60 dias, a lei está sendo descumprida e precisamos forçar o início imediato via Justiça. Já tem mais que 60 dias que você está aguardando?"

PERGUNTAS_NEURO = [
    "Entendi... pode ficar tranquilo(a), vou te ajudar com isso 💙\n\nCasos assim realmente precisam de atenção, principalmente por envolver desenvolvimento.\n\nMe conta: já tem diagnóstico fechado ou ainda está em investigação?",
    "Você tem algum laudo ou relatório médico com o diagnóstico?",
    "Entendo as batalhas diárias que você enfrenta para garantir o melhor para quem você ama. Seja você ou seu filho(a) deve ter seu desenvolvimento barrado por limites impostos pelo SUS. Estou aqui para lutar ao seu lado e garantir todas as terapias que são de direito. Agora me conta uma coisa importante:\n\nQuais terapias o médico indicou? (ABA, Psico, fisioterapia...)",
    "E hoje, como está essa situação no SUS?\n\nVocê conseguiu iniciar as terapias ou ainda está aguardando?",
    "Entendo...\n\nVocê está em fila ou aguardando vaga?",
    "Essa parte é muito importante:\n\nO médico comentou algo sobre prejuízo no desenvolvimento ou necessidade de iniciar rápido as terapias?",
    "Se você puder me contar:\n\nComo essa situação está impactando o dia a dia de vocês?",
    "Você possui o comprovante de que está aguardando na fila?\n\nPode ser o print da tela do App Meu SUS Digital, o comprovante de agendamento da Secretaria de Saúde ou o papel da regulação (SISREG) com o número do seu protocolo."
]

PERGUNTAS_ENDOMETRIOSE = [
    "Entendi... imagino o quanto isso pode estar sendo difícil pra você 🥺. Mas fica tranquila, vou te ajudar com isso 💙.\n\nVocê já tem diagnóstico confirmado de endometriose ou adenomiose?",
    "Obrigado por me contar 🙏.\n\nEsse diagnóstico foi feito por exame? Se ainda não fez, qual exame está aguardando?",
    "Sei o quanto a dor e a incerteza cansam... não é justo que sua cirurgia ou exame continue demorando assim. Quero entender melhor sua situação:\n\nVocê sente dores fortes ou crises que atrapalham sua rotina?",
    "Agora uma parte bem importante:\n\nO médico indicou algum tratamento específico? (Ex: cirurgia de videolaparoscopia, medicamento...)",
    "Você tem relatório médico explicando esse tratamento?",
    "Você está aguardando há quanto tempo mais ou menos?",
    "O médico colocou em relatório ou te informou se existe risco de piora ou agravamento sem o tratamento?",
    "Você possui o comprovante de que está aguardando na fila?\n\nPode ser o print da tela do App Meu SUS Digital, o comprovante de agendamento da Secretaria de Saúde ou o papel da regulação (SISREG) com o número do seu protocolo."
]

PERGUNTAS_MEDICAMENTO_SUS = [
    "Entendi... vamos ver isso com calma 💙.\n\nQual foi o medicamento que o médico indicou pra você?",
    "Perfeito, obrigado por me explicar 🙏.\n\nVocê tem a receita ou relatório médico desse medicamento?",
    "Entendo a frustração de ter um direito negado justamente quando você mais precisa de suporte...\n\nAo te passar esse medicamento o seu médico escreveu no laudo que este remédio específico é o único que pode tratar seu caso agora e que a interrupção trará riscos à sua vida ou saúde?",
    "Essa parte é bem importante:\n\nVocê já utilizou outros medicamentos antes? Se sim, eles não tiveram resultado ou causaram algum problema?",
    "Você chegou a solicitar esse medicamento pelo SUS ou farmácia de alto custo? O que te informaram? (Negado, em análise, falta de estoque...)",
    "O médico comentou o que pode acontecer se você não usar esse medicamento?"
]

PERGUNTAS_BARIATRICA_SUS = [
    "Entendi... vamos ver isso com calma 💙.\n\nVocê já tem indicação médica para cirurgia bariátrica?",
    "Você tem algum laudo ou relatório médico indicando a cirurgia?",
    "Só pra eu entender melhor seu caso:\n\nVocê sabe me informar seu peso e altura? (Pode ser aproximado).",
    "Essa parte é bem importante:\n\nVocê já tentou outros tratamentos antes, como dieta, acompanhamento ou medicamentos? Como foi essa experiência?",
    "Você já está na fila de espera do SUS há quanto tempo? Você possui o comprovante de que está aguardando na fila?\n\nPode ser o print da tela do App Meu SUS Digital, o comprovante de agendamento da Secretaria de Saúde ou o papel da regulação (SISREG) com o número do seu protocolo."
]

PERGUNTAS_NEUROLOGIA_SUS = [
    "Entendi... vamos ver isso com calma 💙.\n\nVocê consegue me explicar qual é o problema neurológico ou o que o médico te disse?",
    "O seu caso envolve uma cirurgia de urgência?",
    "Você tem algum exame ou laudo sobre o problema neurológico?",
    "O médico indicou algum tratamento ou procedimento?",
    "Você tem relatório médico explicando essa necessidade?",
    "Você possui o comprovante de que está aguardando na fila?\n\nPode ser o print da tela do App Meu SUS Digital, o comprovante de agendamento da Secretaria de Saúde ou o papel da regulação (SISREG) com o número do seu protocolo."
]

PERGUNTAS_CARDIOLOGIA_SUS = [
    "Entendi... vamos ver isso com calma 💙.\n\nVocê consegue me explicar qual é o problema cardíaco ou o que o médico te disse?",
    "O seu caso envolve uma cirurgia de urgência (Ponte de safena, troca de válvula, marca-passo/Stent)?",
    "Você tem algum exame ou laudo do coração? (Eletro, eco, cateterismo...)",
    "Quais sintomas você tem sentido? (Dor no peito, falta de ar, tontura, cansaço excessivo).",
    "O médico indicou algum tratamento ou procedimento?",
    "Você tem relatório médico explicando essa necessidade?",
    "Você possui o comprovante de que está aguardando na fila?\n\nPode ser o print da tela do App Meu SUS Digital, o comprovante de agendamento da Secretaria de Saúde ou o papel da regulação (SISREG) com o número do seu protocolo."
]

PERGUNTAS_OUTROS_SUS = [
    "Entendi... como o seu caso é específico, eu preciso entender o que está acontecendo para te direcionar corretamente.\n\nPoderia me dizer qual é a sua condição/doença?",
    "Você já tem algum diagnóstico ou ainda está investigando?",
    "Algum médico já te passou relatório ou pedido de tratamento?",
    "Vamos resolver isso juntos...\n\nO médico comentou se existe urgência ou risco em não realizar esse tratamento?",
    "O que acontece com a sua saúde se você não conseguir isso nos próximos 30 ou 90 dias? Existe risco de agravamento ou sequela irreversível?",
    "Como essa situação tem afetado sua vida hoje?",
    "Você possui o comprovante de que está aguardando na fila?\n\nPode ser o print da tela do App Meu SUS Digital, o comprovante de agendamento da Secretaria de Saúde ou o papel da regulação (SISREG) com o número do seu protocolo."
]

# Pós-perguntas SUS (cirurgia)
MSG_POS_PERGUNTAS_SUS = (
    "{nome}, recebi suas respostas aqui. O que mais me preocupa no seu caso é que o SUS "
    "trata essa situação como se pudesse esperar, mas juridicamente sabemos que o tempo é o seu maior inimigo agora.\n\n"
    "Você sente que, se não resolvermos isso nos próximos dias, a sua saúde corre um risco de piorar de forma irreversível?"
)

MSG_EXPLICACAO_SUS = (
    "Só pra te explicar de forma simples:\n\n"
    "Quando o paciente precisa de atendimento, exame ou tratamento e não consegue pelo SUS, "
    "a Justiça pode intervir pra garantir esse direito.\n\n"
    "Para resolver isso, eu trabalho com um Protocolo de Liberação Urgente. "
    "Buscamos a sua consulta/exame/cirurgia/tratamento com urgência para tirar você da fila e ter acesso ao seu diagnóstico com o médico especialista. "
    "Isso faria diferença na sua vida agora?"
)

MSG_HONORARIOS_SUS = (
    "Como é um trabalho de alta especialidade, o escritório cobra Honorários Iniciais "
    "para assumir o caso e entrar com um processo judicial. Prosseguir com esse caso faz sentido "
    "para você garantir sua saúde hoje e sair dessa espera?"
)

MSG_REVERTER_SUS = (
    "Nesse caso só é possível revertermos a negativa/demora do SUS com medidas judiciais. "
    "Você está no momento exato de agirmos para buscar o seu direito judicialmente. "
    "Agora não é mais hora de esperar, é hora de exigir que o SUS cumpra a lei. "
    "O próximo passo agora é uma reunião rápida para eu te explicar como funciona o processo e valores de honorários. "
    "Não se preocupe, é uma reunião gratuita e on-line."
)

MSG_SIM_HONORARIOS_SUS_DECISAO = (
    "Antes de agendarmos a nossa reunião: além de você, tem mais alguém que participe das decisões familiares ou financeiras, "
    "como seu esposo/esposa, que seria importante estar presente para já tirarmos todas as dúvidas de uma vez?"
)

MSG_ENCERRAMENTO_SUS = (
    "Compreendo. Infelizmente, sem o interesse em avançar com uma medida judicial, "
    "o seu caso continuará dependendo exclusivamente da velocidade da fila do SUS, que como sabemos, não tem previsão.\n\n"
    "Como o escritório da Dra. Lethicia foca apenas em quem deseja forçar a solução imediata, estamos encerrando seu atendimento por aqui.\n\n"
    "Caso a sua situação se agrave ou você decida que não pode mais esperar, sinta-se à vontade para retornar. Desejamos sorte no seu tratamento. 🙏"
)

# ============================================
# SUS - FLUXO CONSULTAS/EXAMES
# ============================================

MSG_SUS_CONSULTA_EXAME = (
    "Você está buscando:\n\n"
    "1️⃣ Consulta com especialista\n"
    "2️⃣ Realização de Exame"
)

# --- FLUXO CONSULTA ---
MSG_SUS_CONSULTA_Q1 = (
    "Entendi que você está aguardando uma consulta especializada. Deixa eu te perguntar: "
    "você já está nessa fila de espera há mais de 30 dias ou o seu caso tem um prazo de urgência que o SUS simplesmente ignorou?"
)
MSG_SUS_CONSULTA_Q2 = "Qual especialidade médica você está aguardando?"
MSG_SUS_CONSULTA_Q3 = "Você tem encaminhamento ou pedido médico pra essa consulta?"
MSG_SUS_CONSULTA_PITCH = (
    "Muitas vezes o SUS nega a consulta dizendo que não tem o especialista, mas a lei é clara: "
    "se o governo não tem o médico, ele é obrigado a pagar uma consulta particular para você. "
    "A espera na fila da regulação não pode ser eterna, principalmente quando há dor ou risco de sequela.\n\n"
    "O Judiciário entende que o Estado não tem o direito de te deixar em uma fila infinita quando existe risco de agravamento. "
    "Você quer continuar contando com a sorte do sistema ou quer que a Dra. Lethicia force o governo a cumprir a lei agora?"
)
MSG_SUS_CONSULTA_AJUDA_Q1 = "Entendi...\n\nVocê está aguardando há quanto tempo mais ou menos?"
MSG_SUS_CONSULTA_AJUDA_Q2 = "O que te informaram quando você questionou sua posição na fila ou quando você foi tentar marcar? (fila, falta de médico, sem previsão...)"
MSG_SUS_CONSULTA_AJUDA_Q3 = "Você teria algum exame informando a condição de saúde que tem?"
MSG_SUS_CONSULTA_AJUDA_Q4 = (
    "Para a Dra. Lethicia validar o seu protocolo de urgência, você possui o print do App Meu SUS Digital ou o comprovante da fila de espera ou o comprovante do SISREG?"
)
MSG_SUS_CONSULTA_AJUDA_Q4B = (
    "Você tem o pedido/encaminhamento do Médico pra sua consulta?"
)
MSG_SUS_CONSULTA_PROTOCOLO = (
    "Para resolver isso, eu trabalho com um Protocolo de Liberação Urgente. "
    "Buscamos a sua consulta/exame com urgência para tirar você da fila e ter acesso ao seu diagnóstico com o médico especialista. "
    "Isso faria diferença na sua vida agora?"
)

# --- FLUXO EXAME ---
MSG_SUS_EXAME_Q1 = "Entendi... vamos ver isso com calma 💙\n\nQual exame o médico solicitou pra você?"
MSG_SUS_EXAME_TIPO = (
    "Esse exame que você precisa é para qual finalidade principal?\n\n"
    "1️⃣ Diagnóstico: Para descobrir o que eu tenho.\n"
    "2️⃣ Pré-operatório: Para eu conseguir operar logo.\n"
    "3️⃣ Confirmação: O médico suspeita de cirurgia e precisa do exame para decidir."
)

PERGUNTAS_EXAME_DIAGNOSTICO = [
    "Entendi...\n\nO médico comentou o que pode estar sendo investigado com esse exame? (se puder me explicar, ajuda muito)",
    "O médico comentou se existe urgência ou risco em não realizar esse exame?",
    "Você está aguardando há quanto tempo mais ou menos?",
    "Quem te pediu esse exame foi o médico especialista ou o médico do postinho/UBS?",
    "Você recebeu algum comprovante do SUS? (Pode ser agendamento; protocolo; print do aplicativo meu SUS; posição na fila)"
]

PERGUNTAS_EXAME_PREOP = [
    "Perfeito...\n\nVocê já tem indicação de cirurgia e esse exame é pra poder realizar o procedimento, certo? Se quiser, pode me explicar melhor o que falta.",
    "Você está aguardando há quanto tempo mais ou menos?",
    "Qual cirurgia que você precisa fazer?",
    "Quem te pediu esse exame foi o médico especialista ou o médico do postinho/UBS?",
    "Essa cirurgia ela é urgente ou não? Tem laudo médico atestando essa urgência?",
    "Você recebeu algum comprovante do SUS? (Pode ser agendamento; protocolo; print do aplicativo meu SUS; posição na fila)"
]

PERGUNTAS_EXAME_CONFIRMACAO = [
    "Entendi...\n\nO médico já suspeita que você pode precisar de qual tipo de cirurgia?",
    "Quais sintomas você apresentou pro médico pedir esse exame?",
    "O médico comentou se existe urgência ou risco em não realizar esse exame?",
    "Você está aguardando há quanto tempo mais ou menos?",
    "Você recebeu algum comprovante do SUS? (Pode ser agendamento; protocolo; print do aplicativo meu SUS; posição na fila)"
]

MSG_SUS_EXAME_PITCH = (
    "No SUS, a demora para realizar um Exame muitas vezes é o que impede o médico de salvar um paciente a tempo.\n\n"
    "O Judiciário entende que o Estado não tem o direito de te deixar em uma fila infinita quando existe risco de agravamento. "
    "Você quer continuar contando com a sorte do sistema ou quer que a Dra. Lethicia force o governo a cumprir a lei agora?"
)

MSG_SUS_EXAME_PROTOCOLO = (
    "Para resolver isso, eu trabalho com um Protocolo de Liberação Urgente. "
    "Buscamos a sua consulta/exame com urgência para tirar você da fila e ter acesso ao seu diagnóstico com o médico especialista. "
    "Isso faria diferença na sua vida agora?"
)

MSG_SUS_CE_ESPECIALIDADE = (
    "Para que eu direcione você para o protocolo correto, qual problema estamos enfrentando hoje?\n\n"
    "Oncologia, Bariátrica, Reparadora, Endometriose/Adenomiose, Cardiologia, Neurologia, Outro"
)

# ============================================
# PLANO DE SAÚDE - MENSAGENS COMPLETAS
# ============================================

PS_TEMPO = "Você já tem seu plano de saúde há mais de 2 anos?"

# NOVA: Pergunta após clicar em NÃO
PS_TEMPO_NAO_SEGUIMENTO = "Seu plano é pessoa física ou empresarial/CNPJ?"

# Fluxo para plano pessoa física com menos de 2 anos
PS_NAO_2ANOS_EDUCACAO = (
    "Entendi. Quando o plano tem menos de 2 anos, precisamos analisar com cuidado se a negativa envolve carência, urgência, doença preexistente ou outro fundamento usado pela operadora."
)
PS_NAO_2ANOS_Q1 = "Qual tratamento, cirurgia, exame ou medicamento você precisa neste momento?"
PS_NAO_2ANOS_Q2 = "O médico indicou urgência ou risco caso você não realize esse tratamento logo?"
PS_NAO_2ANOS_FEEDBACK = (
    "Perfeito. Essa informação é muito importante porque, em casos urgentes, a análise jurídica pode ser diferente da negativa comum por carência."
)
PS_NAO_2ANOS_Q3 = "Essa urgência está por escrito no relatório ou laudo médico?"
PS_NAO_2ANOS_Q4 = "Quando você contratou o plano, você já sabia dessa doença ou condição de saúde?"
PS_NAO_2ANOS_Q5 = "O plano negou usando carência, doença preexistente ou outro motivo parecido?"
PS_NAO_2ANOS_Q6 = "A negativa foi por escrito ou verbal, por telefone/balcão de atendimento?"

PS_SITUACAO = (
    "Para que eu possa te direcionar corretamente, qual é a sua situação atual com o plano de saúde?\n\n"
    "0️⃣ Reparadora\n"
    "1️⃣ Negativa de cirurgia\n"
    "2️⃣ Medicamento negado\n"
    "3️⃣ Exame negado\n"
    "4️⃣ Home care\n"
    "5️⃣ Terapias (Fono, ABA, Fisio, Psicopedagogia...)\n"
    "6️⃣ Reajuste\n"
    "7️⃣ Coparticipação elevada\n"
    "8️⃣ Erro médico\n"
    "9️⃣ OUTRO"
)

# ============================================
# 1. FLUXO REPARADORA (ATUALIZADO)
# ============================================
PS_REP_Q1 = "Você realizou a cirurgia bariátrica ou teve uma perda de peso expressiva através de dieta, exercícios ou uso das canetas emagrecedoras (Mounjaro, Ozempic, Tirzepatida...)?"
PS_REP_Q2 = "Você já chegou ou ainda falta pouco pro peso que gostaria?\n\n1️⃣ Já cheguei à minha meta\n2️⃣ Ainda não"
PS_REP_KG_PERDIDOS = "Quantos kg você perdeu no processo de emagrecimento?"

# NOVA MENSAGEM: Obrigada por compartilhar...
PS_REP_OBRIGADA = (
    "Obrigada por compartilhar isso comigo. Olha, o que você me relatou prova que a sua cirurgia não é estética, ela é funcional e reparadora.\n\n"
    "O erro de muita gente é acreditar quando o plano diz que 'não está no contrato'. A lei obriga o plano a cobrir a sua reconstrução total. Eu já ajudei diversas pessoas a saírem dessa mesma situação e conquistarem a cirurgia sem pagar nada a mais por isso."
)

PS_CONSULTA_ORIENTACAO_INTRO = (
    "Eu entendo perfeitamente que enfrentar uma questão jurídica gera muitas incertezas e dúvidas sobre o tempo certo de agir.\n\n"
    "Muitas pessoas ficam na dúvida se já devem contratar uma assessoria jurídica agora ou se precisam esperar o problema se agravar "
    "(ou uma resposta negativa chegar) para entenderem seus direitos. Meu papel é justamente trazer essa clareza para você."
)

PS_CONSULTA_ORIENTACAO_OPCOES = (
    "Opção 1: Seguir no seu tempo\n"
    "Você dá entrada nos pedidos do plano, caso receba uma negativa, tenha dificuldades ou se sinta pronta para avançar, você me procura para analisarmos o início do processo judicial.\n\n"
    "👉 Opção 2: Reunião de Orientação (Agora)\n"
    "Nós agendamos uma consulta para eu esclarecer todas as suas dúvidas e te orientar juridicamente sobre o seu caso.\n\n"
    "Nessa conversa, vou te explicar:\n"
    "• O que a lei e os tribunais entendem sobre situações como a sua;\n"
    "• Quais direitos podem existir no seu caso;\n"
    "• O que costuma ser necessário para buscar o tratamento, cirurgia, medicamento ou cobertura;\n"
    "• E, principalmente, qual é o melhor momento para agir juridicamente, evitando perda de tempo.\n\n"
    "O que faz mais sentido para você hoje: tentar resolver sozinha por enquanto ou tirar todas as suas dúvidas em uma consulta comigo agora para já se proteger?"
)

PS_REP_ORIENTACAO_INTRO = (
    "Eu entendo que o processo de perda de peso é uma jornada e que muitas dúvidas surgem no caminho, especialmente sobre o que vem depois.\n\n"
    "Muitas pessoas ficam na dúvida se já devem procurar um advogado ou se precisam esperar chegar ao peso final para entender seus direitos."
)

PS_REP_ORIENTACAO_OPCOES = (
    "Opção 1: Seguir no seu tempo\n"
    "Você continua focada na sua meta e, quando se sentir pronta ou o médico indicar as reparadoras, você me procura para darmos início à análise do caso.\n\n"
    "Opção 2: Reunião de Orientação (Agora)\n"
    "Nós agendamos uma consulta para eu esclarecer todos os seus direitos. Nessa conversa, vou te explicar:\n"
    "• O que a lei diz sobre as cirurgias reparadoras;\n"
    "• Quais os critérios que os tribunais usam para garantir esse direito;\n"
    "• E, principalmente, em que momento exato você deve começar a se preparar juridicamente, para não perder prazos ou direitos.\n\n"
    "O meu objetivo é que você passe por essa fase de emagrecimento com tranquilidade, sabendo exatamente o que te espera lá na frente. "
    "O que faz mais sentido para você hoje: aguardar mais um pouco ou tirar essas dúvidas em uma consulta comigo agora?"
)

PS_CONSULTA_PAGA_97 = (
    "O valor da consulta é de R$ 97,00 e ela é feita online, no horário que funcionar melhor pra você.\n\n"
    "E caso depois você decida avançar com o acompanhamento jurídico completo, também conversamos sobre isso na consulta, sem qualquer pressão.\n\n"
    "O meu objetivo é que você passe por essa situação com mais clareza e segurança, sabendo exatamente quais são os seus direitos e quais caminhos existem no seu caso.\n\n"
    "Como deseja realizar o investimento do atendimento? Você prefere Pix ou Cartão de Crédito?"
)

# Mantido o nome antigo para compatibilidade com pontos do fluxo que chamavam essa variável.
PS_REP_NAO_PESO = PS_CONSULTA_PAGA_97

PS_REP_EMPATIA = (
    "Para eu desenhar a melhor estratégia para você, me conte um pouco...\n\n"
    "Esse excesso de pele hoje te causa dores, assaduras ou dermatites que não curam? E além do corpo, como isso tem afetado a sua autoestima e a sua liberdade de movimento no dia a dia?"
)

# NOVA MENSAGEM: Uma curiosidade que poucos sabem...
PS_REP_CURIOSIDADE = (
    "Uma curiosidade que poucos sabem: se você fosse pagar todas as cirurgias reparadoras do seu próprio bolso hoje, o investimento passaria facilmente dos R$ 20 mil reais, podendo chegar a mais de R$ 150 mil reais a depender de quais reparadoras você precisa, entre hospital e equipe. É um valor que foge da realidade de 99% dos brasileiros. Eu ajudo meus clientes a acessarem esse direito sem precisar desembolsar essa fortuna, afinal, o plano de saúde serve para isso. O investimento jurídico é apenas uma fração minúscula perto do que você vai economizar."
)

PS_REP_Q4 = "Quais cirurgias reparadoras você teria interesse em fazer?"
PS_REP_Q5 = "Você já chegou a ir no médico cirurgião plástico pra solicitar as reparadoras?"

# MENSAGEM ALTERADA - com botões específicos
PS_REP_ACOMPANHAMENTO = (
    "Você está no caminho certo 💙 Muitas pessoas acabam procurando ajuda só depois da negativa ou quando o problema já está mais avançado. "
    "Mas quando a gente atua antes, conseguimos evitar erros e fortalecer muito o caso.\n\n"
    "Você prefere tentar sozinho com o plano ou quer o acompanhamento da Dra. para garantir que o seu pedido seja feito à prova de negativas?"
)

# MENSAGEM DO ACOMPANHAMENTO JURÍDICO
MSG_ACOMPANHAMENTO_JURIDICO = (
    "Com o acompanhamento jurídico, você tem as orientações corretas sobre quais médicos deve ir e como que deve ser feitos os laudos, "
    "o que você deve fazer na perícia do plano de saúde (se for solicitado no seu caso), isso tudo sendo organizado agora, "
    "após a negativa do plano, você já vai ter todos os laudos e documentos corretos pra um processo judicial, "
    "assim não precisa corrigir ou ficar correndo atrás de laudos depois. Entende?"
)

# ============================================
# 2. NEGATIVA DE CIRURGIA - ESPECIALIDADES
# ============================================
PS_NEG_CIR_ESP = "Qual é o diagnóstico ou o tratamento específico que o plano está dificultando no momento?\n\n1️⃣ Endometriose\n2️⃣ Bariátrica\n3️⃣ Oncologia (câncer)\n4️⃣ Cardiologia (coração)\n5️⃣ Neurocirurgia\n6️⃣ Ortopedia\n7️⃣ Oftalmologia\n8️⃣ OUTRO"

# 2A. ENDOMETRIOSE
PS_ENDO_Q1 = "Qual tipo de cirurgia foi indicada para o seu caso?"
PS_ENDO_Q2 = "Sinto muito que você esteja passando por isso. Sabemos que a endometriose não é 'só uma cólica', é algo que para a vida da mulher 💙\n\nO plano negou formalmente ou simplesmente não respondeu?"
PS_ENDO_Q3 = "Sei o quanto a dor e a incerteza cansam, mas você merece viver com saúde e qualidade. Não é justo que a sua cirurgia seja negada depois de tanta espera. Vou te ajudar a destravar esse processo 💙\n\nO plano justificou a negativa de alguma forma? (Ex: 'eletivo', 'sem cobertura', 'período de carência')"
PS_ENDO_Q4 = "Você tem os exames que demonstram o seu diagnóstico?"
PS_ENDO_Q5 = "Você já tentou resolver isso diretamente com o plano — ligação, protocolo, ouvidoria ou recurso formal?"

# 2B. BARIÁTRICA
PS_BARI_Q1 = "Qual o seu IMC atual? Se não souber, pode me falar somente seu peso atual e sua altura"
PS_BARI_Q2 = "Você tem comorbidades? (diabetes, hipertensão, apneia do sono, problemas nas articulações)"
PS_BARI_Q3_MSG = "A cirurgia bariátrica nunca é apenas estética. É seu direito concluir esse ciclo com segurança e cobertura total pela operadora. Vou superar esses obstáculos contratuais para que seu procedimento seja autorizado 💙"
PS_BARI_Q3 = PS_BARI_Q3_MSG + "\n\nFez o acompanhamento multidisciplinar exigido (nutricionista, psicólogo, endocrinologista)?"
PS_BARI_Q4 = "O plano negou formalmente ou simplesmente não respondeu?"
PS_BARI_Q5 = "O plano justificou a negativa de alguma forma? (Ex: 'eletivo', 'sem cobertura', 'período de carência')"
PS_BARI_Q6 = "Você já tentou resolver isso diretamente com o plano — ligação, protocolo, ouvidoria ou recurso formal?"

# 2C. ONCOLOGIA
PS_ONCO_Q1 = "Qual o tipo de câncer e qual procedimento foi indicado — cirurgia, quimio, radio, imunoterapia?"
PS_ONCO_Q2 = "Já está em tratamento de alguma forma, ou a negativa está impedindo o início?"
PS_ONCO_Q3 = "Sinto muito que você esteja passando por isso, mas saiba que não está sozinha nessa luta. Vou cuidar de toda a burocracia para que você tenha seu tratamento sem interrupções. Seu foco agora deve ser apenas a sua cura: o resto, pode deixar aqui com a gente.\n\nO plano negou formalmente ou simplesmente não respondeu?"
PS_ONCO_Q4 = "O plano justificou a negativa de alguma forma? (Ex: 'eletivo', 'sem cobertura', 'período de carência')"
PS_ONCO_Q5 = "Você tem os exames que demonstram o seu diagnóstico?"
PS_ONCO_Q6 = "Você já tentou resolver isso diretamente com o plano — ligação, protocolo, ouvidoria ou recurso formal?"

# 2D. CARDIOLOGIA
PS_CARDIO_Q1 = "Qual tipo de cirurgia foi indicada para o seu caso?"
PS_CARDIO_Q2 = "No seu caso o plano negou material cirúrgico ou alguma prótese?"
PS_CARDIO_Q3 = "O plano negou formalmente ou simplesmente não respondeu?"
PS_CARDIO_Q4 = "Você já está internado aguardando o procedimento ou está em casa esperando a autorização para agendar?\n\n1️⃣ Já estou internado\n2️⃣ Estou em casa esperando"
PS_CARDIO_Q5 = "O procedimento foi considerado urgente?\n\n1️⃣ Sim\n2️⃣ Não"
PS_CARDIO_Q6 = "Você tem exames (ecocardiograma, cateterismo, ECG) que confirmam a necessidade cirúrgica?"

# 2E. NEUROCIRURGIA (ATUALIZADA)
PS_NEURO_Q1 = "Qual procedimento neurocirúrgico foi indicado?"
PS_NEURO_Q2 = "O paciente está internado ou com dor insuportável e precisa operar imediatamente?\n\n1️⃣ Sim\n2️⃣ Não"
PS_NEURO_Q3 = "O hospital onde seria realizada a cirurgia é da rede do plano?\n\n1️⃣ Sim\n2️⃣ Não\n3️⃣ Não sei"
PS_NEURO_Q4 = "Sinto muito que você esteja passando por essa insegurança. Para eu desenhar a melhor estratégia jurídica, me conte:\n\nHoje, esse problema neurológico está afetando seus movimentos, causando perda de força ou dores que impedem você de realizar tarefas básicas?"
# ATUALIZADO: A negativa do plano foi por escrita ou verbal (telefone ou balcão de atendimento)?
PS_NEURO_Q5 = "A negativa do plano foi por escrita ou verbal (telefone ou balcão de atendimento)?"
# REMOVIDO: PS_NEURO_Q6 (material cirúrgico) - foi retirado
PS_NEURO_Q7 = "Você tem exames de imagem — ressonância magnética, tomografia — que confirmam a necessidade cirúrgica?"

# 2F. ORTOPEDIA
PS_ORTO_Q1 = "Qual cirurgia ortopédica foi indicada?"
PS_ORTO_Q2 = "A condição está limitando sua mobilidade ou capacidade de trabalho?\n\n1️⃣ Sim, de forma significativa\n2️⃣ Parcialmente\n3️⃣ Ainda consigo me movimentar"
PS_ORTO_Q3 = "O plano justificou a negativa de alguma forma? (Ex: 'eletivo', 'sem cobertura', 'período de carência')"
PS_ORTO_APOIO = "É muito comum os planos de saúde darem desculpas para não pagar um tratamento, ignorando o que o seu médico pediu. Eu sei o quanto é angustiante ouvir um 'não' do plano de saúde, principalmente quando estamos falando de Ortopedia. Mas a regra é simples: se o médico disse que você precisa, o plano tem que cobrir. Como eu trabalho só com casos de saúde, vejo que a gente tem um caminho bem claro para seguir aqui. O contrato do plano existe para cuidar da sua vida, não para te dar dor de cabeça. Você sente que eles estão sendo injustos com você?"
PS_ORTO_Q4 = "No seu caso o plano negou material cirúrgico ou alguma prótese?"
PS_ORTO_Q5 = "A negativa do plano foi por escrita ou verbal (telefone ou balcão de atendimento)?"
PS_ORTO_Q6 = "Você tem exames de imagem — ressonância magnética, tomografia — que confirmam a necessidade cirúrgica?"

# 2G. OFTALMOLOGIA
PS_OFTAL_Q1 = "Qual cirurgia oftalmológica foi indicada?"
PS_OFTAL_Q2 = "A condição está afetando sua visão de forma significativa?\n\n1️⃣ Sim, já estou com visão muito comprometida\n2️⃣ Está piorando progressivamente\n3️⃣ Ainda consigo enxergar razoavelmente"
PS_OFTAL_Q3 = "O médico indicou urgência, risco de perda de visão se não operar logo?\n\n1️⃣ Sim, há urgência expressa no laudo\n2️⃣ O médico disse verbalmente, mas não está no laudo\n3️⃣ Não há urgência indicada"
PS_OFTAL_Q4 = "O plano justificou a negativa de alguma forma? (Ex: 'eletivo', 'sem cobertura', 'período de carência')"
PS_OFTAL_Q5 = "A negativa do plano foi por escrita ou verbal (telefone ou balcão de atendimento)?"
PS_OFTAL_APOIO = "É muito comum os planos de saúde darem desculpas para não pagar um tratamento, ignorando o que o seu médico pediu. Eu sei o quanto é angustiante ouvir um 'não' do plano de saúde, principalmente quando estamos falando de Oftalmologia. Mas a regra é simples: se o médico disse que você precisa, o plano tem que cobrir. Como eu trabalho só com casos de saúde, vejo que a gente tem um caminho bem claro para seguir aqui. O contrato do plano existe para cuidar da sua vida, não para te dar dor de cabeça. Você sente que eles estão sendo injustos com você?"

# 2H. OUTRO
PS_OUTRO_INTRO = "Entendido! Cada procedimento cirúrgico tem a sua importância e, se o seu médico indicou, é porque é necessário para a sua saúde. O plano não tem o direito de 'escolher' qual cirurgia você deve ou não fazer."
PS_OUTRO_Q1 = "Qual cirurgia foi indicada pelo seu médico?"
PS_OUTRO_Q2 = "Para qual problema ou doença ela foi recomendada?"
PS_OUTRO_Q3 = "Você possui exames que comprovam a necessidade?\n\n1️⃣ Sim\n2️⃣ Não"
PS_OUTRO_Q4 = "A cirurgia foi negada?\n\n1️⃣ Sim\n2️⃣ Não\n3️⃣ Ainda não solicitei"
PS_OUTRO_APOIO = "É muito comum os planos de saúde darem desculpas para não pagar um tratamento, ignorando o que o seu médico pediu. Eu sei o quanto é angustiante ouvir um 'não' do plano de saúde, principalmente quando estamos falando do procedimento indicado pelo seu médico. Mas a regra é simples: se o médico disse que você precisa, o plano tem que cobrir. Como eu trabalho só com casos de saúde, vejo que a gente tem um caminho bem claro para seguir aqui. O contrato do plano existe para cuidar da sua vida, não para te dar dor de cabeça. Você sente que eles estão sendo injustos com você?"
PS_OUTRO_Q5 = "O plano justificou a negativa de alguma forma? (Ex: 'eletivo', 'sem cobertura', 'período de carência')"
PS_OUTRO_Q6 = "A negativa do plano foi por escrita ou verbal (telefone ou balcão de atendimento)?"
PS_OUTRO_Q7 = "Hoje, a falta dessa cirurgia te impede de trabalhar, de dormir bem ou de realizar suas atividades simples do dia a dia?"
PS_OUTRO_Q8 = "Se você não realizar a cirurgia, pode ocorrer:\n\n1️⃣ Dor intensa\n2️⃣ Agravamento do problema\n3️⃣ Risco à saúde\n4️⃣ Limitação no dia a dia"
PS_OUTRO_Q9 = "Você possui exames que comprovam a necessidade?\n\n1️⃣ Sim\n2️⃣ Não"

# ============================================
# 3. MEDICAMENTO NEGADO
# ============================================
PS_MED_Q1  = "Qual doença você está tratando?"
PS_MED_Q2  = "Qual medicamento foi prescrito pelo médico?"
PS_MED_Q3  = "O fornecimento do medicamento foi negado?\n\n1️⃣ Sim\n2️⃣ Não\n3️⃣ Ainda não solicitei"
PS_MED_Q4  = "Eu sei que cada dia sem a medicação gera uma ansiedade enorme, afinal, a sua saúde não pode esperar o tempo do plano.\n\nHoje, a falta desse medicamento já está afetando o controle da sua doença ou causando sintomas que impedem sua rotina?"
PS_MED_Q5  = "Qual foi o motivo da negativa?\n\n1️⃣ Fora do rol da ANS\n2️⃣ Alto custo\n3️⃣ Uso domiciliar\n4️⃣ Experimental/off-label\n5️⃣ Outro"
PS_MED_Q6  = "A negativa do plano foi por escrita ou verbal (telefone ou balcão de atendimento)?"
PS_MED_Q7  = "Muitos pacientes desistem quando ouvem que o remédio 'não está no Rol' ou 'é domiciliar' ou 'experimental', mas a verdade é que a justiça entende que se o seu médico prescreveu, o plano é obrigado a fornecer.\n\nVocê possui receita médica do medicamento?"
PS_MED_Q9  = "Qual o valor aproximado do medicamento?"
PS_MED_Q10 = "Você tem laudo médico explicando a necessidade do medicamento?\n\n1️⃣ Sim\n2️⃣ Não"

# ============================================
# 4. EXAME NEGADO (ATUALIZADO - mensagens unificadas)
# ============================================
PS_EXAME_Q1 = "Qual exame foi solicitado pelo seu médico?"
PS_EXAME_Q2 = "Para qual doença ou suspeita esse exame foi indicado?"
# MENSAGEM UNIFICADA
PS_EXAME_Q3_E_Q4 = (
    "Sei o quão frustrante é ter um exame negado. Sem o exame, não há diagnóstico, e sem diagnóstico, não há tratamento. O plano não pode impedir a investigação da sua saúde.\n\n"
    "Você sente que essa demora do plano está prejudicando a sua saúde ou impedindo que você comece o tratamento que tanto precisa?"
)
PS_EXAME_Q5 = "O que o seu médico lhe disse sobre a urgência deste resultado?"
PS_EXAME_Q6 = "Qual foi o motivo da negativa?\n\n1️⃣ Fora do rol da ANS\n2️⃣ Não atende diretriz (DUT)\n3️⃣ Carência\n4️⃣ Não é urgente\n5️⃣ Experimental\n6️⃣ Outro"
PS_MOTIVO_NEGATIVA_GERAL = PS_EXAME_Q6
PS_EXAME_Q7 = "A negativa do plano foi por escrita ou verbal (telefone ou balcão de atendimento)?"

# ============================================
# 5. HOME CARE
# ============================================
PS_HOME_Q1 = "Sinto muito que você e sua família estejam passando por esse momento. Sabemos que o Home Care não é um 'luxo', mas a única forma de garantir dignidade, segurança e uma recuperação humanizada para quem você ama. 💙\n\nQual a doença ou condição do paciente?"
PS_HOME_Q2 = "O paciente está acamado ou depende de cuidados constantes?"
PS_HOME_Q3 = "O paciente já ficou internado recentemente?"
PS_HOME_Q4 = "Eu imagino o peso que está nos seus ombros agora. Cuidar de quem amamos exige muito, e sem a estrutura técnica correta, o medo de algo acontecer é constante.\n\nVocê sente que o plano de saúde está tentando transferir para a sua família uma responsabilidade médica que é deles?"
PS_HOME_Q5 = "O home care foi negado?\n\n1️⃣ Sim\n2️⃣ Não\n3️⃣ Ainda não solicitei"
PS_HOME_Q6 = "Você possui relatório médico detalhado?\n\n1️⃣ Sim\n2️⃣ Não"
PS_HOME_Q7 = "Está descrito o tipo de cuidado necessário (enfermagem, 24h, etc.)?"

# ============================================
# 6. TERAPIAS (ATUALIZADO - com opção OUTROS)
# ============================================
PS_TERA_Q1 = "O tratamento é para:\n\n1️⃣ Autismo (TEA)\n2️⃣ Desenvolvimento infantil\n3️⃣ Reabilitação física\n4️⃣ Saúde mental\n5️⃣ Outro"
PS_TERA_Q2 = "Quais terapias foram indicadas pelo médico?\n\n1️⃣ ABA\n2️⃣ Fisioterapia\n3️⃣ Psicologia\n4️⃣ Fonoaudiologia\n5️⃣ Terapia ocupacional\n6️⃣ Psicopedagogia\n7️⃣ Musicoterapia\n8️⃣ Hidroterapia\n9️⃣ OUTROS"
PS_TERA_Q3 = "Quantas sessões por semana foram indicadas?"
PS_TERA_Q4 = "Eu entendo que essa não é apenas uma briga por 'papéis', é uma briga pelo futuro e pela autonomia sua ou de quem você ama. 💙\n\nHoje, a falta dessas terapias ou a limitação das sessões tem causado retrocessos ou estagnado a evolução que você(s) tanto espera(m)?"
PS_TERA_Q5 = "O que aconteceu?\n\n1️⃣ Limitou número de sessões\n2️⃣ Negou totalmente\n3️⃣ Não tem profissional disponível\n4️⃣ Outro"
PS_TERA_Q6 = "Você possui laudo médico com o diagnóstico?\n\n1️⃣ Sim\n2️⃣ Não"
PS_TERA_Q7 = "A negativa do plano foi por escrita ou verbal (telefone ou balcão de atendimento)?"

# ============================================
# 7. REAJUSTE
# ============================================
PS_REAJ_Q1 = "Recebi seu contato e já quero te tranquilizar: você não precisa aceitar um reajuste que torna o seu plano de saúde impagável. Muitas vezes, esses aumentos são aplicados de forma ilegal para forçar o cancelamento do contrato, mas a justiça está aí para impedir isso. 💙\n\nO plano é:\n\n1️⃣ Individual/Familiar\n2️⃣ Coletivo por adesão\n3️⃣ Empresarial\n4️⃣ Não sei"
PS_REAJ_Q2 = "De quanto foi aproximadamente o aumento?\n\n1️⃣ Até 20%\n2️⃣ 20% a 50%\n3️⃣ Mais de 50%\n4️⃣ Não sei"
PS_REAJ_Q3 = "É muito frustrante ver o valor subir tanto, especialmente quando você sempre honrou com os pagamentos para garantir a sua segurança e a da sua família. 💙\n\nHoje, esse novo valor do boleto compromete a sua renda ou faz você considerar cancelar o plano?"
PS_REAJ_Q4 = "Você (ou o titular) tem mais de 59 anos?\n\n1️⃣ Sim\n2️⃣ Não"
PS_REAJ_Q5 = "O aumento ocorreu após mudança de idade?\n\n1️⃣ Sim\n2️⃣ Não"
PS_REAJ_Q6 = "Você recebeu algum documento detalhando o aumento?\n\n1️⃣ Sim\n2️⃣ Não"
PS_REAJ_Q7 = "Esse plano foi feito por:\n\n1️⃣ Empresa\n2️⃣ Associação/sindicato\n3️⃣ Contratei sozinho"
PS_REAJ_Q8 = "Você possui o contrato do plano?\n\n1️⃣ Sim\n2️⃣ Não"

# Novo fluxo pós-contrato - Reajuste
PS_REAJ_INTRO_ABUSIVO = (
    "É muito comum os planos de saúde aplicarem reajustes anuais ou por mudança de faixa etária que tornam a mensalidade impagável, "
    "ignorando as limitações impostas pela lei e pela ANS. Eu sei o quanto é frustrante ver o valor do seu plano subir drasticamente, "
    "muitas vezes sem uma justificativa clara."
)

PS_REAJ_ANALISE = (
    "Analiso situações de aumentos abusivos diariamente e posso te afirmar: a maioria desses reajustes possui solução jurídica. "
    "Existem índices máximos e regras de clareza que as operadoras são obrigadas a seguir e, quando não seguem, "
    "é possível reduzir a mensalidade e até recuperar o que foi pago a mais. O segredo está em identificar o erro no cálculo aplicado ao seu contrato."
)

PS_REAJ_ESCOLHA = (
    "Agora, para que eu possa te dar o direcionamento correto, escolha a opção que melhor descreve o seu momento atual:\n\n"
    "1️⃣ Já sofro com o aumento abusivo: Desejo uma análise jurídica para ingressar com uma ação, reduzir o valor da mensalidade e buscar a restituição dos valores pagos indevidamente.\n\n"
    "2️⃣ Desejo uma análise preventiva: Quero entender se o reajuste que recebi ou vou receber está dentro da lei ou se existem cláusulas abusivas no meu contrato."
)

PS_REAJ_JUDICIALIZAR_1 = (
    "Compreendo. No Direito à Saúde, a aplicação de reajustes acima dos índices legais é o ponto de partida para a nossa intervenção. "
    "Muitas vezes, esses aumentos carecem de fundamento e ferem o Código de Defesa do Consumidor. "
    "Meu papel agora é analisar tecnicamente esse cálculo para estruturar a medida judicial cabível para o seu caso."
)

PS_REAJ_JUDICIALIZAR_2 = (
    "O próximo passo agora é uma conversa direto com a Dra Lethicia para ela te explicar como funciona o processo e os valores de honorários para a sua demanda. "
    "Não se preocupe, essa análise inicial por aqui é gratuita e rápida."
)

PS_REAJ_CONSULTORIA = (
    "Entendido. Para casos cautelosos com o seu, realizamos uma Consultoria Jurídica.\n\n"
    "Nesta reunião online, eu analisarei detalhadamente o seu contrato e as planilhas de reajuste para te entregar um parecer seguro sobre a abusividade do seu plano.\n\n"
    "Informações sobre a Consultoria:\n"
    "• Investimento: R$ 600,00 (referente à análise técnica e reserva de horário).\n"
    "• Duração: Até 1 hora.\n"
    "• Objetivo: Diagnóstico completo e estratégia jurídica personalizada.\n\n"
    "Deseja prosseguir com o agendamento?"
)

PS_REAJ_PAGAMENTO = (
    "Perfeito! Vamos reservar o seu horário.\n\n"
    "Como deseja realizar o investimento do atendimento? Você prefere Pix ou Cartão de Crédito?"
)

PS_REAJ_CONFIRMACAO = "Ao realizar o pagamento e for dado baixa no nosso financeiro, alguém da nossa equipe vai entrar em contato o quanto antes pra marcar seu atendimento na agenda da Dra Lethicia."

# ============================================
# 8. COPARTICIPAÇÃO
# ============================================
PS_COPA_Q1 = "Recebi seu contato e já te adianto: a coparticipação não pode ser uma surpresa desagradável no seu boleto. Ela deve ser clara e, acima de tudo, dentro dos limites da lei. Ninguém deve ter medo de usar o plano por causa do valor das taxas. 💙\n\nVocê deixou de fazer exames ou tratamentos por causa da coparticipação?\n\n1️⃣ Sim\n2️⃣ Não"
PS_COPA_Q2 = "É muito desgastante você pagar o plano em dia e, quando mais precisa dele, ser surpreendido com taxas que parecem uma segunda mensalidade.\n\nVocê sente que hoje está 'pagando para usar' o que já deveria estar coberto?"
PS_COPA_Q3 = "A coparticipação foi cobrada em:\n\n1️⃣ Consultas\n2️⃣ Exames\n3️⃣ Terapias\n4️⃣ Internação\n5️⃣ Outro"
PS_COPA_Q4 = "Você faz tratamento contínuo?\n\n1️⃣ Sim\n2️⃣ Não"
PS_COPA_Q5 = "Qual tipo de tratamento você faz?"
PS_COPA_Q6 = "Importante você saber: a coparticipação não pode ser ilimitada. A justiça entende que cobrar percentuais muito altos ou taxas sobre internação pode ser considerado abusivo, pois impede o paciente de se tratar."
PS_COPA_Q7 = "Você possui o contrato do plano?\n\n1️⃣ Sim\n2️⃣ Não"

# Novo fluxo pós-contrato - Coparticipação
PS_COPA_VALOR_AUMENTO = "Me informa por favor qual o valor da mensalidade que você costuma pagar e de quanto veio o aumento por causa da coparticipação"

PS_COPA_OBSTACULOS = (
    "É muito comum os planos de saúde criarem obstáculos para limitar a cobertura de tratamentos, "
    "muitas vezes ignorando a prescrição médica através de taxas de coparticipação abusivas. "
    "Eu sei o quanto é desgastante enfrentar essas cobranças inesperadas."
)

PS_COPA_ANALISE = (
    "Analiso situações semelhantes à sua diariamente e posso te afirmar: a maioria dos casos de coparticipação elevada possui solução jurídica. "
    "Existem limites legais que os planos são obrigados a respeitar e, quando essas regras são descumpridas, "
    "é perfeitamente possível reverter os valores ou buscar a restituição. O segredo está em identificar onde o contrato fere os seus direitos."
)

PS_COPA_ESCOLHA = (
    "Agora, para que eu possa te dar o direcionamento correto, escolha a opção que melhor descreve o seu momento atual:\n\n"
    "1️⃣ Já sofro cobranças de coparticipação: Desejo uma análise jurídica para contestar valores que considero abusivos, limitar as cobranças ou buscar a restituição do que foi pago indevidamente.\n\n"
    "2️⃣ Preciso de uma consultoria sobre o contrato: Desejo uma análise técnica para entender as regras de coparticipação do meu plano, ou tratar de outros temas como reajustes, carências e portabilidade.\n\n"
    "Qual dessas opções faz mais sentido para você agora?"
)

PS_COPA_JUDICIALIZAR_1 = (
    "Compreendo. No Direito à Saúde, a imposição de taxas abusivas é o ponto de partida para a nossa intervenção. "
    "Muitas vezes, esse posicionamento da operadora carece de fundamento legal e ignora a soberania da prescrição médica. "
    "Meu papel agora é analisar tecnicamente essa situação para estruturar a medida cabível para o seu caso."
)

PS_COPA_JUDICIALIZAR_2 = (
    "O próximo passo agora é uma reunião rápida para eu te explicar como funciona o processo e valores de honorários.\n\n"
    "Não se preocupe, é uma reunião gratuita e on-line."
)

# ============================================
# 9. ERRO MÉDICO
# ============================================
PS_ERRO_Q1 = "Sinto muito que você esteja passando por isso. Sei que, além da dor física, existe uma quebra de confiança muito grande quando algo não sai como o esperado em um procedimento médico. Estou aqui para te ouvir e entender se houve uma falha que te dá direito à reparação. 💙\n\nO que aconteceu durante o atendimento médico?\n\n1️⃣ Cirurgia\n2️⃣ Atendimento de emergência\n3️⃣ Tratamento contínuo\n4️⃣ Parto\n5️⃣ Outro"
PS_ERRO_Q2 = "O paciente sofreu algum dano?\n\n1️⃣ Agravamento da saúde\n2️⃣ Sequela\n3️⃣ Dor intensa\n4️⃣ Novo procedimento necessário\n5️⃣ Óbito"
PS_ERRO_Q3 = "Eu imagino o quanto esse momento está sendo difícil para você e para sua família. Para que eu possa desenhar a melhor estratégia:\n\nComo esse episódio mudou a sua vida hoje?"
PS_ERRO_Q4 = "Você possui prontuário médico?\n\n1️⃣ Sim\n2️⃣ Não"
PS_ERRO_Q5 = "Outro médico já disse que houve erro ou falha no atendimento?\n\n1️⃣ Sim\n2️⃣ Não"
PS_ERRO_Q6 = "Você sente que houve falta de informação, descaso ou uma falha clara na técnica do médico ou do hospital?"


# Novo fluxo pós-pergunta final - Erro Médico
PS_ERRO_INTRO_DOR = (
    "Eu sei que enfrentar as consequências de um erro médico é uma situação extremamente delicada e dolorosa. "
    "Muitas vezes, o que deveria ser um processo de cura acaba se tornando um trauma por negligência, imprudência ou falha técnica. "
    "O meu papel aqui é garantir que a sua dor e os seus direitos não sejam ignorados."
)

PS_ERRO_ANALISE = (
    "Analiso casos de responsabilidade médica diariamente e posso te afirmar: embora sejam processos complexos, a lei protege rigorosamente o paciente. "
    "Se houve falha no dever de cuidado ou no procedimento, é perfeitamente possível buscar a indenização por danos morais, materiais e estéticos, "
    "além da reparação de todos os prejuízos causados. O segredo está em reunir as provas técnicas corretas para demonstrar a falha do profissional ou do hospital."
)

PS_ERRO_ESCOLHA = (
    "Agora, para que eu possa te dar o direcionamento correto, escolha a opção que melhor descreve o seu momento atual:\n\n"
    "1️⃣ Desejo processar pelo erro ocorrido: Já sofri o dano e busco uma análise jurídica para ingressar com a ação judicial de indenização e reparação de danos.\n\n"
    "2️⃣ Preciso de uma análise sobre o ocorrido: Ainda tenho dúvidas se o que aconteceu no meu caso configura erro médico e quero uma análise técnica do prontuário e dos fatos antes de decidir o que fazer.\n\n"
    "Qual dessas opções faz mais sentido para você agora?"
)

PS_ERRO_JUDICIALIZAR_1 = (
    "Compreendo. No Direito à Saúde, o erro médico é uma das violações mais graves, e a ação judicial é o caminho para buscar justiça e compensação pelo que você passou. "
    "Meu papel agora é analisar tecnicamente os fatos e a documentação para estruturar a estratégia de indenização cabível para o seu caso."
)

PS_ERRO_JUDICIALIZAR_2 = (
    "O próximo passo agora é uma conversa direta comigo para eu te explicar como funciona o processo e os valores de honorários para a sua demanda. "
    "Não se preocupe, essa análise inicial por aqui é gratuita e fundamental para darmos os primeiros passos."
)

PS_ERRO_CONSULTORIA = (
    "Nesta reunião online, faremos um diagnóstico detalhado dos fatos e dos documentos médicos para te entregar um parecer seguro se houve, de fato, falha passível de processo e quais são as suas chances de êxito.\n\n"
    "Informações sobre a Consultoria:\n"
    "• Investimento: R$ 600,00 (referente à análise técnica e reserva de horário).\n"
    "• Duração: Até 1 hora.\n"
    "• Objetivo: Diagnóstico completo e estratégia jurídica personalizada.\n\n"
    "Deseja prosseguir com o agendamento?"
)

PS_ERRO_PAGAMENTO = (
    "Perfeito! Vamos reservar o seu horário.\n\n"
    "Como deseja realizar o investimento do atendimento? Você prefere Pix ou Cartão de Crédito?"
)

PS_ERRO_CONFIRMACAO = "Ao realizar o pagamento e for dado baixa no nosso financeiro, alguém da nossa equipe vai entrar em contato o quanto antes pra marcar seu atendimento na agenda da Dra Lethicia."

# ============================================
# 10. OUTRO (plano) - FLUXO CORRIGIDO
# ============================================
PS_OUTRO_DEMANDA_Q1 = "Entendido! O Direito da Saúde é muito amplo e, se o seu problema envolve o seu bem-estar ou o seu contrato de saúde, você está no lugar certo. 💙\n\nPara que eu possa entender como te ajudar, me conte brevemente o que está acontecendo. O plano de saúde negou algo?"
PS_OUTRO_DEMANDA_Q2 = "Existe algum prazo ou data limite que te preocupa agora (ex: uma cirurgia marcada, um boleto vencendo ou um prazo de defesa)?"
PS_OUTRO_DEMANDA_Q3 = "Você recebeu alguma negativa ou teve dificuldade no atendimento?\n\n1️⃣ Sim\n2️⃣ Não\n3️⃣ Não se encaixa"
PS_OUTRO_DEMANDA_Q4 = "Você tem isso registrado (mensagem, documento, protocolo)?\n\n1️⃣ Sim\n2️⃣ Não\n3️⃣ Não se encaixa"
PS_OUTRO_DEMANDA_Q5 = "Você possui documentos relacionados ao caso?\n\n1️⃣ Sim\n2️⃣ Não"
PS_OUTRO_DEMANDA_Q6 = "Esse problema está afetando sua saúde atualmente?\n\n1️⃣ Sim\n2️⃣ Não"
PS_OUTRO_DEMANDA_Q7 = "Certo, recebi seus detalhes. Independentemente do caso, a minha premissa é sempre a mesma: o contrato de saúde deve servir para proteger a vida e o consumidor, não para criar barreiras."

PS_PONTO_CRITICO = (
    "É muito comum os planos de saúde darem desculpas para não pagar um tratamento, ignorando o que o seu médico pediu. "
    "Eu sei o quanto é angustiante ouvir um 'não' do plano de saúde, principalmente quando estamos falando de {ponto}. "
    "Mas a regra é simples: se o médico disse que você precisa, o plano tem que cobrir. "
    "Como eu trabalho só com casos de saúde, vejo que a gente tem um caminho bem claro para seguir aqui. "
    "O contrato do plano existe para cuidar da sua vida, não para te dar dor de cabeça. "
    "Você sente que eles estão sendo injustos com você?"
)

# ============================================
# MENSAGENS PRÉ-POS BUSCA (2 novas mensagens que antecedem)
# ============================================
MSG_PRE_POS_BUSCA_1 = (
    "Eu analisei muitas situações semelhantes à sua, e posso te dizer com bastante segurança: a maioria dos casos envolvendo plano de saúde tem solução jurídica, mesmo quando o plano tenta negar.\n"
    "Existem regras bem específicas que os planos são obrigados a seguir e, quando descumprem, é possível reverter isso."
)

MSG_PRE_POS_BUSCA_2 = (
    "Aqui no escritório, a gente atua exatamente com esse tipo de situação, tanto na parte de orientação quanto na judicialização, quando necessário.\n"
    "Cada caso tem detalhes importantes que fazem toda a diferença no resultado por isso eu preciso entender exatamente em que momento você está agora."
)

# PS_POS_BUSCA ATUALIZADO (agora com 3 opções)
PS_POS_BUSCA = (
    "Obrigado por todas as informações. Já consigo ter um bom entendimento da sua situação.\n\n"
    "Agora me diz: o que você está buscando nesse momento? Escolha a opção que mais se encaixa com onde você está agora:\n\n"
    "1️⃣ Já tenho a negativa do plano: Desejo orientação especializada para ingressar com a ação judicial e buscar a liberação do meu tratamento.\n\n"
    "2️⃣ Ainda não tenho a negativa, mas preciso me preparar: Quero me antecipar, eu ainda não recebi a negativa do plano, mas sei que meu pedido pode ser recusado. Quero me preparar da forma correta, com orientação jurídica, para aumentar minhas chances de aprovação do tratamento ou sucesso na ação judicial.\n\n"
    "3️⃣ Preciso de uma consultoria jurídica: Desejo uma análise técnica sobre o meu caso de saúde. Indicado para dúvidas sobre reajustes abusivos (anual ou por faixa etária), períodos de carência, migração de plano (portabilidade) ou para saber se um tratamento específico tem cobertura obrigatória."
)

# Mensagens das opções (atualizadas)
PS_OP1_PERGUNTA = (
    "Compreendo. A negativa formal é o ponto de partida para a nossa intervenção estratégica. "
    "No Direito à Saúde, muitas vezes o 'não' da operadora carece de fundamento legal e ignora a soberania da prescrição médica. "
    "Meu papel agora é analisar a fundamentação dessa recusa para estruturar a medida judicial cabível."
)

PS_OP1_REUNIAO = (
    "O próximo passo agora é uma reunião rápida para eu te explicar como funciona o processo e valores de honorários.\n\n"
    "Não se preocupe, é uma reunião gratuita e on-line."
)

PS_OP2_INTRO = (
    "Como você ainda não tem a negativa oficial do plano, você tem dois caminhos possíveis para seguir agora e eu quero te ajudar a escolher o mais seguro:"
)
PS_OP2_CAMINHO_1 = (
    "1️⃣ Você pode tentar solicitar sozinho(a) diretamente ao plano de saúde, buscando a autorização do procedimento, medicamento, cirurgia ou tratamento por conta própria."
)
PS_OP2_CAMINHO_2 = (
    "2️⃣ Ou pode contar com a nossa Assessoria Jurídica desde o início do processo, para que o escritório acompanhe estrategicamente todas as etapas, orientando sobre pedidos, documentos, relatórios médicos, protocolos e a forma correta de conduzir a solicitação perante o plano de saúde.\n\n"
    "Na prática, a segunda opção costuma ser a mais segura e estratégica, porque, com o acompanhamento jurídico desde o começo, conseguimos aumentar a segurança do processo e preparar o caso adequadamente caso seja necessário ingressar judicialmente futuramente."
)
PS_OP2_DECISAO = (
    "Excelente escolha. A assessoria serve justamente para quem não quer correr o risco de negativas por erros na documentação "
    "e deseja que o escritório cuide de toda a parte burocrática e jurídica desde o primeiro dia.\n\n"
    "Atenção: Para esse acompanhamento completo e personalizado, o escritório cobra honorários de assessoria. "
    "Você gostaria de agendar uma reunião para conhecer os valores e como funciona esse suporte jurídico de ponta a ponta?"
)

PS_OP3_CONSULTORIA = (
    "Entendido. Para casos cautelosos com o seu, realizamos uma Consultoria Jurídica.\n\n"
    "Nesta reunião online um advogado especialista em Direito da Saúde analisará detalhadamente o seu caso, documentos e contratos para te entregar um parecer seguro sobre os seus direitos.\n\n"
    "Informações sobre a Consultoria:\n"
    "• Investimento: R$ 500,00 (referente à análise técnica e reserva de horário).\n"
    "• Duração: Até 1 hora.\n"
    "• Objetivo: Diagnóstico completo e estratégia jurídica personalizada.\n\n"
    "Deseja prosseguir com o agendamento?"
)
PS_OP3_PAGAMENTO = (
    "Perfeito! Vamos reservar o seu horário.\n\n"
    "Como deseja realizar o investimento do atendimento? Você prefere Pix ou Cartão de Crédito?"
)
PS_OP3_CONFIRMACAO = "Ao realizar o pagamento e for dado baixa no nosso financeiro, alguém da nossa equipe vai entrar em contato o quanto antes pra marcar seu atendimento na agenda da Dra Lethicia."

# Opção 4 removida - agora temos apenas 3 opções

# Encerramento geral
PS_ENCERRAMENTO = (
    "Entendo perfeitamente e respeito sua decisão.\n\n"
    "Vou encerrar o seu atendimento por aqui para priorizar os casos que já estão com procedimentos em andamento. "
    "Lembre-se apenas que, no Direito da Saúde, o tempo é um fator determinante para o sucesso do tratamento.\n\n"
    "Caso precise de suporte especializado no futuro, nossos canais continuam à disposição."
)

# Decisão compartilhada (ATUALIZADA)
DECISAO_SIM = (
    "Excelente! É fundamental que ele(a) participe, pois como o Direito à Saúde envolve "
    "prazos muito curtos e decisões imediatas sobre o tratamento, é bom que todos "
    "estejam na mesma página.\n\n"
    f"Vamos escolher um horário que fique confortável para vocês dois... "
    f"Logo abaixo vou te mandar a agenda da {L}. Escolha um melhor dia e horário que se encaixe adequadamente na sua agenda.\n\n"
    f"{CALENDLY_LINK}"
)

DECISAO_NAO = (
    "Perfeito, facilita bastante o nosso fluxo. Como você é a única responsável pela decisão, "
    "conseguimos dar um andamento mais ágil aos trabalhos...\n\n"
    f"Logo abaixo vou te mandar a agenda da {L}. Escolha um melhor dia e horário que se encaixe adequadamente na sua agenda.\n\n"
    f"{CALENDLY_LINK}"
)

MSG_FOLLOWUP_LINK = "Estou passando pra saber se você conseguiu acessar o link de agendamento da reunião. Se não conseguiu, basta copiar e colar o link no seu navegador."

DECISAO_REPASSE = (
    "Entendo! Olha, eu sugiro fortemente que ele tente participar, nem que seja apenas "
    "nos primeiros 10 minutos. No Direito à Saúde, os detalhes técnicos sobre a negativa da operadora "
    "costumam gerar muitas dúvidas e, se ele ouvir direto de mim, vocês ganham muito mais segurança para decidir rápido.\n\n"
    "Conseguimos um horário em que ele possa entrar na chamada, ou prefere manter só entre nós por enquanto?"
)

DECISAO_REPASSE_SIM = f"Perfeito! Vamos agendar para vocês dois. Logo abaixo vou te mandar a agenda da {L}. Escolha um melhor dia e horário que se encaixe adequadamente na sua agenda.\n\n{CALENDLY_LINK}"

DECISAO_REPASSE_NAO = f"Entendido! Mantemos só entre nós. Logo abaixo vou te mandar a agenda da {L}. Escolha um melhor dia e horário que se encaixe adequadamente na sua agenda.\n\n{CALENDLY_LINK}"

MSG_AGENDAMENTO_FINALIZADO = (
    "Perfeito. Todas as informações foram registradas com sucesso. A partir de agora, nossa equipe interna assume o acompanhamento para garantir que tudo esteja pronto para o seu atendimento. Tenha um excelente dia e até breve!"
)

MSG_DOCS_INSUFICIENTES = (
    "Entendi sua situação. Para que eu consiga te ajudar judicialmente a conseguir seu atendimento no SUS, "
    "o juiz exige obrigatoriamente alguns documentos que comprovam que o Estado está falhando com você.\n\n"
    "Sem um laudo médico atualizado e o comprovante de inscrição na fila de espera, o processo corre o risco de ser negado logo no início.\n\n"
    "Minha orientação agora: vá até a unidade de saúde, peça a atualização do seu laudo e tire uma foto do comprovante da fila. "
    "Assim que tiver esses papéis em mãos, me envie aqui para agendarmos nossa reunião de estratégia, combinado?"
)

MSG_AGUARDO_RETORNO = "Aguardo o seu retorno o mais breve possível. Até mais!"

MSG_NEG_MATERIAL = "O seu caso foi negado a cirurgia ou algum material/prótese/órtese essencial pra que seja realizada?"


# ============================================
# HELPER: SUS - identificar falta de documentos essenciais
# ============================================
def _resposta_negativa_docs_sus(txt: str) -> bool:
    """Detecta respostas negativas relacionadas a laudo, exame, comprovante, fila, receita ou relatório."""
    n = _n(txt)
    negativos = [
        "não", "nao", "não tenho", "nao tenho", "não possuo", "nao possuo",
        "sem", "não fiz", "nao fiz", "não peguei", "nao peguei",
        "não tenho foto", "nao tenho foto", "não tenho print", "nao tenho print",
        "não tenho comprovante", "nao tenho comprovante", "não tenho laudo", "nao tenho laudo",
        "não tenho exame", "nao tenho exame", "não tenho exames", "nao tenho exames",
        "não tenho relatório", "nao tenho relatorio", "não tenho receita", "nao tenho receita"
    ]
    return any(x in n for x in negativos)

def _pergunta_docs_sus(txt: str) -> bool:
    """Identifica perguntas do SUS que tratam de documentos/provas essenciais."""
    n = _n(txt)
    chaves = [
        "laudo", "relatório", "relatorio", "exame", "exames", "receita",
        "comprovante", "fila", "sisreg", "meu sus", "print", "protocolo",
        "encaminhamento", "pedido médico", "pedido/encaminhamento", "biópsia", "biopsia"
    ]
    return any(c in n for c in chaves)

def _sus_docs_insuficientes(prefixo_resp: str, perguntas=None) -> bool:
    """
    Retorna True quando a maior parte das respostas às perguntas documentais do SUS
    indica ausência de laudo, exames, comprovante de fila, receita, pedido ou protocolo.
    """
    if perguntas is None:
        perguntas = st.session_state.perguntas_ativas
    total_docs = 0
    negativas_docs = 0
    for i, pergunta in enumerate(perguntas or []):
        if _pergunta_docs_sus(pergunta):
            total_docs += 1
            if _resposta_negativa_docs_sus(st.session_state.dados.get(f"{prefixo_resp}{i}", "")):
                negativas_docs += 1
    return total_docs > 0 and negativas_docs >= max(1, (total_docs // 2) + (total_docs % 2))

def _encaminhar_docs_insuficientes_sus():
    st.session_state.estado = "SUS_DOCS_INSUF"
    add_bot(MSG_DOCS_INSUFICIENTES)

# ============================================
# HELPER: detectar pergunta sobre valores
# ============================================
def _e_pergunta_valor(r: str) -> bool:
    texto = _n(r)
    palavras = [
        "valor", "quanto é", "quanto e", "quanto custa", "preço", "preco",
        "custa", "honorário", "honorario", "investimento", "cobram",
        "custo", "quanto é pago", "quanto e pago", "quanto pago", "é pago", "e pago"
    ]
    return any(p in texto for p in palavras)

def _contexto_valor_analise_inicial() -> bool:
    dados = st.session_state.dados
    estado = st.session_state.estado
    canal = dados.get("canal")
    situacao = _n(dados.get("situacao", ""))
    subtipo = _n(dados.get("subtipo", ""))
    tipo = _n(dados.get("tipo", ""))

    # Casos do SUS: consultas e exames.
    if canal == "SUS" and (
        tipo == "consulta_exame"
        or subtipo in ("consulta", "exame")
        or estado.startswith("SUS_CONSULTA")
        or estado.startswith("SUS_EXAME")
    ):
        return True

    # Casos de Plano de Saúde: exame negado e terapias.
    if canal == "PLANO" and ("exame negado" in situacao or "terapias" in situacao):
        return True

    return False

def _msg_valor():
    dados = st.session_state.dados
    situacao = _n(dados.get("situacao", ""))
    if "reajuste" in situacao or "coparticipação" in situacao or "copa" in situacao:
        return MSG_VALORES_REAJUSTE
    return MSG_VALORES_CIRURGIA

def iniciar_interceptacao_valor_analise():
    st.session_state.estado_antes_valor = st.session_state.estado
    st.session_state.dados_antes_valor = st.session_state.dados.copy()
    st.session_state.mensagem_antes_valor = next(
        (m.get("content") for m in reversed(st.session_state.messages) if m.get("role") == "bot"),
        None
    )
    st.session_state.estado = "PERGUNTA_VALOR_ANALISE"
    add_bot(MSG_VALORES_ANALISE_INICIAL)

def voltar_apos_pergunta_valor(resposta: str):
    if _sim(resposta):
        estado_anterior = st.session_state.estado_antes_valor
        mensagem_anterior = st.session_state.mensagem_antes_valor
        st.session_state.estado = estado_anterior
        if st.session_state.dados_antes_valor:
            st.session_state.dados = st.session_state.dados_antes_valor.copy()
        st.session_state.estado_antes_valor = None
        st.session_state.dados_antes_valor = None
        st.session_state.mensagem_antes_valor = None
        if mensagem_anterior:
            add_bot(mensagem_anterior, delay=0)
        return True
    else:
        add_bot(PS_ENCERRAMENTO)
        st.session_state.estado = "FIM"
        st.session_state.estado_antes_valor = None
        st.session_state.dados_antes_valor = None
        st.session_state.mensagem_antes_valor = None
        return False

def iniciar_fluxo_orientacao_97():
    """Inicia o pré-fluxo obrigatório antes da mensagem de consulta paga de R$ 97,00."""
    add_bot(PS_CONSULTA_ORIENTACAO_INTRO)
    st.session_state.estado = "PS_CONSULTA_97_DECISAO"
    add_bot(PS_CONSULTA_ORIENTACAO_OPCOES)

def iniciar_fluxo_reparadora_97():
    """Inicia o pré-fluxo específico de reparadoras antes da consulta paga de R$ 97,00."""
    add_bot(PS_REP_ORIENTACAO_INTRO)
    st.session_state.estado = "PS_CONSULTA_97_DECISAO"
    add_bot(PS_REP_ORIENTACAO_OPCOES)

# Função para obter nome da especialidade (não o número)
def get_nome_especialidade(valor):
    mapa = {
        "1": "Endometriose",
        "2": "Bariátrica", 
        "3": "Oncologia (câncer)",
        "4": "Cardiologia",
        "5": "Neurocirurgia",
        "6": "Ortopedia",
        "7": "Oftalmologia",
        "8": "OUTRO"
    }
    return mapa.get(valor, valor)

# ============================================
# PROCESSAMENTO DO FLUXO
# ============================================

def processar(resposta: str):
    estado = st.session_state.estado
    dados  = st.session_state.dados

    # Atualiza timestamp da última resposta do usuário
    st.session_state.aguardando_resposta_desde = None

    # Verificar se é pergunta sobre resultados (prioridade)
    if estado not in ("INICIO", "PERGUNTA_RESULTADOS") and verificar_pergunta_resultados(resposta):
        processar_pergunta_resultados(resposta)
        return

    # Estado especial para resposta da pergunta sobre resultados
    if estado == "PERGUNTA_RESULTADOS":
        voltar_apos_pergunta_resultados(resposta)
        return

    # Estado especial para resposta da pergunta sobre valores em fluxos específicos
    if estado == "PERGUNTA_VALOR_ANALISE":
        voltar_apos_pergunta_valor(resposta)
        return

    # Interceptar perguntas de valor em qualquer estado (exceto INICIO)
    if estado not in ("INICIO", "FIM", "PERGUNTA_VALOR_ANALISE") and _e_pergunta_valor(resposta):
        if _contexto_valor_analise_inicial():
            iniciar_interceptacao_valor_analise()
        else:
            add_bot(_msg_valor())
        return

    # ========== INICIO ==========
    if estado == "INICIO":
        st.session_state.nome = resposta
        dados["nome"] = resposta
        st.session_state.estado = "CANAL"
        add_bot(MSG_CANAL.format(nome=resposta))

    # ========== CANAL ==========
    elif estado == "CANAL":
        if "sus" in _n(resposta):
            dados["canal"] = "SUS"
            st.session_state.estado = "SUS_DEMANDA"
            add_bot(MSG_SUS_DEMANDA)
        else:
            dados["canal"] = "PLANO"
            st.session_state.estado = "PS_TEMPO"
            add_bot(PS_TEMPO)

    # =====================================================================
    # SUS
    # =====================================================================

    elif estado == "SUS_DEMANDA":
        if "cirurgia" in _n(resposta) or "tratamento" in _n(resposta):
            dados["tipo"] = "cirurgia"
            st.session_state.estado = "SUS_ESPECIALIDADE"
            add_bot(MSG_SUS_ESPECIALIDADE)
        else:
            dados["tipo"] = "consulta_exame"
            st.session_state.estado = "SUS_CONSULTA_EXAME_TIPO"
            add_bot(MSG_SUS_CONSULTA_EXAME)

    # ---- SUS CONSULTA/EXAME ----
    elif estado == "SUS_CONSULTA_EXAME_TIPO":
        if "2" in resposta or "exame" in _n(resposta):
            dados["subtipo"] = "exame"
            st.session_state.estado = "SUS_EXAME_Q1"
            add_bot(MSG_SUS_EXAME_Q1)
        else:
            dados["subtipo"] = "consulta"
            st.session_state.estado = "SUS_CONSULTA_Q1"
            add_bot(MSG_SUS_CONSULTA_Q1)

    # FLUXO CONSULTA
    elif estado == "SUS_CONSULTA_Q1":
        dados["consulta_q1"] = resposta
        st.session_state.estado = "SUS_CONSULTA_Q2"
        add_bot(MSG_SUS_CONSULTA_Q2)
    elif estado == "SUS_CONSULTA_Q2":
        dados["consulta_q2"] = resposta
        st.session_state.estado = "SUS_CONSULTA_Q3"
        add_bot(MSG_SUS_CONSULTA_Q3)
    elif estado == "SUS_CONSULTA_Q3":
        dados["consulta_q3"] = resposta
        st.session_state.estado = "SUS_CONSULTA_PITCH"
        add_bot(MSG_SUS_CONSULTA_PITCH)
    elif estado == "SUS_CONSULTA_PITCH":
        if "aguardar" in _n(resposta) or "não" in _n(resposta):
            add_bot(MSG_ENCERRAMENTO_SUS)
            st.session_state.estado = "FIM"
        else:
            st.session_state.estado = "SUS_CONSULTA_AJUDA_Q1"
            add_bot(MSG_SUS_CONSULTA_AJUDA_Q1)
    elif estado == "SUS_CONSULTA_AJUDA_Q1":
        dados["consulta_tempo"] = resposta
        st.session_state.estado = "SUS_CONSULTA_AJUDA_Q2"
        add_bot(MSG_SUS_CONSULTA_AJUDA_Q2)
    elif estado == "SUS_CONSULTA_AJUDA_Q2":
        dados["consulta_info_fila"] = resposta
        st.session_state.estado = "SUS_CONSULTA_AJUDA_Q3"
        add_bot(MSG_SUS_CONSULTA_AJUDA_Q3)
    elif estado == "SUS_CONSULTA_AJUDA_Q3":
        dados["consulta_exame"] = resposta
        st.session_state.estado = "SUS_CONSULTA_AJUDA_Q4"
        add_bot(MSG_SUS_CONSULTA_AJUDA_Q4)
    elif estado == "SUS_CONSULTA_AJUDA_Q4":
        dados["consulta_docs"] = resposta
        st.session_state.estado = "SUS_CONSULTA_AJUDA_Q4B"
        add_bot(MSG_SUS_CONSULTA_AJUDA_Q4B)
    elif estado == "SUS_CONSULTA_AJUDA_Q4B":
        dados["consulta_pedido"] = resposta
        consulta_docs_negativos = sum(
            1 for chave in ("consulta_docs", "consulta_pedido")
            if _resposta_negativa_docs_sus(dados.get(chave, ""))
        )
        if consulta_docs_negativos >= 1:
            _encaminhar_docs_insuficientes_sus()
        else:
            st.session_state.estado = "SUS_CONSULTA_PROTOCOLO"
            add_bot(MSG_SUS_CONSULTA_PROTOCOLO)
    elif estado == "SUS_CONSULTA_PROTOCOLO":
        if _sim(resposta):
            st.session_state.estado = "SUS_CONSULTA_HONORARIOS"
            add_bot("Como é um trabalho de alta especialidade, o escritório cobra Honorários Iniciais para assumir o caso e protocolar o pedido judicial. Prosseguir com esse caso faz sentido para você garantir sua saúde hoje e sair dessa espera?")
        else:
            add_bot(MSG_ENCERRAMENTO_SUS)
            st.session_state.estado = "FIM"
    elif estado == "SUS_CONSULTA_HONORARIOS":
        if _sim(resposta):
            add_bot("Ótimo. Isso mostra que você prioriza sua saúde acima da burocracia do Estado.\n\nVou encaminhar seus dados para a mesa da Dra. Lethicia neste momento. Em instantes, ela entrará em contato aqui por este chat para te passar a estratégia de liberação e os valores para o seu caso. Fique atento(a)!")
        else:
            add_bot("Compreendo. Infelizmente, sem o interesse em avançar com uma medida judicial, o seu caso continuará dependendo exclusivamente da velocidade da fila do SUS, que como sabemos, não tem previsão.\n\nComo o escritório da Dra. Lethicia foca apenas em quem deseja forçar a solução imediata, estamos encerrando seu atendimento por aqui.\n\nCaso a sua situação se agrave ou você decida que não pode mais esperar, sinta-se à vontade para retornar. Desejamos sorte no seu tratamento.")
        st.session_state.estado = "FIM"

    # FLUXO EXAME
    elif estado == "SUS_EXAME_Q1":
        dados["exame_nome"] = resposta
        st.session_state.estado = "SUS_EXAME_TIPO"
        add_bot(MSG_SUS_EXAME_TIPO)
    elif estado == "SUS_EXAME_TIPO":
        if "1" in resposta or "diagnóstico" in _n(resposta):
            dados["exame_tipo"] = "diagnostico"
            st.session_state.perguntas_ativas = PERGUNTAS_EXAME_DIAGNOSTICO.copy()
        elif "2" in resposta or "pré" in _n(resposta):
            dados["exame_tipo"] = "preop"
            st.session_state.perguntas_ativas = PERGUNTAS_EXAME_PREOP.copy()
        else:
            dados["exame_tipo"] = "confirmacao"
            st.session_state.perguntas_ativas = PERGUNTAS_EXAME_CONFIRMACAO.copy()
        st.session_state.pergunta_idx = 0
        st.session_state.estado = "SUS_EXAME_PERGUNTAS"
        add_bot(st.session_state.perguntas_ativas[0])
    elif estado == "SUS_EXAME_PERGUNTAS":
        idx = st.session_state.pergunta_idx
        dados[f"exame_resp_{idx}"] = resposta
        idx += 1
        st.session_state.pergunta_idx = idx
        if idx < len(st.session_state.perguntas_ativas):
            add_bot(st.session_state.perguntas_ativas[idx])
        else:
            if _sus_docs_insuficientes("exame_resp_"):
                _encaminhar_docs_insuficientes_sus()
            else:
                st.session_state.estado = "SUS_EXAME_PITCH"
                add_bot(MSG_SUS_EXAME_PITCH)
    elif estado == "SUS_EXAME_PITCH":
        if "aguardar" in _n(resposta) or "não" in _n(resposta):
            add_bot(MSG_ENCERRAMENTO_SUS)
            st.session_state.estado = "FIM"
        else:
            st.session_state.estado = "SUS_EXAME_PROTOCOLO"
            add_bot(MSG_SUS_EXAME_PROTOCOLO)
    elif estado == "SUS_EXAME_PROTOCOLO":
        if _sim(resposta):
            st.session_state.estado = "SUS_EXAME_HONORARIOS"
            add_bot("Como é um trabalho de alta especialidade, o escritório cobra Honorários Iniciais para assumir o caso e protocolar o pedido judicial. Prosseguir com esse caso faz sentido para você garantir sua saúde hoje e sair dessa espera?")
        else:
            add_bot(MSG_ENCERRAMENTO_SUS)
            st.session_state.estado = "FIM"
    elif estado == "SUS_EXAME_HONORARIOS":
        if _sim(resposta):
            add_bot("Ótimo. Isso mostra que você prioriza sua saúde acima da burocracia do Estado.\n\nVou encaminhar seus dados para a mesa da Dra. Lethicia neste momento. Em instantes, ela entrará em contato aqui por este chat para te passar a estratégia de liberação e os valores para o seu caso. Fique atento(a)!")
        else:
            add_bot("Compreendo. Infelizmente, sem o interesse em avançar com uma medida judicial, o seu caso continuará dependendo exclusivamente da velocidade da fila do SUS, que como sabemos, não tem previsão.\n\nComo o escritório da Dra. Lethicia foca apenas em quem deseja forçar a solução imediata, estamos encerrando seu atendimento por aqui.\n\nCaso a sua situação se agrave ou você decida que não pode mais esperar, sinta-se à vontade para retornar. Desejamos sorte no seu tratamento.")
        st.session_state.estado = "FIM"

    # ---- SUS CIRURGIA ----
    elif estado == "SUS_ESPECIALIDADE":
        if "oncologia" in _n(resposta) or "1" in resposta:
            st.session_state.perguntas_ativas = PERGUNTAS_ONCOLOGIA.copy()
            dados["especialidade"] = "Oncologia"
        elif "neuro" in _n(resposta) and ("tea" in _n(resposta) or "tdah" in _n(resposta) or "diverg" in _n(resposta) or "2" in resposta):
            st.session_state.perguntas_ativas = PERGUNTAS_NEURO.copy()
            dados["especialidade"] = "Neurodivergências"
        elif "endometriose" in _n(resposta) or "adenomiose" in _n(resposta) or "3" in resposta:
            st.session_state.perguntas_ativas = PERGUNTAS_ENDOMETRIOSE.copy()
            dados["especialidade"] = "Endometriose"
        elif "medicamento" in _n(resposta) or "4" in resposta:
            st.session_state.perguntas_ativas = PERGUNTAS_MEDICAMENTO_SUS.copy()
            dados["especialidade"] = "Medicamento"
        elif "bariátrica" in _n(resposta) or "bariatrica" in _n(resposta) or "5" in resposta:
            st.session_state.perguntas_ativas = PERGUNTAS_BARIATRICA_SUS.copy()
            dados["especialidade"] = "Bariátrica"
        elif "neurologia" in _n(resposta) or "neurocirurgia" in _n(resposta) or "6" in resposta:
            st.session_state.perguntas_ativas = PERGUNTAS_NEUROLOGIA_SUS.copy()
            dados["especialidade"] = "Neurologia"
        elif "cardiologia" in _n(resposta) or "7" in resposta:
            st.session_state.perguntas_ativas = PERGUNTAS_CARDIOLOGIA_SUS.copy()
            dados["especialidade"] = "Cardiologia"
        else:
            st.session_state.perguntas_ativas = PERGUNTAS_OUTROS_SUS.copy()
            dados["especialidade"] = "Outros"

        st.session_state.pergunta_idx = 0
        st.session_state.estado = "SUS_PERGUNTAS"
        add_bot(st.session_state.perguntas_ativas[0])

    elif estado == "SUS_PERGUNTAS":
        idx = st.session_state.pergunta_idx
        dados[f"resp_{idx}"] = resposta
        idx += 1
        st.session_state.pergunta_idx = idx
        
        # Verificar se é oncologia e precisa pular a pergunta dos 60 dias se benigno
        especialidade = dados.get("especialidade", "")
        is_oncologia = "oncologia" in _n(especialidade)
        
        if is_oncologia and idx == 5:  # Índice da pergunta dos 60 dias
            # Verificar se o câncer é maligno (resposta da pergunta 1 - benigno/maligno)
            resp_benigno_maligno = _n(dados.get("resp_1", ""))
            if "benigno" in resp_benigno_maligno or "benigna" in resp_benigno_maligno:
                # Pular a pergunta dos 60 dias
                idx += 1
                st.session_state.pergunta_idx = idx
        
        if idx < len(st.session_state.perguntas_ativas):
            next_q = st.session_state.perguntas_ativas[idx]
            add_bot(next_q)
            if is_oncologia and idx == 1:
                st.session_state.estado = "SUS_ONCOLOGIA_BENIGNO_MALIGNO"
                return
        else:
            if _sus_docs_insuficientes("resp_"):
                _encaminhar_docs_insuficientes_sus()
            else:
                st.session_state.estado = "POS_PERGUNTAS_SUS"
                add_bot(MSG_POS_PERGUNTAS_SUS.replace("{nome}", st.session_state.nome or ""))

    elif estado == "SUS_ONCOLOGIA_BENIGNO_MALIGNO":
        dados[f"resp_{st.session_state.pergunta_idx}"] = resposta
        idx = st.session_state.pergunta_idx + 1
        # Se for benigno, pular a pergunta dos 60 dias
        if "benigno" in _n(resposta):
            idx += 1
        st.session_state.pergunta_idx = idx
        st.session_state.estado = "SUS_PERGUNTAS"
        if idx < len(st.session_state.perguntas_ativas):
            add_bot(st.session_state.perguntas_ativas[idx])
        else:
            if _sus_docs_insuficientes("resp_"):
                _encaminhar_docs_insuficientes_sus()
            else:
                st.session_state.estado = "POS_PERGUNTAS_SUS"
                add_bot(MSG_POS_PERGUNTAS_SUS.replace("{nome}", st.session_state.nome or ""))

    elif estado == "POS_PERGUNTAS_SUS":
        dados["sentimento"] = resposta
        if _sus_docs_insuficientes("resp_"):
            _encaminhar_docs_insuficientes_sus()
        else:
            st.session_state.estado = "PROPOSTA_SUS"
            add_bot(MSG_EXPLICACAO_SUS)

    elif estado == "SUS_DOCS_INSUF":
        n = _n(resposta)
        if "certo" in n or "vou fazer" in n or "ok" in n or "sim" in n or _sim(resposta):
            add_bot(MSG_AGUARDO_RETORNO)
        else:
            add_bot(MSG_AGUARDO_RETORNO)
        st.session_state.estado = "FIM"

    elif estado == "PROPOSTA_SUS":
        if _sim(resposta):
            st.session_state.estado = "HONORARIOS_SUS"
            add_bot(MSG_HONORARIOS_SUS)
        else:
            add_bot(MSG_ENCERRAMENTO_SUS)
            st.session_state.estado = "FIM"

    elif estado == "HONORARIOS_SUS":
        if _sim(resposta):
            add_bot(MSG_REVERTER_SUS)
            st.session_state.estado = "DECISAO_COMPARTILHADA"
            add_bot(MSG_SIM_HONORARIOS_SUS_DECISAO)
        else:
            add_bot(MSG_ENCERRAMENTO_SUS)
            st.session_state.estado = "FIM"

    # =====================================================================
    # PLANO DE SAÚDE
    # =====================================================================

    elif estado == "PS_TEMPO":
        if _sim(resposta):
            dados["plano_2anos"] = "sim"
            dados["plano_tipo"] = "mais_de_2_anos"
            st.session_state.estado = "PS_SITUACAO"
            add_bot(PS_SITUACAO)
        else:
            dados["plano_2anos"] = "nao"
            st.session_state.estado = "PS_TEMPO_NAO_SEGUIMENTO"
            add_bot(PS_TEMPO_NAO_SEGUIMENTO)

    # NOVO: Pergunta sobre tipo de plano (pessoa física ou empresarial) após NÃO
    elif estado == "PS_TEMPO_NAO_SEGUIMENTO":
        dados["plano_tipo_resposta"] = resposta
        if "empresarial" in _n(resposta) or "cnpj" in _n(resposta):
            # Trata como SIM (mais de 2 anos)
            dados["plano_tipo"] = "empresarial"
            st.session_state.estado = "PS_SITUACAO"
            add_bot(PS_SITUACAO)
        else:
            # Pessoa física - continua como NÃO
            dados["plano_tipo"] = "pessoa_fisica"
            st.session_state.estado = "PS_NAO_2ANOS_EDUCACAO"
            add_bot(PS_NAO_2ANOS_EDUCACAO)

    # Caminho NÃO
    elif estado == "PS_NAO_2ANOS_EDUCACAO":
        st.session_state.estado = "PS_NAO_2ANOS_Q1"
        add_bot(PS_NAO_2ANOS_Q1)
    elif estado == "PS_NAO_2ANOS_Q1":
        dados["tratamento"] = resposta
        st.session_state.estado = "PS_NAO_2ANOS_Q2"
        add_bot(PS_NAO_2ANOS_Q2)
    elif estado == "PS_NAO_2ANOS_Q2":
        dados["urgencia_comentario"] = resposta
        st.session_state.estado = "PS_NAO_2ANOS_FEEDBACK"
        add_bot(PS_NAO_2ANOS_FEEDBACK)
    elif estado == "PS_NAO_2ANOS_FEEDBACK":
        st.session_state.estado = "PS_NAO_2ANOS_Q3"
        add_bot(PS_NAO_2ANOS_Q3)
    elif estado == "PS_NAO_2ANOS_Q3":
        dados["urgencia_medica"] = resposta
        st.session_state.estado = "PS_NAO_2ANOS_Q4"
        add_bot(PS_NAO_2ANOS_Q4)
    elif estado == "PS_NAO_2ANOS_Q4":
        dados["conhecia_doenca"] = resposta
        st.session_state.estado = "PS_NAO_2ANOS_Q5"
        add_bot(PS_NAO_2ANOS_Q5)
    elif estado == "PS_NAO_2ANOS_Q5":
        dados["negou_carencia"] = resposta
        st.session_state.estado = "PS_NAO_2ANOS_Q6"
        add_bot(PS_NAO_2ANOS_Q6)
    elif estado == "PS_NAO_2ANOS_Q6":
        dados["negativa_escrita"] = resposta
        # Envia mensagens pré-pos busca
        add_bot(MSG_PRE_POS_BUSCA_1)
        add_bot(MSG_PRE_POS_BUSCA_2)
        st.session_state.estado = "PS_POS_BUSCA"
        add_bot(PS_POS_BUSCA)

    # Caminho SIM - Situação
    elif estado == "PS_SITUACAO":
        dados["situacao"] = resposta
        resp_n = _n(resposta)
        opcao = _opcao_numero(resposta)

        # Nova numeração da pergunta principal de Plano de Saúde:
        # 0 Reparadora | 1 Negativa de cirurgia | 2 Medicamento | 3 Exame |
        # 4 Home care | 5 Terapias | 6 Reajuste | 7 Coparticipação |
        # 8 Erro médico | 9 OUTRO
        if opcao == "9" or "outro" in resp_n:
            dados["situacao"] = "outro"
            st.session_state.estado = "PS_OUTRO_DEMANDA"
            st.session_state.outro_idx = 0
            add_bot(PS_OUTRO_DEMANDA_Q1)

        elif opcao == "0" or "reparadora" in resp_n:
            dados["situacao"] = "reparadora"
            st.session_state.estado = "PS_REP_Q1"
            add_bot(PS_REP_Q1)

        elif opcao == "1" or "negativa" in resp_n:
            dados["situacao"] = "negativa de cirurgia"
            st.session_state.estado = "PS_NEG_CIR_ESP"
            add_bot(PS_NEG_CIR_ESP)

        elif opcao == "2" or "medicamento" in resp_n:
            dados["situacao"] = "medicamento negado"
            st.session_state.perguntas_ativas = [
                PS_MED_Q1, PS_MED_Q2, PS_MED_Q3, PS_MED_Q4, PS_MED_Q5,
                PS_MED_Q6, PS_MED_Q7, PS_MED_Q9, PS_MED_Q10
            ]
            st.session_state.pergunta_idx = 0
            st.session_state.estado = "PS_PERGUNTAS_COLETOR"
            add_bot(PS_MED_Q1)

        elif opcao == "3" or "exame" in resp_n:
            dados["situacao"] = "exame negado"
            st.session_state.perguntas_ativas = [
                PS_EXAME_Q1, PS_EXAME_Q2, PS_EXAME_Q3_E_Q4,
                PS_EXAME_Q5, PS_EXAME_Q6, PS_EXAME_Q7
            ]
            st.session_state.pergunta_idx = 0
            st.session_state.estado = "PS_PERGUNTAS_COLETOR"
            add_bot(PS_EXAME_Q1)

        elif opcao == "4" or "home" in resp_n:
            dados["situacao"] = "home care"
            st.session_state.perguntas_ativas = [
                PS_HOME_Q1, PS_HOME_Q2, PS_HOME_Q3, PS_HOME_Q4,
                PS_HOME_Q5, PS_HOME_Q6, PS_HOME_Q7
            ]
            st.session_state.pergunta_idx = 0
            st.session_state.estado = "PS_PERGUNTAS_COLETOR"
            add_bot(PS_HOME_Q1)

        elif opcao == "5" or "terapia" in resp_n:
            dados["situacao"] = "terapias"
            st.session_state.perguntas_ativas = [
                PS_TERA_Q1, PS_TERA_Q2, PS_TERA_Q3, PS_TERA_Q4,
                PS_TERA_Q5, PS_TERA_Q6, PS_TERA_Q7
            ]
            st.session_state.pergunta_idx = 0
            st.session_state.estado = "PS_PERGUNTAS_COLETOR"
            add_bot(PS_TERA_Q1)

        elif opcao == "6" or "reajuste" in resp_n:
            dados["situacao"] = "reajuste"
            st.session_state.perguntas_ativas = [
                PS_REAJ_Q1, PS_REAJ_Q2, PS_REAJ_Q3, PS_REAJ_Q4,
                PS_REAJ_Q5, PS_REAJ_Q6, PS_REAJ_Q7, PS_REAJ_Q8
            ]
            st.session_state.pergunta_idx = 0
            st.session_state.estado = "PS_PERGUNTAS_COLETOR"
            add_bot(PS_REAJ_Q1)

        elif opcao == "7" or "copart" in resp_n:
            dados["situacao"] = "coparticipação elevada"
            st.session_state.perguntas_ativas = [
                PS_COPA_Q1, PS_COPA_Q2, PS_COPA_Q3, PS_COPA_Q4,
                PS_COPA_Q5, PS_COPA_Q6, PS_COPA_Q7
            ]
            st.session_state.pergunta_idx = 0
            st.session_state.estado = "PS_PERGUNTAS_COLETOR"
            add_bot(PS_COPA_Q1)

        elif opcao == "8" or "erro" in resp_n:
            dados["situacao"] = "erro médico"
            st.session_state.perguntas_ativas = [
                PS_ERRO_Q1, PS_ERRO_Q2, PS_ERRO_Q3,
                PS_ERRO_Q4, PS_ERRO_Q5, PS_ERRO_Q6
            ]
            st.session_state.pergunta_idx = 0
            st.session_state.estado = "PS_PERGUNTAS_COLETOR"
            add_bot(PS_ERRO_Q1)

        else:
            dados["situacao"] = "outro"
            st.session_state.estado = "PS_OUTRO_DEMANDA"
            st.session_state.outro_idx = 0
            add_bot(PS_OUTRO_DEMANDA_Q1)

    # FLUXO OUTRO CORRIGIDO
    elif estado == "PS_OUTRO_DEMANDA":
        idx = st.session_state.get("outro_idx", 0)
        dados[f"outro_{idx}"] = resposta
        idx += 1
        st.session_state.outro_idx = idx
        
        outro_qs = [
            PS_OUTRO_DEMANDA_Q2, PS_OUTRO_DEMANDA_Q3, PS_OUTRO_DEMANDA_Q4,
            PS_OUTRO_DEMANDA_Q5, PS_OUTRO_DEMANDA_Q6, PS_OUTRO_DEMANDA_Q7
        ]
        
        if idx < len(outro_qs) + 1:  # +1 porque Q1 já foi enviada
            q = outro_qs[idx - 1] if idx - 1 < len(outro_qs) else None
            if q:
                add_bot(q)
                if q == PS_OUTRO_DEMANDA_Q7:
                    # Após última pergunta, envia mensagens pré-pos busca
                    add_bot(MSG_PRE_POS_BUSCA_1)
                    add_bot(MSG_PRE_POS_BUSCA_2)
                    st.session_state.estado = "PS_POS_BUSCA"
                    add_bot(PS_POS_BUSCA)
        else:
            add_bot(MSG_PRE_POS_BUSCA_1)
            add_bot(MSG_PRE_POS_BUSCA_2)
            st.session_state.estado = "PS_POS_BUSCA"
            add_bot(PS_POS_BUSCA)

    # Coletor genérico
    elif estado == "PS_PERGUNTAS_COLETOR":
        idx = st.session_state.pergunta_idx
        pergunta_atual = st.session_state.perguntas_ativas[idx] if idx < len(st.session_state.perguntas_ativas) else ""
        dados[f"resp_{idx}"] = resposta
        idx += 1
        st.session_state.pergunta_idx = idx

        # Regra global - Plano de Saúde:
        # Sempre que a pessoa responder à pergunta "A negativa do plano foi por escrita ou verbal...",
        # o robô deve AGUARDAR essa resposta e, somente depois, perguntar o motivo da negativa.
        if "escrita ou verbal" in _n(pergunta_atual):
            st.session_state.estado = "PS_MOTIVO_NEGATIVA_GERAL"
            add_bot(PS_MOTIVO_NEGATIVA_GERAL)
            return

        if idx < len(st.session_state.perguntas_ativas):
            add_bot(st.session_state.perguntas_ativas[idx])
        else:
            # Fluxo específico de Reajuste: após responder sobre contrato do plano,
            # segue para escolha entre judicialização ou consultoria.
            if "reajuste" in _n(dados.get("situacao", "")):
                add_bot(PS_REAJ_INTRO_ABUSIVO)
                add_bot(PS_REAJ_ANALISE)
                st.session_state.estado = "PS_REAJ_ESCOLHA"
                add_bot(PS_REAJ_ESCOLHA)
                return

            # Fluxo específico de Coparticipação: após responder sobre contrato do plano,
            # pergunta valores e segue para escolha entre judicialização ou consultoria.
            if "copart" in _n(dados.get("situacao", "")):
                st.session_state.estado = "PS_COPA_VALOR_AUMENTO"
                add_bot(PS_COPA_VALOR_AUMENTO)
                return

            # Fluxo específico de Erro Médico: após responder sobre falha/descaso/técnica,
            # segue para escolha entre judicialização ou análise técnica.
            if "erro" in _n(dados.get("situacao", "")):
                add_bot(PS_ERRO_INTRO_DOR)
                add_bot(PS_ERRO_ANALISE)
                st.session_state.estado = "PS_ERRO_ESCOLHA"
                add_bot(PS_ERRO_ESCOLHA)
                return

            # Enviar mensagem "ponto crítico" usando nome da especialidade
            situacao_raw = dados.get("situacao", "")
            situacao_n = _n(situacao_raw)
            ponto = dados.get("neg_cir_esp", situacao_raw) or situacao_raw
            nome_ponto = get_nome_especialidade(ponto) if ponto in [str(i) for i in range(1,9)] else ponto
            if not st.session_state.get("ponto_critico_enviado", False):
                add_bot(PS_PONTO_CRITICO.format(ponto=nome_ponto))
                st.session_state.ponto_critico_enviado = True
            # IMPORTANTE: após essa mensagem, o robô deve aguardar a resposta do cliente
            # antes de seguir para negativa de material ou para o pós-busca.
            st.session_state.estado = "PS_PONTO_CRITICO_AGUARDANDO"

    # ---- REAJUSTE: NOVO FLUXO APÓS CONTRATO ----
    elif estado == "PS_REAJ_ESCOLHA":
        n = _n(resposta)
        opcao = _opcao_numero(resposta)
        if opcao == "1" or "judicial" in n or "judicializar" in n or "aumento" in n or "abusivo" in n:
            add_bot(PS_REAJ_JUDICIALIZAR_1)
            add_bot(PS_REAJ_JUDICIALIZAR_2)
            st.session_state.estado = "DECISAO_COMPARTILHADA"
            add_bot(MSG_SIM_HONORARIOS_SUS_DECISAO)
        elif opcao == "2" or "consultoria" in n or "preventiva" in n or "contrato" in n:
            st.session_state.estado = "PS_REAJ_CONSULTORIA"
            add_bot(PS_REAJ_CONSULTORIA)
        else:
            add_bot(PS_REAJ_ESCOLHA)

    elif estado == "PS_REAJ_CONSULTORIA":
        if _sim(resposta):
            st.session_state.estado = "PS_REAJ_PAGAMENTO"
            add_bot(PS_REAJ_PAGAMENTO)
        else:
            add_bot(PS_ENCERRAMENTO)
            st.session_state.estado = "FIM"

    elif estado == "PS_REAJ_PAGAMENTO":
        if "cartão" in _n(resposta) or "cartao" in _n(resposta):
            add_bot(f"✅ Aqui está o link para pagamento via Cartão de Crédito:\n\n{LINK_CARTAO_500}\n\n{PS_REAJ_CONFIRMACAO}")
            st.session_state.estado = "FIM"
        elif "pix" in _n(resposta):
            add_bot(f"✅ Aqui está o link para pagamento via Pix:\n\n{LINK_PIX_500}\n\n{PS_REAJ_CONFIRMACAO}")
            st.session_state.estado = "FIM"

    # ---- COPARTICIPAÇÃO: NOVO FLUXO APÓS CONTRATO ----
    elif estado == "PS_COPA_VALOR_AUMENTO":
        dados["copa_valor_aumento"] = resposta
        add_bot(PS_COPA_OBSTACULOS)
        add_bot(PS_COPA_ANALISE)
        st.session_state.estado = "PS_COPA_ESCOLHA"
        add_bot(PS_COPA_ESCOLHA)

    elif estado == "PS_COPA_ESCOLHA":
        n = _n(resposta)
        opcao = _opcao_numero(resposta)
        if opcao == "1" or "judicial" in n or "judicializar" in n or "cobrança" in n or "cobranca" in n:
            add_bot(PS_COPA_JUDICIALIZAR_1)
            add_bot(PS_COPA_JUDICIALIZAR_2)
            st.session_state.estado = "DECISAO_COMPARTILHADA"
            add_bot(MSG_SIM_HONORARIOS_SUS_DECISAO)
        elif opcao == "2" or "consultoria" in n or "contrato" in n:
            st.session_state.estado = "PS_OP3_CONSULTORIA"
            add_bot(PS_OP3_CONSULTORIA)
        else:
            add_bot(PS_COPA_ESCOLHA)

    # ---- ERRO MÉDICO: NOVO FLUXO APÓS PERGUNTA FINAL ----
    elif estado == "PS_ERRO_ESCOLHA":
        n = _n(resposta)
        opcao = _opcao_numero(resposta)
        if opcao == "1" or "judicial" in n or "judicializar" in n or "processar" in n or "indenização" in n or "indenizacao" in n:
            add_bot(PS_ERRO_JUDICIALIZAR_1)
            add_bot(PS_ERRO_JUDICIALIZAR_2)
            st.session_state.estado = "DECISAO_COMPARTILHADA"
            add_bot(MSG_SIM_HONORARIOS_SUS_DECISAO)
        elif opcao == "2" or "análise" in n or "analise" in n or "técnica" in n or "tecnica" in n or "consultoria" in n:
            st.session_state.estado = "PS_ERRO_CONSULTORIA"
            add_bot(PS_ERRO_CONSULTORIA)
        else:
            add_bot(PS_ERRO_ESCOLHA)

    elif estado == "PS_ERRO_CONSULTORIA":
        if _sim(resposta):
            st.session_state.estado = "PS_ERRO_PAGAMENTO"
            add_bot(PS_ERRO_PAGAMENTO)
        else:
            add_bot(PS_ENCERRAMENTO)
            st.session_state.estado = "FIM"

    elif estado == "PS_ERRO_PAGAMENTO":
        if "cartão" in _n(resposta) or "cartao" in _n(resposta):
            add_bot(f"✅ Aqui está o link para pagamento via Cartão de Crédito:\n\n{LINK_CARTAO_500}\n\n{PS_ERRO_CONFIRMACAO}")
            st.session_state.estado = "FIM"
        elif "pix" in _n(resposta):
            add_bot(f"✅ Aqui está o link para pagamento via Pix:\n\n{LINK_PIX_500}\n\n{PS_ERRO_CONFIRMACAO}")
            st.session_state.estado = "FIM"

    # ---- MOTIVO DA NEGATIVA APÓS ESCRITA/VERBAL ----
    elif estado == "PS_MOTIVO_NEGATIVA_GERAL":
        dados["motivo_negativa"] = resposta
        idx = st.session_state.pergunta_idx

        # Evita repetir a pergunta de motivo caso ela já exista como próxima pergunta no fluxo.
        while idx < len(st.session_state.perguntas_ativas) and "qual foi o motivo da negativa" in _n(st.session_state.perguntas_ativas[idx]):
            idx += 1
        st.session_state.pergunta_idx = idx

        if idx < len(st.session_state.perguntas_ativas):
            st.session_state.estado = "PS_PERGUNTAS_COLETOR"
            add_bot(st.session_state.perguntas_ativas[idx])
        else:
            situacao_raw = dados.get("situacao", "")
            situacao_n = _n(situacao_raw)
            ponto = dados.get("neg_cir_esp", situacao_raw) or situacao_raw
            nome_ponto = get_nome_especialidade(ponto) if ponto in [str(i) for i in range(1,9)] else ponto
            if not st.session_state.get("ponto_critico_enviado", False):
                add_bot(PS_PONTO_CRITICO.format(ponto=nome_ponto))
                st.session_state.ponto_critico_enviado = True
            st.session_state.estado = "PS_PONTO_CRITICO_AGUARDANDO"

    # ---- REPARADORA (ATUALIZADA) ----
    elif estado == "PS_REP_Q1":
        dados["rep_q1"] = resposta
        st.session_state.estado = "PS_REP_Q2"
        add_bot(PS_REP_Q2)
    elif estado == "PS_REP_Q2":
        dados["rep_q2"] = resposta
        st.session_state.estado = "PS_REP_KG_PERDIDOS"
        add_bot(PS_REP_KG_PERDIDOS)
    elif estado == "PS_REP_KG_PERDIDOS":
        dados["rep_kg_perdidos"] = resposta
        st.session_state.estado = "PS_REP_EMPATIA"
        add_bot(PS_REP_EMPATIA)
    elif estado == "PS_REP_FALTAM_KG":
        # Compatibilidade com conversas iniciadas em versões anteriores.
        dados["rep_faltam_kg"] = resposta
        st.session_state.estado = "PS_REP_KG_PERDIDOS"
        add_bot(PS_REP_KG_PERDIDOS)
    elif estado == "PS_CONSULTA_97_DECISAO":
        n = _n(resposta)
        if "tirar" in n or "dúvida" in n or "duvida" in n or _sim(resposta):
            st.session_state.estado = "PS_CONSULTA_97_PAGAMENTO"
            add_bot(PS_CONSULTA_PAGA_97)
        else:
            add_bot(PS_ENCERRAMENTO)
            st.session_state.estado = "FIM"

    elif estado == "PS_CONSULTA_97_PAGAMENTO":
        n = _n(resposta)
        if "cartão" in n or "cartao" in n or "crédito" in n or "credito" in n:
            add_bot(f"✅ Aqui está o link para pagamento via Cartão de Crédito:\n\n{LINK_CARTAO_97}\n\nAo realizar o pagamento e for dado baixa no nosso financeiro, alguém da nossa equipe vai entrar em contato o quanto antes pra marcar seu atendimento na agenda da Dra Lethicia.")
            st.session_state.estado = "FIM"
        elif "pix" in n:
            add_bot(f"✅ Aqui está o link para pagamento via Pix:\n\n{LINK_PIX_97}\n\nAo realizar o pagamento e for dado baixa no nosso financeiro, alguém da nossa equipe vai entrar em contato o quanto antes pra marcar seu atendimento na agenda da Dra Lethicia.")
            st.session_state.estado = "FIM"
        else:
            add_bot(PS_CONSULTA_PAGA_97)

    elif estado == "PS_REP_NAO_PESO":
        # Compatibilidade com conversas já iniciadas nesse estado em versões anteriores.
        iniciar_fluxo_reparadora_97()
    elif estado == "PS_REP_EMPATIA":
        dados["rep_q3"] = resposta
        add_bot(PS_REP_OBRIGADA)
        st.session_state.estado = "PS_REP_Q4"
        add_bot(PS_REP_Q4)
    elif estado == "PS_REP_Q4":
        dados["rep_q4"] = resposta
        add_bot(PS_REP_CURIOSIDADE)
        st.session_state.estado = "PS_REP_Q5"
        add_bot(PS_REP_Q5)
    elif estado == "PS_REP_Q5":
        dados["rep_q5"] = resposta
        st.session_state.estado = "PS_REP_ACOMPANHAMENTO"
        add_bot(PS_REP_ACOMPANHAMENTO)
    elif estado == "PS_REP_ACOMPANHAMENTO":
        if "acompanhamento" in _n(resposta) or "quer" in _n(resposta) or "dra" in _n(resposta):
            add_bot(MSG_ACOMPANHAMENTO_JURIDICO)
            add_bot(MSG_PRE_POS_BUSCA_2)
            st.session_state.estado = "PS_POS_BUSCA"
            add_bot(PS_POS_BUSCA)
        elif "como funciona" in _n(resposta):
            add_bot(MSG_ACOMPANHAMENTO_JURIDICO)
            add_bot(MSG_PRE_POS_BUSCA_2)
            st.session_state.estado = "PS_POS_BUSCA"
            add_bot(PS_POS_BUSCA)
        else:
            add_bot(PS_ENCERRAMENTO)
            st.session_state.estado = "FIM"

    # ---- NEGATIVA DE CIRURGIA ----
    elif estado == "PS_NEG_CIR_ESP":
        dados["neg_cir_esp"] = resposta

        if "endometriose" in _n(resposta) or "1" in resposta:
            st.session_state.perguntas_ativas = [PS_ENDO_Q1, PS_ENDO_Q2, PS_ENDO_Q3, PS_ENDO_Q4, PS_ENDO_Q5]
        elif "bariátrica" in _n(resposta) or "bariatrica" in _n(resposta) or "2" in resposta:
            st.session_state.perguntas_ativas = [
                PS_BARI_Q1, PS_BARI_Q2, PS_BARI_Q3_MSG, PS_BARI_Q3,
                PS_BARI_Q4, PS_BARI_Q5, PS_BARI_Q6
            ]
        elif "oncologia" in _n(resposta) or "3" in resposta:
            st.session_state.perguntas_ativas = [PS_ONCO_Q1, PS_ONCO_Q2, PS_ONCO_Q3, PS_ONCO_Q4, PS_ONCO_Q5, PS_ONCO_Q6]
        elif "cardiologia" in _n(resposta) or "4" in resposta:
            st.session_state.perguntas_ativas = [PS_CARDIO_Q1, PS_CARDIO_Q2, PS_CARDIO_Q3, PS_CARDIO_Q4, PS_CARDIO_Q5, PS_CARDIO_Q6]
        elif "neurocirurgia" in _n(resposta) or "5" in resposta:
            # Neurocirurgia sem a pergunta do material
            st.session_state.perguntas_ativas = [PS_NEURO_Q1, PS_NEURO_Q2, PS_NEURO_Q3, PS_NEURO_Q4, PS_NEURO_Q5, PS_NEURO_Q7]
        elif "ortopedia" in _n(resposta) or "6" in resposta:
            st.session_state.perguntas_ativas = [PS_ORTO_Q1, PS_ORTO_Q2, PS_ORTO_Q3, PS_ORTO_Q4, PS_ORTO_Q5, PS_ORTO_Q6]
        elif "oftalmologia" in _n(resposta) or "7" in resposta:
            st.session_state.perguntas_ativas = [PS_OFTAL_Q1, PS_OFTAL_Q2, PS_OFTAL_Q3, PS_OFTAL_Q4, PS_OFTAL_Q5]
        else:
            st.session_state.perguntas_ativas = [
                PS_OUTRO_INTRO, PS_OUTRO_Q1, PS_OUTRO_Q2, PS_OUTRO_Q3, PS_OUTRO_Q4,
                PS_OUTRO_Q5, PS_OUTRO_Q6, PS_OUTRO_Q7, PS_OUTRO_Q8, PS_OUTRO_Q9
            ]

        st.session_state.pergunta_idx = 0
        st.session_state.estado = "PS_PERGUNTAS_COLETOR"
        add_bot(st.session_state.perguntas_ativas[0])

    # ---- AGUARDA RESPOSTA APÓS PONTO CRÍTICO ----
    elif estado == "PS_PONTO_CRITICO_AGUARDANDO":
        dados["ponto_critico_resposta"] = resposta
        situacao_raw = dados.get("situacao", "")
        situacao_n = _n(situacao_raw)
        # Para negativa de cirurgia, só agora pergunta sobre material/protese.
        if "negativa" in situacao_n or "1" == str(situacao_raw).strip() or "2" == str(situacao_raw).strip():
            st.session_state.estado = "PS_NEG_MATERIAL"
            add_bot(MSG_NEG_MATERIAL)
        else:
            add_bot(MSG_PRE_POS_BUSCA_1)
            add_bot(MSG_PRE_POS_BUSCA_2)
            st.session_state.estado = "PS_POS_BUSCA"
            add_bot(PS_POS_BUSCA)

    # ---- NEGATIVA DE MATERIAL ----
    elif estado == "PS_NEG_MATERIAL":
        dados["neg_material"] = resposta
        add_bot(MSG_PRE_POS_BUSCA_1)
        add_bot(MSG_PRE_POS_BUSCA_2)
        st.session_state.estado = "PS_POS_BUSCA"
        add_bot(PS_POS_BUSCA)

    # ---- POS BUSCA (opções 1-3) ----
    elif estado == "PS_POS_BUSCA":
        if "1" in resposta:
            add_bot(PS_OP1_PERGUNTA)
            add_bot(PS_OP1_REUNIAO)
            st.session_state.estado = "DECISAO_COMPARTILHADA"
            add_bot(MSG_SIM_HONORARIOS_SUS_DECISAO)
        elif "2" in resposta:
            add_bot(PS_OP2_INTRO)
            add_bot(PS_OP2_CAMINHO_1)
            add_bot(PS_OP2_CAMINHO_2)
            st.session_state.estado = "PS_OP2_DECISAO"
            add_bot(PS_OP2_DECISAO)
        elif "3" in resposta:
            st.session_state.estado = "PS_OP3_CONSULTORIA"
            add_bot(PS_OP3_CONSULTORIA)
        else:
            add_bot(PS_POS_BUSCA)

    elif estado == "PS_OP2_DECISAO":
        if _sim(resposta):
            st.session_state.estado = "DECISAO_COMPARTILHADA"
            add_bot(MSG_SIM_HONORARIOS_SUS_DECISAO)
        else:
            add_bot(PS_ENCERRAMENTO)
            st.session_state.estado = "FIM"

    elif estado == "PS_OP3_CONSULTORIA":
        if _sim(resposta):
            st.session_state.estado = "PS_OP3_PAGAMENTO"
            add_bot(PS_OP3_PAGAMENTO)
        else:
            add_bot(PS_ENCERRAMENTO)
            st.session_state.estado = "FIM"

    elif estado == "PS_OP3_PAGAMENTO":
        if "cartão" in _n(resposta) or "cartao" in _n(resposta):
            add_bot(f"✅ Aqui está o link para pagamento via Cartão de Crédito:\n\n{LINK_CARTAO_500}\n\n{PS_OP3_CONFIRMACAO}")
            st.session_state.estado = "FIM"
        elif "pix" in _n(resposta):
            add_bot(f"✅ Aqui está o link para pagamento via Pix:\n\n{LINK_PIX_500}\n\n{PS_OP3_CONFIRMACAO}")
            st.session_state.estado = "FIM"

    # ---- DECISÃO COMPARTILHADA ----
    elif estado == "DECISAO_COMPARTILHADA":
        n = _n(resposta)
        if "sozinho" in n or "sozinha" in n or "não" in n or "nao" in n:
            add_bot(DECISAO_NAO)
        elif "repasse" in n or "passo" in n or "falar" in n or "3" in resposta:
            add_bot(DECISAO_REPASSE)
            st.session_state.estado = "DECISAO_REPASSE_RESPOSTA"
            return
        else:
            add_bot(DECISAO_SIM)
        # Schedule timed messages
        st.session_state.followup_time = time.time() + 600  # 10 min
        st.session_state.finalizacao_time = st.session_state.followup_time + 300  # +5 min
        st.session_state.estado = "AGUARDANDO_TIMED"

    elif estado == "DECISAO_REPASSE_RESPOSTA":
        if _sim(resposta) or "com ele" in _n(resposta):
            add_bot(DECISAO_REPASSE_SIM)
        else:
            add_bot(DECISAO_REPASSE_NAO)
        st.session_state.followup_time = time.time() + 600
        st.session_state.finalizacao_time = st.session_state.followup_time + 300
        st.session_state.estado = "AGUARDANDO_TIMED"

    elif estado == "FIM":
        pass


# ============================================
# INTERFACE STREAMLIT
# ============================================

def main():
    st.title("🌹 Aurora Bot - Assistente Jurídica em Direito da Saúde")
    st.caption(f"Especialista: {L} | Atendimento: SUS, Planos de Saúde")

    init_session()

    # ---- CHECK TIMED MESSAGES ----
    now = time.time()
    rerun_timed = False
    
    # Check timeout de 5 min sem resposta
    if check_no_response_timeout():
        rerun_timed = True
    
    # Check mensagens de 24h
    if check_24h_messages():
        rerun_timed = True
    
    # Check link do Meet (5 min antes)
    if check_meet_link():
        rerun_timed = True
    
    # Followup e finalização
    if st.session_state.followup_time and not st.session_state.followup_sent:
        if now >= st.session_state.followup_time:
            st.session_state.messages.append({"role": "bot", "content": MSG_FOLLOWUP_LINK})
            st.session_state.followup_sent = True
            rerun_timed = True
    if st.session_state.finalizacao_time and not st.session_state.finalizacao_sent:
        if now >= st.session_state.finalizacao_time:
            st.session_state.messages.append({"role": "bot", "content": MSG_AGENDAMENTO_FINALIZADO})
            st.session_state.finalizacao_sent = True
            st.session_state.estado = "FIM"
            rerun_timed = True
    
    if rerun_timed:
        st.rerun()

    # Mantém a página “acordada” para enviar automaticamente o lembrete de 5 minutos,
    # mesmo se o cliente não clicar em nada nem enviar nova mensagem.
    schedule_no_response_autorefresh()

    with st.sidebar:
        st.markdown("### 📋 Informações da Sessão")
        if st.session_state.nome:
            st.info(f"**Cliente:** {st.session_state.nome}")
        if st.session_state.dados.get("canal"):
            st.info(f"**Canal:** {st.session_state.dados['canal']}")
        if st.session_state.dados.get("especialidade"):
            st.info(f"**Especialidade:** {st.session_state.dados['especialidade']}")
        st.markdown("---")
        if st.button("🔄 Nova Conversa", use_container_width=True):
            reset()
            st.rerun()

    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        if msg["role"] == "bot":
            st.markdown(
                f'<div class="chat-message bot-message"><strong>🌹 Aurora:</strong><br>{msg["content"]}</div>',
                unsafe_allow_html=True
            )
        else:
            nome = st.session_state.nome or "Você"
            st.markdown(
                f'<div class="chat-message user-message"><strong>👤 {nome}:</strong><br>{msg["content"]}</div>',
                unsafe_allow_html=True
            )
    st.markdown('</div>', unsafe_allow_html=True)

    # ---- BOTÕES CONTEXTUAIS (abaixo do chat) ----
    estado = st.session_state.estado

    def btn(label, valor=None):
        v = valor or label
        if st.button(label, use_container_width=False, key=f"btn_{label}_{v}"):
            add_user(v)
            processar(v)
            st.rerun()

    def render_opcoes_numeradas(texto):
        """
        Cria botões automaticamente para perguntas que já trazem alternativas no texto
        (ex.: 1️⃣ Sim / 2️⃣ Não / 3️⃣ Não sei).
        Mantém perguntas abertas sem botões quando não houver alternativas numeradas.
        """
        texto = str(texto)
        # Captura opções com emoji numérico, inclusive quando estão na mesma linha.
        matches = list(re.finditer(r"([0-9]|10)️⃣\s*", texto))
        opcoes = []
        for i, m in enumerate(matches):
            inicio = m.end()
            fim = matches[i + 1].start() if i + 1 < len(matches) else len(texto)
            rotulo = texto[inicio:fim].strip()
            rotulo = re.sub(r"\s+", " ", rotulo).strip(" -–:.;")
            if rotulo:
                numero = m.group(1)
                opcoes.append((f"{numero}️⃣ {rotulo}", rotulo))

        if not opcoes:
            return False

        # Evita botões enormes quando a pergunta é explicativa e não uma escolha real.
        opcoes = [(label[:120], valor[:120]) for label, valor in opcoes]
        cols = st.columns(min(3, max(1, len(opcoes))))
        for i, (label, valor) in enumerate(opcoes):
            with cols[i % len(cols)]:
                btn(label, valor)
        return True

    def show_buttons():
        if estado == "CANAL":
            c1, c2 = st.columns(2)
            with c1: btn("🏥 SUS", "SUS")
            with c2: btn("📋 Plano de Saúde", "Plano de Saúde")

        elif estado == "SUS_DEMANDA":
            c1, c2 = st.columns(2)
            with c1: btn("🔪 Cirurgia / Tratamento", "Cirurgia")
            with c2: btn("📋 Consultas / Exames", "Consultas")

        elif estado == "SUS_CONSULTA_EXAME_TIPO":
            c1, c2 = st.columns(2)
            with c1: btn("1️⃣ Consulta com especialista", "1")
            with c2: btn("2️⃣ Realização de Exame", "2")

        elif estado == "SUS_CONSULTA_PITCH":
            c1, c2 = st.columns(2)
            with c1: btn("⏳ Quero aguardar", "aguardar")
            with c2: btn("💙 Quero ajuda da Dra. Lethicia", "quero ajuda")

        elif estado in ("SUS_CONSULTA_AJUDA_Q3", "SUS_CONSULTA_AJUDA_Q4B", "SUS_CONSULTA_Q3"):
            c1, c2 = st.columns(2)
            with c1: btn("✅ Sim", "Sim")
            with c2: btn("❌ Não", "Não")

        elif estado == "SUS_CONSULTA_AJUDA_Q4":
            c1, c2, c3 = st.columns(3)
            with c1: btn("📱 Tenho Meu SUS", "Tenho Meu SUS")
            with c2: btn("📄 Tenho Comprovante", "Tenho Comprovante")
            with c3: btn("📋 Tenho SISREG", "Tenho SISREG")

        elif estado in ("SUS_CONSULTA_PROTOCOLO", "SUS_EXAME_PROTOCOLO",
                        "SUS_CONSULTA_HONORARIOS", "SUS_EXAME_HONORARIOS",
                        "POS_PERGUNTAS_SUS", "PROPOSTA_SUS", "HONORARIOS_SUS"):
            c1, c2 = st.columns(2)
            with c1: btn("✅ SIM", "SIM")
            with c2: btn("❌ NÃO", "NÃO")

        elif estado == "SUS_EXAME_TIPO":
            c1, c2, c3 = st.columns(3)
            with c1: btn("1️⃣ Diagnóstico", "1")
            with c2: btn("2️⃣ Pré-operatório", "2")
            with c3: btn("3️⃣ Confirmação", "3")

        elif estado == "SUS_EXAME_PITCH":
            c1, c2 = st.columns(2)
            with c1: btn("⏳ Quero aguardar", "aguardar")
            with c2: btn("💙 Quero ajuda da Dra. Lethicia", "quero ajuda")

        elif estado == "SUS_ESPECIALIDADE":
            cols = st.columns(4)
            esps = ["Oncologia", "Neurodivergências (TEA, TDAH)", "Endometriose / Adenomiose",
                    "Medicamento", "Bariátrica", "Neurologia / Neurocirurgia", "Cardiologia", "Outros"]
            for i, esp in enumerate(esps):
                with cols[i % 4]: btn(esp)

        elif estado in ("SUS_ONCOLOGIA_BENIGNO_MALIGNO", "SUS_ONCOLOGIA_Q1"):
            c1, c2 = st.columns(2)
            with c1: btn("🔴 Maligno", "Maligno")
            with c2: btn("🟢 Benigno", "Benigno")

        elif estado == "SUS_DOCS_INSUF":
            c1, c2 = st.columns(2)
            with c1: btn("✅ Certo", "Certo")
            with c2: btn("👍 Vou fazer isso", "Vou fazer isso")

        elif estado == "SUS_PERGUNTAS":
            idx = st.session_state.pergunta_idx
            perguntas = st.session_state.perguntas_ativas
            if idx < len(perguntas):
                pergunta_atual = perguntas[idx]
                q = pergunta_atual.lower()
                if render_opcoes_numeradas(pergunta_atual):
                    pass
                elif any(kw in q for kw in ["tem relatório", "possui relatório", "tem o comprovante",
                                           "possui o comprovante", "risco de piora", "agravamento",
                                           "diagnóstico confirmado", "tem laudo", "possui laudo",
                                           "tem a receita", "tem algum laudo", "urgente",
                                           "já foi encaminhado", "já tem mais", "60 dias"]):
                    c1, c2 = st.columns(2)
                    with c1: btn("✅ Sim", "Sim")
                    with c2: btn("❌ Não", "Não")

        elif estado == "PS_TEMPO":
            c1, c2 = st.columns(2)
            with c1: btn("1️⃣ Sim", "Sim")
            with c2: btn("2️⃣ Não", "Não")
        
        elif estado == "PS_TEMPO_NAO_SEGUIMENTO":
            c1, c2 = st.columns(2)
            with c1: btn("🏢 Empresarial/CNPJ", "empresarial")
            with c2: btn("👤 Pessoa Física", "pessoa física")

        elif estado == "PS_SITUACAO":
            opcoes = [
                ("0️⃣ Reparadora", "0"), ("1️⃣ Negativa de cirurgia", "1"),
                ("2️⃣ Medicamento negado", "2"), ("3️⃣ Exame negado", "3"),
                ("4️⃣ Home care", "4"), ("5️⃣ Terapias", "5"),
                ("6️⃣ Reajuste", "6"), ("7️⃣ Coparticipação elevada", "7"),
                ("8️⃣ Erro médico", "8"), ("9️⃣ OUTRO", "9"),
            ]
            cols = st.columns(2)
            for i, (label, val) in enumerate(opcoes):
                with cols[i % 2]: btn(label, val)

        elif estado == "PS_REP_Q2":
            c1, c2 = st.columns(2)
            with c1: btn("1️⃣ Já cheguei à minha meta", "1")
            with c2: btn("2️⃣ Ainda não", "2")

        elif estado == "PS_REP_Q5":
            c1, c2 = st.columns(2)
            with c1: btn("✅ SIM", "SIM")
            with c2: btn("❌ NÃO", "NÃO")

        elif estado == "PS_REP_ACOMPANHAMENTO":
            c1, c2, c3 = st.columns(3)
            with c1: btn("💙 Quero acompanhamento da Dra.", "quero acompanhamento")
            with c2: btn("❓ Como funciona", "como funciona")
            with c3: btn("👤 Não quero acompanhamento", "não quero")

        elif estado == "PS_NEG_CIR_ESP":
            opcoes = [
                ("1️⃣ Endometriose", "1"), ("2️⃣ Bariátrica", "2"),
                ("3️⃣ Oncologia (câncer)", "3"), ("4️⃣ Cardiologia", "4"),
                ("5️⃣ Neurocirurgia", "5"), ("6️⃣ Ortopedia", "6"),
                ("7️⃣ Oftalmologia", "7"), ("8️⃣ OUTRO", "8"),
            ]
            cols = st.columns(2)
            for i, (label, val) in enumerate(opcoes):
                with cols[i % 2]: btn(label, val)

        elif estado == "PS_NEG_MATERIAL":
            c1, c2, c3 = st.columns(3)
            with c1: btn("🔪 Cirurgia negada", "Cirurgia negada")
            with c2: btn("🔩 Material negado", "Material negado")
            with c3: btn("➖ Não se aplica", "Não se aplica")

        elif estado == "PS_CONSULTA_97_DECISAO":
            c1, c2 = st.columns(2)
            with c1: btn("⏳ Aguardar", "Aguardar")
            with c2: btn("💬 Tirar as dúvidas", "Tirar as dúvidas")

        elif estado == "PS_CONSULTA_97_PAGAMENTO":
            c1, c2 = st.columns(2)
            with c1: btn("💳 Cartão de Crédito", "cartão")
            with c2: btn("📱 Pix", "pix")

        elif estado == "PS_OP2_DECISAO":
            c1, c2 = st.columns(2)
            with c1: btn("✅ SIM", "SIM")
            with c2: btn("❌ NÃO", "NÃO")

        elif estado == "PS_OP3_CONSULTORIA":
            c1, c2 = st.columns(2)
            with c1: btn("✅ Sim, quero agendar agora", "Sim, quero agendar agora")
            with c2: btn("❌ Não quero, mas obrigada", "Não quero")

        elif estado == "PS_OP3_PAGAMENTO":
            c1, c2 = st.columns(2)
            with c1: btn("💳 Cartão de Crédito", "cartão")
            with c2: btn("📱 Pix", "pix")

        elif estado == "PERGUNTA_RESULTADOS":
            c1, c2 = st.columns(2)
            with c1: btn("✅ SIM", "SIM")
            with c2: btn("❌ NÃO", "NÃO")

        elif estado == "PERGUNTA_VALOR_ANALISE":
            c1, c2 = st.columns(2)
            with c1: btn("✅ SIM", "SIM")
            with c2: btn("❌ NÃO", "NÃO")

        elif estado == "PS_POS_BUSCA":
            opcoes = [
                ("1️⃣ Já tenho a negativa do plano", "1"),
                ("2️⃣ Ainda não tenho a negativa, mas preciso me preparar", "2"),
                ("3️⃣ Preciso de uma consultoria jurídica", "3"),
            ]
            cols = st.columns(3)
            for i, (label, val) in enumerate(opcoes):
                with cols[i % 3]: btn(label, val)

        elif estado == "DECISAO_COMPARTILHADA":
            c1, c2, c3 = st.columns(3)
            with c1: btn("👨‍👩‍👧 Sim, meu cônjuge/familiar", "sim")
            with c2: btn("👤 Não, eu decido sozinho(a)", "sozinho")
            with c3: btn("📞 Tem, mas pode falar comigo", "repasse")

        elif estado == "DECISAO_REPASSE_RESPOSTA":
            c1, c2 = st.columns(2)
            with c1: btn("👥 Com ele(a)", "com ele")
            with c2: btn("👤 Entre nós", "não")

        elif estado == "PS_OUTRO_DEMANDA":
            idx = st.session_state.get("outro_idx", 0)
            # Q1 já foi enviada, agora verificamos as demais
            if idx == 0:
                # Aguardando resposta da Q1 (texto livre - sem botões)
                pass
            elif idx == 1:
                # Q2 - texto livre
                pass
            elif idx == 2:
                # Q3 - botões
                c1, c2, c3 = st.columns(3)
                with c1: btn("✅ Sim", "Sim")
                with c2: btn("❌ Não", "Não")
                with c3: btn("➖ Não se encaixa", "Não se encaixa")
            elif idx == 3:
                # Q4 - botões
                c1, c2, c3 = st.columns(3)
                with c1: btn("✅ Sim", "Sim")
                with c2: btn("❌ Não", "Não")
                with c3: btn("➖ Não se encaixa", "Não se encaixa")
            elif idx == 4:
                # Q5 - botões
                c1, c2 = st.columns(2)
                with c1: btn("✅ Sim", "Sim")
                with c2: btn("❌ Não", "Não")
            elif idx == 5:
                # Q6 - botões
                c1, c2 = st.columns(2)
                with c1: btn("✅ Sim", "Sim")
                with c2: btn("❌ Não", "Não")

        elif estado == "PS_REAJ_ESCOLHA":
            c1, c2 = st.columns(2)
            with c1: btn("⚖️ Quero judicializar", "1")
            with c2: btn("📄 Quero consultoria jurídica", "2")

        elif estado == "PS_REAJ_CONSULTORIA":
            c1, c2 = st.columns(2)
            with c1: btn("✅ Sim, quero agendar agora", "Sim, quero agendar agora")
            with c2: btn("❌ Não quero, mas obrigada", "Não quero")

        elif estado == "PS_REAJ_PAGAMENTO":
            c1, c2 = st.columns(2)
            with c1: btn("💳 Cartão de Crédito", "cartão")
            with c2: btn("📱 Pix", "pix")

        elif estado == "PS_COPA_ESCOLHA":
            c1, c2 = st.columns(2)
            with c1: btn("⚖️ Quero judicializar", "1")
            with c2: btn("📄 Quero consultoria jurídica", "2")

        elif estado == "PS_ERRO_ESCOLHA":
            c1, c2 = st.columns(2)
            with c1: btn("⚖️ Quero judicializar", "1")
            with c2: btn("📄 Quero análise técnica", "2")

        elif estado == "PS_ERRO_CONSULTORIA":
            c1, c2 = st.columns(2)
            with c1: btn("✅ Sim, quero agendar agora", "Sim, quero agendar agora")
            with c2: btn("❌ Não quero, mas obrigada", "Não quero")

        elif estado == "PS_ERRO_PAGAMENTO":
            c1, c2 = st.columns(2)
            with c1: btn("💳 Cartão de Crédito", "cartão")
            with c2: btn("📱 Pix", "pix")

        elif estado == "PS_MOTIVO_NEGATIVA_GERAL":
            c1, c2, c3 = st.columns(3)
            with c1: btn("1️⃣ Fora do rol da ANS", "Fora do rol da ANS")
            with c2: btn("2️⃣ Não atende diretriz (DUT)", "Não atende diretriz (DUT)")
            with c3: btn("3️⃣ Carência", "Carência")
            c4, c5, c6 = st.columns(3)
            with c4: btn("4️⃣ Não é urgente", "Não é urgente")
            with c5: btn("5️⃣ Experimental", "Experimental")
            with c6: btn("6️⃣ Outro", "Outro")

        elif estado == "PS_PERGUNTAS_COLETOR":
            idx = st.session_state.pergunta_idx
            perguntas = st.session_state.perguntas_ativas
            if idx < len(perguntas):
                pergunta_atual = perguntas[idx]
                q = pergunta_atual.lower()

                # Regra geral: toda pergunta com alternativas numeradas deve virar botão,
                # inclusive Oftalmologia, Exames, Home Care, Terapias, Reajuste, Coparticipação e Erro Médico.
                if render_opcoes_numeradas(pergunta_atual):
                    pass
                # Motivo da negativa: não exibir botões genéricos de Sim/Não.
                # Exibir as 6 opções corretas do texto.
                elif "qual foi o motivo da negativa" in q:
                    c1, c2, c3 = st.columns(3)
                    with c1: btn("1️⃣ Fora do rol da ANS", "Fora do rol da ANS")
                    with c2: btn("2️⃣ Não atende diretriz (DUT)", "Não atende diretriz (DUT)")
                    with c3: btn("3️⃣ Carência", "Carência")
                    c4, c5, c6 = st.columns(3)
                    with c4: btn("4️⃣ Não é urgente", "Não é urgente")
                    with c5: btn("5️⃣ Experimental", "Experimental")
                    with c6: btn("6️⃣ Outro", "Outro")
                # Hospital da rede do plano: NÃO exibir botões genéricos de Sim/Não.
                # Exibir somente as 3 opções corretas: Sim, Não e Não sei.
                elif "hospital onde seria realizada" in q and "rede do plano" in q:
                    c1, c2, c3 = st.columns(3)
                    with c1: btn("1️⃣ Sim", "Sim")
                    with c2: btn("2️⃣ Não", "Não")
                    with c3: btn("3️⃣ Não sei", "Não sei")
                # Para pergunta de negativa por escrita ou verbal
                elif "escrita ou verbal" in q:
                    c1, c2 = st.columns(2)
                    with c1: btn("✍️ Escrita", "Escrita")
                    with c2: btn("📞 Verbal (telefone/balcão)", "Verbal")
                # Opção OUTROS na terapia
                elif "9️⃣ outros" in q:
                    c1 = st.columns(1)[0]
                    with c1: btn("9️⃣ OUTROS", "OUTROS")
                elif any(kw in q for kw in ["1️⃣ sim", "sim\n2️⃣ não", "você possui", "tem laudo",
                                           "tem exames", "tem o laudo", "multidisciplinar",
                                           "foi negado", "urgente", "receita médica"]):
                    c1, c2 = st.columns(2)
                    with c1: btn("✅ Sim", "Sim")
                    with c2: btn("❌ Não", "Não")

    show_buttons()

    st.markdown("---")
    user_input = st.text_input(
        "Digite sua mensagem apenas quando a pergunta for aberta:",
        key="user_input",
        placeholder="Use os botões quando eles aparecerem. Digite somente respostas abertas."
    )

    if st.button("📤 Enviar", use_container_width=True) and user_input:
        add_user(user_input)
        # Atualiza timestamp da última resposta
        st.session_state.aguardando_resposta_desde = None
        processar(user_input)
        # Define novo timeout para resposta
        st.session_state.aguardando_resposta_desde = time.time()
        st.rerun()

    if not st.session_state.messages:
        add_bot(MSG_BOAS_VINDAS)
        st.rerun()


if __name__ == "__main__":
    main()
