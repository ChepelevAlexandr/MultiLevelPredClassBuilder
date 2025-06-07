# -*- coding: utf-8 -*-
# ml_builder.py

import sys
import os
from typing import List, Dict, Tuple, Set

from parser import read_classes_list, read_scene, parse_conjunction, parse_literal
from level_finder import extract_level
from selector import select_and_register_predicates
import utils
from matcher import find_all_matches_multiple
from output_writer import save_level_objects, save_final_descriptions
from subformula import Subformula
from utils import update_thresholds

def build_level_objects(
    level: int,
    registered: List[Subformula],
    subf_to_name: Dict[Subformula, str],
    S_union: List[Tuple[str, List[str]]]
) -> List[List[Tuple[str, ...]]]:
    """
    For each registered Subformula at this level, find all matches in S_union (ground atoms).
    Returns a list of lists: each inner list contains all unique ground assignments (tuples of constants)
    for one Subformula. The order of constants in each tuple is determined by
    the variable order in the first literal of that Subformula.
    """
    level_objects: List[List[Tuple[str, ...]]] = []
    for sf in registered:
        lits = sf.literals  # e.g. ["P(x0,x1)", "Q(x1,x2)"]
        matches = find_all_matches_multiple(lits, S_union)

        # Filter out duplicate assignments using a set
        unique_tuples: Set[Tuple[str, ...]] = set()
        if matches:
            first_lit = lits[0]
            _, args, _ = parse_literal(first_lit)
            var_order = [v for v in args if v and v[0].islower()]

            for subs in matches:
                tup = tuple(subs[v] for v in var_order if v in subs)
                unique_tuples.add(tup)

        # Convert back to list
        level_objects.append(list(unique_tuples))

    return level_objects

def main():
    if len(sys.argv) != 3:
        print("Usage: python ml_builder.py <classes_list.txt> <scene.txt>")
        sys.exit(1)

    classes_file = sys.argv[1]
    scene_file = sys.argv[2]

    # Step 1: Read input files
    classes_conj, num_classes = read_classes_list(classes_file)
    S_union = read_scene(scene_file)

    # Step 2: Compute base thresholds (max literals, max vars across all class‐conjunctions)
    base_max_lits = 0
    base_max_vars = 0
    for conj_list in classes_conj:
        for conj in conj_list:
            lits = parse_conjunction(conj)
            base_max_lits = max(base_max_lits, len(lits))
            vars_set: Set[str] = set()
            for lit in lits:
                _, args, _ = parse_literal(lit)
                for arg in args:
                    if arg.islower():
                        vars_set.add(arg)
            base_max_vars = max(base_max_vars, len(vars_set))

    # Maximum possible levels: at most num_classes + 2 (safe upper bound)
    max_possible_levels = num_classes + 2

    # Prepare data structures to hold raw/registered subformulas and mappings
    raw_subf_by_level: Dict[int, List[Dict]] = {}
    registered_subf_by_level: Dict[int, List[Subformula]] = {}
    subf_to_name_by_level: Dict[int, Dict[Subformula, str]] = {}
    final_subfs: Dict[int, List[Subformula]] = {}
    all_level_objects: Dict[int, List[List[Tuple[str, ...]]]] = {}

    # --- Level 1 ---
    print("[DEBUG] Building level 1 ...")
    raw_subf_by_level[1] = extract_level(1, classes_conj, list(range(len(classes_conj))), num_classes)

    # Compute thresholds for level=1
    max_lits, max_vars, min_freq = update_thresholds(1, base_max_lits, base_max_vars, num_classes)
    # Override utils thresholds so selector uses these values:
    utils.MIN_FREQ = min_freq
    utils.MAX_LITERALS = max_lits
    utils.MAX_VARS = max_vars

    reg1: List[Subformula] = []
    name1: Dict[Subformula, str] = {}
    vars1: Dict[Subformula, List[str]] = {}
    select_and_register_predicates(
        raw_subfs=raw_subf_by_level[1],
        parent_class_map=list(range(len(classes_conj))),
        registered_subfs=reg1,
        subf_to_name=name1,
        subf_to_vars=vars1,
        level=1
    )
    registered_subf_by_level[1] = reg1
    subf_to_name_by_level[1] = name1
    final_subfs[1] = reg1

    print(f"[DEBUG]  → Found {len(reg1)} registered predicates at level 1 "
          f"(MAX_LITS={max_lits}, MAX_VARS={max_vars}, MIN_FREQ={min_freq})")

    objs1 = build_level_objects(1, reg1, name1, S_union)
    all_level_objects[1] = objs1
    save_level_objects(
        1,
        registered_subf_by_level[1],
        subf_to_name_by_level[1],
        objs1
    )

    # --- Levels 2, 3, ... until no more raw subformulas ---
    for l in range(2, max_possible_levels + 1):
        print(f"[DEBUG] Building level {l} ...")
        raw_prev = raw_subf_by_level[l - 1]
        raw_subf_by_level[l] = extract_level(l, classes_conj, list(range(len(classes_conj))), num_classes)
        if not raw_subf_by_level[l]:
            print(f"[DEBUG]  No raw subformulas at level {l}. Stopping.")
            break

        max_lits, max_vars, min_freq = update_thresholds(l, base_max_lits, base_max_vars, num_classes)
        # Override utils thresholds for this level:
        utils.MIN_FREQ = min_freq
        utils.MAX_LITERALS = max_lits
        utils.MAX_VARS = max_vars

        reg_l: List[Subformula] = []
        name_l: Dict[Subformula, str] = {}
        vars_l: Dict[Subformula, List[str]] = {}
        select_and_register_predicates(
            raw_subfs=raw_subf_by_level[l],
            parent_class_map=list(range(len(classes_conj))),
            registered_subfs=reg_l,
            subf_to_name=name_l,
            subf_to_vars=vars_l,
            level=l
        )
        registered_subf_by_level[l] = reg_l
        subf_to_name_by_level[l] = name_l
        final_subfs[l] = reg_l

        print(f"[DEBUG]  → Found {len(reg_l)} registered predicates at level {l} "
              f"(MAX_LITS={max_lits}, MAX_VARS={max_vars}, MIN_FREQ={min_freq})")

        objs_l = build_level_objects(l, reg_l, name_l, S_union)
        all_level_objects[l] = objs_l
        save_level_objects(
            l,
            registered_subf_by_level[l],
            subf_to_name_by_level[l],
            objs_l
        )

    # Step 4: Save final descriptions (predname(vars)|predname2(vars)|... for each level)
    save_final_descriptions(final_subfs, subf_to_name_by_level)

    print("Done! Please check the output/ directory.")

if __name__ == "__main__":
    main()
