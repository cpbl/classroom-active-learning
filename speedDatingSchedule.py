"""
Consider N people who want to meet in pairs, e.g. 5 minutes each.
We will do R rounds. In general, 

N must be even

and

R<=N-1

since in N-1 rounds, everyone can meet everyone.

If we want to have an easier time solving, this, we could choose a lower R and be satisfied with not everyone meeting everyone.  



If N is a power of 2, I see an easy algorithm for assigning the schedule:
  We schedule the first N/2 rounds very easily: split the group in two, line the groups up facing each other, and have one group step left (and wrap back to the other side) each round.
  For the remaining rounds, we carry out the same algorithm within each of the initial groups.

If N is not a power of 2 and we want  R>N/2 

"""

def schedule_speed_dates(N,R=None):
    """ 
N can be an integer, or a list of names (we'll call it's length N)
R can be less than or equal to N-1
    """
    if isinstance(N,int): 
        Names=[str(nn) for nn in range(1,N+1)]
    else:
        Names=N
        N=len(Names)
    if R is None: R=N-1
    import math
    if math.log(N,2) == int(math.log(N,2)):
        sol=schedule_speed_dates_power_of_two(Names)
        print('\n'.join(['%s: %s'%(an,str(sol[ii])) for ii,an in enumerate(Names)]))
        return(sol)
def rotate(l,n):  # Postive N rotates to the right: abcd --> dabc
    return l[-n:] + l[:-n]
def schedule_speed_dates_power_of_two(Names):
    """
    A result is list, for each participant, of their matches in order.
    Split the group in half. Line them up facing each other. Each round, the top half rotates to the right.
    Round 1:       Round 2: ....     Round 4.
    1 2 3 4         4 1 2 3  ...
    5 6 7 8         5 6 7 8  ...
    """
    N=len(Names)
    def solve_half(names):
        nn=len(names)
        assert nn>1
        return([  rotate(names[nn/2:],rot) for rot in range(nn/2) ] + [rotate(names[:nn/2],rot) for rot in range(nn/2) ]  )

    import random
    random.shuffle(Names)
    sol=solve_half(Names)
    if N>2:
        solA=schedule_speed_dates_power_of_two(Names[:N/2]) + schedule_speed_dates_power_of_two(Names[N/2:])
        sol=[sum(a,[]) for a in zip(sol,solA)]
        
    return(sol)
                             
if __name__ == "__main__":
    schedule_speed_dates([L for L in """Antonia
Ari
Chris
David
Frank
Jill
Kristin
Daniel
    """.split('\n') if L.strip()])
"""
"""
