# -*- coding: utf-8 -*-
# subformula.py

from typing import List

class Subformula:
    """
    Represents a conjunction of literals.
    For hashing and equality, store literals in a sorted tuple.
    """
    def __init__(self, literals: List[str]):
        # Sort literals alphabetically for deterministic ordering
        self.literals = sorted(literals)
        self._lit_tuple = tuple(self.literals)

    def __hash__(self):
        return hash(self._lit_tuple)

    def __eq__(self, other):
        if not isinstance(other, Subformula):
            return False
        return self._lit_tuple == other._lit_tuple

    def __len__(self):
        return len(self.literals)

    def __repr__(self):
        return f"Subformula({','.join(self.literals)})"
