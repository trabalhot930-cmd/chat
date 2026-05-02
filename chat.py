"""
Iara Bot - Assistente Jurídica em Direito da Saúde
FLUXO EXATAMENTE IGUAL ÀS IMAGENS ENVIADAS
Versão standalone para Streamlit
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
# MENSAGENS PRINCIPAIS (CONFORME IMAGENS)
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
# PERGUNTAS ONCOLOGIA
# ============================================
PERGUNTAS_ONCOLOGIA = [
    "Entendi… vamos cuidar disso juntos 🚨\n\n👉 Você consegue me contar qual é o tipo de câncer?",
    "👉 Você está aguardando atendimento ou tratamento pelo SUS? Se sim, há quanto tempo mais ou menos?",
    "Só pra eu entender melhor seu caso:\n\n👉 O diagnóstico já foi confirmado por biópsia? E você tem esse laudo em mãos?",
    "Entendi…\n\n👉 Você já foi encaminhado para um hospital especializado em câncer (oncologia) pelo SUS ou ainda nem conseguiu passar com um especialista?\n\nInfelizmente, a fila do SUS não respeita o avanço da doença. Se o hospital não iniciou seu tratamento em 60 dias, a lei está sendo descumprida e precisamos forçar o início imediato via Justiça.",
    "👉 Você possui um relatório médico explicando o tratamento que precisa fazer? (se quiser, pode enviar aqui também 😊)",
    "Última perguntinha, que é bem importante:\n\n👉 O médico falou se o seu caso é urgente?",
    "👉 Você possui o comprovante de que está aguardando na fila?\n\nPode ser o print da tela do App Meu SUS Digital, o comprovante de agendamento da Secretaria de Saúde ou o papel da regulação (SISREG) com o número do seu protocolo."
]

# ============================================
# PERGUNTAS NEURODIVERGÊNCIAS
# ============================================
PERGUNTAS_NEURO = [
    "Entendi… pode ficar tranquilo(a), vou te ajudar com isso 🚨\n\nCasos assim realmente precisam de atenção, principalmente por envolver desenvolvimento.\n\n👉 Me conta: já tem diagnóstico fechado ou ainda está em investigação?",
    "👉 Você tem algum laudo ou relatório médico com o diagnóstico?",
    "Entendo as batalhas diárias que você enfrenta para garantir o melhor para quem você ama. Nenhuma criança deve ter seu desenvolvimento barrado por limites impostos pelo plano. Estou aqui para lutar ao seu lado e garantir todas as terapias que são de direito.\n\nAgora me conta uma coisa importante:\n\n👉 Quais terapias o médico indicou?",
    "E hoje, como está essa situação no SUS?\n\n👉 Você conseguiu iniciar as terapias ou ainda está aguardando?",
    "Essa parte é muito importante:\n\n👉 O médico comentou algo sobre prejuízo no desenvolvimento ou necessidade de iniciar rápido as terapias?",
    "Se você puder me contar:\n\n👉 Como essa situação está impactando o dia a dia de vocês?",
    "👉 Você possui o comprovante de que está aguardando na fila?\n\nPode ser o print da tela do App Meu SUS Digital, o comprovante de agendamento da Secretaria de Saúde ou o papel da regulação (SISREG) com o número do seu protocolo."
]

# ============================================
# PERGUNTAS ENDOMETRIOSE
# ============================================
PERGUNTAS_ENDOMETRIOSE = [
    "Entendi… imagino o quanto isso pode estar sendo difícil pra você 😊\nMas fica tranquila, vou te ajudar com isso 😊\n\n👉 Você já tem diagnóstico confirmado de endometriose ou adenomiose?",
    "Obrigado por me contar 😊\n\n👉 Esse diagnóstico foi feito por exame? Se ainda não fez, qual exame está aguardando?",
    "Sei o quanto a dor e a incerteza cansam, mas você merece viver com saúde e qualidade. Eu também tenho endo e sei que todo dia é uma luta. Não é justo que a sua cirurgia ou exame continue demorando assim. Vou te ajudar a destravar esse processo para que você receba o cuidado que precisa.\n\nQuero entender melhor sua situação:\n\n👉 Você sente dores fortes ou crises que atrapalham sua rotina?",
    "Agora uma parte bem importante:\n\n👉 O médico indicou algum tratamento específico?\n\n(ex: cirurgia de videolaparoscopia, medicamento, acompanhamento…)",
    "👉 Você tem relatório médico explicando esse tratamento?\n\nSe puder enviar, ajuda muito na análise 😉",
    "👉 Você está aguardando há quanto tempo mais ou menos?",
    "👉 O médico colocou em relatório ou te informou se existe risco de piora ou agravamento sem o tratamento?",
    "👉 Você possui o comprovante de que está aguardando na fila?\n\nPode ser o print da tela do App Meu SUS Digital, o comprovante de agendamento da Secretaria de Saúde ou o papel da regulação (SISREG) com o número do seu protocolo."
]

# ============================================
# PERGUNTAS MEDICAMENTO
# ============================================
PERGUNTAS_MEDICAMENTO = [
    "Entendi… vamos ver isso com calma 😊\n\n👉 Qual foi o medicamento que o médico indicou pra você?",
    "Perfeito, obrigado por me explicar 😊\n\n👉 Você tem a receita ou relatório médico desse medicamento?",
    "Entendo a frustração de ter um direito negado justamente quando você mais precisa de suporte. Analisaremos seu caso para garantir que a lei seja cumprida e o acesso à saúde seja imediato. Conte conosco para transformar essa negativa em uma solução rápida e segura.\n\nAo te passar esse medicamento o seu médico escreveu no laudo que este remédio específico é o único que pode tratar seu caso agora e que a interrupção trará riscos à sua vida ou saúde?",
    "Essa parte é bem importante:\n\n👉 Você já utilizou outros medicamentos antes? Se sim, eles não tiveram resultado ou causaram algum problema?",
    "👉 Você chegou a solicitar esse medicamento pelo SUS ou farmácia de alto custo? O que te informaram?\n\n(foi negado, está em análise, falta no estoque… pode me explicar melhor)",
    "👉 O médico comentou o que pode acontecer se você não usar esse medicamento?\n\n(se puder me explicar, isso ajuda muito)"
]

# ============================================
# PERGUNTAS BARIÁTRICA
# ============================================
PERGUNTAS_BARIATRICA = [
    "Entendi… vamos ver isso com calma 😊\n\n👉 Você já tem indicação médica para cirurgia bariátrica?",
    "👉 Você possui outras doenças agravadas pelo peso, como Diabetes, Hipertensão, Apneia do Sono ou problemas graves nas articulações?",
    "👉 Você tem algum laudo ou relatório médico indicando a cirurgia?\n\nSe puder enviar aqui, já me ajuda bastante 😊",
    "Só pra eu entender melhor seu caso:\n\n👉 Você sabe me informar seu peso e altura?\n(se não souber exato, pode ser aproximado)",
    "Essa parte é bem importante:\n\n👉 Você já tentou outros tratamentos antes, como dieta, acompanhamento ou medicamentos? Como foi essa experiência?",
    "👉 Você já está na fila de espera do SUS há quanto tempo?",
    "👉 Você possui o comprovante de que está aguardando na fila?\n\nPode ser o print da tela do App Meu SUS Digital, o comprovante de agendamento da Secretaria de Saúde ou o papel da regulação (SISREG) com o número do seu protocolo."
]

# ============================================
# PERGUNTAS REPARADORA
# ============================================
PERGUNTAS_REPARADORA = [
    "👉 Você passou por cirurgia bariátrica ou teve uma grande perda de peso (canetas, dieta e treino)? (se quiser, pode me contar um pouco da sua história)",
    "Agora quero entender melhor sua situação:\n\n👉 O excesso de pele ou condição tem causado algum problema? (ex: dor, assaduras, infecções, dificuldade de movimentação…)",
    "👉 Você já teve a oportunidade de passar pelo cirurgião plástico?",
    "👉 Algum médico já te deu um relatório solicitando essa cirurgia? (se puder me explicar ou enviar o relatório, ajuda muito 😊)",
    "👉 Você está aguardando há quanto tempo mais ou menos?",
    "👉 Você possui o comprovante de que está aguardando na fila?\n\nPode ser o print da tela do App Meu SUS Digital, o comprovante de agendamento da Secretaria de Saúde ou o papel da regulação (SISREG) com o número do seu protocolo."
]

# ============================================
# PERGUNTAS NEUROLOGIA
# ============================================
PERGUNTAS_NEUROLOGIA = [
    "Entendi… vamos ver isso com calma 😊\n\n👉 Você consegue me explicar qual é o problema neurológico ou diagnóstico?",
    "Obrigado por me explicar 😊\n\n👉 Você tem algum laudo ou exame com esse diagnóstico? (se puder enviar aqui, ajuda bastante 😊)",
    "Sei que o momento é de muita angústia e que cada minuto de espera parece uma eternidade. Vou agir com a rapidez que o caso pede para que o hospital libere logo o necessário. Minha prioridade é tirar esse peso das suas costas e proteger a vida de quem você ama.\n\nGostaria de saber qual cirurgia especificamente você está aguardando. Você pode me dizer?",
    "👉 O médico especialista (Neuro) ou outro médico já emitiu laudo dizendo que a demora pode causar um dano irreversível da sua condição?",
    "👉 Você está aguardando atendimento, exame ou cirurgia? Há quanto tempo mais ou menos?",
    "👉 Você já possui o comprovante de que está aguardando na fila?\n\nPode ser o print da tela do App Meu SUS Digital, o comprovante de agendamento da Secretaria de Saúde ou o papel da regulação (SISREG) com o número do seu protocolo."
]

# ============================================
# PERGUNTAS CARDIOLOGIA
# ============================================
PERGUNTAS_CARDIOLOGIA = [
    "Entendi… vamos ver isso com calma 😊\n\n👉 Você consegue me explicar qual é o problema cardíaco ou o que o médico te disse?",
    "👉 O seu caso envolve uma cirurgia de urgência (como ponte de safena ou troca de válvula), a colocação de um Marca-passo/Stent?",
    "Obrigado por me explicar 😊\n\n👉 Você tem algum exame ou laudo do coração? (ex: eletro, ecocardiograma, cateterismo… se puder enviar 😊)",
    "Sei que o momento é de muita angústia e que cada minuto de espera parece uma eternidade. Vou agir com a rapidez que o caso pede para que o hospital libere logo o necessário. Minha prioridade é tirar esse peso das suas costas e proteger a vida de quem você ama.\n\n👉 Você tem sentido algum desses sintomas?\n\n• Dor no peito\n• Falta de ar\n• Tontura ou desmaio\n• Cansaço excessivo\n\nSe tiver outros, pode me contar também.",
    "👉 O médico indicou algum tratamento ou procedimento? (ex: cirurgia, cateterismo, marcapasso, acompanhamento…)",
    "👉 Você tem relatório médico explicando essa necessidade? (se puder enviar, ajuda muito na análise 😊)",
    "👉 Você já possui o comprovante de que está aguardando na fila?\n\nPode ser o print da tela do App Meu SUS Digital, o comprovante de agendamento da Secretaria de Saúde ou o papel da regulação (SISREG) com o número do seu protocolo."
]

# ============================================
# PERGUNTAS OUTROS SUS
# ============================================
PERGUNTAS_OUTROS = [
    "Entendi. Como o seu caso é específico, eu preciso entender o que está acontecendo para te direcionar corretamente.\n\nPoderia me dizer qual é a sua condição/doença?",
    "Só pra eu entender melhor:\n\n👉 Você já tem algum diagnóstico ou ainda está investigando?",
    "👉 Algum médico já te passou relatório ou pedido de tratamento? Se tiver, pode me enviar aqui 😊",
    "É muito difícil precisar de um atendimento e receber um 'não' como resposta. Não desanime; estamos aqui justamente para transformar essa negativa em um 'sim'. Vamos resolver isso juntos para que você tenha seu tratamento garantido o quanto antes.\n\n👉 O médico comentou se existe urgência ou risco em não realizar esse tratamento?",
    "Recebido. Deixa eu te perguntar algo fundamental: o que acontece com a sua saúde se você não conseguir isso nos próximos 30 ou 90 dias? Existe risco de agravamento ou de uma sequela que não poderá ser revertida depois?",
    "👉 Como essa situação tem afetado sua vida hoje?",
    "👉 Você possui o comprovante de que está aguardando na fila?\n\nPode ser o print da tela do App Meu SUS Digital, o comprovante de agendamento da Secretaria de Saúde ou o papel da regulação (SISREG) com o número do seu protocolo."
]

# ============================================
# PERGUNTAS CONSULTA SUS
# ============================================
PERGUNTAS_CONSULTA = [
    "Entendi que você está aguardando uma consulta especializada. Deixa eu te perguntar: você já está nessa fila de espera há mais de 30 dias ou o seu caso tem um prazo de urgência que o SUS simplesmente ignorou?",
    "👉 Qual especialidade médica você está aguardando?",
    "👉 Você tem encaminhamento ou pedido médico pra essa consulta?\n\nMuitas vezes o SUS nega a consulta dizendo que não tem o especialista, mas a lei é clara: se o governo não tem o médico, ele é obrigado a pagar uma consulta particular para você. A espera na fila da regulação não pode ser eterna, principalmente quando há dor ou risco de sequela.\n\nO Judiciário entende que o Estado não tem o direito de te deixar em uma fila infinita quando existe risco de agravamento.",
    "👉 Está aguardando há quanto tempo mais ou menos?",
    "👉 O que te informaram quando você questionou sua posição na fila ou quando você foi tentar marcar?\n\n(fila, falta de médico, sem previsão…)",
    "👉 Você teria algum exame informando a condição de saúde que tem?",
    "Para a Dra. Lethicia validar o seu protocolo de urgência, você possui o print do App Meu SUS Digital (ou o comprovante da fila de espera) e o Laudo Médico em mãos?"
]

# ============================================
# PERGUNTAS EXAME SUS
# ============================================
PERGUNTAS_EXAME = [
    "Entendi… vamos ver isso com calma 😊\n\n👉 Qual exame o médico solicitou pra você?",
    "Esse exame que você precisa é para qual finalidade principal?\n\n1. Diagnóstico: Para descobrir o que eu tenho.\n2. Pré-operatório: Para eu conseguir operar logo.\n3. Confirmação: O médico suspeita de cirurgia e precisa do exame para decidir.",
]

PERGUNTAS_EXAME_DIAG = [
    "Entendi… 👉 o médico comentou o que pode estar sendo investigado com esse exame? (se puder me explicar, ajuda muito)",
    "👉 o médico comentou se existe urgência ou risco em não realizar esse exame?",
    "👉 você está aguardando há quanto tempo mais ou menos?",
    "👉 Quem te pediu esse exame foi o médico especialista ou o médico do postinho/UBS?",
    "👉 você recebeu algum comprovante do SUS?\n\n(Pode ser agendamento; protocolo; print do aplicativo meu SUS; posição na fila)"
]

PERGUNTAS_EXAME_PREOP = [
    "Perfeito… 👉 você já tem indicação de cirurgia e esse exame é pra poder realizar o procedimento, certo? Se quiser, pode me explicar melhor o que falta.",
    "👉 você está aguardando há quanto tempo mais ou menos?",
    "👉 Qual cirurgia que você precisa fazer?",
    "👉 Quem te pediu esse exame foi o médico especialista ou o médico do postinho/UBS?",
    "👉 Essa cirurgia ela é urgente ou não? Tem laudo médico atestando essa urgência?",
    "👉 você recebeu algum comprovante do SUS?\n\n(Pode ser agendamento; protocolo; print do aplicativo meu SUS; posição na fila)"
]

PERGUNTAS_EXAME_CONF = [
    "Entendi… 👉 o médico já suspeita que você pode precisar de qual tipo de cirurgia?",
    "👉 Quais sintomas você apresentou pro médico pedir esse exame?",
    "👉 o médico comentou se existe urgência ou risco em não realizar esse exame?",
    "👉 você está aguardando há quanto tempo mais ou menos?",
    "👉 você recebeu algum comprovante do SUS?\n\n(Pode ser agendamento; protocolo; print do aplicativo meu SUS; posição na fila)"
]

# ============================================
# PÓS PERGUNTAS SUS
# ============================================
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
    "Buscamos a sua consulta/exame/cirurgia/tratamento com urgência para tirar você da fila. "
    "Isso faria diferença na sua vida agora?"
)

MSG_HONORARIOS = (
    "Como é um trabalho de alta especialidade, o escritório cobra *Honorários Iniciais* "
    "para assumir o caso e protocolar o pedido de liminar.\n\n"
    "Prosseguir com esse caso faz sentido para você garantir sua saúde hoje e sair dessa espera?"
)

MSG_SIM = (
    "Ótimo. Isso mostra que você prioriza sua saúde acima da burocracia do Estado. 💙\n\n"
    "Vou encaminhar seus dados para a mesa da Dra. Lethicia neste momento. "
    "Em instantes, ela entrará em contato aqui por este chat para te passar "
    "a estratégia de liberação e os valores para o seu caso.\n\n"
    "Fique atento(a)! 👀"
)

MSG_NAO = (
    "Compreendo. Infelizmente, sem o interesse em avançar com uma medida judicial, "
    "o seu caso continuará dependendo exclusivamente da velocidade da fila do SUS, "
    "que como sabemos, não tem previsão.\n\n"
    "Como o escritório da Dra. Lethicia foca apenas em quem deseja forçar a solução imediata, "
    "estamos encerrando seu atendimento por aqui.\n\n"
    "Caso a sua situação se agrave ou você decida que não pode mais esperar, "
    "sinta-se à vontade para retornar. Desejamos sorte no seu tratamento. 🙏"
)

# ============================================
# PLANO DE SAÚDE - MENSAGENS (CONFORME IMAGENS)
# ============================================

# PS: Reparadora
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
PS_REP_Q3 = "Eu entendo que essa pele que restou é o capítulo final de uma grande superação, mas ela também pode ser um peso físico e emocional. Para eu desenhar a melhor estratégia para você, me conte um pouco…"
PS_REP_Q4 = "Esse excesso de pele hoje te causa dores, assaduras ou dermatites que não curam? E além do corpo, como isso tem afetado a sua autoestima e a sua liberdade de movimento no dia a dia?"
PS_REP_Q5 = "👉 Quais cirurgias reparadoras você teria interesse em fazer?"
PS_REP_Q6 = "Certo… Você já chegou a ir no médico cirurgião plástico pra solicitar as reparadoras e emitir os laudos?\n\n1️⃣ Sim\n2️⃣ Não"
PS_REP_Q7 = (
    "Você está no caminho certo 💙 Muitas pessoas acabam procurando ajuda só depois da negativa "
    "ou quando o problema já está mais avançado. Mas quando a gente atua antes, conseguimos "
    "evitar erros e fortalecer muito o caso.\n\n"
    "Você prefere tentar sozinho com o plano ou quer o acompanhamento da Dra. para garantir "
    "que o seu pedido seja feito à prova de negativas?"
)
PS_REP_MODALIDADE = (
    "Excelente decisão.\n\n"
    "Para que possamos buscar o seu resultado, nós trabalhamos de duas formas:\n\n"
    "1️⃣ Consultoria Estratégica de Laudos\n"
    "2️⃣ Blindagem Jurídica Integral (A MAIS INDICADA)\n\n"
    "Qual dessas modalidades você deseja iniciar agora?"
)

# PS: Negativa de cirurgia - Especialidades
PS_NEG_CIR_ESP = "Qual é o diagnóstico ou o tratamento específico que o plano está dificultando no momento?\n\n1️⃣ Endometriose\n2️⃣ Bariátrica\n3️⃣ Oncologia (câncer)\n4️⃣ Cardiologia (coração)\n5️⃣ Neurocirurgia\n6️⃣ Ortopedia\n7️⃣ Oftalmologia\n8️⃣ OUTRO"

# PS: Endometriose
PS_ENDO_Q1 = "Qual tipo de cirurgia foi indicada para o seu caso?"
PS_ENDO_Q2 = "Sinto muito que você esteja passando por isso. Sabemos que a endometriose não é 'só uma cólica', é algo que para a vida da mulher 💙\n\nO plano negou formalmente ou simplesmente não respondeu?"
PS_ENDO_Q3 = "Sei o quanto a dor e a incerteza cansam, mas você merece viver com saúde e qualidade. Não é justo que a sua cirurgia seja negada depois de tanta espera. Vou te ajudar a destravar esse processo 💙\n\nO plano justificou a negativa de alguma forma? (Ex: 'eletivo', 'sem cobertura', 'período de carência')"
PS_ENDO_Q4 = "É muito comum os planos de saúde negarem tratamento com justificativas infundadas, ignorando a indicação do seu médico. Mas a lei é clara: quem decide o melhor pra você é ele, não o plano."
PS_ENDO_Q5 = "👉 Você tem os exames que demonstram o seu diagnóstico?"
PS_ENDO_Q6 = "👉 Você já tentou resolver isso diretamente com o plano — ligação, protocolo, ouvidoria ou recurso formal?"

# PS: Bariátrica
PS_BARI_Q1 = "Entendo. A cirurgia bariátrica tem critérios específicos e muitas negativas são indevidas.\n\n👉 Qual o seu IMC atual? Se não souber, pode me falar somente seu peso atual e sua altura"
PS_BARI_Q2 = "👉 Você tem comorbidades? (diabetes, hipertensão, apneia do sono, problemas nas articulações)"
PS_BARI_Q3 = "A cirurgia bariátrica nunca é apenas estética. É seu direito concluir esse ciclo com segurança e cobertura total pela operadora. Vou superar esses obstáculos contratuais para que seu procedimento seja autorizado 💙"
PS_BARI_Q4 = "👉 Fez o acompanhamento multidisciplinar exigido (nutricionista, psicólogo, endocrinologista)?\n\n1️⃣ Sim\n2️⃣ Não"
PS_BARI_Q5 = "👉 O plano negou formalmente ou simplesmente não respondeu?"
PS_BARI_Q6 = "👉 O plano justificou a negativa de alguma forma? (Ex: 'eletivo', 'sem cobertura', 'período de carência')"
PS_BARI_Q7 = "É muito comum os planos de saúde negarem tratamento com justificativas infundadas, ignorando a indicação do seu médico. Mas a lei é clara: quem decide o melhor pra você é ele, não o plano."
PS_BARI_Q8 = "👉 Você já tentou resolver isso diretamente com o plano — ligação, protocolo, ouvidoria ou recurso formal?"

# PS: Oncologia
PS_ONCO_Q1 = "👉 Qual o tipo de câncer e qual procedimento foi indicado — cirurgia, quimio, radio, imunoterapia?"
PS_ONCO_Q2 = "👉 Já está em tratamento de alguma forma, ou a negativa está impedindo o início?"
PS_ONCO_Q3 = "Sinto muito que você esteja passando por isso, mas saiba que não está sozinha nessa luta. Vou cuidar de toda a burocracia para que você tenha seu tratamento sem interrupções. Seu foco agora deve ser apenas a sua cura: o resto, pode deixar aqui com a gente.\n\n👉 O plano negou formalmente ou simplesmente não respondeu?"
PS_ONCO_Q4 = "É muito comum os planos de saúde negarem tratamento com justificativas infundadas, ignorando a indicação do seu médico. Mas a lei é clara: quem decide o melhor pra você é ele, não o plano."
PS_ONCO_Q5 = "👉 O plano justificou a negativa de alguma forma? (Ex: 'eletivo', 'sem cobertura', 'período de carência')"
PS_ONCO_Q6 = "👉 Você tem os exames que demonstram o seu diagnóstico?"
PS_ONCO_Q7 = "👉 Você já tentou resolver isso diretamente com o plano — ligação, protocolo, ouvidoria ou recurso formal?"

# PS: Cardiologia
PS_CARDIO_Q1 = "👉 Qual tipo de cirurgia foi indicada para o seu caso?"
PS_CARDIO_Q2 = "👉 No seu caso o plano negou material cirúrgico ou alguma prótese?"
PS_CARDIO_Q3 = "👉 O plano negou formalmente ou simplesmente não respondeu?"
PS_CARDIO_Q4 = "👉 O plano justificou a negativa de alguma forma? (Ex: 'eletivo', 'sem cobertura', 'período de carência')\n\nÉ muito comum os planos de saúde negarem tratamento com justificativas infundadas, ignorando a indicação do seu médico. Mas a lei é clara: quem decide o melhor pra você é ele, não o plano."
PS_CARDIO_Q5 = "👉 Você já está internado aguardando o procedimento ou está em casa esperando a autorização para agendar?"
PS_CARDIO_Q6 = "👉 O procedimento foi considerado urgente?\n\n1️⃣ Sim\n2️⃣ Não"
PS_CARDIO_Q7 = "👉 Você tem exames (ecocardiograma, cateterismo, ECG) que confirmam a necessidade cirúrgica?"

# PS: Neurocirurgia
PS_NEURO_Q1 = "👉 Qual procedimento neurocirúrgico foi indicado?"
PS_NEURO_Q2 = "👉 O paciente está internado ou com dor insuportável e precisa operar imediatamente?\n\n1️⃣ Sim\n2️⃣ Não"
PS_NEURO_Q3 = "👉 O hospital onde seria realizada a cirurgia é da rede do plano?\n\n1️⃣ Sim\n2️⃣ Não\n3️⃣ Não sei"
PS_NEURO_Q4 = "Sinto muito que você esteja passando por essa insegurança. Para eu desenhar a melhor estratégia jurídica, me conte:\n\n👉 Hoje, esse problema neurológico está afetando seus movimentos, causando perda de força ou dores que impedem você de realizar tarefas básicas?"
PS_NEURO_Q5 = "👉 O plano justificou a negativa de alguma forma? (Ex: 'eletivo', 'sem cobertura', 'período de carência')"
PS_NEURO_Q6 = "É muito comum os planos de saúde negarem tratamento com justificativas infundadas, ignorando a indicação do seu médico. Mas a lei é clara: quem decide o melhor pra você é ele, não o plano."
PS_NEURO_Q7 = "👉 Essa negativa do plano foi por escrita ou verbal?"
PS_NEURO_Q8 = "👉 No seu caso o plano negou material cirúrgico ou alguma prótese?"
PS_NEURO_Q9 = "👉 Você tem exames de imagem — ressonância magnética, tomografia — que confirmam a necessidade cirúrgica?"

# PS: Ortopedia
PS_ORTO_Q1 = "👉 Qual cirurgia ortopédica foi indicada?"
PS_ORTO_Q2 = "👉 A condição está limitando sua mobilidade ou capacidade de trabalho?\n\n1️⃣ Sim, de forma significativa\n2️⃣ Parcialmente\n3️⃣ Ainda consigo me movimentar"
PS_ORTO_Q3 = "👉 O plano justificou a negativa de alguma forma? (Ex: 'eletivo', 'sem cobertura', 'período de carência')"
PS_ORTO_Q4 = "É muito comum os planos de saúde negarem tratamento com justificativas infundadas, ignorando a indicação do seu médico. Mas a lei é clara: quem decide o melhor pra você é ele, não o plano."
PS_ORTO_Q5 = "👉 No seu caso o plano negou material cirúrgico ou alguma prótese?"
PS_ORTO_Q6 = "👉 Essa negativa do plano foi por escrita ou verbal?"
PS_ORTO_Q7 = "👉 Você tem exames de imagem — ressonância magnética, tomografia — que confirmam a necessidade cirúrgica?"

# PS: Oftalmologia
PS_OFTAL_Q1 = "👉 Qual cirurgia oftalmológica foi indicada?"
PS_OFTAL_Q2 = "👉 A condição está afetando sua visão de forma significativa?\n\n1️⃣ Sim, já estou com visão muito comprometida\n2️⃣ Está piorando progressivamente\n3️⃣ Ainda consigo enxergar razoavelmente"
PS_OFTAL_Q3 = "👉 O médico indicou urgência, risco de perda de visão se não operar logo?\n\n1️⃣ Sim, há urgência expressa no laudo\n2️⃣ O médico disse verbalmente, mas não está no laudo\n3️⃣ Não há urgência indicada"
PS_OFTAL_Q4 = "👉 O plano justificou a negativa de alguma forma? (Ex: 'eletivo', 'sem cobertura', 'período de carência')"
PS_OFTAL_Q5 = "👉 Essa negativa do plano foi por escrita ou verbal?"
PS_OFTAL_Q6 = "É muito comum os planos de saúde negarem tratamento com justificativas infundadas, ignorando a indicação do seu médico. Mas a lei é clara: quem decide o melhor pra você é ele, não o plano."

# PS: Medicamento Negado
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

# PS: Exame Negado
PS_EXAME_Q1 = "👉 Qual exame foi solicitado pelo seu médico?"
PS_EXAME_Q2 = "👉 Para qual doença ou suspeita esse exame foi indicado?"
PS_EXAME_Q3 = "Sei o quão frustrante é ter um exame negado. Sem o exame, não há diagnóstico, e sem diagnóstico, não há tratamento. O plano não pode impedir a investigação da sua saúde."
PS_EXAME_Q4 = "👉 Você sente que essa demora do plano está prejudicando a sua saúde ou impedindo que você comece o tratamento que tanto precisa?"
PS_EXAME_Q5 = "👉 O que o seu médico lhe disse sobre a urgência deste resultado?"
PS_EXAME_Q6 = "👉 Qual foi o motivo da negativa?\n\n1️⃣ Fora do rol da ANS\n2️⃣ Não atende diretriz (DUT)\n3️⃣ Carência\n4️⃣ Não é urgente\n5️⃣ Experimental\n6️⃣ Outro"
PS_EXAME_Q7 = "👉 Essa negativa do plano foi por escrita ou verbal?"

# PS: Home Care
PS_HOME_Q1 = "Sinto muito que você e sua família estejam passando por esse momento. Sabemos que o Home Care não é um 'luxo', mas a única forma de garantir dignidade, segurança e uma recuperação humanizada para quem você ama. 💙\n\n👉 Qual a doença ou condição do paciente?"
PS_HOME_Q2 = "👉 O paciente está acamado ou depende de cuidados constantes?"
PS_HOME_Q3 = "👉 O paciente já ficou internado recentemente?"
PS_HOME_Q4 = "Eu imagino o peso que está nos seus ombros agora. Cuidar de quem amamos exige muito, e sem a estrutura técnica correta, o medo de algo acontecer é constante.\n\n👉 Você sente que o plano de saúde está tentando transferir para a sua família uma responsabilidade médica que é deles?"
PS_HOME_Q5 = "👉 O home care foi negado?\n\n1️⃣ Sim\n2️⃣ Não\n3️⃣ Ainda não solicitei"
PS_HOME_Q6 = "👉 Você possui relatório médico detalhado?\n\n1️⃣ Sim\n2️⃣ Não"
PS_HOME_Q7 = "👉 Está descrito o tipo de cuidado necessário (enfermagem, 24h, etc.)?"

# PS: Terapias
PS_TERA_Q1 = "👉 O tratamento é para:\n\n1️⃣ Autismo (TEA)\n2️⃣ Desenvolvimento infantil\n3️⃣ Reabilitação física\n4️⃣ Saúde mental\n5️⃣ Outro"
PS_TERA_Q2 = "👉 Quais terapias foram indicadas pelo médico?\n\n1️⃣ ABA\n2️⃣ Fisioterapia\n3️⃣ Psicologia\n4️⃣ Fonoaudiologia\n5️⃣ Terapia ocupacional\n6️⃣ Psicopedagogia\n7️⃣ Musicoterapia\n8️⃣ Hidroterapia\n9️⃣ Fisioterapia pélvica"
PS_TERA_Q3 = "👉 Quantas sessões por semana foram indicadas?"
PS_TERA_Q4 = "Eu entendo que essa não é apenas uma briga por 'papéis', é uma briga pelo futuro e pela autonomia sua ou de quem você ama. 💙\n\n👉 Hoje, a falta dessas terapias ou a limitação das sessões tem causado retrocessos ou estagnado a evolução que você(s) tanto espera(m)?"
PS_TERA_Q5 = "👉 O que aconteceu?\n\n1️⃣ Limitou número de sessões\n2️⃣ Negou totalmente\n3️⃣ Não tem profissional disponível\n4️⃣ Outro"
PS_TERA_Q6 = "👉 Você possui laudo médico com o diagnóstico?\n\n1️⃣ Sim\n2️⃣ Não"
PS_TERA_Q7 = "👉 Essa negativa do plano foi por escrita ou verbal?"

# PS: Reajuste
PS_REAJ_Q1 = "Recebi seu contato e já quero te tranquilizar: você não precisa aceitar um reajuste que torna o seu plano de saúde impagável. Muitas vezes, esses aumentos são aplicados de forma ilegal para forçar o cancelamento do contrato, mas a justiça está aí para impedir isso. 💙\n\n👉 O plano é:\n\n1️⃣ Individual/Familiar\n2️⃣ Coletivo por adesão\n3️⃣ Empresarial\n4️⃣ Não sei"
PS_REAJ_Q2 = "👉 De quanto foi aproximadamente o aumento?\n\n1️⃣ Até 20%\n2️⃣ 20% a 50%\n3️⃣ Mais de 50%\n4️⃣ Não sei"
PS_REAJ_Q3 = "É muito frustrante ver o valor subir tanto, especialmente quando você sempre honrou com os pagamentos para garantir a sua segurança e a da sua família. 💙\n\n👉 Hoje, esse novo valor do boleto compromete a sua renda ou faz você considerar cancelar o plano?"
PS_REAJ_Q4 = "👉 Você (ou o titular) tem mais de 59 anos?\n\n1️⃣ Sim\n2️⃣ Não"
PS_REAJ_Q5 = "👉 O aumento ocorreu após mudança de idade?\n\n1️⃣ Sim\n2️⃣ Não"
PS_REAJ_Q6 = "👉 Você recebeu algum documento detalhando o aumento?\n\n1️⃣ Sim\n2️⃣ Não"
PS_REAJ_Q7 = "👉 Esse plano foi feito por:\n\n1️⃣ Empresa\n2️⃣ Associação/sindicato\n3️⃣ Contratei sozinho"
PS_REAJ_Q8 = "👉 Você possui o contrato do plano?\n\n1️⃣ Sim\n2️⃣ Não"

# PS: Coparticipação
PS_COPA_Q1 = "Recebi seu contato e já te adianto: a coparticipação não pode ser uma surpresa desagradável no seu boleto. Ela deve ser clara e, acima de tudo, dentro dos limites da lei. Ninguém deve ter medo de usar o plano por causa do valor das taxas. 💙\n\n👉 Você deixou de fazer exames ou tratamentos por causa da coparticipação?\n\n1️⃣ Sim\n2️⃣ Não"
PS_COPA_Q2 = "É muito desgastante você pagar o plano em dia e, quando mais precisa dele, ser surpreendido com taxas que parecem uma segunda mensalidade.\n\n👉 Você sente que hoje está 'pagando para usar' o que já deveria estar coberto?"
PS_COPA_Q3 = "👉 A coparticipação foi cobrada em:\n\n1️⃣ Consultas\n2️⃣ Exames\n3️⃣ Terapias\n4️⃣ Internação\n5️⃣ Outro"
PS_COPA_Q4 = "👉 Você faz tratamento contínuo?\n\n1️⃣ Sim\n2️⃣ Não"
PS_COPA_Q5 = "👉 Qual tipo de tratamento você faz?"
PS_COPA_Q6 = "Importante você saber: a coparticipação não pode ser ilimitada. A justiça entende que cobrar percentuais muito altos ou taxas sobre internação pode ser considerado abusivo, pois impede o paciente de se tratar."
PS_COPA_Q7 = "👉 Você possui o contrato do plano?\n\n1️⃣ Sim\n2️⃣ Não"

# PS: Erro Médico
PS_ERRO_Q1 = "Sinto muito que você esteja passando por isso. Sei que, além da dor física, existe uma quebra de confiança muito grande quando algo não sai como o esperado em um procedimento médico. Estou aqui para te ouvir e entender se houve uma falha que te dá direito à reparação. 💙\n\n👉 O que aconteceu durante o atendimento médico?\n\n1️⃣ Cirurgia\n2️⃣ Atendimento de emergência\n3️⃣ Tratamento contínuo\n4️⃣ Parto\n5️⃣ Outro"
PS_ERRO_Q2 = "👉 O paciente sofreu algum dano?\n\n1️⃣ Agravamento da saúde\n2️⃣ Sequela\n3️⃣ Dor intensa\n4️⃣ Novo procedimento necessário\n5️⃣ Óbito"
PS_ERRO_Q3 = "Eu imagino o quanto esse momento está sendo difícil para você e para sua família. Para que eu possa desenhar a melhor estratégia:\n\n👉 Como esse episódio mudou a sua vida hoje?"
PS_ERRO_Q4 = "👉 Você possui prontuário médico?\n\n1️⃣ Sim\n2️⃣ Não"
PS_ERRO_Q5 = "👉 Outro médico já disse que houve erro ou falha no atendimento?\n\n1️⃣ Sim\n2️⃣ Não"
PS_ERRO_Q6 = "👉 Você sente que houve falta de informação, descaso ou uma falha clara na técnica do médico ou do hospital?"

# PS: OUTRO
PS_OUTRO_Q1 = "Entendido! O Direito da Saúde é muito amplo e, se o seu problema envolve o seu bem-estar ou o seu contrato de saúde, você está no lugar certo. 💙\n\nPara que eu possa entender como te ajudar, me conte brevemente o que está acontecendo. O plano de saúde negou algo?"
PS_OUTRO_Q2 = "👉 Existe algum prazo ou data limite que te preocupa agora (ex: uma cirurgia marcada, um boleto vencendo ou um prazo de defesa)?"
PS_OUTRO_Q3 = "👉 Você recebeu alguma negativa ou teve dificuldade no atendimento?\n\n1️⃣ Sim\n2️⃣ Não\n3️⃣ Não se encaixa"
PS_OUTRO_Q4 = "👉 Você tem isso registrado (mensagem, documento, protocolo)?\n\n1️⃣ Sim\n2️⃣ Não\n3️⃣ Não se encaixa"
PS_OUTRO_Q5 = "👉 Você possui documentos relacionados ao caso?\n\n1️⃣ Sim\n2️⃣ Não"
PS_OUTRO_Q6 = "👉 Esse problema está afetando sua saúde atualmente?\n\n1️⃣ Sim\n2️⃣ Não"
PS_OUTRO_Q7 = "Certo, recebi seus detalhes. Independentemente do caso, a minha premissa é sempre a mesma: o contrato de saúde deve servir para proteger a vida e o consumidor, não para criar barreiras."

# Pós perguntas Plano de Saúde
PS_POS = (
    "Obrigado por todas as informações. Já consigo ter um bom entendimento da sua situação.\n\n"
    "Agora me diz: o que você está buscando nesse momento? Escolha a opção que mais se encaixa:\n\n"
    "1️⃣ Quero apenas tirar dúvidas básicas\n"
    "2️⃣ Já tenho a negativa do plano\n"
    "3️⃣ Não tenho a negativa mas sei que o plano vai negar"
)

PS_OP1 = (
    "Faz todo sentido querer entender bem a situação antes de tomar qualquer decisão.\n\n"
    "Para isso, ofereço uma *consulta de orientação jurídica* — você fala diretamente comigo, "
    "tira todas as suas dúvidas e entende com clareza quais são seus direitos.\n\n"
    "💰 O valor da consulta é de *R$ 97,00* e é feita online.\n\n"
    "Podemos agendar um horário na agenda da Dra. Lethicia?"
)

PS_OP2 = (
    "Nesse caso só é possível revertermos a negativa do plano com medidas judiciais.\n\n"
    "Você está no momento exato de agirmos para buscar o seu direito judicialmente. "
    "Agora não é mais hora de esperar, é hora de exigir que o plano de saúde cumpra a lei.\n\n"
    "Perfeito. O próximo passo agora é uma reunião rápida para eu te explicar como funciona "
    "o processo e valores de honorários.\n\n"
    "Antes de agendarmos: além de você, tem mais alguém que participa dessa decisão?"
)

PS_OP3 = (
    "Você é muito estratégico(a)! Esperar a negativa do plano para só depois agir "
    "é o erro que faz muita gente perder meses de tratamento.\n\n"
    "Meu papel aqui é duplo: primeiro, vou 'blindar' seus laudos para que o plano não "
    "tenha desculpas para negar. E, caso eles insistam na abusividade, já teremos a prova "
    "perfeita para a justiça liberar sua cirurgia de forma imediata.\n\n"
    "Você prefere tentar sozinho com o plano ou quer o acompanhamento da Dra. para garantir "
    "que o seu pedido seja feito à prova de negativas?"
)

PS_ENCERRAMENTO = (
    "Entendo perfeitamente e respeito sua decisão.\n\n"
    "Vou encerrar o seu atendimento por aqui para priorizar os casos que já estão com "
    "liminares em andamento. Lembre-se apenas que, no Direito da Saúde, o tempo é um "
    "fator determinante para o sucesso do tratamento.\n\n"
    "Caso precise de suporte especializado no futuro, meus canais continuam à disposição. 🙏"
)

# ============================================
# PROCESSAMENTO DO FLUXO
# ============================================

def processar(resposta: str):
    estado = st.session_state.estado
    dados = st.session_state.dados

    # INICIO
    if estado == "INICIO":
        st.session_state.nome = resposta
        dados["nome"] = resposta
        st.session_state.estado = "CANAL"
        add_bot(MSG_CANAL.format(nome=resposta))

    # CANAL
    elif estado == "CANAL":
        if "sus" in _n(resposta):
            dados["canal"] = "SUS"
            st.session_state.estado = "SUS_DEMANDA"
            add_bot(MSG_SUS_DEMANDA)
        else:
            dados["canal"] = "PLANO"
            st.session_state.estado = "PLANO_TEMPO"
            add_bot(MSG_PLANO_TEMPO)

    # SUS_DEMANDA
    elif estado == "SUS_DEMANDA":
        if "cirurgia" in _n(resposta) or "1" in resposta:
            dados["tipo"] = "cirurgia"
            st.session_state.estado = "SUS_ESPECIALIDADE"
            add_bot(MSG_SUS_ESPECIALIDADE)
        else:
            dados["tipo"] = "consulta_exame"
            st.session_state.estado = "SUS_CONSULTA_EXAME"
            add_bot("Você está buscando:\n\n1️⃣ Consulta com especialista\n2️⃣ Realização de Exame")

    # SUS_ESPECIALIDADE
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

    # SUS_PERGUNTAS
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

    # POS_PERGUNTAS
    elif estado == "POS_PERGUNTAS":
        dados["sentimento"] = resposta
        add_bot(MSG_EXPLICACAO)
        st.session_state.estado = "HONORARIOS"

    # HONORARIOS
    elif estado == "HONORARIOS":
        dados["honorarios"] = resposta
        add_bot(MSG_HONORARIOS)
        st.session_state.estado = "RESPOSTA_HONORARIOS"

    # RESPOSTA_HONORARIOS
    elif estado == "RESPOSTA_HONORARIOS":
        if _sim(resposta):
            add_bot(MSG_SIM)
        else:
            add_bot(MSG_NAO)
        st.session_state.estado = "FIM"

    # SUS_CONSULTA_EXAME
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

    # SUS_EXAME_TIPO
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

    # PLANO_TEMPO
    elif estado == "PLANO_TEMPO":
        if _sim(resposta):
            dados["plano_2anos"] = "sim"
            st.session_state.estado = "PLANO_SITUACAO"
            add_bot(MSG_PLANO_SITUACAO)
        else:
            dados["plano_2anos"] = "nao"
            st.session_state.estado = "PLANO_NAO_2ANOS"
            add_bot("Entendo! Muitas pessoas acreditam que precisam esperar 2 anos para ter direito a cirurgias ou tratamentos complexos, mas a lei nem sempre funciona assim.\n\nMe conta, qual o tratamento que você precisa fazer?")

    # PLANO_NAO_2ANOS
    elif estado == "PLANO_NAO_2ANOS":
        dados["tratamento"] = resposta
        st.session_state.estado = "PLANO_NAO_2ANOS_URG"
        add_bot("Existem situações onde o plano é obrigado a cobrir o seu procedimento mesmo que você tenha poucos meses de contrato, especialmente se houver urgência ou se a doença não foi declarada por má-fé.\n\nNo seu caso, o médico comentou se isso é urgente ou pode trazer algum risco se não for feito?")

    # PLANO_NAO_2ANOS_URG
    elif estado == "PLANO_NAO_2ANOS_URG":
        dados["urgencia_plano"] = resposta
        st.session_state.estado = "PROPOSTA_JUDICIAL"
        add_bot("Perfeito, isso é importante 😊\n\nSE HÁ URGÊNCIA, o plano já deveria cobrir normalmente esse tipo de situação.\n\nPara resolver isso, eu trabalho com um *Protocolo de Liberação Urgente*. Isso faria diferença na sua vida agora?")

    # PLANO_SITUACAO
    elif estado == "PLANO_SITUACAO":
        dados["situacao"] = resposta
        
        # Roteamento baseado na situação
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
            add_bot("Entendido! Cada procedimento cirúrgico tem a sua importância. Se o seu médico indicou, é porque é necessário para a sua saúde.\n\n👉 Qual cirurgia foi indicada pelo seu médico?")

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
        dados["ps_bari_q8"] = resposta        st.session_state.estado = "PS_POS"
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

    # PS_POS (pós perguntas do plano)
    elif estado == "PS_POS":
        dados["ps_pos_escolha"] = resposta
        if "1" in resposta:
            add_bot(PS_OP1)
            st.session_state.estado = "PS_OP1_AGUARDANDO"
        elif "2" in resposta:
            add_bot(PS_OP2)
            st.session_state.estado = "PS_DECISAO"
        elif "3" in resposta:
            add_bot(PS_OP3)
            st.session_state.estado = "PS_PREVENTIVO"
        else:
            add_bot(PS_POS)

    # PS_OP1 (dúvidas)
    elif estado == "PS_OP1_AGUARDANDO":
        if _sim(resposta):
            add_bot(f"Ótimo! Agende sua consulta: {CALENDLY_LINK}")
        else:
            add_bot("Quando decidir que é o momento de ter segurança jurídica no seu caso, estou à disposição. Sucesso na sua jornada! 🙏")
        st.session_state.estado = "FIM"

    # PS_DECISAO (já tem negativa)
    elif estado == "PS_DECISAO":
        dados["ps_decisao"] = resposta
        if _sim(resposta):
            add_bot("Excelente! Vou te encaminhar para a agenda da Dra. Lethicia.\n\n"
                    f"🔗 {CALENDLY_LINK}\n\n"
                    "Fique atento(a)! Em breve ela entrará em contato. 💙")
        else:
            add_bot(PS_ENCERRAMENTO)
        st.session_state.estado = "FIM"

    # PS_PREVENTIVO (não tem negativa ainda)
    elif estado == "PS_PREVENTIVO":
        if "acompanhamento" in _n(resposta):
            st.session_state.estado = "PS_DECISAO"
            add_bot("Perfeito! O próximo passo agora é uma reunião rápida para a Dra Lethicia te explicar como funciona o processo e valores de honorários.\n\n"
                    "Antes de agendarmos: além de você, tem mais alguém que participa dessa decisão?")
        else:
            add_bot(PS_ENCERRAMENTO)
            st.session_state.estado = "FIM"

    # PROPOSTA_JUDICIAL (para plano)
    elif estado == "PROPOSTA_JUDICIAL":
        if _sim(resposta):
            add_bot("Ótimo! Vou te encaminhar para a agenda da Dra. Lethicia.\n\n"
                    f"🔗 {CALENDLY_LINK}")
        else:
            add_bot(MSG_NAO)
        st.session_state.estado = "FIM"

    # VALORES (interceptado antes)
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
        if st.session_state.dados.get("especialidade"):
            st.markdown(f"**Especialidade:** {st.session_state.dados['especialidade'][:30]}")
        
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
            if st.button("🔪 Cirurgia / Tratamento", use_container_width=True):
                add_user("Cirurgia / Tratamento")
                processar("Cirurgia / Tratamento")
                st.rerun()
        with col2:
            if st.button("📋 Consultas / Exames", use_container_width=True):
                add_user("Consultas / Exames")
                processar("Consultas / Exames")
                st.rerun()
    
    elif estado == "SUS_ESPECIALIDADE":
        st.markdown("---")
        st.markdown("**🔘 Especialidades:**")
        especialidades = [
            "Oncologia", "Neurodivergências", "Endometriose", "Medicamento",
            "Bariátrica", "Reparadora", "Neurologia", "Cardiologia", "Outros"
        ]
        cols = st.columns(3)
        for i, esp in enumerate(especialidades):
            with cols[i % 3]:
                if st.button(esp[:15], use_container_width=True):
                    add_user(esp)
                    processar(esp)
                    st.rerun()
    
    elif estado in ["HONORARIOS", "RESPOSTA_HONORARIOS", "PS_OP1_AGUARDANDO", "PS_DECISAO", "PROPOSTA_JUDICIAL"]:
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
    
    # Interceptar perguntas sobre valores
    if user_input and any(p in _n(user_input) for p in ["valor", "quanto", "preço", "custa", "honorário", "investimento"]):
        add_user(user_input)
        add_bot(
            "Compreendo sua dúvida sobre o investimento. No nosso escritório, nós não trabalhamos com "
            "valores genéricos porque cada vida e cada urgência são únicas.\n\n"
            f"A {L} não define valores por mensagem de texto. Para casos assim, é necessária uma "
            f"Reunião Estratégica por vídeo (15 minutos).\n\n"
            f"🔗 {CALENDLY_LINK}"
        )
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
