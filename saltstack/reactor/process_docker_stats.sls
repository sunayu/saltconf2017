#!py

from __future__ import division

import salt.config
import salt.client
import salt.runner
import logging

def run():
    ret = {}

    # Max number of containers to scale to
    max = 4

    # Track services that should be scaled
    services = []

    # Gather list of containers and hosts
    for item in data['items']:
        items = item.split(':')

        minion_id = items[0]
        container_id = items[1]
        service_name = items[2]

        # Collect services to scale
        if service_name not in services:
            services.append(service_name)

    # Check if each service should be upscaled
    for service_name in services:     
        logging.info('Looking up current number of containers in service ' + service_name + '...')
        replicas = __salt__['saltutil.runner']("docker.get_num_replicas", [service_name])       

        if replicas:
            logging.info(service_name + ' ' + replicas)

            replica_vals = replicas.split('/')
            current_running = replica_vals[0]
            current_max = replica_vals[1]
       
            if int(current_max) < max:
                new_max = int(current_max) + 1
                logging.info('Upscaling service ' + service_name + ' to ' + str(new_max))
            
                # Upscale service_name to new_max
                output = __salt__['saltutil.runner']("docker.scale_service", [service_name,new_max])
                logging.info(output)

            else:
                logging.info('Service ' + service_name + ' is already at max scaling (' + str(max) + ')')
        else:
            logging.info('Could not find number of containers for service ' + service_name)
    return ret
