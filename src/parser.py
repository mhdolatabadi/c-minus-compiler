from anytree import Node, RenderTree
import json
from codegen import write_to_output
import scanner


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
    index += 1


grammer = json.load(open('./data/grammer.json', 'r'))


class TransitionDiagram:
    EOF = False

    def __init__(self, name):
        self.nodes_edges = dict()
        self.terminal_node = 0
        self.name = name
        self.firsts = grammer[name.replace('-', '')]['firsts']
        self.follows = grammer[name.replace('-', '')]['follows']

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
        if errors and 'Unexpected' in errors[-1]:
            return
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
            if value == '$' and type(i) == TransitionDiagram:
                errors.append(
                    f'#{scanner.get_line_number() + 1} : syntax error, Unexpected EOF'
                )
                return False
            if i != value and type(i) != TransitionDiagram:
                errors.append(
                    f'#{scanner.get_line_number()} : syntax error, missing {i}'
                )
                return self.traversal(errors, parent_node, edge[i])
            if value in i.follows or value in self.follows:
                errors.append(
                    f'#{scanner.get_line_number()} : syntax error, missing {i.name}'
                )
                return self.traversal(errors, parent_node, edge[i])
            if value not in self.follows:
                errors.append(
                    f'#{scanner.get_line_number()} : syntax error, illegal {value}'
                )
                next_token()
                return self.traversal(errors, parent_node, edge_number)


Program = TransitionDiagram("Program")
Declarationlist = TransitionDiagram("Declaration-list")
Declaration = TransitionDiagram("Declaration")
Declarationinitial = TransitionDiagram("Declaration-initial")
Declarationprime = TransitionDiagram("Declaration-prime")
Vardeclarationprime = TransitionDiagram("Var-declaration-prime")
Fundeclarationprime = TransitionDiagram("Fun-declaration-prime")
Typespecifier = TransitionDiagram("Type-specifier")
Params = TransitionDiagram("Params")
Paramlist = TransitionDiagram("Param-list")
Param = TransitionDiagram("Param")
Paramprime = TransitionDiagram("Param-prime")
Compoundstmt = TransitionDiagram("Compound-stmt")
Statementlist = TransitionDiagram("Statement-list")
Statement = TransitionDiagram("Statement")
Expressionstmt = TransitionDiagram("Expression-stmt")
Selectionstmt = TransitionDiagram("Selection-stmt")
Elsestmt = TransitionDiagram("Else-stmt")
Iterationstmt = TransitionDiagram("Iteration-stmt")
Returnstmt = TransitionDiagram("Return-stmt")
Returnstmtprime = TransitionDiagram("Return-stmt-prime")
Expression = TransitionDiagram("Expression")
B = TransitionDiagram("B")
H = TransitionDiagram("H")
Simpleexpressionzegond = TransitionDiagram("Simple-expression-zegond")
Simpleexpressionprime = TransitionDiagram("Simple-expression-prime")
C = TransitionDiagram("C")
Relop = TransitionDiagram("Relop")
Additiveexpression = TransitionDiagram("Additive-expression")
Additiveexpressionprime = TransitionDiagram("Additive-expression-prime")
Additiveexpressionzegond = TransitionDiagram("Additive-expression-zegond")
D = TransitionDiagram("D")
Addop = TransitionDiagram("Addop")
Term = TransitionDiagram("Term")
Termprime = TransitionDiagram("Term-prime")
Termzegond = TransitionDiagram("Term-zegond")
G = TransitionDiagram("G")
Factor = TransitionDiagram("Factor")
Varcallprime = TransitionDiagram("Var-call-prime")
Varprime = TransitionDiagram("Var-prime")
Factorprime = TransitionDiagram("Factor-prime")
Factorzegond = TransitionDiagram("Factor-zegond")
Args = TransitionDiagram("Args")
Arglist = TransitionDiagram("Arg-list")
Arglistprime = TransitionDiagram("Arg-list-prime")

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

    write_to_output()
