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
# line as a pair including string and a message with the line number.
# * if the input program lexically correct, sentence 'There is no lexical error.' should be written.
# * when an invalid character is encountered, a string containing just that character and the message 'Invalid input' should be saved in file.
# * if comment remains open when end of the input file is countered, record this with just the message 'Unclosed comment'. it is
# sufficient to print at most the first seven characters of the unclosed comment with three dots.
# * if there is a '*/' outside a comment, scanner should report this errors as 'Unmatched comment' rather than tokenizing it as * and /.
# * if you see '125d', you must report this error as 'Invalid number' rather than tokenizing it as a NUM and a ID.
# * the scanner should recognize tokens with at most one lookahead character.

# Scanner should maintain a variable that indicates which line of the input text is currently being scanned. this
# variable is changed whenever scanner reads a new line symbol (\n). there is no need to record or report COMMENT and
# WHITESPACE tokens.

# This is scanner module of compiler.
import re

KEYWORD = r"if|else|void|int|repeat|break|until|return|endif"
SYMBOL = r" ; | : | , | \[ | \] | \( | \) | { | } | \+ | - | \* | = | < | == "
NUMBER = r"[0-9]+"
IDENTIFIER = r"[A-Za-z][A-Za-z0-9]*"
COMMENT = r"(\/\*.*?\*\/)|(\/{2}.*?\n)"
WHITESPACE = r"\s"

ignore_tokens = [
    "WHITESPACE", "NOTHING", "COMMENT", "UNCLOSED COMMENT",
    "UNMATCHED COMMENT", "INVALID NUMBER"
]


def token_type_enhancer(dfa, token_type: str):
    if token_type == "ID":
        if (re.match(KEYWORD, dfa.value)):
            return 'KEYWORD'
        else:
            dfa.identifiers.append(dfa.value)
    if (token_type == "ASSIGNMENT"):
        return "SYMBOL"
    return token_type


class DFA:
    def __init__(self):
        self.terminal_nodes = set()
        self.nodes_edges = dict()
        self.token_type = dict()
        self.value = ''
        self.tokens = dict()
        self.lexical_errors = dict()
        self.last_token = ''
        self.identifiers = list()
        self.line_number = 1

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

    def get_next_state(self,
                       current_state: int,
                       char: str,
                       line_number: int,
                       lookahead: bool = False):
        if (not self.value):
            self.line_number = line_number
        try:
            next_state = self.nodes_edges[current_state][char]
            token_type = self.token_type[next_state]
        except KeyError:
            self.value += char
            if not lookahead:
                #invalid input
                self.lexical_errors[
                    self.line_number] += f"({self.value}, Invalid input) "
            self.value = ''
            return 0
        if next_state == 0 and self.last_token not in [
                "UNMATCHED COMMENT", "COMMENT"
        ]:
            self.lexical_errors[
                self.line_number] += f"({self.value}, Invalid input) "
        if next_state in self.terminal_nodes:
            if self.last_token == "SYMBOL" and lookahead:
                return 0
            if token_type in ["SYMBOL", "COMMENT", "UNMATCHED COMMENT"]:
                self.value += char
            if token_type in [
                    "UNMATCHED COMMENT", "INVALID NUMBER", "UNCLOSED COMMENT"
            ]:
                if token_type == "UNCLOSED COMMENT":
                    self.lexical_errors[
                        self.
                        line_number] += f"({self.value[0:7]}..., {token_type.capitalize()}) "

                else:
                    self.lexical_errors[
                        self.
                        line_number] += f"({self.value}, {token_type.capitalize()}) "

            if token_type not in ignore_tokens:
                self.value = self.value.replace(" ", "")
                token_type = token_type_enhancer(self, token_type)
                if token_type == 'SYMBOL' and self.value[0] == '*':
                    self.value = '*'
                self.tokens[self.line_number].append({
                    'token_type': token_type,
                    'value': self.value
                })
            self.last_token = token_type
            self.value = ''
            return 0
        else:
            self.value += char
            return next_state


letter = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
digit = "0123456789"
symbol = ";:,[({])}+-=<"
whitespace = "\n\r\f\t\v "
legalchars = letter + digit + whitespace + symbol + "/" + "*"

dfa = DFA()

#id or keyword
dfa.add_node(0, False)
dfa.add_edge(0, 1, letter)
dfa.add_node(1, False)
dfa.add_edge(1, 1, letter + digit)
dfa.add_node(2, True, "ID")
dfa.add_edge(1, 2, legalchars.replace(letter + digit, ''))

#numbers
dfa.add_node(3, False)
dfa.add_edge(0, 3, digit)
dfa.add_edge(3, 3, digit)
dfa.add_node(4, True, "NUM")
dfa.add_edge(3, 4, whitespace + symbol + '~' + '*')

# invalid number
dfa.add_node(18, False)
dfa.add_edge(3, 18, letter)
dfa.add_node(19, True, 'INVALID NUMBER')
dfa.add_edge(18, 19, legalchars)

#symbols
dfa.add_node(5, True, "SYMBOL")
dfa.add_edge(0, 5, symbol)

# == and =
dfa.add_node(6, False)
dfa.add_edge(0, 6, "=")
dfa.add_node(7, False)
dfa.add_edge(6, 7, "=")
dfa.add_node(8, True, "ASSIGNMENT")  # == and =
dfa.add_edge(6, 8, legalchars.replace('=', ''))
dfa.add_edge(7, 8, legalchars)

# one line comments
dfa.add_node(9, False)
dfa.add_node(10, False)
dfa.add_edge(0, 9, "/")
dfa.add_edge(9, 0, legalchars.replace('/', ''))
dfa.add_edge(9, 10, "/")
dfa.add_edge(10, 10, legalchars + ".")
dfa.add_node(11, True, "COMMENT")  #comment
dfa.add_edge(10, 11, "\n")

# multiline comments
dfa.add_node(12, False)
dfa.add_edge(9, 12, "*")
dfa.add_edge(12, 12, legalchars.replace('*', '') + '@#%$')
dfa.add_node(17, True, "UNCLOSED COMMENT")
dfa.add_edge(12, 17, '~')
dfa.add_node(13, False)
dfa.add_edge(12, 13, "*")
dfa.add_edge(13, 12, legalchars.replace('/', ''))
dfa.add_edge(13, 11, "/")

#whitespace
dfa.add_node(14, True, "WHITESPACE")
dfa.add_edge(0, 14, "\n\r\f\t\v ")

#errors
#unmatched comment and * symbol handling
dfa.add_node(15, False)
dfa.add_edge(0, 15, "*")
dfa.add_node(16, True, "UNMATCHED COMMENT")
dfa.add_edge(15, 16, '/')
dfa.add_edge(15, 5, legalchars.replace('*', '').replace('/', ''))


def get_next_token(index: int):
    run()
    tokens = []
    for i in dfa.tokens:
        for j in dfa.tokens[i]:
            tokens.append(j)
    tokens.append({'token_type': 'EOF', 'value': '$'})
    try:
        return tokens[index]
    except:
        return "END"


def run():
    input_file = open("input.txt")
    line_number = 1
    current_state = 0
    for line in input_file:
        dfa.tokens[line_number] = []
        dfa.lexical_errors[line_number] = ""
        for char in line:
            current_state = dfa.get_next_state(current_state, char,
                                               line_number)
            # come back lookahead
            if (current_state == 0):
                current_state = dfa.get_next_state(current_state, char,
                                                   line_number, True)
        line_number += 1

    dfa.tokens[line_number] = []
    dfa.lexical_errors[line_number] = ""
    current_state = dfa.get_next_state(current_state, '~', line_number)
    input_file.close()

    token_file = open("tokens.txt", "w")
    for i in range(1, len(dfa.tokens) + 1):
        if (dfa.tokens[i]):
            # for structuring an string for line with number i
            writable = ""
            for token_dict in dfa.tokens[i]:
                # extract token dictionray key and value and append it to string which should be write in the file
                writable += f"({token_dict['token_type']}, {token_dict['value']}) "
            token_file.write(f"{i}.\t{writable}\n")

    token_file.close()

    lexical_file = open("lexical_errors.txt", "w")
    has_error = False
    for i in range(1, len(dfa.lexical_errors) + 1):
        if (dfa.lexical_errors[i]
                and not dfa.lexical_errors[i].__contains__("~")):
            has_error = True
            lexical_file.write(f"{i}.\t{dfa.lexical_errors[i]}\n")
    if (not dfa.lexical_errors or not has_error):
        lexical_file.write("There is no lexical error.")
    lexical_file.close()

    #symbol table
    symbol_file = open("symbol_table.txt", "w")
    keywords = [
        'if', 'else', 'void', 'int', 'repeat', 'break', 'until', 'return',
        'endif'
    ]
    # add keywords
    for i in range(1, len(keywords) + 1):
        symbol_file.write(f"{i}.\t{keywords[i - 1]}\n")
    # remove redundant elements from list
    dfa.identifiers = list(dict.fromkeys(dfa.identifiers))
    for i in range(1, len(dfa.identifiers) + 1):
        # [i - 1] because range starts with 1
        symbol_file.write(f"{i + len(keywords)}.\t{dfa.identifiers[i - 1]}\n")
    symbol_file.close()
