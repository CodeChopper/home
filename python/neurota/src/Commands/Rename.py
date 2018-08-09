import sys
import Tools
import Commands.Move

def parse_rename_topic(neurota, source, target):

  if not neurota.db.has_key(source):
    Tools.display("Sorry topic %s does not exist in db. Aborting." % (Tools.color(source, "green")))
    sys.exit(1)

  if neurota.db.has_key(target):
    Tools.display("Sorry topic %s already exists in db. Aborting." % (Tools.color(target, "green")))
    sys.exit(1)

  # create new (target) topic, delete source topic.
  neurota.db[target] = neurota.db[source]
  del neurota.db[source]
  neurota.commit()
  Tools.display("Renamed topic: %s to %s" % (Tools.color(source, "green"),
                                             Tools.color(target, "green")))
  
def parse_rename_topic_table(neurota, source, target):

  (source_topic, source_table) = source.split(':')
  (target_topic, target_table) = target.split(':')

  if source_table == target_table:
    # if table names are equal this means that we are simply moving a table to another topic.
    com = [source, 'to', target_topic]
    Commands.Move.parse_move(neurota, 'move', com)
  else:
    # this means we're either renaming a table within the same topic or we're moving to a different topic with different table name.
    # check existance of arguments before performing rename.

    if not source_topic in neurota.db.keys():
      Tools.display("Sorry source topic %s does not exist in db. Aborting." % Tools.color(source_topic, "green"))
      sys.exit(1)
    else:
      if not source_table in neurota.db[source_topic].keys():
        Tools.display("Sorry source table %s does not exist in source topic: %s. Aborting." % (Tools.color(source_table, "green"), Tools.color(source_topic, "green")))
        sys.exit(1)
        
    if not target_topic in neurota.db.keys():
      # create blank topic
      neurota.db[target_topic] = {}
    else:
      if target_table in neurota.db[target_topic].keys():
        Tools.display("Sorry table %s already exists in topic: %s. Aborting." % (Tools.color(target_table, "green"), Tools.color(target_topic, "green")))
        sys.exit(1)

    # proceed for general renaming.
    neurota.db[target_topic][target_table] = neurota.db[source_topic][source_table]
    del neurota.db[source_topic][source_table]
    if len(neurota.db[source_topic]) == 0:
      del neurota.db[source_topic]
    neurota.commit()

    Tools.display("Renamed %s -> %s" % (Tools.color(source, "green"),
                                        Tools.color(target, "green")))

def parse_rename(neurota, com_name, com):

  if len(com) != 3:
    Tools.syntax_abort(neurota.args, "wrong # of commands in rename statement",
                       "rename <topic:table> to <new-topic:new-table>  (either topic and/or table can be new)")
  elif com[1] != 'to':
    Tools.syntax_abort(neurota.args, "missing 'to' in rename statement",
                       "rename <topic:table> to <new-topic:new-table>  (either topic and/or table can be new)")
  # proceed.

  source = com[0]
  target = com[2]

  # check to see if we're dealing with a topic or a topic:table.

  if ":" in source:
    source_type = "topic:table"
  else:
    source_type = "topic"

  if ":" in target:
    target_type = "topic:table"
  else:
    target_type = "topic"

  if source_type != target_type:
    Tools.syntax_abort(neurota.args, "both must be a topic or both must be topic:table",
                       "rename <topic:table> to <new-topic:new-table>")    
  else:
    if source_type == "topic":
      parse_rename_topic(neurota, source, target)
    else:
      parse_rename_topic_table(neurota, source, target)








    
    
