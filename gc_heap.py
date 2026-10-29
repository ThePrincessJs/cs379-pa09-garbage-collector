"""
PA 9: The Garbage Collector -- starter.

Complete GCHeap below. See the assignment, Part B,
for the full requirements.

Use gc_heap.py as specified in the assignment and imported by the harness.

Design note: GCHeap.allocate(obj) takes exactly one argument per the
spec, so an allocated object that references OTHER heap handles must
expose them itself for decref's cascade to find -- via a
get_child_handles() -> list[int] method. HeapNode below is a given
example object shaped this way, used by the cyclic-structure test.
"""

from typing import Any, List


class HeapNode:
    """
    Given: a minimal heap object whose fields may hold OTHER handles
    (ints). get_child_handles() is what GCHeap.decref's cascade calls
    to find them -- it must reflect the CURRENT field values, not a
    snapshot taken at creation time.
    """

    def __init__(self, **fields: Any) -> None:
        self.fields = fields

    def get_child_handles(self) -> List[int]:
        return [v for v in self.fields.values() if isinstance(v, int)]


class GCHeap:
    def __init__(self) -> None:
        # TODO: internal storage -- e.g. {handle: (obj, refcount)} -- and a handle counter.
        self.objects = {}
        self.ref_counts = {}
        self.next_handle = 1
        
        #raise NotImplementedError

    def allocate(self, obj: Any) -> int:
        """Store obj, return a new handle. Initial refcount is 1 (the creating reference)."""
        # TODO
        handle = self.next_handle
        self.next_handle += 1
        self.objects[handle] = obj
        self.ref_counts[handle] = 1
        return handle
        #raise NotImplementedError

    def incref(self, handle: int) -> None:
        # TODO
        if handle in self.objects:
            self.ref_counts[handle] += 1

        #raise NotImplementedError

    def decref(self, handle: int) -> None:
        """
        Decrement the refcount. When it hits 0: free the object, AND
        cascade-decref every handle returned by the freed object's
        get_child_handles() (if it has that method), recursively.
        """
        # TODO
        if handle not in self.objects:
            return

        self.ref_counts[handle] -= 1

        if self.ref_counts[handle] <= 0:
            self._free(handle)        
        #raise NotImplementedError


    def _free(self, handle: int) -> None:
        obj = self.objects.pop(handle,None)
        self.ref_counts.pop(handle, None)

        if obj is not None:
            child_handles = self._extract_child(obj)
            for child_handle in child_handles:
                self.decref(child_handle)

    def _extract_child(self, obj) -> list:
        handles = []
        if hasattr(obj, 'fields') and isinstance(obj.fields, dict):
            for val in obj.fields.values():
                if isinstance(val, int) and val in self.objects:
                    handles.append(val)
        elif hasattr(obj, '__dict__'):
            for val in obj.__dict__.values():
                if isinstance(val, int) and val in self.objects:
                    handles.append(val)
        return handles


    def is_alive(self, handle: int) -> bool:
        # TODO
        return handle in self.objects


        #raise NotImplementedError

    def live_count(self) -> int:
        """Number of currently-alive (refcount > 0) handles."""
        # TODO
        return len(self.objects)
        #raise NotImplementedError
