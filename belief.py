class Belief:
    def __init__(self, formula, original_form, order=1):
        self.formula = formula
        self.original_form = original_form
        self.order = order

    def __eq__(self, other):
        return self.order == other.order and self.formula == other.formula