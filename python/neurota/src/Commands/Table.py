# -------------------------------------------------------------------------
#  File:    Show.py
#  Created: Sat Jul 19 23:23:32 2014
#  By:      Rick C <rick@raven>
#  Comment: 
# -------------------------------------------------------------------------
import os

import Display
import Tools

def parse_table(neurota, com_name, com):

  # scan for optional keywords. remove if found.
  
  times = Tools.scan_option("times", com)
  sort = Tools.scan_option("sort", com)

  # experimentally clear screen before each display.
  # this will probably be removed.
  os.system('clear')
  #

  Display.show_banner(neurota)

  if len(com) == 0:
    Display.show_tree(neurota.db)
  elif len(com) == 1:

    if com[0] == "topics":

      topic_list = neurota.db.keys()
      print            
      print "  %s topics found." % len(topic_list)
      print
      for topic in topic_list:
        print "  %s" % Tools.color(topic, "green")
      print
      
    elif com[0] == "tables":

      num_items = 0
      num_tables = 0      
      topic_tables = []
      print
      
      for topic in neurota.db.keys():
        for table in neurota.db[topic].keys():
          num_tables += 1
          num_items = len(neurota.db[topic][table])
          topic_tables.append((topic, table, num_items))
          
      print "  %s tables found." % num_tables
      old_topic = ""
      for tt in topic_tables:
        topic = tt[0]
        table = tt[1]
        num_items = tt[2]
        if topic != old_topic:
          print "  |"
        print "  %s:%s (%d)" % (Tools.color(topic, "green"),
                                Tools.color(table, "green"), num_items)
        old_topic = topic
      print
      
    elif com[0] in neurota.db.keys():
      topic = com[0]
      Display.show_topic(neurota.db, topic)
    else:
      if com[0].find(':') != -1:
        topic, table = Tools.split_topic(com[0])
        if topic not in neurota.db.keys():
          Tools.display("topic: %s not found!" % Tools.color(topic, "green"))
        else:
          if table not in neurota.db[topic].keys():
            Tools.display("table: %s not found!" % Tools.color(table, "green"))
          else:
            Display.show_table(topic, table, neurota.db[topic][table], sort, times)


