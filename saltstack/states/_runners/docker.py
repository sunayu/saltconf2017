import salt.client
import salt.runner

def stack_deploy(path, name):
    # Get a docker_swarm manager
    opts = salt.config.master_config('/etc/salt/master')
    runner_client = salt.runner.RunnerClient(opts)
    manager = runner_client.cmd('docker.get_manager',print_event=False)

    # Deploy service name from path
    client = salt.client.LocalClient(__opts__['conf_file'])
    return client.cmd(manager, 'docker_stack.deploy',[path, name],timeout=1)[manager]

def stack_rm(name):
    # Get a docker_swarm manager
    opts = salt.config.master_config('/etc/salt/master')
    runner_client = salt.runner.RunnerClient(opts)
    manager = runner_client.cmd('docker.get_manager',print_event=False)

    # Deploy service name from path
    client = salt.client.LocalClient(__opts__['conf_file'])
    return client.cmd(manager, 'docker_stack.rm',[name],timeout=1)[manager]

def get_service_name(container_id, host):
    client = salt.client.LocalClient(__opts__['conf_file'])
    container_info = client.cmd(host, 'docker.inspect',[container_id],timeout=1)

    if host in container_info:
        if 'State' in container_info[host]:
            if 'com.docker.swarm.service.name' in container_info[host]['Config']['Labels']:
                return container_info[host]['Config']['Labels']['com.docker.swarm.service.name']
    return False

def get_manager():
    client = salt.client.LocalClient(__opts__['conf_file'])
    mine_ret = client.cmd('sm','mine.get',['*','docker_manager_ip'],timeout=1)
    return mine_ret['sm'].keys()[0]

def get_num_replicas(service_name):
    client = salt.client.LocalClient(__opts__['conf_file'])
    opts = salt.config.master_config('/etc/salt/master')
    runner_client = salt.runner.RunnerClient(opts)

    # Get a docker_swarm manager
    manager = runner_client.cmd('docker.get_manager',print_event=False)

    # Docker makes service names as service_subservice
    main_service_name = service_name.split('_')[0]

    # Call module to get service replica info
    service_info = client.cmd(manager, 'docker_stack.services',[main_service_name],timeout=1)[manager]
    for service in service_info['services']:
        if service['name'] == service_name:
            return service['replicas'] 
    return False

def scale_service(service_name, new_count):
    # Get a docker_swarm manager
    opts = salt.config.master_config('/etc/salt/master')
    runner_client = salt.runner.RunnerClient(opts)
    manager = runner_client.cmd('docker.get_manager',print_event=False)

    # call module to scale the service
    client = salt.client.LocalClient(__opts__['conf_file'])
    return client.cmd(manager, 'docker_helper.scale',[service_name,new_count],timeout=1)[manager]

# Added for demo app
def get_container_name(container_id, host):
    client = salt.client.LocalClient(__opts__['conf_file'])
    container_info = client.cmd(host, 'docker.inspect',[container_id],timeout=1)

    if host in container_info:
        if 'State' in container_info[host]:
            if 'com.docker.swarm.task.name' in container_info[host]['Config']['Labels']:
                container_name = container_info[host]['Config']['Labels']['com.docker.swarm.task.name']
                short_container_name = container_name.split('.')[:2]
                return '.'.join(short_container_name)
    return False

# Added for demo app
def stats():
    client = salt.client.LocalClient(__opts__['conf_file'])
    return client.cmd('d*', 'docker_helper.stats',timeout=5)
