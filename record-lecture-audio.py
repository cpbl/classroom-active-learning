#!/usr/bin/python
"""
Usage:
  autorecordaudio <filepath> <minutes>

Options:
 -h --help   Show this screen
 --volume=<volume>   Specify ALSA input volume


Record audio. This is used in a cron script to automatically record audio during times I'm giving a lecture.
It's written for use in GNU/Linux OS.

filepath is just the folder location and a prefix. To this will be appended the date/time and ".wav".

Minutes is the duration of the lecture.

You can set this up to run automatically using "crontab -e" or gnome-schedule. For instance, the following records for 81 minutes every Tuesday and Thursday (2,4) starting at 13h04:

4 13 * * 2,4 /path-to-bin/classroom-active-learning/record-lecture-audio.py /path-to-saved-files/audio-lecture-   81 # JOB_ID_1
"""

import docopt
import time,os

arguments = docopt.docopt(__doc__)

outfile=arguments['<filepath>']+time.strftime("%Y%m%d-%H%M%S")+'.wav'
assert os.access(os.path.dirname(outfile), os.W_OK)
#os.path.exists(outfile)
seconds=int(arguments['<minutes>'])* 60
clc='arecord > %s  & sleep %d; kill $!'%(outfile, seconds)
os.system(clc)

