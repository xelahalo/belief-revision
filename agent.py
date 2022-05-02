from belief import Belief
from belief_base import BeliefBase
from sympy.parsing.sympy_parser import parse_expr


def print_initial_info():
    print('Welcome to our belief revision agent!')
    print('With the help of our agent you are able to construct a belief base by applying three operations: ')
    print('1. Expension')
    print('2. Contraction')
    print('3. Revision')
    print('It is also possible to check if your new belief is entailed by the belief base by calling our agents'
          'resolution based entailment check algorithm.')
    print('To write your formula for your belief the following syntax is accepted: ')
    print_syntax_info()


def print_syntax_info():
    print('----------------------------')
    print('NEGATION                  ~')
    print('CONJUNCTIONS/AND          &')
    print('DISJUNCTION/OR            |')
    print('IMPLICATION              =>')
    print('BICONDITIONAL           <=>')
    print('----------------------------')
    print('Make sure to sanity check the parentheses in your formula!!!')


class Agent:
    def __init__(self):
        self.belief_base = BeliefBase()

    def start(self):
        print_initial_info()

    def belief_process_loop(self, choice):
        missing_belief = True
        while missing_belief:
            try:
                parseable = input("Enter your belief: ")
                parseable = parseable.replace(" ", "").upper()
                valid_ops = ['(', ')', '&', '|', '=', '<', '>', '~']
                brace_cnt = 0
                final_replacements = {}
                for i in range(len(parseable)):
                    if not parseable[i].isalpha() and not any(op in parseable[i] for op in valid_ops):
                        raise Exception(parseable[i], 'is not a valid character', 'Position: ', i)
                    if parseable[i] == '(':
                        if not parseable[i + 1] or not parseable[i + 1].isalpha():
                            raise Exception(parseable[i], 'must be followed by a literal', 'Position: ', i)
                        brace_cnt += 1
                    elif parseable[i] == ')':
                        if i == 0 or not parseable[i - 1].isalpha():
                            raise Exception(parseable[i], 'must be preceded by a literal', 'Position: ', i)
                        brace_cnt -= 1
                    elif parseable[i] == '<':
                        if not parseable[i + 1] or parseable[i + 1] != '=':
                            raise Exception(parseable[i], ' must be followed by =', 'Position: ', i)
                        if not parseable[i - 1] or (not parseable[i - 1].isalpha() and parseable[i - 1] != ')'):
                            raise Exception(parseable[i], ' must be preceded by a proper statement', 'Position: ', i)
                    elif parseable[i] == '>':
                        if not parseable[i + 1] or (not parseable[i + 1].isalpha() and parseable[i + 1] != '('):
                            raise Exception(parseable[i], ' must be followed by a proper statement', 'Position: ', i)
                        if not parseable[i - 1] or parseable[i - 1] != '=':
                            raise Exception(parseable[i], ' must be preceded by =', 'Position: ', i)
                    elif parseable[i] == '=':
                        if i == 0:
                            raise Exception(parseable[i], 'must be preceded by a literal or a < sign', 'Position: ', i)
                        valid_croco_sign_cnt = 0
                        if parseable[i + 1] == '>':
                            valid_croco_sign_cnt += 1
                        elif not parseable[i + 1] or not parseable[i + 1].isalpha():
                            raise Exception(parseable[i], 'must be followed by a literal or a > sign', 'Position: ', i)
                        if parseable[i - 1] == '<':
                            valid_croco_sign_cnt += 1
                        elif not parseable[i - 1].isalpha():
                            raise Exception(parseable[i], 'must be preceded by a literal or a < sign', 'Position: ', i)
                        if valid_croco_sign_cnt == 2:
                            st_1 = ""
                            if parseable[i - 2] == ')':
                                k = i - 2
                                while parseable[k] != '(':
                                    k -= 1
                                st_1.join(parseable[k:i - 1])
                            else:
                                st_1 = parseable[i - 2]
                            st_2 = ""
                            if parseable[i + 2] == '(':
                                k = k + 3
                                while parseable[k] != ')':
                                    k += 1
                                st_2.join(parseable[i + 2:k + 1])
                            else:
                                st_2 = parseable[i + 2]
                            final_replacements[
                                st_1 + '<=>' + st_2] = '(' + st_1 + '>>' + st_2 + ')' + '&' + '(' + st_2 + '>>' + st_1 + ')'
                            print(final_replacements)
                if brace_cnt != 0:
                    raise Exception('There is a problem with the closures, please check the braces.')
                original_form = parseable
                for init, repl in final_replacements.items():
                    parseable = parseable.replace(init, repl)
                parseable = parseable.replace('=>', '>>')
                parseable = parseable.replace('<=', '<<')
                parsed_form = parse_expr(parseable)
                missing_order = True
                while missing_order:
                    order = float(input('Enter the order of your belief (0 - 1.0): '))
                    if 0 > order or 1 < order:
                        print('Please enter a valid order value.')
                        continue
                    missing_order = False
                    new_belief = Belief(parsed_form, original_form, order)
                    self.handle_belief(new_belief, choice)
                missing_belief = False
            except Exception as e:
                print(e)
                print('Please try again!')

    def handle_belief(self, new_belief, choice):
        if choice == 1:
            self.belief_base.expand(new_belief)
        elif choice == 2:
            self.belief_base.contract(new_belief)
        elif choice == 3:
            self.belief_base.revise(new_belief)
        elif choice == 4:
            entails = self.belief_base.entails(new_belief)
            if entails:
                print('The current belief base entails the newly entered belief!')
            else:
                print('The current belief base does not entail the newly entered belief!')
            return
        print('Your belief based after the operation:')
        self.belief_base.print()

