"""
PA 8: The VTable Dispatcher -- starter.

Complete VTable, build_vtable, USIObject, and dispatch below. See
PA_08_The_VTable_Dispatcher.md, Part B, for the full requirements.

Design note (simplification): the assignment says to reuse the call
mechanism from PA6/PA7, but PA1-7's expression AST only evaluates
integer arithmetic -- there's no string-literal node, and this PA's
test scenario (Animal/Dog/Puppy) needs string-returning methods. Full
string-literal support would mean extending the grammar/lexer/parser/
evaluator, which is out of scope for what Part B actually asks you to
build (VTable/dispatch mechanics). So here, a method body is a plain
Python callable `fn(self) -> value` instead of a PA3 AST node --
dispatch() still resolves through the VTable and still invokes the
resolved method with the object as receiver, which is the actual
mechanism this PA is about.
"""

from typing import Callable, Dict, Optional


class ClassDecl:
    """Given: a minimal class declaration -- just a name and its own (non-inherited) methods."""

    __slots__ = ("name", "methods")

    def __init__(self, name: str, methods: Dict[str, Callable]) -> None:
        self.name = name
        self.methods = methods  # {method_name: fn(self) -> value}, declared on THIS class only


class VTable:
    def __init__(self, entries: Dict[str, Callable], owning_class_name: str = "?") -> None:
        """`owning_class_name` is just for error messages -- store it alongside entries."""
        # TODO: store entries and owning_class_name.
        self.owning_class_name = owning_class_name
        self.entries = entries
        #raise NotImplementedError

    def resolve(self, method_name: str) -> Callable:
        """
        Return the callable bound to `method_name`. Raise a clear
        error (e.g. AttributeError) whose message names BOTH the
        owning class and the missing method if it doesn't exist.
        """
        # TODO
        if method_name in self.entries:
            return self.entries[method_name]
        raise AttributeError(f"Class '{self.owning_class_name}' has no method called: '{method_name}'.")
        #raise NotImplementedError


def build_vtable(class_node: ClassDecl, parent_vtable: Optional[VTable] = None) -> VTable:
    """
    Start from a copy of parent_vtable's entries (inherited methods),
    then overwrite only the slots class_node itself redeclares. A
    method class_node does NOT override must resolve to the EXACT SAME
    callable object the parent uses -- don't wrap or duplicate it.
    Pass class_node.name as the new VTable's owning_class_name.
    """
    # TODO
    entries = {}
    if parent_vtable is not None:
        entries.update(parent_vtable.entries)

    if class_node.methods:
        entries.update(class_node.methods)

    return VTable(entries=entries, owning_class_name =class_node.name)
    #raise NotImplementedError


class USIObject:
    def __init__(self, class_descriptor: VTable, fields: dict) -> None:
        # TODO: store both. class_descriptor is this object's ACTUAL runtime VTable.
        self.class_descriptor = class_descriptor
        self.fields = fields
        #raise NotImplementedError


def dispatch(obj: USIObject, method_name: str, args: list, caller_env) -> object:
    """
    Resolve method_name through obj's OWN VTable (never a declared/
    static type), then call the resolved method with obj as the
    receiver: resolved_method(obj, *args).
    """
    # TODO
    method = obj.class_descriptor.resolve(method_name)
    return method(obj, *args)
    #raise NotImplementedError
