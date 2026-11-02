"""
Calcoli per proiezioni finanziarie e obiettivi
Supporta scenari multipli (pessimistico, realistico, ottimistico)
"""
import numpy as np
import pandas as pd


class FinancialProjections:
    """Gestisce i calcoli per proiezioni e obiettivi"""
    
    # Scenari predefiniti con moltiplicatori del tasso
    SCENARIOS = {
        "Pessimistico": 0.5,      # metà del rendimento
        "Realistico": 1.0,        # rendimento normale
        "Ottimistico": 1.5        # 50% in più del rendimento
    }
    
    def calculate_projection(self, capitale_iniziale, risparmio_mensile, 
                            tasso_annuo, anni):
        """
        Calcola la proiezione del capitale nel tempo con interesse composto
        e versamenti mensili (scenario singolo)
        """
        mesi = np.arange(anni * 12 + 1)
        tasso_mensile = (1 + tasso_annuo) ** (1/12) - 1
        
        if risparmio_mensile > 0 and tasso_mensile > 0:
            capitale = (capitale_iniziale * (1 + tasso_mensile) ** mesi + 
                       risparmio_mensile * (((1 + tasso_mensile) ** mesi - 1) / tasso_mensile))
        elif risparmio_mensile > 0:
            capitale = capitale_iniziale + risparmio_mensile * mesi
        else:
            capitale = capitale_iniziale * (1 + tasso_mensile) ** mesi
        
        df = pd.DataFrame({
            "Mese": mesi,
            "Capitale": capitale
        })
        
        # Calcola dati annuali
        df_annuale = df[df["Mese"] % 12 == 0].copy()
        df_annuale["Anno"] = df_annuale["Mese"] // 12
        df_annuale["Versato"] = capitale_iniziale + risparmio_mensile * df_annuale["Mese"]
        df_annuale["Interessi"] = df_annuale["Capitale"] - df_annuale["Versato"]
        
        return df, df_annuale
    
    def calculate_multi_scenario(self, capitale_iniziale, risparmio_mensile, 
                                tasso_annuo, anni):
        """
        Calcola la proiezione per 3 scenari: pessimistico, realistico, ottimistico
        Restituisce un DataFrame con una colonna per ogni scenario
        """
        mesi = np.arange(anni * 12 + 1)
        
        df = pd.DataFrame({"Mese": mesi})
        
        for scenario_nome, moltiplicatore in self.SCENARIOS.items():
            tasso_scenario = tasso_annuo * moltiplicatore
            tasso_mensile = (1 + tasso_scenario) ** (1/12) - 1
            
            if risparmio_mensile > 0 and tasso_mensile > 0:
                capitale = (capitale_iniziale * (1 + tasso_mensile) ** mesi + 
                           risparmio_mensile * (((1 + tasso_mensile) ** mesi - 1) / tasso_mensile))
            elif risparmio_mensile > 0:
                capitale = capitale_iniziale + risparmio_mensile * mesi
            else:
                capitale = capitale_iniziale * (1 + tasso_mensile) ** mesi
            
            df[scenario_nome] = capitale
        
        # Colonna "Versato" (senza interessi) per confronto
        df["Solo versato"] = capitale_iniziale + risparmio_mensile * mesi
        
        return df
    
    def find_milestones(self, df, traguardi=None):
        """
        Trova i mesi in cui vengono raggiunti traguardi importanti
        traguardi: lista di valori (es. [10000, 50000, 100000])
        """
        if traguardi is None:
            # Traguardi automatici basati sul capitale finale
            max_val = df["Realistico"].iloc[-1]
            traguardi = [max_val * 0.25, max_val * 0.5, max_val * 0.75, max_val]
            traguardi = [int(t) for t in traguardi if t > 0]
        
        milestones = []
        for traguardo in traguardi:
            # Trova il primo mese in cui il capitale supera il traguardo
            superamenti = df[df["Realistico"] >= traguardo]
            if not superamenti.empty:
                mese_raggiunto = superamenti["Mese"].iloc[0]
                milestones.append({
                    "traguardo": traguardo,
                    "mese": int(mese_raggiunto),
                    "anno": int(mese_raggiunto) / 12
                })
        
        return milestones
    
    def calculate_months_to_goal(self, obiettivo, capitale_iniziale, 
                                risparmio_mensile, tasso_annuo):
        """Calcola i mesi necessari per raggiungere un obiettivo"""
        if risparmio_mensile <= 0:
            return None, None
        
        if obiettivo <= capitale_iniziale:
            return 0, 0
        
        tasso_mensile = (1 + tasso_annuo) ** (1/12) - 1
        
        if tasso_mensile > 0:
            mesi = np.log(
                (obiettivo * tasso_mensile / risparmio_mensile) + 1
            ) / np.log(1 + tasso_mensile)
        else:
            mesi = (obiettivo - capitale_iniziale) / risparmio_mensile
        
        anni = mesi / 12
        return int(np.ceil(mesi)), anni
    
    def calculate_goal_timeline(self, obiettivo, capitale_iniziale, 
                               risparmio_mensile, tasso_annuo, tappe_percentuali=None):
        """
        Calcola la timeline completa verso un obiettivo, con tappe intermedie
        tappe_percentuali: lista di percentuali (es. [0.25, 0.5, 0.75, 1.0])
        Restituisce una lista di dict con info su ogni tappa
        """
        if tappe_percentuali is None:
            tappe_percentuali = [0.25, 0.5, 0.75, 1.0]
        
        timeline = []
        
        for perc in tappe_percentuali:
            obiettivo_tappa = obiettivo * perc
            mesi, anni = self.calculate_months_to_goal(
                obiettivo_tappa,
                capitale_iniziale,
                risparmio_mensile,
                tasso_annuo
            )
            
            if mesi is not None:
                timeline.append({
                    "percentuale": perc,
                    "obiettivo_tappa": obiettivo_tappa,
                    "mesi": mesi,
                    "anni": anni,
                    "raggiunto": False  # verrà aggiornato in base al tempo attuale
                })
        
        return timeline