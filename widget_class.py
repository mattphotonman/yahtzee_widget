#!/usr/bin/env python
"""
Class for Yahtzee widget.  
"""

class Widget:
    """
    Allows you to specify points for each roll at the end
    of the turn, and then has all the tools to calculate
    the optimal strategy, (strategy that maximizes expected
    number of points), and the expected number of points
    given the strategy.  It is also possible to give a string
    like 'yahtzee' which will give 1 point to all rolls considered
    to be yahtzees (all numbers the same), and 0 points to
    everything else.
    """
    def __init__(self,points,n_dice=5,n_faces=6,n_rolls=3):
        """
        points is either a string giving a type of yahtzee
        combination (e.g. 'yahtzee', 'four of a kind'), or
        a dictionary giving point values for each possible
        roll (specified as a tuple) on the last turn.

        n_dice = number of dice; 5 is the default value as
        in the ordinary game of Yahtzee.

        n_faces = number of faces; 6 is the default value as
        with ordinary dice.

        n_rolls = number of rolls allowed (first roll plus
        re-rolls); 3 is the default value as in the ordinary
        game of Yahtzee.
        """
        if (type(points)==str):
            self.parse_points_str(points)
        elif (type(points)==dict):
            self.parse_points_dict(points)
        else:
            print >> sys.stderr, "Error in Widget.__init__: points must be a string or dictionary."
            exit()
        
