# -------------------------------------------------------------------------
#  File:    Node.py
#  Created: Sat May 30 14:13:32 2015
#  By:      Rick <rick@kiryoku>
#  Comment: 
# -------------------------------------------------------------------------

class NeurotaNode(object):
  def __init__(self, 
               item=None,
               timestamp=None,
               note=None,
               value=None,
               cost=0.0,
               started=False,
               done=False):

    self.item = item
    self.note = note
    self.timestamp = timestamp
    self.value = value
    self.cost = cost
    self.started = started
    self.done = done
    self.annotation = None

