# This file contains Implementation and Extended Implementation of LinGraph
#
# Author: Allan Grunert <a_grun07@uni-muenster.de>
# Version: 1.0
#
# This code is based on the following paper:
#
# KORTIK, Sıtar; SARANLI, Uluc. LinGraph: a graph-based automated planner 
# for concurrent task planning based on linear logic. 
# Applied Intelligence, 2017, 47. Jg., S. 914-934.
#
# important notice: A great thanks towards Dr. Sitar Kortik. Large parts of this file, including comments, are based on his provided python source code (https://github.com/sitar42/LinGraph/blob/87ec3cc5191670cf1f90d87fec7e43528fd22eeb/fSearch_multiple_or-tools.py) 

import sys
import copy
import time
from datetime import datetime
import uuid
import json
import math
# CSP solver
from ortools.sat.python import cp_model
sys.path.append("./RestPlanServe/graph/")

# set recursion limit high
sys.setrecursionlimit(100000)

# for further configuration see class Grap.__init__

output_contents = [] # list of strings containing the output of the algorithm
# PRINT_TO_CONSOLE = True

class Graph:
    """ 
    Class in which a graph can be created partitioned by levels.
    There are three types of objects that can be added: state nodes, connections and action nodes
    

    Attributes
    ----------
    currentLevel : string
        Current Level of graph
    self.states : 2-dimensional list of StateNodes at each level
        
    self.actions : 2-dimensional list of StateNodes at each level
    self.connections : 2-dimensional list of Connections at each level

    Methods
    -------
    newLevel( self )
    addState( self, state )
    addAction( self, action )
    
        Prints the animals name and what sound it makes
    """
    # initalisation
    def __init__( self ):
        """Init State
        """
        self.currentLevel = -1
        self.states = []
        self.actions = []
        self.connections = []
        self.newLevel()

    
    def newLevel( self ):
        """Add new level to graph. Initalize 2-dimensional list for state nodes, action nodes and connections
        """
        # add new level and initialize the lists for the new level
        self.currentLevel += 1
        self.states.insert( self.currentLevel, [] )
        self.actions.insert( self.currentLevel, [] )
        self.connections.insert( self.currentLevel, [] )

    def addState( self, state ):
        """Add state node at current level

        Parameters
        ----------
        state : StateNode 
            state node to be added to current level
        """

        self.states[ self.currentLevel ].append( state )

    # add action node to the current level
    def addAction( self, action ):
        """Add action node at current level

        Parameters
        ----------
        action : ActionNode 
            action node to be added to current level
        """
        self.actions[ self.currentLevel ].append( action )

    def addConnection( self, connection ):
        """Add connection at current level

        Parameters
        ----------
        connection : Connection 
            connection to be added to current level
        """
        if self.currentLevel > -1: # only if the current level is not -1 i.e. if there is a level
            self.connections[ self.currentLevel ].append( connection )

    # add a state node to the selected level
    def addStateAt( self, level, state ):
        """Add state node at defined level

        Parameters
        ----------
        level : int
            level at which state node is added, at least 0
        state : StateNode 
            state node to be added to defined level
        """

        if level > -1:
            self.states[ level ].append( state )

    # add a action node to the selected level
    def addActionAt( self, level, action ):
        """Add action node at defined level

        Parameters
        ----------
        level : int
            level at which action node is added, at least 0
        action : ActionNode 
            action node to be added to defined level
        """
        if level > -1:
            self.actions[ level ].append( action )

    # add a connection to the selected level
    def addConnectionAt( self, level, connection ):
        """Add connection at defined level

        Parameters
        ----------
        level : int
            level at which state node is added, at least 0
        connection : Connection
            connection that is added at defined level
        """
        if level > -1: # only if the current level is not -1 i.e. if there is a level
            self.connections[ level ].append( connection )

    def getCurrentActions( self ):
        """Give back action nodes at current level

        Returns
        -------
        list of ActionNode
            list of action nodes in current level
        """
        return self.actions[ self.currentLevel ]

    # get all action nodes at selected level
    def getActionsAtLevel( self, level ):
        """Give back action nodes at defines level

        Parameters
        ----------
        level : int
            level at which the action nodes are present

        Returns
        -------
        list of ActionNode
            list of action nodes in current level
        """
        return self.actions[ level ]

    # get all state nodes at current level
    def getCurrentStates( self ):
        """Give back state nodes at current level

        Returns
        -------
        list of StateNode
            list of state nodes in current level
        """
        return self.states[ self.currentLevel ]

    def getConnectionNodeCount( self, nodeLabelName ):
        """Give back the sum of cardinality of each connection to the node with a given label name

        Parameters
        ----------
        nodeLabelName : string

        Returns
        -------
        list of StateNode
            list of state nodes in current level
        """
        cardinality = 0
        for i in range( 0, self.currentLevel ):
            for connection in self.connections[ i ]:
                if connection.node1.nodeLabelName == nodeLabelName and connection.node2.copy == False:
                    if ( connection.cardinality > 0 ):
                        cardinality += connection.cardinality
        return cardinality 

    def getStateValuesFromLevelOne( self ): 
        """Returns list of tuples containing the state label name and value from all levels until the current level

            Returns
            -------
            list of tuples of Pairs of State Label Names and Values
                List of all states node starting from level 2 (1 is equivalent to level 2 in the list)
        """
        values = []
        if self.currentLevel > 0 :
            for i in range( 1, self.currentLevel + 1 ):
                values.append( list( map( lambda x: ( x.nodeLabelName, x.value ), self.getStatesAtLevel( i ) ) ) )

    def getStatesFromLevelOne( self ):
        """Give back all state nodes from all levels


        Returns
        -------
        list of StateNode
            list of state nodes in all levels
        """
        values = []
        for i in range( 1, self.currentLevel + 1 ):
            values.extend( self.getStatesAtLevel( i ) )
        return values

    def getStatesAtLevel( self, level ):
        """Give back all state nodes from a defined levels

        Parameters
        ----------
            level : int
                level from which to get the state nodes
        
        Returns
        ------- 
            list of StateNode
            list of state nodes in defined level
        """
        if ( level > -1 ):
            return self.states[ level ]
        else:
            return []

    def getCurrentConnections( self ):
        """Give back all connections from current level


        Returns
        -------
        list of Connection
            list of connections from current level
        """

        return self.connections[ self.currentLevel ]

    def getConnectionsAtLevel( self, level ):
        """Give back all connections from defined level

        Parameters
        ----------
        level : int
            level for which connections are returned

        Returns
        -------
        list of Connection
            list of connections from defined level
        """
        if (level>-1):
            return self.connections[ level ]
        else:
            return []
        
    def countStateActions( self, nodeLabelName ):
        """Give back amount of nodes connected to left of the connection


        Parameters 
        ----------
            nodeLabelName : string
                Node on the left side of the conneciton


        Returns
        -------
            int
                amount of connections to defined node at left side of connection
        """

        amount = 0
        for connection in self.getConnectionsAtLevel( self.currentLevel - 1 ):
            if connection.node1.nodeLabelName == nodeLabelName:
                amount += 1
        return amount

    def removeStateByName( self, nodeLabelName ):
        """Remove state node by name


        Parameters 
        ----------
            nodeLabelName : string
                Name of state node

        """
        for l in range( self.currentLevel ):
            for state in self.states[ l ]:
                if state.nodeLabelName == nodeLabelName:
                    self.states[ l ].remove( state )
                    break
        self.removeConnection( nodeLabelName )

    def removeActionByName( self, actionLabelName ):
        """Remove action node by name


        Parameters 
        ----------
            nodeLabelName : string
                Name of action node

        """

        for l in range( self.currentLevel ):
            for action in self.actions[ l ]:
                if action.nodeLabelName == actionLabelName:
                    self.actions[ l ].remove( action )
                    # remove sibling states
                    break
        self.removeConnection( actionLabelName )


    def removeActionSiblings( self, actionNode, level ):
        """Remove siblings of action node in certain level


        Parameters 
        ----------
            actionState : string
                Name of state node for which siblings are removed

        """
        for c in self.connections[ level ]:
            if c.node1 == actionNode:
                self.removeStateByName( c.node2.labelName )

    def removeConnection( self, labelName ):
        """Remove Connections which incorporate defined Node


        Parameters 
        ----------
            labelName : string
                Name of node for which the connection is removed

        """

        for l in range(self.currentLevel):
            for c in self.connections[ l ]:
                if c.node1.nodeLabelName == labelName or c.node2.nodeLabelName == labelName:
                    self.connections[ l ].remove( c ) 

    def toJson( self ):
        """Give back all Actions, States and Connections of all levels as JSon String

        Returns
        -------
            str
                JSON-String containing all state and action nodes and connections
        """
        jsonStr = '['

        for i in range( self.currentLevel + 1 ):
            jsonStr += '{'

            jsonStr += '"level":' + str( i + 1 ) + ',"states":['

            for j in range( len( self.states[ i ] ) ):
                jsonStr += self.states[ i ][ j ].toJson() + ","
            if len( self.states[ i ] )>0:
                jsonStr = jsonStr[ :-1 ]

            jsonStr += "]"

            jsonStr += ',"actions":['

            for j in range( len( self.actions[ i ] ) ):
                jsonStr += self.actions[ i ][ j ].toJson() + ","
            if len( self.actions[ i ] ) > 0:
                jsonStr = jsonStr[ :-1 ]

            jsonStr += "]"

            jsonStr += ',"connections":['

            for j in range( len( self.connections[ i ] ) ):
                jsonStr += self.connections[ i ][ j ].toJson() + ","
            if len( self.connections[ i ] ) > 0:
                jsonStr = jsonStr[ :-1 ]

            jsonStr += "]"

            jsonStr += '},'

        jsonStr = jsonStr[ :-1 ]

        jsonStr += ']'

        return jsonStr
    
    def clear(self):
        """Reset graph, initialize all variables

        """

        self.currentLevel = -1
        self.states = []
        self.actions = []
        self.connections = []


class Constraint:
    """This class was copied from the source code of Dr. Sita Kortik (fSearch_multiple_or-tools.py) and has been slightly modified
        The class can contain either sibling or dependency constraints described in the paper:

        
        - sh_left_nodes: short hands list of left nodes, example: [('s1', 1),('s3',2)]
        - sh_right_nodes: short hands list of right nodes, example: [('s1', 1),('s3',2)]
    """

    def __init__( self, sh_left_nodes=[], sh_right_nodes=[] ):
        """This class was copied from the source code of Dr. Sita Kortik (fSearch_multiple_or-tools.py) 

        Args:
            left_nodes (list, optional): This class attribut contains the left side of the constraint, consisting of states and count values. Defaults to [].
            right_nodes (list, optional): This class attribut contains the left side of the constraint, consisting of states and count values. Defaults to [].
        """
        self.sh_left_nodes = sh_left_nodes # [('s1', 1)] or [('a1', 2),('a2', 1),...]
        self.sh_right_nodes = sh_right_nodes # [('s1', 1)] or [('a1', 2),('a2', 1),...]

    def toJson( self ):
        """Give back JSON-Representation of the class attributes

        Returns
        -------
            str 
                JSON-representation of the constraint
        """
        jsonStr =  '{ "left_nodes": ['

        for node in self.sh_left_nodes:
            jsonStr+= '{"label":"' + node[ 0 ] + '","value":' + str( node[ 1 ] ) + '},'
        jsonStr = jsonStr[ :-1 ] + '], "right_nodes": ['

        for node in self.sh_right_nodes:
            jsonStr+= '{"label":"' + node[ 0 ] + '","value":' + str( node[ 1 ] ) + '},'
        jsonStr = jsonStr[ :-1 ] + ']'
        jsonStr += '}'

        return jsonStr

class ConstraintSolver:
    """Class that includes all constraints.


    """

    def __init__( self ):
        self.DEBUG = False

    def solve_impaired_constraints( self, one_combination, variables, sibling_constraints, dependency_constraints, initNodes ):
        """Checks if impaired constraints has a solution
            This function was copied from the source code of Dr. Sita Kortik (fSearch_multiple_or-tools.py) and has been slightly modified.

        Parameters
        ----------
            one_combination : list of tuples
                Combination that should be tested for impairment
            variables : list of tuples
            sibling_constraints : list of tuples of Constraint
                Sibling constraints
            dependency_constraints : list of tuples of Constraint
                Dependency constraints
            initNodes: list of StateNode
                Initial state nodes

        Returns
        -------
            boolean
                True: if there is a solution for impaired constraints
                False: if there is no solution for impaired constraints
        """

        # Creates the model.
        model = cp_model.CpModel()

        if self.DEBUG:
            printContents( "********** Set up SAT-Solver for Solving impaired constraints *************" )


        # add initial variables, s1=2, s2=1..
        for initNode in initNodes:
            # printContents('solve_constraints - Initial_labels - variable:', variable, ' - count:', count)
            expression = initNode.nodeLabelName + ' = model.NewIntVar(' + str( initNode.value ) + ', ' + str( initNode.value ) + ', "' + initNode.nodeLabelName + '")'
            if self.DEBUG:
                printContents( expression )
            exec( expression )


        # -> effect, count von action . wann? action_count * coefficient1 + copy states

        # for variables adding rest of variables with their possible values, will be range(count+1) 

        for ( variable, count ) in list( map( lambda x: ( x.nodeLabelName, x.numCapacity ), variables ) ):
            # printContents('solve_constraints - variables_GL - variable:', variable, ' - count:', count)
            expression = variable + ' = model.NewIntVar(0, ' + str( count ) + ', "' + variable + '")'
            if self.DEBUG:
                printContents( expression )
            exec( expression )

        # Find non_zero_nodes, which are nodes in one_combination and their siblings
        non_zero_nodes = set()
        for ( node, count ) in one_combination:
            non_zero_nodes.add( node.nodeLabelName )
            expression = 'model.Add(' + node.nodeLabelName + ' >= ' + str( count ) + ')'
            if self.DEBUG:
                printContents( expression )
            eval( expression )

        # Formular for sibling constraints
        for sibling_constraint in sibling_constraints:
            expression = '' # holds whole expression for adding constraints. eval('exp') evaluates the exp
            expression += 'model.Add('
            for node in sibling_constraint.sh_left_nodes: #[('s1', 2)]
                expression += str( node[1] ) + '*' + node[ 0 ] + '+'
            expression = expression[ :-1 ] # removes the last character '+'
            expression += '=='
            for action in sibling_constraint.sh_right_nodes: #[('s1', 2), ('s2', 1), ..]
                expression += str( action[ 1 ] ) + '*' + action[ 0 ] + '+' # 2*s1 + 1*s2..
            expression = expression[ :-1 ] # removes the last character '+'
            expression += ')'
            if self.DEBUG:
                printContents( expression )
            eval( expression ) # evaluates the problem.addConstraint(..) string

        # Formulars for dependency constraints
        for constraint in dependency_constraints:
            expression = '' # holds whole expression for adding constraints. eval('exp') evaluates the exp
            expression += 'model.Add('
            for node in constraint.sh_left_nodes: #[('s1', 2)]
                expression += str( node[ 1 ] ) + '*' + node[ 0 ] + '+' # 2*s1
            expression = expression[ :-1 ] # removes the last character '+'
            expression += '=='
            for action in constraint.sh_right_nodes: #[('s1', 2), ('s2', 1), ..]
                expression += str( action[ 1 ] ) + '*' + action[ 0 ] + '+' # 2*s1 + 1*s2..
            expression = expression[ :-1 ] # removes the last character '+'
            expression += ')'
            eval(expression) # evaluates the problem.addConstraint(..) string
            if self.DEBUG: 
                printContents(expression)

        # Creates a solver and solves the model.
        solver = cp_model.CpSolver()
        status = solver.Solve( model )

        # check if model solvable
        if status == cp_model.FEASIBLE or status == cp_model.OPTIMAL:
            return ( solver, True )
        else:
            return ( solver, False )

    # This function was copied from the source code of Dr. Sita Kortik and slightly modified
    # fSearch_multiple_or-tools.py
    def solve_constraints( self,current_nodes_GL, sibling_constraints, dependency_constraints, goal_constraints, conjunction, zero_labels, initNodes, goalNodes ):
        """ Solve constraints for checking if goal can be reached, i.e. plan can be solved. It also assigns values to the nodes if successfull
            This function was copied from the source code of Dr. Sita Kortik (fSearch_multiple_or-tools.py) and has been slightly modified.



        Parameters
        ----------
            current_nodes_GL : list of tuple
            sibling_constraints : list of tuple of Constraint
            dependency_constraints : list of tuple of Constraint
            goal_constraints : list of tuple of Constraint
            conjunction : list of tuple
            zero_labels : list of tuple 
            initNodes : list of StateNode
            goalNodes : list of StateNode

        Return
        ------
            boolean
                True: Goal can be reached
                False: Goal can not be reached
        """

        printContents("Beginning of solve_constraints - variables_GL:",  str( len( current_nodes_GL ) ), "- constraints_GL:",  str( len( dependency_constraints ) ), "- goal_constraints:", str( len( goal_constraints ) ), "- zero_constraints:", str( len( zero_labels ) ) )

        # Creates the model.
        model = cp_model.CpModel()

        # create initial variables, s1=2, s2=1..
        for initNode in initNodes:
            # printContents('solve_constraints - Initial_labels - variable:', variable, ' - count:', count)
            expression = initNode.nodeLabelName + ' = model.NewIntVar(' + str( initNode.numCapacity ) + ', ' + str( initNode.numCapacity ) + ', "' + initNode.nodeLabelName + '")'
            if self.DEBUG:
                printContents( expression )
            exec( expression )

        # create initial variables, s1=2, s2=1..
        for goalNode in goalNodes:
            # printContents('solve_constraints - goal_labels - variable:', variable, ' - count:', count)
            expression = goalNode.nodeLabelName + ' = model.NewIntVar(' + str( goalNode.numCapacity ) + ', ' + str( goalNode.numCapacity ) + ', "' + goalNode.nodeLabelName + '")'
            if self.DEBUG:
                printContents( expression )
            exec( expression )

        nodes_visited = []
        # for left variables adding rest of variables with their possible values, will be range(count+1) 
        for node in current_nodes_GL:
            if not ( node.nodeLabelName, node.numCapacity ) in nodes_visited:
                nodes_visited.append( ( node.nodeLabelName, node.numCapacity ) )
                # printContents('solve_constraints - variables_GL - variable:', variable, ' - count:', count)
                expression = node.nodeLabelName + ' = model.NewIntVar(0, ' + str( node.numCapacity ) + ', "' + node.nodeLabelName + '")'
                if self.DEBUG:
                    printContents( expression )
                exec( expression ) 

        # We assign zero to nodes that are in zero constraints list
        for variable in zero_labels:
            expression = 'model.Add(' + variable + ' == 0)'
            if self.DEBUG:
                printContents( expression )
            eval( expression )

        # build sibling constraints
        for sibling_constraint in sibling_constraints:
            expression = '' # holds whole expression for adding constraints. eval('exp') evaluates the exp
            expression += 'model.Add('
            for node in sibling_constraint.sh_left_nodes: #[('s1', 2)]
                expression += str( node[ 1 ] ) + '*' + node[ 0 ] + '+'
            expression = expression[ :-1 ] # removes the last character '+'
            expression += '=='
            for action in sibling_constraint.sh_right_nodes: #[('s1', 2), ('s2', 1), ..]
                expression += str( action[ 1 ] ) + '*' + action[ 0 ] + '+' # 2*s1 + 1*s2..
            expression = expression[ :-1 ] # removes the last character '+'
            expression += ')'
            if self.DEBUG:
                printContents( expression )
            eval( expression ) # evaluates the problem.addConstraint(..) string

        # build goal constraints
        for goal_constraint in goal_constraints:
            expression = '' # holds whole expression for adding constraints. eval('exp') evaluates the exp
            expression += 'model.Add('
            for node in goal_constraint.sh_left_nodes: #[('s1', 2)]
                expression += str( node[ 1 ] ) + '*' + node[ 0 ]  + '+' # 2*s1
            expression = expression[ :-1 ] # removes the last character '+'
            expression += '=='
            for action in goal_constraint.sh_right_nodes: #[('s1', 2), ('s2', 1), ..]
                expression += str( action[ 1 ] ) + '*' + action[ 0 ] + '+' # 2*s1 + 1*s2..
            expression = expression[ :-1 ] # removes the last character '+'
            expression += ')'
            if self.DEBUG:
                printContents( expression )
            eval( expression ) # evaluates the problem.addConstraint(..) string

        # add left constraints to the solver
        for constraint in dependency_constraints:
            expression = '' # holds whole expression for adding constraints. eval('exp') evaluates the exp
            expression += 'model.Add('
            for node in constraint.sh_left_nodes: #[('s1', 2)]
                expression += str( node[1] ) + '*' + node[ 0 ] + '+' # 2*s1
            expression = expression[ :-1 ] # removes the last character '+'
            expression += '=='
            for action in constraint.sh_right_nodes: #[('s1', 2), ('s2', 1), ..]
                expression += str( action[ 1 ] ) + '*' + action[ 0 ] + '+' # 2*s1 + 1*s2..
            expression = expression[ :-1 ] # removes the last character '+'
            expression += ')'
            if self.DEBUG:
                printContents( expression )
            eval( expression ) # evaluates the problem.addConstraint(..) string

        # Creates a solver and solves the model.
        solver = cp_model.CpSolver()
        status = solver.Solve( model )

        if status == cp_model.FEASIBLE or status == cp_model.OPTIMAL:
            # store solutions into global variables
            for initNodes in initNodes:
                expression = 'solver.Value(' + initNodes.nodeLabelName + ')'
                node_used = eval( expression )
                if node_used > 0:
                    if self.DEBUG:
                        printContents( initNodes.nodeLabelName )
#                    used_labels_GL.append(variable)
#                    used_variables_GL.append((variable, node_used))
            for goalNode in goalNodes:
                expression = 'solver.Value(' + goalNode.nodeLabelName + ')'
                node_used = eval( expression )
                if node_used > 0:
                    if self.DEBUG:
                        printContents( 'used', goalNode.nodeLabelName )
#                    used_labels_GR.append(variable)
#                   used_variables_GR.append((variable, node_used))
            for node in current_nodes_GL:
                expression = 'solver.Value(' + node.nodeLabelName + ')'
                node_used = eval( expression )

                if node_used > 0:
                    if self.DEBUG:
                        printContents( 'used', node.nodeLabelName )
                    node.value = node_used # Node value modified
                else:
                    node.value = 0

            return True
        else:
            return False



class Node:
    """Base Class for Nodes (State, Action, Goals).

    Parameters
        labelName: string
            Name of the Node
        stateLabelNode: string
            Name of state
        numCapacity: int
            max value that node could hold, important for CSP solver
        value: int
            Value of available resources, calculated by CSP-solver
        copy: boolean
            Defines wether Node is a copy node
        weight: float
            Value for optimization algorithms applied to LinGraph
    """

    def __init__( self, labelName, nodeLabelName, numCapacity, value = 0, copy = False, weight = 0 ):
        self.labelName = "" # Name of resource, i.e. P
        self.nodeLabelName = "" # i.e. S1
        self.numCapacity = "" # ie. 2 -> P:2
        self.value = 0 # Value of Resources i.e. s1 = value
        self.weight = 0

        self.setLabelName( labelName )
        self.setnodeLabelName( nodeLabelName )
        self.setCapactiy( numCapacity )
        self.setValue( value )
        self.setWeight( weight )
        self.copy = copy

        self.original = True
        self.uuid = str(uuid.uuid4())


    # Setter methods
    def setLabelName( self, labelName ):
        self.labelName = labelName

    def setnodeLabelName( self, nodeLabelName ):
        self.nodeLabelName = nodeLabelName

    def setCapactiy( self, numCapacity ):
        self.numCapacity = numCapacity

    def setValue( self, value ):
        self.value = value

    def setWeight( self, weight ):
        self.weight = weight

class ActionFormula():
    """
    effect value is the numer of resources neaded, i.e. name=P and value=4 would mean needing 4 p for precondition to be satisfied
    precondition value is number of resources that will be outputed (see above under effect for more information)

    Parameter
    ---------
        actionName : string
            Name of action to be created
    """

    def __init__( self, actionName ):
        self.actionName = actionName
        self.preconditions = []
        self.effects = []

    def addPrecondition( self, resourceName, resourceValue ):
        """ add single precondition to preconditions

        Parameter
        ---------
            resourceName : string
            resourceValue : int

        """
        self.preconditions.append( {'name':resourceName, 'value': resourceValue} )

    def addEffect( self, resourceName, resourceValue):
        """ add single effec to effects

        Parameter
        ---------
            resourceName : string
            resourceValue : int

        """
        self.effects.append( {'name':resourceName, 'value': resourceValue} )

    # setter
    def getEffects( self ):
        return self.effects

    def getPreconditions( self ):
        return self.preconditions

    def toJson( self ):
        """ Give back JSON representation of action formula
        """
        jsonStr = '{'
        jsonStr += '"name":"' + self.actionName + '",'
        jsonStr += '"preconditions": ['
        for preconditon in self.preconditions:
            jsonStr += '{"label":"' + preconditon[ 'name' ] + '","value":"' + str( preconditon[ 'value' ] ) + '"},'
        if len( self.preconditions ) > 0:
            jsonStr = jsonStr[ :-1 ]
        jsonStr += '],"effects":['
        for effect in self.effects:
            jsonStr += '{"label":"' + effect[ 'name' ] + '","value":"' + str( effect[ 'value' ] ) + '"},'
        if len( self.effects ) > 0:
            jsonStr = jsonStr[ :-1 ]
        jsonStr += ']'
        jsonStr += '}'

        return jsonStr

class ActionNode( Node ):
    """Action Node.

    Args:
        labelName: string
            Name of the Action
        stateLabelNode: string
            Name of state
        numCapacity: int
            value that node could hold
        level: int
            Level at which the node is situated
        value: int
            Value of available resources
    """

    def __init__( self, labelName, nodeLabelName, numCapacity, actionFormula, value = 0, copy = False, weight = 0 ):
            super().__init__( labelName, nodeLabelName, numCapacity, value, copy )
            self.precondions = []
            self.effects = []
            self.actionFormula = actionFormula
            self.weight = weight

    def addPrecondition( self, resourceName, value ):
        """ Add precondition to precondition list 

        Parameter
        ---------
        resourceName : string
            Name of precondition resource from action formulae
        value : int
            Value of precondition
        """
        self.precondions.append( { resourceName : value } )


    def addEffect( self, resourceName, value ):
        """ Add effect to effect list 

        Parameter
        ---------
        resourceName : string
            Name of effect resource from action formulae
        value : int
            Value of effect
        """
        self.effects.append( { resourceName: value } )
    
    def getEffects( self ):
        return self.effects

    # getter 
    def getPreconditions( self ):
        return self.preconditions

    def toJson( self ):
        """return node in JSON representation
        """

        jsonStr = "{"
        jsonStr += '"uuid":"' + self.uuid + '",'
        jsonStr += '"label":"' + self.labelName + '",'
        jsonStr += '"state":"' + self.nodeLabelName + '",'
        jsonStr += '"capacity":' + str( self.numCapacity ) + ","
        jsonStr += '"value":' + str( self.value ) + ","
        jsonStr += '"copy":' + str( self.copy ).lower() + ","
        jsonStr += '"weight":' + str( self.weight )
        jsonStr += "}"

        return jsonStr
    
class StateNode( Node ):
    """State Node.

        for more information refer to class Node
    """
    def toJson( self ):
        """Return a JSON representation of this state node            
        """        
        jsonStr = "{"
        jsonStr += '"uuid":"' + self.uuid + '",'
        jsonStr += '"label":"' + self.labelName + '",'
        jsonStr += '"state":"' + self.nodeLabelName + '",'
        jsonStr += '"capacity":' + str( self.numCapacity ) + ","
        jsonStr += '"value":' + str( self.value ) + ","
        jsonStr += '"copy":' + str( self.copy ).lower() + ","
        jsonStr += '"weight":' + str( self.weight )
        jsonStr += "}"

        return jsonStr


# Cradinality Number of Resources 
class Connection:
    """Class for connecting nodes
    Parameters:
      n1: Node
        Node at left side of connection
      n2: Node
        node at right side of connection
      cardinalatity: int
        value of connection
      coefficient: int
        nunber of times the value can be held
      resource_index: int
        if state is also conneted to other connections the resource index is incremented

    """

    def __init__( self, n1, n2, cardinality, coefficient = 0, resource_index = -1 ):
        self.node1 = n1
        self.node2 = n2
        self.cardinality = cardinality
        self.coefficient = coefficient 
        self.resource_index = resource_index # if connection with action, set resource index
        self.uuid = str(uuid.uuid4())

    # setter
    def setCardinality( self, cardinality ):
        self.cardinality = cardinality

    def setNodes( self, n1, n2 ):
        """sets both connecting nodes

        Parameter
        ---------
            n1 : Node
                Node on the left side of the connection
            n2 : Node
                Node on the right side of the connection
        """
        self.node1 = n1
        self.node2 = n2
    
    def toJson( self ):
        """Returns JSON representation of this connection
        """
        jsonStr = "{"
        jsonStr += '"uuid":"' + self.uuid + '",'
        jsonStr += '"leftnode":"' + self.node1.nodeLabelName + '",'
        jsonStr += '"rightnode":"' + self.node2.nodeLabelName + '",'
        jsonStr += '"cardinality":' + str( self.cardinality )
        jsonStr += "}"
        return jsonStr

class LinGraph:
    """Representation of Graph composed of Nodes and Connections.
        For the body it uses the class Level

    """

    def __init__( self ):
        self.DEBUG = False
        self.limit = 1000 # max levels to iterate # 1000

        # These parameters have not got to be adjusted typically
        self.constraintSolver = ConstraintSolver()
        self.graph = Graph()
        self.sibling_constraints = [] # sibling constraints are stored here
        self.dependency_constraints = [] # dependency constraints are stored here
        self.actionFormulae = [] # List of all ActionFormulae
        self.goalNodes = [] # list of all goal nodes
        self.goalNodeNum = 0
        self.stateNodeNum = 0
        self.actionNodeNum = 0
        self.weightingMethod = None
        self.pruningMethod = None
        self.valueBoundary = False 

        # printContents("DupplCombine",self.valueBoundary)

    # see fSearch_multiple_or-tools.py
    # deom Dr. Sitar Kortik
    def print_node( self, item ):
        """prints out node information

        Parameter
        ---------
            item : Node
                Node from which information is printed out
        """
        printContents( 'value:', item.labelName, '-label: ', item.nodeLabelName  , '-count: ', item.numCapacity, '-Copy: ', item.copy )


    #add statenode to current level 
    def addStateNode( self, label, numCapacity, value, copy=False ):
        """Add state node to graph at current level
        
        Parameter
        ---------
            label : string
                Name of state 
            numCapacity : int
                Max Resources the state value is able to reach
            value : int
                Value set by CSP-solver
            copy : bool
                Defines whether the state node is copy node
        """
        self.stateNodeNum += 1
        node = StateNode( label , "s" + str(self.stateNodeNum), numCapacity,  value, copy )
        self.graph.addState( node )
        return node

    # add state node at selected level
    def addStateNodeAt( self, level, label, numCapacity, value ):
        """Add state node to graph at defined level
        
        Parameter
        ---------
            level : int
                level on which state node is added
            label : string
                Name of state 
            numCapacity : int
                Max Resources the state value is able to reach
            value : int
                Value set by CSP-solver
            copy : bool
                Defines whether the state node is copy node
        """

        self.stateNodeNum += 1
        node = StateNode( label , "s" + str( self.stateNodeNum ), numCapacity,  value )
        self.graph.addStateAt( level, node )
        return node

    # add action node at selected level
    def addActionNodeAt( self,level,label, numCapacity, actionFormula, value=0 ):
        self.actionNodeNum += 1
        node = ActionNode( label, "a" + str(self.actionNodeNum), numCapacity, actionFormula, value )
        self.graph.addActionAt( level, node )
        return node

    # create action node and add it to the graph at current level
    def addActionNode( self, label, numCapacity, actionFormula, value=0 ):
        self.actionNodeNum += 1
        node = ActionNode( label, "a" + str(self.actionNodeNum), numCapacity, actionFormula, value )
        self.graph.addAction( node )
        return node

    # Create connetion node and add it to graph at current level
    def addConnection( self, node1, node2, cardinality ):
        node = Connection( node1,node2, cardinality )
        self.graph.addConnection( node )
        return node

    # add connection to graph at current level
    def addConnectionAt( self, level, node1, node2, cardinality ):
        # printContents("addConnection",node1.nodeLabelName,node2.nodeLabelName, level)
        node = Connection( node1,node2, cardinality )
        self.graph.addConnectionAt( level, node )
        return node
    

    # add init node to graph 
    def addInitNode( self, label, numCapacity ):
        self.stateNodeNum += 1
        node = StateNode( label , "s" + str(self.stateNodeNum), numCapacity,  numCapacity )
        self.graph.addState( node )
        return node

    # add goal node to goal Nodes
    def addGoalNode( self, label, numCapacity ):
        self.goalNodeNum += 1
        node = StateNode( label, "g" + str(self.goalNodeNum), numCapacity, numCapacity )
        self.goalNodes.append( node )
        return node

    # add Action formula to action formulae
    def addActionFormula( self, actionFormula ):
        self.actionFormulae.append( actionFormula )

    # -----------------------------------------

    def removeConstraint( self, labelName ):
        """
            Remove constraints of node

            Parameter
            ---------
                labelName : string
                    Label name of node for which constraints should be removed
        """
        self.removeSiblingConstraint( labelName )
        self.removeDependencyConstraint( labelName )

    def removeSiblingConstraint( self, labelName ):
        """
            Remove sibling constraints of node

            Parameter
            ---------
                labelName : string
                    Label name of node for which constraints should be removed

        """
        for c in self.sibling_constraints:
            if labelName in c.sh_left_nodes:
                if len(c.sh_left_nodes) == 1:
                    self.sibling_constraints.remove( c )
                else:
                    c.sh_left_nodes.remove( labelName )
            if labelName in c.sh_right_nodes:
                if len(c.sh_right_nodes) == 1:
                    self.sibling_constraints.remove( c )
                else:
                    c.sh_right_nodes.remove( labelName )

    def removeDependencyConstraint( self, labelName ):
        """
            Remove dependency constraint for given node

            Parameter
            ---------
                labelName : string
                    Label name of node for which constraints should be removed

        """
        for c in self.dependency_constraints:
            if labelName in c.sh_left_nodes:
                if len( c.sh_left_nodes ) == 1:
                    self.sibling_constraints.remove( c )
                else:
                    c.sh_left_nodes.remove( labelName )
            if labelName in c.sh_right_nodes:
                if len( c.sh_right_nodes ) == 1:
                    self.sibling_constraints.remove( c )
                else:
                    c.sh_right_nodes.remove( labelName )

    def getStateAction( self, nodeLabelName, level ):
        """
            Get action node of state node

            Parameter
            ---------
                nodeLabelName : string
                    node name of which the action node should be returned
                level : int
                    Level on which should be serached for the node

            Return
            ------
                list of ActionNode
                    Action node that is connected to given state node
        """
        if level > -1:
            for connection in self.graph.getConnectionsAtLevel( level ):
                # printContents(connection.node1.nodeLabelName,connection.node2.nodeLabelName,nodeLabelName)
                if connection.node2.nodeLabelName == nodeLabelName:
                    return connection.node1
        return

    def createDependencyConstraints( self ):
        """Create dependency constraints
        """

        if (self.graph.currentLevel > 0):
            for node in self.graph.getStatesAtLevel( self.graph.currentLevel - 1 ):
                first_right_labels = []
                multiplier = 1

                # connection from base node on the left side, for example (s1, s2, ...)
                for connection in self.graph.getConnectionsAtLevel( self.graph.currentLevel - 1 ):
                    # left node on connection is base node
                    if connection.node1.nodeLabelName == node.nodeLabelName: # every node on the left. This means there is action on right

                        # get first effect -> the sibling constraints makes this possible
                        effect = connection.node2.actionFormula.effects[ 0 ] # if action effect resource = state resource, only first effect

                        # iterate through all connections from the action to its children state nodes, which will be sibling if more than one exist
                        visited_action = []
                        for connection2 in self.graph.getConnectionsAtLevel( self.graph.currentLevel ): # go through all connections

                            if connection2.node1.nodeLabelName == connection.node2.nodeLabelName and not connection.node2.nodeLabelName in visited_action:

                                if (connection.node1.original):
                                    first_right_labels.append( ( connection.cardinality, effect['value'],connection2.node2.nodeLabelName ) )

                                multiplier = multiplier * effect[ 'value' ]

                                visited_action.append(connection.node2.nodeLabelName )


                right_labels = []
                for ( coefficientA, coefficientN, label ) in first_right_labels:
                    right_labels.append( ( label, ( multiplier // coefficientN ) * coefficientA ) )

                self.dependency_constraints.append( Constraint( [ ( node.nodeLabelName, multiplier ) ], right_labels ) )


    def isGoalReached( self ):
        """Check if goal has been reachted

        Returns:
            True: A goal has been found there is a solution to the plan
            False: No goal has been found, expand further if possible
        """
        printContents( "*** Check Goal ***" )
        if self.graph.currentLevel == 0: # on first level check all states the easy way
            passGoal = True
            for goalNode in self.goalNodes:
                amount = 0
                for stateNode in self.graph.getCurrentStates():
                    if stateNode.labelName == goalNode.labelName:
                        amount += stateNode.numCapacity
                if goalNode.numCapacity != amount:
                    passGoal = False
            if passGoal:
                return True
            else:
                return False
        else: # if we are in higher level, we have to apply the constraint solver, as different paths my exist
            if self.DEBUG:
                printContents( 'Current States (GL)' )
                for stateNode in self.graph.getCurrentStates():
                    printContents("value:", stateNode.labelName, "-label:", stateNode.nodeLabelName, "-count:", str( stateNode.numCapacity ), "-Copy:",  stateNode.copy )
                printContents( 'Current Goals (GR)' )
                for stateNode in self.goalNodes:
                    printContents( "value:",stateNode.labelName,"-label:", stateNode.nodeLabelName, "-count:", str(stateNode.numCapacity), "-Copy:",  stateNode.copy )
            
            conjunctions = list( set( list( map( lambda x: x.labelName, self.graph.getCurrentStates() ) ) ).intersection( list( map( lambda y: y.labelName,self.goalNodes ) ) ) )
            visited_types = []
            goal_constraints = []
            zero_labels = []

            for goalNode in self.goalNodes:
                if goalNode.labelName not in conjunctions:
                    zero_labels.append( goalNode.nodeLabelName ) 

            for stateNode in self.graph.getCurrentStates():
                if stateNode.labelName not in visited_types:

                    left_constraints = list( map( lambda f_node: ( f_node.nodeLabelName, 1 ), list( filter( lambda node: node.labelName ==  stateNode.labelName, self.graph.getCurrentStates() ) ) ) )
                    right_constraints = list( map( lambda f_node2: ( f_node2.nodeLabelName, 1 ), list( filter( lambda node2: node2.labelName == stateNode.labelName, self.goalNodes ) ) ) )

                    if right_constraints == []:
                        zero_labels.append(stateNode.nodeLabelName)
                    else:
                        goal_constraints.append( Constraint( left_constraints, right_constraints ) )
                    visited_types.append( stateNode.labelName )
                    # printContents(goal_constraints)
            # also the node values are modified
            goalPass = self.constraintSolver.solve_constraints( self.graph.getStatesFromLevelOne(), self.sibling_constraints, self.dependency_constraints, goal_constraints, conjunctions, zero_labels, self.graph.getStatesAtLevel( 0 ), self.goalNodes )

            if ( not goalPass ): 
                printContents( '************* NO SOLUTION!' )
                return False # Goal not found

            self.extractPlanVis()
            self.extractPlan()

            return True

    def extractPlan( self ):
        """ Prints out action labels, values and counts. 
        Parts of this code are taken from the source code of Dr. Sita Kortik (fSearch_multiple_or-tools.py) 

        Returns:
            void
        """

        for level in range( self.graph.currentLevel ):
            printContents( "Level-", str( level + 1 ), "Actions" )
            for action in self.graph.getActionsAtLevel( level ):
                if ( action.value > 0 and not action.copy ):
                    printContents( 'Action value:', action.labelName, ' -- Action label:',  action.nodeLabelName, ' -- Action count:', action.value )
        

    def extractPlanVis( self ):
        """
        Fix the values of the connections and actions. The CSP solver only update the states so we need to update the connections and actions
        Returns:
            void
        """
                    # adjust connections from actions cardinality and action values
        actions_visited = []
        for lvl in range( self.graph.currentLevel + 1 ):
            for connection in self.graph.getConnectionsAtLevel( lvl ):
                if ( connection.node2.nodeLabelName[0] == 's' ): # node 1 is automatically an action node
                    connection.cardinality = connection.node2.value
                    if connection.node1.copy == False and not connection.node1.nodeLabelName in actions_visited:
                        for effect in connection.node1.actionFormula.effects:
                            if effect[ 'name' ] == connection.node2.labelName:
                                actions_visited.append( connection.node1.nodeLabelName )
                                if effect[ 'value' ] == 0:
                                    connection.node1.value = 0
                                else:
                                    connection.node1.value = int( connection.node2.value / effect[ 'value' ] )
                                break

        # adjust copy connections between copy action nodes and child state nodes
        for lvl in reversed( range( self.graph.currentLevel + 1 ) ):
            for connection in self.graph.getConnectionsAtLevel( lvl ):
                if ( connection.node1.nodeLabelName[0] == 'a' and connection.node2.copy ): # node 1 is automatically an state node
                    connection.cardinality = connection.node2.value



        # adjust values for action nodes
        for lvl in reversed( range( self.graph.currentLevel + 1 ) ):
            for connection in self.graph.getConnectionsAtLevel( lvl ):
                actions_visited = [] # action could have same name for SAT solver if copied

                # copy nodes
                if ( connection.node1.copy and connection.node1.nodeLabelName[ 0 ] == 'a' ): # node 1 is automatically an state node
                    if connection.node1.nodeLabelName not in actions_visited:
                        actions_visited.append( connection.node1.nodeLabelName )
                        connection.node1.value = 0
                    connection.node1.value += connection.node2.value
                    connection.node1.numCapacity = connection.node2.numCapacity

        # adjust connections for copy nodes
        for lvl in reversed( range( self.graph.currentLevel + 1 ) ):
            for connection in self.graph.getConnectionsAtLevel( lvl ):
                if (connection.node2.copy and connection.node2.nodeLabelName[ 0 ] == 'a' ): # node 1 is automatically an state node
                    connection.cardinality = connection.node2.value

        # adjust connections from state to action nodes that are not copied
        for lvl in reversed( range( self.graph.currentLevel + 1 ) ):
            for connection in self.graph.getConnectionsAtLevel( lvl ):
                if ( not connection.node2.copy and connection.node2.nodeLabelName[ 0 ] == 'a' ): # node 1 is automatically an state node
                    connection.cardinality = connection.node2.value


    def provePlan( self ):
        """
            Prove plan
            set up graph and outputs information on configuration
        """
        printContents( 'Init Nodes:' )
        for node in self.graph.getCurrentStates():
            self.print_node( node )

        printContents( 'Goal Nodes:' )
        for  node in self.goalNodes:
            self.print_node( node )

        printContents( 'Action Formulars:' )
        for actionFormula in self.actionFormulae:
            printContents( actionFormula.actionName )
            printContents( ' -> preconditions',actionFormula.preconditions )
            printContents( ' -> effects',actionFormula.effects )
        
        if self.valueBoundary:
            printContents( '-------------------------------' )
            printContents( 'Calculate value boundary vector' )
            printContents( '-------------------------------' )
            self.calculateActionFormulaeGoalPreconditionVector()
            printContents('Boundary for resources: ', self.actionFormulaeGoalPreconditionVector)
            printContents( '-------------------------------' )


        return self.process()

    def getPersistentResources( self, actionFormulae ):
        """ 
            extract all persistent ressources

            Parameter
            ..........
                actionFormulae : array of action formulae 
                    action formulae to extract persistent resources from
        """
        resources = []
        for a in actionFormulae:
            for precondition in a.preconditions:
                for effect in a.effects:
                    if ( precondition[ 'name' ] == effect[ 'name' ] ):
                        resources.append( precondition[ 'name' ] )
                        break
        return resources


    def calculateActionFormulaeGoalPreconditionVector( self ):
        """
        Approximate vague need of preconditions
        """

        printContents( '----------------------------------------------------' )
        printContents( 'Calculate Resource limit for generating action nodes' )        
        printContents( '----------------------------------------------------' )

        self.actionFormulaeGoalPreconditionVector = {}
        currentResources = {}
        oldResources = []
        levelCount = 0

        persistentResources = self.getPersistentResources(self.actionFormulae)

        # Algorithm backtracks from goals
        for g in self.goalNodes:
            self.actionFormulaeGoalPreconditionVector[g.labelName] = g.numCapacity
            if g.labelName not in persistentResources:
                currentResources[g.labelName] = g.numCapacity

        # limit the number of iterations
        # only loop if limit has not been reached and new Resources are added or all necessary resources have been found
        while ( oldResources != currentResources and len( currentResources ) != 0 and levelCount < self.limit):
            oldResources = copy.deepcopy( currentResources ) # for checking if there is change
            # iterate through all action formulae
            for a in self.actionFormulae:
                times = 0
                for e in a.effects:
                    if e[ 'name' ] in currentResources.keys():
                        # get times an action has to be performed
                        if times > 0:
                            times = min( times, math.ceil( currentResources[ e[ 'name' ] ] / e[ 'value' ] ) )
                        else:
                            times = math.ceil( currentResources[ e[ 'name' ] ] / e[ 'value' ] )
                        del currentResources[ e[ 'name' ] ] # Resource was found so delete it
                if times > 0:
                    levelCount += 1
                    # add preconditions
                    effectNotInPreconditions = True
                    for p in a.preconditions:
                        for e in a.effects: # filter out persistent preconditions
                            if e[ 'name' ] == p[ 'name' ]:
                                effectNotInPreconditions = False
                                break
                        if effectNotInPreconditions:
                            if p[ 'name' ] in self.actionFormulaeGoalPreconditionVector.keys():
                                self.actionFormulaeGoalPreconditionVector[ p[ 'name' ] ] += times * p[ 'value' ]
                            else: # precondions not yet added
                                self.actionFormulaeGoalPreconditionVector[ p[ 'name' ] ] = times * p[ 'value' ]
                            
                            if p[ 'name' ] in currentResources.keys():
                                currentResources[ p[ 'name' ] ] += times * p[ 'value' ]
                            else:
                                currentResources[ p[ 'name' ] ] = times * p[ 'value' ]

        # correction because of persistent resources if they are greater than the other resources
        maxNum = 0
        minNum = sys.maxsize
        for name in self.actionFormulaeGoalPreconditionVector.keys():
            maxNum = max( maxNum, self.actionFormulaeGoalPreconditionVector[ name ])
            minNum = min( minNum, self.actionFormulaeGoalPreconditionVector[ name ])
        coefficient = maxNum/minNum
        if coefficient < 1:
            coefficient = 1

        for name in self.actionFormulaeGoalPreconditionVector.keys():
            self.actionFormulaeGoalPreconditionVector[ name ] *= coefficient
            self.actionFormulaeGoalPreconditionVector[ name ] = int( self.actionFormulaeGoalPreconditionVector[ name ] )
            # Output information on calculated resource limits
            printContents( name, ":", self.actionFormulaeGoalPreconditionVector[ name ] )
        printContents( '----------------------------------------------------' )

    def process( self ):
        """
            Run LinGraph process

            1. Check if Goal was reached
            2. Else check if level limit has been breached
            3. Else expand graph
        """
        if self.isGoalReached(): 
            printContents( "Found a solution -  Goals have been reached" )
            return True
        else:
            if self.graph.currentLevel >= self.limit-1:
                printContents( "Limit level", self.limit ,"reached - expansion terminated." )
                # exit()
                return False
            if ( self.expandGraph() ):
                return self.process()
            else:
                printContents( "No possibility to reach Goal. No solution available." )
                return False
            
    def step( self ):
        """
        Expand graph one level more layer
        """

        if self.valueBoundary:
            self.calculateActionFormulaeGoalPreconditionVector()

        if self.isGoalReached(): 
            printContents( "Found a solution -  Goals have been reached" )
            return True
        else:
            if self.graph.currentLevel >= self.limit-1:
                printContents( "Limit level", self.limit ,"reached - expansion terminated." )
                # exit()
                return False
            printContents( "Expanding graph once." )
            if ( self.expandGraph() ):
                if self.isGoalReached():
                    printContents( "Found a solution -  Goals have been reached" )
                    return True
                return False

    def use_preconditions( self, node, preconditions ):
        """Return possible preconditions with the help of nodes and preconditions

            This function was copied from the source code of Dr. Sita Kortik and modified 
            fSearch_multiple_or-tools.py 

            Parameter
            ---------

            node : Node
                Node from which different precondition possibilities are derived
            preconditions : list of dictionary 
                Preconditions with name and value

            
            Returns
            -------
                list 
                    List of new precondition with possible counts

        """

        new_preconditions = []
        count = 0
        for precondition in preconditions: # preconditions: [('type', count)..]
            if node.labelName == precondition[ 'name' ]:
                if node.numCapacity >= precondition[ 'value' ]:
                    count = precondition[ 'value' ]
                else:
                    count = node.numCapacity
                    new_preconditions.append( { 'name' : precondition['name'], 'value' : precondition['value'] - count} )
            else:
                new_preconditions.append( precondition )
        return ( new_preconditions, count )


    def find_action_combinations( self, nodes, preconditions, effects, one_combination, combinations ):
        """Find all combinations for the given nodes that satisfy preconditions
            one combination is a list of [(node, count)..].  
            This function was copied from the source code of Dr. Sita Kortik (fSearch_multiple_or-tools.py) and has been slightly modified.
        
        Parameter
        ---------
            nodes : list

            preconditions : list
                Preconditions for creating combinations
            effects : list
                Effects for creating combinations
            one_combination : list of tuple

            combinations: list of tuple

        Returns:
            list of tuple
                New combinations found for beeing tested
        """
        if len( preconditions ) > 0:
            if len( nodes ) > 0:
                node = nodes.pop()

                temp_preconditions = preconditions
                ( new_preconditions, count ) = self.use_preconditions( node, preconditions )

                if count == 0: # no match of preconditions with the given node

                    new_combinations2 = self.find_action_combinations( nodes, preconditions, effects, one_combination, combinations )

                    return new_combinations2
                else:
                    temp_nodes = list( nodes )
                    # temp_new_preconditions = list(new_preconditions)
                    temp_one_combination = list( one_combination )
                    one_combination.append( ( node, count ) )

                    new_combinations3 = self.find_action_combinations( nodes, new_preconditions, effects, one_combination, combinations )

                    k = count - 1 # decreasing used node count 1 to find other combinations
                    if k == 0:

                        new_combinations4 = self.find_action_combinations( temp_nodes, temp_preconditions, effects, temp_one_combination, new_combinations3 )

                        return new_combinations4
                    else:
                        new_node = copy.deepcopy( node )
                        new_node.original = False # Mark this as not original
                        new_node.numCapacity = k
                        temp_nodes.append( new_node )

                        new_combinations5 = self.find_action_combinations( temp_nodes, temp_preconditions, effects, temp_one_combination, new_combinations3 )

                        return new_combinations5

            else: # temp_nodes is empty

                return combinations
        else: # the list of preconditions is empty

            copy_flag = True
            sibling_flag = True
            action_label = ""

            for (node, count) in one_combination:

                if node.copy == False: # at least one node is not a copy node
                    copy_flag = False

                if self.getStateAction( node.nodeLabelName,self.graph.currentLevel - 1 ) == None: # if the n node is at the first level, no need to sibling check
                    sibling_flag = False
                    break
                else:

                    prevAction = self.getStateAction( node.nodeLabelName, self.graph.currentLevel - 1 )
                    # coefficientA = prevAction.numCapacity

                    if action_label == "":

                        action_label = prevAction.nodeLabelName
                    if action_label != prevAction.nodeLabelName: # if at least one action is different, they are not siblings 
                        sibling_flag = False
                    action_label = prevAction.nodeLabelName

            if ( copy_flag == False ):
                if ( sibling_flag == False ): # if preconditions are not sibling, we add the combination
                    return ( [ one_combination ] + combinations )
                else: # if preconditions are siblings, we check if it is not a symmetric action
                    ( node, count ) = one_combination[ 0 ]

                    prevActionNode = self.getStateAction( node.nodeLabelName, self.graph.currentLevel - 1 )

                    ( prevAction, coefficientA )  = lambda x: ( x, x.numCapacity ), prevActionNode 


                    if len( prevActionNode.actionFormula.preconditions ) == len( effects ): # a candidate for a symmetric action
                        new_effect_values = list( map( lambda effect_tuple: effect_tuple[ 'name' ], effects ) )
                        # printContents(new_effect_values)
                        for ( prevAction_precondition, coefficient ) in list( map( lambda x: ( x['name'], x['value'] ), prevActionNode.actionFormula.preconditions ) ):
                            if prevAction_precondition in new_effect_values:
                                new_effect_values.remove( prevAction_precondition )

                            else:

                                return ( [ one_combination ] + combinations )

                        return combinations
                    else: # not a symmetric action
                        return ( [ one_combination ] + combinations )
            else:
                return combinations


    def expandGraph( self ):
        """
            Expand graph 
            1. Create new Level 
            2. find possible combinations of possible acitons
            3. Remove impaired combinations
            4. create action and child nodes
            5. Copy nodes
            6. Apply constraints
        """
        # Create New Level
        self.graph.newLevel()
        printContents( "------> Level ", str( self.graph.currentLevel ), " ------ Expand Graph" )
        if self.DEBUG:
            printContents( "Number of current nodes:", str( len( self.graph.getStatesAtLevel( self.graph.currentLevel - 1 ) ) ) )
            printContents( "Current nodes: " )
            for node in self.graph.getStatesAtLevel( self.graph.currentLevel - 1 ):
                self.print_node( node )
        # Find possible compinations
        for actionFormula in self.actionFormulae:

            tmp_nodes = copy.deepcopy( self.graph.getStatesAtLevel( self.graph.currentLevel - 1 ) )
            effects = copy.deepcopy( actionFormula.effects )
            preconditions = copy.deepcopy( actionFormula.preconditions )

            # For this find all combinations possible
            combinations = self.find_action_combinations( tmp_nodes, preconditions, effects,[],[] )

            if self.DEBUG:
                printContents( "Combinations before deleting:" )
                for combination in combinations:
                    # printContents(combination)
                    printContents( "One Combination:" )
                    for oneCmb in combination:
                        printContents ( oneCmb[ 0 ].labelName, oneCmb[ 0 ].nodeLabelName, "Count: ", oneCmb[ 1 ] )

            # check with constrained solver the new combinations
            newCombinations = []
            for oneCombination in combinations:
                if self.graph.currentLevel > 1:
                    ( solver, isSolved ) = self.constraintSolver.solve_impaired_constraints( oneCombination, self.graph.getStatesFromLevelOne(), self.sibling_constraints, self.dependency_constraints, self.graph.getStatesAtLevel( 0 ) )

                    if isSolved:
                        if self.DEBUG:
                            printContents( '************* A SOLUTION for impaired constraints!' )
                        newCombinations.append( oneCombination )
                else:   # if new combination is ok add it
                    newCombinations.append( oneCombination )

            if self.DEBUG: 
                printContents( "Combinations after deleting:" )
                for combination in newCombinations:
                    printContents( "One Combination:" )
                    for oneCmb in combination:
                        printContents ( oneCmb[0].labelName,oneCmb[0].nodeLabelName,"Count: ",oneCmb[1], oneCmb[0].original )

            maxLabelDict = {}

            for combination in newCombinations:
                for oneCmb in combination:
                        if oneCmb[0].labelName in maxLabelDict.keys():
                            if maxLabelDict[oneCmb[0].labelName] < oneCmb[1]:
                                maxLabelDict[oneCmb[0].labelName] = oneCmb[1]
                        else:
                            maxLabelDict[oneCmb[0].labelName] = oneCmb[1] 

            # if combination are available create action and child state nodes
            if ( len( newCombinations ) > 0 ):
                # if value boundary is activated initialize
                if self.valueBoundary: 
                    countActionformulaePreconditions = {}
                    for e in actionFormula.effects:
                        countActionformulaePreconditions[ e['name'] ] = 0
                        
                tmp_sibling_constraints = []
                for one_combination in newCombinations:
                    action_count = sys.maxsize
                    for ( node, coefficient ) in one_combination:
                        if ( node.numCapacity > 0 ):
                            min_count = node.numCapacity // coefficient 
                            if ( min_count < action_count ):
                                action_count = min_count
                    
                    # if value boundary activated test if new combinations are allowed to be created
                    # Remove action nodes if value boundary is activated and surpassed.
                    if self.valueBoundary and len(self.graph.actions[self.graph.currentLevel - 1]) > 0:
                        doNotIncludeActionNode = False
                        # look through each precondition estimated values
                        for afgp in self.actionFormulaeGoalPreconditionVector.keys():
                            for e in actionFormula.effects:
                                if afgp == e['name']:
                                    # if effect of action is still needed considering estimation add it
                                    # this only applies to one level and does not take other levels into account
                                    if afgp in countActionformulaePreconditions.keys(): 
                                        if self.actionFormulaeGoalPreconditionVector[ afgp ] > countActionformulaePreconditions[ afgp ]: #+ (action_count * e[ 'value']):
                                            countActionformulaePreconditions[ afgp ] += (action_count * e[ 'value'])
                                        else:
                                            doNotIncludeActionNode = True
                                            break # no further action to continue with given resource
                        
                        # if value Boundary activated, if no furhter action to continue with given resource got to next item
                        if doNotIncludeActionNode:
                            continue # do not include action formula

                    # Add for each combination one new action node
                    action = self.addActionNodeAt( self.graph.currentLevel - 1, actionFormula.actionName, action_count, actionFormula, 0 )
                    

                    for ( node, coefficient ) in one_combination:
                        resource_index = 0
                        for precondition in actionFormula.preconditions:
                            if precondition[ 'name' ] == node.labelName:
                                break

                            resource_index += 1

                        conn = self.addConnectionAt( self.graph.currentLevel - 1, node, action, coefficient ) 
                        conn.resource_index = resource_index

                    # action.numCapacity = action_count
                    action.value = 0 # set value to zero

                    # For sibling constraints we need empty first node
                    firstStateNode = None
                    coefficient1 = 0
                    num_effect = 0
                    # create new state nodes for each effect of the action formular
                    for effect in action.actionFormula.effects:
                        stateNode = self.addStateNode( effect['name'], action.numCapacity*effect['value'], 0 )

                        if self.DEBUG:
                            printContents( "new_node created:", stateNode.labelName, stateNode.nodeLabelName, stateNode.numCapacity )

                        connection = self.addConnection( action,stateNode,effect['value'] )
                        connection.resource_index = num_effect
                        num_effect += 1

                        # add sibling constrints
                        if ( firstStateNode == None ): # no node set yet? it must be first node.
                            firstStateNode = stateNode
                            coefficient1 = effect[ 'value' ]
                        else:
                            # Create sibling constraints
                            tmp_sibling_constraints.append( Constraint( [ ( firstStateNode.nodeLabelName,effect[ 'value' ] ) ], [ ( stateNode.nodeLabelName, coefficient1 ) ] ) )

                # add sibling constraints after all state nodes have been created for the new action node
                self.sibling_constraints.extend( tmp_sibling_constraints )
                

        # Copy nodes
        self.copyNodes()

        # Expansion failed if there are no action nodes
        if len( self.graph.getActionsAtLevel( self.graph.currentLevel - 1 ) ) == 0:
            return False


        # create dependeny constraints
        self.createDependencyConstraints()

        if self.weightingMethod != None:
            self.weightingMethod.process(self.graph.getActionsAtLevel( self.graph.currentLevel - 1 ) )
        if self.pruningMethod != None and self.graph.currentLevel > 1: # do not prune in first level as vital resources will be pruned
            self.pruningMethod.process( self.graph, self.graph.getActionsAtLevel( self.graph.currentLevel - 1 ), None, self.sibling_constraints, self.dependency_constraints )

        return True


    def copyNodes( self ):
        """copy nodes
            create a copy action and a state node of each prevous node with the state count
        """

        # create Copy nodes
        for state in self.graph.getStatesAtLevel( self.graph.currentLevel - 1 ):
            # only add copy state if count > 0
            count = self.graph.getConnectionNodeCount( state.nodeLabelName )

            copyActionFormula = ActionFormula( "copy " + state.labelName )
            copyActionFormula.addPrecondition( state.labelName, 1 )

            copyActionFormula.addEffect( state.labelName, 1 )

            action = self.addActionNodeAt( self.graph.currentLevel - 1 ,copyActionFormula.actionName,  1, copyActionFormula )
            action.copy = True
            if ( self.DEBUG ):
                printContents( "new copy node: " + action.nodeLabelName )
            self.addConnectionAt( self.graph.currentLevel-1,state,action, 1 )

            if (self.graph.countStateActions( state.nodeLabelName) > 1 ): 
                stateNew = self.addStateNode( state.labelName, state.numCapacity, 0, True )
            else: # one or less action init state with same label as previous state 
                # seems to be important for solver
                stateNew = StateNode( state.labelName, state.nodeLabelName, state.numCapacity, 0, True )
                self.graph.addState( stateNew )
            self.addConnectionAt( self.graph.currentLevel,action,stateNew, 1 )

    def toJson(self):
        """Export graph with all information
            - graph
            - goal nodes
            - sibling constraints
            - dependency constraints
            - action formulae
        """
        goalNodeJson = ' '

        for goalNode in self.goalNodes:
            goalNodeJson += goalNode.toJson() + ','

        return '{ "graph":' + self.graph.toJson() + ', "goals":[' + goalNodeJson[ :-1 ] +'], "sibling_constraints":[' + self.sibling_constraintsToJson() + '],"dependency_constraints":[' + self.dependency_constraintsToJson() + '], "action_formulas":[' + self.actionFormulaeToJson() +']}' 

    def sibling_constraintsToJson(self):
        """Give back sibling constraints as JSON
        """
        sibling_constraintStr = " "
        for sibling_constraint in self.sibling_constraints:
            sibling_constraintStr += sibling_constraint.toJson() + ","
            
        return sibling_constraintStr[:-1]
        

    def dependency_constraintsToJson(self):
        """Give back dependency constraints as JSON
        """
        dependency_constraintStr = " "
        for dependency_constraint in self.dependency_constraints:
            dependency_constraintStr += dependency_constraint.toJson() + ","
            
        return dependency_constraintStr[ :-1 ]

    def actionFormulaeToJson(self):
        """Give back action formulae as JSON
        """
        actionFormulaetr = " "
        for actionFormula in self.actionFormulae:
            actionFormulaetr += actionFormula.toJson() + ","
            
        return actionFormulaetr[ :-1 ]

    def fromJson( self, jsonStr ):
        """Load Graph from JSON string

            Parameter
            ---------
                jsonStr : string
                    JSON string of graph to be imported
        """
        jsonObject = json.loads( jsonStr )
        graphArr = jsonObject[ "graph" ]

        # empty action formulas
        self.actionFormulae = []
        
        if "action_formulas" in jsonObject:
            for actionFormula in jsonObject[ "action_formulas" ]:
                
                actionFormulaObject = ActionFormula( actionFormula[ 'name' ] )
                for precondition in actionFormula[ "preconditions" ]:
                    actionFormulaObject.addPrecondition( precondition[ 'label' ], int( precondition[ 'value' ] ) )

                for effect in actionFormula[ "effects" ]:
                    actionFormulaObject.addEffect( effect[ 'label' ], int( effect[ 'value' ] ) )
                
                self.actionFormulae.append( actionFormulaObject )

        self.graph.clear()

        for level in graphArr:
            levelNumber = level[ 'level' ]
            self.graph.newLevel()

            for state in level[ 'states' ]:
                self.addStateFromJson( state, levelNumber - 1 )
                
            for action in level[ 'actions' ]:
                self.addActionStateFromJson( action, levelNumber - 1 )


        self.stateNodeNum = int(self.graph.getStatesAtLevel(levelNumber-1)[-1].nodeLabelName[1:])
        if (levelNumber>1):
            self.actionNodeNum = int(self.graph.getActionsAtLevel(levelNumber-2)[-1].nodeLabelName[1:])
        else:
            self.actionNodeNum = 0

        for level in graphArr:
            levelNumber = level[ 'level' ]           
            for connection in level[ 'connections' ]:
                self.addConnectionFromJson( connection, levelNumber - 1 ) 
            
            for connection in self.graph.connections[levelNumber - 1]:
                if connection.node1.__class__.__name__ != 'StateNode' and connection.node1.copy and len(connection.node1.actionFormula.preconditions) == 0:
                    connection.node1.actionFormula.addPrecondition( connection.node2.labelName, 1 )
                    connection.node1.actionFormula.addEffect( connection.node2.labelName, 1 )
                
                if connection.node2.__class__.__name__ != 'StateNode' and connection.node2.copy and len(connection.node2.actionFormula.preconditions) == 0:
                    connection.node2.actionFormula.addPrecondition( connection.node1.labelName, 1 )
                    connection.node2.actionFormula.addEffect( connection.node1.labelName, 1 )

        # goals
        for goal in jsonObject[ "goals" ]:
            self.addGoalFromJson( goal )

        # constraints
        if "sibling_constraints" in jsonObject: 
            for sibling_constraint in jsonObject[ 'sibling_constraints' ]:
                self.addSiblingConstraintFromJson( sibling_constraint )

        if "dependency_constraints" in jsonObject: 
            for dependency_constraint in jsonObject[ 'dependency_constraints' ]:
                self.addDependencyConstraintFromJson( dependency_constraint )

    def addSiblingConstraintFromJson( self, constraint ):
        """Import sibling constraint from JSON

            Parameter
            ---------
                constraint : dict
                    Constraint to be imported to the graph
        """
        # [('s1', 1)]
        left_nodes = []
        right_nodes = []
        for left_node in constraint[ 'left_nodes' ]:
            left_nodes.append( ( left_node[ 'label' ], int( left_node[ 'value' ] ) ) )

        for right_node in constraint[ 'right_nodes' ]:
            right_nodes.append( ( right_node[ 'label' ], int( right_node[ 'value' ] ) ) )
        
        constraintObject = Constraint( left_nodes, right_nodes )
        self.sibling_constraints.append( constraintObject )

    def addDependencyConstraintFromJson( self, constraint ):
        """Import dependency constraint from JSON

            Parameter
            ---------
                constraint : dict
                    Constraint to be imported to the graph
        """
        # [('s1', 1)]
        left_nodes = []
        right_nodes = []
        for left_node in constraint[ 'left_nodes' ]:
            left_nodes.append( ( left_node[ 'label' ], int( left_node[ 'value' ] ) ) )

        for right_node in constraint[ 'right_nodes' ]:
            right_nodes.append( ( right_node[ 'label' ], int( right_node[ 'value' ] ) ) )

        constraintObject = Constraint( left_nodes, right_nodes )
        self.dependency_constraints.append( constraintObject )

    def addGoalFromJson( self, goal ):
        """Import goal from JSON

            Parameter
            ---------
                goal : dict
                    Goal to be imported to the graph
        """

        self.addGoalNode( goal[ 'label' ],goal[ 'capacity' ] )

    def addStateFromJson( self, state, level ):
        """Import state node from JSON at defined level

            Parameter
            ---------
                state : dict
                    state to be imported to the graph
                level : int
                    level at which state is imported to
        """

        if 'copy' in state:
            copyBool = state[ 'copy' ]
        else: 
            copyBool = False

        stateNode = StateNode( state[ 'label' ], state[ 'state' ],  int(state[ 'capacity' ]), int(state[ 'value' ]), copyBool, int(state[ 'weight' ]) )
        self.graph.addStateAt( level, stateNode )

    def addActionStateFromJson( self, action, level):
        """Import action node from JSON at defined level

            Parameter
            ---------
                action : dict
                    action to be imported to the graph
                level : int
                    level at which action is imported to
        """

        if 'copy' in action:
            copyBool = action['copy']
        else: 
            copyBool = False

        actionNode = ActionNode( action['label'], action['state'],  int(action['capacity']), None, int(action['value']), copyBool, int(action['weight']) )

        for actionFormula in self.actionFormulae:
            if (actionFormula.actionName == action['label']):
                actionNode.actionFormula = actionFormula
                break

        # if no action formula present there is a copy node
        if actionNode.actionFormula == None:
            actionNode.actionFormula = ActionFormula(action['label'])

        self.graph.addActionAt( level, actionNode )

    def addConnectionFromJson( self, connection, level ):
        """Import connection from JSON at defined level

            Parameter
            ---------
                connection : dict
                    connection to be imported to the graph
                level : int
                    level at which connection is imported
        """

        n1 = None
        n2 = None

        # only names as strings are available, so iterate through all state and action nodes to these to the connections
        for l in range( level-2, level+2 ): # 3 levels
            if l > -1 and l <= self.graph.currentLevel:
                states = self.graph.getStatesAtLevel( l )
                actions = self.graph.getActionsAtLevel( l )
                for state in states:
                    if state.nodeLabelName == connection[ 'leftnode' ]:
                        n1 = state
                        break
                
                for action in actions:
                    if action.nodeLabelName == connection[ 'leftnode' ]:
                        n1 = action
                        break
                
                states = self.graph.getStatesAtLevel( l )
                actions = self.graph.getActionsAtLevel( l )
                
                for state in states:
                    if state.nodeLabelName == connection[ 'rightnode' ]:
                        n2 = state
                        break
                
                for action in actions:
                    if action.nodeLabelName == connection[ 'rightnode' ]:
                        n2 = action
                        break
            
                if n1 != None and n2 != None: 
                    break
        
        connectionNode = Connection( n1, n2, connection['cardinality'] )
        self.graph.addConnectionAt(level, connectionNode)


    def getNumStates( self ):
        """Returns the number of all state node"""
        sum = 0
        for i in range( self.graph.currentLevel + 1 ):
            sum += len( self.graph.getStatesAtLevel( i ) )
        return sum

    def addShortToLongFormGoals( self, G ):
        """Create Goal nodes from short form (resource name, amount)

            Parameter
            ---------
                G : list of tuples
        """
        for node in G:
            self.addGoalNode( node[0], node[1] )

    def addShortToLongFormInit( self, I ):
        """Create Init nodes from short form (resource name, amount)
            
            Parameter
            ---------
                I  : list of tuples
        """
        for node in I:
            self.addInitNode( node[0], node[ 1 ] )


    def addShortToLongFormActionFormulae( self, A, reverse = False ):
        """Create Init nodes from short form (resource name, amount)
            
            Parameter
            ---------
                A  : list of tuples
                    Action formulae
                reverse : bool
                    Reverse lets the goal nodes be the init nodes
        """

        for action in A:
            actionFormulaName = action[ 0 ]
            if reverse:
                ActionFormulaName += ' (reversed)'
            actionFormula = ActionFormula( actionFormulaName )
            if reverse:
                for precondition in action[ 2 ]:
                    actionFormula.addPrecondition( precondition[ 0 ], precondition[ 1 ] )

                for effect in action[ 1 ]:
                    actionFormula.addEffect( effect[ 0 ], effect[ 1 ] )
            else:
                for precondition in action[ 1 ]:
                    actionFormula.addPrecondition( precondition[ 0 ], precondition[ 1 ] )

                for effect in action[ 2 ]:
                    actionFormula.addEffect( effect[ 0 ], effect[ 1 ] )

            self.addActionFormula( actionFormula )

    def setWeightingMethod(self, method):
        self.weightingMethod = method
    
    def setPruninMethod(self, method):
        self.pruningMethod = method
    
    def setValueBoundary(self, activate):
        """
        Activate Action node generation within limited resources

        Parameter
        ---------
            activate : bool
                If true activate action node creation by resource limit
        """
        self.valueBoundary = activate

    def setUpWithShortform( self, I, A, G, reverse = False ):
        """AI is creating summary for setUpWithShortform

            Example:
            I = [('C', 8), ('M', 4)]
            G = [('P', 4), ('M', 4), ('K', 4)]
            A = [('(C,M)->P',[('C', 1),('M', 1)],[('P', 1),('M', 1)]),('(C,M)->K',[('C', 1),('M', 1)],[('K', 1),('M', 1)])]

        Parameter:
            I : string
                Init nodes in short form
            A : string
                ActionFormulae in short form
            G : string
                Goal nodes in short form 
        """

        if (reverse):
            printContents("Prove Reversed")
            self.addShortToLongFormInit(G)

            self.addShortToLongFormGoals(I)

            self.addShortToLongFormActionFormulae(A, True)

        else:
            self.addShortToLongFormInit(I)

            self.addShortToLongFormGoals(G)

            self.addShortToLongFormActionFormulae(A)

    def setCombine(self, combine):
        """
        Combine Action Formulars with Combine-Class
        """
        self.actionFormulae = combine.combine(self.actionFormulae)

# ---------- Beginning of Modul functions ----------

def printContents( *args ):
        """
        Print out information and 
        """
        print( *args )
        output_contents.append( " ".join( map( str, args ) ) )

def prove ( I, G, A, reverse = False, combine = None, weightingMethod = None, pruningMethod = None, valueBoundary = False ):
    """" Prove graph. First construct the graph and then configure different options. Output graph information
    
    Patameters
        I : string
            Init states in short form
        G : string
            Goal nodes in short form
        A : string
            Action formulae in short from
        reverse : bool
            The goal nodes are seen as init nodes and the init as goal nodes
        combine : CombineActionFormulae
            Clustering action formulae activated
        weightingMethod : WeightedValueOptimization
            Weighting methods for nodes
        pruningMethod : Prune
            Pruning method for nodes
        valueBoundary : boolean
            Activate value boundary for generating action nodes
    """
    graph = LinGraph()

    if (weightingMethod is not None):
        graph.setWeightingMethod(weightingMethod)
        printContents("Graph weighting: ",weightingMethod.__class__)
    
    if (pruningMethod is not None):
        graph.setPruninMethod(pruningMethod)
        printContents("Graph pruning: ",pruningMethod.__class__)

    graph.setValueBoundary(valueBoundary)
    
    # graph.setPropagation( 'forward' )
    graph.setUpWithShortform( I, A, G, reverse )

    if combine != None:
        graph.setCombine( combine )

    printContents( "====================" )
    printContents( "| LinGraph |" )
    printContents( "====================" )
    printContents()

    printContents( '>>>>>>>>>>>>>>>>' )
    printContents( 'Start Algorithm:' )
    printContents( '>>>>>>>>>>>>>>>>' )
    printContents()
    start_time = time.perf_counter()
    printContents( 'Result:' )
    printContents( '----------------' )

    proved = graph.provePlan()

    if ( proved ):
        strProved = 'proved'
    else:
        strProved = 'could not be proved'

    printContents()
    printContents( 'Number of nodes generated (w/o action & goal nodes): ', str( graph.getNumStates() ) )
    printContents( 'I:', I, 'G:', G, strProved)

    printContents( 'Performance: ' )
    printContents( str( time.perf_counter() - start_time ), 'seconds' )
    printContents()
    printContents( '----------------------------' )
    printContents( 'Generate output file (JSON):', "lingraphOutput" + str( datetime.now() ).replace(":",".") + ".json" )
    printContents( '----------------------------' )
    # windows does not like three :'s
    filename =  r"./output/lingraphOutput" + str( datetime.now() ).replace(":",".") + ".json"
    fileObject = open( filename, "w" )
    fileObject.write( graph.toJson() )
    fileObject.close()
    printContents( 'completed' )
    printContents( '----------------------------' )

    return (graph, proved)


# --- MAIN PROGRAMM ---
if __name__ == '__main__':

    # Example 

    I = [('C1', 32), ('C2', 32), ('M', 48)]
    G = [('P', 16), ('FP', 4), ('M', 48)]
    A = [('Make S1',[('C1', 1),('M', 1)],[('S1', 1),('M', 1)]),('Make S2',[('C2', 1),('M', 1)],[('S2', 1),('M', 1)]),('Make P',[('S1', 1),('S2', 1),('M', 1)],[('P', 1),('M', 1)]),('Make FP',[('P', 4),('M', 1)],[('FP', 1),('M', 1)])]


    prove(I, G, A)


