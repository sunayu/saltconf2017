# -*- coding: utf-8 -*-
# vim: ft=sls

{% from "docker/map.jinja" import docker with context %}

{% if grains['os'] == 'CentOS' %}
docker repo:
  pkgrepo.managed:
  - name: Docker-ce-stable
  - humanname: docker-ce-stable
  - baseurl: https://download.docker.com/linux/centos/7/x86_64/stable
  - enabled: 1
  - gpgcheck: 1
  - gpgkey: https://download.docker.com/linux/centos/gpg
{% elif grains['os'] == 'Ubuntu' %}
docker gpg:
  cmd.run:
  - name: curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
  - unless: apt-key list | grep 0EBFCD88

docker repo:
  pkgrepo.managed:
  - humanname: downloaddocker
  - name: deb [arch=amd64] https://download.docker.com/linux/ubuntu {{ grains['oscodename'] }} stable
  - file: /etc/apt/sources.list.d/downloaddocker.list
{% endif %}

# WE DEMOIN
#docker pkg:
#  pkg.installed:
#  - name: {{ docker.pkg }}

# Required for salt docker module
{% if grains['os_family'] == 'Debian' %}
{% set pip_pkg = 'python-pip' %}
{% elif grains['os_family'] == 'RedHat' %}
{% set pip_pkg = 'python2-pip' %}
{% endif %}
# WE DEMOIN
#docker python pip:
#  pkg.installed:
#  - name: {{ pip_pkg }}

# WE DEMOIN
#docker pip docker:
#  pip.installed:
#  - name: docker

