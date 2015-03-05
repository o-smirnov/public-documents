# file: ../beginners_guide/execute_request.py

from Timba.TDL import *
from Timba.Meq import meq

request_counter = 0

#------------------------------------------------------------------------

TDLRuntimeMenu("Parameters of the Request domain:",
               TDLOption('ropt_num_freq', 'nr of freq channels',
                         [10,11,1,20,50,100], more=int,
                         doc='nr of domain cells in the freq direction'),
               TDLOption('ropt_num_time', 'nr of time channels',
                         [11,10,1,20,50,100], more=int,
                         doc='nr of domain cells in the time direction'),
               TDLMenu("time size:",
                       TDLOption('ropt_t1', 'start time (s)',
                                 [1.0,0.0,-1.0], more=float,
                                 doc='min time (s) of the domain (edge)'),
                       TDLOption('ropt_t2', 'stop time (s)',
                                 [10.0,1.0], more=float,
                                 doc='max time (s) of the domain (edge)'),
                       ),
               TDLMenu("freq size:",
                       TDLOption('ropt_f1', 'start freq (Hz)',
                                 [1.0], more=float,
                                 doc='min freq (Hz) of the domain (edge)'),
                       TDLOption('ropt_f2', 'stop freq (Hz)',
                                 [11.0], more=float,
                                 doc='max freq (Hz) of the domain (edge)'),
                       )
               )

#------------------------------------------------------------------------


def execute_request (mqs, node,
                     # f1=None, f2=None, t1=None, t2=None,
                     # num_freq=None, num_time=None,
                     freq_offset=0.0, time_offset=0.0,
                     parent=None, trace=False):
  """
  Execute the given node with the specified time-freq domain (size and cells)
  The (optional) freq and time offsets are fractions of the domain size. 
  """
  
  foffset = (ropt_f1-ropt_f2)*freq_offset
  toffset = (ropt_t1-ropt_t2)*time_offset
  domain = meq.domain(ropt_f1+foffset, ropt_f2+foffset,
                      ropt_t1+toffset, ropt_t2+toffset)                            
  cells = meq.cells(domain, num_freq=ropt_num_freq,
                    num_time=ropt_num_time)

  global request_counter
  request_counter += 1
  rqid = meq.requestid(request_counter)
  request = meq.request(cells, rqid=rqid)
  result = mqs.execute(node, request)
  return None

#------------------------------------------------------------------------
