"""
IARA BOT - ASSISTENTE JURÍDICA EM DIREITO DA SAÚDE
VERSÃO COMPLETA E PERFEITA - TODAS AS 10 SITUAÇÕES DE PLANO DE SAÚDE
"""

import streamlit as st

# ============================================
# CONFIGURAÇÕES GLOBAIS
# ============================================
CALENDLY_LINK = "https://calendly.com/dra-lethicia"
LAWYER_NAME = "Dra. Lethicia Fernanda"

st.set_page_config(page_title="Iara Bot - Assistente Jurídica", page_icon="⚖️", layout="wide")

st.markdown("""
<style>
    .chat-message {padding: 1rem; border-radius: 0.8rem; margin-bottom: 1rem; display: flex; flex-direction: column;}
    .bot-message {background-color: #f0f2f6; border-left: 4px solid #2c7be5; align-items: flex-start;}
    .user-message {background-color: #2c7be5; color: white; align-items: flex-end; margin-left: 20%;}
    .chat-container {max-height: 550px; overflow-y: auto; padding: 1rem; border: 1px solid #ddd; border-radius: 10px; background-color: #fafafa;}
    .stButton button {background-color: #2c7be5; color: white; border-radius: 20px;}
</style>
""", unsafe_allow_html=True)

# ============================================
# FUNÇÕES AUXILIARES
# ============================================

def normalize(text: str) -> str:
    return str(text).strip().lower()

def is_sim(text: str) -> bool:
    keywords = ["sim", "s", "yes", "quero", "ok", "claro", "vamos", "aceito", "topo", "verdade", "certo"]
    return any(k in normalize(text) for k in keywords)

def is_nao(text: str) -> bool:
    keywords = ["não", "nao", "n", "no", "nunca", "recuso", "falso"]
    return any(k in normalize(text) for k in keywords)

def detect_valor_question(text: str) -> bool:
    keywords = ["valor", "quanto custa", "quanto é", "preço", "honorários", "pagamento", "investimento", "custa", "custo"]
    return any(k in normalize(text) for k in keywords)

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
        msg = msg.replace("{lawyer}", LAWYER_NAME)
        msg = msg.replace("{CALENDLY}", CALENDLY_LINK)
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
# PLANO DE SAÚDE - QUALIFICAÇÃO INICIAL
# ============================================

PS_TEMPO = "👉 Você já tem seu plano de saúde há mais de 2 anos?"

PS_SITUACAO = (
    "Para que eu possa te direcionar corretamente, qual é a sua situação atual com o plano de saúde?\n\n"
    "1️⃣ Reparadora\n"
    "2️⃣ Negativa de cirurgia\n"
    "3️⃣ Medicamento negado\n"
    "4️⃣ Exame negado\n"
    "5️⃣ Home care\n"
    "6️⃣ Terapias (fono, ABA, fisio, psicopedagogia...)\n"
    "7️⃣ Reajuste\n"
    "8️⃣ Coparticipação elevada\n"
    "9️⃣ Erro médico\n"
    "🔟 OUTRO"
)

# ============================================
# 1. REPARADORA - FLUXO COMPLETO
# ============================================

REP_Q1 = "👉 Você realizou a cirurgia bariátrica ou teve uma perda de peso expressiva através de dieta, exercícios ou uso das canetas emagrecedoras (Mounjaro, Ozempic, Tirzepatida...)?"

REP_Q2 = "👉 Você já chegou ou ainda falta pouco pro peso que gostaria?"

REP_CONSULTA_67 = (
    "Faz todo sentido querer entender bem a situação antes de tomar qualquer decisão.\n\n"
    "Para isso, ofereço uma **consulta de orientação jurídica** — você fala diretamente com a {lawyer}, "
    "tira todas as suas dúvidas e entende com clareza quais são seus direitos e quais caminhos "
    "existem para o seu caso.\n\n"
    "💬 O valor da consulta é de **R$ 67,00** e é feita online, no horário que melhor funcionar pra você. "
    "E se durante ou depois da consulta você decidir que quer avançar com o acompanhamento jurídico "
    "completo, também é possível — aí conversamos sobre isso na hora. Mas sem nenhuma pressão.\n\n"
    "Gostaria de agendar um horário ainda essa semana?"
)

REP_EMPATIA = (
    "Eu entendo que essa pele que restou é o capítulo final de uma grande superação, mas ela também pode ser um peso físico e emocional. "
    "Para eu desenhar a melhor estratégia para você, me conte um pouco…"
)

REP_Q3 = "👉 Esse excesso de pele hoje te causa dores, assaduras ou dermatites que não curam? E além do corpo, como isso tem afetado a sua autoestima e a sua liberdade de movimento no dia a dia?"

REP_Q4 = "👉 Quais cirurgias reparadoras você teria interesse em fazer?"

REP_Q5 = "👉 Certo... Você já chegou a ir no médico cirurgião plástico pra solicitar as reparadoras e emitir os laudos?"

REP_ACOMPANHAMENTO = (
    "Você está no caminho certo 💙 Muitas pessoas acabam procurando ajuda só depois da negativa ou quando o problema já está mais avançado. "
    "Mas quando a gente atua antes, conseguimos evitar erros e fortalecer muito o caso.\n\n"
    "Você prefere tentar sozinho com o plano ou quer o acompanhamento da {lawyer} para garantir que o seu pedido seja feito à prova de negativas?"
)

# ============================================
# 2. NEGATIVA DE CIRURGIA - ESPECIALIDADES
# ============================================

NEG_ESPECIALIDADE = (
    "Para que eu possa te direcionar corretamente, qual é o tipo de cirurgia que foi negada?\n\n"
    "1️⃣ Endometriose\n"
    "2️⃣ Bariátrica\n"
    "3️⃣ Oncologia (Câncer)\n"
    "4️⃣ Cardiologia (Coração)\n"
    "5️⃣ Neurocirurgia\n"
    "6️⃣ Ortopedia\n"
    "7️⃣ Oftalmologia\n"
    "8️⃣ OUTRO"
)

# Endometriose
NEG_ENDO = [
    "👉 Qual tipo de cirurgia foi indicada e pro seu caso?",
    "👉 O plano negou formalmente ou simplesmente não respondeu?",
    "👉 O plano justificou a negativa de alguma forma? (Ex: 'eletivo', 'sem cobertura', 'período de carência')",
    "👉 Você tem os exames que demonstram o seu diagnóstico?",
    "👉 Você já tentou resolver isso diretamente com o plano (ligação, protocolo, ouvidoria ou recurso formal)?"
]

# Bariátrica
NEG_BARI = [
    "👉 Qual o seu IMC atual? Se não souber, pode me falar somente seu peso atual e sua altura.",
    "👉 Você tem comorbidades? (diabetes, hipertensão, apneia do sono, problemas nas articulações)",
    "👉 Fez o acompanhamento multidisciplinar exigido (nutricionista, psicólogo, endocrinologista)?",
    "👉 O plano negou formalmente ou simplesmente não respondeu?",
    "👉 O plano justificou a negativa de alguma forma?",
    "👉 Você já tentou resolver isso diretamente com o plano?"
]

# Oncologia
NEG_ONCO = [
    "👉 Qual o tipo de câncer e qual procedimento foi indicado (cirurgia, quimio, radio, imunoterapia)?",
    "👉 Já está em tratamento de alguma forma, ou a negativa está impedindo o início?",
    "👉 O plano negou formalmente ou simplesmente não respondeu?",
    "👉 O plano justificou a negativa de alguma forma?",
    "👉 Você tem os exames que demonstram o seu diagnóstico?"
]

# Cardiologia
NEG_CARDIO = [
    "👉 Qual tipo de cirurgia foi indicada e pro seu caso?",
    "👉 No seu caso o plano negou material cirúrgico ou alguma prótese?",
    "👉 O plano negou formalmente ou não respondeu?",
    "👉 Você já está internado aguardando o procedimento ou está em casa esperando a autorização para agendar?",
    "👉 O procedimento foi considerado urgente?",
    "👉 Você tem exames (ecocardiograma, cateterismo, ECG) que confirmam a necessidade cirúrgica?"
]

# Neurocirurgia
NEG_NEURO = [
    "👉 Qual procedimento neurocirúrgico foi indicado?",
    "👉 O paciente está internado ou com dor insuportável e precisa operar imediatamente?",
    "👉 O hospital onde seria realizada a cirurgia é da rede do plano?",
    "👉 Hoje, esse problema neurológico está afetando seus movimentos, causando perda de força ou dores que impedem você de realizar tarefas básicas?",
    "👉 A negativa foi por escrita ou verbal?",
    "👉 O plano negou material cirúrgico ou alguma prótese?"
]

# Ortopedia
NEG_ORTO = [
    "👉 Qual cirurgia ortopédica foi indicada?",
    "👉 A condição está limitando sua mobilidade ou capacidade de trabalho?",
    "👉 O plano justificou a negativa de alguma forma? (Ex: 'eletivo', 'sem cobertura', 'período de carência')",
    "É muito comum os planos de saúde negarem tratamento com justificativas infundadas, ignorando a indicação do seu médico. Mas a lei é clara: quem decide o melhor pra você é ele, não o plano.",
    "👉 No seu caso o plano negou material cirúrgico ou alguma prótese?",
    "👉 Essa negativa do plano foi por escrita ou verbal?",
    "👉 Você tem exames de imagem (ressonância magnética, tomografia) que confirmam a necessidade cirúrgica?"
]

# Oftalmologia
NEG_OFTAL = [
    "👉 Qual cirurgia oftalmológica foi indicada?",
    "👉 A condição está afetando sua visão de forma significativa?",
    "👉 O médico indicou urgência, risco de perda de visão se não operar logo?",
    "👉 O plano justificou a negativa de alguma forma? (Ex: 'eletivo', 'sem cobertura', 'período de carência')",
    "👉 Essa negativa do plano foi por escrita ou verbal?"
]

# OUTRO
NEG_OUTRO_INTRO = "Entendido! Cada procedimento cirúrgico tem a sua importância e, se o seu médico indicou, é porque é necessário para a sua saúde. O plano não tem o direito de 'escolher' qual cirurgia você deve ou não fazer."

NEG_OUTRO = [
    "👉 Qual cirurgia foi indicada pelo seu médico?",
    "👉 Para qual problema ou doença ela foi recomendada?",
    "👉 Você possui exames que comprovam a necessidade?",
    "👉 A cirurgia foi negada?",
    "É muito comum os planos de saúde negarem tratamento com justificativas infundadas, ignorando a indicação do seu médico. Mas a lei é clara: quem decide o melhor pra você é ele, não o plano.",
    "👉 O plano justificou a negativa de alguma forma? (Ex: 'eletivo', 'sem cobertura', 'período de carência')",
    "👉 Essa negativa do plano foi por escrita ou verbal?",
    "👉 Hoje, a falta dessa cirurgia te impede de trabalhar, de dormir bem ou de realizar suas atividades simples do dia a dia?",
    "👉 Se você não realizar a cirurgia, pode ocorrer:",
    "👉 Você possui exames que comprovam a necessidade?"
]

# ============================================
# 3. MEDICAMENTO NEGADO
# ============================================

MED_Q1 = "👉 Qual medicamento foi negado pelo plano?"
MED_Q2 = "👉 O médico indicou este medicamento como o único tratamento eficaz para seu caso?"
MED_Q3 = "👉 Você já tentou resolver isso diretamente com o plano (ligação, protocolo, ouvidoria)?"
MED_Q4 = "👉 O plano negou formalmente ou simplesmente não respondeu?"
MED_Q5 = "👉 O plano justificou a negativa de alguma forma?"

MED_PERGUNTAS = [MED_Q1, MED_Q2, MED_Q3, MED_Q4, MED_Q5]

# ============================================
# 4. EXAME NEGADO
# ============================================

EXAME_Q1 = "👉 Qual exame foi negado pelo plano?"
EXAME_Q2 = "👉 O médico justificou por que esse exame é necessário?"
EXAME_Q3 = "👉 Você já tentou resolver isso diretamente com o plano?"
EXAME_Q4 = "👉 O plano negou formalmente ou simplesmente não respondeu?"
EXAME_Q5 = "👉 O plano justificou a negativa de alguma forma?"

EXAME_PERGUNTAS = [EXAME_Q1, EXAME_Q2, EXAME_Q3, EXAME_Q4, EXAME_Q5]

# ============================================
# 5. HOME CARE
# ============================================

HC_Q1 = "👉 Qual tipo de atendimento home care foi negado?"
HC_Q2 = "👉 O médico indicou a necessidade de home care? Por quanto tempo?"
HC_Q3 = "👉 Você já tentou resolver isso diretamente com o plano?"
HC_Q4 = "👉 O plano negou formalmente ou simplesmente não respondeu?"
HC_Q5 = "👉 O plano justificou a negativa de alguma forma?"

HC_PERGUNTAS = [HC_Q1, HC_Q2, HC_Q3, HC_Q4, HC_Q5]

# ============================================
# 6. TERAPIAS
# ============================================

TERAPIA_Q1 = "👉 Qual tipo de terapia foi negada? (fono, ABA, fisio, psicopedagogia, etc.)"
TERAPIA_Q2 = "👉 O médico ou especialista indicou essa terapia?"
TERAPIA_Q3 = "👉 Quantas sessões foram negadas ou o plano negou completamente?"
TERAPIA_Q4 = "👉 Você já tentou resolver isso diretamente com o plano?"
TERAPIA_Q5 = "👉 O plano negou formalmente ou simplesmente não respondeu?"

TERAPIA_PERGUNTAS = [TERAPIA_Q1, TERAPIA_Q2, TERAPIA_Q3, TERAPIA_Q4, TERAPIA_Q5]

# ============================================
# 7. REAJUSTE
# ============================================

REAJ_Q1 = "👉 Qual foi o percentual de reajuste que você recebeu?"
REAJ_Q2 = "👉 Você acredita que esse reajuste foi abusivo ou acima do permitido?"
REAJ_Q3 = "👉 Você tem quanto tempo de plano?"
REAJ_Q4 = "👉 O reajuste foi aplicado por faixa etária ou anual?"
REAJ_Q5 = "👉 Você já entrou em contato com a operadora para questionar o reajuste?"

REAJ_PERGUNTAS = [REAJ_Q1, REAJ_Q2, REAJ_Q3, REAJ_Q4, REAJ_Q5]

# ============================================
# 8. COPARTICIPAÇÃO ELEVADA
# ============================================

COPART_Q1 = "👉 Qual é o valor da sua coparticipação atual?"
COPART_Q2 = "👉 Você acha que esse valor está muito elevado comparado ao seu plano anterior?"
COPART_Q3 = "👉 Você tem quanto tempo de plano?"
COPART_Q4 = "👉 A coparticipação aumentou recentemente?"
COPART_Q5 = "👉 Você já questionou a operadora sobre esse valor?"

COPART_PERGUNTAS = [COPART_Q1, COPART_Q2, COPART_Q3, COPART_Q4, COPART_Q5]

# ============================================
# 9. ERRO MÉDICO
# ============================================

ERRO_Q1 = "👉 Qual foi o erro médico que ocorreu?"
ERRO_Q2 = "👉 Você sofreu danos ou sequelas por causa desse erro?"
ERRO_Q3 = "👉 O plano reconheceu o erro ou está negando responsabilidade?"
ERRO_Q4 = "👉 Você já procurou alguma orientação jurídica sobre isso?"
ERRO_Q5 = "👉 Você tem documentação médica comprovando o erro?"

ERRO_PERGUNTAS = [ERRO_Q1, ERRO_Q2, ERRO_Q3, ERRO_Q4, ERRO_Q5]

# ============================================
# 10. OUTRO
# ============================================

OUTRO_Q1 = "👉 Qual é a sua situação com o plano de saúde?"
OUTRO_Q2 = "👉 O plano negou ou está recusando algo?"
OUTRO_Q3 = "👉 Você já tentou resolver isso diretamente com o plano?"
OUTRO_Q4 = "👉 Você tem documentação sobre essa situação?"
OUTRO_Q5 = "👉 Como isso tem afetado sua saúde ou vida?"

OUTRO_PERGUNTAS = [OUTRO_Q1, OUTRO_Q2, OUTRO_Q3, OUTRO_Q4, OUTRO_Q5]

# ============================================
# CAMINHO B - MENOS DE 2 ANOS
# ============================================

MENOS_2ANOS_INTRO = (
    "Entendo! Muitas pessoas acreditam que precisam esperar 2 anos para ter direito a cirurgias ou tratamentos complexos, "
    "mas a lei nem sempre funciona assim. Existem situações onde o plano é obrigado a cobrir o seu procedimento mesmo que você tenha "
    "poucos meses de contrato, especialmente se houver urgência ou se a doença não foi declarada por má-fé."
)

MENOS_2ANOS_Q1 = "👉 Me conta, qual o tratamento que você precisa fazer?"
MENOS_2ANOS_Q2 = "👉 No seu caso, o médico comentou se isso é urgente ou pode trazer algum risco se não for feito?"
MENOS_2ANOS_FEEDBACK = "Perfeito, isso é importante! 👊 SE HÁ URGÊNCIA, o plano já deveria cobrir normalmente esse tipo de situação. Mesmo assim, eles podem acabar negando indevidamente em alguns casos."
MENOS_2ANOS_Q3 = "👉 O médico indicou que o tratamento é urgente?"
MENOS_2ANOS_Q4 = "👉 Você já sabia dessa doença antes de contratar o plano?"
MENOS_2ANOS_Q5 = "👉 O plano negou alegando carência?"
MENOS_2ANOS_Q6 = "👉 Você tem a negativa por escrito?"

# ============================================
# DETECÇÃO DE VALORES - 3 CENÁRIOS
# ============================================

VALOR_CENARIO1 = (
    "Compreendo sua dúvida sobre o investimento. No meu escritório, nós não trabalhamos com valores iguais porque cada vida e cada urgência são únicas.\n\n"
    "Como o seu caso envolve uma situação de alta complexidade técnica e risco direto à saúde, "
    "a {lawyer} não define valores para casos de alta complexidade por mensagem de texto.\n\n"
    "Para situações assim, é necessária uma **Reunião Estratégica por vídeo (15 minutos)**. Nessa reunião, ela vai te apresentar o plano de ação "
    "para cercar o juiz e garantir que seu direito não seja negado, além de alinhar o investimento necessário para a condução do processo."
)

VALOR_CENARIO2 = (
    "Compreendo sua dúvida sobre o investimento. No meu escritório, nós não trabalhamos com valores iguais porque cada caso exige um empenho técnico diferente.\n\n"
    "Como o seu caso envolve a liberação de consulta ou exame, a {lawyer} faz questão de analisar pessoalmente a documentação na mesa de trabalho "
    "antes de passar qualquer orçamento.\n\n"
    "Valores para esse tipo de demanda são informados somente após essa triagem técnica, garantindo que o valor seja justo e condizente com a complexidade "
    "do seu pedido. Assim que ela analisar seus documentos, você receberá o retorno."
)

VALOR_CENARIO3 = (
    "Compreendo sua dúvida sobre o investimento. No meu escritório, tratamos cada contrato de forma individualizada, pois os valores de reajuste "
    "e as cláusulas variam drasticamente entre as operadoras.\n\n"
    "Como o seu caso envolve uma análise financeira e contratual detalhada, a {lawyer} não define valores para questões contratuais por mensagem de texto.\n\n"
    "É necessário uma **Reunião Estratégica** (vídeo ou áudio) para que ela te explique como buscaremos o reequilíbrio do seu plano e a restituição de valores "
    "pagos indevidamente, alinhando o investimento da consultoria nessa etapa."
)

# ============================================
# DECISÃO COMPARTILHADA
# ============================================

DECISAO_SIM = (
    "Excelente! É fundamental que ele(a) participe, pois como o Direito à Saúde envolve "
    "prazos muito curtos e decisões imediatas sobre o tratamento, é bom que todos "
    "estejam na mesma página.\n\n"
    f"Vamos escolher um horário que fique confortável para vocês dois. Logo abaixo vou te mandar a agenda da {{lawyer}}.\n\n"
    f"🔗 {CALENDLY_LINK}"
)

DECISAO_NAO = (
    "Perfeito, facilita bastante o nosso fluxo. Como você é a única responsável pela decisão, "
    "conseguimos dar um andamento mais ágil aos trabalhos.\n\n"
    f"Logo abaixo vou te mandar a agenda da {{lawyer}}, e você marque o dia e horário que fica melhor pra você.\n\n"
    f"🔗 {CALENDLY_LINK}"
)

# ============================================
# PROCESSAMENTO DO FLUXO
# ============================================

def processar(resposta: str):
    estado = st.session_state.estado
    dados = st.session_state.dados

    # DETECTAR PERGUNTA SOBRE VALOR SEMPRE PRIMEIRO
    if detect_valor_question(resposta):
        situacao = dados.get("situacao", "")
        if any(s in situacao for s in ["Cirurgia", "Medicamento", "Home", "Reparadora"]):
            add_bot(VALOR_CENARIO1)
        elif any(s in situacao for s in ["Exame", "Terapia"]):
            add_bot(VALOR_CENARIO2)
        elif any(s in situacao for s in ["Reajuste", "Coparticipação"]):
            add_bot(VALOR_CENARIO3)
        return

    # ========== INICIO ==========
    if estado == "INICIO":
        st.session_state.nome = resposta
        dados["nome"] = resposta
        st.session_state.estado = "CANAL"
        add_bot(MSG_CANAL.format(nome=resposta))

    # ========== CANAL ==========
    elif estado == "CANAL":
        if "plano" in normalize(resposta):
            dados["canal"] = "PLANO"
            st.session_state.estado = "PS_TEMPO"
            add_bot(PS_TEMPO)
        else:
            st.session_state.estado = "FIM"
            add_bot("SUS - Fluxo em desenvolvimento")

    # ========== PLANO - TEMPO ==========
    elif estado == "PS_TEMPO":
        if is_sim(resposta):
            dados["plano_tempo"] = "SIM"
            st.session_state.estado = "PS_SITUACAO"
            add_bot(PS_SITUACAO)
        else:
            dados["plano_tempo"] = "NAO"
            st.session_state.estado = "MENOS_2ANOS_INTRO"
            add_bot(MENOS_2ANOS_INTRO)

    # ========== PLANO - SITUAÇÃO (CAMINHO A) ==========
    elif estado == "PS_SITUACAO":
        if "1" in resposta:
            dados["situacao"] = "Reparadora"
            st.session_state.estado = "REP_Q1"
            add_bot(REP_Q1)
        elif "2" in resposta:
            dados["situacao"] = "Negativa de Cirurgia"
            st.session_state.estado = "NEG_ESPECIALIDADE"
            add_bot(NEG_ESPECIALIDADE)
        elif "3" in resposta:
            dados["situacao"] = "Medicamento negado"
            st.session_state.perguntas_ativas = MED_PERGUNTAS.copy()
            st.session_state.pergunta_idx = 0
            st.session_state.estado = "PERGUNTAS_GENERICO"
            add_bot(st.session_state.perguntas_ativas[0])
        elif "4" in resposta:
            dados["situacao"] = "Exame negado"
            st.session_state.perguntas_ativas = EXAME_PERGUNTAS.copy()
            st.session_state.pergunta_idx = 0
            st.session_state.estado = "PERGUNTAS_GENERICO"
            add_bot(st.session_state.perguntas_ativas[0])
        elif "5" in resposta:
            dados["situacao"] = "Home care"
            st.session_state.perguntas_ativas = HC_PERGUNTAS.copy()
            st.session_state.pergunta_idx = 0
            st.session_state.estado = "PERGUNTAS_GENERICO"
            add_bot(st.session_state.perguntas_ativas[0])
        elif "6" in resposta:
            dados["situacao"] = "Terapias"
            st.session_state.perguntas_ativas = TERAPIA_PERGUNTAS.copy()
            st.session_state.pergunta_idx = 0
            st.session_state.estado = "PERGUNTAS_GENERICO"
            add_bot(st.session_state.perguntas_ativas[0])
        elif "7" in resposta:
            dados["situacao"] = "Reajuste"
            st.session_state.perguntas_ativas = REAJ_PERGUNTAS.copy()
            st.session_state.pergunta_idx = 0
            st.session_state.estado = "PERGUNTAS_GENERICO"
            add_bot(st.session_state.perguntas_ativas[0])
        elif "8" in resposta:
            dados["situacao"] = "Coparticipação elevada"
            st.session_state.perguntas_ativas = COPART_PERGUNTAS.copy()
            st.session_state.pergunta_idx = 0
            st.session_state.estado = "PERGUNTAS_GENERICO"
            add_bot(st.session_state.perguntas_ativas[0])
        elif "9" in resposta:
            dados["situacao"] = "Erro médico"
            st.session_state.perguntas_ativas = ERRO_PERGUNTAS.copy()
            st.session_state.pergunta_idx = 0
            st.session_state.estado = "PERGUNTAS_GENERICO"
            add_bot(st.session_state.perguntas_ativas[0])
        elif "10" in resposta:
            dados["situacao"] = "OUTRO"
            st.session_state.perguntas_ativas = OUTRO_PERGUNTAS.copy()
            st.session_state.pergunta_idx = 0
            st.session_state.estado = "PERGUNTAS_GENERICO"
            add_bot(st.session_state.perguntas_ativas[0])

    # ========== REPARADORA ==========
    elif estado == "REP_Q1":
        dados["rep_q1"] = resposta
        st.session_state.estado = "REP_Q2"
        add_bot(REP_Q2)

    elif estado == "REP_Q2":
        if is_nao(resposta) or "ainda" in normalize(resposta):
            st.session_state.estado = "REP_CONSULTA"
            add_bot(REP_CONSULTA_67)
        else:
            st.session_state.estado = "REP_EMPATIA"
            add_bot(REP_EMPATIA)

    elif estado == "REP_CONSULTA":
        if is_sim(resposta):
            st.session_state.estado = "FIM"
            add_bot(f"Ótimo! Agende sua consulta: {CALENDLY_LINK}")
        else:
            st.session_state.estado = "FIM"
            add_bot("Entendo. Fica à vontade para retornar quando precisar!")

    elif estado == "REP_EMPATIA":
        st.session_state.estado = "REP_Q3"
        add_bot(REP_Q3)

    elif estado == "REP_Q3":
        dados["rep_q3"] = resposta
        st.session_state.estado = "REP_Q4"
        add_bot(REP_Q4)

    elif estado == "REP_Q4":
        dados["rep_q4"] = resposta
        st.session_state.estado = "REP_Q5"
        add_bot(REP_Q5)

    elif estado == "REP_Q5":
        if is_sim(resposta):
            st.session_state.estado = "REP_ACOMPANHAMENTO"
            add_bot(REP_ACOMPANHAMENTO)
        else:
            st.session_state.estado = "REP_ACOMPANHAMENTO"
            add_bot(REP_ACOMPANHAMENTO)

    elif estado == "REP_ACOMPANHAMENTO":
        if "acompanhamento" in normalize(resposta) or "dra" in normalize(resposta):
            st.session_state.estado = "DECISAO_FAMILIAR"
            add_bot("Antes de agendarmos: além de você, tem mais alguém que participe das decisões familiares ou financeiras?")
        else:
            st.session_state.estado = "FIM"
            add_bot("Entendo! Fica à vontade para retornar quando precisar de ajuda.")

    # ========== NEGATIVA DE CIRURGIA ==========
    elif estado == "NEG_ESPECIALIDADE":
        if "1" in resposta:
            st.session_state.perguntas_ativas = NEG_ENDO.copy()
            dados["neg_esp"] = "Endometriose"
        elif "2" in resposta:
            st.session_state.perguntas_ativas = NEG_BARI.copy()
            dados["neg_esp"] = "Bariátrica"
        elif "3" in resposta:
            st.session_state.perguntas_ativas = NEG_ONCO.copy()
            dados["neg_esp"] = "Oncologia"
        elif "4" in resposta:
            st.session_state.perguntas_ativas = NEG_CARDIO.copy()
            dados["neg_esp"] = "Cardiologia"
        elif "5" in resposta:
            st.session_state.perguntas_ativas = NEG_NEURO.copy()
            dados["neg_esp"] = "Neurocirurgia"
        elif "6" in resposta:
            st.session_state.perguntas_ativas = NEG_ORTO.copy()
            dados["neg_esp"] = "Ortopedia"
        elif "7" in resposta:
            st.session_state.perguntas_ativas = NEG_OFTAL.copy()
            dados["neg_esp"] = "Oftalmologia"
        else:
            st.session_state.perguntas_ativas = NEG_OUTRO.copy()
            dados["neg_esp"] = "OUTRO"
            add_bot(NEG_OUTRO_INTRO)
        
        st.session_state.pergunta_idx = 0
        st.session_state.estado = "NEG_PERGUNTAS"
        if dados["neg_esp"] != "OUTRO":
            add_bot(st.session_state.perguntas_ativas[0])

    elif estado == "NEG_PERGUNTAS":
        idx = st.session_state.pergunta_idx
        perguntas = st.session_state.perguntas_ativas
        
        dados[f"neg_q{idx}"] = resposta
        idx += 1
        st.session_state.pergunta_idx = idx
        
        if idx < len(perguntas):
            add_bot(perguntas[idx])
        else:
            st.session_state.estado = "ACOMPANHAMENTO"
            add_bot(REP_ACOMPANHAMENTO)

    # ========== PERGUNTAS GENÉRICO (Medicamento, Exame, Home Care, Terapias, Reajuste, Coparticipação, Erro Médico, OUTRO) ==========
    elif estado == "PERGUNTAS_GENERICO":
        idx = st.session_state.pergunta_idx
        perguntas = st.session_state.perguntas_ativas
        
        dados[f"q{idx}"] = resposta
        idx += 1
        st.session_state.pergunta_idx = idx
        
        if idx < len(perguntas):
            add_bot(perguntas[idx])
        else:
            st.session_state.estado = "ACOMPANHAMENTO"
            add_bot(REP_ACOMPANHAMENTO)

    # ========== CAMINHO B - MENOS DE 2 ANOS ==========
    elif estado == "MENOS_2ANOS_INTRO":
        st.session_state.estado = "MENOS_2ANOS_Q1"
        add_bot(MENOS_2ANOS_Q1)

    elif estado == "MENOS_2ANOS_Q1":
        dados["menos2anos_tratamento"] = resposta
        st.session_state.estado = "MENOS_2ANOS_Q2"
        add_bot(MENOS_2ANOS_Q2)

    elif estado == "MENOS_2ANOS_Q2":
        dados["menos2anos_risco"] = resposta
        st.session_state.estado = "MENOS_2ANOS_FEEDBACK"
        add_bot(MENOS_2ANOS_FEEDBACK)

    elif estado == "MENOS_2ANOS_FEEDBACK":
        st.session_state.estado = "MENOS_2ANOS_Q3"
        add_bot(MENOS_2ANOS_Q3)

    elif estado == "MENOS_2ANOS_Q3":
        dados["menos2anos_urgente"] = resposta
        st.session_state.estado = "MENOS_2ANOS_Q4"
        add_bot(MENOS_2ANOS_Q4)

    elif estado == "MENOS_2ANOS_Q4":
        dados["menos2anos_sabia"] = resposta
        st.session_state.estado = "MENOS_2ANOS_Q5"
        add_bot(MENOS_2ANOS_Q5)

    elif estado == "MENOS_2ANOS_Q5":
        dados["menos2anos_carencia"] = resposta
        st.session_state.estado = "MENOS_2ANOS_Q6"
        add_bot(MENOS_2ANOS_Q6)

    elif estado == "MENOS_2ANOS_Q6":
        dados["menos2anos_escrito"] = resposta
        st.session_state.estado = "ACOMPANHAMENTO"
        add_bot(REP_ACOMPANHAMENTO)

    # ========== ACOMPANHAMENTO ==========
    elif estado == "ACOMPANHAMENTO":
        if "acompanhamento" in normalize(resposta) or "dra" in normalize(resposta):
            st.session_state.estado = "DECISAO_FAMILIAR"
            add_bot("Antes de agendarmos: além de você, tem mais alguém que participe das decisões familiares ou financeiras?")
        else:
            st.session_state.estado = "FIM"
            add_bot("Entendo! Fica à vontade para retornar quando precisar de ajuda.")

    # ========== DECISÃO FAMILIAR ==========
    elif estado == "DECISAO_FAMILIAR":
        if is_sim(resposta):
            st.session_state.estado = "FIM"
            add_bot(DECISAO_SIM.format(lawyer=LAWYER_NAME))
        elif is_nao(resposta) or "sozinho" in normalize(resposta):
            st.session_state.estado = "FIM"
            add_bot(DECISAO_NAO.format(lawyer=LAWYER_NAME))
        else:
            st.session_state.estado = "FIM"
            add_bot("Perfeito! Vamos agendar. " + DECISAO_NAO.format(lawyer=LAWYER_NAME))

# ============================================
# INTERFACE STREAMLIT
# ============================================

def main():
    st.title("⚖️ Iara Bot - Assistente Jurídica em Direito da Saúde")
    st.caption(f"Especialista: {LAWYER_NAME} | Atendimento: SUS, Planos de Saúde")

    init_session()

    with st.sidebar:
        st.markdown("### 📋 Informações da Sessão")
        if st.session_state.nome:
            st.info(f"**Cliente:** {st.session_state.nome}")
        if st.session_state.dados.get("situacao"):
            st.info(f"**Situação:** {st.session_state.dados['situacao']}")
        st.markdown("---")
        if st.button("🔄 Nova Conversa", use_container_width=True):
            reset()
            st.rerun()

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

        estado = st.session_state.estado

        # Botões contextuais
        if estado == "CANAL":
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("🏥 SUS", use_container_width=True):
                    add_user("SUS")
                    processar("SUS")
                    st.rerun()
            with col_b:
                if st.button("📋 Plano de Saúde", use_container_width=True):
                    add_user("Plano de Saúde")
                    processar("Plano de Saúde")
                    st.rerun()

        elif estado == "PS_TEMPO":
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("✅ SIM", use_container_width=True):
                    add_user("SIM")
                    processar("sim")
                    st.rerun()
            with col_b:
                if st.button("❌ NÃO", use_container_width=True):
                    add_user("NÃO")
                    processar("não")
                    st.rerun()

        elif estado == "PS_SITUACAO":
            opcoes = ["Reparadora", "Negativa Cirurgia", "Medicamento", "Exame", "Home Care", "Terapias", "Reajuste", "Coparticipação", "Erro Médico", "OUTRO"]
            cols = st.columns(2)
            for i, op in enumerate(opcoes):
                with cols[i % 2]:
                    if st.button(op, use_container_width=True):
                        add_user(op)
                        processar(str(i+1))
                        st.rerun()

        elif estado == "NEG_ESPECIALIDADE":
            esp = ["Endometriose", "Bariátrica", "Oncologia", "Cardiologia", "Neurocirurgia", "Ortopedia", "Oftalmologia", "OUTRO"]
            cols = st.columns(2)
            for i, e in enumerate(esp):
                with cols[i % 2]:
                    if st.button(e, use_container_width=True):
                        add_user(e)
                        processar(str(i+1))
                        st.rerun()

        elif estado in ["REP_Q2", "REP_Q5", "MENOS_2ANOS_Q3", "MENOS_2ANOS_Q4", "MENOS_2ANOS_Q5", "MENOS_2ANOS_Q6"]:
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("✅ SIM", use_container_width=True):
                    add_user("SIM")
                    processar("sim")
                    st.rerun()
            with col_b:
                if st.button("❌ NÃO", use_container_width=True):
                    add_user("NÃO")
                    processar("não")
                    st.rerun()

        elif estado in ["REP_ACOMPANHAMENTO", "ACOMPANHAMENTO"]:
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("👤 Tentar sozinho", use_container_width=True):
                    add_user("Tentar sozinho")
                    processar("sozinho")
                    st.rerun()
            with col_b:
                if st.button("👩‍⚖️ Com acompanhamento da Dra.", use_container_width=True):
                    add_user("Com acompanhamento da Dra.")
                    processar("acompanhamento")
                    st.rerun()

        elif estado == "DECISAO_FAMILIAR":
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("✅ SIM", use_container_width=True):
                    add_user("SIM")
                    processar("sim")
                    st.rerun()
            with col_b:
                if st.button("❌ NÃO", use_container_width=True):
                    add_user("NÃO")
                    processar("não")
                    st.rerun()

        # Input de texto
        if estado != "FIM":
            st.markdown("---")
            col_input, col_send = st.columns([4, 1])
            with col_input:
                user_input = st.text_input("Digite sua mensagem:", key="user_input", placeholder="Digite aqui sua resposta...")
            with col_send:
                if st.button("📤 Enviar", use_container_width=True):
                    if user_input:
                        add_user(user_input)
                        processar(user_input)
                        st.rerun()
        else:
            st.markdown("---")
            st.success("✅ Atendimento finalizado!")

    if not st.session_state.messages:
        add_bot(MSG_BOAS_VINDAS)
        st.rerun()

if __name__ == "__main__":
    main()
