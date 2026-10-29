"""
PA 5 dependency: paste in YOUR OWN completed PA 3 parser.py here
(needed transitively -- symtable.py imports from this file).

Complete the parsing functions below. AST node types are already
defined -- do not modify them. See the assignment,
Part B, for the full requirements.
"""

from dataclasses import dataclass, field
from typing import List

from lexer import Token, tokenize


@dataclass
class Program:
    statements: list


@dataclass
class Declaration:
    name: str
    expr: object
    line: int


@dataclass
class Assignment:
    name: str
    expr: object
    line: int


@dataclass
class BinOp:
    op: str
    left: object
    right: object
    line: int


@dataclass
class Number:
    value: int
    line: int


@dataclass
class Variable:
    name: str
    line: int


class ParseError(Exception):
    pass


class _ParserState:
    """Given: a small cursor wrapper over the token list. Not required to use, but handy."""

    def __init__(self, tokens: List[Token]) -> None:
        self.tokens = tokens
        self.pos = 0

    def peek(self) -> Token:
        return self.tokens[self.pos]

    def advance(self) -> Token:
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def expect(self, type_: str) -> Token:
        tok = self.peek()
        if tok.type != type_:
            raise ParseError(f"Line {tok.line}: expected {type_}, found {tok.type} ({tok.lexeme!r}).")
        return self.advance()


def parse_factor(state: _ParserState):
    # TODO
    if state.peek() is None:
        raise ParseError("Unexpected end of input")
    if state.peek().type == "NUMBER":
        tok = state.advance()
        return Number(value=int(tok.lexeme), line=tok.line)
    elif state.peek().type == "IDENT":
        tok = state.advance()
        return Variable(name=tok.lexeme, line=tok.line)
    elif state.peek().type == "LPAREN":
        state.advance()  # consume '('
        expr = parse_expr(state)
        state.expect("RPAREN")  # expect ')'
        return expr
    else:
        raise ParseError(f"Line {state.peek().line}: Expected token of type NUMBER, IDENT, or LPAREN, but found {state.peek().type} ({state.peek().lexeme!r}).")

    raise NotImplementedError

#Multiplicationa and Division layer
def parse_term(state: _ParserState):
    # TODO
    left = parse_factor(state)
    while state.peek().type in ("STAR", "SLASH"):
        op_token = state.advance()
        right = parse_factor(state)
        left = BinOp(op=op_token.lexeme, left=left, right=right, line=op_token.line)
    return left
    raise NotImplementedError

#Plus and Minus Layer!
def parse_expr(state: _ParserState):
    # TODO
    left = parse_term(state)

    while state.peek().type in ("PLUS", "MINUS"):
        op_token = state.advance()
        right = parse_term(state)
        left = BinOp(op=op_token.lexeme, left=left, right=right, line=op_token.line)
    return left
    raise NotImplementedError

# Let there be light
def parse_declaration(state: _ParserState) -> Declaration:
    # TODO
    let_token = state.expect("LET")
    ident_token = state.expect("IDENT")
    print(ident_token)
    state.expect("ASSIGN")
    expr = parse_expr(state)
    state.expect("SEMI")
    return Declaration(name=ident_token.lexeme, expr=expr, line=let_token.line)
    raise NotImplementedError

# there be light
def parse_assignment(state: _ParserState) -> Assignment:
    #
    ident_token = state.expect("IDENT")
    state.expect("ASSIGN")
    expr = parse_expr(state)
    state.expect("SEMI")
    return Assignment(name=ident_token.lexeme, expr=expr, line=ident_token.line)
    #raise NotImplementedError

#Let or Light?
def parse_statement(state: _ParserState):
    # TODO: peek at state.peek().type to choose declaration vs. assignment
    if state.peek().type == "LET":
        return parse_declaration(state)
    elif state.peek().type == "IDENT":
        return parse_assignment(state)
    else:
        raise ParseError(f"Line {state.peek().line}: Expected 'LET' or identifier, but found {state.peek().type} ({state.peek().lexeme!r}).")
    
    raise NotImplementedError

#Parse the entire program
def parse_program(state: _ParserState) -> Program:
    # TODO: loop parse_statement() until EOF
    statements = []
    while state.peek().type != "EOF":
        #print(f"Current token: {state.peek().type} ({state.peek().lexeme}) at line {state.peek().line}")
        statements.append(parse_statement(state))
    return Program(statements=statements)

def parse(tokens: List[Token]) -> Program:
    state = _ParserState(tokens)
    return parse_program(state)
