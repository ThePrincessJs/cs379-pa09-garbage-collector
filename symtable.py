"""
PA 5 dependency: paste in YOUR OWN completed PA 4 symtable.py here.

Complete Environment and check_program below. See
PA_04_The_USILang_Symbol_Table.md, Part B, for the full requirements.
"""

from typing import Optional

from parser import Assignment, BinOp, Declaration, Number, Program, Variable


class SemanticError(Exception):
    pass


class Environment:
    def __init__(self, parent: Optional["Environment"] = None) -> None:
        self.parent = parent
        self._names: dict = {}  # name -> declaration line, THIS scope only

    def define(self, name: str, line: int) -> None:
        """
        Store name -> line in THIS scope. Raise SemanticError if `name`
        is already defined in THIS scope (not a parent scope --
        shadowing a parent name is allowed).
        """
        # TODO
        if name in self._names:
            orig_line = self._names[name]
            raise SemanticError(f"Duplicate Declaration! Name '{name}' on line {line} is already defined at line {orig_line}")
        self._names[name] = line

    def resolve(self, name: str) -> int:
        """
        Look up `name` in this scope, then climb `parent` links.
        Return the declaration line, or raise SemanticError if not
        found anywhere in the chain.
        """
        # Check and make sure that the name was already defined in this scope.
        if name in self._names:
            return self._names[name]
        if self.parent is not None:
            return self.parent.resolve(name)
        raise SemanticError(f"Name '{name}' not defined, Try adding a let statement for '{name}' before using it. God Bless you! ")

def check_expression(expr, env: Environment) -> None:
    if expr is None:
        return

    expr_type = type(expr).__name__

    if expr_type == "Variable" or hasattr(expr, "name"):
        # Check if the variable is defined in the environment
        try:
            env.resolve(expr.name)
        except SemanticError as e:
            line = getattr(expr, "line", "unknown")
            raise SemanticError(f"Use of undefined variable '{expr.name}' at line {line}") from e
    elif expr_type == "BinOp":
        # Recursively check the left and right expressions, poinT!
        check_expression(expr.left, env)
        check_expression(expr.right, env)
    elif expr_type == "UnaryOp":
        check_expression(expr.operand, env)


def check_program(ast: Program) -> Environment:
    """
    Walk `ast.statements` in order, using one top-level Environment.
    For a Declaration: resolve every Variable in its expr BEFORE
    defining the new name (so `let x = x;` fails as use-before-decl).
    For an Assignment: resolve the assigned-to name, then resolve
    every Variable in its expr. Errors must surface at the first
    offending statement, not be collected and reported together.
    """
    # Create a new environment for the program
    env = Environment()
    for stmt in ast.statements:
        if isinstance(stmt, Declaration):
            # Check the expression for variable usage
            check_expression(stmt.expr, env)
            # Define the new variable in the current environment
            env.define(stmt.name, stmt.line)
        elif isinstance(stmt, Assignment):
            try:
                env.resolve(stmt.name)
            except SemanticError as e:
                raise SemanticError(f"Assignment to undefined variable '{stmt.name}' at line {stmt.line}, Please define the variable first next time :)") from e
            # Check the expression for variable usage
            check_expression(stmt.expr, env)
        
    return env