This formula distributes a certs ssl key, ssl cert, and ca cert

Required to run this formula:

1. Install python deps on master

  yum install pyOpenSSL

or

  yum install python-pip
  pip install pyOpenSSL

2. Generate certs on the master

  1. Run files/generate_fakeca.py
    - This will use salts tls module to create a fake ca and keypairs for all servers listed in salt-key --list all.
  2. Run files/fakeca_to_saltpki.py
    - This will create the directory structure listed above and move the fakeca keys into the correct directories.

3. The following configuration on the salt master under /etc/salt/master.d/pki_ext_pillar.conf
```
ext_pillar:
  - file_tree:
      root_dir: /etc/salt/server_certs
      follow_dir_links: False
      raw_data: False
```

4. Restart the salt master

  service salt-master restart

5. Run pki formula on nodes

  salt node state.apply pki

Notes:

By default the pub/private minion keys and ca will be dropped in the following dirs::

/etc/pki/public
/etc/pki/private
/etc/pki/cacerts
 
The scripts will create a directory /etc/salt/server_certs/hosts with the following structure:
```
minion_id/pki/public_key
minion_id/pki/private_key
minion_id/pki/cacerts/ca.crt
```
For example:
```
/etc/salt/server_certs/hosts/vm1/pki/public_key
/etc/salt/server_certs/hosts/vm1/pki/private_key
/etc/salt/server_certs/hosts/vm1/pki/cacerts/ca.crt
/etc/salt/server_certs/hosts/vm2/pki/public_key
/etc/salt/server_certs/hosts/vm2/pki/private_key
/etc/salt/server_certs/hosts/vm2/pki/cacerts/ca.crt
/etc/salt/server_certs/hosts/vm2/pki/cacerts/ca2.crt
```
Where vm1 and vm2 are minion ids
