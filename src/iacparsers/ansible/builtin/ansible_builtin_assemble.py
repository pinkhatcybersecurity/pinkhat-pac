from iacparsers.ansible.ansible_security_check_core import AnsibleSecurityCheckCore


class AnsibleBuiltinAssemble(AnsibleSecurityCheckCore):
    """
    Description of Ansible Builtin Copy Module:
    https://docs.ansible.com/ansible/latest/collections/ansible/builtin/assemble_module.html

    - name: Assemble from fragments from a directory
      ansible.builtin.assemble:
        src: /etc/someapp/fragments
        dest: /etc/someapp/someapp.conf
    """

    MODULE_NAME = "ansible.builtin.assemble"
