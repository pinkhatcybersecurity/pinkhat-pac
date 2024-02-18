class AnsibleBuiltinRpmKey:
    """
    Description of Ansible Builtin Copy Module:
    https://docs.ansible.com/ansible/latest/collections/ansible/builtin/rpm_key_module.html

    - name: Assemble from fragments from a directory
      ansible.builtin.assemble:
        src: /etc/someapp/fragments
        dest: /etc/someapp/someapp.conf
    """

    MODULE_NAME = "ansible.builtin.rpm_key"
