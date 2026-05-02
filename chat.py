"""
Iara Bot - Assistente Jurídica em Direito da Saúde
FLUXO EXATAMENTE IGUAL ÀS IMAGENS ENVIADAS
Versão final - sem erros de sintaxe
"""

import streamlit as st
from datetime import datetime

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
    return any(p in _n(r) for p in ["sim", "s", "yes", "quero", "ok", "claro", "vamos", "aceito", "topo", "1"])

def _nao(r: str) -> bool:
    return any(p in _n(r) for p in ["não", "nao", "no", "2", "depois", "agora não"])

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

def add_bot(msg):
    if msg:
        msg = msg.replace("{nome}", st.session_state.nome or "")
        msg = msg.replace("{lawyer}", L)
        msg = msg.replace("{CALENDLY_LINK}", CALENDLY_LINK)
        st.session_state.messages.append({"role": "bot", "content": msg})

def add_user(msg):
    st.session_state.messages.append({"role": "user", "content": msg})

def reset():
    st.session_state.clear()
    init_session()
    add_bot(MSG_BOAS_VINDAS)

# ============================================
# MENSAGENS PRINCIPAIS
# ============================================

MSG_BOAS_VINDAS = (
    "Olá, seja bem vindo(a). 🌟\n\n"
    "Sou a Lara, assistente jurídica do escritório da Dra Lethicia Fernanda, "
    "advogada especialista em Direito da Saúde.\n\n"
    "**Fico feliz que você entrou em contato conosco.**\n\n"
    "Qual o seu nome?"
)

MSG_CANAL = "Olá, {nome}! Seu atendimento é pelo **SUS** ou por **Plano de Saúde**?"

MSG_SUS_DEMANDA = "Me diga o que você está aguardando?\n\n1️⃣ Cirurgia / Tratamento\n2️⃣ Consultas / Exames"

MSG_SUS_ESPECIALIDADE = (
    "Para que eu direcione você para o protocolo de urgência correto, "
    "qual problema estamos enfrentando hoje?\n\n"
    "1️⃣ Oncologia\n2️⃣ Neurodivergências (TEA, TDAH)\n3️⃣ Endometriose / Adenomiose\n"
    "4️⃣ Medicamento\n5️⃣ Bariátrica\n6️⃣ Reparadora\n7️⃣ Neurologia / Neurocirurgia\n"
    "8️⃣ Cardiologia\n9️⃣ Outros"
)

# ============================================
# PERGUNTAS SUS
# ============================================

PERGUNTAS_ONCOLOGIA = [
    "Entendi… vamos cuidar disso juntos 🚨\n\n👉 Você consegue me contar qual é o tipo de câncer?",
    "👉 Você está aguardando atendimento ou tratamento pelo SUS? Se sim, há quanto tempo mais ou menos?",
    "👉 O diagnóstico já foi confirmado por biópsia? E você tem esse laudo em mãos?",
    "👉 Você já foi encaminhado para um hospital especializado em câncer pelo SUS?",
    "👉 Você possui um relatório médico explicando o tratamento que precisa fazer?",
    "👉 O médico falou se o seu caso é urgente?",
    "👉 Você possui o comprovante de que está aguardando na fila?"
]

PERGUNTAS_NEURO = [
    "Entendi… pode ficar tranquilo(a) 🚨\n\n👉 Me conta: já tem diagnóstico fechado?",
    "👉 Você tem algum laudo ou relatório médico com o diagnóstico?",
    "👉 Quais terapias o médico indicou?",
    "👉 Você conseguiu iniciar as terapias ou ainda está aguardando?",
    "👉 O médico comentou sobre prejuízo no desenvolvimento?",
    "👉 Como essa situação está impactando o dia a dia?",
    "👉 Você possui o comprovante de que está aguardando na fila?"
]

PERGUNTAS_ENDOMETRIOSE = [
    "👉 Você já tem diagnóstico confirmado de endometriose ou adenomiose?",
    "👉 Esse diagnóstico foi feito por exame?",
    "👉 Você sente dores fortes ou crises que atrapalham sua rotina?",
    "👉 O médico indicou algum tratamento específico?",
    "👉 Você tem relatório médico explicando esse tratamento?",
    "👉 Você está aguardando há quanto tempo?",
    "👉 Existe risco de piora ou agravamento sem o tratamento?",
    "👉 Você possui o comprovante de que está aguardando na fila?"
]

PERGUNTAS_MEDICAMENTO = [
    "👉 Qual foi o medicamento que o médico indicou?",
    "👉 Você tem a receita ou relatório médico?",
    "👉 O médico escreveu que este é o único medicamento?",
    "👉 Você já utilizou outros medicamentos antes?",
    "👉 Você solicitou pelo SUS ou farmácia de alto custo?",
    "👉 O que pode acontecer se você não usar este medicamento?"
]

PERGUNTAS_BARIATRICA = [
    "👉 Você já tem indicação médica para cirurgia bariátrica?",
    "👉 Você possui outras doenças agravadas pelo peso?",
    "👉 Você tem laudo médico indicando a cirurgia?",
    "👉 Qual seu peso e altura?",
    "👉 Você já tentou outros tratamentos antes?",
    "👉 Você já está na fila de espera do SUS há quanto tempo?",
    "👉 Você possui o comprovante de que está aguardando na fila?"
]

PERGUNTAS_REPARADORA = [
    "👉 Você passou por cirurgia bariátrica ou teve grande perda de peso?",
    "👉 O excesso de pele tem causado algum problema?",
    "👉 Você já passou pelo cirurgião plástico?",
    "👉 Algum médico já te deu um relatório solicitando a cirurgia?",
    "👉 Você está aguardando há quanto tempo?",
    "👉 Você possui o comprovante de que está aguardando na fila?"
]

PERGUNTAS_NEUROLOGIA = [
    "👉 Qual é o problema neurológico ou diagnóstico?",
    "👉 Você tem laudo ou exame com esse diagnóstico?",
    "👉 Qual cirurgia especificamente você está aguardando?",
    "👉 A demora pode causar dano irreversível?",
    "👉 Você está aguardando há quanto tempo?",
    "👉 Você já possui o comprovante de que está aguardando na fila?"
]

PERGUNTAS_CARDIOLOGIA = [
    "👉 Qual é o problema cardíaco?",
    "👉 Envolve cirurgia de urgência, marca-passo ou stent?",
    "👉 Você tem exame ou laudo do coração?",
    "👉 Você tem sentido dor no peito, falta de ar, tontura?",
    "👉 O médico indicou algum tratamento ou procedimento?",
    "👉 Você tem relatório médico explicando a necessidade?",
    "👉 Você possui comprovante de que está na fila?"
]

PERGUNTAS_OUTROS = [
    "👉 Poderia me dizer qual é a sua condição/doença?",
    "👉 Você já tem diagnóstico ou ainda está investigando?",
    "👉 Algum médico já te passou relatório ou pedido de tratamento?",
    "👉 O médico comentou se existe urgência ou risco?",
    "👉 O que acontece se não conseguir nos próximos 30 ou 90 dias?",
    "👉 Como essa situação tem afetado sua vida hoje?",
    "👉 Você possui o comprovante de que está aguardando na fila?"
]

PERGUNTAS_CONSULTA = [
    "👉 Você já está nessa fila há mais de 30 dias?",
    "👉 Qual especialidade médica você está aguardando?",
    "👉 Você tem encaminhamento ou pedido médico?",
    "👉 Está aguardando há quanto tempo?",
    "👉 O que te informaram sobre a fila?",
    "👉 Você teria algum exame informando a condição?",
    "👉 Você possui comprovante da fila e laudo médico?"
]

PERGUNTAS_EXAME = [
    "👉 Qual exame o médico solicitou?",
    "👉 É para Diagnóstico, Pré-operatório ou Confirmação?"
]

PERGUNTAS_EXAME_DIAG = [
    "👉 O que está sendo investigado com esse exame?",
    "👉 Existe urgência ou risco em não realizar?",
    "👉 Você está aguardando há quanto tempo?",
    "👉 Quem pediu o exame (especialista ou UBS)?",
    "👉 Você recebeu algum comprovante do SUS?"
]

PERGUNTAS_EXAME_PREOP = [
    "👉 Você já tem indicação de cirurgia?",
    "👉 Está aguardando há quanto tempo?",
    "👉 Qual cirurgia você precisa fazer?",
    "👉 Quem pediu o exame?",
    "👉 A cirurgia é urgente?",
    "👉 Você recebeu algum comprovante do SUS?"
]

PERGUNTAS_EXAME_CONF = [
    "👉 O médico suspeita de qual tipo de cirurgia?",
    "👉 Quais sintomas você apresentou?",
    "👉 Existe urgência ou risco em não realizar?",
    "👉 Está aguardando há quanto tempo?",
    "👉 Você recebeu algum comprovante do SUS?"
]

# ============================================
# MENSAGENS PÓS PERGUNTAS
# ============================================

MSG_POS_PERGUNTAS = (
    "_{nome}_, recebi suas respostas aqui. O que mais me preocupa no seu caso é que o SUS "
    "trata isso como se pudesse esperar, mas juridicamente sabemos que o *tempo é o seu maior inimigo agora*.\n\n"
    "Você sente que, se não resolvermos isso nos próximos dias, a sua saúde corre risco de piorar?"
)

MSG_EXPLICACAO = (
    "Só pra te explicar de forma simples:\n\n"
    "Quando o paciente não consegue atendimento pelo SUS, a Justiça pode intervir.\n\n"
    "Trabalho com um *Protocolo de Liberação Urgente* para tirar você da fila. "
    "Isso faria diferença na sua vida agora?"
)

MSG_HONORARIOS = (
    "O escritório cobra *Honorários Iniciais* para assumir o caso e protocolar o pedido de liminar.\n\n"
    "Prosseguir com esse caso faz sentido para você garantir sua saúde hoje?"
)

MSG_SIM = (
    "Ótimo! 💙\n\n"
    "Vou encaminhar seus dados para a mesa da Dra. Lethicia.\n\n"
    f"🔗 Agende sua reunião: {CALENDLY_LINK}\n\n"
    "Fique atento(a)! 👀"
)

MSG_NAO = (
    "Compreendo. Infelizmente, sem ação judicial, seu caso continuará na fila do SUS.\n\n"
    "Caso mude de ideia, estamos à disposição. Desejamos sorte no seu tratamento. 🙏"
)

# ============================================
# PLANO DE SAÚDE - MENSAGENS
# ============================================

PS_REP_Q1 = "👉 Você realizou cirurgia bariátrica ou teve grande perda de peso?"
PS_REP_Q2 = "👉 Você já chegou ao peso que gostaria?\n\n1️⃣ Sim\n2️⃣ Ainda não"
PS_REP_NAO_PESO = "Ofereço uma *consulta de orientação jurídica* por R$ 67,00.\n\nGostaria de agendar um horário?"
PS_REP_Q3 = "Me conte um pouco sobre sua situação..."
PS_REP_Q4 = "Esse excesso de pele causa dores, assaduras ou afeta sua autoestima?"
PS_REP_Q5 = "👉 Quais cirurgias reparadoras você tem interesse?"
PS_REP_Q6 = "👉 Você já foi ao cirurgião plástico para emitir os laudos?\n\n1️⃣ Sim\n2️⃣ Não"
PS_REP_Q7 = "👉 Você prefere tentar sozinho ou quer o acompanhamento da Dra.?"
PS_REP_MODALIDADE = "Qual modalidade deseja?\n\n1️⃣ Consultoria de Laudos\n2️⃣ Blindagem Jurídica Integral"

PS_NEG_CIR_ESP = "Qual o diagnóstico?\n\n1️⃣ Endometriose\n2️⃣ Bariátrica\n3️⃣ Oncologia\n4️⃣ Cardiologia\n5️⃣ Neurocirurgia\n6️⃣ Ortopedia\n7️⃣ Oftalmologia\n8️⃣ OUTRO"

PS_ENDO_Q1 = "Qual tipo de cirurgia foi indicada?"
PS_ENDO_Q2 = "O plano negou formalmente ou não respondeu?"
PS_ENDO_Q3 = "O plano justificou a negativa?"
PS_ENDO_Q4 = "A lei é clara: quem decide é seu médico, não o plano."
PS_ENDO_Q5 = "👉 Você tem os exames que comprovam o diagnóstico?"
PS_ENDO_Q6 = "👉 Você já tentou resolver com o plano?"

PS_BARI_Q1 = "👉 Qual seu peso e altura (IMC)?"
PS_BARI_Q2 = "👉 Você tem comorbidades?"
PS_BARI_Q3 = "A cirurgia bariátrica é por saúde, nunca apenas estética."
PS_BARI_Q4 = "👉 Fez o acompanhamento multidisciplinar?\n\n1️⃣ Sim\n2️⃣ Não"
PS_BARI_Q5 = "👉 O plano negou formalmente?"
PS_BARI_Q6 = "👉 O plano justificou a negativa?"
PS_BARI_Q7 = "A lei é clara: quem decide é seu médico, não o plano."
PS_BARI_Q8 = "👉 Você já tentou resolver com o plano?"

PS_ONCO_Q1 = "👉 Qual o tipo de câncer e procedimento indicado?"
PS_ONCO_Q2 = "👉 Já está em tratamento ou a negativa impediu?"
PS_ONCO_Q3 = "👉 O plano negou formalmente?"
PS_ONCO_Q4 = "A lei é clara: quem decide é seu médico, não o plano."
PS_ONCO_Q5 = "👉 O plano justificou a negativa?"
PS_ONCO_Q6 = "👉 Você tem os exames que comprovam?"
PS_ONCO_Q7 = "👉 Você já tentou resolver com o plano?"

PS_CARDIO_Q1 = "👉 Qual cirurgia foi indicada?"
PS_CARDIO_Q2 = "👉 O plano negou material ou prótese?"
PS_CARDIO_Q3 = "👉 O plano negou formalmente?"
PS_CARDIO_Q4 = "👉 O plano justificou a negativa?"
PS_CARDIO_Q5 = "👉 Você está internado ou em casa?"
PS_CARDIO_Q6 = "👉 O procedimento é urgente?"
PS_CARDIO_Q7 = "👉 Você tem exames que comprovam a necessidade?"

PS_NEURO_Q1 = "👉 Qual procedimento neurocirúrgico?"
PS_NEURO_Q2 = "👉 O paciente está internado ou com dor intensa?"
PS_NEURO_Q3 = "👉 O hospital é da rede do plano?"
PS_NEURO_Q4 = "👉 Está afetando movimentos ou causando perda de força?"
PS_NEURO_Q5 = "👉 O plano justificou a negativa?"
PS_NEURO_Q6 = "A lei é clara: quem decide é seu médico."
PS_NEURO_Q7 = "👉 Negativa foi por escrito ou verbal?"
PS_NEURO_Q8 = "👉 O plano negou material ou prótese?"
PS_NEURO_Q9 = "👉 Você tem exames de imagem que comprovam?"

PS_ORTO_Q1 = "👉 Qual cirurgia ortopédica?"
PS_ORTO_Q2 = "👉 Está limitando sua mobilidade?"
PS_ORTO_Q3 = "👉 O plano justificou a negativa?"
PS_ORTO_Q4 = "A lei é clara: quem decide é seu médico."
PS_ORTO_Q5 = "👉 O plano negou material ou prótese?"
PS_ORTO_Q6 = "👉 Negativa foi por escrito ou verbal?"
PS_ORTO_Q7 = "👉 Você tem exames de imagem que comprovam?"

PS_OFTAL_Q1 = "👉 Qual cirurgia oftalmológica?"
PS_OFTAL_Q2 = "👉 Está afetando sua visão significativamente?"
PS_OFTAL_Q3 = "👉 O médico indicou urgência (risco de perda de visão)?"
PS_OFTAL_Q4 = "👉 O plano justificou a negativa?"
PS_OFTAL_Q5 = "👉 Negativa foi por escrito ou verbal?"
PS_OFTAL_Q6 = "A lei é clara: quem decide é seu médico."

PS_MED_Q1 = "👉 Qual doença você está tratando?"
PS_MED_Q2 = "👉 Qual medicamento foi prescrito?"
PS_MED_Q3 = "👉 O fornecimento foi negado?\n\n1️⃣ Sim\n2️⃣ Não\n3️⃣ Ainda não solicitei"
PS_MED_Q4 = "👉 A falta do medicamento está afetando sua saúde?"
PS_MED_Q5 = "👉 Motivo da negativa?\n1️⃣ Fora do rol\n2️⃣ Alto custo\n3️⃣ Uso domiciliar\n4️⃣ Experimental\n5️⃣ Outro"
PS_MED_Q6 = "👉 Negativa foi por escrito ou verbal?"
PS_MED_Q7 = "A justiça entende que se seu médico prescreveu, o plano deve fornecer."
PS_MED_Q8 = "👉 Você tem receita médica?"
PS_MED_Q9 = "👉 Qual o valor aproximado do medicamento?"
PS_MED_Q10 = "👉 Você tem laudo médico explicando a necessidade?"

PS_EXAME_Q1 = "👉 Qual exame foi solicitado?"
PS_EXAME_Q2 = "👉 Para qual doença ou suspeita?"
PS_EXAME_Q3 = "Sem exame não há diagnóstico, sem diagnóstico não há tratamento."
PS_EXAME_Q4 = "👉 A demora está prejudicando sua saúde?"
PS_EXAME_Q5 = "👉 O que o médico disse sobre a urgência?"
PS_EXAME_Q6 = "👉 Motivo da negativa?"
PS_EXAME_Q7 = "👉 Negativa foi por escrito ou verbal?"

PS_HOME_Q1 = "👉 Qual a doença ou condição do paciente?"
PS_HOME_Q2 = "👉 O paciente está acamado?"
PS_HOME_Q3 = "👉 Já ficou internado recentemente?"
PS_HOME_Q4 = "👉 O plano quer transferir responsabilidade para a família?"
PS_HOME_Q5 = "👉 O home care foi negado?"
PS_HOME_Q6 = "👉 Você tem relatório médico detalhado?"
PS_HOME_Q7 = "👉 Está descrito o tipo de cuidado necessário?"

PS_TERA_Q1 = "👉 O tratamento é para?\n1️⃣ TEA\n2️⃣ Desenvolvimento\n3️⃣ Reabilitação\n4️⃣ Saúde mental\n5️⃣ Outro"
PS_TERA_Q2 = "👉 Quais terapias?\n1️⃣ ABA\n2️⃣ Fisio\n3️⃣ Psico\n4️⃣ Fono\n5️⃣ TO\n6️⃣ Outras"
PS_TERA_Q3 = "👉 Quantas sessões por semana?"
PS_TERA_Q4 = "👉 A falta das terapias tem causado retrocessos?"
PS_TERA_Q5 = "👉 O que aconteceu?\n1️⃣ Limitou sessões\n2️⃣ Negou\n3️⃣ Sem profissional\n4️⃣ Outro"
PS_TERA_Q6 = "👉 Você tem laudo médico com diagnóstico?"
PS_TERA_Q7 = "👉 Negativa foi por escrito ou verbal?"

PS_REAJ_Q1 = "👉 O plano é?\n1️⃣ Individual\n2️⃣ Coletivo\n3️⃣ Empresarial\n4️⃣ Não sei"
PS_REAJ_Q2 = "👉 De quanto foi o aumento?"
PS_REAJ_Q3 = "👉 O novo valor compromete sua renda?"
PS_REAJ_Q4 = "👉 Você tem mais de 59 anos?"
PS_REAJ_Q5 = "👉 Aumento ocorreu após mudança de idade?"
PS_REAJ_Q6 = "👉 Recebeu documento detalhando o aumento?"
PS_REAJ_Q7 = "👉 Plano foi feito por?\n1️⃣ Empresa\n2️⃣ Associação\n3️⃣ Sozinho"
PS_REAJ_Q8 = "👉 Você tem o contrato do plano?"

PS_COPA_Q1 = "👉 Você deixou de fazer exames por causa da coparticipação?"
PS_COPA_Q2 = "👉 Sente que está 'pagando para usar'?"
PS_COPA_Q3 = "👉 Coparticipação foi cobrada em?\n1️⃣ Consultas\n2️⃣ Exames\n3️⃣ Terapias\n4️⃣ Internação\n5️⃣ Outro"
PS_COPA_Q4 = "👉 Você faz tratamento contínuo?"
PS_COPA_Q5 = "👉 Qual tipo de tratamento?"
PS_COPA_Q6 = "Coparticipação não pode ser ilimitada - a justiça entende que pode ser abusiva."
PS_COPA_Q7 = "👉 Você tem o contrato do plano?"

PS_ERRO_Q1 = "👉 O que aconteceu?\n1️⃣ Cirurgia\n2️⃣ Emergência\n3️⃣ Tratamento\n4️⃣ Parto\n5️⃣ Outro"
PS_ERRO_Q2 = "👉 O paciente sofreu algum dano?"
PS_ERRO_Q3 = "👉 Como isso mudou sua vida?"
PS_ERRO_Q4 = "👉 Você tem prontuário médico?"
PS_ERRO_Q5 = "👉 Outro médico disse que houve erro?"
PS_ERRO_Q6 = "👉 Houve falta de informação ou falha técnica?"

PS_OUTRO_Q1 = "👉 Me conte brevemente o que está acontecendo."
PS_OUTRO_Q2 = "👉 Existe algum prazo que te preocupa?"
PS_OUTRO_Q3 = "👉 Recebeu alguma negativa?"
PS_OUTRO_Q4 = "👉 Tem isso registrado?"
PS_OUTRO_Q5 = "👉 Possui documentos relacionados?"
PS_OUTRO_Q6 = "👉 Está afetando sua saúde?"
PS_OUTRO_Q7 = "O contrato de saúde deve proteger a vida, não criar barreiras."

PS_POS = (
    "Obrigado pelas informações. Agora me diz: o que você busca?\n\n"
    "1️⃣ Tirar dúvidas básicas\n"
    "2️⃣ Já tenho a negativa\n"
    "3️⃣ Não tenho a negativa mas sei que vão negar"
)

PS_OP1 = f"Ofereço uma consulta de orientação jurídica por R$ 97,00. Podemos agendar? {CALENDLY_LINK}"
PS_OP2 = "Nesse caso só conseguimos reverter com medidas judiciais. Vou te encaminhar para a agenda da Dra."
PS_OP3 = "Você é estratégico(a)! Vamos blindar seus laudos antes da negativa."

PS_ENCERRAMENTO = "Entendo e respeito sua decisão. Encerramos por aqui. Caso precise, estamos à disposição. 🙏"

# ============================================
# PROCESSAMENTO DO FLUXO
# ============================================

def processar(resposta: str):
    estado = st.session_state.estado
    dados = st.session_state.dados

    if estado == "INICIO":
        st.session_state.nome = resposta
        dados["nome"] = resposta
        st.session_state.estado = "CANAL"
        add_bot(MSG_CANAL.format(nome=resposta))

    elif estado == "CANAL":
        if "sus" in _n(resposta):
            dados["canal"] = "SUS"
            st.session_state.estado = "SUS_DEMANDA"
            add_bot(MSG_SUS_DEMANDA)
        else:
            dados["canal"] = "PLANO"
            st.session_state.estado = "PLANO_TEMPO"
            add_bot("Você já tem seu plano de saúde há mais de 2 anos?\n\n1️⃣ Sim\n2️⃣ Não")

    elif estado == "SUS_DEMANDA":
        if "cirurgia" in _n(resposta) or "1" in resposta:
            dados["tipo"] = "cirurgia"
            st.session_state.estado = "SUS_ESPECIALIDADE"
            add_bot(MSG_SUS_ESPECIALIDADE)
        else:
            dados["tipo"] = "consulta_exame"
            st.session_state.estado = "SUS_CONSULTA_EXAME"
            add_bot("Você está buscando:\n\n1️⃣ Consulta com especialista\n2️⃣ Realização de Exame")

    elif estado == "SUS_ESPECIALIDADE":
        if "oncologia" in _n(resposta) or "1" in resposta:
            st.session_state.perguntas_ativas = PERGUNTAS_ONCOLOGIA.copy()
        elif "neuro" in _n(resposta) or "2" in resposta:
            st.session_state.perguntas_ativas = PERGUNTAS_NEURO.copy()
        elif "endometriose" in _n(resposta) or "3" in resposta:
            st.session_state.perguntas_ativas = PERGUNTAS_ENDOMETRIOSE.copy()
        elif "medicamento" in _n(resposta) or "4" in resposta:
            st.session_state.perguntas_ativas = PERGUNTAS_MEDICAMENTO.copy()
        elif "bariátrica" in _n(resposta) or "5" in resposta:
            st.session_state.perguntas_ativas = PERGUNTAS_BARIATRICA.copy()
        elif "reparadora" in _n(resposta) or "6" in resposta:
            st.session_state.perguntas_ativas = PERGUNTAS_REPARADORA.copy()
        elif "neurologia" in _n(resposta) or "7" in resposta:
            st.session_state.perguntas_ativas = PERGUNTAS_NEUROLOGIA.copy()
        elif "cardiologia" in _n(resposta) or "8" in resposta:
            st.session_state.perguntas_ativas = PERGUNTAS_CARDIOLOGIA.copy()
        else:
            st.session_state.perguntas_ativas = PERGUNTAS_OUTROS.copy()
        
        dados["especialidade"] = resposta
        st.session_state.pergunta_idx = 0
        st.session_state.estado = "SUS_PERGUNTAS"
        add_bot(st.session_state.perguntas_ativas[0])

    elif estado == "SUS_PERGUNTAS":
        idx = st.session_state.pergunta_idx
        perguntas = st.session_state.perguntas_ativas
        
        dados[f"resp_{idx}"] = resposta
        idx += 1
        st.session_state.pergunta_idx = idx
        
        if idx < len(perguntas):
            add_bot(perguntas[idx])
        else:
            st.session_state.estado = "POS_PERGUNTAS"
            add_bot(MSG_POS_PERGUNTAS.format(nome=st.session_state.nome))

    elif estado == "POS_PERGUNTAS":
        dados["sentimento"] = resposta
        add_bot(MSG_EXPLICACAO)
        st.session_state.estado = "HONORARIOS"

    elif estado == "HONORARIOS":
        dados["honorarios"] = resposta
        add_bot(MSG_HONORARIOS)
        st.session_state.estado = "RESPOSTA_HONORARIOS"

    elif estado == "RESPOSTA_HONORARIOS":
        if _sim(resposta):
            add_bot(MSG_SIM)
        else:
            add_bot(MSG_NAO)
        st.session_state.estado = "FIM"

    elif estado == "SUS_CONSULTA_EXAME":
        if "consulta" in _n(resposta) or "1" in resposta:
            dados["sub_tipo"] = "consulta"
            st.session_state.perguntas_ativas = PERGUNTAS_CONSULTA.copy()
            st.session_state.pergunta_idx = 0
            st.session_state.estado = "SUS_PERGUNTAS"
            add_bot(PERGUNTAS_CONSULTA[0])
        else:
            dados["sub_tipo"] = "exame"
            st.session_state.perguntas_ativas = PERGUNTAS_EXAME.copy()
            st.session_state.pergunta_idx = 0
            st.session_state.estado = "SUS_EXAME_TIPO"
            add_bot(PERGUNTAS_EXAME[0])

    elif estado == "SUS_EXAME_TIPO":
        dados["exame_tipo"] = resposta
        if "diagnóstico" in _n(resposta) or "1" in resposta:
            st.session_state.perguntas_ativas = PERGUNTAS_EXAME_DIAG.copy()
        elif "pré" in _n(resposta) or "2" in resposta:
            st.session_state.perguntas_ativas = PERGUNTAS_EXAME_PREOP.copy()
        else:
            st.session_state.perguntas_ativas = PERGUNTAS_EXAME_CONF.copy()
        
        st.session_state.pergunta_idx = 0
        st.session_state.estado = "SUS_PERGUNTAS"
        add_bot(st.session_state.perguntas_ativas[0])

    elif estado == "PLANO_TEMPO":
        if _sim(resposta):
            dados["plano_2anos"] = "sim"
            st.session_state.estado = "PLANO_SITUACAO"
            add_bot("Para que eu possa te direcionar corretamente, qual é a sua situação atual com o plano de saúde?\n\n1️⃣ Reparadora\n2️⃣ Negativa de cirurgia\n3️⃣ Medicamento negado\n4️⃣ Exame negado\n5️⃣ Home care\n6️⃣ Terapias\n7️⃣ Reajuste\n8️⃣ Coparticipação\n9️⃣ Erro médico\n🔟 OUTRO")
        else:
            dados["plano_2anos"] = "nao"
            st.session_state.estado = "PLANO_NAO_2ANOS"
            add_bot("Entendo! Muitas pessoas acreditam que precisam esperar 2 anos, mas a lei nem sempre funciona assim.\n\nMe conta, qual o tratamento que você precisa fazer?")

    elif estado == "PLANO_NAO_2ANOS":
        dados["tratamento"] = resposta
        st.session_state.estado = "PLANO_NAO_2ANOS_URG"
        add_bot("Existem situações onde o plano é obrigado a cobrir mesmo com poucos meses de contrato, especialmente se houver urgência.\n\nNo seu caso, o médico comentou se isso é urgente ou pode trazer algum risco se não for feito?")

    elif estado == "PLANO_NAO_2ANOS_URG":
        dados["urgencia_plano"] = resposta
        st.session_state.estado = "PROPOSTA_JUDICIAL"
        add_bot("Perfeito! SE HÁ URGÊNCIA, o plano já deveria cobrir.\n\nPara resolver isso, trabalho com um Protocolo de Liberação Urgente. Isso faria diferença na sua vida agora?")

    elif estado == "PLANO_SITUACAO":
        dados["situacao"] = resposta
        
        if "reparadora" in _n(resposta) or "1" in resposta:
            st.session_state.estado = "PS_REP_Q1"
            add_bot(PS_REP_Q1)
        elif "negativa de cirurgia" in _n(resposta) or "2" in resposta:
            st.session_state.estado = "PS_NEG_CIR_ESP"
            add_bot(PS_NEG_CIR_ESP)
        elif "medicamento" in _n(resposta) or "3" in resposta:
            st.session_state.estado = "PS_MED_Q1"
            add_bot(PS_MED_Q1)
        elif "exame" in _n(resposta) or "4" in resposta:
            st.session_state.estado = "PS_EXAME_Q1"
            add_bot(PS_EXAME_Q1)
        elif "home" in _n(resposta) or "5" in resposta:
            st.session_state.estado = "PS_HOME_Q1"
            add_bot(PS_HOME_Q1)
        elif "terapia" in _n(resposta) or "6" in resposta:
            st.session_state.estado = "PS_TERA_Q1"
            add_bot(PS_TERA_Q1)
        elif "reajuste" in _n(resposta) or "7" in resposta:
            st.session_state.estado = "PS_REAJ_Q1"
            add_bot(PS_REAJ_Q1)
        elif "coparticipação" in _n(resposta) or "8" in resposta:
            st.session_state.estado = "PS_COPA_Q1"
            add_bot(PS_COPA_Q1)
        elif "erro" in _n(resposta) or "9" in resposta:
            st.session_state.estado = "PS_ERRO_Q1"
            add_bot(PS_ERRO_Q1)
        else:
            st.session_state.estado = "PS_OUTRO_Q1"
            add_bot(PS_OUTRO_Q1)

    # ========== PS REPARADORA ==========
    elif estado == "PS_REP_Q1":
        dados["ps_rep_q1"] = resposta
        st.session_state.estado = "PS_REP_Q2"
        add_bot(PS_REP_Q2)
    elif estado == "PS_REP_Q2":
        if "ainda não" in _n(resposta) or "2" in resposta:
            add_bot(PS_REP_NAO_PESO)
            st.session_state.estado = "PS_REP_AGUARDANDO"
        else:
            st.session_state.estado = "PS_REP_Q3"
            add_bot(PS_REP_Q3)
    elif estado == "PS_REP_AGUARDANDO":
        if _sim(resposta):
            add_bot(f"Ótimo! Agende sua consulta: {CALENDLY_LINK}")
        else:
            add_bot(PS_ENCERRAMENTO)
        st.session_state.estado = "FIM"
    elif estado == "PS_REP_Q3":
        dados["ps_rep_q3"] = resposta
        st.session_state.estado = "PS_REP_Q4"
        add_bot(PS_REP_Q4)
    elif estado == "PS_REP_Q4":
        dados["ps_rep_q4"] = resposta
        st.session_state.estado = "PS_REP_Q5"
        add_bot(PS_REP_Q5)
    elif estado == "PS_REP_Q5":
        dados["ps_rep_q5"] = resposta
        st.session_state.estado = "PS_REP_Q6"
        add_bot(PS_REP_Q6)
    elif estado == "PS_REP_Q6":
        dados["ps_rep_q6"] = resposta
        st.session_state.estado = "PS_REP_Q7"
        add_bot(PS_REP_Q7)
    elif estado == "PS_REP_Q7":
        if "acompanhamento" in _n(resposta):
            st.session_state.estado = "PS_REP_MODALIDADE"
            add_bot(PS_REP_MODALIDADE)
        else:
            add_bot(PS_ENCERRAMENTO)
            st.session_state.estado = "FIM"
    elif estado == "PS_REP_MODALIDADE":
        add_bot(f"Ótimo! Agende sua reunião: {CALENDLY_LINK}")
        st.session_state.estado = "FIM"

    # ========== PS NEGATIVA DE CIRURGIA ==========
    elif estado == "PS_NEG_CIR_ESP":
        dados["ps_cir_esp"] = resposta
        if "endometriose" in _n(resposta) or "1" in resposta:
            st.session_state.estado = "PS_ENDO_Q1"
            add_bot(PS_ENDO_Q1)
        elif "bariátrica" in _n(resposta) or "2" in resposta:
            st.session_state.estado = "PS_BARI_Q1"
            add_bot(PS_BARI_Q1)
        elif "oncologia" in _n(resposta) or "3" in resposta:
            st.session_state.estado = "PS_ONCO_Q1"
            add_bot(PS_ONCO_Q1)
        elif "cardiologia" in _n(resposta) or "4" in resposta:
            st.session_state.estado = "PS_CARDIO_Q1"
            add_bot(PS_CARDIO_Q1)
        elif "neuro" in _n(resposta) or "5" in resposta:
            st.session_state.estado = "PS_NEURO_Q1"
            add_bot(PS_NEURO_Q1)
        elif "ortopedia" in _n(resposta) or "6" in resposta:
            st.session_state.estado = "PS_ORTO_Q1"
            add_bot(PS_ORTO_Q1)
        elif "oftalmologia" in _n(resposta) or "7" in resposta:
            st.session_state.estado = "PS_OFTAL_Q1"
            add_bot(PS_OFTAL_Q1)
        else:
            st.session_state.estado = "PS_CIR_OUTRO"
            add_bot("👉 Qual cirurgia foi indicada pelo seu médico?")

    # PS ENDOMETRIOSE
    elif estado == "PS_ENDO_Q1":
        dados["ps_endo_q1"] = resposta
        st.session_state.estado = "PS_ENDO_Q2"
        add_bot(PS_ENDO_Q2)
    elif estado == "PS_ENDO_Q2":
        dados["ps_endo_q2"] = resposta
        st.session_state.estado = "PS_ENDO_Q3"
        add_bot(PS_ENDO_Q3)
    elif estado == "PS_ENDO_Q3":
        dados["ps_endo_q3"] = resposta
        st.session_state.estado = "PS_ENDO_Q4"
        add_bot(PS_ENDO_Q4)
    elif estado == "PS_ENDO_Q4":
        dados["ps_endo_q4"] = resposta
        st.session_state.estado = "PS_ENDO_Q5"
        add_bot(PS_ENDO_Q5)
    elif estado == "PS_ENDO_Q5":
        dados["ps_endo_q5"] = resposta
        st.session_state.estado = "PS_ENDO_Q6"
        add_bot(PS_ENDO_Q6)
    elif estado == "PS_ENDO_Q6":
        dados["ps_endo_q6"] = resposta
        st.session_state.estado = "PS_POS"
        add_bot(PS_POS)

    # PS BARIÁTRICA
    elif estado == "PS_BARI_Q1":
        dados["ps_bari_q1"] = resposta
        st.session_state.estado = "PS_BARI_Q2"
        add_bot(PS_BARI_Q2)
    elif estado == "PS_BARI_Q2":
        dados["ps_bari_q2"] = resposta
        st.session_state.estado = "PS_BARI_Q3"
        add_bot(PS_BARI_Q3)
    elif estado == "PS_BARI_Q3":
        dados["ps_bari_q3"] = resposta
        st.session_state.estado = "PS_BARI_Q4"
        add_bot(PS_BARI_Q4)
    elif estado == "PS_BARI_Q4":
        dados["ps_bari_q4"] = resposta
        st.session_state.estado = "PS_BARI_Q5"
        add_bot(PS_BARI_Q5)
    elif estado == "PS_BARI_Q5":
        dados["ps_bari_q5"] = resposta
        st.session_state.estado = "PS_BARI_Q6"
        add_bot(PS_BARI_Q6)
    elif estado == "PS_BARI_Q6":
        dados["ps_bari_q6"] = resposta
        st.session_state.estado = "PS_BARI_Q7"
        add_bot(PS_BARI_Q7)
    elif estado == "PS_BARI_Q7":
        dados["ps_bari_q7"] = resposta
        st.session_state.estado = "PS_BARI_Q8"
        add_bot(PS_BARI_Q8)
    elif estado == "PS_BARI_Q8":
        dados["ps_bari_q8"] = resposta
        st.session_state.estado = "PS_POS"
        add_bot(PS_POS)

    # PS ONCOLOGIA
    elif estado == "PS_ONCO_Q1":
        dados["ps_onco_q1"] = resposta
        st.session_state.estado = "PS_ONCO_Q2"
        add_bot(PS_ONCO_Q2)
    elif estado == "PS_ONCO_Q2":
        dados["ps_onco_q2"] = resposta
        st.session_state.estado = "PS_ONCO_Q3"
        add_bot(PS_ONCO_Q3)
    elif estado == "PS_ONCO_Q3":
        dados["ps_onco_q3"] = resposta
        st.session_state.estado = "PS_ONCO_Q4"
        add_bot(PS_ONCO_Q4)
    elif estado == "PS_ONCO_Q4":
        dados["ps_onco_q4"] = resposta
        st.session_state.estado = "PS_ONCO_Q5"
        add_bot(PS_ONCO_Q5)
    elif estado == "PS_ONCO_Q5":
        dados["ps_onco_q5"] = resposta
        st.session_state.estado = "PS_ONCO_Q6"
        add_bot(PS_ONCO_Q6)
    elif estado == "PS_ONCO_Q6":
        dados["ps_onco_q6"] = resposta
        st.session_state.estado = "PS_ONCO_Q7"
        add_bot(PS_ONCO_Q7)
    elif estado == "PS_ONCO_Q7":
        dados["ps_onco_q7"] = resposta
        st.session_state.estado = "PS_POS"
        add_bot(PS_POS)

    # PS CARDIOLOGIA
    elif estado == "PS_CARDIO_Q1":
        dados["ps_cardio_q1"] = resposta
        st.session_state.estado = "PS_CARDIO_Q2"
        add_bot(PS_CARDIO_Q2)
    elif estado == "PS_CARDIO_Q2":
        dados["ps_cardio_q2"] = resposta
        st.session_state.estado = "PS_CARDIO_Q3"
        add_bot(PS_CARDIO_Q3)
    elif estado == "PS_CARDIO_Q3":
        dados["ps_cardio_q3"] = resposta
        st.session_state.estado = "PS_CARDIO_Q4"
        add_bot(PS_CARDIO_Q4)
    elif estado == "PS_CARDIO_Q4":
        dados["ps_cardio_q4"] = resposta
        st.session_state.estado = "PS_CARDIO_Q5"
        add_bot(PS_CARDIO_Q5)
    elif estado == "PS_CARDIO_Q5":
        dados["ps_cardio_q5"] = resposta
        st.session_state.estado = "PS_CARDIO_Q6"
        add_bot(PS_CARDIO_Q6)
    elif estado == "PS_CARDIO_Q6":
        dados["ps_cardio_q6"] = resposta
        st.session_state.estado = "PS_CARDIO_Q7"
        add_bot(PS_CARDIO_Q7)
    elif estado == "PS_CARDIO_Q7":
        dados["ps_cardio_q7"] = resposta
        st.session_state.estado = "PS_POS"
        add_bot(PS_POS)

    # PS NEUROCIRURGIA
    elif estado == "PS_NEURO_Q1":
        dados["ps_neuro_q1"] = resposta
        st.session_state.estado = "PS_NEURO_Q2"
        add_bot(PS_NEURO_Q2)
    elif estado == "PS_NEURO_Q2":
        dados["ps_neuro_q2"] = resposta
        st.session_state.estado = "PS_NEURO_Q3"
        add_bot(PS_NEURO_Q3)
    elif estado == "PS_NEURO_Q3":
        dados["ps_neuro_q3"] = resposta
        st.session_state.estado = "PS_NEURO_Q4"
        add_bot(PS_NEURO_Q4)
    elif estado == "PS_NEURO_Q4":
        dados["ps_neuro_q4"] = resposta
        st.session_state.estado = "PS_NEURO_Q5"
        add_bot(PS_NEURO_Q5)
    elif estado == "PS_NEURO_Q5":
        dados["ps_neuro_q5"] = resposta
        st.session_state.estado = "PS_NEURO_Q6"
        add_bot(PS_NEURO_Q6)
    elif estado == "PS_NEURO_Q6":
        dados["ps_neuro_q6"] = resposta
        st.session_state.estado = "PS_NEURO_Q7"
        add_bot(PS_NEURO_Q7)
    elif estado == "PS_NEURO_Q7":
        dados["ps_neuro_q7"] = resposta
        st.session_state.estado = "PS_NEURO_Q8"
        add_bot(PS_NEURO_Q8)
    elif estado == "PS_NEURO_Q8":
        dados["ps_neuro_q8"] = resposta
        st.session_state.estado = "PS_NEURO_Q9"
        add_bot(PS_NEURO_Q9)
    elif estado == "PS_NEURO_Q9":
        dados["ps_neuro_q9"] = resposta
        st.session_state.estado = "PS_POS"
        add_bot(PS_POS)

    # PS ORTOPEDIA
    elif estado == "PS_ORTO_Q1":
        dados["ps_orto_q1"] = resposta
        st.session_state.estado = "PS_ORTO_Q2"
        add_bot(PS_ORTO_Q2)
    elif estado == "PS_ORTO_Q2":
        dados["ps_orto_q2"] = resposta
        st.session_state.estado = "PS_ORTO_Q3"
        add_bot(PS_ORTO_Q3)
    elif estado == "PS_ORTO_Q3":
        dados["ps_orto_q3"] = resposta
        st.session_state.estado = "PS_ORTO_Q4"
        add_bot(PS_ORTO_Q4)
    elif estado == "PS_ORTO_Q4":
        dados["ps_orto_q4"] = resposta
        st.session_state.estado = "PS_ORTO_Q5"
        add_bot(PS_ORTO_Q5)
    elif estado == "PS_ORTO_Q5":
        dados["ps_orto_q5"] = resposta
        st.session_state.estado = "PS_ORTO_Q6"
        add_bot(PS_ORTO_Q6)
    elif estado == "PS_ORTO_Q6":
        dados["ps_orto_q6"] = resposta
        st.session_state.estado = "PS_ORTO_Q7"
        add_bot(PS_ORTO_Q7)
    elif estado == "PS_ORTO_Q7":
        dados["ps_orto_q7"] = resposta
        st.session_state.estado = "PS_POS"
        add_bot(PS_POS)

    # PS OFTALMOLOGIA
    elif estado == "PS_OFTAL_Q1":
        dados["ps_oftal_q1"] = resposta
        st.session_state.estado = "PS_OFTAL_Q2"
        add_bot(PS_OFTAL_Q2)
    elif estado == "PS_OFTAL_Q2":
        dados["ps_oftal_q2"] = resposta
        st.session_state.estado = "PS_OFTAL_Q3"
        add_bot(PS_OFTAL_Q3)
    elif estado == "PS_OFTAL_Q3":
        dados["ps_oftal_q3"] = resposta
        st.session_state.estado = "PS_OFTAL_Q4"
        add_bot(PS_OFTAL_Q4)
    elif estado == "PS_OFTAL_Q4":
        dados["ps_oftal_q4"] = resposta
        st.session_state.estado = "PS_OFTAL_Q5"
        add_bot(PS_OFTAL_Q5)
    elif estado == "PS_OFTAL_Q5":
        dados["ps_oftal_q5"] = resposta
        st.session_state.estado = "PS_OFTAL_Q6"
        add_bot(PS_OFTAL_Q6)
    elif estado == "PS_OFTAL_Q6":
        dados["ps_oftal_q6"] = resposta
        st.session_state.estado = "PS_POS"
        add_bot(PS_POS)

    # PS MEDICAMENTO
    elif estado == "PS_MED_Q1":
        dados["ps_med_q1"] = resposta
        st.session_state.estado = "PS_MED_Q2"
        add_bot(PS_MED_Q2)
    elif estado == "PS_MED_Q2":
        dados["ps_med_q2"] = resposta
        st.session_state.estado = "PS_MED_Q3"
        add_bot(PS_MED_Q3)
    elif estado == "PS_MED_Q3":
        dados["ps_med_q3"] = resposta
        st.session_state.estado = "PS_MED_Q4"
        add_bot(PS_MED_Q4)
    elif estado == "PS_MED_Q4":
        dados["ps_med_q4"] = resposta
        st.session_state.estado = "PS_MED_Q5"
        add_bot(PS_MED_Q5)
    elif estado == "PS_MED_Q5":
        dados["ps_med_q5"] = resposta
        st.session_state.estado = "PS_MED_Q6"
        add_bot(PS_MED_Q6)
    elif estado == "PS_MED_Q6":
        dados["ps_med_q6"] = resposta
        st.session_state.estado = "PS_MED_Q7"
        add_bot(PS_MED_Q7)
    elif estado == "PS_MED_Q7":
        dados["ps_med_q7"] = resposta
        st.session_state.estado = "PS_MED_Q8"
        add_bot(PS_MED_Q8)
    elif estado == "PS_MED_Q8":
        dados["ps_med_q8"] = resposta
        st.session_state.estado = "PS_MED_Q9"
        add_bot(PS_MED_Q9)
    elif estado == "PS_MED_Q9":
        dados["ps_med_q9"] = resposta
        st.session_state.estado = "PS_MED_Q10"
        add_bot(PS_MED_Q10)
    elif estado == "PS_MED_Q10":
        dados["ps_med_q10"] = resposta
        st.session_state.estado = "PS_POS"
        add_bot(PS_POS)

    # PS EXAME
    elif estado == "PS_EXAME_Q1":
        dados["ps_exame_q1"] = resposta
        st.session_state.estado = "PS_EXAME_Q2"
        add_bot(PS_EXAME_Q2)
    elif estado == "PS_EXAME_Q2":
        dados["ps_exame_q2"] = resposta
        st.session_state.estado = "PS_EXAME_Q3"
        add_bot(PS_EXAME_Q3)
    elif estado == "PS_EXAME_Q3":
        dados["ps_exame_q3"] = resposta
        st.session_state.estado = "PS_EXAME_Q4"
        add_bot(PS_EXAME_Q4)
    elif estado == "PS_EXAME_Q4":
        dados["ps_exame_q4"] = resposta
        st.session_state.estado = "PS_EXAME_Q5"
        add_bot(PS_EXAME_Q5)
    elif estado == "PS_EXAME_Q5":
        dados["ps_exame_q5"] = resposta
        st.session_state.estado = "PS_EXAME_Q6"
        add_bot(PS_EXAME_Q6)
    elif estado == "PS_EXAME_Q6":
        dados["ps_exame_q6"] = resposta
        st.session_state.estado = "PS_EXAME_Q7"
        add_bot(PS_EXAME_Q7)
    elif estado == "PS_EXAME_Q7":
        dados["ps_exame_q7"] = resposta
        st.session_state.estado = "PS_POS"
        add_bot(PS_POS)

    # PS HOME CARE
    elif estado == "PS_HOME_Q1":
        dados["ps_home_q1"] = resposta
        st.session_state.estado = "PS_HOME_Q2"
        add_bot(PS_HOME_Q2)
    elif estado == "PS_HOME_Q2":
        dados["ps_home_q2"] = resposta
        st.session_state.estado = "PS_HOME_Q3"
        add_bot(PS_HOME_Q3)
    elif estado == "PS_HOME_Q3":
        dados["ps_home_q3"] = resposta
        st.session_state.estado = "PS_HOME_Q4"
        add_bot(PS_HOME_Q4)
    elif estado == "PS_HOME_Q4":
        dados["ps_home_q4"] = resposta
        st.session_state.estado = "PS_HOME_Q5"
        add_bot(PS_HOME_Q5)
    elif estado == "PS_HOME_Q5":
        dados["ps_home_q5"] = resposta
        st.session_state.estado = "PS_HOME_Q6"
        add_bot(PS_HOME_Q6)
    elif estado == "PS_HOME_Q6":
        dados["ps_home_q6"] = resposta
        st.session_state.estado = "PS_HOME_Q7"
        add_bot(PS_HOME_Q7)
    elif estado == "PS_HOME_Q7":
        dados["ps_home_q7"] = resposta
        st.session_state.estado = "PS_POS"
        add_bot(PS_POS)

    # PS TERAPIAS
    elif estado == "PS_TERA_Q1":
        dados["ps_tera_q1"] = resposta
        st.session_state.estado = "PS_TERA_Q2"
        add_bot(PS_TERA_Q2)
    elif estado == "PS_TERA_Q2":
        dados["ps_tera_q2"] = resposta
        st.session_state.estado = "PS_TERA_Q3"
        add_bot(PS_TERA_Q3)
    elif estado == "PS_TERA_Q3":
        dados["ps_tera_q3"] = resposta
        st.session_state.estado = "PS_TERA_Q4"
        add_bot(PS_TERA_Q4)
    elif estado == "PS_TERA_Q4":
        dados["ps_tera_q4"] = resposta
        st.session_state.estado = "PS_TERA_Q5"
        add_bot(PS_TERA_Q5)
    elif estado == "PS_TERA_Q5":
        dados["ps_tera_q5"] = resposta
        st.session_state.estado = "PS_TERA_Q6"
        add_bot(PS_TERA_Q6)
    elif estado == "PS_TERA_Q6":
        dados["ps_tera_q6"] = resposta
        st.session_state.estado = "PS_TERA_Q7"
        add_bot(PS_TERA_Q7)
    elif estado == "PS_TERA_Q7":
        dados["ps_tera_q7"] = resposta
        st.session_state.estado = "PS_POS"
        add_bot(PS_POS)

    # PS REAJUSTE
    elif estado == "PS_REAJ_Q1":
        dados["ps_reaj_q1"] = resposta
        st.session_state.estado = "PS_REAJ_Q2"
        add_bot(PS_REAJ_Q2)
    elif estado == "PS_REAJ_Q2":
        dados["ps_reaj_q2"] = resposta
        st.session_state.estado = "PS_REAJ_Q3"
        add_bot(PS_REAJ_Q3)
    elif estado == "PS_REAJ_Q3":
        dados["ps_reaj_q3"] = resposta
        st.session_state.estado = "PS_REAJ_Q4"
        add_bot(PS_REAJ_Q4)
    elif estado == "PS_REAJ_Q4":
        dados["ps_reaj_q4"] = resposta
        st.session_state.estado = "PS_REAJ_Q5"
        add_bot(PS_REAJ_Q5)
    elif estado == "PS_REAJ_Q5":
        dados["ps_reaj_q5"] = resposta
        st.session_state.estado = "PS_REAJ_Q6"
        add_bot(PS_REAJ_Q6)
    elif estado == "PS_REAJ_Q6":
        dados["ps_reaj_q6"] = resposta
        st.session_state.estado = "PS_REAJ_Q7"
        add_bot(PS_REAJ_Q7)
    elif estado == "PS_REAJ_Q7":
        dados["ps_reaj_q7"] = resposta
        st.session_state.estado = "PS_REAJ_Q8"
        add_bot(PS_REAJ_Q8)
    elif estado == "PS_REAJ_Q8":
        dados["ps_reaj_q8"] = resposta
        st.session_state.estado = "PS_POS"
        add_bot(PS_POS)

    # PS COPARTICIPAÇÃO
    elif estado == "PS_COPA_Q1":
        dados["ps_copa_q1"] = resposta
        st.session_state.estado = "PS_COPA_Q2"
        add_bot(PS_COPA_Q2)
    elif estado == "PS_COPA_Q2":
        dados["ps_copa_q2"] = resposta
        st.session_state.estado = "PS_COPA_Q3"
        add_bot(PS_COPA_Q3)
    elif estado == "PS_COPA_Q3":
        dados["ps_copa_q3"] = resposta
        st.session_state.estado = "PS_COPA_Q4"
        add_bot(PS_COPA_Q4)
    elif estado == "PS_COPA_Q4":
        dados["ps_copa_q4"] = resposta
        st.session_state.estado = "PS_COPA_Q5"
        add_bot(PS_COPA_Q5)
    elif estado == "PS_COPA_Q5":
        dados["ps_copa_q5"] = resposta
        st.session_state.estado = "PS_COPA_Q6"
        add_bot(PS_COPA_Q6)
    elif estado == "PS_COPA_Q6":
        dados["ps_copa_q6"] = resposta
        st.session_state.estado = "PS_COPA_Q7"
        add_bot(PS_COPA_Q7)
    elif estado == "PS_COPA_Q7":
        dados["ps_copa_q7"] = resposta
        st.session_state.estado = "PS_POS"
        add_bot(PS_POS)

    # PS ERRO MÉDICO
    elif estado == "PS_ERRO_Q1":
        dados["ps_erro_q1"] = resposta
        st.session_state.estado = "PS_ERRO_Q2"
        add_bot(PS_ERRO_Q2)
    elif estado == "PS_ERRO_Q2":
        dados["ps_erro_q2"] = resposta
        st.session_state.estado = "PS_ERRO_Q3"
        add_bot(PS_ERRO_Q3)
    elif estado == "PS_ERRO_Q3":
        dados["ps_erro_q3"] = resposta
        st.session_state.estado = "PS_ERRO_Q4"
        add_bot(PS_ERRO_Q4)
    elif estado == "PS_ERRO_Q4":
        dados["ps_erro_q4"] = resposta
        st.session_state.estado = "PS_ERRO_Q5"
        add_bot(PS_ERRO_Q5)
    elif estado == "PS_ERRO_Q5":
        dados["ps_erro_q5"] = resposta
        st.session_state.estado = "PS_ERRO_Q6"
        add_bot(PS_ERRO_Q6)
    elif estado == "PS_ERRO_Q6":
        dados["ps_erro_q6"] = resposta
        st.session_state.estado = "PS_POS"
        add_bot(PS_POS)

    # PS OUTRO
    elif estado == "PS_OUTRO_Q1":
        dados["ps_outro_q1"] = resposta
        st.session_state.estado = "PS_OUTRO_Q2"
        add_bot(PS_OUTRO_Q2)
    elif estado == "PS_OUTRO_Q2":
        dados["ps_outro_q2"] = resposta
        st.session_state.estado = "PS_OUTRO_Q3"
        add_bot(PS_OUTRO_Q3)
    elif estado == "PS_OUTRO_Q3":
        dados["ps_outro_q3"] = resposta
        st.session_state.estado = "PS_OUTRO_Q4"
        add_bot(PS_OUTRO_Q4)
    elif estado == "PS_OUTRO_Q4":
        dados["ps_outro_q4"] = resposta
        st.session_state.estado = "PS_OUTRO_Q5"
        add_bot(PS_OUTRO_Q5)
    elif estado == "PS_OUTRO_Q5":
        dados["ps_outro_q5"] = resposta
        st.session_state.estado = "PS_OUTRO_Q6"
        add_bot(PS_OUTRO_Q6)
    elif estado == "PS_OUTRO_Q6":
        dados["ps_outro_q6"] = resposta
        st.session_state.estado = "PS_OUTRO_Q7"
        add_bot(PS_OUTRO_Q7)
    elif estado == "PS_OUTRO_Q7":
        dados["ps_outro_q7"] = resposta
        st.session_state.estado = "PS_POS"
        add_bot(PS_POS)

    # PS_CIR_OUTRO
    elif estado == "PS_CIR_OUTRO":
        dados["ps_cir_outro"] = resposta
        st.session_state.estado = "PS_POS"
        add_bot(PS_POS)

    # PS_POS
    elif estado == "PS_POS":
        dados["ps_pos_escolha"] = resposta
        if "1" in resposta:
            add_bot(PS_OP1)
            st.session_state.estado = "PS_OP1_AGUARDANDO"
        elif "2" in resposta:
            add_bot(PS_OP2)
            add_bot(f"🔗 Agende sua reunião: {CALENDLY_LINK}")
            st.session_state.estado = "FIM"
        elif "3" in resposta:
            add_bot(PS_OP3)
            st.session_state.estado = "PS_PREVENTIVO"
        else:
            add_bot(PS_POS)

    elif estado == "PS_OP1_AGUARDANDO":
        if _sim(resposta):
            add_bot(f"Ótimo! Agende sua consulta: {CALENDLY_LINK}")
        else:
            add_bot("Quando decidir, estou à disposição. 🙏")
        st.session_state.estado = "FIM"

    elif estado == "PS_PREVENTIVO":
        if "acompanhamento" in _n(resposta):
            add_bot(f"Perfeito! Agende sua reunião: {CALENDLY_LINK}")
        else:
            add_bot(PS_ENCERRAMENTO)
        st.session_state.estado = "FIM"

    elif estado == "PROPOSTA_JUDICIAL":
        if _sim(resposta):
            add_bot(f"Ótimo! Agende sua reunião: {CALENDLY_LINK}")
        else:
            add_bot(MSG_NAO)
        st.session_state.estado = "FIM"

    elif estado == "FIM":
        add_bot("Atendimento finalizado. Se precisar novamente, digite 'oi' para recomeçar.")

# ============================================
# INTERFACE
# ============================================

def render_sidebar():
    with st.sidebar:
        st.markdown(f"## ⚖️ {L}")
        st.markdown("*Especialista em Direito da Saúde*")
        st.markdown("---")
        
        if st.session_state.nome:
            st.markdown(f"**Cliente:** {st.session_state.nome}")
        if st.session_state.dados.get("canal"):
            st.markdown(f"**Canal:** {st.session_state.dados['canal']}")
        
        st.markdown("---")
        if st.button("🔄 Nova Conversa", use_container_width=True):
            reset()
            st.rerun()

def render_chat():
    with st.container():
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for msg in st.session_state.messages:
            if msg["role"] == "bot":
                st.markdown(f'<div class="chat-message bot-message"><strong>🤖 Lara:</strong><br>{msg["content"]}</div>', unsafe_allow_html=True)
            else:
                nome = st.session_state.nome or "Você"
                st.markdown(f'<div class="chat-message user-message"><strong>👤 {nome}:</strong><br>{msg["content"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

def render_botoes():
    estado = st.session_state.estado
    
    if estado == "CANAL":
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🏥 SUS", use_container_width=True):
                add_user("SUS")
                processar("SUS")
                st.rerun()
        with col2:
            if st.button("📋 Plano de Saúde", use_container_width=True):
                add_user("Plano de Saúde")
                processar("Plano de Saúde")
                st.rerun()
    
    elif estado == "SUS_DEMANDA":
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔪 Cirurgia", use_container_width=True):
                add_user("Cirurgia")
                processar("Cirurgia")
                st.rerun()
        with col2:
            if st.button("📋 Consultas/Exames", use_container_width=True):
                add_user("Consultas")
                processar("Consultas")
                st.rerun()
    
    elif estado == "SUS_ESPECIALIDADE":
        st.markdown("---")
        st.markdown("**🔘 Especialidades:**")
        especialidades = ["Oncologia", "Neuro", "Endometriose", "Medicamento", "Bariátrica", "Reparadora", "Neurologia", "Cardiologia", "Outros"]
        cols = st.columns(3)
        for i, esp in enumerate(especialidades):
            with cols[i % 3]:
                if st.button(esp[:12], use_container_width=True):
                    add_user(esp)
                    processar(esp)
                    st.rerun()
    
    elif estado in ["HONORARIOS", "RESPOSTA_HONORARIOS", "PS_OP1_AGUARDANDO", "PROPOSTA_JUDICIAL"]:
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ SIM", use_container_width=True):
                add_user("SIM")
                processar("SIM")
                st.rerun()
        with col2:
            if st.button("❌ NÃO", use_container_width=True):
                add_user("NÃO")
                processar("NÃO")
                st.rerun()

def render_input():
    estado = st.session_state.estado
    
    if estado == "FIM":
        st.info("✨ Atendimento finalizado. Clique em 'Nova Conversa' para recomeçar.")
        return
    
    col1, col2 = st.columns([4, 1])
    with col1:
        user_input = st.text_input("Digite sua mensagem:", key="user_input", placeholder="Digite aqui sua resposta...")
    with col2:
        send = st.button("📤 Enviar", use_container_width=True)
    
    if user_input and any(p in _n(user_input) for p in ["valor", "quanto", "preço", "custa", "honorário", "investimento"]):
        add_user(user_input)
        add_bot(f"Compreendo sua dúvida. A {L} não define valores por mensagem. Para casos cirúrgicos, é necessária uma Reunião Estratégica por vídeo.\n\n🔗 {CALENDLY_LINK}")
        st.rerun()
    
    if send and user_input:
        add_user(user_input)
        processar(user_input)
        st.rerun()

# ============================================
# MAIN
# ============================================

def main():
    st.title("⚖️ Lara Bot - Assistente Jurídica em Direito da Saúde")
    st.caption(f"{L} | Atendimento SUS e Planos de Saúde")
    
    init_session()
    
    col1, col2 = st.columns([3, 1])
    with col1:
        render_chat()
        render_botoes()
        render_input()
    with col2:
        render_sidebar()
    
    if len(st.session_state.messages) == 0:
        add_bot(MSG_BOAS_VINDAS)
        st.rerun()

if __name__ == "__main__":
    main()
