class TransitionDiagram:
    def __init__(self):
        self.terminal_nodes = set()

    def add_node(self,
                 node_id: int,
                 is_starter: bool = True,
                 is_terminal: bool = False):
        pass

    def add_edge(self, from_node: int, to_node: int, by: str):
        pass


Addop = TransitionDiagram()
Addop.add_node(0)
Addop.add_node(1, False, True)
Addop.add_edge(0, 1, '+')
Addop.add_edge(0, 1, '-')

Relop = TransitionDiagram()
Relop.add_node(0)
Relop.add_node(1, False, True)
Relop.add_edge(0, 1, '<')
Relop.add_edge(0, 1, '==')

Paramprime = TransitionDiagram()
Paramprime.add_node(0)
Paramprime.add_node(1, False)
Paramprime.add_node(2, False, True)
Paramprime.add_edge(0, 1, '[')
Paramprime.add_edge(1, 2, ']')
Paramprime.add_edge(0, 2, 'EPSILON')

Typespecifier = TransitionDiagram()
Typespecifier.add_node(0)
Typespecifier.add_node(1, False, True)
Typespecifier.add_edge(0, 1, 'int')
Typespecifier.add_edge(0, 1, 'void')

Vardeclarationprime = TransitionDiagram()
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
