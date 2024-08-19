# pinkhat-iac

# Quick start
The application will scan the given target file or folder:
```shell
python pinkhat/main.py <<path_to_file_or_folder>>
```
Currently, the application only gives json output.

Usage:
```
usage: pinkhat [OPTION] [DIRECTORY]...

pinkhat 1.0.0 Application executes defined policy checks on the given directory path

positional arguments:
  files          file directory/directories or file/files

options:
  -h, --help     show this help message and exit
  -v, --version  show program's version number and exit
```

# Writing own policies
```yaml
version: 1.0
policies:
  - module: "Module name"
    category: "yaml or terraform"
    rules:
      - name: "Rule name"
        link: "yaml or terraform"
        description: "Short description"
        remediation: "Short remediation"
        failureMessage: "On failure put a message"
        report_on: "true or false - report only if statement is true or false"
        helper: "Jinja script that allows you to run additional actions"
        statement: "Jinja statement that verifies the defined policy"
```

# Terraform policies
Pinkhat reads the terraform files (*.tf) and generates a graph in memory for it.
```terraform
resource "aws_ecr_repository" "ecr_repository_name" {
  ...
  image_scanning_configuration {
    scan_on_push = true
  }
  ...
}
```
The above code is converted to JSON, and it's an object.
- You can get access to the fields by using **this** key word and **object**
- You can use **.** or **get**, it works like ordinary python operation on **dict**

```python
this.object.get('image_scanning_configuration', [])
```

## Local and other variables support
In terraform it is possible to override local and other types of variables:

https://github.com/hashicorp/terraform/issues/18351

It might even contain some expression, it is really difficult to predict if a user overriden a variable from command line or other file. So, it makes it impossible to say what is the actual condition of some statements etc.
More information about variables:

https://developer.hashicorp.com/terraform/language/values/locals

It means that if there are no default values assigned in terraform resources, then always it will be reported as an issue. It might increase a number of false positives.
