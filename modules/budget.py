"""
Gestione del budget mensile: entrate, spese, calcolo risparmio
"""


class BudgetManager:
    """Gestisce il calcolo del budget mensile"""
    
    def __init__(self):
        self.default_spese = {
            "Affitto/Mutuo": 700.0,
            "Bollette": 150.0,
            "Spesa alimentare": 350.0,
            "Trasporti": 100.0,
            "Svago": 150.0,
            "Altro": 100.0
        }
    
    def calculate_budget(self, entrate, spese_dict):
        """Calcola il budget: risparmio mensile e annuo"""
        totale_spese = sum(spese_dict.values())
        risparmio_mensile = entrate - totale_spese
        risparmio_annuo = risparmio_mensile * 12
        
        return {
            "entrate": entrate,
            "spese": spese_dict,
            "totale_spese": totale_spese,
            "risparmio_mensile": risparmio_mensile,
            "risparmio_annuo": risparmio_annuo,
            "percentuale_risparmio": (risparmio_mensile / entrate * 100) if entrate > 0 else 0
        }
    
    def get_budget_status(self, risparmio_mensile, entrate):
        """Restituisce lo stato del budget (positivo, negativo, ecc.)"""
        if risparmio_mensile < 0:
            return {
                "status": "error",
                "message": "⚠️ Attenzione: le tue spese superano le entrate! Rivedi il budget.",
                "icon": "⚠️"
            }
        elif risparmio_mensile == 0:
            return {
                "status": "warning",
                "message": "⚠️ Non stai risparmiando nulla. Cerca di ridurre le spese.",
                "icon": "⚠️"
            }
        else:
            percentuale = (risparmio_mensile / entrate * 100) if entrate > 0 else 0
            return {
                "status": "success",
                "message": f"✅ Ottimo! Stai risparmiando € {risparmio_mensile:,.2f} al mese ({percentuale:.1f}% delle entrate).",
                "icon": "✅"
            }