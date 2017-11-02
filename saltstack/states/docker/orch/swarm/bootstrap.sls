# Configure manager
{% for manager in salt['pillar.get']('docker:swarm:managers') %}

{% if loop.first %}
{% set manager_sls = 'docker.swarm.manager.first' %}
{% else %}
{% set manager_sls = 'docker.swarm.manager.join' %}
{% endif %}

bootstrap swarm manager {{ manager }}:
  salt.state:
    - sls: {{ manager_sls }}
    - tgt: {{ manager }}

update mine for {{ manager }}:
  salt.function:
    - name: mine.update
    - tgt: '*'
    - require:
      - salt: bootstrap swarm manager {{ manager }}

{% endfor %}

# Configure workers
{% for worker in salt['pillar.get']('docker:swarm:workers') %}
bootstrap swarm worker {{ worker }}:
  salt.state:
    - sls: docker.swarm.worker.join
    - tgt: {{ worker }}

{% endfor %}
