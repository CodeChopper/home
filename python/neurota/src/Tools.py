
# -------------------------------------------------------------------------
#  File:    Tools.py
#  Created: Sat Jul 19 23:23:43 2014
#  By:      Rick C <rick@raven>
#  Comment: 
# -------------------------------------------------------------------------

import datetime
import time
import os
import sys
import pickle
import subprocess as sub

# Custom class to display the attributes as a formatted table.

class ReportMaker:
  class ReportColumn:
    def __init__(self, label, minLength):
      self.label = label
      self.length = max(minLength, len(label))

  def __init__(self, symbol):
    self.dash = symbol
    self.title = None
    self.columns = []
    self.numTabs = 5

  def setTitle(self, title, numTabs):

    self.title = title
    self.numTabs = numTabs

  def addColumn(self, label, width):
    self.columns.append(self.ReportColumn(label, width))

  def getTitle(self):
    width = len(self.title)
    tabs = '\t'*self.numTabs

    title = ""
    title += "\n%s %s" % (tabs, str(self.dash*width).ljust(width))
    title += "\n%s %s" % (tabs, str(self.title).ljust(width))
    title += "\n%s %s" % (tabs, str(self.dash*width).ljust(width))
    title += "\n"

    return title

  def getHeaders(self):
    headers = "\n"
    #for col in self.columns:
    #  headers += " %s " % blue(str(self.dash*col.length).ljust(col.length))
    #headers += "\n"
    for col in self.columns:
      headers += " %s " % str(col.label).ljust(col.length)
    headers += "\n"
    for col in self.columns:
      headers += " %s " % blue(str(self.dash*col.length).ljust(col.length))

    return headers

  def getFooter(self):
    footer = "\n"
    for col in self.columns:
      footer += " %s " % blue(str(self.dash*col.length).ljust(col.length))
    footer += "\n"

    return footer

  def addData(self, rowList):
    
    rows = "\n"

    i = int(0)
    for col in self.columns:
      item = str(rowList[i])
      rows += " %s " % str(item[:col.length]).ljust(col.length)
      i += 1

    return rows
      
#
# support functions.
#

def justify(page, width, prefix):

	jpage = []
	all_words = []
	for line in page:
		words = line.split(' ')
		for w in words:
			all_words.append(w)

	new_line = [] ; line_count = 0
	for w in all_words:
		if line_count + len(w) <= width:
			new_line.append(w)
			line_count += len(w)
		else:
			jpage.append(new_line)
			new_line = [] ; line_count = 0
			# append word that didn't make the last sentence
			new_line.append(w)
			line_count += len(w)
	if new_line != []:
		jpage.append(new_line)

	# convert lists of words back to strings.
	# I know, I know, this isn't the right way to do it.

	justified = []
	for line in jpage:
		new_sentence = "%s " % prefix
		for w in line:
			new_sentence += w
			new_sentence += " "
		justified.append(new_sentence)

	return justified

def is_attribute(table):
  if len(table) == 1:
    return True
  else:
    return False

def split_topic(s):
  topic_table = s.split(':')
  return (topic_table[0], topic_table[1])

def split_item_path(p):
  topic_table_item = p.split(':')
  return (topic_table_item[0],
	  topic_table_item[1],
	  topic_table_item[2])

def nocolor(s, c):
  return s
  
def color(s, c):
  colormap = {"red": "\033[1;31m",
              "ured": "\033[4;31m",
              "bkred": "\033[41m",
              #
              "green": "\033[1;32m",
              "ugreen": "\033[4;32m",
              "bkgreen": "\033[42m",
              #
              "yellow": "\033[1;33m",
              "uyellow": "\033[4;33m",
              "bkyellow": "\033[43m",
              #
              "blue": "\033[1;34m",
              "ublue": "\033[4;34m",
              "bkblue": "\033[44m",
              #
              "magenta": "\033[1;35m",
              "umagenta": "\033[4;35m",
              "bkmagenta": "\033[45m",
              #
              "cyan": "\033[1;36m",
              "ucyan": "\033[4;36m",
              "bkcyan": "\033[46m",
              #
              "white": "\033[1;37m",
              "uwhite": "\033[4;37m",
              "bkwhite": "\033[47m",
              "reset": "\033[0m"}

  return "%s%s%s" % (colormap[c], s, colormap["reset"])

# some convenience functions.

def red(s):
  return color(s, "red")

def ured(s):
  return color(s, "ured")

def bkred(s):
  return color(s, "bkred")

def green(s):
  return color(s, "green")

def ugreen(s):
  return color(s, "ugreen")

def bkgreen(s):
  return color(s, "bkgreen")

def yellow(s):
  return color(s, "yellow")

def uyellow(s):
  return color(s, "uyellow")

def bkyellow(s):
  return color(s, "bkyellow")

def orange(s):
  return color(s, "orange")

def uorange(s):
  return color(s, "uorange")

def blue(s):
  return color(s, "blue")

def ublue(s):
  return color(s, "ublue")

def bkblue(s):
  return color(s, "bkblue")

def magenta(s):
  return color(s, "magenta")

def umagenta(s):
  return color(s, "umagenta")

def bkmagenta(s):
  return color(s, "bkmagenta")

def cyan(s):
  return color(s, "cyan")

def ucyan(s):
  return color(s, "ucyan")

def bkcyan(s):
  return color(s, "bkcyan")

def white(s):
  return color(s, "white")

def uwhite(s):
  return color(s, "uwhite")

def bkwhite(s):
  return color(s, "bkwhite")

def display(msg):
  print "%s - %s\n" % (bkcyan("[neurota]"), msg),

def edit():
  display("Temporary Edit mode. Enter single '.' on separate line to finish.")
  text = [] ; s = ""
  while s.strip() != ".":
    s = raw_input(": ")
    if s.strip() != ".":
      text.append(s)

  return text

def syntax_abort(incorrect, specific, correct):
  display("%s: %s" % (color("error detected", "red"), color(specific, "green")))
  display("There is a problem with this command -> '%s'" % color(incorrect, "green"))
  display("The correct syntax is %s" % color(correct, "yellow"))
  sys.exit(1)

def scan_option(option, command):
  option_found = False ; i = 0; 
  for c in command:
    if c == option:
      option_found = True
      del command[i]
      break
    else:
      i += 1

  return option_found

def yes_no(prompt):
  satisfied = False
  while not satisfied:
    msg = "[neurota] %s [y/n]?: " % prompt
    ans = raw_input(msg).lower()
    if ans in ['y', 'n']:
      satisfied = True      

  return {'y': True, 'n': False}[ans]

def split_time(t):

  hours = 0 ; mins = 0 ; secs = 0

  fields = t.split(' ')
  times = fields[0]
  am_pm = fields[1]

  if am_pm not in ['am', 'pm']:
    display("Time must end with am or pm.")
    sys.exit(1)

  if len(times) < 2:
    display("Time must have at least hours and mins.")
    sys.exit(1)

  tfields = times.split(':')		
  hours = int(tfields[0])
  mins  = int(tfields[1])
  if len(tfields) == 3:
    secs = int(tfields[2])	

  if am_pm == "pm":
    hours = hours + 12
		
  return (hours, mins, secs)

def split_date(d):

  year = 0 ; mon = 0  ; day = 0
  
  if len(d) != 10:
    display("error bad date!")
    sys.exit(1)
  else:
    mon = int(d[0:2]) ; day = int(d[3:5]) ; year = int(d[6:10])
	
  return (year, mon, day)

def run_unix(cmd):
  p = sub.Popen(cmd, shell = True, stdin=sub.PIPE, stdout=sub.PIPE, stderr=sub.STDOUT, close_fds=True)
  return p.stdout.readlines()

def years_from_days(days):
  years = float(days) / 365.25
  whole_years = math.floor(years)
  rem_days = (years - whole_years) * 365.25
  
  return (whole_years, rem_days)

def months_from_days(days):
  months = float(days)/30.416
  whole_months = math.floor(months)
  rem_days = (months - whole_months) * 30.416

  return (whole_months, math.floor(rem_days))

def elapsed(d):

  # d is a timedelta of elapsed time not a datetime. e will be a datetime.
  e = datetime.datetime(1,1,1) + d
  
  return color("(%d days, %02d:%02d:%02d)" % (d.days, e.hour, e.minute, e.second), "magenta")

def store_node(neurota, node_path, new_node):

  fields = node_path.split(':')
  topic = fields[0] ; table = fields[1]

  # needed this extra code to handle ':' in item.
  first_colon = node_path.find(':') + 1
  sec_part = node_path[first_colon:]
  sec_colon = sec_part.find(':') + 1
  item = sec_part[sec_colon:]

  node = None
  # search for  item
  i = 0 ; found = False
  for i in range(len(neurota.db[topic][table])):
    if neurota.db[topic][table][i].item == item:
      neurota.db[topic][table][i] = new_node
      found = True
      break
    else:
      i += 1

  if not found:
    neurota.db[topic][table].append(new_node)

  # commit changes to db
  neurota.commit()        

def get_node(neurota, node_path):
   
  fields = node_path.split(':')
  topic = fields[0] ; table = fields[1]

  # needed this extra code to handle ':' in item.
  first_colon = node_path.find(':') + 1
  sec_part = node_path[first_colon:]
  sec_colon = sec_part.find(':') + 1
  item = sec_part[sec_colon:]

  node = None
  # search for  item

  if topic not in neurota.db.keys():
    display("topic [%s] not found in db." % topic)
    sys.exit(1)
  elif table not in neurota.db[topic].keys():
    display("table [%s] not found in [%s]." % (table, topic))
    sys.exit(1)
    
  i = 0
  for i in range(len(neurota.db[topic][table])):
    if neurota.db[topic][table][i].item == item:
      node = neurota.db[topic][table][i]
      break
    else:
      i += 1

  return node




