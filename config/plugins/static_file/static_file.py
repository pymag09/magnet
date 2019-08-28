class Inventory:
  def __init__(self):
    self.nodes_list = []
  def match_nodes(self, filter_string):
    tmp_nodes = self.nodes_list
    for word in filter_string.split(' '):
        tmp_nodes = list(filter(lambda hs: word in hs['words'], tmp_nodes))
    return tmp_nodes
