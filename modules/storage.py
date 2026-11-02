"""
Gestione salvataggio automatico dei dati con ID utente univoco
Ogni utente ha i propri dati privati salvati sul server
"""
import json
import os
import uuid
import streamlit as st
import streamlit.components.v1 as components


class AutoStorage:
    """Gestisce il salvataggio automatico dei dati con separazione per utente"""
    
    LAST_SESSION_FILE = "data/last_session.json"
    USER_ID_COOKIE = "coinpilot_user_id"
    
    @staticmethod
    def get_user_id():
        """
        Restituisce un ID utente univoco.
        Se non esiste, ne genera uno nuovo e lo salva in un cookie del browser.
        """
        if "user_id" not in st.session_state:
            # Prova a leggere l'ID dal cookie (tramite JavaScript)
            js_code = f"""
            <script>
            function getCookie(name) {{
                const value = `; ${{document.cookie}}`;
                const parts = value.split(`; ${{name}}=`);
                if (parts.length === 2) return parts.pop().split(';').shift();
            }}
            const userId = getCookie("{AutoStorage.USER_ID_COOKIE}");
            if (userId) {{
                window.parent.postMessage({{type: "streamlit:setComponentValue", userId: userId}}, "*");
            }}
            </script>
            """
            components.html(js_code, height=0)
            
            # Se non c'è un ID salvato, generane uno nuovo
            st.session_state["user_id"] = str(uuid.uuid4())[:8]
            
            # Salva l'ID in un cookie (tramite JavaScript)
            js_save = f"""
            <script>
            document.cookie = "{AutoStorage.USER_ID_COOKIE}={st.session_state['user_id']}; path=/; max-age=31536000";
            </script>
            """
            components.html(js_save, height=0)
        
        return st.session_state["user_id"]
    
    @staticmethod
    def get_user_file_path(filename):
        """Restituisce il percorso del file specifico per l'utente"""
        user_id = AutoStorage.get_user_id()
        return f"data/user_{user_id}_{filename}"
    
    @staticmethod
    def save_last_session(data_dict):
        """Salva i dati correnti nell'ultima sessione (file separato per utente)"""
        os.makedirs("data", exist_ok=True)
        filepath = AutoStorage.get_user_file_path("last_session.json")
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data_dict, f, indent=2, ensure_ascii=False)
    
    @staticmethod
    def load_last_session():
        """Carica i dati dall'ultima sessione salvata (file specifico per utente)"""
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
        """Salva i risultati del quiz (file separato per utente)"""
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
        """Carica i risultati del quiz salvati"""
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