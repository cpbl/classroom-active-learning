#!/usr/bin/python
import os
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
    os.system("echo "" | ps2pdf -sPAPERSIZE=usletter - "+BLANKPAGE)


#### no use:     convert -background none -geometry +0+0 -fill \#000000 -pointsize 12 label:"From the library of..." -set label '' -page letter watermark.pdf


 
def createSingleWatermarkedPage(wtext,outfile='tmp_watermark_out.pdf',blankpage=BLANKPAGE,color='#dddddd'):
    wtext=''.join([cc for cc in wtext if cc not in """'"'"""])
    syscmd=("""
    convert -size 500x120 xc:none -stroke "#eeeeee" -fill "#eeeeee" -pointsize 24    -gravity NorthWest -draw "text 10,10 '"""+wtext+"""'"      -gravity SouthEast -draw "text 5,15 '"""+wtext+"""'"    miff:- |     composite -tile - pageblanche.pdf  wmark_text_tiled.pdf
    """).replace('pageblanche.pdf',blankpage).replace('wmark_text_tiled.pdf',outfile)
    #convert -size 200x80 xc:none -fill '"""+color+""""' -stroke  '"""+color+""""'    -gravity NorthWest -draw "text 10,10 '"""+wtext+"""'"      -gravity SouthEast -draw "text 5,15 '"""+wtext+"""'"    miff:- |     composite -tile - pageblanche.pdf  wmark_text_tiled.pdf
    ###  convert -size 200x80 xc:none -fill "#dddddd"     -gravity NorthWest -draw "text 10,10 '"""+wtext+"""'"      -gravity SouthEast -draw "text 5,15 '"""+wtext+"""'"    miff:- |     composite -tile - pageblanche.pdf  wmark_text_tiled.pdf
    os.system( syscmd)
    print(syscmd)
  
def blend_PDFwatermarkPage_to_multipagePDF(infile='input_file.pdf',outfile='output_file.pdf',watermarkfile='wmark_text_tiled.pdf'):
    os.system("""
pdftk input_file.pdf background wmark_text_tiled.pdf output output_file.pdf
""".replace('input_file.pdf',infile).replace('output_file.pdf',outfile).replace('wmark_text_tiled.pdf',watermarkfile))


def create_individualized_files(PDFfile,classlistfile='/home/meuser/courses/201/classlist.csv',  forceUpdate=False):
    createBlankPDFpage()
    # Create a password file, and delete the httpd.conf additions:
    os.system("""
    htpasswd -bc /home/meuser/htpasswd/.htpasswd dummyuser dummypassword 
    rm """+SP+""" addmeto-httpd.conf
    """)
    PDFfileName=os.path.splitext(os.path.split(PDFfile)[1])[0]
    from classroomActiveLearning import cpblClassroomTools
    clt=cpblClassroomTools()
    df=clt.loadClassList(classlistfile)
    for ii,adf in df.iterrows():
        sID=str(adf['ID'])
        watermarkFile=SP+'tmp_watermark_out_%s.pdf'%sID
        if not os.path.exists(watermarkFile) or forceUpdate:
            print(' Creating watermark for '+adf['Student Name'])
            createSingleWatermarkedPage('Exclusively for '+adf['Student Name'],outfile=watermarkFile,color='#ffffff')
        print(' Creating individualized document for '+adf['Student Name'])
        os.system("""
        mkdir -p """+WWW+sID )
        blend_PDFwatermarkPage_to_multipagePDF(PDFfile,WWW+sID+'/'+PDFfileName+'%s.pdf'%sID,watermarkFile     )
        # Also append this student to a password file: 
        print(' Creating individualized access for '+adf['Student Name']+' '+sID+' '+adf['Email'])
        os.system("""
        htpasswd -b /home/meuser/htpasswd/.htpasswd """+sID +' '+adf['Email'].split('@')[0]+"""
        """)
        # And tell the web server to protect this directory, allowing only the student. This addmeto-httpd.conf file will need to be appended to the server configuration (e.g. httpd.conf)
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
    
def emailEachStudent(): #Not finished
    """ We could email each student the file directly as an attachment, or we could (e.g. just once per term) email them the URL of a private http folder. Rather than use authentication, this could simply be a long random string. Maybe a hash of their sid?
"""
    clt=cpblClassroomTools()
    df=clt.loadClassList(classlistfile)
    for ii,adf in df.iterrows():
        sID=str(adf['ID'])
        email=adf['Email']
        muttcmd="""
mutt -s "Test from mutt" user@yahoo.com -a /tmp/file.jpg      < /tmp/message.txt 
"""
    
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
    create_individualized_files('tmp.pdf',classlistfile='/home/meuser/courses/201/classlist.csv',  forceUpdate=False)
  #Notes: 2015: .htpasswd file is /etc/meuser-htpasswd   I am using httpd.conf entries rather than .htaccess.

  # A nicer way to do all of this might be with .htaccess files without username:
#  http://stackoverflow.com/questions/12112917/htacess-protection-folder-without-username
 # Or else do the authentication using PHP rather than apache's.??   Is this useful: http://php.net/manual/en/features.http-auth.php 
