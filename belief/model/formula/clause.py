from belief.model.formula.formula_base import FormulaBase
from belief.utils.constants import LogicalOperators, Notation

class Clause(FormulaBase):
    def __init__(self, literals, isNegated = False):
        super().__init__(isNegated)
        self._literals = literals

    def __str__(self):
        super().__str__(self._literals, [LogicalOperators[Notation.DISJUNCTION] for _ in range(self._literals - 1)])

    def evaluate(self):
        self.value = False
        for literal in self._literals:
            self.value = self.value or literal

        if self.isNegated:
            self.value = not self.value

        return self.value