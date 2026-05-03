"""
Iara Bot - Assistente Jurídica em Direito da Saúde
VERSÃO FINAL - CORRIGIDA 100%
"""

import streamlit as st
from datetime import datetime

# ============================================
# CONFIGURAÇÕES
# ============================================
CALENDLY_LINK = "https://calendly.com/dra-lethicia"
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
# SUS - MENSAGENS
# ============================================

MSG_SUS_DEMANDA = "Me diga o que você está aguardando?\n\n🔪 Cirurgia / Tratamento\n\n📋 Consultas / Exames"

MSG_SUS_ESPECIALIDADE = (
    "Para que eu direcione você para o protocolo de urgência correto, "
    "qual problema estamos enfrentando hoje?\n\n"
    "1️⃣ Oncologia\n2️⃣ Neurodivergências (TEA, TDAH)\n3️⃣ Endometriose / Adenomiose\n"
    "4️⃣ Medicamento\n5️⃣ Bariátrica\n6️⃣ Neurologia / Neurocirurgia\n"
    "7️⃣ Cardiologia\n8️⃣ Outros"
)

# ============================================
# SUS - PERGUNTAS POR ESPECIALIDADE
# ============================================

# 1. ONCOLOGIA
PERGUNTAS_ONCOLOGIA = [
    "Entendi… vamos cuidar disso juntos 💙\n\n👉 Você consegue me contar qual é o tipo de câncer?",
    "👉 Você está aguardando atendimento ou tratamento pelo SUS? Se sim, há quanto tempo mais ou menos?",
    "Só pra eu entender melhor seu caso:\n\n👉 O diagnóstico já foi confirmado por biópsia? E você tem esse laudo em mãos?",
    "Entendi…\n\n👉 Você já foi encaminhado para um hospital especializado em câncer (oncologia) pelo SUS ou ainda nem conseguiu passar com um especialista?\n\nInfelizmente, a fila do SUS não respeita o avanço da doença. Se o hospital não iniciou seu tratamento em 60 dias, a lei está sendo descumprida e precisamos forçar o início imediato via Justiça.",
    "👉 Você possui um relatório médico explicando o tratamento que precisa fazer? (se quiser, pode enviar aqui também 📎)",
    "Última perguntinha, que é bem importante:\n\n👉 O médico falou se o seu caso é urgente?",
    "👉 Você possui o comprovante de que está aguardando na fila?\n\nPode ser o print da tela do App Meu SUS Digital, o comprovante de agendamento da Secretaria de Saúde ou o papel da regulação (SISREG) com o número do seu protocolo."
]

# 2. NEURODIVERGÊNCIAS
PERGUNTAS_NEURO = [
    "Entendi… pode ficar tranquilo(a), vou te ajudar com isso 💙\n\nCasos assim realmente precisam de atenção, principalmente por envolver desenvolvimento.\n\n👉 Me conta: já tem diagnóstico fechado ou ainda está em investigação?",
    "👉 Você tem algum laudo ou relatório médico com o diagnóstico?",
    "Entendo as batalhas diárias que você enfrenta para garantir o melhor para quem você ama. Nenhuma criança deve ter seu desenvolvimento barrado por limites impostos pelo **SUS**. Estou aqui para lutar ao seu lado e garantir todas as terapias que são de direito.\n\nAgora me conta uma coisa importante:\n\n👉 Quais terapias o médico indicou?",
    "E hoje, como está essa situação no SUS?\n\n👉 Você conseguiu iniciar as terapias ou ainda está aguardando?",
    "Entendo…\n\n👉 Você está em fila ou aguardando vaga?",
    "Essa parte é muito importante:\n\n👉 O médico comentou algo sobre prejuízo no desenvolvimento ou necessidade de iniciar rápido as terapias?",
    "Se você puder me contar:\n\n👉 Como essa situação está impactando o dia a dia de vocês?",
    "👉 Você possui o comprovante de que está aguardando na fila?\n\nPode ser o print da tela do App Meu SUS Digital, o comprovante de agendamento da Secretaria de Saúde ou o papel da regulação (SISREG) com o número do seu protocolo."
]

# 3. ENDOMETRIOSE
PERGUNTAS_ENDOMETRIOSE = [
    "Entendi… imagino o quanto isso pode estar sendo difícil pra você 🥺\nMas fica tranquila, vou te ajudar com isso 💙\n\n👉 Você já tem diagnóstico confirmado de endometriose ou adenomiose?",
    "Obrigado por me contar 🙏\n\n👉 Esse diagnóstico foi feito por exame? Se ainda não fez, qual exame está aguardando?",
    "Sei o quanto a dor e a incerteza cansam, mas você merece viver com saúde e qualidade. Não é justo que a sua cirurgia ou exame continue demorando assim. Vou te ajudar a destravar esse processo para que você receba o cuidado que precisa.\n\nQuero entender melhor sua situação:\n\n👉 Você sente dores fortes ou crises que atrapalham sua rotina?",
    "Agora uma parte bem importante:\n\n👉 O médico indicou algum tratamento específico?\n\n(ex: cirurgia de videolaparoscopia, medicamento, acompanhamento…)",
    "👉 Você tem relatório médico explicando esse tratamento?\n\nSe puder enviar, ajuda muito na análise 📎",
    "👉 Você está aguardando há quanto tempo mais ou menos?",
    "👉 O médico colocou em relatório ou te informou se existe risco de piora ou agravamento sem o tratamento?",
    "👉 Você possui o comprovante de que está aguardando na fila?\n\nPode ser o print da tela do App Meu SUS Digital, o comprovante de agendamento da Secretaria de Saúde ou o papel da regulação (SISREG) com o número do seu protocolo."
]

# 4. MEDICAMENTO
PERGUNTAS_MEDICAMENTO = [
    "Entendi… vamos ver isso com calma 💙\n\n👉 Qual foi o medicamento que o médico indicou pra você?",
    "Perfeito, obrigado por me explicar 🙏\n\n👉 Você tem a receita ou relatório médico desse medicamento?",
    "Entendo a frustração de ter um direito negado justamente quando você mais precisa de suporte. Analisaremos seu caso para garantir que a lei seja cumprida e o acesso à saúde seja imediato. Conte conosco para transformar essa negativa em uma solução rápida e segura.\n\nAo te passar esse medicamento o seu médico escreveu no laudo que este remédio específico é o único que pode tratar seu caso agora e que a interrupção trará riscos à sua vida ou saúde?",
    "Essa parte é bem importante:\n\n👉 Você já utilizou outros medicamentos antes? Se sim, eles não tiveram resultado ou causaram algum problema?",
    "👉 Você chegou a solicitar esse medicamento pelo SUS ou farmácia de alto custo? O que te informaram?\n\n(foi negado, está em análise, falta no estoque… pode me explicar melhor)",
    "👉 O médico comentou o que pode acontecer se você não usar esse medicamento?\n\n(se puder me explicar, isso ajuda muito)"
]

# 5. BARIÁTRICA
PERGUNTAS_BARIATRICA = [
    "Entendi… vamos ver isso com calma 💙\n\n👉 Você já tem indicação médica para cirurgia bariátrica?",
    "👉 Você possui outras doenças agravadas pelo peso, como Diabetes, Hipertensão, Apneia do Sono ou problemas graves nas articulações?",
    "👉 Você tem algum laudo ou relatório médico indicando a cirurgia? Se puder enviar aqui, já me ajuda bastante 📎",
    "Só pra eu entender melhor seu caso:\n\n👉 Você sabe me informar seu peso e altura? (se não souber exato, pode ser aproximado)",
    "Essa parte é bem importante:\n\n👉 Você já tentou outros tratamentos antes, como dieta, acompanhamento ou medicamentos? Como foi essa experiência?",
    "👉 Você já está na fila de espera do SUS há quanto tempo?",
    "👉 Você possui o comprovante de que está aguardando na fila?\n\nPode ser o print da tela do App Meu SUS Digital, o comprovante de agendamento da Secretaria de Saúde ou o papel da regulação (SISREG) com o número do seu protocolo."
]

# 6. NEUROLOGIA
PERGUNTAS_NEUROLOGIA = [
    "Entendi… vamos ver isso com calma 💙\n\n👉 Você consegue me explicar qual é o problema neurológico ou diagnóstico?",
    "Obrigado por me explicar 🙏\n\n👉 Você tem algum laudo ou exame com esse diagnóstico? (se puder enviar aqui, ajuda bastante 📎)",
    "Sei que o momento é de muita angústia e que cada minuto de espera parece uma eternidade. Vou agir com a rapidez que o caso pede para que o hospital libere logo o necessário. Minha prioridade é tirar esse peso das suas costas e proteger a vida de quem você ama.\n\n👉 Gostaria de saber qual cirurgia especificamente você está aguardando. Você pode me dizer?",
    "👉 O médico especialista (Neuro) ou outro médico já emitiu o laudo dizendo que a demora pode causar um dano irreversível da sua condição?",
    "👉 Você está aguardando tratamento ou cirurgia? Há quanto tempo mais ou menos?",
    "👉 Você já possui o comprovante de que está aguardando na fila?\n\nPode ser o print da tela do App Meu SUS Digital, o comprovante de agendamento da Secretaria de Saúde ou o papel da regulação (SISREG) com o número do seu protocolo."
]

# 7. CARDIOLOGIA
PERGUNTAS_CARDIOLOGIA = [
    "Entendi… vamos ver isso com calma 💙\n\n👉 Você consegue me explicar qual é o problema cardíaco ou o que o médico te disse?",
    "👉 O seu caso envolve uma cirurgia de urgência (como ponte de safena ou troca de válvula), a colocação de um Marca-passo/Stent?",
    "Obrigado por me explicar 🙏\n\n👉 Você tem algum exame ou laudo do coração? (ex: eletro, ecocardiograma, cateterismo… se puder enviar 📎)",
    "👉 Você tem sentido algum desses sintomas?\n\n• Dor no peito\n• Falta de ar\n• Tontura ou desmaio\n• Cansaço excessivo\n\nSe tiver outros, pode me contar também.",
    "👉 O médico indicou algum tratamento ou procedimento? (ex: cirurgia, cateterismo, marcapasso, acompanhamento…)",
    "👉 Você tem relatório médico explicando essa necessidade? (se puder enviar, ajuda muito na análise 📎)",
    "👉 Você já possui o comprovante de que está aguardando na fila?\n\nPode ser o print da tela do App Meu SUS Digital, o comprovante de agendamento da Secretaria de Saúde ou o papel da regulação (SISREG) com o número do seu protocolo."
]

# 8. OUTROS
PERGUNTAS_OUTROS = [
    "Entendi. Como o seu caso é específico, eu preciso entender o que está acontecendo para te direcionar corretamente.\n\n👉 Poderia me dizer qual é a sua condição/doença?",
    "Só pra eu entender melhor:\n\n👉 Você já tem algum diagnóstico ou ainda está investigando?",
    "👉 Algum médico já te passou relatório ou pedido de tratamento? Se tiver, pode me enviar aqui 📎",
    "Vamos resolver isso juntos…\n\n👉 O médico comentou se existe urgência ou risco em não realizar esse tratamento?",
    "👉 O que acontece com a sua saúde se você não conseguir isso nos próximos 30 ou 90 dias? Existe risco de agravamento ou sequela irreversível?",
    "👉 Como essa situação tem afetado sua vida hoje?",
    "👉 Você possui o comprovante de que está aguardando na fila?\n\nPode ser o print da tela do App Meu SUS Digital, o comprovante de agendamento da Secretaria de Saúde ou o papel da regulação (SISREG) com o número do seu protocolo."
]

# ============================================
# SUS - PÓS PERGUNTAS
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
    "para assumir o caso e entrar com um processo judicial. Prosseguir com esse caso faz sentido "
    "para você garantir sua saúde hoje e sair dessa espera?"
)

MSG_ENCERRAMENTO_SUS = (
    "Compreendo. Infelizmente, sem o interesse em avançar com uma medida judicial, "
    "o seu caso continuará dependendo exclusivamente da velocidade da fila do SUS, "
    "que como sabemos, não tem previsão.\n\n"
    "Como o escritório da Dra. Lethicia foca apenas em quem deseja forçar a solução imediata, "
    "estamos encerrando seu atendimento por aqui.\n\n"
    "Caso a sua situação se agrave ou você decida que não pode mais esperar, "
    "sinta-se à vontade para retornar. Desejamos sorte no seu tratamento. 🙏"
)

MSG_SEM_DOCUMENTOS = (
    "Entendi sua situação. Para que eu consiga te ajudar judicialmente a conseguir esse [exame/cirurgia/medicamento], "
    "o juiz exige obrigatoriamente alguns documentos que comprovam que o Estado está falhando com você.\n\n"
    "Sem um laudo médico atualizado e o comprovante de inscrição na fila de espera, "
    "o processo corre o risco de ser negado logo no início.\n\n"
    "Minha orientação agora: vá até a unidade de saúde, peça a atualização do seu laudo "
    "e tire uma foto do comprovante da fila. Assim que tiver esses papéis em mãos, "
    "me envie aqui para agendarmos nossa reunião de estratégia, combinado?"
)

# ============================================
# PLANO DE SAÚDE - MENSAGENS INICIAIS
# ============================================

PS_TEMPO = "Você já tem seu plano de saúde há mais de 2 anos?\n\n1️⃣ Sim\n2️⃣ Não"
PS_TIPO_PLANO = "Seu plano é pessoa física ou empresarial/CNPJ?\n\n1️⃣ Pessoa Física\n2️⃣ Empresarial/CNPJ"

PS_SITUACAO = (
    "Para que eu possa te direcionar corretamente, qual é a sua situação atual com o plano de saúde?\n\n"
    "1️⃣ Reparadora\n2️⃣ Negativa de cirurgia\n3️⃣ Medicamento negado\n4️⃣ Exame negado\n"
    "5️⃣ Home care\n6️⃣ Terapias\n7️⃣ Reajuste\n8️⃣ Coparticipação\n9️⃣ Erro médico\n🔟 OUTRO"
)

PS_NAO_2ANOS = "Entendo! Muitas pessoas acreditam que precisam esperar 2 anos para ter direito a cirurgias ou tratamentos complexos, mas a lei nem sempre funciona assim.\n\nMe conta, qual o tratamento que você precisa fazer?"
PS_NAO_2ANOS_URG = "Existem situações onde o plano é obrigado a cobrir o seu procedimento mesmo que você tenha poucos meses de contrato, especialmente se houver urgência ou se a doença não foi declarada por má-fé.\n\nNo seu caso, o médico comentou se isso é urgente ou pode trazer algum risco se não for feito?"
PS_URGENCIA = "Perfeito, isso é importante 😊\n\nSE HÁ URGÊNCIA, o plano já deveria cobrir normalmente esse tipo de situação. Mesmo assim, eles podem acabar negando indevidamente em alguns casos.\n\nO médico indicou que o tratamento é urgente?"

# ============================================
# PLANO - REPARADORA
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
PS_REP_Q3 = (
    "Eu entendo que essa pele que restou é o capítulo final de uma grande superação, mas ela também pode ser um peso físico e emocional. Para eu desenhar a melhor estratégia para você, me conte um pouco…\n\n"
    "Esse excesso de pele hoje te causa dores, assaduras ou dermatites que não curam? E além do corpo, como isso tem afetado a sua autoestima e a sua liberdade de movimento no dia a dia?"
)
PS_REP_Q4 = "👉 Quais cirurgias reparadoras você teria interesse em fazer?"
PS_REP_Q5 = "Certo… Você já chegou a ir no médico cirurgião plástico pra solicitar as reparadoras e emitir os laudos?\n\n1️⃣ Sim\n2️⃣ Não"
PS_REP_Q6 = "Você está no caminho certo 💙 Muitas pessoas acabam procurando ajuda só depois da negativa ou quando o problema já está mais avançado. Mas quando a gente atua antes, conseguimos evitar erros e fortalecer muito o caso.\n\nVocê prefere tentar sozinho com o plano ou quer o acompanhamento da Dra. para garantir que o seu pedido seja feito à prova de negativas?"

# ============================================
# PLANO - PÓS PERGUNTAS (COM 4 OPÇÕES)
# ============================================

PS_POS = (
    "Obrigado por todas as informações. Já consigo ter um bom entendimento da sua situação.\n\n"
    "Agora me diz: o que você está buscando nesse momento? Escolha a opção que mais se encaixa com onde você está agora:\n\n"
    "1️⃣ Quero entender se o plano de saúde é obrigado a cobrir determinado tratamento ou Tenho uma dúvida específica ou um caso diferente e gostaria de orientação jurídica para entender quais são meus direitos e possibilidades.\n\n"
    "2️⃣ Já tenho a negativa do plano: Desejo orientação especializada para ingressar com a ação judicial e buscar a liberação do meu tratamento.\n\n"
    "3️⃣ Ainda não tenho a negativa, mas preciso me preparar: Quero me antecipar, eu ainda não recebi a negativa do plano, mas sei que meu pedido pode ser recusado. Quero me preparar da forma correta, com orientação jurídica, para aumentar minhas chances de aprovação do tratamento ou sucesso na ação judicial.\n\n"
    "4️⃣ Preciso de uma consultoria jurídica: Desejo uma análise técnica sobre o meu caso de saúde. Indicado para dúvidas sobre reajustes abusivos (anual ou por faixa etária), períodos de carência, migração de plano (portabilidade) ou para saber se um tratamento específico tem cobertura obrigatória pela ANS."
)

# Opção 1 - Atendimento Expresso
PS_OP1 = "Perfeito! Para esse tipo de dúvida pontual, oferecemos o Atendimento Expresso. Diferente da consultoria completa, aqui você envia sua dúvida e um especialista te responde de forma técnica e direta, analisando se o seu direito é garantido por lei. Isso te ajudaria?"

PS_OP1_DETALHES = (
    "O investimento no atendimento particular é de R$ 97,00 e é feito online.\n\n"
    "É um atendimento individual e aprofundado onde você terá os seguintes benefícios:\n"
    "• Resposta Técnica Direta: Esclarecimento sobre a obrigatoriedade de cobertura (Rol da ANS e entendimentos judiciais recentes).\n"
    "• Análise de Viabilidade: Uma opinião profissional sobre se o seu caso tem chances reais de sucesso na justiça ou se é uma questão administrativa.\n"
    "• Indicação de Documentos: Lista do que você precisa providenciar imediatamente para não perder seus direitos.\n\n"
    "Podemos marcar um horário pra você na agenda da Dra Lethicia?"
)

# Opção 2 - Já tem negativa
PS_OP2 = (
    "Nesse caso só é possível revertermos a negativa do plano com medidas judiciais. "
    "Você está no momento exato de agirmos para buscar o seu direito judicialmente. "
    "Agora não é mais hora de esperar, é hora de exigir que o plano de saúde cumpra a lei.\n\n"
    "O próximo passo agora é uma reunião rápida para eu te explicar como funciona o processo e valores de honorários.\n\n"
    "Antes de agendarmos: além de você, tem mais alguém que participe das decisões familiares ou financeiras, como seu esposo/esposa, que seria importante estar presente para já tirarmos todas as dúvidas de uma vez?"
)

# Opção 3 - Preventivo
PS_OP3 = (
    "Você fez está no caminho certo, buscar uma orientação antes de pedir ao plano! "
    "Esperar a negativa do plano para só depois agir é o erro que faz muita gente perder meses de tratamento.\n\n"
    "Com o acompanhamento jurídico, você tem as orientações corretas sobre quais médicos deve ir e como que deve ser feitos os laudos, "
    "o que você deve fazer na perícia do plano de saúde (se for solicitado no seu caso), isso tudo sendo organizado agora, "
    "após a negativa do plano, você já vai ter todos os laudos e documentos corretos pra um processo judicial, "
    "assim não precisa corrigir ou ficar correndo atrás de laudos depois. Entende?"
)

PS_OP3_PERMISSAO = "Você prefere tentar sozinho com o plano ou quer o acompanhamento da Dra. para garantir que o seu pedido seja feito à prova de negativas (principalmente ao entrarmos na justiça)?"

# Opção 4 - Consultoria Jurídica
PS_OP4 = (
    "Entendido. Para casos de análise contratual, reajustes ou dúvidas preventivas, realizamos uma Consultoria Jurídica Especializada.\n\n"
    "Nesta reunião online um advogado especialista em Direito da Saúde analisará detalhadamente o seu caso, documentos e contratos para te entregar um parecer seguro sobre os seus direitos.\n\n"
    "Informações sobre a Consultoria:\n"
    "• Investimento: R$ 500,00 (referente à análise técnica e reserva de horário).\n"
    "• Duração: Até 1 hora.\n"
    "• Objetivo: Diagnóstico completo e estratégia jurídica personalizada.\n\n"
    "Deseja prosseguir com o agendamento?"
)

# Mensagens de pagamento
PS_PAGAMENTO = "Perfeito! Vamos reservar o seu horário.\n\nPasso 1: Escolha o melhor dia e hora no link abaixo:\n🔗 {CALENDLY_LINK}\n\nPasso 2: Após escolher o horário, realize o pagamento da consultoria."

PS_ENCERRAMENTO = (
    "Entendo perfeitamente e respeito sua decisão.\n\n"
    "Vou encerrar o seu atendimento por aqui para priorizar os casos que já estão com "
    "liminares em andamento. Lembre-se apenas que, no Direito da Saúde, o tempo é um "
    "fator determinante para o sucesso do tratamento.\n\n"
    "Caso precise de suporte especializado no futuro, meus canais continuam à disposição. 🙏"
)

# ============================================
# DECISÃO COMPARTILHADA
# ============================================

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
            st.session_state.estado = "PLANO_TEMPO"
            add_bot(PS_TEMPO)

    # ========== SUS_DEMANDA ==========
    elif estado == "SUS_DEMANDA":
        if "cirurgia" in _n(resposta):
            dados["tipo"] = "cirurgia"
            st.session_state.estado = "SUS_ESPECIALIDADE"
            add_bot(MSG_SUS_ESPECIALIDADE)
        else:
            dados["tipo"] = "consulta_exame"
            add_bot("Atendimento finalizado. Obrigado!")
            st.session_state.estado = "FIM"

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
            # Verificar se tem documentos
            tem_docs = False
            for i in range(len(perguntas)):
                if "sim" in _n(str(dados.get(f"resp_{i}", ""))):
                    tem_docs = True
                    break
            
            if not tem_docs:
                add_bot(MSG_SEM_DOCUMENTOS)
                st.session_state.estado = "FIM"
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
            add_bot("Perfeito. O próximo passo agora é uma reunião rápida para eu te explicar como funciona o processo e os valores de honorários.\n\nAntes de agendarmos: além de você, tem mais alguém que participa dessa decisão? (cônjuge, familiar…)")
            st.session_state.estado = "DECISAO_COMPARTILHADA"
        else:
            add_bot(MSG_ENCERRAMENTO_SUS)
            st.session_state.estado = "FIM"

    # ========== DECISAO_COMPARTILHADA ==========
    elif estado == "DECISAO_COMPARTILHADA":
        if "sim" in _n(resposta):
            add_bot(DECISAO_SIM)
        elif "não" in _n(resposta) or "sozinho" in _n(resposta):
            add_bot(DECISAO_NAO)
        else:
            add_bot(DECISAO_REPASSE)
            st.session_state.estado = "DECISAO_REPASSE_RESPOSTA"
            return
        st.session_state.estado = "FIM"

    # ========== DECISAO_REPASSE_RESPOSTA ==========
    elif estado == "DECISAO_REPASSE_RESPOSTA":
        if _sim(resposta):
            add_bot(DECISAO_REPASSE_SIM)
        else:
            add_bot(DECISAO_REPASSE_NAO)
        st.session_state.estado = "FIM"

    # ========== PLANO_TEMPO ==========
    elif estado == "PLANO_TEMPO":
        if _sim(resposta):
            dados["plano_2anos"] = "sim"
            st.session_state.estado = "PLANO_TIPO"
            add_bot(PS_TIPO_PLANO)
        else:
            dados["plano_2anos"] = "nao"
            st.session_state.estado = "PLANO_NAO_2ANOS"
            add_bot(PS_NAO_2ANOS)

    # ========== PLANO_TIPO ==========
    elif estado == "PLANO_TIPO":
        dados["plano_tipo"] = resposta
        st.session_state.estado = "PLANO_SITUACAO"
        add_bot(PS_SITUACAO)

    # ========== PLANO_NAO_2ANOS ==========
    elif estado == "PLANO_NAO_2ANOS":
        dados["tratamento_sem_carencia"] = resposta
        st.session_state.estado = "PLANO_NAO_2ANOS_URG"
        add_bot(PS_NAO_2ANOS_URG)

    # ========== PLANO_NAO_2ANOS_URG ==========
    elif estado == "PLANO_NAO_2ANOS_URG":
        dados["urgencia_plano"] = resposta
        st.session_state.estado = "PLANO_URGENCIA"
        add_bot(PS_URGENCIA)

    # ========== PLANO_URGENCIA ==========
    elif estado == "PLANO_URGENCIA":
        dados["urgencia_confirmada"] = resposta
        st.session_state.estado = "PLANO_SITUACAO"
        add_bot(PS_SITUACAO)

    # ========== PLANO_SITUACAO ==========
    elif estado == "PLANO_SITUACAO":
        dados["situacao"] = resposta
        
        if "reparadora" in _n(resposta) or "1" in resposta:
            st.session_state.estado = "PS_REP_Q1"
            add_bot(PS_REP_Q1)
        else:
            add_bot(PS_POS)
            st.session_state.estado = "PS_POS"

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
        if "acompanhamento" in _n(resposta):
            st.session_state.estado = "PS_POS"
            add_bot(PS_POS)
        else:
            add_bot(PS_ENCERRAMENTO)
            st.session_state.estado = "FIM"

    # ========== PS_POS ==========
    elif estado == "PS_POS":
        dados["ps_pos_escolha"] = resposta
        if "1" in resposta:
            st.session_state.estado = "PS_OP1"
            add_bot(PS_OP1)
        elif "2" in resposta:
            st.session_state.estado = "PS_OP2"
            add_bot(PS_OP2)
        elif "3" in resposta:
            st.session_state.estado = "PS_OP3"
            add_bot(PS_OP3)
        elif "4" in resposta:
            st.session_state.estado = "PS_OP4"
            add_bot(PS_OP4)
        else:
            add_bot(PS_POS)

    # ========== PS_OP1 ==========
    elif estado == "PS_OP1":
        if _sim(resposta):
            add_bot(PS_OP1_DETALHES)
            st.session_state.estado = "PS_OP1_AGENDAMENTO"
        else:
            add_bot(PS_ENCERRAMENTO)
            st.session_state.estado = "FIM"

    # ========== PS_OP1_AGENDAMENTO ==========
    elif estado == "PS_OP1_AGENDAMENTO":
        if _sim(resposta):
            add_bot(PS_PAGAMENTO.format(CALENDLY_LINK=CALENDLY_LINK))
        else:
            add_bot(PS_ENCERRAMENTO)
        st.session_state.estado = "FIM"

    # ========== PS_OP2 ==========
    elif estado == "PS_OP2":
        st.session_state.estado = "PS_OP2_BOTOES"

    # ========== PS_OP2_BOTOES ==========
    elif estado == "PS_OP2_BOTOES":
        if "sim" in _n(resposta) or "1" in resposta:
            add_bot(DECISAO_SIM)
        elif "não" in _n(resposta) or "2" in resposta:
            add_bot(DECISAO_NAO)
        else:
            add_bot(DECISAO_REPASSE)
            st.session_state.estado = "DECISAO_REPASSE_RESPOSTA"
            return
        st.session_state.estado = "FIM"

    # ========== PS_OP3 ==========
    elif estado == "PS_OP3":
        dados["ps_op3_entendeu"] = resposta
        st.session_state.estado = "PS_OP3_PERMISSAO"
        add_bot(PS_OP3_PERMISSAO)

    # ========== PS_OP3_PERMISSAO ==========
    elif estado == "PS_OP3_PERMISSAO":
        if "acompanhamento" in _n(resposta):
            add_bot("Perfeito. O próximo passo agora é uma reunião rápida para a Dra Lethicia te explicar como funciona o processo e valores de honorários.\n\nAntes de agendarmos: além de você, tem mais alguém que participe das decisões familiares ou financeiras, como seu esposo/esposa, que seria importante estar presente para já tirarmos todas as dúvidas de uma vez?")
            st.session_state.estado = "PS_OP2_BOTOES"
        else:
            add_bot(PS_ENCERRAMENTO)
            st.session_state.estado = "FIM"

    # ========== PS_OP4 ==========
    elif estado == "PS_OP4":
        if _sim(resposta):
            add_bot(PS_PAGAMENTO.format(CALENDLY_LINK=CALENDLY_LINK))
        else:
            add_bot(PS_ENCERRAMENTO)
        st.session_state.estado = "FIM"

    # ========== FIM ==========
    elif estado == "FIM":
        pass


# ============================================
# INTERFACE STREAMLIT
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
            if st.button("🔪 Cirurgia / Tratamento", use_container_width=True):
                add_user("Cirurgia")
                processar("Cirurgia")
                st.rerun()
        with col2:
            if st.button("📋 Consultas / Exames", use_container_width=True):
                add_user("Consultas")
                processar("Consultas")
                st.rerun()
    
    elif estado == "SUS_ESPECIALIDADE":
        st.markdown("---")
        st.markdown("**🔘 Especialidades:**")
        especialidades = ["Oncologia", "Neurodivergências", "Endometriose", "Medicamento", "Bariátrica", "Neurologia", "Cardiologia", "Outros"]
        cols = st.columns(4)
        for i, esp in enumerate(especialidades):
            with cols[i % 4]:
                if st.button(esp, use_container_width=True):
                    add_user(esp)
                    processar(esp)
                    st.rerun()
    
    elif estado in ["PROPOSTA", "HONORARIOS", "PS_OP1", "PS_OP1_AGENDAMENTO", "PS_OP4"]:
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
    
    elif estado == "DECISAO_COMPARTILHADA":
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("👨‍👩‍👧 Juntos (cônjuge)", use_container_width=True):
                add_user("Sim, meu cônjuge decide comigo")
                processar("Sim")
                st.rerun()
        with col2:
            if st.button("👤 Sozinho(a)", use_container_width=True):
                add_user("Não, eu decido tudo sozinho")
                processar("Não")
                st.rerun()
        with col3:
            if st.button("📞 Só eu, mas repasso", use_container_width=True):
                add_user("Tem meu cônjuge, mas pode falar só comigo")
                processar("Tem")
                st.rerun()
    
    elif estado == "DECISAO_REPASSE_RESPOSTA":
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Sim, pode participar", use_container_width=True):
                add_user("Sim")
                processar("Sim")
                st.rerun()
        with col2:
            if st.button("❌ Não, mantém só comigo", use_container_width=True):
                add_user("Não")
                processar("Não")
                st.rerun()
    
    elif estado == "PS_OP2_BOTOES":
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("👨‍👩‍👧 Juntos (cônjuge)", use_container_width=True):
                add_user("Sim")
                processar("Sim")
                st.rerun()
        with col2:
            if st.button("👤 Sozinho(a)", use_container_width=True):
                add_user("Não")
                processar("Não")
                st.rerun()
        with col3:
            if st.button("📞 Só eu, mas repasso", use_container_width=True):
                add_user("Tem")
                processar("Tem")
                st.rerun()
    
    elif estado == "PS_OP3_PERMISSAO":
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Quero o acompanhamento da Dra.", use_container_width=True):
                add_user("acompanhamento")
                processar("acompanhamento")
                st.rerun()
        with col2:
            if st.button("❌ Prefiro tentar sozinho", use_container_width=True):
                add_user("sozinho")
                processar("sozinho")
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
    
    if send and user_input:
        add_user(user_input)
        processar(user_input)
        st.rerun()


# ============================================
# MAIN
# ============================================

def main():
    st.title("⚖️ Lara Bot - Assistente Jurídica em Direito da Saúde")
    st.caption(f"{L} | Atendimento SUS, Planos de Saúde e INSS")
    
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
