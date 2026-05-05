"""
Iara Bot - Assistente Jurídica em Direito da Saúde
VERSÃO CORRIGIDA E COMPLETA - v2
"""

import streamlit as st

# ============================================
# CONFIGURAÇÕES
# ============================================
CALENDLY_LINK = "https://calendly.com/dra-lethicia"
L = "Dra. Lethicia Fernanda"

LINK_CARTAO_97  = "https://www.asaas.com/c/oilhnffc7xyvc4n6"
LINK_PIX_97     = "https://www.asaas.com/c/9025wgqkpuziono4"
LINK_CARTAO_500 = "https://www.asaas.com/c/apigp8m45tileghw"
LINK_PIX_500    = "https://www.asaas.com/c/x1dfvyoajxnlgpp2"

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
    return any(p in _n(r) for p in ["sim", "s", "yes", "quero", "ok", "claro", "vamos", "aceito", "topo", "com certeza", "certeza"])

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
# HELPER: nome legível da situação
# ============================================
SITUACAO_LABEL = {
    "1": "Reparadora",
    "2": "Negativa de cirurgia",
    "3": "Medicamento negado",
    "4": "Exame negado",
    "5": "Home Care",
    "6": "Terapias",
    "7": "Reajuste",
    "8": "Coparticipação elevada",
    "9": "Erro médico",
    "10": "Outro",
    "reparadora": "Reparadora",
    "negativa": "Negativa de cirurgia",
    "medicamento": "Medicamento negado",
    "exame": "Exame negado",
    "home": "Home Care",
    "terapia": "Terapias",
    "reajuste": "Reajuste",
    "copart": "Coparticipação elevada",
    "copa": "Coparticipação elevada",
    "erro": "Erro médico",
}

def _situacao_nome(resposta: str) -> str:
    """Retorna o nome legível da situação escolhida."""
    r = _n(resposta)
    for key, label in SITUACAO_LABEL.items():
        if key in r:
            return label
    return resposta  # fallback: devolve o que veio

# ============================================
# MENSAGENS PRINCIPAIS
# ============================================

# CORREÇÃO: emoji alterado de 🌟 para 🌹
MSG_BOAS_VINDAS = (
    "Olá, seja bem vindo(a). 🌹\n\n"
    "Sou a Lara, assistente jurídica do escritório da Dra Lethicia Fernanda, "
    "advogada especialista em Direito da Saúde.\n\n"
    "**Fico feliz que você entrou em contato conosco.**\n\n"
    "Qual o seu nome?"
)

MSG_CANAL = "Olá, {nome}! Seu atendimento é pelo **SUS** ou por **Plano de Saúde**?"

# ============================================
# MENSAGENS DE VALORES (INTERCEPTAÇÃO) — VERSÃO ATUALIZADA
# ============================================
MSG_VALORES_CIRURGIA = (
    "Compreendo perfeitamente sua dúvida sobre o investimento. No entanto, como lidamos com o Direito à Saúde, "
    "entendemos que cada caso e cada urgência são únicos.\n\n"
    "Por envolver uma vida e um cenário de alta complexidade técnica, a Dra. Lethicia Fernanda não define honorários "
    "por mensagens de texto, para garantir a precisão que o seu caso exige. Para situações assim, realizamos uma "
    "Reunião de Viabilidade Jurídica por vídeo (20 minutos).\n\n"
    "Nesse encontro, ela apresentará o plano de ação estratégico para cercar o juiz e garantir que seu direito seja "
    "respeitado, além de alinhar o investimento necessário para a condução segura do processo. Esta reunião inicial "
    "é gratuita e totalmente online.\n\n"
    "Podemos seguir com a marcação do seu horário por aqui?"
)

MSG_VALORES_CONSULTA = (
    "Compreendo sua dúvida sobre o investimento. No meu escritório, nós não trabalhamos com valores iguais porque "
    "cada caso exige um empenho técnico diferente.\n\n"
    "Como o seu caso envolve a liberação de Consulta / Exame Específico, a Dra. Lethicia faz questão de analisar "
    "pessoalmente a documentação na mesa de trabalho antes de passar qualquer orçamento.\n\n"
    "Valores para esse tipo de demanda são informados somente após essa triagem técnica, garantindo que o valor seja "
    "justo e condizente com a complexidade do seu pedido. Assim que ela analisar seus documentos, você receberá o retorno."
)

MSG_VALORES_REAJUSTE = (
    "Compreendo perfeitamente sua dúvida sobre o investimento. No entanto, como lidamos com o Direito à Saúde, "
    "entendemos que cada caso e cada urgência são únicos.\n\n"
    "Por envolver uma análise financeira e contratual detalhada, a Dra. Lethicia Fernanda não define honorários por "
    "mensagens de texto, para garantir a precisão que o seu caso exige. Para situações assim, realizamos uma "
    "Reunião de Viabilidade Jurídica por vídeo (20 minutos).\n\n"
    "Nesse encontro, ela explicará como buscaremos o reequilíbrio do seu plano e a restituição de valores pagos "
    "indevidamente, além de alinhar o investimento necessário. Esta reunião inicial é gratuita e totalmente online.\n\n"
    "Podemos seguir com a marcação do seu horário por aqui?"
)

# ============================================
# SUS - FLUXO CIRURGIA
# ============================================

MSG_SUS_DEMANDA = "Me diga o que você está aguardando?\n\n🔪 Cirurgia / Tratamento\n\n📋 Consultas / Exames"

MSG_SUS_ESPECIALIDADE = (
    "Para que eu direcione você para o protocolo de urgência correto, "
    "qual problema estamos enfrentando hoje?\n\n"
    "1️⃣ Oncologia\n2️⃣ Neurodivergências (TEA, TDAH)\n3️⃣ Endometriose / Adenomiose\n"
    "4️⃣ Medicamento\n5️⃣ Bariátrica\n6️⃣ Neurologia / Neurocirurgia\n"
    "7️⃣ Cardiologia\n8️⃣ Outros"
)

# Perguntas SUS por especialidade (CIRURGIA)
PERGUNTAS_ONCOLOGIA = [
    "Entendi... vamos cuidar disso juntos 💙\n\n👉 Você consegue me contar qual é o tipo de câncer?",
    "👉 Você está aguardando atendimento ou tratamento pelo SUS? Se sim, há quanto tempo mais ou menos?",
    "Só pra eu entender melhor seu caso:\n\n👉 O diagnóstico já foi confirmado por biópsia? E você tem esse laudo em mãos?",
    "Entendi...\n\n👉 Você já foi encaminhado para um hospital especializado em câncer (oncologia) pelo SUS ou ainda nem conseguiu passar com um especialista?\n\nInfelizmente, a fila do SUS não respeita o avanço da doença. Se o hospital não iniciou seu tratamento em 60 dias, a lei está sendo descumprida e precisamos forçar o início imediato via Justiça.",
    "👉 Você possui um relatório médico explicando o tratamento que precisa fazer? (se quiser, pode enviar aqui também 📎)",
    "Última perguntinha, que é bem importante:\n\n👉 O médico falou se o seu caso é urgente?",
    "👉 Você possui o comprovante de que está aguardando na fila?\n\nPode ser o print da tela do App Meu SUS Digital, o comprovante de agendamento da Secretaria de Saúde ou o papel da regulação (SISREG) com o número do seu protocolo."
]

PERGUNTAS_NEURO = [
    "Entendi... pode ficar tranquilo(a), vou te ajudar com isso 💙\n\nCasos assim realmente precisam de atenção, principalmente por envolver desenvolvimento.\n\n👉 Me conta: já tem diagnóstico fechado ou ainda está em investigação?",
    "👉 Você tem algum laudo ou relatório médico com o diagnóstico?",
    "Entendo as batalhas diárias que você enfrenta para garantir o melhor para quem você ama. Seja você ou seu filho(a) deve ter seu desenvolvimento barrado por limites impostos pelo **SUS**. Estou aqui para lutar ao seu lado e garantir todas as terapias que são de direito. Agora me conta uma coisa importante:\n\n👉 Quais terapias o médico indicou? (ABA, Psico, fisioterapia...)",
    "E hoje, como está essa situação no SUS?\n\n👉 Você conseguiu iniciar as terapias ou ainda está aguardando?",
    "Entendo...\n\n👉 Você está em fila ou aguardando vaga?",
    "Essa parte é muito importante:\n\n👉 O médico comentou algo sobre prejuízo no desenvolvimento ou necessidade de iniciar rápido as terapias?",
    "Se você puder me contar:\n\n👉 Como essa situação está impactando o dia a dia de vocês?",
    "👉 Você possui o comprovante de que está aguardando na fila?\n\nPode ser o print da tela do App Meu SUS Digital, o comprovante de agendamento da Secretaria de Saúde ou o papel da regulação (SISREG) com o número do seu protocolo."
]

PERGUNTAS_ENDOMETRIOSE = [
    "Entendi... imagino o quanto isso pode estar sendo difícil pra você 🥺. Mas fica tranquila, vou te ajudar com isso 💙.\n\n👉 Você já tem diagnóstico confirmado de endometriose ou adenomiose?",
    "Obrigado por me contar 🙏.\n\n👉 Esse diagnóstico foi feito por exame? Se ainda não fez, qual exame está aguardando?",
    "Sei o quanto a dor e a incerteza cansam... não é justo que sua cirurgia ou exame continue demorando assim. Quero entender melhor sua situação:\n\n👉 Você sente dores fortes ou crises que atrapalham sua rotina?",
    "Agora uma parte bem importante:\n\n👉 O médico indicou algum tratamento específico? (Ex: cirurgia de videolaparoscopia, medicamento...)",
    "👉 Você tem relatório médico explicando esse tratamento?",
    "👉 Você está aguardando há quanto tempo mais ou menos?",
    "👉 O médico colocou em relatório ou te informou se existe risco de piora ou agravamento sem o tratamento?",
    "👉 Você possui o comprovante de que está aguardando na fila?\n\nPode ser o print da tela do App Meu SUS Digital, o comprovante de agendamento da Secretaria de Saúde ou o papel da regulação (SISREG) com o número do seu protocolo."
]

PERGUNTAS_MEDICAMENTO_SUS = [
    "Entendi... vamos ver isso com calma 💙.\n\n👉 Qual foi o medicamento que o médico indicou pra você?",
    "Perfeito, obrigado por me explicar 🙏.\n\n👉 Você tem a receita ou relatório médico desse medicamento?",
    "Entendo a frustração de ter um direito negado justamente quando você mais precisa de suporte...\n\nAo te passar esse medicamento o seu médico escreveu no laudo que este remédio específico é o único que pode tratar seu caso agora e que a interrupção trará riscos à sua vida ou saúde?",
    "Essa parte é bem importante:\n\n👉 Você já utilizou outros medicamentos antes? Se sim, eles não tiveram resultado ou causaram algum problema?",
    "👉 Você chegou a solicitar esse medicamento pelo SUS ou farmácia de alto custo? O que te informaram? (Negado, em análise, falta de estoque...)",
    "👉 O médico comentou o que pode acontecer se você não usar esse medicamento?"
]

PERGUNTAS_BARIATRICA_SUS = [
    "Entendi... vamos ver isso com calma 💙.\n\n👉 Você já tem indicação médica para cirurgia bariátrica?",
    "👉 Você tem algum laudo ou relatório médico indicando a cirurgia?",
    "Só pra eu entender melhor seu caso:\n\n👉 Você sabe me informar seu peso e altura? (Pode ser aproximado).",
    "Essa parte é bem importante:\n\n👉 Você já tentou outros tratamentos antes, como dieta, acompanhamento ou medicamentos? Como foi essa experiência?",
    "Você já está na fila de espera do SUS há quanto tempo? Você possui o comprovante de que está aguardando na fila?\n\nPode ser o print da tela do App Meu SUS Digital, o comprovante de agendamento da Secretaria de Saúde ou o papel da regulação (SISREG) com o número do seu protocolo."
]

PERGUNTAS_NEUROLOGIA_SUS = [
    "Entendi... vamos ver isso com calma 💙.\n\n👉 Você consegue me explicar qual é o problema neurológico ou o que o médico te disse?",
    "O seu caso envolve uma cirurgia de urgência?",
    "👉 Você tem algum exame ou laudo sobre o problema neurológico?",
    "👉 O médico indicou algum tratamento ou procedimento?",
    "👉 Você tem relatório médico explicando essa necessidade?",
    "👉 Você possui o comprovante de que está aguardando na fila?\n\nPode ser o print da tela do App Meu SUS Digital, o comprovante de agendamento da Secretaria de Saúde ou o papel da regulação (SISREG) com o número do seu protocolo."
]

PERGUNTAS_CARDIOLOGIA_SUS = [
    "Entendi... vamos ver isso com calma 💙.\n\n👉 Você consegue me explicar qual é o problema cardíaco ou o que o médico te disse?",
    "O seu caso envolve uma cirurgia de urgência (Ponte de safena, troca de válvula, marca-passo/Stent)?",
    "👉 Você tem algum exame ou laudo do coração? (Eletro, eco, cateterismo...)",
    "Quais sintomas você tem sentido? (Dor no peito, falta de ar, tontura, cansaço excessivo).",
    "👉 O médico indicou algum tratamento ou procedimento?",
    "👉 Você tem relatório médico explicando essa necessidade?",
    "👉 Você possui o comprovante de que está aguardando na fila?\n\nPode ser o print da tela do App Meu SUS Digital, o comprovante de agendamento da Secretaria de Saúde ou o papel da regulação (SISREG) com o número do seu protocolo."
]

PERGUNTAS_OUTROS_SUS = [
    "Entendi... como o seu caso é específico, eu preciso entender o que está acontecendo para te direcionar corretamente.\n\n👉 Poderia me dizer qual é a sua condição/doença?",
    "👉 Você já tem algum diagnóstico ou ainda está investigando?",
    "👉 Algum médico já te passou relatório ou pedido de tratamento?",
    "Vamos resolver isso juntos...\n\n👉 O médico comentou se existe urgência ou risco em não realizar esse tratamento?",
    "👉 O que acontece com a sua saúde se você não conseguir isso nos próximos 30 ou 90 dias? Existe risco de agravamento ou sequela irreversível?",
    "👉 Como essa situação tem afetado sua vida hoje?",
    "👉 Você possui o comprovante de que está aguardando na fila?\n\nPode ser o print da tela do App Meu SUS Digital, o comprovante de agendamento da Secretaria de Saúde ou o papel da regulação (SISREG) com o número do seu protocolo."
]

# Pós-perguntas SUS (cirurgia)
MSG_POS_PERGUNTAS_SUS = (
    "_{nome}_, recebi suas respostas aqui. O que mais me preocupa no seu caso é que o SUS "
    "trata essa situação como se pudesse esperar, mas juridicamente sabemos que o *tempo é o seu maior inimigo agora*.\n\n"
    "Você sente que, se não resolvermos isso nos próximos dias, a sua saúde corre um risco de piorar de forma irreversível?"
)

MSG_EXPLICACAO_SUS = (
    "Só pra te explicar de forma simples:\n\n"
    "Quando o paciente precisa de atendimento, exame ou tratamento e não consegue pelo SUS, "
    "a Justiça pode intervir pra garantir esse direito.\n\n"
    "Para resolver isso, eu trabalho com um *Protocolo de Liberação Urgente*. "
    "Buscamos a sua consulta/exame/cirurgia/tratamento com urgência para tirar você da fila e ter acesso ao seu diagnóstico com o médico especialista. "
    "Isso faria diferença na sua vida agora?"
)

MSG_HONORARIOS_SUS = (
    "Como é um trabalho de alta especialidade, o escritório cobra *Honorários Iniciais* "
    "para assumir o caso e entrar com um processo judicial. Prosseguir com esse caso faz sentido "
    "para você garantir sua saúde hoje e sair dessa espera?"
)

MSG_SIM_HONORARIOS_SUS_DECISAO = (
    "Antes de agendarmos: além de você, tem mais alguém que participe das decisões familiares ou financeiras, "
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
    "Para a Dra. Lethicia validar o seu protocolo de urgência, você possui o print do App Meu SUS Digital "
    "(ou o comprovante da fila de espera) e o Laudo Médico em mãos?"
)
MSG_SUS_CONSULTA_PROTOCOLO = (
    "Para resolver isso, eu trabalho com um *Protocolo de Liberação Urgente*. "
    "Buscamos a sua consulta/exame com urgência para tirar você da fila e ter acesso ao seu diagnóstico com o médico especialista. "
    "Isso faria diferença na sua vida agora?"
)

# --- FLUXO EXAME ---
MSG_SUS_EXAME_Q1 = "Entendi... vamos ver isso com calma 💙\n\n👉 Qual exame o médico solicitou pra você?"
MSG_SUS_EXAME_TIPO = (
    "Esse exame que você precisa é para qual finalidade principal?\n\n"
    "1️⃣ Diagnóstico: Para descobrir o que eu tenho.\n"
    "2️⃣ Pré-operatório: Para eu conseguir operar logo.\n"
    "3️⃣ Confirmação: O médico suspeita de cirurgia e precisa do exame para decidir."
)

# EXAME OPÇÃO 1 - Diagnóstico
PERGUNTAS_EXAME_DIAGNOSTICO = [
    "Entendi...\n\n👉 O médico comentou o que pode estar sendo investigado com esse exame? (se puder me explicar, ajuda muito)",
    "👉 O médico comentou se existe urgência ou risco em não realizar esse exame?",
    "👉 Você está aguardando há quanto tempo mais ou menos?",
    "Quem te pediu esse exame foi o médico especialista ou o médico do postinho/UBS?",
    "👉 Você recebeu algum comprovante do SUS? (Pode ser agendamento; protocolo; print do aplicativo meu SUS; posição na fila)"
]

# EXAME OPÇÃO 2 - Pré-operatório
PERGUNTAS_EXAME_PREOP = [
    "Perfeito...\n\n👉 Você já tem indicação de cirurgia e esse exame é pra poder realizar o procedimento, certo? Se quiser, pode me explicar melhor o que falta.",
    "👉 Você está aguardando há quanto tempo mais ou menos?",
    "Qual cirurgia que você precisa fazer?",
    "Quem te pediu esse exame foi o médico especialista ou o médico do postinho/UBS?",
    "Essa cirurgia ela é urgente ou não? Tem laudo médico atestando essa urgência?",
    "👉 Você recebeu algum comprovante do SUS? (Pode ser agendamento; protocolo; print do aplicativo meu SUS; posição na fila)"
]

# EXAME OPÇÃO 3 - Confirmação
PERGUNTAS_EXAME_CONFIRMACAO = [
    "Entendi...\n\n👉 O médico já suspeita que você pode precisar de qual tipo de cirurgia?",
    "Quais sintomas você apresentou pro médico pedir esse exame?",
    "👉 O médico comentou se existe urgência ou risco em não realizar esse exame?",
    "👉 Você está aguardando há quanto tempo mais ou menos?",
    "👉 Você recebeu algum comprovante do SUS? (Pode ser agendamento; protocolo; print do aplicativo meu SUS; posição na fila)"
]

MSG_SUS_EXAME_PITCH = (
    "No SUS, a demora para realizar um Exame muitas vezes é o que impede o médico de salvar um paciente a tempo.\n\n"
    "O Judiciário entende que o Estado não tem o direito de te deixar em uma fila infinita quando existe risco de agravamento. "
    "Você quer continuar contando com a sorte do sistema ou quer que a Dra. Lethicia force o governo a cumprir a lei agora?"
)

MSG_SUS_EXAME_PROTOCOLO = (
    "Para resolver isso, eu trabalho com um *Protocolo de Liberação Urgente*. "
    "Buscamos a sua consulta/exame com urgência para tirar você da fila e ter acesso ao seu diagnóstico com o médico especialista. "
    "Isso faria diferença na sua vida agora?"
)

# ============================================
# PLANO DE SAÚDE - MENSAGENS COMPLETAS
# ============================================

# NOVO: Pergunta sobre tipo de plano (pessoa física ou empresarial)
PS_TIPO_PLANO = "Seu plano é **pessoa física** ou **empresarial/CNPJ**?"

PS_TEMPO = "Você já tem seu plano de saúde há mais de 2 anos?"

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
PS_REP_Q2 = "👉 Você já chegou ou ainda falta pouco pro peso que gostaria?\n\n1️⃣ Já cheguei à minha meta\n2️⃣ Ainda não"

# NOVO: Mensagens educativas antes da oferta para quem ainda não chegou ao peso
PS_REP_NAO_PESO_EDU1 = (
    "Muitas pessoas acreditam que só têm direitos após perderem peso ou passarem pela cirurgia, mas a lei e o "
    "entendimento dos tribunais protegem você desde o primeiro passo da jornada. É fundamental entender agora o que "
    "o plano de saúde é obrigado a cobrir por lei e o que é considerado abusividade, para que você não seja pega de "
    "surpresa com negativas infundadas no futuro.\n\nVocê já tem clareza sobre quais cirurgias o plano é obrigado a "
    "custear no seu caso específico?"
)
PS_REP_NAO_PESO_EDU2 = (
    "Um ponto crucial que você precisa saber agora é a diferença jurídica entre um procedimento estético e um "
    "reparador. Mesmo que você ainda não esteja no peso ideal, o seu direito à saúde não pode ser limitado por "
    "critérios puramente comerciais das operadoras. Entender essa distinção agora evita que você aceite respostas "
    "negativas como se fossem definitivas.\n\nVocê gostaria de entender melhor como os tribunais interpretam o seu "
    "direito à cirurgia reparadora?"
)
PS_REP_NAO_PESO = (
    "Faz todo sentido querer entender bem a situação antes de tomar qualquer decisão.\n\n"
    "Para isso, ofereço uma consulta de orientação jurídica, onde você fala diretamente com a Dra., "
    "tira todas as suas dúvidas e entende com clareza quais são seus direitos e quais caminhos "
    "existem para o seu caso.\n\n"
    "💬 O valor da consulta é de *R$ 67,00* e é feita online, no horário que melhor funcionar pra você. "
    "E se durante ou depois da consulta você decidir que quer avançar com o acompanhamento jurídico "
    "completo, também é possível, mas é algo a alinharmos na hora da nossa reunião.\n\n"
    "Gostaria de agendar um horário com a Dra Lethicia ainda essa semana?"
)
PS_REP_NAO_PESO_PAGAMENTO = (
    f"Perfeito! Vamos reservar o seu horário.\n\n"
    f"Como deseja realizar o investimento do atendimento? Você prefere Pix ou Cartão de Crédito?"
)

PS_REP_EMPATIA = (
    "Eu entendo que essa pele que restou é o capítulo final de uma grande superação, mas ela também pode ser um peso físico e emocional. "
    "Para eu desenhar a melhor estratégia para você, me conte um pouco..."
)
PS_REP_Q3 = "👉 Esse excesso de pele hoje te causa dores, assaduras ou dermatites que não curam? E além do corpo, como isso tem afetado a sua autoestima e a sua liberdade de movimento no dia a dia?"
PS_REP_Q4 = "👉 Quais cirurgias reparadoras você teria interesse em fazer?"
# CORREÇÃO: removida a parte "e emitir os laudos"
PS_REP_Q5 = "Certo... Você já chegou a ir no médico cirurgião plástico pra solicitar as reparadoras?"

# CORREÇÃO: nova mensagem de acompanhamento para reparadora (substituindo a anterior)
PS_REP_ACOMPANHAMENTO = (
    "O meu papel aqui é garantir que você não dê nenhum passo no escuro e acabe fornecendo provas que o plano de "
    "saúde possa usar contra você no futuro. Preparar essa base documental agora é o que diferencia um processo "
    "rápido de uma batalha judicial desgastante.\n\nFaz sentido para você garantir essa segurança antes de qualquer "
    "negativa formal?"
)

# ============================================
# 2. NEGATIVA DE CIRURGIA - ESPECIALIDADES
# ============================================
PS_NEG_CIR_ESP = "Qual é o diagnóstico ou o tratamento específico que o plano está dificultando no momento?\n\n1️⃣ Endometriose\n2️⃣ Bariátrica\n3️⃣ Oncologia (câncer)\n4️⃣ Cardiologia (coração)\n5️⃣ Neurocirurgia\n6️⃣ Ortopedia\n7️⃣ Oftalmologia\n8️⃣ OUTRO"

# 2A. ENDOMETRIOSE
PS_ENDO_Q1 = "👉 Qual tipo de cirurgia foi indicada para o seu caso?"
PS_ENDO_Q2 = "Sinto muito que você esteja passando por isso. Sabemos que a endometriose não é 'só uma cólica', é algo que para a vida da mulher 💙\n\n👉 O plano negou formalmente ou simplesmente não respondeu?"
PS_ENDO_Q3 = "Sei o quanto a dor e a incerteza cansam, mas você merece viver com saúde e qualidade. Não é justo que a sua cirurgia seja negada depois de tanta espera. Vou te ajudar a destravar esse processo 💙\n\n👉 O plano justificou a negativa de alguma forma? (Ex: 'eletivo', 'sem cobertura', 'período de carência')"
PS_ENDO_Q4 = "👉 Você tem os exames que demonstram o seu diagnóstico?"
PS_ENDO_Q5 = "👉 Você já tentou resolver isso diretamente com o plano — ligação, protocolo, ouvidoria ou recurso formal?"

# 2B. BARIÁTRICA
PS_BARI_Q1 = "👉 Qual o seu IMC atual? Se não souber, pode me falar somente seu peso atual e sua altura"
PS_BARI_Q2 = "👉 Você tem comorbidades? (diabetes, hipertensão, apneia do sono, problemas nas articulações)"
# CORREÇÃO: Q3_MSG e Q3 devem ser enviadas juntas no fluxo sem esperar resposta
PS_BARI_Q3_MSG = "A cirurgia bariátrica nunca é apenas estética. É seu direito concluir esse ciclo com segurança e cobertura total pela operadora. Vou superar esses obstáculos contratuais para que seu procedimento seja autorizado 💙"
PS_BARI_Q3 = "👉 Fez o acompanhamento multidisciplinar exigido (nutricionista, psicólogo, endocrinologista)?"
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
PS_CARDIO_Q4 = "👉 Você já está internado aguardando o procedimento ou está em casa esperando a autorização para agendar?"
PS_CARDIO_Q5 = "👉 O procedimento foi considerado urgente?"
PS_CARDIO_Q6 = "👉 Você tem exames (ecocardiograma, cateterismo, ECG) que confirmam a necessidade cirúrgica?"

# 2E. NEUROCIRURGIA
PS_NEURO_Q1 = "👉 Qual procedimento neurocirúrgico foi indicado?"
PS_NEURO_Q2 = "👉 O paciente está internado ou com dor insuportável e precisa operar imediatamente?"
PS_NEURO_Q3 = "👉 O hospital onde seria realizada a cirurgia é da rede do plano?"
PS_NEURO_Q4 = "Sinto muito que você esteja passando por essa insegurança. Para eu desenhar a melhor estratégia jurídica, me conte:\n\n👉 Hoje, esse problema neurológico está afetando seus movimentos, causando perda de força ou dores que impedem você de realizar tarefas básicas?"
PS_NEURO_Q5 = "👉 A negativa foi por escrita ou verbal?"
PS_NEURO_Q6 = "👉 No seu caso o plano negou material cirúrgico ou alguma prótese?"
PS_NEURO_Q7 = "👉 Você tem exames de imagem — ressonância magnética, tomografia — que confirmam a necessidade cirúrgica?"

# 2F. ORTOPEDIA
PS_ORTO_Q1 = "👉 Qual cirurgia ortopédica foi indicada?"
PS_ORTO_Q2 = "👉 A condição está limitando sua mobilidade ou capacidade de trabalho?"
PS_ORTO_Q3 = "👉 O plano justificou a negativa de alguma forma? (Ex: 'eletivo', 'sem cobertura', 'período de carência')"
PS_ORTO_APOIO = "É muito comum os planos de saúde negarem tratamento com justificativas infundadas, ignorando a indicação do seu médico. Mas a lei é clara: quem decide o melhor pra você é ele, não o plano."
PS_ORTO_Q4 = "👉 No seu caso o plano negou material cirúrgico ou alguma prótese?"
PS_ORTO_Q5 = "👉 Essa negativa do plano foi por escrita ou verbal?"
PS_ORTO_Q6 = "👉 Você tem exames de imagem — ressonância magnética, tomografia — que confirmam a necessidade cirúrgica?"

# 2G. OFTALMOLOGIA
PS_OFTAL_Q1 = "👉 Qual cirurgia oftalmológica foi indicada?"
PS_OFTAL_Q2 = "👉 A condição está afetando sua visão de forma significativa?"
PS_OFTAL_Q3 = "👉 O médico indicou urgência, risco de perda de visão se não operar logo?"
PS_OFTAL_Q4 = "👉 O plano justificou a negativa de alguma forma? (Ex: 'eletivo', 'sem cobertura', 'período de carência')"
PS_OFTAL_Q5 = "👉 Essa negativa do plano foi por escrita ou verbal?"
PS_OFTAL_APOIO = "É muito comum os planos de saúde negarem tratamento com justificativas infundadas, ignorando a indicação do seu médico. Mas a lei é clara: quem decide o melhor pra você é ele, não o plano."

# 2H. OUTRO
PS_OUTRO_INTRO = "Entendido! Cada procedimento cirúrgico tem a sua importância e, se o seu médico indicou, é porque é necessário para a sua saúde. O plano não tem o direito de 'escolher' qual cirurgia você deve ou não fazer."
PS_OUTRO_Q1 = "👉 Qual cirurgia foi indicada pelo seu médico?"
PS_OUTRO_Q2 = "👉 Para qual problema ou doença ela foi recomendada?"
PS_OUTRO_Q3 = "👉 Você possui exames que comprovam a necessidade?"
PS_OUTRO_Q4 = "👉 A cirurgia foi negada?"
PS_OUTRO_APOIO = "É muito comum os planos de saúde negarem tratamento com justificativas infundadas, ignorando a indicação do seu médico. Mas a lei é clara: quem decide o melhor pra você é ele, não o plano."
PS_OUTRO_Q5 = "👉 O plano justificou a negativa de alguma forma? (Ex: 'eletivo', 'sem cobertura', 'período de carência')"
PS_OUTRO_Q6 = "👉 Essa negativa do plano foi por escrita ou verbal?"
PS_OUTRO_Q7 = "👉 Hoje, a falta dessa cirurgia te impede de trabalhar, de dormir bem ou de realizar suas atividades simples do dia a dia?"
PS_OUTRO_Q8 = "👉 Se você não realizar a cirurgia, pode ocorrer:\n\nDor intensa, Agravamento do problema, Risco à saúde ou Limitação no dia a dia?"
PS_OUTRO_Q9 = "👉 Você possui exames que comprovam a necessidade?"

# ============================================
# 3. MEDICAMENTO NEGADO
# ============================================
PS_MED_Q1  = "👉 Qual doença você está tratando?"
PS_MED_Q2  = "👉 Qual medicamento foi prescrito pelo médico?"
PS_MED_Q3  = "👉 O fornecimento do medicamento foi negado?"
PS_MED_Q4  = "Eu sei que cada dia sem a medicação gera uma ansiedade enorme, afinal, a sua saúde não pode esperar o tempo do plano.\n\n👉 Hoje, a falta desse medicamento já está afetando o controle da sua doença ou causando sintomas que impedem sua rotina?"
PS_MED_Q5  = "👉 Qual foi o motivo da negativa?"
PS_MED_Q6  = "👉 Essa negativa do plano foi por escrita ou verbal?"
PS_MED_Q7  = "Muitos pacientes desistem quando ouvem que o remédio 'não está no Rol' ou 'é domiciliar' ou 'experimental', mas a verdade é que a justiça entende que se o seu médico prescreveu, o plano é obrigado a fornecer."
PS_MED_Q8  = "👉 Você possui receita médica do medicamento?"
PS_MED_Q9  = "👉 Qual o valor aproximado do medicamento?"
PS_MED_Q10 = "👉 Você tem laudo médico explicando a necessidade do medicamento?"

# ============================================
# 4. EXAME NEGADO
# ============================================
PS_EXAME_Q1 = "👉 Qual exame foi solicitado pelo seu médico?"
PS_EXAME_Q2 = "👉 Para qual doença ou suspeita esse exame foi indicado?"
PS_EXAME_Q3 = "Sei o quão frustrante é ter um exame negado. Sem o exame, não há diagnóstico, e sem diagnóstico, não há tratamento. O plano não pode impedir a investigação da sua saúde."
PS_EXAME_Q4 = "👉 Você sente que essa demora do plano está prejudicando a sua saúde ou impedindo que você comece o tratamento que tanto precisa?"
PS_EXAME_Q5 = "👉 O que o seu médico lhe disse sobre a urgência deste resultado?"
PS_EXAME_Q6 = "👉 Qual foi o motivo da negativa?"
PS_EXAME_Q7 = "👉 Essa negativa do plano foi por escrita ou verbal?"

# ============================================
# 5. HOME CARE
# ============================================
PS_HOME_Q1 = "Sinto muito que você e sua família estejam passando por esse momento. Sabemos que o Home Care não é um 'luxo', mas a única forma de garantir dignidade, segurança e uma recuperação humanizada para quem você ama. 💙\n\n👉 Qual a doença ou condição do paciente?"
PS_HOME_Q2 = "👉 O paciente está acamado ou depende de cuidados constantes?"
PS_HOME_Q3 = "👉 O paciente já ficou internado recentemente?"
PS_HOME_Q4 = "Eu imagino o peso que está nos seus ombros agora. Cuidar de quem amamos exige muito, e sem a estrutura técnica correta, o medo de algo acontecer é constante.\n\n👉 Você sente que o plano de saúde está tentando transferir para a sua família uma responsabilidade médica que é deles?"
PS_HOME_Q5 = "👉 O home care foi negado?"
PS_HOME_Q6 = "👉 Você possui relatório médico detalhado?"
PS_HOME_Q7 = "👉 Está descrito o tipo de cuidado necessário (enfermagem, 24h, etc.)?"

# ============================================
# 6. TERAPIAS
# ============================================
PS_TERA_Q1 = "👉 O tratamento é para:\n\nAutismo (TEA), Desenvolvimento infantil, Reabilitação física, Saúde mental ou Outro?"
PS_TERA_Q2 = "👉 Quais terapias foram indicadas pelo médico?\n\nABA, Fisioterapia, Psicologia, Fonoaudiologia, Terapia ocupacional, Psicopedagogia, Musicoterapia ou Hidroterapia?"
PS_TERA_Q3 = "👉 Quantas sessões por semana foram indicadas?"
PS_TERA_Q4 = "Eu entendo que essa não é apenas uma briga por 'papéis', é uma briga pelo futuro e pela autonomia sua ou de quem você ama. 💙\n\n👉 Hoje, a falta dessas terapias ou a limitação das sessões tem causado retrocessos ou estagnado a evolução que você(s) tanto espera(m)?"
PS_TERA_Q5 = "👉 O que aconteceu?\n\nLimitou número de sessões, Negou totalmente, Não tem profissional disponível ou Outro?"
PS_TERA_Q6 = "👉 Você possui laudo médico com o diagnóstico?"
PS_TERA_Q7 = "👉 Essa negativa do plano foi por escrita ou verbal?"

# ============================================
# 7. REAJUSTE
# ============================================
PS_REAJ_Q1 = "Recebi seu contato e já quero te tranquilizar: você não precisa aceitar um reajuste que torna o seu plano de saúde impagável. Muitas vezes, esses aumentos são aplicados de forma ilegal para forçar o cancelamento do contrato, mas a justiça está aí para impedir isso. 💙\n\n👉 O plano é:\n\nIndividual/Familiar, Coletivo por adesão, Empresarial ou Não sei?"
PS_REAJ_Q2 = "👉 De quanto foi aproximadamente o aumento?\n\nAté 20%, De 20% a 50%, Mais de 50% ou Não sei?"
PS_REAJ_Q3 = "É muito frustrante ver o valor subir tanto, especialmente quando você sempre honrou com os pagamentos para garantir a sua segurança e a da sua família. 💙\n\n👉 Hoje, esse novo valor do boleto compromete a sua renda ou faz você considerar cancelar o plano?"
PS_REAJ_Q4 = "👉 Você (ou o titular) tem mais de 59 anos?"
PS_REAJ_Q5 = "👉 O aumento ocorreu após mudança de idade?"
PS_REAJ_Q6 = "👉 Você recebeu algum documento detalhando o aumento?"
PS_REAJ_Q7 = "👉 Esse plano foi feito por:\n\nEmpresa, Associação/sindicato ou Contratei sozinho?"
PS_REAJ_Q8 = "👉 Você possui o contrato do plano?"

# ============================================
# 8. COPARTICIPAÇÃO
# ============================================
PS_COPA_Q1 = "Recebi seu contato e já te adianto: a coparticipação não pode ser uma surpresa desagradável no seu boleto. Ela deve ser clara e, acima de tudo, dentro dos limites da lei. Ninguém deve ter medo de usar o plano por causa do valor das taxas. 💙\n\n👉 Você deixou de fazer exames ou tratamentos por causa da coparticipação?"
PS_COPA_Q2 = "É muito desgastante você pagar o plano em dia e, quando mais precisa dele, ser surpreendido com taxas que parecem uma segunda mensalidade.\n\n👉 Você sente que hoje está 'pagando para usar' o que já deveria estar coberto?"
PS_COPA_Q3 = "👉 A coparticipação foi cobrada em:\n\nConsultas, Exames, Terapias, Internação ou Outro?"
PS_COPA_Q4 = "👉 Você faz tratamento contínuo?"
PS_COPA_Q5 = "👉 Qual tipo de tratamento você faz?"
PS_COPA_Q6 = "Importante você saber: a coparticipação não pode ser ilimitada. A justiça entende que cobrar percentuais muito altos ou taxas sobre internação pode ser considerado abusivo, pois impede o paciente de se tratar."
PS_COPA_Q7 = "👉 Você possui o contrato do plano?"

# ============================================
# 9. ERRO MÉDICO
# ============================================
PS_ERRO_Q1 = "Sinto muito que você esteja passando por isso. Sei que, além da dor física, existe uma quebra de confiança muito grande quando algo não sai como o esperado em um procedimento médico. Estou aqui para te ouvir e entender se houve uma falha que te dá direito à reparação. 💙\n\n👉 O que aconteceu durante o atendimento médico?\n\nCirurgia, Atendimento de emergência, Tratamento contínuo, Parto ou Outro?"
PS_ERRO_Q2 = "👉 O paciente sofreu algum dano?\n\nAgravamento da saúde, Sequela, Dor intensa, Novo procedimento necessário ou Óbito?"
PS_ERRO_Q3 = "Eu imagino o quanto esse momento está sendo difícil para você e para sua família. Para que eu possa desenhar a melhor estratégia:\n\n👉 Como esse episódio mudou a sua vida hoje?"
PS_ERRO_Q4 = "👉 Você possui prontuário médico?"
PS_ERRO_Q5 = "👉 Outro médico já disse que houve erro ou falha no atendimento?"
PS_ERRO_Q6 = "👉 Você sente que houve falta de informação, descaso ou uma falha clara na técnica do médico ou do hospital?"

# ============================================
# 10. OUTRO (plano)
# ============================================
PS_OUTRO_DEMANDA_Q1 = "Entendido! O Direito da Saúde é muito amplo e, se o seu problema envolve o seu bem-estar ou o seu contrato de saúde, você está no lugar certo. 💙\n\nPara que eu possa entender como te ajudar, me conte brevemente o que está acontecendo. O plano de saúde negou algo?"
PS_OUTRO_DEMANDA_Q2 = "👉 Existe algum prazo ou data limite que te preocupa agora (ex: uma cirurgia marcada, um boleto vencendo ou um prazo de defesa)?"
PS_OUTRO_DEMANDA_Q3 = "👉 Você recebeu alguma negativa ou teve dificuldade no atendimento?"
PS_OUTRO_DEMANDA_Q4 = "👉 Você tem isso registrado (mensagem, documento, protocolo)?"
PS_OUTRO_DEMANDA_Q5 = "👉 Você possui documentos relacionados ao caso?"
PS_OUTRO_DEMANDA_Q6 = "👉 Esse problema está afetando sua saúde atualmente?"
PS_OUTRO_DEMANDA_Q7 = "Certo, recebi seus detalhes. Independentemente do caso, a minha premissa é sempre a mesma: o contrato de saúde deve servir para proteger a vida e o consumidor, não para criar barreiras."

# ============================================
# CAMINHO NÃO (menos de 2 anos)
# ============================================
PS_NAO_2ANOS_EDUCACAO = (
    "Entendo! Muitas pessoas acreditam que precisam esperar 2 anos para ter direito a cirurgias ou tratamentos complexos, "
    "mas a lei nem sempre funciona assim. Existem situações onde o plano é obrigado a cobrir o seu procedimento mesmo que você "
    "tenha poucos meses de contrato, especialmente se houver urgência ou se a doença não foi declarada por má-fé."
)
PS_NAO_2ANOS_Q1       = "👉 Me conta, qual o tratamento que você precisa fazer?"
PS_NAO_2ANOS_Q2       = "👉 No seu caso, o médico comentou se isso é urgente ou pode trazer algum risco se não for feito?"
PS_NAO_2ANOS_FEEDBACK = "Perfeito, isso é importante! 👊 SE HÁ URGÊNCIA, o plano já deveria cobrir normalmente esse tipo de situação. Mesmo assim, eles podem acabar negando indevidamente em alguns casos."
PS_NAO_2ANOS_Q3       = "👉 O médico indicou que o tratamento é urgente?"
PS_NAO_2ANOS_Q4       = "👉 Você já sabia dessa doença antes de contratar o plano?"
PS_NAO_2ANOS_Q5       = "👉 O plano negou alegando carência?"
PS_NAO_2ANOS_Q6       = "👉 Você tem a negativa por escrito?"

# ============================================
# PÓS-PERGUNTAS PLANO (PS_POS_BUSCA)
# ============================================

# NOVO: Mensagem de ponto crítico antes do PS_POS_BUSCA
def MSG_PONTO_CRITICO(situacao_nome: str) -> str:
    return (
        f"Com base no que você me relatou, o seu caso é uma prioridade, especialmente por envolver "
        f"**{situacao_nome}**. Pela minha experiência em Direito da Saúde, vejo que temos fundamentos sólidos "
        f"para agir, pois o contrato deve proteger sua vida e não criar barreiras desnecessárias."
    )

PS_POS_BUSCA = (
    "Obrigado por todas as informações. Já consigo ter um bom entendimento da sua situação.\n\n"
    "Agora me diz: o que você está buscando nesse momento? Escolha a opção que mais se encaixa com onde você está agora:\n\n"
    "1️⃣ Quero entender se o plano de saúde é obrigado a cobrir determinado tratamento ou Tenho uma dúvida específica ou um caso diferente e gostaria de orientação jurídica para entender quais são meus direitos e possibilidades.\n\n"
    "2️⃣ Já tenho a negativa do plano: Desejo orientação especializada para ingressar com a ação judicial e buscar a liberação do meu tratamento.\n\n"
    "3️⃣ Ainda não tenho a negativa, mas preciso me preparar: Quero me antecipar, eu ainda não recebi a negativa do plano, mas sei que meu pedido pode ser recusado. Quero me preparar da forma correta, com orientação jurídica, para aumentar minhas chances de aprovação do tratamento ou sucesso na ação judicial.\n\n"
    "4️⃣ Preciso de uma consultoria jurídica: Desejo uma análise técnica sobre o meu caso de saúde. Indicado para dúvidas sobre reajustes abusivos (anual ou por faixa etária), períodos de carência, migração de plano (portabilidade) ou para saber se um tratamento específico tem cobertura obrigatória pela ANS."
)

# Opção 1
PS_OP1_PERGUNTA = (
    "Perfeito! Para esse tipo de dúvida pontual, oferecemos o Atendimento Expresso. "
    "Diferente da consultoria completa, aqui você envia sua dúvida e um especialista te responde de forma técnica e direta, "
    "analisando se o seu direito é garantido por lei. Isso te ajudaria?"
)
PS_OP1_DETALHES = (
    "O investimento no atendimento particular é de R$ 97,00 e é feito online.\n\n"
    "É um atendimento individual e aprofundado onde você terá os seguintes benefícios:\n\n"
    "• **Resposta Técnica Direta:** Esclarecimento sobre a obrigatoriedade de cobertura (Rol da ANS e entendimentos judiciais recentes).\n"
    "• **Análise de Viabilidade:** Uma opinião profissional sobre se o seu caso tem chances reais de sucesso na justiça ou se é uma questão administrativa.\n"
    "• **Indicação de Documentos:** Lista do que você precisa providenciar imediatamente para não perder seus direitos.\n\n"
    "Podemos marcar um horário pra você na agenda da Dra Lethicia?"
)
PS_OP1_PAGAMENTO = (
    f"Perfeito! Vamos reservar o seu horário.\n\n"
    f"**Passo 1:** Escolha o melhor dia e hora no link abaixo:\n🔗 {CALENDLY_LINK}\n\n"
    f"**Passo 2:** Após escolher o horário, realize o pagamento da consultoria. Como deseja realizar o investimento? Você prefere Pix ou Cartão de Crédito?"
)
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
PS_OP3_DECISAO_INTRO = (
    "Perfeito. O próximo passo agora é uma reunião rápida para a Dra Lethicia te explicar como funciona o processo e valores de honorários.\n\n"
    "Antes de agendarmos: além de você, tem mais alguém que participe das decisões familiares ou financeiras, "
    "como seu esposo/esposa, que seria importante estar presente para já tirarmos todas as dúvidas de uma vez?"
)

# Opção 4 — NOVO: duas mensagens antes da oferta de consultoria
PS_OP4_EDU1 = (
    "Entender os seus direitos é o primeiro passo para não se tornar refém das decisões unilaterais dos planos de saúde. "
    "Muitas vezes, as operadoras impõem negativas de tratamentos, exames e cirurgias, ou aplicam reajustes e carências que "
    "parecem definitivos, mas que, na verdade, ferem as normas da ANS e a legislação vigente.\n\n"
    "Você sente que o plano de saúde está sendo realmente transparente com você sobre as coberturas e regras do seu contrato?"
)
PS_OP4_EDU2 = (
    "Cada contrato de saúde possui cláusulas específicas e, quase sempre, as respostas que o SAC do plano te dá não condizem "
    "com o que a Justiça e a lei determinam para o seu caso. Uma análise técnica detalhada serve para identificar exatamente "
    "onde o seu direito está sendo violado, seja na negativa de uma cirurgia, no fornecimento de medicação de alto custo, em "
    "reajustes desproporcionais ou na limitação de terapias essenciais. É a única forma de você agir com segurança, parando de "
    "aceitar o 'não' da operadora e passando a utilizar o embasamento jurídico correto.\n\n"
    "Gostaria de uma análise profissional para o seu caso específico?"
)
# ATUALIZADO: texto da consultoria com duração 2h
PS_OP4_PERGUNTA = (
    "Entendido. Para casos de análise contratual, reajustes abusivos ou orientações preventivas, o próximo passo é a nossa "
    "Consultoria Jurídica Especializada.\n\n"
    "Nesta reunião online, um advogado especialista em Direito da Saúde analisará detalhadamente o seu contrato e documentos "
    "para entregar um parecer técnico definitivo sobre os seus direitos, evitando que você tome decisões baseadas em "
    "informações incompletas.\n\n"
    "**Informações sobre a Consultoria:**\n"
    "• Objetivo: Diagnóstico completo e construção da estratégia jurídica personalizada.\n"
    "• Duração: Até 2 horas de atendimento exclusivo.\n"
    "• Investimento: R$ 500,00 (análise técnica especializada e reserva de horário).\n\n"
    "Deseja garantir sua segurança jurídica e prosseguir com o agendamento?"
)
PS_OP4_PAGAMENTO = (
    f"Perfeito! Vamos reservar o seu horário.\n\n"
    f"**Passo 1:** Escolha o melhor dia e hora no link abaixo:\n🔗 {CALENDLY_LINK}\n\n"
    f"**Passo 2:** Após escolher o horário, realize o pagamento da consultoria. Como deseja realizar o investimento? Você prefere Pix ou Cartão de Crédito?"
)
PS_OP4_CONFIRMACAO = "Ao realizar o pagamento e for dado baixa no nosso financeiro, alguém da nossa equipe vai entrar em contato o quanto antes pra marcar seu atendimento na agenda da Dra Lethicia."

# Encerramento geral
PS_ENCERRAMENTO = (
    "Entendo perfeitamente e respeito sua decisão.\n\n"
    "Vou encerrar o seu atendimento por aqui para priorizar os casos que já estão com liminares em andamento. "
    "Lembre-se apenas que, no Direito da Saúde, o tempo é um fator determinante para o sucesso do tratamento.\n\n"
    "Caso precise de suporte especializado no futuro, nossos canais continuam à disposição."
)

# Encerramento para opção 4 quando não
PS_ENCERRAMENTO_OP4_NAO = (
    "Entendo perfeitamente e respeito sua decisão. "
    "Vou encerrar o seu atendimento por aqui para priorizar os casos que já estão com procedimentos em andamento. "
    "Lembre-se apenas que, no Direito da Saúde, o tempo é um fator determinante para o sucesso do tratamento. "
    "Caso precise de suporte especializado no futuro, nossos canais continuam à disposição."
)

# Decisão compartilhada
DECISAO_SIM = (
    "Excelente! É fundamental que ele(a) participe, pois como o Direito à Saúde envolve "
    "prazos muito curtos e decisões imediatas sobre o tratamento, é bom que todos "
    "estejam na mesma página.\n\n"
    f"Vamos escolher um horário que fique confortável para vocês dois... "
    f"Logo abaixo vou te mandar a agenda da {L}, e você marque o dia e horário "
    "que fica melhor pra ambos.\n\n"
    f"🔗 {CALENDLY_LINK}"
)
DECISAO_NAO = (
    "Perfeito, facilita bastante o nosso fluxo. Como você é a única responsável pela decisão, "
    "conseguimos dar um andamento mais ágil aos trabalhos...\n\n"
    f"Logo abaixo vou te mandar a agenda da {L}, e você marque o dia e horário "
    "que fica melhor pra você.\n\n"
    f"🔗 {CALENDLY_LINK}"
)
# CORREÇÃO: "ele" → "ele(a)"
DECISAO_REPASSE = (
    "Entendo! Olha, eu sugiro fortemente que ele(a) tente participar, nem que seja apenas "
    "nos primeiros 10 minutos. No Direito à Saúde, os detalhes técnicos sobre a negativa da operadora "
    "costumam gerar muitas dúvidas e, se ele ouvir direto de mim, vocês ganham muito mais segurança para decidir rápido.\n\n"
    "Conseguimos um horário em que ele(a) possa entrar na chamada, ou prefere manter só entre nós por enquanto?"
)
DECISAO_REPASSE_SIM = f"Perfeito! Vamos agendar para vocês dois. Logo abaixo vou te mandar a agenda da {L}.\n\n🔗 {CALENDLY_LINK}"
DECISAO_REPASSE_NAO = f"Entendido! Mantemos só entre nós. Logo abaixo vou te mandar a agenda da {L}.\n\n🔗 {CALENDLY_LINK}"


# ============================================
# HELPER: detectar pergunta sobre valores
# ============================================
def _e_pergunta_valor(r: str) -> bool:
    palavras = ["valor", "quanto", "preço", "custa", "honorário", "investimento", "cobram", "custo"]
    return any(p in _n(r) for p in palavras)

def _msg_valor():
    dados = st.session_state.dados
    situacao = _n(dados.get("situacao", ""))
    canal = _n(dados.get("canal", ""))
    if "reajuste" in situacao or "coparticipação" in situacao or "copa" in situacao:
        return MSG_VALORES_REAJUSTE
    if "exame" in situacao or "consulta" in situacao or canal == "sus_consulta" or canal == "sus_exame":
        return MSG_VALORES_CONSULTA
    return MSG_VALORES_CIRURGIA


# ============================================
# HELPER: enviar ponto crítico + POS_BUSCA
# ============================================
def _enviar_pos_busca():
    """Envia a mensagem de ponto crítico + a mensagem POS_BUSCA."""
    situacao_raw = st.session_state.dados.get("situacao", "")
    situacao_nome = _situacao_nome(situacao_raw)
    add_bot(MSG_PONTO_CRITICO(situacao_nome))
    add_bot(PS_POS_BUSCA)
    st.session_state.estado = "PS_POS_BUSCA"


# ============================================
# PROCESSAMENTO DO FLUXO
# ============================================

def processar(resposta: str):
    estado = st.session_state.estado
    dados  = st.session_state.dados

    # Interceptar perguntas de valor em qualquer estado (exceto INICIO/FIM)
    if estado not in ("INICIO", "FIM") and _e_pergunta_valor(resposta):
        msg_val = _msg_valor()
        add_bot(msg_val)
        # Para as mensagens de valores cirurgia e reajuste, que terminam com pergunta,
        # esperamos Sim/Não mas não mudamos de estado — apenas enviamos a mensagem e seguimos
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
            # NOVO: primeiro pergunta tipo de plano
            st.session_state.estado = "PS_TIPO_PLANO"
            add_bot(PS_TIPO_PLANO)

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
        st.session_state.estado = "SUS_CONSULTA_PROTOCOLO"
        add_bot(MSG_SUS_CONSULTA_PROTOCOLO)
    elif estado == "SUS_CONSULTA_PROTOCOLO":
        if _sim(resposta):
            add_bot("Ótimo. Isso mostra que você prioriza sua saúde acima da burocracia do Estado.\n\nVou encaminhar seus dados para a mesa da Dra. Lethicia neste momento. Em instantes, ela entrará em contato aqui por este chat para te passar a estratégia de liberação e os valores para o seu caso. Fique atento(a)!")
        else:
            add_bot(MSG_ENCERRAMENTO_SUS)
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
            add_bot("Ótimo. Isso mostra que você prioriza sua saúde acima da burocracia do Estado.\n\nVou encaminhar seus dados para a mesa da Dra. Lethicia neste momento. Em instantes, ela entrará em contato aqui por este chat para te passar a estratégia de liberação e os valores para o seu caso. Fique atento(a)!")
        else:
            add_bot(MSG_ENCERRAMENTO_SUS)
        st.session_state.estado = "FIM"

    # ---- SUS CIRURGIA ----
    elif estado == "SUS_ESPECIALIDADE":
        if "oncologia" in _n(resposta) or "1" in resposta:
            st.session_state.perguntas_ativas = PERGUNTAS_ONCOLOGIA.copy()
        elif "neuro" in _n(resposta) and ("tea" in _n(resposta) or "tdah" in _n(resposta) or "diverg" in _n(resposta) or "2" in resposta):
            st.session_state.perguntas_ativas = PERGUNTAS_NEURO.copy()
        elif "endometriose" in _n(resposta) or "adenomiose" in _n(resposta) or "3" in resposta:
            st.session_state.perguntas_ativas = PERGUNTAS_ENDOMETRIOSE.copy()
        elif "medicamento" in _n(resposta) or "4" in resposta:
            st.session_state.perguntas_ativas = PERGUNTAS_MEDICAMENTO_SUS.copy()
        elif "bariátrica" in _n(resposta) or "bariatrica" in _n(resposta) or "5" in resposta:
            st.session_state.perguntas_ativas = PERGUNTAS_BARIATRICA_SUS.copy()
        elif "neurologia" in _n(resposta) or "neurocirurgia" in _n(resposta) or "6" in resposta:
            st.session_state.perguntas_ativas = PERGUNTAS_NEUROLOGIA_SUS.copy()
        elif "cardiologia" in _n(resposta) or "7" in resposta:
            st.session_state.perguntas_ativas = PERGUNTAS_CARDIOLOGIA_SUS.copy()
        else:
            st.session_state.perguntas_ativas = PERGUNTAS_OUTROS_SUS.copy()

        dados["especialidade"] = resposta
        st.session_state.pergunta_idx = 0
        st.session_state.estado = "SUS_PERGUNTAS"
        add_bot(st.session_state.perguntas_ativas[0])

    elif estado == "SUS_PERGUNTAS":
        idx = st.session_state.pergunta_idx
        dados[f"resp_{idx}"] = resposta
        idx += 1
        st.session_state.pergunta_idx = idx
        if idx < len(st.session_state.perguntas_ativas):
            add_bot(st.session_state.perguntas_ativas[idx])
        else:
            st.session_state.estado = "POS_PERGUNTAS_SUS"
            add_bot(MSG_POS_PERGUNTAS_SUS.replace("{nome}", st.session_state.nome or ""))

    elif estado == "POS_PERGUNTAS_SUS":
        dados["sentimento"] = resposta
        st.session_state.estado = "PROPOSTA_SUS"
        add_bot(MSG_EXPLICACAO_SUS)

    elif estado == "PROPOSTA_SUS":
        if _sim(resposta):
            st.session_state.estado = "HONORARIOS_SUS"
            add_bot(MSG_HONORARIOS_SUS)
        else:
            add_bot(MSG_ENCERRAMENTO_SUS)
            st.session_state.estado = "FIM"

    elif estado == "HONORARIOS_SUS":
        if _sim(resposta):
            st.session_state.estado = "DECISAO_COMPARTILHADA"
            add_bot(MSG_SIM_HONORARIOS_SUS_DECISAO)
        else:
            add_bot(MSG_ENCERRAMENTO_SUS)
            st.session_state.estado = "FIM"

    # =====================================================================
    # PLANO DE SAÚDE
    # =====================================================================

    # NOVO: tipo de plano
    elif estado == "PS_TIPO_PLANO":
        dados["tipo_plano"] = resposta
        if "empresa" in _n(resposta) or "cnpj" in _n(resposta) or "empresarial" in _n(resposta):
            # Empresarial vai direto para situação (sem perguntar 2 anos)
            dados["plano_2anos"] = "empresarial"
            st.session_state.estado = "PS_SITUACAO"
            add_bot(PS_SITUACAO)
        else:
            # Pessoa física → pergunta dos 2 anos
            st.session_state.estado = "PS_TEMPO"
            add_bot(PS_TEMPO)

    elif estado == "PS_TEMPO":
        if _sim(resposta):
            dados["plano_2anos"] = "sim"
            st.session_state.estado = "PS_SITUACAO"
            add_bot(PS_SITUACAO)
        else:
            dados["plano_2anos"] = "nao"
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
        _enviar_pos_busca()

    # Caminho SIM - Situação
    elif estado == "PS_SITUACAO":
        dados["situacao"] = resposta

        if "reparadora" in _n(resposta) or "1" in resposta:
            st.session_state.estado = "PS_REP_Q1"
            add_bot(PS_REP_Q1)

        elif "negativa" in _n(resposta) or "2" in resposta:
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
                PS_EXAME_Q1, PS_EXAME_Q2, PS_EXAME_Q3, PS_EXAME_Q4,
                PS_EXAME_Q5, PS_EXAME_Q6, PS_EXAME_Q7
            ]
            st.session_state.pergunta_idx = 0
            st.session_state.estado = "PS_PERGUNTAS_COLETOR"
            add_bot(PS_EXAME_Q1)

        elif "home" in _n(resposta) or "5" in resposta:
            st.session_state.perguntas_ativas = [
                PS_HOME_Q1, PS_HOME_Q2, PS_HOME_Q3, PS_HOME_Q4,
                PS_HOME_Q5, PS_HOME_Q6, PS_HOME_Q7
            ]
            st.session_state.pergunta_idx = 0
            st.session_state.estado = "PS_PERGUNTAS_COLETOR"
            add_bot(PS_HOME_Q1)

        elif "terapia" in _n(resposta) or "6" in resposta:
            st.session_state.perguntas_ativas = [
                PS_TERA_Q1, PS_TERA_Q2, PS_TERA_Q3, PS_TERA_Q4,
                PS_TERA_Q5, PS_TERA_Q6, PS_TERA_Q7
            ]
            st.session_state.pergunta_idx = 0
            st.session_state.estado = "PS_PERGUNTAS_COLETOR"
            add_bot(PS_TERA_Q1)

        elif "reajuste" in _n(resposta) or "7" in resposta:
            st.session_state.perguntas_ativas = [
                PS_REAJ_Q1, PS_REAJ_Q2, PS_REAJ_Q3, PS_REAJ_Q4,
                PS_REAJ_Q5, PS_REAJ_Q6, PS_REAJ_Q7, PS_REAJ_Q8
            ]
            st.session_state.pergunta_idx = 0
            st.session_state.estado = "PS_PERGUNTAS_COLETOR"
            add_bot(PS_REAJ_Q1)

        elif "copart" in _n(resposta) or "copa" in _n(resposta) or "8" in resposta:
            st.session_state.perguntas_ativas = [
                PS_COPA_Q1, PS_COPA_Q2, PS_COPA_Q3, PS_COPA_Q4,
                PS_COPA_Q5, PS_COPA_Q6, PS_COPA_Q7
            ]
            st.session_state.pergunta_idx = 0
            st.session_state.estado = "PS_PERGUNTAS_COLETOR"
            add_bot(PS_COPA_Q1)

        elif "erro" in _n(resposta) or "9" in resposta:
            st.session_state.perguntas_ativas = [
                PS_ERRO_Q1, PS_ERRO_Q2, PS_ERRO_Q3,
                PS_ERRO_Q4, PS_ERRO_Q5, PS_ERRO_Q6
            ]
            st.session_state.pergunta_idx = 0
            st.session_state.estado = "PS_PERGUNTAS_COLETOR"
            add_bot(PS_ERRO_Q1)

        else:  # OUTRO (10 ou qualquer outro)
            st.session_state.perguntas_ativas = [
                PS_OUTRO_DEMANDA_Q1, PS_OUTRO_DEMANDA_Q2, PS_OUTRO_DEMANDA_Q3,
                PS_OUTRO_DEMANDA_Q4, PS_OUTRO_DEMANDA_Q5, PS_OUTRO_DEMANDA_Q6,
                PS_OUTRO_DEMANDA_Q7
            ]
            st.session_state.pergunta_idx = 0
            st.session_state.estado = "PS_PERGUNTAS_COLETOR"
            add_bot(PS_OUTRO_DEMANDA_Q1)

    # Coletor genérico
    elif estado == "PS_PERGUNTAS_COLETOR":
        idx = st.session_state.pergunta_idx
        dados[f"resp_{idx}"] = resposta
        idx += 1
        st.session_state.pergunta_idx = idx
        if idx < len(st.session_state.perguntas_ativas):
            add_bot(st.session_state.perguntas_ativas[idx])
        else:
            _enviar_pos_busca()

    # ---- REPARADORA ----
    elif estado == "PS_REP_Q1":
        dados["rep_q1"] = resposta
        st.session_state.estado = "PS_REP_Q2"
        add_bot(PS_REP_Q2)
    elif estado == "PS_REP_Q2":
        if "ainda" in _n(resposta) or "2" in resposta:
            # NOVO: duas mensagens educativas antes da oferta
            st.session_state.estado = "PS_REP_NAO_PESO_EDU1"
            add_bot(PS_REP_NAO_PESO_EDU1)
        else:
            st.session_state.estado = "PS_REP_EMPATIA"
            add_bot(PS_REP_EMPATIA)

    # Fluxo educativo reparadora (ainda não chegou ao peso)
    elif estado == "PS_REP_NAO_PESO_EDU1":
        # Independente da resposta (Sim ou Não) avança para segunda mensagem educativa
        st.session_state.estado = "PS_REP_NAO_PESO_EDU2"
        add_bot(PS_REP_NAO_PESO_EDU2)
    elif estado == "PS_REP_NAO_PESO_EDU2":
        # Independente da resposta avança para oferta
        st.session_state.estado = "PS_REP_NAO_PESO"
        add_bot(PS_REP_NAO_PESO)
    elif estado == "PS_REP_NAO_PESO":
        if _sim(resposta):
            st.session_state.estado = "PS_REP_NAO_PESO_PAGAMENTO"
            add_bot(PS_REP_NAO_PESO_PAGAMENTO)
        else:
            add_bot(PS_ENCERRAMENTO)
            st.session_state.estado = "FIM"
    elif estado == "PS_REP_NAO_PESO_PAGAMENTO":
        if "cartão" in _n(resposta) or "cartao" in _n(resposta):
            add_bot(f"✅ Aqui está o link para pagamento via **Cartão de Crédito**:\n\n{LINK_CARTAO_97}\n\n{PS_OP1_CONFIRMACAO}")
            st.session_state.estado = "FIM"
        elif "pix" in _n(resposta):
            add_bot(f"✅ Aqui está o link para pagamento via **Pix**:\n\n{LINK_PIX_97}\n\n{PS_OP1_CONFIRMACAO}")
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
        if _sim(resposta) or "sentido" in _n(resposta) or "certeza" in _n(resposta):
            _enviar_pos_busca()
        else:
            add_bot(PS_ENCERRAMENTO)
            st.session_state.estado = "FIM"

    # ---- NEGATIVA DE CIRURGIA ----
    elif estado == "PS_NEG_CIR_ESP":
        dados["neg_cir_esp"] = resposta

        if "endometriose" in _n(resposta) or "1" in resposta:
            st.session_state.perguntas_ativas = [PS_ENDO_Q1, PS_ENDO_Q2, PS_ENDO_Q3, PS_ENDO_Q4, PS_ENDO_Q5]
        elif "bariátrica" in _n(resposta) or "bariatrica" in _n(resposta) or "2" in resposta:
            # CORREÇÃO: bariátrica envia Q3_MSG e Q3 juntos (sem esperar resposta)
            # Implementado com uma pergunta combinada
            st.session_state.perguntas_ativas = [
                PS_BARI_Q1, PS_BARI_Q2,
                PS_BARI_Q3_MSG + "\n\n" + PS_BARI_Q3,  # juntas numa só mensagem
                PS_BARI_Q4, PS_BARI_Q5, PS_BARI_Q6
            ]
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
        else:
            st.session_state.perguntas_ativas = [
                PS_OUTRO_INTRO, PS_OUTRO_Q1, PS_OUTRO_Q2, PS_OUTRO_Q3, PS_OUTRO_Q4,
                PS_OUTRO_APOIO, PS_OUTRO_Q5, PS_OUTRO_Q6, PS_OUTRO_Q7, PS_OUTRO_Q8, PS_OUTRO_Q9
            ]

        st.session_state.pergunta_idx = 0
        st.session_state.estado = "PS_PERGUNTAS_COLETOR"
        add_bot(st.session_state.perguntas_ativas[0])

    # ---- POS BUSCA (opções 1-4) ----
    elif estado == "PS_POS_BUSCA":
        if "1" in resposta:
            st.session_state.estado = "PS_OP1_PERGUNTA"
            add_bot(PS_OP1_PERGUNTA)
        elif "2" in resposta:
            st.session_state.estado = "DECISAO_COMPARTILHADA"
            add_bot(PS_OP2_PERGUNTA)
        elif "3" in resposta:
            st.session_state.estado = "PS_OP3_PERGUNTA"
            add_bot(PS_OP3_PERGUNTA)
        elif "4" in resposta:
            # NOVO: duas mensagens educativas antes da oferta
            st.session_state.estado = "PS_OP4_EDU1"
            add_bot(PS_OP4_EDU1)
        else:
            add_bot(PS_POS_BUSCA)

    # Opção 1
    elif estado == "PS_OP1_PERGUNTA":
        if _sim(resposta):
            st.session_state.estado = "PS_OP1_DETALHES"
            add_bot(PS_OP1_DETALHES)
        else:
            add_bot(PS_ENCERRAMENTO)
            st.session_state.estado = "FIM"
    elif estado == "PS_OP1_DETALHES":
        if _sim(resposta):
            st.session_state.estado = "PS_OP1_PAGAMENTO"
            add_bot(PS_OP1_PAGAMENTO)
        else:
            add_bot(PS_ENCERRAMENTO)
            st.session_state.estado = "FIM"
    elif estado == "PS_OP1_PAGAMENTO":
        if "cartão" in _n(resposta) or "cartao" in _n(resposta):
            add_bot(f"✅ Aqui está o link para pagamento via **Cartão de Crédito**:\n\n{LINK_CARTAO_97}\n\n{PS_OP1_CONFIRMACAO}")
            st.session_state.estado = "FIM"
        elif "pix" in _n(resposta):
            add_bot(f"✅ Aqui está o link para pagamento via **Pix**:\n\n{LINK_PIX_97}\n\n{PS_OP1_CONFIRMACAO}")
            st.session_state.estado = "FIM"

    # Opção 3
    elif estado == "PS_OP3_PERGUNTA":
        st.session_state.estado = "PS_OP3_PERMISSAO"
        add_bot(PS_OP3_PERMISSAO)
    elif estado == "PS_OP3_PERMISSAO":
        if "acompanhamento" in _n(resposta) or "quer" in _n(resposta) or "dra" in _n(resposta) or _sim(resposta):
            st.session_state.estado = "DECISAO_COMPARTILHADA"
            add_bot(PS_OP3_DECISAO_INTRO)
        else:
            # CORREÇÃO: quando tenta sozinho → encerramento
            add_bot(PS_ENCERRAMENTO)
            st.session_state.estado = "FIM"

    # Opção 4 — fluxo com duas mensagens educativas
    elif estado == "PS_OP4_EDU1":
        # Independente de Sim ou Não, avança para segunda mensagem educativa
        st.session_state.estado = "PS_OP4_EDU2"
        add_bot(PS_OP4_EDU2)
    elif estado == "PS_OP4_EDU2":
        if _sim(resposta):
            st.session_state.estado = "PS_OP4_PERGUNTA"
            add_bot(PS_OP4_PERGUNTA)
        else:
            add_bot(PS_ENCERRAMENTO_OP4_NAO)
            st.session_state.estado = "FIM"
    elif estado == "PS_OP4_PERGUNTA":
        if _sim(resposta):
            st.session_state.estado = "PS_OP4_PAGAMENTO"
            add_bot(PS_OP4_PAGAMENTO)
        else:
            add_bot(PS_ENCERRAMENTO_OP4_NAO)
            st.session_state.estado = "FIM"
    elif estado == "PS_OP4_PAGAMENTO":
        if "cartão" in _n(resposta) or "cartao" in _n(resposta):
            add_bot(f"✅ Aqui está o link para pagamento via **Cartão de Crédito**:\n\n{LINK_CARTAO_500}\n\n{PS_OP4_CONFIRMACAO}")
            st.session_state.estado = "FIM"
        elif "pix" in _n(resposta):
            add_bot(f"✅ Aqui está o link para pagamento via **Pix**:\n\n{LINK_PIX_500}\n\n{PS_OP4_CONFIRMACAO}")
            st.session_state.estado = "FIM"

    # ---- DECISÃO COMPARTILHADA ----
    elif estado == "DECISAO_COMPARTILHADA":
        n = _n(resposta)
        if "sozinho" in n or "sozinha" in n or "não" in n or "nao" in n:
            add_bot(DECISAO_NAO)
            st.session_state.estado = "FIM"
        elif "repasse" in n or "passo" in n or "falar" in n or "3" in resposta:
            add_bot(DECISAO_REPASSE)
            st.session_state.estado = "DECISAO_REPASSE_RESPOSTA"
        else:
            add_bot(DECISAO_SIM)
            st.session_state.estado = "FIM"

    elif estado == "DECISAO_REPASSE_RESPOSTA":
        if _sim(resposta) or "com ele" in _n(resposta):
            add_bot(DECISAO_REPASSE_SIM)
        else:
            add_bot(DECISAO_REPASSE_NAO)
        st.session_state.estado = "FIM"

    elif estado == "FIM":
        pass


# ============================================
# INTERFACE STREAMLIT
# ============================================

def main():
    st.title("⚖️ Iara Bot - Assistente Jurídica em Direito da Saúde")
    st.caption(f"Especialista: {L} | Atendimento: SUS, Planos de Saúde")

    init_session()

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

        user_input = st.text_input(
            "Digite sua mensagem:",
            key="user_input",
            placeholder="Digite aqui sua resposta..."
        )

        if st.button("📤 Enviar", use_container_width=True) and user_input:
            add_user(user_input)
            processar(user_input)
            st.rerun()

    # ---- BOTÕES CONTEXTUAIS ----
    with col2:
        estado = st.session_state.estado

        def btn(label, valor=None):
            v = valor or label
            if st.button(label, use_container_width=True):
                add_user(v)
                processar(v)
                st.rerun()

        if estado == "CANAL":
            btn("🏥 SUS", "SUS")
            btn("📋 Plano de Saúde", "Plano de Saúde")

        # NOVO: tipo de plano
        elif estado == "PS_TIPO_PLANO":
            btn("👤 Pessoa Física", "Pessoa Física")
            btn("🏢 Empresarial/CNPJ", "Empresarial")

        elif estado == "SUS_DEMANDA":
            btn("🔪 Cirurgia / Tratamento", "Cirurgia")
            btn("📋 Consultas / Exames", "Consultas")

        elif estado == "SUS_CONSULTA_EXAME_TIPO":
            btn("Consulta com especialista", "1")
            btn("Realização de Exame", "2")

        elif estado == "SUS_CONSULTA_PITCH":
            btn("⏳ Quero aguardar", "aguardar")
            btn("💙 Quero ajuda da Dra. Lethicia", "quero ajuda")

        elif estado == "SUS_CONSULTA_AJUDA_Q3":
            btn("✅ Sim", "Sim")
            btn("❌ Não", "Não")
            btn("➖ Não se aplica", "Não se aplica")

        elif estado == "SUS_CONSULTA_AJUDA_Q4":
            btn("✅ Sim, tenho os documentos.", "Sim")
            btn("⚠️ Tenho apenas o pedido médico.", "Tenho pedido")
            btn("❌ Não tenho comprovante da fila.", "Não tenho")

        elif estado == "SUS_CONSULTA_PROTOCOLO":
            btn("✅ SIM", "SIM")
            btn("❌ NÃO", "NÃO")

        elif estado == "SUS_EXAME_TIPO":
            btn("Diagnóstico", "1")
            btn("Pré-operatório", "2")
            btn("Confirmação", "3")

        elif estado == "SUS_EXAME_PITCH":
            btn("⏳ Quero aguardar", "aguardar")
            btn("💙 Quero ajuda da Dra. Lethicia", "quero ajuda")

        elif estado == "SUS_EXAME_PROTOCOLO":
            btn("✅ SIM", "SIM")
            btn("❌ NÃO", "NÃO")

        elif estado == "SUS_ESPECIALIDADE":
            for esp in ["Oncologia", "Neurodivergências (TEA, TDAH)", "Endometriose / Adenomiose",
                        "Medicamento", "Bariátrica", "Neurologia / Neurocirurgia", "Cardiologia", "Outros"]:
                btn(esp)

        elif estado in ("POS_PERGUNTAS_SUS", "PROPOSTA_SUS"):
            btn("✅ SIM", "SIM")
            btn("❌ NÃO", "NÃO")

        elif estado == "HONORARIOS_SUS":
            btn("✅ SIM", "SIM")
            btn("❌ NÃO", "NÃO")

        elif estado == "PS_TEMPO":
            btn("Sim", "Sim")
            btn("Não", "Não")

        elif estado == "PS_SITUACAO":
            opcoes = [
                ("Reparadora", "1"),
                ("Negativa de cirurgia", "2"),
                ("Medicamento negado", "3"),
                ("Exame negado", "4"),
                ("Home care", "5"),
                ("Terapias", "6"),
                ("Reajuste", "7"),
                ("Coparticipação elevada", "8"),
                ("Erro médico", "9"),
                ("OUTRO", "10"),
            ]
            for label, val in opcoes:
                btn(label, val)

        elif estado == "PS_REP_Q2":
            btn("Já cheguei à minha meta", "1")
            btn("Ainda não", "2")

        # NOVO: botões para mensagens educativas reparadora
        elif estado == "PS_REP_NAO_PESO_EDU1":
            btn("Sim", "Sim")
            btn("Não", "Não")

        elif estado == "PS_REP_NAO_PESO_EDU2":
            btn("Sim", "Sim")
            btn("Não", "Não")

        elif estado == "PS_REP_NAO_PESO":
            btn("✅ Sim", "Sim")
            btn("❌ Não", "Não")

        # NOVO: botões de pagamento reparadora não chegou ao peso
        elif estado == "PS_REP_NAO_PESO_PAGAMENTO":
            btn("💳 Cartão de Crédito", "cartão")
            btn("📱 Pix", "pix")

        elif estado == "PS_REP_Q5":
            btn("✅ Sim", "Sim")
            btn("❌ Não", "Não")

        # CORREÇÃO: botões para nova mensagem de acompanhamento reparadora
        elif estado == "PS_REP_ACOMPANHAMENTO":
            btn("✅ Sim, faz sentido!", "Sim")
            btn("Com certeza!", "com certeza")
            btn("❌ Não agora", "não")

        elif estado == "PS_NEG_CIR_ESP":
            for label, val in [
                ("Endometriose", "1"),
                ("Bariátrica", "2"),
                ("Oncologia (câncer)", "3"),
                ("Cardiologia", "4"),
                ("Neurocirurgia", "5"),
                ("Ortopedia", "6"),
                ("Oftalmologia", "7"),
                ("OUTRO", "8"),
            ]:
                btn(label, val)

        elif estado == "PS_PERGUNTAS_COLETOR":
            idx = st.session_state.pergunta_idx
            perguntas = st.session_state.perguntas_ativas
            if idx < len(perguntas):
                pergunta_atual = perguntas[idx]
                # Botões contextuais por pergunta
                # Medicamento Q3: fornecimento negado
                if pergunta_atual == PS_MED_Q3:
                    btn("Sim", "Sim")
                    btn("Não", "Não")
                    btn("Ainda não solicitei", "Ainda não solicitei")
                # Medicamento Q5: motivo da negativa
                elif pergunta_atual == PS_MED_Q5:
                    btn("Fora do rol da ANS", "Fora do rol da ANS")
                    btn("Alto custo", "Alto custo")
                    btn("Uso domiciliar", "Uso domiciliar")
                    btn("Experimental/off-label", "Experimental/off-label")
                    btn("Outro", "Outro")
                # Medicamento Q8: possui receita
                elif pergunta_atual == PS_MED_Q8:
                    btn("Sim", "Sim")
                    btn("Não", "Não")
                # Medicamento Q10: laudo médico
                elif pergunta_atual == PS_MED_Q10:
                    btn("Sim", "Sim")
                    btn("Não", "Não")
                # Negativa escrita ou verbal (detecta por conteúdo da pergunta)
                elif "escrita ou verbal" in pergunta_atual.lower():
                    btn("Escrita", "Escrita")
                    btn("Verbal", "Verbal")
                    btn("Não tive a negativa ainda", "Não tive a negativa ainda")
                # Exame negado Q6: motivo
                elif pergunta_atual == PS_EXAME_Q6:
                    btn("Fora do rol da ANS", "Fora do rol da ANS")
                    btn("Não atende diretriz (DUT)", "Não atende diretriz (DUT)")
                    btn("Carência", "Carência")
                    btn("Não é urgente", "Não é urgente")
                    btn("Experimental", "Experimental")
                    btn("Outro", "Outro")
                # Home care Q5: negado
                elif pergunta_atual == PS_HOME_Q5:
                    btn("Sim", "Sim")
                    btn("Não", "Não")
                    btn("Ainda não solicitei", "Ainda não solicitei")
                # Home care Q6 e Q7: Sim/Não
                elif pergunta_atual in (PS_HOME_Q6, PS_HOME_Q7):
                    btn("Sim", "Sim")
                    btn("Não", "Não")
                # Cardiologia Q4: internado ou em casa
                elif pergunta_atual == PS_CARDIO_Q4:
                    btn("Já estou internado", "Já estou internado")
                    btn("Estou em casa esperando", "Estou em casa esperando")
                # Cardiologia Q5: urgente
                elif pergunta_atual == PS_CARDIO_Q5:
                    btn("Sim", "Sim")
                    btn("Não", "Não")
                # Neuro Q2: internado/dor
                elif pergunta_atual == PS_NEURO_Q2:
                    btn("Sim", "Sim")
                    btn("Não", "Não")
                # Neuro Q3: rede do plano
                elif pergunta_atual == PS_NEURO_Q3:
                    btn("Sim", "Sim")
                    btn("Não", "Não")
                    btn("Não sei", "Não sei")
                # Ortopedia Q2: mobilidade
                elif pergunta_atual == PS_ORTO_Q2:
                    btn("Sim, de forma significativa", "Sim, de forma significativa")
                    btn("Parcialmente", "Parcialmente")
                    btn("Ainda consigo me movimentar", "Ainda consigo me movimentar")
                # Oftalmologia Q2: visão
                elif pergunta_atual == PS_OFTAL_Q2:
                    btn("Sim, visão muito comprometida", "Sim, visão muito comprometida")
                    btn("Está piorando progressivamente", "Está piorando progressivamente")
                    btn("Ainda consigo enxergar razoavelmente", "Ainda consigo enxergar razoavelmente")
                # Oftalmologia Q3: urgência
                elif pergunta_atual == PS_OFTAL_Q3:
                    btn("Sim, há urgência no laudo", "Sim, há urgência no laudo")
                    btn("O médico disse verbalmente", "O médico disse verbalmente")
                    btn("Não há urgência indicada", "Não há urgência indicada")
                # Outro Q3 e Q9: exames
                elif pergunta_atual in (PS_OUTRO_Q3, PS_OUTRO_Q9):
                    btn("Sim", "Sim")
                    btn("Não", "Não")
                # Outro Q4: cirurgia negada
                elif pergunta_atual == PS_OUTRO_Q4:
                    btn("Sim", "Sim")
                    btn("Não", "Não")
                    btn("Ainda não solicitei", "Ainda não solicitei")
                # Outro demanda Q3 e Q4: sim/não/não se encaixa
                elif pergunta_atual in (PS_OUTRO_DEMANDA_Q3, PS_OUTRO_DEMANDA_Q4):
                    btn("Sim", "Sim")
                    btn("Não", "Não")
                    btn("Não se encaixa", "Não se encaixa")
                # Outro demanda Q5 e Q6: sim/não
                elif pergunta_atual in (PS_OUTRO_DEMANDA_Q5, PS_OUTRO_DEMANDA_Q6):
                    btn("Sim", "Sim")
                    btn("Não", "Não")
                # Erro Q4 e Q5: possui prontuário / outro médico disse
                elif pergunta_atual in (PS_ERRO_Q4, PS_ERRO_Q5):
                    btn("Sim", "Sim")
                    btn("Não", "Não")
                # Copa Q1 e Q4: sim/não
                elif pergunta_atual in (PS_COPA_Q1, PS_COPA_Q4):
                    btn("Sim", "Sim")
                    btn("Não", "Não")
                # Reajuste Q4 e Q5 e Q6: sim/não
                elif pergunta_atual in (PS_REAJ_Q4, PS_REAJ_Q5, PS_REAJ_Q6, PS_REAJ_Q8):
                    btn("Sim", "Sim")
                    btn("Não", "Não")
                # Bariátrica Q3 combinada (acompanhamento multidisciplinar)
                elif "acompanhamento multidisciplinar" in pergunta_atual.lower():
                    btn("Sim", "Sim")
                    btn("Não", "Não")
                # Terapia Q6: laudo
                elif pergunta_atual == PS_TERA_Q6:
                    btn("Sim", "Sim")
                    btn("Não", "Não")
                # Genérico sim/não para demais
                elif any(p in pergunta_atual.lower() for p in ["possui", "tem ", "você já", "está descrito", "já está"]):
                    btn("Sim", "Sim")
                    btn("Não", "Não")

        elif estado in ("PS_OP1_PERGUNTA", "PS_OP1_DETALHES"):
            btn("✅ SIM", "SIM")
            btn("❌ NÃO", "NÃO")

        elif estado in ("PS_OP1_PAGAMENTO", "PS_OP4_PAGAMENTO", "PS_REP_NAO_PESO_PAGAMENTO"):
            btn("💳 Cartão de Crédito", "cartão")
            btn("📱 Pix", "pix")

        elif estado == "PS_POS_BUSCA":
            btn("Entender meus direitos", "1")
            btn("Já tenho a negativa", "2")
            btn("Me preparar antes da negativa", "3")
            btn("Consultoria jurídica", "4")

        elif estado == "PS_OP3_PERMISSAO":
            btn("💙 Quero acompanhamento da Dra.", "quero acompanhamento")
            btn("👤 Quero tentar sozinho(a)", "quero tentar sozinho")

        # NOVO: botões para mensagens educativas opção 4
        elif estado == "PS_OP4_EDU1":
            btn("Sim", "Sim")
            btn("Não", "Não")

        elif estado == "PS_OP4_EDU2":
            btn("✅ Sim, quero a análise", "Sim")
            btn("❌ Não agora", "Não")

        elif estado == "PS_OP4_PERGUNTA":
            btn("✅ SIM", "SIM")
            btn("❌ NÃO", "NÃO")

        elif estado == "DECISAO_COMPARTILHADA":
            btn("Sim, meu cônjuge/familiar", "sim")
            btn("Não, eu decido sozinho(a)", "sozinho")
            btn("Tem, mas pode falar comigo", "repasse")

        elif estado == "DECISAO_REPASSE_RESPOSTA":
            btn("Com ele(a)", "com ele")
            btn("Entre nós", "não")

        # NAO 2 ANOS botões
        elif estado == "PS_NAO_2ANOS_Q3":
            btn("Sim", "Sim")
            btn("Não", "Não")

        elif estado == "PS_NAO_2ANOS_Q4":
            btn("Sim", "Sim")
            btn("Não", "Não")
            btn("Descobri depois", "Descobri depois")

        elif estado == "PS_NAO_2ANOS_Q5":
            btn("Sim", "Sim")
            btn("Não", "Não")

        elif estado == "PS_NAO_2ANOS_Q6":
            btn("Sim", "Sim")
            btn("Não", "Não")

    if not st.session_state.messages:
        add_bot(MSG_BOAS_VINDAS)
        st.rerun()


if __name__ == "__main__":
    main()
