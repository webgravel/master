#!/usr/bin/env python2.7
import sys
import os
import shlex

sys.path.append('/gravel/pkg/gravel-common')

def main():
    ssh_command = os.environ.get('SSH_ORIGINAL_COMMAND', None)
    if ssh_command is not None:
        client = sys.argv[1]
        args = ['sudo', os.path.abspath(sys.argv[0])]
        if client == '--operator':
            pass
        elif client.startswith('--node='):
            args.append('--node=' + client[len('--node='):])
        else:
            raise ValueError('invalid client')
        args += shlex.split(ssh_command)
        os.execvp(args[0], args)
    else:
        os.chdir(os.path.dirname(os.path.realpath(sys.argv[0])))
        if not sys.argv[1:]:
            fail_with_help()
            return
        action = sys.argv[1]
        node = None
        if action.startswith('--node='):
            node = action[len('--node='):]
            del sys.argv[1:2]
            action = sys.argv[1]

        command_directory = 'node.d' if node is not None else 'operator.d'
        if node is not None:
            os.environ['NODE'] = node
        os.environ['ACTION'] = action
        os.environ['PYTHONPATH'] = '/gravel/pkg/gravel-common:/gravel/pkg/gravel-master'

        if action not in os.listdir(command_directory):
            # imporant check
            fail_with_help()
            return

        action_command = command_directory + '/' + action

        os.execv(action_command, [action_command] + sys.argv[2:])

def fail_with_help():
    usage = 'Usage: gravel [--node=name] action args...\n'
    for thing in ['operator', 'node']:
        usage += '\n%s commands:\n\n' % thing
        for command in os.listdir(thing + '.d'):
            usage += '\t%s\n' % command
    sys.exit(usage)

if __name__ == '__main__':
    main()
