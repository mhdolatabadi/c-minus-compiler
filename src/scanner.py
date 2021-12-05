# the input to the compiler (through a file called input.txt) includes C-minus program.
# get_next_token should return (Token Type, Token String).
# while loop call get_next_token.
# tokens must be saved in tokens.txt each line has a number corresponds to a line number in the input file.
# input includes only ASCII characters.
# scanner should be robust and work for any conceivable input.
# Handle errors such as:
#    1. illegal character appearing in the input stream(with the exception of comments, which may include any character)
#    2. ill-formed number such as '125d'.
#    3. also make some preparations for a graceful termination in the case of a fatal error.
#    * Uncaught exceptions are not acceptable

# All token types that scanner must be able to recognize:
#    NUM: Any string matching: [0-9]+
#    ID: Any string matching: [A-Za-z][A-Za-z0-9]*
#    KEYWORD: if, else, void, int, repeat, break, until, return
#    SYMBOL: ; : , [] () {} + - * = < ==
#    COMMENT: Any string between a /* and a */ OR any string after a // and before a \n or EOF
#    WHITESPACE: blank(ASCII 32), \n(ASCII 10), \r(ASCII 13), \t(ASCII 9), \v(ASCII 11), \f(ASCII 12)

# Lexical errors must be recorded in a text file called 'lexical_errors.txt'. each error is reported on a separate
# line as a pair including string and a message with the line number. if the input program lexically correct,
# sentence 'There is no lexical error.' should be written. * when an invalid character is encountered,
# a string containing just that character and the message 'Invalid input' should be saved in file. * if comment
# remains open when end of the input file is countered, record this with just the message 'Unclosed comment'. it is
# sufficient to print at most the first seven characters of the unclosed comment with three dots. * if there is a
# '*/' outside a comment, scanner should report this errors as 'Unmatched comment' rather than tokenizing it as * and
# /. * if you see '125d', you must report this error as 'Invalid number' rather than tokenizing it as a NUM and a ID.
# * the scanner should recognize tokens with at most one lookahead character.

# Scanner should maintain a variable that indicates which line of the input text is currently being scanned. this
# variable is changed whenever scanner reads a new line symbol (\n). there is no need to record or report COMMENT and
# WHITESPACE tokens.

# This is scanner module of compiler.

# class DFA:
#     def __init__(self):
#         self.terminal_nodes = set()
#         self.refeed_nodes = set()

#     def add_node(self, node_id: int, is_terminal:bool, token_type: str, is_refeeder: bool):
#         if is_terminal:
#             self.terminal_nodes.add(node_id)
#         self.token_type[node_id] = token_type
#         if is_refeeder:
#             self.refeed_nodes.add(node_id)
#         self.nodes_edges[node_id] = dict()

#     def add_edge(self, from_node: int, to_node: int, chars: typing.Set):
#         edges_dict = self.nodes_edges[from_node]
#         for char in chars:
#             edges_dict[char] = to_node

#     def add_non_sigma_edge(self, from_node: int, to_node: int):
#         self.non_sigma_edges[from_node] = to_node

#     def init_traversal(self, start_node: int):
#         self.reset_node = start_node
#         self.current_node = start_node

import re

KEYWORD = r"if|else|void|int|repeat|break|until|return"
SYMBOL = r" ; | : | , | \[ | \] | \( | \) | { | } | \+ | - | \* | = | < | == "
NUMBER = r"[0-9]+"
IDENTIFIER = r"[A-Za-z][A-Za-z0-9]*"
COMMENT = r"(\/\*.*?\*\/)|(\/{2}.*?\n)"
WHITESPACE = r"\s"


class DFA:
    def __init__(self):
        self.terminal_nodes = set()
        self.nodes_edges = dict()
        self.token_type = dict()

    def add_node(self,
                 node_id: int,
                 is_terminal: bool,
                 token_type: str = "NOTHING"):
        if is_terminal:
            self.terminal_nodes.add(node_id)
        self.nodes_edges[node_id] = dict()
        if token_type:
            self.token_type[node_id] = token_type

    def add_edge(self, from_node: int, to_node: int, chars: str):
        for char in chars:
            self.nodes_edges[from_node][char] = to_node

    def get_next_state(self, state: int, char: str):
        next_state = self.nodes_edges[state][char]
        if next_state in self.terminal_nodes:
            return self.token_type[next_state]
        else:
            return next_state


letter = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
digit = "0123456789"
symbol = ";:,[({])}+-*=<"

dfa = DFA()
#start

#id or keyword
dfa.add_node(0, False)
dfa.add_edge(0, 1, letter)
dfa.add_node(1, False)
dfa.add_edge(1, 1, letter + digit)
dfa.add_node(2, True, "WORD")
dfa.add_edge(1, 2, "@")

#numbers
dfa.add_node(3, False)
dfa.add_edge(0, 3, digit)
dfa.add_edge(3, 3, digit)
dfa.add_node(4, True, "NUMBER")
dfa.add_edge(3, 4, "@")

#symbols
dfa.add_node(5, True)
dfa.add_edge(0, 5, symbol)

# == and =
dfa.add_node(6, False)
dfa.add_edge(0, 6, "=")
dfa.add_node(7, False)
dfa.add_edge(6, 7, "=")
dfa.add_node(8, True)  # == and =
dfa.add_edge(6, 8, "@")
dfa.add_edge(7, 8, "@")

# one line comments
dfa.add_node(9, False)
dfa.add_node(10, False)
dfa.add_edge(0, 9, "/")
dfa.add_edge(9, 0, "@")
dfa.add_edge(9, 10, "/")
dfa.add_edge(10, 0, "@")
dfa.add_node(11, True, "COMMENT")  #comment
dfa.add_edge(10, 11, "\n")

# multiline comments
dfa.add_node(12, False)
dfa.add_edge(9, 12, "*")
dfa.add_edge(12, 12, "@")
dfa.add_node(13, False)
dfa.add_edge(12, 13, "*")
dfa.add_edge(13, 12, "@")
dfa.add_edge(13, 11, "/")

#whitespace
dfa.add_node(14, True, "WHITESPACE")
dfa.add_edge(0, 14, "\n\r\f\t\v ")

# def find_pattern(text, regex):
#     matches = re.findall(regex, text)
#     return matches


def get_next_token():
    pass


def run():
    input_file = open("input.txt")
    line_number = 1
    current_state = 0
    for line in input_file:
        for char in line:
            current_state = dfa.get_next_state(0, char)
            print(char, current_state)
        line_number += 1
    input_file.close()
