"""
Gestione salvataggio automatico dei dati
CoinPilot - Il tuo copilota per una finanza paziente
"""
import json
import os
import streamlit as st


class AutoStorage:
    """Gestisce il salvataggio automatico dei dati in un file locale"""
    
    LAST_SESSION_FILE = "data/last_session.json"
    
    @staticmethod
    def save_last_session(data_dict):
        """
        Salva i dati correnti nell'ultima sessione
        data_dict: dizionario con i dati da salvare
        """
        # Assicurati che la directory esista
        os.makedirs("data", exist_ok=True)
        
        with open(AutoStorage.LAST_SESSION_FILE, 'w', encoding='utf-8') as f:
            json.dump(data_dict, f, indent=2, ensure_ascii=False)
    
    @staticmethod
    def load_last_session():
        """
        Carica i dati dall'ultima sessione salvata
        Restituisce un dizionario con i dati o None se non ci sono dati salvati
        """
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
    def init_auto_save(inputs_key="auto_save_inputs"):
        """
        Inizializza il sistema di salvataggio automatico
        Carica i dati dall'ultima sessione se esistono
        """
        if inputs_key not in st.session_state:
            # Prova a caricare dall'ultima sessione
            saved_data = AutoStorage.load_last_session()
            if saved_data:
                st.session_state[inputs_key] = saved_data
            else:
                st.session_state[inputs_key] = None
    
    @staticmethod
    def auto_save_current(inputs_dict, inputs_key="auto_save_inputs"):
        """
        Salva automaticamente i dati correnti
        inputs_dict: dizionario con i dati correnti
        """
        st.session_state[inputs_key] = inputs_dict
        AutoStorage.save_last_session(inputs_dict)