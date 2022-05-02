from sympy.logic.boolalg import Or, And

def get_conjunct_clauses(formula):
    return separate_formula_by_operator(And, [formula])

def get_disjunct_clauses(formula):
    return separate_formula_by_operator(Or, [formula])

def apply_operator(op, formulas):
    formulas = separate_formula_by_operator(op, formulas)
    if len(formulas) == 0:
        return op.identity
    elif len(formulas) == 1:
        return formulas[0]
    else:
        return op(*formulas)

def separate_formula_by_operator(op, formulas):
    result = []

    def get_subformulas(subformulas):
        for f in subformulas:
            if hasattr(f, 'ob') and f.op == op:
                get_subformulas(f.args)
            else:
                result.append(f)

    get_subformulas(formulas)
    return result

def resolve(ci, cj):
    clauses = []
    dci = get_disjunct_clauses(ci)
    dcj = get_disjunct_clauses(cj)

    for di in dci:
        for dj in dcj:
            if di == ~dj or ~di == dj:
                res = filter_clause(di, dci) + filter_clause(dj, dcj)
                res = list(set(res))
                dnew = apply_operator(Or, res)
                clauses.append(dnew)

    return clauses

def filter_clause(clause, clauses):
    return [x for x in clauses if x != clause]