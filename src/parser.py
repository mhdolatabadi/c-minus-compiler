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


class TransitionDiagram:
    def __init__(self, name):
        self.nodes_edges = dict()
        self.current_node = []
        self.terminal_node = 0
        self.name = name
        self.depth = -1
        self.node_depth = -1
        self.node = []

    def print_tree(self):
        for pre, fill, node in RenderTree(self.node[0]):
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

    def traversal(self, char: str, path, parent_node=Node('God')):
        node = 0
        self.depth += 1
        self.node_depth += 1
        try:
            self.current_node[self.depth]
            self.node[self.node_depth]
        except IndexError:
            self.current_node.append(0)
            self.node.append(Node(self.name))
        starting_rule = self.current_node[self.depth]
        edge = self.nodes_edges[starting_rule]
        for j in edge:
            if type(j) == TransitionDiagram:
                result = j.traversal(char, path, self.node[self.node_depth])
                if (result):
                    if not self.node[self.node_depth].parent:
                        self.node[self.node_depth].parent = parent_node
                        write_traversal(f'{self.name} {parent_node.name}\n')
                    path.append(self.name)
                    if (result == 14):
                        self.depth -= 1
                        self.node_depth -= 1
                        return 14
                    else:
                        if edge[j] == self.terminal_node:
                            self.current_node[self.depth] = 0
                            self.depth -= 1
                            self.node_depth -= 1
                            if self.name == 'Statement':
                                write_traversal(
                                    f'True {self.node_depth} {j.name}\n')
                            self.node.pop()
                            return True
                        else:
                            self.current_node[self.depth] = edge[j]
                            self.depth -= 1
                            self.node_depth -= 1
                            if self.name == 'Statement':
                                write_traversal(
                                    f'14 {self.node_depth} {j.name}\n')
                            return 14
            if j == char['value']:
                leaf_name = f"({char['token_type']}, {char['value']})" if char[
                    'value'] != '$' else char['value']
                path.append(leaf_name)
                path.append(self.name)

                if edge[j] == self.terminal_node:
                    node = Node(leaf_name)
                    node.parent = self.node[self.node_depth]
                    if not self.node[self.node_depth].parent:
                        self.node[self.node_depth].parent = parent_node
                    self.current_node[self.depth] = 0
                    self.depth -= 1
                    self.node_depth -= 1
                    if self.name != 'Program':
                        self.node.pop()
                    return True
                else:
                    node = Node(leaf_name)
                    node.parent = self.node[self.node_depth]
                    if not self.node[self.node_depth].parent:
                        self.node[self.node_depth].parent = parent_node
                    self.current_node[self.depth] = edge[j]
                    self.depth -= 1
                    self.node_depth -= 1
                    return 14

            if j in ['NUM', 'ID']:
                if (char['token_type'] == j):
                    path.append(f"({char['token_type']}, {char['value']})")
                    path.append(self.name)
                    node = Node(f"({char['token_type']}, {char['value']})")
                    node.parent = self.node[self.node_depth]
                    if not self.node[self.node_depth].parent:
                        self.node[self.node_depth].parent = parent_node
                    if edge[j] == self.terminal_node:
                        self.current_node[self.depth] = 0
                        self.depth -= 1
                        self.node_depth -= 1
                        self.node.pop()
                        return True
                    else:
                        self.current_node[self.depth] = edge[j]
                        self.depth -= 1
                        self.node_depth -= 1
                        return 14
            if j == 'EPSILON':
                path.append('epsilon')
                path.append(self.name)
                node = Node('epsilon')
                node.parent = self.node[self.node_depth]
                if not self.node[self.node_depth].parent:
                    self.node[self.node_depth].parent = parent_node
                if edge[j] == self.terminal_node:
                    self.current_node[self.depth] = 0
                    self.depth -= 1
                    self.node_depth -= 1
                    self.node.pop()
                    return 'epsilon'
        self.node_depth -= 1
        self.depth -= 1
        self.node.pop()

        return False


Paramprime = TransitionDiagram("Param-prime")
Param = TransitionDiagram("Param")
Paramlist = TransitionDiagram("Param-list")
Params = TransitionDiagram("Params")
Vardeclarationprime = TransitionDiagram("Var-declaration-prime")
Fundeclarationprime = TransitionDiagram("Fun-declaration-prime")
Typespecifier = TransitionDiagram("Type-specifier")
Declarationprime = TransitionDiagram("Declaration-prime")
Declarationinitial = TransitionDiagram("Declaration-initial")
Declaration = TransitionDiagram("Declaration")
Declarationlist = TransitionDiagram("Declaration-list")
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
Program = TransitionDiagram("Program")

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
Factor.add_node(3, False, True)
Factor.add_node(4, False)
Factor.add_edge(0, 3, 'NUM')
Factor.add_edge(0, 1, '(')
Factor.add_edge(1, 2, Expression)
Factor.add_edge(2, 3, ')')
Factor.add_edge(0, 4, 'ID')
Factor.add_edge(4, 3, Varcallprime)

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
    index = 0
    while scanner.get_next_token(index) != "END":
        by = scanner.get_next_token(index)
        print(by)
        path = []
        Program.traversal(by, path)
        file = open("pathes.txt", "a")
        file.write(f"{path}\n")
        file.close()
        # print(path)
        if (path[0] != 'epsilon'):
            index += 1

    Program.print_tree()
    syntax = open('syntax_errors.txt', 'w')
    syntax.write('There is no syntax error.')
    syntax.close()
