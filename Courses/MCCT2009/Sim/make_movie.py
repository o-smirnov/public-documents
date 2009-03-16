#!/usr/bin/python

import pyrap_tables
import sys
import os

# default arguments
data="CORRECTED_DATA"
msname = "demo.MS"
weight = "default";
stokes = "I";
select = "";
npix = 256;
cellsize = '1arcsec';
channel = 1
nframes = 120;
dt = 120;

# parse command line
for a in sys.argv:
  argspair=a.split("=",1);
  if len(argspair)>1:
    kw,value = argspair;
    print 'arg: ',kw,value;
    if kw == 'data':
      data = value;
    elif kw == "ms":
      msname = value;
    elif kw == "weight":
      weight = value;
    elif kw == "channel":
      channel = int(value);
    elif kw == "npix":
      npix = int(value);
    elif kw == "cell":
      cellsize = value;
    elif kw == "nframes":+
      nframes = int(value);
    elif kw == "dt":
      dt = int(value);

print "MS name is ",msname; 
# generate an output image name
imgname0 = msname;
os.system('rm -f *-slice*fits');

t0 = pyrap_tables.table(msname).getcol('TIME',0,1)[0]-1;

args0 = [ "lwimager","data="+data,"ms="+msname,"mode=channel","stokes=I","npix=%d"%npix,
"cellsize="+cellsize,"spwid=0","field=0","weight="+weight,
"chanmode=channel","nchan=1",
"chanstart=%d"%channel,"chanstep=1",
"img_chanstart=%d"%channel,"img_nchan=1",
"image=tmp.img" ];

for i in range(nframes):
  args = list(args0);
  args += [ "select=TIME >= %.12f AND TIME <= %.12f"%(t0+i*dt,t0+(i+1)*dt),
    "fits=%s-slice-%04d.fits"%(msname,i) ];
  print " ".join(args);
  os.spawnvp(os.P_WAIT,args[0],args);

# make karma cube
kcube = "%s-movie.kf"%imgname0;
os.system('images2karma *-slice*fits '+kcube);
os.system('rm -fr tmp.img *-slice*fits');
