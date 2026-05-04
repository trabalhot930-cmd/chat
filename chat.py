"""
Iara Bot - Assistente Jurídica em Direito da Saúde
VERSÃO PERFEITA E COMPLETA - SUS + PLANO DE SAÚDE 100% CORRETO
"""

import streamlit as st

# ============================================
# CONFIGURAÇÕES
# ============================================
CALENDLY_LINK = "https://calendly.com/dra-lethicia"
L = "Dra. Lethicia Fernanda"

# Links de Pagamento Asaas
LINK_CARTAO_97 = "https://www.asaas.com/c/oilhnffc7xyvc4n6"
LINK_PIX_97 = "https://www.asaas.com/c/9025wgqkpuziono4"
LINK_CARTAO_500 = "https://www.asaas.com/c/apigp8m45tileghw"
LINK_PIX_500 = "https://www.asaas.com/c/x1dfvyoajxnlgpp2"

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
    return any(p in _n(r) for p in ["sim", "s", "yes", "quero", "ok", "claro", "vamos", "aceito", "topo"])

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
    if "respostas_nao" not in st.session_state:
        st.session_state.respostas_nao = 0

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

# ============================================
# SUS - MENSAGENS (resumidas por espaço)
# ============================================

MSG_SUS_DEMANDA = "Me diga o que você está aguardando?\n\n🔪 Cirurgia / Tratamento\n\n📋 Consultas / Exames"

MSG_SUS_ESPECIALIDADE = (
    "Para que eu direcione você para o protocolo de urgência correto, "
    "qual problema estamos enfrentando hoje?\n\n"
    "1️⃣ Oncologia\n2️⃣ Neurodivergências (TEA, TDAH)\n3️⃣ Endometriose / Adenomiose\n"
    "4️⃣ Medicamento\n5️⃣ Bariátrica\n6️⃣ Neurologia / Neurocirurgia\n"
    "7️⃣ Cardiologia\n8️⃣ Outros"
)

PERGUNTAS_ONCOLOGIA = [
    "Entendi… vamos cuidar disso juntos 💙\n\n👉 Você consegue me contar qual é o tipo de câncer?",
    "👉 Você está aguardando atendimento ou tratamento pelo SUS? Se sim, há quanto tempo mais ou menos?",
    "👉 O diagnóstico já foi confirmado por biópsia? E você tem esse laudo em mãos?",
    "👉 Você já foi encaminhado para um hospital especializado em câncer pelo SUS?",
    "👉 Você possui um relatório médico explicando o tratamento que precisa fazer?",
    "👉 O médico falou se o seu caso é urgente?",
    "👉 Você possui o comprovante de que está aguardando na fila?"
]

PERGUNTAS_NEURO = [
    "Entendi… pode ficar tranquilo(a), vou te ajudar com isso 💙\n\n👉 Me conta: já tem diagnóstico fechado?",
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

MSG_POS_PERGUNTAS = (
    "_{nome}_, recebi suas respostas aqui. O que mais me preocupa no seu caso é que o SUS "
    "trata essa situação como se pudesse esperar, mas juridicamente sabemos que o *tempo é o seu maior inimigo agora*.\n\n"
    "Você sente que, se não resolvermos isso nos próximos dias, a sua saúde corre um risco de piorar de forma irreversível?"
)

MSG_EXPLICACAO = (
    "Só pra te explicar de forma simples:\n\n"
    "Quando o paciente precisa de atendimento, exame ou tratamento e não consegue pelo SUS, "
    "a Justiça pode intervir pra garantir esse direito.\n\n"
    "Para resolver isso, eu trabalho com um *Protocolo de Liberação Urgente*. "
    "Isso faria diferença na sua vida agora?"
)

MSG_HONORARIOS = (
    "Como é um trabalho de alta especialidade, o escritório cobra *Honorários Iniciais* "
    "para assumir o caso e protocolar o pedido de liminar. Prosseguir com esse caso faz sentido "
    "para você garantir sua saúde hoje e sair dessa espera?"
)

MSG_ENCERRAMENTO_SUS = (
    "Compreendo. Infelizmente, sem o interesse em avançar com uma medida judicial, "
    "o seu caso continuará dependendo exclusivamente da velocidade da fila do SUS.\n\n"
    "Caso a sua situação se agrave, sinta-se à vontade para retornar. Desejamos sorte no seu tratamento. 🙏"
)

MSG_SIM_HONORARIOS = (
    "Ótimo. Isso mostra que você prioriza sua saúde acima da burocracia do Estado.\n\n"
    "Vou encaminhar seus dados para a mesa da Dra. Lethicia neste momento. Em instantes, ela entrará em contato aqui por este chat para te passar a estratégia de liberação e os valores para o seu caso. Fique atento(a)!"
)


# ============================================
# PLANO DE SAÚDE - MENSAGENS COMPLETAS
# ============================================

# Qualificação Inicial
PS_TEMPO = "Você já tem seu plano de saúde há mais de 2 anos?\n\n1️⃣ Sim\n2️⃣ Não"

# Caminho SIM - Lista de situações
PS_SITUACAO = (
    "Para que eu possa te direcionar corretamente, qual é a sua situação atual com o plano de saúde?\n\n"
    "1️⃣ Reparadora\n2️⃣ Negativa de cirurgia\n3️⃣ Medicamento negado\n4️⃣ Exame negado\n"
    "5️⃣ Home care\n6️⃣ Terapias (fono, ABA, fisio, psicopedagogia...)\n7️⃣ Reajuste\n"
    "8️⃣ Coparticipação elevada\n9️⃣ Erro médico\n🔟 OUTRO"
)

# ============================================
# 1. FLUXO REPARADORA
# ============================================
PS_REP_Q1 = "👉 Você realizou a cirurgia bariátrica ou teve uma perda de peso expressiva através de dieta, exercícios ou uso das canetas emagrecedoras (Mounjaro, Ozempic, Tirzepatida...)?"
PS_REP_Q2 = "👉 Você já chegou ou ainda falta pouco pro peso que gostaria?\n\n1️⃣ Sim, já atingi meu objetivo\n2️⃣ Ainda não"
PS_REP_NAO_PESO = (
    "Faz todo sentido querer entender bem a situação antes de tomar qualquer decisão.\n\n"
    "Para isso, ofereço uma *consulta de orientação jurídica* — você fala diretamente com a Dra., "
    "tira todas as suas dúvidas e entende com clareza quais são seus direitos e quais caminhos "
    "existem para o seu caso.\n\n"
    "💬 O valor da consulta é de *R$ 67,00* e é feita online, no horário que melhor funcionar pra você. "
    "E se durante ou depois da consulta você decidir que quer avançar com o acompanhamento jurídico "
    "completo, também é possível — aí conversamos sobre isso na hora. Mas sem nenhuma pressão.\n\n"
    "Gostaria de agendar um horário ainda essa semana?"
)
PS_REP_EMPATIA = (
    "Eu entendo que essa pele que restou é o capítulo final de uma grande superação, mas ela também pode ser um peso físico e emocional. "
    "Para eu desenhar a melhor estratégia para você, me conte um pouco..."
)
PS_REP_Q3 = "👉 Esse excesso de pele hoje te causa dores, assaduras ou dermatites que não curam? E além do corpo, como isso tem afetado a sua autoestima e a sua liberdade de movimento no dia a dia?"
PS_REP_Q4 = "👉 Quais cirurgias reparadoras você teria interesse em fazer?"
PS_REP_Q5 = "Certo… Você já chegou a ir no médico cirurgião plástico pra solicitar as reparadoras e emitir os laudos?\n\n1️⃣ Sim\n2️⃣ Não"
PS_REP_ACOMPANHAMENTO = (
    "Você está no caminho certo 💙 Muitas pessoas acabam procurando ajuda só depois da negativa ou quando o problema já está mais avançado. "
    "Mas quando a gente atua antes, conseguimos evitar erros e fortalecer muito o caso.\n\n"
    "Você prefere tentar sozinho com o plano ou quer o acompanhamento da Dra. para garantir que o seu pedido seja feito à prova de negativas?"
)

# ============================================
# 2. FLUXO NEGATIVA DE CIRURGIA - ESPECIALIDADES
# ============================================
PS_NEG_CIR_ESP = "Qual é o diagnóstico ou o tratamento específico que o plano está dificultando no momento?\n\n1️⃣ Endometriose\n2️⃣ Bariátrica\n3️⃣ Oncologia (câncer)\n4️⃣ Cardiologia (coração)\n5️⃣ Neurocirurgia\n6️⃣ Ortopedia\n7️⃣ Oftalmologia\n8️⃣ OUTRO"

# 2A. ENDOMETRIOSE
PS_ENDO_Q1 = "Qual tipo de cirurgia foi indicada para o seu caso?"
PS_ENDO_Q2 = "Sinto muito que você esteja passando por isso. Sabemos que a endometriose não é 'só uma cólica', é algo que para a vida da mulher 💙\n\n👉 O plano negou formalmente ou simplesmente não respondeu?"
PS_ENDO_Q3 = "Sei o quanto a dor e a incerteza cansam, mas você merece viver com saúde e qualidade. Não é justo que a sua cirurgia seja negada depois de tanta espera. Vou te ajudar a destravar esse processo 💙\n\n👉 O plano justificou a negativa de alguma forma? (Ex: 'eletivo', 'sem cobertura', 'período de carência')"
PS_ENDO_Q4 = "👉 Você tem os exames que demonstram o seu diagnóstico?"
PS_ENDO_Q5 = "👉 Você já tentou resolver isso diretamente com o plano — ligação, protocolo, ouvidoria ou recurso formal?"

# 2B. BARIÁTRICA
PS_BARI_Q1 = "👉 Qual o seu IMC atual? Se não souber, pode me falar somente seu peso atual e sua altura"
PS_BARI_Q2 = "👉 Você tem comorbidades? (diabetes, hipertensão, apneia do sono, problemas nas articulações)"
PS_BARI_Q3 = "👉 Fez o acompanhamento multidisciplinar exigido (nutricionista, psicólogo, endocrinologista)?\n\n1️⃣ Sim\n2️⃣ Não"
PS_BARI_Q4 = "👉 O plano negou formalmente ou simplesmente não respondeu?"
PS_BARI_Q5 = "👉 O plano justificou a negativa de alguma forma? (Ex: 'eletivo', 'sem cobertura', 'período de carência')"
PS_BARI_Q6 = "👉 Você já tentou resolver isso diretamente com o plano — ligação, protocolo, ouvidoria ou recurso formal?"

# 2C. ONCOLOGIA
PS_ONCO_Q1 = "👉 Qual o tipo de câncer e qual procedimento foi indicado — cirurgia, quimio, radio, imunoterapia?"
PS_ONCO_Q2 = "👉 Já está em tratamento de alguma forma, ou a negativa está impedindo o início?"
PS_ONCO_Q3 = "Sinto muito que você esteja passando por isso, mas saiba que não está sozinha nessa luta. Vou cuidar de toda a burocracia para que você tenha seu tratamento sem interrupções. Seu foco agora deve ser apenas a sua cura: o resto, pode deixar aqui com a gente.\n\n👉 O plano negou formalmente ou simplesmente não respondeu?"
PS_ONCO_Q4 = "👉 O plano justificou a negativa de alguma forma? (Ex: 'eletivo', 'sem cobertura', 'período de carência')"
PS_ONCO_Q5 = "👉 Você tem os exames que demonstram o seu diagnóstico?"
PS_ONCO_Q6 = "👉 Você já tentou resolver isso diretamente com o plano — ligação, protocolo, ouvidoria ou recurso formal?"

# 2D. CARDIOLOGIA
PS_CARDIO_Q1 = "👉 Qual tipo de cirurgia foi indicada para o seu caso?"
PS_CARDIO_Q2 = "👉 No seu caso o plano negou material cirúrgico ou alguma prótese?"
PS_CARDIO_Q3 = "👉 O plano negou formalmente ou simplesmente não respondeu?"
PS_CARDIO_Q4 = "👉 Você já está internado aguardando o procedimento ou está em casa esperando a autorização para agendar?\n\n1️⃣ Já estou internado\n2️⃣ Estou em casa esperando"
PS_CARDIO_Q5 = "👉 O procedimento foi considerado urgente?\n\n1️⃣ Sim\n2️⃣ Não"
PS_CARDIO_Q6 = "👉 Você tem exames (ecocardiograma, cateterismo, ECG) que confirmam a necessidade cirúrgica?"

# 2E. NEUROCIRURGIA
PS_NEURO_Q1 = "👉 Qual procedimento neurocirúrgico foi indicado?"
PS_NEURO_Q2 = "👉 O paciente está internado ou com dor insuportável e precisa operar imediatamente?\n\n1️⃣ Sim\n2️⃣ Não"
PS_NEURO_Q3 = "👉 O hospital onde seria realizada a cirurgia é da rede do plano?\n\n1️⃣ Sim\n2️⃣ Não\n3️⃣ Não sei"
PS_NEURO_Q4 = "Sinto muito que você esteja passando por essa insegurança. Para eu desenhar a melhor estratégia jurídica, me conte:\n\n👉 Hoje, esse problema neurológico está afetando seus movimentos, causando perda de força ou dores que impedem você de realizar tarefas básicas?"
PS_NEURO_Q5 = "👉 A negativa foi por escrita ou verbal?"
PS_NEURO_Q6 = "👉 No seu caso o plano negou material cirúrgico ou alguma prótese?"
PS_NEURO_Q7 = "👉 Você tem exames de imagem — ressonância magnética, tomografia — que confirmam a necessidade cirúrgica?"

# 2F. ORTOPEDIA
PS_ORTO_Q1 = "👉 Qual cirurgia ortopédica foi indicada?"
PS_ORTO_Q2 = "👉 A condição está limitando sua mobilidade ou capacidade de trabalho?\n\n1️⃣ Sim, de forma significativa\n2️⃣ Parcialmente\n3️⃣ Ainda consigo me movimentar"
PS_ORTO_Q3 = "👉 O plano justificou a negativa de alguma forma? (Ex: 'eletivo', 'sem cobertura', 'período de carência')"
PS_ORTO_APOIO = "É muito comum os planos de saúde negarem tratamento com justificativas infundadas, ignorando a indicação do seu médico. Mas a lei é clara: quem decide o melhor pra você é ele, não o plano."
PS_ORTO_Q4 = "👉 No seu caso o plano negou material cirúrgico ou alguma prótese?"
PS_ORTO_Q5 = "👉 Essa negativa do plano foi por escrita ou verbal?"
PS_ORTO_Q6 = "👉 Você tem exames de imagem — ressonância magnética, tomografia — que confirmam a necessidade cirúrgica?"

# 2G. OFTALMOLOGIA
PS_OFTAL_Q1 = "👉 Qual cirurgia oftalmológica foi indicada?"
PS_OFTAL_Q2 = "👉 A condição está afetando sua visão de forma significativa?\n\n1️⃣ Sim, já estou com visão muito comprometida\n2️⃣ Está piorando progressivamente\n3️⃣ Ainda consigo enxergar razoavelmente"
PS_OFTAL_Q3 = "👉 O médico indicou urgência, risco de perda de visão se não operar logo?\n\n1️⃣ Sim, há urgência expressa no laudo\n2️⃣ O médico disse verbalmente, mas não está no laudo\n3️⃣ Não há urgência indicada"
PS_OFTAL_Q4 = "👉 O plano justificou a negativa de alguma forma? (Ex: 'eletivo', 'sem cobertura', 'período de carência')"
PS_OFTAL_Q5 = "👉 Essa negativa do plano foi por escrita ou verbal?"
PS_OFTAL_APOIO = "É muito comum os planos de saúde negarem tratamento com justificativas infundadas, ignorando a indicação do seu médico. Mas a lei é clara: quem decide o melhor pra você é ele, não o plano."

# 2H. OUTRO
PS_OUTRO_INTRO = "Entendido! Cada procedimento cirúrgico tem a sua importância e, se o seu médico indicou, é porque é necessário para a sua saúde. O plano não tem o direito de 'escolher' qual cirurgia você deve ou não fazer."
PS_OUTRO_Q1 = "👉 Qual cirurgia foi indicada pelo seu médico?"
PS_OUTRO_Q2 = "👉 Para qual problema ou doença ela foi recomendada?"
PS_OUTRO_Q3 = "👉 Você possui exames que comprovam a necessidade?\n\n1️⃣ Sim\n2️⃣ Não"
PS_OUTRO_Q4 = "👉 A cirurgia foi negada?\n\n1️⃣ Sim\n2️⃣ Não\n3️⃣ Ainda não solicitei"
PS_OUTRO_APOIO = "É muito comum os planos de saúde negarem tratamento com justificativas infundadas, ignorando a indicação do seu médico. Mas a lei é clara: quem decide o melhor pra você é ele, não o plano."
PS_OUTRO_Q5 = "👉 O plano justificou a negativa de alguma forma? (Ex: 'eletivo', 'sem cobertura', 'período de carência')"
PS_OUTRO_Q6 = "👉 Essa negativa do plano foi por escrita ou verbal?"
PS_OUTRO_Q7 = "👉 Hoje, a falta dessa cirurgia te impede de trabalhar, de dormir bem ou de realizar suas atividades simples do dia a dia?"
PS_OUTRO_Q8 = "👉 Se você não realizar a cirurgia, pode ocorrer:\n\n1️⃣ Dor intensa\n2️⃣ Agravamento do problema\n3️⃣ Risco à saúde\n4️⃣ Limitação no dia a dia"
PS_OUTRO_Q9 = "👉 Você possui exames que comprovam a necessidade?\n\n1️⃣ Sim\n2️⃣ Não"

# ============================================
# 3. FLUXO MEDICAMENTO NEGADO
# ============================================
PS_MED_Q1 = "👉 Qual doença você está tratando?"
PS_MED_Q2 = "👉 Qual medicamento foi prescrito pelo médico?"
PS_MED_Q3 = "👉 O fornecimento do medicamento foi negado?\n\n1️⃣ Sim\n2️⃣ Não\n3️⃣ Ainda não solicitei"
PS_MED_Q4 = "Eu sei que cada dia sem a medicação gera uma ansiedade enorme, afinal, a sua saúde não pode esperar o tempo do plano.\n\n👉 Hoje, a falta desse medicamento já está afetando o controle da sua doença ou causando sintomas que impedem sua rotina?"
PS_MED_Q5 = "👉 Qual foi o motivo da negativa?\n\n1️⃣ Fora do rol da ANS\n2️⃣ Alto custo\n3️⃣ Uso domiciliar\n4️⃣ Experimental/off-label\n5️⃣ Outro"
PS_MED_Q6 = "👉 Essa negativa do plano foi por escrita ou verbal?"
PS_MED_Q7 = "Muitos pacientes desistem quando ouvem que o remédio 'não está no Rol' ou 'é domiciliar' ou 'experimental', mas a verdade é que a justiça entende que se o seu médico prescreveu, o plano é obrigado a fornecer."
PS_MED_Q8 = "👉 Você possui receita médica do medicamento?\n\n1️⃣ Sim\n2️⃣ Não"
PS_MED_Q9 = "👉 Qual o valor aproximado do medicamento?"
PS_MED_Q10 = "👉 Você tem laudo médico explicando a necessidade do medicamento?\n\n1️⃣ Sim\n2️⃣ Não"

# ============================================
# 4. FLUXO EXAME NEGADO
# ============================================
PS_EXAME_Q1 = "👉 Qual exame foi solicitado pelo seu médico?"
PS_EXAME_Q2 = "👉 Para qual doença ou suspeita esse exame foi indicado?"
PS_EXAME_Q3 = "Sei o quão frustrante é ter um exame negado. Sem o exame, não há diagnóstico, e sem diagnóstico, não há tratamento. O plano não pode impedir a investigação da sua saúde."
PS_EXAME_Q4 = "👉 Você sente que essa demora do plano está prejudicando a sua saúde ou impedindo que você comece o tratamento que tanto precisa?"
PS_EXAME_Q5 = "👉 O que o seu médico lhe disse sobre a urgência deste resultado?"
PS_EXAME_Q6 = "👉 Qual foi o motivo da negativa?\n\n1️⃣ Fora do rol da ANS\n2️⃣ Não atende diretriz (DUT)\n3️⃣ Carência\n4️⃣ Não é urgente\n5️⃣ Experimental\n6️⃣ Outro"
PS_EXAME_Q7 = "👉 Essa negativa do plano foi por escrita ou verbal?"

# ============================================
# 5. FLUXO HOME CARE
# ============================================
PS_HOME_Q1 = "Sinto muito que você e sua família estejam passando por esse momento. Sabemos que o Home Care não é um 'luxo', mas a única forma de garantir dignidade, segurança e uma recuperação humanizada para quem você ama. 💙\n\n👉 Qual a doença ou condição do paciente?"
PS_HOME_Q2 = "👉 O paciente está acamado ou depende de cuidados constantes?"
PS_HOME_Q3 = "👉 O paciente já ficou internado recentemente?"
PS_HOME_Q4 = "Eu imagino o peso que está nos seus ombros agora. Cuidar de quem amamos exige muito, e sem a estrutura técnica correta, o medo de algo acontecer é constante.\n\n👉 Você sente que o plano de saúde está tentando transferir para a sua família uma responsabilidade médica que é deles?"
PS_HOME_Q5 = "👉 O home care foi negado?\n\n1️⃣ Sim\n2️⃣ Não\n3️⃣ Ainda não solicitei"
PS_HOME_Q6 = "👉 Você possui relatório médico detalhado?\n\n1️⃣ Sim\n2️⃣ Não"
PS_HOME_Q7 = "👉 Está descrito o tipo de cuidado necessário (enfermagem, 24h, etc.)?"

# ============================================
# 6. FLUXO TERAPIAS
# ============================================
PS_TERA_Q1 = "👉 O tratamento é para:\n\n1️⃣ Autismo (TEA)\n2️⃣ Desenvolvimento infantil\n3️⃣ Reabilitação física\n4️⃣ Saúde mental\n5️⃣ Outro"
PS_TERA_Q2 = "👉 Quais terapias foram indicadas pelo médico?\n\n1️⃣ ABA\n2️⃣ Fisioterapia\n3️⃣ Psicologia\n4️⃣ Fonoaudiologia\n5️⃣ Terapia ocupacional\n6️⃣ Psicopedagogia\n7️⃣ Musicoterapia\n8️⃣ Hidroterapia"
PS_TERA_Q3 = "👉 Quantas sessões por semana foram indicadas?"
PS_TERA_Q4 = "Eu entendo que essa não é apenas uma briga por 'papéis', é uma briga pelo futuro e pela autonomia sua ou de quem você ama. 💙\n\n👉 Hoje, a falta dessas terapias ou a limitação das sessões tem causado retrocessos ou estagnado a evolução que você(s) tanto espera(m)?"
PS_TERA_Q5 = "👉 O que aconteceu?\n\n1️⃣ Limitou número de sessões\n2️⃣ Negou totalmente\n3️⃣ Não tem profissional disponível\n4️⃣ Outro"
PS_TERA_Q6 = "👉 Você possui laudo médico com o diagnóstico?\n\n1️⃣ Sim\n2️⃣ Não"
PS_TERA_Q7 = "👉 Essa negativa do plano foi por escrita ou verbal?"

# ============================================
# 7. FLUXO REAJUSTE
# ============================================
PS_REAJ_Q1 = "Recebi seu contato e já quero te tranquilizar: você não precisa aceitar um reajuste que torna o seu plano de saúde impagável. Muitas vezes, esses aumentos são aplicados de forma ilegal para forçar o cancelamento do contrato, mas a justiça está aí para impedir isso. 💙\n\n👉 O plano é:\n\n1️⃣ Individual/Familiar\n2️⃣ Coletivo por adesão\n3️⃣ Empresarial\n4️⃣ Não sei"
PS_REAJ_Q2 = "👉 De quanto foi aproximadamente o aumento?\n\n1️⃣ Até 20%\n2️⃣ 20% a 50%\n3️⃣ Mais de 50%\n4️⃣ Não sei"
PS_REAJ_Q3 = "É muito frustrante ver o valor subir tanto, especialmente quando você sempre honrou com os pagamentos para garantir a sua segurança e a da sua família. 💙\n\n👉 Hoje, esse novo valor do boleto compromete a sua renda ou faz você considerar cancelar o plano?"
PS_REAJ_Q4 = "👉 Você (ou o titular) tem mais de 59 anos?\n\n1️⃣ Sim\n2️⃣ Não"
PS_REAJ_Q5 = "👉 O aumento ocorreu após mudança de idade?\n\n1️⃣ Sim\n2️⃣ Não"
PS_REAJ_Q6 = "👉 Você recebeu algum documento detalhando o aumento?\n\n1️⃣ Sim\n2️⃣ Não"
PS_REAJ_Q7 = "👉 Esse plano foi feito por:\n\n1️⃣ Empresa\n2️⃣ Associação/sindicato\n3️⃣ Contratei sozinho"
PS_REAJ_Q8 = "👉 Você possui o contrato do plano?\n\n1️⃣ Sim\n2️⃣ Não"

# ============================================
# 8. FLUXO COPARTICIPAÇÃO
# ============================================
PS_COPA_Q1 = "Recebi seu contato e já te adianto: a coparticipação não pode ser uma surpresa desagradável no seu boleto. Ela deve ser clara e, acima de tudo, dentro dos limites da lei. Ninguém deve ter medo de usar o plano por causa do valor das taxas. 💙\n\n👉 Você deixou de fazer exames ou tratamentos por causa da coparticipação?\n\n1️⃣ Sim\n2️⃣ Não"
PS_COPA_Q2 = "É muito desgastante você pagar o plano em dia e, quando mais precisa dele, ser surpreendido com taxas que parecem uma segunda mensalidade.\n\n👉 Você sente que hoje está 'pagando para usar' o que já deveria estar coberto?"
PS_COPA_Q3 = "👉 A coparticipação foi cobrada em:\n\n1️⃣ Consultas\n2️⃣ Exames\n3️⃣ Terapias\n4️⃣ Internação\n5️⃣ Outro"
PS_COPA_Q4 = "👉 Você faz tratamento contínuo?\n\n1️⃣ Sim\n2️⃣ Não"
PS_COPA_Q5 = "👉 Qual tipo de tratamento você faz?"
PS_COPA_Q6 = "Importante você saber: a coparticipação não pode ser ilimitada. A justiça entende que cobrar percentuais muito altos ou taxas sobre internação pode ser considerado abusivo, pois impede o paciente de se tratar."
PS_COPA_Q7 = "👉 Você possui o contrato do plano?\n\n1️⃣ Sim\n2️⃣ Não"

# ============================================
# 9. FLUXO ERRO MÉDICO
# ============================================
PS_ERRO_Q1 = "Sinto muito que você esteja passando por isso. Sei que, além da dor física, existe uma quebra de confiança muito grande quando algo não sai como o esperado em um procedimento médico. Estou aqui para te ouvir e entender se houve uma falha que te dá direito à reparação. 💙\n\n👉 O que aconteceu durante o atendimento médico?\n\n1️⃣ Cirurgia\n2️⃣ Atendimento de emergência\n3️⃣ Tratamento contínuo\n4️⃣ Parto\n5️⃣ Outro"
PS_ERRO_Q2 = "👉 O paciente sofreu algum dano?\n\n1️⃣ Agravamento da saúde\n2️⃣ Sequela\n3️⃣ Dor intensa\n4️⃣ Novo procedimento necessário\n5️⃣ Óbito"
PS_ERRO_Q3 = "Eu imagino o quanto esse momento está sendo difícil para você e para sua família. Para que eu possa desenhar a melhor estratégia:\n\n👉 Como esse episódio mudou a sua vida hoje?"
PS_ERRO_Q4 = "👉 Você possui prontuário médico?\n\n1️⃣ Sim\n2️⃣ Não"
PS_ERRO_Q5 = "👉 Outro médico já disse que houve erro ou falha no atendimento?\n\n1️⃣ Sim\n2️⃣ Não"
PS_ERRO_Q6 = "👉 Você sente que houve falta de informação, descaso ou uma falha clara na técnica do médico ou do hospital?"

# ============================================
# 10. FLUXO OUTRO
# ============================================
PS_OUTRO_DEMANDA_Q1 = "Entendido! O Direito da Saúde é muito amplo e, se o seu problema envolve o seu bem-estar ou o seu contrato de saúde, você está no lugar certo. 💙\n\nPara que eu possa entender como te ajudar, me conte brevemente o que está acontecendo. O plano de saúde negou algo?"
PS_OUTRO_DEMANDA_Q2 = "👉 Existe algum prazo ou data limite que te preocupa agora (ex: uma cirurgia marcada, um boleto vencendo ou um prazo de defesa)?"
PS_OUTRO_DEMANDA_Q3 = "👉 Você recebeu alguma negativa ou teve dificuldade no atendimento?\n\n1️⃣ Sim\n2️⃣ Não\n3️⃣ Não se encaixa"
PS_OUTRO_DEMANDA_Q4 = "👉 Você tem isso registrado (mensagem, documento, protocolo)?\n\n1️⃣ Sim\n2️⃣ Não\n3️⃣ Não se encaixa"
PS_OUTRO_DEMANDA_Q5 = "👉 Você possui documentos relacionados ao caso?\n\n1️⃣ Sim\n2️⃣ Não"
PS_OUTRO_DEMANDA_Q6 = "👉 Esse problema está afetando sua saúde atualmente?\n\n1️⃣ Sim\n2️⃣ Não"
PS_OUTRO_DEMANDA_Q7 = "Certo, recebi seus detalhes. Independentemente do caso, a minha premissa é sempre a mesma: o contrato de saúde deve servir para proteger a vida e o consumidor, não para criar barreiras."

# ============================================
# CAMINHO NÃO (menos de 2 anos)
# ============================================
PS_NAO_2ANOS_EDUCACAO = (
    "Entendo! Muitas pessoas acreditam que precisam esperar 2 anos para ter direito a cirurgias ou tratamentos complexos, "
    "mas a lei nem sempre funciona assim. Existem situações onde o plano é obrigado a cobrir o seu procedimento mesmo que você "
    "tenha poucos meses de contrato, especialmente se houver urgência ou se a doença não foi declarada por má-fé."
)
PS_NAO_2ANOS_Q1 = "👉 Me conta, qual o tratamento que você precisa fazer?"
PS_NAO_2ANOS_Q2 = "👉 No seu caso, o médico comentou se isso é urgente ou pode trazer algum risco se não for feito?"
PS_NAO_2ANOS_FEEDBACK = "Perfeito, isso é importante! 👊 SE HÁ URGÊNCIA, o plano já deveria cobrir normalmente esse tipo de situação. Mesmo assim, eles podem acabar negando indevidamente em alguns casos."
PS_NAO_2ANOS_Q3 = "👉 O médico indicou que o tratamento é urgente?\n\n1️⃣ Sim\n2️⃣ Não"
PS_NAO_2ANOS_Q4 = "👉 Você já sabia dessa doença antes de contratar o plano?\n\n1️⃣ Sim\n2️⃣ Não\n3️⃣ Descobri depois"
PS_NAO_2ANOS_Q5 = "👉 O plano negou alegando carência?\n\n1️⃣ Sim\n2️⃣ Não"
PS_NAO_2ANOS_Q6 = "👉 Você tem a negativa por escrito?\n\n1️⃣ Sim\n2️⃣ Não"

# ============================================
# MENSAGENS DE VALORES (INTERCEPTAÇÃO)
# ============================================
MSG_VALORES_CIRURGIA = (
    "Compreendo sua dúvida sobre o investimento. No meu escritório, nós não trabalhamos com valores iguais porque cada vida e cada urgência são únicas.\n\n"
    "Como o seu caso envolve [Cirurgia / Medicamento de Alto Custo / Home Care], estamos tratando de um cenário de alta complexidade técnica e risco direto à saúde. "
    f"A {L} não define valores para casos de alta complexidade por mensagem de texto.\n\n"
    "Para situações assim, é necessária uma Reunião Estratégica por vídeo (15 minutos). Nessa reunião, ela vai te apresentar o plano de ação para cercar o juiz e garantir que seu direito não seja negado, além de alinhar o investimento necessário para a condução do processo."
)

MSG_VALORES_CONSULTA = (
    "Compreendo sua dúvida sobre o investimento. No meu escritório, nós não trabalhamos com valores iguais porque cada caso exige um empenho técnico diferente.\n\n"
    "Como o seu caso envolve a liberação de [Consulta / Exame Específico], a Dra. Lethicia faz questão de analisar pessoalmente a documentação na mesa de trabalho antes de passar qualquer orçamento.\n\n"
    "Valores para esse tipo de demanda são informados somente após essa triagem técnica, garantindo que o valor seja justo e condizente com a complexidade do seu pedido. Assim que ela analisar seus documentos, você receberá o retorno."
)

MSG_VALORES_REAJUSTE = (
    "Compreendo sua dúvida sobre o investimento. No meu escritório, tratamos cada contrato de forma individualizada, pois os valores de reajuste e as cláusulas variam drasticamente entre as operadoras.\n\n"
    "Como o seu caso envolve [Reajuste Abusivo / Coparticipação], estamos tratando de uma análise financeira e contratual detalhada. "
    f"A {L} não define valores para questões contratuais por mensagem de texto.\n\n"
    "É necessário uma Reunião Estratégica (vídeo ou áudio) para que ela te explique como buscaremos o reequilíbrio do seu plano e a restituição de valores pagos indevidamente, alinhando o investimento da consultoria nessa etapa."
)

# ============================================
# MENSAGEM FINAL (PÓS NEGATIVA/PÓS PERGUNTAS)
# ============================================
PS_POS_BUSCA = (
    "Obrigado por todas as informações. Já consigo ter um bom entendimento da sua situação.\n\n"
    "Agora me diz: o que você está buscando nesse momento? Escolha a opção que mais se encaixa com onde você está agora:\n\n"
    "1️⃣ Quero entender se o plano de saúde é obrigado a cobrir determinado tratamento ou Tenho uma dúvida específica ou um caso diferente e gostaria de orientação jurídica para entender quais são meus direitos e possibilidades.\n\n"
    "2️⃣ Já tenho a negativa do plano: Desejo orientação especializada para ingressar com a ação judicial e buscar a liberação do meu tratamento.\n\n"
    "3️⃣ Ainda não tenho a negativa, mas preciso me preparar: Quero me antecipar, eu ainda não recebi a negativa do plano, mas sei que meu pedido pode ser recusado. Quero me preparar da forma correta, com orientação jurídica, para aumentar minhas chances de aprovação do tratamento ou sucesso na ação judicial.\n\n"
    "4️⃣ Preciso de uma consultoria jurídica: Desejo uma análise técnica sobre o meu caso de saúde. Indicado para dúvidas sobre reajustes abusivos (anual ou por faixa etária), períodos de carência, migração de plano (portabilidade) ou para saber se um tratamento específico tem cobertura obrigatória pela ANS."
)

# Opção 1
PS_OP1_PERGUNTA = "Perfeito! Para esse tipo de dúvida pontual, oferecemos o Atendimento Particular. Diferente da consultoria completa, aqui você tira todas as suas dúvidas, tem um direcionamento claro do seu caso e um especialista te responde de forma técnica e direta, analisando se o seu direito é garantido por lei. Isso te ajudaria?"
PS_OP1_DETALHES = (
    "O investimento no atendimento particular é de R$ 97,00 e é feito online.\n\n"
    "É um atendimento individual e aprofundado onde você terá os seguintes benefícios:\n"
    "• Resposta Técnica Direta: Esclarecimento sobre a obrigatoriedade de cobertura (Rol da ANS e entendimentos judiciais recentes).\n"
    "• Análise de Viabilidade: Uma opinião profissional sobre se o seu caso tem chances reais de sucesso na justiça ou se é uma questão administrativa.\n"
    "• Indicação de Documentos: Lista do que você precisa providenciar imediatamente para não perder seus direitos.\n\n"
    "Podemos marcar um horário pra você na agenda da Dra Lethicia?"
)
PS_OP1_PAGAMENTO = "Perfeito! Vamos reservar o seu horário.\n\nComo deseja realizar o investimento do atendimento? Você prefere Pix ou Cartão de Crédito?"
PS_OP1_CONFIRMACAO = "Ao realizar o pagamento e for dado baixa no nosso financeiro, alguém da nossa equipe vai entrar em contato o quanto antes pra marcar seu atendimento na agenda da Dra Lethicia."

# Opção 2
PS_OP2_PERGUNTA = (
    "Nesse caso só é possível revertermos a negativa do plano com medidas judiciais. "
    "Você está no momento exato de agirmos para buscar o seu direito judicialmente. "
    "Agora não é mais hora de esperar, é hora de exigir que o plano de saúde cumpra a lei.\n\n"
    "O próximo passo agora é uma reunião rápida para eu te explicar como funciona o processo e valores de honorários.\n\n"
    "Antes de agendarmos: além de você, tem mais alguém que participe das decisões familiares ou financeiras, "
    "como seu esposo/esposa, que seria importante estar presente para já tirarmos todas as dúvidas de uma vez?"
)

# Opção 3
PS_OP3_PERGUNTA = (
    "Você está no caminho certo, buscar uma orientação antes de pedir ao plano! "
    "Esperar a negativa do plano para só depois agir é o erro que faz muita gente perder meses de tratamento.\n\n"
    "Com o acompanhamento jurídico, você tem as orientações corretas sobre quais médicos deve ir e como que deve ser feitos os laudos, "
    "o que você deve fazer na perícia do plano de saúde (se for solicitado no seu caso), isso tudo sendo organizado agora, "
    "após a negativa do plano, você já vai ter todos os laudos e documentos corretos pra um processo judicial, "
    "assim não precisa corrigir ou ficar correndo atrás de laudos depois. Entende?"
)
PS_OP3_PERMISSAO = (
    "Você prefere tentar sozinho com o plano ou quer o acompanhamento da Dra. para garantir que o seu pedido seja feito à prova de negativas "
    "(principalmente ao entrarmos na justiça)?"
)

# Opção 4
PS_OP4_PERGUNTA = (
    "Entendido. Para casos de análise contratual, reajustes ou dúvidas preventivas, realizamos uma Consultoria Jurídica Especializada.\n\n"
    "Nesta reunião online um advogado especialista em Direito da Saúde analisará detalhadamente o seu caso, documentos e contratos "
    "para te entregar um parecer seguro sobre os seus direitos.\n\n"
    "Informações sobre a Consultoria:\n"
    "• Investimento: R$ 500,00 (referente à análise técnica e reserva de horário).\n"
    "• Duração: Até 1 hora.\n"
    "• Objetivo: Diagnóstico completo e estratégia jurídica personalizada.\n\n"
    "Deseja prosseguir com o agendamento?"
)
PS_OP4_PAGAMENTO = "Perfeito! Vamos reservar o seu horário.\n\nComo deseja realizar o investimento do atendimento? Você prefere Pix ou Cartão de Crédito?"
PS_OP4_CONFIRMACAO = "Ao realizar o pagamento e for dado baixa no nosso financeiro, alguém da nossa equipe vai entrar em contato o quanto antes pra marcar seu atendimento na agenda da Dra Lethicia."

# Encerramento
PS_ENCERRAMENTO = (
    "Entendo perfeitamente e respeito sua decisão.\n\n"
    "Vou encerrar o seu atendimento por aqui para priorizar os casos que já estão com liminares em andamento. "
    "Lembre-se apenas que, no Direito da Saúde, o tempo é um fator determinante para o sucesso do tratamento.\n\n"
    "Caso precise de suporte especializado no futuro, nossos canais continuam à disposição."
)

# Decisão Compartilhada
DECISAO_SIM = (
    "Excelente! É fundamental que ele(a) participe, pois como o Direito à Saúde envolve "
    "prazos muito curtos e decisões imediatas sobre o tratamento, é bom que todos "
    "estejam na mesma página.\n\n"
    "Vamos escolher um horário que fique confortável para vocês dois... "
    f"Logo abaixo vou te mandar a agenda da {L}, e você marque o dia e horário "
    "que fica melhor pra ambos.\n\n"
    f"🔗 {CALENDLY_LINK}"
)

DECISAO_NAO = (
    "Perfeito, facilita bastante o nosso fluxo. Como você é a única responsável pela decisão, "
    "conseguimos dar um andamento mais ágil aos trabalhos... "
    f"Logo abaixo vou te mandar a agenda da {L}, e você marque o dia e horário "
    "que fica melhor pra você.\n\n"
    f"🔗 {CALENDLY_LINK}"
)

DECISAO_REPASSE = (
    "Entendo! Olha, eu sugiro fortemente que ele tente participar, nem que seja apenas "
    "nos primeiros 10 minutos. No Direito à Saúde, os detalhes técnicos sobre a negativa da operadora "
    "costumam gerar muitas dúvidas e, se ele ouvir direto de mim, vocês ganham muito mais segurança para decidir rápido.\n\n"
    "Conseguimos um horário em que ele possa entrar na chamada, ou prefere manter só entre nós por enquanto?"
)

DECISAO_REPASSE_SIM = f"Perfeito! Vamos agendar para vocês dois. Logo abaixo vou te mandar a agenda da {L}.\n\n🔗 {CALENDLY_LINK}"
DECISAO_REPASSE_NAO = f"Entendido! Mantemos só entre nós. Logo abaixo vou te mandar a agenda da {L}.\n\n🔗 {CALENDLY_LINK}"


# ============================================
# PROCESSAMENTO DO FLUXO
# ============================================

def processar(resposta: str):
    estado = st.session_state.estado
    dados = st.session_state.dados

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

    # ========== SUS_DEMANDA ==========
    elif estado == "SUS_DEMANDA":
        if "cirurgia" in _n(resposta):
            dados["tipo"] = "cirurgia"
            st.session_state.estado = "SUS_ESPECIALIDADE"
            add_bot(MSG_SUS_ESPECIALIDADE)
        else:
            dados["tipo"] = "consulta_exame"
            st.session_state.estado = "FIM"
            add_bot("Atendimento finalizado. Obrigado!")

    # ========== SUS_ESPECIALIDADE ==========
    elif estado == "SUS_ESPECIALIDADE":
        if "oncologia" in _n(resposta) or "1" in resposta:
            st.session_state.perguntas_ativas = PERGUNTAS_ONCOLOGIA.copy()
        elif "neurodivergências" in _n(resposta) or "tea" in _n(resposta) or "tdah" in _n(resposta) or "2" in resposta:
            st.session_state.perguntas_ativas = PERGUNTAS_NEURO.copy()
        elif "endometriose" in _n(resposta) or "adenomiose" in _n(resposta) or "3" in resposta:
            st.session_state.perguntas_ativas = PERGUNTAS_ENDOMETRIOSE.copy()
        elif "medicamento" in _n(resposta) or "4" in resposta:
            st.session_state.perguntas_ativas = PERGUNTAS_MEDICAMENTO.copy()
        elif "bariátrica" in _n(resposta) or "5" in resposta:
            st.session_state.perguntas_ativas = PERGUNTAS_BARIATRICA.copy()
        elif "neurologia" in _n(resposta) or "neurocirurgia" in _n(resposta) or "6" in resposta:
            st.session_state.perguntas_ativas = PERGUNTAS_NEUROLOGIA.copy()
        elif "cardiologia" in _n(resposta) or "7" in resposta:
            st.session_state.perguntas_ativas = PERGUNTAS_CARDIOLOGIA.copy()
        else:
            st.session_state.perguntas_ativas = PERGUNTAS_OUTROS.copy()
        
        dados["especialidade"] = resposta
        st.session_state.pergunta_idx = 0
        st.session_state.respostas_nao = 0
        st.session_state.estado = "SUS_PERGUNTAS"
        add_bot(st.session_state.perguntas_ativas[0])

    # ========== SUS_PERGUNTAS ==========
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

    # ========== POS_PERGUNTAS ==========
    elif estado == "POS_PERGUNTAS":
        dados["sentimento"] = resposta
        add_bot(MSG_EXPLICACAO)
        st.session_state.estado = "PROPOSTA"

    # ========== PROPOSTA ==========
    elif estado == "PROPOSTA":
        if _sim(resposta):
            add_bot(MSG_HONORARIOS)
            st.session_state.estado = "HONORARIOS"
        else:
            add_bot(MSG_ENCERRAMENTO_SUS)
            st.session_state.estado = "FIM"

    # ========== HONORARIOS ==========
    elif estado == "HONORARIOS":
        if _sim(resposta):
            add_bot(MSG_SIM_HONORARIOS)
            st.session_state.estado = "FIM"
        else:
            add_bot(MSG_ENCERRAMENTO_SUS)
            st.session_state.estado = "FIM"

    # ========================================
    # PLANO DE SAÚDE - FLUXO COMPLETO
    # ========================================

    # ========== PS_TEMPO ==========
    elif estado == "PS_TEMPO":
        if "sim" in _n(resposta):
            dados["plano_2anos"] = "sim"
            st.session_state.estado = "PS_SITUACAO"
            add_bot(PS_SITUACAO)
        else:
            dados["plano_2anos"] = "nao"
            st.session_state.estado = "PS_NAO_2ANOS_EDUCACAO"
            add_bot(PS_NAO_2ANOS_EDUCACAO)

    # ========== PS_NAO_2ANOS - Coleta de dados ==========
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
        st.session_state.estado = "PS_POS_BUSCA"
        add_bot(PS_POS_BUSCA)

    # ========== PS_SITUACAO (Caminho SIM) ==========
    elif estado == "PS_SITUACAO":
        dados["situacao"] = resposta
        
        if "reparadora" in _n(resposta) or "1" in resposta:
            st.session_state.estado = "PS_REP_Q1"
            add_bot(PS_REP_Q1)
        elif "negativa de cirurgia" in _n(resposta) or "2" in resposta:
            st.session_state.estado = "PS_NEG_CIR_ESP"
            add_bot(PS_NEG_CIR_ESP)
        elif "medicamento" in _n(resposta) or "3" in resposta:
            st.session_state.perguntas_ativas = [
                PS_MED_Q1, PS_MED_Q2, PS_MED_Q3, PS_MED_Q4, PS_MED_Q5,
                PS_MED_Q6, PS_MED_Q7, PS_MED_Q8, PS_MED_Q9, PS_MED_Q10
            ]
            st.session_state.pergunta_idx = 0
            st.session_state.estado = "PS_PERGUNTAS_COLETOR"
            add_bot(PS_MED_Q1)
        elif "exame" in _n(resposta) or "4" in resposta:
            st.session_state.perguntas_ativas = [
                PS_EXAME_Q1, PS_EXAME_Q2, PS_EXAME_Q3, PS_EXAME_Q4, PS_EXAME_Q5, PS_EXAME_Q6, PS_EXAME_Q7
            ]
            st.session_state.pergunta_idx = 0
            st.session_state.estado = "PS_PERGUNTAS_COLETOR"
            add_bot(PS_EXAME_Q1)
        elif "home" in _n(resposta) or "5" in resposta:
            st.session_state.perguntas_ativas = [
                PS_HOME_Q1, PS_HOME_Q2, PS_HOME_Q3, PS_HOME_Q4, PS_HOME_Q5, PS_HOME_Q6, PS_HOME_Q7
            ]
            st.session_state.pergunta_idx = 0
            st.session_state.estado = "PS_PERGUNTAS_COLETOR"
            add_bot(PS_HOME_Q1)
        elif "terapia" in _n(resposta) or "6" in resposta:
            st.session_state.perguntas_ativas = [
                PS_TERA_Q1, PS_TERA_Q2, PS_TERA_Q3, PS_TERA_Q4, PS_TERA_Q5, PS_TERA_Q6, PS_TERA_Q7
            ]
            st.session_state.pergunta_idx = 0
            st.session_state.estado = "PS_PERGUNTAS_COLETOR"
            add_bot(PS_TERA_Q1)
        elif "reajuste" in _n(resposta) or "7" in resposta:
            st.session_state.perguntas_ativas = [
                PS_REAJ_Q1, PS_REAJ_Q2, PS_REAJ_Q3, PS_REAJ_Q4, PS_REAJ_Q5, PS_REAJ_Q6, PS_REAJ_Q7, PS_REAJ_Q8
            ]
            st.session_state.pergunta_idx = 0
            st.session_state.estado = "PS_PERGUNTAS_COLETOR"
            add_bot(PS_REAJ_Q1)
        elif "coparticipação" in _n(resposta) or "8" in resposta:
            st.session_state.perguntas_ativas = [
                PS_COPA_Q1, PS_COPA_Q2, PS_COPA_Q3, PS_COPA_Q4, PS_COPA_Q5, PS_COPA_Q6, PS_COPA_Q7
            ]
            st.session_state.pergunta_idx = 0
            st.session_state.estado = "PS_PERGUNTAS_COLETOR"
            add_bot(PS_COPA_Q1)
        elif "erro" in _n(resposta) or "9" in resposta:
            st.session_state.perguntas_ativas = [
                PS_ERRO_Q1, PS_ERRO_Q2, PS_ERRO_Q3, PS_ERRO_Q4, PS_ERRO_Q5, PS_ERRO_Q6
            ]
            st.session_state.pergunta_idx = 0
            st.session_state.estado = "PS_PERGUNTAS_COLETOR"
            add_bot(PS_ERRO_Q1)
        else:  # OUTRO
            st.session_state.perguntas_ativas = [
                PS_OUTRO_DEMANDA_Q1, PS_OUTRO_DEMANDA_Q2, PS_OUTRO_DEMANDA_Q3,
                PS_OUTRO_DEMANDA_Q4, PS_OUTRO_DEMANDA_Q5, PS_OUTRO_DEMANDA_Q6, PS_OUTRO_DEMANDA_Q7
            ]
            st.session_state.pergunta_idx = 0
            st.session_state.estado = "PS_PERGUNTAS_COLETOR"
            add_bot(PS_OUTRO_DEMANDA_Q1)

    # ========== PS_PERGUNTAS_COLETOR (para todas as situações com lista) ==========
    elif estado == "PS_PERGUNTAS_COLETOR":
        idx = st.session_state.pergunta_idx
        perguntas = st.session_state.perguntas_ativas
        
        dados[f"resp_{idx}"] = resposta
        idx += 1
        st.session_state.pergunta_idx = idx
        
        if idx < len(perguntas):
            add_bot(perguntas[idx])
        else:
            st.session_state.estado = "PS_POS_BUSCA"
            add_bot(PS_POS_BUSCA)

    # ========== PS_REP_Q1 (Reparadora) ==========
    elif estado == "PS_REP_Q1":
        dados["rep_q1"] = resposta
        st.session_state.estado = "PS_REP_Q2"
        add_bot(PS_REP_Q2)
    elif estado == "PS_REP_Q2":
        if "ainda não" in _n(resposta) or "2" in resposta:
            st.session_state.estado = "PS_REP_NAO_PESO"
            add_bot(PS_REP_NAO_PESO)
        else:
            st.session_state.estado = "PS_REP_EMPATIA"
            add_bot(PS_REP_EMPATIA)
    elif estado == "PS_REP_NAO_PESO":
        if _sim(resposta):
            add_bot(f"Ótimo! Agende sua consulta: {CALENDLY_LINK}")
        else:
            add_bot(PS_ENCERRAMENTO)
        st.session_state.estado = "FIM"
    elif estado == "PS_REP_EMPATIA":
        st.session_state.estado = "PS_REP_Q3"
        add_bot(PS_REP_Q3)
    elif estado == "PS_REP_Q3":
        dados["rep_q3"] = resposta
        st.session_state.estado = "PS_REP_Q4"
        add_bot(PS_REP_Q4)
    elif estado == "PS_REP_Q4":
        dados["rep_q4"] = resposta
        st.session_state.estado = "PS_REP_Q5"
        add_bot(PS_REP_Q5)
    elif estado == "PS_REP_Q5":
        dados["rep_q5"] = resposta
        st.session_state.estado = "PS_REP_ACOMPANHAMENTO"
        add_bot(PS_REP_ACOMPANHAMENTO)
    elif estado == "PS_REP_ACOMPANHAMENTO":
        if "acompanhamento" in _n(resposta) or "quer" in _n(resposta):
            st.session_state.estado = "PS_POS_BUSCA"
            add_bot(PS_POS_BUSCA)
        else:
            add_bot(PS_ENCERRAMENTO)
            st.session_state.estado = "FIM"

    # ========== PS_NEG_CIR_ESP (Negativa de cirurgia) ==========
    elif estado == "PS_NEG_CIR_ESP":
        dados["neg_cir_esp"] = resposta
        
        if "endometriose" in _n(resposta) or "1" in resposta:
            st.session_state.perguntas_ativas = [PS_ENDO_Q1, PS_ENDO_Q2, PS_ENDO_Q3, PS_ENDO_Q4, PS_ENDO_Q5]
        elif "bariátrica" in _n(resposta) or "2" in resposta:
            st.session_state.perguntas_ativas = [PS_BARI_Q1, PS_BARI_Q2, PS_BARI_Q3, PS_BARI_Q4, PS_BARI_Q5, PS_BARI_Q6]
        elif "oncologia" in _n(resposta) or "3" in resposta:
            st.session_state.perguntas_ativas = [PS_ONCO_Q1, PS_ONCO_Q2, PS_ONCO_Q3, PS_ONCO_Q4, PS_ONCO_Q5, PS_ONCO_Q6]
        elif "cardiologia" in _n(resposta) or "4" in resposta:
            st.session_state.perguntas_ativas = [PS_CARDIO_Q1, PS_CARDIO_Q2, PS_CARDIO_Q3, PS_CARDIO_Q4, PS_CARDIO_Q5, PS_CARDIO_Q6]
        elif "neurocirurgia" in _n(resposta) or "5" in resposta:
            st.session_state.perguntas_ativas = [PS_NEURO_Q1, PS_NEURO_Q2, PS_NEURO_Q3, PS_NEURO_Q4, PS_NEURO_Q5, PS_NEURO_Q6, PS_NEURO_Q7]
        elif "ortopedia" in _n(resposta) or "6" in resposta:
            st.session_state.perguntas_ativas = [PS_ORTO_Q1, PS_ORTO_Q2, PS_ORTO_Q3, PS_ORTO_APOIO, PS_ORTO_Q4, PS_ORTO_Q5, PS_ORTO_Q6]
        elif "oftalmologia" in _n(resposta) or "7" in resposta:
            st.session_state.perguntas_ativas = [PS_OFTAL_Q1, PS_OFTAL_Q2, PS_OFTAL_Q3, PS_OFTAL_Q4, PS_OFTAL_Q5, PS_OFTAL_APOIO]
        else:  # OUTRO
            st.session_state.perguntas_ativas = [
                PS_OUTRO_INTRO, PS_OUTRO_Q1, PS_OUTRO_Q2, PS_OUTRO_Q3, PS_OUTRO_Q4,
                PS_OUTRO_APOIO, PS_OUTRO_Q5, PS_OUTRO_Q6, PS_OUTRO_Q7, PS_OUTRO_Q8, PS_OUTRO_Q9
            ]
        
        st.session_state.pergunta_idx = 0
        st.session_state.estado = "PS_PERGUNTAS_COLETOR"
        add_bot(st.session_state.perguntas_ativas[0])

    # ========== PS_POS_BUSCA (pós perguntas) ==========
    elif estado == "PS_POS_BUSCA":
        if "1" in resposta:
            st.session_state.estado = "PS_OP1_PERGUNTA"
            add_bot(PS_OP1_PERGUNTA)
        elif "2" in resposta:
            st.session_state.estado = "PS_OP2_PERGUNTA"
            add_bot(PS_OP2_PERGUNTA)
        elif "3" in resposta:
            st.session_state.estado = "PS_OP3_PERGUNTA"
            add_bot(PS_OP3_PERGUNTA)
        elif "4" in resposta:
            st.session_state.estado = "PS_OP4_PERGUNTA"
            add_bot(PS_OP4_PERGUNTA)
        else:
            add_bot(PS_POS_BUSCA)

    # ========== OPÇÃO 1 ==========
    elif estado == "PS_OP1_PERGUNTA":
        if _sim(resposta):
            st.session_state.estado = "PS_OP1_DETALHES"
            add_bot(PS_OP1_DETALHES)
        else:
            st.session_state.estado = "FIM"
            add_bot(PS_ENCERRAMENTO)
    elif estado == "PS_OP1_DETALHES":
        if _sim(resposta):
            st.session_state.estado = "PS_OP1_PAGAMENTO"
            add_bot(PS_OP1_PAGAMENTO)
        else:
            st.session_state.estado = "FIM"
            add_bot(PS_ENCERRAMENTO)
    elif estado == "PS_OP1_PAGAMENTO":
        if "cartão" in _n(resposta):
            add_bot(f"✅ Aqui está o link para pagamento via **Cartão de Crédito**:\n\n{LINK_CARTAO_97}\n\n{PS_OP1_CONFIRMACAO}")
            st.session_state.estado = "FIM"
        elif "pix" in _n(resposta):
            add_bot(f"✅ Aqui está o link para pagamento via **Pix**:\n\n{LINK_PIX_97}\n\n{PS_OP1_CONFIRMACAO}")
            st.session_state.estado = "FIM"

    # ========== OPÇÃO 2 ==========
    elif estado == "PS_OP2_PERGUNTA":
        st.session_state.estado = "DECISAO_COMPARTILHADA"

    # ========== OPÇÃO 3 ==========
    elif estado == "PS_OP3_PERGUNTA":
        st.session_state.estado = "PS_OP3_PERMISSAO"
        add_bot(PS_OP3_PERMISSAO)
    elif estado == "PS_OP3_PERMISSAO":
        if "acompanhamento" in _n(resposta) or "quer" in _n(resposta):
            st.session_state.estado = "DECISAO_COMPARTILHADA"
            add_bot("Perfeito. O próximo passo agora é uma reunião rápida para a Dra Lethicia te explicar como funciona o processo e valores de honorários.\n\nAntes de agendarmos: além de você, tem mais alguém que participe das decisões familiares ou financeiras, como seu esposo/esposa, que seria importante estar presente para já tirarmos todas as dúvidas de uma vez?")
        else:
            st.session_state.estado = "FIM"
            add_bot(PS_ENCERRAMENTO)

    # ========== OPÇÃO 4 ==========
    elif estado == "PS_OP4_PERGUNTA":
        if _sim(resposta):
            st.session_state.estado = "PS_OP4_PAGAMENTO"
            add_bot(PS_OP4_PAGAMENTO)
        else:
            st.session_state.estado = "FIM"
            add_bot(PS_ENCERRAMENTO)
    elif estado == "PS_OP4_PAGAMENTO":
        if "cartão" in _n(resposta):
            add_bot(f"✅ Aqui está o link para pagamento via **Cartão de Crédito**:\n\n{LINK_CARTAO_500}\n\n{PS_OP4_CONFIRMACAO}")
            st.session_state.estado = "FIM"
        elif "pix" in _n(resposta):
            add_bot(f"✅ Aqui está o link para pagamento via **Pix**:\n\n{LINK_PIX_500}\n\n{PS_OP4_CONFIRMACAO}")
            st.session_state.estado = "FIM"

    # ========== DECISAO_COMPARTILHADA ==========
    elif estado == "DECISAO_COMPARTILHADA":
        if "sim" in _n(resposta):
            add_bot(DECISAO_SIM)
            st.session_state.estado = "FIM"
        elif "não" in _n(resposta) or "sozinho" in _n(resposta):
            add_bot(DECISAO_NAO)
            st.session_state.estado = "FIM"
        else:
            add_bot(DECISAO_REPASSE)
            st.session_state.estado = "DECISAO_REPASSE_RESPOSTA"

    # ========== DECISAO_REPASSE_RESPOSTA ==========
    elif estado == "DECISAO_REPASSE_RESPOSTA":
        if _sim(resposta):
            add_bot(DECISAO_REPASSE_SIM)
        else:
            add_bot(DECISAO_REPASSE_NAO)
        st.session_state.estado = "FIM"

    # ========== FIM ==========
    elif estado == "FIM":
        pass


# ============================================
# INTERFACE STREAMLIT
# ============================================

def main():
    st.title("⚖️ Iara Bot - Assistente Jurídica em Direito da Saúde")
    st.caption(f"Especialista: {L} | Atendimento: SUS, Planos de Saúde")

    init_session()

    # Sidebar
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

    # Chat Container
    col1, col2 = st.columns([3, 1])

    with col1:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for msg in st.session_state.messages:
            if msg["role"] == "bot":
                st.markdown(
                    f'<div class="chat-message bot-message"><strong>🤖 Lara:</strong><br>{msg["content"]}</div>',
                    unsafe_allow_html=True
                )
            else:
                nome = st.session_state.nome or "Você"
                st.markdown(
                    f'<div class="chat-message user-message"><strong>👤 {nome}:</strong><br>{msg["content"]}</div>',
                    unsafe_allow_html=True
                )
        st.markdown('</div>', unsafe_allow_html=True)

        # Interceptar perguntas sobre valores
        user_input = st.text_input("Digite sua mensagem:", key="user_input", placeholder="Digite aqui sua resposta...")
        
        if user_input:
            palavras_valor = ["valor", "quanto", "preço", "custa", "honorário", "investimento", "cobram"]
            if any(p in _n(user_input) for p in palavras_valor):
                tipo_demanda = st.session_state.dados.get("situacao", "")
                if "reajuste" in _n(tipo_demanda) or "coparticipação" in _n(tipo_demanda):
                    add_bot(MSG_VALORES_REAJUSTE)
                elif "exame" in _n(tipo_demanda) or "consulta" in _n(tipo_demanda):
                    add_bot(MSG_VALORES_CONSULTA)
                else:
                    add_bot(MSG_VALORES_CIRURGIA)
                st.rerun()
        
        # Botão enviar
        if st.button("📤 Enviar", use_container_width=True) and user_input:
            add_user(user_input)
            processar(user_input)
            st.rerun()

    # Botões contextuais na coluna direita
    with col2:
        estado = st.session_state.estado
        
        if estado == "CANAL":
            if st.button("🏥 SUS", use_container_width=True):
                add_user("SUS")
                processar("SUS")
                st.rerun()
            if st.button("📋 Plano de Saúde", use_container_width=True):
                add_user("Plano de Saúde")
                processar("Plano de Saúde")
                st.rerun()
        
        elif estado == "SUS_DEMANDA":
            if st.button("🔪 Cirurgia / Tratamento", use_container_width=True):
                add_user("Cirurgia")
                processar("Cirurgia")
                st.rerun()
            if st.button("📋 Consultas / Exames", use_container_width=True):
                add_user("Consultas")
                processar("Consultas")
                st.rerun()
        
        elif estado == "SUS_ESPECIALIDADE":
            esp_opts = ["Oncologia", "Neurodivergências", "Endometriose", "Medicamento", "Bariátrica", "Neurologia", "Cardiologia", "Outros"]
            for esp in esp_opts:
                if st.button(esp, use_container_width=True):
                    add_user(esp)
                    processar(esp)
                    st.rerun()
        
        elif estado in ["POS_PERGUNTAS", "PROPOSTA", "HONORARIOS", "PS_OP1_PERGUNTA", "PS_OP1_DETALHES", "PS_OP4_PERGUNTA"]:
            if st.button("✅ SIM", use_container_width=True):
                add_user("SIM")
                processar("SIM")
                st.rerun()
            if st.button("❌ NÃO", use_container_width=True):
                add_user("NÃO")
                processar("NÃO")
                st.rerun()
        
        elif estado == "PS_TEMPO":
            if st.button("1️⃣ Sim", use_container_width=True):
                add_user("Sim")
                processar("Sim")
                st.rerun()
            if st.button("2️⃣ Não", use_container_width=True):
                add_user("Não")
                processar("Não")
                st.rerun()
        
        elif estado == "PS_SITUACAO":
            for i in range(1, 11):
                if st.button(f"{i}️⃣", use_container_width=True):
                    add_user(str(i))
                    processar(str(i))
                    st.rerun()
        
        elif estado in ["PS_OP1_PAGAMENTO", "PS_OP4_PAGAMENTO"]:
            if st.button("💳 Cartão de Crédito", use_container_width=True):
                add_user("Cartão de Crédito")
                processar("cartão")
                st.rerun()
            if st.button("📱 Pix", use_container_width=True):
                add_user("Pix")
                processar("pix")
                st.rerun()
        
        elif estado in ["DECISAO_COMPARTILHADA"]:
            if st.button("👨‍👩‍👧 Sim, meu cônjuge/familiar", use_container_width=True):
                add_user("Sim, meu cônjuge/familiar")
                processar("sim")
                st.rerun()
            if st.button("👤 Não, eu decido sozinho(a)", use_container_width=True):
                add_user("Não, eu decido sozinho(a)")
                processar("não")
                st.rerun()
            if st.button("📞 Tem meu cônjuge, mas pode falar comigo", use_container_width=True):
                add_user("Tem")
                processar("repasse")
                st.rerun()
        
        elif estado == "DECISAO_REPASSE_RESPOSTA":
            if st.button("👥 Com ele(a)", use_container_width=True):
                add_user("Com ele(a)")
                processar("sim")
                st.rerun()
            if st.button("👤 Entre nós", use_container_width=True):
                add_user("Entre nós")
                processar("não")
                st.rerun()

    # Inicializar chat se vazio
    if not st.session_state.messages:
        add_bot(MSG_BOAS_VINDAS)
        st.rerun()

if __name__ == "__main__":
    main()
