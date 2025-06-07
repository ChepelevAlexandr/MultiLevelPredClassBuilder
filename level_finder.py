# -*- coding: utf-8 -*-
# level_finder.py

from typing import List, Dict, Set, Tuple
from parser import parse_conjunction, parse_literal
from subformula import Subformula
from matcher import find_max_common_subf  # IMPORT the helper for multi‐literal intersection

def extract_level(
    level: int,
    classes_conj: List[List[str]],
    parent_class_map: List[int],
    num_classes: int
) -> List[Dict]:
    """
    Multi‐level extractor for raw subformulas.

    If level == 1:
      - For every pair of classes (i<j), for every pair of conjunction‐strings from those classes,
        find all common single‐literal subformulas and collect them.

    If level >= 2:
      - For every pair of classes (i<j), for every pair of conjunction‐strings from those classes,
        compute all maximal common subformulas (of any length) via find_max_common_subf.
        From those, select exactly those of length == level.

    Return: a list of dicts {'literals': [lit1, lit2, …], 'origins': [(i,j), …]}.
    """
    raw_subfs: List[Dict] = []
    seen: Set[Tuple[str, ...]] = set()
    n_classes = len(classes_conj)

    # If parent_class_map is empty, assume each class maps to itself:
    if not parent_class_map:
        parent_class_map = list(range(n_classes))

    # --- LEVEL 1: single‐literal subformulas (as before) ---
    if level == 1:
        for i in range(n_classes):
            for j in range(i + 1, n_classes):
                if parent_class_map[i] == parent_class_map[j]:
                    continue
                for conj_i in classes_conj[i]:
                    lits_i = parse_conjunction(conj_i)
                    for conj_j in classes_conj[j]:
                        lits_j = parse_conjunction(conj_j)
                        # find all common literals (same predicate name, ignoring variables)
                        for lit1 in lits_i:
                            pred1, args1, _ = parse_literal(lit1)
                            for lit2 in lits_j:
                                pred2, args2, _ = parse_literal(lit2)
                                if pred1 == pred2:
                                    sf_key = (lit1,)
                                    if sf_key not in seen:
                                        seen.add(sf_key)
                                        raw_subfs.append({
                                            "literals": [lit1],
                                            "origins": [(i, j)]
                                        })
        return raw_subfs

    # --- LEVEL >=2: look for common subformulas of exact length == level ---
    # For each pair of classes i<j, for every pair of conjunctions:
    for i in range(n_classes):
        for j in range(i + 1, n_classes):
            if parent_class_map[i] == parent_class_map[j]:
                continue
            for conj_i in classes_conj[i]:
                lits_i = parse_conjunction(conj_i)
                for conj_j in classes_conj[j]:
                    lits_j = parse_conjunction(conj_j)
                    # find_max_common_subf returns all maximal common subf. lists of literals.
                    common_list = find_max_common_subf(lits_i, lits_j)
                    # Among them, pick only those whose length == level
                    for common in common_list:
                        if len(common) == level:
                            # Sort for deterministic key
                            lit_tuple = tuple(sorted(common))
                            if lit_tuple not in seen:
                                seen.add(lit_tuple)
                                raw_subfs.append({
                                    "literals": list(lit_tuple),
                                    "origins": [(i, j)]
                                })
    return raw_subfs
