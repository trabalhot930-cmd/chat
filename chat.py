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

def _nao(r: str) -> bool:
    return any(p in _n(r) for p in ["não", "nao", "n", "no", "nunca", "recuso"])

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

PERGUNTAS_ONCOLOGIA = [
    "Entendi… vamos cuidar disso juntos 💙\n\n👉 Você consegue me contar qual é o tipo de câncer?",
    "👉 Você está aguardando atendimento ou tratamento pelo SUS? Se sim, há quanto tempo mais ou menos?",
    "Só pra eu entender melhor seu caso:\n\n👉 O diagnóstico já foi confirmado por biópsia? E você tem esse laudo em mãos?",
    "Entendi…\n\n👉 Você já foi encaminhado para um hospital especializado em câncer (oncologia) pelo SUS ou ainda nem conseguiu passar com um especialista?",
    "👉 Você possui um relatório médico explicando o tratamento que precisa fazer?",
    "Última perguntinha, que é bem importante:\n\n👉 O médico falou se o seu caso é urgente?",
    "👉 Você possui o comprovante de que está aguardando na fila?"
]

PERGUNTAS_NEURO = [
    "Entendi… pode ficar tranquilo(a), vou te ajudar com isso 💙\n\nCasos assim realmente precisam de atenção, principalmente por envolver desenvolvimento.\n\n👉 Me conta: já tem diagnóstico fechado ou ainda está em investigação?",
    "👉 Você tem algum laudo ou relatório médico com o diagnóstico?",
    "Entendo as batalhas diárias que você enfrenta para garantir o melhor para quem você ama. Nenhuma criança deve ter seu desenvolvimento barrado por limites impostos pelo **SUS**. Estou aqui para lutar ao seu lado e garantir todas as terapias que são de direito.\n\nAgora me conta uma coisa importante:\n\n👉 Quais terapias o médico indicou? (ABA, Psico, fisioterapia...)",
    "E hoje, como está essa situação no SUS?\n\n👉 Você conseguiu iniciar as terapias ou ainda está aguardando?",
    "Entendo…\n\n👉 Você está em fila ou aguardando vaga?",
    "Essa parte é muito importante:\n\n👉 O médico comentou algo sobre prejuízo no desenvolvimento ou necessidade de iniciar rápido as terapias?",
    "Se você puder me contar:\n\n👉 Como essa situação está impactando o dia a dia de vocês?",
    "👉 Você possui o comprovante de que está aguardando na fila?"
]

PERGUNTAS_ENDOMETRIOSE = [
    "Entendi… imagino o quanto isso pode estar sendo difícil pra você 🥺\nMas fica tranquila, vou te ajudar com isso 💙\n\n👉 Você já tem diagnóstico confirmado de endometriose ou adenomiose?",
    "Obrigado por me contar 🙏\n\n👉 Esse diagnóstico foi feito por exame? Se ainda não fez, qual exame está aguardando?",
    "Sei o quanto a dor e a incerteza cansam, mas você merece viver com saúde e qualidade. Não é justo que a sua cirurgia ou exame continue demorando assim. Vou te ajudar a destravar esse processo para que você receba o cuidado que precisa.\n\nQuero entender melhor sua situação:\n\n👉 Você sente dores fortes ou crises que atrapalham sua rotina?",
    "Agora uma parte bem importante:\n\n👉 O médico indicou algum tratamento específico?\n\n(ex: cirurgia de videolaparoscopia, medicamento, acompanhamento…)",
    "👉 Você tem relatório médico explicando esse tratamento?",
    "👉 Você está aguardando há quanto tempo mais ou menos?",
    "👉 O médico colocou em relatório ou te informou se existe risco de piora ou agravamento sem o tratamento?",
    "👉 Você possui o comprovante de que está aguardando na fila?"
]

PERGUNTAS_MEDICAMENTO = [
    "Entendi… vamos ver isso com calma 💙\n\n👉 Qual foi o medicamento que o médico indicou pra você?",
    "Perfeito, obrigado por me explicar 🙏\n\n👉 Você tem a receita ou relatório médico desse medicamento?",
    "Entendo a frustração de ter um direito negado justamente quando você mais precisa de suporte. Analisaremos seu caso para garantir que a lei seja cumprida e o acesso à saúde seja imediato. Conte conosco para transformar essa negativa em uma solução rápida e segura.\n\nAo te passar esse medicamento o seu médico escreveu no laudo que este remédio específico é o único que pode tratar seu caso agora e que a interrupção trará riscos à sua vida ou saúde?",
    "Essa parte é bem importante:\n\n👉 Você já utilizou outros medicamentos antes? Se sim, eles não tiveram resultado ou causaram algum problema?",
    "👉 Você chegou a solicitar esse medicamento pelo SUS ou farmácia de alto custo? O que te informaram?",
    "👉 O médico comentou o que pode acontecer se você não usar esse medicamento?"
]

PERGUNTAS_BARIATRICA = [
    "Entendi… vamos ver isso com calma 💙\n\n👉 Você já tem indicação médica para cirurgia bariátrica?",
    "👉 Você possui outras doenças agravadas pelo peso, como Diabetes, Hipertensão, Apneia do Sono ou problemas graves nas articulações?",
    "👉 Você tem algum laudo ou relatório médico indicando a cirurgia?",
    "Só pra eu entender melhor seu caso:\n\n👉 Você sabe me informar seu peso e altura? (se não souber exato, pode ser aproximado)",
    "Essa parte é bem importante:\n\n👉 Você já tentou outros tratamentos antes, como dieta, acompanhamento ou medicamentos? Como foi essa experiência?",
    "👉 Você já está na fila de espera do SUS há quanto tempo?",
    "👉 Você possui o comprovante de que está aguardando na fila?"
]

PERGUNTAS_NEUROLOGIA = [
    "Entendi… vamos ver isso com calma 💙\n\n👉 Você consegue me explicar qual é o problema neurológico ou diagnóstico?",
    "Obrigado por me explicar 🙏\n\n👉 Você tem algum laudo ou exame com esse diagnóstico?",
    "Sei que o momento é de muita angústia e que cada minuto de espera parece uma eternidade. Vou agir com a rapidez que o caso pede para que o hospital libere logo o necessário.\n\n👉 Gostaria de saber qual cirurgia especificamente você está aguardando. Você pode me dizer?",
    "👉 O médico especialista (Neuro) ou outro médico já emitiu o laudo dizendo que a demora pode causar um dano irreversível da sua condição?",
    "👉 Você está aguardando tratamento ou cirurgia? Há quanto tempo mais ou menos?",
    "👉 Você já possui o comprovante de que está aguardando na fila?"
]

PERGUNTAS_CARDIOLOGIA = [
    "Entendi… vamos ver isso com calma 💙\n\n👉 Você consegue me explicar qual é o problema cardíaco ou o que o médico te disse?",
    "O seu caso envolve uma cirurgia de urgência (Ponte de safena, troca de válvula, marca-passo/Stent)?",
    "👉 Você tem algum exame ou laudo do coração? (ex: eletro, ecocardiograma, cateterismo…)",
    "👉 Quais sintomas você tem sentido? (Dor no peito, falta de ar, tontura, cansaço excessivo)",
    "👉 O médico indicou algum tratamento ou procedimento?",
    "👉 Você tem relatório médico explicando essa necessidade?",
    "👉 Você já possui o comprovante de que está aguardando na fila?"
]

PERGUNTAS_OUTROS = [
    "Entendi. Como o seu caso é específico, eu preciso entender o que está acontecendo para te direcionar corretamente.\n\n👉 Poderia me dizer qual é a sua condição/doença?",
    "Só pra eu entender melhor:\n\n👉 Você já tem algum diagnóstico ou ainda está investigando?",
    "👉 Algum médico já te passou relatório ou pedido de tratamento?",
    "Vamos resolver isso juntos…\n\n👉 O médico comentou se existe urgência ou risco em não realizar esse tratamento?",
    "👉 O que acontece com a sua saúde se você não conseguir isso nos próximos 30 ou 90 dias? Existe risco de agravamento ou sequela irreversível?",
    "👉 Como essa situação tem afetado sua vida hoje?",
    "👉 Você possui o comprovante de que está aguardando na fila?"
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
    "para assumir o caso e protocolar o pedido de liminar. Prosseguir com esse caso faz sentido "
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
    "Entendi sua situação. Para que eu consiga te ajudar judicialmente a conseguir o atendimento que você precisa no SUS, "
    "o juiz exige obrigatoriamente alguns documentos que comprovam que o Estado está falhando com você.\n\n"
    "Sem um laudo médico atualizado e o comprovante de inscrição na fila de espera, "
    "o processo corre o risco de ser negado logo no início.\n\n"
    "Minha orientação agora: vá até a unidade de saúde, peça a atualização do seu laudo "
    "e tire uma foto do comprovante da fila. Assim que tiver esses papéis em mãos, "
    "me envie aqui para agendarmos nossa reunião de estratégia, combinado?"
)

MSG_SUS_NEGATIVA = (
    "Nesse caso só é possível revertermos a negativa do plano com medidas judiciais. "
    "Você está no momento exato de agirmos para buscar o seu direito judicialmente. "
    "Agora não é mais hora de esperar, é hora de exigir que o SUS cumpra a lei. "
    "O próximo passo agora é uma reunião rápida para eu te explicar como funciona o processo e valores de honorários. "
    "Não se preocupe, é uma reunião gratuita e on-line. "
    "Antes de agendarmos: além de você, tem mais alguém que participe das decisões familiares ou financeiras, "
    "como seu esposo/esposa, que seria importante estar presente para já tirarmos todas as dúvidas de uma vez?"
)

MSG_SUS_SIM_HONORARIOS = (
    "Ótimo. Isso mostra que você prioriza sua saúde acima da burocracia do Estado.\n\n"
    "Vou encaminhar seus dados para a mesa da Dra. Lethicia neste momento. Em instantes, ela entrará em contato aqui por este chat para te passar a estratégia de liberação e os valores para o seu caso. Fique atento(a)!"
)

MSG_SUS_NAO_HONORARIOS = (
    "Compreendo. Infelizmente, sem o interesse em avançar com uma medida judicial, "
    "o seu caso continuará dependendo exclusivamente da velocidade da fila do SUS, que como sabemos, não tem previsão.\n\n"
    "Como o escritório da Dra. Lethicia foca apenas em quem deseja forçar a solução imediata, "
    "estamos encerrando seu atendimento por aqui.\n\n"
    "Caso a sua situação se agrave ou você decida que não pode mais esperar, "
    "sinta-se à vontade para retornar. Desejamos sorte no seu tratamento."
)

# ============================================
# PLANO DE SAÚDE - MENSAGENS
# ============================================

PS_BUSCA = (
    "Obrigado por todas as informações. Já consigo ter um bom entendimento da sua situação.\n\n"
    "Agora me diz: o que você está buscando nesse momento? Escolha a opção que mais se encaixa com onde você está agora:\n\n"
    "1️⃣ Quero entender se o plano de saúde é obrigado a cobrir determinado tratamento ou Tenho uma dúvida específica ou um caso diferente e gostaria de orientação jurídica para entender quais são meus direitos e possibilidades.\n\n"
    "2️⃣ Já tenho a negativa do plano: Desejo orientação especializada para ingressar com a ação judicial e buscar a liberação do meu tratamento.\n\n"
    "3️⃣ Ainda não tenho a negativa, mas preciso me preparar: Quero me antecipar, eu ainda não recebi a negativa do plano, mas sei que meu pedido pode ser recusado. Quero me preparar da forma correta, com orientação jurídica, para aumentar minhas chances de aprovação do tratamento ou sucesso na ação judicial.\n\n"
    "4️⃣ Preciso de uma consultoria jurídica: Desejo uma análise técnica sobre o meu caso de saúde. Indicado para dúvidas sobre reajustes abusivos (anual ou por faixa etária), períodos de carência, migração de plano (portabilidade) ou para saber se um tratamento específico tem cobertura obrigatória pela ANS."
)

# OPÇÃO 1 - ATENDIMENTO PARTICULAR
PS_OP1_PERGUNTA = (
    "Perfeito! Para esse tipo de dúvida pontual, oferecemos o Atendimento Particular. "
    "Diferente da consultoria completa, aqui você tira todas as suas dúvidas, tem um direcionamento claro do seu caso "
    "e um especialista te responde de forma técnica e direta, analisando se o seu direito é garantido por lei. Isso te ajudaria?"
)

PS_OP1_DETALHES = (
    "O investimento no atendimento particular é de R$ 97,00 e é feito online.\n\n"
    "É um atendimento individual e aprofundado onde você terá os seguintes benefícios:\n"
    "• Resposta Técnica Direta: Esclarecimento sobre a obrigatoriedade de cobertura (Rol da ANS e entendimentos judiciais recentes).\n"
    "• Análise de Viabilidade: Uma opinião profissional sobre se o seu caso tem chances reais de sucesso na justiça ou se é uma questão administrativa.\n"
    "• Indicação de Documentos: Lista do que você precisa providenciar imediatamente para não perder seus direitos.\n\n"
    "Podemos marcar um horário pra você na agenda da Dra Lethicia?"
)

PS_OP1_PAGAMENTO = (
    "Perfeito! Vamos reservar o seu horário.\n\n"
    "Como deseja realizar o investimento do atendimento? Você prefere Pix ou Cartão de Crédito?"
)

PS_OP1_CONFIRMACAO = (
    "Ao realizar o pagamento e for dado baixa no nosso financeiro, alguém da nossa equipe vai entrar em contato o quanto antes pra marcar seu atendimento na agenda da Dra Lethicia."
)

# OPÇÃO 2 - JÁ TEM NEGATIVA
PS_OP2_PERGUNTA = (
    "Nesse caso só é possível revertermos a negativa do plano com medidas judiciais. "
    "Você está no momento exato de agirmos para buscar o seu direito judicialmente. "
    "Agora não é mais hora de esperar, é hora de exigir que o plano de saúde cumpra a lei.\n\n"
    "O próximo passo agora é uma reunião rápida para eu te explicar como funciona o processo e valores de honorários.\n\n"
    "Antes de agendarmos: além de você, tem mais alguém que participe das decisões familiares ou financeiras, "
    "como seu esposo/esposa, que seria importante estar presente para já tirarmos todas as dúvidas de uma vez?"
)

# OPÇÃO 3 - PREVENTIVO
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

# OPÇÃO 4 - CONSULTORIA JURÍDICA
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

PS_OP4_PAGAMENTO = (
    "Perfeito! Vamos reservar o seu horário.\n\n"
    "Como deseja realizar o investimento do atendimento? Você prefere Pix ou Cartão de Crédito?"
)

PS_OP4_CONFIRMACAO = (
    "Ao realizar o pagamento e for dado baixa no nosso financeiro, alguém da nossa equipe vai entrar em contato o quanto antes pra marcar seu atendimento na agenda da Dra Lethicia."
)

# ENCERRAMENTO
PS_ENCERRAMENTO = (
    "Entendo perfeitamente e respeito sua decisão.\n\n"
    "Vou encerrar o seu atendimento por aqui para priorizar os casos que já estão com liminares em andamento. "
    "Lembre-se apenas que, no Direito da Saúde, o tempo é um fator determinante para o sucesso do tratamento.\n\n"
    "Caso precise de suporte especializado no futuro, nossos canais continuam à disposição."
)

# DECISÃO COMPARTILHADA
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
            st.session_state.estado = "PS_BUSCA"
            add_bot(PS_BUSCA)

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
        
        # Contar respostas "não" para perguntas críticas (últimas 4)
        if idx >= len(perguntas) - 4:
            if _nao(resposta):
                st.session_state.respostas_nao += 1
        
        idx += 1
        st.session_state.pergunta_idx = idx
        
        if idx < len(perguntas):
            add_bot(perguntas[idx])
        else:
            # Verificar se faltam documentos críticos
            if st.session_state.respostas_nao >= 2:
                st.session_state.estado = "FIM"
                add_bot(MSG_SEM_DOCUMENTOS)
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
            add_bot(MSG_SUS_SIM_HONORARIOS)
            st.session_state.estado = "FIM"
        else:
            add_bot(MSG_SUS_NAO_HONORARIOS)
            st.session_state.estado = "FIM"

    # ========== PLANO DE SAÚDE - BUSCA ==========
    elif estado == "PS_BUSCA":
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

    # ========== PS_OP1 - ATENDIMENTO PARTICULAR ==========
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

    # ========== PS_OP2 - JÁ TEM NEGATIVA ==========
    elif estado == "PS_OP2_PERGUNTA":
        st.session_state.estado = "DECISAO_COMPARTILHADA"

    # ========== PS_OP3 - PREVENTIVO ==========
    elif estado == "PS_OP3_PERGUNTA":
        st.session_state.estado = "PS_OP3_PERMISSAO"
        add_bot(PS_OP3_PERMISSAO)

    elif estado == "PS_OP3_PERMISSAO":
        st.session_state.estado = "DECISAO_COMPARTILHADA"

    # ========== PS_OP4 - CONSULTORIA JURÍDICA ==========
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

        # Botões contextuais
        estado = st.session_state.estado

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

        elif estado == "SUS_DEMANDA":
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("🔪 Cirurgia / Tratamento", use_container_width=True):
                    add_user("Cirurgia")
                    processar("Cirurgia")
                    st.rerun()
            with col_b:
                if st.button("📋 Consultas / Exames", use_container_width=True):
                    add_user("Consultas")
                    processar("Consultas")
                    st.rerun()

        elif estado == "SUS_ESPECIALIDADE":
            especialidades = ["Oncologia", "Neurodivergências", "Endometriose", "Medicamento", "Bariátrica", "Neurologia", "Cardiologia", "Outros"]
            cols = st.columns(2)
            for i, esp in enumerate(especialidades):
                with cols[i % 2]:
                    if st.button(esp, use_container_width=True):
                        add_user(esp)
                        processar(str(i+1))
                        st.rerun()

        elif estado in ["POS_PERGUNTAS", "PROPOSTA", "HONORARIOS"]:
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("✅ SIM", use_container_width=True):
                    add_user("SIM")
                    processar("SIM")
                    st.rerun()
            with col_b:
                if st.button("❌ NÃO", use_container_width=True):
                    add_user("NÃO")
                    processar("NÃO")
                    st.rerun()

        elif estado == "PS_BUSCA":
            options = ["1️⃣ Dúvida Cobertura", "2️⃣ Já Negativa", "3️⃣ Preventivo", "4️⃣ Consultoria"]
            cols = st.columns(2)
            for i, opt in enumerate(options):
                with cols[i % 2]:
                    if st.button(opt, use_container_width=True):
                        add_user(opt)
                        processar(str(i+1))
                        st.rerun()

        elif estado in ["PS_OP1_PERGUNTA", "PS_OP1_DETALHES", "PS_OP4_PERGUNTA"]:
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("✅ SIM", use_container_width=True):
                    add_user("SIM")
                    processar("SIM")
                    st.rerun()
            with col_b:
                if st.button("❌ NÃO", use_container_width=True):
                    add_user("NÃO")
                    processar("NÃO")
                    st.rerun()

        elif estado in ["PS_OP1_PAGAMENTO", "PS_OP4_PAGAMENTO"]:
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("💳 Cartão de Crédito", use_container_width=True):
                    add_user("Cartão de Crédito")
                    processar("cartão")
                    st.rerun()
            with col_b:
                if st.button("📱 Pix", use_container_width=True):
                    add_user("Pix")
                    processar("pix")
                    st.rerun()

        elif estado == "DECISAO_COMPARTILHADA":
            if st.button("👨‍👩‍👧 Sim, meu cônjuge/familiar", use_container_width=True):
                add_user("Sim, meu cônjuge/familiar")
                processar("sim")
                st.rerun()
            if st.button("👤 Não, eu decido tudo sozinho(a)", use_container_width=True):
                add_user("Não, eu decido tudo sozinho(a)")
                processar("não")
                st.rerun()
            if st.button("📞 Tem meu cônjuge, mas pode falar comigo", use_container_width=True):
                add_user("Tem meu cônjuge, mas pode falar comigo")
                processar("repasse")
                st.rerun()

        elif estado == "DECISAO_REPASSE_RESPOSTA":
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("👥 Com ele(a)", use_container_width=True):
                    add_user("Com ele(a)")
                    processar("sim")
                    st.rerun()
            with col_b:
                if st.button("👤 Entre nós", use_container_width=True):
                    add_user("Entre nós")
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
            st.success("✅ Atendimento finalizado! Clique em 'Nova Conversa' para começar novamente.")

    # Inicializar chat se vazio
    if not st.session_state.messages:
        add_bot(MSG_BOAS_VINDAS)
        st.rerun()

if __name__ == "__main__":
    main()
