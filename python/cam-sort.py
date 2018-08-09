#!/usr/bin/env python

import os
import sys
import shutil

# We include the following two lines so that
# we do not need to have a DISPLAY set
# (so that it works from cron.)

import matplotlib
matplotlib.use('Agg')

from PIL import Image
from pylab import *

cam_dir = "/home/rick/webcam/data"
sorted_dir = "/home/rick/webcam/sorted"
dark_dir = "/home/rick/webcam/sorted/dark"

def DisplayException(msg):
    print()
    print("++++ %s ++++" % msg)
    print()

def isdark(h, t):
    """
    Detect if the histogram of an image appears to be very dark.
    h: histogram
    t: threshold for darkness
    """
    sum = 0.0
    for i in range(60, 128):
        sum += h[0][i]

    print("sum = %f" % float(sum))
                
    if sum < t:
        print("[DARK]")
        return True
    else:
        print("[LIGHT]")
        return False

def isdarkfile(f, threshold=5e4):
    """
    Detect if an image file (f) appears to be dark.
    """
    if not os.path.exists(f):
        DisplayException("Couldn't find image file: %s" % f)
        sys.exit(1)

    # read image to array convert to greyscale.
    im = array(Image.open(f).convert('L'))
    # get histogram.
    h = hist(im.flatten(),128)

    return isdark(h, threshold)
        
def readdate(f):
    """
    Parse date/time to year, month, day, time.
    """
        
    datestamp = f.split('.')[0]
    year = datestamp[0:4]
    month = datestamp[4:6]
    day = datestamp[6:8]
    time = datestamp[8:12]

    return (year, month, day, time)

def dropdir(d):
    """
    Change to a lower directory.  If it doesn't exist, create it.
    """
    if not os.path.isdir(d):
        print(" :: creating dir: %s" % d)
        os.mkdir(d)
    os.chdir(d)

def sortfile(year, month, day, f):
    """
    Put a file in the correct directory based on date/time stamp.
    """
    dropdir(year)
    dropdir(month)
    dropdir(day)
    cmd = "mv -v %s %s" % (joinpath(cam_dir, f), '.')
    print(os.getcwd())
    print(cmd)
    os.system(cmd)
    os.chdir(cam_dir)

def joinpath(d, f):
    return os.path.join(d, f)


# main, need try catch etc.

# check directories: if dark dir etc.

files = os.listdir(cam_dir)
os.chdir(cam_dir)
jpegs = [f for f in files if f.endswith('.jpeg')]
for j in jpegs:
        if isdarkfile(j):
            shutil.move(j, dark_dir)
        else:
            os.chdir(sorted_dir)
            year, month, day, time = readdate(j)
            sortfile(year, month, day, j)

