    # PLANO_TEMPO
    elif estado == "PLANO_TEMPO":
        if _sim(resposta):
            dados["plano_2anos"] = "sim"
            st.session_state.estado = "PLANO_TIPO"
            add_bot(PS_TIPO_PLANO)
        else:
            dados["plano_2anos"] = "nao"
            st.session_state.estado = "PLANO_NAO_2ANOS"
            add_bot(PS_NAO_2ANOS)

    # PLANO_TIPO
    elif estado == "PLANO_TIPO":
        dados["plano_tipo"] = resposta
        st.session_state.estado = "PLANO_SITUACAO"
        add_bot(PS_SITUACAO)

    # PLANO_NAO_2ANOS
    elif estado == "PLANO_NAO_2ANOS":
        dados["tratamento_sem_carencia"] = resposta
        st.session_state.estado = "PLANO_NAO_2ANOS_URG"
        add_bot(PS_NAO_2ANOS_URG)

    # PLANO_NAO_2ANOS_URG
    elif estado == "PLANO_NAO_2ANOS_URG":
        dados["urgencia_plano"] = resposta
        st.session_state.estado = "PLANO_URGENCIA"
        add_bot(PS_URGENCIA)

    # PLANO_URGENCIA
    elif estado == "PLANO_URGENCIA":
        dados["urgencia_confirmada"] = resposta
        st.session_state.estado = "PLANO_SITUACAO"
        add_bot(PS_SITUACAO)

    # PLANO_SITUACAO
    elif estado == "PLANO_SITUACAO":
        dados["situacao"] = resposta
        
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

    # PS REPARADORA
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
            add_bot(PS_REP_Q3_JUNTAS)
    elif estado == "PS_REP_AGUARDANDO":
        if _sim(resposta):
            add_bot(f"Ótimo! Agende sua consulta: {CALENDLY_LINK}")
            st.session_state.link_enviado_em = datetime.now()
            st.session_state.lembrete_enviado = False
        else:
            add_bot(MSG_ENCERRAMENTO)
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
        if "acompanhamento" in _n(resposta) or "quero" in _n(resposta):
            st.session_state.estado = "PS_POS_PLANO"
            add_bot(PS_POS_CORRIGIDA)
        else:
            add_bot(MSG_ENCERRAMENTO)
            st.session_state.estado = "FIM"

    # PS_NEG_CIR_ESP
    elif estado == "PS_NEG_CIR_ESP":
        dados["ps_cir_esp"] = resposta
        if "endometriose" in _n(resposta) or "1" in resposta:
            st.session_state.perguntas_ativas = [PS_ENDO_Q1, PS_ENDO_Q2, PS_ENDO_Q3, PS_ENDO_Q4, PS_ENDO_Q5]
            st.session_state.pergunta_idx = 0
            st.session_state.estado = "PS_PERGUNTAS_GENERICO"
            add_bot(PS_ENDO_Q1)
        elif "bariátrica" in _n(resposta) or "2" in resposta:
            st.session_state.perguntas_ativas = [PS_BARI_Q1, PS_BARI_Q2, PS_BARI_Q3, PS_BARI_Q4, PS_BARI_Q5, PS_BARI_Q6, PS_BARI_Q7]
            st.session_state.pergunta_idx = 0
            st.session_state.estado = "PS_PERGUNTAS_GENERICO"
            add_bot(PS_BARI_Q1)
        elif "oncologia" in _n(resposta) or "3" in resposta:
            st.session_state.perguntas_ativas = [PS_ONCO_Q1, PS_ONCO_Q2, PS_ONCO_Q3, PS_ONCO_Q4, PS_ONCO_Q5, PS_ONCO_Q6]
            st.session_state.pergunta_idx = 0
            st.session_state.estado = "PS_PERGUNTAS_GENERICO"
            add_bot(PS_ONCO_Q1)
        elif "cardiologia" in _n(resposta) or "4" in resposta:
            st.session_state.perguntas_ativas = [PS_CARDIO_Q1, PS_CARDIO_Q2, PS_CARDIO_Q3, PS_CARDIO_Q4]
            st.session_state.pergunta_idx = 0
            st.session_state.estado = "PS_PERGUNTAS_GENERICO"
            add_bot(PS_CARDIO_Q1)
        elif "neurocirurgia" in _n(resposta) or "5" in resposta:
            st.session_state.perguntas_ativas = [PS_NEURO_Q1, PS_NEURO_Q2, PS_NEURO_Q3, PS_NEURO_Q4, PS_NEURO_Q5, PS_NEURO_Q6, PS_NEURO_Q7, PS_NEURO_Q8]
            st.session_state.pergunta_idx = 0
            st.session_state.estado = "PS_PERGUNTAS_GENERICO"
            add_bot(PS_NEURO_Q1)
        elif "ortopedia" in _n(resposta) or "6" in resposta:
            st.session_state.perguntas_ativas = [PS_ORTO_Q1, PS_ORTO_Q2, PS_ORTO_Q3, PS_ORTO_Q4, PS_ORTO_Q5, PS_ORTO_Q6]
            st.session_state.pergunta_idx = 0
            st.session_state.estado = "PS_PERGUNTAS_GENERICO"
            add_bot(PS_ORTO_Q1)
        elif "oftalmologia" in _n(resposta) or "7" in resposta:
            st.session_state.perguntas_ativas = [PS_OFTAL_Q1, PS_OFTAL_Q2, PS_OFTAL_Q3, PS_OFTAL_Q4, PS_OFTAL_Q5]
            st.session_state.pergunta_idx = 0
            st.session_state.estado = "PS_PERGUNTAS_GENERICO"
            add_bot(PS_OFTAL_Q1)
        else:
            st.session_state.perguntas_ativas = [PS_OUTRO_Q1, PS_OUTRO_Q2, PS_OUTRO_Q3, PS_OUTRO_Q4, PS_OUTRO_Q5, PS_OUTRO_Q6, PS_OUTRO_Q7]
            st.session_state.pergunta_idx = 0
            st.session_state.estado = "PS_PERGUNTAS_GENERICO"
            add_bot(PS_OUTRO_Q1)

    # PS_PERGUNTAS_GENERICO
    elif estado == "PS_PERGUNTAS_GENERICO":
        idx = st.session_state.pergunta_idx
        perguntas = st.session_state.perguntas_ativas
        
        dados[f"ps_resp_{idx}"] = resposta
        idx += 1
        st.session_state.pergunta_idx = idx
        
        if idx < len(perguntas):
            add_bot(perguntas[idx])
        else:
            st.session_state.estado = "PS_POS_PLANO"
            add_bot(PS_POS_CORRIGIDA)

    # PS MEDICAMENTO
    elif estado == "PS_MED_Q1":
        st.session_state.perguntas_ativas = [PS_MED_Q1, PS_MED_Q2, PS_MED_Q3, PS_MED_Q4, PS_MED_Q5, PS_MED_Q6, PS_MED_Q7, PS_MED_Q8, PS_MED_Q9, PS_MED_Q10]
        st.session_state.pergunta_idx = 0
        st.session_state.estado = "PS_PERGUNTAS_GENERICO"
        add_bot(PS_MED_Q1)

    # PS EXAME
    elif estado == "PS_EXAME_Q1":
        st.session_state.perguntas_ativas = [PS_EXAME_Q1, PS_EXAME_Q2, PS_EXAME_Q3, PS_EXAME_Q4, PS_EXAME_Q5, PS_EXAME_Q6, PS_EXAME_Q7]
        st.session_state.pergunta_idx = 0
        st.session_state.estado = "PS_PERGUNTAS_GENERICO"
        add_bot(PS_EXAME_Q1)

    # PS HOME CARE
    elif estado == "PS_HOME_Q1":
        st.session_state.perguntas_ativas = [PS_HOME_Q1, PS_HOME_Q2, PS_HOME_Q3, PS_HOME_Q4, PS_HOME_Q5, PS_HOME_Q6, PS_HOME_Q7]
        st.session_state.pergunta_idx = 0
        st.session_state.estado = "PS_PERGUNTAS_GENERICO"
        add_bot(PS_HOME_Q1)

    # PS TERAPIAS
    elif estado == "PS_TERA_Q1":
        st.session_state.perguntas_ativas = [PS_TERA_Q1, PS_TERA_Q2, PS_TERA_Q3, PS_TERA_Q4, PS_TERA_Q5, PS_TERA_Q6, PS_TERA_Q7]
        st.session_state.pergunta_idx = 0
        st.session_state.estado = "PS_PERGUNTAS_GENERICO"
        add_bot(PS_TERA_Q1)

    # PS REAJUSTE
    elif estado == "PS_REAJ_Q1":
        st.session_state.perguntas_ativas = [PS_REAJ_Q1, PS_REAJ_Q2, PS_REAJ_Q3, PS_REAJ_Q4, PS_REAJ_Q5, PS_REAJ_Q6, PS_REAJ_Q7, PS_REAJ_Q8]
        st.session_state.pergunta_idx = 0
        st.session_state.estado = "PS_PERGUNTAS_GENERICO"
        add_bot(PS_REAJ_Q1)

    # PS COPARTICIPAÇÃO
    elif estado == "PS_COPA_Q1":
        st.session_state.perguntas_ativas = [PS_COPA_Q1, PS_COPA_Q2, PS_COPA_Q3, PS_COPA_Q4, PS_COPA_Q5, PS_COPA_Q6, PS_COPA_Q7]
        st.session_state.pergunta_idx = 0
        st.session_state.estado = "PS_PERGUNTAS_GENERICO"
        add_bot(PS_COPA_Q1)

    # PS ERRO MÉDICO
    elif estado == "PS_ERRO_Q1":
        st.session_state.perguntas_ativas = [PS_ERRO_Q1, PS_ERRO_Q2, PS_ERRO_Q3, PS_ERRO_Q4, PS_ERRO_Q5, PS_ERRO_Q6]
        st.session_state.pergunta_idx = 0
        st.session_state.estado = "PS_PERGUNTAS_GENERICO"
        add_bot(PS_ERRO_Q1)

    # PS OUTRO
    elif estado == "PS_OUTRO_Q1":
        st.session_state.perguntas_ativas = [PS_OUTRO_Q1, PS_OUTRO_Q2, PS_OUTRO_Q3, PS_OUTRO_Q4, PS_OUTRO_Q5, PS_OUTRO_Q6, PS_OUTRO_Q7]
        st.session_state.pergunta_idx = 0
        st.session_state.estado = "PS_PERGUNTAS_GENERICO"
        add_bot(PS_OUTRO_Q1)

    # PS_POS_PLANO (4 opções)
    elif estado == "PS_POS_PLANO":
        dados["ps_pos_escolha"] = resposta
        if "1" in resposta:
            st.session_state.estado = "PS_OP1_PERMISSAO"
            add_bot(PS_OP1_PERMISSAO)
        elif "2" in resposta:
            st.session_state.estado = "PS_OP2"
            add_bot(PS_OP2)
        elif "3" in resposta:
            st.session_state.estado = "PS_OP3"
            add_bot(PS_OP3_CORRIGIDA)
        elif "4" in resposta:
            st.session_state.estado = "PS_OP4"
            add_bot(PS_OP4)
        else:
            add_bot(PS_POS_CORRIGIDA)

    # PS_OP1 - Atendimento Expresso
    elif estado == "PS_OP1_PERMISSAO":
        if _sim(resposta):
            add_bot(PS_OP1_DETALHES)
            st.session_state.estado = "PS_OP1_AGENDAMENTO"
        else:
            add_bot(MSG_ENCERRAMENTO)
            st.session_state.estado = "FIM"

    # PS_OP1_AGENDAMENTO
    elif estado == "PS_OP1_AGENDAMENTO":
        if _sim(resposta):
            add_bot(MSG_AGENDAMENTO)
            st.session_state.estado = "PS_PAGAMENTO"
        else:
            add_bot(MSG_ENCERRAMENTO)
            st.session_state.estado = "FIM"

    # PS_OP2 - Já tem negativa
    elif estado == "PS_OP2":
        dados["ps_op2_decisao"] = resposta
        st.session_state.estado = "PS_OP2_BOTOES"
        # Aguardar botões na interface

    # PS_OP2_BOTOES
    elif estado == "PS_OP2_BOTOES":
        if "sim" in _n(resposta) or "1" in resposta:
            add_bot(DECISAO_SIM)
            st.session_state.link_enviado_em = datetime.now()
            st.session_state.lembrete_enviado = False
        elif "não" in _n(resposta) or "2" in resposta:
            add_bot(DECISAO_NAO)
            st.session_state.link_enviado_em = datetime.now()
            st.session_state.lembrete_enviado = False
        else:
            add_bot(DECISAO_REPASSE)
            st.session_state.estado = "DECISAO_REPASSE_RESPOSTA"
            return
        st.session_state.estado = "FIM"

    # PS_OP3 - Preventivo
    elif estado == "PS_OP3":
        dados["ps_op3_entendeu"] = resposta
        st.session_state.estado = "PS_OP3_PERMISSAO"
        add_bot(PS_OP3_PERMISSAO)

    # PS_OP3_PERMISSAO
    elif estado == "PS_OP3_PERMISSAO":
        if "acompanhamento" in _n(resposta) or "quero" in _n(resposta):
            add_bot("Perfeito. O próximo passo agora é uma reunião rápida para a Dra Lethicia te explicar como funciona o processo e valores de honorários.\n\nAntes de agendarmos: além de você, tem mais alguém que participe das decisões familiares ou financeiras, como seu esposo/esposa, que seria importante estar presente para já tirarmos todas as dúvidas de uma vez?")
            st.session_state.estado = "PS_OP2_BOTOES"
        else:
            add_bot(MSG_ENCERRAMENTO)
            st.session_state.estado = "FIM"

    # PS_OP4 - Consultoria Jurídica
    elif estado == "PS_OP4":
        if _sim(resposta):
            add_bot(MSG_AGENDAMENTO)
            st.session_state.estado = "PS_PAGAMENTO_CONSULTORIA"
        else:
            add_bot(MSG_ENCERRAMENTO)
            st.session_state.estado = "FIM"

    # PS_PAGAMENTO
    elif estado == "PS_PAGAMENTO":
        add_bot("Perfeito! Vamos reservar o seu horário.")
        st.session_state.link_enviado_em = datetime.now()
        st.session_state.lembrete_enviado = False
        st.session_state.estado = "FIM"

    # PS_PAGAMENTO_CONSULTORIA
    elif estado == "PS_PAGAMENTO_CONSULTORIA":
        add_bot(f"Perfeito! Vamos reservar o seu horário.\n\n🔗 {CALENDLY_LINK}")
        st.session_state.link_enviado_em = datetime.now()
        st.session_state.lembrete_enviado = False
        st.session_state.estado = "FIM"

    # FIM
    elif estado == "FIM":
        pass

    enviar_lembrete()


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
    
    elif estado in ["HONORARIOS", "AGUARDANDO_DOCUMENTOS", "PS_OP1_PERMISSAO", "PS_OP1_AGENDAMENTO", "PS_OP4"]:
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
    
    elif estado == "CONSULTA_BOTOES":
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ QUERO AJUDA DA DRA LETHICIA", use_container_width=True):
                add_user("Quero ajuda")
                processar("Quero ajuda")
                st.rerun()
        with col2:
            if st.button("❌ QUERO AGUARDAR", use_container_width=True):
                add_user("quero aguardar")
                processar("quero aguardar")
                st.rerun()
    
    elif estado == "EXAME_BOTOES":
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ QUERO AJUDA DA DRA LETHICIA", use_container_width=True):
                add_user("Quero ajuda")
                processar("Quero ajuda")
                st.rerun()
        with col2:
            if st.button("❌ QUERO AGUARDAR", use_container_width=True):
                add_user("quero aguardar")
                processar("quero aguardar")
                st.rerun()
    
    elif estado == "CONSULTA_SIM_NAO" or estado == "EXAME_SIM_NAO":
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
    
    elif estado == "CONSULTA_DOCUMENTOS":
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("✅ Sim, tenho os documentos", use_container_width=True):
                add_user("Sim, tenho os documentos")
                processar("Sim, tenho os documentos")
                st.rerun()
        with col2:
            if st.button("⚠️ Tenho apenas o pedido médico", use_container_width=True):
                add_user("Tenho apenas o pedido médico")
                processar("Tenho apenas o pedido médico")
                st.rerun()
        with col3:
            if st.button("❌ Não tenho comprovante", use_container_width=True):
                add_user("Não tenho comprovante")
                processar("Não tenho comprovante")
                st.rerun()
    
    elif estado == "PS_OP2_BOTOES":
        st.markdown("---")
        st.markdown("**🔘 Como prefere prosseguir?**")
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
                processar("Tem meu cônjuge, mas pode falar só comigo")
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
    
    elif estado == "PS_OP3_PERMISSAO":
        st.markdown("---")
        st.markdown("**🔘 Como prefere prosseguir?**")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Quero o acompanhamento da Dra.", use_container_width=True):
                add_user("Quero acompanhamento")
                processar("acompanhamento")
                st.rerun()
        with col2:
            if st.button("❌ Prefiro tentar sozinho", use_container_width=True):
                add_user("sozinho")
                processar("sozinho")
                st.rerun()
    
    elif estado == "PS_PAGAMENTO":
        st.markdown("---")
        st.markdown("**💳 Forma de pagamento:**")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💳 Cartão de Crédito", use_container_width=True):
                st.markdown("🔗 [Link para pagamento com cartão](https://www.asaas.com/c/oilhnffc7xyvc4n6)")
                add_user("Cartão de crédito")
                processar("Cartão")
                st.rerun()
        with col2:
            if st.button("📱 PIX", use_container_width=True):
                st.markdown(f"**Chave PIX:** `{PIX_KEY}`\n\n🔗 [Link para pagamento PIX](https://www.asaas.com/c/9025wgqkpuziono4)")
                add_user("PIX")
                processar("PIX")
                st.rerun()
    
    elif estado == "PS_PAGAMENTO_CONSULTORIA":
        st.markdown("---")
        st.markdown("**💳 Forma de pagamento:**")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💳 Cartão de Crédito", use_container_width=True):
                st.markdown("🔗 [Link para pagamento com cartão](https://www.asaas.com/c/apigp8m45tileghw)")
                add_user("Cartão de crédito")
                processar("Cartão")
                st.rerun()
        with col2:
            if st.button("📱 PIX", use_container_width=True):
                st.markdown(f"**Chave PIX:** `{PIX_KEY}`\n\n🔗 [Link para pagamento PIX](https://www.asaas.com/c/x1dfvyoajxnlgpp2)")
                add_user("PIX")
                processar("PIX")
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
