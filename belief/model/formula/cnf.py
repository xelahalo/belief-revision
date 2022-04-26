from belief.model.formula.formula_base import FormulaBase
from belief.model.operator.logical_operator import LogicalOperator
from belief.utils.constants import LogicalOperators, Notation

class CNF(FormulaBase):
    def __init__(self, clauses, isNegated = False):
        super().__init__(isNegated)
        self._clauses = clauses

    def __str__(self):
        super().__str__(self._clauses, [LogicalOperators[Notation.CONJUNCTION] for _ in range(self._clauses - 1)])

    def evaluate(self):
        self.value = True
        for clause in self._clauses:
            self.value = self.value and clause

        if self.isNegated:
            self.value = not self.value

        return self.value