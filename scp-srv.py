#!/usr/bin/env python3

import sys
import re
import dns.resolver
import dns.exception
import subprocess

NOARG_FLAG_REGEX = '-[346BCpqrv]+'


def is_remote(arg):
    return ':' in arg or '@' in arg


def launch_scp(args):
    print('Launching: scp ' + ' '.join(args))
    cmd = ['scp'] + args
    p = subprocess.run(cmd)
    pass


def is_not_flag(args, index):
    # is not a flag if:
    # doesn't begin with -
    # doesn't follow an arg that begins with - but is not a single flag (NOARG_FLAG_REGEX)
    if args[index][0] == '-':
        return False
    elif args[index - 1][0] == '-' and not re.match(NOARG_FLAG_REGEX, args[index - 1]):
        return False
    else:
        return True


def domain_name(remote):
    if '@' in remote:
        remote = remote.split('@')[1]
    if ':' in remote:
        remote = remote.split(':')[0]
    return remote


def main(args):
    new_args = args

    if any([arg == '-P' for arg in args]):
        print('skipped!')
    else:
        # find remotes:
        # SRC is the first argument that doesn't follow a flag
        # DST is the last argument that doesn't follow a flag
        no_flag = [(ind, x) for ind, x in enumerate(args) if is_not_flag(args, ind)]
        remote = no_flag[0] if is_remote(no_flag[0][1]) else no_flag[-1] if is_remote(no_flag[-1][1]) else None
        if remote is not None:
            resolver = dns.resolver.Resolver()
            domain = domain_name(remote[1])
            srv_address = '_ssh._tcp.' + domain
            try:
                answers = resolver.query(srv_address, 'SRV')
                target = str(answers[0].target)[:-1]
                port = answers[0].port
                print('Found srv record {}:{} for search {}'.format(target, port, srv_address))
                new_arg = re.sub(domain, target, remote[1])
                new_args[remote[0]] = new_arg
                new_args = ['-P', str(port)] + new_args
            except dns.exception.DNSException:
                print('No SRV records found for search {}'.format(srv_address))

    launch_scp(new_args)


if __name__ == '__main__':
    main(sys.argv[1:])
