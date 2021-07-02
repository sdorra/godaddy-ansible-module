
# Copyright: (c) 2020, Sebastian Sdorra <s.sdorra@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: godaddy_record

short_description: Manage Godaddy DNS Records

version_added: "2.4"

description:
    - "Create, delete and update GoDaddy DNS Records"

options:
    name:
        description:
            - Name of the dns recors
        required: true
    type:
        description:
            - Type of record
        required: true

author:
    - Sebastian Sdorra (@ssdorra)
'''

EXAMPLES = '''
# Update A Record
- name: Test with a message
  godaddy_record:
    name: mail
    type: A
'''

RETURN = '''
original_message:
    description: The original name param that was passed in
    type: str
    returned: always
message:
    description: The output message that the test module generates
    type: str
    returned: always
'''

from ansible.module_utils.basic import AnsibleModule
from godaddypy import Client, Account

SUPPORTED_RECORD_TYPES = ['A', 'AAAA', 'CNAME', 'SRV', 'TXT', 'SOA', 'NS', 'MX', 'SPF', 'PTR']

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        api_key=dict(type='str', required=True),
        api_secret=dict(type='str', required=True),
        domain=dict(type='str', required=True),
        name=dict(type='str', required=True),
        type=dict(type='str', required=False, default="A", choices=SUPPORTED_RECORD_TYPES),
        data=dict(type='str',required=True),
        ttl=dict(type='int', required=False, default=3600),
        # TODO
        state= dict(default='present', choices=['present', 'absent'])
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False
        #original_message='',
        #message=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    client = Client(Account(api_key=module.params['api_key'], api_secret=module.params['api_secret']))

    domain = module.params['domain']
    t = module.params['type']
    name = module.params['name']
    ttl = module.params['ttl']
    data = module.params['data']

    recs = client.get_records(domain, record_type=t, name=name)
    if len(recs) == 0:
        client.add_record(domain, {'data': data, 'name': name, 'ttl': ttl, 'type': t})
        result['changed'] = True
    else:
        rec = recs[0]
        if rec['data'] != data or rec['ttl'] != ttl:
            rec['data'] = data 
            rec['ttl'] = ttl
            client.update_record(domain, {'data': data, 'name': name, 'ttl': ttl, 'type': t})
            result['changed'] = True

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    #result['original_message'] = module.params['name']
    #result['message'] = 'goodbye'

    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target
    #if module.params['new']:
    #    result['changed'] = True

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    #if module.params['name'] == 'fail me':
    #    module.fail_json(msg='You requested this to fail', **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
