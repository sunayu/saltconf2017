hosts file:
  file.managed:
  - name: /etc/hosts
  - source: salt://hosts/hosts.j2
  - template: jinja
