em não quer correr o risco de negativas por erros na documentação "
    "e deseja que o escritório cuide de toda a parte burocrática e jurídica desde o primeiro dia.\n\n"
    "Atenção: Para esse acompanhamento completo e personalizado, o escritório cobra honorários de assessoria. "
    "Você gostaria de agendar uma reunião para conhecer os valores e como funciona esse suporte jurídico de ponta a ponta?"
)

PS_OP3_CONSULTORIA = (
    "Entendido. Para casos cautelosos com o seu, realizamos uma Consultoria Jurídica.\n\n"
    "Nesta reunião online um advogado especialista em Direito da Saúde analisará detalhadamente o seu caso, documentos e contratos para te entregar um parecer seguro sobre os seus direitos.\n\n"
    "Informações sobre a Consultoria:\n"
    "• Investimento: R$ 500,00 (referente à análise técnica e reserva de horário).\n"
    "• Duração: Até 1 hora.\n"
    "• Objetivo: Diagnóstico completo e estratégia jurídica personalizada.\n\n"
    "Deseja prosseguir com o agendamento?"
)
PS_OP3_PAGAMENTO = (
    "Perfeito! Vamos reservar o seu horário.\n\n"
    "Como deseja realizar o investimento do atendimento? Você prefere Pix ou Cartão de Crédito?"
)
PS_OP3_CONFIRMACAO = "Ao realizar o pagamento e for dado baixa no nosso financeiro, alguém da nossa equipe vai entrar em contato o quanto antes pra marcar seu atendimento na agenda da Dra Lethicia."

# Opção 4 removida - agora temos apenas 3 opções

# Encerramento geral
PS_ENCERRAMENTO = (
    "Entendo perfeitamente e respeito sua decisão.\n\n"
    "Vou encerrar o seu atendimento por aqui para priorizar os casos que já estão com procedimentos em andamento. "
    "Lembre-se apenas que, no Direito da Saúde, o tempo é um fator determinante para o sucesso do tratamento.\n\n"
    "Caso precise de suporte especializado no futuro, nossos canais continuam à disposição."
)

# Decisão compartilhada (ATUALIZADA)
DECISAO_SIM = (
    "Excelente! É fundamental que ele(a) participe, pois como o Direito à Saúde envolve "
    "prazos muito curtos e decisões imediatas sobre o tratamento, é bom que todos "
    "estejam na mesma página.\n\n"
    f"Vamos escolher um horário que fique confortável para vocês dois... "
    f"Logo abaixo vou te mandar a agenda da {L}. Escolha um melhor dia e horário que se encaixe adequadamente na sua agenda.\n\n"
    f"{CALENDLY_LINK}"
)

DECISAO_NAO = (
    "Perfeito, facilita bastante o nosso fluxo. Como você é a única responsável pela decisão, "
    "conseguimos dar um andamento mais ágil aos trabalhos...\n\n"
    f"Logo abaixo vou te mandar a agenda da {L}. Escolha um melhor dia e horário que se encaixe adequadamente na sua agenda.\n\n"
    f"{CALENDLY_LINK}"
)

MSG_FOLLOWUP_LINK = "Estou passando pra saber se você conseguiu acessar o link de agendamento da reunião. Se não conseguiu, basta copiar e colar o link no seu navegador."

DECISAO_REPASSE = (
    "Entendo! Olha, eu sugiro fortemente que ele tente participar, nem que seja apenas "
    "nos primeiros 10 minutos. No Direito à Saúde, os detalhes técnicos sobre a negativa da operadora "
    "costumam gerar muitas dúvidas e, se ele ouvir direto de mim, vocês ganham muito mais segurança para decidir rápido.\n\n"
    "Conseguimos um horário em que ele possa entrar na chamada, ou prefere manter só entre nós por enquanto?"
)

DECISAO_REPASSE_SIM = f"Perfeito! Vamos agendar para vocês dois. Logo abaixo vou te mandar a agenda da {L}. Escolha um melhor dia e horário que se encaixe adequadamente na sua agenda.\n\n{CALENDLY_LINK}"

DECISAO_REPASSE_NAO = f"Entendido! Mantemos só entre nós. Logo abaixo vou te mandar a agenda da {L}. Escolha um melhor dia e horário que se encaixe adequadamente na sua agenda.\n\n{CALENDLY_LINK}"

MSG_AGENDAMENTO_FINALIZADO = (
    "Perfeito. Todas as informações foram registradas com sucesso. A partir de agora, nossa equipe interna assume o acompanhamento para garantir que tudo esteja pronto para o seu atendimento. Tenha um excelente dia e até breve!"
)

MSG_DOCS_INSUFICIENTES = (
    "Entendi sua situação. Para que eu consiga te ajudar judicialmente a conseguir seu atendimento no SUS, "
    "o juiz exige obrigatoriamente alguns documentos que comprovam que o Estado está falhando com você.\n\n"
    "Sem um laudo médico atualizado e o comprovante de inscrição na fila de espera, o processo corre o risco de ser negado logo no início.\n\n"
    "Minha orientação agora: vá até a unidade de saúde, peça a atualização do seu laudo e tire uma foto do comprovante da fila. "
    "Assim que tiver esses papéis em mãos, me envie aqui para agendarmos nossa reunião de estratégia, combinado?"
)

MSG_AGUARDO_RETORNO = "Aguardo o seu retorno o mais breve possível. Até mais!"

MSG_NEG_MATERIAL = "O seu caso foi negado a cirurgia ou algum material/prótese/órtese essencial pra que seja realizada?"


# ====
# HELPER: SUS - identificar falta de documentos essenciais
# ====
def _resposta_negativa_docs_sus(txt: str) -> bool:
    """Detecta respostas negativas relacionadas a laudo, exame, comprovante, fila, receita ou relatório."""
    n = _n(txt)
    negativos = [
        "não", "nao", "não tenho", "nao tenho", "não possuo", "nao possuo",
        "sem", "não fiz", "nao fiz", "não peguei", "nao peguei",
        "não tenho foto", "nao tenho foto", "não tenho print", "nao tenho print",
        "não tenho comprovante", "nao tenho comprovante", "não tenho laudo", "nao tenho laudo",
        "não tenho exame", "nao tenho exame", "não tenho exames", "nao tenho exames",
        "não tenho relatório", "nao tenho relatorio", "não tenho receita", "nao tenho receita"
    ]
    return any(x in n for x in negativos)

def _pergunta_docs_sus(txt: str) -> bool:
    """Identifica perguntas do SUS que tratam de documentos/provas essenciais."""
    n = _n(txt)
    chaves = [
        "laudo", "relatório", "relatorio", "exame", "exames", "receita",
        "comprovante", "fila", "sisreg", "meu sus", "print", "protocolo",
        "encaminhamento", "pedido médico", "pedido/encaminhamento", "biópsia", "biopsia"
    ]
    return any(c in n for c in chaves)

def _sus_docs_insuficientes(prefixo_resp: str, perguntas=None) -> bool:
    """
    Retorna True quando a maior parte das respostas às perguntas documentais do SUS
    indica ausência de laudo, exames, comprovante de fila, receita, pedido ou protocolo.
    """
    if perguntas is None:
        perguntas = st.session_state.perguntas_ativas
    total_docs = 0
    negativas_docs = 0
    for i, pergunta in enumerate(perguntas or []):
        if _pergunta_docs_sus(pergunta):
            total_docs += 1
            if _resposta_negativa_docs_sus(st.session_state.dados.get(f"{prefixo_resp}{i}", "")):
                negativas_docs += 1
    return total_docs > 0 and negativas_docs >= max(1, (total_docs // 2) + (total_docs % 2))

def _encaminhar_docs_insuficientes_sus():
    st.session_state.estado = "SUS_DOCS_INSUF"
    add_bot(MSG_DOCS_INSUFICIENTES)

# ====
# HELPER: detectar pergunta sobre valores
# ====
def _e_pergunta_valor(r: str) -> bool:
    texto = _n(r)
    palavras = [
        "valor", "quanto é", "quanto e", "quanto custa", "preço", "preco",
        "custa", "honorário", "honorario", "investimento", "cobram",
        "custo", "quanto é pago", "quanto e pago", "quanto pago", "é pago", "e pago"
    ]
    return any(p in texto for p in palavras)



def _resposta_e_opcao_de_fluxo_valor(resposta: str) -> bool:
    """Evita que opções internas do fluxo sejam confundidas com pergunta sobre honorários/valores.

    Ex.: no fluxo de Medicamento Negado, a opção "Alto custo" é motivo da negativa
    do plano, não uma pergunta do cliente sobre valor do serviço jurídico.
    """
    texto = _n(resposta)
    texto_limpo = re.sub(r"^[0-9]+\s*️⃣?\s*", "", texto).strip()
    opcoes_fluxo = {
        "alto custo",
        "2 alto custo",
        "2️⃣ alto custo",
        "uso domiciliar",
        "experimental/off-label",
        "fora do rol da ans",
        "não atende diretriz (dut)",
        "nao atende diretriz (dut)",
        "carência",
        "carencia",
        "não é urgente",
        "nao é urgente",
        "experimental",
        "outro",
    }
    if texto in opcoes_fluxo or texto_limpo in opcoes_fluxo:
        # Confirma que a pergunta ativa é de opção/motivo de negativa, para não bloquear
        # perguntas reais sobre preço feitas fora desse contexto.
        perguntas = st.session_state.get("perguntas_ativas", []) or []
        idx = st.session_state.get("pergunta_idx", 0)
        pergunta_atual = perguntas[idx] if idx < len(perguntas) else ""
        ultima_bot = next((m.get("content", "") for m in reversed(st.session_state.get("messages", [])) if m.get("role") == "bot"), "")
        contexto = _n(f"{pergunta_atual} {ultima_bot}")
        if "qual foi o motivo da negativa" in contexto or "motivo da negativa" in contexto:
            return True
    return False

def _contexto_valor_analise_inicial() -> bool:
    dados = st.session_state.dados
    estado = st.session_state.estado
    canal = dados.get("canal")
    situacao = _n(dados.get("situacao", ""))
    subtipo = _n(dados.get("subtipo", ""))
    tipo = _n(dados.get("tipo", ""))

    # Casos do SUS: consultas e exames.
    if canal == "SUS" and (
        tipo == "consulta_exame"
        or subtipo in ("consulta", "exame")
        or estado.startswith("SUS_CONSULTA")
        or estado.startswith("SUS_EXAME")
    ):
        return True

    # Casos de Plano de Saúde: exame negado e terapias.
    if canal == "PLANO" and ("exame negado" in situacao or "terapias" in situacao):
        return True

    return False

def _msg_valor():
    dados = st.session_state.dados
    situacao = _n(dados.get("situacao", ""))
    if "reajuste" in situacao or "coparticipação" in situacao or "copa" in situacao:
        return MSG_VALORES_REAJUSTE
    return MSG_VALORES_CIRURGIA

def iniciar_interceptacao_valor_analise():
    st.session_state.estado_antes_valor = st.session_state.estado
    st.session_state.dados_antes_valor = st.session_state.dados.copy()
    st.session_state.mensagem_antes_valor = next(
        (m.get("content") for m in reversed(st.session_state.messages) if m.get("role") == "bot"),
        None
    )
    st.session_state.estado = "PERGUNTA_VALOR_ANALISE"
    add_bot(MSG_VALORES_ANALISE_INICIAL)

def iniciar_interceptacao_valor_geral():
    """Pausa o fluxo quando a pessoa pergunta sobre valores e retoma após resposta afirmativa."""
    st.session_state.estado_antes_valor = st.session_state.estado
    st.session_state.dados_antes_valor = st.session_state.dados.copy()
    st.session_state.mensagem_antes_valor = next(
        (m.get("content") for m in reversed(st.session_state.messages) if m.get("role") == "bot"),
        None
    )
    st.session_state.estado = "PERGUNTA_VALOR_GERAL"
    add_bot(_msg_valor())

def voltar_apos_pergunta_valor(resposta: str):
    if _sim(resposta):
        estado_anterior = st.session_state.estado_antes_valor
        mensagem_anterior = st.session_state.mensagem_antes_valor
        st.session_state.estado = estado_anterior
        if st.session_state.dados_antes_valor:
            st.session_state.dados = st.session_state.dados_antes_valor.copy()
        st.session_state.estado_antes_valor = None
        st.session_state.dados_antes_valor = None
        st.session_state.mensagem_antes_valor = None
        if mensagem_anterior:
            add_bot(mensagem_anterior, delay=0)
        return True
    else:
        add_bot(PS_ENCERRAMENTO)
        st.session_state.estado = "FIM"
        st.session_state.estado_antes_valor = None
        st.session_state.dados_antes_valor = None
        st.session_state.mensagem_antes_valor = None
        return False

def iniciar_fluxo_orientacao_97():
    """Inicia o pré-fluxo obrigatório antes da mensagem de consulta paga de R$ 97,00."""
    add_bot(PS_CONSULTA_ORIENTACAO_INTRO)
    st.session_state.estado = "PS_CONSULTA_97_DECISAO"
    add_bot(PS_CONSULTA_ORIENTACAO_OPCOES)

def iniciar_fluxo_reparadora_97():
    """Inicia o pré-fluxo específico de reparadoras antes da consulta paga de R$ 97,00."""
    add_bot(PS_REP_ORIENTACAO_INTRO)
    st.session_state.estado = "PS_CONSULTA_97_DECISAO"
    add_bot(PS_REP_ORIENTACAO_OPCOES)

# Função para obter nome da especialidade (não o número)
def get_nome_especialidade(valor):
    mapa = {
        "1": "endometriose/adenomiose",
        "2": "Bariátrica", 
        "3": "Oncologia (câncer)",
        "4": "Cardiologia",
        "5": "Neurocirurgia",
        "6": "Ortopedia",
        "7": "Oftalmologia",
        "8": "OUTRO"
    }
    return mapa.get(valor, valor)


MSG_ESCALA_URGENCIA = (
    "Em uma escala de 1 a 5, o quanto esse problema é urgente para você hoje?\n(Sendo 1 não urgente e 5 muito urgente)\n\n"
    "1️⃣ 1\n2️⃣ 2\n3️⃣ 3\n4️⃣ 4\n5️⃣ 5"
)

def _perguntar_escala_urgencia(retorno_estado: str, proxima_msg: str = None, proximo_estado: str = None, chave: str = None):
    """Pausa o fluxo após a terceira pergunta da área e coleta a urgência de 1 a 5."""
    st.session_state.urgencia_retorno_estado = retorno_estado
    st.session_state.urgencia_proxima_msg = proxima_msg
    st.session_state.urgencia_proximo_estado = proximo_estado or retorno_estado
    st.session_state.urgencia_chave = chave or retorno_estado
    st.session_state.estado = "ESCALA_URGENCIA"
    add_bot(MSG_ESCALA_URGENCIA)

def _retomar_apos_escala_urgencia(resposta: str):
    chave = st.session_state.get("urgencia_chave") or "geral"
    st.session_state.dados[f"urgencia_{chave}"] = resposta
    proximo_estado = st.session_state.get("urgencia_proximo_estado") or st.session_state.get("urgencia_retorno_estado")
    proxima_msg = st.session_state.get("urgencia_proxima_msg")
    st.session_state.urgencia_retorno_estado = None
    st.session_state.urgencia_proxima_msg = None
    st.session_state.urgencia_proximo_estado = None
    st.session_state.urgencia_chave = None
    st.session_state.estado = proximo_estado
    if proxima_msg:
        add_bot(proxima_msg)

# ====
# PROCESSAMENTO DO FLUXO
# ====

def processar(resposta: str):
    pergunta_atual = ""
    if st.session_state.get("perguntas_ativas"):
        try:
            pergunta_atual = st.session_state.perguntas_ativas[st.session_state.pergunta_idx]
        except Exception:
            pergunta_atual = ""
    estado = st.session_state.estado
    dados  = st.session_state.dados

    # Atualiza timestamp da última resposta do usuário
    st.session_state.aguardando_resposta_desde = None

    # Interceptação global de perguntas sobre resultado/garantia/medo de perder.
    # Fica antes de qualquer outro estado para funcionar em qualquer etapa do fluxo,
    # inclusive durante escala de urgência, perguntas com botões, valores e finais de rota.
    if estado == "PERGUNTA_RESULTADOS":
        voltar_apos_pergunta_resultados(resposta)
        return

    if estado not in ("INICIO", "FIM") and verificar_pergunta_resultados(resposta):
        processar_pergunta_resultados(resposta)
        return

    # Resposta à escala de urgência inserida após a terceira pergunta da área
    if estado == "ESCALA_URGENCIA":
        _retomar_apos_escala_urgencia(resposta)
        return

    # Estado especial para resposta da pergunta sobre valores
    if estado in ("PERGUNTA_VALOR_ANALISE", "PERGUNTA_VALOR_GERAL"):
        voltar_apos_pergunta_valor(resposta)
        return

    # Interceptar perguntas de valor em qualquer estado (exceto INICIO)
    if (
        estado not in ("INICIO", "FIM", "PERGUNTA_VALOR_ANALISE", "PERGUNTA_VALOR_GERAL")
        and _e_pergunta_valor(resposta)
        and not _resposta_e_opcao_de_fluxo_valor(resposta)
    ):
        if _contexto_valor_analise_inicial():
            iniciar_interceptacao_valor_analise()
        else:
            iniciar_interceptacao_valor_geral()
        return

    # ==== INICIO ====
    if estado == "INICIO":
        st.session_state.nome = resposta
        dados["nome"] = resposta
        st.session_state.estado = "CANAL"
        add_bot(MSG_CANAL.format(nome=resposta))

    # ==== CANAL ====
    elif estado == "CANAL":
        if "sus" in _n(resposta):
            dados["canal"] = "SUS"
            st.session_state.estado = "SUS_DEMANDA"
            add_bot(MSG_SUS_DEMANDA)
        else:
            dados["canal"] = "PLANO"
            st.session_state.estado = "PS_TEMPO"
            add_bot(PS_TEMPO)

    # ====
    # SUS
    # ====

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
        _perguntar_escala_urgencia("SUS_CONSULTA_PITCH", MSG_SUS_CONSULTA_PITCH, "SUS_CONSULTA_PITCH", "sus_consulta")
        return
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
        add_bot(SUS_PROVA_SOCIAL_CONSULTA_A25)
        st.session_state.estado = "SUS_CONSULTA_AJUDA_Q3"
        add_bot(MSG_SUS_CONSULTA_AJUDA_Q3)
    elif estado == "SUS_CONSULTA_AJUDA_Q3":
        dados["consulta_exame"] = resposta
        st.session_state.estado = "SUS_CONSULTA_AJUDA_Q4"
        add_bot(MSG_SUS_CONSULTA_AJUDA_Q4)
    elif estado == "SUS_CONSULTA_AJUDA_Q4":
        dados["consulta_docs"] = resposta
        st.session_state.estado = "SUS_CONSULTA_AJUDA_Q4B"
        add_bot(MSG_SUS_CONSULTA_AJUDA_Q4B)
    elif estado == "SUS_CONSULTA_AJUDA_Q4B":
        dados["consulta_pedido"] = resposta
        consulta_docs_negativos = sum(
            1 for chave in ("consulta_docs", "consulta_pedido")
            if _resposta_negativa_docs_sus(dados.get(chave, ""))
        )
        if consulta_docs_negativos >= 1:
            _encaminhar_docs_insuficientes_sus()
        else:
            st.session_state.estado = "SUS_CONSULTA_PROTOCOLO"
            add_bot(MSG_SUS_CONSULTA_PROTOCOLO)
    elif estado == "SUS_CONSULTA_PROTOCOLO":
        if _sim(resposta):
            st.session_state.estado = "SUS_CONSULTA_HONORARIOS"
            add_bot("Como é um trabalho de alta especialidade, o escritório cobra um valor de Honorários Iniciais para assumir o caso e protocolar o pedido judicial. Prosseguir com esse caso faz sentido para você garantir sua saúde hoje e sair dessa espera?")
        else:
            add_bot(MSG_ENCERRAMENTO_SUS)
            st.session_state.estado = "FIM"
    elif estado == "SUS_CONSULTA_HONORARIOS":
        if _sim(resposta):
            add_bot("Ótimo. Isso mostra que você prioriza sua saúde acima da burocracia do Estado.\n\nVou encaminhar seus dados para a mesa da Dra. Lethicia neste momento. Em instantes, ela entrará em contato aqui por este chat para te passar a estratégia de liberação e os valores para o seu caso. Fique atento(a)!")
        else:
            add_bot("Compreendo. Infelizmente, sem o interesse em avançar com uma medida judicial, o seu caso continuará dependendo exclusivamente da velocidade da fila do SUS, que como sabemos, não tem previsão.\n\nComo o escritório da Dra. Lethicia foca apenas em quem deseja forçar a solução imediata, estamos encerrando seu atendimento por aqui.\n\nCaso a sua situação se agrave ou você decida que não pode mais esperar, sinta-se à vontade para retornar. Desejamos sorte no seu tratamento.")
        st.session_state.estado = "FIM"

    # FLUXO EXAME
    elif estado == "SUS_EXAME_Q1":
        dados["exame_nome"] = resposta
        st.session_state.estado = "SUS_EXAME_FILA_INFO"
        add_bot(MSG_SUS_EXAME_FILA_INFO)
    elif estado == "SUS_EXAME_FILA_INFO":
        dados["exame_info_fila"] = resposta
        add_bot(SUS_PROVA_SOCIAL_EXAME_A25_A24)
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
        if idx == 3 and not dados.get("urgencia_sus_exame_feita"):
            dados["urgencia_sus_exame_feita"] = True
            proxima = st.session_state.perguntas_ativas[idx] if idx < len(st.session_state.perguntas_ativas) else None
            _perguntar_escala_urgencia("SUS_EXAME_PERGUNTAS", proxima, "SUS_EXAME_PERGUNTAS", "sus_exame")
            return
        if idx < len(st.session_state.perguntas_ativas):
            proxima_pergunta = st.session_state.perguntas_ativas[idx]
            # Coparticipação: a mensagem explicativa deve vir seguida imediatamente
            # da pergunta sobre contrato, sem aguardar resposta entre as duas.
            if "copart" in _n(dados.get("situacao", "")) and proxima_pergunta == PS_COPA_Q6:
                add_bot(PS_COPA_Q6)
                add_bot(PS_COPA_Q7)
                st.session_state.pergunta_idx = idx + 1
                return
            add_bot(proxima_pergunta)
        else:
            if _sus_docs_insuficientes("exame_resp_"):
                _encaminhar_docs_insuficientes_sus()
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
            st.session_state.estado = "SUS_EXAME_HONORARIOS"
            add_bot("Como é um trabalho de alta especialidade, o escritório cobra um valor de Honorários Iniciais para assumir o caso e protocolar o pedido judicial. Prosseguir com esse caso faz sentido para você garantir sua saúde hoje e sair dessa espera?")
        else:
            add_bot(MSG_ENCERRAMENTO_SUS)
            st.session_state.estado = "FIM"
    elif estado == "SUS_EXAME_HONORARIOS":
        if _sim(resposta):
            add_bot("Ótimo. Isso mostra que você prioriza sua saúde acima da burocracia do Estado.\n\nVou encaminhar seus dados para a mesa da Dra. Lethicia neste momento. Em instantes, ela entrará em contato aqui por este chat para te passar a estratégia de liberação e os valores para o seu caso. Fique atento(a)!")
        else:
            add_bot("Compreendo. Infelizmente, sem o interesse em avançar com uma medida judicial, o seu caso continuará dependendo exclusivamente da velocidade da fila do SUS, que como sabemos, não tem previsão.\n\nComo o escritório da Dra. Lethicia foca apenas em quem deseja forçar a solução imediata, estamos encerrando seu atendimento por aqui.\n\nCaso a sua situação se agrave ou você decida que não pode mais esperar, sinta-se à vontade para retornar. Desejamos sorte no seu tratamento.")
        st.session_state.estado = "FIM"

    # ---- SUS CIRURGIA ----
    elif estado == "SUS_ESPECIALIDADE":
        if "oncologia" in _n(resposta) or "1" in resposta:
            st.session_state.perguntas_ativas = PERGUNTAS_ONCOLOGIA.copy()
            dados["especialidade"] = "Oncologia"
        elif "neuro" in _n(resposta) and ("tea" in _n(resposta) or "tdah" in _n(resposta) or "diverg" in _n(resposta) or "2" in resposta):
            st.session_state.perguntas_ativas = PERGUNTAS_NEURO.copy()
            dados["especialidade"] = "Neurodivergências"
        elif "endometriose" in _n(resposta) or "adenomiose" in _n(resposta) or "3" in resposta:
            st.session_state.perguntas_ativas = PERGUNTAS_ENDOMETRIOSE.copy()
            dados["especialidade"] = "Endometriose"
        elif "medicamento" in _n(resposta) or "4" in resposta:
            st.session_state.perguntas_ativas = PERGUNTAS_MEDICAMENTO_SUS.copy()
            dados["especialidade"] = "Medicamento"
        elif "bariátrica" in _n(resposta) or "bariatrica" in _n(resposta) or "5" in resposta:
            st.session_state.perguntas_ativas = PERGUNTAS_BARIATRICA_SUS.copy()
            dados["especialidade"] = "Bariátrica"
        elif "neurologia" in _n(resposta) or "neurocirurgia" in _n(resposta) or "6" in resposta:
            st.session_state.perguntas_ativas = PERGUNTAS_NEUROLOGIA_SUS.copy()
            dados["especialidade"] = "Neurologia"
        elif "cardiologia" in _n(resposta) or "7" in resposta:
            st.session_state.perguntas_ativas = PERGUNTAS_CARDIOLOGIA_SUS.copy()
            dados["especialidade"] = "Cardiologia"
        else:
            st.session_state.perguntas_ativas = PERGUNTAS_OUTROS_SUS.copy()
            dados["especialidade"] = "Outros"

        st.session_state.pergunta_idx = 0
        st.session_state.estado = "SUS_PERGUNTAS"
        add_bot(st.session_state.perguntas_ativas[0])

    elif estado == "SUS_PERGUNTAS":
        idx = st.session_state.pergunta_idx
        dados[f"resp_{idx}"] = resposta
        if "qual foi o motivo da negativa" in _n(locals().get("pergunta_atual", "")):
            dados["motivo_negativa_ja_perguntado"] = True
        idx += 1
        st.session_state.pergunta_idx = idx
        
        # Verificar se é oncologia e precisa pular a pergunta dos 60 dias se benigno
        especialidade = dados.get("especialidade", "")
        is_oncologia = "oncologia" in _n(especialidade)
        
        if is_oncologia and idx == 5:  # Índice da pergunta dos 60 dias
            # Verificar se o câncer é maligno (resposta da pergunta 1 - benigno/maligno)
            resp_benigno_maligno = _n(dados.get("resp_1", ""))
            if "benigno" in resp_benigno_maligno or "benigna" in resp_benigno_maligno:
                # Pular a pergunta dos 60 dias
                idx += 1
                st.session_state.pergunta_idx = idx
        
        if idx == 3 and not dados.get("urgencia_sus_cirurgia_feita"):
            dados["urgencia_sus_cirurgia_feita"] = True
            proxima = st.session_state.perguntas_ativas[idx] if idx < len(st.session_state.perguntas_ativas) else None
            _perguntar_escala_urgencia("SUS_PERGUNTAS", proxima, "SUS_PERGUNTAS", "sus_cirurgia")
            return

        if idx < len(st.session_state.perguntas_ativas):
            next_q = st.session_state.perguntas_ativas[idx]
            add_bot(next_q)
            if is_oncologia and idx == 1:
                st.session_state.estado = "SUS_ONCOLOGIA_BENIGNO_MALIGNO"
                return
        else:
            if _sus_docs_insuficientes("resp_"):
                _encaminhar_docs_insuficientes_sus()
            else:
                st.session_state.estado = "POS_PERGUNTAS_SUS"
                add_bot(MSG_POS_PERGUNTAS_SUS.replace("{nome}", st.session_state.nome or ""))

    elif estado == "SUS_ONCOLOGIA_BENIGNO_MALIGNO":
        dados[f"resp_{st.session_state.pergunta_idx}"] = resposta
        idx = st.session_state.pergunta_idx + 1
        # Se for benigno, pular a pergunta dos 60 dias
        if "benigno" in _n(resposta):
            idx += 1
        st.session_state.pergunta_idx = idx
        st.session_state.estado = "SUS_PERGUNTAS"
        if idx < len(st.session_state.perguntas_ativas):
            proxima_pergunta = st.session_state.perguntas_ativas[idx]
            # Coparticipação: a mensagem explicativa deve vir seguida imediatamente
            # da pergunta sobre contrato, sem aguardar resposta entre as duas.
            if "copart" in _n(dados.get("situacao", "")) and proxima_pergunta == PS_COPA_Q6:
                add_bot(PS_COPA_Q6)
                add_bot(PS_COPA_Q7)
                st.session_state.pergunta_idx = idx + 1
                return
            add_bot(proxima_pergunta)
        else:
            if _sus_docs_insuficientes("resp_"):
                _encaminhar_docs_insuficientes_sus()
            else:
                st.session_state.estado = "POS_PERGUNTAS_SUS"
                add_bot(MSG_POS_PERGUNTAS_SUS.replace("{nome}", st.session_state.nome or ""))

    elif estado == "POS_PERGUNTAS_SUS":
        dados["sentimento"] = resposta
        if _sus_docs_insuficientes("resp_"):
            _encaminhar_docs_insuficientes_sus()
        else:
            prova_sus = _prova_social_sus_pos_respostas()
            if prova_sus:
                add_bot(prova_sus)
            st.session_state.estado = "PROPOSTA_SUS"
            add_bot(MSG_EXPLICACAO_SUS)

    elif estado == "SUS_DOCS_INSUF":
        n = _n(resposta)
        if "certo" in n or "vou fazer" in n or "ok" in n or "sim" in n or _sim(resposta):
            add_bot(MSG_AGUARDO_RETORNO)
        else:
            add_bot(MSG_AGUARDO_RETORNO)
        st.session_state.estado = "FIM"

    elif estado == "PROPOSTA_SUS":
        if _sim(resposta):
            st.session_state.estado = "HONORARIOS_SUS"
            add_bot(MSG_HONORARIOS_SUS)
        else:
            add_bot(MSG_ENCERRAMENTO_SUS)
            st.session_state.estado = "FIM"

    elif estado == "HONORARIOS_SUS":
        if _sim(resposta):
            add_bot(MSG_REVERTER_SUS)
            st.session_state.estado = "DECISAO_COMPARTILHADA"
            add_bot(MSG_SIM_HONORARIOS_SUS_DECISAO)
        else:
            add_bot(MSG_ENCERRAMENTO_SUS)
            st.session_state.estado = "FIM"

    # ====
    # PLANO DE SAÚDE
    # ====

    elif estado == "PS_TEMPO":
        if _sim(resposta):
            dados["plano_2anos"] = "sim"
            dados["plano_tipo"] = "mais_de_2_anos"
            st.session_state.estado = "PS_SITUACAO"
            add_bot(PS_SITUACAO)
        else:
            dados["plano_2anos"] = "nao"
            st.session_state.estado = "PS_TEMPO_NAO_SEGUIMENTO"
            add_bot(PS_TEMPO_NAO_SEGUIMENTO)

    # NOVO: Pergunta sobre tipo de plano (pessoa física ou empresarial) após NÃO
    elif estado == "PS_TEMPO_NAO_SEGUIMENTO":
        dados["plano_tipo_resposta"] = resposta
        if "empresarial" in _n(resposta) or "cnpj" in _n(resposta):
            # Trata como SIM (mais de 2 anos)
            dados["plano_tipo"] = "empresarial"
            st.session_state.estado = "PS_SITUACAO"
            add_bot(PS_SITUACAO)
        else:
            # Pessoa física - continua como NÃO.
            # Envia a explicação e já pergunta o tratamento, sem aguardar nova resposta entre as mensagens.
            dados["plano_tipo"] = "pessoa_fisica"
            add_bot(PS_NAO_2ANOS_EDUCACAO)
            st.session_state.estado = "PS_NAO_2ANOS_Q1"
            add_bot(PS_NAO_2ANOS_Q1)

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
        add_bot(PS_NAO_2ANOS_FEEDBACK)
        st.session_state.estado = "PS_NAO_2ANOS_Q3"
        add_bot(PS_NAO_2ANOS_Q3)
    elif estado == "PS_NAO_2ANOS_FEEDBACK":
        # Compatibilidade com conversas iniciadas em versões anteriores.
        st.session_state.estado = "PS_NAO_2ANOS_Q3"
        add_bot(PS_NAO_2ANOS_Q3)
    elif estado == "PS_NAO_2ANOS_Q3":
        dados["urgencia_medica"] = resposta
        _perguntar_escala_urgencia("PS_NAO_2ANOS_Q4", PS_NAO_2ANOS_Q4, "PS_NAO_2ANOS_Q4", "plano_menos_2_anos")
        return
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
        # Envia mensagens pré-pos busca
        add_bot(MSG_PRE_POS_BUSCA_1)
        add_bot(MSG_PRE_POS_BUSCA_2)
        st.session_state.estado = "PS_POS_BUSCA"
        add_bot(PS_POS_BUSCA)

    # Caminho SIM - Situação
    elif estado == "PS_SITUACAO":
        dados["situacao"] = resposta
        resp_n = _n(resposta)
        opcao = _opcao_numero(resposta)

        # Nova numeração da pergunta principal de Plano de Saúde:
        # 0 Reparadora | 1 Negativa de cirurgia | 2 Medicamento | 3 Exame |
        # 4 Home care | 5 Terapias | 6 Reajuste | 7 Coparticipação |
        # 8 Erro médico | 9 OUTRO
        if opcao == "9" or "outro" in resp_n:
            dados["situacao"] = "outro"
            st.session_state.estado = "PS_OUTRO_DEMANDA"
            st.session_state.outro_idx = 0
            add_bot(PS_OUTRO_DEMANDA_Q1)

        elif opcao == "0" or "reparadora" in resp_n:
            dados["situacao"] = "reparadora"
            st.session_state.estado = "PS_REP_Q1"
            add_bot(PS_REP_Q1)

        elif opcao == "1" or "negativa" in resp_n:
            dados["situacao"] = "negativa de cirurgia"
            st.session_state.estado = "PS_NEG_CIR_ESP"
            add_bot(PS_NEG_CIR_ESP)

        elif opcao == "2" or "medicamento" in resp_n:
            dados["situacao"] = "medicamento negado"
            st.session_state.perguntas_ativas = [
                PS_MED_Q1, PS_MED_Q2, PS_MED_Q2B, PS_MED_Q3, PS_MED_Q4, PS_MED_Q5,
                PS_MED_Q6, PS_MED_Q7, PS_MED_Q9, PS_MED_Q10
            ]
            st.session_state.pergunta_idx = 0
            st.session_state.estado = "PS_PERGUNTAS_COLETOR"
            add_bot(PS_MED_Q1)

        elif opcao == "3" or "exame" in resp_n:
            dados["situacao"] = "exame negado"
            st.session_state.perguntas_ativas = [
                PS_EXAME_Q1, PS_EXAME_Q2, PS_EXAME_Q3_E_Q4,
                PS_EXAME_Q5, PS_EXAME_Q6, PS_EXAME_Q7
            ]
            st.session_state.pergunta_idx = 0
            st.session_state.estado = "PS_PERGUNTAS_COLETOR"
            add_bot(PS_EXAME_Q1)

        elif opcao == "4" or "home" in resp_n:
            dados["situacao"] = "home care"
            st.session_state.perguntas_ativas = [
                PS_HOME_Q1, PS_HOME_Q2, PS_HOME_Q3, PS_HOME_Q4,
                PS_HOME_Q5, PS_HOME_Q6, PS_HOME_Q7
            ]
            st.session_state.pergunta_idx = 0
            st.session_state.estado = "PS_PERGUNTAS_COLETOR"
            add_bot(PS_HOME_Q1)

        elif opcao == "5" or "terapia" in resp_n:
            dados["situacao"] = "terapias"
            st.session_state.perguntas_ativas = [
                PS_TERA_Q1, PS_TERA_Q2, PS_TERA_Q3, PS_TERA_Q4,
                PS_TERA_Q5, PS_TERA_Q6, PS_TERA_Q7
            ]
            st.session_state.pergunta_idx = 0
            st.session_state.estado = "PS_PERGUNTAS_COLETOR"
            add_bot(PS_TERA_Q1)

        elif opcao == "6" or "reajuste" in resp_n:
            dados["situacao"] = "reajuste"
            st.session_state.perguntas_ativas = [
                PS_REAJ_Q1, PS_REAJ_Q2, PS_REAJ_Q3, PS_REAJ_Q4,
                PS_REAJ_Q5, PS_REAJ_Q6, PS_REAJ_Q7, PS_REAJ_Q8
            ]
            st.session_state.pergunta_idx = 0
            st.session_state.estado = "PS_PERGUNTAS_COLETOR"
            add_bot(PS_REAJ_Q1)

        elif opcao == "7" or "copart" in resp_n:
            dados["situacao"] = "coparticipação elevada"
            st.session_state.perguntas_ativas = [
                PS_COPA_Q1, PS_COPA_Q2, PS_COPA_Q3, PS_COPA_Q4,
                PS_COPA_Q5, PS_COPA_Q6, PS_COPA_Q7
            ]
            st.session_state.pergunta_idx = 0
            st.session_state.estado = "PS_PERGUNTAS_COLETOR"
            add_bot(PS_COPA_Q1)

        elif opcao == "8" or "erro" in resp_n:
            dados["situacao"] = "erro médico"
            st.session_state.perguntas_ativas = [
                PS_ERRO_Q1, PS_ERRO_Q2, PS_ERRO_Q3,
                PS_ERRO_Q4, PS_ERRO_Q5, PS_ERRO_Q6, PS_ERRO_Q7_ESTAGIO
            ]
            st.session_state.pergunta_idx = 0
            st.session_state.estado = "PS_PERGUNTAS_COLETOR"
            add_bot(PS_ERRO_Q1)

        else:
            dados["situacao"] = "outro"
            st.session_state.estado = "PS_OUTRO_DEMANDA"
            st.session_state.outro_idx = 0
            add_bot(PS_OUTRO_DEMANDA_Q1)

    # FLUXO OUTRO CORRIGIDO
    elif estado == "PS_OUTRO_DEMANDA":
        idx = st.session_state.get("outro_idx", 0)
        dados[f"outro_{idx}"] = resposta
        idx += 1
        st.session_state.outro_idx = idx
        
        if idx == 3 and not dados.get("urgencia_plano_outro_feita"):
            dados["urgencia_plano_outro_feita"] = True
            outro_qs_preview = [
                PS_OUTRO_DEMANDA_Q2, PS_OUTRO_DEMANDA_Q3, PS_OUTRO_DEMANDA_Q4,
                PS_OUTRO_DEMANDA_Q5, PS_OUTRO_DEMANDA_Q5B, PS_OUTRO_DEMANDA_Q6, PS_OUTRO_DEMANDA_Q7
            ]
            proxima = outro_qs_preview[idx - 1] if idx - 1 < len(outro_qs_preview) else None
            _perguntar_escala_urgencia("PS_OUTRO_DEMANDA", proxima, "PS_OUTRO_DEMANDA", "plano_outro")
            return

        outro_qs = [
            PS_OUTRO_DEMANDA_Q2, PS_OUTRO_DEMANDA_Q3, PS_OUTRO_DEMANDA_Q4,
            PS_OUTRO_DEMANDA_Q5, PS_OUTRO_DEMANDA_Q5B, PS_OUTRO_DEMANDA_Q6, PS_OUTRO_DEMANDA_Q7
        ]
        
        if idx < len(outro_qs) + 1:  # +1 porque Q1 já foi enviada
            q = outro_qs[idx - 1] if idx - 1 < len(outro_qs) else None
            if q:
                add_bot(q)
                if q == PS_OUTRO_DEMANDA_Q7:
                    # Após última pergunta, envia mensagens pré-pos busca
                    add_bot(MSG_PRE_POS_BUSCA_1)
                    add_bot(MSG_PRE_POS_BUSCA_2)
                    st.session_state.estado = "PS_POS_BUSCA"
                    add_bot(PS_POS_BUSCA)
        else:
            add_bot(MSG_PRE_POS_BUSCA_1)
            add_bot(MSG_PRE_POS_BUSCA_2)
            st.session_state.estado = "PS_POS_BUSCA"
            add_bot(PS_POS_BUSCA)

    # Coletor genérico
    elif estado == "PS_PERGUNTAS_COLETOR":
        idx = st.session_state.pergunta_idx
        pergunta_atual = st.session_state.perguntas_ativas[idx] if idx < len(st.session_state.perguntas_ativas) else ""
        dados[f"resp_{idx}"] = resposta
        idx += 1
        st.session_state.pergunta_idx = idx

        # Fluxo específico - Plano de Saúde / Bariátrica:
        # após a resposta da segunda pergunta, envia a mensagem explicativa e, imediatamente,
        # a escala de urgência, sem esperar resposta na mensagem explicativa.
        if (
            idx == 2
            and not dados.get("urgencia_plano_coletor_feita")
            and ("bari" in _n(dados.get("neg_cir_esp", "")) or str(dados.get("neg_cir_esp", "")).strip() == "2")
        ):
            dados["urgencia_plano_coletor_feita"] = True
            add_bot(PS_BARI_Q3_MSG)
            proxima = st.session_state.perguntas_ativas[idx] if idx < len(st.session_state.perguntas_ativas) else None
            _perguntar_escala_urgencia("PS_PERGUNTAS_COLETOR", proxima, "PS_PERGUNTAS_COLETOR", "plano_bariatrica")
            return

        # Prova social específica - Coparticipação: após a resposta à mensagem
        # "pagando para usar", envia a mensagem com marcador da imagem A13.png
        # e segue o fluxo normalmente.
        if pergunta_atual == PS_COPA_Q2 and not dados.get("prova_social_copa_a13_enviada"):
            dados["prova_social_copa_a13_enviada"] = True
            add_bot(PS_PROVA_SOCIAL_COPA_A13)

        if pergunta_atual == PS_REAJ_Q3 and not dados.get("prova_social_reajuste_a12_enviada"):
            dados["prova_social_reajuste_a12_enviada"] = True
            add_bot(PS_PROVA_SOCIAL_REAJUSTE_A12)

        if idx == 3 and not dados.get("urgencia_plano_coletor_feita"):
            dados["urgencia_plano_coletor_feita"] = True
            proxima = st.session_state.perguntas_ativas[idx] if idx < len(st.session_state.perguntas_ativas) else None
            _perguntar_escala_urgencia("PS_PERGUNTAS_COLETOR", proxima, "PS_PERGUNTAS_COLETOR", f"plano_{_n(dados.get('situacao', 'geral')).replace(' ', '_')}")
            return

        # Regra global - Plano de Saúde:
        # Sempre que a pessoa responder à pergunta "A negativa do plano foi por escrita ou verbal...",
        # o robô deve AGUARDAR essa resposta e, somente depois, perguntar o motivo da negativa.
        if "escrita ou verbal" in _n(pergunta_atual):
            if not dados.get("motivo_negativa_ja_perguntado"):
                st.session_state.estado = "PS_MOTIVO_NEGATIVA_GERAL"
                add_bot(PS_MOTIVO_NEGATIVA_GERAL)
                return
            # Se o motivo já foi perguntado antes no fluxo, não repete.
            while idx < len(st.session_state.perguntas_ativas) and "qual foi o motivo da negativa" in _n(st.session_state.perguntas_ativas[idx]):
                idx += 1
            st.session_state.pergunta_idx = idx

        if idx < len(st.session_state.perguntas_ativas):
            proxima_pergunta = st.session_state.perguntas_ativas[idx]
            # Coparticipação: a mensagem explicativa deve vir seguida imediatamente
            # da pergunta sobre contrato, sem aguardar resposta entre as duas.
            if "copart" in _n(dados.get("situacao", "")) and proxima_pergunta == PS_COPA_Q6:
                add_bot(PS_COPA_Q6)
                add_bot(PS_COPA_Q7)
                st.session_state.pergunta_idx = idx + 1
                return
            add_bot(proxima_pergunta)
        else:
            # Fluxo específico de Reajuste: após responder sobre contrato do plano,
            # segue para escolha entre judicialização ou consultoria.
            if "reajuste" in _n(dados.get("situacao", "")):
                add_bot(PS_REAJ_INTRO_ABUSIVO)
                add_bot(PS_REAJ_ANALISE)
                st.session_state.estado = "PS_REAJ_ESCOLHA"
                add_bot(PS_REAJ_ESCOLHA)
                return

            # Fluxo específico de Coparticipação: após responder sobre contrato do plano,
            # pergunta valores e segue para escolha entre judicialização ou consultoria.
            if "copart" in _n(dados.get("situacao", "")):
                st.session_state.estado = "PS_COPA_VALOR_AUMENTO"
                add_bot(PS_COPA_VALOR_AUMENTO)
                return

            # Fluxo específico de Erro Médico: após responder sobre falha/descaso/técnica,
            # segue para escolha entre judicialização ou análise técnica.
            if "erro" in _n(dados.get("situacao", "")):
                st.session_state.estado = "PS_ERRO_INTRO_AGUARDANDO"
                add_bot(PS_ERRO_INTRO_DOR)
                return

            # Enviar mensagem "ponto crítico" usando nome da especialidade
            situacao_raw = dados.get("situacao", "")
            situacao_n = _n(situacao_raw)
            ponto = dados.get("neg_cir_esp", situacao_raw) or situacao_raw
            nome_ponto = get_nome_especialidade(ponto) if ponto in [str(i) for i in range(1,9)] else ponto
            if not st.session_state.get("ponto_critico_enviado", False):
                add_bot(PS_PONTO_CRITICO.format(ponto=nome_ponto))
                st.session_state.ponto_critico_enviado = True
            # IMPORTANTE: após essa mensagem, o robô deve aguardar a resposta do cliente
            # antes de seguir para negativa de material ou para o pós-busca.
            st.session_state.estado = "PS_PONTO_CRITICO_AGUARDANDO"

    # ---- REAJUSTE: NOVO FLUXO APÓS CONTRATO ----
    elif estado == "PS_REAJ_ESCOLHA":
        n = _n(resposta)
        opcao = _opcao_numero(resposta)
        if opcao == "1" or "judicial" in n or "judicializar" in n or "aumento" in n or "abusivo" in n:
            add_bot(PS_REAJ_JUDICIALIZAR_1)
            add_bot(PS_REAJ_JUDICIALIZAR_2)
            st.session_state.estado = "DECISAO_COMPARTILHADA"
            add_bot(MSG_SIM_HONORARIOS_SUS_DECISAO)
        elif opcao == "2" or "consultoria" in n or "preventiva" in n or "contrato" in n:
            st.session_state.estado = "PS_REAJ_CONSULTORIA"
            add_bot(PS_REAJ_CONSULTORIA)
        else:
            add_bot(PS_REAJ_ESCOLHA)

    elif estado == "PS_REAJ_CONSULTORIA":
        if _sim(resposta):
            st.session_state.estado = "PS_REAJ_PAGAMENTO"
            add_bot(PS_REAJ_PAGAMENTO)
        else:
            add_bot(PS_ENCERRAMENTO)
            st.session_state.estado = "FIM"

    elif estado == "PS_REAJ_PAGAMENTO":
        if "cartão" in _n(resposta) or "cartao" in _n(resposta):
            add_bot(f"✅ Aqui está o link para pagamento via Cartão de Crédito:\n\n{LINK_CARTAO_500}\n\n{PS_REAJ_CONFIRMACAO}")
            st.session_state.estado = "FIM"
        elif "pix" in _n(resposta):
            add_bot(f"✅ Aqui está o link para pagamento via Pix:\n\n{LINK_PIX_500}\n\n{PS_REAJ_CONFIRMACAO}")
            st.session_state.estado = "FIM"

    # ---- COPARTICIPAÇÃO: NOVO FLUXO APÓS CONTRATO ----
    elif estado == "PS_COPA_VALOR_AUMENTO":
        dados["copa_valor_aumento"] = resposta
        add_bot(PS_COPA_OBSTACULOS)
        add_bot(PS_COPA_ANALISE)
        st.session_state.estado = "PS_COPA_ESCOLHA"
        add_bot(PS_COPA_ESCOLHA)

    elif estado == "PS_COPA_ESCOLHA":
        n = _n(resposta)
        opcao = _opcao_numero(resposta)
        if opcao == "1" or "judicial" in n or "judicializar" in n or "cobrança" in n or "cobranca" in n:
            add_bot(PS_COPA_JUDICIALIZAR_1)
            add_bot(PS_COPA_JUDICIALIZAR_2)
            st.session_state.estado = "DECISAO_COMPARTILHADA"
            add_bot(MSG_SIM_HONORARIOS_SUS_DECISAO)
        elif opcao == "2" or "consultoria" in n or "contrato" in n:
            st.session_state.estado = "PS_OP3_CONSULTORIA"
            add_bot(PS_OP3_CONSULTORIA)
        else:
            add_bot(PS_COPA_ESCOLHA)

    # ---- ERRO MÉDICO: NOVO FLUXO APÓS PERGUNTA FINAL ----
    elif estado == "PS_ERRO_INTRO_AGUARDANDO":
        dados["erro_intro_resposta"] = resposta
        if not dados.get("prova_social_erro_a14_enviada"):
            dados["prova_social_erro_a14_enviada"] = True
            add_bot(PS_PROVA_SOCIAL_ERRO_A14)
        add_bot(PS_ERRO_ANALISE)
        st.session_state.estado = "PS_ERRO_ESCOLHA"
        add_bot(PS_ERRO_ESCOLHA)

    elif estado == "PS_ERRO_ESCOLHA":
        n = _n(resposta)
        opcao = _opcao_numero(resposta)
        if opcao == "1" or "judicial" in n or "judicializar" in n or "processar" in n or "indenização" in n or "indenizacao" in n:
            add_bot(PS_ERRO_JUDICIALIZAR_1)
            add_bot(PS_ERRO_JUDICIALIZAR_2)
            st.session_state.estado = "DECISAO_COMPARTILHADA"
            add_bot(MSG_SIM_HONORARIOS_SUS_DECISAO)
        elif opcao == "2" or "análise" in n or "analise" in n or "técnica" in n or "tecnica" in n or "consultoria" in n:
            st.session_state.estado = "PS_ERRO_CONSULTORIA"
            add_bot(PS_ERRO_CONSULTORIA)
        else:
            add_bot(PS_ERRO_ESCOLHA)

    elif estado == "PS_ERRO_CONSULTORIA":
        if _sim(resposta):
            st.session_state.estado = "PS_ERRO_PAGAMENTO"
            add_bot(PS_ERRO_PAGAMENTO)
        else:
            add_bot(PS_ENCERRAMENTO)
            st.session_state.estado = "FIM"

    elif estado == "PS_ERRO_PAGAMENTO":
        if "cartão" in _n(resposta) or "cartao" in _n(resposta):
            add_bot(f"✅ Aqui está o link para pagamento via Cartão de Crédito:\n\n{LINK_CARTAO_500}\n\n{PS_ERRO_CONFIRMACAO}")
            st.session_state.estado = "FIM"
        elif "pix" in _n(resposta):
            add_bot(f"✅ Aqui está o link para pagamento via Pix:\n\n{LINK_PIX_500}\n\n{PS_ERRO_CONFIRMACAO}")
            st.session_state.estado = "FIM"

    # ---- MOTIVO DA NEGATIVA APÓS ESCRITA/VERBAL ----
    elif estado == "PS_MOTIVO_NEGATIVA_GERAL":
        dados["motivo_negativa"] = resposta
        dados["motivo_negativa_ja_perguntado"] = True
        idx = st.session_state.pergunta_idx

        # Evita repetir a pergunta de motivo caso ela já exista como próxima pergunta no fluxo.
        while idx < len(st.session_state.perguntas_ativas) and "qual foi o motivo da negativa" in _n(st.session_state.perguntas_ativas[idx]):
            idx += 1
        st.session_state.pergunta_idx = idx

        if idx < len(st.session_state.perguntas_ativas):
            st.session_state.estado = "PS_PERGUNTAS_COLETOR"
            add_bot(st.session_state.perguntas_ativas[idx])
        else:
            situacao_raw = dados.get("situacao", "")
            situacao_n = _n(situacao_raw)
            ponto = dados.get("neg_cir_esp", situacao_raw) or situacao_raw
            nome_ponto = get_nome_especialidade(ponto) if ponto in [str(i) for i in range(1,9)] else ponto
            if not st.session_state.get("ponto_critico_enviado", False):
                add_bot(PS_PONTO_CRITICO.format(ponto=nome_ponto))
                st.session_state.ponto_critico_enviado = True
            st.session_state.estado = "PS_PONTO_CRITICO_AGUARDANDO"

    # ---- REPARADORA (ATUALIZADA) ----
    elif estado == "PS_REP_Q1":
        dados["rep_q1"] = resposta
        st.session_state.estado = "PS_REP_Q2"
        add_bot(PS_REP_Q2)
    elif estado == "PS_REP_Q2":
        dados["rep_q2"] = resposta
        resp_norm = _n(resposta)

        # Se a pessoa já chegou à meta, NÃO pergunta quantos kg faltam.
        # Segue diretamente para "Quantos kg você perdeu no processo de emagrecimento?"
        if (
            resposta == "1"
            or "já cheguei" in resp_norm
            or "ja cheguei" in resp_norm
            or "cheguei" in resp_norm
            or "minha meta" in resp_norm
        ):
            st.session_state.estado = "PS_REP_KG_PERDIDOS"
            add_bot(PS_REP_KG_PERDIDOS)
            return

        # Só pergunta quantos kg faltam se a pessoa clicar/responder "Ainda não".
        if (
            resposta == "2"
            or "ainda não" in resp_norm
            or "ainda nao" in resp_norm
            or "não cheguei" in resp_norm
            or "nao cheguei" in resp_norm
        ):
            st.session_state.estado = "PS_REP_FALTAM_META"
            add_bot(PS_REP_FALTAM_META)
            return

        # Segurança: se a resposta não for reconhecida, reapresenta as opções corretas.
        add_bot("Escolha uma das opções para eu te direcionar corretamente:\n\n1️⃣ Já cheguei à minha meta\n2️⃣ Ainda não")
        st.session_state.estado = "PS_REP_Q2"
        return
    elif estado == "PS_REP_FALTAM_META":
        dados["rep_faltam_meta"] = resposta
        faltam = _extrair_primeiro_numero(resposta)
        if faltam is None:
            add_bot("Me informe apenas um número aproximado de quantos quilos ainda faltam para chegar à sua meta, por favor.")
            st.session_state.estado = "PS_REP_FALTAM_META"
            return
        if faltam <= 6:
            # Segue como se a pessoa já estivesse na meta ou muito próxima dela.
            st.session_state.estado = "PS_REP_KG_PERDIDOS"
            add_bot(PS_REP_KG_PERDIDOS)
        else:
            # Novo fluxo para quem ainda precisa perder mais de 6kg.
            st.session_state.estado = "PS_REP_MAIS6_KG_PERDIDOS"
            add_bot(PS_REP_MAIS6_PARABENS)
    elif estado == "PS_REP_KG_PERDIDOS":
        dados["rep_kg_perdidos"] = resposta
        _perguntar_escala_urgencia("PS_REP_EMPATIA", PS_REP_EMPATIA, "PS_REP_EMPATIA", "plano_reparadora")
        return
    elif estado == "PS_REP_FALTAM_KG":
        # Compatibilidade com conversas iniciadas em versões anteriores.
        dados["rep_faltam_kg"] = resposta
        st.session_state.estado = "PS_REP_FALTAM_META"
        add_bot(PS_REP_FALTAM_META)
    elif estado == "PS_REP_MAIS6_KG_PERDIDOS":
        dados["rep_mais6_kg_perdidos"] = resposta
        st.session_state.estado = "PS_REP_MAIS6_SABIA"
        add_bot(PS_REP_MAIS6_MITO)
    elif estado == "PS_REP_MAIS6_SABIA":
        dados["rep_mais6_sabia"] = resposta
        st.session_state.estado = "PS_REP_MAIS6_GUIA_PERGUNTA"
        add_bot(PS_REP_MAIS6_GUIA_PERGUNTA)
    elif estado == "PS_REP_MAIS6_GUIA_PERGUNTA":
        dados["rep_mais6_guia"] = resposta
        add_bot(PS_REP_MAIS6_GUIA_LINK)
        st.session_state.estado = "PS_REP_MAIS6_DECISAO"
        add_bot(PS_REP_MAIS6_DECISAO)
    elif estado == "PS_REP_MAIS6_DECISAO":
        n = _n(resposta)
        if "análise" in n or "analise" in n or "individual" in n:
            st.session_state.estado = "PS_REP_MAIS6_ATENDIMENTO_AJUDA"
            add_bot(PS_REP_MAIS6_ATENDIMENTO)
        else:
            add_bot(PS_REP_MAIS6_ENCERRAMENTO)
            st.session_state.estado = "FIM"
    elif estado == "PS_REP_MAIS6_ATENDIMENTO_AJUDA":
        if _sim(resposta):
            st.session_state.estado = "PS_REP_MAIS6_MARCAR"
            add_bot(PS_REP_MAIS6_INVESTIMENTO)
        else:
            add_bot(PS_REP_MAIS6_ENCERRAMENTO)
            st.session_state.estado = "FIM"
    elif estado == "PS_REP_MAIS6_MARCAR":
        if _sim(resposta):
            st.session_state.estado = "PS_REP_MAIS6_PAGAMENTO"
            add_bot("Perfeito! Vamos reservar o seu horário.\n\nComo deseja realizar o investimento do atendimento? Você prefere Pix ou Cartão de Crédito?")
        else:
            add_bot(PS_REP_MAIS6_ENCERRAMENTO)
            st.session_state.estado = "FIM"
    elif estado == "PS_REP_MAIS6_PAGAMENTO":
        n = _n(resposta)
        if "cartão" in n or "cartao" in n or "crédito" in n or "credito" in n:
            add_bot(f"✅ Aqui está o link para pagamento via Cartão de Crédito:\n\n{LINK_CARTAO_97}")
        elif "pix" in n:
            add_bot(f"✅ Aqui está o link para pagamento via Pix:\n\n{LINK_PIX_97}")
        else:
            add_bot("Como deseja realizar o investimento do atendimento? Você prefere Pix ou Cartão de Crédito?")
            st.session_state.estado = "PS_REP_MAIS6_PAGAMENTO"
            return
        add_bot(f"Para facilitar, você mesma pode escolher o melhor dia e horário para a sua reunião através do link abaixo.\n{PS_REP_MAIS6_CALENDLY}")
        add_bot("Atenção: Como a agenda da Dra. Lethicia é muito concorrida, o seu horário só será confirmado e garantido após a identificação do pagamento pelo nosso setor financeiro.\nAssim que o pagamento for processado, nossa equipe entrará em contato imediatamente para validar o seu atendimento.")
        add_bot("Ao realizar o pagamento e for dado baixa no nosso financeiro, alguém da nossa equipe vai entrar em contato o quanto antes para confirmar seu atendimento na agenda da Dra. Lethicia. 🌹")
        st.session_state.estado = "FIM"
    elif estado == "PS_CONSULTA_97_DECISAO":
        n = _n(resposta)
        if "tirar" in n or "dúvida" in n or "duvida" in n or _sim(resposta):
            st.session_state.estado = "PS_CONSULTA_97_PAGAMENTO"
            add_bot(PS_CONSULTA_PAGA_97)
        else:
            add_bot(PS_ENCERRAMENTO)
            st.session_state.estado = "FIM"

    elif estado == "PS_CONSULTA_97_PAGAMENTO":
        n = _n(resposta)
        if "cartão" in n or "cartao" in n or "crédito" in n or "credito" in n:
            add_bot(f"✅ Aqui está o link para pagamento via Cartão de Crédito:\n\n{LINK_CARTAO_97}\n\nAo realizar o pagamento e for dado baixa no nosso financeiro, alguém da nossa equipe vai entrar em contato o quanto antes pra marcar seu atendimento na agenda da Dra Lethicia.")
            st.session_state.estado = "FIM"
        elif "pix" in n:
            add_bot(f"✅ Aqui está o link para pagamento via Pix:\n\n{LINK_PIX_97}\n\nAo realizar o pagamento e for dado baixa no nosso financeiro, alguém da nossa equipe vai entrar em contato o quanto antes pra marcar seu atendimento na agenda da Dra Lethicia.")
            st.session_state.estado = "FIM"
        else:
            add_bot(PS_CONSULTA_PAGA_97)

    elif estado == "PS_REP_NAO_PESO":
        # Compatibilidade com conversas já iniciadas nesse estado em versões anteriores.
        iniciar_fluxo_reparadora_97()
    elif estado == "PS_REP_EMPATIA":
        dados["rep_q3"] = resposta
        add_bot(PS_REP_OBRIGADA)
        add_bot(PS_REP_PROVA_SOCIAL_A1)
        st.session_state.estado = "PS_REP_Q4"
        add_bot(PS_REP_Q4)
    elif estado == "PS_REP_Q4":
        dados["rep_q4"] = resposta
        add_bot(PS_REP_CURIOSIDADE)
        st.session_state.estado = "PS_REP_Q5"
        add_bot(PS_REP_Q5)
    elif estado == "PS_REP_Q5":
        dados["rep_q5"] = resposta
        st.session_state.estado = "PS_REP_ACOMPANHAMENTO"
        add_bot(PS_REP_ACOMPANHAMENTO)
    elif estado == "PS_REP_ACOMPANHAMENTO":
        if "acompanhamento" in _n(resposta) or "quer" in _n(resposta) or "dra" in _n(resposta):
            add_bot(MSG_ACOMPANHAMENTO_JURIDICO)
            add_bot(MSG_PRE_POS_BUSCA_2)
            st.session_state.estado = "PS_POS_BUSCA"
            add_bot(PS_POS_BUSCA)
        elif "como funciona" in _n(resposta):
            add_bot(MSG_ACOMPANHAMENTO_JURIDICO)
            add_bot(MSG_PRE_POS_BUSCA_2)
            st.session_state.estado = "PS_POS_BUSCA"
            add_bot(PS_POS_BUSCA)
        else:
            add_bot(PS_ENCERRAMENTO)
            st.session_state.estado = "FIM"

    # ---- NEGATIVA DE CIRURGIA ----
    elif estado == "PS_NEG_CIR_ESP":
        dados["neg_cir_esp"] = resposta

        if "endometriose" in _n(resposta) or "1" in resposta:
            st.session_state.perguntas_ativas = [PS_ENDO_Q1, PS_ENDO_Q2, PS_ENDO_Q3, PS_ENDO_Q4, PS_ENDO_Q5]
        elif "bariátrica" in _n(resposta) or "bariatrica" in _n(resposta) or "2" in resposta:
            # Bariátrica: a mensagem explicativa vem imediatamente seguida da escala de urgência,
            # sem aguardar resposta nela. Depois da escala, o fluxo pergunta sobre acompanhamento multidisciplinar.
            st.session_state.perguntas_ativas = [
                PS_BARI_Q1, PS_BARI_Q2, PS_BARI_Q3_PERGUNTA,
                PS_BARI_Q4, PS_BARI_Q5, PS_BARI_Q6
            ]
        elif "oncologia" in _n(resposta) or "3" in resposta:
            st.session_state.perguntas_ativas = [PS_ONCO_Q1, PS_ONCO_Q2, PS_ONCO_Q3, PS_ONCO_Q4, PS_ONCO_Q5, PS_ONCO_Q6]
        elif "cardiologia" in _n(resposta) or "4" in resposta:
            st.session_state.perguntas_ativas = [PS_CARDIO_Q1, PS_CARDIO_Q3, PS_CARDIO_Q4, PS_CARDIO_Q5, PS_CARDIO_Q6]
        elif "neurocirurgia" in _n(resposta) or "5" in resposta:
            # Neurocirurgia sem a pergunta do material
            st.session_state.perguntas_ativas = [PS_NEURO_Q1, PS_NEURO_Q2, PS_NEURO_Q3, PS_NEURO_Q4, PS_NEURO_Q5, PS_NEURO_Q7]
        elif "ortopedia" in _n(resposta) or "6" in resposta:
            st.session_state.perguntas_ativas = [PS_ORTO_Q1, PS_ORTO_Q2, PS_ORTO_Q3, PS_ORTO_Q5, PS_ORTO_Q6]
        elif "oftalmologia" in _n(resposta) or "7" in resposta:
            st.session_state.perguntas_ativas = [PS_OFTAL_Q1, PS_OFTAL_Q2, PS_OFTAL_Q3, PS_OFTAL_Q4, PS_OFTAL_Q5]
        else:
            st.session_state.perguntas_ativas = [
                PS_OUTRO_INTRO, PS_OUTRO_Q1, PS_OUTRO_Q2, PS_OUTRO_Q3, PS_OUTRO_Q4,
                PS_OUTRO_Q5, PS_OUTRO_Q6, PS_OUTRO_Q7, PS_OUTRO_Q8, PS_OUTRO_Q9
            ]

        st.session_state.pergunta_idx = 0
        st.session_state.estado = "PS_PERGUNTAS_COLETOR"
        add_bot(st.session_state.perguntas_ativas[0])

    # ---- AGUARDA RESPOSTA APÓS PONTO CRÍTICO ----
    elif estado == "PS_PONTO_CRITICO_AGUARDANDO":
        dados["ponto_critico_resposta"] = resposta
        esp_n = _n(dados.get("neg_cir_esp", ""))
        if not dados.get("prova_social_neg_cir_enviada"):
            if "bari" in esp_n or str(dados.get("neg_cir_esp", "")).strip() == "2":
                add_bot(PS_PROVA_SOCIAL_BARI_A3)
                dados["prova_social_neg_cir_enviada"] = True
            elif "endometriose" in esp_n or "adenomiose" in esp_n or str(dados.get("neg_cir_esp", "")).strip() == "1":
                add_bot(PS_PROVA_SOCIAL_ENDO_A2)
                dados["prova_social_neg_cir_enviada"] = True
            elif "onco" in esp_n or "câncer" in esp_n or "cancer" in esp_n or str(dados.get("neg_cir_esp", "")).strip() == "3":
                add_bot(PS_PROVA_SOCIAL_ONCO_A4)
                dados["prova_social_neg_cir_enviada"] = True
            elif "cardio" in esp_n or "coração" in esp_n or "coracao" in esp_n or str(dados.get("neg_cir_esp", "")).strip() == "4":
                add_bot(PS_PROVA_SOCIAL_CARDIO_A5)
                dados["prova_social_neg_cir_enviada"] = True
            elif "neuro" in esp_n or "neurologia" in esp_n or "neurocirurgia" in esp_n or str(dados.get("neg_cir_esp", "")).strip() == "5":
                add_bot(PS_PROVA_SOCIAL_NEURO_A6)
                dados["prova_social_neg_cir_enviada"] = True
            elif "orto" in esp_n or "ortopedia" in esp_n or str(dados.get("neg_cir_esp", "")).strip() == "6":
                add_bot(PS_PROVA_SOCIAL_ORTO_A7)
                dados["prova_social_neg_cir_enviada"] = True
            elif "oftal" in esp_n or "oftalmologia" in esp_n or str(dados.get("neg_cir_esp", "")).strip() == "7":
                add_bot(PS_PROVA_SOCIAL_OFTAL_A8)
                dados["prova_social_neg_cir_enviada"] = True
        situacao_raw = dados.get("situacao", "")
        situacao_n = _n(situacao_raw)
        # Para negativa de cirurgia, só agora pergunta sobre material/protese.
        if "negativa" in situacao_n or "1" == str(situacao_raw).strip() or "2" == str(situacao_raw).strip():
            st.session_state.estado = "PS_NEG_MATERIAL"
            add_bot(MSG_NEG_MATERIAL)
        else:
            if not dados.get("prova_social_plano_geral_enviada"):
                dados["prova_social_plano_geral_enviada"] = True
                situacao_atual = _n(dados.get("situacao", ""))
                tipo_terapia = _n(dados.get("resp_0", "") + " " + dados.get("resp_1", ""))
                if "medicamento" in situacao_atual:
                    add_bot(PS_PROVA_SOCIAL_MEDICAMENTO_A9)
                elif "home" in situacao_atual:
                    add_bot(PS_PROVA_SOCIAL_HOMECARE_A10)
                elif "terapia" in situacao_atual:
                    if "reabilitação" in tipo_terapia or "reabilitacao" in tipo_terapia or "fisioterapia" in tipo_terapia or "físic" in tipo_terapia or "fisic" in tipo_terapia:
                        add_bot(PS_PROVA_SOCIAL_REABILITACAO_A15_A26)
                    else:
                        add_bot(PS_PROVA_SOCIAL_TEA_A11)
            add_bot(MSG_PRE_POS_BUSCA_1)
            add_bot(MSG_PRE_POS_BUSCA_2)
            st.session_state.estado = "PS_POS_BUSCA"
            add_bot(PS_POS_BUSCA)

    # ---- NEGATIVA DE MATERIAL ----
    elif estado == "PS_NEG_MATERIAL":
        dados["neg_material"] = resposta
        add_bot(MSG_PRE_POS_BUSCA_1)
        add_bot(MSG_PRE_POS_BUSCA_2)
        st.session_state.estado = "PS_POS_BUSCA"
        add_bot(PS_POS_BUSCA)

    # ---- POS BUSCA (opções 1-3) ----
    elif estado == "PS_POS_BUSCA":
        if "1" in resposta:
            add_bot(PS_OP1_PERGUNTA)
            add_bot(PS_OP1_REUNIAO)
            st.session_state.estado = "DECISAO_COMPARTILHADA"
            add_bot(MSG_SIM_HONORARIOS_SUS_DECISAO)
        elif "2" in resposta:
            add_bot(PS_OP2_INTRO)
            add_bot(PS_OP2_CAMINHO_1)
            add_bot(PS_OP2_CAMINHO_2)
            st.session_state.estado = "PS_OP2_DECISAO"
            add_bot(PS_OP2_DECISAO)
        elif "3" in resposta:
            st.session_state.estado = "PS_OP3_CONSULTORIA"
            add_bot(PS_OP3_CONSULTORIA)
        else:
            add_bot(PS_POS_BUSCA)

    elif estado == "PS_OP2_DECISAO":
        if _sim(resposta):
            st.session_state.estado = "DECISAO_COMPARTILHADA"
            add_bot(MSG_SIM_HONORARIOS_SUS_DECISAO)
        else:
            add_bot(PS_ENCERRAMENTO)
            st.session_state.estado = "FIM"

    elif estado == "PS_OP3_CONSULTORIA":
        if _sim(resposta):
            st.session_state.estado = "PS_OP3_PAGAMENTO"
            add_bot(PS_OP3_PAGAMENTO)
        else:
            add_bot("Entendo perfeitamente. Cada decisão tem o seu tempo certo. Vou encerrar seu atendimento por aqui, mas saiba que nossos canais continuam abertos. Caso você mude de ideia ou sinta que o momento de agir chegou, é só me chamar.")
            st.session_state.estado = "FIM"

    elif estado == "PS_OP3_PAGAMENTO":
        if "cartão" in _n(resposta) or "cartao" in _n(resposta):
            add_bot(f"✅ Aqui está o link para pagamento via Cartão de Crédito:\n\n{LINK_CARTAO_500}\n\n{PS_OP3_CONFIRMACAO}")
            st.session_state.estado = "FIM"
        elif "pix" in _n(resposta):
            add_bot(f"✅ Aqui está o link para pagamento via Pix:\n\n{LINK_PIX_500}\n\n{PS_OP3_CONFIRMACAO}")
            st.session_state.estado = "FIM"

    # ---- DECISÃO COMPARTILHADA ----
    elif estado == "DECISAO_COMPARTILHADA":
        n = _n(resposta)
        if "sozinho" in n or "sozinha" in n or "não" in n or "nao" in n:
            add_bot(DECISAO_NAO)
        elif "repasse" in n or "passo" in n or "falar" in n or "3" in resposta:
            add_bot(DECISAO_REPASSE)
            st.session_state.estado = "DECISAO_REPASSE_RESPOSTA"
            return
        else:
            add_bot(DECISAO_SIM)
        # Schedule timed messages
        st.session_state.followup_time = time.time() + 600  # 10 min
        st.session_state.finalizacao_time = st.session_state.followup_time + 300  # +5 min
        st.session_state.estado = "AGUARDANDO_TIMED"

    elif estado == "DECISAO_REPASSE_RESPOSTA":
        if _sim(resposta) or "com ele" in _n(resposta):
            add_bot(DECISAO_REPASSE_SIM)
        else:
            add_bot(DECISAO_REPASSE_NAO)
        st.session_state.followup_time = time.time() + 600
        st.session_state.finalizacao_time = st.session_state.followup_time + 300
        st.session_state.estado = "AGUARDANDO_TIMED"

    elif estado == "FIM":
        pass


# ====
# INTERFACE STREAMLIT
# ====


def _render_content_with_images(content: str, role: str = "bot"):
    """Renderiza mensagens com suporte seguro a imagens.

    As imagens podem vir como marcadores [[IMG:URL]] ou como tags antigas <img src="URL">.
    O texto é exibido separado da imagem e a imagem é renderizada com st.image(),
    evitando erro de HTML/aspas no Streamlit.
    """
    content = str(content or "")

    # Captura imagens no formato novo: [[IMG:https://...]]
    marker_pattern = re.compile(r'\[\[IMG:([^\]]+)\]\]', re.IGNORECASE)
    marker_urls = marker_pattern.findall(content)
    content = marker_pattern.sub("", content)

    # Captura imagens que ainda estejam no formato antigo HTML.
    html_pattern = re.compile(r'<br>\s*<img\s+src=["\']([^"\']+)["\'][^>]*>', re.IGNORECASE)
    html_urls = html_pattern.findall(content)
    content = html_pattern.sub("", content)

    urls = marker_urls + html_urls
    text_only = content.strip()

    if role == "bot":
        if text_only:
            st.markdown(
                f'<div class="chat-message bot-message"><strong>🌹 Aurora:</strong><br>{text_only}</div>',
                unsafe_allow_html=True,
            )
        for url in urls:
            url = str(url).strip()
            if not url:
                continue
            try:
                st.image(url, use_container_width=True)
            except TypeError:
                # Compatibilidade com versões antigas do Streamlit.
                st.image(url)
            except Exception:
                # Fallback clicável caso o ambiente bloqueie a imagem externa.
                st.markdown(f'<a href="{url}" target="_blank">Abrir imagem</a>', unsafe_allow_html=True)
    else:
        nome = st.session_state.nome or "Você"
        st.markdown(
            f'<div class="chat-message user-message"><strong>👤 {nome}:</strong><br>{content}</div>',
            unsafe_allow_html=True,
        )


def render_chat_content(content: str):
    """Renderiza mensagens com texto, links clicáveis e imagens reais no Streamlit."""
    if not content:
        return

    parts = re.split(r"(\[\[IMAGE:https?://[^\]]+\]\])", content)
    for part in parts:
        if not part:
            continue
        if part.startswith("[[IMAGE:") and part.endswith("]]"):
            url = part[len("[[IMAGE:"):-2].strip()
            st.image(url, use_container_width=True)
        else:
            st.markdown(tornar_links_clicaveis(part), unsafe_allow_html=True)

def main():
    st.title("🌹 Aurora Bot - Assistente Jurídica em Direito da Saúde")
    st.caption(f"Especialista: {L} | Atendimento: SUS, Planos de Saúde")

    init_session()

    # ---- CHECK TIMED MESSAGES ----
    now = time.time()
    rerun_timed = False
    
    # Check timeout de 5 min sem resposta
    if check_no_response_timeout():
        rerun_timed = True
    
    # Check mensagens de 24h
    if check_24h_messages():
        rerun_timed = True
    
    # Check link do Meet (5 min antes)
    if check_meet_link():
        rerun_timed = True
    
    # Followup e finalização
    if st.session_state.followup_time and not st.session_state.followup_sent:
        if now >= st.session_state.followup_time:
            st.session_state.messages.append({"role": "bot", "content": tornar_links_clicaveis(MSG_FOLLOWUP_LINK)})
            st.session_state.followup_sent = True
            rerun_timed = True
    if st.session_state.finalizacao_time and not st.session_state.finalizacao_sent:
        if now >= st.session_state.finalizacao_time:
            st.session_state.messages.append({"role": "bot", "content": tornar_links_clicaveis(MSG_AGENDAMENTO_FINALIZADO)})
            st.session_state.finalizacao_sent = True
            st.session_state.estado = "FIM"
            rerun_timed = True
    
    if rerun_timed:
        st.rerun()

    # Mantém a página “acordada” para enviar automaticamente o lembrete de 5 minutos,
    # mesmo se o cliente não clicar em nada nem enviar nova mensagem.
    schedule_no_response_autorefresh()

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

    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        _render_content_with_images(msg.get("content", ""), msg.get("role", "bot"))
    st.markdown('</div>', unsafe_allow_html=True)

    # ---- BOTÕES CONTEXTUAIS (abaixo do chat) ----
    estado = st.session_state.estado

    def btn(label, valor=None):
        v = valor or label
        if st.button(label, use_container_width=False, key=f"btn_{label}_{v}"):
            enviar_resposta_usuario(v, exibicao=label)
            st.rerun()

    def render_opcoes_numeradas(texto):
        """
        Cria botões automaticamente para perguntas que já trazem alternativas no texto
        (ex.: 1️⃣ Sim / 2️⃣ Não / 3️⃣ Não sei).
        Mantém perguntas abertas sem botões quando não houver alternativas numeradas.
        """
        texto = str(texto)
        # Captura opções com emoji numérico, inclusive quando estão na mesma linha.
        matches = list(re.finditer(r"([0-9]|10)️⃣\s*", texto))
        opcoes = []
        for i, m in enumerate(matches):
            inicio = m.end()
            fim = matches[i + 1].start() if i + 1 < len(matches) else len(texto)
            rotulo = texto[inicio:fim].strip()
            rotulo = re.sub(r"\s+", " ", rotulo).strip(" -–:.;")
            if rotulo:
                numero = m.group(1)
                opcoes.append((f"{numero}️⃣ {rotulo}", rotulo))

        if not opcoes:
            return False

        # Evita botões enormes quando a pergunta é explicativa e não uma escolha real.
        opcoes = [(label[:120], valor[:120]) for label, valor in opcoes]
        cols = st.columns(min(3, max(1, len(opcoes))))
        for i, (label, valor) in enumerate(opcoes):
            with cols[i % len(cols)]:
                btn(label, valor)
        return True

    def render_multiselect_terapias():
        """Permite selecionar mais de uma terapia indicada pelo médico."""
        opcoes_terapias = [
            "ABA",
            "Fisioterapia",
            "Psicologia",
            "Fonoaudiologia",
            "Terapia ocupacional",
            "Psicopedagogia",
            "Musicoterapia",
            "Hidroterapia",
            "OUTROS",
        ]
        selecionadas = st.multiselect(
            "Selecione todas as terapias indicadas pelo médico:",
            opcoes_terapias,
            key="multiselect_terapias_indicadas",
        )
        if st.button("✅ Confirmar terapias", use_container_width=False, key="btn_confirmar_terapias_multiplas"):
            if not selecionadas:
                st.warning("Selecione pelo menos uma terapia para continuar.")
            else:
                resposta_multiplas = ", ".join(selecionadas)
                enviar_resposta_usuario(resposta_multiplas)
                st.rerun()
        return True

    def show_buttons():
        if estado == "CANAL":
            c1, c2 = st.columns(2)
            with c1: btn("🏥 SUS", "SUS")
            with c2: btn("📋 Plano de Saúde", "Plano de Saúde")

        elif estado == "ESCALA_URGENCIA":
            cols = st.columns(5)
            for i in range(1, 6):
                with cols[i-1]:
                    btn(str(i), str(i))

        elif estado == "SUS_DEMANDA":
            c1, c2 = st.columns(2)
            with c1: btn("🔪 Cirurgia / Tratamento", "Cirurgia")
            with c2: btn("📋 Consultas / Exames", "Consultas")

        elif estado == "SUS_CONSULTA_EXAME_TIPO":
            c1, c2 = st.columns(2)
            with c1: btn("1️⃣ Consulta com especialista", "1")
            with c2: btn("2️⃣ Realização de Exame", "2")

        elif estado == "SUS_CONSULTA_PITCH":
            c1, c2 = st.columns(2)
            with c1: btn("⏳ Quero aguardar", "aguardar")
            with c2: btn("💙 Quero ajuda da Dra. Lethicia", "quero ajuda")

        elif estado in ("SUS_CONSULTA_AJUDA_Q3", "SUS_CONSULTA_AJUDA_Q4B", "SUS_CONSULTA_Q3"):
            c1, c2 = st.columns(2)
            with c1: btn("✅ Sim", "Sim")
            with c2: btn("❌ Não", "Não")

        elif estado == "SUS_CONSULTA_AJUDA_Q4":
            c1, c2, c3 = st.columns(3)
            with c1: btn("📱 Tenho Meu SUS", "Tenho Meu SUS")
            with c2: btn("📄 Tenho Comprovante", "Tenho Comprovante")
            with c3: btn("📋 Tenho SISREG", "Tenho SISREG")

        elif estado in ("SUS_CONSULTA_PROTOCOLO", "SUS_EXAME_PROTOCOLO",
                    "SUS_CONSULTA_HONORARIOS", "SUS_EXAME_HONORARIOS",
                    "POS_PERGUNTAS_SUS", "PROPOSTA_SUS", "HONORARIOS_SUS"):
            c1, c2 = st.columns(2)
            with c1: btn("✅ SIM", "SIM")
            with c2: btn("❌ NÃO", "NÃO")

        elif estado == "SUS_EXAME_TIPO":
            c1, c2, c3 = st.columns(3)
            with c1: btn("1️⃣ Diagnóstico", "1")
            with c2: btn("2️⃣ Pré-operatório", "2")
            with c3: btn("3️⃣ Confirmação", "3")

        elif estado == "SUS_EXAME_PITCH":
            c1, c2 = st.columns(2)
            with c1: btn("⏳ Quero aguardar", "aguardar")
            with c2: btn("💙 Quero ajuda da Dra. Lethicia", "quero ajuda")

        elif estado == "SUS_ESPECIALIDADE":
            cols = st.columns(4)
            esps = ["Oncologia", "Neurodivergências (TEA, TDAH)", "Endometriose / Adenomiose",
                    "Medicamento", "Bariátrica", "Neurologia / Neurocirurgia", "Cardiologia", "Outros"]
            for i, esp in enumerate(esps):
                with cols[i % 4]: btn(esp)

        elif estado in ("SUS_ONCOLOGIA_BENIGNO_MALIGNO", "SUS_ONCOLOGIA_Q1"):
            c1, c2 = st.columns(2)
            with c1: btn("🔴 Maligno", "Maligno")
            with c2: btn("🟢 Benigno", "Benigno")

        elif estado == "SUS_DOCS_INSUF":
            c1, c2 = st.columns(2)
            with c1: btn("✅ Certo", "Certo")
            with c2: btn("👍 Vou fazer isso", "Vou fazer isso")

        elif estado == "SUS_PERGUNTAS":
            idx = st.session_state.pergunta_idx
            perguntas = st.session_state.perguntas_ativas
            if idx < len(perguntas):
                pergunta_atual = perguntas[idx]
                q = pergunta_atual.lower()
                if render_opcoes_numeradas(pergunta_atual):
                    pass
                elif any(kw in q for kw in ["tem relatório", "possui relatório", "tem o comprovante",
                    "possui o comprovante", "risco de piora", "agravamento",
                    "diagnóstico confirmado", "tem laudo", "possui laudo",
                    "tem a receita", "tem algum laudo", "urgente",
                    "já foi encaminhado", "já tem mais", "60 dias"]):
                    c1, c2 = st.columns(2)
                    with c1: btn("✅ Sim", "Sim")
                    with c2: btn("❌ Não", "Não")

        elif estado == "PS_TEMPO":
            c1, c2 = st.columns(2)
            with c1: btn("1️⃣ Sim", "Sim")
            with c2: btn("2️⃣ Não", "Não")
        
        elif estado == "PS_TEMPO_NAO_SEGUIMENTO":
            c1, c2 = st.columns(2)
            with c1: btn("🏢 Empresarial/CNPJ", "empresarial")
            with c2: btn("👤 Pessoa Física", "pessoa física")

        elif estado == "PS_SITUACAO":
            opcoes = [
                ("0️⃣ Reparadora", "0"), ("1️⃣ Negativa de cirurgia", "1"),
                ("2️⃣ Medicamento negado", "2"), ("3️⃣ Exame negado", "3"),
                ("4️⃣ Home care", "4"), ("5️⃣ Terapias", "5"),
                ("6️⃣ Reajuste", "6"), ("7️⃣ Coparticipação elevada", "7"),
                ("8️⃣ Erro médico", "8"), ("9️⃣ OUTRO", "9"),
            ]
            cols = st.columns(2)
            for i, (label, val) in enumerate(opcoes):
                with cols[i % 2]: btn(label, val)

        elif estado == "PS_REP_Q2":
            c1, c2 = st.columns(2)
            with c1: btn("1️⃣ Já cheguei à minha meta", "1")
            with c2: btn("2️⃣ Ainda não", "2")

        elif estado == "PS_REP_MAIS6_DECISAO":
            c1, c2 = st.columns(2)
            with c1: btn("⚖️ ANÁLISE INDIVIDUAL", "ANÁLISE INDIVIDUAL")
            with c2: btn("👤 SOZINHO(A)", "SOZINHO(A)")

        elif estado in ("PS_REP_MAIS6_ATENDIMENTO_AJUDA", "PS_REP_MAIS6_MARCAR"):
            c1, c2 = st.columns(2)
            with c1: btn("✅ SIM", "SIM")
            with c2: btn("❌ NÃO", "NÃO")

        elif estado == "PS_REP_MAIS6_PAGAMENTO":
            c1, c2 = st.columns(2)
            with c1: btn("💳 Cartão de Crédito", "cartão")
            with c2: btn("📱 Pix", "pix")

        elif estado == "PS_REP_Q5":
            c1, c2 = st.columns(2)
            with c1: btn("✅ SIM", "SIM")
            with c2: btn("❌ NÃO", "NÃO")

        elif estado == "PS_REP_ACOMPANHAMENTO":
            c1, c2, c3 = st.columns(3)
            with c1: btn("💙 Quero acompanhamento da Dra.", "quero acompanhamento")
            with c2: btn("❓ Como funciona", "como funciona")
            with c3: btn("👤 Não quero acompanhamento", "não quero")

        elif estado == "PS_NEG_CIR_ESP":
            opcoes = [
                ("1️⃣ Endometriose", "1"), ("2️⃣ Bariátrica", "2"),
                ("3️⃣ Oncologia (câncer)", "3"), ("4️⃣ Cardiologia", "4"),
                ("5️⃣ Neurocirurgia", "5"), ("6️⃣ Ortopedia", "6"),
                ("7️⃣ Oftalmologia", "7"), ("8️⃣ OUTRO", "8"),
            ]
            cols = st.columns(2)
            for i, (label, val) in enumerate(opcoes):
                with cols[i % 2]: btn(label, val)

        elif estado == "PS_NEG_MATERIAL":
            c1, c2, c3 = st.columns(3)
            with c1: btn("🔪 Cirurgia negada", "Cirurgia negada")
            with c2: btn("🔩 Material negado", "Material negado")
            with c3: btn("➖ Não se aplica", "Não se aplica")

        elif estado == "PS_CONSULTA_97_DECISAO":
            c1, c2 = st.columns(2)
            with c1: btn("⏳ Aguardar", "Aguardar")
            with c2: btn("💬 Tirar as dúvidas", "Tirar as dúvidas")

        elif estado == "PS_CONSULTA_97_PAGAMENTO":
            c1, c2 = st.columns(2)
            with c1: btn("💳 Cartão de Crédito", "cartão")
            with c2: btn("📱 Pix", "pix")

        elif estado == "PS_OP2_DECISAO":
            c1, c2 = st.columns(2)
            with c1: btn("👤 VOU FAZER SOZINHO", "NÃO")
            with c2: btn("⚖️ QUERO A ASSESSORIA", "SIM")

        elif estado == "PS_OP3_CONSULTORIA":
            c1, c2 = st.columns(2)
            with c1: btn("✅ Sim, quero agendar agora", "Sim, quero agendar agora")
            with c2: btn("❌ Não quero, mas obrigada", "Não quero")

        elif estado == "PS_OP3_PAGAMENTO":
            c1, c2 = st.columns(2)
            with c1: btn("💳 Cartão de Crédito", "cartão")
            with c2: btn("📱 Pix", "pix")

        elif estado == "PERGUNTA_RESULTADOS":
            c1, c2 = st.columns(2)
            with c1: btn("✅ SIM", "SIM")
            with c2: btn("❌ NÃO", "NÃO")

        elif estado == "PERGUNTA_VALOR_ANALISE":
            c1, c2 = st.columns(2)
            with c1: btn("✅ SIM", "SIM")
            with c2: btn("❌ NÃO", "NÃO")

        elif estado == "PS_POS_BUSCA":
            opcoes = [
                ("1️⃣ Já tenho a negativa do plano", "1"),
                ("2️⃣ Ainda não tenho a negativa, mas preciso me preparar", "2"),
                ("3️⃣ Preciso de uma consultoria jurídica", "3"),
            ]
            cols = st.columns(3)
            for i, (label, val) in enumerate(opcoes):
                with cols[i % 3]: btn(label, val)

        elif estado == "DECISAO_COMPARTILHADA":
            c1, c2, c3 = st.columns(3)
            with c1: btn("👨‍👩‍👧 Sim, meu cônjuge/familiar", "sim")
            with c2: btn("👤 Não, eu decido sozinho(a)", "sozinho")
            with c3: btn("📞 Tem, mas pode falar comigo", "repasse")

        elif estado == "DECISAO_REPASSE_RESPOSTA":
            c1, c2 = st.columns(2)
            with c1: btn("👥 Com ele(a)", "com ele")
            with c2: btn("👤 Entre nós", "não")

        elif estado == "PS_OUTRO_DEMANDA":
            idx = st.session_state.get("outro_idx", 0)
            # Q1 já foi enviada, agora verificamos as demais
            if idx == 0:
                # Aguardando resposta da Q1 (texto livre - sem botões)
                pass
            elif idx == 1:
                # Q2 - texto livre
                pass
            elif idx == 2:
                # Q3 - botões
                c1, c2, c3 = st.columns(3)
                with c1: btn("✅ Sim", "Sim")
                with c2: btn("❌ Não", "Não")
                with c3: btn("➖ Não se encaixa", "Não se encaixa")
            elif idx == 3:
                # Q4 - botões
                c1, c2, c3 = st.columns(3)
                with c1: btn("✅ Sim", "Sim")
                with c2: btn("❌ Não", "Não")
                with c3: btn("➖ Não se encaixa", "Não se encaixa")
            elif idx == 4:
                # Q5 - botões
                c1, c2 = st.columns(2)
                with c1: btn("✅ Sim", "Sim")
                with c2: btn("❌ Não", "Não")
            elif idx == 5:
                # Q6 - botões
                c1, c2 = st.columns(2)
                with c1: btn("✅ Sim", "Sim")
                with c2: btn("❌ Não", "Não")

        elif estado == "PS_REAJ_ESCOLHA":
            c1, c2 = st.columns(2)
            with c1: btn("⚖️ Quero judicializar", "1")
            with c2: btn("📄 Quero consultoria jurídica", "2")

        elif estado == "PS_REAJ_CONSULTORIA":
            c1, c2 = st.columns(2)
            with c1: btn("✅ Sim, quero agendar agora", "Sim, quero agendar agora")
            with c2: btn("❌ Não quero, mas obrigada", "Não quero")

        elif estado == "PS_REAJ_PAGAMENTO":
            c1, c2 = st.columns(2)
            with c1: btn("💳 Cartão de Crédito", "cartão")
            with c2: btn("📱 Pix", "pix")

        elif estado == "PS_COPA_ESCOLHA":
            c1, c2 = st.columns(2)
            with c1: btn("⚖️ Quero judicializar", "1")
            with c2: btn("📄 Quero consultoria jurídica", "2")

        elif estado == "PS_ERRO_ESCOLHA":
            c1, c2 = st.columns(2)
            with c1: btn("⚖️ Quero judicializar", "1")
            with c2: btn("📄 Quero análise técnica", "2")

        elif estado == "PS_ERRO_CONSULTORIA":
            c1, c2 = st.columns(2)
            with c1: btn("✅ Sim, quero agendar agora", "Sim, quero agendar agora")
            with c2: btn("❌ Não quero, mas obrigada", "Não quero")

        elif estado == "PS_ERRO_PAGAMENTO":
            c1, c2 = st.columns(2)
            with c1: btn("💳 Cartão de Crédito", "cartão")
            with c2: btn("📱 Pix", "pix")

        elif estado == "PS_MOTIVO_NEGATIVA_GERAL":
            c1, c2, c3 = st.columns(3)
            with c1: btn("1️⃣ Fora do rol da ANS", "Fora do rol da ANS")
            with c2: btn("2️⃣ Não atende diretriz (DUT)", "Não atende diretriz (DUT)")
            with c3: btn("3️⃣ Carência", "Carência")
            c4, c5, c6 = st.columns(3)
            with c4: btn("4️⃣ Não é urgente", "Não é urgente")
            with c5: btn("5️⃣ Experimental", "Experimental")
            with c6: btn("6️⃣ Outro", "Outro")

        elif estado == "PS_PERGUNTAS_COLETOR":
            idx = st.session_state.pergunta_idx
            perguntas = st.session_state.perguntas_ativas
            if idx < len(perguntas):
                pergunta_atual = perguntas[idx]
                q = pergunta_atual.lower()

                # Terapias indicadas: permite múltiplas alternativas, pois o médico pode prescrever mais de uma terapia.
                if pergunta_atual == PS_TERA_Q2:
                    render_multiselect_terapias()
                # Regra geral: toda pergunta com alternativas numeradas deve virar botão,
                # inclusive Oftalmologia, Exames, Home Care, Terapias, Reajuste, Coparticipação e Erro Médico.
                elif render_opcoes_numeradas(pergunta_atual):
                    pass
                # Motivo da negativa: não exibir botões genéricos de Sim/Não.
                # Exibir as 6 opções corretas do texto.
                elif "qual foi o motivo da negativa" in q:
                    c1, c2, c3 = st.columns(3)
                    with c1: btn("1️⃣ Fora do rol da ANS", "Fora do rol da ANS")
                    with c2: btn("2️⃣ Não atende diretriz (DUT)", "Não atende diretriz (DUT)")
                    with c3: btn("3️⃣ Carência", "Carência")
                    c4, c5, c6 = st.columns(3)
                    with c4: btn("4️⃣ Não é urgente", "Não é urgente")
                    with c5: btn("5️⃣ Experimental", "Experimental")
                    with c6: btn("6️⃣ Outro", "Outro")
                # Hospital da rede do plano: NÃO exibir botões genéricos de Sim/Não.
                # Exibir somente as 3 opções corretas: Sim, Não e Não sei.
                elif "hospital onde seria realizada" in q and "rede do plano" in q:
                    c1, c2, c3 = st.columns(3)
                    with c1: btn("1️⃣ Sim", "Sim")
                    with c2: btn("2️⃣ Não", "Não")
                    with c3: btn("3️⃣ Não sei", "Não sei")
                # Para pergunta de negativa por escrita ou verbal
                elif "escrita ou verbal" in q:
                    c1, c2 = st.columns(2)
                    with c1: btn("✍️ Escrita", "Escrita")
                    with c2: btn("📞 Verbal (telefone/balcão)", "Verbal")
                # Opção OUTROS na terapia
                elif "9️⃣ outros" in q:
                    c1 = st.columns(1)[0]
                    with c1: btn("9️⃣ OUTROS", "OUTROS")
                elif any(kw in q for kw in ["1️⃣ sim", "sim\n2️⃣ não", "você possui", "tem laudo",
                    "tem exames", "tem o laudo", "multidisciplinar",
                    "foi negado", "urgente", "receita médica"]):
                    c1, c2 = st.columns(2)
                    with c1: btn("✅ Sim", "Sim")
                    with c2: btn("❌ Não", "Não")

    show_buttons()

    st.markdown("---")
    user_input = st.text_input(
        "Digite sua mensagem apenas quando a pergunta for aberta:",
        key="user_input",
        placeholder="Use os botões quando eles aparecerem. Digite somente respostas abertas."
    )

    if st.button("📤 Enviar", use_container_width=True) and user_input:
        enviar_resposta_usuario(user_input)
        # Define novo timeout para resposta
        st.session_state.aguardando_resposta_desde = time.time()
        st.rerun()

    if not st.session_state.messages:
        add_bot(MSG_BOAS_VINDAS)
        st.rerun()


if __name__ == "__main__":
    main(
