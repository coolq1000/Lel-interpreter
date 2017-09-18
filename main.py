
import re, shlex, sys

class Error:

    ERROR_TYPE_INCORRECTNUMBEROFARGUMENTS = Exception('E: Incorrect number of arguments.')

    def check_args(args, count):
        if len(args) != count:
            raise Error.ERROR_TYPE_INCORRECTNUMBEROFARGUMENTS
        

class Null:
    
    def __repr__(self):
        return 'null'

class Pre:

    def __init__(self, code):
        self.code = code
    
    def pre(self):
        result = []
        for l in self.code.split('\n'):
            if not l.replace('\t', ' ').lstrip(' ').startswith(';'):
                result += [l]
        return '\n'.join(result)

class Token:

    def __init__(self, name, value):
        self.name, self.value = name, value
    
    def __repr__(self):
        return '<Token, {}, {}>'.format(self.name, self.value)

class Lexer:

    def __init__(self, code):
        self.code = code
    
    def lexer(self):
        match = list(shlex.shlex(self.code))
        i = 0
        while i < len(match):
            if match[i] == '.':
                if i > 0 and i < len(match) - 1:

                    match[i] = match[i - 1] + '.' + match[i + 1]
                    match.pop(i + 1)
                    match.pop(i - 1)
            i += 1
        out = []
        for m in match:
            if (m.startswith('"') and m.endswith('"')) or (m.startswith("'") or m.endswith("'")):
                out += [Token('STRING', m[1:-1])]
            elif m.replace('.', '').isdigit():
                out += [Token('NUMBER', float(m) if '.' in m else int(m))]
            else:
                out += [Token('KEYWORD', m)]
        return out

class Parse:

    def __init__(self, code):
        self.code = code
        self.tree = []
        self.parent = []
        self.working = self.tree
    
    def parse(self):
        for token in self.code:
            n, v = token.name, token.value
            if v == '(':
                self.working += [[]]
                self.parent += [self.working]
                self.working = self.working[-1]
            elif v == ')':
                self.working = self.parent.pop()
            else:
                self.working += [token]
        return self.tree

class Evaluator:

    def __init__(self, code, stdout=None):
        self.stdout = stdout
        self.buffer = []
        self.code = code
        self.variables = {'null': [Null()]}
        self.functions = {}
        self.builtins = {
            'let': self._let,
            'print': self._print,
            'puts': self._puts,
            'function': self._function,
            'loop': self._loop,
            'if': self._if,
            'list': self._list,
            'index': self._index,
            'len': self._len,
            'exit': self._exit,
            'set': self._set,
            'push': self._push,
            'pop': self._pop,
            '+': self._add,
            '-': self._sub,
            '*': self._mul,
            '/': self._div,
            '%': self._mod,
            '=': self._equ,
            '!': self._not,
            '<': self._les,
            '>': self._gre
        }
    
    def get_var(self, name):
        if name in self.variables:
            return self.variables[name][0]
        raise Exception('E: Attempt to access undefined variable.')
    
    def set_var(self, name, value, scope=0):
        self.variables[name] = (value, scope)
    
    def _let(self, args):
        setter = self.evaluate_expr([args[1]])
        self.set_var(args[0].value, setter)

    def _print(self, args):
        if self.stdout == None:
            print(self.evaluate_expr(args))
        else:
            ans = self.evaluate_expr(args)
            if type(ans) is list:
                self.buffer.append(list(ans))
            else:
                self.buffer.append(ans)
    
    def _puts(self, args):
        if self.stdout == None:
            print(self.evaluate_expr(args), end='')
        else:
            if len(self.buffer) > 0:
                self.buffer[-1].append(self.evaluate_expr(args))
            else:
                self.buffer.append(self.evaluate_expr(args))
    
    def _function(self, args):
        name = args[0]
        parameters = args[1]
        code = args[2:]
        self.functions[name.value] = (code, parameters)

    def _loop(self, args):
        expr = args[0]
        code = args[1:]
        while self.evaluate_expr(expr) == 1:
            self.evaluate_expr(code)
    
    def _if(self, args):
        expr = args[0]
        code = args[1:]
        if self.evaluate_expr(expr) == 1:
            self.evaluate_expr(code)
    
    def _list(self, args):
        return [self.evaluate_expr([x]) for x in args]

    def _index(self, args):
        ind = self.evaluate_expr([args[0]])
        lst = self.evaluate_expr([args[1]])
        return lst[int(ind)]
    
    def _len(self, args):
        return len(self.evaluate_expr([args[0]]))

    def _exit(self, args):
        raise SystemExit
    
    def _set(self, args):
        args = [self.evaluate_expr([x]) for x in args]
        args[1][int(args[0])] = args[2]

    def _push(self, args):
        args = [self.evaluate_expr([x]) for x in args]
        args[0].append(args[1])
    
    def _pop(self, args):
        args = [self.evaluate_expr([x]) for x in args]
        args[0].pop()
    
    def _add(self, args):
        ans = self.evaluate_expr([args[0]]) + self.evaluate_expr([args[1]])
        return ans

    def _sub(self, args):
        ans = self.evaluate_expr([args[0]]) - self.evaluate_expr([args[1]])
        return ans

    def _mul(self, args):
        ans = self.evaluate_expr([args[0]]) * self.evaluate_expr([args[1]])
        return ans

    def _div(self, args):
        ans = self.evaluate_expr([args[0]]) / self.evaluate_expr([args[1]])
        return ans

    def _mod(self, args):
        ans = self.evaluate_expr([args[0]]) % self.evaluate_expr([args[1]])
        return ans
    
    def _equ(self, args):
        ans = self.evaluate_expr([args[0]]) == self.evaluate_expr([args[1]])
        return 1 if ans else 0

    def _not(self, args):
        ans = self.evaluate_expr([args[0]]) == self.evaluate_expr([args[1]])
        return 0 if ans else 1

    def _les(self, args):
        ans = self.evaluate_expr([args[0]]) < self.evaluate_expr([args[1]])
        return 1 if ans else 0
    
    def _gre(self, args):
        ans = self.evaluate_expr([args[0]]) > self.evaluate_expr([args[1]])
        return 1 if ans else 0

    def call(self, fn, args):
        fn = self.functions[fn]
        parameters = fn[1]
        code = fn[0]
        for i, p in enumerate(parameters):
            self.set_var(p.value, self.evaluate_expr([args[i]]))
        return self.evaluate_expr(code)

    def evaluate_expr(self, e):
        last = None
        for i, cmd in enumerate(e):
            if type(cmd) is list:
                ans = self.evaluate_expr(cmd)
                last = ans
            else:
                if type(cmd) is Token:
                    n, v = cmd.name, cmd.value
                else:
                    last = cmd
                    break

                if n == 'NUMBER':
                    last = v
                elif n == 'STRING':
                    last = v
                elif n == 'KEYWORD':
                    if v in self.variables:
                        last = self.get_var(v)
                    elif v in self.functions:
                        last = self.call(v, e[1:])
                        break
                    elif v in self.builtins:
                        last = self.builtins[v](e[1:])
                        break
                    else:
                        raise Exception('E: Unexpected token `{}`.'.format(v))
        return last

    def run(self):
        self.evaluate_expr([self.code])

if __name__ == '__main__':
    if len(sys.argv) == 2:
        code = open(sys.argv[1], 'r').read()
        code = Pre(code).pre()
        code = Lexer(code).lexer()
        code = Parse(code).parse()
        Evaluator(code).run()
    else:
        # Create REPL,
        evaluate = Evaluator([])
        while True:
            cmd = input('LEL> ')
            left = 0
            right = 0
            for char in cmd:
                if char == '(': left += 1
                if char == ')': right += 1
            while left > right:
                cmd += input('...> ')
                left = 0
                right = 0
                for char in cmd:
                    if char == '(': left += 1
                    if char == ')': right += 1
            code = cmd
            code = Pre(code).pre()
            code = Lexer(code).lexer()
            code = Parse(code).parse()
            try:
                ans = evaluate.evaluate_expr(code)
                if ans != None: print(ans)
            except Exception as e:
                print(e)
