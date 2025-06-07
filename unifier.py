# -*- coding: utf-8 -*-
# unifier.py

from typing import List, Dict, Tuple, Set
from parser import parse_literal

def unify_two(literal1: str, literal2: str) -> List[Dict[str, str]]:
    """
    Attempt to unify two literals (strings) up to variable renaming.
    Returns a list of substitution maps (var→var or var→const) if there are any unifiers,
    or an empty list otherwise.
    For simplicity, assume each literal is of form "P(x,a,b)".
    """
    pred1, args1, _ = parse_literal(literal1)
    pred2, args2, _ = parse_literal(literal2)
    if pred1 != pred2 or len(args1) != len(args2):
        return []

    substitutions: Dict[str, str] = {}
    for a1, a2 in zip(args1, args2):
        if a1.islower() and a2.islower():
            # variable–variable: arbitrarily bind a1→a2
            substitutions[a1] = a2
        elif a1.islower() and not a2.islower():
            # var–constant
            substitutions[a1] = a2
        elif not a1.islower() and a2.islower():
            substitutions[a2] = a1
        else:
            # constant–constant: must match exactly
            if a1 != a2:
                return []  # no unifier

    return [substitutions]

def is_isomorphic_args(args1: List[str], args2: List[str]) -> bool:
    """
    Check if two lists of arguments are isomorphic up to renaming of lowercase vars.
    """
    if len(args1) != len(args2):
        return False
    mapping: Dict[str, str] = {}
    used: Set[str] = set()
    for a1, a2 in zip(args1, args2):
        if a1.islower() and a2.islower():
            if a1 in mapping:
                if mapping[a1] != a2:
                    return False
            else:
                if a2 in used:
                    return False
                mapping[a1] = a2
                used.add(a2)
        elif a1.islower() or a2.islower():
            # one is var, the other is constant → not isomorphic
            return False
        else:
            if a1 != a2:
                return False
    return True
