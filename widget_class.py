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

        self.values=[]
        for i in range(self.n_rolls):
            self.values.append({})
        self.strategy=[]
        for i in range(self.n_rolls-1):
            self.strategy.append({})
        
        if type(points)==str:
            self.parse_points_str(points)
        elif type(points)==dict:
            self.parse_points_dict(points)
        else:
            print >> sys.stderr, "Error in Widget.__init__: points must be a string or dictionary."
            exit()

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

def rolls(n_dice,upper,lower=1):
    """
    This generator returns an iterator over all
    possible rolls of n_dice dice, where each die
    has the integer values from lower to upper
    (inclusive) exactly once on different faces.
    It returns each roll as a sorted tuple of length
    n_dice for which each entry is an integer from
    lower to upper.

    Ex.  3 dice, upper=6, lower=1, returns
    (1,1,1)
    (1,1,2)
    .
    .
    .
    (5,6,6)
    (6,6,6)
    """
    if n_dice==0:
        yield ()
    else:
        for first_die in range(lower,upper+1):
            for rest_die in rolls(n_dice-1,upper,first_die):
                yield (first_die,)+rest_die

