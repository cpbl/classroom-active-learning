#!/usr/bin/python
"""
Usage:
 individualizeFiles.py <basepdf>  [options]

Options:
  -h --help      Show this screen.
  --scratchpath=<SP>   Path for temporary files
  -f --force-update    Overwrite/recalculate database tables and outputs
  -s --serial       Turn off parallel computation; useful for debugging 
  --classlistfile=<classlistfile>   Specify a csv file in McGill's format listing class enrollment, or the number of a hardcoded course

Name your source PDF file with a name ending in "-.pdf".  This way, the hyphen will separate the rest of the name from the students' identities.


To do: parallelize steps in stages.
"""
import docopt

import os
from classroomActiveLearning import cpblClassroomTools
try:
    from cpblUtilities.parallel import runFunctionsInParallel
except ImportError:
    def runFunctionsInParallel(funclist,names=None,parallel=None):
        for ff in funclist:
            if len(ff)==2:
                ff+=[{}]
            ff[0](ff[1],ff[2])
    fppstopher

"""
This spells out how to put each student's name as a watermark on an individualized version of a given PDF which you want to distribute in a way which discourages sharing of documents.
It also provides one or two ways to distribute them, either by automated individual emails or by directing people to individualized (hidden) folders accessed by http, optionally with authentication based on their student ID and name.

The tools assume you're using GNU/Linux, so probably MacOS can do it all with ease, also. 

CPBL 2015.
"""

"""
After creating individualized files, you could either email them individually to each student, or set up a web site to distribute them  with password (student ID and email address or name?) authentiation.
Sending files by individual email may be the simplest, or sending individual url links to each student (non-guessable URL? or a URL with authentication).
 I've found the best way to do this is using mutt.  I set up mutt to use an external SMTP server (which uses SSL encryption). Then a command-line mutt command uses it and my default email address to create/send an email. Swish

Revision plan:
 - copy/watermark each file in a folder "ToDistribute".
 - put watermarked files in individual, hidden folders by creating a random (hash, so reproducible) folder name for each.
 - That way, I could do my own authentication using PHP, or I could simply email a link to the folder for each student.

"""


SP='/home/meuser/tmp/watermarks/'               # Scratch path
BLANKPAGE=SP+'pageblanche.pdf' # This is created below.
WWW=SP+'indivdist/'
HTPASSWD=SP+'.htpasswd'  # Actual server location  of the htpasswd

def createBlankPDFpage(): # This defaults to letter sized
    os.system("echo "" | ps2pdf -sPAPERSIZE=letter - "+BLANKPAGE)


#### no use:     convert -background none -geometry +0+0 -fill \#000000 -pointsize 12 label:"From the library of..." -set label '' -page letter watermark.pdf


 
def createSingleWatermarkedPage(wtext,outfile='tmp_watermark_out.pdf',blankpage=BLANKPAGE,color='#dddddd'):
    wtext=''.join([cc for cc in wtext if cc not in """'"'"""])
    syscmd=("""
    convert -size 500x120 xc:none -stroke "%s" -fill "%s" -pointsize 24    -gravity NorthWest -draw "text 10,10 '"""%(color,color)+wtext+"""'"      -gravity SouthEast -draw "text 5,15 '"""+wtext+"""'"    miff:- |     composite -tile - pageblanche.pdf  wmark_text_tiled.pdf
    """).replace('pageblanche.pdf',blankpage).replace('wmark_text_tiled.pdf',outfile)
    #convert -size 200x80 xc:none -fill '"""+color+""""' -stroke  '"""+color+""""'    -gravity NorthWest -draw "text 10,10 '"""+wtext+"""'"      -gravity SouthEast -draw "text 5,15 '"""+wtext+"""'"    miff:- |     composite -tile - pageblanche.pdf  wmark_text_tiled.pdf
    ###  convert -size 200x80 xc:none -fill "#dddddd"     -gravity NorthWest -draw "text 10,10 '"""+wtext+"""'"      -gravity SouthEast -draw "text 5,15 '"""+wtext+"""'"    miff:- |     composite -tile - pageblanche.pdf  wmark_text_tiled.pdf
    print(syscmd)
    os.system( syscmd.encode('utf8'))
  
def blend_PDFwatermarkPage_to_multipagePDF(infile='input_file.pdf',outfile='output_file.pdf',tmpfile=None,watermarkfile='wmark_text_tiled.pdf',rasterize=True):
    if tmpfile is None:
        tmpfile=SP+'tmpPreRaster-'+os.path.split(outfile)[1]
    os.system("""
pdftk input_file.pdf background wmark_text_tiled.pdf output output_file.pdf
""".replace('input_file.pdf',infile).replace('output_file.pdf',tmpfile if rasterize else outfile).replace('wmark_text_tiled.pdf',watermarkfile)+"""
"""+rasterize* """
tmpfile2=$(mktemp).pdf
echo "   Rasterizing; ...  then optimizing to shrink pdf file..."
convert -render -density 300 """+tmpfile+""" $tmpfile2  
gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dNOPAUSE -dQUIET -dBATCH -sOutputFile="""+outfile+""" $tmpfile2
rm $tmpfile2
""")
    print(" Output to "+outfile)


def create_individualized_files(PDFfile,classlistfile='/home/meuser/courses/201/classlist.csv', showIDandName=True, rasterize=True, gray=None, forceUpdate=False, domax=99999):
    print('\n--------------------')
    createBlankPDFpage()
    # Create a password file, and delete the httpd.conf additions:
    os.system("""
    htpasswd -bc /home/meuser/htpasswd/.htpasswd dummyuser dummypassword 
    touch """+SP+"""addmeto-httpd.conf  &&  rm """+SP+"""addmeto-httpd.conf
    """)
    if gray is None:
        gray='#ffffff'
        gray='#dddddd'
    PDFfileName=os.path.splitext(os.path.split(PDFfile)[1])[0]
    df=CLT.loadClassList(classlistfile)
    funcs,    names=[],[]
    for ii,adf in df.iterrows():
        assert ii<domax
        sID=str(adf['ID'])
        watermarkFile=SP+'tmp_watermark_out_%s.pdf'%sID
        if not os.path.exists(watermarkFile) or forceUpdate:
            forceUpdate=True
            print(' Creating watermark for '+adf['Student Name'])
            funcs+=[[createSingleWatermarkedPage,['Exclusively for '+adf['Student Name']+(showIDandName)*('  '+sID)],dict(outfile=watermarkFile,color=gray)]]
            names+=['blank watermark'+adf['Student Name']]
            #createSingleWatermarkedPage('Exclusively for '+adf['Student Name']+(showIDandName)*('  '+sID),outfile=watermarkFile,color=gray)
    runFunctionsInParallel(funcs,names=names,parallel=PARALLEL)
    funcs,    names=[],[]    
    for ii,adf in df.iterrows():
        assert ii<domax
        sID=str(adf['ID'])
        watermarkFile=SP+'tmp_watermark_out_%s.pdf'%sID

        print(' Creating individualized document for '+adf['Student Name'])
        os.system("""
        mkdir -p """+WWW+sID )
        if not os.path.exists(SP+PDFfileName+'%s.pdf'%sID) or forceUpdate:
            forceUpdate=True
            funcs+= [[blend_PDFwatermarkPage_to_multipagePDF,[PDFfile,SP+PDFfileName+'%s.pdf'%sID,None, watermarkFile], dict(rasterize=rasterize )]]
            #blend_PDFwatermarkPage_to_multipagePDF(PDFfile,SP+PDFfileName+'%s.pdf'%sID,None, watermarkFile ],dict(rasterize=rasterize) ]]
            names+= [sID+'rasterize']
        # Now we also have to update the PDF metadata, so the title is something more sensible than what Imagemagick (?) made.
        with open(SP+'tmp_fileinfo_%s.info'%sID,'wt') as fout:
            fout.write("""
InfoKey: Title
InfoValue: Exclusively for """+adf['Student Name'].strip().encode('utf8')+""". No distribution permitted.
""")
    runFunctionsInParallel(funcs,names=names,parallel=PARALLEL)
    # The rest is fast enough to do in serial:
    for ii,adf in df.iterrows():
        assert ii<domax
        sID=str(adf['ID'])
        watermarkFile=SP+'tmp_watermark_out_%s.pdf'%sID

        if not os.path.exists(WWW+sID+'/'+PDFfileName+'%s.pdf'%sID) or forceUpdate:
            forceUpdate=True
            # The following also disallows copying and printing:
            os.system("""
pdftk """+SP+PDFfileName+'%s.pdf'%sID+""" update_info """+SP+'tmp_fileinfo_%s.info'%sID+""" output """+WWW+sID+'/'+PDFfileName+'%s.pdf'%sID+""" owner_pw "trivialtogetaroundthis" 
""")
        
        # Also append this student to a password file: 
        print(' Creating individualized access for '+adf['Student Name']+' '+sID+' '+adf['Email'])
        os.system("""
        htpasswd -b /home/meuser/htpasswd/.htpasswd """+sID +' '+adf['Email'].split('@')[0]+"""
        """)
        # And tell the web server (if we want to distribute things this way) to protect this directory, allowing only the student. This addmeto-httpd.conf file will need to be appended to the server configuration (e.g. httpd.conf)
        # N.B.: If you need to use .htaccess files, instead, just create one in each folder, here.
        with open(SP+'addmeto-httpd.conf','a') as fout:
            fout.write( """
<Directory """+WWW+sID+""">
AuthType Basic
AuthName "Enter your student ID. Then, as a password, enter your complete McGill email address."
AuthUserFile """+HTPASSWD+"""
Require user """+sID+"""
</Directory>
""")

def createHiddenFoldersForEachStudent(): # Not finished
    """ We could
 (e.g. just once per term) email them the URL of a private http folder. Rather than use authentication, this could simply be a long random string. Maybe a hash of their sid?
"""
    
def emailEachStudent(originalFileStem,subject=None,body=None,classlistfile='/home/meuser/courses/201/classlist-test.csv'):
#    emailEachStudent('tmp.pdf',
    """ We could email each student the file directly as an attachment, or we could (e.g. just once per term) email them the URL of a private http folder. Rather than use authentication, this could simply be a long random string. Maybe a hash of their sid?
"""
    df=CLT.loadClassList(classlistfile)
    emailbodyfile=SP+'emailmessage'+originalFileStem+'.txt'
    with open(emailbodyfile,'wt') as fout:
        fout.write('\n'+body+'\n')
    for ii,adf in df.iterrows():
        sID=str(adf['ID'])
        email=adf['Email']
        fileToSend=WWW+sID+'/'+originalFileStem+sID+'.pdf'
        muttcmd="""
"""+'mutt -s "'+subject.replace('"','')+'" '+email+' -a '+fileToSend +'  < '+emailbodyfile+"""
"""
        print(muttcmd),
        os.system(muttcmd)
        print('   ... sent!')
    
def createOrAddToWebsite():
    # This issn't done. Why not just email them instead? Use seendemail (rather than  sendmail) or mutt for easy command-line emailing using an external SMTP service, without changing your MTA (ie for me, without uninstalling postfix, which is what ssmtp requires)
    
    # 
    # Use apache folder-level access control to require people to know email address and student ID to get their files:
    # How about: have a folder named with student ID for each student, and require their email address as the password? Can easily make a PHP page to generate URL from student ID
    # N.B.: we could put htaccess files in each student's directory. But much more efficient for the server, if you have access to the server, is to put this information into the apache server configuration.
    cmds="""
mkdir """+WWW+"""
create_individualized_files('tmp.pdf',forceUpdate=True)
"""

if __name__ == '__main__':
    try:
        # Parse arguments, use file docstring as a parameter definition
        arguments = docopt.docopt(__doc__)
        basepdf = arguments['<basepdf>']
        forceUpdate =  arguments['--force-update'] == True
        classlistfile= arguments['--classlistfile']
        PARALLEL=not arguments['--serial']
        CLT=cpblClassroomTools(classlistfile)
        print arguments
    # Handle invalid options
    except docopt.DocoptExit as e:
        print e.message
        stopthen
    assert basepdf.endswith('.pdf')
    
    create_individualized_files(basepdf,classlistfile='/home/meuser/courses/201/classlist.csv',  forceUpdate=forceUpdate)
    emailEachStudent(os.path.split(basepdf)[1][:-4],subject="[ENVR 201] Solutions for MT multiple choice",body="Hello. I'm sending you a copy of the answers to the multiple choice questions on the last midterm. The attached file is individualized; please do not share it.",classlistfile='/home/meuser/courses/201/classlist.csv')


    stophere
    """
    #'MT2-MC-.pdf'
    create_individualized_files('MT2-MC-.pdf',classlistfile='/home/meuser/courses/201/classlist.csv',  forceUpdate=False, )
    emailEachStudent(basepdf[:-4],subject="[ENVR 201] Solutions for MT multiple choice",body="Hello. I'm sending you a copy of the answers to the multiple choice questions on the last midterm. The attached file is individualized; please do not share it.",classlistfile='/home/meuser/courses/201/classlist.csv')
    """
    #Notes: 2015: .htpasswd file is /etc/meuser-htpasswd   I am using httpd.conf entries rather than .htaccess.

  # A nicer way to do all of this might be with .htaccess files without username:
#  http://stackoverflow.com/questions/12112917/htacess-protection-folder-without-username
 # Or else do the authentication using PHP rather than apache's.??   Is this useful: http://php.net/manual/en/features.http-auth.php 
