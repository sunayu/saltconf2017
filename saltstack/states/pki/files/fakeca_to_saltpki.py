#! /usr/bin/env python

import os
import subprocess
import shutil

base_dir = '/etc/salt/server_certs'
fakeca_ca_dir = '/etc/pki/fakeca'
fakeca_certs_dir = '/etc/pki/fakeca/certs'

def check_and_create_dir (directory):
  if not os.path.exists(directory):
    print "Creating: " + directory
    os.makedirs(directory)

def copy_file (file_from, file_to):
  print "Copying: " + file_from + " to: " + file_to
  shutil.copyfile(file_from, file_to)

if __name__ == "__main__":
  # First we need to create some base directories
  check_and_create_dir(base_dir)
  check_and_create_dir(base_dir + '/hosts')

  # Gather host list from salt-key command
  hosts = os.popen("salt-key --list acc").read().split("\n")
  # First and last entry are formatting so remove them
  hosts.pop(0)
  hosts.pop(-1)

  for host in hosts:
    if os.path.isfile(fakeca_certs_dir + '/' + host + '.crt'):

      server_key_path = fakeca_certs_dir + '/' + host + '.key'
      server_cert_path = fakeca_certs_dir + '/' + host + '.crt'

      check_and_create_dir(base_dir + '/hosts/' + host)
      check_and_create_dir(base_dir + '/hosts/' + host + '/pki')
      check_and_create_dir(base_dir + '/hosts/' + host + '/pki/cacerts')

      # Copy the hosts private/public keys and the fakeca certificate
      copy_file(server_key_path, base_dir + '/hosts/' + host + '/pki/private_key')
      copy_file(server_cert_path, base_dir + '/hosts/' + host + '/pki/public_key')
      copy_file(fakeca_ca_dir + '/fakeca_ca_cert.crt', base_dir + '/hosts/' + host + '/pki/cacerts/fakeca.crt')
