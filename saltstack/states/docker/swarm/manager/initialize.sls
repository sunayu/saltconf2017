{% from "docker/map.jinja" import docker with context %}

init new swarm cluster:
  cmd.run:
    - name: 'docker swarm init --advertise-addr {{ grains['fqdn_ip4'][0] }}'
{% if docker.swarm_drain_managers %}
    - require_in:
      - cmd: drain manager
{% endif %}
