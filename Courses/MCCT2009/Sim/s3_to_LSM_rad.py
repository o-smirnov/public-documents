#!/usr/bin/python
# Examine structure of S3 query and pull out relevant columns 
# to generate MeqTrees LSM file (rad format)
#
# ianh 12.03.09
#

# Manually edit the s3string to your requirements

#
# LSM (build_from_extlist_dms)
# build local sky model from a list of extended sources
# 
#

#
# For purposes of constructing the LSM this centres the S3 query on (0,0)
# using the lens.centre file.
#
# Offsets based on the central pointing of the measurement set (in degrees)
# need to be added manually.
#

#
# Requirements:
# name RA Dec I Q U V Alpha Maj Min PA
#


import sys
import os
from math import log10, pi

# max sources to write -- sorted by brightness
MAX_SOURCES = 100;

def deg2dms(deg=0):
	"""
	Feed in an angle in degrees, it spits out deg, min, sec  (for Declinations)
	"""
	absdeg = abs(deg)
	minutes = (absdeg % 1)* 60
	seconds = (minutes % 1) * 60
	intdeg = absdeg - (absdeg % 1)
	intmin = minutes - (minutes % 1)
	if deg < 0.0:
		intdeg = -1*intdeg
		intmin = -1*intmin
		seconds = -1*seconds 
	return(intdeg, intmin, seconds)
	

def deg2hms(deg=0):
	"""
	Feed in an angle in degrees, it spits out hours, min, sec (for Right Ascensions)
	"""
	absdeg = abs(deg)
	hours = absdeg/15
	minutes = (absdeg % 1)* 60
	seconds = (minutes % 1) * 60
	inthours = hours - (hours % 1)
	intmin = minutes - (minutes % 1)
	if deg > 0.0:				# Greater than... MeqTrees left handed, S3 right
		inthours = -1*inthours
		intmin = -1*intmin
		seconds = -1*seconds 
	return(inthours, intmin, seconds)

def deg2rad(deg=0):
	"""
	Feed in an angle in degrees, it spits out radians
	"""
	rad = deg*2*pi/360.0
	return(rad)
	


if len(sys.argv) < 3 or not sys.argv[1].endswith('.tar.gz'):
	print "Usage: s3_to_LSM_rad.py <query_filename.tar.gz> <lsm filename>";
	sys.exit(1);
	
	
os.system("tar zxvf "+sys.argv[1]);
s3string = sys.argv[1][:-7];

structure_file = s3string+".query.structure"
result_file = s3string+".query.result"
window_file = s3string+".query.window"

centre_file = s3string+".lens.centre"

output_file = open(sys.argv[2],'wt');

required_cols = []

w = open(window_file,"r")
c = open(centre_file,"w")

window = w.readline()
window_split = window.split()

x_centre = (eval(window_split[1].strip(',')) + eval(window_split[0].strip(',')))/2.0
y_centre = (eval(window_split[2].strip(',')) + eval(window_split[3].strip(',')))/2.0

print >> c,x_centre
print >> c,y_centre

c.close()
w.close()

f = open(structure_file,"r")

structure = f.readline()
items = structure.split()

for i in range(len(items)):

	if items[i].strip(',') == 'source':
#		print "source in column ",i
		required_cols.append(i)
		source_col = i
	
	if items[i].strip(',') == 'right_ascension':
#		print "right ascension in column ",i
		required_cols.append(i)
		ra_col = i
		
	if items[i].strip(',') == 'declination':
#		print "declination in column ",i
		required_cols.append(i)
		dec_col = i

	if items[i].strip(',') == 'position_angle':
#		print "position angle in column ",i
		required_cols.append(i)
		pa_col = i
	
	if items[i].strip(',') == 'major_axis':
#		print "major axis in column ",i
		required_cols.append(i)
		maj_col = i

	if items[i].strip(',') == 'minor_axis':
#		print "minor axis in column ",i
		required_cols.append(i)
		min_col = i
		
	if items[i].strip(',') == 'i_1400':
#		print "i_1400 in column ",i
		required_cols.append(i)
		i_1400_col = i
	
f.close()

if len(required_cols) != 7:
	print "Required columns not present"
	sys.exit(-1)

sources = [];

# read list of sources from S3 file
f = open(result_file,"r")
for line in f:
	columns = line.split()
	if eval(columns[i_1400_col]) > -20:
#	for i in range(len(columns)):
#		print required_cols[i]
#		print columns[i]
		name = columns[source_col];
		ra = deg2rad(eval(columns[ra_col])+0)		# Manually insert RA of MS
		dec = deg2rad(eval(columns[dec_col])+25)	# Manually insert dec of MS
		I = (10.0**(eval(columns[i_1400_col])));
		Q = U = V = 0;
		spi = 0;
		smaj = eval(columns[maj_col])/206264.806;
		smin = eval(columns[min_col])/206264.806;
		pa   = eval(columns[pa_col])
                sources.append((name,ra,dec,I,Q,U,V,spi,smaj,smin,pa));
f.close()

# sort by flux (#3 in tuple)
sources.sort(lambda a,b:cmp(b[3],a[3]));

for src in sources[:MAX_SOURCES]:
    output_file.write("%s %.8f %.8f %.8g %.8g %.8g %8.g %8.g %8.g %8.g %8.g\n"%src);
     
output_file.close();

