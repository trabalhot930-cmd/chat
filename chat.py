import streamlit as st
import re
from datetime import datetime

# ============================================
# CONFIGURAÇÕES
# ============================================
st.set_page_config(
    page_title="Iara Bot - Assistente Jurídica",
    page_icon="⚖️",
    layout="wide"
)

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
    .sidebar-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# TEXTOS DO FLUXO (IGUAL AO ORIGINAL)
# ============================================

MSG_BOAS_VINDAS = (
    "Olá, seja bem vindo(a). 🌹\n"
    "Sou a Iara, assistente jurídica do escritório da Dra. Lethicia Fernanda, "
    "advogada especialista em Direito da Saúde.\n\n"
    "Fico feliz que você entrou em contato conosco.\n\n"
    "Qual o seu nome?"
)

MSG_SUS_OU_PLANO = (
    "Olá, {nome}! 😊\n\n"
    "Seu atendimento é pelo *SUS* ou por *Plano de Saúde*?\n\n"
    "1️⃣ SUS\n"
    "2️⃣ Plano de Saúde"
)

MSG_SUS_DEMANDA = (
    "Me diga o que você está aguardando?\n\n"
    "1️⃣ Cirurgia / Tratamento\n"
    "2️⃣ Consultas / Exames"
)

MSG_SUS_ESPECIALIDADE = (
    "Para que eu direcione você para o protocolo de urgência correto, "
    "qual problema estamos enfrentando hoje?\n\n"
    "1️⃣ Oncologia\n"
    "2️⃣ Neurodivergências (TEA, TDAH)\n"
    "3️⃣ Endometriose / Adenomiose\n"
    "4️⃣ Medicamento\n"
    "5️⃣ Bariátrica\n"
    "6️⃣ Reparadora\n"
    "7️⃣ Neurologia / Neurocirurgia\n"
    "8️⃣ Cardiologia\n"
    "9️⃣ Outros"
)

MSG_SUS_CONSULTA_ESPECIALIDADE = (
    "Para que eu direcione você para o protocolo correto, "
    "qual problema estamos enfrentando hoje?\n\n"
    "1️⃣ Oncologia\n"
    "2️⃣ Bariátrica\n"
    "3️⃣ Reparadora\n"
    "4️⃣ Endometriose / Adenomiose\n"
    "5️⃣ Cardiologia\n"
    "6️⃣ Neurologia\n"
    "7️⃣ Exame específico\n\n"
    "👆 Clique ou digite o número da especialidade que você precisa."
)

MSG_SUS_CONSULTA_TIPO = (
    "Você está buscando:\n\n"
    "1️⃣ Consulta com especialista\n"
    "2️⃣ Realização de Exame"
)

MSG_PLANO_CARENCIA = (
    "Você já tem seu plano de saúde há mais de 2 anos?\n\n"
    "1️⃣ Sim\n"
    "2️⃣ Não"
)

MSG_PLANO_SITUACAO = (
    "Para que eu possa te direcionar corretamente, qual é a sua situação atual com o plano de saúde?\n\n"
    "1️⃣ Cirurgia Reparadora\n"
    "2️⃣ Negativa de Cirurgia\n"
    "3️⃣ Medicamento Negado\n"
    "4️⃣ Exame Negado\n"
    "5️⃣ Home Care\n"
    "6️⃣ Terapias (fono, ABA, fisio...)\n"
    "7️⃣ Reajuste Abusivo\n"
    "8️⃣ Coparticipação Elevada\n"
    "9️⃣ Erro Médico\n"
    "🔟 Outro"
)

MSG_PLANO_SEM_CARENCIA = (
    "Entendo! Muitas pessoas acreditam que precisam esperar 2 anos para ter direito a cirurgias ou tratamentos complexos, "
    "mas a lei nem sempre funciona assim.\n\n"
    "Me conta, qual o tratamento que você precisa fazer?"
)

MSG_POS_PERGUNTAS_SUS = (
    "Pelos dados que você enviou, fica claro que o seu caso não é apenas uma 'espera comum'. "
    "No SUS, o governo muitas vezes usa a fila da regulação para camuflar a falta de investimento. "
    "Enquanto o sistema diz que você deve aguardar, a sua saúde paga um preço que pode ser irreversível.\n\n"
    "{nome}, o que mais me preocupa no seu caso é que o SUS trata isso como se pudesse esperar, "
    "mas juridicamente sabemos que o tempo é o seu maior inimigo agora.\n\n"
    "Você sente que, se não resolvermos isso nos próximos dias, a sua saúde corre risco de piorar de forma irreversível?"
)

MSG_PROTOCOLO_URGENTE = (
    "Para resolver isso, eu trabalho com um *Protocolo de Liberação Urgente*. "
    "Buscamos a sua consulta/exame com urgência para tirar você da fila e ter acesso ao seu diagnóstico "
    "com o médico especialista. Isso faria diferença na sua vida agora?"
)

MSG_HONORARIOS = (
    "Como é um trabalho de alta especialidade, o escritório cobra Honorários Iniciais "
    "para assumir o caso e protocolar o pedido de liminar.\n\n"
    "Prosseguir com esse caso faz sentido para você garantir sua saúde hoje e sair dessa espera?"
)

MSG_SIM_HONORARIOS = (
    "Ótimo. Isso mostra que você prioriza sua saúde acima da burocracia do Estado. 💙\n\n"
    "Vou encaminhar seus dados para a mesa da Dra. Lethicia neste momento. "
    "Em instantes, ela entrará em contato aqui por este chat para te passar a estratégia "
    "de liberação e os valores para o seu caso.\n\n"
    "Fique atento(a)!"
)

MSG_NAO_HONORARIOS = (
    "Compreendo. Infelizmente, sem o interesse em avançar com uma medida judicial, "
    "o seu caso continuará dependendo exclusivamente da velocidade da fila do SUS, "
    "que como sabemos, não tem previsão.\n\n"
    "Como o escritório da Dra. Lethicia foca apenas em quem deseja forçar a solução imediata, "
    "estamos encerrando seu atendimento por aqui.\n\n"
    "Caso a sua situação se agrave ou você decida que não pode mais esperar, "
    "sinta-se à vontade para retornar. Desejamos sorte no seu tratamento. 🙏"
)

MSG_VALORES_SUS_CONSULTA = (
    "Compreendo sua dúvida sobre o investimento. No meu escritório, nós não trabalhamos com "
    "valores genéricos porque cada vida e cada urgência são únicas.\n\n"
    "Como são demandas de diagnóstico, a Dra. Lethicia precisa fazer uma análise da sua "
    "documentação agora. Se o seu caso for viável, os valores de investimento serão passados "
    "diretamente aqui pelo WhatsApp."
)

MSG_VALORES_CIRURGIA = (
    "Compreendo sua dúvida sobre o investimento. No meu escritório, nós não trabalhamos com "
    "valores genéricos porque cada vida e cada urgência são únicas. Como o seu caso envolve "
    "um procedimento cirúrgico, estamos tratando de um cenário de alta complexidade técnica e risco à vida.\n\n"
    "A Dra. Lethicia não define valores para cirurgias por mensagem de texto. "
    "Para casos assim, é obrigatória uma *Reunião Estratégica por vídeo (15 minutos)*.\n\n"
    "Escolha o melhor horário na agenda da Dra. pelo link abaixo:\n"
    "🔗 [LINK DA SUA AGENDA AQUI]"
)

MSG_PLANO_ENCERRAMENTO_NEGATIVA = (
    "Entendo perfeitamente e respeito sua decisão.\n\n"
    "Vou encerrar o seu atendimento por aqui para priorizar os casos que já estão com "
    "liminares em andamento. Lembre-se apenas que, no Direito da Saúde, o tempo é um "
    "fator determinante para o sucesso do tratamento.\n\n"
    "Caso precise de suporte especializado no futuro, meus canais continuam à disposição. 🙏"
)

MSG_PLANO_OP1 = (
    "Faz todo sentido querer entender bem a situação antes de tomar qualquer decisão.\n\n"
    "Para isso, ofereço uma *Consulta de Orientação Jurídica* — você fala diretamente com a Dra., "
    "tira todas as suas dúvidas e entende com clareza quais são seus direitos e quais caminhos "
    "existem para o seu caso.\n\n"
    "💰 O valor da consulta é de *R$ 97,00* e é feita online.\n\n"
    "Podemos agendar um horário na agenda da Dra. Lethicia?"
)

MSG_PLANO_OP2 = (
    "Você está no momento exato de agirmos para buscar o seu direito judicialmente. "
    "Agora não é mais hora de esperar, é hora de exigir que o plano de saúde cumpra a lei.\n\n"
    "O seu próximo passo é o nosso *Diagnóstico Estratégico*. Nessa reunião, a Dra. Lethicia "
    "analisa seu caso a fundo para traçarmos a estratégia da sua liminar.\n\n"
    "✅ Essa reunião é *GRATUITA*.\n\n"
    "Podemos agendar sua reunião para garantirmos sua cirurgia o quanto antes?"
)

MSG_PLANO_OP3 = (
    "Você é muito estratégico(a)! Esperar a negativa do plano para só depois agir é o erro "
    "que faz muita gente perder meses de tratamento.\n\n"
    "Meu papel aqui é duplo: primeiro, vou 'blindar' seus laudos para que o plano não tenha "
    "desculpas para negar. E, caso insistam na abusividade, já teremos a prova perfeita para "
    "a justiça liberar sua cirurgia com urgência.\n\n"
    "O próximo passo é o nosso *Diagnóstico Estratégico* (reunião gratuita).\n\n"
    "Podemos agendar sua reunião com a Dra. pra garantirmos sua cirurgia ainda este semestre?"
)

# ============================================
# PERGUNTAS ESPECÍFICAS (IGUAL AO ORIGINAL)
# ============================================

PERGUNTAS_ONCOLOGIA = [
    "Entendi… vamos cuidar disso juntos 💙\n\n"
    "👉 Você consegue me contar qual é o tipo de câncer?",

    "👉 Você está aguardando atendimento ou tratamento pelo SUS? "
    "Se sim, há quanto tempo mais ou menos?",

    "Só pra eu entender melhor seu caso:\n"
    "👉 O diagnóstico já foi confirmado por biópsia? E você tem esse laudo em mãos?",

    "👉 Você já foi encaminhado para um hospital especializado em câncer (oncologia) "
    "pelo SUS ou ainda nem conseguiu passar com um especialista?\n\n"
    "_(Infelizmente, a fila do SUS não respeita o avanço da doença. Se o hospital não "
    "iniciou seu tratamento em 60 dias, a lei está sendo descumprida.)_",

    "👉 Você possui um relatório médico explicando o tratamento que precisa fazer? "
    "(se quiser, pode enviar aqui também 📎)",

    "Última perguntinha, que é bem importante:\n"
    "👉 O médico falou se o seu caso é urgente? _(responde só com sim ou não, por favor)_",

    "Você possui o comprovante de que está aguardando na fila?\n"
    "Pode ser o print do App Meu SUS Digital, o comprovante de agendamento "
    "da Secretaria de Saúde ou o papel da regulação (SISREG) com o número do seu protocolo.",
]

PERGUNTAS_NEURODIVERGENCIAS = [
    "Entendi… pode ficar tranquilo(a), vou te ajudar com isso 💙\n\n"
    "Casos assim realmente precisam de atenção, principalmente por envolver desenvolvimento.\n\n"
    "👉 Me conta: já tem diagnóstico fechado ou ainda está em investigação?",

    "👉 Você tem algum laudo ou relatório médico com o diagnóstico?",

    "Agora me conta uma coisa importante:\n"
    "👉 Quais terapias o médico indicou?",

    "E hoje, como está essa situação no SUS?\n"
    "👉 Você conseguiu iniciar as terapias ou ainda está aguardando?",

    "👉 Você está em fila ou aguardando vaga?",

    "Essa parte é muito importante:\n"
    "👉 O médico comentou algo sobre prejuízo no desenvolvimento ou necessidade de iniciar rápido as terapias?",

    "Se você puder me contar:\n"
    "👉 Como essa situação está impactando o dia a dia de vocês?",

    "Você possui o comprovante de que está aguardando na fila?\n"
    "Pode ser o print do App Meu SUS Digital, comprovante da Secretaria de Saúde ou papel da regulação (SISREG).",
]

PERGUNTAS_ENDOMETRIOSE = [
    "Entendi… imagino o quanto isso pode estar sendo difícil pra você 😔\n"
    "Mas fica tranquila, vou te ajudar com isso 💙\n\n"
    "👉 Você já tem diagnóstico confirmado de endometriose ou adenomiose?",

    "Obrigada por me contar 🙏\n"
    "👉 Esse diagnóstico foi feito por exame? Se ainda não fez, qual exame está aguardando?",

    "Quero entender melhor sua situação:\n"
    "👉 Você sente dores fortes ou crises que atrapalham sua rotina?",

    "Agora uma parte bem importante:\n"
    "👉 O médico indicou algum tratamento específico?\n"
    "_(ex: cirurgia de videolaparoscopia, medicamento, acompanhamento…)_",

    "👉 Você tem relatório médico explicando esse tratamento?\n"
    "Se puder enviar, ajuda muito na análise 📎",

    "👉 Você está aguardando há quanto tempo mais ou menos?",

    "👉 O médico colocou em relatório ou te informou se existe risco de piora ou "
    "agravamento sem o tratamento?",

    "Você possui o comprovante de que está aguardando na fila?\n"
    "Pode ser o print do App Meu SUS Digital, comprovante da Secretaria de Saúde ou papel da regulação (SISREG).",
]

PERGUNTAS_MEDICAMENTO = [
    "Entendi… vamos ver isso com calma 💙\n\n"
    "👉 Qual foi o medicamento que o médico indicou pra você?",

    "Perfeito, obrigado por me explicar 🙏\n"
    "👉 Você tem a receita ou relatório médico desse medicamento?",

    "Ao te passar esse medicamento, o seu médico escreveu no laudo que este remédio "
    "específico é o único que pode tratar seu caso agora e que a interrupção trará "
    "riscos à sua vida ou saúde?",

    "Essa parte é bem importante:\n"
    "👉 Você já utilizou outros medicamentos antes? Se sim, eles não tiveram resultado "
    "ou causaram algum problema?",

    "👉 Você chegou a solicitar esse medicamento pelo SUS ou farmácia de alto custo? "
    "O que te informaram?\n_(foi negado, está em análise, falta no estoque…)_",

    "👉 O médico comentou o que pode acontecer se você não usar esse medicamento?\n"
    "_(se puder me explicar, isso ajuda muito)_",
]

PERGUNTAS_BARIATRICA = [
    "Entendi… vamos ver isso com calma 💙\n"
    "👉 Você já tem indicação médica para cirurgia bariátrica?",

    "Você possui outras doenças agravadas pelo peso, como Diabetes, Hipertensão, "
    "Apneia do Sono ou problemas graves nas articulações?",

    "👉 Você tem algum laudo ou relatório médico indicando a cirurgia?\n"
    "Se puder enviar aqui, já me ajuda bastante 📎",

    "Só pra eu entender melhor seu caso:\n"
    "👉 Você sabe me informar seu peso e altura?\n"
    "_(se não souber exato, pode ser aproximado)_",

    "Essa parte é bem importante:\n"
    "👉 Você já tentou outros tratamentos antes, como dieta, acompanhamento "
    "ou medicamentos? Como foi essa experiência?",

    "Você já está na fila de espera do SUS há quanto tempo?",

    "Você possui o comprovante de que está aguardando na fila?\n"
    "Pode ser o print do App Meu SUS Digital, comprovante da Secretaria de Saúde ou papel da regulação (SISREG).",
]

PERGUNTAS_REPARADORA = [
    "Perfeito, obrigado por me explicar 🙏\n"
    "👉 Você passou por cirurgia bariátrica ou teve uma grande perda de peso?\n"
    "_(se quiser, pode me contar um pouco da sua história)_",

    "Agora quero entender melhor sua situação:\n"
    "👉 O excesso de pele ou condição tem causado algum problema?\n"
    "_(ex: dor, assaduras, infecções, dificuldade de movimentação…)_",

    "Você já teve a oportunidade de passar pelo cirurgião plástico?",

    "👉 Algum médico já te deu um relatório solicitando essa cirurgia?\n"
    "_(se puder me explicar ou enviar o relatório, ajuda muito 📎)_",

    "👉 Você está aguardando há quanto tempo mais ou menos?",

    "Você possui o comprovante de que está aguardando na fila?\n"
    "Pode ser o print do App Meu SUS Digital, comprovante da Secretaria de Saúde ou papel da regulação (SISREG).",
]

PERGUNTAS_NEUROLOGIA = [
    "Entendi… vamos ver isso com calma 💙\n"
    "👉 Você consegue me explicar qual é o problema neurológico ou diagnóstico?",

    "Obrigado por me explicar 🙏\n"
    "👉 Você tem algum laudo ou exame com esse diagnóstico?\n"
    "_(se puder enviar aqui, ajuda bastante 📎)_",

    "Gostaria de saber qual cirurgia especificamente você está aguardando. Você pode me dizer?",

    "O médico especialista (Neuro) ou outro médico já emitiu laudo dizendo que a "
    "demora pode causar um dano irreversível da sua condição?",

    "👉 Você está aguardando atendimento, exame ou cirurgia? Há quanto tempo mais ou menos?",

    "Você já possui o comprovante de que está aguardando na fila?\n"
    "Pode ser o print do App Meu SUS Digital, comprovante da Secretaria de Saúde ou papel da regulação (SISREG).",
]

PERGUNTAS_CARDIOLOGIA = [
    "Entendi… vamos ver isso com calma 💙\n"
    "👉 Você consegue me explicar qual é o problema cardíaco ou o que o médico te disse?",

    "O seu caso envolve uma cirurgia de urgência (como ponte de safena ou troca de válvula), "
    "a colocação de um Marca-passo/Stent?",

    "Obrigado por me explicar 🙏\n"
    "👉 Você tem algum exame ou laudo do coração?\n"
    "_(ex: eletro, ecocardiograma, cateterismo… se puder enviar 📎)_",

    "👉 Você tem sentido algum desses sintomas?\n"
    "• Dor no peito\n• Falta de ar\n• Tontura ou desmaio\n• Cansaço excessivo\n\n"
    "Se tiver outros, pode me contar também.",

    "👉 O médico indicou algum tratamento ou procedimento?\n"
    "_(ex: cirurgia, cateterismo, marcapasso, acompanhamento…)_",

    "👉 Você tem relatório médico explicando essa necessidade?\n"
    "_(se puder enviar, ajuda muito na análise 📎)_",

    "Você já possui o comprovante de que está aguardando na fila?\n"
    "Pode ser o print do App Meu SUS Digital, comprovante da Secretaria de Saúde ou papel da regulação (SISREG).",
]

PERGUNTAS_OUTROS_SUS = [
    "Entendi. Como o seu caso é específico, eu preciso entender o que está acontecendo "
    "para te direcionar corretamente.\n\n"
    "Poderia me dizer qual é a sua condição/doença?",

    "Só pra eu entender melhor:\n"
    "👉 Você já tem algum diagnóstico ou ainda está investigando?",

    "👉 Algum médico já te passou relatório ou pedido de tratamento?\n"
    "Se tiver, pode me enviar aqui 📎",

    "👉 O médico comentou se existe urgência ou risco em não realizar esse tratamento?",

    "Recebido. Deixa eu te perguntar algo fundamental: o que acontece com a sua saúde "
    "se você não conseguir isso nos próximos 30 ou 90 dias? Existe risco de agravamento "
    "ou de uma sequela que não poderá ser revertida depois?",

    "👉 Como essa situação tem afetado sua vida hoje?",

    "Você possui o comprovante de que está aguardando na fila?\n"
    "Pode ser o print do App Meu SUS Digital, comprovante da Secretaria de Saúde ou papel da regulação (SISREG).",
]

PERGUNTAS_SUS_CONSULTA = [
    "Entendi que você está aguardando uma consulta especializada.\n\n"
    "👉 Qual especialidade médica você está aguardando?",

    "👉 Você tem encaminhamento ou pedido médico pra essa consulta?",

    "👉 Está aguardando há quanto tempo mais ou menos?",

    "👉 O que te informaram quando você questionou sua posição na fila ou quando "
    "foi tentar marcar?\n_(fila, falta de médico, sem previsão…)_",

    "Você teria algum exame informando a condição de saúde que tem?",
]

PERGUNTAS_SUS_EXAME = [
    "Entendi… vamos ver isso com calma 💙\n"
    "👉 Qual exame o médico solicitou pra você?",

    "Esse exame que você precisa é para qual finalidade principal?\n\n"
    "1️⃣ Diagnóstico — para descobrir o que tenho\n"
    "2️⃣ Pré-operatório — para conseguir operar logo\n"
    "3️⃣ Confirmação — o médico suspeita de cirurgia e precisa do exame para decidir",

    "👉 O médico comentou se existe urgência ou risco em não realizar esse exame?",

    "👉 Você está aguardando há quanto tempo mais ou menos?",

    "Quem te pediu esse exame foi o médico especialista ou o médico do postinho/UBS?",

    "Você possui o comprovante de que está aguardando na fila?\n"
    "Pode ser o print do App Meu SUS Digital, comprovante da Secretaria de Saúde ou papel da regulação (SISREG).",
]

PERGUNTAS_PLANO_REPARADORA = [
    "Você realizou a cirurgia bariátrica ou teve uma perda de peso expressiva através "
    "de dieta, exercícios ou uso das canetas emagrecedoras (Mounjaro, Ozempic, Tirzepatida...)?",

    "Você já chegou ou ainda falta pouco pro peso que gostaria?\n\n"
    "1️⃣ Sim, já atingi meu objetivo\n"
    "2️⃣ Ainda não",

    "Esse excesso de pele hoje te causa dores, assaduras ou dermatites que não curam? "
    "E além do corpo, como isso tem afetado a sua autoestima e a sua liberdade de movimento no dia a dia?",

    "Você já chegou a ir no médico cirurgião plástico pra solicitar as reparadoras e emitir os laudos?\n\n"
    "1️⃣ Sim\n"
    "2️⃣ Não",

    "Você prefere tentar sozinho com o plano ou quer o acompanhamento da Dra. para garantir "
    "que o seu pedido seja feito à prova de negativas?\n\n"
    "1️⃣ Quero o acompanhamento\n"
    "2️⃣ Vou tentar sozinho",
]

PERGUNTAS_PLANO_NEG_CIRURGIA_COMUM = [
    "Qual é o diagnóstico ou o tratamento específico que o plano está dificultando no momento?",
    "O plano negou formalmente ou simplesmente não respondeu?",
    "O plano justificou a negativa de alguma forma?\n_(Ex: 'eletivo', 'sem cobertura', 'período de carência')_",
    "Você tem os exames ou documentos que demonstram o diagnóstico e a necessidade do procedimento?",
    "Você já tentou resolver isso diretamente com o plano?\n_(ligação, protocolo, ouvidoria ou recurso formal)_",
]

PERGUNTAS_PLANO_MEDICAMENTO = [
    "Qual doença você está tratando?",
    "Qual medicamento foi prescrito pelo médico?",
    "O fornecimento do medicamento foi negado?\n\n1️⃣ Sim\n2️⃣ Não\n3️⃣ Ainda não solicitei",
    "Eu sei que cada dia sem a medicação gera uma ansiedade enorme, afinal, a sua saúde não pode esperar o tempo do plano.\n\nHoje, a falta desse medicamento já está afetando o controle da sua doença ou causando sintomas que impedem sua rotina?",
    "Qual foi o motivo da negativa?\n1️⃣ Fora do rol da ANS\n2️⃣ Alto custo\n3️⃣ Uso domiciliar\n4️⃣ Experimental/off-label\n5️⃣ Outro",
    "Essa negativa do plano foi por escrito ou verbal?",
    "Você possui receita médica do medicamento?\n\n1️⃣ Sim\n2️⃣ Não",
    "Qual o valor aproximado do medicamento?",
    "Você tem laudo médico explicando a necessidade do medicamento?\n\n1️⃣ Sim\n2️⃣ Não",
]

PERGUNTAS_PLANO_EXAME = [
    "Qual exame foi solicitado pelo seu médico?",
    "Para qual doença ou suspeita esse exame foi indicado?",
    "Sei o quão frustrante é ter um exame negado. Sem o exame, não há diagnóstico, e sem diagnóstico, não há tratamento.\n\nVocê sente que essa demora do plano está prejudicando a sua saúde ou impedindo que você comece o tratamento?",
    "O que o seu médico lhe disse sobre a urgência deste resultado?",
    "Qual foi o motivo da negativa?\n1️⃣ Fora do rol da ANS\n2️⃣ Não atende diretriz (DUT)\n3️⃣ Carência\n4️⃣ Não é urgente\n5️⃣ Experimental\n6️⃣ Outro",
    "Essa negativa do plano foi por escrito ou verbal?",
]

PERGUNTAS_PLANO_HOMECARE = [
    "Qual a doença ou condição do paciente?",
    "O paciente está acamado ou depende de cuidados constantes?",
    "O paciente já ficou internado recentemente?",
    "Você sente que o plano de saúde está tentando transferir para a sua família uma responsabilidade médica que é deles?",
    "O home care foi negado?\n\n1️⃣ Sim\n2️⃣ Não\n3️⃣ Ainda não solicitei",
    "Você possui relatório médico detalhado?\n\n1️⃣ Sim\n2️⃣ Não",
]

PERGUNTAS_PLANO_TERAPIAS = [
    "O tratamento é para:\n1️⃣ Autismo (TEA)\n2️⃣ Desenvolvimento infantil\n3️⃣ Reabilitação física\n4️⃣ Saúde mental\n5️⃣ Outro",
    "Quais terapias foram indicadas pelo médico?\n1️⃣ ABA\n2️⃣ Fisioterapia\n3️⃣ Psicologia\n4️⃣ Fonoaudiologia\n5️⃣ Terapia ocupacional\n6️⃣ Psicopedagogia\n7️⃣ Outras",
    "Quantas sessões por semana foram indicadas?",
    "Hoje, a falta dessas terapias tem causado retrocessos ou estagnado a evolução que você tanto espera?\n\nMe conta como está sendo.",
    "O que aconteceu?\n1️⃣ Limitou número de sessões\n2️⃣ Negou totalmente\n3️⃣ Não tem profissional disponível\n4️⃣ Outro",
    "Você possui laudo médico com o diagnóstico?\n\n1️⃣ Sim\n2️⃣ Não",
    "Essa negativa do plano foi por escrito ou verbal?",
]

PERGUNTAS_PLANO_REAJUSTE = [
    "O plano é:\n1️⃣ Individual/Familiar\n2️⃣ Coletivo por adesão\n3️⃣ Empresarial\n4️⃣ Não sei",
    "De quanto foi aproximadamente o aumento?\n1️⃣ Até 20%\n2️⃣ 20% a 50%\n3️⃣ Mais de 50%\n4️⃣ Não sei",
    "Esse novo valor do boleto compromete a sua renda ou faz você considerar cancelar o plano?",
    "Você (ou o titular) tem mais de 59 anos?\n\n1️⃣ Sim\n2️⃣ Não",
    "O aumento ocorreu após mudança de faixa de idade?\n\n1️⃣ Sim\n2️⃣ Não",
    "Você recebeu algum documento detalhando o aumento?\n\n1️⃣ Sim\n2️⃣ Não",
    "Esse plano foi feito por:\n1️⃣ Empresa\n2️⃣ Associação/sindicato\n3️⃣ Contratei sozinho",
    "Você possui o contrato do plano?\n\n1️⃣ Sim\n2️⃣ Não",
]

PERGUNTAS_PLANO_COPARTICIPACAO = [
    "Você deixou de fazer exames ou tratamentos por causa da coparticipação?\n\n1️⃣ Sim\n2️⃣ Não",
    "Você sente que hoje está 'pagando para usar' o que já deveria estar coberto?",
    "A coparticipação foi cobrada em:\n1️⃣ Consultas\n2️⃣ Exames\n3️⃣ Terapias\n4️⃣ Internação\n5️⃣ Outro",
    "Você faz tratamento contínuo?\n\n1️⃣ Sim\n2️⃣ Não",
    "Qual tipo de tratamento você faz?",
    "Você possui o contrato do plano?\n\n1️⃣ Sim\n2️⃣ Não",
]

PERGUNTAS_PLANO_ERRO_MEDICO = [
    "O que aconteceu durante o atendimento médico?\n1️⃣ Cirurgia\n2️⃣ Atendimento de emergência\n3️⃣ Tratamento contínuo\n4️⃣ Parto\n5️⃣ Outro",
    "O paciente sofreu algum dano?\n1️⃣ Agravamento da saúde\n2️⃣ Sequela\n3️⃣ Dor intensa\n4️⃣ Novo procedimento necessário\n5️⃣ Óbito",
    "Como esse episódio mudou a sua vida hoje?",
    "Você possui prontuário médico?\n\n1️⃣ Sim\n2️⃣ Não",
    "Outro médico já disse que houve erro ou falha no atendimento?\n\n1️⃣ Sim\n2️⃣ Não",
    "Você sente que houve falta de informação, descaso ou uma falha clara na técnica do médico ou do hospital?",
]

PERGUNTAS_PLANO_OUTRO = [
    "Entendido! O Direito da Saúde é muito amplo e, se o seu problema envolve o seu bem-estar "
    "ou o seu contrato de saúde, você está no lugar certo.\n\n"
    "Para que eu possa entender como te ajudar, me conte brevemente o que está acontecendo.",

    "Existe algum prazo ou data limite que te preocupa agora?\n"
    "_(ex: uma cirurgia marcada, um boleto vencendo ou um prazo de defesa)_",

    "Você recebeu alguma negativa ou teve dificuldade no atendimento?\n\n"
    "1️⃣ Sim\n2️⃣ Não\n3️⃣ Não se encaixa",

    "Você tem isso registrado (mensagem, documento, protocolo)?\n\n"
    "1️⃣ Sim\n2️⃣ Não\n3️⃣ Não se encaixa",

    "Você possui documentos relacionados ao caso?\n\n"
    "1️⃣ Sim\n2️⃣ Não",
    "Esse problema está afetando sua saúde atualmente?\n\n"
    "1️⃣ Sim\n2️⃣ Não",
]

PERGUNTAS_PLANO_POR_SITUACAO = {
    "1": PERGUNTAS_PLANO_REPARADORA,
    "2": PERGUNTAS_PLANO_NEG_CIRURGIA_COMUM,
    "3": PERGUNTAS_PLANO_MEDICAMENTO,
    "4": PERGUNTAS_PLANO_EXAME,
    "5": PERGUNTAS_PLANO_HOMECARE,
    "6": PERGUNTAS_PLANO_TERAPIAS,
    "7": PERGUNTAS_PLANO_REAJUSTE,
    "8": PERGUNTAS_PLANO_COPARTICIPACAO,
    "9": PERGUNTAS_PLANO_ERRO_MEDICO,
    "10": PERGUNTAS_PLANO_OUTRO,
}

PERGUNTAS_POR_ESPECIALIDADE = {
    "1": PERGUNTAS_ONCOLOGIA,
    "2": PERGUNTAS_NEURODIVERGENCIAS,
    "3": PERGUNTAS_ENDOMETRIOSE,
    "4": PERGUNTAS_MEDICAMENTO,
    "5": PERGUNTAS_BARIATRICA,
    "6": PERGUNTAS_REPARADORA,
    "7": PERGUNTAS_NEUROLOGIA,
    "8": PERGUNTAS_CARDIOLOGIA,
    "9": PERGUNTAS_OUTROS_SUS,
}

# ============================================
# GERENCIAMENTO DE SESSÃO
# ============================================

def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "session" not in st.session_state:
        st.session_state.session = {
            "estado": "inicio",
            "nome": None,
            "tipo_atendimento": None,
            "tipo_demanda": None,
            "especialidade": None,
            "dados": {},
            "pergunta_idx": 0
        }

def add_bot_message(text: str):
    st.session_state.messages.append({"role": "bot", "content": text})

def add_user_message(text: str):
    st.session_state.messages.append({"role": "user", "content": text})

def reset_session():
    st.session_state.session = {
        "estado": "inicio",
        "nome": None,
        "tipo_atendimento": None,
        "tipo_demanda": None,
        "especialidade": None,
        "dados": {},
        "pergunta_idx": 0
    }
    st.session_state.messages = []

def processar_mensagem(mensagem: str) -> str:
    session = st.session_state.session
    msg = mensagem.strip()
    estado = session["estado"]

    # Detecta se pergunta sobre valores
    palavras_valores = ["valor", "quanto", "preço", "custa", "honorário", "investimento", "cobram"]
    if any(p in msg.lower() for p in palavras_valores) and estado not in ["inicio", "aguardando_nome"]:
        tipo = session.get("tipo_demanda", "")
        if tipo in ["cirurgia", "tratamento"]:
            return MSG_VALORES_CIRURGIA
        else:
            return MSG_VALORES_SUS_CONSULTA

    # INICIO
    if estado == "inicio":
        session["estado"] = "aguardando_nome"
        return MSG_BOAS_VINDAS

    if estado == "aguardando_nome":
        session["nome"] = msg.title()
        session["estado"] = "sus_ou_plano"
        return MSG_SUS_OU_PLANO.format(nome=session["nome"])

    # SUS OU PLANO
    if estado == "sus_ou_plano":
        if "1" in msg or "sus" in msg.lower():
            session["tipo_atendimento"] = "SUS"
            session["estado"] = "sus_demanda"
            return MSG_SUS_DEMANDA
        elif "2" in msg or "plano" in msg.lower():
            session["tipo_atendimento"] = "PLANO"
            session["estado"] = "plano_carencia"
            return MSG_PLANO_CARENCIA
        else:
            return MSG_SUS_OU_PLANO.format(nome=session["nome"])

    # FLUXO SUS
    if estado == "sus_demanda":
        if "1" in msg or "cirurgia" in msg.lower():
            session["tipo_demanda"] = "cirurgia"
            session["estado"] = "sus_especialidade"
            return MSG_SUS_ESPECIALIDADE
        elif "2" in msg or "consulta" in msg.lower():
            session["tipo_demanda"] = "consulta_exame"
            session["estado"] = "sus_consulta_especialidade"
            return MSG_SUS_CONSULTA_ESPECIALIDADE
        else:
            return MSG_SUS_DEMANDA

    if estado == "sus_especialidade":
        opcoes = {"1", "2", "3", "4", "5", "6", "7", "8", "9"}
        escolha = next((o for o in opcoes if o in msg), None)
        if escolha:
            session["especialidade"] = escolha
            session["estado"] = "sus_perguntas"
            session["pergunta_idx"] = 0
            perguntas = PERGUNTAS_POR_ESPECIALIDADE.get(escolha, PERGUNTAS_OUTROS_SUS)
            return perguntas[0]
        else:
            return MSG_SUS_ESPECIALIDADE

    if estado == "sus_perguntas":
        idx = session.get("pergunta_idx", 0)
        especialidade = session.get("especialidade", "9")
        perguntas = PERGUNTAS_POR_ESPECIALIDADE.get(especialidade, PERGUNTAS_OUTROS_SUS)

        session["dados"][f"resposta_{idx}"] = msg
        idx += 1
        session["pergunta_idx"] = idx

        if idx < len(perguntas):
            return perguntas[idx]
        else:
            session["estado"] = "sus_pos_perguntas"
            return MSG_POS_PERGUNTAS_SUS.format(nome=session["nome"]) + "\n\n" + MSG_PROTOCOLO_URGENTE

    if estado == "sus_pos_perguntas":
        session["estado"] = "sus_honorarios"
        return MSG_HONORARIOS

    if estado == "sus_honorarios":
        if any(p in msg.lower() for p in ["sim", "yes", "quero", "ok", "claro", "vamos", "pode"]):
            session["estado"] = "finalizado"
            return MSG_SIM_HONORARIOS
        else:
            session["estado"] = "finalizado"
            return MSG_NAO_HONORARIOS

    # SUS CONSULTA/EXAME
    if estado == "sus_consulta_especialidade":
        session["especialidade_consulta"] = msg
        session["estado"] = "sus_consulta_tipo"
        return MSG_SUS_CONSULTA_TIPO

    if estado == "sus_consulta_tipo":
        if "1" in msg or "consulta" in msg.lower():
            session["tipo_demanda"] = "consulta"
            session["estado"] = "sus_consulta_perguntas"
            session["pergunta_idx"] = 0
            return PERGUNTAS_SUS_CONSULTA[0]
        elif "2" in msg or "exame" in msg.lower():
            session["tipo_demanda"] = "exame"
            session["estado"] = "sus_exame_perguntas"
            session["pergunta_idx"] = 0
            return PERGUNTAS_SUS_EXAME[0]
        else:
            return MSG_SUS_CONSULTA_TIPO

    if estado == "sus_consulta_perguntas":
        idx = session.get("pergunta_idx", 0)
        session["dados"][f"resposta_{idx}"] = msg
        idx += 1
        session["pergunta_idx"] = idx

        if idx < len(PERGUNTAS_SUS_CONSULTA):
            return PERGUNTAS_SUS_CONSULTA[idx]
        else:
            session["estado"] = "sus_pos_perguntas"
            msg_judiciario = (
                "Muitas vezes o SUS nega a consulta dizendo que não tem o especialista, "
                "mas a lei é clara: se o governo não tem o médico, ele é obrigado a pagar "
                "uma consulta particular para você.\n\n"
                "O Judiciário entende que o Estado não tem o direito de te deixar em uma "
                "fila infinita quando existe risco de agravamento.\n\n"
                "Você quer continuar contando com a sorte do sistema ou quer que a Dra. Lethicia "
                "force o governo a cumprir a lei agora?"
            )
            return msg_judiciario

    if estado == "sus_exame_perguntas":
        idx = session.get("pergunta_idx", 0)
        session["dados"][f"resposta_{idx}"] = msg
        idx += 1
        session["pergunta_idx"] = idx

        if idx < len(PERGUNTAS_SUS_EXAME):
            return PERGUNTAS_SUS_EXAME[idx]
        else:
            session["estado"] = "sus_pos_perguntas"
            return (
                "No SUS, a demora para realizar um Exame muitas vezes é o que impede "
                "o médico de salvar um paciente a tempo.\n\n"
                "O Judiciário entende que o Estado não tem o direito de te deixar em uma "
                "fila infinita quando existe risco de agravamento.\n\n"
                "Você quer continuar contando com a sorte do sistema ou quer que a Dra. Lethicia "
                "force o governo a cumprir a lei agora?"
            )

    # FLUXO PLANO
    if estado == "plano_carencia":
        if "1" in msg or "sim" in msg.lower():
            session["plano_carencia"] = True
            session["estado"] = "plano_situacao"
            return MSG_PLANO_SITUACAO
        elif "2" in msg or "não" in msg.lower():
            session["plano_carencia"] = False
            session["estado"] = "plano_sem_carencia"
            return MSG_PLANO_SEM_CARENCIA
        else:
            return MSG_PLANO_CARENCIA

    if estado == "plano_sem_carencia":
        session["dados"]["tratamento_sem_carencia"] = msg
        session["estado"] = "plano_sem_carencia_urgencia"
        return (
            "Existem situações onde o plano é obrigado a cobrir o seu procedimento mesmo "
            "que você tenha poucos meses de contrato, especialmente se houver urgência.\n\n"
            "No seu caso, o médico comentou se isso é urgente ou pode trazer algum risco se não for feito?"
        )

    if estado == "plano_sem_carencia_urgencia":
        session["dados"]["urgencia"] = msg
        session["estado"] = "plano_sem_carencia_negativa"
        return "O plano negou alegando carência?\n\n1️⃣ Sim\n2️⃣ Não"

    if estado == "plano_sem_carencia_negativa":
        session["dados"]["negou_carencia"] = msg
        session["estado"] = "plano_sem_carencia_escrita"
        return "Você tem a negativa por escrito?\n\n1️⃣ Sim\n2️⃣ Não"

    if estado == "plano_sem_carencia_escrita":
        session["dados"]["negativa_escrita"] = msg
        session["estado"] = "plano_pos_perguntas"
        return "Obrigado pelas informações! Agora me diz: o que você está buscando nesse momento?\n\n1️⃣ Tirar dúvidas básicas\n2️⃣ Já tenho a negativa\n3️⃣ Não tenho a negativa ainda"

    if estado == "plano_situacao":
        opcoes = {"1", "2", "3", "4", "5", "6", "7", "8", "9", "10"}
        escolha = next((o for o in opcoes if o in msg), None)
        if escolha:
            session["situacao_plano"] = escolha
            session["estado"] = "plano_perguntas"
            session["pergunta_idx"] = 0
            perguntas = PERGUNTAS_PLANO_POR_SITUACAO.get(escolha, PERGUNTAS_PLANO_OUTRO)
            return perguntas[0]
        else:
            return MSG_PLANO_SITUACAO

    if estado == "plano_perguntas":
        idx = session.get("pergunta_idx", 0)
        situacao = session.get("situacao_plano", "10")
        perguntas = PERGUNTAS_PLANO_POR_SITUACAO.get(situacao, PERGUNTAS_PLANO_OUTRO)

        session["dados"][f"resposta_{idx}"] = msg
        idx += 1
        session["pergunta_idx"] = idx

        if idx < len(perguntas):
            return perguntas[idx]
        else:
            session["estado"] = "plano_pos_perguntas"
            return "Obrigado pelas informações! Agora me diz: o que você está buscando nesse momento?\n\n1️⃣ Tirar dúvidas básicas\n2️⃣ Já tenho a negativa\n3️⃣ Não tenho a negativa ainda"

    if estado == "plano_pos_perguntas":
        if "1" in msg:
            session["estado"] = "finalizado"
            return MSG_PLANO_OP1
        elif "2" in msg:
            session["estado"] = "finalizado"
            return MSG_PLANO_OP2
        elif "3" in msg:
            session["estado"] = "finalizado"
            return MSG_PLANO_OP3
        else:
            return "1️⃣ Tirar dúvidas básicas\n2️⃣ Já tenho a negativa\n3️⃣ Não tenho a negativa ainda"

    # Fallback
    reset_session()
    return MSG_BOAS_VINDAS

# ============================================
# INTERFACE STREAMLIT
# ============================================

def main():
    st.title("⚖️ Iara Bot - Assistente Jurídica")
    st.caption("Dra. Lethicia Fernanda | Especialista em Direito da Saúde")

    init_session_state()

    # Sidebar
    with st.sidebar:
        st.markdown("### 📊 Status do Atendimento")
        session = st.session_state.session
        if session.get("nome"):
            st.markdown(f"**Cliente:** {session['nome']}")
        if session.get("tipo_atendimento"):
            st.markdown(f"**Canal:** {session['tipo_atendimento']}")
        if session.get("tipo_demanda"):
            st.markdown(f"**Demanda:** {session['tipo_demanda']}")
        st.markdown("---")
        if st.button("🔄 Nova Conversa", use_container_width=True):
            reset_session()
            st.rerun()

    # Chat
    chat_container = st.container()
    with chat_container:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for msg in st.session_state.messages:
            if msg["role"] == "bot":
                st.markdown(f'<div class="chat-message bot-message"><strong>🤖 Iara:</strong><br>{msg["content"]}</div>', unsafe_allow_html=True)
            else:
                nome = st.session_state.session.get("nome", "Você")
                st.markdown(f'<div class="chat-message user-message"><strong>👤 {nome}:</strong><br>{msg["content"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Input
    col1, col2 = st.columns([4, 1])
    with col1:
        user_input = st.text_input("Digite sua mensagem:", key="user_input")
    with col2:
        send_button = st.button("📤 Enviar", use_container_width=True)

    if send_button and user_input:
        add_user_message(user_input)
        resposta = processar_mensagem(user_input)
        add_bot_message(resposta)
        st.rerun()

    # Mensagem inicial
    if len(st.session_state.messages) == 0:
        add_bot_message(MSG_BOAS_VINDAS)
        st.rerun()

if __name__ == "__main__":
    main()
