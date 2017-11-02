{% from "docker/map.jinja" import docker with context %}

{% set join_token = salt['mine.get']('*', 'docker_manager_token').items()[0][1] %}
{% set join_ip = salt['mine.get']('*', 'docker_manager_ip').items()[0][1] %}

include:
  - docker
  - docker.swarm.mine
{% if docker.swarm_drain_managers %}
  - docker.swarm.manager.drain
{% endif %}

join cluster:
  cmd.run:
    - name: 'docker swarm join --token {{ join_token }} {{ join_ip }}:2377'
{% if docker.swarm_drain_managers %}
    - require_in:
      - cmd: drain manager
{% endif %}
