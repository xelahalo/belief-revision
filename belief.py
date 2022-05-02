class Belief:
    def __init__(self, formula, order=1):
        self.formula = formula
        self.order = order

    def __eq__(self, other):
        return self.order == other.order and self.formula == other.formula