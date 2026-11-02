"""
CoinPilot - Pianificatore Finanziario Personale
Entry point principale dell'applicazione
Con schermata di benvenuto, salvataggio automatico e ottimizzazione mobile
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
from modules.storage import AutoStorage
from modules.welcome import WelcomeScreen

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

# ============================================================================
# SCHERMATA DI BENVENUTO
# ============================================================================
if WelcomeScreen.should_show_welcome():
    WelcomeScreen.render()
    st.stop()  # Ferma l'esecuzione qui, non carica il resto dell'app

# ============================================================================
# APP PRINCIPALE (dopo la welcome)
# ============================================================================

# Inizializza salvataggio automatico
AutoStorage.init_auto_save()

# Carica dati dall'ultima sessione se esistono
saved_inputs = st.session_state.get("auto_save_inputs", None)

# Renderizza header
ui.render_header()

# Messaggio informativo per mobile
st.markdown(
    """
    <div style="background-color: #FFF3CD; border-left: 4px solid #B8860B; 
                padding: 15px; border-radius: 10px; margin-bottom: 20px;">
        <strong>📱 Suggerimento:</strong> Tocca il menu <strong>☰</strong> in alto a sinistra 
        per inserire i tuoi dati finanziari.
    </div>
    """,
    unsafe_allow_html=True
)

# Renderizza sidebar e ottieni input (con valori salvati se esistono)
if saved_inputs:
    # Usa i dati salvati come valori di default
    default_entrate = saved_inputs.get("entrate", 2000.0)
    default_spese = saved_inputs.get("spese", budget_manager.default_spese)
    # FIX: il tasso è già salvato in formato decimale (es. 0.05), non dividere per 100
    default_tasso = saved_inputs.get("tasso", 0.05)
    default_anni = saved_inputs.get("anni", 10)
    default_capitale = saved_inputs.get("capitale_iniziale", 0.0)
    
    # Mostra notifica che i dati sono stati caricati
    st.info("📂 Dati caricati dall'ultima sessione")
else:
    # Usa i valori di default
    default_entrate = 2000.0
    default_spese = budget_manager.default_spese
    default_tasso = 0.05  # 5% in formato decimale
    default_anni = 10
    default_capitale = 0.0

# Sidebar con valori di default dinamici
st.sidebar.header("📊 I tuoi dati finanziari")

entrate = st.sidebar.number_input(
    "Entrate mensili nette (€)",
    min_value=0.0,
    value=float(default_entrate),
    step=50.0,
    format="%.2f"
)

st.sidebar.subheader("Spese mensili")
spese = {}
for categoria, default_val in default_spese.items():
    spese[categoria] = st.sidebar.number_input(
        f"{categoria} (€)",
        min_value=0.0,
        value=float(default_val),
        step=10.0,
        format="%.2f"
    )

st.sidebar.subheader("💼 Parametri investimento")

# Slider tasso con display del valore percentuale
tasso_percentuale = st.sidebar.slider(
    "Rendimento annuo stimato (%)",
    min_value=0.0,
    max_value=15.0,
    value=float(default_tasso * 100),
    step=0.1,
    format="%.1f%%"
)
tasso = tasso_percentuale / 100

# Slider anni con display del valore
anni = st.sidebar.slider(
    "Orizzonte temporale (anni)",
    min_value=1,
    max_value=40,
    value=int(default_anni),
    step=1,
    format="%d anni"
)

capitale_iniziale = st.sidebar.number_input(
    "Capitale iniziale (€)",
    min_value=0.0,
    value=float(default_capitale),
    step=100.0,
    format="%.2f"
)

# Costruisci il dizionario inputs
inputs = {
    "entrate": entrate,
    "spese": spese,
    "tasso": tasso,
    "anni": anni,
    "capitale_iniziale": capitale_iniziale
}

# Salva automaticamente i dati correnti
AutoStorage.auto_save_current(inputs)

# Calcola budget
budget_data = budget_manager.calculate_budget(
    inputs["entrate"], 
    inputs["spese"]
)

# Riepilogo rapido (utile su mobile per vedere i dati senza aprire la sidebar)
with st.expander("📋 Riepilogo dati correnti", expanded=False):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Entrate", f"€ {entrate:,.0f}")
        st.metric("Capitale iniziale", f"€ {capitale_iniziale:,.0f}")
    with col2:
        st.metric("Spese totali", f"€ {budget_data['totale_spese']:,.0f}")
        st.metric("Tasso annuo", f"{inputs['tasso']*100:.1f}%")
    with col3:
        st.metric("Risparmio mensile", f"€ {budget_data['risparmio_mensile']:,.0f}")
        st.metric("Orizzonte", f"{anni} anni")

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

# --- TAB 3: Proiezione ---
with tab3:
    st.subheader("🎯 Proiezione del capitale nel tempo")
    st.markdown(
        f"Con un risparmio mensile di **€ {budget_data['risparmio_mensile']:,.2f}**, "
        f"un rendimento annuo del **{inputs['tasso']*100:.1f}%** "
        f"e un capitale iniziale di **€ {inputs['capitale_iniziale']:,.2f}**, "
        f"ecco la proiezione a **{inputs['anni']} anni**:"
    )
    
    # Calcolo multi-scenario
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
    st.markdown("Definisci il tuo obiettivo e visualizza il percorso passo dopo passo.")
    
    obiettivo = st.number_input(
        "Quanto vuoi risparmiare? (€)", 
        min_value=0.0, 
        value=10000.0, 
        step=500.0,
        format="%.2f"
    )
    
    if budget_data["risparmio_mensile"] > 0 and obiettivo > inputs["capitale_iniziale"]:
        # Calcola la timeline completa con tappe intermedie
        timeline = projections.calculate_goal_timeline(
            obiettivo,
            inputs["capitale_iniziale"],
            budget_data["risparmio_mensile"],
            inputs["tasso"]
        )
        
        # Renderizza la timeline visuale
        ui.render_goal_timeline(timeline, obiettivo)
        
        # Messaggio finale con calcolo originale
        mesi, anni_obj = projections.calculate_months_to_goal(
            obiettivo,
            inputs["capitale_iniziale"],
            budget_data["risparmio_mensile"],
            inputs["tasso"]
        )
        
        st.success(
            f"🎉 Raggiungerai **€ {obiettivo:,.2f}** in circa "
            f"**{anni_obj:.1f} anni** ({mesi} mesi)."
        )
        
        # Suggerimento basato sulla pazienza finanziaria
        st.info(
            "💡 *Ricorda: la costanza batte l'intensità. "
            "Piccoli risparmi mensili, moltiplicati dal tempo e dall'interesse composto, "
            "costruiscono la vera ricchezza.*"
        )
        
    elif budget_data["risparmio_mensile"] <= 0:
        st.warning("⚠️ Con un risparmio mensile pari o inferiore a zero non puoi raggiungere l'obiettivo.")
        st.markdown(
            "Prima di tutto, cerca di creare un surplus mensile. "
            "Anche solo € 50 al mese possono fare la differenza nel lungo periodo!"
        )
    else:
        st.info("L'obiettivo è inferiore al capitale iniziale: l'hai già raggiunto! 🎉")

# --- TAB 5: Gestione Dati ---
with tab5:
    st.subheader("💾 Salva, carica ed esporta i tuoi dati")
    
    # Notifica salvataggio automatico
    st.info("💾 I tuoi dati vengono salvati automaticamente ad ogni modifica")
    
    col1, col2, col3 = st.columns(3)
    
    # SALVA MANUALE
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
                # Salva i dati caricati nel salvataggio automatico
                AutoStorage.auto_save_current({
                    "entrate": loaded_data["entrate"],
                    "spese": loaded_data["spese"],
                    "tasso": loaded_data["tasso"],
                    "anni": loaded_data["anni"],
                    "capitale_iniziale": loaded_data["capitale_iniziale"]
                })
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
                # Salva i dati importati nel salvataggio automatico
                AutoStorage.auto_save_current({
                    "entrate": imported_data.get("entrate", 2000.0),
                    "spese": {k.replace("spesa_", ""): v for k, v in imported_data.items() if k.startswith("spesa_")},
                    "tasso": imported_data.get("tasso", 0.05),
                    "anni": imported_data.get("anni", 10),
                    "capitale_iniziale": imported_data.get("capitale_iniziale", 0.0)
                })
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
    
    # RESET
    st.markdown("---")
    st.markdown("#### Reset dati")
    if st.button("🔄 Resetta all'ultima sessione", use_container_width=True):
        AutoStorage.clear_last_session()
        st.success("✅ Dati resettati! Ricarica la pagina per usare i valori di default.")
        st.rerun()
    
    # RESET WELCOME
    st.markdown("---")
    st.markdown("#### Mostra di nuovo la schermata di benvenuto")
    if st.button("👋 Rivedi welcome page", use_container_width=True):
        WelcomeScreen.reset_welcome()
        st.success("✅ Welcome page resettata! Ricarica la pagina per vederla di nuovo.")
        st.rerun()

# Renderizza footer
ui.render_footer()