#!/usr/bin/env python
"""
Class for Yahtzee widget, and related functions.
"""
from numpy import *
import sys

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

        #self.values is a list of n_rolls dictionaries.
        #The elements of the list correspond to successive
        #rolls, and they are dictionaries giving the
        #expected number of points for each roll at that
        #turn.self.values[-1] is therefore the dictionary
        #input by the user via the "points" argument to
        #__init__, specifying the point values of each
        #possible roll after the last turn.  The keys of
        #the dictionaries are rolls, which are represented
        #by sorted tuples of integers.  For now,
        #initialize self.values to a list of n_rolls
        #empty dictionaries.
        self.values=[]
        for i in range(self.n_rolls):
            self.values.append({})

        #self.strategy is a list of n_rolls-1 dictionaries.
        #The elements of list correspond to successive rolls
        #(except the last one), and they are dictionaries
        #that tell which numbers to keep (and not re-roll)
        #for each possible roll on that turn.  Thus the keys
        #of the dictionaries are sorted tuples representing
        #the rolls, and the values are sorted tuples of a
        #subset of the integers in the roll, which are the
        #numbers to be kept and not re-rolled.  For now,
        #initialize self.strategy to a list of n_rolls-1
        #empty dictionaries.
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
        pass

    def parse_points_dict(self,points):
        """
        Uses the dictionary points to initialize
        self.values[-1].  Checks that the keys
        of points correspond to unique rolls
        before copying to self.values[-1].
        """

        #Clear self.values[-1]
        self.values[-1]={}

        #Run through the key, value pairs of points, check that
        #the keys are valid rolls, then add the key, value pair
        #to self.values[-1].
        for key, value in points.iteritems():
            
            if type(key)!=tuple:
                print >> sys.stderr, "Error in Widget.parse_points_dict: keys in points dictionary must be tuples."
                exit()

            if len(key)!=self.n_dice:
                print >> sys.stderr, "Error in Widget.parse_points_dict: keys in points must be tuples of length", self.n_dice
                exit()

            #Check that each element of the tuple representing the roll
            #is an integer between 1 and self.n_faces.
            for i in key:
                if i<1 or i>self.n_faces:
                    print >> sys.stderr, "Error in Widget.parse_points_dict: numbers in rolls must be between 1 and", self.n_faces
                    exit()
                if type(i)!=int:
                    print >> sys.stderr, "Error in Widget.parse_points_dict: numbers in rolls must be integers."
                    exit()

            #key is a valid tuple representing a roll if you get
            #to this point, however, we only want to deal with sorted
            #tuples as rolls.
            roll=tuple(sort(key))

            #If this roll already has a point value assigned to it
            #in self.values[-1], different than that of "value",
            #then this is an error.
            if roll in self.values[-1].keys() and self.values[-1][roll]!=value:
                print >> sys.stderr, "Error in Widget.parse_points_dict: multiple, inconsistent point values given for roll", roll
                exit()
            #Otherwise we can assign a point value of "value" to
            #this roll in self.values[-1].
            self.values[-1][roll]=value

        #For any rolls for which point values have not yet
        #been specified in self.values[-1], give them point
        #values of 0.
        for roll in rolls(self.n_dice,self.n_faces):
            if roll not in self.values[-1].keys():
                self.values[-1][roll]=0.

    

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

