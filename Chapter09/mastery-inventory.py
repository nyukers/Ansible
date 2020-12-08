# Mastering Ansible Second Edition
Полное руководство Ansible, 3 изд.
Джеймс Фриман и Джесс Китинг

Глава 9. Расширение Ansible
http://onreader.mdl.ru/MasteringAnsible.3ed/content/Ch09.html#01

Разработка модулей, часть 3

# Разработка встраиваемых модулей динамического учёта
# Не полный список встраиваемых модулей инвентаризации:
apache-libcloud
cobbler
console_io
digital_ocean
docker
ec2
gce
libvirt_lxc
linode
openshift
openstack
rax
vagrant
vmware
windows_azure

# mastery-inventory.py

#!/usr/bin/env python 
# 

import json 
import argparse

inventory = {} 
inventory['web'] = {'hosts': ['mastery.example.name'], 
                    'vars': {'http_port': 80, 
                             'proxy_timeout': 5}} 
inventory['dns'] = {'hosts': ['backend.example.name']} 
inventory['database'] = {'hosts': ['backend.example.name'], 
                         'vars': {'ansible_ssh_user': 'database'}} 
inventory['frontend'] = {'children': ['web']} 
inventory['backend'] = {'children': ['dns', 'database'], 
                        'vars': {'ansible_ssh_user': 'blotto'}} 
inventory['errors'] = {'hosts': ['scsihost']} 
inventory['failtest'] = {'hosts': ["failer%02d" % n for n in 
                                   range(1,11)]} 

allgroupvars = {'ansible_ssh_user': 'otto'}

hostvars = {} 
hostvars['web'] = {'ansible_ssh_host': '192.168.10.25'} 
hostvars['scsihost'] = {'ansible_ssh_user': 'jkeating'} 

parser = argparse.ArgumentParser(description='Simple Inventory') 
parser.add_argument('--list', action='store_true', 
                    help='List all hosts') 
parser.add_argument('--host', help='List details of a host') 
args = parser.parse_args() 

if args.list: 
    for group in inventory: 
        ag = allgroupvars.copy() 
        ag.update(inventory[group].get('vars', {})) 
        inventory[group]['vars'] = ag 
    print(json.dumps(inventory)) 


#elif args.host: 
#    print(json.dumps(hostvars.get(args.host, {}))) 

elif args.host:
    hostfound = False
    agghostvars = allgroupvars.copy()
    for group in inventory:
        if args.host in inventory[group].get('hosts', {}):
            hostfound = True
            for childgroup in inventory:
                if group in inventory[childgroup].get('children', {}):
                    agghostvars.update(inventory[childgroup].get('vars', {}))
    for group in inventory:
        if args.host in inventory[group].get('hosts', {}):
            hostfound = True
            agghostvars.update(inventory[group].get('vars', {}))
    if hostvars.get(args.host, {}):
        hostfound = True
    agghostvars.update(hostvars.get(args.host, {}))
    if not hostfound:
        agghostvars = {}
    print(json.dumps(agghostvars))


# chmod +x mastery-inventory.py
# ./mastery-inventory.py --help
# ./mastery-inventory.py --list
# ./mastery-inventory.py --host mastery.name
# ./mastery-inventory.py --host web


# ansible.cfg
[inventory]
enable_plugins = ini, script

# inventory_test.yaml

--- 
- name: test the inventory 
  hosts: all 
  gather_facts: false 
 
  tasks: 
    - name: hello world 
      debug: 
        msg: "Hello world, I am {{ inventory_hostname }}. 
              My username is {{ ansible_ssh_user }}"


hostvars['scsihost'] = {'ansible_ssh_user': 'jkeating'} 
 
inventory['_meta'] = {'hostvars': hostvars} 
 
parser = argparse.ArgumentParser(description='Simple Inventory') 
Next we'll change the --host handling to raise an exception: 
elif args.host: 
    raise StandardError("You've been a bad boy")

$ source ./hacking/env-setup

$ test/runner/ansible-test integration -v posix/ci/

# ansible-plybook -i mastery-inventory.py inventory_test.yaml --limit backend,frontend,errors





