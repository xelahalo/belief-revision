from abc import abstractclassmethod

from belief.utils.constants import Notation

class FormulaBase:
    def __init__(self, isNegated = False):
        self._value = None
        self._isNegated = isNegated

    @property
    def isNegated(self):
        return self._isNegated
        
    @property
    def value(self):
        return self._value

    @value.setter
    def setValue(self, value):
        self._value = value

    @abstractclassmethod
    def evaluate(self):
        pass

    def __str__(self, formulas, operators):
        string = ''
        for i in range(formulas):
            string += formulas[i]
            if i < len(operators):
                string += ' ' + operators[i] + ' '

        if self.isNegated:
            string = Notation.NEGATION.value + '(' + string + ')'

        return string