"""
file ../beginners_guide/tensor_matrix22.py
"""

from Timba.TDL import *
import make_bookmark as BM

#-------------------------------------------------------------------

TDLCompileMenu(".tensor_matrix22():",
               toggle='copt_tensor_matrix22')

#-------------------------------------------------------------------

def tensor_matrix22 (ns):
  """
  The function .tensor_matrix22() demonstrates operations on
  2x2 matrices, like the cohaerency and Jones matrices used
  in the radio astronomical Measurement Equation.

  The 2x2 matrix M has elements M11,M12,M21 and M22.
  - M11 = complex(freq,time)
  - M12 = 0
  - M21 = 0
  - M22 = complex(time,freq)

  At this moment, MeqTrees only offers matrix inversion for
  2x2 matrices, which is sufficient for radio astronomy.
  Minv is the inverse of M, and the product MMinv = (M x Minv)
  should be unity (i.e. complex(1,0)) for all domain cells.
  """

  if not copt_tensor_matrix22:
    return None                          # not selected

  freq = ns << Meq.Freq()
  time = ns << Meq.Time()
  M11 = ns.M11 << Meq.ToComplex(freq,time)
  M22 = ns.M22 << Meq.ToComplex(time,freq)
  M = ns.M << Meq.Matrix22(M11,0,0,M22)
  Minv = ns.Minv << Meq.MatrixInvert22(M)
  MMinv = ns.MMinv << Meq.MatrixMultiply(M,Minv)

  # Finishing touches:
  BM.bookpage_nodes ([M11,M22,M,Minv,MMinv],
                     name='matrix22 nodes',
                     help=tensor_matrix22.__doc__)
  # BM.make_bookmark (Minv, name='Minv', viewer='Collections Plotter')
  return MMinv
  
  
#-------------------------------------------------------------------
