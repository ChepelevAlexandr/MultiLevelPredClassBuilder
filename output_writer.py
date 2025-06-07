# -*- coding: utf-8 -*-
# output_writer.py

import os
from typing import List, Tuple, Dict
from subformula import Subformula
from parser import parse_literal

def save_level_objects(
    level: int,
    registered: List[Subformula],
    subf_to_name: Dict[Subformula, str],
    level_objects: List[List[Tuple[str, ...]]]
):
    """
    Write output/level{level}_objects.txt in a clear, annotated format.

    For each registered Subformula (in the same order as 'registered'),
    print its predicate name (e.g. 'p1_1', 'p1_2', etc.) on a dedicated line,
    then all unique tuples (comma-separated) if any matches were found.
    If there are no matches for that predicate, write:
      # <predname> : no matches

    Between different predicates, insert exactly one blank line.
    """
    os.makedirs("output", exist_ok=True)
    path = os.path.join("output", f"level{level}_objects.txt")
    with open(path, "w", encoding="utf-8") as fout:
        for sf, tuples_list in zip(registered, level_objects):
            predname = subf_to_name[sf]
            fout.write(f"# {predname}\n")

            if not tuples_list:
                fout.write(f"# {predname} : no matches\n")
            else:
                for tup in tuples_list:
                    fout.write(",".join(tup) + "\n")

            fout.write("\n")  # exactly one blank line before next predicate

def save_final_descriptions(
    final_subfs: Dict[int, List[Subformula]],
    subf_to_name: Dict[int, Dict[Subformula, str]]
):
    """
    Write output/final_descriptions.txt.
    For each level (ascending order) and each Subformula, output
      predname(var1,var2,…) | predname2(...)
    where variables are taken in the order they appear in the first literal.
    """
    os.makedirs("output", exist_ok=True)
    path = os.path.join("output", "final_descriptions.txt")
    with open(path, "w", encoding="utf-8") as fout:
        levels = sorted(final_subfs.keys())
        for l in levels:
            line_items: List[str] = []
            for sf in final_subfs[l]:
                predname = subf_to_name[l][sf]
                first_lit = sf.literals[0]
                _, args, _ = parse_literal(first_lit)
                var_list = [arg for arg in args if arg and arg[0].islower()]
                line_items.append(f"{predname}({','.join(var_list)})")
            fout.write("|".join(line_items) + "\n")
