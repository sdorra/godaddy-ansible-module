# Ansible Role for GoDaddy API

## Installation

Just clone the repository and add the library folder to the ansible module path.
For more information have a look at the [ansible documentation](https://docs.ansible.com/ansible/latest/dev_guide/developing_locally.html#adding-a-module-locally).

## Usage

```yaml
- name: Setup dns record for dns.example.net
  godaddy_record:
    api_key: "your_api_key"
    api_secret: "your_api_secret"
    domain: "example.net"
    name: "dns"
    type: "A"
    data: "8.8.8.8"
```
