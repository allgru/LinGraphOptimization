# This file contains Testscenarios on Patterns
#
# Author: Allan Grunert <a_grun07@uni-muenster.de>
#

import sys
sys.path.append("./RestPlanServe/graph/")
import graph
import clustering 
import measure
from datetime import datetime

def checkGrouping():
    # combine = clustering.CombineActionFormulae('distance')
    combine = clustering.CombineActionFormulae('distance',measure.BrayCurtisDissimilarity())
    #combine = clustering.CombineActionFormulae('distance',measure.CanberraDistanceFunction())
    #combine = clustering.CombineActionFormulae('distance',measure.ChebychevDistanceFunction())
    #combine = clustering.CombineActionFormulae('distance',measure.CorrelationDistanceFunction())
    #combine = clustering.CombineActionFormulae('distance',measure.CosineSimilarity())
    #combine = clustering.CombineActionFormulae('distance',measure.DiceDistanceFunction())
    #combine = clustering.CombineActionFormulae('distance',measure.EuclideanDistanceFunction())
    #combine = clustering.CombineActionFormulae('distance',measure.HammingDistanceFunction())
    #combine = clustering.CombineActionFormulae('distance',measure.JaccardDistanceFunction())
    #combine = clustering.CombineActionFormulae('distance',measure.JensenshannonDistanceFunction())
    #combine = clustering.CombineActionFormulae('distance',measure.Kulczyinski1DistanceFunction())
    #combine = clustering.CombineActionFormulae('distance',measure.ManhattanDistanceFunction())
    #combine = clustering.CombineActionFormulae('distance',measure.MinkowskiDistanceFunction())
    #combine = clustering.CombineActionFormulae('distance',measure.PearsonCorrelationPValue())
    #combine = clustering.CombineActionFormulae('distance',measure.RogerstanimotoDistanceFunction())
    #combine = clustering.CombineActionFormulae('distance',measure.RussellraoDistanceFunction())
    #combine = clustering.CombineActionFormulae('distance',measure.SokalmichenerDistanceFunction())
    #combine = clustering.CombineActionFormulae('distance',measure.SokalsneathDistanceFunction()) 
    #combine = clustering.CombineActionFormulae('distance',measure.SpearmanRankCorrelation())
    #combine = clustering.CombineActionFormulae('distance',measure.SQEuclidDistanceFunction())
    #combine = clustering.CombineActionFormulae('distance',measure.WassersteinDistanceFunction())
    #combine = clustering.CombineActionFormulae('distance',measure.YuleDistanceFunction())
    

    grph = graph.Graph()

    groupingtype = 4
    
    # 1 sukzessiv
    if groupingtype == 1:
        A = [
            ('A',[('A', 1),('B', 1)],[('C', 1),('D', 1)]),
            ('C',[('C', 1),('D', 1)],[('E', 1),('F', 1)]),
            ('E',[('E', 1),('F', 1)],[('G', 1),('H', 1)]),
            ('G',[('G', 1),('H', 1)],[('I', 1),('J', 1)])]

    # 2 sukzessiv mit Überlappung
    if groupingtype == 2:
        A = [
            ('A',[('A', 1),('B', 1)],[('C', 1),('D', 1)]),
            ('C',[('C', 1),('D', 1)],[('E', 1),('F', 1)]),
            ('E',[('E', 1),('F', 1),('C',1),('D',1)],[('G', 1),('H', 1)]),
            ('G',[('G', 1),('H', 1),('E', 1),('F', 1)],[('I', 1),('J', 1)])]
    # A = [('Make S1',[('C1', 1),('M', 1)],[('S1', 1),('M', 1)]),('Make S2',[('C2', 1),('M', 1)],[('S2', 1),('M', 1)]),('Make P',[('S1', 1),('S2', 1),('M', 1)],[('P', 1),('M', 1)]),('Make FP',[('P', 4),('M', 1)],[('FP', 1),('M', 1)])]
    if groupingtype == 3:
        A = [
            ('A',[('A', 1),('B', 1)],[('C', 1),('D', 1)]),
            ('C',[('C', 1),('D', 1),('G', 1),('H', 1)],[('E', 1),('F', 1)]),
            ('E',[('E', 1),('F', 1),('C',1),('D',1)],[('G', 1),('H', 1)]),
            ('G',[('G', 1),('H', 1),('E', 1),('F', 1)],[('I', 1),('J', 1)])]

    if groupingtype == 4:
        # 3 Überlappung innerhalb der Gruppe
        A = [('Make S1',[('C1', 1),('M', 1)],[('S1', 1),('M', 1)]),('Make S2',[('C2', 1),('M', 1)],[('S2', 1),('M', 1)]),('Make P',[('S1', 1),('S2', 1),('M', 1)],[('P', 1),('M', 1)]),('Make FP',[('P', 4),('M', 1)],[('FP', 1),('M', 1)])]

    grph.addShortToLongFormActionFormulas(A)
    persistentResources = combine.getPersistentResources(grph.ActionFormulas)
    groups = combine.groupActionFormulas(grph.ActionFormulas, persistentResources)
    for a in grph.ActionFormulas:
        print(a.actionName,':','pre.',a.effects,'eff.',a.preconditions)
    for l in groups:
        print(list(map(lambda x: x.actionName,l)))

    comb = combine.combine(grph.ActionFormulas)

    for c in comb:
        print(c.actionName,':','pre.',c.effects,'eff.',c.preconditions)

def testJsonLoading():
    filename = "output\\<Please enter file name here>"
    fileObject = open( filename, "r" )
    JsonStr = fileObject.read()
    fileObject.close()

    print( JsonStr )
    print( "---" )

    grph = graph.Graph()
    grph.fromJson(JsonStr)

    filename = '.\\output\\lingraphOutputtest' + str( datetime.now() ).replace(":",".") + ".json"
    fileObject = open( filename, mode="w" )
    fileObject.write( grph.toJson() )
    fileObject.close()

    print( grph.toJson() )

def testCombine():
    # combine = CombineActionFormulae()
    parameters = {}
    parameters['combineddistance'] = 0.5
    combine =  clustering.CombineActionFormulae('distance',measure.BrayCurtisDissimilarity())
    #combine = CombineActionFormulae('distance', meassure.ChebychevMeassure())
    #combine = CombineActionFormulae('distance',meassure.CosineSimilarityMeassure()) 
    #combine = CombineActionFormulae('distance',meassure.EuclideanDistanceMeassure())
    # combine = CombineActionFormulae('distance',meassure.ManhattanDistanceMeassure())
    # combine = CombineActionFormulae('distance',meassure.MinkowskiDistanceMeassure())
    # combine = CombineActionFormulae('distance',meassure.PearsonCorrelationCoefficientMeassure())
    # combine = CombineActionFormulae('distance',meassure.SpearmanRankCorrelationMeassure())
    # combine = CombineActionFormulae('distance',meassure.HammingDistanceMeassure())
    # combine = CombineActionFormulae('distance',meassure.MahalanobisDistanceMeassure())  # Mahalobis needs many observations, not for pair wise
    # combine = CombineActionFormulae('distance',meassure.KLDivergenceMeassure()) # not applicable??
    # combine = CombineActionFormulae('distance',meassure.CanberraDistanceMeassure())
    # combine = CombineActionFormulae('distance',meassure.WassersteinDistanceMeassure()) # TODO: Devide by zero error
    # combine = CombineActionFormulae('distance',meassure.CorrelationDistanceMeassure()) 
    # combine = CombineActionFormulae('distance',meassure.CzekanowskiDiceCoeeficientMeassure())
    # combine = CombineActionFormulae('distance',meassure.BrayCuritsDissimilarityMeassure())
    # combine = CombineActionFormulae('distance',meassure.JensenshannonMeassure())
    # combine = CombineActionFormulae('distance',meassure.NormalizedCompressionDistanceMeassure()) # <- not implemented
    # combine = CombineActionFormulae('distance',meassure.SEuclidMeassure()) # TODO: not working
    # combine = CombineActionFormulae('distance',meassure.SQEuclidMeassure()) 
    # combine = CombineActionFormulae('distance',meassure.RogerstanimotoMeassure())
    # combine = CombineActionFormulae('distance',meassure.JaccardMeassure())
    # combine = CombineActionFormulae('distance',meassure.Kulczyinski1Meassure())
    # combine = CombineActionFormulae('distance',meassure.RussellraoMeassure())
    # combine = CombineActionFormulae('distance',meassure.SokalmichenerMeassure())
    # combine = CombineActionFormulae('distance',meassure.SokalsneathMeassure())
    # combine = CombineActionFormulae('distance',meassure.YuleMeassure())
    # combine = CombineActionFormulae('distance',meassure.HaversineMeassure()) # not working
    # combine = CombineActionFormulae('distance',meassure.MatchingDistance()) # not working

    #combine.setParameters(parameters)
    #combine = None
    # combine = 
    # prove(I, G, A, False, combine)
    # testPatterns(6)
    # loopTest(2)

    # checkGrouping()
    #pass

    # combine = clustering.CombineActionFormulae('distance',measure.BrayCurtisDissimilarity())

    grph = graph.Graph()

    groupingtype = 3
    
    # 1 sukzessiv
    if groupingtype == 1:
        A = [
            ('A',[('A', 1),('B', 1)],[('C', 1),('D', 1)]),
            ('C',[('C', 1),('D', 1)],[('E', 1),('F', 1)]),
            ('E',[('E', 1),('F', 1)],[('G', 1),('H', 1)]),
            ('G',[('G', 1),('H', 1)],[('I', 1),('J', 1)])]

    # 2 sukzessiv mit Überlappung
    if groupingtype == 2:
        A = [
            ('A',[('A', 1),('B', 1)],[('C', 1),('D', 1)]),
            ('C',[('C', 1),('D', 1)],[('E', 1),('F', 1)]),
            ('E',[('E', 1),('F', 1),('C',1),('D',1)],[('G', 1),('H', 1)]),
            ('G',[('G', 1),('H', 1),('E', 1),('F', 1)],[('I', 1),('J', 1)])]
    # A = [('Make S1',[('C1', 1),('M', 1)],[('S1', 1),('M', 1)]),('Make S2',[('C2', 1),('M', 1)],[('S2', 1),('M', 1)]),('Make P',[('S1', 1),('S2', 1),('M', 1)],[('P', 1),('M', 1)]),('Make FP',[('P', 4),('M', 1)],[('FP', 1),('M', 1)])]
    if groupingtype == 3:
        A = [
            ('A',[('A', 1),('B', 1)],[('C', 1),('D', 1)]),
            ('C',[('C', 1),('D', 1),('G', 1),('H', 1)],[('E', 1),('F', 1)]),
            ('E',[('E', 1),('F', 1),('C',1),('D',1)],[('G', 1),('H', 1)]),
            ('G',[('G', 1),('H', 1),('E', 1),('F', 1)],[('I', 1),('J', 1)])]

    # 3 Überlappung innerhalb der Gruppe
    # A = [('Make S1',[('C1', 1),('M', 1)],[('S1', 1),('M', 1)]),('Make S2',[('C2', 1),('M', 1)],[('S2', 1),('M', 1)]),('Make P',[('S1', 1),('S2', 1),('M', 1)],[('P', 1),('M', 1)]),('Make FP',[('P', 4),('M', 1)],[('FP', 1),('M', 1)])]

    grph.addShortToLongFormActionFormulas(A)
    persistentResources = combine.getPersistentResources(grph.ActionFormulas)
    groups = combine.groupActionFormulas(grph.ActionFormulas, persistentResources)
    for a in grph.ActionFormulas:
        print(a.actionName,':','pre.',a.effects,'eff.',a.preconditions)
    for l in groups:
        print(list(map(lambda x: x.actionName,l)))

    comb = combine.combine(grph.ActionFormulas)

    for c in comb:
        print(c.actionName,':','pre.',c.effects,'eff.',c.preconditions)
        #print(list(map(lambda x: x.actionName,c)))


def testPruning():
        # Without optimisation
    #for i in range(5):
    #        graph = LinGraph()
    #        graph, result = examples.paperExample( 2 )
   
   
#    p = [optimisation.TopPercentPruning(),optimisation.BottomPercentPruning(), optimisation.MiddlePercentPruning(), optimisation.OuterPercentPruning()]
#    o = [optimisation.MaxWeightedOptimisation(), optimisation.MinWeightedOptimisation(), optimisation.MeanWeightedValueOptimisation(), optimisation.MedianWeightedValueOptimisation(), optimisation.RandomWeightedValueOptimisation()] 
    #pruning.setPercent(20)
#    print('--------------------------------')
#    for oe in o:
#        for pe in p:
#            for percent in range(5,30,5):
#                if pe != None:
#                    pe.setPercent(percent)
#                print(oe.__class__, pe.__class__, percent)
#                print('--------------------------------')
#                for i in range(5):
#                    graph = LinGraph()
#                    graph, result = examples.paperExample( 2, None, None, oe, pe)
    pass

if __name__ == '__main__':
    checkGrouping()