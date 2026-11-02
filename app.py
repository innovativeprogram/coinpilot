"""
CoinPilot - Pianificatore Finanziario Personale
Entry point principale dell'applicazione
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Carica stile CSS personalizzato
def load_css(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("style.css")

# Import moduli personalizzati
from modules.budget import BudgetManager
from modules.projections import FinancialProjections
from modules.data_manager import DataManager
from modules.ui_components import UIComponents

# Configurazione pagina
st.set_page_config(
    page_title="CoinPilot — Pianificatore Finanziario",
    page_icon="🪙",
    layout="wide"
)

# Inizializza gestori
budget_manager = BudgetManager()
projections = FinancialProjections()
data_manager = DataManager()
ui = UIComponents()

# Renderizza header
ui.render_header()

# Renderizza sidebar e ottieni input
inputs = ui.render_sidebar_inputs(budget_manager)

# Calcola budget
budget_data = budget_manager.calculate_budget(
    inputs["entrate"], 
    inputs["spese"]
)

# --- TABS principali ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Riepilogo", 
    "📊 Analisi Spese", 
    "🎯 Proiezione", 
    "🏆 Obiettivi",
    "💾 Dati"
])

# --- TAB 1: Riepilogo ---
with tab1:
    ui.render_metrics(budget_data)
    
    status = budget_manager.get_budget_status(
        budget_data["risparmio_mensile"],
        budget_data["entrate"]
    )
    
    if status["status"] == "error":
        st.error(status["message"])
    elif status["status"] == "warning":
        st.warning(status["message"])
    else:
        st.success(status["message"])

# --- TAB 2: Analisi Spese ---
with tab2:
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("Distribuzione delle spese")
        ui.render_pie_chart(inputs["spese"])
    
    with col_right:
        st.subheader("Entrate vs Spese")
        ui.render_bar_chart(budget_data)

# --- TAB 3: Proiezione (AGGIORNATA CON MULTI-SCENARIO) ---
with tab3:
    st.subheader("🎯 Proiezione del capitale nel tempo")
    st.markdown(
        f"Con un risparmio mensile di **€ {budget_data['risparmio_mensile']:,.2f}**, "
        f"un rendimento annuo del **{inputs['tasso']*100:.1f}%** "
        f"e un capitale iniziale di **€ {inputs['capitale_iniziale']:,.2f}**, "
        f"ecco la proiezione a **{inputs['anni']} anni**:"
    )
    
    # Calcolo multi-scenario (nuovo!)
    df_multi = projections.calculate_multi_scenario(
        inputs["capitale_iniziale"],
        budget_data["risparmio_mensile"],
        inputs["tasso"],
        inputs["anni"]
    )
    
    # Trova traguardi importanti
    milestones = projections.find_milestones(df_multi)
    
    # Grafico interattivo con 3 scenari
    ui.render_multi_scenario_chart(df_multi, milestones)
    
    # Tabella annuale (scenario realistico)
    df_proiezione, df_annuale = projections.calculate_projection(
        inputs["capitale_iniziale"],
        budget_data["risparmio_mensile"],
        inputs["tasso"],
        inputs["anni"]
    )
    
    st.markdown("#### 📋 Dettaglio annuale")
    ui.render_annual_table(df_annuale)
    
    # Riepilogo finale
    capitale_finale = df_proiezione["Capitale"].iloc[-1]
    interessi_totali = capitale_finale - (inputs["capitale_iniziale"] + 
                                          budget_data["risparmio_mensile"] * inputs["anni"] * 12)
    
    st.info(
        f"💡 Dopo {inputs['anni']} anni avrai: **€ {capitale_finale:,.2f}** "
        f"(di cui **€ {interessi_totali:,.2f}** di interessi guadagnati)."
    )
    
    # Mostra traguardi raggiunti
    if milestones:
        st.markdown("#### 🏆 Traguardi raggiunti")
        cols = st.columns(len(milestones))
        for i, milestone in enumerate(milestones):
            with cols[i]:
                st.metric(
                    label=f"Anno {milestone['anno']:.1f}",
                    value=f"€ {milestone['traguardo']:,.0f}",
                    delta=f"Mese {milestone['mese']}"
                )

# --- TAB 4: Obiettivi ---
with tab4:
    st.subheader("🏆 Quando raggiungerai il tuo obiettivo?")
    obiettivo = st.number_input(
        "Quanto vuoi risparmiare? (€)", 
        min_value=0.0, 
        value=10000.0, 
        step=500.0
    )
    
    if budget_data["risparmio_mensile"] > 0 and obiettivo > inputs["capitale_iniziale"]:
        mesi, anni = projections.calculate_months_to_goal(
            obiettivo,
            inputs["capitale_iniziale"],
            budget_data["risparmio_mensile"],
            inputs["tasso"]
        )
        
        st.success(
            f"🎉 Raggiungerai **€ {obiettivo:,.2f}** in circa "
            f"**{anni:.1f} anni** ({mesi} mesi)."
        )
    elif budget_data["risparmio_mensile"] <= 0:
        st.warning("⚠️ Con un risparmio mensile pari o inferiore a zero non puoi raggiungere l'obiettivo.")
    else:
        st.info("L'obiettivo è inferiore al capitale iniziale: l'hai già raggiunto! 🎉")

# --- TAB 5: Gestione Dati ---
with tab5:
    st.subheader("💾 Salva, carica ed esporta i tuoi dati")
    
    col1, col2, col3 = st.columns(3)
    
    # SALVA
    with col1:
        st.markdown("#### Salva budget corrente")
        if st.button("💾 Salva ora", use_container_width=True):
            filepath = data_manager.save_budget({
                "entrate": inputs["entrate"],
                "spese": inputs["spese"],
                "tasso": inputs["tasso"],
                "anni": inputs["anni"],
                "capitale_iniziale": inputs["capitale_iniziale"],
                "timestamp": datetime.now().isoformat()
            })
            st.success(f"✅ Salvato in {filepath}")
    
    # CARICA
    with col2:
        st.markdown("#### Carica budget salvato")
        saved_files = data_manager.list_saved_budgets()
        
        if saved_files:
            selected_file = st.selectbox("Seleziona file", saved_files)
            if st.button("📂 Carica", use_container_width=True):
                loaded_data = data_manager.load_budget(
                    f"data/{selected_file}"
                )
                st.session_state.update(loaded_data)
                st.success("✅ Dati caricati! Ricarica la pagina per vederli applicati.")
                st.rerun()
        else:
            st.info("Nessun budget salvato trovato.")
    
    # ESPORTA/IMPORTA CSV
    with col3:
        st.markdown("#### Esporta/Importa CSV")
        
        # Esporta
        if st.button("📤 Esporta CSV", use_container_width=True):
            filepath = data_manager.export_to_csv({
                "entrate": inputs["entrate"],
                **{f"spesa_{k}": v for k, v in inputs["spese"].items()},
                "tasso": inputs["tasso"],
                "anni": inputs["anni"],
                "capitale_iniziale": inputs["capitale_iniziale"]
            })
            st.success(f"✅ Esportato in {filepath}")
        
        # Importa
        uploaded_file = st.file_uploader("Importa CSV", type=["csv"])
        if uploaded_file is not None:
            if st.button("📥 Importa", use_container_width=True):
                # Salva temporaneamente il file
                temp_path = f"data/temp_import.csv"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                imported_data = data_manager.import_from_csv(temp_path)
                st.session_state.update(imported_data)
                st.success("✅ Dati importati! Ricarica la pagina per vederli applicati.")
                st.rerun()
    
    # ELIMINA
    st.markdown("---")
    st.markdown("#### Elimina budget salvati")
    if saved_files:
        file_to_delete = st.selectbox(
            "Seleziona file da eliminare", 
            saved_files,
            key="delete_select"
        )
        if st.button("🗑️ Elimina", use_container_width=True):
            if data_manager.delete_budget(file_to_delete):
                st.success(f"✅ Eliminato {file_to_delete}")
                st.rerun()

# Renderizza footer
ui.render_footer()