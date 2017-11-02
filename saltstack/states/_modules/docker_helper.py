#!/usr/bin/env python
'''
Helper modules for newer docker functionalities
'''

import os

import salt.utils
from salt.exceptions import SaltException

def __virtual__():
    '''
    Only load module if docker is installed

    '''
    # TODO: This is a terrible check
    if os.path.exists('/etc/docker'):
        return 'docker_helper'
    return False

# docker service scale
def scale(service, count):
    cmd = 'docker service scale -d ' + service + '=' + str(count)
    return __salt__['cmd.run_all'](cmd)

'''
CONTAINER           CPU %               MEM USAGE / LIMIT     MEM %               NET I/O             BLOCK I/O           PIDS
96e26c51f3de        0.34%               37.16MiB / 1.796GiB   2.02%               4.55MB / 1.48MB     0B / 27.6kB         21
e212b8986fca        52.70%              21.19MiB / 1.796GiB   1.15%               1.55GB / 1.51GB     1.84MB / 0B         17
0352c98c0159        0.01%               56.54MiB / 1.796GiB   3.07%               816B / 0B           0B / 0B             5
7d85b41e2d9f        18.40%              5.203MiB / 1.796GiB   0.28%               861MB / 1.04GB      0B / 153kB          8
'''
def _parsestats(stats_output):
    data = {}
    data['retcode'] = stats_output['retcode']
    data['pid'] = stats_output['pid']    
#    data['stderr'] = stats_output['stderr']
#    data['stdout'] = stats_output['stdout']
    data['stats'] = []

    for line in stats_output['stdout'].split("\n")[1:]:
        line_data = line.split()
        stats_data = {}
        stats_data['container'] = line_data[0]
        # TODO: Parse out %?
        stats_data['cpu_percent'] = line_data[1]
        stats_data['mem_usage'] = line_data[2]
        stats_data['mem_limit'] = line_data[4]
        stats_data['mem_percent'] = line_data[5]
        stats_data['net_in'] = line_data[6]
        stats_data['net_out'] = line_data[8]
        stats_data['block_in'] = line_data[9]
        stats_data['block_out'] = line_data[11]
        stats_data['pids'] = line_data[12]

        data['stats'].append(stats_data)
    return data

# docker stats
def stats():
    cmd = 'docker stats --no-stream'
    data = _parsestats(__salt__['cmd.run_all'](cmd,output_loglevel='quiet'))
    return data
