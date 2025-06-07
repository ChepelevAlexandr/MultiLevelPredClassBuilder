# -*- coding: utf-8 -*-
# utils.py

from typing import Tuple

# Default thresholds (will be overridden in ml_builder via update_thresholds)
MIN_FREQ = 1
MAX_LITERALS = 10
MAX_VARS = 10

def update_thresholds(level: int,
                      base_max_lits: int,
                      base_max_vars: int,
                      num_classes: int) -> Tuple[int, int, int]:
    """
    Compute thresholds for a given level:
      MAX_LITERALS = max(1, base_max_lits*2 - (level-1))
      MAX_VARS     = max(1, base_max_vars*2 - (level-1))
      MIN_FREQ     = max(1, num_classes // (2**level))
    """
    max_lits = max(1, base_max_lits * 2 - (level - 1))
    max_vars = max(1, base_max_vars * 2 - (level - 1))
    min_freq = max(1, num_classes // (2 ** level))
    return max_lits, max_vars, min_freq
