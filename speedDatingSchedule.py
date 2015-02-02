#!/usr/bin/python
"""
Pairwise unisex Speed Dating Schedule / Speed date scheduling

This seems to be a simple "round robin" scheduling problem, solved even on Wikipedia.
The algorithm is similar for even and odd numbers; with odd, just add an extra "nobody" person.

Consider N people who want to meet in pairs, e.g. 5 minutes each.
We will do R rounds. In general, 

   N must be even, so no one has to sit out.

and

   R <= N-1

since in N-1 rounds, everyone can meet everyone.

"""
def rotate(l,n):  # Postive N rotates to the right: abcd --> dabc
    return l[-n:] + l[:-n]

def schedule_speed_dates(N,R=None):
    """
    Stand one person fixed at head of long, narrow table. Rotate everyone else around all the other positions. People play with the person facing them.

    N can be an integer, or a list of names (we'll call its length N)
    R can be less than or equal to N-1
    """
    if isinstance(N,int): 
        Names=[str(nn) for nn in range(1,N+1)]
    else:
        Names=N
        N=len(Names)

    if not  N%2==0:
        Names+=['nobody (bye)']
        N+=1

    import random
    random.shuffle(Names)

    if R is None: R=N-1

    # Initialize a dict containing each player's schedule
    schedule=dict([[nn,[]] for nn in Names])

    restOfTable=Names[1:]
    tableLength=N/2 -1
    for rn in range(R):
        lon=rotate(restOfTable,rn)
        lineups= zip (   Names[:1] + lon[:tableLength]    , [lon[tableLength]] + lon[tableLength:][::-1]  )
        for apair in lineups:
            schedule[apair[0]]+=[apair[1]]
            schedule[apair[1]]+=[apair[0]]
    for nn,mm in schedule.items(): # This order is not well determined. It comes from dict. Sort?
        print(nn+':  '+str(mm))
    return(schedule)
                             
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
