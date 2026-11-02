"""
Quiz della Pazienza Finanziaria
CoinPilot - Il tuo copilota per una finanza paziente
Con salvataggio dei risultati per utente
"""
import streamlit as st
from datetime import datetime
from modules.storage import AutoStorage


class FinancialQuiz:
    """Gestisce il quiz per scoprire il profilo dell'investitore"""
    
    QUESTIONS = [
        {
            "question": "Il tuo portafoglio investimenti perde il 20% in un mese. Cosa fai?",
            "options": [
                ("Vendo tutto per paura di perdere altro.", 1),
                ("Aspetto e valuto la situazione senza fare nulla di impulsivo.", 2),
                ("Approfitto dei prezzi bassi per comprare di più, sapendo che il tempo recupera tutto.", 3)
            ]
        },
        {
            "question": "Qual è il tuo orizzonte temporale ideale per un investimento?",
            "options": [
                ("Meno di 1 anno (ho bisogno dei soldi a breve).", 1),
                ("Tra 1 e 5 anni (un obiettivo di medio termine).", 2),
                ("Oltre 10 anni (sto costruendo il mio futuro a lungo termine).", 3)
            ]
        },
        {
            "question": "Qual è il tuo approccio al risparmio mensile?",
            "options": [
                ("Risparmio solo ciò che mi avanza a fine mese (se avanza).", 1),
                ("Cerco di mettere da parte una cifra fissa, ma a volte salto i mesi.", 2),
                ("Automatizzo il risparmio: una percentuale fissa viene investita prima ancora di spendere.", 3)
            ]
        },
        {
            "question": "Come reagisci alle notizie finanziarie allarmistiche?",
            "options": [
                ("Mi agito e controllo il portafoglio più volte al giorno.", 1),
                ("Le leggo con attenzione e mi preoccupo moderatamente.", 2),
                ("Le ignoro: il mio piano è basato sulla costanza, non sulle emozioni del momento.", 3)
            ]
        },
        {
            "question": "Cosa significa per te 'Indipendenza Finanziaria'?",
            "options": [
                ("Avere abbastanza soldi per fare acquisti di lusso subito.", 1),
                ("Avere un fondo di emergenza per imprevisti.", 2),
                ("Costruire un patrimonio che generi rendite passive per vivere con serenità e libertà.", 3)
            ]
        }
    ]

    @staticmethod
    def should_show_quiz():
        """Decide se mostrare il quiz (solo se non ci sono risultati salvati)"""
        saved_results = AutoStorage.load_quiz_results()
        
        if saved_results:
            # Carica i risultati salvati in session_state
            st.session_state["investor_profile"] = saved_results["profile"]
            st.session_state["quiz_score"] = saved_results["score"]
            st.session_state["quiz_completed"] = True
            return False
        
        return not st.session_state.get("quiz_completed", False)

    @staticmethod
    def complete_quiz(profile_name, score):
        """Salva il risultato del quiz"""
        st.session_state["quiz_completed"] = True
        st.session_state["investor_profile"] = profile_name
        st.session_state["quiz_score"] = score
        st.session_state["quiz_timestamp"] = datetime.now().isoformat()
        
        # Salva i risultati nel file specifico per l'utente
        AutoStorage.save_quiz_results(profile_name, score)

    @staticmethod
    def reset_quiz():
        """Resetta il quiz (permette di rifarlo)"""
        st.session_state["quiz_completed"] = False
        AutoStorage.clear_quiz_results()
        
        if "investor_profile" in st.session_state:
            del st.session_state["investor_profile"]
        if "quiz_score" in st.session_state:
            del st.session_state["quiz_score"]
        if "quiz_timestamp" in st.session_state:
            del st.session_state["quiz_timestamp"]

    @staticmethod
    def render():
        """Renderizza l'interfaccia del quiz"""
        st.title("🧠 Quiz della Pazienza Finanziaria")
        st.markdown(
            "Prima di iniziare il tuo viaggio con CoinPilot, scopriamo qual è il tuo profilo di investitore. "
            "Rispondi con sincerità: non ci sono risposte sbagliate, solo consapevolezza!"
        )
        st.markdown("---")
        
        answers = {}
        
        for i, q in enumerate(FinancialQuiz.QUESTIONS):
            st.markdown(f"**{i+1}. {q['question']}**")
            options = [opt[0] for opt in q['options']]
            
            choice = st.radio(
                "Scegli un'opzione:", 
                options, 
                key=f"q_{i}",
                index=None
            )
            
            if choice:
                idx = options.index(choice)
                answers[i] = q['options'][idx][1]
        
        st.markdown("---")
        
        if len(answers) == len(FinancialQuiz.QUESTIONS):
            total_score = sum(answers.values())
            
            if total_score <= 7:
                profile = "🌱 Principiante Impaziente"
                advice = "La fretta è cattiva consigliera. Inizia con piccoli passi: crea un fondo di emergenza e impara a risparmiare con costanza prima di investire."
            elif total_score <= 11:
                profile = "⚖️ Investitore Bilanciato"
                advice = "Hai una buona base! Cerchi l'equilibrio tra sicurezza e crescita. Perfeziona la tua disciplina automatizzando i risparmi e allungando l'orizzonte temporale."
            else:
                profile = "🦉 Maestro della Pazienza Finanziaria"
                advice = "Complimenti! Hai compreso il segreto più grande: il tempo è il tuo alleato più potente. La costanza e la disciplina batteranno sempre l'emotività del mercato."
            
            st.markdown(f"### Il tuo profilo: **{profile}**")
            st.info(f"💡 **Consiglio per te:** {advice}")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("🚀 Inizia il tuo viaggio con CoinPilot", type="primary", use_container_width=True):
                FinancialQuiz.complete_quiz(profile, total_score)
                st.rerun()
        else:
            st.warning("⚠️ Rispondi a tutte le domande per scoprire il tuo profilo!")