# TODO: These should be pillar vars with defaults
{% set private_key_dir = '/etc/pki/private' %}
{% set public_key_dir = '/etc/pki/public' %}
{% set cacerts_dir = '/etc/pki/cacerts' %}
{% set cacerts_in_dir = '/etc/pki/.cacerts_in' %}
# TODO: Add jks functionality
{% set create_jks_files = false %}
{% set java_key_dir = '/etc/pki/java' %}
{% set truststore_password = 'changeit' %}
{% set keystore_password   = 'changeit' %}

# Handle server certs
server_public_key_dir:
  file.directory:
  - name: {{ public_key_dir }}
  - makedirs: true

{% if salt['pillar.get']('pki:public_key', false) %}
server_public_key:
  file.managed:
  - name:  {{ public_key_dir }}/{{ grains['fqdn'] }}.pem
  - contents_pillar: pki:public_key
{% endif %}

server_private_key_dir:
  file.directory:
  - name: {{ private_key_dir }}

{% if salt['pillar.get']('pki:private_key', false) %}
server_private_key:
  file.managed:
  - name: {{ private_key_dir }}/{{ grains['fqdn'] }}.pem
  - contents_pillar: pki:private_key
{% endif %}

# Handle cacerts
server_cacerts_dir:
  file.directory:
  - name: {{ cacerts_dir }}

{% if salt['pillar.get']('pki:cacerts', false) %}
{%   for cert,data in salt['pillar.get']('pki:cacerts',{}).iteritems() %}
{{ cacerts_dir }}/{{ cert }}:
  file.managed:
  - contents_pillar: pki:cacerts:{{ cert }}
  - watch_in:
    - cmd: hash_cas_script_run
{%   endfor %}
{% endif %}

hash_cas_script:
  file.managed:
  - name: /usr/local/bin/hash_cas.sh
  - mode: 0700
  - source: 'salt://pki/files/hash_cas.sh.jin'
  - template: jinja
  - defaults:
    cacerts_dir: {{ cacerts_dir }}

hash_cas_script_run:
  cmd.wait:
  - name: /usr/local/bin/hash_cas.sh
  - watch:
    - file: hash_cas_script
