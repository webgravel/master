import graveldb
import ssh_utils
import os
import re
import pwd

PATH = '/gravel/system/master'

class Node(graveldb.Table('nodes', PATH)):
    default = dict(sshkey=None, address=None)

    def setup(self):
        if not re.match('^[a-zA-Z0-9._-]+$', self.name):
            raise ValueError('bad name')

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
