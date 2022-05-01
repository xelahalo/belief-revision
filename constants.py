""" 

    String constants for symbols and literals used throughout the app.

"""

class Notation(Enum):
    NEGATION = '¬'
    CONJUNCTION = '∧'
    DISJUNCTION = '∨'
    IMPLICATION = '→'
    BI_IMPLICATION = '↔'

# ezek valszeg nem kellenek, mert a sympy.logic.boolalgban benne vannak az operátorok
