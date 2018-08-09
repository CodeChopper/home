# -------------------------------------------------------------------------
#  File:    mb_monster.py
#  Created: Tue Feb  7 20:26:02 2006
# -------------------------------------------------------------------------

import random
import string
import math

import mb_go
import mb_io
import mb_subs
from mb_go import GameObject

class Monster(GameObject):
    """
    The monster object holds attributes unique to that monster.
    A monster can attack and defend against other monsters.
    Successful attacks incurs damage to the victim's health.
    A monster is considered dead when its health points reach zero.

    """

    def __init__(self, gamedir, filename = None):

        """
        Create attributes that all monsters should have.

        """

        self.gamedir = gamedir

        # The following attributes are internal and are not
        # defined in the file.

        self.has_taunts = False
        self.total_damage = 0
        self.num_attacks  = 0
        self.kills = 0
        self.percent_health = 100.0
        self.resurrections = 0
        self.parents = list()
        self.current_target = None
        self.current_weapon = None
        self.current_weapon_index = 0

        # This needs to go here and not with the weapon
        # otherwise, it causes some funny side-effects.
        self.weapon_pointing_angle = 0
        self.weapon_pointing_x = 0
        self.weapon_pointing_y = 0

        self.location = None
        self.x = 0
        self.y = 0
        self.radius = 25
        self.velocity = 0
        self.move_waypoint_x = None
        self.move_waypoint_y = None
        self.is_first_round = True

        # The attributes below can be specified in the monster file.

        self.family = None
        self.attacks = list()
        self.defences = list()
        self.fatalities = list()
        self.taunts = list()
        self.weapons = list()

        # These are the physical traits of the monster.
        # They are normalized or relative to an average
        # 180 lb 6 ft. athletic human.

        self.height          = 1.0
        self.weight          = 1.0
        self.agility         = 1.0
        self.mobility        = 1.0  # i.e. running/walking speed
        self.quickness       = 1.0
        self.strength        = 1.0
        self.jaw_strength    = 1.0
        self.grip_strength   = 1.0
        self.dexterity       = 1.0
        self.intelligence    = 1.0
        self.aggressiveness   = 1.0
        self.weapon_ability  = 1.0
        self.skin_strength   = 1.0
        self.leaping_ability = 1.0

        # This is the default body makeup of the monster.

        self.heads = 1
        self.eyes  = 2
        self.horns = 0
        self.arms  = 2
        self.claws = 0
        self.legs  = 2
        self.tails = 0

        # Default health

        self.health = 0

        # call init of parent object.  (is this necessary?)

        GameObject.__init__(self, self.gamedir, filename)
        self.originalName = self.name

        if filename is not None:
            self.read_in_config(filename)


    def read_in_config(self, filename):

        parser = GameObject.read_in_config(self, filename)
        if parser.has_section('body'):

            if parser.has_option('body', 'heads'):
                self.heads = int(parser.get('body', 'heads'))
            if parser.has_option('body', 'eyes'):
                self.eyes = int(parser.get('body', 'eyes'))
            if parser.has_option('body', 'horns'):
                self.horns = int(parser.get('body', 'horns'))
            if parser.has_option('body', 'arms'):
                self.arms = int(parser.get('body', 'arms'))
            if parser.has_option('body', 'legs'):
                self.legs = int(parser.get('body', 'legs'))
            if parser.has_option('body', 'tails'):
                self.tails = int(parser.get('body', 'tails'))

        if parser.has_section('bio'):

            self.health  = int(parser.get('bio', 'health'))

            if parser.has_option('bio', 'family'):
                self.family = parser.get('bio', 'family')

            if parser.has_option('bio', 'height'):
                self.height = float(parser.get('bio', 'height'))

            if parser.has_option('bio', 'weight'):
                self.weight = float(parser.get('bio', 'weight'))

            if parser.has_option('bio', 'agility'):
                self.agility = int(parser.get('bio', 'agility'))
            else:
                self.agility = 25

            if parser.has_option('bio', 'mobility'):
                self.mobility = float(parser.get('bio', 'mobility'))

            if parser.has_option('bio', 'quickness'):
                self.quickness = float(parser.get('bio', 'quickness'))

            if parser.has_option('bio', 'strength'):
                self.strength = float(parser.get('bio', 'strength'))

            if parser.has_option('bio', 'jaw_strength'):
                self.jaw_strength = float(parser.get('bio', 'jaw_strength'))

            if parser.has_option('bio', 'grip_strength'):
                self.grip_strength = float(parser.get('bio', 'grip_strength'))

            if parser.has_option('bio', 'dexterity'):
                self.dexterity = float(parser.get('bio', 'dexterity'))

            if parser.has_option('bio', 'intelligence'):
                self.intelligence = float(parser.get('bio', 'intelligence'))

            if parser.has_option('bio', 'aggressiveness'):
                self.aggressiveness = float(parser.get('bio', 'aggressiveness'))

            if parser.has_option('bio', 'weapon_ability'):
                self.weapon_ability = float(parser.get('bio', 'weapon_ability'))

            if parser.has_option('bio', 'skin_strength'):
                self.skin_strength = float(parser.get('bio', 'skin_strength'))

            if parser.has_option('bio', 'leaping_ability'):
                self.leaping_ability = float(parser.get('bio', 'leaping_ability'))

            # Not ready to implement this yet.

            if parser.has_option('bio', 'weapons'):
                weapons_str = parser.get('bio', 'weapons')
                self.weapons = weapons_str.split(',')

        # end bio section.

        if parser.has_section('attacks'):
            self.attacks = mb_subs.actions(parser.items('attacks'))

        if parser.has_section('defences'):
            self.defences = mb_subs.actions(parser.items('defences'))

        if parser.has_section('fatalities'):
            self.fatalities = parser.options('fatalities')

        if parser.has_section('taunts'):
            self.taunts = parser.options('taunts')
            self.has_taunts = True

        return parser


    def dead(self):
        """
        Returns True if the being is out of health

        """
        return self.health <= 0

    def __add__(self, other):
        """
        This overloads the + operator to mutate
        this monster with another!  This returns
        a new (baby) monster.
        """

        embryo = Monster(self.gamedir)
        embryo.type = 'monster'
        embryo.family = None
        embryo.health = int((self.health + other.health)/2)

        if len(self.originalName) >= 4:
            a_name = self.originalName[:4]
        else:
            a_name = self.originalName

        if len(other.originalName) >= 4:
            b_name = other.originalName[-4:]
        else:
            b_name = other.originalName

        embryo.name = a_name + b_name
        embryo.originalName = embryo.name
        embryo.attacks.append(self.strongest_attack())
        embryo.attacks.append(other.strongest_attack())
        embryo.defences.append(self.strongest_defense())
        embryo.defences.append(other.strongest_defense())

        # The mutant will have an animated sprite that
        # is created by two random sprite frames chosen
        # from the parents which are then quickly flipped
        # back and forth.

        if self.image_list is not None and other.image_list is not None:
            a_image = random.choice(self.image_list)
            b_image = random.choice(other.image_list)
            embryo.image_list = [a_image, b_image]
            embryo.image_rate = 0
            embryo.image_back = self.image_back
            embryo.build_sprites()

        return embryo

    def strongest_attack(self):
        """
        Return the strongest attack of this monster.
        """

        strongest = ('',0)
        max = 0
        if self.attacks:
            for comment, dam in self.attacks:
                if dam > max:
                    max = dam
                    strongest = (comment,dam)

        return strongest

    def strongest_defense(self):
        """
        Return the strongest defense of this monster.
        """

        strongest = ('',0)
        max = 0
        if self.defences:
            for comment, dam in self.defences:
                if dam > max:
                    max = dam
                    strongest = (comment,dam)

        return strongest

    def lock_and_load(self, weapon_object_list):

        """
        This method should be called after the monster config file
        has already been loaded.  At this point the monster object
        will contain a list of weapon names (strings) in self.weapons.
        This method will replace the strings with the actual weapon
        game objects.  This method needs to be called after the
        weapon game objects have been loaded from disk.
        """

        real_weapons = []

        for w in self.weapons:
            for weapon in weapon_object_list:
                if weapon.name == w:
                    real_weapons.append(weapon)

        del self.weapons
        self.weapons = real_weapons
        if len(self.weapons) > 0:
            self.current_weapon_index = random.randint(0, len(self.weapons) - 1)
            self.current_weapon = self.weapons[self.current_weapon_index]

    def cycle_weapon(self):
        if self.current_weapon_index < (len(self.weapons) - 1):
            self.current_weapon_index += 1
        else:
            self.current_weapon_index = 0
        self.current_weapon = self.weapons[self.current_weapon_index]


    def attack(self, victim):
        """
        Launch an unarmed attack against the victim.
        """

        (attack, damage_points) = self.get_unarmed_attack()

        victim.health = mb_subs.subtract_to_floor(victim.health, damage_points)

        # update stats

        self.update_total_damage(damage_points)
        self.inc_num_attacks()

        # This will return the attack with the victim's name inserted.

        return attack % victim.name


    def weapon_attack(self, victim):

        """
        Launch an armed attack against the victim.
        """

        (attack, damage_points) = self.get_weapon_attack()

        victim.health = mb_subs.subtract_to_floor(victim.health, damage_points)

        # update stats

        self.update_total_damage(damage_points)
        self.inc_num_attacks()

        # This will return the attack with the victim's name inserted.

        return attack % victim.name



#     def attack(self, victim):

#         """
#         Launch an unarmed attack against the victim.  The victim
#         may be able to counter.
#         """

#         counter_attack = ''
#         attac = self.get_unarmed_attack()
#         attac = (attac[0], self.compute_damage(attac[1]))
#         attack = attac[0]
#         counter_attack, damage = victim.counter(attac)
#         attack_mesg  = '%s %s' % (self.name, attack % victim.name)

#         # Save damage and count attack for this attacker
#         self.update_total_damage(damage)
#         self.inc_num_attacks()

#         return damage, attack_mesg, counter_attack

#     def weapon_attack(self, victim):

#         """
#         Launch an armed attack against the victim.  The victim
#         may be able to counter.
#         """

#         attac = self.get_weapon_attack()
#         attac = (attac[0], self.compute_damage(attac[1]))
#         attack = attac[0]
#         counter_attack, damage = victim.counter(attac)
#         attack_mesg  = '%s %s' % (self.name, attack % victim.name)

#         # Save damage and count attack for this attacker
#         self.update_total_damage(damage)
#         self.inc_num_attacks()

#         return damage, attack_mesg, counter_attack


#     def counter(self, (attack, damage)):
#         """
#         Randomly defend against the attack for a given number of
#         anti-damage points.

#         """

#         if self.defences:

#             # Check if weapon has a defense.

#             if self.weapons:
#                 wep = random.choice(self.weapons)
#                 if wep.defences:
#                     defense = random.choice(wep.defences)
#                 else:
#                     defense = random.choice(self.defences)
#             else:
#                 defense = random.choice(self.defences)

#             defence, antidamage = defense
#             counter_attack = 'but %s %s!' % (self.name, defence)
#             damage = mb_subs.subtract_to_floor(damage, antidamage)
#         else:
#             counter_attack = ''

#         self.health = mb_subs.subtract_to_floor(self.health, damage)
#         return counter_attack, damage

    def aim(self, t):

        """
        Compute angle in degrees to aim weapon at target t.
        """

        # These angles increase clockwise starting
        # at the x-axis.
        # 0 = east, 90 = south, 180 = west 270 = north

        theta = 0   # initialize to default.

        mx = self.x
        my = self.y

        x = abs(mx - t.x)
        y = abs(my - t.y)
        r = math.sqrt(x**2 + y**2)

        # monster is to the upper left of target.
        if mx < t.x and my < t.y:
            theta = math.degrees(math.acos(x/r))

        # monster is to upper right of target.
        elif mx > t.x and my < t.y:
            theta = 90 + math.degrees(math.acos(y/r))

        # monster is to lower left of target.
        elif mx < t.x and my > t.y:
            theta = 360 - math.degrees(math.acos(x/r))

        # monster is to lower right of target.
        elif mx > t.x and my > t.y:
            theta = 270 - math.degrees(math.acos(y/r))
        else:
            pass

        return theta

    def aim_pos(self, t_x, t_y):

        """
        Compute angle in degrees to aim weapon at x,y coord.
        """

        # These angles increase clockwise starting
        # at the x-axis.
        # 0 = east, 90 = south, 180 = west 270 = north

        theta = 0   # initialize to default.

        mx = self.x
        my = self.y

        x = abs(mx - t_x)
        y = abs(my - t_y)
        r = math.sqrt(x**2 + y**2)

        # monster is to the upper left of target.
        if mx < t_x and my < t_y:
            theta = math.degrees(math.acos(x/r))

        # monster is to upper right of target.
        elif mx > t_x and my < t_y:
            theta = 90 + math.degrees(math.acos(y/r))

        # monster is to lower left of target.
        elif mx < t_x and my > t_y:
            theta = 360 - math.degrees(math.acos(x/r))

        # monster is to lower right of target.
        elif mx > t_x and my > t_y:
            theta = 270 - math.degrees(math.acos(y/r))
        else:
            pass

        return theta

    #
    # Modify damage a little bit so that it's not so predictable.
    #

    def compute_damage(self, damage):

        real_damage = 0
        if damage > 0:
            real_damage = random.randrange(damage)

        return real_damage


    def nocounter(self, (attack, damage) ):
        """
        No defense is possible, just take the damage and like it

        """
        self.health = mb_subs.subtract_to_floor(self.health, damage)
        return attack, damage

    def get_unarmed_attack(self):
        """
        Return random unarmed attack.
        """

        attack = None
        if self.attacks:
            attack = random.choice(self.attacks)

        return attack

    def get_weapon_attack(self):
        """
        Return random attack of the current weapon.
        """

        attack = None
        if self.current_weapon.attacks:
            attack = random.choice(self.current_weapon.attacks)

        return attack

    def get_random_counter(self):
        """
        Return random counter to defend against an attack.
        """

        counter = None
        counter = random.choice(self.defences)

        return counter


    # Return name of monster that has attacked me the most!
    # If a bunch of monsters have attacked me equal times,
    # this function will simply return the first one of
    # the bunch.

    def most_attacks(self):

        most = None
        max  = 0
        for m in self.attacker_names.keys():
            if self.attacker_names[m] > max:
                max = self.attacker_names[m]
                most = m

        return most


    def add_weapon(self, weapon, location):
        """
        Monster has encountered a weapon.  Add it to its
        weapon list and remove it from the current location.

        """
        self.weapons.append(weapon)
        if not self.current_weapon_index:
            self.current_weapon_index = 0
        else:
            self.current_weapon_index += 1
        self.current_weapon = self.weapons[self.current_weapon_index]

        location.del_object(weapon)


    def drop_weapons(self, win, location):
        """
        Drop all weapons monster has picked up and return them
        to the current location.

        """
        while self.weapons:
            weapon = self.weapons.pop()
            weapon.x = self.x
            weapon.y = self.y
            location.add_object(weapon)
            self.current_weapon = None
            self.current_weapon_index = None

    def move_left(self):
        return self.location.move_left(self)

    def move_right(self):
        return self.location.move_right(self)

    def move_up(self):
        return self.location.move_up(self)

    def move_down(self):
        return self.location.move_down(self)


    def fatality(self):
        """
        Return a fatality string, if available

        """
        if self.dead():
            fatality = 'has died'
            if self.fatalities:
                fatality = random.choice(self.fatalities)
            return fatality


    def taunt(self):
        """
        Return a taunt string if available
        """
        taunt = 'Yo mama!'
        if self.has_taunts:
            taunt = random.choice(self.taunts)
        return taunt


    def update_total_damage(self, damage):
        """
        Adds to total damage caused by this monster.

        """
        self.total_damage += damage


    def inc_num_attacks(self):
        """
        Increments the number of attacks caused by this monster.

        """
        self.num_attacks += 1

    def inc_num_kills(self):
        """
        Increments the number of kills caused by this monster.

        """
        self.kills += 1


    def inc_num_resurrections(self):
        """
        Increments the number of times this monster is resurrected.

        """
        self.resurrections += 1

