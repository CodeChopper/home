# -------------------------------------------------------------------------
#  File:    Assign.py
#  Created: Sat Jul 19 23:24:20 2014
#  By:      Rick C <rick@raven>
#  Comment: 
# ------------------------------------------------------------------------- 

import datetime
import Node
import Tools

def parse_assign(neurota, com_name, com):

  if len(com) not in [5,7,10]:
    print "length of com is %d" % len(com)
    Tools.syntax_abort(com, "wrong # of commands in add statement",
                       "add symbol = value to [table:list] <on [date] at [time]>")
  if ':' not in com[4]:
    Tools.syntax_abort(com, "missing ':' in table:list",
                       "add symbol = value to [table:list] <on [date] at [time]>")
  if com[3] != "to":
    Tools.syntax_abort(com, "missing 'to' in add statement",
                       "add symbol = value to [table:list] <on [date] at [time]>")
  if len(com) == 7 and com[5] != "on":
    Tools.syntax_abort(com, "missing 'on' in add statement",
                       "add symbol = value to [table:list] <on [date] at [time]>")
    
  # made it past error checking!
  symbol = com[0] ; value  = com[2]
  topic, table = Tools.split_topic(com[4])

  # edit note portion of node interactively. 'add' command bypasses this action
  # and 'add' should be used for batch adds.

  if com_name == "add":
    note = []
  else:
    note = Tools.edit()
  
  # create what needs to be created along the way.
  if not neurota.db.has_key(topic):
    neurota.db[topic] = {}
  if not neurota.db[topic].has_key(table):
    neurota.db[topic][table] = []

  # add item
  if len(com) == 7 and com[5] == "on":
    y, m, d = Tools.dwSplitDate(com[6])
    timestamp = datetime.datetime(y, m, d)

  elif len(com) == 10 and com[5] == "on" and com[7] == "at":
    y, m, d = Tools.dwSplitDate(com[6])
    h, ms, s = Tools.dwSplitTime(com[8] + ' ' + com[9])
    timestamp = datetime.datetime(y, m, d, h, ms, s)
  else:                         
    timestamp = datetime.datetime.now()

  n = Node.NeurotaNode(symbol, timestamp, note, value)
  neurota.db[topic][table].append(n)
  num_items = len(neurota.db[topic][table])

  # commit changes to db
  neurota.commit()
  Tools.display('added "%s is %s" to %s:%s [%s now has %d item(s)]' % (symbol, value, topic, 
                                                                 table, table, num_items))
