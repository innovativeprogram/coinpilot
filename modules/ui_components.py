"""
Componenti UI riutilizzabili per Streamlit
"""
import streamlit as st
import plotly.express as px
import pandas as pd


class UIComponents:
    """Componenti UI riutilizzabili"""
    
    @staticmethod
    def render_header():
        """Renderizza l'header dell'app"""
        st.title("🪙 CoinPilot")
        st.markdown("### *Il tuo copilota per una finanza paziente*")
        st.markdown(
            "Gestisci il tuo budget, simula risparmi e pianifica i tuoi obiettivi finanziari "
            "con la calma e la lungimiranza di chi sa che il tempo è il miglior alleato."
        )
    
    @staticmethod
    def render_sidebar_inputs(budget_manager):
        """Renderizza gli input nella sidebar"""
        st.sidebar.header("📊 I tuoi dati finanziari")
        
        entrate = st.sidebar.number_input(
            "Entrate mensili nette (€)", 
            min_value=0.0, 
            value=2000.0, 
            step=50.0
        )
        
        st.sidebar.subheader("Spese mensili")
        spese = {}
        for categoria, default in budget_manager.default_spese.items():
            spese[categoria] = st.sidebar.number_input(
                f"{categoria} (€)", 
                0.0, 
                default, 
                10.0
            )
        
        st.sidebar.subheader("💼 Parametri investimento")
        tasso = st.sidebar.slider(
            "Rendimento annuo stimato (%)", 
            0.0, 15.0, 5.0, 0.1
        ) / 100
        anni = st.sidebar.slider(
            "Orizzonte temporale (anni)", 
            1, 40, 10
        )
        capitale_iniziale = st.sidebar.number_input(
            "Capitale iniziale (€)", 
            0.0, 0.0, 100.0
        )
        
        return {
            "entrate": entrate,
            "spese": spese,
            "tasso": tasso,
            "anni": anni,
            "capitale_iniziale": capitale_iniziale
        }
    
    @staticmethod
    def render_metrics(budget_data):
        """Renderizza le metriche principali"""
        col1, col2, col3, col4 = st.columns(4)
        
        col1.metric("Entrate", f"€ {budget_data['entrate']:,.2f}")
        col2.metric(
            "Spese", 
            f"€ {budget_data['totale_spese']:,.2f}",
            delta=f"{(budget_data['totale_spese']/budget_data['entrate']*100) if budget_data['entrate']>0 else 0:.1f}% entrate"
        )
        col3.metric(
            "Risparmio mensile", 
            f"€ {budget_data['risparmio_mensile']:,.2f}",
            delta=f"{budget_data['percentuale_risparmio']:.1f}%"
        )
        col4.metric("Risparmio annuo", f"€ {budget_data['risparmio_annuo']:,.2f}")
    
    @staticmethod
    def render_pie_chart(spese_dict):
        """Renderizza il grafico a torta delle spese"""
        df = pd.DataFrame({
            "Categoria": list(spese_dict.keys()),
            "Importo (€)": list(spese_dict.values())
        })
        df = df[df["Importo (€)"] > 0]
        
        if not df.empty:
            fig = px.pie(
                df,
                values="Importo (€)",
                names="Categoria",
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Nessuna spesa inserita.")
    
    @staticmethod
    def render_bar_chart(budget_data):
        """Renderizza il grafico a barre entrate vs spese"""
        df = pd.DataFrame({
            "Voce": ["Entrate", "Spese", "Risparmio"],
            "Importo (€)": [
                budget_data["entrate"], 
                budget_data["totale_spese"], 
                max(budget_data["risparmio_mensile"], 0)
            ]
        })
        
        fig = px.bar(
            df,
            x="Voce", y="Importo (€)",
            color="Voce",
            color_discrete_map={
                "Entrate": "#2ecc71",
                "Spese": "#e74c3c",
                "Risparmio": "#3498db"
            }
        )
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def render_footer():
        """Renderizza il footer"""
        st.markdown("---")
        st.markdown(
            "<div style='text-align: center; color: #666; font-size: 0.9em;'>"
            "🪙 <strong>CoinPilot</strong> — Il tuo copilota per una finanza paziente<br>"
            "<em>Ispirato a 'L'arte della pazienza finanziaria'</em>"
            "</div>",
            unsafe_allow_html=True
        )