# -*- coding: utf-8 -*-
# vim: ft=sls

{% from "docker/map.jinja" import docker with context %}

docker registry certs.d:
  file.directory:
  - name: /etc/docker/certs.d

{% for registry in docker.registries %}
docker registry certs.d dir:
  file.directory:
  - name: /etc/docker/certs.d/{{ registry['host'] }}:{{ registry['port'] }}

# Current version of docker seems to ignore client certs?
#docker registry certs.d {{ registry['host'] }} client cert:
#  file.copy:
#  - name: '/etc/docker/certs.d/{{ registry['host'] }}:{{ registry['port'] }}/client.cert'
#  - source: /etc/pki/public/{{ grains['fqdn'] }}.pem

#docker registry certs.d {{ registry['host'] }} client key:
#  file.copy:
#  - name: '/etc/docker/certs.d/{{ registry['host'] }}:{{ registry['port'] }}/client.key'
#  - source: /etc/pki/private/{{ grains['fqdn'] }}.pem

docker registry certs.d {{ registry['host'] }} ca.crt:
  file.copy:
  - name: "/etc/docker/certs.d/{{ registry['host'] }}:{{ registry['port'] }}/ca.crt"
  - source: /etc/pki/cacerts/fakeca.crt
{% endfor %}
