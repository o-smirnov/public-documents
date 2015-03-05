"""
file:  ../beginners_guide/ROOT_mySecondTree.py
... description of this module
... copyright statement
"""

from Timba.TDL import *
import mySecondTree as DT
import execute_request as ER
import execute_sequence as ES
import make_bookmark as BM


#-------------------------------------------------------------  
# Required compile-time function: it defines the forest of trees of nodes.
# The global variable 'rootnode' represents the node that will receive the
# execution Request in the runtime function(s) '_tdl_job_xyz()' below.
#-------------------------------------------------------------  

def _define_forest (ns, **kwargs):
  """
  The code of this function may be inspected in the code section
  of the MeqBrowser. The results of its tree building function
  mySecondTree() may be inspected via its own bookmark(s).

  Some things to do before executing the tree:
  - Play with the TDLCompileOptions to generate different trees.
  - Browse these trees in the left section of this browser.

  Now execute a single request and inspect the results: 
  - Invoke the Bookmark called 'mySecondTree()'.
  - Use the popup window (or TDL Exec) to execute this tree.
  - Do you understand the node results in the various bookpages?
  - Inspect the state record again, especially 'cache_result'.

  Now execute a sequence of requests:
  - Play with the various TDLRuntimeOptions.
  
  """
  global rootnode       
  rootnode = DT.mySecondTree(ns)
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
  The size and cells of the Request domain may be specified in the runtime menu.
  """
  return ER.execute_request(mqs, rootnode.name)

#.............................................................

def _tdl_job_execute_sequence (mqs, parent):
  """
  Execute a sequence of requests.
  """
  return ES.execute_sequence(mqs, rootnode.name)


#-------------------------------------------------------------  
#  For testing without the meqbrowser, type '> python ROOT_mySecondTree.py'
#-------------------------------------------------------------  

if __name__ == '__main__':
  print '\n** Start of standalone test of: ROOT_mySecondTree.py:\n' 
  ns = NodeScope()
  _define_forest(ns)
  ns.resolve()
  print '\n** End of standalone test of: ROOT_mySecondTree.py:\n' 

#-------------------------------------------------------------  

