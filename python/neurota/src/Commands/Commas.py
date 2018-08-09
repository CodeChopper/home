# -------------------------------------------------------------------------
#  File:    Commas.py
#  Created: Wed Dec  7 21:24:57 2016
#  By:      rick <rick@shark>
#  Comment: Implements the commas command which imports a comma-separated-value file.
# -------------------------------------------------------------------------

import Tools
import Commands.Add

def parse_commas(neurota, com_name, com):
	
	if len(com) != 3:
		Tools.syntax_abort(neurota.args, "wrong # of commands in commas statement",
						   "commas [filename] to [topic]")
	# open file

	fname = com[0]
	topic = com[2]
	with open(fname) as f:
		flines = f.readlines()

	attributes = flines[0].strip().split(',')
	attributes = [a.strip() for a in attributes]

	# first one is not used since that is used as the table name
	# in the command.
	attributes = attributes[1:]  
	numAttributes = len(attributes)

	# remove header line
	flines = flines[1:]

	print "Attributes"
	print attributes

	rows = []
	for line in flines:
		row = line.strip().split(',')
		row = [i.strip() for i in row]
		if len(row) == numAttributes + 1:
			rows.append(row)

	print "Items"
	print rows

	numRows = len(rows)
	for i in range(numRows):
		table = rows[i][0]
		for j in range(numAttributes):
			value = rows[i][j+1]
			cmd = "%s is %s to %s:%s" % (attributes[j], value, topic, table)
			com = cmd.split(' ')
			Commands.Add.parse_add(neurota, 'add', com)



