#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Thomas Vincent <thomasvincent@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
name: firewall_ports
author: Thomas Vincent (@thomasvincent)
version_added: "1.0.0"
short_description: Lookup common service ports
description:
    - Returns port numbers for common services
    - Supports both service name to port and port to service name lookups
options:
    _terms:
        description: Service name or port number to lookup
        required: True
    protocol:
        description: Protocol (tcp or udp)
        type: string
        default: tcp
'''

EXAMPLES = '''
- name: Get port for HTTP
  debug:
    msg: "HTTP port is {{ lookup('thomasvincent.firewall.firewall_ports', 'http') }}"

- name: Get service name for port 443
  debug:
    msg: "Port 443 is {{ lookup('thomasvincent.firewall.firewall_ports', '443') }}"

- name: Get multiple ports
  debug:
    msg: "Ports are {{ lookup('thomasvincent.firewall.firewall_ports', 'http', 'https', 'ssh') }}"
'''

RETURN = '''
_list:
    description: List of port numbers or service names
    type: list
'''

from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase


# Comprehensive service to port mapping
SERVICE_PORTS = {
    'tcp': {
        'ftp-data': 20,
        'ftp': 21,
        'ssh': 22,
        'telnet': 23,
        'smtp': 25,
        'dns': 53,
        'http': 80,
        'pop3': 110,
        'imap': 143,
        'https': 443,
        'smtps': 465,
        'submission': 587,
        'imaps': 993,
        'pop3s': 995,
        'mssql': 1433,
        'mysql': 3306,
        'rdp': 3389,
        'postgresql': 5432,
        'redis': 6379,
        'http-alt': 8080,
        'https-alt': 8443,
        'elasticsearch': 9200,
        'mongodb': 27017,
    },
    'udp': {
        'dns': 53,
        'dhcp-server': 67,
        'dhcp-client': 68,
        'tftp': 69,
        'ntp': 123,
        'snmp': 161,
        'snmp-trap': 162,
        'syslog': 514,
    }
}


class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):
        protocol = kwargs.get('protocol', 'tcp').lower()

        if protocol not in SERVICE_PORTS:
            raise AnsibleError(f"Invalid protocol: {protocol}")

        results = []
        port_map = SERVICE_PORTS[protocol]
        reverse_map = {v: k for k, v in port_map.items()}

        for term in terms:
            term = str(term).lower().strip()

            # Check if term is a service name
            if term in port_map:
                results.append(port_map[term])
            # Check if term is a port number
            elif term.isdigit():
                port_num = int(term)
                service_name = reverse_map.get(port_num)
                if service_name:
                    results.append(service_name)
                else:
                    results.append(port_num)
            else:
                raise AnsibleError(f"Unknown service or invalid port: {term}")

        return results
