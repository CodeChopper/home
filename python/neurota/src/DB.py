# -------------------------------------------------------------------------
#  File:    DB.py
#  Comment: This contains the implementation of the actual database.
# -------------------------------------------------------------------------

import os
import sys
import time
import pickle
import jsonpickle

class NeurotaDB(object):

  def __init__(self, path, args):
    """
    Init the database.  If the db exists (comprised of topic files then
    load them back into Python memory.
    """
    self.db = {}      
    self.path = path
    self.args = args

    # Load topics for existing database (JSON).
    topic_files = [f for f in os.listdir(path) if f.endswith('json')]
    for topic_fname in topic_files:
      topic_name = topic_fname.split('.')[0]
      with open(os.path.join(self.path, topic_fname)) as f:
        frozen = f.read()
        topic_dict = jsonpickle.decode(frozen)
        self.db[topic_name] = topic_dict

  def commit(self):
    """
    For certain commands, we commit the database.  Since the persistence
    is file-based, this means deleting all current topic files and rewriting them.
    """
    for i in range(2):
      for c in ['\\', '-', '/', '-']:
        print "%c\b\b" % c,
        sys.stdout.flush()
        time.sleep(0.03)

    # del existing topic files before saving with new.
    clean_cmd = "rm -f %s/*" % self.path
    os.system(clean_cmd)

    # save all topics to files (JSON).
    for k in self.db.keys():
      topic_fname = os.path.join(self.path, "%s.json" % k)
      with open(topic_fname, "w") as f:
        frozen_obj = jsonpickle.encode(self.db[k])
        f.write(frozen_obj)

