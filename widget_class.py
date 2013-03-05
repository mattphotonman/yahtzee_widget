#!/usr/bin/env python
"""
Class for Yahtzee widget, and related functions.
"""
from numpy import *

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
        self.n_dice=parse_int(n_dice,"n_dice",1)
        self.n_faces=parse_int(n_faces,"n_faces",1)
        self.n_rolls=parse_int(n_rolls,"n_rolls",1)

        self.init_values_strategy()
        
        if type(points)==str:
            self.parse_points_str(points)
        elif type(points)==dict:
            self.parse_points_dict(points)
        else:
            print >> sys.stderr, "Error in Widget.__init__: points must be a string or dictionary."
            exit()

    def init_values_strategy(self):
        """Initialize self.values and self.strategy"""
        self.values=[]
        self.strategy=[]
        pass
        
    
    def parse_points_str(self,points):
        self.points=[]
        pass

def parse_int(n,name,lower=None,upper=None):
    """
    Checks that n is a type int, and that it is in
    the bounds [lower,upper] if provided.
    """
    if type(n)!=int:
        print >> sys.stderr, "Error:", name, "not type int."
        exit()

    if lower!=None and n<lower:
        print >> sys.stderr, "Error:", name, "must be >=", lower
        exit()

    if upper!=None and n>upper:
        print >> sys.stderr, "Error:", name, "must be <=", upper
        exit()

def rolls(n_dice,n_faces,lower=1):
    """
    This generator returns an iterator over all
    possible rolls of n_dice dice with n_faces
    faces.  It returns each roll as a sorted
    tuple of length n_dice for which each entry
    is an integer from 1 to n_faces.  The optional
    argument lower allows you to specify a lower
    limit on the dice values, and is used when the
    generator calls itself recursively.

    Ex.  3 dice, 6 faces, returns
    (1,1,1)
    (1,1,2)
    .
    .
    .
    (5,6,6)
    (6,6,6)

    3 dice, 6 faces, lower=2, returns
    (2,2,2)
    (2,2,3)
    .
    .
    .
    (5,6,6)
    (6,6,6)
    """
    if n_dice==0:
        yield ()
    else:
        for first_die in range(lower,n_faces+1):
            for rest_die in rolls(n_dice-1,n_faces,first_die):
                yield (first_die,)+rest_die

