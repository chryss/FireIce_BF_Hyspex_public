#!/usr/bin/python
###############################################################################
#                                                                             #
#       Script for extracting all relevant info for ATCOR from HySpex         #
#       navigation file and ENVI header file for each flightline after        #
#       PARGE processing                                                      #
#                                                                             #
#   Script written for Python 3.6 and higher; should work with 2.7(untested)  #
#   Needs standard extension  plus:                                           #
#      asciitable                                                             #
#      numpy                                                                  #
#      Pysolar                                                                #
#                                                                             #
#   Originally written by Dr. Marcel Buchhorn                                 #
#   HyLab, GI, UAF                                                            #
#   Updated to Py 3 by Dr. Chris Waigl                                        #
#   Alaska EPSCoR Fire & Ice                                                  #
#                                                                             #
###############################################################################

from __future__ import division
from __future__ import print_function
from builtins import str
from past.utils import old_div
import asciitable
import numpy
import datetime
import pytz
from pysolar import solar
import os.path
import argparse

# getting the filename from the arguments and check if arguments exits which are needed
parser = argparse.ArgumentParser(description='This is a script for extracting important information from the flight line for PARGE.')
parser.add_argument('-i','--input', help='Input file name',required=True)
args = parser.parse_args()

# extracting imortant information from flight line navigation file
data = asciitable.read(args.input)

# saving the file name and location (excluding the extension) in a variable
filename = os.path.splitext(args.input)

position = int(round(old_div(len(data), 2),0))  # position of center of flight line

lat = data[position][2]
lon = data[position][1]

height = round(old_div(numpy.mean(data['col4']),1000),3) #avg height of flight line
heading = round(numpy.mean(data['col7']),2) #avg heading of flight line

# convert PGS seconds to UTC timestamp
day, hour = divmod((old_div(data[position][7], 86400)), 1)
hour, minu = divmod((old_div((hour * 86400), 3600)), 1)
minu, sec = divmod((old_div((minu * 3600),60)), 1)
sec = int(round(sec * 60,0))

# read out aquisition date and time from ENVI header
filename2 = '..\\RAD\\' + filename[0] + '_rad_bsq_float32.hdr'
f = open(filename2, 'r')
dataf = []
for line in f:
    line = line.strip()
    if "acquisition" in line:
        dataf.append(line)
f.close()

ad = dataf[0][19:]  # aquisition date
at = dataf[1][25:]  # aquisition time

d = datetime.datetime.strptime(ad + ' ' + at, '%Y-%m-%d %H:%M:%S')
d = pytz.utc.localize(d)

# replace flight line time stamp with time stamp of center of flight line
d3 = d.replace(hour = int(hour), minute = int(minu), second = int(sec))
if d.hour > d3.hour:
    d3 = d3 + datetime.timedelta(days=1)

# calculating sun position (check if we need topo height)
sza = round(90 - solar.get_altitude(lat, lon, d3), 2)

saa = solar.get_azimuth(lat, lon, d3)
if saa > -180:
    saa = round(180 - saa, 2)
elif saa < -180:
    saa = round((180 - saa) - 360, 2)

#output
filename3 = filename[0] + '_rad_f32_geo_flightdata.txt'  # set fielname for output file

with open(filename3, 'w') as g:
    g.write('# data for ATCOR processing of fligh line: ' + filename[0] + '_rad_f32_geo.bsq \n')
    g.write('############ \n')
    g.write ('basic data:\n')
    g.write ('ENVI header aquisition time       : {}.0Z\n'.format(d.strftime('%Y-%m-%dT%H:%M:%S')))
    g.write ('GPS aquisition time (UTC)         : {}.0Z\n'.format(d3.strftime('%Y-%m-%dT%H:%M:%S')))
    g.write ('\n')
    g.write ('Avg. lat: ' + str(lat) + '\n')
    g.write ('Avg. lon: ' + str(lon) + '\n')
    g.write ('\n')
    g.write ('\n')
    g.write('average flight height (km)   : ' + str(height) + ' \n')
    g.write('average heading (deg)        : ' + str(heading) + ' \n')
    g.write('sun zenith angle (SZA) (deg) : ' + str(sza) + ' \n')
    g.write('sun azimuth angle (SAA) (deg): ' + str(saa) + ' \n')

print('#### flight data extraction sucessful ####')
