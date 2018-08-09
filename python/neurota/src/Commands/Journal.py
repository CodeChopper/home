# -------------------------------------------------------------------------
#  File:    Journal.py
#  Created: Mon Jul 21 13:55:25 2014
#  By:      Rick <rick@darkseid>
#  Comment: 
# -------------------------------------------------------------------------

import datetime
import Commands.Add
import Tools

def parse_journal(neurota, com_name, com):
  if len(com) not in [2,3]:
    Tools.syntax_abort(neurota.args, "wrong # of commands in journal statement",
                       "journal to [table:list]")
    
  if com[0] == 'to':
    table_list = com[1]
    today = datetime.datetime.now()    
    title = today.strftime("%A %B %d %Y")
    add_com = [title, com[0], com[1]]
    Commands.Add.parse_add(neurota, com_name, add_com)
  else:
    print "special journaling not supported yet!"
    # one_day = datetime.timedelta(days=1)
    # day_earlier = in_date - one_day



