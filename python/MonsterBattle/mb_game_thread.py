# -------------------------------------------------------------------------
#  File:    mb_game_thread.py
#  Comment: An object of this class acts as the "time-slicer" of the
#           simulation engine.  Anytime, the simulation needs to pause
#           for display or timing reasons it calls GameThread.run(time).
#           This makes this object go into a time-slicing mode where it
#           can still process input events but still delays for time seconds.
#           Since the majority of time is actually spent in delays (compared
#           to actual I/O or processing) all keyboard control is processed
#           in the run method of this class.
# -------------------------------------------------------------------------

import os, sys
import random, time
import curses

import pygame
import pygame.image
import pygame.mixer
import pygame.time

import mb_io
from mb_buffer import ScreenBuffer
from mb_option import Option
from mb_option_manager import OptionManager

class GameThread:

    def __init__(self, screen, resources):
        self.quit         = False
        self.screen       = screen
        self.resources    = resources

        #self.raycaster    = raycaster

    def quit_game(self):
        return bool(self.quit)

    def run(self, delay):

        # Get initial number of ticks
        start = pygame.time.get_ticks()
        # Delay is seconds, calculate stop as start time + desired milliseconds
        stop = start + delay * 1000

        # If user has already quit, return immediately
        if self.quit == True:
            return

        while pygame.time.get_ticks() < stop:
            pygame.event.pump()

            # We want to sleep for <delay> seconds
            for event in pygame.event.get():

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        #
                        # Break simulation loop.
                        self.quit = True
                        return

                    if event.key == pygame.K_c:
                        #
                        # Display fake character screen.
                        #
                        mb_io.character_screen(self.screen)

                    if event.key == pygame.K_m:
                        #
                        # Display map.
                        #
                        mb_io.map_screen(self.screen, self.resources['gamedir'])

                    if event.key == pygame.K_o:
                        #
                        # Display options screen.
                        #
                        options = OptionManager(self.screen, self.resources['splash'])
                        options.add_option('Music Volume', range(11), mb_io.get_music_volume(), mb_io.set_music_volume)
                        options.add_option('Effects Volume', range(11), mb_io.get_sound_volume(), mb_io.set_sound_volume)
                        options.start()


            # Reset weapon firing.

            self.resources['player_fired'] = False
            turbo = 0
            if pygame.key.get_pressed()[pygame.K_LCTRL]:
                turbo = 2

            if pygame.key.get_pressed()[pygame.K_a]:
                 if self.resources['player'].current_weapon != None:
                     self.resources['player'].weapon_pointing_angle = (self.resources['player'].weapon_pointing_angle - 20) % 360

            if pygame.key.get_pressed()[pygame.K_d]:
                if self.resources['player'].current_weapon != None:
                    self.resources['player'].weapon_pointing_angle = (self.resources['player'].weapon_pointing_angle + 20) % 360

            if pygame.key.get_pressed()[pygame.K_UP]:
                self.resources['player'].y -= 10 * turbo
                self.resources['player'].last_dir = 'u'
            if pygame.key.get_pressed()[pygame.K_DOWN]:
                self.resources['player'].y += 10 * turbo
                self.resources['player'].last_dir = 'd'
            if pygame.key.get_pressed()[pygame.K_LEFT]:
                self.resources['player'].x -= 10 * turbo
                self.resources['player'].last_dir = 'l'
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                self.resources['player'].x += 10 * turbo
                self.resources['player'].last_dir = 'r'

            if pygame.key.get_pressed()[pygame.K_SPACE]:
                self.resources['player_fired'] = True

            if pygame.key.get_pressed()[pygame.K_TAB]:
                self.resources['player_switched_weapon'] = True

            #if self.resources['player'].current_weapon != None:
            #    (mouse_x, mouse_y) = pygame.mouse.get_pos()
            #    self.resources['player'].weapon_pointing_angle = self.resources['player'].aim_pos(mouse_x, mouse_y)
            #    if pygame.mouse.get_pressed() == (1, 0, 0):
            #        self.resources['player_fired'] = True

            # Sleep for a small amount of time
            pygame.time.wait(50)





