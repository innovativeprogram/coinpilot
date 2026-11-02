"""
Gestione salvataggio automatico dei dati
CoinPilot - Il tuo copilota per una finanza paziente
"""
import json
import os
import streamlit as st


class AutoStorage:
    """Gestisce il salvataggio automatico dei dati"""
    
    LAST_SESSION_FILE = "data/last_session.json"
    QUIZ_RESULTS_FILE = "data/quiz_results.json"
    HISTORY_FILE = "data/history.json"
    
    @staticmethod
    def save_last_session(data_dict):
        """Salva i dati correnti nell'ultima sessione"""
        os.makedirs("data", exist_ok=True)
        with open(AutoStorage.LAST_SESSION_FILE, 'w', encoding='utf-8') as f:
            json.dump(data_dict, f, indent=2, ensure_ascii=False)
    
    @staticmethod
    def load_last_session():
        """Carica i dati dall'ultima sessione salvata"""
        if not os.path.exists(AutoStorage.LAST_SESSION_FILE):
            return None
        
        try:
            with open(AutoStorage.LAST_SESSION_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None
    
    @staticmethod
    def clear_last_session():
        """Cancella i dati dell'ultima sessione"""
        if os.path.exists(AutoStorage.LAST_SESSION_FILE):
            os.remove(AutoStorage.LAST_SESSION_FILE)
    
    @staticmethod
    def init_auto_save():
        """Inizializza il sistema di salvataggio automatico"""
        if "auto_save_inputs" not in st.session_state:
            saved_data = AutoStorage.load_last_session()
            if saved_data:
                st.session_state["auto_save_inputs"] = saved_data
            else:
                st.session_state["auto_save_inputs"] = None
    
    @staticmethod
    def auto_save_current(inputs_dict):
        """Salva automaticamente i dati correnti"""
        st.session_state["auto_save_inputs"] = inputs_dict
        AutoStorage.save_last_session(inputs_dict)
    
    @staticmethod
    def save_quiz_results(profile_name, score):
        """Salva i risultati del quiz"""
        os.makedirs("data", exist_ok=True)
        quiz_data = {
            "profile": profile_name,
            "score": score,
            "timestamp": st.session_state.get("quiz_timestamp", None)
        }
        with open(AutoStorage.QUIZ_RESULTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(quiz_data, f, indent=2, ensure_ascii=False)
    
    @staticmethod
    def load_quiz_results():
        """Carica i risultati del quiz salvati"""
        if not os.path.exists(AutoStorage.QUIZ_RESULTS_FILE):
            return None
        
        try:
            with open(AutoStorage.QUIZ_RESULTS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None
    
    @staticmethod
    def clear_quiz_results():
        """Cancella i risultati del quiz"""
        if os.path.exists(AutoStorage.QUIZ_RESULTS_FILE):
            os.remove(AutoStorage.QUIZ_RESULTS_FILE)
    
    @staticmethod
    def save_history(history_data):
        """Salva la cronologia"""
        os.makedirs("data", exist_ok=True)
        with open(AutoStorage.HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history_data, f, indent=2, ensure_ascii=False)
    
    @staticmethod
    def load_history():
        """Carica la cronologia"""
        if not os.path.exists(AutoStorage.HISTORY_FILE):
            return {}
        
        try:
            with open(AutoStorage.HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    
    @staticmethod
    def clear_history():
        """Cancella la cronologia"""
        if os.path.exists(AutoStorage.HISTORY_FILE):
            os.remove(AutoStorage.HISTORY_FILE)