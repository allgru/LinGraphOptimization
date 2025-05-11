# LinGraph Examples for testing the algorithm
#
# Author: Allan Grunert <a_grun07@uni-muenster.de>
# Version: 1.0
#
#
import sys
sys.path.append("./RestPlanServe/graph/")

def testPC(number, reverse = False):
    """Different Examples for testing resource count
    """
    from graph import prove
    if (number==1): # Example 1
        I = [('C', 2), ('M', 2)]
        G = [('P', 1), ('M', 2), ('K', 1)]
        A = [('(C,M)->P',[('C', 1),('M', 1)],[('P', 1),('M', 1)]),('(C,M)->K',[('C', 1),('M', 1)],[('K', 1),('M', 1)])]
    elif (number==2): # Example 2
        I = [('C', 4), ('M', 4)]
        G = [('P', 2), ('M', 4), ('K', 2)]
        A = [('(C,M)->P',[('C', 1),('M', 1)],[('P', 1),('M', 1)]),('(C,M)->K',[('C', 1),('M', 1)],[('K', 1),('M', 1)])]
    elif (number==3): # Exanple 3
        I = [('C', 4), ('M', 2)]
        G = [('P', 2), ('M', 2), ('K', 2)]
        A = [('(C,M)->P',[('C', 2),('M', 2)],[('P', 2),('M', 2)]),('(C,M)->K',[('C', 1),('M', 1)],[('K', 1),('M', 1)])]
    elif (number==4): # Example 4
        I = [('C', 4), ('M', 2)]
        G = [('P', 2), ('M', 2), ('K', 2)]
        A = [('(C,M)->P',[('C', 1),('M', 1)],[('P', 1),('M', 1)]),('(C,M)->K',[('C', 1),('M', 1)],[('K', 1),('M', 1)])]

    return prove(I, G, A, reverse)


# ----------------------------------------------------------------------------------------------------------------------------------------
# The following examples are copied from the source code of Dr. Sita Kortik (fSearch_multiple_or-tools.py) and has been slightly modified.

    
# There are 2 arms(L,R), 2 rooms(A,B) and 2 balls(b1,b2)  
# def gripper():
    # Init = ['r_at_A','free_l','free_r','b1_at_A','b2_at_A']
    # Goal = ['b1_at_B', 'b2_at_B', 'r_at_B', 'free_l', 'free_r']
    # Rules = [('Move-A-B',['r_at_A'],['r_at_B']), ('Pick-b1-A-L',['b1_at_A','r_at_A','free_l'],['carry_b1_l', 'r_at_A']), ('Pick-b2-A-R',['b2_at_A','r_at_A','free_r'],['carry_b2_r','r_at_A']), ('Drop-b1-B-L',['carry_b1_l', 'r_at_B'],['b1_at_B','r_at_B','free_l']), ('Drop-b2-B-R',['carry_b2_r','r_at_B'],['b2_at_B','r_at_B','free_r'])]
    # return prove(Init, Goal, Rules, True)

#    Init = ['r_at_A','free_l','free_r','b1_at_A','b2_at_A']
#    Goal = ['b1_at_B', 'b2_at_A', 'r_at_B', 'free_l', 'free_r']
#    Rules = [('Move-A-B',['r_at_A'],['r_at_B']), ('Move-B-A',['r_at_B'],['r_at_A']), ('Pick-b1-A-L',['b1_at_A','r_at_A','free_l'],['carry_b1_l', 'r_at_A']), ('Pick-b2-A-R',['b2_at_A','r_at_A','free_r'],['carry_b2_r','r_at_A']), ('Drop-b1-B-L',['carry_b1_l', 'r_at_B'],['b1_at_B','r_at_B','free_l']), ('Drop-b2-B-R',['carry_b2_r','r_at_B'],['b2_at_B','r_at_B','free_r'])]
#    return prove(Init, Goal, Rules, True)

    
    # Init = ['r1','r2','r3']
    # Goal = ['k1', 'k2', 'k3']
    # Rules = [('Move-A-B',['r1'],['k1']), ('Move-B-A',['r2'],['k2']), ('Pick-b1-A-L',['r3'],['k3'])]
    # return prove(Init, Goal, Rules, True)

def blocksworld(number, reverse = False):
    from graph import prove
    if number == 1:
        I = [('empty', 1), ('clear_a', 1), ('ontable_a', 1)]
        G = [('hold_a', 1)]
        A = [('FT(a)',[('empty',1), ('ontable_a',1), ('clear_a',1)],[('hold_a',1)]), ('ON(a,b)',[('hold_a',1),('clear_b',1)],[('empty',1),('on_a_b',1),('clear_a',1)])]
    # elif number == 2:
    #     I = ['empty', 'clear_a', 'ontable_a', 'clear_b', 'ontable_b']
    #     G = ['empty', 'clear_a', 'on_a_b', 'ontable_b']
    #     A = [('FT(a)',['empty', 'ontable_a', 'clear_a'],['hold_a']), ('OT(a)',['hold_a'],['empty','ontable_a','clear_a']), ('ON(a,b)',['hold_a','clear_b'],['empty','on_a_b','clear_a'])]
    # elif number == 3:
    #     I = ['hold_a', 'clear_b', 'ontable_b']
    #     G = ['empty', 'clear_b', 'on_b_a', 'ontable_a']
    #     #??
    # elif number == 5:
    #     I = ['empty', 'clear_a', 'on_a_b', 'on_b_c', 'ontable_c']
    #     G = ['hold_c', 'clear_b', 'on_b_a', 'ontable_a']
    #     A = [('U(a,b)',['empty','on_a_b','clear_a'],['hold_a','clear_b']), ('OT(a)',['hold_a'],['empty','ontable_a','clear_a']), ('U(b,c)',['empty','on_b_c','clear_b'],['hold_b','clear_c']), ('O(b,a)',['hold_b','clear_a'],['empty','on_b_a','clear_b']), ('FT(c)',['empty', 'ontable_c', 'clear_c'],['hold_c']), ('O(c,b)',['hold_c','clear_b'],['empty','on_c_b','clear_c'])]
    # elif number == 6:
    #     I = ['empty', 'clear_a', 'on_a_b', 'on_b_c', 'ontable_c']
    #     G = ['empty', 'clear_c', 'on_c_b', 'on_b_a', 'ontable_a']
    #     A = [('U(a,b)',['empty','on_a_b','clear_a'],['hold_a','clear_b']), ('OT(a)',['hold_a'],['empty','ontable_a','clear_a']), ('U(b,c)',['empty','on_b_c','clear_b'],['hold_b','clear_c']), ('O(b,a)',['hold_b','clear_a'],['empty','on_b_a','clear_b']), ('FT(c)',['empty', 'ontable_c', 'clear_c'],['hold_c']), ('O(c,b)',['hold_c','clear_b'],['empty','on_c_b','clear_c'])]
    elif number == 16: # plan has 1-Step (1 action)
        I = [('empty', 1), ('clear_a', 1), ('on_a_b', 1), ('on_b_c', 1), ('ontable_c', 1)]
        G = [('hold_a', 1), ('clear_b', 1), ('on_b_c', 1), ('ontable_c', 1)]
        A = [('U(a,b)',[('empty', 1),('on_a_b', 1),('clear_a', 1)],[('hold_a', 1),('clear_b', 1)]), ('OT(a)',[('hold_a', 1)],[('empty', 1),('ontable_a', 1),('clear_a', 1)]), ('U(b,c)',[('empty', 1),('on_b_c', 1),('clear_b', 1)],[('hold_b', 1),('clear_c', 1)]), ('O(b,a)',[('hold_b', 1),('clear_a', 1)],[('empty', 1),('on_b_a', 1),('clear_b', 1)]), ('FT(c)',[('empty', 1), ('ontable_c', 1), ('clear_c', 1)],[('hold_c', 1)]), ('O(c,b)',[('hold_c', 1),('clear_b', 1)],[('empty', 1),('on_c_b', 1),('clear_c', 1)])]
    elif number == 26: # plan has 2-Step (2 actions)
        I = [('empty', 1), ('clear_a', 1), ('on_a_b', 1), ('on_b_c', 1), ('ontable_c', 1)]
        G = [('empty', 1), ('clear_b', 1), ('on_b_c', 1), ('ontable_c', 1), ('ontable_a', 1), ('clear_a', 1)]
        A = [('U(a,b)',[('empty', 1),('on_a_b', 1),('clear_a', 1)],[('hold_a', 1),('clear_b', 1)]), ('OT(a)',[('hold_a', 1)],[('empty', 1),('ontable_a', 1),('clear_a', 1)]), ('U(b,c)',[('empty', 1),('on_b_c', 1),('clear_b', 1)],[('hold_b', 1),('clear_c', 1)]), ('O(b,a)',[('hold_b', 1),('clear_a', 1)],[('empty', 1),('on_b_a', 1),('clear_b', 1)]), ('FT(c)',[('empty', 1), ('ontable_c', 1), ('clear_c', 1)],[('hold_c', 1)]), ('O(c,b)',[('hold_c', 1),('clear_b', 1)],[('empty', 1),('on_c_b', 1),('clear_c', 1)])]
    elif number == 36: # plan has 3-Step (3 actions)
        I = [('empty', 1), ('clear_a', 1), ('on_a_b', 1), ('on_b_c', 1), ('ontable_c', 1)]
        G = [('hold_b', 1), ('ontable_c', 1), ('clear_c', 1), ('ontable_a', 1), ('clear_a', 1)]
        A = [('U(a,b)',[('empty', 1),('on_a_b', 1),('clear_a', 1)],[('hold_a', 1),('clear_b', 1)]), ('OT(a)',[('hold_a', 1)],[('empty', 1),('ontable_a', 1),('clear_a', 1)]), ('U(b,c)',[('empty', 1),('on_b_c', 1),('clear_b', 1)],[('hold_b', 1),('clear_c', 1)]), ('O(b,a)',[('hold_b', 1),('clear_a', 1)],[('empty', 1),('on_b_a', 1),('clear_b', 1)]), ('FT(c)',[('empty', 1), ('ontable_c', 1), ('clear_c', 1)],[('hold_c', 1)]), ('O(c,b)',[('hold_c', 1),('clear_b', 1)],[('empty', 1),('on_c_b', 1),('clear_c', 1)])]
    elif number == 46: # plan has 4-Step (4 actions)
        I = [('empty', 1), ('clear_a', 1), ('on_a_b', 1), ('on_b_c', 1), ('ontable_c', 1)]
        G = [('empty', 1), ('ontable_c', 1), ('clear_c', 1), ('ontable_a', 1), ('on_b_a', 1), ('clear_b', 1)]
        A = [('U(a,b)',[('empty', 1),('on_a_b', 1),('clear_a', 1)],[('hold_a', 1),('clear_b', 1)]), ('OT(a)',[('hold_a', 1)],[('empty', 1),('ontable_a', 1),('clear_a', 1)]), ('U(b,c)',[('empty', 1),('on_b_c', 1),('clear_b', 1)],[('hold_b', 1),('clear_c', 1)]), ('O(b,a)',[('hold_b', 1),('clear_a', 1)],[('empty', 1),('on_b_a', 1),('clear_b', 1)]), ('FT(c)',[('empty', 1), ('ontable_c', 1), ('clear_c', 1)],[('hold_c', 1)]), ('O(c,b)',[('hold_c', 1),('clear_b', 1)],[('empty', 1),('on_c_b', 1),('clear_c', 1)])]
    elif number == 56: # plan has 5-Step (5 actions)
        I = [('empty', 1), ('clear_a', 1), ('on_a_b', 1), ('on_b_c', 1), ('ontable_c', 1)]
        G = [('hold_c', 1), ('clear_b', 1), ('on_b_a', 1), ('ontable_a', 1)]
        A = [('U(a,b)',[('empty', 1),('on_a_b', 1),('clear_a', 1)],[('hold_a', 1),('clear_b', 1)]), ('OT(a)',[('hold_a', 1)],[('empty', 1),('ontable_a', 1),('clear_a', 1)]), ('U(b,c)',[('empty', 1),('on_b_c', 1),('clear_b', 1)],[('hold_b', 1),('clear_c', 1)]), ('O(b,a)',[('hold_b', 1),('clear_a', 1)],[('empty', 1),('on_b_a', 1),('clear_b', 1)]), ('FT(c)',[('empty', 1), ('ontable_c', 1), ('clear_c', 1)],[('hold_c', 1)]), ('O(c,b)',[('hold_c', 1),('clear_b', 1)],[('empty', 1),('on_c_b', 1),('clear_c', 1)])]
    elif number == 66: # plan has 6-Step (6 actions)
        I = [('empty', 1), ('clear_a', 1), ('on_a_b', 1), ('on_b_c', 1), ('ontable_c', 1)]
        G = [('empty', 1), ('clear_c', 1), ('on_c_b', 1), ('on_b_a', 1), ('ontable_a', 1)]
        A = [('U(a,b)',[('empty', 1),('on_a_b', 1),('clear_a', 1)],[('hold_a', 1),('clear_b', 1)]), ('OT(a)',[('hold_a', 1)],[('empty', 1),('ontable_a', 1),('clear_a', 1)]), ('U(b,c)',[('empty', 1),('on_b_c', 1),('clear_b', 1)],[('hold_b', 1),('clear_c', 1)]), ('O(b,a)',[('hold_b', 1),('clear_a', 1)],[('empty', 1),('on_b_a', 1),('clear_b', 1)]), ('FT(c)',[('empty', 1), ('ontable_c', 1), ('clear_c', 1)],[('hold_c', 1)]), ('O(c,b)',[('hold_c', 1),('clear_b', 1)],[('empty', 1),('on_c_b', 1),('clear_c', 1)])]
    return prove(I, G, A, reverse)

# ----------------------------------------------------------------------------------------------------------------------------------------

def paperExample( number, reverse = False, combination = None, optimisationMethod = None, pruningMethod = None ):
    from graph import prove
    if number ==1:
        I = [('C', 2), ('M', 1)]
        G = [('P', 2), ('M', 1)]
        A = [('Make P',[('C', 1),('M', 1)], [('P', 1),('M', 1)])]
    elif number == 2: 
        I = [('C1', 32), ('C2', 32), ('M', 48)]
        G = [('P', 16), ('FP', 4), ('M', 48)]
        A = [('Make S1',[('C1', 1),('M', 1)],[('S1', 1),('M', 1)]),('Make S2',[('C2', 1),('M', 1)],[('S2', 1),('M', 1)]),('Make P',[('S1', 1),('S2', 1),('M', 1)],[('P', 1),('M', 1)]),('Make FP',[('P', 4),('M', 1)],[('FP', 1),('M', 1)])]
    elif number == 3:  # Paper Example modified with merged action formulae Make S1 and Make S2
        I = [('C1', 32), ('C2', 32), ('M', 48)]
        G = [('P', 16), ('FP', 4), ('M', 48)]
        A = [('Make S1 and S2',[('C1', 1),('C2', 1),('M', 2)],[('S1', 1),('S2', 1),('M', 2)]),('Make P',[('S1', 1),('S2', 1),('M', 1)],[('P', 1),('M', 1)]),('Make FP',[('P', 4),('M', 1)],[('FP', 1),('M', 1)])]
    elif number == 4: # unsolvable?
        I = [('C1', 32), ('C2', 32), ('M', 48)]
        G = [('P', 16), ('FP', 4), ('M', 48)]
        A = [('Make S1_2',[('C1', 1),('M', 1)],[('S1', 1),('M', 1)]),('Make S2_2',[('C2', 1),('M', 1)],[('S2', 1),('M', 1)]),('Make S1',[('C1', 1),('M', 1)],[('S1', 1),('M', 1)]),('Make S2',[('C2', 1),('M', 1)],[('S2', 1),('M', 1)]),('Make P',[('S1', 1),('S2', 1),('M', 1)],[('P', 1),('M', 1)]),('Make FP',[('P', 4),('M', 1)],[('FP', 1),('M', 1)])]
    return prove( I, G, A, reverse, combination, optimisationMethod, pruningMethod )


# Testing if loops work
def loopTest(number):
    from graph import prove
    if number == 1:
        I = [('X1', 1), ('X2', 1),('M',2)]
        G = [('A', 2), ('B',2),('M', 2)]
        A = [('Make A',[('X2', 1),('M', 1)], [('A', 1),('X1', 1),('M', 1)]),('Make B',[('X1', 1),('M', 1)], [('B', 1),('X2', 1),('M', 1)])]
    if number == 2:
        I = [('X1', 1), ('X2', 1),('Y1', 1), ('Y2', 1),('M',2)]
        G = [('C', 2), ('D',2),('M', 2)]
        A = [('Make A',[('X2', 1),('M', 1)], [('A', 1),('X1', 1),('M', 1)]),('Make B',[('X1', 1),('M', 1)], [('B', 1),('X2', 1),('M', 1)]),('Make C',[('Y2', 1),('M', 1),('A',1)], [('C', 1),('Y1', 1),('M', 1)]),('Make D',[('Y1', 1),('B',1),('M', 1)], [('D', 1),('Y2', 1),('M', 1)])]


    return prove(I, G, A, False) 

# Testing different patterns
def testPatterns(number):
    """ Examples for testing different patterns
    """
    from graph import prove
    # Test different patterns
    if number == 1: # Pattern 1
        I = [('A',1)]
        G = [('C',1)]
        A = [('A to B',[('A',1)],[('B',1)]), ('B to C',[('B',1)],[('C',1)])]
        #
        # A - B - C
        #
    if number == 2: # Pattern 2
        I = [('A',2)]
        G = [('D',1)]
        A = [('A to B',[('A',1)],[('B',1)]), ('A to C',[('A',1)],[('C',1)]),('B,C to D',[('B',1),('C',1)],[('D',1)])]
        #   / B \
        # A      D
        #   \ C /
    if number == 3: # Pattern 3
        I = [('A',1)]
        G = [('G',1)]
        A = [('A to B',[('A',1)],[('B',1)]), ('B to C',[('B',1)],[('C',1)]),('C to D',[('C',1)],[('D',1)]),('D to E',[('D',1)],[('E',1)]),('E to F',[('E',1)],[('F',1)]),('F to G',[('F',1)],[('G',1)])]
        # test length
        # 
        # A - B - C - D - E - F - G
        #
    if number == 4: # Pattern 4
        I = [('A',8)]
        G = [('J',1)]
        A = [('A to B',[('A',1)],[('B',1)]), ('A to C',[('A',1)],[('C',1)]), ('A to D',[('A',1)],[('D',1)]), ('A to E',[('A',1)],[('E',1)]), ('A to F',[('A',1)],[('F',1)]), ('A to G',[('A',1)],[('G',1)]), ('A to H',[('A',1)],[('H',1)]), ('A to I',[('A',1)],[('I',1)]),('B, C, D, E, F, G, H, I to J',[('B',1),('C',1),('D',1),('E',1),('F',1),('G',1),('H',1),('I',1)],[('J',1)])]
        # test width
        #      B 
        #      C \
        #      D   \
        #   /  E    \
        # A    F      J
        #   \  G    / 
        #      H  /
        #      I
    if number == 5: # Pattern 5
        # simple interleaving
        I = [('A',1),('B',1),('C',1),('D',1)]
        G = [('G',1)]
        A = [('A,C to A,D,E',[('A',1),('C',1)],[('A',1),('D',1),('E',1)]),('B,D to B,C,F',[('B',1),('D',1)],[('B',1),('C',1),('F',1)]),('E,F to G',[('E',1),('F',1)],[('G',1)])]
        #  A  -  - A
        #  C  -  - D
        #        \ E ---- 
        #  B  -  - B      \
        #  D  -  - C       G
        #        \ F ---- /
    if number == 6: # Pattern 6
        # Multiple interleaving
        # up to 4 works
        I = [('A',1),('B',1),('C',1),('D',1)]
        G = [('G',1)]
        A = [('A,C to B,D,E',[('A',1),('C',1)],[('B',1),('D',1),('E',1)]),('B,D to A,C,F',[('B',1),('D',1)],[('A',1),('C',1),('F',1)]),('E,F to G',[('E',3),('F',3)],[('G',1)])]
        #  A  -  - B
        #  C  -  - D
        #        \ E   ...  E=3 ---- 
        #  B  -  - A                 \
        #  D  -  - C                  G
        #        \ F   ...  F=3 ---- /
    if number == 7:
        # simple loop
        I = [('A',1)]
        G = [('C',1)]
        A = [('A to A,B',[('A',1)],[('A',1),('B',1)]),('B to A,C',[('B',1)],[('C',1)])]
        # A -   - C
        #   \B  /
    if number == 8:
        # multiple loop
        I = [('A',1)]
        G = [('C',1)]
        A = [('A to A,B',[('A',1)],[('A',1),('B',1)]),('B to C',[('B',7)],[('C',1)])]
        # A -  ... A    - C
        #   \B ... B =7 /


    combine = CombineActionFormulars()
    parameters = {}
    parameters['combineddistance'] = 0.5
    combine = CombineActionFormulars('distance',meassure.ChebychevMeassure())
    #combine = CombineActionFormulars('distance',meassure.CosineSimilarityMeassure()) 
    # combine = CombineActionFormulars('distance',meassure.EuclideanDistanceMeassure())
    # combine = CombineActionFormulars('distance',meassure.ManhattanDistanceMeassure())
    # combine = CombineActionFormulars('distance',meassure.MinkowskiDistanceMeassure())
    # combine = CombineActionFormulars('distance',meassure.PearsonCorrelationCoefficientMeassure())
    # combine = CombineActionFormulars('distance',meassure.SpearmanRankCorrelationMeassure())
    # combine = CombineActionFormulars('distance',meassure.HammingDistanceMeassure())
    # combine = CombineActionFormulars('distance',meassure.MahalanobisDistanceMeassure())  # Mahalobis needs many observations, not for pair wise
    # combine = CombineActionFormulars('distance',meassure.KLDivergenceMeassure()) # not applicable??
    # combine = CombineActionFormulars('distance',meassure.CanberraDistanceMeassure())
    # combine = CombineActionFormulars('distance',meassure.CorrelationDistanceMeassure()) 
    # combine = CombineActionFormulars('distance',meassure.CzekanowskiDiceCoeeficientMeassure())
    # combine = CombineActionFormulars('distance',meassure.BrayCuritsDissimilarityMeassure())
    # combine = CombineActionFormulars('distance',meassure.JensenshannonMeassure())
    # combine = CombineActionFormulars('distance',meassure.NormalizedCompressionDistanceMeassure()) # <- not implemented
    # combine = CombineActionFormulars('distance',meassure.SQEuclidMeassure()) 
    # combine = CombineActionFormulars('distance',meassure.RogerstanimotoMeassure())
    # combine = CombineActionFormulars('distance',meassure.JaccardMeassure())
    # combine = CombineActionFormulars('distance',meassure.Kulczyinski1Meassure())
    # combine = CombineActionFormulars('distance',meassure.RussellraoMeassure())
    # combine = CombineActionFormulars('distance',meassure.SokalmichenerMeassure())
    # combine = CombineActionFormulars('distance',meassure.SokalsneathMeassure())
    # combine = CombineActionFormulars('distance',meassure.YuleMeassure())
    # combine = CombineActionFormulars('distance',meassure.HaversineMeassure()) # not working
    # combine = CombineActionFormulars('distance',meassure.MatchingDistance()) # not working
    combine.setParameters(parameters)
    combine = None

    return prove(I, G, A, False, combine) 


# This example was thought for sending commands to the ROS interface, which was removed from the web service
def simpleROSRoboter(number):
    """ ROS Robot simulator example
    """
    from graph import prove
    if number == 1:
        # only one robot
        I = [('empty',1),('0 meter',1)]
        G = [('empty',1),('20 meter',1)]

        # this code does not work loaded=1
        #A = [('load at beginning',[('empty',1),('0 meter',1)],[('loaded',1),('0 meter',1)])
        #    ,('move at 0 meter',[('loaded',1),('0 meter',1)],[('loaded',1),('5 meter',1)])
        #    ,('move 5 meter',[('loaded',1),('5 meter',1)],[('loaded',1),('5 meter',2)])
        #    ,('stop at 20 meter',[('loaded',1),('5 meter',4)],[('loaded',1),('20 meter',1)])
        #    ,('unload',[('loaded',1),('20 meter',1)],[('empty',1),('20 meter',1)])
        #     ]


        A = [('load at beginning',[('empty',1),('0 meter',1)],[('loaded',1),('0 meter',1)])
            ,('move at 0 meter',[('loaded',1),('0 meter',1)],[('loaded',2),('5 meter',1)])
            ,('move 5 meter',[('loaded',1),('5 meter',1)],[('loaded',1),('5 meter',2)])
            ,('stop at 20 meter',[('loaded',1),('5 meter',4)],[('loaded',1),('20 meter',1)])
            ,('unload',[('loaded',1),('20 meter',1)],[('empty',1),('20 meter',1)])
             ]
    if number == 2:
        # two robots
        I = [('r1 empty',1),('r1 0 meter',1),('r2 empty',1),('r2 0 meter',1)]
        G = [('r1 empty',1),('r1 20 meter',1),('r2 empty',1),('r2 20 meter',1)]
        A = [('r1 load at beginning',[('r1 empty',1),('r1 0 meter',1)],[('r1 loaded',1),('r1 0 meter',1)])
             ,('r1 move at 0 meter',[('r1 loaded',1),('r1 0 meter',1)],[('r1 loaded',2),('r1 5 meter',1)])
             ,('r1 move 5 meter',[('r1 loaded',1),('r1 5 meter',1)],[('r1 loaded',1),('r1 5 meter',2)])
            ,('r1 stop at 20 meter',[('r1 loaded',1),('r1 5 meter',4)],[('r1 loaded',1),('r1 20 meter',1)])
            ,('r1 unload',[('r1 loaded',1),('r1 20 meter',1)],[('r1 empty',1),('r1 20 meter',1)])
            ,('r2 load at beginning',[('r2 empty',1),('r2 0 meter',1)],[('r2 loaded',1),('r2 0 meter',1)])
             ,('r2 move at 0 meter',[('r2 loaded',1),('r2 0 meter',1)],[('r2 loaded',2),('r2 5 meter',1)])
             ,('r2 move 5 meter',[('r2 loaded',1),('r2 5 meter',1)],[('r2 loaded',1),('r2 5 meter',2)])
            ,('r2 stop at 20 meter',[('r2 loaded',1),('r2 5 meter',4)],[('r2 loaded',1),('r2 20 meter',1)])
            ,('r2 unload',[('r2 loaded',1),('r2 20 meter',1)],[('r2 empty',1),('r2 20 meter',1)])

             ]
        pass
    if number == 3:
        # ten robots
        I = [('r1 empty',1),('r1 0 meter',1),('r2 empty',1),('r2 0 meter',1)]
        G = [('r1 empty',1),('r1 20 meter',1),('r2 empty',1),('r2 20 meter',1),('r3 empty',1),('r3 20 meter',1),('r4 empty',1),('r4 20 meter',1),('r5 empty',1),('r5 20 meter',1),('r6 empty',1),('r6 20 meter',1),('r7 empty',1),('r7 20 meter',1),('r8 empty',1),('r8 20 meter',1),('r9 empty',1),('r9 20 meter',1),('r10 empty',1),('r10 20 meter',1)]
        A = [('r1 load at beginning',[('r1 empty',1),('r1 0 meter',1)],[('r1 loaded',1),('r1 0 meter',1)])
             ,('r1 move at 0 meter',[('r1 loaded',1),('r1 0 meter',1)],[('r1 loaded',2),('r1 5 meter',1)])
             ,('r1 move 5 meter',[('r1 loaded',1),('r1 5 meter',1)],[('r1 loaded',1),('r1 5 meter',2)])
            ,('r1 stop at 20 meter',[('r1 loaded',1),('r1 5 meter',4)],[('r1 loaded',1),('r1 20 meter',1)])
            ,('r1 unload',[('r1 loaded',1),('r1 20 meter',1)],[('r1 empty',1),('r1 20 meter',1)])
            ,('r2 load at beginning',[('r2 empty',1),('r2 0 meter',1)],[('r2 loaded',1),('r2 0 meter',1)])
             ,('r2 move at 0 meter',[('r2 loaded',1),('r2 0 meter',1)],[('r2 loaded',2),('r2 5 meter',1)])
             ,('r2 move 5 meter',[('r2 loaded',1),('r2 5 meter',1)],[('r2 loaded',1),('r2 5 meter',2)])
            ,('r2 stop at 20 meter',[('r2 loaded',1),('r2 5 meter',4)],[('r2 loaded',1),('r2 20 meter',1)])
            ,('r2 unload',[('r2 loaded',1),('r2 20 meter',1)],[('r2 empty',1),('r2 20 meter',1)])
            ,('r3 load at beginning',[('r3 empty',1),('r3 0 meter',1)],[('r3 loaded',1),('r3 0 meter',1)])
             ,('r3 move at 0 meter',[('r3 loaded',1),('r3 0 meter',1)],[('r3 loaded',2),('r3 5 meter',1)])
             ,('r3 move 5 meter',[('r3 loaded',1),('r3 5 meter',1)],[('r3 loaded',1),('r3 5 meter',2)])
            ,('r3 stop at 20 meter',[('r3 loaded',1),('r3 5 meter',4)],[('r3 loaded',1),('r3 20 meter',1)])
            ,('r3 unload',[('r3 loaded',1),('r3 20 meter',1)],[('r3 empty',1),('r3 20 meter',1)])

            ,('r4 load at beginning',[('r4 empty',1),('r4 0 meter',1)],[('r4 loaded',1),('r4 0 meter',1)])
             ,('r4 move at 0 meter',[('r4 loaded',1),('r4 0 meter',1)],[('r4 loaded',2),('r4 5 meter',1)])
             ,('r4 move 5 meter',[('r4 loaded',1),('r4 5 meter',1)],[('r4 loaded',1),('r4 5 meter',2)])
            ,('r4 stop at 20 meter',[('r4 loaded',1),('r4 5 meter',4)],[('r4 loaded',1),('r4 20 meter',1)])
            ,('r4 unload',[('r4 loaded',1),('r4 20 meter',1)],[('r4 empty',1),('r4 20 meter',1)])

            ,('r5 load at beginning',[('r5 empty',1),('r5 0 meter',1)],[('r5 loaded',1),('r5 0 meter',1)])
             ,('r5 move at 0 meter',[('r5 loaded',1),('r5 0 meter',1)],[('r5 loaded',2),('r5 5 meter',1)])
             ,('r5 move 5 meter',[('r5 loaded',1),('r5 5 meter',1)],[('r5 loaded',1),('r5 5 meter',2)])
            ,('r5 stop at 20 meter',[('r5 loaded',1),('r5 5 meter',4)],[('r5 loaded',1),('r5 20 meter',1)])
            ,('r5 unload',[('r5 loaded',1),('r5 20 meter',1)],[('r5 empty',1),('r5 20 meter',1)])

            ,('r6 load at beginning',[('r6 empty',1),('r6 0 meter',1)],[('r6 loaded',1),('r6 0 meter',1)])
             ,('r6 move at 0 meter',[('r6 loaded',1),('r6 0 meter',1)],[('r6 loaded',2),('r6 5 meter',1)])
             ,('r6 move 5 meter',[('r6 loaded',1),('r6 5 meter',1)],[('r6 loaded',1),('r6 5 meter',2)])
            ,('r6 stop at 20 meter',[('r6 loaded',1),('r6 5 meter',4)],[('r6 loaded',1),('r6 20 meter',1)])
            ,('r6 unload',[('r6 loaded',1),('r6 20 meter',1)],[('r6 empty',1),('r6 20 meter',1)])

            ,('r7 load at beginning',[('r7 empty',1),('r7 0 meter',1)],[('r7 loaded',1),('r7 0 meter',1)])
             ,('r7 move at 0 meter',[('r7 loaded',1),('r7 0 meter',1)],[('r7 loaded',2),('r7 5 meter',1)])
             ,('r7 move 5 meter',[('r7 loaded',1),('r7 5 meter',1)],[('r7 loaded',1),('r7 5 meter',2)])
            ,('r7 stop at 20 meter',[('r7 loaded',1),('r7 5 meter',4)],[('r7 loaded',1),('r7 20 meter',1)])
            ,('r7 unload',[('r7 loaded',1),('r7 20 meter',1)],[('r7 empty',1),('r7 20 meter',1)])

            ,('r8 load at beginning',[('r8 empty',1),('r8 0 meter',1)],[('r8 loaded',1),('r8 0 meter',1)])
             ,('r8 move at 0 meter',[('r8 loaded',1),('r8 0 meter',1)],[('r8 loaded',2),('r8 5 meter',1)])
             ,('r8 move 5 meter',[('r8 loaded',1),('r8 5 meter',1)],[('r8 loaded',1),('r8 5 meter',2)])
            ,('r8 stop at 20 meter',[('r8 loaded',1),('r8 5 meter',4)],[('r8 loaded',1),('r8 20 meter',1)])
            ,('r8 unload',[('r8 loaded',1),('r8 20 meter',1)],[('r8 empty',1),('r8 20 meter',1)])

            ,('r9 load at beginning',[('r9 empty',1),('r9 0 meter',1)],[('r9 loaded',1),('r9 0 meter',1)])
             ,('r9 move at 0 meter',[('r9 loaded',1),('r9 0 meter',1)],[('r9 loaded',2),('r9 5 meter',1)])
             ,('r9 move 5 meter',[('r9 loaded',1),('r9 5 meter',1)],[('r9 loaded',1),('r9 5 meter',2)])
            ,('r9 stop at 20 meter',[('r9 loaded',1),('r9 5 meter',4)],[('r9 loaded',1),('r9 20 meter',1)])
            ,('r9 unload',[('r9 loaded',1),('r9 20 meter',1)],[('r9 empty',1),('r9 20 meter',1)])

            ,('r10 load at beginning',[('r10 empty',1),('r10 0 meter',1)],[('r10 loaded',1),('r10 0 meter',1)])
             ,('r10 move at 0 meter',[('r10 loaded',1),('r10 0 meter',1)],[('r10 loaded',2),('r10 5 meter',1)])
             ,('r10 move 5 meter',[('r10 loaded',1),('r10 5 meter',1)],[('r10 loaded',1),('r10 5 meter',2)])
            ,('r10 stop at 20 meter',[('r10 loaded',1),('r10 5 meter',4)],[('r10 loaded',1),('r10 20 meter',1)])
            ,('r10 unload',[('r10 loaded',1),('r10 20 meter',1)],[('r10 empty',1),('r10 20 meter',1)])
        ]

    return prove(I, G, A, False)


if __name__ == '__main__':
    testPC(1)