"""
Calcoli per proiezioni finanziarie e obiettivi
"""
import numpy as np
import pandas as pd


class FinancialProjections:
    """Gestisce i calcoli per proiezioni e obiettivi"""
    
    def calculate_projection(self, capitale_iniziale, risparmio_mensile, 
                            tasso_annuo, anni):
        """
        Calcola la proiezione del capitale nel tempo con interesse composto
        e versamenti mensili
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