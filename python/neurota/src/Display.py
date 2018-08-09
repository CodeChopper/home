# -------------------------------------------------------------------------
#  File:    Display.py
#  Created: Sat Jul 19 23:23:22 2014
#  By:      Rick C <rick@raven>
#  Comment: 
# -------------------------------------------------------------------------

import datetime
import Tools
import random

def make_dashes(n):
  return n*'-'

def show_node(i, node, max_len, times=False, show_note=True):

  if node.value:
    item = "%s %s %s" % (node.item, Tools.color("is", "magenta"), node.value)
  else:
    item = "- %s -" % node.item
    
  if node.annotation:
    # if a special annotation has been inserted for this node before display,
    # show that instead of normal stuff.
    print "       %d %s %s %s)" % (i, Tools.color("|", "magenta"),
                                  node.annotation, item )
  else:
    if times:
      print "       %d %s [%s] %s" % (i, Tools.color("|", "magenta"),
                                       Tools.color(node.timestamp.strftime("%A %b %d %Y"), "green"), item )
    else:
      print "      %d %s %s" % (i, Tools.color("|", "magenta"), item)

  # handle notes.
      
  if show_note:
    # justified = Tools.justify(node.note, 40, "   ")
    # for l in justified:
    #   print "        %s" % Tools.red(l)
    for l in node.note:
      print  "          %s" % Tools.red(l)
  else:
    if node.note:
      first_line = node.note[0]
      portion = int(len(first_line)/1.8)
      print "\t %s %s" % (Tools.color("note: ", "ured"), "<%s>" % first_line[0:portion])
  

def has_attributes(db, topic):

  found_attributes = False
  for table in db[topic].keys():
    for node in db[topic][table]:
      if node.value:
        found_attributes = True
        break

  return found_attributes

def display_topic_table(db, topic):

  unique_attributes = set()
  for table in db[topic].keys():
    for node in db[topic][table]:
      if node.value:
        unique_attributes.add(node.item)

  report = Tools.ReportMaker('_')
  report.addColumn('object', 10)
  for a in unique_attributes:
    report.addColumn(a, 20)
    
  print report.getHeaders(),

  for table in db[topic].keys():
    vals_found = 0
    columnlist = []
    columnlist.append(table)
    for a in unique_attributes:
      columnval = "-"
      for node in db[topic][table]:
        if node.item == a:
          columnval = node.value
          vals_found += 1
      columnlist.append(columnval)

    if vals_found > 0:
      print report.addData( columnlist ),
  print report.getFooter(),

  
def show_topic(db, topic, hidden):
  topic_has_attributes = has_attributes(db, topic)
  if not hidden and topic_has_attributes:
    display_topic_table(db, topic)
  else:

    num_tables_per_row = 8
    num_dashes = 40 - len(topic)
    dash_char = '-'
    print " %s:" % topic,

    tables = db[topic].keys()
    tables.sort()
    ntables = len(tables)
    if ntables <= 2:
      midtable = 0
    else:
      midtable = (ntables / 2)

    # print "     ",
    for i in range(ntables):
      item_count = len(db[topic][tables[i]])
      print "%s:%s " % (Tools.blue(tables[i]), Tools.ured(str(item_count))),
      if not hidden:
        show_table(topic, tables[i], db[topic][tables[i]], sort=False, times=False, show_notes=False)

  print

def show_topic_hidden(db, topic):
  show_topic(db, topic, True)

def show_topic_expanded(db, topic):
  show_topic(db, topic, False)

def show_table(topic_name, table_name, table, sort=False, times=False, show_notes=True):
  full_table_name = "%s:%s" % (topic_name, table_name)

  # print "  [-]",
  # print "%s" % Tools.color(full_table_name, "blue")
  print 
  if sort:
    table.sort(key=lambda l: l.item)
    print "  <sorted>"

  # find longest item.
  max_len = 0
  for node in table:
    if len(node.item) > max_len: max_len = len(node.item)
    
  i = 0
  for i in range(len(table)):
    show_node(i+1, table[i], max_len+2, times, show_notes)
  print

def totlengthcmp(topicA, topicB):
  sumA = 0 ; sumB = 0
  
##   for table in neurota.db[topicA]:
##     sumA += len(table)
##   for table in neurota.db[topicB]:
##     sumB += len(table)

  sumA = len(topicA) ; sumB = len(topicB)

  if sumA > sumB:
    return 1
  elif sumA == sumB:
    return 0
  else:
    return -1

def show_topic_chunk(topics, db):

  report = Tools.ReportMaker('=')
  
  for t in topics:
    report.addColumn(t, 15)
  print report.getHeaders(),
  
  maxTables = 0
  # find max # of tables per topic.
  for t in topics:
    if len(db[t]) > maxTables:
      maxTables = len(db[t])
      
  numRows = maxTables
  for r in range(numRows):
    row = []
    for t in topics:
      tables = db[t].keys()
      tables.sort(key=lambda s: s.lower())
      if len(tables) >= r+1:
        row.append(tables[r])
      else:
        row.append("-")
    print report.addData(row), 

  print report.getFooter(),

def split_list(l, k):
	"""
	Return sublists of l of size k (plus remainder list if necessary).
	"""

	n = len(l)
	sublists = []
	nsubs = n / k
	nrems = n % k

	# little algo to split lists.

	i = int(0)
	while i < n:
		sublists.append(l[i:i+k])
		i += k

	return sublists

def show_tree(db):

  topics = db.keys()
  topics.sort()

  chunk_size = 5
  topic_chunks = split_list(topics, chunk_size)

  for c in topic_chunks:
    show_topic_chunk(c, db)

def show_banner(neurota):
  
  num_topics = len(neurota.db)
  num_items  = 0
  num_tables = 0
  for topic in neurota.db.keys():
    num_tables += len(neurota.db[topic])
    for table in neurota.db[topic].keys():
      num_items += len(neurota.db[topic][table])

  print
  timestamp = datetime.datetime.now()
  timeform = "%A %B %d %Y"
  stats = "[topics: %d   tables: %d   items: %d]" % (num_topics, num_tables, num_items)
  print "%s %s" % ("[neurota]", Tools.color(timestamp.strftime(timeform), "blue"))
  print "%s" % stats



  
  
