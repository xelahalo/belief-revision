# class Expression:
#     def __init__(self, op, *args) -> None:
#         self.op = str(op)
#         self.args = args

#     # def to_variables(self):
#     #     return [x for x in self.get_subexpressions() if self.is_variable()]
    
#     # def get_subexpressions(self):
#     #     yield self
#     #     if isinstance(self, Expression):
#     #         for arg in self.args:
#     #             yield from self.get_subexpressions(arg)

#     # def is_variable(self):
#     #     return not self.args and self.op[0].islower()

#     def __call__(self, *args):
#         if self.args:
#             raise ValueError('Can only do a call for a Symbol, not an Expr')
#         else:
#             return Expression(self.op, *args)

#     def __repr__(self):
#         op = self.op
#         args = [str(arg) for arg in self.args]
#         if op.isidentifier():
#             return '{}({})'.format(op, ', '.join(args)) if args else op
#         elif len(args) == 1:
#             return op + args[0]
#         else:
#             opp = (' ' + op + ' ')
#             return '(' + opp.join(args) + ')'