from iacparsers.ansible.core.ansible_permission_core import AnsiblePermissionCore


class AnsibleBuiltinFile(AnsiblePermissionCore):
    """
    Description of Ansible Builtin File Module:
    https://docs.ansible.com/ansible/latest/collections/ansible/builtin/file_module.html

    - name: Give insecure permissions to an existing file
      ansible.builtin.file:
        path: /work
        owner: root
        group: root
        mode: '1777'
    """

    SECURITY_CHECKS = [
        lambda file_name, component: AnsibleBuiltinFile._security_check_file_permissions(
            file_name=file_name,
            component=component,
            module_name=AnsibleBuiltinFile.MODULE_NAME,
        )
    ]
    MODULE_NAME = "ansible.builtin.file"

    @classmethod
    def _get_security_checks(cls) -> list:
        return cls.SECURITY_CHECKS
