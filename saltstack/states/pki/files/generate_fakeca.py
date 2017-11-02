#! /usr/bin/env python

import os

print os.popen('salt-call tls.create_ca fakeca bits=2048 days=365 CN=fakeca C=US ST=Maryland L=Baltimore O=Sunayu emailAddress="no@no.com"').read()

hosts = os.popen("salt-key --list acc").read().split("\n")
hosts.pop(0)
hosts.pop(-1)

for host in hosts:
  print os.popen("salt-call tls.create_csr fakeca CN=" + host).read()
  print os.popen("salt-call tls.create_ca_signed_cert fakeca CN=" + host).read()
