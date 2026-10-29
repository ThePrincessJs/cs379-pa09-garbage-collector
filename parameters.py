"""
PA 7: The Parameter Simulator -- starter.

Complete bind_parameters, commit_value_result, and Closure below.
Cell, evaluate(), and FunctionDecl are already provided -- do not
modify them. See the assignment, Part B, for the
full requirements.

Value-result binding has two steps: bind_parameters runs at call time
and records each caller destination; commit_value_result runs after
the simulated body and copies the final local values back in parameter
order. The handout specifies both steps.

Design note 2: variables are stored as Cell objects (a mutable box),
not raw values, specifically so reference-mode parameters can share
the exact same storage as the caller's variable -- see Part A,
Questions 1-2, for why "bind directly to the caller's slot" requires
this instead of just copying a plain value.
"""


from typing import Any, List, Tuple
from frames import ActivationRecord

from parser import BinOp, Number, Variable
from symtable import Environment


class Cell:
    """Given: a mutable box. Two names that share the SAME Cell are aliased."""

    __slots__ = ("value",)

    def __init__(self, value: Any) -> None:
        self.value = value


class FunctionDecl:
    """Given: a minimal function declaration -- params and a single expr body."""

    __slots__ = ("params", "body")

    def __init__(self, params: List[str], body) -> None:
        self.params = params
        self.body = body


def evaluate(node, env: Environment):
    """Given: evaluate a PA3 expression AST node against `env` (Cells are transparently dereferenced)."""
    if isinstance(node, Number):
        return node.value
    if isinstance(node, Variable):
        val = env.resolve(node.name)
        return val.value if isinstance(val, Cell) else val
    if isinstance(node, BinOp):
        if node.op == "neg":
            return -evaluate(node.left, env)
        left = evaluate(node.left, env)
        right = evaluate(node.right, env)
        return {"+": lambda a, b: a + b, "-": lambda a, b: a - b, "*": lambda a, b: a * b, "/": lambda a, b: a / b}[node.op](left, right)
    raise ValueError(f"cannot evaluate node: {node!r}")


def assign_through(env: Environment, name: str, value: Any) -> None:
    """Given: write `value` into whatever Cell `name` resolves to (mutates in place, does not rebind)."""
    cell = env.resolve(name)
    if not isinstance(cell, Cell):
        raise TypeError(f"'{name}' is not bound to a Cell -- did you forget to wrap it?")
    cell.value = value


def bind_parameters(param_specs: List[Tuple[str, str]], arg_nodes: list, caller_env: Environment, callee_record) -> None:
    """
    Populate callee_record.locals_env according to each parameter's
    mode ("value", "reference", or "value-result"). For value-result
    parameters, also record what commit_value_result needs to do the
    delayed write-back later -- store it whichever way you like (e.g.
    an attribute on callee_record such as callee_record.pending_writeback).
    """
    # TODO
    value_result_destinations = []

    for (param_name, mode), arg_node in zip(param_specs,arg_nodes):
        if mode =="value":
            val = evaluate(arg_node, caller_env)
            callee_record.locals_env.define(param_name, Cell(val))
        elif mode == "reference":
            var_name = arg_node.name if hasattr(arg_node, 'name') else arg_node
            caller_cell = caller_env.resolve(var_name)
            callee_record.locals_env.define(param_name, caller_cell)
        elif mode == "value-result":
            val = evaluate(arg_node, caller_env)
            local_cell = Cell(val)
            callee_record.locals_env.define(param_name, local_cell)

            var_name = arg_node.name if hasattr(arg_node,'name') else arg_node
            caller_cell = caller_env.resolve(var_name)
            value_result_destinations.append((local_cell, caller_cell))
    callee_record.value_result_destinations = value_result_destinations
    #raise NotImplementedError


def commit_value_result(callee_record, caller_env: Environment) -> None:
    """
    For every value-result parameter bound by bind_parameters on this
    callee_record, copy its FINAL local value back into the caller's
    corresponding variable now (call this only after the callee's body
    has finished running).
    """
    # TODO
    if hasattr(callee_record, 'value_result_destinations'):
        for local_cell, caller_cell in callee_record.value_result_destinations:
            caller_cell.value = local_cell.value
    #raise NotImplementedError


class Closure:
    def __init__(self, declaration: FunctionDecl, defining_env: Environment) -> None:
        # TODO
        self.declaration = declaration
        self.defining_env = defining_env # Static Link

    def call(self, args: list, caller_env: Environment):
        """
        Create the callee Environment as a child of self.defining_env
        (NOT caller_env) -- this is what makes closure capture work.
        Bind each declaration.params[i] to args[i] (already-evaluated
        values, wrapped in a Cell), then evaluate declaration.body in
        that new environment and return the result.
        """
        # TODO
        callee_env = Environment(parent=self.defining_env)
        callee_record = ActivationRecord(
            function_name=getattr(self.declaration, 'name', 'anonymous'),
            parameters=self.declaration.params,
            locals_env=callee_env,
            return_address="",
            static_link=self.defining_env,
            dynamic_link=None
        )
        

        for param_spec, arg_val in zip(self.declaration.params, args):
            
            if isinstance(param_spec, (list,tuple)):
                param_name = param_spec[0]
                mode = param_spec[1] if len(param_spec) > 1 else "value"
            else:
                param_name = param_spec
                mode = "value"
                
            callee_env.define(param_name, Cell(arg_val))

        result = evaluate(self.declaration.body,callee_record)
        return result
        #raise NotImplementedError
