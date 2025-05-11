# This file contains optimization methods for LinGraph
#
# Author: Allan Grunert <a_grun07@uni-muenster.de>
# Version: 1.0
#
import numpy as np
import random as rnd
import sys
sys.path.append("./RestPlanServe/graph/")


# -----------------------------------------------------------------------------
# Weighting Methods
# -----------------------------------------------------------------------------

class WeightedValueOptimization:
    """Class for applying weighting optimization to LinGraph
        Base class for all optimization methods
        Weight value go from 0 to 1
    """

    def __init__(self):
        self.output_contents = []
        self.percent = 30

    def process(self, actions):
        self.printContents("---------")
        self.printContents("Weighting")
        self.printContents(self.__class__)

    def printContents( self, *args ):
        print( *args )
        self.output_contents.append( " ".join( map( str, args ) ) )

class MaxWeightedValueOptimization( WeightedValueOptimization ):
    """ Class for Weighting action node capacity by maximum capacity value
        Weight value go from 0 to 1

    """
    def process(self, actions):
        super().process(actions)

        actionListCapacity = []

        for action in actions:
            actionListCapacity.append( action.numCapacity )

        MaxActionCapacity = np.max( actionListCapacity )

        for action in actions:
            action.weight = action.numCapacity / MaxActionCapacity
        # max = 1 min = 0

class MedianWeightedValueOptimization( WeightedValueOptimization ):
    """ Class for Weighting action node capacity by median capacity value
        Weight value go from 0 to 1

    """

    # adjust the weight of the actions s.t. the further away from the median the lower the weight gets
    # the median is the middle value
    def process( self, actions ):
        super().process(actions)

        actionListCapacity = []
        for action in actions:
            actionListCapacity.append( action.numCapacity )

        # we don't want a mean if the list is simetric, so choose lower value
        if len( actionListCapacity ) % 2 == 0: # if even, add an element
            actionListCapacity.append( 0 ) # as we do not want a mean value

        sortetedActionListCapacity = np.sort( actionListCapacity )
        actionCapacityMedian = np.median( sortetedActionListCapacity )

        # as we have a reference the actions will be modified
        for action in actions:
            if actionCapacityMedian > action.numCapacity: # value lower the higher it gets nearer
                action.weight = ( action.numCapacity / actionCapacityMedian ) # normalize
            else: # value higher the higher it gets further
                action.weight = ( actionCapacityMedian / action.numCapacity ) # notmalize

# Class containing optimization method applying mean
class MeanWeightedValueOptimization( WeightedValueOptimization ):
    """ Class for Weighting action node capacity by mean capacity value
        Weight value go from 0 to 1
    """
    def process( self, actions ):
        super().process(actions)

        actionListCapacity = []

        for action in actions:
            actionListCapacity.append( action.numCapacity )

        sortetedActionListCapacity = np.sort( actionListCapacity )
        actionCapacityMean = np.mean( sortetedActionListCapacity )

        # as we have a reference the actions will be modified
        for action in actions:
            if actionCapacityMean > action.numCapacity: # value lower the higher it gets nearer
                action.weight = ( action.numCapacity / actionCapacityMean ) # normalize
            else: # value higher the higher it gets further
                action.weight = ( actionCapacityMean / action.numCapacity ) # normalize

# Class containing optimization method applying min value to have heighest weight value
class MinWeightedValueOptimization( WeightedValueOptimization ):
    """ Class for Weighting action node capacity by minimum capacity value
        Weight value go from 0 to 1
    """
    def process( self, actions ):
        super().process(actions)

        actionListCapacity = []

        for action in actions:
            actionListCapacity.append( action.numCapacity )

        MinActionCapacity = np.min( actionListCapacity )

        for action in actions:
            action.weight = MinActionCapacity / action.numCapacity
        # min = 1 max = 0

class RandomWeightedValueOptimization( WeightedValueOptimization ):
    """ Class for Weighting action nodes randomly
        Weight value go from 0 to 1
    """

    def process( self, actions ):
        super().process(actions)

        actionListCapacity = []

        for action in actions:
            actionListCapacity.append( action.numCapacity )
        
        rng = np.random.default_rng() # Numpy random generator

        for action in actions:
            action.weight = rng.random()

# -----------------------------------------------------------------------------
# Pruning Methods
# -----------------------------------------------------------------------------

class Pruning():
    """ class for application of pruning nodes
        Weighting alone is irrelevant for the algorithm as long as action nodes and their siblings are not pruned and connections corrected
    """
    def __init__( self ):
        self.output_contents = []


    def printContents( self, *args ):
        self.output_contents.append( " ".join( map( str, args ) ) )

    def sortActionNodes( self, actionNodes ):
        """Sort action nodes by weight
        
        Parameter
        ---------
            actionNodes : list
                Action nodes to be sorted
        """
        self.quicksort( actionNodes, 0, len( actionNodes ) - 1 )

    def quicksort( self, actionNodes, start, end ):
        """Quicksort 
        
            see Hoare, Charles AR. "Quicksort." The computer journal 5.1 (1962): 10-16.
        
        Parameter
        ---------
            actionNodes : list
                Action nodes to be sorted
        """
        if ( start < end ):
            p = self.partition( actionNodes, start, end )
            self.quicksort( actionNodes, start, p - 1 )
            self.quicksort( actionNodes, p + 1, end )
    
    def partition( self, actionNodes, start, end ):
        """
            Swap elements on basis of pivot element for selected partition 

            Parameter
            ---------
            actionNodes : list
                action nodes to be sorted
            start : int
                Beginning of partition
            end : int
                End of partition
        """
        i = start - 1 # begin left of partition
        pivot = actionNodes[ end ] # last element is pivot element
        for j in range( start, end ):
            if actionNodes[ j ].weight <= pivot.weight: # has pivot element higher value?
                i = i +  1 # shift to the right
                self.swap( actionNodes[ i ], actionNodes[ j ] ) # swap with pivot element
        self.swap( actionNodes[ i + 1 ], actionNodes[ end ] ) # swap with last element
        return ( i + 1 )

    def swap( self, actionNode1, actionNode2 ):
        """
            swap actions with each other

            Paremeter
            ---------
                actionNode1 : list
                    first action node to be swapped
                actionNode2 : list
                    second action node to be swapped
        """
        tmpActionNode = actionNode1
        actionNode1 = actionNode2
        actionNode2 = tmpActionNode

    # remove action node
    def prune( self, level, actionStateLabel, sibling_constraints,  dependency_constraints ):
        # can a be multiple times in state label 
        self.printContents( "Prune:", actionStateLabel)
        # Connections have to be updated
        states = self.correctConnections( actionStateLabel, level.connections )
        
        # remove states related to action node from constraints
        for s in states:
            self.correctConstraints( s.nodeLabelName, sibling_constraints )
            self.correctConstraints( s.nodeLabelName, dependency_constraints )

            # state only exists once
            for ls in level.states:
                if s in ls:
                    ls.remove( s )
                    break

        # action only once in actions 
        for la in level.actions:
            for a in la:
                if a.nodeLabelName == actionStateLabel:
                    la.remove( a )
                    break

    # remove connections where action node is involved and give back states
    def correctConnections( self, actionStateLabel, connections ):
        states = []
        # each level
        for lc in connections:
            for i in range(len(lc)):
                if i == len(lc):
                    break
                if lc[ i ].node1.nodeLabelName == actionStateLabel:
                    states.append( lc[ i ].node2 )
                    print( lc[ i ] )
                    lc.remove( lc[ i ] )
                    if i > -1:
                        i -= 1 # python has to jump one element back
                    # Sibling states
                elif lc[ i ].node2.nodeLabelName == actionStateLabel:
                    print( lc[ i ] )
                    lc.remove( lc[ i ] )
                    if i > -1:
                        i -= 1 # python has to jump one element back
        return states



    # Remove states from constraints
    def correctConstraints( self, nodeLabelName, constraints ):
        """
            correct constraints
            remove if node pruned
        """
        self.printContents("Prune:",nodeLabelName)
        for i in range(len(constraints)):
            if i == len(constraints):
                break
            # remove constraint if is on left size
            if i < len(constraints):
                if len( constraints[i].sh_left_nodes ) == 1 and constraints[i].sh_left_nodes[ 0 ][ 0 ] == nodeLabelName:
                    if i > -1:
                        constraints.remove( constraints[i] )
                        i -= 1 # python has to jump one element back
                else: # correct dependency constraints, modify constraint
                    
                    for j in range( len( constraints[ i ].sh_left_nodes ) ): 
                        if j == len( constraints[ i ].sh_left_nodes ):
                                    break
                        if constraints[i].sh_left_nodes[ j ][ 0 ] == nodeLabelName:
                            constraints[i].remove( constraints[i].sh_left_nodes[ j ] )
                            j -= 1 # python has to jump one element back
                    
                    
                    for j in range(len(constraints[i].sh_right_nodes)):
                        if j == len( constraints[ i ].sh_right_nodes ):
                            break

                        # remove state out of constraints right labels
                        if constraints[i].sh_right_nodes[ j ][ 0 ]  == nodeLabelName:
                            constraints[i].sh_right_nodes.remove( constraints[i].sh_right_nodes[j] )
                            if len(constraints[i].sh_right_nodes) == 0:
                                constraints.remove( constraints[i] )
                                if i > -1:
                                    i = i - 1
                                break

class TopPercentPruning( Pruning ):
    """ Prune Top percent of action nodes    
    """
    def __init__( self ):
        self.percent = 30
        super().__init__()


    def setPercent(self, percent):
        self.percent = percent

    def process(self, level, actionNodes, percent, sibling_constraints, dependency_constraints):
        p = len( actionNodes ) / 100

        if percent == None:
            percent = self.percent
        num = int( p * percent )

        # sort by weightxy 
        self.sortActionNodes( actionNodes )

        for i in range( 0, num ):
            self.prune( level, actionNodes[0].nodeLabelName, sibling_constraints, dependency_constraints )


class BottomPercentPruning( Pruning ):
    """ Prune Bottom percent of action nodes    
    """
    def __init__( self ):
        self.percent = 30
        super().__init__()

    def setPercent(self, percent):
        self.percent = percent

    def process( self, level, actionNodes, percent, sibling_constraints, dependency_constraints ):
        p = len( actionNodes ) / 100

        if percent == None:
            percent = self.percent
        num = int( p * percent )

        # sort by weightxy
        self.sortActionNodes( actionNodes )

        for i in range(  num):
            print(i, len(actionNodes))            
            self.prune( level, actionNodes[len( actionNodes ) - num].nodeLabelName, sibling_constraints, dependency_constraints )
            



class OuterPercentPruning( Pruning ):
    """ Prune Outer percent of action nodes, preserve middle nodes    
    """
    def __init__( self ):
        self.percent = 30
        super().__init__()

    def setPercent(self, percent):
        self.percent = percent

    def process( self, level, actionNodes, percent, sibling_constraints, dependency_constraints ):

        p = len( actionNodes ) / 100

        if percent == None:
            percent = self.percent
        num = int( ( p * percent ) / 2 )

        # sort by weightxy 
        self.sortActionNodes( actionNodes )

        # prine top nodes
        for i in range( 0, num ):
            self.prune( level, actionNodes[ 0 ].nodeLabelName, sibling_constraints, dependency_constraints )

        # prune bottom nodes
        for i in range( 0, num ):
            self.prune( level, actionNodes[ len( actionNodes ) - 1 ].nodeLabelName, sibling_constraints, dependency_constraints )

# Prune middle percent
class MiddlePercentPruning( Pruning ):
    """ Prune percent of middle action nodes    
    """

    def __init__( self ):
        self.percent = 30
        super().__init__()

    def setPercent(self, percent):
        self.percent = percent

    def process( self, level, actionNodes, percent, sibling_constraints, dependency_constraints ):

        p = len( actionNodes ) / 100

        if percent == None:
            percent = self.percent
        num = int( ( p * percent ) / 2 ) # number of action nodes to be removed

        # sort by weightxy
        self.sortActionNodes( actionNodes )

        start = int( ( len ( actionNodes ) - 1 - num ) / 2 )
        for i in range( num ):
            self.prune( level, actionNodes[ start ].nodeLabelName, sibling_constraints, dependency_constraints  )

# Randomly pruning
class RandomPercentPruning( Pruning ):
    """ Randomly prune nodes
    """

    def __init__( self ):
        self.percent = 30
        super().__init__()

    def setPercent(self, percent):
        self.percent = percent

    def process( self, level, actionNodes, percent, sibling_constraints, dependency_constraints ):        
        p = len( actionNodes ) / 100

        if percent == None:
            percent = self.percent
        num = int( ( p * percent ) / 2 )

        self.sortActionNodes( actionNodes )

        for x in range( num ):
            i = rnd.randint( 0, len(actionNodes) - 1 )
            self.prune( level, actionNodes[ i ].nodeLabelName, sibling_constraints, dependency_constraints  )
    
def __main__():
    pass