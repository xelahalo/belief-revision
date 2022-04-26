from belief.model.formula.formula_base import FormulaBase


class GenericFormula(FormulaBase):
    def __init__(self, formulas, operators, isNegated = False):
        super().__init__(isNegated)
        assert len(formulas) - 1 == len(operators)
        self._formulas = formulas
        self._operators = operators

    def __str__(self):
        return super().__str__(self._formulas, self._operators)