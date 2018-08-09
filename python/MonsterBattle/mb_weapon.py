# -------------------------------------------------------------------------
#  File:    mb_weapon.py
#  Created: Tue Feb  7 20:53:00 2006
# -------------------------------------------------------------------------

import mb_subs
from mb_go import GameObject

class Weapon(GameObject):
    """
    This class is used to create weapons (offensive and defensive).
    When a combatant picks up a weapon, the special attacks and defenses
    of the weapon get added to the combatant's attacks and defenses.
    If a 'weapon' is purely defensive, such as a shield, then it will
    only contain a [defences] section and vice versa.

    """
    def __init__(self, gamedir, projectiles, filename = None):

        self.attacks  = list()
        self.defences = list()
        self.x = 0
        self.y = 0
        self.radius = 0
        self.is_first_round = True
        self.all_projectiles = projectiles
        self.projectile = None

        GameObject.__init__(self, gamedir, filename)

    def read_in_config(self, filename):

        parser = GameObject.read_in_config(self, filename)

        if parser.has_section('bio'):
            if parser.has_option('bio', 'projectile'):
                self.projectile = parser.get('bio', 'projectile')

                # Convert projectile string to real object.

                found = False
                for p in self.all_projectiles:
                    if self.projectile == p.name:
                        self.projectile = p
                        found = True
                if not found:
                    print "Warning: Projectile object could not be located for: %s" % self.projectile

        if parser.has_section('attacks'):
            self.attacks = mb_subs.actions(parser.items('attacks'))

        if parser.has_section('defences'):
            self.defences = mb_subs.actions(parser.items('defences'))
