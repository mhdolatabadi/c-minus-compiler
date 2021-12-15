import scanner
from anytree import Node, RenderTree


def write_traversal(text):
    file = open("traversal.txt", "a")
    file.write(text)
    file.close()


def write_parse_tree(text):
    file = open("parse_tree.txt", "a")
    file.write(f'{text}\n')
    file.close()


def write_syntax_error(text):
    syntax = open('syntax_errors.txt', 'a')
    syntax.write(f'{text}\n')
    syntax.close()


index = None


def next_token():
    global char
    global index
    if index == None:
        index = 0
    char = scanner.get_next_token(index)
    print(char)
    index += 1


class TransitionDiagram:
    EOF = False

    def __init__(self, name, firsts, follows):
        self.nodes_edges = dict()
        self.terminal_node = 0
        self.name = name
        self.firsts = firsts
        self.follows = follows

    def print_tree(self, root):
        for pre, fill, node in RenderTree(root):
            write_parse_tree("%s%s" % (pre, node.name))

    def add_node(self,
                 node_id: int,
                 is_starter: bool = True,
                 is_terminal: bool = False):
        self.nodes_edges[node_id] = dict()
        if is_terminal:
            self.terminal_node = node_id

    def add_edge(self, from_node: int, to_node: int, by):
        self.nodes_edges[from_node][by] = to_node

    def traversal(self, errors, parent_node=Node('God'), edge_number: int = 0):
        try:
            if 'Unexpected' in errors[-1]:
                return
        except:
            print('khob ke chi')
        value = char['token_type'] if char['token_type'] in [
            'NUM', 'ID'
        ] else char['value']
        leaf_name = f"({char['token_type']}, {char['value']})" if value != '$' else value
        edge = self.nodes_edges[edge_number]
        node = Node(
            self.name
        ) if edge_number == 0 and self.name != 'Program' else parent_node
        for rule in edge:
            if type(rule) == TransitionDiagram and (
                    value in rule.firsts or
                ('EPSILON' in rule.firsts and value in rule.follows)):
                result = rule.traversal(errors, node)
                if edge[rule] != self.terminal_node:
                    self.traversal(errors, node, edge[rule])
                if edge_number == 0 and self.name != 'Program' and result:
                    node.parent = parent_node
                return True
            elif rule == char['value'] or (rule in ['NUM', 'ID']
                                           and char['token_type'] == rule):
                leaf_node = Node(leaf_name)
                leaf_node.parent = node
                next_token()
                if edge[rule] != self.terminal_node:
                    self.traversal(errors, node, edge[rule])
                if edge_number == 0:
                    node.parent = parent_node
                return True
            elif rule == 'EPSILON':
                leaf_node = Node('epsilon')
                leaf_node.parent = node
                node.parent = parent_node
                return True
        for i in edge:
            print(self.name, i, value, edge[i], self.terminal_node)
            if value == '$' and type(i) == TransitionDiagram:
                print('Unexpected EOF')
                errors.append(
                    f'#{scanner.get_line_number() + 1} : syntax error, Unexpected EOF'
                )
                return False
            if i != value and type(i) != TransitionDiagram:
                print('missing', i)
                errors.append(
                    f'#{scanner.get_line_number()} : syntax error, missing {i}'
                )
                return self.traversal(errors, parent_node, edge[i])
            if value in i.follows or value in self.follows:
                print('missing', i.name)
                errors.append(
                    f'#{scanner.get_line_number()} : syntax error, missing {i.name}'
                )
                return self.traversal(errors, parent_node, edge[i])
            if value not in self.follows:
                print('illegal', value)
                errors.append(
                    f'#{scanner.get_line_number()} : syntax error, illegal {value}'
                )
                next_token()
                return self.traversal(errors, parent_node, edge_number)


Program = TransitionDiagram('Program', ['int', 'void'], ['$'])
Declarationlist = TransitionDiagram(
    'Declaration-list', ['int', 'void', 'EPSILON'],
    ['$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}'])
Declaration = TransitionDiagram('Declaration', ['int', 'void'], [
    'int', 'void', '$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(',
    'NUM', '}'
])
Declarationinitial = TransitionDiagram('Declaration-initial', ['int', 'void'],
                                       ['(', ';', '[', ',', ')'])
Declarationprime = TransitionDiagram('Declaration-prime', ['(', ';', '['], [
    'int', 'void', '$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(',
    'NUM', '}'
])
Vardeclarationprime = TransitionDiagram('Var-declaration-prime', [';', '['], [
    'int', 'void', '$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(',
    'NUM', '}'
])
Fundeclarationprime = TransitionDiagram('Fun-declaration-prime', ['('], [
    'int', 'void', '$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(',
    'NUM', '}'
])
Typespecifier = TransitionDiagram('Type-specifier', ['int', 'void'], ['ID'])
Params = TransitionDiagram('Params', ['int', 'void'], [')'])
Paramlist = TransitionDiagram('Param-list', [',', 'EPSILON'], [')'])
Param = TransitionDiagram('Param', ['int', 'void'], [',', ')'])
Paramprime = TransitionDiagram('Param-prime', ['[', 'EPSILON'], [',', ')'])
Compoundstmt = TransitionDiagram('Compound-stmt', ['{'], [
    'int', 'void', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(',
    'NUM', '}', 'endif', 'else', 'until'
])
Statementlist = TransitionDiagram(
    'Statement-list',
    ['EPSILON', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM'],
    ['}'])
Statement = TransitionDiagram(
    'Statement',
    ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM'], [
        '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}',
        'endif', 'else', 'until'
    ])
Expressionstmt = TransitionDiagram(
    'Expression-stmt', ['break', ';', 'ID', '(', 'NUM'], [
        '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}',
        'endif', 'else', 'until'
    ])
Selectionstmt = TransitionDiagram('Selection-stmt', ['if'], [
    '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}',
    'endif', 'else', 'until'
])
Elsestmt = TransitionDiagram('Else-stmt', ['endif', 'else'], [
    '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}',
    'endif', 'else', 'until'
])
Iterationstmt = TransitionDiagram('Iteration-stmt', ['repeat'], [
    '{', 'break', ';', 'if', 'repeat', 'return', 'ID(', 'NUM', '}', 'endif',
    'else', 'until'
])
Returnstmt = TransitionDiagram('Return-stmt', ['return'], [
    '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}',
    'endif', 'else', 'until'
])
Returnstmtprime = TransitionDiagram(
    'Return-stmt-prime', [';', 'ID', '(', 'NUM'], [
        '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}',
        'endif', 'else', 'until'
    ])
Expression = TransitionDiagram('Expression', ['ID', '(', 'NUM'],
                               [';', ')', ']', ','])
B = TransitionDiagram('B',
                      ['=', '[', '(', '*', '+', '-', '<', '==', 'EPSILON'],
                      [';', ')', ']', ','])
H = TransitionDiagram('H', ['=', '*', 'EPSILON', '+', '-', '<', '=='],
                      [';', ')', ']', ','])
Simpleexpressionzegond = TransitionDiagram('Simple-expression-zegond',
                                           ['(', 'NUM'], [';', ')', ']', ','])
Simpleexpressionprime = TransitionDiagram(
    'Simple-expression-prime', ['(', '*', '+', '-', '<', '==', 'EPSILON'],
    [';', ')', ']', ','])
C = TransitionDiagram('C', ['EPSILON', '<', '=='], [';', ')', ']', ','])
Relop = TransitionDiagram('Relop', ['<', '=='], ['(', 'ID', 'NUM'])
Additiveexpression = TransitionDiagram('Additive-expression',
                                       ['(', 'ID', 'NUM'],
                                       [';', ')', ']', ','])
Additiveexpressionprime = TransitionDiagram('Additive-expression-prime',
                                            ['(', '*', '+', '-', 'EPSILON'],
                                            ['<', '==', ';', ')', ']', ','])
Additiveexpressionzegond = TransitionDiagram('Additive-expression-zegond',
                                             ['(', 'NUM'],
                                             ['<', '==', ';', ')', ']', ','])
D = TransitionDiagram('D', ['EPSILON', '+', '-'],
                      ['<', '==', ';', ')', ']', ','])
Addop = TransitionDiagram('Addop', ['+', '-'], ['(', 'ID', 'NUM'])
Term = TransitionDiagram('Term', ['(', 'ID', 'NUM'],
                         ['+', '-', ';', ')', '<', '==', ']', ','])
Termprime = TransitionDiagram('Term-prime', ['(', '*', 'EPSILON'],
                              ['+', '-', '<', '==', ';', ')', ']', ','])
Termzegond = TransitionDiagram('Term-zegond', ['(', 'NUM'],
                               ['+', '-', '<', '==', ';', ')', ']', ','])
G = TransitionDiagram('G', ['*', 'EPSILON'],
                      ['+', '-', '<', '==', ';', ')', ']', ','])
Factor = TransitionDiagram('Factor', ['(', 'ID', 'NUM'],
                           ['*', '+', '-', ';', ')', '<', '==', ']', ','])
Varcallprime = TransitionDiagram(
    'Var-call-prime', ['(', '[', 'EPSILON'],
    ['*', '+', '-', ';', ')', '<', '==', ']', ','])
Varprime = TransitionDiagram('Var-prime', ['[', 'EPSILON'],
                             ['*', '+', '-', ';', ')', '<', '==', ']', ','])
Factorprime = TransitionDiagram('Factor-prime', ['(', 'EPSILON'],
                                ['*', '+', '-', '<', '==', ';', ')', ']', ','])
Factorzegond = TransitionDiagram(
    'Factor-zegond', ['(', 'NUM'],
    ['*', '+', '-', '<', '==', ';', ')', ']', ','])
Args = TransitionDiagram('Args', ['EPSILON', 'ID', '(', 'NUM'], [')'])
Arglist = TransitionDiagram('Arg-list', ['ID', '(', 'NUM'], [')'])
Arglistprime = TransitionDiagram('Arg-list-prime', [',', 'EPSILON'], [')'])

Paramprime.add_node(0)
Paramprime.add_node(1, False)
Paramprime.add_node(2, False, True)
Paramprime.add_edge(0, 1, '[')
Paramprime.add_edge(1, 2, ']')
Paramprime.add_edge(0, 2, 'EPSILON')

Param.add_node(0)
Param.add_node(1, False)
Param.add_node(2, False, True)
Param.add_edge(0, 1, Declarationinitial)
Param.add_edge(1, 2, Paramprime)

Paramlist.add_node(0)
Paramlist.add_node(1, False)
Paramlist.add_node(2, False)
Paramlist.add_node(3, False, True)
Paramlist.add_edge(0, 1, ',')
Paramlist.add_edge(1, 2, Param)
Paramlist.add_edge(2, 3, Paramlist)
Paramlist.add_edge(0, 3, 'EPSILON')

Params.add_node(0)
Params.add_node(1, False)
Params.add_node(2, False)
Params.add_node(3, False)
Params.add_node(4, False, True)
Params.add_edge(0, 1, 'int')
Params.add_edge(1, 2, 'ID')
Params.add_edge(2, 3, Paramprime)
Params.add_edge(3, 4, Paramlist)
Params.add_edge(0, 4, 'void')

Vardeclarationprime.add_node(0)
Vardeclarationprime.add_node(1, False)
Vardeclarationprime.add_node(2, False)
Vardeclarationprime.add_node(3, False)
Vardeclarationprime.add_node(4, False, True)
Vardeclarationprime.add_edge(0, 4, ';')
Vardeclarationprime.add_edge(0, 1, '[')
Vardeclarationprime.add_edge(1, 2, 'NUM')
Vardeclarationprime.add_edge(2, 3, ']')
Vardeclarationprime.add_edge(3, 4, ';')

Fundeclarationprime.add_node(0)
Fundeclarationprime.add_node(1, False)
Fundeclarationprime.add_node(2, False)
Fundeclarationprime.add_node(3, False)
Fundeclarationprime.add_node(4, False, True)
Fundeclarationprime.add_edge(0, 1, '(')
Fundeclarationprime.add_edge(1, 2, Params)
Fundeclarationprime.add_edge(2, 3, ')')
Fundeclarationprime.add_edge(3, 4, Compoundstmt)

Typespecifier.add_node(0)
Typespecifier.add_node(1, False, True)
Typespecifier.add_edge(0, 1, 'int')
Typespecifier.add_edge(0, 1, 'void')

Declarationprime.add_node(0)
Declarationprime.add_node(1, False, True)
Declarationprime.add_edge(0, 1, Fundeclarationprime)
Declarationprime.add_edge(0, 1, Vardeclarationprime)

Declarationinitial.add_node(0)
Declarationinitial.add_node(1, False)
Declarationinitial.add_node(2, False, True)
Declarationinitial.add_edge(0, 1, Typespecifier)
Declarationinitial.add_edge(1, 2, 'ID')

Declaration.add_node(0)
Declaration.add_node(1, False)
Declaration.add_node(2, False, True)
Declaration.add_edge(0, 1, Declarationinitial)
Declaration.add_edge(1, 2, Declarationprime)

Declarationlist.add_node(0)
Declarationlist.add_node(1, False)
Declarationlist.add_node(2, False, True)
Declarationlist.add_edge(0, 1, Declaration)
Declarationlist.add_edge(1, 2, Declarationlist)
Declarationlist.add_edge(0, 2, 'EPSILON')

Compoundstmt.add_node(0)
Compoundstmt.add_node(1, False)
Compoundstmt.add_node(2, False)
Compoundstmt.add_node(3, False)
Compoundstmt.add_node(4, False, True)
Compoundstmt.add_edge(0, 1, '{')
Compoundstmt.add_edge(1, 2, Declarationlist)
Compoundstmt.add_edge(2, 3, Statementlist)
Compoundstmt.add_edge(3, 4, '}')

Statementlist.add_node(0)
Statementlist.add_node(1, False)
Statementlist.add_node(2, False, True)
Statementlist.add_edge(0, 1, Statement)
Statementlist.add_edge(1, 2, Statementlist)
Statementlist.add_edge(0, 2, 'EPSILON')

Statement.add_node(0)
Statement.add_node(1, False, True)
Statement.add_edge(0, 1, Iterationstmt)
Statement.add_edge(0, 1, Selectionstmt)
Statement.add_edge(0, 1, Compoundstmt)
Statement.add_edge(0, 1, Returnstmt)
Statement.add_edge(0, 1, Expressionstmt)

Expressionstmt.add_node(0)
Expressionstmt.add_node(1, False)
Expressionstmt.add_node(2, False, True)
Expressionstmt.add_edge(0, 1, Expression)
Expressionstmt.add_edge(1, 2, ';')
Expressionstmt.add_edge(0, 1, 'break')
Expressionstmt.add_edge(1, 2, ';')
Expressionstmt.add_edge(0, 2, ';')

Selectionstmt.add_node(0)
Selectionstmt.add_node(1, False)
Selectionstmt.add_node(2, False)
Selectionstmt.add_node(3, False)
Selectionstmt.add_node(4, False)
Selectionstmt.add_node(5, False)
Selectionstmt.add_node(6, False, True)
Selectionstmt.add_edge(0, 1, 'if')
Selectionstmt.add_edge(1, 2, '(')
Selectionstmt.add_edge(2, 3, Expression)
Selectionstmt.add_edge(3, 4, ')')
Selectionstmt.add_edge(4, 5, Statement)
Selectionstmt.add_edge(5, 6, Elsestmt)

Elsestmt.add_node(0)
Elsestmt.add_node(1, False)
Elsestmt.add_node(2, False)
Elsestmt.add_node(3, False, True)
Elsestmt.add_edge(0, 3, 'endif')
Elsestmt.add_edge(0, 1, 'else')
Elsestmt.add_edge(1, 2, Statement)
Elsestmt.add_edge(2, 3, 'endif')

Iterationstmt.add_node(0)
Iterationstmt.add_node(1, False)
Iterationstmt.add_node(2, False)
Iterationstmt.add_node(3, False)
Iterationstmt.add_node(4, False)
Iterationstmt.add_node(5, False)
Iterationstmt.add_node(6, False, True)
Iterationstmt.add_edge(0, 1, 'repeat')
Iterationstmt.add_edge(1, 2, Statement)
Iterationstmt.add_edge(2, 3, 'until')
Iterationstmt.add_edge(3, 4, '(')
Iterationstmt.add_edge(4, 5, Expression)
Iterationstmt.add_edge(5, 6, ')')

Returnstmt.add_node(0)
Returnstmt.add_node(1, False)
Returnstmt.add_node(2, False, True)
Returnstmt.add_edge(0, 1, 'return')
Returnstmt.add_edge(1, 2, Returnstmtprime)

Returnstmtprime.add_node(0)
Returnstmtprime.add_node(1, False)
Returnstmtprime.add_node(2, False, True)
Returnstmtprime.add_edge(0, 1, Expression)
Returnstmtprime.add_edge(1, 2, ';')
Returnstmtprime.add_edge(0, 2, ';')

Expression.add_node(0)
Expression.add_node(1, False)
Expression.add_node(2, False, True)
Expression.add_edge(0, 2, Simpleexpressionzegond)
Expression.add_edge(0, 1, 'ID')
Expression.add_edge(1, 2, B)

B.add_node(0)
B.add_node(1, False)
B.add_node(2, False)
B.add_node(3, False)
B.add_node(4, False, True)
B.add_node(5, False)
B.add_edge(0, 5, '=')
B.add_edge(5, 4, Expression)
B.add_edge(0, 1, '[')
B.add_edge(1, 2, Expression)
B.add_edge(2, 3, ']')
B.add_edge(3, 4, H)
B.add_edge(0, 4, Simpleexpressionprime)

H.add_node(0)
H.add_node(1, False)
H.add_node(2, False)
H.add_node(3, False)
H.add_node(4, False, True)
H.add_edge(0, 3, '=')
H.add_edge(3, 4, Expression)
H.add_edge(0, 1, G)
H.add_edge(1, 2, D)
H.add_edge(2, 4, C)

Simpleexpressionzegond.add_node(0)
Simpleexpressionzegond.add_node(1, False)
Simpleexpressionzegond.add_node(2, False, True)
Simpleexpressionzegond.add_edge(0, 1, Additiveexpressionzegond)
Simpleexpressionzegond.add_edge(1, 2, C)

Simpleexpressionprime.add_node(0)
Simpleexpressionprime.add_node(1, False)
Simpleexpressionprime.add_node(2, False, True)
Simpleexpressionprime.add_edge(0, 1, Additiveexpressionprime)
Simpleexpressionprime.add_edge(1, 2, C)

C.add_node(0)
C.add_node(1, False)
C.add_node(2, False, True)
C.add_edge(0, 1, Relop)
C.add_edge(1, 2, Additiveexpression)
C.add_edge(0, 2, 'EPSILON')

Relop.add_node(0)
Relop.add_node(1, False, True)
Relop.add_edge(0, 1, '<')
Relop.add_edge(0, 1, '==')

Additiveexpression.add_node(0)
Additiveexpression.add_node(1, False)
Additiveexpression.add_node(2, False, True)
Additiveexpression.add_edge(0, 1, Term)
Additiveexpression.add_edge(1, 2, D)

Additiveexpressionprime.add_node(0)
Additiveexpressionprime.add_node(1, False)
Additiveexpressionprime.add_node(2, False, True)
Additiveexpressionprime.add_edge(0, 1, Termprime)
Additiveexpressionprime.add_edge(1, 2, D)

Additiveexpressionzegond.add_node(0)
Additiveexpressionzegond.add_node(1, False)
Additiveexpressionzegond.add_node(2, False, True)
Additiveexpressionzegond.add_edge(0, 1, Termzegond)
Additiveexpressionzegond.add_edge(1, 2, D)

D.add_node(0)
D.add_node(1, False)
D.add_node(2, False)
D.add_node(3, False, True)
D.add_edge(0, 1, Addop)
D.add_edge(1, 2, Term)
D.add_edge(2, 3, D)
D.add_edge(0, 3, 'EPSILON')

Addop.add_node(0)
Addop.add_node(1, False, True)
Addop.add_edge(0, 1, '+')
Addop.add_edge(0, 1, '-')

Term.add_node(0)
Term.add_node(1, False)
Term.add_node(2, False, True)
Term.add_edge(0, 1, Factor)
Term.add_edge(1, 2, G)

Termprime.add_node(0)
Termprime.add_node(1, False)
Termprime.add_node(2, False, True)
Termprime.add_edge(0, 1, Factorprime)
Termprime.add_edge(1, 2, G)

Termzegond.add_node(0)
Termzegond.add_node(1, False)
Termzegond.add_node(2, False, True)
Termzegond.add_edge(0, 1, Factorzegond)
Termzegond.add_edge(1, 2, G)

G.add_node(0)
G.add_node(1, False)
G.add_node(2, False)
G.add_node(3, False, True)
G.add_edge(0, 1, '*')
G.add_edge(1, 2, Factor)
G.add_edge(2, 3, G)
G.add_edge(0, 3, 'EPSILON')

Factor.add_node(0)
Factor.add_node(1, False)
Factor.add_node(2, False)
Factor.add_node(3, False)
Factor.add_node(4, False, True)
Factor.add_edge(0, 1, '(')
Factor.add_edge(1, 2, Expression)
Factor.add_edge(2, 4, ')')
Factor.add_edge(0, 4, 'NUM')
Factor.add_edge(0, 3, 'ID')
Factor.add_edge(3, 4, Varcallprime)

Varcallprime.add_node(0)
Varcallprime.add_node(1, False)
Varcallprime.add_node(2, False)
Varcallprime.add_node(3, False, True)
Varcallprime.add_edge(0, 1, '(')
Varcallprime.add_edge(1, 2, Args)
Varcallprime.add_edge(2, 3, ')')
Varcallprime.add_edge(0, 3, Varprime)

Varprime.add_node(0)
Varprime.add_node(1, False)
Varprime.add_node(2, False)
Varprime.add_node(3, False, True)
Varprime.add_edge(0, 1, '[')
Varprime.add_edge(1, 2, Expression)
Varprime.add_edge(2, 3, ']')
Varprime.add_edge(0, 3, 'EPSILON')

Factorprime.add_node(0)
Factorprime.add_node(1, False)
Factorprime.add_node(2, False)
Factorprime.add_node(3, False, True)
Factorprime.add_edge(0, 1, '(')
Factorprime.add_edge(1, 2, Args)
Factorprime.add_edge(2, 3, ')')
Factorprime.add_edge(0, 3, 'EPSILON')

Factorzegond.add_node(0)
Factorzegond.add_node(1, False)
Factorzegond.add_node(2, False)
Factorzegond.add_node(3, False, True)
Factorzegond.add_edge(0, 1, '(')
Factorzegond.add_edge(1, 2, Expression)
Factorzegond.add_edge(2, 3, ')')
Factorzegond.add_edge(0, 3, 'NUM')

Args.add_node(0)
Args.add_node(1, False, True)
Args.add_edge(0, 1, Arglist)
Args.add_edge(0, 1, 'EPSILON')

Arglist.add_node(0)
Arglist.add_node(1, False)
Arglist.add_node(2, False, True)
Arglist.add_edge(0, 1, Expression)
Arglist.add_edge(1, 2, Arglistprime)

Arglistprime.add_node(0)
Arglistprime.add_node(1, False)
Arglistprime.add_node(2, False)
Arglistprime.add_node(3, False, True)
Arglistprime.add_edge(0, 1, ',')
Arglistprime.add_edge(1, 2, Expression)
Arglistprime.add_edge(2, 3, Arglistprime)
Arglistprime.add_edge(0, 3, 'EPSILON')

Program.add_node(0)
Program.add_node(1, False)
Program.add_node(2, False, True)
Program.add_edge(0, 1, Declarationlist)
Program.add_edge(1, 2, '$')


def run():
    next_token()
    errors = list()
    node = Node('Program')
    Program.traversal(errors, node)
    Program.print_tree(node)
    if errors:
        for error in errors:
            write_syntax_error(error)
            if 'Unexpected' in error:
                break
    else:
        write_syntax_error('There is no syntax error.')
