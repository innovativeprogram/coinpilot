"""
Gestione salvataggio automatico nel localStorage del browser
CoinPilot - Il tuo copilota per una finanza paziente
"""
import streamlit as st
import streamlit.components.v1 as components
import json


class BrowserStorage:
    """Gestisce il salvataggio automatico dei dati nel localStorage del browser"""
    
    STORAGE_KEY = "coinpilot_data"
    
    @staticmethod
    def load_data():
        """
        Carica i dati salvati nel localStorage del browser.
        Restituisce un dizionario con i dati o None se non ci sono dati salvati.
        """
        # JavaScript che legge dal localStorage e passa i dati a Streamlit
        js_code = f"""
        <script>
        const data = localStorage.getItem("{BrowserStorage.STORAGE_KEY}");
        const streamlitData = window.parent.document.querySelector("#storage-data");
        if (streamlitData) {{
            streamlitData.innerText = data || "null";
        }}
        </script>
        <div id="storage-data" style="display:none;"></div>
        """
        components.html(js_code, height=0)
        
        # Recupera i dati dal componente hidden
        # Nota: Streamlit non può leggere direttamente dal JS, quindi usiamo session_state
        return st.session_state.get("loaded_data", None)
    
    @staticmethod
    def save_data(data_dict):
        """
        Salva i dati nel localStorage del browser.
        data_dict: dizionario con i dati da salvare
        """
        data_json = json.dumps(data_dict)
        
        # JavaScript che scrive nel localStorage
        js_code = f"""
        <script>
        const data = {json.dumps(data_json)};
        localStorage.setItem("{BrowserStorage.STORAGE_KEY}", data);
        </script>
        """
        components.html(js_code, height=0)
        
        # Salva anche in session_state per uso immediato
        st.session_state["loaded_data"] = data_dict
    
    @staticmethod
    def clear_data():
        """Cancella i dati salvati nel localStorage"""
        js_code = f"""
        <script>
        localStorage.removeItem("{BrowserStorage.STORAGE_KEY}");
        </script>
        """
        components.html(js_code, height=0)
        st.session_state["loaded_data"] = None
    
    @staticmethod
    def init_storage():
        """
        Inizializza il sistema di storage: carica i dati salvati all'avvio
        e li rende disponibili in session_state
        """
        if "loaded_data" not in st.session_state:
            st.session_state["loaded_data"] = None
        
        # JavaScript che legge dal localStorage al caricamento della pagina
        js_code = f"""
        <script>
        (function() {{
            const data = localStorage.getItem("{BrowserStorage.STORAGE_KEY}");
            if (data) {{
                // Invia i dati a Streamlit tramite un evento personalizzato
                window.parent.postMessage({{
                    type: "streamlit:setComponentValue",
                    data: data
                }}, "*");
            }}
        }})();
        </script>
        """
        components.html(js_code, height=0)