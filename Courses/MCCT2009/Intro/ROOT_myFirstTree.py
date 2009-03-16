"""
file:  ../beginners_guide/ROOT_myFirstTree.py
... description of this module
... copyright statement
"""

from Timba.TDL import *
import myFirstTree as DT
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
  myFirstTree() may be inspected via its own bookmark(s).

  The fact that you are reading this means that you have compiled
  the tree, and invoked the Bookmark item '_define_forest()'.

  Some things to do before executing the tree:
  - Scroll through the Python/TDL code in the middle section.
  - Check this against Chapter 1 of the Beginners Manual. 
  - Invoke the various Bookmarks and inspect their panels.
  - Browse the tree itself in the left section of this browser.
  - Right and Left-click on a few nodes in the tree.

  Now execute the tree and inspect the results: 
  - Go back to the Bookmark called 'myFirstTree()'.
  - Use the popup window (or TDL Exec) to execute this tree.
  - Do you understand the node results in the various bookpages?
  - Inspect the state record again, especially the cache (result).

  Congratulations! You are no longer a Raw Beginner.
  Go on to ROOT_mySecondTree.py, which is more interesting.
  """
  global rootnode       
  rootnode = DT.myFirstTree(ns)
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


#-------------------------------------------------------------  
#  For testing without the meqbrowser, type '> python ROOT_myFirstTree.py'
#-------------------------------------------------------------  

if __name__ == '__main__':
  print '\n** Start of standalone test of: ROOT_myFirstTree.py:\n' 
  ns = NodeScope()

  if 1:
    _define_forest(ns)
    
  ns.resolve()
  print '\n** End of standalone test of: ROOT_myFirstTree.py:\n' 

#-------------------------------------------------------------  

