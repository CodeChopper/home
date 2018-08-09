# --------------------------------------------------------------
#  File:    mb_buffer.py
#  Created: Mon Mar  6 22:04:39 2006
# --------------------------------------------------------------

import pygame
import pygame.image
from mb_win import PyGameWin

class ScreenBuffer:
    """
    This class implements a screen buffer that the program can
    write to.  It provides a method to flip itself to the main
    screen to achieve double buffering.
    """

    def __init__(self, screen, width, height):
        self.screen  = screen
        self.width   = width
        self.height  = height
        self.subwins = list()
        self.buffer  = PyGameWin(width, height, 0, 0)
        self.buffer.set_bg((0,0,0)) # black

    def add_win(self, win):
        """
        Add a nested PyGameWin to this buffer.
        """
        self.subwins.append(win)

    def render(self):

        """
        Blit all the subwindows to the buffer then
        blit the buffer to the real screen.
        """
        for w in self.subwins:
            self.buffer.bitblt(w.get_blit())

        self.screen.blit(self.buffer.surf, (0, 0))
        pygame.display.flip()

    def snapshot(self, fname):
        pygame.image.save(self.buffer.surf, fname)


