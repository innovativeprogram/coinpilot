"""
Componenti UI riutilizzabili per Streamlit
CoinPilot - Il tuo copilota per una finanza paziente
Versione con Dark Mode funzionante
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


class UIComponents:
    """Componenti UI riutilizzabili"""

    COLOR_PRIMARY = "#B8860B"
    COLOR_SUCCESS = "#2ECC71"
    COLOR_ERROR = "#E74C3C"
    COLOR_INFO = "#3498DB"
    COLOR_NEUTRAL = "#95A5A6"
    COLOR_MILESTONE = "#F39C12"

    # CSS per tema scuro - iniettato dinamicamente
    DARK_MODE_CSS = """
    <style>
    /* Sfondo principale */
    .stApp {
        background-color: #1a1a2e !important;
        color: #eaeaea !important;
    }
    
    /* Header e titoli */
    .stApp h1, .stApp h2, .stApp h3, .stApp h4 {
        color: #eaeaea !important;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #16213e !important;
    }
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] label {
        color: #eaeaea !important;
    }
    
    /* Card metriche */
    div[data-testid="stMetric"] {
        background-color: #0f3460 !important;
        border: 1px solid #2a2a4a !important;
    }
    div[data-testid="stMetric"] label {
        color: #b0b0b0 !important;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #eaeaea !important;
    }
    
    /* Input e number input */
    .stNumberInput input, .stTextInput input, .stTextArea textarea {
        background-color: #0f3460 !important;
        color: #eaeaea !important;
        border-color: #2a2a4a !important;
    }
    
    /* Slider */
    .stSlider label {
        color: #eaeaea !important;
    }
    
    /* Tabs */
    button[data-baseweb="tab"] {
        color: #b0b0b0 !important;
        background-color: #16213e !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #B8860B !important;
        background-color: #0f3460 !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #0f3460 !important;
        color: #eaeaea !important;
    }
    
    /* Alert e messaggi */
    .stAlert {
        background-color: #0f3460 !important;
        color: #eaeaea !important;
    }
    
    /* DataFrame */
    .stDataFrame {
        background-color: #0f3460 !important;
    }
    
    /* Pulsanti */
    .stButton > button {
        background-color: #0f3460 !important;
        color: #eaeaea !important;
        border-color: #B8860B !important;
    }
    
    /* Selectbox */
    .stSelectbox label {
        color: #eaeaea !important;
    }
    
    /* File uploader */
    .stFileUploader label {
        color: #eaeaea !important;
    }
    
    /* Checkbox e radio */
    .stCheckbox label, .stRadio label {
        color: #eaeaea !important;
    }
    
    /* Testo normale */
    p, span, div {
        color: #eaeaea !important;
    }
    
    /* Link */
    a {
        color: #3498DB !important;
    }
    
    /* Sfondo grafici Plotly */
    .js-plotly-plot .plotly {
        background-color: #0f3460 !important;
    }
    </style>
    """

    # ------------------------------------------------------------------
    # DARK MODE TOGGLE
    # ------------------------------------------------------------------
    @staticmethod
    def render_dark_mode_toggle():
        """Renderizza il toggle per attivare/disattivare la dark mode"""
        if "dark_mode" not in st.session_state:
            st.session_state["dark_mode"] = False
        
        # Posiziona il toggle in alto a destra usando columns
        col1, col2 = st.columns([10, 1])
        with col2:
            dark_mode = st.toggle("🌙", value=st.session_state["dark_mode"], key="dark_mode_toggle")
            if dark_mode != st.session_state["dark_mode"]:
                st.session_state["dark_mode"] = dark_mode
                st.rerun()
        
        return st.session_state["dark_mode"]

    @staticmethod
    def apply_dark_mode(is_dark):
        """Applica il tema scuro iniettando CSS dinamico"""
        if is_dark:
            st.markdown(UIComponents.DARK_MODE_CSS, unsafe_allow_html=True)

    # ------------------------------------------------------------------
    # HEADER E FOOTER
    # ------------------------------------------------------------------
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

    # ------------------------------------------------------------------
    # INPUT SIDEBAR
    # ------------------------------------------------------------------
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
                min_value=0.0,
                value=float(default),
                step=10.0
            )

        st.sidebar.subheader("💼 Parametri investimento")
        tasso = st.sidebar.slider(
            "Rendimento annuo stimato (%)",
            min_value=0.0,
            max_value=15.0,
            value=5.0,
            step=0.1
        ) / 100

        anni = st.sidebar.slider(
            "Orizzonte temporale (anni)",
            min_value=1,
            max_value=40,
            value=10
        )

        capitale_iniziale = st.sidebar.number_input(
            "Capitale iniziale (€)",
            min_value=0.0,
            value=0.0,
            step=100.0
        )

        return {
            "entrate": entrate,
            "spese": spese,
            "tasso": tasso,
            "anni": anni,
            "capitale_iniziale": capitale_iniziale
        }

    # ------------------------------------------------------------------
    # METRICHE
    # ------------------------------------------------------------------
    @staticmethod
    def render_metrics(budget_data):
        """Renderizza le metriche principali"""
        col1, col2, col3, col4 = st.columns(4)

        perc_spese = (
            budget_data["totale_spese"] / budget_data["entrate"] * 100
            if budget_data["entrate"] > 0 else 0
        )

        col1.metric("Entrate", f"€ {budget_data['entrate']:,.2f}")
        col2.metric(
            "Spese",
            f"€ {budget_data['totale_spese']:,.2f}",
            delta=f"{perc_spese:.1f}% entrate",
            delta_color="inverse"
        )
        col3.metric(
            "Risparmio mensile",
            f"€ {budget_data['risparmio_mensile']:,.2f}",
            delta=f"{budget_data['percentuale_risparmio']:.1f}%"
        )
        col4.metric("Risparmio annuo", f"€ {budget_data['risparmio_annuo']:,.2f}")

    # ------------------------------------------------------------------
    # GRAFICI BASE
    # ------------------------------------------------------------------
    @staticmethod
    def render_pie_chart(spese_dict):
        """Renderizza il grafico a torta delle spese"""
        df = pd.DataFrame({
            "Categoria": list(spese_dict.keys()),
            "Importo (€)": list(spese_dict.values())
        })
        df = df[df["Importo (€)"] > 0]

        if df.empty:
            st.info("Nessuna spesa inserita.")
            return

        fig = px.pie(
            df,
            values="Importo (€)",
            names="Categoria",
            hole=0.45,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig.update_traces(
            textposition="inside",
            textinfo="percent+label",
            hovertemplate="<b>%{label}</b><br>€ %{value:,.2f}<br>%{percent}<extra></extra>"
        )
        fig.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(t=20, b=20, l=20, r=20)
        )
        st.plotly_chart(fig, use_container_width=True)

    @staticmethod
    def render_bar_chart(budget_data):
        """Renderizza il grafico a barre entrate vs spese"""
        df = pd.DataFrame({
            "Voce": ["Entrate", "Spese", "Risparmio"],
            "Importo (€)": [
                budget_data["entrate"],
                budget_data["totale_spese"],
                max(budget_data["risparmio_mensile"], 0.0)
            ]
        })

        fig = px.bar(
            df,
            x="Voce",
            y="Importo (€)",
            color="Voce",
            text_auto=",.0f",
            color_discrete_map={
                "Entrate": UIComponents.COLOR_SUCCESS,
                "Spese": UIComponents.COLOR_ERROR,
                "Risparmio": UIComponents.COLOR_INFO
            }
        )
        fig.update_traces(
            hovertemplate="<b>%{x}</b><br>€ %{y:,.2f}<extra></extra>"
        )
        fig.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            showlegend=False,
            margin=dict(t=20, b=20, l=20, r=20)
        )
        fig.update_yaxes(tickformat="€,.0f", gridcolor="LightGrey")
        st.plotly_chart(fig, use_container_width=True)

    # ------------------------------------------------------------------
    # GRAFICO MULTI-SCENARIO
    # ------------------------------------------------------------------
    @staticmethod
    def render_multi_scenario_chart(df_multi, milestones=None):
        """Renderizza il grafico con 3 scenari e traguardi"""
        fig = go.Figure()

        colori = {
            "Pessimistico": UIComponents.COLOR_ERROR,
            "Realistico": UIComponents.COLOR_INFO,
            "Ottimistico": UIComponents.COLOR_SUCCESS
        }

        fig.add_trace(go.Scatter(
            x=df_multi["Mese"],
            y=df_multi["Ottimistico"],
            line=dict(width=0),
            showlegend=False,
            hoverinfo="skip"
        ))
        fig.add_trace(go.Scatter(
            x=df_multi["Mese"],
            y=df_multi["Pessimistico"],
            fill="tonexty",
            fillcolor="rgba(52, 152, 219, 0.10)",
            line=dict(width=0),
            name="Area di incertezza",
            hoverinfo="skip"
        ))

        fig.add_trace(go.Scatter(
            x=df_multi["Mese"],
            y=df_multi["Solo versato"],
            name="Solo versato",
            line=dict(color=UIComponents.COLOR_NEUTRAL, width=2, dash="dash"),
            hovertemplate="Solo versato: € %{y:,.0f}<extra></extra>"
        ))

        for scenario in ["Pessimistico", "Realistico", "Ottimistico"]:
            fig.add_trace(go.Scatter(
                x=df_multi["Mese"],
                y=df_multi[scenario],
                name=scenario,
                line=dict(color=colori[scenario], width=3),
                hovertemplate=f"{scenario}: € %{{y:,.0f}}<extra></extra>"
            ))

        if milestones:
            mesi_x = []
            valori_y = []
            testi = []
            for m in milestones:
                idx = int(m["mese"])
                if idx < len(df_multi):
                    mesi_x.append(idx)
                    valori_y.append(float(df_multi["Realistico"].iloc[idx]))
                    testi.append(f"€ {m['traguardo']:,.0f}")

            if mesi_x:
                fig.add_trace(go.Scatter(
                    x=mesi_x,
                    y=valori_y,
                    mode="markers+text",
                    marker=dict(
                        size=14,
                        color=UIComponents.COLOR_MILESTONE,
                        symbol="star",
                        line=dict(width=1, color="white")
                    ),
                    text=testi,
                    textposition="top center",
                    textfont=dict(size=10, color=UIComponents.COLOR_PRIMARY),
                    name="Traguardi",
                    hovertemplate="Traguardo %{text}<br>Mese %{x}<extra></extra>"
                ))

        fig.update_layout(
            title="Proiezione Multi-Scenario",
            xaxis_title="Mesi",
            yaxis_title="Capitale (€)",
            hovermode="x unified",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(size=12),
            margin=dict(t=60, b=40, l=20, r=20)
        )

        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="LightGrey")
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="LightGrey", tickformat="€,.0f")

        st.plotly_chart(fig, use_container_width=True)

    # ------------------------------------------------------------------
    # TABELLA ANNUALE
    # ------------------------------------------------------------------
    @staticmethod
    def render_annual_table(df_annuale):
        """Renderizza la tabella riassuntiva annuale"""
        st.dataframe(
            df_annuale[["Anno", "Capitale", "Versato", "Interessi"]]
            .style.format({
                "Capitale": "€ {:,.2f}",
                "Versato": "€ {:,.2f}",
                "Interessi": "€ {:,.2f}"
            }),
            use_container_width=True,
            hide_index=True
        )

    # ------------------------------------------------------------------
    # TIMELINE OBIETTIVI
    # ------------------------------------------------------------------
    @staticmethod
    def render_goal_timeline(timeline, obiettivo):
        """Renderizza una timeline visuale con tappe intermedie"""
        if not timeline:
            st.info("Nessuna tappa calcolata.")
            return

        st.markdown("#### 📊 Progresso verso l'obiettivo")
        
        progress_html = f"""
        <div style="background-color: #f0f0f0; border-radius: 10px; padding: 5px; margin: 20px 0;">
            <div style="background: linear-gradient(90deg, {UIComponents.COLOR_PRIMARY} 0%, {UIComponents.COLOR_SUCCESS} 100%); 
                        height: 30px; border-radius: 8px; 
                        display: flex; align-items: center; justify-content: center;
                        color: white; font-weight: bold; font-size: 14px;">
                Obiettivo: € {obiettivo:,.0f}
            </div>
        </div>
        """
        st.markdown(progress_html, unsafe_allow_html=True)

        st.markdown("#### 🎯 Tappe intermedie")
        
        cols = st.columns(len(timeline))
        
        for i, tappa in enumerate(timeline):
            with cols[i]:
                if tappa["percentuale"] == 1.0:
                    icon = "🏆"
                    color = UIComponents.COLOR_MILESTONE
                elif tappa["percentuale"] >= 0.75:
                    icon = "🎯"
                    color = UIComponents.COLOR_SUCCESS
                elif tappa["percentuale"] >= 0.5:
                    icon = "⭐"
                    color = UIComponents.COLOR_INFO
                else:
                    icon = "📍"
                    color = UIComponents.COLOR_NEUTRAL

                card_html = f"""
                <div style="background-color: white; border: 2px solid {color}; 
                            border-radius: 15px; padding: 15px; text-align: center;
                            box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                    <div style="font-size: 32px; margin-bottom: 10px;">{icon}</div>
                    <div style="font-size: 18px; font-weight: bold; color: {color}; 
                                margin-bottom: 5px;">
                        {tappa['percentuale']*100:.0f}%
                    </div>
                    <div style="font-size: 14px; color: #666; margin-bottom: 10px;">
                        € {tappa['obiettivo_tappa']:,.0f}
                    </div>
                    <div style="font-size: 12px; color: #999;">
                        {tappa['anni']:.1f} anni<br>
                        ({tappa['mesi']} mesi)
                    </div>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)

        st.markdown("---")
        st.success(
            f"💪 Mantieni la costanza! Con il tuo risparmio mensile, "
            f"raggiungerai **€ {obiettivo:,.0f}** in **{timeline[-1]['anni']:.1f} anni**."
        )

    # ------------------------------------------------------------------
    # PRESENTAZIONE LIBRO
    # ------------------------------------------------------------------
    @staticmethod
    def render_book_presentation():
        """Renderizza la sezione di presentazione del libro"""
        st.markdown("### 📖 L'Arte della Pazienza Finanziaria")
        st.markdown("Il compagno di viaggio per trasformare la finanza da fonte di ansia a strumento di libertà.")
        st.markdown("---")
        
        col_img, col_text = st.columns([1, 2])
        
        with col_img:
            try:
                st.image("assets/cover.jpg", caption="L'Arte della Pazienza Finanziaria", use_container_width=True)
            except Exception:
                st.markdown(
                    """
                    <div style="background-color: #F0F0F0; border-radius: 15px; padding: 40px 20px; text-align: center; border: 2px dashed #B8860B;">
                        <div style="font-size: 60px; margin-bottom: 15px;">📚</div>
                        <div style="font-size: 18px; font-weight: bold; color: #2C3E50;">L'Arte della Pazienza Finanziaria</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        
        with col_text:
            st.markdown("""
            Quante volte hai rinunciato a investire perché ti sentivi sopraffatto? O hai preso decisioni finanziarie sbagliate per colpa dell'ansia o dell'entusiasmo del momento? 
            
            La verità è che il tuo peggior nemico non è il mercato, ma la tua psicologia. La paura di perdere, l'avidità e la FOMO sono le vere trappole che ti fanno perdere soldi.
            """)
            
            st.markdown("""
            **"L'Arte della Pazienza Finanziaria"** non è l'ennesimo manuale di "fuffa guru" e non promette ricchezze facili. È un percorso passo dopo passo che parte dal risparmio consapevole e ti guida fino al PAC su ETF, con un linguaggio chiaro, onesto e accessibile a tutti.
            """)
            
            st.markdown("""
            Se stai cercando un modo per diventare ricco in un giorno, questo libro non fa per te. Ma se vuoi costruire un rapporto più sereno con i tuoi risparmi, proteggere il tuo futuro dall'inflazione e imparare a investire con logica, allora questo è il tuo compagno di viaggio ideale.
            
            *Perché l'educazione finanziaria non è un lusso per pochi esperti, ma un diritto di tutti.*
            """)
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.link_button("🛒 Acquista su Amazon", "https://link.amazon/B07tC2LqG", use_container_width=True)

    # ------------------------------------------------------------------
    # CALCOLATORE FIRE
    # ------------------------------------------------------------------
    @staticmethod
    def render_fire_calculator(spese_annuali, capitale_attuale, risparmio_annuo, tasso_annuo):
        """Calcola quando l'utente può raggiungere l'indipendenza finanziaria"""
        st.markdown("### 🔥 Calcolatore FIRE")
        st.markdown("*Financial Independence, Retire Early - La regola del 4%*")
        st.markdown("---")
        
        capitale_fire = spese_annuali / 0.04
        
        st.markdown(f"#### 🎯 Il tuo numero FIRE: **€ {capitale_fire:,.0f}**")
        st.markdown(
            f"Secondo la **Regola del 4%**, hai bisogno di **€ {capitale_fire:,.0f}** "
            f"investiti per vivere di rendita prelevando il 4% all'anno "
            f"(€ {spese_annuali:,.0f}/anno) senza erodere il capitale."
        )
        
        st.markdown("---")
        
        if risparmio_annuo > 0 and capitale_attuale < capitale_fire:
            anni_per_fire = 0
            capitale_simulato = capitale_attuale
            capitale_list = [capitale_attuale]
            anni_list = [0]
            
            while capitale_simulato < capitale_fire and anni_per_fire < 100:
                capitale_simulato = capitale_simulato * (1 + tasso_annuo) + risparmio_annuo
                anni_per_fire += 1
                capitale_list.append(capitale_simulato)
                anni_list.append(anni_per_fire)
            
            st.success(
                f"🎉 Con un risparmio annuo di **€ {risparmio_annuo:,.0f}** e un rendimento del **{tasso_annuo*100:.1f}%**, "
                f"raggiungerai la libertà finanziaria in **{anni_per_fire} anni**!"
            )
            
            df_fire = pd.DataFrame({
                "Anno": anni_list,
                "Capitale": capitale_list
            })
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df_fire["Anno"],
                y=df_fire["Capitale"],
                mode="lines+markers",
                name="Il tuo capitale",
                line=dict(color=UIComponents.COLOR_PRIMARY, width=3)
            ))
            fig.add_hline(
                y=capitale_fire,
                line_dash="dash",
                line_color=UIComponents.COLOR_SUCCESS,
                annotation_text=f"🎯 FIRE: € {capitale_fire:,.0f}",
                annotation_position="top left"
            )
            fig.update_layout(
                title="Percorso verso la libertà finanziaria",
                xaxis_title="Anni",
                yaxis_title="Capitale (€)",
                plot_bgcolor="white",
                paper_bgcolor="white",
                yaxis_tickformat="€,.0f"
            )
            st.plotly_chart(fig, use_container_width=True)
            
        elif capitale_attuale >= capitale_fire:
            st.balloons()
            st.success(
                f"🏆 **HAI GIÀ RAGGIUNTO LA LIBERTÀ FINANZIARIA!** "
                f"Il tuo capitale attuale (€ {capitale_attuale:,.0f}) supera il tuo numero FIRE (€ {capitale_fire:,.0f}). "
                f"Sei ufficialmente libero!"
            )
        else:
            st.warning("⚠️ Con un risparmio annuo pari o inferiore a zero, non puoi raggiungere la FIRE.")
        
        st.markdown("---")
        st.info(
            "💡 **La Regola del 4%**: Studi storici mostrano che prelevare il 4% all'anno "
            "da un portafoglio bilanciato (azioni/obbligazioni) permette di non erodere il capitale "
            "per almeno 30 anni. È la base matematica del movimento FIRE."
        )

    # ------------------------------------------------------------------
    # SIMULATORE INFLAZIONE
    # ------------------------------------------------------------------
    @staticmethod
    def render_inflation_simulator(capitale_iniziale, risparmio_mensile, tasso_annuo, anni, inflazione_annua=0.025):
        """Simula l'effetto dell'inflazione sul potere d'acquisto"""
        import numpy as np
        
        st.markdown("### 📉 Simulatore di Inflazione")
        st.markdown("*Quanto varranno davvero i tuoi soldi tra qualche anno?*")
        st.markdown("---")
        
        mesi = np.arange(anni * 12 + 1)
        tasso_mensile = (1 + tasso_annuo) ** (1/12) - 1
        inflazione_mensile = (1 + inflazione_annua) ** (1/12) - 1
        
        if risparmio_mensile > 0 and tasso_mensile > 0:
            capitale_nominale = (capitale_iniziale * (1 + tasso_mensile) ** mesi + 
                                risparmio_mensile * (((1 + tasso_mensile) ** mesi - 1) / tasso_mensile))
        else:
            capitale_nominale = capitale_iniziale + risparmio_mensile * mesi
        
        fattore_inflazione = (1 + inflazione_mensile) ** mesi
        capitale_reale = capitale_nominale / fattore_inflazione
        
        df_inflazione = pd.DataFrame({
            "Mese": mesi,
            "Capitale Nominale (€)": capitale_nominale,
            "Capitale Reale (€)": capitale_reale,
            "Potere d'acquisto (%)": (capitale_reale / capitale_nominale) * 100
        })
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_inflazione["Mese"],
            y=df_inflazione["Capitale Nominale (€)"],
            name="Capitale Nominale",
            line=dict(color=UIComponents.COLOR_INFO, width=3)
        ))
        fig.add_trace(go.Scatter(
            x=df_inflazione["Mese"],
            y=df_inflazione["Capitale Reale (€)"],
            name="Capitale Reale (potere d'acquisto)",
            line=dict(color=UIComponents.COLOR_ERROR, width=3)
        ))
        fig.update_layout(
            title=f"Capitale Nominale vs Reale (inflazione {inflazione_annua*100:.1f}% annua)",
            xaxis_title="Mesi",
            yaxis_title="Valore (€)",
            hovermode="x unified",
            plot_bgcolor="white",
            paper_bgcolor="white",
            yaxis_tickformat="€,.0f"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        capitale_finale_nominale = capitale_nominale[-1]
        capitale_finale_reale = capitale_reale[-1]
        perdita_potere = ((capitale_finale_nominale - capitale_finale_reale) / capitale_finale_nominale) * 100
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "Capitale Nominale",
                f"€ {capitale_finale_nominale:,.0f}",
                help="Il valore numerico dei tuoi soldi"
            )
        with col2:
            st.metric(
                "Capitale Reale",
                f"€ {capitale_finale_reale:,.0f}",
                delta=f"-{perdita_potere:.1f}%",
                delta_color="inverse",
                help="Il potere d'acquisto reale dei tuoi soldi"
            )
        with col3:
            st.metric(
                "Perdita potere d'acquisto",
                f"{perdita_potere:.1f}%",
                help="Quanto valore 'perdi' a causa dell'inflazione"
            )
        
        st.markdown("---")
        st.warning(
            f"⚠️ Tra {anni} anni, **€ {capitale_finale_nominale:,.0f}** avranno lo stesso potere d'acquisto "
            f"di **€ {capitale_finale_reale:,.0f}** di oggi. "
            f"L'inflazione erode il **{perdita_potere:.1f}%** del tuo potere d'acquisto!"
        )
        
        st.info(
            "💡 **Perché è importante**: L'inflazione media in Europa è circa 2-3% all'anno. "
            "Lasciare i soldi fermi sul conto corrente significa perdere potere d'acquisto ogni anno. "
            "Investire con un rendimento superiore all'inflazione è l'unico modo per preservare e far crescere la tua ricchezza reale."
        )

    # ------------------------------------------------------------------
    # UTILS
    # ------------------------------------------------------------------
    @staticmethod
    def is_mobile():
        """Rileva se l'utente sta usando un dispositivo mobile"""
        if "is_mobile" not in st.session_state:
            st.session_state["is_mobile"] = False
        return st.session_state.get("is_mobile", False)