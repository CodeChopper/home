# -------------------------------------------------------------------------
#  File:    Search.py
#  Created: Mon Jul 21 16:29:49 2014
#  By:      Rick <rick@darkseid>
#  Comment: 
# -------------------------------------------------------------------------

import Display
import Tools
import re

def parse_search(neurota, com_name, com):
  
  # scan for optional keywords.  remove if found.

  times = Tools.scan_option("times", com)
  sort = Tools.scan_option("sort", com)

  if len(com) == 2 and com[0].find(':') != -1:
    topic, table = Tools.split_topic(com[0])
    pattern = com[1]
    if topic not in neurota.db.keys():
      Tools.display("topic: %s not found!" % Tools.color(topic, "green"))
    else:
      if table not in neurota.db[topic].keys():
        Tools.display("table: %s not found!" % Tools.color(table, "green"))
      else:
        search_results = []

        # Search title and note of node for search term.
        # If found, highlight the search pattern.

        reg = re.compile(pattern, re.IGNORECASE)

        for node in neurota.db[topic][table]:

          found_in_node = False
          # This searches the title of the node.
          if reg.search(node.item):
            found_in_node = True
            node.item = node.item.replace(pattern, Tools.color(pattern, "green"))

          # This searches the note of the node.
          i = 0
          for i in range(len(node.note)):
            if reg.search(node.note[i]):
              found_in_node = True
              node.note[i] = node.note[i].replace(pattern, Tools.color(pattern, "green"))

          if found_in_node:
            search_results.append(node)

        if len(search_results) == 0:
          print
          Tools.display("Search pattern: %s not found in:" % pattern)
        Display.show_table(topic, table, search_results, sort, times)    

  elif len(com) == 2 and com[0] == 'topics':

    pattern = com[1]
    reg = re.compile(pattern, re.IGNORECASE)

    for k in neurota.db.keys():
      if reg.search(k):
        Display.show_topic(k)

