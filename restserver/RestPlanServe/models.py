from django.db import models
from django.forms import ModelForm
from RestPlanServe.graph.graph import prove, output_contents
from RestPlanServe.graph.clustering import CombineActionFormulae
from RestPlanServe.graph import measure
from RestPlanServe.graph import optimisation
import os

class GraphInterface( models.Model ):
    """
        Model for the Interface
    """
    class Meta:
        managed = False

    def __init__( self, *args, **kwargs ):
        super( GraphInterface, self ).__init__( *args, **kwargs )
class GraphInterfaceForm( ModelForm ):
    """
        Model to run LinGraph algorithms
    """
    graph_output =''
    links = []

    def __init__( self, *args, **kwargs ):
        super( GraphInterfaceForm, self).__init__( *args, **kwargs )
        self.links = sorted( os.listdir( "output" ), reverse=True )

    def runGraph( self, input, algorithm, reverse, action_combine, distanceFunction, similarityThreshold, mergeTechnique, strWeightingMethod, pruning, strPruningMethod, pruningPercentage, value_boundary  ):
        """
            Run LnGraph algorithm

            Parameters
            ----------
                input : str
                    Input graph in the form of strings
                algorithm : str
                    Name of the LnGraph algorithm
                reverse : str
                    Boolean indicating whether the algorithm should run in reverse mode
                action_combine : str
                    Name of the method to combine action formulae
                combination : str
                    Name of the distance function to use for combining
                value_boundary : float
                    Value boundary for clustering
        """
        proveInput = input.splitlines()
        self.graph_output = str( len( proveInput ) )
        if ( len( proveInput ) >= 3 ):
            I = eval( proveInput[0] )
            G = eval( proveInput[1] )
            A = eval( proveInput[2] )
            combine = None
            
            if ( reverse == 'True' ):
                bool_reverse = True
            else:
                bool_reverse = False

            if action_combine == "1":
                if distanceFunction == 'simple':
                    combine = CombineActionFormulae( 'simple' , None, mergeTechnique) # Combination without distance functions
                elif distanceFunction == 'braycurtis': 
                    combine = CombineActionFormulae( 'distance', measure.BrayCurtisDissimilarity(), mergeTechnique )
                elif distanceFunction == 'canberra':
                    combine = CombineActionFormulae( 'distance', measure.CanberraDistanceFunction(), mergeTechnique )
                elif distanceFunction == 'chebychev': 
                    combine = CombineActionFormulae( 'distance', measure.ChebychevDistanceFunction(), mergeTechnique )
                elif distanceFunction == 'correlation': 
                    combine = CombineActionFormulae( 'distance', measure.CorrelationDistanceFunction(), mergeTechnique )
                elif distanceFunction == 'cosine': 
                    combine = CombineActionFormulae( 'distance', measure.CosineSimilarity(), mergeTechnique )
                elif distanceFunction == 'dice': 
                    combine = CombineActionFormulae( 'distance', measure.DiceDistanceFunction(), mergeTechnique )
                elif distanceFunction == 'euclidean': 
                    combine = CombineActionFormulae( 'distance', measure.EuclideanDistanceFunction(), mergeTechnique )
                elif distanceFunction == 'hamming': 
                    combine = CombineActionFormulae( 'distance', measure.HammingDistanceFunction(), mergeTechnique )
                elif distanceFunction == 'jaccard': 
                    combine = CombineActionFormulae( 'distance', measure.JaccardDistanceFunction(), mergeTechnique )
                elif distanceFunction == 'jensenshannon':  
                    combine = CombineActionFormulae( 'distance', measure.JensenshannonDistanceFunction(), mergeTechnique )
                elif distanceFunction == 'kulczyinski1': 
                    combine = CombineActionFormulae( 'distance', measure.Kulczyinski1DistanceFunction(), mergeTechnique )
                elif distanceFunction == 'manhattan': 
                    combine = CombineActionFormulae( 'distance', measure.ManhattanDistanceFunction(), mergeTechnique )
                elif distanceFunction == 'minkowski': 
                    combine = CombineActionFormulae( 'distance', measure.MinkowskiDistanceFunction(), mergeTechnique )
                elif distanceFunction == 'pearson': 
                    combine = CombineActionFormulae( 'distance', measure.PearsonCorrelationPValue(), mergeTechnique )
                elif distanceFunction == 'rogertanimoto': 
                    combine = CombineActionFormulae( 'distance', measure.RogerstanimotoDistanceFunction(), mergeTechnique )
                elif distanceFunction == 'russelrao': 
                    combine = CombineActionFormulae( 'distance', measure.RussellraoDistanceFunction(), mergeTechnique )
                elif distanceFunction == 'sokalmichener': 
                    combine = CombineActionFormulae( 'distance', measure.SokalmichenerDistanceFunction(), mergeTechnique )
                elif distanceFunction == 'sokalsneath': 
                    combine = CombineActionFormulae( 'distance', measure.SokalsneathDistanceFunction(), mergeTechnique )  
                elif distanceFunction == 'spearman': 
                    combine = CombineActionFormulae( 'distance', measure.SpearmanRankCorrelation(), mergeTechnique )
                elif distanceFunction == 'sqeuclid': 
                    combine = CombineActionFormulae( 'distance', measure.SQEuclidDistanceFunction(), mergeTechnique )
                elif distanceFunction == 'wasserstein': 
                    combine = CombineActionFormulae( 'distance', measure.WassersteinDistanceFunction(), mergeTechnique )
                elif distanceFunction == 'yule': 
                    combine = CombineActionFormulae( 'distance', measure.YuleDistanceFunction(), mergeTechnique )
            
            if combine != None and mergeTechnique != None:
                combine.groupingType = mergeTechnique
            
            if combine != None and similarityThreshold != None:
                combine.threshold = float( similarityThreshold )

            weightingMethod = None
            pruningMethod = None 

            if int(pruning) == 1:
                if strWeightingMethod == "random":
                        weightingMethod = optimisation.RandomWeightedValueOptimization()
                elif strWeightingMethod == "max":
                        weightingMethod = optimisation.MaxWeightedValueOptimization()
                elif strWeightingMethod == "min":
                        weightingMethod = optimisation.MinWeightedValueOptimization()
                elif strWeightingMethod == "median": 
                        weightingMethod = optimisation.MedianWeightedValueOptimization()
                elif strWeightingMethod == "mean":
                        weightingMethod = optimisation.MeanWeightedValueOptimization()

                if strPruningMethod == "random":
                    pruningMethod = optimisation.RandomPercentPruning()
                elif strPruningMethod == "top":
                    pruningMethod = optimisation.TopPercentPruning()
                elif strPruningMethod == "bottom":
                    pruningMethod = optimisation.BottomPercentPruning()
                elif strPruningMethod == "outer":
                    pruningMethod = optimisation.OuterPercentPruning()
                elif strPruningMethod == "middle":
                    pruningMethod = optimisation.MiddlePercentPruning()

                    pruningMethod.setPercent(pruningPercentage)

            prove( I, G, A, bool_reverse, combine, weightingMethod, pruningMethod, value_boundary )
            self.graph_output = "\n".join( output_contents )
            
            if combine != None:
                self.graph_output =  "\n".join( combine.output_contents ) + "\n" + self.graph_output
            
            if pruning == 1:
                self.graph_output +=  "\n" + "\n".join( weightingMethod.output_contents ) 
                self.graph_output +=  "\n" + "\n".join( pruningMethod.output_contents )

        # Create list of generated files
        self.links = sorted( os.listdir( "output" ), reverse=True )

    class Meta:
        model = GraphInterface
        fields = "__all__"

class ShowGraph( models.Model ):
    """
        Model for Output
    """
    class Meta:
        managed = False

    def __init__ ( self, *args, **kwargs ):
        super( ShowGraph, self ).__init__( *args, **kwargs )


class ShowGraphForm( ModelForm ):
    """
        Form Model for Output
    """    
    url = ''

    def __init__( self, *args, **kwargs ):
        super( ShowGraphForm, self ).__init__( *args, **kwargs )

    class Meta:
        model = ShowGraph
        fields = "__all__"
