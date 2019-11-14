# -------------------------------------------------------------------------
#  File:    mb_scroll.py
#  Created: Thu May  4 21:05:43 2006
#  By: 
#  Comment: This class handles printing to a window meant for scrolling.
#
#           Currently, it is not performing true scrolling with a buffer
#           but instead is just starting at the top, displaying top down
#           and clearing the screen when the window is full and starting
#           over.
#
# -------------------------------------------------------------------------

import os
import time
import pygame
import mb_io
import datetime

class ScrollWin:

    """
    This class is used to display a single line at a time in a scrolling window.
    """

    def __init__(self, graphics, resources, game_thread, log):

        self.graphics    = graphics
        self.win         = self.graphics['map']
        self.main        = self.graphics['main']
        self.resources   = resources
        self.screen      = resources['screen']
        self.game_thread = game_thread
        self.lines       = list()
        self.max_lines   = 6
        self.sim_start   = datetime.datetime.now()
        self.log         = log

        for i in xrange(self.max_lines):
            self.lines.append(('', 'red'))

    def line_out(self, mesg, color='cyan'):

        # write line to log file.

        now = datetime.datetime.now() - self.sim_start
        timestamp = "%08d.%d" % (now.seconds, now.microseconds)
        print >>self.log, "%s | %s" % (timestamp, mesg)

        # Shift existing lines up one.

        num_lines_shift = len(self.lines)-1
        for i in xrange(num_lines_shift):
            self.lines[i] = self.lines[i+1]

        # Add new line.
        self.lines[len(self.lines)-1] = (mesg, color)


    def display_buffer(self):

        # Display contents of line buffer.

        i = 0
        for line in self.lines:
            (mesg, color) = line
            text = self.graphics['fonts']['label'].render(mesg, 1, self.graphics['colors'][color])

            # x_bias = 0.05;
            x_bias = 0.01;
            y_bias = 0.1;
            
            # blit_info = ( text, (int(self.resources['screen_width'] * x_bias),
            #                      int(self.resources['screen_height'] * y_bias) + (i*20) ) )

            blit_info = (text, (8, 8 + (i*20)))
            self.win.bitblt(blit_info)
            i += 1






