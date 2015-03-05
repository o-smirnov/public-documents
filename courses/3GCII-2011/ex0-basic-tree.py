# -*- coding: utf-8 -*-
#
#% $Id$ 
#
#
# Copyright (C) 2002-2007
# The MeqTree Foundation & 
# ASTRON (Netherlands Foundation for Research in Astronomy)
# P.O.Box 2, 7990 AA Dwingeloo, The Netherlands
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>,
# or write to the Free Software Foundation, Inc., 
# 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

from Timba.TDL import *
from Timba.Meq import meq

def _define_forest (ns, **kwargs):
  ## This defines a tree for
  ##    f = a*sin(t*cos(2*f))
  
  ns.b << 1;
  ns.c << 2;
  ns.x << Meq.Time;
  ns.y << Meq.Freq;
  
  a = ns.a << 297.61903062068177;
  # note that here we've declared a Constant node named "a", and that
  # the Python variable 'a' now refers _TO THAT NODE_...

  # ...so the variable can subsequently be used elsewhere:
  ns.f << a*Meq.Sin(ns.b*ns.x + ns.c*ns.y + 1);

  

def _test_forest (mqs, parent):
  domain = meq.domain(10,20,0,10)                            
  cells = meq.cells(domain,num_freq=200, num_time=100)
  request = meq.request(cells, rqtype='ev')
  result = mqs.execute('f',request);




Settings.forest_state.bookmarks = [
  record(name="result of 'f'",viewer='Result Plotter',udi='/node/f'),
];
Settings.forest_state.cache_policy = 100;
