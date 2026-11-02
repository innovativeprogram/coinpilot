"""
Componenti UI riutilizzabili per Streamlit
CoinPilot - Il tuo copilota per una finanza paziente
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


class UIComponents:
    """Componenti UI riutilizzabili"""

    # Palette colori del brand CoinPilot
    COLOR_PRIMARY = "#B8860B"      # Oro
    COLOR_SUCCESS = "#2ECC71"      # Verde
    COLOR_ERROR = "#E74C3C"        # Rosso
    COLOR_INFO = "#3498DB"         # Blu
    COLOR_NEUTRAL = "#95A5A6"      # Grigio
    COLOR_MILESTONE = "#F39C12"    # Arancio

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

        # Area di riempimento tra pessimistico e ottimistico
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

        # Linea "Solo versato" (senza interessi)
        fig.add_trace(go.Scatter(
            x=df_multi["Mese"],
            y=df_multi["Solo versato"],
            name="Solo versato",
            line=dict(color=UIComponents.COLOR_NEUTRAL, width=2, dash="dash"),
            hovertemplate="Solo versato: € %{y:,.0f}<extra></extra>"
        ))

        # Le 3 linee degli scenari
        for scenario in ["Pessimistico", "Realistico", "Ottimistico"]:
            fig.add_trace(go.Scatter(
                x=df_multi["Mese"],
                y=df_multi[scenario],
                name=scenario,
                line=dict(color=colori[scenario], width=3),
                hovertemplate=f"{scenario}: € %{{y:,.0f}}<extra></extra>"
            ))

        # Marker sui traguardi
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
    # TIMELINE OBIETTIVI (NUOVO)
    # ------------------------------------------------------------------
    @staticmethod
    def render_goal_timeline(timeline, obiettivo):
        """
        Renderizza una timeline visuale con tappe intermedie verso l'obiettivo
        timeline: lista di dict con chiave 'percentuale', 'obiettivo_tappa', 'mesi', 'anni'
        """
        if not timeline:
            st.info("Nessuna tappa calcolata.")
            return

        # Barra di progresso principale
        st.markdown("#### 📊 Progresso verso l'obiettivo")
        
        # Crea una barra di progresso HTML personalizzata
        progress_html = """
        <div style="background-color: #f0f0f0; border-radius: 10px; padding: 5px; margin: 20px 0;">
            <div style="background: linear-gradient(90deg, {color_start} 0%, {color_end} 100%); 
                        height: 30px; border-radius: 8px; 
                        display: flex; align-items: center; justify-content: center;
                        color: white; font-weight: bold; font-size: 14px;">
                {progress_text}
            </div>
        </div>
        """.format(
            color_start=UIComponents.COLOR_PRIMARY,
            color_end=UIComponents.COLOR_SUCCESS,
            progress_text=f"Obiettivo: € {obiettivo:,.0f}"
        )
        st.markdown(progress_html, unsafe_allow_html=True)

        # Timeline con tappe
        st.markdown("#### 🎯 Tappe intermedie")
        
        cols = st.columns(len(timeline))
        
        for i, tappa in enumerate(timeline):
            with cols[i]:
                # Icona in base alla percentuale
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

                # Card della tappa
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

        # Messaggio motivazionale
        st.markdown("---")
        st.success(
            f"💪 Mantieni la costanza! Con il tuo risparmio mensile, "
            f"raggiungerai **€ {obiettivo:,.0f}** in **{timeline[-1]['anni']:.1f} anni**."
        )