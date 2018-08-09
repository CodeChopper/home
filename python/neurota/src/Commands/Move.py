import sys
import Tools

# This command is used to move tables between topics.

def parse_move(neurota, com_name, com):

  if len(com) != 3:
    Tools.syntax_abort(neurota.args, "wrong # of commands in move statement",
                       "move <topic:table> to <topic>")
  if com[1] != 'to':
    Tools.syntax_abort(neurota.args, "missing 'to' in move statement",
                       "move <topic:table> to <topic>")
  if not ":" in com[0]:
    Tools.syntax_abort(neurota.args, "First parameter needs to be topic:table",
                       "move <topic:table> to <topic>")
  if ":" in com[2]:
    Tools.syntax_abort(neurota.args, "Second parameter needs to be a topic not a topic:table",
                       "move <topic:table> to <topic>")

  source_topic_table = com[0]
  (source_topic, source_table) = source_topic_table.split(':')
  target_topic = com[2]

  # make sure source topic and table are really there.

  if source_topic not in neurota.db.keys():
    Tools.display("topic: %s not found!" % Tools.color(source_topic, "green"))
    sys.exit(1)
  if source_table not in neurota.db[source_topic].keys():
    Tools.display("table: %s not found!" % Tools.color(source_table, "green"))
    sys.exit(1)

  # make sure that target topic exists.
    
  if target_topic not in neurota.db.keys():
    Tools.display("Topic %s not found.  Creating topic %s." % (Tools.color(target_topic, "green"), Tools.color(target_topic, "green")))
    neurota.db[target_topic] = {}
  else:
    # make sure that the table doesn't already exist in the target topic.
    if source_table in neurota.db[target_topic].keys():
      Tools.display("Sorry a table named %s already exists in topic %s." % (Tools.color(source_table, "green"),
                                                                            Tools.color(target_topic, "green")))
  # copy information and delete
  neurota.db[target_topic][source_table] = neurota.db[source_topic][source_table]
  del neurota.db[source_topic][source_table]
  if len(neurota.db[source_topic]) == 0:
    del neurota.db[source_topic]
  # commit changes to db.
  neurota.commit()
  Tools.display("Moved table %s to topic %s" % (Tools.color(source_table, "green"),
                                                Tools.color(target_topic, "green")))







    
    
