"""
file:  ../beginners_guide/ROOT_solving.py
... description of this module
... copyright statement
"""

from Timba.TDL import *
import solving_11 as DT
import make_bookmark as BM
import execute_request as ER

#-------------------------------------------------------------  
# Required compile-time function: it defines the forest of trees of nodes.
# The global variable 'rootnode' represents the node that will receive the
# execution Request in the runtime function(s) '_tdl_job_xyz()' below.
#-------------------------------------------------------------  

def _define_forest (ns, **kwargs):
  """
  The code of this function may be inspected in the code section
  of the MeqBrowser. The results of its tree building function
  solving_11() may be inspected via its own bookmark(s).
  """
  global rootnode       
  rootnode = DT.solving_11(ns)
  rootnode = BM.bookpage_function_result(rootnode, _define_forest,
                                         show_state=False, ns=ns)
  return None

#-------------------------------------------------------------  
# Runtime functions have names that begin with '_tdl_job_'.
# They will appear in the runtime menu (under the 'TDL exec' button).
#-------------------------------------------------------------  
  
def _tdl_job_execute_request (mqs, parent):
  """
  Execute by issuing a request to the node in the global variable 'rootnode'.
  """
  return ER.execute_request(mqs, rootnode.name)


#-------------------------------------------------------------  
#  For testing without the meqbrowser, type '> python ROOT_solving.py'
#-------------------------------------------------------------  

if __name__ == '__main__':
  print '\n** Start of standalone test of: ROOT_solving.py:\n' 
  ns = NodeScope()
  _define_forest(ns)
  ns.resolve()
  print '\n** End of standalone test of: ROOT_solving.py:\n' 

#-------------------------------------------------------------  

