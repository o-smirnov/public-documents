"""
file:  ../beginners_guide/make_bookmark.py
Description:
- Various functions for making bookmarks.
- Used in the example scripts of the MeqTrees Beginners Guide.
- (Feel free to copy them for your own custom canibalization.)
-- import make_bookmarks as BM
--- BM.make_bookmark(node)          # bookmark a single node
--- BM.bookpage_nodes(nodes)        # bookmark a page of nodes
--- BM.bookpage_node(node)          # bookmark a page of multiple views of the same node
--- node = BM.bookpage_function_result(node, func)    # bookmark a page for a tree definition function
"""

from Timba.TDL import *

#==========================================================================
# Bookmark functions:
#==========================================================================

def make_bookmark (node, name=None, viewer='Result Plotter'):
  """
  The simplest possible bookmark function. Make a bookmark for the given node,
  using the specified viewer. If no name is specified, use the node name for
  the bookmark menu. NB: A single bookmark like this (i.e. not a bookpage) will
  be displayed in an empty panel of the current pookpage.
  """
  bm = bm_node_result (node, name=name, viewer=viewer)
  append_bookmark(bm)
  return None

#-------------------------------------------------------------  

def bookpage_nodes (nodes, name=None, help=None):
  """Make a (bookmark for a) bookpage for the results of the given
  list of node(s). If no name is provided, a default name is used.
  If help is provided, display it in an extra panel of the bookpage.
  """
  pp = []
  if isinstance(help,str):
    pp.append(bm_node_help(nodes[-1],help=help))
  for node in nodes:
    pp.append(bm_node_result(node))
  if not isinstance(name,str):
    name = nodes[0].name+' ...'
  make_bookpage(pp, name=name, nodes=nodes)
  return None

#-------------------------------------------------------------  

def bookpage_node (node, name=None, help=True, other=[],
                   show_result=True, inspector=False,
                   show_state=True):   
  """
  Make a bookpage with various views of the given node.
  If help is provided (string), attach it to its quickref_help field.
  If help is True (or string) make a panel for its quickref_help field.
  If show_result is True, make a panel with the Result Plotter.
  If inspector is True, make a panel with the Collections Plotter.
  If show_state is True, make a panel for its state record.
  If one or more other nodes are given, display them too.
  If a name is specified, use that for the bookmark in the menu.
  Otherwise use the node-name.
  """
  pp = []
  if show_result: pp.append(bm_node_result(node))
  if show_state: pp.append(bm_node_state(node))
  if help: pp.append(bm_node_help(node, help=help))
  if inspector: pp.append(bm_node_result(node, viewer='Collections Plotter'))
  for node in other:
    pp.append(bm_node_result(node))
  make_bookpage(pp, name=name)
  return None

#-------------------------------------------------------------  

def bookpage_function_result (node, func, help='', other=[], ns=None,
                              show_result=True, inspector=False,
                              show_state=True):
  """
  Make a bookmark for the result of (the rootnode returned by a)
  tree definition function (func). The bookmark name is the name
  of the function. The __doc__ string of the function is attached
  to the quickref_help field of the node, and displayed also.
  If one or more other nodes are given, display them too.
  If a nodescope (ns) is given, a MeqIdentity node is generated,
  with the name of the function. This new node is then returned.
  """
  name = node.name
  help += '<br>This is the __doc__ string of tree definition function:  '
  if getattr(func, 'func_name', None):
    name = str(func.func_name)+'()'
    help += name+':<br>'+str(func.__doc__)
  if ns:
    node = ns[name] << Meq.Identity(node)
    help += '<br><br><br><font color="black">'
    help += 'NB: This node: '+str(node)+' has been created for tree readability only.'
    help += ' It passes on the result of its child node: '+str(node.children[0][1])+'.'
    help += ' The only difference is its name.'
    help += '</font>'
  bookpage_node (node, name=name, help=help, other=other,
                 show_result=show_result, inspector=inspector,
                 show_state=show_state)   
  return node




#==========================================================================
# Helper functions for generation bookmark records:
#==========================================================================

def bm_node_result (node, name=None, viewer='Result Plotter'):
  """Return the bookmark record for the result of the given node,
  using the specified viewer. If a name is specified, use that
  for the bookmark name, otherwise use the node-name.
  """
  bm = record(name=str(name or node.name),
              viewer=viewer, udi='/node/'+node.name)
  return bm
  
#-------------------------------------------------------------  

def bm_node_state (node, name=None):
  """Return the bookmark record for the state record of the given node.
  """
  return bm_node_result (node, name=name, viewer='Record Browser')
  
#-------------------------------------------------------------  

def bm_node_inspector (node, name=None):
  """Return the bookmark record for the inspector of the given node.
  """
  return bm_node_result (node, name=name, viewer='Collections Plotter')
  
#-------------------------------------------------------------  

def bm_node_help (node, help=None, name=None):
  """Return the bookmark record for the quickref_help field of the
  given node. If necessary, a default quickref_help text is attached.
  If help is provided, it is attached to the quickref_help.
  """
  key = 'quickref_help'
  if not node.initrec().has_key(key):
    qhelp = '<font color="black">** quickref_help **</font><br>'
    node.initrec()[key] = qhelp
  qhelp = str(node.initrec()[key])
  if isinstance(help, str):
    qhelp += str(help)
  qhelp = insert_html(qhelp, color='blue')
  node.initrec()[key] = qhelp
  return bm_node_result (node, name=name, viewer='QuickRef Display')
  

#-------------------------------------------------------------  
#-------------------------------------------------------------  

def insert_html(qhelp, color='blue'):
  """Helper function to insert html tags into the given string.
  """
  ss = qhelp.split('\n')
  qhelp = '<font color="blue">'
  for s in ss:
    if s=='':
      s = '<br><br>'
    if '- ' in s[:5]:
      s = '<li>'+s
    s = s.replace('<<','<font color="red">&#60;&#60;</font>')
    s = s.replace('error','<font color="red">error</font>')
    s = s.replace('warning','<font color="magenta">warning</font>')
    # print '----',s[:10]
    qhelp += s
  qhelp += '</font>'
  return qhelp



#==========================================================================
# Helper functions for generating an actual bookmark:
#==========================================================================

def make_bookpage (pp, name=None, nodes=None):
  """
  Helper function to make a bookmark with the given name for a
  'bookpage' of the given list (pp) of bookmark records.
  Panel positions on the page are assigned automatically.
  """
  n = len(pp)            
  if n<=2:
    pos = [(0,0),(1,0)]
  elif n<=4:
    pos = [(0,0),(1,0),
           (0,1),(1,1)]
  elif n<=6:
    pos = [(0,0),(1,0),(2,0),
           (0,1),(1,1),(2,1)]
  elif n<=9:
    pos = [(0,0),(1,0),(2,0),
           (0,1),(1,1),(2,1),
           (0,2),(1,2),(2,2)]
  elif n<=12:
    pos = [(0,0),(1,0),(2,0),(3,0),
           (0,1),(1,1),(2,1),(3,1),
           (0,2),(1,2),(2,2),(3,2)]
  elif n<=16:
    pos = [(0,0),(1,0),(2,0),(3,0),
           (0,1),(1,1),(2,1),(3,1),
           (0,2),(1,2),(2,2),(3,2),
           (0,3),(1,3),(2,3),(3,3)]
  else:
    pos = [(0,0),(1,0),(0,1),(1,1)]
    s = '<font color="red"> Warning: Too many panels (>16) for the bookpage!</font>'
    pp = pp[:3]
    pp.append(bm_node_help(nodes[0], help=s))
    
  for i,bm in enumerate(pp):
    pp[i].pos = pos[i]
  if not isinstance(name,str):
    name = 'bookpage: '+str(n)+' nodes'
  bm = record(page=pp, name=str(name))
  append_bookmark(bm)
  return None
  
#-------------------------------------------------------------  

def append_bookmark(bm):
  """
  Make sure that the forest_state record hase a 'bookmarks' field
  of type list, and that the cache policy is set to 100 (=always).
  Then append the given bookmark (bm, single or page). 
  """
  rr = Settings.forest_state         # the forest state record
  key = 'bookmarks'                  # its relevant field name
  if not rr.has_key(key):
    rr.bookmarks = []
    rr.cache_policy = 100
  elif not isinstance(rr[key],list):
    rr.bookmarks = []
    rr.cache_policy = 100
  rr.bookmarks.append(bm)
  return None

#-------------------------------------------------------------



