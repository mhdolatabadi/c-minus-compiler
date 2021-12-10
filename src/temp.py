import scanner


class TransitionDiagram:
    def __init__(self, name):
        self.nodes_edges = dict()
        self.current_node = 0
        self.terminal_node = 0
        self.name = name

    def add_node(self,
                 node_id: int,
                 is_starter: bool = True,
                 is_terminal: bool = False):
        self.nodes_edges[node_id] = dict()
        if is_terminal:
            self.terminal_node = node_id

    def add_edge(self, from_node: int, to_node: int, by):
        self.nodes_edges[from_node][by] = to_node

    def traversal(self, char: str, path):
        file = open("traversal.txt", "a")
        file.write(f"{char['value']} {self.name} {self.current_node}\n")
        file.close()
        print(self.name, self.current_node)
        for i in range(self.current_node, len(self.nodes_edges)):
            edge = self.nodes_edges[i]
            for j in edge:
                if j == char['value']:
                    path.append(f"({char['token_type']}, {char['value']})")
                    path.append(self.name)
                    if edge[j] == self.terminal_node:
                        file = open("traversal.txt", "a")
                        file.write(f"this is fuck {char['value']}\n")
                        file.close()
                        self.current_node = 0
                        return True
                    else:
                        return 14
                if type(j) == TransitionDiagram:
                    temp = self.current_node
                    self.current_node = 0
                    result = j.traversal(char, path)
                    self.current_node = temp
                    if (result == 14):
                        path.append(self.name)
                        return 14
                    elif (result):
                        path.append(self.name)
                        if edge[j] == self.terminal_node:
                            self.current_node = 0
                            return True
                        else:
                            self.current_node += 1
                            file = open("traversal.txt", "a")
                            file.write(f"{self.name} increase current node\n")
                            file.close()
                            return 14

                if j in ['EPSILON', 'NUM', 'ID']:
                    if (char['token_type'] == j):
                        path.append(f"({char['token_type']}, {char['value']})")
                        path.append(self.name)
                        if edge[j] == self.terminal_node:
                            file = open("traversal.txt", "a")
                            file.write(f"this is fuck {char['value']}\n")
                            file.close()
                            self.current_node = 0
                            return True
                        else:
                            return 14
                file = open("traversal.txt", "a")
                file.write(f"{self.name} {j} break\n")
                file.close()
                self.current_node += 1
        return False


Paramprime = TransitionDiagram("Paramprime")
Param = TransitionDiagram("Param")
Paramlist = TransitionDiagram("Paramlist")
Params = TransitionDiagram("Params")
Vardeclarationprime = TransitionDiagram("Vardeclarationprime")
Fundeclarationprime = TransitionDiagram("Fundeclarationprime")
Typespecifier = TransitionDiagram("Typespecifier")
Declarationprime = TransitionDiagram("Declarationprime")
Declarationinitial = TransitionDiagram("Declarationinitial")
Declaration = TransitionDiagram("Declaration")
Declarationlist = TransitionDiagram("Declarationlist")
Compoundstmt = TransitionDiagram("Compoundstmt")
Statementlist = TransitionDiagram("Statementlist")
Statement = TransitionDiagram("Statement")
Expressionstmt = TransitionDiagram("Expressionstmt")
Selectionstmt = TransitionDiagram("Selectionstmt")
Elsestmt = TransitionDiagram("Elsestmt")
Iterationstmt = TransitionDiagram("Iterationstmt")
Returnstmt = TransitionDiagram("Returnstmt")
Returnstmtprime = TransitionDiagram("Returnstmtprime")
Expression = TransitionDiagram("Expression")
B = TransitionDiagram("B")
H = TransitionDiagram("H")
Simpleexpressionzegond = TransitionDiagram("Simpleexpressionzegond")
Simpleexpressionprime = TransitionDiagram("Simpleexpressionprime")
C = TransitionDiagram("C")
Relop = TransitionDiagram("Relop")
Additiveexpression = TransitionDiagram("Additiveexpression")
Additiveexpressionprime = TransitionDiagram("Additiveexpressionprime")
Additiveexpressionzegond = TransitionDiagram("Additiveexpressionzegond")
D = TransitionDiagram("D")
Addop = TransitionDiagram("Addop")
Term = TransitionDiagram("Term")
Termprime = TransitionDiagram("Termprime")
Termzegond = TransitionDiagram("Termzegond")
G = TransitionDiagram("G")
Factor = TransitionDiagram("Factor")
Varcallprime = TransitionDiagram("Varcallprime")
Varprime = TransitionDiagram("Varprime")
Factorprime = TransitionDiagram("Factorprime")
Factorzegond = TransitionDiagram("Factorzegond")
Args = TransitionDiagram("Args")
Arglist = TransitionDiagram("Arglist")
Arglistprime = TransitionDiagram("Arglistprime")
Program = TransitionDiagram("Program")

Paramprime.add_node(0)
Paramprime.add_node(1, False)
Paramprime.add_node(2, False)
Paramprime.add_node(3, False, True)
Paramprime.add_edge(0, 1, '[')
Paramprime.add_edge(1, 2, ']')
Paramprime.add_edge(0, 2, 'EPSILON')

Param.add_node(0)
Param.add_node(1, False, True)
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
Vardeclarationprime.add_edge(0, 4, '[')
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
Declarationlist.add_node(2, False)
Declarationlist.add_node(3, False, True)
Declarationlist.add_edge(0, 1, Declaration)
Declarationlist.add_edge(1, 2, Declarationlist)
Declarationlist.add_edge(2, 3, 'EPSILON')

Compoundstmt.add_node(0)
Compoundstmt.add_node(1, False)
Compoundstmt.add_node(2, False)
Compoundstmt.add_node(3, False, True)
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
Statement.add_edge(0, 1, Expressionstmt)
Statement.add_edge(0, 1, Compoundstmt)
Statement.add_edge(0, 1, Selectionstmt)
Statement.add_edge(0, 1, Iterationstmt)
Statement.add_edge(0, 1, Returnstmt)

Expressionstmt.add_node(0)
Expressionstmt.add_node(1, False)
Expressionstmt.add_node(2, False, True)
Expressionstmt.add_edge(0, 1, Expression)
Expressionstmt.add_edge(1, 2, ';')
Expressionstmt.add_edge(0, 1, 'break')
Expressionstmt.add_edge(1, 2, ';')
Expressionstmt.add_edge(0, 1, ';')

Selectionstmt.add_node(0)
Selectionstmt.add_node(1, False)
Selectionstmt.add_node(2, False)
Selectionstmt.add_node(3, False)
Selectionstmt.add_node(4, False)
Selectionstmt.add_node(5, False, True)
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
Returnstmt.add_node(1, False, True)
Returnstmt.add_edge(0, 1, 'return')
Returnstmt.add_edge(1, 2, Returnstmtprime)

Returnstmtprime.add_node(0)
Returnstmtprime.add_node(1, False)
Returnstmtprime.add_node(2, False, True)
Returnstmtprime.add_edge(0, 2, ';')
Returnstmtprime.add_edge(0, 1, Expression)
Returnstmtprime.add_edge(1, 2, ';')

Expression.add_node(0)
Expression.add_node(1, False, True)
Expression.add_edge(0, 1, Simpleexpressionzegond)
Expression.add_edge(0, 1, 'ID')
Expression.add_edge(1, 2, B)

B.add_node(0)
B.add_node(1, False)
B.add_node(2, False)
B.add_node(3, False)
B.add_node(4, False)
B.add_node(5, False, True)
B.add_edge(0, 4, '=')
B.add_edge(4, 5, Expression)
B.add_edge(0, 1, '[')
B.add_edge(1, 2, Expression)
B.add_edge(2, 3, ']')
B.add_edge(3, 5, H)
B.add_edge(0, 5, Simpleexpressionprime)

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
Simpleexpressionzegond.add_node(1, False, True)
Simpleexpressionzegond.add_edge(0, 1, Additiveexpressionzegond)
Simpleexpressionzegond.add_edge(1, 2, C)

Simpleexpressionprime.add_node(0)
Simpleexpressionprime.add_node(1, False, True)
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
Additiveexpression.add_node(1, False, True)
Additiveexpression.add_edge(0, 1, Term)
Additiveexpression.add_edge(1, 2, D)

Additiveexpressionprime.add_node(0)
Additiveexpressionprime.add_node(1, False, True)
Additiveexpressionprime.add_edge(0, 1, Termprime)
Additiveexpressionprime.add_edge(1, 2, D)

Additiveexpressionzegond.add_node(0)
Additiveexpressionzegond.add_node(1, False, True)
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
Term.add_node(1, False, True)
Term.add_edge(0, 1, Factor)
Term.add_edge(1, 2, G)

Termprime.add_node(0)
Termprime.add_node(1, False, True)
Termprime.add_edge(0, 1, Factorprime)
Termprime.add_edge(1, 2, G)

Termzegond.add_node(0)
Termzegond.add_node(1, False, True)
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
Factor.add_edge(0, 3, 'ID')
Factor.add_edge(3, 4, Varcallprime)
Factor.add_edge(0, 4, 'NUM')

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
Arglist.add_node(1, False, True)
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
        path = []
        print(by['value'])
        Program.traversal(by, path)
        file = open("pathes.txt", "a")
        file.write(f"{path}\n")
        file.close()
        print(path)
        index += 1
