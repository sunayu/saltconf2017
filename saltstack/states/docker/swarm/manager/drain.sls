# TODO nodes show up with fqdn not id
drain manager:
  cmd.run:
    - name: 'docker node update --availability drain {{ grains['fqdn'] }}'
