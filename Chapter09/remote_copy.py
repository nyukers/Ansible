# Mastering Ansible Second Edition
Полное руководство Ansible, 3 изд.
Джеймс Фриман и Джесс Китинг

Глава 9. Расширение Ansible
http://onreader.mdl.ru/MasteringAnsible.3ed/content/Ch09.html#01

Разработка модулей, часть 1

#!/usr/bin/python 
# remote_copy.py 

import shutil 

def main(): 
    module = AnsibleModule( 
        argument_spec = dict( 
            source=dict(required=True, type='str'), 
            dest=dict(required=True, type='str') 
        ) 
    ) 

 shutil.copy(module.params['source'], 
                module.params['dest'])


 module.exit_json(changed=True)


from ansible.module_utils.basic import *


if __name__ == '__main__': 
    main()

# simple_module.yaml 
--- 
- name: test remote_copy module 
  hosts: localhost 
  gather_facts: false 
 
  tasks: 
    - name: ensure foo 
      file: 
        path: /tmp/foo 
        state: touch 
 
    - name: do a remote copy 
      remote_copy: 
        source: /tmp/foo 
        dest: /tmp/bar 


ansible-playbook -i mastery-hosts simple_module.yaml -v

# remote_copy.py FULL
# ansible-doc -M library/ remote_copy

import shutil 
 
DOCUMENTATION = ''' 
--- 
module: remote_copy 
version_added: future 
short_description: Copy a file on the remote host 
description: 
  - The remote_copy module copies a file on the remote host from a given source to a provided destination. 
options: 
  source: 
    description: 
      - Path to a file on the source file on the remote host 
    required: True 
  dest: 
    description: 
      - Path to the destination on the remote host for the copy 
    required: True 
author: 
  - Jesse Keating 
''' 

EXAMPLES = ''' 
# Example from Ansible Playbooks 
- name: backup a config file 
  remote_copy: 
    source: /etc/herp/derp.conf 
    dest: /root/herp-derp.conf.bak 
''' 


 module.exit_json(changed=True, source=module.params['source'], 
                     dest=module.params['dest']) 


RETURN = ''' 
source: 
  description: source file used for the copy 
  returned: success 
  type: string 
  sample: "/path/to/file.name" 
dest: 
  description: destination of the copy 
  returned: success 
  type: string 
  sample: "/path/to/destination.file" 
gid: 
  description: group ID of destination target 
  returned: success 
  type: int 
  sample: 502 
group: 
  description: group name of destination target 
  returned: success 
  type: string 
  sample: "users" 
uid: 
  description: owner ID of destination target 
  returned: success 
  type: int 
  sample: 502 
owner: 
  description: owner name of destination target 
  returned: success 
  type: string 
  sample: "fred" 
mode: 
  description: permissions of the destination target 
  returned: success 
  type: int 
  sample: 0644 
size: 
  description: size of destination target 
  returned: success 
  type: int 
  sample: 20 
state: 
  description: state of destination target 
  returned: success 
  type: string 
  sample: "file" 
''' 


# facts

facts = {'rc_source': module.params['source'], 
             'rc_dest': module.params['dest']} 
 
    module.exit_json(changed=True, ansible_facts=facts) 


 - name: show a fact 
      debug: 
        var: rc_dest 


- name: do a remote copy 
      remote_copy: 
        source: /tmp/foo 
        dest: /tmp/bar 
      register: mycopy 
 
    - name: set facts from mycopy 
      set_fact: 
        rc_dest: "{{ mycopy.dest }}" 

###########
#check mode

 module = AnsibleModule( 
        argument_spec = dict( 
            source=dict(required=True, type='str'), 
            dest=dict(required=True, type='str') 
        ), 
        supports_check_mode=True 
    ) 



 if not module.check_mode: 
        shutil.copy(module.params['source'], 
                    module.params['dest']) 

###########
ansible-playbook -i mastery-hosts simple_module.yaml -v -C

