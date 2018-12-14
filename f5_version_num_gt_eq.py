#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: f5_version_num_gt_eq

short_description: This module will return True if the version passed in is greater than or equal 
    to a particular version. Else it will return False.

description:
    - "This module will return True if the version passed in is greater than or equal 
    to a particular version. Else it will return False."

options:
    version_number_one:
        description:
            - This is the version to check
        required: true
    version_number_two:
        description:
            - This is the lower-bound version that will be compared to version_to_check. Any
              value below this number will return False. Any value greater than or equal to this
              number will return True.
        required: true

author:
    - Chris Zacny
'''

EXAMPLES = '''
# Test - should return True
- name: Check version
  f5_version_num_gt_eq:
    version_number_one: 13.1.0
    version_number_two: 12.1.3
'''

RETURN = '''
original_message:
    description: The original name param that was passed in
    type: str
message:
    description: The output message that the sample module generates
'''

from ansible.module_utils.basic import AnsibleModule
from collections import deque


class QueuesLenNotEqualError(Exception):
    pass


class VersionInfo(object):
    Major = 0
    Minor = 1
    Build = 2
    Revision = 3

    def __init__(self, version_string):
        split_version = version_string.split('.')
        self.major = int(split_version[VersionInfo.Major])
        self.minor = int(split_version[VersionInfo.Minor])
        self.build = int(split_version[VersionInfo.Build])
        if len(split_version) > 3:
            try:
                self.revision = int(split_version[VersionInfo.Revision])
            except ValueError:
                self.revision = 0
        else:
            self.revision = 0

    def reursive_gt_check(self, number_queue_1, number_queue_2):
        # Constraint is that len(number_queue_1) and len(number_queue_2) must be equal
        if len(number_queue_1) != len(number_queue_2):
            raise QueuesLenNotEqualError
        try:
            val1 = number_queue_1.popleft()
            val2 = number_queue_2.popleft()
        except IndexError:
            # At this point, we can assume the versions are equal
            return True

        if val1 > val2:
            return True
        elif val1 == val2:
            return self.reursive_gt_check(number_queue_1, number_queue_2)
        else:
            return False

    def __gt__(self, other):
        return self.reursive_gt_check(deque([self.major, self.minor, self.build, self.revision]),
                                      deque([other.major, other.minor, other.build, other.revision]))

    def __ge__(self, other):
        if self.__eq__(other):
            return True
        elif self.__gt__(other):
            return True
        return False

    def __eq__(self, other):
        if self.major == other.major and \
                self.minor == other.minor and \
                self.build == other.build and \
                self.revision == other.revision:
            return True
        return False

    def __repr__(self):
        return '{}.{}.{}.{}'.format(self.major, self.minor, self.build, self.revision)

    def __str__(self):
        return self.__repr__()


def execute_version_check(version_number_one, version_number_two):
    """
    This method will check if version_number_one >= version_number_two.
    F5 versions of of the form A.B.C.D(.*). Here, we only care about A.B.C.D. The fourth
    digit is not required. If there is ever a fifth digit introduced, this won't work.
    :param version_number_one:
    :param version_number_two:
    :return: If >= return True. If < return False.
    """
    version_number_one_obj = VersionInfo(version_number_one)
    version_number_two_obj = VersionInfo(version_number_two)

    if version_number_one_obj >= version_number_two_obj:
        return True

    return False


def run_module():
    module_args = dict(
        version_number_one=dict(type='str', required=True),
        version_number_two=dict(type='str', required=False, default='13.1.0')
    )
    result = dict(
        changed=False,
        result=''
    )
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )
    result['result'] = execute_version_check(module_args['version_number_one'], module_args['version_number_two'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
