from iacparsers.ansible.core.ansible_permission_core import AnsiblePermissionCore


class AnsibleBuiltinCopy(AnsiblePermissionCore):
    """
    Description of Ansible Builtin Copy Module:
    https://docs.ansible.com/ansible/latest/collections/ansible/builtin/copy_module.html

    - name: Copy file with owner and permissions
      ansible.builtin.copy:
        src: /srv/myfiles/foo.conf
        dest: /etc/foo.conf
        owner: foo
        group: foo
        mode: '0644'
    """

    SECURITY_CHECKS = [
        lambda file_name, component: AnsibleBuiltinCopy._security_check_file_permissions(
            file_name=file_name,
            component=component,
            module_name=AnsibleBuiltinCopy.MODULE_NAME,
        )
    ]
    MODULE_NAME = "ansible.builtin.copy"

    @classmethod
    def _get_security_checks(cls) -> list:
        return cls.SECURITY_CHECKS
