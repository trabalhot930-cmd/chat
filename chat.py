"""
Iara Bot - Assistente Jurídica em Direito da Saúde
Fluxo EXATO das imagens do WhatsApp
Versão standalone para Streamlit
"""

import streamlit as st
import re
from datetime import datetime
from typing import Dict, Optional, List

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
    hr {
        margin: 1rem 0;
    }
    .info-box {
        background-color: #e8f5e9;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
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

# ============================================
# GERENCIAMENTO DE SESSÃO
# ============================================

def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "estado" not in st.session_state:
        st.session_state.estado = "INICIO"
    if "dados" not in st.session_state:
        st.session_state.dados = {}
    if "nome" not in st.session_state:
        st.session_state.nome = None
    if "sub_estado" not in st.session_state:
        st.session_state.sub_estado = None
    if "pergunta_idx" not in st.session_state:
        st.session_state.pergunta_idx = 0
    if "lista_perguntas" not in st.session_state:
        st.session_state.lista_perguntas = []

def add_bot_message(text: str):
    if not text:
        return
    text = text.replace("{nome}", st.session_state.nome or "")
    text = text.replace("{lawyer}", L)
    text = text.replace("{CALENDLY_LINK}", CALENDLY_LINK)
    text = text.replace("{PIX_KEY}", PIX_KEY)
    st.session_state.messages.append({"role": "bot", "content": text})

def add_user_message(text: str):
    st.session_state.messages.append({"role": "user", "content": text})

def reset_conversa():
    st.session_state.clear()
    init_session_state()
    add_bot_message(MSG_BOAS_VINDAS)

# ============================================
# MENSAGENS DO FLUXO (CONFORME IMAGENS)
# ============================================

MSG_BOAS_VINDAS = (
    "Olá, seja bem vindo(a). 🌟\n\n"
    "Sou a Lara, assistente jurídica do escritório da Dra Lethicia Fernanda, "
    "advogada especialista em Direito da Saúde.\n\n"
    "**Fico feliz que você entrou em contato conosco.**\n\n"
    "Qual o seu nome?"
)

MSG_CANAL = "Olá, {nome}! Seu atendimento é pelo **SUS** ou por **Plano de Saúde**?"

MSG_SUS_DEMANDA = "Me diga o que você está aguardando?"

MSG_SUS_ESPECIALIDADE = (
    "Para que eu direcione você para o protocolo de urgência correto, "
    "qual problema estamos enfrentando hoje?"
)

MSG_PLANO_TEMPO = "Você já tem seu plano de saúde há mais de 2 anos?"

MSG_PLANO_SITUACAO = (
    "Para que eu possa te direcionar corretamente, qual é a sua situação atual com o plano de saúde?"
)

# ============================================
# LISTAS DE PERGUNTAS POR ESPECIALIDADE
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

PERGUNTAS_NEURO = [
    "Entendi… pode ficar tranquilo(a), vou te ajudar com isso 🚨\n\nCasos assim realmente precisam de atenção, principalmente por envolver desenvolvimento.\n\n👉 Me conta: já tem diagnóstico fechado ou ainda está em investigação?",
    "👉 Você tem algum laudo ou relatório médico com o diagnóstico?",
    "Entendo as batalhas diárias que você enfrenta para garantir o melhor para quem você ama. Nenhuma criança deve ter seu desenvolvimento barrado por limites impostos pelo plano. Estou aqui para lutar ao seu lado e garantir todas as terapias que são de direito.\n\nAgora me conta uma coisa importante:\n\n👉 Quais terapias o médico indicou?",
    "E hoje, como está essa situação no SUS?\n\n👉 Você conseguiu iniciar as terapias ou ainda está aguardando?",
    "Essa parte é muito importante:\n\n👉 O médico comentou algo sobre prejuízo no desenvolvimento ou necessidade de iniciar rápido as terapias?",
    "Se você puder me contar:\n\n👉 Como essa situação está impactando o dia a dia de vocês?",
    "👉 Você possui o comprovante de que está aguardando na fila?\n\nPode ser o print da tela do App Meu SUS Digital, o comprovante de agendamento da Secretaria de Saúde ou o papel da regulação (SISREG) com o número do seu protocolo."
]

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

PERGUNTAS_MEDICAMENTO = [
    "Entendi… vamos ver isso com calma 😊\n\n👉 Qual foi o medicamento que o médico indicou pra você?",
    "Perfeito, obrigado por me explicar 😊\n\n👉 Você tem a receita ou relatório médico desse medicamento?",
    "Entendo a frustração de ter um direito negado justamente quando você mais precisa de suporte. Analisaremos seu caso para garantir que a lei seja cumprida e o acesso à saúde seja imediato. Conte conosco para transformar essa negativa em uma solução rápida e segura.\n\nAo te passar esse medicamento o seu médico escreveu no laudo que este remédio específico é o único que pode tratar seu caso agora e que a interrupção trará riscos à sua vida ou saúde?",
    "Essa parte é bem importante:\n\n👉 Você já utilizou outros medicamentos antes? Se sim, eles não tiveram resultado ou causaram algum problema?",
    "👉 Você chegou a solicitar esse medicamento pelo SUS ou farmácia de alto custo? O que te informaram?\n\n(foi negado, está em análise, falta no estoque… pode me explicar melhor)",
    "👉 O médico comentou o que pode acontecer se você não usar esse medicamento?\n\n(se puder me explicar, isso ajuda muito)"
]

PERGUNTAS_BARIATRICA = [
    "Entendi… vamos ver isso com calma 😊\n\n👉 Você já tem indicação médica para cirurgia bariátrica?",
    "👉 Você possui outras doenças agravadas pelo peso, como Diabetes, Hipertensão, Apneia do Sono ou problemas graves nas articulações?",
    "👉 Você tem algum laudo ou relatório médico indicando a cirurgia?\n\nSe puder enviar aqui, já me ajuda bastante 😊",
    "Só pra eu entender melhor seu caso:\n\n👉 Você sabe me informar seu peso e altura?\n(se não souber exato, pode ser aproximado)",
    "Essa parte é bem importante:\n\n👉 Você já tentou outros tratamentos antes, como dieta, acompanhamento ou medicamentos? Como foi essa experiência?",
    "👉 Você já está na fila de espera do SUS há quanto tempo?",
    "👉 Você possui o comprovante de que está aguardando na fila?\n\nPode ser o print da tela do App Meu SUS Digital, o comprovante de agendamento da Secretaria de Saúde ou o papel da regulação (SISREG) com o número do seu protocolo."
]

PERGUNTAS_REPARADORA = [
    "👉 Você passou por cirurgia bariátrica ou teve uma grande perda de peso (canetas, dieta e treino)? (se quiser, pode me contar um pouco da sua história)",
    "Agora quero entender melhor sua situação:\n\n👉 O excesso de pele ou condição tem causado algum problema? (ex: dor, assaduras, infecções, dificuldade de movimentação…)",
    "👉 Você já teve a oportunidade de passar pelo cirurgião plástico?",
    "👉 Algum médico já te deu um relatório solicitando essa cirurgia? (se puder me explicar ou enviar o relatório, ajuda muito 😊)",
    "👉 Você está aguardando há quanto tempo mais ou menos?",
    "👉 Você possui o comprovante de que está aguardando na fila?\n\nPode ser o print da tela do App Meu SUS Digital, o comprovante de agendamento da Secretaria de Saúde ou o papel da regulação (SISREG) com o número do seu protocolo."
]

PERGUNTAS_NEUROLOGIA = [
    "Entendi… vamos ver isso com calma 😊\n\n👉 Você consegue me explicar qual é o problema neurológico ou diagnóstico?",
    "Obrigado por me explicar 😊\n\n👉 Você tem algum laudo ou exame com esse diagnóstico? (se puder enviar aqui, ajuda bastante 😊)",
    "Sei que o momento é de muita angústia e que cada minuto de espera parece uma eternidade. Vou agir com a rapidez que o caso pede para que o hospital libere logo o necessário. Minha prioridade é tirar esse peso das suas costas e proteger a vida de quem você ama.\n\nGostaria de saber qual cirurgia especificamente você está aguardando. Você pode me dizer?",
    "👉 O médico especialista (Neuro) ou outro médico já emitiu laudo dizendo que a demora pode causar um dano irreversível da sua condição?",
    "👉 Você está aguardando atendimento, exame ou cirurgia? Há quanto tempo mais ou menos?",
    "👉 Você já possui o comprovante de que está aguardando na fila?\n\nPode ser o print da tela do App Meu SUS Digital, o comprovante de agendamento da Secretaria de Saúde ou o papel da regulação (SISREG) com o número do seu protocolo."
]

PERGUNTAS_CARDIOLOGIA = [
    "Entendi… vamos ver isso com calma 😊\n\n👉 Você consegue me explicar qual é o problema cardíaco ou o que o médico te disse?",
    "👉 O seu caso envolve uma cirurgia de urgência (como ponte de safena ou troca de válvula), a colocação de um Marca-passo/Stent?",
    "Obrigado por me explicar 😊\n\n👉 Você tem algum exame ou laudo do coração? (ex: eletro, ecocardiograma, cateterismo… se puder enviar 😊)",
    "Sei que o momento é de muita angústia e que cada minuto de espera parece uma eternidade. Vou agir com a rapidez que o caso pede para que o hospital libere logo o necessário. Minha prioridade é tirar esse peso das suas costas e proteger a vida de quem você ama.\n\n👉 Você tem sentido algum desses sintomas?\n\n• Dor no peito\n• Falta de ar\n• Tontura ou desmaio\n• Cansaço excessivo\n\nSe tiver outros, pode me contar também.",
    "👉 O médico indicou algum tratamento ou procedimento? (ex: cirurgia, cateterismo, marcapasso, acompanhamento…)",
    "👉 Você tem relatório médico explicando essa necessidade? (se puder enviar, ajuda muito na análise 😊)",
    "👉 Você já possui o comprovante de que está aguardando na fila?\n\nPode ser o print da tela do App Meu SUS Digital, o comprovante de agendamento da Secretaria de Saúde ou o papel da regulação (SISREG) com o número do seu protocolo."
]

PERGUNTAS_CONSULTA = [
    "Entendi que você está aguardando uma consulta especializada. Deixa eu te perguntar: você já está nessa fila de espera há mais de 30 dias ou o seu caso tem um prazo de urgência que o SUS simplesmente ignorou?",
    "👉 Qual especialidade médica você está aguardando?",
    "👉 Você tem encaminhamento ou pedido médico pra essa consulta?\n\nMuitas vezes o SUS nega a consulta dizendo que não tem o especialista, mas a lei é clara: se o governo não tem o médico, ele é obrigado a pagar uma consulta particular para você. A espera na fila da regulação não pode ser eterna, principalmente quando há dor ou risco de sequela.\n\nO Judiciário entende que o Estado não tem o direito de te deixar em uma fila infinita quando existe risco de agravamento.",
    "👉 Está aguardando há quanto tempo mais ou menos?",
    "👉 O que te informaram quando você questionou sua posição na fila ou quando você foi tentar marcar?\n\n(fila, falta de médico, sem previsão…)",
    "👉 Você teria algum exame informando a condição de saúde que tem?",
    "Para a Dra. Lethicia validar o seu protocolo de urgência, você possui o print do App Meu SUS Digital (ou o comprovante da fila de espera) e o Laudo Médico em mãos?"
]

PERGUNTAS_EXAME = [
    "Entendi… vamos ver isso com calma 😊\n\n👉 Qual exame o médico solicitou pra você?",
    "Esse exame que você precisa é para qual finalidade principal?\n\n1. Diagnóstico: Para descobrir o que eu tenho.\n2. Pré-operatório: Para eu conseguir operar logo.\n3. Confirmação: O médico suspeita de cirurgia e precisa do exame para decidir.",
    "👉 o médico comentou o que pode estar sendo investigado com esse exame? (se puder me explicar, ajuda muito)",
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
# MENSAGENS PÓS PERGUNTAS
# ============================================

MSG_POS_PERGUNTAS_SUS = (
    "_{nome}_, recebi suas respostas aqui. O que mais me preocupa no seu caso é que o SUS "
    "trata essa situação como se pudesse esperar, mas juridicamente sabemos que o *tempo é o seu maior inimigo agora*.\n\n"
    "Você sente que, se não resolvermos isso nos próximos dias, a sua saúde corre um risco de piorar de forma irreversível?"
)

MSG_EXPLICACAO_JUDICIAL = (
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

MSG_SIM_HONORARIOS = (
    "Perfeito. O próximo passo agora é uma reunião rápida para eu te explicar "
    "como funciona o processo e os valores de honorários.\n\n"
    "Antes de agendarmos: além de você, tem mais alguém que participa dessa decisão? "
    "(cônjuge, familiar…)"
)

MSG_NAO_HONORARIOS = (
    "Compreendo. Infelizmente, sem o interesse em avançar com uma medida judicial, "
    "o seu caso continuará dependendo exclusivamente da velocidade da fila do SUS, "
    "que como sabemos, não tem previsão.\n\n"
    "Como o escritório da {lawyer} foca apenas em quem deseja forçar a solução imediata, "
    "estamos encerrando seu atendimento por aqui.\n\n"
    "Caso a sua situação se agrave ou você decida que não pode mais esperar, "
    "sinta-se à vontade para retornar. Desejamos sorte no seu tratamento. 🙏"
)

MSG_VALORES_CONSULTA = (
    "Compreendo sua dúvida sobre o investimento. Aqui no escritório, nós não trabalhamos com "
    "valores iguais porque cada vida e cada urgência são únicas.\n\n"
    "Como são demandas de diagnóstico, a Dra. Lethicia precisa fazer uma análise da sua "
    "documentação agora. Se o seu caso for viável, os valores de investimento serão passados "
    "diretamente aqui pelo WhatsApp, para ganharmos tempo e agilizarmos seu atendimento no SUS."
)

MSG_VALORES_CIRURGIA = (
    "Compreendo sua dúvida sobre o investimento. No meu escritório, nós não trabalhamos com "
    "valores iguais porque cada vida e cada urgência são únicas. Como o seu caso envolve "
    "um procedimento cirúrgico, estamos tratando de um cenário de alta complexidade técnica e risco à vida.\n\n"
    f"A {L} não define valores para cirurgias por mensagem de texto. "
    "Para casos assim, é necessária uma *Reunião Estratégica por vídeo (15 minutos)*.\n\n"
    f"Escolha o melhor horário na agenda da Dra. pelo link abaixo:\n{CALENDLY_LINK}"
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
# PROCESSAMENTO DO FLUXO
# ============================================

def processar_resposta(resposta: str):
    estado = st.session_state.estado
    dados = st.session_state.dados
    
    # ========== INICIO ==========
    if estado == "INICIO":
        st.session_state.nome = resposta
        st.session_state.dados["nome"] = resposta
        st.session_state.estado = "CANAL"
        add_bot_message(MSG_CANAL.format(nome=resposta))
    
    # ========== CANAL ==========
    elif estado == "CANAL":
        if "sus" in _n(resposta):
            st.session_state.dados["canal"] = "SUS"
            st.session_state.estado = "SUS_DEMANDA"
            add_bot_message(MSG_SUS_DEMANDA)
        else:
            st.session_state.dados["canal"] = "PLANO"
            st.session_state.estado = "PLANO_TEMPO"
            add_bot_message(MSG_PLANO_TEMPO)
    
    # ========== SUS DEMANDA ==========
    elif estado == "SUS_DEMANDA":
        if "cirurgia" in _n(resposta) or "tratamento" in _n(resposta) or "1" in resposta:
            st.session_state.dados["tipo_demanda"] = "cirurgia"
            st.session_state.estado = "SUS_ESPECIALIDADE_CIRURGIA"
            add_bot_message(MSG_SUS_ESPECIALIDADE)
        else:
            st.session_state.dados["tipo_demanda"] = "consulta_exame"
            st.session_state.estado = "SUS_CONSULTA_EXAME"
            add_bot_message("Você está buscando:\n\n1️⃣ Consulta com especialista\n2️⃣ Realização de Exame")
    
    # ========== SUS ESPECIALIDADE CIRURGIA ==========
    elif estado == "SUS_ESPECIALIDADE_CIRURGIA":
        especialidades = {
            "oncologia": PERGUNTAS_ONCOLOGIA,
            "neuro": PERGUNTAS_NEURO,
            "endometriose": PERGUNTAS_ENDOMETRIOSE,
            "medicamento": PERGUNTAS_MEDICAMENTO,
            "bariátrica": PERGUNTAS_BARIATRICA,
            "reparadora": PERGUNTAS_REPARADORA,
            "neurologia": PERGUNTAS_NEUROLOGIA,
            "cardiologia": PERGUNTAS_CARDIOLOGIA
        }
        
        for key, perguntas in especialidades.items():
            if key in _n(resposta):
                st.session_state.dados["especialidade"] = key
                st.session_state.lista_perguntas = perguntas
                st.session_state.pergunta_idx = 0
                st.session_state.estado = "SUS_PERGPTAS_ESPECIALIDADE"
                add_bot_message(perguntas[0])
                return
        
        # Outros
        st.session_state.dados["especialidade"] = "outros"
        st.session_state.lista_perguntas = PERGUNTAS_OUTROS
        st.session_state.pergunta_idx = 0
        st.session_state.estado = "SUS_PERGPTAS_ESPECIALIDADE"
        add_bot_message(PERGUNTAS_OUTROS[0])
    
    # ========== SUS PERGUNTAS ESPECIALIDADE ==========
    elif estado == "SUS_PERGPTAS_ESPECIALIDADE":
        idx = st.session_state.pergunta_idx
        perguntas = st.session_state.lista_perguntas
        
        st.session_state.dados[f"resp_{idx}"] = resposta
        idx += 1
        st.session_state.pergunta_idx = idx
        
        if idx < len(perguntas):
            add_bot_message(perguntas[idx])
        else:
            # Verificar se tem documentos
            tem_laudo = any("laudo" in _n(str(st.session_state.dados.get("resp_2", ""))) 
                          or "sim" in _n(str(st.session_state.dados.get("resp_2", ""))))
            tem_comprovante = any("comprovante" in _n(str(st.session_state.dados.get("resp_6", "")))
                                or "sim" in _n(str(st.session_state.dados.get("resp_6", ""))))
            
            if not tem_laudo or not tem_comprovante:
                add_bot_message(MSG_SEM_DOCUMENTOS)
                st.session_state.estado = "AGUARDANDO_DOCUMENTOS"
            else:
                st.session_state.estado = "POS_PERGUNTAS"
                add_bot_message(MSG_POS_PERGUNTAS_SUS.format(nome=st.session_state.nome))
    
    # ========== SUS CONSULTA/EXAME ==========
    elif estado == "SUS_CONSULTA_EXAME":
        if "consulta" in _n(resposta) or "1" in resposta:
            st.session_state.dados["sub_tipo"] = "consulta"
            st.session_state.lista_perguntas = PERGUNTAS_CONSULTA
            st.session_state.pergunta_idx = 0
            st.session_state.estado = "SUS_PERGUNTAS_CONSULTA"
            add_bot_message(PERGUNTAS_CONSULTA[0])
        else:
            st.session_state.dados["sub_tipo"] = "exame"
            st.session_state.estado = "SUS_EXAME_TIPO"
            add_bot_message(PERGUNTAS_EXAME[0])
    
    # ========== SUS PERGUNTAS CONSULTA ==========
    elif estado == "SUS_PERGUNTAS_CONSULTA":
        idx = st.session_state.pergunta_idx
        perguntas = st.session_state.lista_perguntas
        
        st.session_state.dados[f"resp_{idx}"] = resposta
        idx += 1
        st.session_state.pergunta_idx = idx
        
        if idx < len(perguntas):
            add_bot_message(perguntas[idx])
        else:
            # Verificar documentos
            tem_docs = any("sim" in _n(str(st.session_state.dados.get("resp_6", ""))))
            if tem_docs:
                st.session_state.estado = "PROPOSTA_JUDICIAL"
                add_bot_message(MSG_EXPLICACAO_JUDICIAL)
            else:
                add_bot_message(MSG_SEM_DOCUMENTOS)
                st.session_state.estado = "AGUARDANDO_DOCUMENTOS"
    
    # ========== SUS EXAME TIPO ==========
    elif estado == "SUS_EXAME_TIPO":
        if "diagnóstico" in _n(resposta) or "1" in resposta:
            st.session_state.lista_perguntas = PERGUNTAS_EXAME
        elif "pré" in _n(resposta) or "2" in resposta:
            st.session_state.lista_perguntas = PERGUNTAS_EXAME_PREOP
        else:
            st.session_state.lista_perguntas = PERGUNTAS_EXAME_CONF
        
        st.session_state.pergunta_idx = 1  # Pular primeira pergunta (já respondida)
        st.session_state.estado = "SUS_PERGUNTAS_EXAME"
        add_bot_message(st.session_state.lista_perguntas[1] if len(st.session_state.lista_perguntas) > 1 else st.session_state.lista_perguntas[0])
    
    # ========== SUS PERGUNTAS EXAME ==========
    elif estado == "SUS_PERGUNTAS_EXAME":
        idx = st.session_state.pergunta_idx
        perguntas = st.session_state.lista_perguntas
        
        st.session_state.dados[f"resp_{idx}"] = resposta
        idx += 1
        st.session_state.pergunta_idx = idx
        
        if idx < len(perguntas):
            add_bot_message(perguntas[idx])
        else:
            add_bot_message(MSG_EXPLICACAO_JUDICIAL)
            st.session_state.estado = "PROPOSTA_JUDICIAL"
    
    # ========== POS PERGUNTAS ==========
    elif estado == "POS_PERGUNTAS":
        st.session_state.dados["sentimento"] = resposta
        add_bot_message(MSG_EXPLICACAO_JUDICIAL)
        st.session_state.estado = "PROPOSTA_JUDICIAL"
    
    # ========== PROPOSTA JUDICIAL ==========
    elif estado == "PROPOSTA_JUDICIAL":
        st.session_state.dados["resposta_proposta"] = resposta
        add_bot_message(MSG_HONORARIOS)
        st.session_state.estado = "HONORARIOS"
    
    # ========== HONORARIOS ==========
    elif estado == "HONORARIOS":
        if _sim(resposta):
            add_bot_message(MSG_SIM_HONORARIOS)
            st.session_state.estado = "DECISAO_COMPARTILHADA"
        else:
            add_bot_message(MSG_NAO_HONORARIOS)
            st.session_state.estado = "FIM"
    
    # ========== DECISAO COMPARTILHADA ==========
    elif estado == "DECISAO_COMPARTILHADA":
        st.session_state.dados["decisao"] = resposta
        
        if _sim(resposta):
            add_bot_message(
                "Excelente! É fundamental que ele(a) participe, pois como o Direito à Saúde envolve "
                "prazos muito curtos e decisões imediatas sobre o tratamento, é bom que todos estejam na mesma página.\n\n"
                f"Logo abaixo vou te mandar a agenda da {L}, e você marque o dia e horário que fica melhor pra vocês.\n\n"
                f"🔗 {CALENDLY_LINK}"
            )
        else:
            add_bot_message(
                "Perfeito, facilita bastante o nosso fluxo. Como você é a única pessoa responsável "
                "pela decisão, conseguimos dar um andamento mais ágil aos trabalhos.\n\n"
                f"Logo abaixo vou te mandar a agenda da {L}, e você marque o dia e horário que fica melhor pra você.\n\n"
                f"🔗 {CALENDLY_LINK}"
            )
        st.session_state.estado = "AGUARDANDO_AGENDA"
    
    # ========== PLANO DE SAÚDE ==========
    elif estado == "PLANO_TEMPO":
        if _sim(resposta):
            st.session_state.dados["plano_2anos"] = "sim"
            st.session_state.estado = "PLANO_SITUACAO"
            add_bot_message(MSG_PLANO_SITUACAO)
        else:
            st.session_state.dados["plano_2anos"] = "nao"
            st.session_state.estado = "PLANO_SEM_CARENCIA"
            add_bot_message(
                "Entendo! Muitas pessoas acreditam que precisam esperar 2 anos para ter direito a cirurgias "
                "ou tratamentos complexos, mas a lei nem sempre funciona assim.\n\n"
                "Me conta, qual o tratamento que você precisa fazer?"
            )
    
    elif estado == "PLANO_SEM_CARENCIA":
        st.session_state.dados["tratamento_sem_carencia"] = resposta
        st.session_state.estado = "PLANO_SEM_CARENCIA_URGENCIA"
        add_bot_message(
            "Existem situações onde o plano é obrigado a cobrir o seu procedimento mesmo que você "
            "tenha poucos meses de contrato, especialmente se houver urgência ou se a doença não "
            "foi declarada por má-fé.\n\n"
            "No seu caso, o médico comentou se isso é urgente ou pode trazer algum risco se não for feito?"
        )
    
    elif estado == "PLANO_SEM_CARENCIA_URGENCIA":
        st.session_state.dados["urgencia_plano"] = resposta
        st.session_state.estado = "PROPOSTA_JUDICIAL"
        add_bot_message(
            "Perfeito, isso é importante 😊\n\n"
            "SE HÁ URGÊNCIA, o plano já deveria cobrir normalmente esse tipo de situação.\n\n"
            "Para resolver isso, eu trabalho com um *Protocolo de Liberação Urgente*. "
            "Isso faria diferença na sua vida agora?"
        )
    
    elif estado == "PLANO_SITUACAO":
        st.session_state.dados["situacao_plano"] = resposta
        st.session_state.estado = "PROPOSTA_JUDICIAL"
        add_bot_message(
            "Obrigado por todas as informações. Já consigo ter um bom entendimento da sua situação.\n\n"
            "Para resolver isso, eu trabalho com um *Protocolo de Liberação Urgente*. "
            "Isso faria diferença na sua vida agora?"
        )
    
    # ========== AGUARDANDO ==========
    elif estado == "AGUARDANDO_DOCUMENTOS":
        add_bot_message(
            "Assim que tiver os documentos em mãos, retorne aqui para agendarmos sua reunião de estratégia. 😊"
        )
        st.session_state.estado = "FIM"
    
    elif estado == "AGUARDANDO_AGENDA":
        if _sim(resposta):
            add_bot_message(
                f"Ótimo! Vou encaminhar seus dados para a mesa da {L} neste momento.\n\n"
                f"Em instantes, ela entrará em contato aqui por este chat para te passar "
                f"a estratégia de liberação e os valores para o seu caso.\n\n"
                f"Fique atento(a)! 👀"
            )
        st.session_state.estado = "FIM"

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
        if st.session_state.dados.get("tipo_demanda"):
            st.markdown(f"**Demanda:** {st.session_state.dados['tipo_demanda']}")
        if st.session_state.dados.get("especialidade"):
            st.markdown(f"**Especialidade:** {st.session_state.dados['especialidade']}")
        
        st.markdown("---")
        if st.button("🔄 Nova Conversa", use_container_width=True):
            reset_conversa()
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

def render_opcoes_rapidas():
    estado = st.session_state.estado
    
    # Botões para opções comuns
    if estado == "CANAL":
        st.markdown("---")
        st.markdown("**🔘 Selecione uma opção:**")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🏥 SUS", use_container_width=True):
                add_user_message("SUS")
                processar_resposta("SUS")
                st.rerun()
        with col2:
            if st.button("📋 Plano de Saúde", use_container_width=True):
                add_user_message("Plano de Saúde")
                processar_resposta("Plano de Saúde")
                st.rerun()
    
    elif estado == "SUS_DEMANDA":
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔪 Cirurgia / Tratamento", use_container_width=True):
                add_user_message("Cirurgia / Tratamento")
                processar_resposta("Cirurgia / Tratamento")
                st.rerun()
        with col2:
            if st.button("📋 Consultas / Exames", use_container_width=True):
                add_user_message("Consultas / Exames")
                processar_resposta("Consultas / Exames")
                st.rerun()
    
    elif estado == "SUS_ESPECIALIDADE_CIRURGIA":
        st.markdown("---")
        st.markdown("**🔘 Selecione a especialidade:**")
        especialidades = ["Oncologia", "Neurodivergências", "Endometriose", "Medicamento", "Bariátrica", "Reparadora", "Neurologia", "Cardiologia", "Outros"]
        cols = st.columns(3)
        for i, esp in enumerate(especialidades):
            with cols[i % 3]:
                if st.button(esp[:20], key=f"esp_{i}", use_container_width=True):
                    add_user_message(esp)
                    processar_resposta(esp)
                    st.rerun()
    
    elif estado in ["HONORARIOS", "DECISAO_COMPARTILHADA"]:
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ SIM", use_container_width=True):
                add_user_message("SIM")
                processar_resposta("SIM")
                st.rerun()
        with col2:
            if st.button("❌ NÃO", use_container_width=True):
                add_user_message("NÃO")
                processar_resposta("NÃO")
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
        send_button = st.button("📤 Enviar", use_container_width=True)
    
    # Interceptar perguntas sobre valores
    if user_input and any(p in _n(user_input) for p in ["valor", "quanto", "preço", "custa", "honorário", "investimento"]):
        tipo = st.session_state.dados.get("tipo_demanda", "")
        if "cirurgia" in tipo or "tratamento" in tipo:
            add_bot_message(MSG_VALORES_CIRURGIA)
        else:
            add_bot_message(MSG_VALORES_CONSULTA)
        st.rerun()
    
    if send_button and user_input:
        add_user_message(user_input)
        processar_resposta(user_input)
        st.rerun()

# ============================================
# MAIN
# ============================================

def main():
    st.title("⚖️ Iara Bot - Assistente Jurídica em Direito da Saúde")
    st.caption(f"{L} | Atendimento SUS e Planos de Saúde")
    
    init_session_state()
    
    col1, col2 = st.columns([3, 1])
    with col1:
        render_chat()
        render_opcoes_rapidas()
        render_input()
    with col2:
        render_sidebar()
    
    if len(st.session_state.messages) == 0:
        add_bot_message(MSG_BOAS_VINDAS)
        st.rerun()

if __name__ == "__main__":
    main()
