#!/usr/bin/env python
"""
Class for Yahtzee widget, and related functions.
"""
from numpy import *
import sys
from collections import Counter

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
        #the rolls, and the values are lists of sorted tuples
        #of a subset of the integers in the roll, which are the
        #numbers to be kept and not re-rolled.  The values are
        #lists of tuples because there may be more than one
        #optimal choice of numbers to keep, and the list will
        #contain them all.  For now, initialize self.strategy
        #to a list of n_rolls-1 empty dictionaries.
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

        #Compute the optimal strategy and expected scores.
        self.compute_strategy()

    def parse_points_str(self,points):
        """
        Takes a string describing a combination, such
        as 'yahtzee', or 'four of a kind', creates a dictionary
        called points_dict which gives a point value of 1 to
        rolls of that type and 0 to rolls not of that type,
        and passes points_dict to self.parse_points_dict.
        Can also add the word 'weighted' on the end, e.g.
        'four of a kind weighted', to weight rolls by the actual
        number of points you would score with that roll, rather
        than just 1.
        """
        combos=['three of a kind','four of a kind','full house','small straight','large straight','yahtzee','chance','ones','twos','threes','fours','fives','sixes']
        combos_weighted=[]
        for combo in combos:
            combos_weighted.append(combo+' weighted')

        numbers=['ones','twos','threes','fours','fives','sixes']
        numbers_weighted=[]
        for combo in numbers:
            numbers_weighted.append(combo+' weighted')

        combo=points.lower()

        if combo not in combos and combo not in combos_weighted:
            print >> sys.stderr, "Error in Widget.parse_points_str:", points, "not a valid combination.  Must be one of:"
            for c in combos:
                print >> sys.stderr, c, "[weighted]"
            exit()

        #Checked that combo is a valid combination, now big if
        #statement to create points_dict for each combination.
        points_dict={}

        #-----------------------------------------------------
        if combo=='three of a kind' or combo=='three of a kind weighted':
            for roll in rolls(self.n_dice,self.n_faces):
                c=Counter(roll)
                #c.most_common(1)[0] gives an order pair:
                #(most common number,its frequency)
                #Thus c.most_common(1)[0][1] is the frequency
                #of the most common number.
                if c.most_common(1)[0][1]>=3:
                    if combo=='three of a kind':
                        points_dict[roll]=1.
                    else:
                        points_dict[roll]=float(sum(roll))
                else:
                    point_dict[roll]=0.
            
        elif combo=='four of a kind' or combo=='four of a kind weighted':
            for roll in rolls(self.n_dice,self.n_faces):
                c=Counter(roll)
                #c.most_common(1)[0] gives an order pair:
                #(most common number,its frequency)
                #Thus c.most_common(1)[0][1] is the frequency
                #of the most common number.
                if c.most_common(1)[0][1]>=4:
                    if combo=='four of a kind':
                        points_dict[roll]=1.
                    else:
                        points_dict[roll]=float(sum(roll))
                else:
                    point_dict[roll]=0.
            
        elif combo=='full house' or combo=='full house weighted':
            for roll in rolls(self.n_dice,self.n_faces):
                c=Counter(roll)
                #For an arbitary number of dice, I define a full
                #house to be only two different numbers appearing
                #in the roll, and n_dice/2 of each for n_dice even,
                #but (n_dice+1)/2 of one and (n_dice-1)/2 of the
                #other for n_dice odd.
                #
                #To treat both cases at the same time, let
                #
                #freq1=c.most_common(2)[0][1]
                #freq2=c.most_common(2)[1][1]
                #
                #i.e. freq1 and freq2 are the frequencies of the
                #two most common numbers.  For a full house, must
                #have freq1+freq2=n_dice, and freq1, freq2 >= n_dice/2
                #(integer division).
                #
                #The case of n_dice=1 must be treated separately;
                #for that case, everything is a full house.
                if self.n_dice==1:
                    points_dict[roll]=1.
                else:
                    mc=c.most_common(2)
                    freq1=mc[0][1]
                    if len(mc)<2:
                        freq2=0
                    else:
                        freq2=mc[1][1]
                    if freq1+freq2==self.n_dice and freq1>=self.n_dice/2 and freq2>=self.n_dice/2:
                        points_dict[roll]=1.
                    else:
                        points_dict[roll]=0.

                if combo=='full house weighted':
                    points_dict[roll]*=25.  #25 is the point value of any full house

        elif combo=='small straight' or combo=='small straight weighted':
            for roll in rolls(self.n_dice,self.n_faces):
                c=Counter(roll)
                #A small straight means that n_dice-1 of the
                #numbers on the dice are in consecutive order,
                #and the remaining die can show any number.
                #We can split this into two cases:
                #(i) the remaining die shows a number different
                #than any of the other dice.
                #(ii) the remaining die shows a number the
                #same as one of the other dice.
                #Thus we have (i) all dice show different values
                #and (ii) two dice show the same values but all
                #the rest are different.  Therefore, we can look at
                #
                #freq1=c.most_common(2)[0][1]
                #freq2=c.most_common(2)[1][1]
                #
                #which are the frequencies of the most and second
                #most common number.  If freq1>2 then we definitely
                #can't have a small straight.  If freq1=2 then we
                #can use the fact that roll is sorted and test for
                #case (ii) by checking if roll[-1]-roll[0]=n_dice-2.
                #If freq1=1 then we can check for case(i) checking if
                #roll[-2]-roll[0]=n_dice-2 or roll[-1]-roll[1]=n_dice-2.
                #
                #n_dice<=2 must be treated separately; in this case
                #everything is a small straight.
                if self.n_dice<=2:
                    points_dict[roll]=1.
                else:
                    mc=c.most_common(2)
                    freq1=mc[0][1]
                    if len(mc)<2:
                        freq2=0
                    else:
                        freq2=mc[1][1]
                    if freq1>2:
                        points_dict[roll]=0.
                    elif freq1==2:
                        if roll[-1]-roll[0]==self.n_dice-2:
                            points_dict[roll]=1.
                        else:
                            points_dict[roll]=0.
                    else:
                        if roll[-2]-roll[0]==self.n_dice-2 or roll[-1]-roll[1]==self.n_dice-2:
                            points_dict[roll]=1.
                        else:
                            points_dict[roll]=0.
                
                if combo=='small straight weighted':
                    points_dict[roll]*=30.  #30 is the point value of any small straight

        elif combo=='large straight' or combo=='large straight weighted':
            for roll in rolls(self.n_dice,self.n_faces):
                c=Counter(roll)
                #A large straight is when all dice show numbers
                #in consecutive order.  Since roll is sorted, can
                #test for this by checking that all numbers in
                #the roll are different (c.most_common(1)[0][1]=1),
                #and that roll[-1]-roll[0]=n_dice-1.
                if c.most_common(1)[0][1]==1 and roll[-1]-roll[0]==self.n_dice-1:
                    points_dict[roll]=1.
                else:
                    points_dict[roll]=0.

                if combo=='large straight weighted':
                    points_dict[roll]*=40.  #40 is the point value of any large straight

        elif combo=='yahtzee' or combo=='yahtzee weighted':
            for roll in rolls(self.n_dice,self.n_faces):
                c=Counter(roll)
                if c.most_common(1)[0][1]==self.n_dice:
                    points_dict[roll]=1.
                else:
                    points_dict[roll]=0.

                if combo=='yahtzee weighted':
                    points_dict[roll]*=50.  #50 is the point value of any yahtzee

        elif combo=='chance' or combo=='chance weighted':
            for roll in rolls(self.n_dice,self.n_faces):
                if combo=='chance':
                    points_dict[roll]=1.
                else:
                    points_dict[roll]=float(sum(roll))

        elif combo in numbers or combo in numbers_weighted:
            if combo in numbers:
                num=numbers.index(combo)+1
            else:
                num=numbers_weighted.index(combo)+1
            for roll in rolls(self.n_dice,self.n_faces):
                c=Counter(roll)
                if combo in numbers:
                    if c[num]>0:
                        points_dict[roll]=1.
                    else:
                        points_dict[roll]=0.
                else:
                    points_dict[roll]=float(c[num]*num)

        #-----------------------------------------------------
        #Big if statement to create points_dict for each
        #combination is finished.  Now pass points_dict
        #to self.parse_points_dict.
        self.parse_points_dict(points_dict)

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

    def compute_strategy(self):
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

