#!/usr/bin/env python2.7
import sys
import os
import shlex

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
        sys.exit(repr(sys.argv))

if __name__ == '__main__':
    main()
