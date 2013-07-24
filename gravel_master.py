import graveldb
import gravelrpc
import ssh_utils
import os
import re
import pwd

PATH = '/gravel/system/master'

class Node(graveldb.Table('nodes', PATH)):
    default = dict(sshkey=None, address=None)
    autocreate = False

    def validate(self):
        if not re.match('^[a-zA-Z0-9._-]+$', self.name):
            raise ValueError('bad name')

    def call(self, *args, **kwargs):
        return ssh_utils.call('gravelnode@' + self.data.address, *args, **kwargs)

    def arrange_p2p(self, *args):
        resp = self.call('arrange_p2p', *args, **dict(decode=gravelrpc.bson))
        return (self.data.address, resp['port'], resp['key'])

def regenerate_authorized_keys():
    ssh_utils.write_authorized_keys(
        [('gravel --node=' + node.name, node.data.sshkey)
         for node in Node.all() if node.data.sshkey ],
        user='gravelmaster')
    uid = pwd.getpwnam('gravelmaster').pw_uid
    path = os.path.expanduser('~gravelmaster/.ssh')
    os.chown(path, uid, 0)
    os.chown(path + '/authorized_keys', uid, 0)

def get_node():
    return Node(os.environ['NODE'])

def get_nodes(spec):
    if ',' in spec:
        nodes = []
        return [ item for item in lst for lst in map(get_nodes, spec.split()) ]
    elif spec == '@all':
        return Node.all()
    else:
        node = Node(spec)
        if not node.exists:
            raise ValueError('node %s doesn\'t exist' % spec)
        return [node]

def get_one_node(spec):
    nodes = get_nodes(spec)
    if not nodes:
        raise ValueError('no nodes found')
    elif len(nodes) > 1:
        raise ValueError('too many nodes')
    return nodes[0]
