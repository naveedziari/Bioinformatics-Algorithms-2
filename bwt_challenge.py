#partners: Lucas, Alex, Aidan, Erik
#January 31, 2019

import sys
import numpy


"""The following uses Python to challenge you to create an algorithm for finding
matches between a set of aligned strings. Minimal familiarity with Python is 
necessary, notably list and Numpy array slicing. 
"""

"""Problem 1.

Let X be a list of M binary strings (over the alphabet { 0, 1 }) each of length 
N. 

For integer 0<=i<=N we define an ith prefix sort as a lexicographic sort 
(here 0 precedes 1) of the set of ith prefixes: { x[:i] | x in X }.
Similarly an ith reverse prefix sort is a lexicographic sort of the set of
ith prefixes after each prefix is reversed.

Let A be an Mx(N+1) matrix such that for all 0<=i<M, 0<=j<=N, A[i,j] is the 
index in X of the ith string ordered by jth reverse prefix. To break ties 
(equal prefixes) the ordering of the strings in X is used. 

Complete code for the following function that computes A for a given X.

Here X is a Python list of Python strings. 
To represent A we use a 2D Numpy integer array.

Example:

>>> X = getRandomX() #This is in the challenge1UnitTest.py file
>>> X
['110', '000', '001', '010', '100', '001', '100'] #Binary strings, M=7 and N=3
>>> A = constructReversePrefixSortMatrix(X)
>>> A
array([[0, 1, 1, 1],
       [1, 2, 2, 4],
       [2, 3, 5, 6],
       [3, 5, 4, 3],
       [4, 0, 6, 0],
       [5, 4, 3, 2],
       [6, 6, 0, 5]])
>>> 

Hint:
Column j (0 < j <= N) of the matrix can be constructed from column j-1 and the 
symbol in each sequence at index j-1.  

Question 1: In terms of M and N what is the asymptotic cost of your algorithm?
O(MN)
***coefficients removed/simplified from O(N*2M)
"""

def constructReversePrefixSortMatrix(X):


    #Creates the Mx(N+1) matrix
    A = numpy.empty(shape=[len(X), 1 if len(X) == 0 else len(X[0])+1], dtype=int) 


    A[:,0] = [i for i in range(len(X))] #initialize first column of A
    for k in range(len(X[0])):
      a,b = [],[] #reinitialize a,b as empty for sorting in next column
      for i in range(len(X)):
        #perform 0/1 sorting with conditional
        if X[A[i][k]][k] == '0': a.append(A[i][k])
        else: b.append(A[i][k])
      A[:,k+1] = a + b

    
    return A

"""Problem 2: 

Following on from the previous problem, let Y be the MxN matrix such that for 
all 0 <= i < M, 0 <= j < N, Y[i,j] = X[A[i,j]][j].

Complete the following to construct Y for X. 

Hint: You can either use your solution to constructReversePrefixSortMatrix() 
or adapt the code from that algorithm to create Y without using 
constructReversePrefixSortMatrix().

Question 2: In terms of M and N what is the asymptotic cost of your algorithm?
O(MN)
***O(MN) for constructing A + O(MN) for constructing Y = O(MN)***
"""
def constructYFromX(X):

    #Creates the MxN matrix
    Y = numpy.empty(shape=[len(X), 0 if len(X) == 0 else len(X[0]) ], dtype=int)
    
    A = constructReversePrefixSortMatrix(X) #construct A

    #derive Y from A
    for j in range(len(X[0])): #loop through positions
      for i in range(len(X)): #loop through haplotypes
        Y[i,j] = X[A[i][j]][j]
    
    return Y

"""Problem 3.

Y is a transformation of X. Complete the following to construct X from Y, 
returning X as a list of strings as defined in problem 1.
Hint: This is the inverse of X to Y, but the code may look very similar.

Question 3a: In terms of M and N what is the asymptotic cost of your algorithm?

O(MN)
***O(MN) for populating X + O(M*N) for amending temp_column***

Question 3b: What could you use the transformation of Y for? 
Hint: consider the BWT.

Y can construct all the other arrays in the paper (X and A). analogous to FM index for BWT, in this case PBWT. 

Question 3c: Can you come up with a more efficient data structure for storing Y?

Run length encoding. It is a form of lossless data compression that takes less space, and as quoted in the paper, its average-case compression could be 100x
"""
def constructXFromY(Y):
    #Creates the MxN matrix
    X = numpy.empty(shape=[len(Y), 0 if len(Y) == 0 else len(Y[0]) ], dtype=int)


    temp_column = [i for i in range(len(X))] #this mimics A, but updating to current position in loop below
    for k in range(len(Y[0])): #loop through positions
      for i in range(len(X)): #loop through haplotypes
        X[temp_column[i]][k] = Y[i][k]
      a,b = [],[]
      for i in range(len(X)): #loop through haplotypes
        #perform 0/1 sorting with conditional
        if Y[i][k] == 0: a.append(temp_column[i])
        else: b.append(temp_column[i])
      temp_column = a+b
    
    return list(map(lambda i : "".join(map(str, i)), X)) #Convert back to a list of strings

"""Problem 4.

Define the common suffix of two strings to be the maximum length suffix shared 
by both strings, e.g. for "10110" and "10010" the common suffix is "10" because 
both end with "10" but not both "110" or both "010". 

Let D be a Mx(N+1) Numpy integer array such that for all 1<=i<M, 1<=j<=N, 
D[i,j] is the length of the common suffix between the substrings X[A[i,j]][:j] 
and X[A[i-1,j]][:j].  

Complete code for the following function that computes D for a given A.

Example:

>>> X = getRandomX()
>>> X
['110', '000', '001', '010', '100', '001', '100']
>>> A = constructReversePrefixSortMatrix(X)
>>> A
array([[0, 1, 1, 1],
       [1, 2, 2, 4],
       [2, 3, 5, 6],
       [3, 5, 4, 3],
       [4, 0, 6, 0],
       [5, 4, 3, 2],
       [6, 6, 0, 5]])
>>> D = constructCommonSuffixMatrix(A, X)
>>> D
array([[0, 0, 0, 0],
       [0, 1, 2, 2],
       [0, 1, 2, 3],
       [0, 1, 1, 1],
       [0, 0, 2, 2],
       [0, 1, 0, 0],
       [0, 1, 1, 3]])

Hints: 

As before, column j (0 < j <= N) of the matrix can be constructed from column j-1 
and thesymbol in each sequence at index j-1.

For an efficient algorithm consider that the length of the common suffix 
between X[A[i,j]][:j] and X[A[i-k,j]][:j], for all 0<k<=i is 
min(D[i-k+1,j], D[i-k+2,j], ..., D[i,j]).

Question 4: In terms of M and N what is the asymptotic cost of your algorithm?
"""
#A4: O(MN)

def constructCommonSuffixMatrix(A, X):
    D = numpy.zeros(shape=A.shape, dtype=int) #Creates the Mx(N+1) D matrix 


    for k in range(1,len(A[0])): #loop through each position, 
      a,b = [],[] #reinitialize a,b for sorting in loop
      p,q = 0,0 #reinitialize p,q for tracking suffix match 
      for i in range(len(A)): #loop through each haplotype
        p = min(p,D[i][k-1]+1) #variable storing position of 0
        q = min(q,D[i][k-1]+1) #variable storing position of 1
        #sort 0/1 and reinitialize p/q with conditionals
        if X[A[i][k-1]][k-1] == '0':
          a.append(p)
          p = float('inf') #reset to max in order to take min before conditional
        else:
          b.append(q)
          q = float('inf')
      D[:,k] = a + b

    
    return D

"""Problem 5.

For a pair of strings X[x], X[y], a long match ending at j is a common substring
of X[x] and X[y] that ends at j (so that X[x][j] != X[y][j] or j == N) that is longer
than a threshold 'minLength'. E.g. for strings "0010100" and "1110111" and length
threshold 2 (or 3) there is a long match "101" ending at 5.
    
The following algorithm enumerates for all long matches between all substrings of
X, except for simplicity those long matches that are not terminated at
the end of the strings.
    
Question 5a: What is the asymptotic cost of the algorithm in terms of M, N and the
number of long matches?

O(NM^2)

O(max(NM,# of matches)) - you have loop on NM, but store long match in B and C, in worst case go through NM, and in best case you stop before 
worst case scenario for # of matches is O(NM^2) in pairwise comparison
for time complexity in big O notation, the worst case (asymptotic) is conventional
    
Question 5b: Can you see any major time efficiencies that could be gained by
refactoring?

O(max(NM),# of matches) - in the worst case 
building A & D within the loops rather than prior to the algorithm means that you can take it one position at a time

instead of reporting pairs, just report blocks. for this set of pairs, there is a long match - eliminates square term
O(NM) time complexity
    
Question 5c: Can you see any major space efficiencies that could be gained by
refactoring?

O(M) - as quoted in the paragraph below algorithm 3, it can be constructed in O(M) space. Given same paradigm as answer for 5b building and reinstantiating A & D for each column
explicitly, do not need to construct A & D matrices 

    
Question 5d: Can you imagine alternative algorithms to compute such matches?,
if so, what would be the asymptotic cost and space usage?

hash tables identify exact seed matches (written in Discussion of paper). 

hash tables offer improvement in time complexity, but at the expense of space complexity 
time complexity: O(N) - assuming only one bucket 
space complexity: O(NM) - O(N) for each haplotype, with M haplotypes

"""
def getLongMatches(X, minLength):
    assert minLength > 0
    
    A = constructReversePrefixSortMatrix(X)
    D = constructCommonSuffixMatrix(A, X)
    
    #For each column, in ascending order of column index
    for j in range(1, 0 if len(X) == 0 else len(X[0])):
        #Working arrays used to store indices of strings containing long matches
        #b is an array of strings that have a '0' at position j
        #c is an array of strings that have a '1' at position j
        #When reporting long matches we'll report all pairs of indices in b X c,
        #as these are the long matches that end at j.
        b, c = [], []
        
        #Iterate over the aligned symbols in column j in reverse prefix order
        for i in range(len(X)):
            #For each string in the order check if there is a long match between
            #it and the previous string.
            #If there isn't a long match then this implies that there can
            #be no long matches ending at j between sequences indices in A[:i,j]
            #and sequence indices in A[i:,j], thus we report all long matches
            #found so far and empty the arrays storing long matches.
            if D[i,j] < minLength:
                for x in b:
                    for y in c:
                        #The yield keyword converts the function into a
                        #generator - alternatively we could just to append to
                        #a list and return the list
                        
                        #We return the match as tuple of two sequence
                        #indices (ordered by order in X) and coordinate at which
                        #the match ends
                        yield (x, y, j) if x < y else (y, x, j)
                b, c = [], []
            
            #Partition the sequences by if they have '0' or '1' at position j.
            if X[A[i,j]][j] == '0':
                b.append(A[i,j])
            else:
                c.append(A[i,j])
        
        #Report any leftover long matches for the column
        for x in b:
            for y in c:
                yield (x, y, j) if x < y else (y, x, j)
