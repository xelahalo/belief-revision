from belief.model.formula.formula_base import FormulaBase

class Literal(FormulaBase):
    def __init__(self, character, isNegated = False):
        super().__init__(isNegated)
        self._character = character

    def __str__(self):
        return self.character

    def evaluate(self):
        self.value = not self.isNegated
        return self.value