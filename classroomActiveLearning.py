#!/usr/bin/python
"""
Randomly choose a student from the class list, and pop-up their name using operating system Desktop notification.

Assign this to a hotkey for easy access during class.

TO DO:
 -  Also assign some other keys to assign a grade of 1 to 3, say, for evaluating a student's response. Store list of who was asked, and how they did, in a database somewhere.
 - Record every assignment made by its date
 - algorithm for dealing with uneven group sizes is not good. e.g. splitting up 27 people into groups of 10 gives 11, 11, and 5.

What formats of student names does it recognize?
 - columns named firstName and lastName
 - one column called "Student Name" with content formatted "last name, first name"

"""
import pandas as pd
import os

GRADES_FILE='/home/cpbl/courses/activeLearningGrades.tsv'

def chooseClassListFile():
    """
    Some custom specification of the class list default, if not given on command line
    """
    import time
    now = time.strftime("%c")
    if "Tue" in now or "Thu" in now:
        classlistfile='/home/cpbl/courses/201/classlist.csv'
    else:
        classlistfile='/home/cpbl/courses/swb/classlist.csv'
    return(classlistfile)

def recordGradeForLastStudent(thegrade):
    with open(GRADES_FILE,'at') as ff:
        ff.write('\t'+str(thegrade))
    os.system(' play /usr/share/sounds/KDE-K3B-Finish-Success.ogg &')


###########################################################################################
###
class cpblClassroomTools():  #  # # # # #    MAJOR CLASS    # # # # #  #
    ###
    #######################################################################################
    """
    """
    # Caution: If you define variables here, before __init__, you can access them with cpblClassroomTools.avar , but those are common to the entire class, not to an instance.
    def __init__(self,classlistfile=None):

        if classlistfile is None:
            classlistfile=chooseClassListFile()
        self.classlistfile=classlistfile
        """
        Shuffling the classlist initially to make remaining routines simpler
        """
        df=pd.read_csv(classlistfile,skiprows=8,encoding='iso-8859-1',index_col=False)
        # Process first, last names
        if "Student Name" in df:
            df['firstName']=df['Student Name'].map(lambda ss: ss.split(',')[1].strip())
            df['lastName']=df['Student Name'].map(lambda ss: ss.split(',')[0].strip())
            df['SNtex']=df.apply(lambda dd: dd.firstName+r' {\bf '+dd.lastName+ r'}',axis=1)
            df['SNhtml']=df.apply(lambda dd: dd.firstName+r' <b> '+dd.lastName+ r'</b>',axis=1)
        df['studentName']=df['Student Name']
        df['ID']=df.ID.map(str)
        # Shuffle it.
        from random import shuffle
        ii=range(len(df))
        shuffle(ii)
        self.classlist=df.reindex(ii)
    def randomlyChooseOneStudent(self):
        #import pandas as pd
        if 0:
            df=self.classlist
            import numpy as np
            astudent= df.ix[np.random.choice(df.index, 1)]['studentName'].values[0]
        astudent=self.classlist.iloc[0]['SNhtml']
        import time
        now = time.strftime("%c")
        with open(GRADES_FILE,'at') as ff:
            ff.write('\n'+'\t'.join([now,self.classlistfile,self.classlist.iloc[0]['studentName'],self.classlist.iloc[0]['ID']]))
        os.system("""zenity --title "" --info --text "<span foreground='blue' font='32'>%s</span>"   & """%astudent)

    def randomlyAssignGroups(self,groupsize=3):
        """
        Class size N. Just count of n=groupsize individuals from the shuffled list.  So we end up with leftover  1, 2, ...N-1.
        Distribute the extras to other groups?  unless it is preferred to have small groups

        How (sorry.. this needs a real algorithm)
        increment group name
        if more than N remain, assign N+x to next group, where x is 0 or 1, depending on whether remaining number mod N ==0

        For display, why not just create/show a PDF, rather than using a GUI text box tool? Seems easy enough, and it can be saved/ recalled.
        """
        df=self.classlist
        df['groupName']=''
        # Groups are named by letter
        groupnames='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        groupnames=list(groupnames) + [ii+jj for ii in groupnames for jj in groupnames]
        ii=0
        while ii<len(df):
            x=   (len(df)-ii)   %    groupsize
            thisN=groupsize + 1*(x>0)
            df['groupName'].iloc[ii:ii+thisN]=groupnames[0]
            #df[ii:(ii+thisN)]['groupName']=groupnames[0]
            #fooo
            ii=ii+thisN
            groupnames=groupnames[1:]
        html=''
        tex=r"""\documentclass{article}\begin{document} """
        tex=r"""\documentclass{beamer}\usepackage[utf8]{inputenc}\begin{document}\begin{frame}[allowframebreaks]  """
        closing='\n'+r'\end{document}'+'\n'
        closing='\n'+r'\end{frame}\end{document}'+'\n'
        tex=r"""
\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage{color}
\usepackage{lscape}
\usepackage[landscape,margin=0cm]{geometry}
\begin{document} 
%\begin{landscape} 
\huge
"""
        closing='\n'+ r""" \end{document}""" +'\n'
        for gg, ss in df.groupby('groupName',sort=False)['SNtex']:
            html+=""" <table><tr><td>"""+gg+"""</td><td>"""+ss.values[0]+'</td></tr>'+  ''.join([ '<tr><td></td><td>'+nn+'</td></tr>' for nn in ss.values[1:]])+"""</table>"""
            tex+=r' \begin{tabular}{|rl|}\hline  {\bf\color{blue} '+gg+':} & '+ss.values[0]+r' \\'+' \n'+  ''.join([ ' & '+nn+r' \\ ' for nn in ss.values[1:]])+ r' \hline \end{tabular}'+' \n'
        print(html)
        tex+=closing
        import codecs
        DDR='/home/cpbl/tmp/'
        with codecs.open(DDR+'tmpGroups.tex','wt',encoding='utf8') as ff:
            ff.write(tex)
        os.system('cd '+DDR +' && pdflatex tmpGroups.tex')
        os.system('cd '+DDR +' && pdflatex tmpGroups.tex')
        os.system('evince  '+DDR+'tmpGroups.pdf &')
#        os.system("""zenity --title "" --text-info --html --text=" """+html+' "   &')
        print("""zenity --title "" --text-info --html --text=" """+html+' " ')
        #"<span foreground='blue' font='32'>%s</span>" """%astudent)
        #os.system("""zenity --title "" --info --text " """+html+' " ') #<span foreground='blue' font='32'>%s</span>" """%astudent)
 
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Various desktop pop-up tools for interactive classes.')
    parser.add_argument('-c','--classlist', #, metavar=None, type=str, nargs='1',
                        action='store',
                        help='A csv file containing data on the class list')
    parser.add_argument('--choose-student',#,  type=int, nargs='+',
                        action='store_true',
                       help=' Display one student name, and record the name for subsequent grading')
    parser.add_argument('-s', '--record-score', #-choose-student',#,  type=int, nargs='+',
                        action='store',
                       help=' Save a mark, associated with the recently displayed individual')
    #parser.add_argument('--sum', dest='accumulate', action='store_const',
    #                   const=sum, default=max,
    #                   help='sum the integers (default: find the max)')

    args = parser.parse_args()
    ct=cpblClassroomTools(classlistfile=args.classlist)

    if args.choose_student:
        ct.randomlyChooseOneStudent()
    elif args.record_score is not None:
        recordGradeForLastStudent(args.record_score)
    else: # Demo

        ct=cpblClassroomTools(classlistfile=classlistfile)
    #    ct.randomlyAssignGroups(3)
    #    ct.randomlyAssignGroups(4)
        ct.randomlyAssignGroups(10)
        #ct.randomlyChooseOneStudent()



