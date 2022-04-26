from enum import Enum

from belief.model.operator.logical_operator import LogicalOperator

class Operator(Enum):
    EXPANSION = '+'
    CONTRACTION = '-'
    REVISION = '*'
    REMAINDER = '⊥'
    RESOLVE = '|='

class Notation(Enum):
    NEGATION = '¬'
    CONJUNCTION = '∧'
    DISJUNCTION = '∨'
    IMPLICATION = '→'
    BI_IMPLICATION = '↔'

class Set(Enum):
    A = 'A'
    B = 'B'
    C = 'C'

class Symbol(Enum):
    PHI = 'ϕ'
    CHI = 'χ'
    PSI = 'ψ'

LogicalOperators = {
    Notation.NEGATION: LogicalOperator((lambda a,_: not a.evaluate()), Notation.NEGATION),
    Notation.CONJUNCTION: LogicalOperator((lambda a,b: a.evaluate() and b.evaluate()), Notation.CONJUNCTION),
    Notation.DISJUNCTION: LogicalOperator((lambda a,b: a.evaluate() or b.evaluate()), Notation.DISJUNCTION),
    Notation.IMPLICATION: LogicalOperator((lambda a,b: not(not a.evaluate() and b.evaluate())), Notation.IMPLICATION),
    Notation.BI_IMPLICATION: LogicalOperator((lambda a,b: a.evaluate() == b.evaluate()), Notation.BI_IMPLICATION),
}