#! /usr/bin/env python3

from subprocess import PIPE, run 
from sys import exit


VALID_BRANCH_TYPES = [
    'feature',
    'bugfix',
    'hotfix',
    'refactor',
]

def create_release_branch():
    current_branch_name = run(['git', 'branch', '--show-current'], capture_output=True).stdout
    current_branch_name = current_branch_name.decode('utf-8').strip()
    _validate_branch_name(current_branch_name)
    release_branch_name = _get_release_branch_name(current_branch_name)
    _switch_to_release_branch(release_branch_name)

    run(['git', 'pull', 'origin', 'stable'])
    run(['git', 'pull', 'origin', current_branch_name])
    run(['git', 'push', 'origin', release_branch_name])
    run(['git', 'checkout', current_branch_name])
    

def _switch_to_release_branch(branch_name):
    checkout_message = run(['git', 'checkout', '-b', branch_name], capture_output=True).stderr
    checkout_message = checkout_message.decode('utf-8').strip()
    if 'already exists' in checkout_message:
        run(['git', 'checkout', branch_name])


def _get_release_branch_name(current_branch_name):
    branch_type = _get_branch_type_from_branch_name(current_branch_name)
    release_branch_name = current_branch_name.replace(branch_type, 'release')
    return release_branch_name


def _validate_branch_name(current_branch_name):
    if current_branch_name is None:
        print('Enter in git repository')
        exit(1)
    branch_type = _get_branch_type_from_branch_name(current_branch_name)
    if branch_type not in VALID_BRANCH_TYPES:
        valid_branch_types_str = ', '.join([type for type in VALID_BRANCH_TYPES])
        print(f'Your branch type must be one of then {valid_branch_types_str}')
        exit(1)


def _get_branch_type_from_branch_name(branch_name):
    final_branch_type_index = branch_name.find('/')
    branch_type = branch_name[0:final_branch_type_index]
    return branch_type


def main():
    create_release_branch()
    exit(0)


if __name__ == '__main__':
    main()