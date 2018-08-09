# -------------------------------------------------------------------------
#  File:    Latex.py
#  Created: Mon Jul 21 13:45:33 2014
#  By:      Rick <rick@darkseid>
#  Comment: 
# -------------------------------------------------------------------------

import os, sys
import datetime
import Display
import Tools

def parse_latex(neurota, com_name, com):

  if len(com) != 4:
    Tools.syntax_abort(neurota.args, "wrong # of commands in latex command",
                       "latex to [filename] as [title]")
  if com[0] != 'to':
    Tools.syntax_abort(neurota.args, "missing 'to' in Latex command.",
                       "latex to [filename] as [title]")
  if com[2] != 'as':
    Tools.syntax_abort(neurota.args, "missing 'as' in Latex command.",
                       "latex to [filename] as [title]")
    
  fname = com[1]
  title = com[3]
  
  # Start outputting db to latex file.

  if os.path.exists(fname):
	Tools.display("file %s already exists. Aborting" % fname)
	sys.exit(1)
  else:
    Tools.display("Outputting latex to: %s with title: %s" % (fname, title))
    f = open(fname, "w")

    print >>f, "\documentclass[letterpaper,10pt]{book}"
    print >>f, "\\begin{document}"
    print >>f, "\\title{%s}" % title
    print >>f, "\maketitle"

    # No output the content, looping over every topic and table.

    for topic in neurota.db.keys():
      print >>f, "\section{%s}" % topic
      for table in neurota.db[topic].keys():
        print >>f, "\n\subsection{%s}" % table
        
        print >>f, "\\begin{enumerate}"
        for node in neurota.db[topic][table]:
          print >>f, "{\item {\\bf %s}" % (node.item),

          for l in node.note:
            print >>f, "%s" % l,

          print >>f, "}"

        print >>f, "\end{enumerate}"
          
    # Finish up.

    print >>f, "\n\n\n\n\n\n\n"
    print >>f, "\end{document}"             
    f.close()

