import numpy as np

# Write a function that takes as input two lists Y, P,
# and returns the float corresponding to their cross-entropy.

# CROSS ENTROPY = - ( y1 * ln p1 ) + ( (1 - y1) * ln (1 - p1) )
#                 - ( y2 * ln p2 ) + ( (1 - y2) * ln (1 - p2) )
#                 ...
#                 - ( yn * ln pn ) + ( (1 - yn) * ln (1 - pn) )

# We subtract the CE values because ln of values below 1 is negative
# (because ln 1 = 0)
# So we get a positive score
# Lower is better

def cross_entropy(Y, P):
    sum = 0
    for i in range(0, len(Y)):
        _y = Y[i]
        _p = P[i]
        sum -= (_y * np.log(_p)) + ((1 - _y) * np.log(1 - _p))
    return sum
