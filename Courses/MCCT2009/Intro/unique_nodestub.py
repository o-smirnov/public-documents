"""
file:  ../beginners_guide/unique_nodestub.py
... description of this module
... copyright statement
"""

from Timba.TDL import *

stubtree = None                # global variable, used below

#-------------------------------------------------------------  

def unique_nodestub(ns, name, quals=[], kwquals={},
                    level=0, trace=False):
  """
  Function:  .unique_nodestub (ns, name, quals=[], kwquals={})
  

  Helper function to generate a unique nodestub with the given
  (node)name, qualifiers (quals) and keyword qualifiers (kwquals).
  If it exists already, its name will be changed recursively,
  until the resulting stub is not yet initialized.

  A stub becomes a node when it is initialized: stub << Meq.Node(..).
  But since our unique stub will already be initialized (see below),
  it must be qualified to generate nodes with unique names:
  - import unique_nodestub as UN
  - stub = UN.unique_nodestub(ns, name [, quals=[..]] [,kwquals={..}])
  - node = stub(qual1)(..) << Meq[nodeclass](...) 

  Since the stub is unique, chances are good that there will not be
  any nodename clashes if we generate nodes by qualifying it. This is
  not guaranteed, of course. But the chances are maximized by
  consistently generating ALL nodes by qualifying unique nodestubs. 
  
  The new nodestub will be initialized to an actual node so that it
  can be recognized later. To avoid a clutter of orphaned rootnodes
  in the MeqBrowser the initialized stubs are attached to a tree with
  a single (orphaned) rootnode named 'StubTree'.
  """
  
  if level>10:
    s = '** .unique_nodestub('+str(name)+','+str(quals)
    s += ','+str(kwquals)+', level='+str(level)+'):'
    s += ' max recursion level exceeded!'
    raise ValueError,s

  # Check the quals and kwquals:
  if not isinstance(quals,(list,tuple)):
    quals = [quals]
  if not isinstance(kwquals,dict):
    kwquals = dict()
    
  # Make the nodestub:
  stub = ns[name](*quals)(**kwquals)
  if trace:
    if level==0:
      print '\n** .unique_nodestub(',name,quals,kwquals,'):'
    prefix = '*'+(level*'.')
    print prefix,'-> stub =',str(stub),' stub.initialized() -> ',stub.initialized()

  # Make sure that the nodestub is unique (recursively):
  if stub.initialized():              # the stub represents an existing node
    nn = name+'|'                     # change the basename (better)
    stub = unique_nodestub(ns, nn, quals, kwquals,
                           level=level+1, trace=trace)

  # Found an uninitialized stub:
  if level==0:
    global stubtree
    if not is_node(stubtree):
      stubtree = ns['StubTree'] << Meq.Constant(-0.123456789)
    stubtree = stub << Meq.Identity(stubtree)
    if trace:
      print '    -->',str(stub),str(stubtree),str(stubtree.children[0][1])

  # Return the unique nodestub:
  return stub



#-------------------------------------------------------------  
#  For testing without the meqbrowser, type '> python unique_nodestub.py'
#-------------------------------------------------------------  

if __name__ == '__main__':
  print '\n** Start of standalone test of: unique_nodestub.py:\n' 
  ns = NodeScope()

  if 0:
    unique_nodestub(ns, 'a', trace=True)
    unique_nodestub(ns, 'a', trace=True)
    unique_nodestub(ns, 'a', trace=True)
    unique_nodestub(ns, 'a', trace=True)
    unique_nodestub(ns, 'a', trace=True)
    unique_nodestub(ns, 'a', trace=True)

  if 1:
    unique_nodestub(ns, 'b', trace=True)
    unique_nodestub(ns, 'b', quals=[7], trace=True)
    unique_nodestub(ns, 'b', quals=[7], trace=True)
    unique_nodestub(ns, 'b', quals=7, trace=True)
    unique_nodestub(ns, 'b', kwquals=dict(x=8), trace=True)
    unique_nodestub(ns, 'b', kwquals=dict(x=8), trace=True)
    unique_nodestub(ns, 'c', kwquals=dict(x=8), trace=True)
    
  print '\n** End of standalone test of: unique_nodestub.py:\n' 

#-------------------------------------------------------------  

