
import Tools
import Commands.Add

def parse_quick(neurota, com_name, com):
  if len(com) != 1:
    Tools.syntax_abort(neurota.args, "wrong # of commands in quick statement",
                       "quick <string>")
  com.append('to')
  com.append('quick:list')
  Commands.Add.parse_add(neurota, 'insert', com)

