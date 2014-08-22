#!/usr/bin/python
"""
Randomly choose a student from the class list, and pop-up their name using operating system Desktop notification.

Assign this to a hotkey for easy access during class.

TO DO: Also assign some other keys to assign a grade of 1 to 3, say, for evaluating a student's response. Store list of who was asked, and how they did, in a database somewhere.

"""
import sys
if len(sys.arg)==2:
    classlistfile=sys.arg[1]
else:
    classlistfile='/home/cpbl/courses/swb/classlist.csv'
import pandas as pd
df=pd.read_csv(classlistfile,skiprows=8,encoding='iso-8859-1',index_col=False)
import numpy as np
astudent= df.ix[np.random.choice(df.index, 1)]['Student Name'].values[0]
import os
os.system("""zenity --title "" --info --text "<span foreground='blue' font='32'>%s</span>" """%astudent)

