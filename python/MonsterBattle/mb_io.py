# -------------------------------------------------------------------------
#  File:    mb_io.py
#  Created: Tue Feb  7 20:37:34 2006
# -------------------------------------------------------------------------

import os
import sys
import time
import pygame
import pygame.image
import pygame.mixer
import pygame.time

from mb_monster import Monster
from mb_buffer import ScreenBuffer
from mb_option import Option
from mb_option_manager import OptionManager
from mb_globals import *

music = None

# -------------------------------------------------------------------------
# Setup some global i/o devices.
# -------------------------------------------------------------------------

def splash_file():
    splash = None
    try:
        splash = open('mb_splash.jpg')
    except:
        print "Note: Create mb_splash.jpg in code directory if you want a start up splash screen."
    return splash

def write_text(graphics, window_name, mesg, x, y, color):
    """
    Print to the graphics_window using text font.
    """
    fonts = graphics['fonts']
    t = fonts['text'].render(mesg, 1, color)
    blit_info = (t, (x, y))
    graphics[window_name].bitblt(blit_info)

def set_sound_volume(vol):

    # We need global since we are
    # changing the value.

    global g_sound_volume

    g_sound_volume = vol
    play_sound('punch')

def set_music_volume(vol):

    # We need global since we are
    # changing the value.

    global g_music_volume

    g_music_volume = vol
    music.set_volume(g_music_volume / 10.0)

def get_sound_volume():
    return g_sound_volume

def get_music_volume():
    return g_music_volume

def play_music(file):

    # Change the global music object, not a
    # local instance.

    global music

    if os.path.exists(file):
        music = pygame.mixer.Sound(file)
        music.set_volume(g_music_volume / 10.0)
        music.play(-1)

def play_sound(name):

    fname = os.path.join('sounds',name + '.ogg')
    if os.path.exists(fname):
        sound = pygame.mixer.Sound(fname)
        sound.set_volume(g_sound_volume / 10.0)
        sound.play()

def play_soundpath(fname):

    if os.path.exists(fname):
        sound = pygame.mixer.Sound(fname)
        sound.set_volume(g_sound_volume / 10.0)
        sound.play()

def character_screen(screen):
    """
    This is an example of using the ScreenBuffer class to
    create an additional screen that can be displayed with
    a key press.
    """

    # Create character screen.
    char_screen = ScreenBuffer(screen, 800, 600)

    # This could have sub windows (PyGameWin objects)
    # but since we're using the whole screen, we'll
    # write to this surface directly.

    yellow = (255, 255, 0)
    font = pygame.font.Font(None, 24)

    text = font.render('Character Screen', 1, yellow)
    blit_info = (text, (300, 250))
    char_screen.buffer.bitblt(blit_info)

    text = font.render('[Press Escape to Continue]', 1, yellow)
    blit_info = (text, (50, 500))
    char_screen.buffer.bitblt(blit_info)

    # Display the screen.
    char_screen.render()

    wait = True
    while wait:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    wait = False


def map_screen(screen, gamedir):
    """
    Show the map for this level.
    """

    # Create new buffer for screen.
    map_screen = ScreenBuffer(screen, 800, 600)

    # This could have sub windows (PyGameWin objects)
    # but since we're using the whole screen, we'll
    # write to this surface directly.

    map_image = pygame.image.load(os.path.join(gamedir, 'Images/map.jpg'))
    map_image =  pygame.transform.scale(map_image, (800, 600))
    blit_info = (map_image, (0, 0))
    map_screen.buffer.bitblt(blit_info)

    # Display the screen.
    map_screen.render()

    wait = True
    while wait:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    wait = False

def shrink_image(globals, screen, image_fname):
    """
    Shrink an image from full screen to nothing.
    """

    zoom_screen = ScreenBuffer(screen, globals['screen_width'], globals['screen_height'])
    imag = pygame.image.load('%s' % image_fname)

    start_width  = globals['screen_width']
    start_height = globals['screen_height']
    shrink_factor = 20

    for i in xrange(0, 20):

        offset = shrink_factor * i

        w = start_width - offset
        h = start_height - offset

        imag = pygame.transform.scale(imag, (w, h))
        blit_info = (imag, (offset/2, offset/4))
        zoom_screen.buffer.bitblt(blit_info)
        zoom_screen.render()
        zoom_screen.buffer.surf.fill((0,0,0))

def zoom_image(globals, screen, image_fname):
    """
    Zoom a message to full screen.
    """

    zoom_screen = ScreenBuffer(screen, globals['screen_width'], globals['screen_height'])
    tru_imag = pygame.image.load('%s' % image_fname)

    width = int(globals['screen_width'] / 20)
    height = int(globals['screen_height'] / 20)

    for percentage in xrange(0, 22, 1):

        w = int(width * percentage)
        h = int(height * percentage)

        imag = pygame.transform.scale(tru_imag, (w, h))
        blit_info = (imag, (0,0))
        zoom_screen.buffer.bitblt(blit_info)
        zoom_screen.render()
        zoom_screen.buffer.surf.fill((0,0,0))



