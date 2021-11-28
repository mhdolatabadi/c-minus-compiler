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

import re

KEYWORD = r"if|else|void|int|repeat|break|until|return"
SYMBOL = r";|:|,|\[|\]|\(|\)|{|}|\+|-|\*|=|<|=="
NUMBER = r"[0-9]+"
IDENTIFIER = r"[A-Za-z][A-Za-z0-9]*"
COMMENT = r"(\/\*.*?\*\/)|(\/{2}.*?\n)"
WHITESPACE = r"\s"


def find_pattern(text, regex):
    matches = re.findall(regex, text)
    return matches


def get_next_token():
    pass


def run():
    input_file = open("input.txt")
    line_number = 1
    for line in input_file:
        print("=================> line_number: ", line_number, " <================")
        print("keywords: ", find_pattern(line, KEYWORD))
        print("symbols: ", find_pattern(line, SYMBOL))
        print("numbers: ", find_pattern(line, NUMBER))
        print("identifiers: ", find_pattern(line, IDENTIFIER))
        print("comments: ", find_pattern(line, COMMENT))
        print("whitespaces: ", find_pattern(line, WHITESPACE))
        line_number += 1
    input_file.close()
