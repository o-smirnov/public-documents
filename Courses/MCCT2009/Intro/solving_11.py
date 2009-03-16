"""
file ../beginners_guide/solving_11.py
"""

from Timba.TDL import *
import make_bookmark as BM

#-------------------------------------------------------------------

unops = [None,'Cos','Sin','Tan','Acos','Asin','Atan','Cosh','Sinh','Tanh',
         'Exp','Log','Abs','Negate','Invert','Sqrt','Pow2','Pow3','Pow8',
         'Ceil','Floor','Identity']
binops = ['Multiply','Add','Subtract','Divide','Pow',
          'ToComplex','Polar','Composer']

TDLCompileMenu(".solving_11():",
               TDLOption('copt_binop', 'binop', binops, more=str,
                         doc='ft = MeqFreq binop MeqTime'),
               TDLOption('copt_unop', 'unop', unops, more=str,
                         doc='lhs = unop(ft)'),
               TDLOption('copt_stddev', 'noise', [0.0,0.01,0.1,0.1,1.0,10.0], more=float,
                         doc='stddev of added Gaussian noise'),
               TDLOption('copt_fdeg', 'fdeg', range(6), more=int,
                         doc='degree of MeqParm freq poly'),
               TDLOption('copt_tdeg', 'tdeg', range(6), more=int,
                         doc='degree of MeqParm time poly'),
               TDLOption('copt_num_iter', 'num_iter', [3,1,2,5,10,20,100], more=int,
                         doc='number of iterations'),
               toggle='copt_solving')

#-------------------------------------------------------------------

def solving_11 (ns):
  """
  This function defines a solving tree in which the MeqSolver has a
  single MeqCondeq child, with children lhs and rhs.

  The left-hand-side (lhs) child is a user-defined subtree that produces
  a result that varies (optionally non-linearly) in freq and time:
  -  lhs = ft = binop(freq, time)    (e.g. binop = Multiply)
  -  [lhs = unop(ft)]                (e.g. unop = Cos)
  -  [lhs = noisy = lhs+noise]       (if stddev>0)

  The right-hand-side (rhs) child is a single MeqParm node that
  represents a polc, i.e. a 2D polynomial in freq and time: 
  -  rhs = MeqParm(0.0, shape=[tdeg+1,fdeg+1])

  The shape of the polc (i.e. the polynomial degree in freq and time)
  is specified by the user by means of TDLOptions.
  The solver solves for the polc coefficients, in several iterations.
  The result of the condeq node contains the residuals, i.e. rhs-lhs.
  With increasing polc polynomial degree, the residuals approach zero.
  """

  # Make the left-hand side (the copt_... are TDLCompileOptions):
  # First combine (Multiply or Add or ...) MeqFreq and MeqTime:
  lhs_name = 'f_'+copt_binop+'_t'
  lhs = ft = ns[lhs_name] << getattr(Meq,copt_binop)(ns<<Meq.Freq(), ns<<Meq.Time())

  if isinstance(copt_unop,str):
    # Optionally, apply a unary operation (e.g. Cos) on ft:
    lhs_name = copt_unop+'('+lhs_name+')'
    lhs = ns[lhs_name] << getattr(Meq,copt_unop)(lhs)

  if copt_stddev>0:
    # Optionally, add Gaussian noise:
    noise = ns.noise << Meq.GaussNoise(stddev=copt_stddev)
    lhs_name += '+noise'
    lhs = ns[lhs_name] << Meq.Add(lhs,noise)

  # Make the right-hand side:
  rhs = ns.rhs << Meq.Parm(0.0, shape=[copt_tdeg+1,copt_fdeg+1])

  # Make the MeqConde and the MeqSolver:
  condeq = ns.condeq << Meq.Condeq(rhs,lhs)
  rootnode = ns.solver << Meq.Solver(condeq, solvable=rhs,
                                     num_iter=copt_num_iter)

  # Finishing touches:
  help = 'lhs = '+str(copt_unop)+'(ft)'
  help += '\n  in which: ft = (freq '+str(copt_binop)+' time)'
  BM.bookpage_nodes ([ft,lhs,rhs,condeq,rootnode],
                     name='solving_11 nodes', help=help)
  rootnode = BM.bookpage_function_result (rootnode, func=solving_11,
                                          ns=ns, other=[condeq])
  return rootnode
  
  
#-------------------------------------------------------------------
