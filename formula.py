class Formula:
    def __init__(self, formula):
        self.formula = formula

    def get_propositional_symbols(self):
        return [symbol for arg in self.formula for symbol in self.get_propositional_symbols(arg)]
    
    