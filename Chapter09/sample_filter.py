# Mastering Ansible Second Edition
Полное руководство Ansible, 3 изд.
Джеймс Фриман и Джесс Китинг

Глава 9. Расширение Ansible
http://onreader.mdl.ru/MasteringAnsible.3ed/content/Ch09.html#01

Разработка модулей, часть 2

1) 
# Встраиваемые модули фильтрации
# Наш фильтр превращает слова the cloud в somebody else's computer.
# Имеющиеся встраиваемые модули фильтрации можно найти в plugins/filter/.
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
# Встраиваемые модули обратного вызова
# свой callback_plugins/shrug.py.
# В нашем случае мы подключаемся к точке v2_on_any с тем, чтобы наш подключаемый модуль запускался во всех точках обратного вызова
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


