class AnsibleBuiltinGetUrl:
    """
    Description of Ansible Builtin Copy Module:
    https://docs.ansible.com/ansible/latest/collections/ansible/builtin/get_url_module.html

    - name: < Fetch file that requires authentication.
      username/password only available since 2.8, in older versions you need to use url_username/url_password
      ansible.builtin.get_url:
        url: http://example.com/path/file.conf
        dest: /etc/foo.conf
        username: bar
        password: '{{ mysecret }}'
    """

    MODULE_NAME = "ansible.builtin.get_url"

    # tutaj mode i url/ftp http itp. i jeszcze password
