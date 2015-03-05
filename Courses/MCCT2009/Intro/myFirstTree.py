# file ../beginners_guide/myFirstTree.py


from Timba.TDL import *
import make_bookmark as BM


#-------------------------------------------------------------------

def myFirstTree (ns):
  """
  This function defines a tree for: f(x,y) = alpha*sin(b*x+c*y+1.2)
  """

  # This defines a leaf node named "alpha" of class Meq.Constant, 
  # initialized with the given value
  # (i.e. the Fine Structure Constant, in appropriate units)
  alpha = ns.alpha << Meq.Constant(value=297.61903062068177)
  
  # It is easier to just do <<(numeric value).
  # This implicitly defines MeqConstant nodes.
  b = ns.b << 1
  c = ns.c << 2.0
  x = ns.x << -1
  y = ns.y << 1.5
  
  # Multiply(the results of) two nodes: bx = b*x, the hard way:
  # This defines a node named "bx" of class Meq.Multiply, with two children
  bx = ns.bx << Meq.Multiply(b,x)
  
  # Multiply (the results of) two nodes: cy = c*y, the easy way: 
  # Arithmetic on nodes implicitly defines the "right" things
  cy = ns.cy << c * y
  
  # Add (the results of) three nodes: sum = b*x+c*y+1, the easy way
  # This will implictly create a Meq.Constant node for the "1.2", etc.
  sum = ns.sum << bx + cy + 1.2
  
  # The final result. Note the alternative way of specifying the node name.
  # Note that an intermediate node of class Meq.Sin is created automatically
  rootnode = ns['f(x,y)'] << alpha * Meq.Sin(sum)
  
  # NB: We could have accomplished the same thing with:
  # rootnode = ns['f(x,y)'] << ns.alpha*Meq.Sin(ns.b*ns.x + ns.c*ns.y + 1.2)

  # Finishing touches:
  BM.bookpage_nodes ([alpha,b,c,x,y,bx,cy,sum,rootnode],
                     name='myFirstTree nodes',
                     help='f(x,y) = alpha * sin(b*x + c*y + 1.2)')
  rootnode = BM.bookpage_function_result (rootnode, func=myFirstTree,
                                          ns=ns, other=[bx,cy])
  return rootnode
  
#-------------------------------------------------------------------
