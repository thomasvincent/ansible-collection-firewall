#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2025, Thomas Vincent <thomasvincent@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
name: firewall_filters
author: Thomas Vincent (@thomasvincent)
version_added: "1.0.0"
short_description: Filters for firewall rule manipulation
description:
    - Provides filters for parsing, validating, and transforming firewall rules
'''

import re
from ansible.errors import AnsibleFilterError


def validate_port(port):
    """Validate port number or range"""
    if isinstance(port, int):
        return 1 <= port <= 65535

    if isinstance(port, str):
        # Check for port range
        if '-' in port:
            try:
                start, end = map(int, port.split('-'))
                return 1 <= start <= end <= 65535
            except ValueError:
                return False

        # Check for single port
        try:
            port_num = int(port)
            return 1 <= port_num <= 65535
        except ValueError:
            return False

    return False


def validate_cidr(cidr):
    """Validate CIDR notation"""
    if '/' not in cidr:
        return False

    try:
        ip, prefix = cidr.split('/')
        prefix = int(prefix)

        # Check prefix length
        if not (0 <= prefix <= 32):
            return False

        # Check IP address
        octets = ip.split('.')
        if len(octets) != 4:
            return False

        for octet in octets:
            num = int(octet)
            if not (0 <= num <= 255):
                return False

        return True
    except (ValueError, AttributeError):
        return False


def normalize_port_range(port):
    """Normalize port to standard format"""
    if isinstance(port, int):
        return str(port)

    if isinstance(port, str):
        port = port.strip()
        if '-' in port:
            start, end = map(int, port.split('-'))
            return f"{start}-{end}"
        return str(int(port))

    raise AnsibleFilterError(f"Invalid port format: {port}")


def port_to_service(port, protocol='tcp'):
    """Convert port number to common service name"""
    services = {
        ('20', 'tcp'): 'ftp-data',
        ('21', 'tcp'): 'ftp',
        ('22', 'tcp'): 'ssh',
        ('23', 'tcp'): 'telnet',
        ('25', 'tcp'): 'smtp',
        ('53', 'tcp'): 'dns',
        ('53', 'udp'): 'dns',
        ('80', 'tcp'): 'http',
        ('110', 'tcp'): 'pop3',
        ('143', 'tcp'): 'imap',
        ('443', 'tcp'): 'https',
        ('465', 'tcp'): 'smtps',
        ('587', 'tcp'): 'submission',
        ('993', 'tcp'): 'imaps',
        ('995', 'tcp'): 'pop3s',
        ('3306', 'tcp'): 'mysql',
        ('5432', 'tcp'): 'postgresql',
        ('6379', 'tcp'): 'redis',
        ('8080', 'tcp'): 'http-alt',
        ('8443', 'tcp'): 'https-alt',
    }

    return services.get((str(port), protocol.lower()), None)


def service_to_port(service):
    """Convert service name to port number"""
    services = {
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
        'mysql': 3306,
        'postgresql': 5432,
        'redis': 6379,
        'http-alt': 8080,
        'https-alt': 8443,
    }

    return services.get(service.lower(), None)


def group_rules_by_protocol(rules):
    """Group firewall rules by protocol"""
    grouped = {}

    for rule in rules:
        protocol = rule.get('protocol', 'tcp')
        if protocol not in grouped:
            grouped[protocol] = []
        grouped[protocol].append(rule)

    return grouped


def filter_rules_by_port_range(rules, min_port, max_port):
    """Filter rules within a port range"""
    filtered = []

    for rule in rules:
        port = rule.get('port')
        if not port:
            continue

        try:
            if isinstance(port, int):
                if min_port <= port <= max_port:
                    filtered.append(rule)
            elif '-' in str(port):
                start, end = map(int, str(port).split('-'))
                if not (end < min_port or start > max_port):
                    filtered.append(rule)
            else:
                port_num = int(port)
                if min_port <= port_num <= max_port:
                    filtered.append(rule)
        except (ValueError, AttributeError):
            continue

    return filtered


def merge_port_ranges(ports):
    """Merge overlapping port ranges"""
    if not ports:
        return []

    # Convert all ports to (start, end) tuples
    ranges = []
    for port in ports:
        if isinstance(port, int):
            ranges.append((port, port))
        elif '-' in str(port):
            start, end = map(int, str(port).split('-'))
            ranges.append((start, end))
        else:
            p = int(port)
            ranges.append((p, p))

    # Sort ranges
    ranges.sort()

    # Merge overlapping ranges
    merged = [ranges[0]]
    for current in ranges[1:]:
        last = merged[-1]
        if current[0] <= last[1] + 1:
            merged[-1] = (last[0], max(last[1], current[1]))
        else:
            merged.append(current)

    # Convert back to string format
    result = []
    for start, end in merged:
        if start == end:
            result.append(str(start))
        else:
            result.append(f"{start}-{end}")

    return result


class FilterModule:
    """Ansible filter plugin for firewall operations"""

    def filters(self):
        return {
            'validate_port': validate_port,
            'validate_cidr': validate_cidr,
            'normalize_port_range': normalize_port_range,
            'port_to_service': port_to_service,
            'service_to_port': service_to_port,
            'group_rules_by_protocol': group_rules_by_protocol,
            'filter_rules_by_port_range': filter_rules_by_port_range,
            'merge_port_ranges': merge_port_ranges,
        }
