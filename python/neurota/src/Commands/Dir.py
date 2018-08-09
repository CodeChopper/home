# -------------------------------------------------------------------------
#  File:    Dir.py
#  Created: Tue Sep 16 11:32:51 2014
#  By:      Rick <rick@darkseid>
#  Comment: 
# -------------------------------------------------------------------------

import Tools
import Commands.Add

def parse_dir(neurota, com_name, com):

  title = None

  if len(com) not in [3,5]:
    Tools.display(neurota.args, "wrong # of commands in import statement",
                  "import [filename] to [table:list] < as [title] >")      
  if ':' not in com[2]:
    Tools.display(neurota.args, "missing ':' in table:list",
                  "import [filename] to [table:list] < as [title] >")
  if com[1] != "to":
    Tools.display(neurota.args, "missing 'to' in import statement",
                  "import [filename] to [table:list] < as [title] >")

  if len(com) == 5:
    if com[3] == "as":
      title = com[4]
    else:
      Tools.display(neurota.args, "missing 'as' in import statement",
                    "import [filename] to [table:list] < as [title] >")

  # open file and suck out lines.

  fname = com[0]
  flines = []
  with open(fname) as f:
    flines = f.readlines()

  # if as keyword was not used then import as items in table.
  # else import as the note of a node.

  if not title:
    for line in flines:
      com[0] = line.strip()
      if com[0] != "":
        Commands.Add.parse_add(neurota, 'insert', com)
  else:
    Tools.display("import as selected")

