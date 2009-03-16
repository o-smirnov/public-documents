# file: ../beginners_guide/execute_sequence.py

from Timba.TDL import *
import execute_request as ER

#------------------------------------------------------------------------

TDLRuntimeMenu("Parameters of the Request sequence:",
               TDLRuntimeOption('ropt_num_steps', 'nr of steps',
                                [3,10,30], more=int,
                                doc='nr of steps in the sequence'),
               TDLRuntimeOption('ropt_tstep', 'time-step (fraction)',
                                [1.0,0.0,0.1,0.5,-0.1], more=float,
                                doc='fraction of the domain time-size'),
               TDLRuntimeOption('ropt_fstep', 'freq-step (fraction)',
                                [0.0,1.0,0.1,0.5,-0.1], more=float,
                                doc='fraction of the domain freq-size'),
               )

#------------------------------------------------------------------------

def execute_sequence (mqs, node,
                      # num_steps=None, fstep=None, tstep=None,
                      parent=None, trace=False):
  """
  Execute a sequence of 'ropt_num_steps' requests, each shifted by
  the specified fraction of the domain (as specified in execute_request().
  """
  for i in range(ropt_num_steps):             
      ER.execute_request (mqs=mqs, node=node,
                          freq_offset=i*ropt_fstep,
                          time_offset=i*ropt_tstep,
                          parent=parent, trace=trace)
  return None

#------------------------------------------------------------------------
