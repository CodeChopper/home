# -------------------------------------------------------------------------
#  File:    mb_subs.py
#  Created: Tue Feb  7 20:46:27 2006
# -------------------------------------------------------------------------

def actions(action_list):
    return [(action, int(value)) for action, value in action_list]

def subtract_to_floor(a, b, floor=0):
    """
    Subtracts b from a, where a bottoms out at floor.
    floor defaults to 0 if not provided.

    """
    a -= b
    if a < floor:
        a = floor
    return a
