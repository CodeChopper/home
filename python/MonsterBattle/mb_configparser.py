# -------------------------------------------------------------------------
#  File:    mb_configparser.py
#  Created: Sat Apr  1 23:09:56 2006
# -------------------------------------------------------------------------

from ConfigParser import ConfigParser

class mbConfigParser(ConfigParser):

    """
    Subclass Python's ConfigParser to preserve case.
    Override the optionxform() method to achieve this.
    """

    def optionxform(self, optionstr):
        """
        This method in ConfigParser ends up converting
        all the options to lowercase by:

        return optionstr.lower()

        This is annoying!  Instead just return optionstr.
        """

        return optionstr

