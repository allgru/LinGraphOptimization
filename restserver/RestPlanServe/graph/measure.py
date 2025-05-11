# This file contains Classes of different distance functions and the similarity function
#
# Author: Allan Grunert <a_grun07@uni-muenster.de>
# Version: 1.0
import sys
sys.path.append("./RestPlanServe/graph/")

import numpy as np

from scipy.stats import pearsonr
from scipy.stats import spearmanr
from scipy.stats import wasserstein_distance

from scipy.spatial.distance import braycurtis
from scipy.spatial.distance import canberra
from scipy.spatial.distance import chebyshev
from scipy.spatial.distance import cityblock
from scipy.spatial.distance import cosine
from scipy.spatial.distance import dice
from scipy.spatial.distance import euclidean
from scipy.spatial.distance import hamming
from scipy.spatial.distance import jaccard
from scipy.spatial.distance import jensenshannon
from scipy.spatial.distance import kulczynski1
from scipy.spatial.distance import minkowski
from scipy.spatial.distance import rogerstanimoto
from scipy.spatial.distance import sqeuclidean
from scipy.spatial.distance import russellrao
from scipy.spatial.distance import correlation
from scipy.spatial.distance import sokalmichener
from scipy.spatial.distance import sokalsneath
from scipy.spatial.distance import yule



# Abstact class for distance functions
class DistanceFunction():
    def __init__( self ):
        pass
    
    # d is the function in which the (absolute) distance is calculated 
    def d(self, x, y):
        pass

# Class for calculating the similarity, uses a distance function to calculate the distance
class SimilarityFunction():
    """
    Class for calculating the similarity. It takes a distance function 
    for calculating the similarity.
    """
    def __init__( self ):
        self.distanceFunction = None
        self.output_contents = []

    def printContents(self, *args ):
        print( *args )
        self.output_contents.append( " ".join( map( str, args ) ) )

    def relative( self, x, y ):
        """
        calculate relative similarity 

        Parameters
            x : list of integers
                First precondition vector to be compared 
            y : list of integers
                Second precondition vector to be compared 

        Return
        ------
            float 
                Gives back relativ value beteen 0-1
        """
        # Output 
        self.printContents( "---------------------------------------------------------" )        
        self.printContents( "Calculate Similarity" )        
        self.printContents( "====================" )        
        self.printContents( "Input x:", x )         
        self.printContents( "Input y:", y )
        self.printContents( "Distance function class:", self.distanceFunction.__class__ )

        distance = self.distanceFunction.d( x, y ) 

        # Output distance calculation
        self.printContents( "Distance function calculated value:", distance)

        # Normalisation with similarity function
        similarity = 1 / ( 1 + distance )
        # Output similarity calculation
        self.printContents( "Calculated similarity value:", similarity )
        self.printContents( "---------------------------------------------------------" )        
        return similarity 
    
    def setDistanceFunction( self, distanceFunction ):
        self.distanceFunction = distanceFunction
    
    # gives back the absolute value calculated by the algorithm

# ----------------------------------------------------------------

class BrayCurtisDissimilarity( DistanceFunction ):
    """  Bray-Curtis distance
    sum_i ( | x_i - y_i |) / sum_i ( | x_i + y_i |)
    see https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.braycurtis.html#scipy.spatial.distance.braycurtis
    
    """
    def __init__( self ):
        pass
    
    # gives back the absolute value calculated by the algorithm
    def d( self, x, y ):
        """
            Calculate distance from two action formula vectors

            Parameter
            ---------
                x : list of int
                    Precondition vector of action formula 1
                y : list of int
                    Precondition vector of action formula 2

            Return
            ------
                float
                    distance between action formula vectors

        """

        return braycurtis( x, y )


class CanberraDistanceFunction( DistanceFunction ):
    """Canberra Distance
    sum_i (|x_i - y_i| / ( |x_i| + |y_i|)
    see https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.canberra.html
    """
    def __init__( self ):
        pass
    
    # gives back the absolute value calculated by the algorithm
    def d( self, x, y ):
        """
            Calculate distance from two action formula vectors

            Parameter
            ---------
                x : list of int
                    Precondition vector of action formula 1
                y : list of int
                    Precondition vector of action formula 2

            Return
            ------
                float
                    distance between action formula vectors

        """


        return canberra( x, y )

class ChebychevDistanceFunction( DistanceFunction ):
    """Chebyshev distance function
        max_i |x_i - y_i |
        see https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.chebyshev.html

        """
    def __init__( self ):
        pass

    def d( self, x, y ):
        return chebyshev(x,y)


class CorrelationDistanceFunction( DistanceFunction ):
    """Correlation distance function
    
        see https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.correlation.html#scipy.spatial.distance.correlation

    """
    def __init__( self ):
        pass
    
    # gives back the absolute value calculated by the algorithm
    def d( self, x, y ):
        """
            Calculate distance from two action formula vectors

            Parameter
            ---------
                x : list of int
                    Precondition vector of action formula 1
                y : list of int
                    Precondition vector of action formula 2

            Return
            ------
                float
                    distance between action formula vectors

        """


        return abs( correlation( x, y ) )

class CosineSimilarity( DistanceFunction ):
    """
        Cosine similarity function
        K(X, Y) = <X, Y> / (||X||*||Y||)
        see https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.cosine.html#scipy.spatial.distance.cosine
    """
    def __init__( self ):
        # super.__init__('cosine')
        pass
    
    # Override relative function as, we have a similarity
    def d( self, x, y ):
        """
            Calculate distance from two action formula vectors

            Parameter
            ---------
                x : list of int
                    Precondition vector of action formula 1
                y : list of int
                    Precondition vector of action formula 2

            Return
            ------
                float
                    distance between action formula vectors

        """


        return abs( cosine( x, y) ) 


class DiceDistanceFunction( DistanceFunction ):
    """
        Dice distance function
        see https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.dice.html
    """
    def __init__( self ):
        pass
    
    # gives back the absolute value calculated by the algorithm
    def d( self, x, y ):
        """
            Calculate distance from two action formula vectors

            Parameter
            ---------
                x : list of int
                    Precondition vector of action formula 1
                y : list of int
                    Precondition vector of action formula 2

            Return
            ------
                float
                    distance between action formula vectors

        """


        return abs( dice( x, y ) )

class EuclideanDistanceFunction( DistanceFunction ):
    """
    Euclidean distance function
    dist(x, y) = sqrt(dot(x, x) - 2 * dot(x, y) + dot(y, y))
    see https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.euclidean.html#scipy.spatial.distance.euclidean
    """
    def __init__(self):
        #super.__init__(self)
        pass
    
    # gives back the absolute value calculated by the algorithm
    def d( self, x, y ):
        """
            Calculate distance from two action formula vectors

            Parameter
            ---------
                x : list of int
                    Precondition vector of action formula 1
                y : list of int
                    Precondition vector of action formula 2

            Return
            ------
                float
                    distance between action formula vectors

        """


        return euclidean( x, y )
        #return np.sum( euclidean_distances( [x], [y] ) ) / len( x ) 

class HammingDistanceFunction( DistanceFunction ):
    """
        Hamming Distance ( n<>x is treated like 1 to 0 or 0 to 1 )
        see https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.hamming.html#scipy.spatial.distance.hamming
    """
    def __init__( self ):
        #super.__init__('hamming')
        pass
    # gives back the absolute value calculated by the algorithm
    def d( self, x, y ):
        """
            Calculate distance from two action formula vectors

            Parameter
            ---------
                x : list of int
                    Precondition vector of action formula 1
                y : list of int
                    Precondition vector of action formula 2

            Return
            ------
                float
                    distance between action formula vectors

        """


        return hamming( x, y ) 

class JaccardDistanceFunction( DistanceFunction ):
    """
    Jaccard Distance
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.jaccard.html#scipy.spatial.distance.jaccard
    """
    def __init__( self ):
        pass #super.__init__('jaccard')

    # gives back the absolute value calculated by the algorithm
    def d( self, x, y ):
        """
            Calculate distance from two action formula vectors

            Parameter
            ---------
                x : list of int
                    Precondition vector of action formula 1
                y : list of int
                    Precondition vector of action formula 2

            Return
            ------
                float
                    distance between action formula vectors

        """


        return jaccard( x, y )

class JensenshannonDistanceFunction( DistanceFunction ):
    """
        Jensen-Shannon Distance
        see https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.jensenshannon.html#scipy.spatial.distance.jensenshannon  
    """
    def __init__(self):
        pass
    
    # gives back the absolute value calculated by the algorithm
    def d( self, x, y ):
        """
            Calculate distance from two action formula vectors

            Parameter
            ---------
                x : list of int
                    Precondition vector of action formula 1
                y : list of int
                    Precondition vector of action formula 2

            Return
            ------
                float
                    distance between action formula vectors

        """


        return jensenshannon( x, y )

class Kulczyinski1DistanceFunction( DistanceFunction ): 
    """
        Kulczyinski 1 distance function

        # see https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.kulczynski1.html
    """
    def __init__( self ):
        pass # super.__init__('kulczynski1')

    # gives back the absolute value calculated by the algorithm
    def d( self, x, y ):
        """
            Calculate distance from two action formula vectors

            Parameter
            ---------
                x : list of int
                    Precondition vector of action formula 1
                y : list of int
                    Precondition vector of action formula 2

            Return
            ------
                float
                    distance between action formula vectors

        """


        return abs( kulczynski1( x, y ) )


class ManhattanDistanceFunction( DistanceFunction ):
    """
        Manhattan distance function
        L1 distances: sum_i( x_i - y_i)
        see https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.cityblock.html#scipy.spatial.distance.cityblock
    """
    def __init__( self ):
        #super.__init__()
        pass

    # gives back the absolute value calculated by the algorithm
    def d( self, x, y ):
        """
            Calculate distance from two action formula vectors

            Parameter
            ---------
                x : list of int
                    Precondition vector of action formula 1
                y : list of int
                    Precondition vector of action formula 2

            Return
            ------
                float
                    distance between action formula vectors

        """


        return cityblock( x, y)

class MinkowskiDistanceFunction( DistanceFunction ):
    """
        Minkowski distance function
        dist( x, y ) = ( sum_i( | x_i - y_i | ^ p ) ) ^ 1 / p
        see https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.minkowski.html
    """
    def __init__( self ):
        # super.__init__()
        self.p = 1.5
            
    # gives back the absolute value calculated by the algorithm
    def d( self, x, y ):
        """
            Calculate distance from two action formula vectors

            Parameter
            ---------
                x : list of int
                    Precondition vector of action formula 1
                y : list of int
                    Precondition vector of action formula 2

            Return
            ------
                float
                    distance between action formula vectors

        """


        return minkowski( x, y, self.p )
        
class PearsonCorrelationPValue( DistanceFunction ): # TODO: negative?
    """
        Pearson correlation p-value
        # TODO: test on p < 0.05 > 0.1 ?
        see https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.pearsonr.html 
    """
    def __init__( self ):
        #super.__init__()
        pass
    
    def d( self, x, y ):
        """
            Calculate distance from two action formula vectors

            Parameter
            ---------
                x : list of int
                    Precondition vector of action formula 1
                y : list of int
                    Precondition vector of action formula 2

            Return
            ------
                float
                    distance between action formula vectors

        """


        return pearsonr( x, y ).pvalue 

class RogerstanimotoDistanceFunction( DistanceFunction ): 
    """
        Rogers-Tanimoto distance
        see https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.rogerstanimoto.html
    """
    def __init__( self ):
        pass

    def d( self, x, y ):
        """
            Calculate distance from two action formula vectors

            Parameter
            ---------
                x : list of int
                    Precondition vector of action formula 1
                y : list of int
                    Precondition vector of action formula 2

            Return
            ------
                float
                    distance between action formula vectors

        """


        return abs( rogerstanimoto( x, y ) )

class RussellraoDistanceFunction( DistanceFunction ):
    """
    Russel-Rao distance function
    see https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.russellrao.html

    """
    def __init__( self ):
        pass #super.__init__('russellrao')

    # gives back the absolute value calculated by the algorithm
    def d( self, x, y ):
        """
            Calculate distance from two action formula vectors

            Parameter
            ---------
                x : list of int
                    Precondition vector of action formula 1
                y : list of int
                    Precondition vector of action formula 2

            Return
            ------
                float
                    distance between action formula vectors

        """


        return abs( russellrao( x, y ) )


class SokalmichenerDistanceFunction ( DistanceFunction ): 
    """
        Sokal-Michener distance function
        see https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.sokalmichener.html#scipy.spatial.distance.sokalmichener
    """
    def __init__(self):
        pass #super.__init__('sokalmichener')

    # gives back the absolute value calculated by the algorithm
    def d( self, x, y ):
        """
            Calculate distance from two action formula vectors

            Parameter
            ---------
                x : list of int
                    Precondition vector of action formula 1
                y : list of int
                    Precondition vector of action formula 2

            Return
            ------
                float
                    distance between action formula vectors

        """


        return abs( sokalmichener( x, y ) )

class SokalsneathDistanceFunction( DistanceFunction ): 
    """
        Sokal-Sneath    
        see https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.sokalsneath.html#scipy.spatial.distance.sokalsneath
    """
    def __init__(self):
        pass # super.__init__('sokalsneath')

    # gives back the absolute value calculated by the algorithm
    def d( self, x, y ):
        """
            Calculate distance from two action formula vectors

            Parameter
            ---------
                x : list of int
                    Precondition vector of action formula 1
                y : list of int
                    Precondition vector of action formula 2

            Return
            ------
                float
                    distance between action formula vectors

        """


        return abs( sokalsneath( x, y ) )

class SpearmanRankCorrelation( SimilarityFunction ):
    """
        Spearman rank correlation p-value
        TODO: test on p < 0.05 > 0.1 ?
        p value in Spearman rank correlation
        see scipy.stats.spearman
    """
    def __init__( self ):
        #super.__init__()
        pass
    
    # gives back the absolute value calculated by the algorithm
    def d( self, x, y ):
        """
            Calculate distance from two action formula vectors

            Parameter
            ---------
                x : list of int
                    Precondition vector of action formula 1
                y : list of int
                    Precondition vector of action formula 2

            Return
            ------
                float
                    distance between action formula vectors

        """


        return spearmanr( x, y ).pvalue


class SQEuclidDistanceFunction( DistanceFunction ):
    """
        Square Euclid distance function
        see https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.sqeuclidean.html
    """
    def __init__( self ):
        pass
    

    # gives back the absolute value calculated by the algorithm
    def d( self, x, y ):
        """
            Calculate distance from two action formula vectors

            Parameter
            ---------
                x : list of int
                    Precondition vector of action formula 1
                y : list of int
                    Precondition vector of action formula 2

            Return
            ------
                float
                    distance between action formula vectors

        """

        return sqeuclidean( x, y )

class WassersteinDistanceFunction( DistanceFunction ):
    """
        Wasserstein distance function
        see https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.wasserstein_distance.html
    """
    def __init__( self ):
        pass
        #super.__init__()
    
    # gives back the absolute value calculated by the algorithm
    def d( self, x, y ):
        """
            Calculate distance from two action formula vectors

            Parameter
            ---------
                x : list of int
                    Precondition vector of action formula 1
                y : list of int
                    Precondition vector of action formula 2

            Return
            ------
                float
                    distance between action formula vectors

        """


        return wasserstein_distance( x, y )

class YuleDistanceFunction( DistanceFunction ):
    """
        Yule distance function
        see https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.yule.html#scipy.spatial.distance.yule
    """
    def __init__( self ):
        pass # super.__init__('yule')

    # gives back the absolute value calculated by the algorithm
    def d( self, x, y ):
        """
            Calculate distance from two action formula vectors

            Parameter
            ---------
                x : list of int
                    Precondition vector of action formula 1
                y : list of int
                    Precondition vector of action formula 2

            Return
            ------
                float
                    distance between action formula vectors

        """


        return yule( x, y )