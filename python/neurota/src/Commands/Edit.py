
# -------------------------------------------------------------------------
#  File:    Edit.py
#  Created: Tue Jul 22 22:48:25 2014
#  By:      Rick <rick@kiryoku>
#  Comment: 
# -------------------------------------------------------------------------

import os
import datetime

import Display
import Tools

def parse_edit(neurota, com_name, com):
  
  if len(com) != 3:
    Tools.syntax_abort(neurota.args, "wrong # of commands in edit statement",
                       "edit [topic:table:item] with [editor name]")      
  item_path = com[0]
  editor = com[2]
  
  cmd = "which %s" % editor
  editor_path = Tools.run_unix(cmd)[0].strip()
  if os.path.isfile(editor_path):
    Tools.display("using editor: %s" % editor_path)

  node = Tools.get_node(neurota, item_path)
  if not node:
    topic, table, item = Tools.split_item_path(item_path)
    timestamp = datetime.datetime.now()
    node = Node.NeurotaNode(item, timestamp)

  fname = ".neurotaedittmp"
  f = open(fname, "w")
  if node.note:
    for l in node.note:
      print >>f, l
  f.close()

  cmd = "%s %s" % (editor_path, fname)
  null = Tools.run_unix(cmd)

  # done editing?
  with open(fname) as f:
    lines = f.readlines()

  edited_note = []
  for l in lines:
    edited_note.append(l.strip())

  node.note = edited_note
  Tools.display("Finished editing. Storing the following note:")
  max_len = len(node.item)  
  Display.show_node(1, node, max_len+2)
  Tools.store_node(neurota, item_path, node)


