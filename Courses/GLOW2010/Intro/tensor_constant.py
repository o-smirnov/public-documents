"""
file ../beginners_guide/tensor_constant.py
"""

from Timba.TDL import *
import make_bookmark as BM

#-------------------------------------------------------------------

binops = ['Add','Multiply','Subtract','Divide','Pow',
          'ToComplex','Polar','Composer']

TDLCompileMenu(".tensor_constant():",
               TDLOption('copt_n1', 'n1', [3]+range(1,5),
                         doc='nr of elements in t1'),
               TDLOption('copt_n2', 'n2', [3]+range(1,5),
                         doc='nr of elements in t2'),
               TDLOption('copt_binop', 'binop', binops, more=str,
                         doc='operation to combine t1 and t2'),
               toggle='copt_tensor_constant')

#-------------------------------------------------------------------

def tensor_constant (ns):
  """
  This function demonstrates tensor nodes, i.e. nodes that have
  Results with multiple vellsets (scalar nodes have one vellset).

  First make tensors t1 and t2, each with a user-defined number
  of elements. Then combine them into t12 with a user-defined
  operation (e.g. 'Add'). Finally, t1,t12,t2 and t1 (again!)
  are 'composed' into a single tensor node with MeqComposer. 

  Since the elements are constants, which do not vary over the
  domain, the node Results are shown as lists of element values.
  This makes it easy to see what happens.

  Note what happens if t1 and t2 have different numbers of elements,
  especially if none of them is a scalar (one element).

  Note that MeqComposer just makes a list of the elements of its
  children, in the order in which they are given. The same child
  can be used more than once.

  Obviously, it would be nice if the elements would be labelled
  in the Result. This has been on Tony's list for some time.  
  """

  if not copt_tensor_constant:
    return None                          # not selected

  t1 = ns.t1 << Meq.Constant(range(copt_n1))
  t2 = ns.t2 << Meq.Constant(range(10,10+copt_n2))
  t12 = ns.t12 << getattr(Meq, copt_binop)(t1,t2)
  rootnode = ns['t1,t12,t2,t1'] << Meq.Composer(t1,t12,t2,t1)

  # Finishing touches:
  BM.bookpage_nodes ([t1,t2,t12,rootnode],
                     name='tensor nodes',
                     help=None)
  rootnode = BM.bookpage_function_result (rootnode, func=tensor_constant,
                                          inspector=False, ns=ns, other=[])
  return rootnode
  
  
#-------------------------------------------------------------------
