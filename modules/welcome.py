"""
Schermata di benvenuto per CoinPilot
CoinPilot - Il tuo copilota per una finanza paziente
"""
import streamlit as st
import random


class WelcomeScreen:
    """Gestisce la schermata di benvenuto iniziale"""
    
    # Citazioni ispirazionali dal libro "L'arte della pazienza finanziaria"
    CITAZIONI = [
        {
            "testo": "La ricchezza non si costruisce con la velocità, ma con la costanza.",
            "autore": "L'arte della pazienza finanziaria"
        },
        {
            "testo": "Il tempo è l'alleato più potente dell'investitore paziente.",
            "autore": "L'arte della pazienza finanziaria"
        },
        {
            "testo": "Ogni euro risparmiato oggi è un seme che fiorirà domani.",
            "autore": "L'arte della pazienza finanziaria"
        },
        {
            "testo": "La vera libertà finanziaria nasce dalla calma, non dalla fretta.",
            "autore": "L'arte della pazienza finanziaria"
        },
        {
            "testo": "Pianificare con pazienza significa costruire il futuro con consapevolezza.",
            "autore": "L'arte della pazienza finanziaria"
        }
    ]
    
    @staticmethod
    def should_show_welcome():
        """
        Decide se mostrare la schermata di benvenuto
        Restituisce True se è la prima visita o se l'utente non ha ancora iniziato
        """
        if "welcome_completed" not in st.session_state:
            st.session_state["welcome_completed"] = False
        return not st.session_state["welcome_completed"]
    
    @staticmethod
    def complete_welcome():
        """Marca la welcome come completata"""
        st.session_state["welcome_completed"] = True
    
    @staticmethod
    def reset_welcome():
        """Resetta la welcome (per mostrarla di nuovo)"""
        st.session_state["welcome_completed"] = False
    
    @staticmethod
    def render():
        """Renderizza la schermata di benvenuto completa"""
        
        # CSS personalizzato per la welcome page
        welcome_css = """
        <style>
        .welcome-container {
            text-align: center;
            padding: 60px 20px;
            background: linear-gradient(135deg, #FAFAFA 0%, #F0F0F0 100%);
            border-radius: 20px;
            margin: 20px 0;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
        }
        
        .welcome-logo {
            font-size: 100px;
            margin-bottom: 20px;
            animation: float 3s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-15px); }
        }
        
        .welcome-title {
            font-size: 48px;
            font-weight: 800;
            color: #B8860B;
            margin-bottom: 10px;
            letter-spacing: -1px;
        }
        
        .welcome-subtitle {
            font-size: 20px;
            color: #2C3E50;
            font-style: italic;
            margin-bottom: 40px;
        }
        
        .welcome-quote-box {
            background: white;
            border-left: 5px solid #B8860B;
            padding: 30px;
            margin: 30px auto;
            max-width: 600px;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        }
        
        .welcome-quote-text {
            font-size: 22px;
            color: #2C3E50;
            font-style: italic;
            line-height: 1.5;
            margin-bottom: 15px;
        }
        
        .welcome-quote-author {
            font-size: 14px;
            color: #999;
            font-weight: 600;
        }
        
        .welcome-description {
            font-size: 16px;
            color: #666;
            max-width: 700px;
            margin: 30px auto;
            line-height: 1.6;
        }
        
        .welcome-features {
            display: flex;
            justify-content: center;
            gap: 30px;
            flex-wrap: wrap;
            margin: 40px 0;
        }
        
        .welcome-feature {
            background: white;
            padding: 20px;
            border-radius: 15px;
            width: 200px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        }
        
        .welcome-feature-icon {
            font-size: 40px;
            margin-bottom: 10px;
        }
        
        .welcome-feature-title {
            font-size: 16px;
            font-weight: 700;
            color: #2C3E50;
            margin-bottom: 5px;
        }
        
        .welcome-feature-desc {
            font-size: 13px;
            color: #666;
        }
        
        @media (max-width: 768px) {
            .welcome-container {
                padding: 40px 15px;
            }
            
            .welcome-logo {
                font-size: 70px;
            }
            
            .welcome-title {
                font-size: 32px;
            }
            
            .welcome-subtitle {
                font-size: 16px;
            }
            
            .welcome-quote-text {
                font-size: 18px;
            }
            
            .welcome-features {
                gap: 15px;
            }
            
            .welcome-feature {
                width: 150px;
                padding: 15px;
            }
        }
        </style>
        """
        
        st.markdown(welcome_css, unsafe_allow_html=True)
        
        # Seleziona una citazione casuale
        citazione = random.choice(WelcomeScreen.CITAZIONI)
        
        # Container principale - HEADER
        st.markdown(
            """
            <div class="welcome-container">
                <div class="welcome-logo">🪙</div>
                <div class="welcome-title">CoinPilot</div>
                <div class="welcome-subtitle">Il tuo copilota per una finanza paziente</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Box citazione
        st.markdown(
            f"""
            <div class="welcome-quote-box">
                <div class="welcome-quote-text">"{citazione['testo']}"</div>
                <div class="welcome-quote-author">— {citazione['autore']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Descrizione
        st.markdown(
            """
            <div class="welcome-description">
                Un'app pensata per chi crede che la vera ricchezza si costruisca 
                con calma, costanza e lungimiranza. Pianifica il tuo futuro finanziario 
                con la serenità di chi sa che il tempo è il miglior alleato.
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Feature cards
        st.markdown(
            """
            <div class="welcome-features">
                <div class="welcome-feature">
                    <div class="welcome-feature-icon">📊</div>
                    <div class="welcome-feature-title">Budget</div>
                    <div class="welcome-feature-desc">Gestisci entrate e spese con chiarezza</div>
                </div>
                <div class="welcome-feature">
                    <div class="welcome-feature-icon">🎯</div>
                    <div class="welcome-feature-title">Proiezioni</div>
                    <div class="welcome-feature-desc">Visualizza la crescita del tuo capitale</div>
                </div>
                <div class="welcome-feature">
                    <div class="welcome-feature-icon">🏆</div>
                    <div class="welcome-feature-title">Obiettivi</div>
                    <div class="welcome-feature-desc">Raggiungi i tuoi traguardi passo dopo passo</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Pulsante "Inizia"
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Inizia il tuo viaggio", use_container_width=True, type="primary"):
                WelcomeScreen.complete_welcome()
                st.rerun()
        
        # Footer con riferimento al libro
        st.markdown(
            """
            <div style="text-align: center; margin-top: 40px; color: #999; font-size: 13px;">
                <em>Ispirato a "L'arte della pazienza finanziaria"</em>
            </div>
            """,
            unsafe_allow_html=True
        )