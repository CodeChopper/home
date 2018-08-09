# -------------------------------------------------------------------------
#  File:    mb_location.py
#  Created: Tue Feb  7 20:50:34 2006
# -------------------------------------------------------------------------

import random

class LocationMap:

    """
    This class is used to store a group of locations and
    to manage the event loop over these locations.
    """
    def __init__(self):
        self.locations = list()

    def add_location(self, location):
        self.locations.append(location)

    def rand_location(self):
        return self.locations[random.randrange(self.num_locs())]

    def link_locations(self):
        """
        This method goes through each location and examines
        each of the links in the location.  When these links
        are read from the file, they are simply the names
        of locations, they do not reference the real location
        objects yet.  This method attempts to replace the names
        of locations with a reference to the real linked location.
        This has to be done at this level instead of in the location
        class itself, because a location object does not have access
        to a list of all the other location objects. This method
        (unfortunately) needs to be called explicitly after a
        LocationMap is created and loaded with all the locations.
        """

        for loc in self.locations:
            for name in loc.links.keys():
                loc.links[name] = self.location_named(loc.links[name])

    def run_sim(self, sim, player):
        """
        This method runs the specified sim object
        only over the location where the player
        is currently located.
        """
        sim.run(player.location)

    def num_locs(self):
        return len(self.locations)

    def being_count(self):
        count = int(0)
        for location in self.locations:
            count += location.being_count()
        return count

    def enemy_count(self, player_family):
        count = int(0)
        for location in self.locations:
            if location.name != 'graveyard':
                for b in location.beings:
                    if b.family != player_family:
                        count += 1
        return count

    def location_named(self, n):
        """
        Return the location object with the name n.
        """
        loc = [l for l in self.locations if l.name == n]
        if len(loc) == 1:
            return loc[0]
        else:
            return None

    def last_one(self):

        survivor = None
        if self.being_count() == 1:
            for location in self.locations:
                if location.being_count() == 1:
                    survivor = location.beings[0]
                    break
        return survivor


