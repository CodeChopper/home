# -------------------------------------------------------------------------
#  File:    Add.py
#  Created: Fri Jul 18 11:43:29 2014
#  By:      Rick <rick@darkseid>
#  Comment: 
# -------------------------------------------------------------------------

import datetime
import Commands.Assign
import Tools
import Node

def parse_add(neurota, com_name, com):

  if 'is' in com:
    # process assignment statement separately
    Commands.Assign.parse_assign(neurota, com_name, com)
    return
  
  if len(com) not in [3,5,8]:
    Tools.syntax_abort(com, "wrong # of commands in add statement",
                       "add [string] to [table:list] <on [date] at [time]>")
  if ':' not in com[2]:
    Tools.syntax_abort(com, "missing ':' in table:list",
                       "add [string] to [table:list] <on [date] at [time]>")
  if com[1] != "to":
    Tools.syntax_abort(com, "missing 'to' in add statement",
                       "add [string] to [table:list] <on [date] at [time]>")
  if len(com) == 5 and com[3] != "on":
    Tools.syntax_abort(com, "missing 'on' in add statement",
                       "add [string] to [table:list] <on [date] at [time]>")
    
  # made it past error checking!
  item = com[0]
  topic, table = Tools.split_topic(com[2])

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
  if len(com) == 5 and com[3] == "on":
    y, m, d = Tools.split_date(com[4])
    timestamp = datetime.datetime(y, m, d)

  elif len(com) == 8 and com[3] == "on" and com[5] == "at":
    y, m, d = Tools.split_date(com[4])
    h, ms, s = Tools.split_time(com[6] + ' ' + com[7])
    timestamp = datetime.datetime(y, m, d, h, ms, s)
  else:                         
    timestamp = datetime.datetime.now()

  n = Node.NeurotaNode(item, timestamp, note)
  neurota.db[topic][table].append(n)
  num_items = len(neurota.db[topic][table])

  # commit changes to neurota.db
  neurota.commit()
  Tools.display('added "%s" to %s:%s [%s now has %d item(s)]' % (item, topic, 
                                                           table, table, num_items))



