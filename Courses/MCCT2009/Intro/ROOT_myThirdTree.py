"""
file:  ../beginners_guide/ROOT_myThirdTree.py
... description of this module
... copyright statement
"""

from Timba.TDL import *
import tensor_constant as TC
import tensor_matrix as TM
import tensor_matrix22 as TM22
import execute_request as ER
import execute_sequence as ES
import make_bookmark as BM


#-------------------------------------------------------------  
# Required compile-time function: it defines the forest of trees of nodes.
# The global variable 'rootnode' represents the node that will receive the
# execution Request in the runtime function(s) '_tdl_job_xyz()' below.
#-------------------------------------------------------------  

TDLCompileMenu("ROOT_myThirdTree:",
               TC,     
               TM,
               TM22,
               toggle='copt_myThirdTree')

#-------------------------------------------------------------  

def _define_forest (ns, **kwargs):
  """
  The code of this function may be inspected in the code section
  of the MeqBrowser. The results of its tree building functions
  may be inspected via their own bookmark(s).

  ROOT_myThirdTree deals with tensor nodes, i.e. nodes that
  have Results with multiple vellsets. A tensor node may be composed
  from other (scalar and tensor) nodes, and it is also possible to
  extract one of its vellsets as the Result of a scalar node.

  This script also demonstrates the choice (by the user) between three
  different tree definition scripts, which demonstrate different aspects
  of tensor nodes.

  Some things to do before executing the tree:
  - Play with the TDLCompileOptions to generate different trees.
  - Browse these trees in the left section of this browser.

  Now execute a single request and inspect the results: 
  - Do you understand the node results in the various bookpages?
  - Inspect the state record again, especially the cache (result).

  Now execute a sequence of requests:
  - Play with the various TDLRuntimeOptions.
  
  """
  # NB: The tree definition functions return a node (i.e. subtree) if
  # they are selected, and None otherwise. The first valid node is used. 
  global rootnode       
  rootnode = TC.tensor_constant(ns)
  if not is_node(rootnode):
    rootnode = TM.tensor_matrix(ns)
  if not is_node(rootnode):
    rootnode = TM22.tensor_matrix22(ns)
  if not is_node(rootnode):
    rootnode = ns.dummy << -0.123456789

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
#  For testing without the meqbrowser, type '> python ROOT_myThirdTree.py'
#-------------------------------------------------------------  

if __name__ == '__main__':
  print '\n** Start of standalone test of: ROOT_myThirdTree.py:\n' 
  ns = NodeScope()
  _define_forest(ns)
  ns.resolve()
  print '\n** End of standalone test of: ROOT_myThirdTree.py:\n' 

#-------------------------------------------------------------  

