"""
file ../beginners_guide/mySecondTree.py
"""

from Timba.TDL import *
import make_bookmark as BM

#-------------------------------------------------------------------

TDLCompileMenu(".mySecondTree():",
               TDLOption('copt_MeqFreq', 'add MeqFreq', True,
                         doc='if True, add a Meq.Freq node'),
               TDLOption('copt_MeqTime', 'add MeqTime', True,
                         doc='if True, add a MeqTime node'),
               TDLOption('copt_complex', 'add complex', True,
                         doc='if True, add a complex node'),
               TDLOption('copt_MeqGaussNoise', 'add MeqGaussNoise',
                         [0.0, 0.1, 1.0, 10.0], more=float,
                         doc='if True, a MeqGaussNoise(stddev)'),
               toggle='copt_mySecondTree')

#-------------------------------------------------------------------

def mySecondTree (ns):
  """
  This function makes a sum of leaf nodes with different behaviour,
  e.g. MeqTime, MeqToComplex, MeqGaussNoise etc.
  The leaf nodes may be specified by means of TDLOptions. 
  """

  # Make a list of the child nodes specified by TDLOptions:
  cc = []
  if copt_MeqFreq:
    cc.append(ns.MeqFreq << Meq.Freq())
  if copt_MeqTime:
    cc.append(ns.MeqTime << Meq.Time())
  if copt_complex:
    cc.append(ns.complex << Meq.ToComplex(ns << Meq.Freq(), ns << Meq.Time()))
  if copt_MeqGaussNoise>0:
    cc.append(ns.MeqGaussNoise << Meq.GaussNoise(stddev=copt_MeqGaussNoise))

  # Make sure that there is at least one child, and add them all:
  if len(cc)==0:
    cc.append(ns.zero << 0.0)
  rootnode = ns.sum << Meq.Add(*cc)

  # Finishing touches:
  BM.bookpage_nodes (cc+[rootnode], help=None,
                     name='mySecondTree nodes')
  rootnode = BM.bookpage_function_result (rootnode, func=mySecondTree, ns=ns, other=[])
  return rootnode
  
  
#-------------------------------------------------------------------
