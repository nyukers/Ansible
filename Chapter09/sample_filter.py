# Mastering Ansible Second Edition
������ ����������� Ansible, 3 ���.
������ ������ � ����� ������

����� 9. ���������� Ansible
http://onreader.mdl.ru/MasteringAnsible.3ed/content/Ch09.html#01

���������� �������, ����� 2

1) 
# ������������ ������ ����������
# ��� ������ ���������� ����� the cloud � somebody else's computer.
# ��������� ������������ ������ ���������� ����� ����� � plugins/filter/.
# sample_filter.py
# ansible_playbook -i master_hosts simple_filter.yaml

def cloud_truth(a): 
    return a.replace("the cloud", "somebody else's computer") 


class FilterModule(object): 
    '''Cloud truth filters''' 
    def filters(self): 
        return {'cloud_truth': cloud_truth} 


# simple_filter.yaml:

--- 
- name: test cloud_truth filter 
  hosts: localhost 
  gather_facts: false 
  vars: 
    statement: "I store my files in the cloud" 
  tasks: 
    - name: make a statement 
      debug: 
        msg: "{{ statement | cloud_truth }}" 



2)
# ������������ ������ ��������� ������
# ���� callback_plugins/shrug.py.
# � ����� ������ �� ������������ � ����� v2_on_any � ���, ����� ��� ������������ ������ ���������� �� ���� ������ ��������� ������
# ansible_playbook -i master_hosts simple_filter.yaml

from ansible.plugins.callback import default 
 class CallbackModule(default.CallbackModule):     
 CALLBACK_VERSION = 2.0     
 CALLBACK_TYPE = 'stdout'     
 CALLBACK_NAME = 'shrug'  
    def v2_on_any(self, *args, **kwargs): 
        msg = '\xc2\xaf\\_(\xe3\x83\x84)_/\xc2\xaf' 
              self._display.display(msg.decode('utf-8') * 8) 


# ansible.cfg 

[defaults] 
stdout_callback = shrug


