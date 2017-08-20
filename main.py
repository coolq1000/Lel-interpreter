import re

''' Commented out because it seemed a little over kill for what I wanted.
class Node:
    
    def __init__(self, data=None):
        self.children = []
        self.parent = None
        self.data = data
    
    def set_parent(self, obj):
        if self.parent == None:
            obj.add_child(self)
            self.parent = obj
        else:
            self.parent.del_child(self)
            obj.add_child(self)
            self.parent = obj
    
    def add_child(self, obj):
        self.children.append(obj)
    
    def del_child(self, obj):
        self.children.pop([i for i, x in enumerate(self.children) if x == obj][0])
    
    def is_leaf(self):
        if self.children == []:
            return True
        return False
    
    def is_root(self):
        if self.children == []:
            return True
        return False
    
    def output(self, count=0):
        print('____'*count + str(self.data) if self.data is not None else 'Node')
        for c in self.children:
            c.output(count=count + 1)
'''

class Token:
    
    def __init__(self, name, value, regex=''):
        self.name, self.value, self.regex = name, value, regex
    
    def __repr__(self):
        return '<Token, {}, {}>'.format(self.name, self.value)

class Lexer:
    
    tokens = {
        r'\(': 'LPAREN',
        r'\)': 'RPAREN',
        r'[0-9]+': 'NUMBER',
        r"'.*?'": 'STRING',
        r'".*?"': 'STRING',
        r'[A-Za-z0-9\-\!\$\%\^\&\*\_\+\|\~\=\`\{\}\[\]\:\"\;\'\<\>?,.\/]+': 'KEYWORD'
    }
    
    def __init__(self, code):
        self.code = code
    
    def lexer(self):
        token_string = '|'.join(self.tokens)
        match = re.findall(token_string, self.code)
        tks = []
        for i in match:
            for j in self.tokens:
                if re.findall(j, i):
                    tks += [Token(self.tokens[j], i, regex=j)]
                    break
        return tks

class Parse:
    
    def __init__(self, code):
        self.code = code
        self.tree = []
        self.parent = []
        self.work = self.tree
        self.line = 0
    
    def parse(self):
        while self.line < len(self.code):
            token = self.code[self.line]
            name, value = token.name, token.value
            if name == 'LPAREN':
                self.work += [[]]
                self.parent.append(self.work)
                self.work = self.work[-1]
            elif name == 'RPAREN':
                self.work = self.parent.pop()
            else:
                self.work.append(token)
            self.line += 1
        return self.tree

class Evaluate:
    
    def __init__(self, code):
        self.variables = {}
        self.functions = {}
        self.code = code
    
    def evaluate_expr(self, expr):
        for i, c in enumerate(expr):
            if type(c) is list:
                self.evaluate_expr(c)
            else:
                name, value = c.name, c.value
                if   name == 'NUMBER':
                    return int(value)
                elif value in self.variables:
                    return self.variables[value]
                elif value == 'let':
                    print('Ding!')
                
    
    def evaluate(self):
        self.evaluate_expr(self.code)

code = '''
(function cube (x)
  (* x x x)
)
 
(let threeCubed (cube 3))
 
(print threeCubed)
'''
code = Lexer(code).lexer()
print(code)
code = Parse(code).parse()
print(code)
Evaluate(code).evaluate()
