#    ---------------------------------------------------
#  -------------------------------------------------------
#   Option Manager
#  -------------------------------------------------------
#    ---------------------------------------------------

import pygame

from mb_option import Option
from mb_buffer import ScreenBuffer

class OptionManager(object):
    """
    Manages the display of Option objects and translation
    of option values to game settings

    """
    def __init__(self, screen, splash):
        # List of options
        self.options = list()
        # Current value's index in values list
        self.selected_option = None
        # Window we are displaying into.
        self.screen = screen
        #
        self.splash = splash

    def add_option(self, name, values, current_value, callback = None):
        coords = [ 10, 100 + len(self.options) * 25 ]
        option = Option(name, values, self.screen, coords, callback)
        option.set_value(current_value)
        self.options.append(option)

    def display(self, option_screen):
        for option in self.options:
            option.display(option_screen.buffer, self.selected_option == option)
        option_screen.render()

    def start(self):

        option_screen = ScreenBuffer(self.screen, 800, 600)

        yellow = (255, 255, 0)

        # Render background

        splash_pos = (0,0)
        option_screen.buffer.surf.blit(self.splash, splash_pos)
        self.write_text(option_screen.buffer, 'GAME OPTIONS', 10, 10, yellow, 24)
        self.write_text(option_screen.buffer, 'Use UP/DOWN arrows to select Option', 10, 40, yellow, 14)
        self.write_text(option_screen.buffer, 'Use LEFT/RIGHT arrows to adjust selected option', 10, 56, yellow, 14)
        self.write_text(option_screen.buffer, 'Press ESC key to exit options screen', 10, 72, yellow, 14)

        # Display initial option state
        self.selected_option = self.options[0]
        self.display(option_screen)

        quit_options = False

        # Loop until user hits Escape key
        while not quit_options:
            pygame.event.pump()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        quit_options = True
                        break

                    if event.key == pygame.K_DOWN:
                        self.selected_option = self.options[min(self.options.index(self.selected_option)+1,len(self.options)-1)]

                    if event.key == pygame.K_UP:
                        self.selected_option = self.options[max(0, self.options.index(self.selected_option)-1)]
                    if event.key == pygame.K_RIGHT:
                        self.selected_option.increase()

                    if event.key == pygame.K_LEFT:
                        self.selected_option.decrease()

            # Update display
            self.display(option_screen)

    def write_text(self, buffer, mesg, x, y, color, size):

        font = pygame.font.Font(None, size)
        text = font.render(mesg, 1, color)
        blit_info = (text, (x, y))
        buffer.bitblt(blit_info)




