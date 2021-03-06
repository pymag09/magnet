import sys
from os import environ

try:
    import consul
except ImportError as e:
    print('Required module is missing. Use "pip3 install python-consul" to resolve the problem.')
    sys.exit(1)
import configparser

class PluginConfigNotFound(Exception):
    pass


class Inventory:
    def __init__(self):
        self.nodes_list = []
        self.consul_api = self.get_consul_api()

        if self.consul_api:
            self.load_data_for_datacenter()

    @staticmethod
    def get_consul_api():
        config = configparser.ConfigParser()
        consumed_files = config.read('%s/.magnet/consul.conf' % str(environ['HOME']))
        if not consumed_files:
            raise PluginConfigNotFound('Config file for consul plugin is missing.')
        host = config['DEFAULT']['host']
        port = config['DEFAULT']['port']
        token = config['DEFAULT']['token']
        scheme = config['DEFAULT']['scheme']
        return consul.Consul(host=host, port=port, token=token, scheme=scheme)

    def load_all_data_consul(self):
        datacenters = self.consul_api.catalog.datacenters()
        return datacenters

    def load_data_for_datacenter(self):
        for dc in self.load_all_data_consul():
            index, nodes = self.consul_api.catalog.nodes(dc=dc)
            for node in nodes:
                node_index, node_data = self.consul_api.catalog.node(node['Node'], dc=dc)
                key = "%s/%s/%s" % ("ansible/groups", dc, node['Node'])
                kv_index, groups = self.consul_api.kv.get(key)
                tags = ' '.join(['%s %s' % (s['Service'],
                                            ' '.join(s['Tags'])) for s in node_data['Services'].values()])
                self.nodes_list.append({'host': node['Address'],
                                        'words': '%s %s %s' % (groups.get('Value') if groups else '',
                                                               tags,
                                                               node['Address'])})

    def match_nodes(self, filter_string):
        tmp_nodes = self.nodes_list
        for word in filter_string.split(' '):
            tmp_nodes = list(filter(lambda hs: word in hs['words'], tmp_nodes))
        return tmp_nodes
