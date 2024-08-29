from unittest import TestCase, main
from internals import Environment, IntpretorException

class Intepretor:

    def __init__(self):
        self.environments = {}
        self.globalEnv = Environment(map={
            'null': None
        })
        

    def eval(self, expr, environ=None):
        #######################
        # setting default env
        #######################
        if environ is None:
            environ = self.globalEnv
        #######################
        # self evaluating expr
        #######################
        if type(expr) == int or type(expr) == float:
            return expr
        elif type(expr) == str:
            if environ.detect(expr):
                return environ.lookup(expr)
            else:
                return expr.strip('"')
        
        elif type(expr) == list:
            if expr == []:
                return []
            else:
                #######################
                # arithmetic operation
                #######################
                if expr[0] == '+':
                    return self.eval(expr[1], environ) + self.eval(expr[2], environ)
                elif expr[0] == '-':
                    return self.eval(expr[1], environ) - self.eval(expr[2], environ)
                elif expr[0] == '%':
                    return self.eval(expr[1], environ) % self.eval(expr[2], environ)
                elif expr[0] == '*':
                    return self.eval(expr[1], environ) * self.eval(expr[2], environ)
                elif expr[0] == '/':
                    return self.eval(expr[1], environ) / self.eval(expr[2], environ)
                ########################
                # conditionals operation
                ########################
                elif expr[0] == '>':
                    return self.eval(expr[1], environ) > self.eval(expr[2], environ)
                elif expr[0] == '<':
                    return self.eval(expr[1], environ) < self.eval(expr[2], environ)
                elif expr[0] == '<=':
                    return self.eval(expr[1], environ) <= self.eval(expr[2], environ)
                elif expr[0] == '>=':
                    return self.eval(expr[1], environ) >= self.eval(expr[2], environ)
                elif expr[0] == '!=':
                    return self.eval(expr[1], environ) != self.eval(expr[2], environ)
                elif expr[0] == '==':
                    return self.eval(expr[1], environ) == self.eval(expr[2], environ)
                ########################
                # branch operation
                ########################
                elif expr[0] == 'if':
                    if len(expr) != 4 and len(expr) != 3:
                        raise IntpretorException(f"Invalid if expression. Has {len(expr)} number of expression.")
                    elif len(expr[1:]) == 2:
                        if self.eval(expr[1],environ):
                            return self.eval(expr[2],environ)
                    else:
                        if self.eval(expr[1],environ):
                            return self.eval(expr[2],environ)
                        else:
                            return self.eval(expr[3],environ)
                elif expr[0] == 'while':
                    if len(expr) != 3 and len(expr) != 2:
                        raise IntpretorException(f"Invalid while expression. Has {len(expr)} number of expression.")
                    result = self.globalEnv.lookup('null')
                    whileEnv = Environment(parent=environ)
                    while (self.eval(expr[1],whileEnv)):
                        result = self.eval(expr[2],whileEnv)
                    return result
                #######################
                # assignment operation
                #######################
                elif expr[0] == 'var':
                    environ.set(expr[1],self.eval(expr[2],environ))
                    return self.eval(expr[2],environ)
                elif expr[0] == 'set':
                    value = self.eval(expr[2],environ)
                    return environ.assign(expr[1], value)
                elif expr[0] == 'block':
                    return self._evalBlock(expr[1:],environ)
                elif type(expr[0]) == str:
                    return environ.lookup(expr[0])
                else:
                    raise IntpretorException("Unknown expression start!!")
        else:
            raise IntpretorException("Unknown expression!!")
        
    def _evalBlock(self, expressions, environ):
        globalEnv = self.globalEnv
        result = globalEnv.lookup('null')
        newEnv = Environment(parent=environ)
        for expr in expressions:
            result = self.eval(expr, newEnv)

        return result


class IntepretorTest(TestCase):

    def test_string(self):
        i = Intepretor()
        string = 'hello'
        self.assertEqual(string, i.eval(string))
    
    def test_number(self):
        i = Intepretor()
        value = 12
        self.assertEqual(value, i.eval(value))

    def test_sum(self):
        i = Intepretor()
        tt = []
        tt.append({'value': ['+', 1, 2], 'sum': 3})
        tt.append({'value': ['+', ['+', 1, 2], 2], 'sum': 5})
        tt.append({'value': ['+', ['+', 1, ['+', 1, 2]], 2], 'sum': 6})
        for t in tt:
            sum = t['sum']
            value = t['value']
            self.assertEqual(sum, i.eval(value))

    def test_var(self):
        i = Intepretor()
        tt = []
        tt.append({'definition': ['var', 'x', 2], 'query': ['x'], 'value': 2})
        tt.append({'definition': ['var', 'y', 'x'], 'query': ['y'], 'value': 2})
        for t in tt:
            i.eval(t['definition'])
            value = t['value']
            self.assertEqual(value, i.eval(t['query']))

    def test_var_undefined(self):
        i = Intepretor()
        try:
            i.eval(['x'])
        except IntpretorException as e:
            self.assertEqual("Undefined variable!!",e.errors)
        else:
            self.assertEqual(True,False)
    
    def test_block(self):
        i = Intepretor()
        tt = []
        tt.append({'value': ['block'], 'result': None})
        tt.append({'value': ['block',
                             ['var', 'sum', ['+', 10 ,20]],
                             'sum',
                             ], 'result': 30})
        tt.append({'value': ['block',
                             ['var', 'sum', ['+', 10 ,20]],
                             ['var','prod',['*', 'sum', 20]],
                             'prod'
                             ], 'result': 600})
        for t in tt:
            result = t['result']
            value = t['value']
            self.assertEqual(result, i.eval(value))
    
    def test_branch(self):
        i = Intepretor()
        tt = []
        tt.append({'value': ['while',['>', 1, 2]], 'result': None})
        tt.append({'value': ['block',
                             ['var', 'count', 0],
                             ['while',
                             ['<', 'count', 5],
                                ['set', 'count', ['+', 'count', 1]]
                             ]], 'result': 5})
        tt.append({'value': ['if',
                             ['>', 1, ['+', 10 ,20]],
                             10,
                             25
                             ], 'result': 25})
        tt.append({'value': ['if',
                             ['<', 1, ['+', 10 ,20]],
                             10,
                             25
                             ], 'result': 10})
        
        for t in tt:
            result = t['result']
            value = t['value']
            self.assertEqual(result, i.eval(value))

    def test_set(self):
        i = Intepretor()
        tt = []
        tt.append({'value': ['block',
                             ['var', 'sum', ['+', 10 ,20]],
                             ['block',
                              ['var', 'x', 10],
                              ['set', 'sum', 'x'],
                              ],
                             'sum',
                             ], 'result': 10})
        tt.append({'value': ['block',
                             ['var', 'sum', ['+', 10 ,20]],
                             ['block',
                              ['var', 'x', 10],
                              ['set', 'sum', 40],
                              ],
                             'sum',
                             ], 'result': 40})
        
        tt.append({'value': ['block',
                             ['var', 'sum', ['+', 10 ,20]],
                             ['block',
                              ['var', 'x', 10],
                              ['set', 'sum', ['+','x', 'sum']],
                              ],
                             'sum',
                             ], 'result': 40})

        for t in tt:
            result = t['result']
            value = t['value']
            self.assertEqual(result, i.eval(value))

if __name__ == '__main__':
    main()