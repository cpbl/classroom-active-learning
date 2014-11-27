#!/usr/bin/python
from codecs import open
import os

def createExamVersions(srcPath=None,n_exams=4):
    """
    CPBL Nov 2014
    Decidedly not "active learning", this function is for making exams with multiple choice questions, inter alia, in LaTeX.

    This is to take a LaTeX file which contains some multiple choice questions, and randomly rearrange the multiple choice questions (but leave everything else intact).
So this lets me use my preferred exam class  (and the \mcquestion environment defined in cpblExams.sty) but benefit also from randomization of question order.

    This is necessary because in the big-class courses at McGill we have several versions of the exam to minimize the value of wandering gaze during exams.

    This also creates answer keys, useful for giving to the computer-grading office.
    """
    N_EXAMS= n_exams  # Plus version 0, which is not randomized
    assert srcPath.endswith('.tex')
    srcPathNoExt=srcPath[:-4]
    #srcDir,srcFile=os.path.split(srcPath)
    intex=open(srcPath,'rt').read()

    import re

    beforeMC,trest=intex.split('\n%BEGINMULTIPLECHOICESECTION')

    mcqsection,afterMC=trest.split('\n%ENDMULTIPLECHOICESECTION')
    #%re.findall('(.*?)\n%BEGINMULTIPLECHOICESECTION(.*?)\n%ENDMULTIPLECHOICESECTION(.*?)',intex,re.DOTALL)

    # Drop comment lines first:
    mcqsection='\n'.join([LL for LL in mcqsection.split('\n') if not LL.strip().startswith('%')])
    mcqs=re.findall(r'.begin{mcquestion}.*?.end{mcquestion}',mcqsection,re.DOTALL)

    # Set up PERMANENT REORDERINGS: This was done one-time using:
    xxx=range(1,100)
    import random
    questionorders=[xxx]+[sorted(xxx, key=lambda *args: random.random()) for nn in range(5)]
    # But is now hardcoded for up to 100 questions and 6 versions (N.B. It may be fairest not to use the first version, which is unrandomized)
    questionorders=[[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99], [10, 97, 50, 34, 16, 96, 81, 8, 58, 13, 24, 12, 85, 89, 52, 54, 9, 49, 29, 15, 90, 26, 45, 36, 74, 27, 57, 84, 95, 94, 63, 99, 47, 80, 66, 72, 37, 86, 48, 65, 75, 44, 33, 6, 91, 92, 14, 51, 64, 30, 76, 5, 41, 77, 70, 32, 11, 59, 61, 42, 43, 23, 67, 56, 83, 3, 55, 98, 93, 73, 22, 4, 62, 79, 31, 35, 7, 19, 28, 20, 69, 1, 60, 39, 88, 46, 21, 71, 53, 68, 17, 40, 87, 82, 2, 18, 25, 38, 78], [15, 41, 16, 62, 56, 40, 34, 92, 88, 8, 67, 9, 55, 1, 54, 50, 25, 3, 12, 43, 10, 82, 70, 7, 76, 18, 73, 2, 91, 63, 99, 79, 37, 66, 22, 94, 4, 81, 60, 49, 51, 24, 38, 53, 86, 83, 68, 69, 14, 52, 20, 90, 28, 87, 75, 96, 19, 5, 74, 39, 36, 44, 21, 26, 71, 31, 42, 11, 27, 46, 47, 45, 84, 80, 30, 89, 58, 64, 35, 48, 13, 93, 57, 77, 65, 61, 29, 32, 95, 23, 17, 33, 98, 97, 85, 59, 78, 72, 6], [86, 83, 31, 96, 56, 32, 76, 4, 87, 47, 18, 78, 44, 66, 53, 46, 95, 5, 29, 79, 98, 88, 8, 45, 90, 21, 19, 12, 16, 82, 84, 28, 7, 94, 3, 67, 39, 75, 54, 72, 97, 85, 74, 89, 38, 20, 73, 49, 61, 26, 9, 80, 37, 50, 58, 60, 71, 41, 2, 91, 99, 24, 92, 65, 23, 33, 14, 30, 48, 27, 11, 64, 55, 34, 13, 10, 17, 57, 42, 1, 70, 81, 15, 59, 52, 22, 36, 93, 25, 68, 63, 43, 51, 6, 35, 77, 62, 40, 69], [10, 94, 78, 70, 33, 1, 99, 66, 89, 11, 19, 16, 86, 21, 8, 64, 81, 45, 43, 25, 83, 62, 53, 60, 9, 74, 29, 56, 92, 4, 76, 59, 7, 65, 18, 38, 48, 47, 88, 6, 91, 35, 95, 73, 17, 87, 54, 40, 69, 28, 93, 37, 15, 72, 14, 80, 96, 77, 75, 12, 68, 84, 85, 67, 61, 90, 30, 51, 27, 49, 71, 79, 57, 52, 2, 23, 39, 55, 98, 36, 31, 34, 32, 97, 22, 3, 44, 41, 46, 50, 5, 58, 42, 20, 63, 13, 24, 82, 26], [44, 56, 5, 69, 58, 11, 8, 13, 63, 98, 40, 31, 93, 9, 38, 70, 77, 91, 32, 67, 65, 33, 85, 43, 28, 60, 94, 24, 17, 34, 22, 81, 80, 86, 46, 99, 16, 41, 48, 87, 35, 18, 54, 66, 21, 29, 45, 20, 26, 84, 6, 49, 59, 47, 79, 12, 3, 27, 50, 64, 71, 68, 52, 75, 57, 73, 42, 83, 89, 61, 19, 51, 92, 1, 76, 78, 2, 90, 55, 39, 72, 23, 30, 82, 7, 14, 25, 62, 10, 74, 97, 88, 96, 15, 36, 4, 95, 37, 53]]

    # Reorder the quesitons:

    srcTxt=beforeMC+"""
    %BEGINMULTIPLECHOICESECTION

    MC_QUESTIONS_HERE

    %ENDMULTIPLECHOICESECTION
    """+afterMC
    #%re.findall('(.*?)\n%BEGINMULTIPLECHOICESECTION(.*?)\n%ENDMULTIPLECHOICESECTION(.*?)',intex,re.DOTALL)
    mcqs=re.findall(r'.begin{mcquestion}.*?.end{mcquestion}',mcqsection,re.DOTALL)

    for iver in range(N_EXAMS+1):
        outtxt= srcTxt.replace('EXAMVERSIONNUMBER', str(iver)).replace( 'MC_QUESTIONS_HERE','\n\n'.join( [qq for nn,qq in  sorted(zip(questionorders[iver],mcqs))]  ))
        outpath=srcPathNoExt+'-version%d.tex'%iver
        with open(outpath,'wt') as ff:
            ff.write(outtxt)


    # Now, let's also try to divine the answer keys!!!
    akey=[]
    for qq in mcqs:
        # Drop comment lines.
        # Then find answers:
        qql=[LL for LL in qq.split('\n') if not LL.strip().startswith('%')]
        # The following is not quite right, but I think it's okay as a kludge.
        choices=re.findall(r'(\\(Correct)?.hoice)','\n'.join(qql),re.DOTALL)
        choices=[cc for cc,bb in choices]
        assert all([cc in [r'\choice','\CorrectChoice'] for cc in choices])
        ianswer=[ii for ii,cc in enumerate(choices) if cc in [r'\CorrectChoice']]
        if not ianswer:
            answer='NOANSWER'
        else:
            assert len(ianswer)==1
            answer=list('ABCDEFGHIJ')[ianswer[0]]
        akey+=[answer]
        print answer
    keys={}
    for iver in range(N_EXAMS+1):
        keys[iver]= [qq for nn,qq in  sorted(zip(questionorders[iver],akey))]
    
    #Produce answer key: 
    with open(srcPathNoExt+'-answerkeys.tex','wt') as fkey:
        fkey.write(r"""
\documentclass{article}

\begin{document}
        \begin{tabular}{"""+'c|'*(N_EXAMS+2)+"""|}
  Question & """+ ' & '.join(['Version %d'%iexam for iexam in range(N_EXAMS+1)]) + r' \\ \hline'+"""
        """+'\n'.join(['Q %d & '%(iq+1) + ' & '.join([keys[iexam][iq] for iexam in range(N_EXAMS+1)]) + r' \\' for iq in range(len(mcqs))])+"""

\end{tabular}
\end{document}
""")


###createExamVersions('/home/cpbl/courses/201/quizzes/MT2-Nov2014.tex')
  
