# file: ../beginners_guide/execute_general_request.py

from Timba.TDL import *
from Timba.Meq import meq

request_counter = 0


#------------------------------------------------------------------------

def execute_general_request (mqs, node,
                             dsize=record(freq=(1,10), time=(1,10), L=(-1,1), M=(-1,1)),
                             ncells=record(num_freq=20, num_time=21, num_L=9, num_M=9),
                             parent=None, trace=False):
  """
  Execute the given node with a domain with an arbitrary number of dimensions,
  i.e. different from the default freq-time (see execute_request() above).
  The size of the domain in the various dimensions is specified by the record dsize.
  The number of cells for the various dimensions is specified by the record ncells.
  """
  global request_counter
  request_counter += 1
  rqid = meq.requestid(request_counter)
  domain = meq.gen_domain(**dsize)
  cells = meq.gen_cells(domain, **ncells)
  request = meq.request(cells, rqid=rqid)
  result = mqs.execute(node, request)
  return None


#------------------------------------------------------------------------
