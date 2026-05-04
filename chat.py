"""
Iara Bot v4 - Assistente Jurídica em Direito da Saúde
VERSÃO 2 - FLUXO PLANO DE SAÚDE CORRIGIDO
Fluxos: SUS (Exames, Consultas, Especialidades), Planos de Saúde, Detecção de Valores
"""

import streamlit as st
from datetime import datetime
import json

# ============================================
# CONFIGURAÇÕES INICIAIS
# ============================================
CALENDLY_LINK = "https://calendly.com/dra-lethicia"
L = "Dra. Lethicia Fernanda"

# Links de Pagamento Asaas
LINK_CARTAO_97 = "https://www.asaas.com/c/oilhnffc7xyvc4n6"
LINK_PIX_97 = "https://www.asaas.com/c/9025wgqkpuziono4"
LINK_CARTAO_500 = "https://www.asaas.com/c/apigp8m45tileghw"
LINK_PIX_500 = "https://www.asaas.com/c/x1dfvyoajxnlgpp2"

st.set_page_config(
    page_title="Iara Bot - Assistente Jurídica em Direito da Saúde",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CSS CUSTOMIZADO
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
        max-height: 600px;
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
        font-weight: 600;
    }
    .stButton button:hover {
        background-color: #1e40af;
    }
    .info-box {
        background-color: #e0f2fe;
        border-left: 4px solid #0284c7;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .success-box {
        background-color: #dcfce7;
        border-left: 4px solid #16a34a;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# FUNÇÕES AUXILIARES
# ============================================

def _n(r: str) -> str:
    """Normaliza texto para comparação (minúsculas, sem espaços)"""
    return str(r).strip().lower()

def _sim(r: str) -> bool:
    """Detecta respostas afirmativas"""
    gatilhos_sim = ["sim", "s", "yes", "quero", "ok", "claro", "vamos", "aceito", "topo", "acompanhamento", "ajuda", "prosseguir", "avançar"]
    return any(p in _n(r) for p in gatilhos_sim)

def _nao(r: str) -> bool:
    """Detecta respostas negativas"""
    gatilhos_nao = ["não", "nao", "n", "no", "nunca", "recuso", "negativo"]
    return any(p in _n(r) for p in gatilhos_nao)

def detectar_pergunta_valor(texto: str) -> bool:
    """Detecta perguntas sobre valores/custos"""
    gatilhos = ["valor", "quanto custa", "quanto é", "preço", "honorários", "pagamento", "investimento", "custa", "custo", "valor do"]
    return any(g in _n(texto) for g in gatilhos)

def responder_valor(dados: dict) -> str:
    """Retorna resposta contextualizada sobre valores"""
    canal = dados.get("canal", "")
    sus_tipo = dados.get("sus_tipo", "")
    ps_busca = dados.get("ps_busca", "")
    
    # Cenário 1: Cirurgia, Oncologia, Medicamento (Alta Complexidade)
    if "Cirurgia" in sus_tipo or "Oncologia" in sus_tipo or "Medicamento" in sus_tipo or "Bariátrica" in sus_tipo:
        return (
            "Compreendo sua dúvida sobre o investimento. No meu escritório, nós não trabalhamos com valores iguais porque cada vida e cada urgência são únicas.\n\n"
            "Como o seu caso envolve um cenário de alta complexidade técnica e risco direto à saúde, a Dra. Lethicia não define valores por mensagem de texto.\n\n"
            "Para situações assim, é necessária uma **Reunião Estratégica por vídeo (15 minutos)**. Nessa reunião, ela vai te apresentar o plano de ação para cercar o juiz e garantir que seu direito não seja negado, além de alinhar o investimento necessário.\n\n"
            f"Vamos agendar? {CALENDLY_LINK}"
        )
    
    # Cenário 2: Consultas e Exames
    elif "Consulta" in sus_tipo or "Exame" in sus_tipo or "Neurodivergências" in sus_tipo or "Endometriose" in sus_tipo:
        return (
            "Compreendo sua dúvida sobre o investimento. No meu escritório, nós não trabalhamos com valores iguais porque cada caso exige um empenho técnico diferente.\n\n"
            "Como o seu caso envolve a liberação de Consulta ou Exame, a Dra. Lethicia faz questão de analisar pessoalmente a documentação na mesa de trabalho antes de passar qualquer orçamento.\n\n"
            "Valores para esse tipo de demanda são informados somente após essa triagem técnica, garantindo que o valor seja justo e condizente com a complexidade do seu pedido. Assim que ela analisar seus documentos, você receberá o retorno."
        )
    
    # Cenário 3: Reajustes, Contratos (Plano de Saúde)
    elif "Consultoria" in ps_busca or "Reajuste" in ps_busca or "Coparticipação" in ps_busca:
        return (
            "Compreendo sua dúvida sobre o investimento. No meu escritório, tratamos cada contrato de forma individualizada, pois os valores de reajuste e as cláusulas variam drasticamente entre as operadoras.\n\n"
            "Como o seu caso envolve uma análise financeira e contratual detalhada, a Dra. Lethicia não define valores por mensagem de texto.\n\n"
            "É necessário uma **Reunião Estratégica** (vídeo ou áudio) para que ela te explique como buscaremos o reequilíbrio do seu plano e a restituição de valores pagos indevidamente, alinhando o investimento da consultoria nessa etapa."
        )
    
    else:
        return "Compreendo sua dúvida sobre o investimento. Para te passar um valor justo, a Dra. Lethicia precisa entender melhor a complexidade do seu caso. Vamos continuar com as perguntas para que eu possa coletar os dados necessários?"

def init_session():
    """Inicializa variáveis de sessão"""
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
    if "perguntas" not in st.session_state:
        st.session_state.perguntas = []

def add_bot(msg: str):
    """Adiciona mensagem do bot"""
    if msg:
        msg = msg.replace("{nome}", st.session_state.nome or "")
        msg = msg.replace("{lawyer}", L)
        msg = msg.replace("{CALENDLY_LINK}", CALENDLY_LINK)
        st.session_state.messages.append({"role": "bot", "content": msg})

def add_user(msg: str):
    """Adiciona mensagem do usuário"""
    st.session_state.messages.append({"role": "user", "content": msg})

def reset():
    """Reseta a conversa"""
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
# FLUXO SUS - MENSAGENS
# ============================================

MSG_SUS_DEMANDA = "Me diga o que você está aguardando?\n\n🔪 Cirurgia / Tratamento\n\n📋 Consultas / Exames"

MSG_SUS_EXAME_INICIO = "Entendi… vamos ver isso com calma 💙\n\n👉 Qual exame o médico solicitou pra você?"

MSG_SUS_EXAME_FINALIDADE = (
    "Esse exame que você precisa é para qual finalidade principal?\n\n"
    "1️⃣ **Diagnóstico:** Para descobrir o que eu tenho.\n"
    "2️⃣ **Pré-operatório:** Para eu conseguir operar logo.\n"
    "3️⃣ **Confirmação:** O médico suspeita de cirurgia e precisa do exame para decidir."
)

PERGUNTAS_EXAME_OP1 = [
    "Entendi... 👉 o médico comentou o que pode estar sendo investigado com esse exame? (se puder me explicar, ajuda muito)",
    "👉 o médico comentou se existe urgência ou risco em não realizar esse exame?",
    "👉 você está aguardando há quanto tempo mais ou menos?",
    "Quem te pediu esse exame foi o médico especialista ou o médico do postinho/UBS?",
    "👉 você recebeu algum comprovante do SUS? (Pode ser agendamento; protocolo; print do aplicativo meu SUS; posição na fila)"
]

PERGUNTAS_EXAME_OP2 = [
    "Perfeito... 👉 você já tem indicação de cirurgia e esse exame é pra poder realizar o procedimento, certo? Se quiser, pode me explicar melhor o que falta.",
    "👉 você está aguardando há quanto tempo mais ou menos?",
    "Qual cirurgia que você precisa fazer?",
    "Quem te pediu esse exame foi o médico especialista ou o médico do postinho/UBS?",
    "Essa cirurgia ela é urgente ou não? Tem laudo médico atestando essa urgência?",
    "👉 você recebeu algum comprovante do SUS? (Pode ser agendamento; protocolo; print do aplicativo meu SUS; posição na fila)"
]

PERGUNTAS_EXAME_OP3 = [
    "Entendi.. 👉 o médico já suspeita que você pode precisar de qual tipo de cirurgia?",
    "Quais sintomas você apresentou pro médico pedir esse exame?",
    "👉 o médico comentou se existe urgência ou risco em não realizar esse exame?",
    "👉 você está aguardando há quanto tempo mais ou menos?",
    "👉 você recebeu algum comprovante do SUS? (Pode ser agendamento; protocolo; print do aplicativo meu SUS; posição na fila)"
]

MSG_SUS_CONSULTA_INICIO = (
    "Entendi que você está aguardando uma consulta especializada. "
    "Deixa eu te perguntar: você já está nessa fila de espera há mais de 30 dias ou o seu caso tem um prazo de urgência que o SUS simplesmente ignorou?"
)

PERGUNTAS_CONSULTA = [
    "Qual especialidade médica você está aguardando?",
    "Você tem encaminhamento ou pedido médico pra essa consulta?",
    "Entendi...\n\nVocê está aguardando há quanto tempo mais ou menos?",
    "O que te informaram quando você questionou sua posição na fila ou quando você foi tentar marcar? (fila, falta de médico, sem previsão...)",
    "Você teria algum exame informando a condição de saúde que tem?"
]

MSG_SUS_ESPECIALIDADE_ESCOLHA = (
    "Para que eu direcione você para o protocolo de urgência correto, qual problema estamos enfrentando hoje?\n\n"
    "1️⃣ Oncologia\n2️⃣ Neurodivergências (TEA, TDAH)\n3️⃣ Endometriose / Adenomiose\n"
    "4️⃣ Medicamento\n5️⃣ Bariátrica\n6️⃣ Cardiologia\n7️⃣ Outros"
)

PERGUNTAS_SUS_ONCO = [
    "Entendi... vamos cuidar disso juntos 💙\n\n👉 Você consegue me contar qual é o tipo de câncer?",
    "👉 Você está aguardando atendimento ou tratamento pelo SUS? Se sim, há quanto tempo mais ou menos?",
    "Só pra eu entender melhor seu caso:\n\n👉 O diagnóstico já foi confirmado por biópsia? E você tem esse laudo em mãos?",
    "Entendi...\n\n👉 Você já foi encaminhado para um hospital especializado em câncer (oncologia) pelo SUS ou ainda nem conseguiu passar com um especialista?\n\nInfelizmente, a fila do SUS não respeita o avanço da doença. Se o hospital não iniciou seu tratamento em 60 dias, a lei está sendo descumprida e precisamos forçar o início imediato via Justiça.",
    "👉 Você possui um relatório médico explicando o tratamento que precisa fazer? (se quiser, pode enviar aqui também 📎)",
    "Última perguntinha, que é bem importante:\n\n👉 O médico falou se o seu caso é urgente?",
    "Você possui o comprovante de que está aguardando na fila? (Print do Meu SUS Digital, agendamento ou papel do SISREG)."
]

MSG_NEURO_REESTRUTURADA = (
    "Entendo as batalhas diárias que você enfrenta para garantir o melhor para quem você ama. "
    "Seja você ou seu filho(a) não deve ter seu desenvolvimento barrado por limites impostos pelo **SUS**. "
    "Estou aqui para lutar ao seu lado e garantir todas as terapias que são de direito. "
    "Agora me conta uma coisa importante: 👉 Quais terapias o médico indicou? (ABA, Psico, fisioterapia...)"
)

PERGUNTAS_SUS_NEURO = [
    "Entendi... pode ficar tranquilo(a), vou te ajudar com isso 💙. Casos assim realmente precisam de atenção, principalmente por envolver desenvolvimento.\n\n👉 Me conta: já tem diagnóstico fechado ou ainda está em investigação?",
    "👉 Você tem algum laudo ou relatório médico com o diagnóstico?",
    MSG_NEURO_REESTRUTURADA,
    "E hoje, como está essa situação no SUS?\n\n👉 Você conseguiu iniciar as terapias ou ainda está aguardando?",
    "Entendo...\n\n👉 Você está em fila ou aguardando vaga?",
    "Essa parte é muito importante:\n\n👉 O médico comentou algo sobre prejuízo no desenvolvimento ou necessidade de iniciar rápido as terapias?",
    "Se você puder me contar:\n\n👉 Como essa situação está impactando o dia a dia de vocês?",
    "Você possui o comprovante de que está aguardando na fila? (Print do Meu SUS Digital, agendamento ou SISREG)."
]

PERGUNTAS_SUS_ENDO = [
    "Entendi... imagino o quanto isso pode estar sendo difícil pra você 🥺. Mas fica tranquila, vou te ajudar com isso 💙.\n\n👉 Você já tem diagnóstico confirmado de endometriose ou adenomiose?",
    "Obrigado por me contar 🙏.\n\n👉 Esse diagnóstico foi feito por exame? Se ainda não fez, qual exame está aguardando?",
    "Sei o quanto a dor e a incerteza cansam... não é justo que sua cirurgia ou exame continue demorando assim.\n\n👉 Você sente dores fortes ou crises que atrapalham sua rotina?",
    "Agora uma parte bem importante:\n\n👉 O médico indicou algum tratamento específico? (Ex: cirurgia de videolaparoscopia, medicamento...)",
    "👉 Você tem relatório médico explicando esse tratamento?",
    "👉 Você está aguardando há quanto tempo mais ou menos?",
    "👉 O médico colocou em relatório ou te informou se existe risco de piora ou agravamento sem o tratamento?",
    "Você possui o comprovante de que está aguardando na fila?"
]

PERGUNTAS_SUS_MED = [
    "Entendi... vamos ver isso com calma 💙.\n\n👉 Qual foi o medicamento que o médico indicou pra você?",
    "Perfeito, obrigado por me explicar 🙏.\n\n👉 Você tem a receita ou relatório médico desse medicamento?",
    "Entendo a frustração de ter um direito negado justamente quando você mais precisa de suporte... Ao te passar esse medicamento o seu médico escreveu no laudo que este remédio específico é o único que pode tratar seu caso agora e que a interrupção trará riscos à sua vida ou saúde?",
    "Essa parte é bem importante:\n\n👉 Você já utilizou outros medicamentos antes? Se sim, eles não tiveram resultado ou causaram algum problema?",
    "👉 Você já chegou a solicitar esse medicamento pelo SUS ou farmácia de alto custo? O que te informaram? (Negado, em análise, falta de estoque...)",
    "👉 O médico comentou o que pode acontecer se você não usar esse medicamento?"
]

PERGUNTAS_SUS_BARI = [
    "Entendi... vamos ver isso com calma 💙.\n\n👉 Você já tem indicação médica para cirurgia bariátrica?",
    "👉 Você tem algum laudo ou relatório médico indicando a cirurgia?",
    "Só pra eu entender melhor seu caso:\n\n👉 Você sabe me informar seu peso e altura? (Pode ser aproximado).",
    "Essa parte é bem importante:\n\n👉 Você já tentou outros tratamentos antes, como dieta, acompanhamento ou medicamentos? Como foi essa experiência?",
    "Você já está na fila de espera do SUS há quanto tempo? Você possui o comprovante de que está aguardando na fila?"
]

PERGUNTAS_SUS_CARDIO = [
    "Entendi... vamos ver isso com calma 💙.\n\n👉 Você consegue me explicar qual é o problema cardíaco ou o que o médico te disse?",
    "O seu caso envolve uma cirurgia de urgência (Ponte de safena, troca de válvula, marca-passo/Stent)?",
    "👉 Você tem algum exame ou laudo do coração? (Eletro, eco, cateterismo...)",
    "Quais sintomas você tem sentido? (Dor no peito, falta de ar, tontura, cansaço excessivo).",
    "👉 O médico indicou algum tratamento ou procedimento?",
    "👉 Você tem relatório médico explicando essa necessidade?",
    "Você possui o comprovante de que está aguardando na fila?"
]

PERGUNTAS_SUS_OUTROS = [
    "Entendi... como o seu caso é específico, eu preciso entender o que está acontecendo para te direcionar corretamente.\n\n👉 Poderia me dizer qual é a sua condição/doença?",
    "👉 Você já tem algum diagnóstico ou ainda está investigando?",
    "👉 Algum médico já te passou relatório ou pedido de tratamento?",
    "Vamos resolver isso juntos...\n\n👉 O médico comentou se existe urgência ou risco em não realizar esse tratamento?",
    "👉 O que acontece com a sua saúde se você não conseguir isso nos próximos 30 ou 90 dias? Existe risco de agravamento ou sequela irreversível?",
    "👉 Como essa situação tem afetado sua vida hoje?",
    "Você possui o comprovante de que está aguardando na fila?"
]

MSG_SUS_RISCO_SAUDE = (
    "{nome}, recebi suas respostas aqui. O que mais me preocupa no seu caso é que o SUS trata essa necessidade como se pudesse esperar, "
    "mas juridicamente sabemos que o tempo é o seu maior inimigo agora.\n\n"
    "Você sente que, se não resolvermos isso nos próximos dias, a sua saúde corre um risco de piorar de forma irreversível?"
)

MSG_SUS_PITCH_PROTOCOLO = (
    "O Judiciário entende que o Estado não tem o direito de te deixar em uma fila infinita quando existe risco de agravamento. "
    "Você quer continuar contando com a sorte do sistema ou quer que a Dra. Lethicia force o governo a cumprir a lei agora?\n\n"
    "Para resolver isso, eu trabalho com um **Protocolo de Liberação Urgente**. Buscamos a sua consulta/exame/cirurgia com urgência para tirar você da fila. "
    "Isso faria diferença na sua vida agora?"
)

MSG_SUS_HONORARIOS_INICIAIS = (
    "Como é um trabalho de alta especialidade, o escritório cobra Honorários Iniciais para assumir o caso e entrar com um processo judicial. "
    "Prosseguir com esse caso faz sentido para você garantir sua saúde hoje e sair dessa espera?"
)

MSG_SUS_ENCERRAMENTO = (
    "Compreendo. Infelizmente, sem o interesse em avançar com uma medida judicial, o seu caso continuará dependendo exclusivamente da velocidade da fila do SUS.\n\n"
    "Como o escritório da Dra. Lethicia foca apenas em quem deseja forçar a solução imediata, estamos encerrando seu atendimento por aqui.\n\n"
    "Caso a sua situação se agrave ou você decida que não pode mais esperar, sinta-se à vontade para retornar. Desejamos sorte no seu tratamento."
)

# ============================================
# FLUXO PLANO DE SAÚDE - MENSAGENS (CORRIGIDAS)
# ============================================

PS_BUSCA = (
    "Obrigado por todas as informações. Já consigo ter um bom entendimento da sua situação.\n\n"
    "Agora me diz: o que você está buscando nesse momento? Escolha a opção que mais se encaixa com onde você está agora:\n\n"
    "1️⃣ **Quero entender se o plano de saúde é obrigado a cobrir determinado tratamento** ou Tenho uma dúvida específica ou um caso diferente e gostaria de orientação jurídica para entender quais são meus direitos e possibilidades.\n\n"
    "2️⃣ **Já tenho a negativa do plano:** Desejo orientação especializada para ingressar com a ação judicial e buscar a liberação do meu tratamento.\n\n"
    "3️⃣ **Ainda não tenho a negativa, mas preciso me preparar:** Quero me antecipar, eu ainda não recebi a negativa do plano, mas sei que meu pedido pode ser recusado. Quero me preparar da forma correta, com orientação jurídica, para aumentar minhas chances de aprovação do tratamento ou sucesso na ação judicial.\n\n"
    "4️⃣ **Preciso de uma consultoria jurídica:** Desejo uma análise técnica sobre o meu caso de saúde. Indicado para dúvidas sobre reajustes abusivos (anual ou por faixa etária), períodos de carência, migração de plano (portabilidade) ou para saber se um tratamento específico tem cobertura obrigatória pela ANS."
)

PS_OP1_MSG = (
    "Perfeito! Para esse tipo de dúvida pontual, oferecemos o **Atendimento Expresso**. "
    "Diferente da consultoria completa, aqui você envia sua dúvida e um especialista te responde de forma técnica e direta, "
    "analisando se o seu direito é garantido por lei. Isso te ajudaria?"
)

PS_OP1_INVESTIMENTO = (
    "O investimento no atendimento particular é de **R$ 97,00** e é feito online.\n\n"
    "É um atendimento individual e aprofundado onde você terá os seguintes benefícios:\n"
    "• **Resposta Técnica Direta:** Esclarecimento sobre a obrigatoriedade de cobertura (Rol da ANS e entendimentos judiciais recentes).\n"
    "• **Análise de Viabilidade:** Uma opinião profissional sobre se o seu caso tem chances reais de sucesso na justiça ou se é uma questão administrativa.\n"
    "• **Indicação de Documentos:** Lista do que você precisa providenciar imediatamente para não perder seus direitos.\n\n"
    "Podemos marcar um horário pra você na agenda da Dra Lethicia?"
)

PS_OP1_PAGAMENTO = (
    "Perfeito! Vamos reservar o seu horário.\n\n"
    "**Passo 1:** Escolha o melhor dia e hora no link abaixo:\n"
    f"{CALENDLY_LINK}\n\n"
    "**Passo 2:** Após escolher o horário, realize o pagamento da consultoria. "
    "Você vai realizar o pagamento via **Pix** ou **Cartão de Crédito**?"
)

PS_OP4_MSG = (
    "Entendido. Para casos de análise contratual, reajustes ou dúvidas preventivas, realizamos uma **Consultoria Jurídica Especializada**.\n\n"
    "Nesta reunião online um advogado especialista em Direito da Saúde analisará detalhadamente o seu caso, documentos e contratos "
    "para te entregar um parecer seguro sobre os seus direitos.\n\n"
    "**Informações sobre a Consultoria:**\n"
    "• **Investimento:** R$ 500,00 (referente à análise técnica e reserva de horário).\n"
    "• **Duração:** Até 1 hora.\n"
    "• **Objetivo:** Diagnóstico completo e estratégia jurídica personalizada.\n\n"
    "Deseja prosseguir com o agendamento?"
)

PS_OP4_PAGAMENTO = (
    "Perfeito! Vamos reservar o seu horário.\n\n"
    "**Passo 1:** Escolha o melhor dia e hora no link abaixo:\n"
    f"{CALENDLY_LINK}\n\n"
    "**Passo 2:** Após escolher o horário, realize o pagamento da consultoria. "
    "Você vai realizar o pagamento via **Pix** ou **Cartão de Crédito**?"
)

PS_NEGATIVA_JUDICIAL = (
    "Nesse caso só é possível revertermos a negativa do plano com medidas judiciais. "
    "Você está no momento exato de agirmos para buscar o seu direito judicialmente. "
    "Agora não é mais hora de esperar, é hora de exigir que o plano de saúde cumpra a lei.\n\n"
    "O próximo passo agora é uma reunião rápida para eu te explicar como funciona o processo e valores de honorários.\n\n"
    "Antes de agendarmos: além de você, tem mais alguém que participe das decisões familiares ou financeiras, "
    "como seu esposo/esposa, que seria importante estar presente para já tirarmos todas as dúvidas de uma vez?"
)

DECISAO_SIM_MSG = (
    "Excelente! É fundamental que ele(a) participe, pois como o Direito à Saúde envolve prazos muito curtos e decisões imediatas "
    "sobre o tratamento, é bom que todos estejam na mesma página.\n\n"
    "Vamos escolher um horário que fique confortável para vocês dois... Logo abaixo vou te mandar a agenda da Dra Lethicia:\n\n"
    f"{CALENDLY_LINK}"
)

DECISAO_NAO_MSG = (
    "Perfeito, facilita bastante o nosso fluxo. Como você é a única responsável pela decisão, "
    "conseguimos dar um andamento mais ágil aos trabalhos... Logo abaixo vou te mandar a agenda da Dra Lethicia:\n\n"
    f"{CALENDLY_LINK}"
)

DECISAO_REPASSE_MSG = (
    "Entendo! Olha, eu sugiro fortemente que ele tente participar, nem que seja apenas nos primeiros 10 minutos. "
    "No Direito à Saúde, os detalhes técnicos sobre a negativa da operadora costumam gerar muitas dúvidas e, "
    "se ele ouvir direto de mim, vocês ganham muito mais segurança para decidir rápido.\n\n"
    "Conseguimos um horário em que ele possa entrar na chamada, ou prefere manter só entre nós por enquanto?"
)

DECISAO_REPASSE_COM = (
    f"Logo abaixo vou te mandar a agenda da Dra Lethicia, e você marque o dia e horário que fica melhor pra você:\n\n{CALENDLY_LINK}"
)

MSG_ENCERRAMENTO_NAO = (
    "Entendo perfeitamente e respeito sua decisão.\n\n"
    "Vou encerrar o seu atendimento por aqui para priorizar os casos que já estão com liminares em andamento. "
    "Lembre-se apenas que, no Direito da Saúde, o tempo é um fator determinante para o sucesso do tratamento.\n\n"
    "Caso precise de suporte especializado no futuro, nossos canais continuam à disposição."
)

# ============================================
# LÓGICA DE PROCESSAMENTO
# ============================================

def processar(resposta: str):
    """Processa a resposta do usuário e avança o fluxo"""
    estado = st.session_state.estado
    dados = st.session_state.dados

    # Detecção de pergunta sobre valores (SEMPRE VERIFICAR PRIMEIRO)
    if detectar_pergunta_valor(resposta):
        add_bot(responder_valor(dados))
        return

    # --- INÍCIO ---
    if estado == "INICIO":
        st.session_state.nome = resposta
        st.session_state.estado = "CANAL"
        add_bot(MSG_CANAL)

    elif estado == "CANAL":
        if "plano" in _n(resposta):
            dados["canal"] = "Plano de Saúde"
            st.session_state.estado = "PS_BUSCA"
            add_bot(PS_BUSCA)
        else:
            dados["canal"] = "SUS"
            st.session_state.estado = "SUS_DEMANDA"
            add_bot(MSG_SUS_DEMANDA)

    # --- FLUXO SUS ---
    elif estado == "SUS_DEMANDA":
        if "cirurgia" in _n(resposta):
            dados["sus_tipo"] = "Cirurgia"
            st.session_state.estado = "SUS_ESPECIALIDADE"
            add_bot(MSG_SUS_ESPECIALIDADE_ESCOLHA)
        else:
            dados["sus_tipo"] = "Consulta/Exame"
            st.session_state.estado = "SUS_EXAME_OU_CONSULTA"
            add_bot("Você está aguardando um **Exame** ou uma **Consulta Especializada**?")

    elif estado == "SUS_EXAME_OU_CONSULTA":
        if "exame" in _n(resposta):
            st.session_state.estado = "SUS_EXAME_INICIO"
            add_bot(MSG_SUS_EXAME_INICIO)
        else:
            st.session_state.estado = "SUS_CONSULTA_INICIO"
            add_bot(MSG_SUS_CONSULTA_INICIO)

    # --- SUS EXAMES ---
    elif estado == "SUS_EXAME_INICIO":
        dados["exame_nome"] = resposta
        st.session_state.estado = "SUS_EXAME_FINALIDADE"
        add_bot(MSG_SUS_EXAME_FINALIDADE)

    elif estado == "SUS_EXAME_FINALIDADE":
        if "1" in resposta:
            dados["exame_op"] = "OP1"
            st.session_state.perguntas = PERGUNTAS_EXAME_OP1
        elif "2" in resposta:
            dados["exame_op"] = "OP2"
            st.session_state.perguntas = PERGUNTAS_EXAME_OP2
        else:
            dados["exame_op"] = "OP3"
            st.session_state.perguntas = PERGUNTAS_EXAME_OP3
        st.session_state.pergunta_idx = 0
        st.session_state.estado = "SUS_PERGUNTAS_LOOP"
        add_bot(st.session_state.perguntas[0])

    # --- SUS CONSULTAS ---
    elif estado == "SUS_CONSULTA_INICIO":
        st.session_state.perguntas = PERGUNTAS_CONSULTA
        st.session_state.pergunta_idx = 0
        st.session_state.estado = "SUS_PERGUNTAS_LOOP"
        add_bot(st.session_state.perguntas[0])

    # --- SUS ESPECIALIDADES ---
    elif estado == "SUS_ESPECIALIDADE":
        esp = _n(resposta)
        if "onco" in esp or "1" in resposta:
            dados["sus_tipo"] = "Oncologia"
            st.session_state.perguntas = PERGUNTAS_SUS_ONCO
        elif "neurodiver" in esp or "2" in resposta:
            dados["sus_tipo"] = "Neurodivergências"
            st.session_state.perguntas = PERGUNTAS_SUS_NEURO
        elif "endo" in esp or "3" in resposta:
            dados["sus_tipo"] = "Endometriose"
            st.session_state.perguntas = PERGUNTAS_SUS_ENDO
        elif "med" in esp or "4" in resposta:
            dados["sus_tipo"] = "Medicamento"
            st.session_state.perguntas = PERGUNTAS_SUS_MED
        elif "bari" in esp or "5" in resposta:
            dados["sus_tipo"] = "Bariátrica"
            st.session_state.perguntas = PERGUNTAS_SUS_BARI
        elif "cardio" in esp or "6" in resposta:
            dados["sus_tipo"] = "Cardiologia"
            st.session_state.perguntas = PERGUNTAS_SUS_CARDIO
        else:
            dados["sus_tipo"] = "Outros"
            st.session_state.perguntas = PERGUNTAS_SUS_OUTROS
        st.session_state.pergunta_idx = 0
        st.session_state.estado = "SUS_PERGUNTAS_LOOP"
        add_bot(st.session_state.perguntas[0])

    # --- LOOP DE PERGUNTAS SUS ---
    elif estado == "SUS_PERGUNTAS_LOOP":
        idx = st.session_state.pergunta_idx
        dados[f"pergunta_{idx}"] = resposta
        idx += 1
        if idx < len(st.session_state.perguntas):
            st.session_state.pergunta_idx = idx
            add_bot(st.session_state.perguntas[idx])
        else:
            st.session_state.estado = "SUS_RISCO_SAUDE"
            add_bot(MSG_SUS_RISCO_SAUDE)

    elif estado == "SUS_RISCO_SAUDE":
        st.session_state.estado = "SUS_PITCH"
        add_bot(MSG_SUS_PITCH_PROTOCOLO)

    elif estado == "SUS_PITCH":
        if _sim(resposta):
            st.session_state.estado = "SUS_HONORARIOS"
            add_bot(MSG_SUS_HONORARIOS_INICIAIS)
        else:
            add_bot(MSG_SUS_ENCERRAMENTO)
            st.session_state.estado = "FIM"

    elif estado == "SUS_HONORARIOS":
        if _sim(resposta):
            st.session_state.estado = "DECISAO_PERGUNTA"
            add_bot(PS_NEGATIVA_JUDICIAL)
        else:
            add_bot(MSG_SUS_ENCERRAMENTO)
            st.session_state.estado = "FIM"

    # --- FLUXO PLANO DE SAÚDE (CORRIGIDO) ---
    elif estado == "PS_BUSCA":
        if "1" in resposta:
            dados["ps_busca"] = "Dúvida Cobertura"
            st.session_state.estado = "PS_OP1_PERGUNTA"
            add_bot(PS_OP1_MSG)
        elif "2" in resposta or "3" in resposta:
            dados["ps_busca"] = "Negativa Judicial"
            st.session_state.estado = "DECISAO_PERGUNTA"
            add_bot(PS_NEGATIVA_JUDICIAL)
        elif "4" in resposta:
            dados["ps_busca"] = "Consultoria Técnica"
            st.session_state.estado = "PS_OP4_PERGUNTA"
            add_bot(PS_OP4_MSG)

    elif estado == "PS_OP1_PERGUNTA":
        if _sim(resposta):
            st.session_state.estado = "PS_OP1_INVESTIMENTO_MSG"
            add_bot(PS_OP1_INVESTIMENTO)
        else:
            add_bot(MSG_ENCERRAMENTO_NAO)
            st.session_state.estado = "FIM"

    elif estado == "PS_OP1_INVESTIMENTO_MSG":
        if _sim(resposta):
            st.session_state.estado = "PS_OP1_PAGAMENTO_METODO"
            add_bot(PS_OP1_PAGAMENTO)
        else:
            add_bot(MSG_ENCERRAMENTO_NAO)
            st.session_state.estado = "FIM"

    elif estado == "PS_OP1_PAGAMENTO_METODO":
        if "cartão" in _n(resposta):
            add_bot(f"✅ Aqui está o link para pagamento via **Cartão de Crédito**:\n\n{LINK_CARTAO_97}\n\nApós realizar o pagamento, você receberá um e-mail de confirmação com as instruções para a reunião.")
            st.session_state.estado = "FIM"
        elif "pix" in _n(resposta):
            add_bot(f"✅ Aqui está o link para pagamento via **Pix**:\n\n{LINK_PIX_97}\n\nApós realizar o pagamento, você receberá um e-mail de confirmação com as instruções para a reunião.")
            st.session_state.estado = "FIM"

    elif estado == "PS_OP4_PERGUNTA":
        if _sim(resposta):
            st.session_state.estado = "PS_OP4_PAGAMENTO_METODO"
            add_bot(PS_OP4_PAGAMENTO)
        else:
            add_bot(MSG_ENCERRAMENTO_NAO)
            st.session_state.estado = "FIM"

    elif estado == "PS_OP4_PAGAMENTO_METODO":
        if "cartão" in _n(resposta):
            add_bot(f"✅ Aqui está o link para pagamento via **Cartão de Crédito**:\n\n{LINK_CARTAO_500}\n\nApós realizar o pagamento, você receberá um e-mail de confirmação com as instruções para a reunião.")
            st.session_state.estado = "FIM"
        elif "pix" in _n(resposta):
            add_bot(f"✅ Aqui está o link para pagamento via **Pix**:\n\n{LINK_PIX_500}\n\nApós realizar o pagamento, você receberá um e-mail de confirmação com as instruções para a reunião.")
            st.session_state.estado = "FIM"

    # --- DECISÃO E AGENDAMENTO ---
    elif estado == "DECISAO_PERGUNTA":
        if "conjuge" in _n(resposta) or "sim" in _n(resposta):
            st.session_state.estado = "FIM"
            add_bot(DECISAO_SIM_MSG)
        elif "sozinho" in _n(resposta) or _nao(resposta):
            st.session_state.estado = "FIM"
            add_bot(DECISAO_NAO_MSG)
        elif "repasso" in _n(resposta) or "tem" in _n(resposta):
            st.session_state.estado = "DECISAO_REPASSE"
            add_bot(DECISAO_REPASSE_MSG)

    elif estado == "DECISAO_REPASSE":
        st.session_state.estado = "FIM"
        add_bot(DECISAO_REPASSE_COM)

# ============================================
# INTERFACE STREAMLIT
# ============================================

def main():
    st.title("⚖️ Iara Bot - Assistente Jurídica em Direito da Saúde")
    st.caption(f"Especialista: {L} | Atendimento: SUS, Planos de Saúde e INSS")

    init_session()

    # Sidebar
    with st.sidebar:
        st.markdown("### 📋 Informações da Sessão")
        if st.session_state.nome:
            st.info(f"**Cliente:** {st.session_state.nome}")
        if st.session_state.dados.get("canal"):
            st.info(f"**Canal:** {st.session_state.dados['canal']}")
        if st.session_state.dados.get("sus_tipo"):
            st.info(f"**Tipo:** {st.session_state.dados['sus_tipo']}")

        st.markdown("---")
        if st.button("🔄 Nova Conversa", use_container_width=True):
            reset()
            st.rerun()

        st.markdown("---")
        st.markdown("### 📝 Sobre Iara Bot")
        st.markdown(
            "Assistente jurídico inteligente especializado em Direito da Saúde. "
            "Qualifica automaticamente casos de SUS, Planos de Saúde e INSS."
        )

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

        elif estado == "SUS_EXAME_OU_CONSULTA":
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("🔬 Exame", use_container_width=True):
                    add_user("Exame")
                    processar("Exame")
                    st.rerun()
            with col_b:
                if st.button("👨‍⚕️ Consulta", use_container_width=True):
                    add_user("Consulta")
                    processar("Consulta")
                    st.rerun()

        elif estado == "SUS_EXAME_FINALIDADE":
            if st.button("1️⃣ Diagnóstico", use_container_width=True):
                add_user("Diagnóstico")
                processar("1")
                st.rerun()
            if st.button("2️⃣ Pré-operatório", use_container_width=True):
                add_user("Pré-operatório")
                processar("2")
                st.rerun()
            if st.button("3️⃣ Confirmação", use_container_width=True):
                add_user("Confirmação")
                processar("3")
                st.rerun()

        elif estado == "SUS_ESPECIALIDADE":
            especialidades = ["Oncologia", "Neurodivergências", "Endometriose", "Medicamento", "Bariátrica", "Cardiologia", "Outros"]
            cols = st.columns(2)
            for i, esp in enumerate(especialidades):
                with cols[i % 2]:
                    if st.button(esp, use_container_width=True):
                        add_user(esp)
                        processar(str(i+1))
                        st.rerun()

        elif estado == "SUS_PITCH":
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("⚖️ Quero ajuda da Dra. Lethicia", use_container_width=True):
                    add_user("Quero ajuda")
                    processar("ajuda")
                    st.rerun()
            with col_b:
                if st.button("⏳ Quero aguardar", use_container_width=True):
                    add_user("Quero aguardar")
                    processar("aguardar")
                    st.rerun()

        elif estado in ["PS_OP1_PERGUNTA", "PS_OP1_INVESTIMENTO_MSG", "PS_OP4_PERGUNTA", "SUS_HONORARIOS"]:
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
            options = ["1️⃣ Dúvida Cobertura", "2️⃣ Já tenho Negativa", "3️⃣ Vou ter Negativa", "4️⃣ Consultoria Técnica"]
            cols = st.columns(2)
            for i, opt in enumerate(options):
                with cols[i % 2]:
                    if st.button(opt, use_container_width=True):
                        add_user(opt)
                        processar(str(i+1))
                        st.rerun()

        elif estado in ["PS_OP1_PAGAMENTO_METODO", "PS_OP4_PAGAMENTO_METODO"]:
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

        elif estado == "DECISAO_PERGUNTA":
            if st.button("👨‍👩‍👧 Sim, meu cônjuge/familiar", use_container_width=True):
                add_user("Sim, meu cônjuge/familiar")
                processar("conjuge")
                st.rerun()
            if st.button("👤 Não, eu decido tudo sozinho(a)", use_container_width=True):
                add_user("Não, eu decido tudo sozinho(a)")
                processar("sozinho")
                st.rerun()
            if st.button("📞 Tem meu cônjuge, mas pode falar comigo", use_container_width=True):
                add_user("Tem meu cônjuge, mas pode falar comigo")
                processar("repasso")
                st.rerun()

        elif estado == "DECISAO_REPASSE":
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("👥 Com ele(a)", use_container_width=True):
                    add_user("Com ele(a)")
                    processar("com ele")
                    st.rerun()
            with col_b:
                if st.button("👤 Entre nós", use_container_width=True):
                    add_user("Entre nós")
                    processar("entre nós")
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
