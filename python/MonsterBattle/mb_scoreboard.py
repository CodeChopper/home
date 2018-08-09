
import os
import time
import pygame
import mb_io

class ScoreBoard:
    """
    This class is used to display the health scoreboard.
    """

    def __init__(self, graphics, resources, game_thread):

        self.graphics    = graphics
        self.win         = self.graphics['map']
        self.main        = self.graphics['main']
        self.resources   = resources
        self.screen      = resources['screen']
        self.game_thread = game_thread
        self.lines       = []
        self.line_color  = 'yellow'
        self.max_lines   = 20
        self.display_count = 0
        self.top_beings = []

    def update(self, location):

        self.lines = []

        beings = location.beings

        #beings.sort(key = lambda b: b.health)
        #beings.reverse()
        #top_beings = beings[:self.max_lines]

        self.top_beings = beings
        for (i, being) in enumerate(self.top_beings):
            mesg = "%s [%d]" % (being.name, being.health)
            self.lines.append((mesg, self.line_color))

    def display_buffer(self):

        # Display contents of line buffer.

        i = 0
        for line in self.lines:
            (mesg, color) = line
            text = self.graphics['fonts']['text'].render(mesg, 1, self.graphics['colors'][color])
            blit_info = ( text, (10, 10 + (i*15)) )
            self.win.bitblt(blit_info)
            i += 1

        self.display_count += 1
        if self.display_count % 10 == 0:
            print
            for (i, being) in enumerate(self.top_beings):
                mesg = "%s [%d]" % (being.name, being.health)
                print mesg






