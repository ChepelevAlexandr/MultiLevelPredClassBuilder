# -*- coding: utf-8 -*-
# matcher.py

from typing import List, Tuple, Dict
from unifier import unify_two
from parser import parse_literal

def apply_subst(literal: str, subst: Dict[str, str]) -> str:
    """
    Apply a substitution mapping (var → constant) to a single literal,
    producing a new literal string with constants substituted.
    """
    pred, args, _ = parse_literal(literal)
    new_args: List[str] = [subst.get(arg, arg) for arg in args]
    return f"{pred}({','.join(new_args)})"

def find_max_common_subf(conj_i: List[str], conj_j: List[str]) -> List[List[str]]:
    """
    Given two conjunctions (lists of literal‐strings), find all maximal common subformulas
    (up to variable renaming). For simplicity, we unify only literal‐by‐literal and collect common parts.
    Returns a list of literal‐lists, each representing a maximal common subformula.
    """
    candidate_maps: List[List[str]] = []
    for lit_i in conj_i:
        for lit_j in conj_j:
            maps = unify_two(lit_i, lit_j)  # using unifier.unify_two
            for mp in maps:
                replaced_i = [apply_subst(l, mp) for l in conj_i]
                replaced_j = [apply_subst(l, mp) for l in conj_j]
                common = list(set(replaced_i) & set(replaced_j))
                if common:
                    candidate_maps.append(sorted(common))

    if not candidate_maps:
        return []
    max_len = max(len(c) for c in candidate_maps)
    return [c for c in candidate_maps if len(c) == max_len]

def find_all_matches_multiple(
    lits: List[str],
    S_union: List[Tuple[str, List[str]]]
) -> List[Dict[str, str]]:
    """
    For a given conjunction‐template (list of literals with variables),
    find all variable→constant assignments that match against the ground atoms S_union.
    S_union is a list of (predicate_name, [arg1, arg2, ...]) for ground atoms.
    Returns a list of substitution Dicts mapping variable names to constants.
    """
    results: List[Dict[str, str]] = []

    def dfs(idx: int, curr_map: Dict[str, str]):
        if idx == len(lits):
            # Completed matching all literals → record current substitution
            results.append(curr_map.copy())
            return

        lit = lits[idx]
        pred_lit, args_lit, _ = parse_literal(lit)
        for pred_s, args_s in S_union:
            if pred_s != pred_lit or len(args_s) != len(args_lit):
                continue
            local_map = curr_map.copy()
            valid = True
            for a_l, a_s in zip(args_lit, args_s):
                if a_l.islower():
                    # a_l is a variable
                    if a_l in local_map:
                        if local_map[a_l] != a_s:
                            valid = False
                            break
                    else:
                        local_map[a_l] = a_s
                else:
                    # a_l is treated as constant; it must match exactly
                    if a_l != a_s:
                        valid = False
                        break
            if not valid:
                continue
            dfs(idx + 1, local_map)

    dfs(0, {})
    return results
