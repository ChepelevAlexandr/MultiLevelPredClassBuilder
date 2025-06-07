# -*- coding: utf-8 -*-
# selector.py

from collections import defaultdict
from typing import List, Dict, Set, Tuple

from utils import MIN_FREQ, MAX_LITERALS, MAX_VARS
from subformula import Subformula
from parser import parse_literal

def select_and_register_predicates(
    raw_subfs: List[Dict],
    parent_class_map: List[int],
    registered_subfs: List[Subformula],
    subf_to_name: Dict[Subformula, str],
    subf_to_vars: Dict[Subformula, List[str]],
    level: int
):
    """
    From raw_subfs (each entry: {'literals': [...], 'origins': [(i,j), ...]}),
    compute frequency of each unique set of literals across distinct classes.
    Filter by:
       - frequency >= MIN_FREQ
       - number of literals <= MAX_LITERALS
       - number of distinct variables <= MAX_VARS
    Remove any subformula that is strictly contained in a larger one (on this level).
    Assign names p{level}_{counter} to each surviving Subformula.
    Populate:
      - registered_subfs (list of Subformula objects)
      - subf_to_name: map from Subformula to its predicate name
      - subf_to_vars: map from Subformula to ordered list of its variables
    """
    # Build a map: literal‐tuple → set of class‐indices where it occurs
    freq_map: Dict[Tuple[str, ...], Set[int]] = defaultdict(set)
    for entry in raw_subfs:
        lit_tuple = tuple(sorted(entry['literals']))
        for (i, j) in entry['origins']:
            ci = parent_class_map[i]
            cj = parent_class_map[j]
            freq_map[lit_tuple].add(ci)
            freq_map[lit_tuple].add(cj)

    class Candidate:
        __slots__ = ('subf', 'freq', 'num_lits', 'num_vars')
        def __init__(self, subf: Subformula, freq: int, num_vars: int):
            self.subf = subf
            self.freq = freq
            self.num_lits = len(subf)
            self.num_vars = num_vars

    candidates: List[Candidate] = []
    for lit_tuple, class_set in freq_map.items():
        freq = len(class_set)
        if freq < MIN_FREQ:
            continue
        # Count distinct lowercase variables across all literals
        vars_set: Set[str] = set()
        for lit in lit_tuple:
            _, args, _ = parse_literal(lit)
            for a in args:
                if a.islower():
                    vars_set.add(a)
        num_vars = len(vars_set)
        subf = Subformula(list(lit_tuple))
        candidates.append(Candidate(subf, freq, num_vars))

    # Filter candidates by literal‐count and var‐count
    filtered = [
        cand for cand in candidates
        if cand.num_lits <= MAX_LITERALS and cand.num_vars <= MAX_VARS
    ]

    # Remove duplicates (keep first occurrence of each unique Subformula)
    unique_list: List[Subformula] = []
    seen: Set[Subformula] = set()
    for cand in filtered:
        if cand.subf not in seen:
            seen.add(cand.subf)
            unique_list.append(cand.subf)

    # Remove any subformula that is strictly contained in another
    maximal_list: List[Subformula] = []
    for sf in unique_list:
        is_contained = False
        for other in unique_list:
            if sf == other:
                continue
            set_sf = set(sf.literals)
            set_other = set(other.literals)
            if set_sf.issubset(set_other) and len(sf.literals) < len(other.literals):
                is_contained = True
                break
        if not is_contained:
            maximal_list.append(sf)

    # Register each maximal subformula with a unique name p{level}_{i}
    idx_counter = 1
    for sf in maximal_list:
        name = f"p{level}_{idx_counter}"
        registered_subfs.append(sf)
        subf_to_name[sf] = name

        # Determine variable ordering (first‐seen in literal order)
        vars_order: List[str] = []
        seen_vars: Set[str] = set()
        for lit in sf.literals:
            _, args, _ = parse_literal(lit)
            for a in args:
                if a.islower() and a not in seen_vars:
                    vars_order.append(a)
                    seen_vars.add(a)
        subf_to_vars[sf] = vars_order.copy()

        idx_counter += 1
