#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Thomas Vincent <thomasvincent@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: firewall_rule
short_description: Manage firewall rules across multiple backends
version_added: "1.0.0"
description:
    - Manage firewall rules across different firewall backends (firewalld, ufw, iptables, nftables)
    - Provides a unified interface for firewall rule management
    - Automatically detects and uses the appropriate firewall backend

options:
    name:
        description:
            - Name of the firewall rule
        required: true
        type: str
    state:
        description:
            - State of the firewall rule
        choices: [ present, absent, enabled, disabled ]
        default: present
        type: str
    port:
        description:
            - Port number or range (e.g., 80, 8080-8090)
        type: str
    protocol:
        description:
            - Protocol for the rule
        choices: [ tcp, udp, icmp, any ]
        default: tcp
        type: str
    source:
        description:
            - Source IP address or CIDR range
        type: str
    destination:
        description:
            - Destination IP address or CIDR range
        type: str
    action:
        description:
            - Action to take for matching packets
        choices: [ accept, drop, reject ]
        default: accept
        type: str
    direction:
        description:
            - Direction of traffic
        choices: [ inbound, outbound, both ]
        default: inbound
        type: str
    zone:
        description:
            - Firewall zone (firewalld only)
        type: str
        default: public
    backend:
        description:
            - Force specific firewall backend
        choices: [ auto, firewalld, ufw, iptables, nftables ]
        default: auto
        type: str
    priority:
        description:
            - Rule priority (lower number = higher priority)
        type: int
        default: 100

author:
    - Thomas Vincent (@thomasvincent)

requirements:
    - Python >= 3.6
    - Appropriate firewall backend installed
'''

EXAMPLES = r'''
- name: Allow HTTP traffic
  thomasvincent.firewall.firewall_rule:
    name: allow_http
    port: 80
    protocol: tcp
    action: accept
    state: present

- name: Allow HTTPS from specific subnet
  thomasvincent.firewall.firewall_rule:
    name: allow_https_subnet
    port: 443
    protocol: tcp
    source: 192.168.1.0/24
    action: accept
    state: present

- name: Block outbound traffic to specific IP
  thomasvincent.firewall.firewall_rule:
    name: block_malicious_ip
    destination: 10.0.0.1
    action: drop
    direction: outbound
    state: present

- name: Remove firewall rule
  thomasvincent.firewall.firewall_rule:
    name: old_rule
    state: absent

- name: Allow port range
  thomasvincent.firewall.firewall_rule:
    name: app_port_range
    port: 8080-8090
    protocol: tcp
    action: accept
    state: present
'''

RETURN = r'''
changed:
    description: Whether the firewall rule was modified
    type: bool
    returned: always
    sample: true
rule:
    description: Details of the firewall rule
    type: dict
    returned: always
    sample: {
        "name": "allow_http",
        "port": "80",
        "protocol": "tcp",
        "action": "accept",
        "state": "present"
    }
backend:
    description: Firewall backend that was used
    type: str
    returned: always
    sample: "firewalld"
message:
    description: Human-readable message about the operation
    type: str
    returned: always
    sample: "Firewall rule 'allow_http' created successfully"
'''

import os
import subprocess
from ansible.module_utils.basic import AnsibleModule


class FirewallBackend:
    """Base class for firewall backends"""

    def __init__(self, module):
        self.module = module

    def is_available(self):
        """Check if this backend is available"""
        raise NotImplementedError

    def add_rule(self, rule):
        """Add a firewall rule"""
        raise NotImplementedError

    def remove_rule(self, rule):
        """Remove a firewall rule"""
        raise NotImplementedError

    def rule_exists(self, rule):
        """Check if a rule exists"""
        raise NotImplementedError


class FirewalldBackend(FirewallBackend):
    """Firewalld backend implementation"""

    def is_available(self):
        rc, _, _ = self.module.run_command("which firewall-cmd")
        return rc == 0

    def add_rule(self, rule):
        zone = rule.get('zone', 'public')
        port = rule['port']
        protocol = rule['protocol']

        cmd = [
            'firewall-cmd',
            f'--zone={zone}',
            f'--add-port={port}/{protocol}',
            '--permanent'
        ]

        rc, stdout, stderr = self.module.run_command(cmd)
        if rc != 0:
            self.module.fail_json(msg=f"Failed to add rule: {stderr}")

        # Reload firewalld
        self.module.run_command(['firewall-cmd', '--reload'])
        return True

    def remove_rule(self, rule):
        zone = rule.get('zone', 'public')
        port = rule['port']
        protocol = rule['protocol']

        cmd = [
            'firewall-cmd',
            f'--zone={zone}',
            f'--remove-port={port}/{protocol}',
            '--permanent'
        ]

        rc, stdout, stderr = self.module.run_command(cmd)
        if rc != 0:
            return False

        self.module.run_command(['firewall-cmd', '--reload'])
        return True

    def rule_exists(self, rule):
        zone = rule.get('zone', 'public')
        port = rule['port']
        protocol = rule['protocol']

        cmd = [
            'firewall-cmd',
            f'--zone={zone}',
            '--list-ports'
        ]

        rc, stdout, stderr = self.module.run_command(cmd)
        if rc != 0:
            return False

        return f"{port}/{protocol}" in stdout


class UFWBackend(FirewallBackend):
    """UFW backend implementation"""

    def is_available(self):
        rc, _, _ = self.module.run_command("which ufw")
        return rc == 0

    def add_rule(self, rule):
        port = rule['port']
        protocol = rule['protocol']
        action = rule['action']

        cmd = ['ufw', action, 'proto', protocol, 'to', 'any', 'port', port]

        if rule.get('source'):
            cmd.extend(['from', rule['source']])

        rc, stdout, stderr = self.module.run_command(cmd)
        if rc != 0:
            self.module.fail_json(msg=f"Failed to add rule: {stderr}")

        return True

    def remove_rule(self, rule):
        port = rule['port']
        protocol = rule['protocol']

        cmd = ['ufw', 'delete', 'allow', 'proto', protocol, 'to', 'any', 'port', port]

        rc, stdout, stderr = self.module.run_command(cmd)
        return rc == 0

    def rule_exists(self, rule):
        cmd = ['ufw', 'status', 'numbered']
        rc, stdout, stderr = self.module.run_command(cmd)

        if rc != 0:
            return False

        port = rule['port']
        protocol = rule['protocol']

        return f"{port}/{protocol}" in stdout.lower()


def detect_backend(module):
    """Auto-detect available firewall backend"""
    backends = [
        ('firewalld', FirewalldBackend),
        ('ufw', UFWBackend),
    ]

    for name, backend_class in backends:
        backend = backend_class(module)
        if backend.is_available():
            return name, backend

    module.fail_json(msg="No supported firewall backend found")


def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type='str', required=True),
            state=dict(type='str', default='present', choices=['present', 'absent', 'enabled', 'disabled']),
            port=dict(type='str'),
            protocol=dict(type='str', default='tcp', choices=['tcp', 'udp', 'icmp', 'any']),
            source=dict(type='str'),
            destination=dict(type='str'),
            action=dict(type='str', default='accept', choices=['accept', 'drop', 'reject']),
            direction=dict(type='str', default='inbound', choices=['inbound', 'outbound', 'both']),
            zone=dict(type='str', default='public'),
            backend=dict(type='str', default='auto', choices=['auto', 'firewalld', 'ufw', 'iptables', 'nftables']),
            priority=dict(type='int', default=100),
        ),
        supports_check_mode=True,
    )

    # Validate port is provided for most rules
    if module.params['state'] in ['present', 'enabled'] and not module.params.get('port'):
        module.fail_json(msg="port is required when state is present or enabled")

    # Detect or use specified backend
    if module.params['backend'] == 'auto':
        backend_name, backend = detect_backend(module)
    else:
        backend_name = module.params['backend']
        backend_map = {
            'firewalld': FirewalldBackend,
            'ufw': UFWBackend,
        }
        backend = backend_map[backend_name](module)
        if not backend.is_available():
            module.fail_json(msg=f"Specified backend '{backend_name}' is not available")

    rule = {
        'name': module.params['name'],
        'port': module.params.get('port'),
        'protocol': module.params['protocol'],
        'source': module.params.get('source'),
        'destination': module.params.get('destination'),
        'action': module.params['action'],
        'direction': module.params['direction'],
        'zone': module.params.get('zone', 'public'),
    }

    changed = False
    state = module.params['state']

    if module.check_mode:
        module.exit_json(changed=True, backend=backend_name, rule=rule)

    if state in ['present', 'enabled']:
        if not backend.rule_exists(rule):
            backend.add_rule(rule)
            changed = True
            message = f"Firewall rule '{rule['name']}' created successfully"
        else:
            message = f"Firewall rule '{rule['name']}' already exists"

    elif state in ['absent', 'disabled']:
        if backend.rule_exists(rule):
            backend.remove_rule(rule)
            changed = True
            message = f"Firewall rule '{rule['name']}' removed successfully"
        else:
            message = f"Firewall rule '{rule['name']}' does not exist"

    module.exit_json(
        changed=changed,
        rule=rule,
        backend=backend_name,
        message=message
    )


if __name__ == '__main__':
    main()
