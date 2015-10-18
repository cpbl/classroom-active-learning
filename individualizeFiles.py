#!/usr/bin/python
import os

SP='/home/meuser/tmp/watermarks/'               # Scratch path
BLANKPAGE=SP+'pageblanche.pdf' # This is created below.
WWW=SP+'indivdist/'
HTPASSWD=SP+'.htpasswd'  # Actual server location  of the htpasswd

def createBlankPDFpage(): # This defaults to letter sized
    os.system("echo "" | ps2pdf -sPAPERSIZE=a4 - "+BLANKPAGE)


#### no use:     convert -background none -geometry +0+0 -fill \#000000 -pointsize 12 label:"From the library of..." -set label '' -page letter watermark.pdf


 
def createSingleWatermarkedPage(wtext,outfile='tmp_watermark_out.pdf',blankpage=BLANKPAGE):
    wtext=''.join([cc for cc in wtext if cc not in """'"'"""])
    os.system( ("""
  convert -size 200x80 xc:none -fill "#dddddd" \
          -gravity NorthWest -draw "text 10,10 '"""+wtext+"""'" \
          -gravity SouthEast -draw "text 5,15 '"""+wtext+"""'" \
          miff:- |\
    composite -tile - pageblanche.pdf  wmark_text_tiled.pdf
    """).replace('pageblanche.pdf',blankpage).replace('wmark_text_tiled.pdf',outfile))
  
def blend_PDFwatermarkPage_to_multipagePDF(infile='input_file.pdf',outfile='output_file.pdf',watermarkfile='wmark_text_tiled.pdf'):
    os.system("""
pdftk input_file.pdf stamp wmark_text_tiled.pdf output output_file.pdf
""".replace('input_file.pdf',infile).replace('output_file.pdf',outfile).replace('wmark_text_tiled.pdf',watermarkfile))


def create_individualized_files(PDFfile,classlistfile='/home/meuser/courses/201/classlist.csv',  forceUpdate=False):
    createBlankPDFpage()
    # Create a password file:
    os.system("""
    htpasswd -bc /home/meuser/htpasswd/.htpasswd dummyuser dummypassword 
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
            createSingleWatermarkedPage('Exclusively for '+adf['Student Name'],outfile=watermarkFile)
        print(' Creating individualized document for '+adf['Student Name'])
        os.system("""
        mkdir -p """+WWW+sID )
        blend_PDFwatermarkPage_to_multipagePDF(PDFfile,WWW+sID+'/'+PDFfileName+'%s.pdf'%sID,watermarkFile     )
        # Also append this student to a password file: 
        os.system("""
        htpasswd -b /home/meuser/htpasswd/.htpasswd """+sID +' '+adf['Email']+"""
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
        
def createOrAddToWebsite(): 
    # Use apache folder-level access control to require people to know email address and student ID to get their files:
    # How about: have a folder named with student ID for each student, and require their email address as the password? Can easily make a PHP page to generate URL from student ID
    # N.B.: we could put htaccess files in each student's directory. But much more efficient for the server, if you have access to the server, is to put this information into the apache server configuration.
    cmds="""
mkdir """+WWW+"""
create_individualized_files('tmp.pdf',forceUpdate=True)
"""

if __name__ == '__main__':
    create_individualized_files('tmp.pdf',classlistfile='/home/meuser/courses/201/classlist.csv',  forceUpdate=False)
