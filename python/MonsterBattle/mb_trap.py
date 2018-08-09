# -------------------------------------------------------------------------
#  File:    mb_trap.py
#  Created: Tue Feb  7 20:51:32 2006
# -------------------------------------------------------------------------

import random

import mb_io
import mb_subs
from mb_go import GameObject

class Trap(GameObject):
    """
    This class is used to create traps (or blessing objects) that exist
    in the arena on their own but that are not subject to attack.
    The only real attributes traps have is different types of attacks that
    they can carry out on combatants in the arena.

    """
    def __init__(self, gamedir, filename = None):

        self.attacks = list()
        self.x = 0
        self.y = 0
        self.radius = 0
        self.is_first_round = True
        GameObject.__init__(self, gamedir, filename)

    def read_in_config(self, filename):
        parser = GameObject.read_in_config(self, filename)
        if parser.has_section('attacks'):
            self.attacks = mb_subs.actions(parser.items('attacks'))
        del parser

    def trigger_trap(self, victim):

        attac = random.choice(self.attacks)
        attack = attac[0]
        damage = attac[1]
        victim.health = mb_subs.subtract_to_floor(victim.health, damage)

        if damage >= 0:
            commentary = '(OH NO!) %s' % (attack % victim.name)
        else:
            commentary = '(WOW!) %s' % (attack % victim.name)
        return commentary, damage
