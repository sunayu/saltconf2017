# -*- coding: utf-8 -*-
# vim: ft=sls

{% from "docker/map.jinja" import docker with context %}

docker swarm info:
  file.managed:
  - name: /etc/salt/minion.d/docker_swarm_mine.conf
  - source: salt://docker/files/swarm/docker_swarm_mine.conf
  - context:
      docker: {{ docker }}

docker mine worker token:
  module.run:
  - name: mine.send
  - func: docker_worker_token
  - kwargs:
      mine_function: cmd.run
      cmd: 'docker swarm join-token worker -q'

docker mine manager token:
  module.run:
  - name: mine.send
  - func: docker_manager_token
  - kwargs:
      mine_function: cmd.run
      cmd: 'docker swarm join-token manager -q'

docker mine manager ip:
  module.run:
  - name: mine.send
  - func: docker_manager_ip
  - kwargs:
      mine_function: grains.get
  - args:
    - ip4_interfaces:{{ docker.nic }}:0
