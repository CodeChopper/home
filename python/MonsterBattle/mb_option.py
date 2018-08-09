#    ---------------------------------------------------
#  -------------------------------------------------------
#   Option
#  -------------------------------------------------------
#    ---------------------------------------------------

import pygame

class Option(object):
    """
    Sets an option using curses slider

    """
    def __init__(self, option_name, values, win, display_coords, callback = None):
        # Name of this option
        self.option_name = option_name
        # List of values for this Option
        self.values = values
        # Current value's index in values list
        self.selected_ndx = 0
        # Curses window we are displaying into.
        self.win = win
        # Starting coordinates in the display window for this option
        self.display_coords = display_coords
        # Callback function that is executed with a single argument
        # that is the current option value
        self.callback = callback

    def set_value(self, value):
        """
        Sets the selected_ndx to index of value

        """
        if value in self.values:
            self.selected_ndx = self.values.index(value)

    def increase(self):
        """
        Sets the selected value to next value in the list

        """
        self.selected_ndx = min(self.selected_ndx + 1, len(self.values) - 1)
        self.set_option()

    def decrease(self):
        """
        Sets the selected value to previous value in the list

        """
        self.selected_ndx = max(0, self.selected_ndx - 1)
        self.set_option()

    def get_value(self):
        """
        Returns current option value

        """
        return self.values[self.selected_ndx]

    def display(self, buffer, active = False):
        """
        Draws the option display

        """
        # Calculate length as a fraction of 200
        interval = 200 / (len(self.values) - 1)
        length = interval * self.selected_ndx
        if self.selected_ndx == len(self.values) - 1:
            length = 200

        # Display
        if active:
            green = (0, 255, 0)
        else:
            green = (0, 192, 0)

        self.write_text(buffer, self.option_name, self.display_coords[0],
                        self.display_coords[1], green, 22)

        gray = (127, 127, 127)
        darkgray = (75, 75, 75)

        # Draw the boundary rect
        pygame.draw.rect(buffer.surf, darkgray,
                         pygame.Rect(self.display_coords[0] + 150,
                                     self.display_coords[1], 202, 22), 0)
        if length > 0:
            pygame.draw.rect(buffer.surf, green,
                         pygame.Rect(self.display_coords[0] + 151,
                                     self.display_coords[1] + 1, length, 20), 0)
        if length < 200:
            pygame.draw.rect(buffer.surf, gray,
                         pygame.Rect(self.display_coords[0] + 151 + length,
                                     self.display_coords[1] + 1, 200 - length, 20), 0)

    def set_option(self):
        """
        If a callback function was passed, call it with the value of the selected option

        """
        if not self.callback == None:
            self.callback(self.values[self.selected_ndx])

    def write_text(self, buffer, mesg, x, y, color, size):

        font = pygame.font.Font(None, size)
        text = font.render(mesg, 1, color)
        blit_info = (text, (x, y))
        buffer.bitblt(blit_info)

