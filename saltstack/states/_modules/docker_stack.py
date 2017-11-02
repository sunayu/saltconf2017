#!/usr/bin/env python
'''
Support for querying docker stacks
'''

import os

# import salt libs
import salt.utils
from salt.exceptions import SaltException

def __virtual__():
    '''
    Only load module if docker is installed and the node is a manager
    '''
    # TODO: This is a terrible check
    if os.path.exists('/etc/docker'):
        return 'docker_stack'
    return False

def deploy(compose_file, stack_name):
    cmd = 'docker stack deploy --compose-file ' + compose_file + ' ' + stack_name
    return __salt__['cmd.run_all'](cmd)

def rm(stack_name):
    cmd = 'docker stack rm ' + stack_name
    return __salt__['cmd.run_all'](cmd)

'''
NAME                SERVICES
vote                6
'''
def _parsels(ls_output):
    data = {}
    data['retcode'] = ls_output['retcode']
    data['pid'] = ls_output['pid']    
#    data['stderr'] = ls_output['stderr']
#    data['stdout'] = ls_output['stdout']
    data['stacks'] = []

    for line in ls_output['stdout'].split("\n")[1:]:
        stack_info = line.split()
        data['stacks'].append({'name': stack_info[0],'num_services': stack_info[1]})
    return data

def ls():
    cmd = 'docker stack ls'
    data =_parsels(__salt__['cmd.run_all'](cmd))
    return data

'''
ID                  NAME                IMAGE                                          NODE                DESIRED STATE       CURRENT STATE            ERROR               PORTS
geqzty43djw5        vote_db.1           postgres:9.4                                   c71.novalocal       Running             Running 26 minutes ago                       
iry9wjrbbbyj        vote_redis.1        redis:alpine                                   c72.novalocal       Running             Running 26 minutes ago                       
shkvoigtak90        vote_visualizer.1   dockersamples/visualizer:stable                c71.novalocal       Running             Running 26 minutes ago                       
srzv2uhc8uyk        vote_worker.1       dockersamples/examplevotingapp_worker:latest   c71.novalocal       Running             Running 26 minutes ago                       
sd1qp6anoywq        vote_result.1       dockersamples/examplevotingapp_result:before   c73.novalocal       Running             Running 27 minutes ago                       
7vgfyl3b8j20        vote_vote.1         dockersamples/examplevotingapp_vote:before     c71.novalocal       Running             Running 27 minutes ago                       
vkldz5r757oy        vote_vote.2         dockersamples/examplevotingapp_vote:before     c72.novalocal       Running             Running 27 minutes ago                       
'''
def _parseps(ps_output):
    data = {}
    data['retcode'] = ps_output['retcode']
    data['pid'] = ps_output['pid']
    #data['stderr'] = ps_output['stderr']
    #data['stdout'] = ps_output['stdout']
    data['containers'] = []

    for line in ps_output['stdout'].split("\n")[1:]:
        line_data = line.split()
        ps_data  = {}
        ps_data['id'] = line_data[0]
        ps_data['name'] = line_data[1]
        ps_data['image'] = line_data[2]
        ps_data['node'] = line_data[3]
        ps_data['desired_state'] = line_data[4]
        ps_data['current_state'] = line_data[5]
        # TODO: Grab error and ports ?

        data['containers'].append(ps_data)

    return data

def ps(stack_name):
    cmd = 'docker stack ps ' + stack_name
    data = _parseps(__salt__['cmd.run_all'](cmd))
    return data

'''
root@c71 example-voting-app]# docker stack services vote
ID                  NAME                MODE                REPLICAS            IMAGE                                          PORTS
3badgs1cbbgm        vote_result         replicated          1/1                 dockersamples/examplevotingapp_result:before   *:5001->80/tcp
klpcxpsvs9a5        vote_redis          replicated          1/1                 redis:alpine                                   *:0->6379/tcp
knqwriggmt56        vote_visualizer     replicated          1/1                 dockersamples/visualizer:stable                *:8080->8080/tcp
nni08jmnkjh4        vote_vote           replicated          2/2                 dockersamples/examplevotingapp_vote:before     *:5000->80/tcp
p8330s8ra0yy        vote_worker         replicated          1/1                 dockersamples/examplevotingapp_worker:latest   
pbrcf8v7wqa9        vote_db             replicated          1/1                 postgres:9.4                                   
'''
def _parseservices(services_output):
    data = {}
    data['retcode'] = services_output['retcode']
    data['pid'] = services_output['pid']
#    data['stderr'] = services_output['stderr']
#    data['stdout'] = services_output['stdout']

    data['services'] = []
    for line in services_output['stdout'].split("\n")[1:]:
        line_data = line.split()
        service_data = {}
        service_data['id'] = line_data[0]
        service_data['name'] = line_data[1]
        service_data['mode'] = line_data[2]
        service_data['replicas'] = line_data[3]
        service_data['image'] = line_data[4]
        if len(line_data) > 5:
            service_data['ports'] = line_data[5]

        data['services'].append(service_data)

    return data

def services(stack_name):
    cmd = 'docker stack services ' + stack_name
    data = _parseservices(__salt__['cmd.run_all'](cmd))
    return data
