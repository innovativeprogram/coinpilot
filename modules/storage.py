"""
Gestione salvataggio automatico dei dati con LocalStorage (Browser)
I dati rimangono salvati nel browser dell'utente, garantendo privacy e persistenza.
"""
import json
import uuid
import streamlit as st
from streamlit_local_storage import LocalStorage


class AutoStorage:
    """Gestisce il salvataggio automatico dei dati nel browser dell'utente"""
    
    _storage = LocalStorage()
    USER_ID_KEY = "coinpilot_user_id"
    SESSION_KEY = "coinpilot_last_session"
    QUIZ_KEY = "coinpilot_quiz_results"
    HISTORY_KEY = "coinpilot_history"

    @staticmethod
    def get_user_id():
        """Restituisce un ID utente univoco salvato nel browser"""
        if "user_id" not in st.session_state:
            uid = AutoStorage._storage.getItem(AutoStorage.USER_ID_KEY)
            if not uid:
                uid = str(uuid.uuid4())[:8]
                AutoStorage._storage.setItem(AutoStorage.USER_ID_KEY, uid)
            st.session_state["user_id"] = uid
        return st.session_state["user_id"]

    @staticmethod
    def save_last_session(data_dict):
        """Salva i dati correnti nel browser"""
        AutoStorage._storage.setItem(AutoStorage.SESSION_KEY, json.dumps(data_dict))

    @staticmethod
    def load_last_session():
        """Carica i dati dal browser"""
        data = AutoStorage._storage.getItem(AutoStorage.SESSION_KEY)
        if data:
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                return None
        return None

    @staticmethod
    def clear_last_session():
        """Cancella i dati della sessione dal browser"""
        AutoStorage._storage.removeItem(AutoStorage.SESSION_KEY)

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
        """Salva i risultati del quiz nel browser"""
        quiz_data = {
            "profile": profile_name,
            "score": score,
            "timestamp": st.session_state.get("quiz_timestamp", None)
        }
        AutoStorage._storage.setItem(AutoStorage.QUIZ_KEY, json.dumps(quiz_data))

    @staticmethod
    def load_quiz_results():
        """Carica i risultati del quiz dal browser"""
        data = AutoStorage._storage.getItem(AutoStorage.QUIZ_KEY)
        if data:
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                return None
        return None

    @staticmethod
    def clear_quiz_results():
        """Cancella i risultati del quiz dal browser"""
        AutoStorage._storage.removeItem(AutoStorage.QUIZ_KEY)

    @staticmethod
    def save_history(history_data):
        """Salva la cronologia nel browser"""
        AutoStorage._storage.setItem(AutoStorage.HISTORY_KEY, json.dumps(history_data))

    @staticmethod
    def load_history():
        """Carica la cronologia dal browser"""
        data = AutoStorage._storage.getItem(AutoStorage.HISTORY_KEY)
        if data:
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                return {}
        return {}