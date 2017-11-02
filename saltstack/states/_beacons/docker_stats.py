# -*- coding: utf-8 -*-
'''
Beacon to monitor docker container cpu usage.

Example config:

beacons:
  docker_stats:
    disable_during_state_run: True
    interval: 30
    stats:
    - cpu: 40
'''

# Import Python libs
from __future__ import absolute_import
import logging
import re
import os
import salt.client

log = logging.getLogger(__name__)

__virtualname__ = 'docker_stats'

def __virtual__():
    '''
    Only load module if docker is installed

    '''
    # TODO: This is a terrible check
    if os.path.exists('/etc/docker'):
        return __virtualname__
    return False

def __validate__(config):
    '''
    Validate the beacon configuration
    '''
    # TODO: Correctly validate vs all options
    # Configuration for docker_stats beacon should be a list of dicts
    if not isinstance(config, dict):
        return False, ('Configuration for docker_stats '
                       'beacon must be a dictionary.')
    else:
        if 'stats' not in config:
            return False, ('Must include stats')
    return True, 'Valid beacon configuration'

def beacon(config):
    '''
    Monitor the cpu usage of docker containers

    Specify thresholds for stats and only emit a beacon if it is exceeded.

    .. code-block:: yaml

        beacons:
          docker_stats:
            stats
            - cpu: 40
    '''
    # Initialize return list
    ret = []

    # Gather config
    # TODO: support other options, not just cpu
    for limit in config['stats']:
        cpu_limit = float(limit['cpu'])
        log.debug('cpu limit is set to: ' + str(cpu_limit))
        # Gather docker stats
        log.info('checking docker stats')
        docker_stats = __salt__['docker_helper.stats']()

        # Check each container
        for container in docker_stats['stats']:
            cpu_usage =  re.sub('%', '', container['cpu_percent'])
            cpu_usage = float(cpu_usage)
            log.debug('container_id: ' + container['container'] + 'cpu usage is: ' + str(cpu_usage))

            if cpu_usage > cpu_limit:
                log.debug('Getting service name for container: ' + container['container'])
                container_info = __salt__['docker.inspect'](container['container'])
                service_name = container_info['Config']['Labels']['com.docker.swarm.service.name']
                log.debug('Firing beacon for container: ' + container['container'])
                ret.append({'container_id': container['container'], 'cpu': cpu_usage, 'service_name': service_name})

    # Return beacon
    return ret
