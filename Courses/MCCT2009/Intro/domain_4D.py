"""
file ../beginners_guide/domain_4D.py
"""

from Timba.TDL import *
import make_bookmark as BM

#-------------------------------------------------------------------

TDLCompileMenu(".domain_4D():",
               TDLOption('copt_MeqFreq', 'add MeqFreq', True,
                         doc='if True, add a Meq.Freq node'),
               TDLOption('copt_MeqTime', 'add MeqTime', True,
                         doc='if True, add a MeqTime node'),
               TDLOption('copt_MeqGridL', 'add MeqGrid(axis=L)', True,
                         doc='if True, add a MeqGrid node for dimension L'),
               TDLOption('copt_MeqGridM', 'add MeqGrid(axis=M)', True,
                         doc='if True, add a MeqGrid node for dimension M'),
               toggle='copt_4D')

#-------------------------------------------------------------------

def domain_4D (ns):
  """
  This function akes a sum of leaf nodes with variation over
  different dimensions like the standard MeqTime and MeqFreq, but also
  some extra dimensions L and M. The latter are specified with the
  MeqGrid(axis='L'), which is a generalized version of MeqFreq/Time.
  When a request is issued with a 4D domain (freq,time,L,M), the
  result will be 4D also.
  """

  # Make a list of the child nodes specified by TDLOptions:
  cc = []
  if copt_MeqFreq:
    cc.append(ns.MeqFreq << Meq.Freq())
  if copt_MeqTime:
    cc.append(ns.MeqTime << Meq.Time())
  if copt_MeqGridL:
    cc.append(ns.MeqGridL << Meq.Grid(axis='L'))
  if copt_MeqGridM:
    cc.append(ns.MeqGridM << Meq.Grid(axis='M'))

  # Make sure that there is at least one child, and add them all:
  if len(cc)==0:
    cc.append(ns.zero << 0.0)
  rootnode = ns.sum << Meq.Add(*cc)

  # Finishing touches:
  BM.bookpage_nodes (cc+[rootnode], name='constituent nodes', help=None)
  rootnode = BM.bookpage_function_result (rootnode, func=domain_4D, ns=ns, other=[])
  return rootnode
  
  
#-------------------------------------------------------------------
