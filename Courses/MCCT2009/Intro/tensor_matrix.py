"""
file ../beginners_guide/tensor_matrix.py
"""

from Timba.TDL import *
import make_bookmark as BM

#-------------------------------------------------------------------

TDLCompileMenu(".tensor_matrix():",
               toggle='copt_tensor_matrix')

#-------------------------------------------------------------------

def tensor_matrix (ns):
  """
  This function .tensor_matrix() demonstrates matrix operations.
  Matrices are 2-dimensional 'tensor' nodes, i.e. their Result
  contains multiple vellsets, for which a 2D shape has been defined:
  
  M23 = ns.M23 << Meq.Composer(children=[<6 nodes>], dims=[2,3])

  In this example, all matrix elements are constants, for easy
  inspection: the Result Plotter shows lists of element values.

  The node M32 is a tensor node with 6 (complex) elements, and
  a shape: dims=[3,2]. M23 is its conjugate transpose. Matrix
  multiplication yields the square matrices:
  - M22 = (M23 x M32)       (2x2)
  - M33 = (M32 x M23)       (3x3)

  Finally, the results of M23 and M32 are composed into a single
  tensor node. This gives an error, since the tensor shapes are
  different. Check this in the state record of node 'composer'.
  """

  if not copt_tensor_matrix:
    return None                          # not selected

  cc = []
  stub = ns.melem                        # uninitialized nodestub
  for i in range(6):
    cc.append(stub(i) << Meq.Constant(complex(i,i)))
  # cc = Timba.array.array([[1,2],[3,4],[5,6]])       # causes crash
  # M32 = ns.M32 << Meq.Constant(cc, dims=[3,2])      # dims ignored
  M32 = ns.M32 << Meq.Composer(children=cc, dims=[3,2])
  M23 = ns.M23 << Meq.ConjTranspose(M32)
  M22 = ns['M23xM32'] << Meq.MatrixMultiply(M23,M32)
  M33 = ns['M32xM23'] << Meq.MatrixMultiply(M32,M23)
  rootnode = ns.composer << Meq.Composer(M22,M33)

  # Finishing touches:
  BM.bookpage_nodes ([M32,M23,M22,M33,rootnode],
                     name='matrix nodes',
                     help=tensor_matrix.__doc__)
  rootnode = BM.bookpage_function_result (rootnode, func=tensor_matrix,
                                          inspector=False, ns=ns, other=[])
  return rootnode
  
  
#-------------------------------------------------------------------
