#!/usr/bin/env python
#
# MonsterBattle: monsterbattle.py
#
# Copyright 2008 Team MB
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import datetime
import glob
import math
import os
import random
import string
import sys
import time

import pygame
import pygame.image
from pygame.locals import *
from optparse import OptionParser

# MonsterBattle Modules

import mb_subs   # Misc utility functions.
import mb_io     # Display, sound, input functions.

from mb_go import GameObject
from mb_monster import Monster
from mb_location import Location
from mb_map import LocationMap
from mb_trap import Trap
from mb_weapon import Weapon
from mb_projectile import Projectile
from mb_option import Option
from mb_option_manager import OptionManager
from mb_win import PyGameWin

from mb_buffer import ScreenBuffer
from mb_game_thread import GameThread
from mb_scroll import ScrollWin
from mb_scoreboard import ScoreBoard
from mb_init import GameStartUp

# Bullets if monster has weapon.

from mb_bullets import Bullet
from mb_bullets import BulletManager

# Points that float off of screen when
# health or traps are encountered.

from mb_bonus_points import Point
from mb_bonus_points import PointManager

# Particle explosions for fatalities.

from mb_particle_explosion import Particle
from mb_particle_explosion import ParticleManager

# Another type of explosion.

from mb_derez_explosion import Derez
from mb_derez_explosion import DerezManager

##################################################################
#  Clear arena (playfield).                                      #
##################################################################

def clear_arena(arena, location, scroll, scoreboard, fonts, colors,
                mid_height, max_height, mid_width, max_width):

    blit_info = (location.get_sprite_frame(), (0,0))
    arena.bitblt(blit_info)

    # drawn box around scrolling messages.
    x1 = 0 ; y1 = 0 ; x2 = 400 ; y2 = 130
    rect = pygame.Rect(x1, y1, x2, y2)
    pygame.draw.rect(arena.surf, colors['blue'], rect, 4)
    
    scroll.display_buffer()
    scoreboard.display_buffer()

##################################################################
#  Zoom text effect.                                             #
##################################################################

def zoom_text(message, zfonts, location, arena, main_screen, color):

    """
    This zooms a piece of text into the middle of the playing field.
    """

    for i in zfonts:

        blit_info = (location.get_sprite_frame(), (0,0))
        arena.bitblt(blit_info)

        # Blit the main screen buffer to the real screen.
        main_screen.render()

        text = i.render(message, 1, color)
        blit_info = (text, (100, 100))
        arena.bitblt(blit_info)

        # Blit the main screen buffer to the real screen.
        main_screen.render()

##################################################################
#  Draw line between two objects.                                #
##################################################################

def object_line(arena, m1, m2, color):

    """
    Draw line between center of two objects.
    """

    pygame.draw.line(arena.surf, color, (m1.x, m1.y), (m2.x, m2.y), 2);

##################################################################
#  Draw ring around two objects.                                 #
##################################################################

def object_ring(arena, m1, m2, color):

    """
    Draw outer ring around two objects.
    """

    pygame.draw.circle(arena.surf, color, (m1.x, m1.y), m1.radius + 5, 2);
    pygame.draw.circle(arena.surf, color, (m2.x, m2.y), m2.radius + 5, 2);
    mb_io.play_sound('pong')

##################################################################
#  Distance between two objects.                                 #
##################################################################

def object_distance(m1, m2):

    # Compute distance between the two objects.

    xdiff = m1.x - m2.x
    ydiff = m1.y - m2.y

    return math.sqrt((xdiff*xdiff) + (ydiff*ydiff))

##################################################################
#  Check for collision between two objects.                      #
##################################################################

def object_collision(m1, m2):

    """
    Check for outer collision for monsters.
    """

    try:
        # return outer_object_collision(m1, m2)
        return inner_object_collision(m1, m2)
    except Exception, e:
        raise RuntimeError, "object_collision()-> %s" % e

##################################################################
#  Check for outer collision (more forgiving).                   #
##################################################################

def outer_object_collision(m1, m2):

    dist = object_distance(m1, m2)

    # If the distance between the centers of the
    # two objects is less than the sum of both of
    # their radii than they must have collided.

    # Since this is checking for a small threshold
    # this is only true when the outer rings of
    # the objects overlap.

    radius = m1.radius + m2.radius
    if abs(dist - radius) < 1.00:
        return True
    else:
        return False

##################################################################
#  Check for inner collision (less forgiving).                   #
##################################################################

def inner_object_collision(m1, m2):

    dist = object_distance(m1, m2)
    if dist < m1.radius or dist < m2.radius:
        return True
    else:
        return False

##################################################################
#  Monster resurrection.                                         #
##################################################################

def check_resurrection(chance, graveyard, location, scroll):

    dead_guy = None
    if chance > random.uniform(0,100):
        dead_guy = graveyard.random_being()
        dead_guy.health = random.uniform(5, 25)
        graveyard.move_to(location, dead_guy)
        dead_guy.inc_num_resurrections()

        mesg = "%s has been resurrected!" % dead_guy.name
        scroll.line_out(mesg, 'pink')

    return dead_guy

##################################################################
#  Monster mutation.                                             #
##################################################################

def incubate_mutation(location, chance, scroll):

    mutant_baby = None
    if chance > random.uniform(0,100):

        parent_a = location.random_being()
        possible_mates = list(set(location.beings) - set([parent_a]))
        parent_b = random.choice(possible_mates)
        mutant_baby = parent_a + parent_b

        if location.has_name(mutant_baby.name):
            # Abort! Don't create duplicate mutants.
            del mutant_baby
            mutant_baby = None
        else:
            mb_io.play_sound('mutation')
            mesg = '%s has mutated with %s creating %s!' % \
                 (parent_a.name, parent_b.name, mutant_baby.name)
            scroll.line_out(mesg, 'pink')

    return mutant_baby

##################################################################
#  Main                                                          #
##################################################################

def main(argv):

    # Create argument parser.

    parser = OptionParser()
    parser.add_option('-l', '--log', dest='log_fname', default='monster-battle.log',
                      help='specify simulation log file.')
    parser.add_option('-g', '--gamepack', dest='gamepack_dir', default=None,
                      help='specify gamepack directory.')

    (options, args) = parser.parse_args()

    # Initialize game data, globals and other startup code.

    if not options.gamepack_dir:
        raise RuntimeError('Please specify gamepack with -g <dir> or --gamepack <dir>')

    log_f = open(options.log_fname, 'w')
    print >>log_f
    print >>log_f, "  MonsterBattle Activity Log"
    print >>log_f, "  started @ %s" % datetime.datetime.now().isoformat()

    try:
        game_start = GameStartUp(options.gamepack_dir)

        # Display splash screen.

        game_start.display_splash()
        game_start.start_music()

    except Exception, e:
        raise RuntimeError, "game init-> %s" % e

    globals     = game_start.globals
    colors      = game_start.colors
    screen      = game_start.screen
    main_screen = game_start.main_screen
    graphics    = game_start.windows

    # These lists hold the different types of objects that are
    # placed in the game locations.

    traps_loaded       = []
    weapons_loaded     = []
    projectiles_loaded = []
    monsters_loaded    = []

    # Various counts and stats
    num_mutations = 0
    num_resurrections = 0
    
    # Battlemap holds the locations which allow combat.

    battlemap = LocationMap()

    ##################################################################
    #  Load game data from a single directory containing game data   #
    #  files.                                                        #
    ##################################################################

    game_start.boot_message('Loading game objects')

    gamedir = globals['gamedir']

    try:
        gameObjects = []
        for gamefile in glob.glob( os.path.join(gamedir,'*') ):
            if os.path.isfile(gamefile):
                go = GameObject(gamedir, gamefile)
                gameObjects.append(go)
    except Exception, e:
        raise RuntimeError, "loading game objects-> %s" % e

    game_start.boot_message('Sorting game objects')

    # Load projectile type game objects first since weapons depend on them.

    for go in gameObjects:
        if go.type == 'projectile':
            j = Projectile(gamedir, go.filename)
            projectiles_loaded.append(j)
    try:
        for go in gameObjects:
            if go.type == 'location':
                l = Location(globals, gamedir, go.filename)
                battlemap.add_location(l)
            elif go.type == 'trap':
                t = Trap(gamedir, go.filename)
                traps_loaded.append(t)
            elif go.type == 'weapon':
                w = Weapon(gamedir, projectiles_loaded, go.filename)
                weapons_loaded.append(w)
            elif go.type == 'monster':
                m = Monster(gamedir, go.filename)
                monsters_loaded.append(m)
            elif go.type == 'projectile':
                pass
            else:
                print 'the game object type "%s" is unknown!' % go.type

    except Exception, e:
        raise RuntimeError, "sorting game objects-> %s" % e

    game_start.boot_message('Initializing built-in locations')

    # The lockers are where the monsters hang out before battle.

    try:
        lockers = Location(globals, gamedir)
        lockers.set_name("lockers")
    except Exception, e:
        raise RuntimeError, "creating lockers-> %s" % e

    # Dead monsters go to the graveyard.

    try:
        graveyard = Location(globals, gamedir)
        graveyard.set_name("graveyard")
    except Exception, e:
        raise RuntimeError, "creating graveyard-> %s" % e

    # A location map must call this method to activate
    # the links between the locations before the
    # simulation starts.

    game_start.boot_message('Linking locations')

    try:
        battlemap.link_locations()
    except Exception, e:
        raise RuntimeError, "linking locations-> %s" % e

    game_start.boot_message('Placing traps')

    # Assign traps to their locations.
    # The same trap type can exist in multiple locations.

    try:
        traps_used = []

        for location in battlemap.locations:
            for location_trap_name in location.traps:
                # search for corresponding trap game object.
                for trap in traps_loaded:
                    if trap.name.lower() == location_trap_name.lower():
                        location.add_object(trap)
                        traps_used.append(trap)
                        break

        remaining_traps = list(set(traps_loaded) - set(traps_used))

    except:
        raise RuntimeError, "assigning traps-> %s" % e

    game_start.boot_message('Placing weapons')

    # Assign weapons to their locations.
    # The same weapon type can exist in multiple locations.

    try:
        weapons_used = []

        for location in battlemap.locations:
            for location_weapon_name in location.weapons:
                # search for corresponding weapon game object.
                for weapon in weapons_loaded:
                    if weapon.name.lower() == location_weapon_name.lower():
                        location.add_object(weapon)
                        weapons_used.append(weapon)
                        break

        remaining_weapons = list(set(weapons_loaded) - set(weapons_used))
    except Exception, e:
        raise RuntimeError, "assigning weapons-> %s" % e

    # Time for monsters already starting with a weapon, to pick up
    # the real weapon game object.  They only have the weapon
    # name in their config.  Time to lock and load.

    game_start.boot_message('Monsters picking up weapons')

    for m in monsters_loaded:
        m.lock_and_load(weapons_loaded)

    # Assign monsters to their locations.
    # The same monster type can exist in multiple locations.

    game_start.boot_message('Assigning monsters')

    print >>log_f, "\n Number of monsters loaded: %d" % len(monsters_loaded)
    for monster in monsters_loaded:
        lockers.add_being(monster)
        print >>log_f, "  starting health of %s = %d" % (monster.name, monster.health)

    print
    print >>log_f, "\n Number of monsters in locker room: %d" % len(lockers.beings)
    print >>log_f

    ###      try:
    ###          game_start.boot_message('Distributing extra traps and weapons')
    ###  
    ###          # Distribute remaining traps and weapons among battle locations.
    ###  
    ###          for trap in remaining_traps:
    ###              battlemap.rand_location().add_object(trap)
    ###  
    ###          for weapon in remaining_weapons:
    ###              battlemap.rand_location().add_object(weapon)
    ###  
    ###          game_start.boot_message('Loading monsters')
    ###  
    ###      except Exception, e:
    ###          raise RuntimeError, "distributing remaining-> %s" % e

    # Define windows as late as possible that way we don't end up with
    # a blank screen while things are initializing.

    game_start.build_windows()

    # Initialize GameThread object.  This is used to manage any time delays
    # in the sim and also handles all input (i.e. keyboard) events.
    # Without it, the input events would be blocked out for seconds at a
    # time whenever the sim would pause to display something.

    try:
        game_thread = GameThread(screen, globals)
    except Exception, e:
        raise RuntimeError, "init game_thread-> %s" % e

    ##################################################################
    #  Main simulation loop.                                         #
    ##################################################################

    zfonts = list()
    for i in xrange(30, 50, 1):
        zfonts.append(pygame.font.Font(None, i))

    scroll = ScrollWin(graphics, globals, game_thread, log_f)
    scoreboard = ScoreBoard(graphics, globals, game_thread)

    main_win = graphics['main']
    fonts    = graphics['fonts']
    colors   = graphics['colors']
    arena    = graphics['map']

    max_width   = arena.width
    max_height  = arena.height
    mid_height  = int(max_height / 2)
    mid_width   = int(max_width / 2)

    # This object keeps track of the bullets.
    bullets = BulletManager(arena.surf, 0, 0, max_width, max_height)

    # This object keeps track of points that appear and float off the screen.
    points = PointManager(arena, 0, 0, max_width, max_height, fonts)

    # This object keeps track of particles for particle explosions.
    particles = ParticleManager(0, 0, max_width, max_height)

    # This object keeps track of particles for derez explosions.
    derezes = DerezManager(0, 0, max_width, max_height)

    current_location = battlemap.rand_location()
    #for monster in lockers.beings:
    #    zoom_text(monster.name, zfonts, current_location, arena, main_win, colors['blue'])

    while not game_thread.quit_game():

        #
        # Phase 1: Move monsters from locker room into arena.
        #

        try:
            while lockers.being_count() > 0:
                new_monster = lockers.random_being()
                lockers.move_to(current_location, new_monster)
        except Exception, e:
            raise RuntimeError, "adding monster-> %s" % e

        ##################################################################
        ##################################################################
        #  Massive amount of combat and gameplay code begins here!       #
        ##################################################################
        ##################################################################

        try:

            # Set this anywhere in the code before the main screen render to
            # get a slight pause after the render.  E.g. after a taunt.
            display_pause = False

            if current_location.being_count() == 0:
                return

            # Clear arena for next frame

            clear_arena(arena, current_location, scroll, scoreboard, fonts, colors,
                        mid_height, max_height, mid_width, max_width)

            # draw borders
            rect = pygame.Rect(0, 0, arena.width-2, arena.height-2)
            pygame.draw.rect(arena.surf, colors['purple'], rect, 4)

            # Initialize monsters with random location.

            for m in current_location.beings:
                if m.is_first_round:
                    m.is_first_round = False
                    m.x = int(random.uniform(5, current_location.width - 5))
                    m.y = int(random.uniform(5, current_location.height - 5))

            # Initialize traps with random location if
            # new to location.  If not first time, just
            # redraw in current location.

            for obj in current_location.objects:
                if obj.type == 'trap':

                    if obj.is_first_round:
                        obj.x = int(random.uniform(40, current_location.width - 40))
                        obj.y = int(random.uniform(40, current_location.height - 40))
                        obj.radius = len(obj.name)/2
                        obj.is_first_round = False

                    # Draw current position!

                    text = fonts['label'].render(obj.name, 1, colors['pink'])
                    blit_info = (text, (obj.x - obj.radius, obj.y + obj.radius) )
                    arena.bitblt(blit_info)
                    blit_info = (obj.get_sprite_frame(), (obj.x, obj.y))
                    arena.bitblt(blit_info)

                    # While we're dealing with traps, check for collision against monsters.

                    for monster in current_location.beings:
                        if object_collision(monster, obj):
                            commentary, damage = obj.trigger_trap(monster)
                            if damage >= 0:
                                mesg = "%s = %d damage." % (commentary, damage)
                                scroll.line_out(mesg)
                                points.add_point(monster.x, monster.y, damage)
                                current_location.del_object(obj)

                            if monster.dead():
                                mb_io.play_sound('fatality')
                                fatal_msg = '%s %s!' % (monster.name, monster.fatality())
                                zoom_text('Trapped!', zfonts, current_location, arena, main_win, colors['purple'])
                                scroll.line_out(fatal_msg, 'red')
                                monster.drop_weapons(graphics['status'], current_location)
                                current_location.move_to(graveyard, monster)

            # Initialize weapons with random location if
            # new to location.  If not first time, just
            # redraw in current location.

            for obj in current_location.objects:
                if obj.type == 'weapon':

                    if obj.is_first_round:
                        obj.x = int(random.uniform(20, current_location.width - 20))
                        obj.y = int(random.uniform(20, current_location.height - 20))
                        obj.radius = len(obj.name)
                        obj.is_first_round = False

                    # Draw current position!

                    text = fonts['label'].render(obj.name, 1, colors['pink'])
                    blit_info = (text, (obj.x - obj.radius, obj.y + obj.radius) )
                    arena.bitblt(blit_info)
                    blit_info = (obj.get_sprite_frame(), (obj.x, obj.y))
                    arena.bitblt(blit_info)

                    # While we're dealing with weapons, check for collision against monsters.

                    for monster in current_location.beings:
                        if object_collision(monster, obj):
                            monster.add_weapon(obj, current_location)
                            mesg = '%s has picked up the %s!' % (monster.name, obj.name)
                            scroll.line_out(mesg, 'tan')

            # Update position of monsters.

            for m in current_location.beings:

                # save old info

                old_x = m.x
                old_y = m.y

                # Update velocity.

                m.velocity = 8

                if m.move_waypoint_x is None and m.move_waypoint_y is None:
					
					# including objects instead of just beings creates some non-converging
					# runs as all beings gravitate towards health pack.

                    # waypoint_objects = current_location.beings + current_location.objects                 
                    waypoint_objects = current_location.beings                                  
                    next_waypoint = random.choice(waypoint_objects)

                    m.move_waypoint_x = next_waypoint.x + int(random.uniform(-40,40))
                    m.move_waypoint_y = next_waypoint.y + int(random.uniform(-40,40))

                # Keep moving until next waypoint is reached.

                if m.move_waypoint_x is None:
                    pass
                else:
                    if abs(m.x - m.move_waypoint_x) < 10:
                        m.move_waypoint_x = None
                    elif m.x > m.move_waypoint_x:
                        m.x -= m.velocity
                    else:
                        m.x += m.velocity

                if m.move_waypoint_y is None:
                    pass
                else:
                    if abs(m.y - m.move_waypoint_y) < 10:
                        m.move_waypoint_y = None
                    elif m.y > m.move_waypoint_y:
                        m.y -= m.velocity
                    else:
                        m.y += m.velocity

                # Blit current sprite frame at current position to buffer.

                blit_info = (m.get_sprite_frame(), (m.x-10, m.y-12))
                arena.bitblt(blit_info)

                #
                # Uncomment this bounding circle to debug collision detection.
                #
                #pygame.draw.circle(arena.surf, colors['yellow'], (m.x, m.y), m.radius, 1);

                # Draw labels underneath sprite.

                monster_label = "%s" % (m.name)
                text = fonts['text'].render(monster_label, 1, colors['white'])
                blit_info = (text, (m.x - m.radius + 3, m.y + 5) )
                arena.bitblt(blit_info)

                try:
                    if m.current_weapon:
                        enemy_target = random.choice(current_location.beings)
                        m.weapon_pointing_angle = m.aim(enemy_target)
                except Exception, e:
                    raise RuntimeError, "aiming weapon-> %s" % e

                # Draw weapon if monster has one.

                try:
                    if m.current_weapon is not None:
                        rotated_weapon_sprite = m.current_weapon.get_small_sprite_frame()
                        rotated_weapon_sprite = pygame.transform.rotate(rotated_weapon_sprite, -m.weapon_pointing_angle)
                        blit_info = (rotated_weapon_sprite, (m.x, m.y-10))
                        arena.bitblt(blit_info)

                        m.weapon_pointing_x = m.x + (m.radius * math.cos(math.radians(m.weapon_pointing_angle)))
                        m.weapon_pointing_y = m.y + (m.radius * math.sin(math.radians(m.weapon_pointing_angle)))

                except Exception, e:
                    raise RuntimeError, "drawing weapon-> %s" % e

                # Check if we've fired this round. 

                if m.current_weapon is not None and m.current_weapon.projectile:
                    if random.uniform(0, 100) < 10:
                        bullets.add_bullet(m, m.current_weapon)

                # Check for collision with other monster.

                # Compute remaining victim monsters. (Exclude attacker.)

                available_monsters = list(set(current_location.beings) - set([m]))

                try:
                    for other_monster in available_monsters:

                        if object_collision(m, other_monster):

                            # Monsters of the same family don't attack each other.

                            if not m.family or (m.family != other_monster.family):

                                object_line(arena, m, other_monster, colors['cyan'])
                                object_ring(arena, m, other_monster, colors['green'])

                                # reuse code and variables from previous combat sim.

                                attacker = m
                                thing = other_monster

                                if random.uniform(0, 100) < 25 and attacker.has_taunts:
                                    print "<just taunt!>"
                                    
                                    #
                                    # Just taunt don't really attack.
                                    #
                                    try:
                                        mesg = "%s %s %s" % (attacker.name, thing.name, attacker.taunt())
                                    except Exception, e:
                                        print "<I think taunts for [%s] are messed up.>" % attacker.name
                                        
                                    print "[taunt: %s]" % mesg
                                    # scroll.line_out(mesg, 'white')
                                    # zoom_text(attacker.taunt(), zfonts, current_location, arena, main_win, colors['white'])
                                else:
                                    #
                                    # Really attack!
                                    #
                                    # Save thing's health before the attack.

                                    print "<really attack!>"

                                    pre_health = thing.health
                                    if attacker.current_weapon and not attacker.current_weapon.projectile:
                                        attack_string = attacker.weapon_attack(thing)
                                    else:
                                        attack_string = attacker.attack(thing)

                                    attack_mesg = "%s %s" % (attacker.name, attack_string)
                                    scroll.line_out(attack_mesg)

                                    if thing.dead():
                                        mb_io.play_sound('fatality')
                                        fatal_msg = '%s %s!' % (thing.name, thing.fatality())
                                        scroll.line_out(fatal_msg, 'red')
                                        mb_io.play_sound('explosion')
                                        for i in xrange(100):
                                            derezes.add_derez(thing.x, thing.y)
                                        thing.drop_weapons(graphics['status'], current_location)
                                        current_location.move_to(graveyard, thing)

                                        #
                                        # reward attacker with thing's pre health
                                        # attacker.health += pre_health
										#
										# going to replace this instead w/ code
										# that will drop an object w/ health points
										# where thing died. (i.e. life force)
										#

                                        attacker.inc_num_kills()

                except Exception, e:
                    raise RuntimeError, "checking collision-> %s" % e

                ##################################################################
                #  Check for collision with wall.  If there's a location to go   #
                #  to in that direction (i.e. no wall) then the monster (or      #
                #  player) leaves the screen and moves to new location.          #
                #  Otherwise bounce back from wall.                              #
                ##################################################################

                try:
                    wall_space = 2
                    jump_offset = 80

                    # Hitting left wall
                    if (m.x - m.radius - wall_space) <= 0:

                        if m.move_waypoint_x is not None:
                            m.move_waypoint_x += 25
                        mb_io.play_sound('wall')

                    # Hitting right wall
                    if (m.x + m.radius + wall_space) >= current_location.width:

                        if m.move_waypoint_x is not None:
                            m.move_waypoint_x -= 25
                        mb_io.play_sound('wall')

                    # Hitting top wall
                    if (m.y - m.radius - wall_space) <= 0:

                        if m.move_waypoint_y is not None:
                            m.move_waypoint_y += 25
                        mb_io.play_sound('wall')

                    # Hitting bottom wall
                    if (m.y + m.radius + wall_space) >= current_location.height:

                        if m.move_waypoint_y is not None:
                            m.move_waypoint_y -= 25
                        mb_io.play_sound('wall')

                except Exception, e:
                    raise RuntimeError, "wall collision-> %s" % e

            ##################################################################
            #  Handle bullets for this round (frame).                        #
            ##################################################################

            try:
                monsters_hit = bullets.fire_bullets(current_location.beings)
                bullets.draw_bullets(arena)

                # Now check if any of the monsters hit are dead from the bullet.

                for monster in monsters_hit:
                    if monster.dead():
                        try:
                            fatal_msg = '%s %s!' % (monster.name, monster.fatality())
                            scroll.line_out(fatal_msg, 'red')
                            for i in xrange(100):
                                particles.add_particle(monster.x, monster.y)
                            monster.drop_weapons(graphics['status'], current_location)
                            current_location.move_to(graveyard, monster)
                        except Exception, e:
                            raise RuntimeError, "monster dead-> %s" % e

            except Exception, e:
                raise RuntimeError, "handling bullets-> %s" % e

            ##################################################################
            #  Handle floating points for this round (frame).                #
            ##################################################################

            try:
                points.move_points()
                points.draw_points(colors['yellow'], colors['red'])
            except Exception, e:
                raise RuntimeError, "handling points-> %s" % e

            ##################################################################
            #  Handle particle explosions for this frame.                    #
            ##################################################################

            try:
                particles.move_particles()
                particles.draw_particles(arena.surf, colors['green'])
                derezes.move_derezes()
                derezes.draw_derezes(arena.surf, colors['blue'])
                game_thread.run(0.025)
            except Exception, e:
                raise RuntimeError, "handling particles-> %s" % e
        except Exception, e:
            print "Exception inside massive main loop code!\n" + str(e)
            raise e

        ##################################################################
        ##################################################################
        #  Massive amount of combat code ends here!                      #
        ##################################################################
        ##################################################################

        #
        # Phase 3: Check for resurrection.
        #

		# move this to a config file.
        p_resurrection = 0.3 # use small percent
        if graveyard.being_count() > 2:
            alive = check_resurrection(p_resurrection, graveyard, current_location, scroll)
            if alive:
                num_resurrections += 1
                mb_io.play_sound('resurrection')
        #
        # Phase 4: Check for mutation.
        #

		# move this to a config file.
        p_mutation = 0.2
        if current_location.being_count() > 2:
            mutant_baby = incubate_mutation(current_location, p_mutation, scroll)
            if mutant_baby:
                mesg = "%s is a new mutation!" % mutant_baby.name
                scroll.line_out(mesg, 'green')
                zoom_text(mesg, zfonts, current_location, arena, main_win, colors['green'])
                current_location.add_being(mutant_baby)
                num_mutations += 1

        ##################################################################
        #  Update status display.                                        #
        ##################################################################

        graphics['status'].clear()

        monster_count = "Monsters Remaining: %d" % current_location.being_count()
        text = graphics['fonts']['text'].render(monster_count, 1, graphics['colors']['cyan'])
        blit_info = (text, (10,4))
        graphics['status'].bitblt(blit_info)

        mutation_count = "Num Mutations: %d" % num_mutations
        text = graphics['fonts']['text'].render(mutation_count, 1, graphics['colors']['cyan'])
        blit_info = (text, (150,4))      
        graphics['status'].bitblt(blit_info)

        resurrection_count = "Num Resurrections: %d" % num_resurrections
        text = graphics['fonts']['text'].render(resurrection_count, 1, graphics['colors']['cyan'])
        blit_info = (text, (270, 4))      
        graphics['status'].bitblt(blit_info)

        ##################################################################
        #  Render current frame.  This should be the *only* place where  #
        #  the main screen is rendered.                                  #
        ##################################################################

        main_screen.render()
        if display_pause:
            time.sleep(1)

        if current_location.being_count() < 2:
            game_thread.quit = True

    ##################################################################
    #  Print out the winner and final standings and quit.            #
    ##################################################################

    time.sleep(3)
    pygame.mixer.stop()

    if current_location.being_count() == 1:
        winner = current_location.beings[0]
        winner_msg = "%s is the winner!" % winner.name
        mb_io.play_sound('phasor')
        main_screen.snapshot('mb_last_screen.bmp')
        mb_io.shrink_image(globals, screen, 'mb_last_screen.bmp')
        zoom_text(winner_msg, zfonts, current_location, arena, main_win, colors['yellow'])
        mb_io.play_sound('winner')
        time.sleep(3)
        
        print >>log_f, "\n"
        print >>log_f, " Winner is %s" % winner.name
        print >>log_f, " ________________________________________"      
        print >>log_f, " Number of mutations: %d" % num_mutations
        print >>log_f, " Number of resurrections: %d" % num_resurrections
        print >>log_f, " ________________________________________"
        print >>log_f, "\n"

##################################################################
#  Handle arguments and call main simulation function.           #
##################################################################

if __name__ == '__main__':
    try:
        main(sys.argv)
    except Exception, e:
        print "monsterbattle: error encountered!"
        print e
        print "Shutting down simulation..."
        print 
        sys.exit(1)


