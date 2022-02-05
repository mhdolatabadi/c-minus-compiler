from anytree import Node as TreeNode, RenderTree
import json
from codegen import CodeGen
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
    global token
    global index
    if index == None:
        index = 0
    token = scanner.get_next_token(index)
    index += 1


grammer = json.load(open('./data/grammer.json', 'r'))
code_gen = CodeGen()

class Action:
    def __init__(self, name, expected_token: str = None):
        self.name = name
        self.expected_token = expected_token

class Edge:
    def __init__(
        self,
        src,
        token,
        dst,
    ):
        self.src = src
        self.token = token
        self.dst = dst




class Node:
    def __init__(self, node_id, is_terminal, actions):
        self.node_id = node_id
        self.is_terminal = is_terminal
        self.edges = []
        self.actions = actions
    
    def run_actions(self):
        if self.actions:
            for action in self.actions:
                if (token.lexeme == action.expected_token or
                 token.type == action.expected_token or
                  not action.expected_token):
                    code_gen.run(action.name, token)

class TransitionDiagram:
    EOF = False

    def __init__(self, name: str):
        self.nodes = []
        self.nodes_edges = dict()
        self.terminal_node = 0
        self.name = name
        self.firsts = grammer[name.replace('-', '')]['firsts']
        self.follows = grammer[name.replace('-', '')]['follows']
    
    def print_tree(self, root):
        for pre, fill, node in RenderTree(root):
            write_parse_tree("%s%s" % (pre, node.name))

    def add_node(
        self,
        node_id: int,
        is_terminal: bool = False,
        actions: Action = None
    ):
        node = Node(node_id, is_terminal, actions)
        self.nodes.append(node)

    def get_node_by_id(self, node_id: int) -> Node:
        for node in self.nodes:
            if node.node_id == node_id:
                return node

    def add_edge(
        self,
        src: int,
        dst: int,
        token,
    ):
        node = self.get_node_by_id(src)
        node.edges.append(Edge(src, token, dst))

    def traversal(
        self,
        errors,
        parent_node: TreeNode = TreeNode('God'),
        current_node_id: int = 0
    ):
        if errors and 'Unexpected' in errors[-1]:
            return
        
        value = token.type if token.type in [
            'NUM', 'ID'
        ] else token.lexeme

        leaf_name = f"({token.type}, {token.lexeme})" if value != '$' else value

        current_node = self.get_node_by_id(current_node_id)
        current_node.run_actions()



        tree_node = TreeNode(
            self.name
        ) if current_node_id == 0 and self.name != 'Program' else parent_node

        
        for edge in current_node.edges:
            if type(edge.token) == TransitionDiagram and (
                    value in edge.token.firsts or
                ('EPSILON' in edge.token.firsts and value in edge.token.follows)):

                result = edge.token.traversal(errors, tree_node)

                if not self.get_node_by_id(edge.dst).is_terminal:
                    self.traversal(errors, tree_node, edge.dst)
                else:
                    self.get_node_by_id(edge.dst).run_actions()

                if current_node_id == 0 and self.name != 'Program' and result:
                    tree_node.parent = parent_node

                return True

            if edge.token == token.lexeme or (edge.token in ['NUM', 'ID']
                                           and token.type == edge.token):

                TreeNode(leaf_name, tree_node)

                next_token()

                if not self.get_node_by_id(edge.dst).is_terminal:
                    self.traversal(errors, tree_node, edge.dst)
                else:
                    self.get_node_by_id(edge.dst).run_actions()


                if current_node_id == 0:
                    tree_node.parent = parent_node

                return True

            if edge.token == 'EPSILON':

                TreeNode('epsilon', tree_node)
                tree_node.parent = parent_node

                return True

        #syntax errors
        for edge in current_node.edges:
            line_number = scanner.get_line_number()
            if value == '$' and type(edge.token) == TransitionDiagram:
                errors.append(
                    f'#{line_number + 1} : syntax error, Unexpected EOF'
                )
                return False

            if edge.token != value and type(edge.token) != TransitionDiagram:
                errors.append(
                    f'#{line_number} : syntax error, missing {edge.token}'
                )
                return self.traversal(errors, parent_node, edge.dst)
            if value in edge.token.follows or value in self.follows:

                errors.append(
                    f'#{line_number} : syntax error, missing {edge.token.name}'
                )

                return self.traversal(errors, parent_node, edge.dst)

            if value not in self.follows:
                errors.append(
                    f'#{line_number} : syntax error, illegal {value}'
                )
                next_token()
                return self.traversal(errors, parent_node, current_node_id)


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


Declarationlist.add_node(0)
Declarationlist.add_node(1)
Declarationlist.add_node(2, True)
Declarationlist.add_edge(0, 1, Declaration)
Declarationlist.add_edge(1, 2, Declarationlist)
Declarationlist.add_edge(0, 2, 'EPSILON')

Declaration.add_node(0)
Declaration.add_node(1)
Declaration.add_node(2, True)
Declaration.add_edge(0, 1, Declarationinitial)
Declaration.add_edge(1, 2, Declarationprime)

Declarationinitial.add_node(0)
Declarationinitial.add_node(1, False, [Action('#pid', 'ID')])
Declarationinitial.add_node(2, True)
Declarationinitial.add_edge(0, 1, Typespecifier)
Declarationinitial.add_edge(1, 2, 'ID')

Declarationprime.add_node(0)
Declarationprime.add_node(1, True)
Declarationprime.add_edge(0, 1, Fundeclarationprime)
Declarationprime.add_edge(0, 1, Vardeclarationprime)

Vardeclarationprime.add_node(0, False, [Action('#declare_id', ';')])
Vardeclarationprime.add_node(1, False, [Action('#pnum', 'NUM')])
Vardeclarationprime.add_node(2)
Vardeclarationprime.add_node(3, False, [Action('#declare_arr', ';')])
Vardeclarationprime.add_node(4, True)
Vardeclarationprime.add_edge(0, 4, ';')
Vardeclarationprime.add_edge(0, 1, '[')
Vardeclarationprime.add_edge(1, 2, 'NUM')
Vardeclarationprime.add_edge(2, 3, ']')
Vardeclarationprime.add_edge(3, 4, ';')

Fundeclarationprime.add_node(0, False, [Action('#declare_func', '(')])
Fundeclarationprime.add_node(1)
Fundeclarationprime.add_node(2)
Fundeclarationprime.add_node(3, False, [Action('#scope_start')])
Fundeclarationprime.add_node(4, True, [Action('#scope_end')])
Fundeclarationprime.add_edge(0, 1, '(')
Fundeclarationprime.add_edge(1, 2, Params)
Fundeclarationprime.add_edge(2, 3, ')')
Fundeclarationprime.add_edge(3, 4, Compoundstmt)

Typespecifier.add_node(0)
Typespecifier.add_node(1, True)
Typespecifier.add_edge(0, 1, 'int')
Typespecifier.add_edge(0, 1, 'void')

Params.add_node(0)
Params.add_node(1, False, [Action('#pid', 'ID')])
Params.add_node(2)
Params.add_node(3)
Params.add_node(4, True)
Params.add_edge(0, 1, 'int')
Params.add_edge(1, 2, 'ID')
Params.add_edge(2, 3, Paramprime)
Params.add_edge(3, 4, Paramlist)
Params.add_edge(0, 4, 'void')

Paramlist.add_node(0)
Paramlist.add_node(1)
Paramlist.add_node(2)
Paramlist.add_node(3, True)
Paramlist.add_edge(0, 1, ',')
Paramlist.add_edge(1, 2, Param)
Paramlist.add_edge(2, 3, Paramlist)
Paramlist.add_edge(0, 3, 'EPSILON')

Param.add_node(0)
Param.add_node(1)
Param.add_node(2, True)
Param.add_edge(0, 1, Declarationinitial)
Param.add_edge(1, 2, Paramprime)

Paramprime.add_node(0, False, [Action('#declare_id_parameter', 'EPSILON')])
Paramprime.add_node(1, False, [Action('#declare_array_parameter', ']')])
Paramprime.add_node(2, True)
Paramprime.add_edge(0, 1, '[')
Paramprime.add_edge(1, 2, ']')
Paramprime.add_edge(0, 2, 'EPSILON')

Compoundstmt.add_node(0)
Compoundstmt.add_node(1)
Compoundstmt.add_node(2)
Compoundstmt.add_node(3)
Compoundstmt.add_node(4, True)
Compoundstmt.add_edge(0, 1, '{')
Compoundstmt.add_edge(1, 2, Declarationlist)
Compoundstmt.add_edge(2, 3, Statementlist)
Compoundstmt.add_edge(3, 4, '}')

Statementlist.add_node(0)
Statementlist.add_node(1)
Statementlist.add_node(2, True)
Statementlist.add_edge(0, 1, Statement)
Statementlist.add_edge(1, 2, Statementlist)
Statementlist.add_edge(0, 2, 'EPSILON')

Statement.add_node(0)
Statement.add_node(1, True)
Statement.add_edge(0, 1, Iterationstmt)
Statement.add_edge(0, 1, Selectionstmt)
Statement.add_edge(0, 1, Compoundstmt)
Statement.add_edge(0, 1, Returnstmt)
Statement.add_edge(0, 1, Expressionstmt)

Expressionstmt.add_node(0)
Expressionstmt.add_node(1)
Expressionstmt.add_node(2, True)
Expressionstmt.add_edge(0, 1, Expression)
Expressionstmt.add_edge(1, 2, ';')
Expressionstmt.add_edge(0, 1, 'break')
Expressionstmt.add_edge(1, 2, ';')
Expressionstmt.add_edge(0, 2, ';')

Selectionstmt.add_node(0)
Selectionstmt.add_node(1)
Selectionstmt.add_node(2)
Selectionstmt.add_node(3)
Selectionstmt.add_node(4)
Selectionstmt.add_node(5)
Selectionstmt.add_node(6, True)
Selectionstmt.add_edge(0, 1, 'if')
Selectionstmt.add_edge(1, 2, '(')
Selectionstmt.add_edge(2, 3, Expression)
Selectionstmt.add_edge(3, 4, ')')
Selectionstmt.add_edge(4, 5, Statement)
Selectionstmt.add_edge(5, 6, Elsestmt)

Elsestmt.add_node(0)
Elsestmt.add_node(1)
Elsestmt.add_node(2)
Elsestmt.add_node(3, True)
Elsestmt.add_edge(0, 3, 'endif')
Elsestmt.add_edge(0, 1, 'else')
Elsestmt.add_edge(1, 2, Statement)
Elsestmt.add_edge(2, 3, 'endif')

Iterationstmt.add_node(0)
Iterationstmt.add_node(1)
Iterationstmt.add_node(2)
Iterationstmt.add_node(3)
Iterationstmt.add_node(4)
Iterationstmt.add_node(5)
Iterationstmt.add_node(6, True)
Iterationstmt.add_edge(0, 1, 'repeat')
Iterationstmt.add_edge(1, 2, Statement)
Iterationstmt.add_edge(2, 3, 'until')
Iterationstmt.add_edge(3, 4, '(')
Iterationstmt.add_edge(4, 5, Expression)
Iterationstmt.add_edge(5, 6, ')')

Returnstmt.add_node(0)
Returnstmt.add_node(1)
Returnstmt.add_node(2, True)
Returnstmt.add_edge(0, 1, 'return')
Returnstmt.add_edge(1, 2, Returnstmtprime)

Returnstmtprime.add_node(0)
Returnstmtprime.add_node(1)
Returnstmtprime.add_node(2, True)
Returnstmtprime.add_edge(0, 1, Expression)
Returnstmtprime.add_edge(1, 2, ';')
Returnstmtprime.add_edge(0, 2, ';')

Expression.add_node(0, False, [Action('#pid', 'ID')])
Expression.add_node(1)
Expression.add_node(2, True)
Expression.add_edge(0, 2, Simpleexpressionzegond)
Expression.add_edge(0, 1, 'ID')
Expression.add_edge(1, 2, B)

B.add_node(0)
B.add_node(1)
B.add_node(2, True, [Action('#assign')])
B.add_node(3)
B.add_node(4)
B.add_node(5)
B.add_node(6, True)
B.add_node(7, True)
B.add_edge(0, 1, '=')
B.add_edge(1, 2, Expression)
B.add_edge(0, 3, '[')
B.add_edge(3, 4, Expression)
B.add_edge(4, 5, ']')
B.add_edge(5, 6, H)
B.add_edge(0, 7, Simpleexpressionprime)

H.add_node(0)
H.add_node(1)
H.add_node(2, True, [Action('#assign')])
H.add_node(3)
H.add_node(4)
H.add_node(5, True)
H.add_edge(0, 1, '=')
H.add_edge(1, 2, Expression)
H.add_edge(0, 3, G)
H.add_edge(3, 4, D)
H.add_edge(4, 5, C)

Simpleexpressionzegond.add_node(0)
Simpleexpressionzegond.add_node(1)
Simpleexpressionzegond.add_node(2, True)
Simpleexpressionzegond.add_edge(0, 1, Additiveexpressionzegond)
Simpleexpressionzegond.add_edge(1, 2, C)

Simpleexpressionprime.add_node(0)
Simpleexpressionprime.add_node(1)
Simpleexpressionprime.add_node(2, True)
Simpleexpressionprime.add_edge(0, 1, Additiveexpressionprime)
Simpleexpressionprime.add_edge(1, 2, C)

C.add_node(0)
C.add_node(1)
C.add_node(2, True, [Action('#exec_op')])
C.add_node(3, True)
C.add_edge(0, 1, Relop)
C.add_edge(1, 2, Additiveexpression)
C.add_edge(0, 3, 'EPSILON')

Relop.add_node(0, False, [Action('#push_op')])
Relop.add_node(1, True)
Relop.add_edge(0, 1, '<')
Relop.add_edge(0, 1, '==')

Additiveexpression.add_node(0)
Additiveexpression.add_node(1)
Additiveexpression.add_node(2, True)
Additiveexpression.add_edge(0, 1, Term)
Additiveexpression.add_edge(1, 2, D)

Additiveexpressionprime.add_node(0)
Additiveexpressionprime.add_node(1)
Additiveexpressionprime.add_node(2, True)
Additiveexpressionprime.add_edge(0, 1, Termprime)
Additiveexpressionprime.add_edge(1, 2, D)

Additiveexpressionzegond.add_node(0)
Additiveexpressionzegond.add_node(1)
Additiveexpressionzegond.add_node(2, True)
Additiveexpressionzegond.add_edge(0, 1, Termzegond)
Additiveexpressionzegond.add_edge(1, 2, D)

D.add_node(0)
D.add_node(1)
D.add_node(2, False, [Action('#exec_op')])
D.add_node(3, True)
D.add_edge(0, 1, Addop)
D.add_edge(1, 2, Term)
D.add_edge(2, 3, D)
D.add_edge(0, 3, 'EPSILON')

Addop.add_node(0, False, [Action('#push_op')])
Addop.add_node(1, True)
Addop.add_edge(0, 1, '+')
Addop.add_edge(0, 1, '-')

Term.add_node(0)
Term.add_node(1)
Term.add_node(2, True)
Term.add_edge(0, 1, Factor)
Term.add_edge(1, 2, G)

Termprime.add_node(0)
Termprime.add_node(1)
Termprime.add_node(2, True)
Termprime.add_edge(0, 1, Factorprime)
Termprime.add_edge(1, 2, G)

Termzegond.add_node(0)
Termzegond.add_node(1)
Termzegond.add_node(2, True)
Termzegond.add_edge(0, 1, Factorzegond)
Termzegond.add_edge(1, 2, G)

G.add_node(0, False, [Action('#push_op', '*')])
G.add_node(1)
G.add_node(2, False, [Action('#exec_op')])
G.add_node(3, True)
G.add_edge(0, 1, '*')
G.add_edge(1, 2, Factor)
G.add_edge(2, 3, G)
G.add_edge(0, 3, 'EPSILON')

Factor.add_node(0, False, [Action('#pid', 'ID'), Action('#pnum', 'NUM')])
Factor.add_node(1)
Factor.add_node(2)
Factor.add_node(3)
Factor.add_node(4, True)
Factor.add_edge(0, 1, '(')
Factor.add_edge(1, 2, Expression)
Factor.add_edge(2, 4, ')')
Factor.add_edge(0, 4, 'NUM')
Factor.add_edge(0, 3, 'ID')
Factor.add_edge(3, 4, Varcallprime)

Varcallprime.add_node(0)
Varcallprime.add_node(1)
Varcallprime.add_node(2)
Varcallprime.add_node(3, True)
Varcallprime.add_edge(0, 1, '(')
Varcallprime.add_edge(1, 2, Args)
Varcallprime.add_edge(2, 3, ')')
Varcallprime.add_edge(0, 3, Varprime)

Varprime.add_node(0)
Varprime.add_node(1)
Varprime.add_node(2)
Varprime.add_node(3, True)
Varprime.add_edge(0, 1, '[')
Varprime.add_edge(1, 2, Expression)
Varprime.add_edge(2, 3, ']')
Varprime.add_edge(0, 3, 'EPSILON')

Factorprime.add_node(0)
Factorprime.add_node(1)
Factorprime.add_node(2)
Factorprime.add_node(3, True)
Factorprime.add_edge(0, 1, '(')
Factorprime.add_edge(1, 2, Args)
Factorprime.add_edge(2, 3, ')')
Factorprime.add_edge(0, 3, 'EPSILON')

Factorzegond.add_node(0, False, [Action('#pnum', 'NUM')])
Factorzegond.add_node(1)
Factorzegond.add_node(2)
Factorzegond.add_node(3, True)
Factorzegond.add_edge(0, 1, '(')
Factorzegond.add_edge(1, 2, Expression)
Factorzegond.add_edge(2, 3, ')')
Factorzegond.add_edge(0, 3, 'NUM')

Args.add_node(0)
Args.add_node(1, True)
Args.add_edge(0, 1, Arglist)
Args.add_edge(0, 1, 'EPSILON')

Arglist.add_node(0)
Arglist.add_node(1)
Arglist.add_node(2, True)
Arglist.add_edge(0, 1, Expression)
Arglist.add_edge(1, 2, Arglistprime)

Arglistprime.add_node(0)
Arglistprime.add_node(1)
Arglistprime.add_node(2)
Arglistprime.add_node(3, True)
Arglistprime.add_edge(0, 1, ',')
Arglistprime.add_edge(1, 2, Expression)
Arglistprime.add_edge(2, 3, Arglistprime)
Arglistprime.add_edge(0, 3, 'EPSILON')

Program.add_node(0)
Program.add_node(1)
Program.add_node(2, True)
Program.add_edge(0, 1, Declarationlist)
Program.add_edge(1, 2, '$')

def run():
    next_token()
    errors = list()
    node = TreeNode('Program')
    Program.traversal(errors, node)
    Program.print_tree(node)
    if errors:
        for error in errors:
            write_syntax_error(error)
            if 'Unexpected' in error:
                break
    else:
        write_syntax_error('There is no syntax error.')

    code_gen.write_to_output()
