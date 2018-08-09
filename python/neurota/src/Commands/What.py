# -------------------------------------------------------------------------
#  File:    What.py
#  Created: Thu May  7 23:59:12 2015
#  By:      Rick <rick@kiryoku>
#  Comment: 
# -------------------------------------------------------------------------

import os
import Display
import Tools

def parse_what(neurota, com_name, com):

	if len(com) != 4 or ':' not in com[3]:
  	  Tools.syntax_abort(neurota.args, "wrong # of commands in what statement",
    			                     "what is <attribute> of <topic:table>")
	elif com[2] != 'of':
  	  Tools.syntax_abort(neurota.args, "wrong # of commands in what statement",
    			                     "what is <attribute> of <topic:table>")		
  	else:
  		topic, table = Tools.split_topic(com[3])	
  		attribute = com[1]
    	if topic not in neurota.db.keys():
      		Tools.display("topic: %s not found!" % Tools.color(topic, "green"))
    	elif table not in neurota.db[topic].keys():
        	Tools.display("table: %s not found!" % Tools.color(table, "green"))
      	else:      		
      		found = False ; i = 0
        	for node in neurota.db[topic][table]:
        		if node.item == attribute:
        			max_len = len(node.item) ; found = True
        			Display.show_node(i, node, max_len, times=False, show_note=True)
        			break
        		i += 1
        	if not found:
        		Tools.display("%s not found!" % Tools.color(attribute, "green"))



