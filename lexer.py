"""
PA 5 dependency: paste in YOUR OWN completed PA 2 lexer.py here.
(Needed transitively -- symtable.py imports from parser.py, which
imports from this file. PA 5's own new work doesn't touch lexing or
parsing directly.)

This is the same file from PA 2's repo -- copy your own working
tokenize() implementation over this stub before starting parser.py.
Every PA repo is independent (no shared filesystem across repos), so
each pipeline stage bundles its own copy of the prior stages.

Complete tokenize() below. See the assignment, Part B,
for the full requirements. Must use a single compiled master regex
with named groups -- not a hand-rolled character-by-character loop.
"""

import re
from dataclasses import dataclass
from typing import List


@dataclass
class Token:
    type: str
    lexeme: str
    line: int


class LexError(Exception):
    pass


# TODO: build your master regex here, e.g.:
# _MASTER_RE = re.compile(r"(?P<NUMBER>\d+)|(?P<IDENT>[A-Za-z_]\w*)|...")
MASTER_PATTERN = re.compile(

r"(?P<LET>\blet\b)" #Very important to check for let first, otherwise it will be recognized as an identifier
r"(?P<NUMBER>[0-9]+(\.[0-9]+)?)"
r"|(?P<IDENT>[a-zA-Z_][a-zA-Z0-9_]*)"
r"|(?P<PLUS>\+)|(?P<MINUS>-)|(?P<STAR>\*)|(?P<SLASH>/)"
r"|(?P<LPAREN>\()|(?P<RPAREN>\))|(?P<ASSIGN>=)|(?P<SEMI>;)"
r"|(?P<COMMENT>#.*)|(?P<NEWLINE>\n)|(?P<WHITESPACE>[ \t]+)|(?P<EOF>$ )"
)


def tokenize(source: str) -> List[Token]:
    """
    Convert `source` into a list of Token objects, ending in an EOF
    token with an empty lexeme. Recognize NUMBER, IDENT, LET, PLUS,
    MINUS, STAR, SLASH, LPAREN, RPAREN, ASSIGN, SEMI. Discard
    whitespace and '#'-prefixed comments without emitting tokens for
    them. Track 1-indexed line numbers. Raise LexError (with the
    offending character and line) on unrecognized input.
    """
    # TODO
    tokens_specifications = [
        ("LET", r"let"), #Check Let first! (Cost me 3 hours of extra work because I forgot to check for let first, and it was being recognized as an identifier)
        ("IDENT", r"[A-Za-z_][A-Za-z0-9_]*"),
        ("NUMBER", r"\d+"),
        ("PLUS", r"\+"),
        ("MINUS", r"-"),
        ("STAR", r"\*"),
        ("SLASH", r"/"),
        ("LPAREN", r"\("),
        ("RPAREN", r"\)"),
        ("ASSIGN", r"="),
        ("SEMI", r";"),
        ("COMMENT", r"#.*"),
        ("WHITESPACE", r"[ \t]+"),
        ("NEWLINE", r"\n"),
        ("SKIP", r"[ \t]+"),
        ("MISMATCH", r"."),  # Any other character
        ("EOF", r"$"), # End of File
    ]
    token_regex = "|".join(f"(?P<{name}>{pattern})" for name, pattern in tokens_specifications)
    line_num = 1
    tokens = []

    for match in re.finditer(token_regex, source):
        kind = match.lastgroup
        value = match.group()

        if kind == "NEWLINE":
            line_num += 1
        elif kind == "WHITESPACE" or kind == "COMMENT":
            continue
        elif kind == "MISMATCH":
            raise LexError(f"Unexpected character {value!r} on line {line_num}")
        else:
            tokens.append(Token(kind, value, line_num))

    tokens.append(Token("EOF", "", line_num))
    return tokens
    #raise NotImplementedError
