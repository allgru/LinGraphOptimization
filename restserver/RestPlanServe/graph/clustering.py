# This file contains a method for grouping and merging action formulas of the LinGraph planner
#
# Author: Allan Grunert <a_grun07@uni-muenster.de>
# Version: 1.0
import sys
import copy
sys.path.append("./RestPlanServe/graph/") # Ensure path is found, if run from restserver directory
from measure import SimilarityFunction

class CombineActionFormulae():
    """Combine to Action Nodes into one Node.

    Parameters
    ..........
      combineType: Type 
      distanceFunction: Function to calculate distance between action formulas (default: None)
      groupByFunction

    """
    def __init__( self, combineType = 'simple', distanceFunction = None, groupingType = 'standard' ):
        self.combineType = combineType
        self.distanceFunction = distanceFunction
        self.groupingType = groupingType
        self.pseudoResourceCounter = 0
        self.threshold = 0.8
        self.output_contents = []


    def printContents( self, *args ):
            print( *args )
            self.output_contents.append( " ".join( map( str, args ) ) )

    def combine( self, actionFormulae ):
        """
        Method for combining action formulae

        Parameter
        ---------
            actionFormulae : array of action formulae 
                action formulae to be combined

        Return
        ......
            array of action formulae
                Array of newly combined action formulae
        """
        self.printContents("----------------")
        self.printContents("Start Clustering")
        self.printContents("----------------")


        if ( self.combineType == 'simple'): # no distance function applied
            self.printContents('simple->')
            return self.combineSimple( actionFormulae ) # distance function applied
        if ( self.combineType == 'distance' ):
            self.printContents('distance')
            return self.combineWithDistanceFunction( actionFormulae )

    def combineSimple( self, actionFormulae ):
        """ combine action formulars with no dependencies 

        Args:
            actionFormulae (ActionFormula): Array of action formulars to be combined

        Returns:
            array of ActionFormula: Combined Actionsformulars
        """
        dependency = []
        for actionFormula in actionFormulae:
            for precondition in actionFormula.preconditions:
                # don't check Gamma-Reources
                skip = False
                # check if there exists a dependency from other action formula
                for effect in actionFormula.effects:
                    if effect[ 'name' ] == precondition[ 'name' ] and effect[ 'value' ] == precondition[ 'value' ]:
                        skip = True # There is no dependency precondition == effect
                        break

                if not skip: # if no persistent resource
                    for actionFormula2 in actionFormulae:
                        if actionFormula2.actionName != actionFormula.actionName:
                            for effect in actionFormula2.effects:
                                if precondition[ 'name' ] == effect[ 'name' ]:
                                    dependency.append( actionFormula.actionName )
        combine = []
        for actionFormula in actionFormulae:
            if not actionFormula.actionName in dependency:
                combine.append( actionFormula )

        # crearte new Action
        if ( len( combine ) > 0 ):
            newActionFormula = self.combineActionFormula( combine )
            actionFormulae.append( newActionFormula )
            self.printContents( "Combined Action formula", newActionFormula.actionName )
            
        # remove Actions
        for ActionFormula in combine:
            actionFormulae.remove( ActionFormula )

        return actionFormulae


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

    def combineWithDistanceFunction( self, actionFormulae ):
        """
            Combine action Formulae with distance functions 

            Parameter
            ---------
                actionFormulae : array of action formulae
                    action formulae to combine
        """

        # Set similarity function and set its distance function
        simFunc = SimilarityFunction()
        simFunc.setDistanceFunction(self.distanceFunction)

        combinations = []
        # Create resource vector of all resouces
        resourceVector = self.getResourceVector( actionFormulae )

        # Create groups of action formulae
        combineGroups = self.groupactionFormulae( actionFormulae, self.getPersistentResources(actionFormulae ) )

        # iterate through each group
        for combineGroup in combineGroups:
            actionFormulaeVectorized = []
            for ActionFormula in combineGroup:
                # generate vector with all resources for all action Formulaes # 0 = name, 1 = precondition, 2 = effect
                actionFormulaeVectorized.append( ( ActionFormula.actionName, self.generateResourceVector( resourceVector, ActionFormula.preconditions ), self.generateResourceVector( resourceVector, ActionFormula.effects ) ) )

            # Iterate through action formulae with full vector of preconditions and effects # iterate list with two loops
            for ActionFormula1 in actionFormulaeVectorized:
                for ActionFormula2 in actionFormulaeVectorized:
                    if ActionFormula1[ 0 ] != ActionFormula2[ 0 ]: # action is not the same
                        similarity = simFunc.relative( ActionFormula1[ 1 ], ActionFormula2[ 1 ] ) # check similarity of precondition vectors @ 1, 0 is name, 2 is effect

                        self.printContents("Similarity:",similarity,">",self.threshold,"?")
                        if  similarity > self.threshold: # similarity function result higher than threshold
                            self.printContents("yes")
                            combinations.append( ( ActionFormula1[ 0 ], ActionFormula2[ 0 ] ) )
        
        newCombinations = []
        for combination in combinations:
            newCombination = []
            for combination2 in combinations:
                if not combination == combination2: # not the same
                    if not combination2[ 0 ] in newCombination:
                        newCombination.append( combination2[ 0 ] ) # add first
                    if not combination2[ 1 ] in newCombination:
                        newCombination.append( combination2[ 1 ] ) # add second action formula
            newCombinations.append( copy.deepcopy( newCombination ) )


        for combination in newCombinations:
            combine = []
            for actionFormula in actionFormulae:
                if actionFormula.actionName in combination:
                    combine.append( actionFormula )

            # crearte new Action
            if ( len( combine ) > 0 ):
                if self.groupingType == 'partial': # if partial grouping different creation process
                    combinedActionFormulae = self.combinePartialactionFormulae( combine )
                    for c in combinedActionFormulae:
                        actionFormulae.append( c )
                        self.printContents( "Combined Action formula", c.actionName )
                else:
                    newActionFormula = self.combineActionFormula( combine )
                    actionFormulae.append( newActionFormula )
                    self.printContents( "Combined Action formula", newActionFormula.actionName )

            # remove Actions
            for ActionFormula in combine:
                actionFormulae.remove( ActionFormula )
        
        self.output_contents += simFunc.output_contents # add output of similarity function

        return actionFormulae

    def combineActionFormula( self, actionFormulae ):
        """"
            Combine action formulae
            n actionFormulae action formulae that have been grouped and should be merged together

            Parameter
            ..........
                actionFormulae : array of action formulae
                    action formulae to be combined
        """
        from graph import ActionFormula

        # create a new action formula with no name
        newActionFormula = ActionFormula("")
        for actionFormula in actionFormulae:
            if newActionFormula.actionName == "": # if there is no name, add name of first aciton formula
                newActionFormula.actionName = actionFormula.actionName
            else: # add name of action formula that will be merged with an and
                newActionFormula.actionName += " and " + actionFormula.actionName

            # if preconditions already exist, check if precondition has already been added
            # if it exists, add the resource value
            # if it does not exist add the precondition
            if len( newActionFormula.preconditions ) > 0:
                preconditionFound = False
                for precondition in actionFormula.preconditions:
                    for precondition2 in newActionFormula.preconditions:
                        if precondition[ 'name' ] == precondition2[ 'name' ]:
                            preconditionFound = True
                            precondition2[ 'value' ] += precondition[ 'value' ]
                            break
                    if not preconditionFound:
                        newActionFormula.preconditions.append( precondition )
            else: # copy the precondition of the action formula selected
                newActionFormula.preconditions = copy.deepcopy( actionFormula.preconditions )

            # check if new action formula already has effects
            # if it exists, add the resource value
            # if it does not exist, add the effect
            if len(newActionFormula.effects) > 0:
                for effect in actionFormula.effects:
                    effectFound = False
                    for effect2 in newActionFormula.effects:
                        if effect[ 'name' ] == effect2[ 'name' ]:
                            effectFound = True
                            effect2[ 'value' ] += effect[ 'value' ]
                            break
                    if not effectFound:
                        newActionFormula.effects.append( copy.deepcopy( effect ) )
            else: # copy the effect of the action formula selected
                newActionFormula.effects = copy.deepcopy( actionFormula.effects )
            
        return newActionFormula


    def setParameters( self, parameters ):
        self.parameters = parameters


    def getResourceVector( self, actionFormulae ):
        """
            change to preconditions / effects to vector
        """
        resourceNames = []
        for ActionFormula in actionFormulae:
            for precondition in ActionFormula.preconditions:
                if not precondition[ 'name' ] in resourceNames:
                    resourceNames.append( precondition[ 'name' ] )
            for effect in ActionFormula.effects:
                if not effect[ 'name' ] in resourceNames:
                    resourceNames.append( effect[ 'name' ] )
        return resourceNames

    def getResourcePreconditions( self, actionFormulae ):
        """
            change to preconditions / effects to vector
        """
        resourceNames = []
        for ActionFormula in actionFormulae:
            for precondition in ActionFormula.preconditions:
                if not precondition[ 'name' ] in resourceNames:
                    resourceNames.append( precondition[ 'name' ] )
        return resourceNames

    def generateResourceVector( self, resourceVector, preconditions_or_effects ):
        """
            Generate a resource vector from effects

            Parameter
            ..........
                resourceVector : array of resource names
                    resource names to be included in the vector
                preconditions_or_effects : array of preconditions or effects
                    preconditions or effects to be included in the vector

            Returns
            ..........
                array of resource values
                    resource values corresponding to the resource names in the input vector
        """
        vector = []

        i = 0
        # iterate through all resource vectors
        for resource in resourceVector:
            i += 1
            resourceFound = False
            for item in preconditions_or_effects:
                if item[ 'name' ] == resource: # if item from preconditions or effects found add value
                    vector.append( item[ 'value' ])
                    resourceFound = True
                    break
            if not resourceFound: # if no resource found empty
                vector.append( 0 )
        return vector
    
    def combinePartialactionFormulae(self, actionFormulae):
        """
            we need to create three #(action formulae)+1 action formulae

            new action formulae preconditions + become one - different (=3 differeren new action formulae)
                        o-------
            +++++++++o
            +++++++++p
                        p-------
            Return
            ------
                array of action formulae
                    action formulae partly fully combined and dependent aciton formulae
        """
        self.pseudoResourceCounter += 1
        from graph import ActionFormula

        resourceVectorPrecondition = self.getResourceVector( actionFormulae )
        resourcePreconditionDict = {}

        combineResourceNames = []
        newActionFormulae = []

        # count all occurances of precondition names
        for a in actionFormulae:
            for precondition in a.preconditions:
                if precondition["name"] in resourcePreconditionDict.keys():
                    resourcePreconditionDict[ precondition["name"] ] += 1
                else:
                    resourcePreconditionDict[ precondition["name"] ] = 1
        
        # add all precondition names that are present in all actionFormulae
        for preconditionName in resourceVectorPrecondition:
            if preconditionName in resourcePreconditionDict.keys() and resourcePreconditionDict[preconditionName] == len(actionFormulae):
                combineResourceNames.append(preconditionName)

        # create a new action formula with no name
        newActionFormula = ActionFormula("")
        for p in combineResourceNames:
            newActionFormula.preconditions.append({"name": p, "value": 0})
        differentActionFormulae = []
        for i in range(len(actionFormulae)):
            differentActionFormulae.append(ActionFormula(""))

        
        for i in range(len(actionFormulae)):
            for p in actionFormulae[i].preconditions:
                # add all that can be combined to new action formula
                if p["name"] in combineResourceNames:
                    if actionFormulae[i].actionName not in newActionFormula.actionName:
                        if newActionFormula.actionName == "":
                            newActionFormula.actionName = actionFormulae[i].actionName
                        else:
                            newActionFormula.actionName += "," + actionFormulae[i].actionName
                    for j in range(len(newActionFormula.preconditions)):
                        if newActionFormula.preconditions[j]['name'] == p["name"]:
                            newActionFormula.preconditions[j]['value'] += p['value']
                            break
                else:
                    # otherwise add it to one of the differenting action formulae
                    if differentActionFormulae[i].actionName == "":
                        differentActionFormulae[i].actionName = actionFormulae[i].actionName + " (part)"
                    differentActionFormulae[i].preconditions.append(copy.deepcopy(p))
                    if differentActionFormulae[i].effects == []:
                        differentActionFormulae[i].effects = copy.deepcopy(actionFormulae[i].effects)

        # remove all action Formulas that have no name
        for a in actionFormulae:
                if a.actionName == "":
                    differentActionFormulae.remove(a)
        
        if len(differentActionFormulae) == 0:
            # go through each action formula and add effect
            # add all effects to new action
            # no pseudoprecodition or effect necessary
            for a in actionFormulae:
                for effect in a.effects:
                    # add name to new action
                    effectFound = False
                    for effect2 in newActionFormula.effects:
                        if effect2['name'] == effect['name']:
                            effectFound = True
                            effect2['value'] += effect['value']
                            break
                    if (not effectFound):
                        newActionFormula.effects.append(copy.deepcopy(effect))
        else:
            # Add pseudo ressource as effect of new action formulae and as precondition for differenting partial action formulae
            pseudoResource              = {'name': 'psRes' + str(self.pseudoResourceCounter), 'value': len(differentActionFormulae)}
            pseudoResourcePrecondition  = {'name': 'psRes' + str(self.pseudoResourceCounter), 'value': 1}
            # add new pesudo ressource as single effect to new action formula
            newActionFormula.effects.append(copy.deepcopy(pseudoResource))
            # add new pseudo ressource as precondition to each different action formula precondition
            for d in differentActionFormulae:
                d.preconditions.append(copy.deepcopy(pseudoResourcePrecondition)) 

        # add Combined action formula
        newActionFormulae.append( newActionFormula )
        # add differing action formula accessible through pseudo resource
        for da in differentActionFormulae:
            newActionFormulae.append( da )

        return newActionFormulae

    def groupactionFormulae( self, actionFormulae, persistentResources ):
        """
            Group action formulae based on their dependencies.

            Parameter
            ..........
                actionFormulae : list of ActionFormula
                    action formulae to be grouped
                persistentResources : list of string
                    persistent resources that should not be grouped with other action formulae
        """
        ActionFormulaListAdded = []
        groups = []
        groups.append([])
        for a in actionFormulae:
            ActionFormulaDependent = False
            for b in actionFormulae:
                # not same action
                if a.actionName != b.actionName:
                    for precondition in a.preconditions: # 
                        if not precondition['name'] in persistentResources:
                            for effect in b.effects:
                                if effect['name'] == precondition['name']: # dependent
                                    ActionFormulaDependent = True
                                    break
                if ActionFormulaDependent:
                    break
            if not ActionFormulaDependent: 
                ActionFormulaListAdded.append(a)
                groups[0].append(a)

        index = 0
        if len(groups[0])==0:
            print("error: action formulars have logic mistake")
            exit()

        while(len(ActionFormulaListAdded) < len(actionFormulae) and len(groups[index])>0):
            groups.append([])

            for a in actionFormulae:
                followGroup = False # effect in precondition
                otherConnection = False

                if not a in ActionFormulaListAdded:
                    for b in groups[index]:
                        for effect in b.effects:
                            if not effect['name'] in persistentResources:
                                for precondition in a.preconditions:
                                    if not precondition['name'] in persistentResources:
                                        if precondition['name'] == effect['name']:
                                            followGroup = True

                    if followGroup:
                        for c in actionFormulae:
                            if not c in ActionFormulaListAdded or c in groups[index+1]: # Vorherige einbezogen
                                if c.actionName != a.actionName:
                                    for effect in c.effects:
                                        if not effect['name'] in persistentResources:
                                            for precondition in a.preconditions:
                                                if not precondition['name'] in persistentResources:
                                                    if precondition['name'] == effect['name']:
                                                        # prüfen, ob Gegenseitge Abhängigkeiten vorliegen
                                                        otherConnection = True

                    # only add action formulae if precondition can only be found in previous effects
                    if followGroup and not otherConnection:
                        groups[ index + 1 ].append(a)
                        ActionFormulaListAdded.append(a)

            index += 1

        if len(ActionFormulaListAdded) < len(actionFormulae):
            print("Error dependency on same level")

        return groups