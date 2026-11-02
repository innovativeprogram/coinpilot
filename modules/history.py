"""
Gestione cronologia mensile dei dati finanziari
CoinPilot - Il tuo copilota per una finanza paziente
"""
import streamlit as st
from datetime import datetime
from modules.storage import AutoStorage


class HistoryManager:
    """Gestisce lo storico mese per mese dei dati finanziari"""
    
    @staticmethod
    def load_history():
        """Carica la cronologia salvata nel browser"""
        return AutoStorage.load_history()
    
    @staticmethod
    def save_history(history_data):
        """Salva la cronologia nel browser"""
        AutoStorage.save_history(history_data)
    
    @staticmethod
    def add_month(year, month, entrate, spese, risparmio_mensile, note=""):
        """Aggiunge o aggiorna un mese nella cronologia"""
        history = HistoryManager.load_history()
        
        month_key = f"{year}-{month:02d}"
        
        history[month_key] = {
            "anno": year,
            "mese": month,
            "entrate": float(entrate),
            "spese": {k: float(v) for k, v in spese.items()},
            "totale_spese": float(sum(spese.values())),
            "risparmio_mensile": float(risparmio_mensile),
            "note": note,
            "timestamp": datetime.now().isoformat()
        }
        
        HistoryManager.save_history(history)
        return month_key
    
    @staticmethod
    def delete_month(month_key):
        """Elimina un mese dalla cronologia"""
        history = HistoryManager.load_history()
        
        if month_key in history:
            del history[month_key]
            HistoryManager.save_history(history)
            return True
        return False
    
    @staticmethod
    def get_month_data(month_key):
        """Restituisce i dati di un mese specifico"""
        history = HistoryManager.load_history()
        return history.get(month_key, None)
    
    @staticmethod
    def get_all_months_sorted():
        """Restituisce tutti i mesi ordinati cronologicamente"""
        history = HistoryManager.load_history()
        return sorted(history.keys())
    
    @staticmethod
    def clear_history():
        """Cancella tutta la cronologia"""
        AutoStorage._storage.removeItem(AutoStorage.HISTORY_KEY)