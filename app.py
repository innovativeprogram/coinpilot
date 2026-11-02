"""
CoinPilot - Pianificatore Finanziario Personale
Con Dark Mode, FIRE Calculator, Inflation Simulator, Export PDF, Quiz facoltativo, Glossario e Cronologia mensile
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from fpdf import FPDF

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
from modules.quiz import FinancialQuiz
from modules.history import HistoryManager

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
# 1. SCHERMATA DI BENVENUTO
# ============================================================================
if WelcomeScreen.should_show_welcome():
    WelcomeScreen.render()
    st.stop()

# ============================================================================
# 2. APP PRINCIPALE (il quiz è ora facoltativo, accessibile dalla sidebar)
# ============================================================================

# Applica Dark Mode se attiva
is_dark = ui.render_dark_mode_toggle()
ui.apply_dark_mode(is_dark)

AutoStorage.init_auto_save()
saved_inputs = st.session_state.get("auto_save_inputs", None)

ui.render_header()

# Mostra il profilo dell'investitore se il quiz è stato fatto
if st.session_state.get("investor_profile"):
    st.markdown(
        f"""
        <div style="background-color: #E8F5E9; border-left: 4px solid #2ECC71; 
                    padding: 15px; border-radius: 10px; margin-bottom: 20px;">
            <strong>🦉 Il tuo profilo:</strong> {st.session_state["investor_profile"]}
        </div>
        """,
        unsafe_allow_html=True
    )

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

if saved_inputs:
    default_entrate = saved_inputs.get("entrate", 2000.0)
    default_spese = saved_inputs.get("spese", budget_manager.default_spese)
    default_tasso = saved_inputs.get("tasso", 0.05)
    default_anni = saved_inputs.get("anni", 10)
    default_capitale = saved_inputs.get("capitale_iniziale", 0.0)
    st.info("📂 Dati caricati dall'ultima sessione")
else:
    default_entrate = 2000.0
    default_spese = budget_manager.default_spese
    default_tasso = 0.05
    default_anni = 10
    default_capitale = 0.0

st.sidebar.header("📊 I tuoi dati finanziari")

entrate = st.sidebar.number_input("Entrate mensili nette (€)", min_value=0.0, value=float(default_entrate), step=50.0, format="%.2f")

st.sidebar.subheader("Spese mensili")
spese = {}
for categoria, default_val in default_spese.items():
    spese[categoria] = st.sidebar.number_input(f"{categoria} (€)", min_value=0.0, value=float(default_val), step=10.0, format="%.2f")

st.sidebar.subheader("💼 Parametri investimento")

tasso_percentuale = st.sidebar.number_input(
    "Rendimento annuo stimato (%)", min_value=0.0, max_value=15.0, value=float(default_tasso * 100), step=0.1, format="%.1f", help="Inserisci il rendimento annuo atteso (es. 5.0 per 5%)"
)
tasso = tasso_percentuale / 100

anni = st.sidebar.number_input(
    "Orizzonte temporale (anni)", min_value=1, max_value=40, value=int(default_anni), step=1, format="%d", help="Per quanti anni vuoi investire?"
)

capitale_iniziale = st.sidebar.number_input("Capitale iniziale (€)", min_value=0.0, value=float(default_capitale), step=100.0, format="%.2f")

inputs = {
    "entrate": entrate,
    "spese": spese,
    "tasso": tasso,
    "anni": anni,
    "capitale_iniziale": capitale_iniziale
}

AutoStorage.auto_save_current(inputs)
budget_data = budget_manager.calculate_budget(inputs["entrate"], inputs["spese"])

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

# ============================================================================
# MENU LATERALE: OBIETTIVI MULTIPLI, GLOSSARIO, QUIZ E CRONOLOGIA
# ============================================================================
st.sidebar.markdown("---")

# OBIETTIVI MULTIPLI
with st.sidebar.expander("🎯 Obiettivi Multipli"):
    if "multi_goals" not in st.session_state:
        st.session_state["multi_goals"] = []
    
    with st.form("add_goal_form"):
        goal_name = st.text_input("Nome obiettivo (es. Casa, Auto, Viaggio)")
        goal_amount = st.number_input("Importo target (€)", min_value=100.0, step=100.0)
        submitted = st.form_submit_button("➕ Aggiungi Obiettivo")
        
        if submitted and goal_name.strip():
            st.session_state["multi_goals"].append({"nome": goal_name.strip(), "importo": float(goal_amount)})
            st.success(f"✅ '{goal_name}' aggiunto!")
            st.rerun()
    
    if st.session_state["multi_goals"]:
        st.markdown("**I tuoi obiettivi:**")
        for idx, goal in enumerate(st.session_state["multi_goals"]):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"• **{goal['nome']}**: € {goal['importo']:,.0f}")
            with col2:
                if st.button("🗑️", key=f"del_goal_{idx}"):
                    st.session_state["multi_goals"].pop(idx)
                    st.rerun()
    else:
        st.info("Nessun obiettivo aggiunto. Inizia a pianificare!")

# GLOSSARIO FINANZIARIO
with st.sidebar.expander("📚 Glossario Finanziario"):
    st.markdown("""
    **💰 Interesse Composto**  
    Guadagnare interessi non solo sul capitale iniziale, ma anche sugli interessi accumulati nel tempo.

    **📈 PAC (Piano di Accumulo)**  
    Investire una cifra fissa a intervalli regolari, riducendo l'impatto della volatilità.

    **🏦 ETF (Exchange Traded Fund)**  
    Un fondo che replica un indice di mercato, offrendo diversificazione a costi bassissimi.

    **🔥 FIRE**  
    *Financial Independence, Retire Early*. Accumulare capitale sufficiente a vivere di rendita.

    **📉 Inflazione**  
    L'aumento generale dei prezzi, che riduce il potere d'acquisto del denaro.
    """)

# QUIZ FACOLTATIVO
with st.sidebar.expander("🧠 Quiz della Pazienza"):
    if st.session_state.get("investor_profile"):
        st.markdown(f"**Il tuo profilo attuale:**")
        st.markdown(f"### {st.session_state['investor_profile']}")
        st.markdown(f"**Punteggio:** {st.session_state.get('quiz_score', 0)}/15")
        st.markdown("---")
        if st.button("🔄 Rifai il Quiz", use_container_width=True):
            FinancialQuiz.reset_quiz()
            st.success("Quiz resettato! Ricarica la pagina per rifarlo.")
            st.rerun()
    else:
        st.info("Il quiz è facoltativo. Fallo per scoprire il tuo profilo!")
        if st.button("🧠 Inizia il Quiz", use_container_width=True):
            FinancialQuiz.render()
            st.stop()

# ============================================================================
# TABS PRINCIPALI
# ============================================================================
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
    "📈 Riepilogo", 
    "📊 Analisi Spese", 
    "🎯 Proiezione", 
    "🏆 Obiettivi",
    "🔥 FIRE",
    "📉 Inflazione",
    "📅 Cronologia",
    "💾 Dati",
    "📖 Il Libro"
])

with tab1:
    ui.render_metrics(budget_data)
    status = budget_manager.get_budget_status(budget_data["risparmio_mensile"], budget_data["entrate"])
    if status["status"] == "error":
        st.error(status["message"])
    elif status["status"] == "warning":
        st.warning(status["message"])
    else:
        st.success(status["message"])

with tab2:
    col_left, col_right = st.columns(2)
    with col_left:
        st.subheader("Distribuzione delle spese")
        ui.render_pie_chart(inputs["spese"])
    with col_right:
        st.subheader("Entrate vs Spese")
        ui.render_bar_chart(budget_data)

with tab3:
    st.subheader("🎯 Proiezione del capitale nel tempo")
    st.markdown(f"Con un risparmio mensile di **€ {budget_data['risparmio_mensile']:,.2f}**, un rendimento annuo del **{inputs['tasso']*100:.1f}%** e un capitale iniziale di **€ {inputs['capitale_iniziale']:,.2f}**, ecco la proiezione a **{inputs['anni']} anni**:")
    
    df_multi = projections.calculate_multi_scenario(inputs["capitale_iniziale"], budget_data["risparmio_mensile"], inputs["tasso"], inputs["anni"])
    milestones = projections.find_milestones(df_multi)
    ui.render_multi_scenario_chart(df_multi, milestones)
    
    df_proiezione, df_annuale = projections.calculate_projection(inputs["capitale_iniziale"], budget_data["risparmio_mensile"], inputs["tasso"], inputs["anni"])
    st.markdown("#### 📋 Dettaglio annuale")
    ui.render_annual_table(df_annuale)
    
    capitale_finale = df_proiezione["Capitale"].iloc[-1]
    interessi_totali = capitale_finale - (inputs["capitale_iniziale"] + budget_data["risparmio_mensile"] * inputs["anni"] * 12)
    st.info(f"💡 Dopo {inputs['anni']} anni avrai: **€ {capitale_finale:,.2f}** (di cui **€ {interessi_totali:,.2f}** di interessi guadagnati).")
    
    if milestones:
        st.markdown("#### 🏆 Traguardi raggiunti")
        cols = st.columns(len(milestones))
        for i, milestone in enumerate(milestones):
            with cols[i]:
                st.metric(label=f"Anno {milestone['anno']:.1f}", value=f"€ {milestone['traguardo']:,.0f}", delta=f"Mese {milestone['mese']}")

with tab4:
    st.subheader("🏆 Quando raggiungerai il tuo obiettivo?")
    st.markdown("Definisci il tuo obiettivo e visualizza il percorso passo dopo passo.")
    obiettivo = st.number_input("Quanto vuoi risparmiare? (€)", min_value=0.0, value=10000.0, step=500.0, format="%.2f")
    
    if budget_data["risparmio_mensile"] > 0 and obiettivo > inputs["capitale_iniziale"]:
        timeline = projections.calculate_goal_timeline(obiettivo, inputs["capitale_iniziale"], budget_data["risparmio_mensile"], inputs["tasso"])
        ui.render_goal_timeline(timeline, obiettivo)
        mesi, anni_obj = projections.calculate_months_to_goal(obiettivo, inputs["capitale_iniziale"], budget_data["risparmio_mensile"], inputs["tasso"])
        st.success(f"🎉 Raggiungerai **€ {obiettivo:,.2f}** in circa **{anni_obj:.1f} anni** ({mesi} mesi).")
        st.info("💡 *Ricorda: la costanza batte l'intensità. Piccoli risparmi mensili, moltiplicati dal tempo e dall'interesse composto, costruiscono la vera ricchezza.*")
    elif budget_data["risparmio_mensile"] <= 0:
        st.warning("⚠️ Con un risparmio mensile pari o inferiore a zero non puoi raggiungere l'obiettivo.")
        st.markdown("Prima di tutto, cerca di creare un surplus mensile. Anche solo € 50 al mese possono fare la differenza nel lungo periodo!")
    else:
        st.info("L'obiettivo è inferiore al capitale iniziale: l'hai già raggiunto! 🎉")

with tab5:
    spese_annuali = budget_data["totale_spese"] * 12
    risparmio_annuo = budget_data["risparmio_mensile"] * 12
    
    ui.render_fire_calculator(
        spese_annuali=spese_annuali,
        capitale_attuale=inputs["capitale_iniziale"],
        risparmio_annuo=risparmio_annuo,
        tasso_annuo=inputs["tasso"]
    )

with tab6:
    inflazione_annua = st.number_input(
        "Tasso di inflazione annuo stimato (%)",
        min_value=0.0,
        max_value=10.0,
        value=2.5,
        step=0.1,
        format="%.1f",
        help="L'inflazione media in Europa è circa 2-3% annuo"
    ) / 100
    
    ui.render_inflation_simulator(
        capitale_iniziale=inputs["capitale_iniziale"],
        risparmio_mensile=budget_data["risparmio_mensile"],
        tasso_annuo=inputs["tasso"],
        anni=inputs["anni"],
        inflazione_annua=inflazione_annua
    )

# ============================================================================
# TAB 7: CRONOLOGIA MENSILE (NUOVA)
# ============================================================================
with tab7:
    st.subheader("📅 Cronologia Mensile")
    st.markdown("Registra e monitora i tuoi dati finanziari mese per mese.")
    st.markdown("---")
    
    # Form per aggiungere/modificare un mese
    col_form1, col_form2 = st.columns(2)
    
    with col_form1:
        st.markdown("#### ➕ Aggiungi/Modifica Mese")
        with st.form("add_month_form"):
            anno = st.number_input("Anno", min_value=2020, max_value=2100, value=datetime.now().year, step=1)
            mese = st.number_input("Mese", min_value=1, max_value=12, value=datetime.now().month, step=1)
            
            entrate_mese = st.number_input("Entrate del mese (€)", min_value=0.0, value=float(entrate), step=50.0, format="%.2f")
            
            st.markdown("**Spese del mese:**")
            spese_mese = {}
            for categoria in budget_manager.default_spese.keys():
                spese_mese[categoria] = st.number_input(
                    f"{categoria} (€)", 
                    min_value=0.0, 
                    value=float(spese.get(categoria, 0.0)), 
                    step=10.0, 
                    format="%.2f"
                )
            
            risparmio_mese = st.number_input("Risparmio mensile (€)", min_value=0.0, value=float(budget_data["risparmio_mensile"]), step=50.0, format="%.2f")
            note_mese = st.text_input("Note (opzionale)", placeholder="Es. Mese con spese straordinarie")
            
            submitted = st.form_submit_button("💾 Salva Mese", use_container_width=True, type="primary")
            
            if submitted:
                month_key = HistoryManager.add_month(
                    anno, mese, entrate_mese, spese_mese, risparmio_mese, note_mese
                )
                st.success(f"✅ Mese {mese}/{anno} salvato con successo!")
                st.rerun()
    
    with col_form2:
        st.markdown("#### 📊 Andamento nel Tempo")
        
        history = HistoryManager.load_history()
        
        if history:
            months_sorted = HistoryManager.get_all_months_sorted()
            
            # Prepara dati per il grafico
            df_history = pd.DataFrame([history[m] for m in months_sorted])
            df_history["Periodo"] = df_history.apply(lambda x: f"{x['mese']:02d}/{x['anno']}", axis=1)
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=df_history["Periodo"],
                y=df_history["entrate"],
                name="Entrate",
                line=dict(color="#2ECC71", width=3),
                mode="lines+markers"
            ))
            
            fig.add_trace(go.Scatter(
                x=df_history["Periodo"],
                y=df_history["totale_spese"],
                name="Spese",
                line=dict(color="#E74C3C", width=3),
                mode="lines+markers"
            ))
            
            fig.add_trace(go.Scatter(
                x=df_history["Periodo"],
                y=df_history["risparmio_mensile"],
                name="Risparmio",
                line=dict(color="#3498DB", width=3),
                mode="lines+markers"
            ))
            
            fig.update_layout(
                title="Andamento Mensile",
                xaxis_title="Periodo",
                yaxis_title="Importo (€)",
                hovermode="x unified",
                plot_bgcolor="white",
                paper_bgcolor="white",
                yaxis_tickformat="€,.0f",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Statistiche
            st.markdown("#### 📈 Statistiche")
            col_stat1, col_stat2, col_stat3 = st.columns(3)
            
            with col_stat1:
                media_entrate = df_history["entrate"].mean()
                st.metric("Media Entrate", f"€ {media_entrate:,.0f}")
            
            with col_stat2:
                media_spese = df_history["totale_spese"].mean()
                st.metric("Media Spese", f"€ {media_spese:,.0f}")
            
            with col_stat3:
                media_risparmio = df_history["risparmio_mensile"].mean()
                st.metric("Media Risparmio", f"€ {media_risparmio:,.0f}")
        else:
            st.info("Nessun dato storico. Aggiungi il primo mese usando il form a sinistra!")
    
    # Lista mesi salvati
    st.markdown("---")
    st.markdown("#### 📋 Mesi Registrati")
    
    history = HistoryManager.load_history()
    
    if history:
        months_sorted = HistoryManager.get_all_months_sorted()
        
        for month_key in reversed(months_sorted):
            month_data = history[month_key]
            
            with st.expander(f"📅 {month_data['mese']:02d}/{month_data['anno']} - Entrate: € {month_data['entrate']:,.0f} | Risparmio: € {month_data['risparmio_mensile']:,.0f}"):
                col_info1, col_info2, col_info3 = st.columns(3)
                
                with col_info1:
                    st.markdown(f"**Entrate:** € {month_data['entrate']:,.2f}")
                    st.markdown(f"**Risparmio:** € {month_data['risparmio_mensile']:,.2f}")
                
                with col_info2:
                    st.markdown("**Spese:**")
                    for categoria, importo in month_data['spese'].items():
                        st.markdown(f"  • {categoria}: € {importo:,.2f}")
                    st.markdown(f"**Totale Spese:** € {month_data['totale_spese']:,.2f}")
                
                with col_info3:
                    if month_data.get('note'):
                        st.markdown(f"**Note:** {month_data['note']}")
                    st.markdown(f"**Salvato il:** {month_data['timestamp'][:10]}")
                
                if st.button(f"🗑️ Elimina {month_key}", key=f"del_{month_key}"):
                    HistoryManager.delete_month(month_key)
                    st.success(f"✅ Mese {month_key} eliminato!")
                    st.rerun()
    else:
        st.info("Nessun mese registrato. Inizia ad aggiungere i tuoi dati!")

with tab8:
    st.subheader("💾 Salva, carica ed esporta i tuoi dati")
    st.info("💾 I tuoi dati vengono salvati automaticamente ad ogni modifica")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### Salva budget corrente")
        if st.button("💾 Salva ora", use_container_width=True):
            filepath = data_manager.save_budget({"entrate": inputs["entrate"], "spese": inputs["spese"], "tasso": inputs["tasso"], "anni": inputs["anni"], "capitale_iniziale": inputs["capitale_iniziale"], "timestamp": datetime.now().isoformat()})
            st.success(f"✅ Salvato in {filepath}")
    
    with col2:
        st.markdown("#### Carica budget salvato")
        saved_files = data_manager.list_saved_budgets()
        if saved_files:
            selected_file = st.selectbox("Seleziona file", saved_files)
            if st.button("📂 Carica", use_container_width=True):
                loaded_data = data_manager.load_budget(f"data/{selected_file}")
                AutoStorage.auto_save_current({"entrate": loaded_data["entrate"], "spese": loaded_data["spese"], "tasso": loaded_data["tasso"], "anni": loaded_data["anni"], "capitale_iniziale": loaded_data["capitale_iniziale"]})
                st.success("✅ Dati caricati! Ricarica la pagina per vederli applicati.")
                st.rerun()
        else:
            st.info("Nessun budget salvato trovato.")
    
    with col3:
        st.markdown("#### Esporta/Importa CSV")
        if st.button("📤 Esporta CSV", use_container_width=True):
            filepath = data_manager.export_to_csv({"entrate": inputs["entrate"], **{f"spesa_{k}": v for k, v in inputs["spese"].items()}, "tasso": inputs["tasso"], "anni": inputs["anni"], "capitale_iniziale": inputs["capitale_iniziale"]})
            st.success(f"✅ Esportato in {filepath}")
        
        uploaded_file = st.file_uploader("Importa CSV", type=["csv"])
        if uploaded_file is not None:
            if st.button("📥 Importa", use_container_width=True):
                temp_path = f"data/temp_import.csv"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                imported_data = data_manager.import_from_csv(temp_path)
                AutoStorage.auto_save_current({"entrate": imported_data.get("entrate", 2000.0), "spese": {k.replace("spesa_", ""): v for k, v in imported_data.items() if k.startswith("spesa_")}, "tasso": imported_data.get("tasso", 0.05), "anni": imported_data.get("anni", 10), "capitale_iniziale": imported_data.get("capitale_iniziale", 0.0)})
                st.success("✅ Dati importati! Ricarica la pagina per vederli applicati.")
                st.rerun()
    
    st.markdown("---")
    
    st.markdown("#### 📄 Esporta Report PDF")
    st.markdown("Scarica un report completo del tuo piano finanziario")
    
    if st.button("📄 Genera Report PDF", use_container_width=True, type="primary"):
        try:
            pdf = FPDF()
            pdf.add_page()
            
            pdf.set_font("Helvetica", "B", 24)
            pdf.set_text_color(184, 134, 11)
            pdf.cell(0, 15, "CoinPilot - Report Finanziario", ln=True, align="C")
            pdf.ln(5)
            
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(100, 100, 100)
            pdf.cell(0, 8, f"Generato il {datetime.now().strftime('%d/%m/%Y alle %H:%M')}", ln=True, align="C")
            pdf.ln(10)
            
            pdf.set_font("Helvetica", "B", 16)
            pdf.set_text_color(44, 62, 80)
            pdf.cell(0, 12, "1. RIEPILOGO FINANZIARIO", ln=True)
            pdf.ln(3)
            
            pdf.set_font("Helvetica", "", 11)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(90, 8, "Entrate mensili:")
            pdf.cell(0, 8, f"EUR {entrate:,.2f}", ln=True)
            pdf.cell(90, 8, "Spese mensili totali:")
            pdf.cell(0, 8, f"EUR {budget_data['totale_spese']:,.2f}", ln=True)
            pdf.cell(90, 8, "Risparmio mensile:")
            pdf.cell(0, 8, f"EUR {budget_data['risparmio_mensile']:,.2f}", ln=True)
            pdf.cell(90, 8, "Risparmio annuo:")
            pdf.cell(0, 8, f"EUR {budget_data['risparmio_annuo']:,.2f}", ln=True)
            pdf.cell(90, 8, "Capitale iniziale:")
            pdf.cell(0, 8, f"EUR {inputs['capitale_iniziale']:,.2f}", ln=True)
            pdf.ln(8)
            
            pdf.set_font("Helvetica", "B", 16)
            pdf.cell(0, 12, "2. PROIEZIONE A " + str(inputs["anni"]) + " ANNI", ln=True)
            pdf.ln(3)
            
            pdf.set_font("Helvetica", "", 11)
            pdf.cell(90, 8, "Rendimento annuo stimato:")
            pdf.cell(0, 8, f"{inputs['tasso']*100:.1f}%", ln=True)
            pdf.cell(90, 8, "Capitale finale stimato:")
            pdf.cell(0, 8, f"EUR {capitale_finale:,.2f}", ln=True)
            pdf.cell(90, 8, "Interessi guadagnati:")
            pdf.cell(0, 8, f"EUR {interessi_totali:,.2f}", ln=True)
            pdf.ln(8)
            
            spese_annuali_pdf = budget_data["totale_spese"] * 12
            capitale_fire = spese_annuali_pdf / 0.04
            
            pdf.set_font("Helvetica", "B", 16)
            pdf.cell(0, 12, "3. ANALISI FIRE (Indipendenza Finanziaria)", ln=True)
            pdf.ln(3)
            
            pdf.set_font("Helvetica", "", 11)
            pdf.cell(90, 8, "Numero FIRE (capitale necessario):")
            pdf.cell(0, 8, f"EUR {capitale_fire:,.2f}", ln=True)
            pdf.cell(90, 8, "Spese annuali:")
            pdf.cell(0, 8, f"EUR {spese_annuali_pdf:,.2f}", ln=True)
            pdf.ln(8)
            
            pdf.ln(10)
            pdf.set_font("Helvetica", "I", 9)
            pdf.set_text_color(150, 150, 150)
            pdf.cell(0, 8, "Report generato da CoinPilot - Il tuo copilota per una finanza paziente", ln=True, align="C")
            pdf.cell(0, 8, "Ispirato a 'L'Arte della Pazienza Finanziaria' di Canio Tedesco", ln=True, align="C")
            
            pdf_path = "data/coinpilot_report.pdf"
            pdf.output(pdf_path)
            
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="⬇️ Scarica il tuo Report PDF",
                    data=f,
                    file_name="CoinPilot_Report.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            
            st.success("✅ Report PDF generato con successo!")
            
        except Exception as e:
            st.error(f"Errore nella generazione del PDF: {str(e)}")
    
    st.markdown("---")
    st.markdown("#### Elimina budget salvati")
    if saved_files:
        file_to_delete = st.selectbox("Seleziona file da eliminare", saved_files, key="delete_select")
        if st.button("🗑️ Elimina", use_container_width=True):
            if data_manager.delete_budget(file_to_delete):
                st.success(f"✅ Eliminato {file_to_delete}")
                st.rerun()
    
    st.markdown("---")
    st.markdown("#### Reset dati")
    if st.button("🔄 Resetta all'ultima sessione", use_container_width=True):
        AutoStorage.clear_last_session()
        st.success("✅ Dati resettati! Ricarica la pagina per usare i valori di default.")
        st.rerun()
    
    st.markdown("---")
    st.markdown("#### Mostra di nuovo la schermata di benvenuto")
    if st.button("👋 Rivedi welcome page", use_container_width=True):
        WelcomeScreen.reset_welcome()
        st.success("✅ Welcome page resettata! Ricarica la pagina per vederla di nuovo.")
        st.rerun()

with tab9:
    ui.render_book_presentation()

ui.render_footer()