"""
Gestione salvataggio dati con separazione per utente tramite cookie
Ogni utente ha un ID univoco salvato in un cookie del browser
"""
import json
import os
import uuid
import streamlit as st
from streamlit_cookies_controller import CookieController


class AutoStorage:
    """Gestisce il salvataggio automatico dei dati con separazione per utente"""
    
    controller = CookieController()
    
    @staticmethod
    def get_user_id():
        """Restituisce un ID utente univoco salvato in un cookie"""
        if "user_id" not in st.session_state:
            user_id = AutoStorage.controller.get('coinpilot_user_id')
            if not user_id:
                user_id = str(uuid.uuid4())[:12]
                AutoStorage.controller.set('coinpilot_user_id', user_id)
            st.session_state["user_id"] = user_id
        return st.session_state["user_id"]
    
    @staticmethod
    def get_user_file_path(filename):
        """Restituisce il percorso del file specifico per l'utente"""
        user_id = AutoStorage.get_user_id()
        return f"data/user_{user_id}_{filename}"
    
    @staticmethod
    def save_last_session(data_dict):
        """Salva i dati correnti nel file specifico per l'utente"""
        os.makedirs("data", exist_ok=True)
        filepath = AutoStorage.get_user_file_path("last_session.json")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data_dict, f, indent=2, ensure_ascii=False)
    
    @staticmethod
    def load_last_session():
        """Carica i dati dal file specifico per l'utente"""
        filepath = AutoStorage.get_user_file_path("last_session.json")
        
        if not os.path.exists(filepath):
            return None
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None
    
    @staticmethod
    def clear_last_session():
        """Cancella i dati dell'ultima sessione"""
        filepath = AutoStorage.get_user_file_path("last_session.json")
        if os.path.exists(filepath):
            os.remove(filepath)
    
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
        """Salva i risultati del quiz nel file specifico per l'utente"""
        os.makedirs("data", exist_ok=True)
        filepath = AutoStorage.get_user_file_path("quiz_results.json")
        
        quiz_data = {
            "profile": profile_name,
            "score": score,
            "timestamp": st.session_state.get("quiz_timestamp", None)
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(quiz_data, f, indent=2, ensure_ascii=False)
    
    @staticmethod
    def load_quiz_results():
        """Carica i risultati del quiz dal file specifico per l'utente"""
        filepath = AutoStorage.get_user_file_path("quiz_results.json")
        
        if not os.path.exists(filepath):
            return None
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None
    
    @staticmethod
    def clear_quiz_results():
        """Cancella i risultati del quiz"""
        filepath = AutoStorage.get_user_file_path("quiz_results.json")
        if os.path.exists(filepath):
            os.remove(filepath)
    
    @staticmethod
    def save_history(history_data):
        """Salva la cronologia nel file specifico per l'utente"""
        os.makedirs("data", exist_ok=True)
        filepath = AutoStorage.get_user_file_path("history.json")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(history_data, f, indent=2, ensure_ascii=False)
    
    @staticmethod
    def load_history():
        """Carica la cronologia dal file specifico per l'utente"""
        filepath = AutoStorage.get_user_file_path("history.json")
        
        if not os.path.exists(filepath):
            return {}
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    
    @staticmethod
    def clear_history():
        """Cancella la cronologia"""
        filepath = AutoStorage.get_user_file_path("history.json")
        if os.path.exists(filepath):
            os.remove(filepath)