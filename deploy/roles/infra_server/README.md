## Creating .htpasswd file

The Ansible code currently hardcodes a basic auth file at /etc/nginx/.htpasswd.

You can add users to this file using the `htpasswd` command:

```bash
sudo htpasswd -c /etc/nginx/.htpasswd sammy
```
