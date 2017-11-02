{% from "docker/map.jinja" import docker with context %}

include:
  - docker
  - docker.swarm.manager.initialize
{% if docker.swarm_drain_managers %}
  - docker.swarm.manager.drain
{% endif %}
  - docker.swarm.manager.mine
