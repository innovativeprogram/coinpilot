"""
Gestione salvataggio, caricamento e import/export dati
"""
import json
import os
from datetime import datetime
import pandas as pd


class DataManager:
    """Gestisce il salvataggio e il caricamento dei dati finanziari"""
    
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
    def save_budget(self, budget_data, filename=None):
        """Salva il budget corrente in formato JSON"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"budget_{timestamp}.json"
        
        filepath = os.path.join(self.data_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(budget_data, f, indent=2, ensure_ascii=False)
        
        return filepath
    
    def load_budget(self, filepath):
        """Carica un budget da file JSON"""
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def list_saved_budgets(self):
        """Lista tutti i budget salvati"""
        if not os.path.exists(self.data_dir):
            return []
        
        files = [f for f in os.listdir(self.data_dir) 
                if f.startswith('budget_') and f.endswith('.json')]
        return sorted(files, reverse=True)
    
    def export_to_csv(self, budget_data, filename=None):
        """Esporta il budget in formato CSV"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"budget_export_{timestamp}.csv"
        
        filepath = os.path.join(self.data_dir, filename)
        
        df = pd.DataFrame([budget_data])
        df.to_csv(filepath, index=False, encoding='utf-8')
        
        return filepath
    
    def import_from_csv(self, filepath):
        """Importa un budget da file CSV"""
        df = pd.read_csv(filepath)
        return df.iloc[0].to_dict()
    
    def delete_budget(self, filename):
        """Elimina un budget salvato"""
        filepath = os.path.join(self.data_dir, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False