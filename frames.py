"""
PA 6: The Activation Record -- starter.

Complete ActivationRecord and CallStack below. See
PA_06_The_Activation_Record.md, Part B, for the full requirements.

Note on scope: PA1-5 never added function-call SYNTAX to USILang's
grammar (deliberately -- see PA5's pipeline-context note). PA6's
Part B interface is pure Python classes with no mention of parser
changes either, so test_frames.py drives ActivationRecord/CallStack
directly in Python (simulating what a parsed function call sequence
would do) rather than parsing real USILang function syntax. Your job
this week is the frame model itself, not a grammar extension.
"""

from typing import Dict, List, Optional

from symtable import Environment


class ActivationRecord:
    def __init__(
        self,
        function_name: str,
        parameters: Dict[str, object],
        locals_env: Environment,
        return_address: str,
        static_link: Optional["ActivationRecord"],
        dynamic_link: Optional["ActivationRecord"],
    ) -> None:
        # TODO: store all six arguments as attributes of the same names.
        self.function_name = function_name
        self.parameters = parameters
        self.locals_env = locals_env
        self.return_address = return_address
        self.static_link = static_link # Static!
        self.dynamic_link = dynamic_link #Dynamic!

    def resolve(self, name: str):
        """Delegate variable resolution directly to the inner locals environment."""
        return self.locals_env.resolve(name)

        #raise NotImplementedError


class CallStack:
    def __init__(self) -> None:
        # TODO: internal storage for the stack of frames.
        self._frames: List[ActivationRecord] = []

        #raise NotImplementedError

    def push(self, record: ActivationRecord) -> None:
        # TODO
        self._frames.append(record)
        #raise NotImplementedError

    def pop(self) -> ActivationRecord:
        """Remove and return the top frame."""
        # TODO
        if not self._frames:        # Check if the stack is empty before popping!
            raise IndexError("Call stack is empty, cannot pop.")
        return self._frames.pop()
        #raise NotImplementedError

    def current(self) -> ActivationRecord:
        """Return (without removing) the top frame."""
        # TODO
        if not self._frames:        # Check if the stack is empty before currenting!
            raise IndexError("Call stack is empty, cannot access current frame.")
        return self._frames[-1]
        #raise NotImplementedError

    def trace(self) -> List[str]:
        """
        Return one formatted string per live frame, BOTTOM of the
        stack first (oldest call first). Format is up to you, but
        each line must include the function_name and its parameters.
        """
        # TODO
        trace_lines = []
        for i, frame in enumerate(self._frames):
            dynamic_str = (         # Dynamic link, search and check through the caller
                frame.dynamic_link.function_name
                if frame.dynamic_link is not None
                else "None"
            )
            static_str = (          # Static link, search and check through the defining scope
                frame.static_link.function_name
                if frame.static_link is not None
                else "None"
            )
            line = (                # Bunch of importnat lines I need
                f"[{i}] {frame.function_name} | "
                f"params={frame.parameters} | "
                f"dynamic_link={dynamic_str} | "
                f"static_link={static_str}"
                f"return={frame.return_address}"
            )
            trace_lines.append(line)
        return trace_lines #Get it, got it, gotta have it

    
        #raise NotImplementedError
