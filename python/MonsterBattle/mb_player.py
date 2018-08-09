# -------------------------------------------------------------------------
#  File:    mb_monster.py
#  Created: Tue Feb  7 20:26:02 2006
# -------------------------------------------------------------------------

import random
import string

import mb_io
import mb_subs
from mb_monster import Monster

class Player(Monster):
    """
    The Player is considered a special type of monster with a few more
    game book keeping related attributes.  The Player is considered
    a singleton but the creation of only one player is handled outside
    of this class.
    """

    def __init__(self, gamedir, filename = None):

        """
        Initialize player.
        """

        # The following attributes are internal and are not
        # defined in the file.

        self.game_dir = gamedir
        self.last_dir = ''

        # Last direction that sprite was facing.

        self.last_sprite_facing = None

        # The following can be specified in the Player config
        # file in addition to any Monster attributes.  If they
        # are not defined in the file, they will use these
        # defaults.

        self.extra_lives = 3
        self.start_x = 200
        self.start_y = 200

        # Read Monster attributes from file.

        Monster.__init__(self, self.game_dir, filename)
        self.read_in_config(filename)

    def read_in_config(self, filename):

        parser = Monster.read_in_config(self, filename)

        if parser.has_section('game'):

            if parser.has_option('game', 'extra_lives'):
                self.extra_lives = int(parser.get('game', 'extra_lives'))
            if parser.has_option('game', 'start_x'):
                self.start_x = int(parser.get('game', 'start_x'))
            if parser.has_option('game', 'start_y'):
                self.horns = int(parser.get('game', 'start_y'))

        return parser



