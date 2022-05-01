from operator import neg
from sympy import Equivalent, ordered
from sympy.logic import to_cnf, Or
from belief import Belief
from utils import apply_operator, get_conjunct_clauses, resolve

class BeliefBase:
    def __init__(self, beliefs):
        self._beliefs = beliefs

    @property
    def beliefs(self):
        return sorted(key=lambda b: b.order, reverse=True)

    def revise(self, belief):
        # ignore contradictions
        if BeliefBase([]).entails(Belief(~belief.formula, belief.order)):
            return 

        degree = self._get_degree_of_proposed_belief(belief)
        new_order = belief.order

        if BeliefBase([]).entails(belief):
            new_order = 1
        elif new_order <= degree:
            self.contract(belief)
        else:
            self.contract(Belief(~belief.formula, 0))
            self.expand(belief, False)
        
        self._add(Belief(belief.formula, new_order))

    def expand(self, belief, add=True):
        # ignore contradictions
        if BeliefBase([]).entails(Belief(~belief.formula, belief.order)):
            return 

        new_order = belief.order
        beliefs_to_reorder = []

        if BeliefBase([]).entails(belief):
            new_order = 1
        else:

            for b in self.beliefs:
                x = belief.formula
                y = b.formula
                if b.order > new_order:
                    continue

                degree = self._get_degree_of_proposed_belief(Belief(x >> y))
                if BeliefBase([]).entails(Belief(Equivalent(x, y))) or b.order <= new_order < degree:
                    beliefs_to_reorder.add((b, new_order))
                else:
                    beliefs_to_reorder.add((belief, degree))

            self._reorder_beliefs(beliefs_to_reorder)

        if add:
            self.add(belief)

    def contract(self, belief):
        beliefs_to_reorder = []
        for b in self.beliefs:

            x = belief.formula
            y = b.formula

            if b.order > belief.order:
                x_degree = self._get_degree_of_proposed_belief(belief)
                x_or_y = apply_operator(Or, [x, y])
                x_or_y_degree = self._get_degree_of_proposed_belief(Belief(x_or_y))

                if x_degree == x_or_y_degree:
                    beliefs_to_reorder.append((b, belief.order))

        self._reorder_beliefs(beliefs_to_reorder)


    def entails(self, belief):
        """
        Resolution-based entailment check
        """

        formula = to_cnf(belief.formula)

        clauses = [get_conjunct_clauses(to_cnf(belief.formula)) for belief in self.beliefs]
        clauses.append(get_conjunct_clauses(to_cnf(~formula)))
        clauses = set(clauses)

        result = set()
        while True:
            for ci in clauses:
                for cj in clauses:

                    if ci == cj:
                        continue

                    resolvents = resolve(ci, cj)
                    if False in resolvents:
                        return True
                    result = result.union(set(resolvents))

            if result.issubset(clauses):
                return False

            clauses = clauses.union(result)

    def _add(self, belief):
        self._remove_beliefs_by_formula(belief.formula)
        self.beliefs.add(belief)

    def _get_symbol_set(self):
        result_set = set()
        for belief in self.beliefs:
            for symbol in belief.formula.get_propositional_symbols():
                result_set.add(symbol)

        return result_set

    def _get_degree_of_proposed_belief(self, belief):
        if(BeliefBase([]).entails(belief)):
            return 1

        beliefs = []
        for o, b in self:
            beliefs.append(b)
            if BeliefBase(beliefs).entails(belief):
                return o
        
        return 0

    def _remove_beliefs_by_formula(self, formula):
        beliefs_to_remove = []
        for belief in self.beliefs:
            if belief.formula == formula:
                beliefs_to_remove.append(belief)

        for belief in beliefs_to_remove:
            self.beliefs.remove(belief)

    def _reorder_beliefs(self, beliefs_and_orders):
        for belief, order in beliefs_and_orders:
            self.beliefs.remove(belief)
            if order > 0:
                self.beliefs.add(Belief(belief.formula, order))


    def __iter__(self):
        result = []
        last_order = None

        for belief in self.beliefs:
            if last_order is None:
                result.append(belief)
                last_order = belief.order
                continue
            if abs(belief.order - last_order) < 0.0001:
                result.append(belief)
            else:
                yield last_order, result
                result = [belief]
                last_order = belief.order

        yield last_order, result
