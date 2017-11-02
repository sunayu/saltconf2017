{% set join_token = salt['mine.get']('*', 'docker_worker_token').items()[0][1] %}
{% set join_ip = salt['mine.get']('*', 'docker_manager_ip').items()[0][1] %}

include:
  - docker

join cluster:
  cmd.run:
    - name: 'docker swarm join --token {{ join_token }} {{ join_ip }}:2377'
