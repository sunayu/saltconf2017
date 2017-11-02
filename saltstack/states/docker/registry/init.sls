# -*- coding: utf-8 -*-
# vim: ft=sls

{% from "docker/map.jinja" import docker with context %}

docker data dirs:
  file.directory:
  - makedirs: True
  - names: 
    - /data
    - /data/docker
    - /data/docker/registry
    - /data/docker/registry/data
    - /data/docker/registry/certs

docker data docker registry certs cert:
  file.copy:
  - name: /data/docker/registry/certs/{{ grains['id'] }}.crt
  - source: /etc/pki/public/{{ grains['fqdn'] }}.pem

docker data docker registry certs key:
  file.copy:
  - name: /data/docker/registry/certs/{{ grains['id'] }}.key
  - source: /etc/pki/private/{{ grains['fqdn'] }}.pem

# TODO: Setup as swarm service instead of standalone container
docker registry container:
  docker_container.running:
  - name: registry
  - image: registry:2
  - restart_policy: always
  - detach: true
  - binds:
    - /data/docker/registry/certs:/certs
    - /data/docker/registry/data:/var/lib/registry
  - port_bindings:
    - 5000:80
  - environment:
    - REGISTRY_HTTP_ADDR: 0.0.0.0:80
    - REGISTRY_HTTP_TLS_CERTIFICATE: certs/{{ grains['id'] }}.crt
    - REGISTRY_HTTP_TLS_KEY: certs/{{ grains['id'] }}.key

