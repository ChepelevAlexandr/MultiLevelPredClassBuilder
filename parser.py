# -*- coding: utf-8 -*-
import re
import sys
from typing import List, Tuple

def trim_whitespace(s: str) -> str:
    """
    Trim leading and trailing whitespace from the input string.
    """
    start = 0
    while start < len(s) and s[start].isspace():
        start += 1
    if start == len(s):
        return ""
    end = len(s) - 1
    while end > start and s[end].isspace():
        end -= 1
    return s[start:end+1]

def split_and_trim(s: str, delim: str) -> List[str]:
    """
    Split the string `s` by delimiter `delim` and trim whitespace around each token.
    """
    parts: List[str] = []
    tokens = s.split(delim)
    for token in tokens:
        t = trim_whitespace(token)
        if t:
            parts.append(t)
    return parts

def parse_literal(lit_str: str) -> Tuple[str, List[str], List[str]]:
    """
    Parse a single literal of form Name(arg1,arg2,...).
    Returns a tuple: (predicate_name, [args...], copy_of_args).
    Raises ValueError if format is invalid.
    """
    lit_str = trim_whitespace(lit_str)
    m = re.fullmatch(r"([A-Za-z]\w*)\(([-A-Za-z0-9_,]+)\)", lit_str)
    if not m:
        raise ValueError(f"Invalid literal format: '{lit_str}'")
    pred = m.group(1)
    args_part = m.group(2)
    args = [arg.strip() for arg in args_part.split(",")]
    return pred, args, args.copy()

def parse_conjunction(conj_str: str) -> List[str]:
    """
    Parse a conjunction string like "P(x,a)&Q(a,b)&R(b,c)" into
    a list of literal substrings: ["P(x,a)", "Q(a,b)", "R(b,c)"].
    Validates each literal by calling parse_literal.
    Raises ValueError if any literal is invalid.
    """
    conj_str = trim_whitespace(conj_str).replace("\n", "")
    literals = split_and_trim(conj_str, '&')
    for lit in literals:
        _ = parse_literal(lit)  # validate each literal
    return literals

def read_classes_list(classes_path: str) -> Tuple[List[List[str]], int]:
    """
    Read the classes_list.txt file. Each line is a path to a class file.
    Each class file contains one conjunction per line (e.g. "P(x0,x1)&Q(x1,x2)").
    Returns:
      - classes_conj: a list (for each class) of lists of conjunction‐strings.
      - num_classes: total number of classes.
    """
    classes_conj: List[List[str]] = []
    try:
        with open(classes_path, "r", encoding="utf-8") as fin:
            for line in fin:
                class_file = trim_whitespace(line)
                if not class_file:
                    continue
                conj_list: List[str] = []
                with open(class_file, "r", encoding="utf-8") as cf:
                    for cl in cf:
                        cl = trim_whitespace(cl)
                        if not cl:
                            continue
                        # Validate conjunction format
                        _ = parse_conjunction(cl)
                        conj_list.append(cl)
                classes_conj.append(conj_list)
    except Exception as ex:
        print(f"Error reading classes list: {ex}", file=sys.stderr)
        sys.exit(1)
    return classes_conj, len(classes_conj)

def read_scene(scene_path: str) -> List[Tuple[str, List[str]]]:
    """
    Read the scene.txt file. Each line is a ground atom "P(a,b)".
    Returns a list of tuples: (predicate_name, [arg1, arg2, ...]).
    """
    scene_atoms: List[Tuple[str, List[str]]] = []
    try:
        with open(scene_path, "r", encoding="utf-8") as fin:
            for line in fin:
                atom_str = trim_whitespace(line)
                if not atom_str:
                    continue
                try:
                    pred, args, _ = parse_literal(atom_str)
                    scene_atoms.append((pred, args))
                except ValueError as ve:
                    print(f"Skipping invalid scene line '{atom_str}': {ve}", file=sys.stderr)
    except Exception as ex:
        print(f"Error reading scene file: {ex}", file=sys.stderr)
        sys.exit(1)
    return scene_atoms
