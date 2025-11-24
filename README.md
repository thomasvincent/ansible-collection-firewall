# Ansible Collection - thomasvincent.firewall

[![CI](https://github.com/thomasvincent/ansible-collection-firewall/workflows/CI/badge.svg)](https://github.com/thomasvincent/ansible-collection-firewall/actions/workflows/ci.yml)
[![Release](https://github.com/thomasvincent/ansible-collection-firewall/workflows/Release/badge.svg)](https://github.com/thomasvincent/ansible-collection-firewall/actions/workflows/release.yml)
[![License](https://img.shields.io/badge/license-GPL--3.0-blue.svg)](LICENSE)
[![Ansible Galaxy](https://img.shields.io/badge/galaxy-thomasvincent.firewall-blue.svg)](https://galaxy.ansible.com/thomasvincent/firewall)

Enterprise-grade firewall management collection for Ansible. Provides unified interface for managing multiple firewall backends (firewalld, UFW, iptables, nftables) with comprehensive testing and documentation.

## Features

- **Multi-Backend Support**: Unified interface for firewalld, UFW, iptables, and nftables
- **Automatic Detection**: Automatically detects and uses appropriate firewall backend
- **Enterprise Testing**: Comprehensive Molecule tests across multiple distributions
- **Custom Modules**: Advanced firewall_rule module for unified rule management
- **Rich Filters**: Port validation, CIDR validation, service-to-port conversion
- **Lookup Plugins**: Service port lookup functionality
- **Production Ready**: Tested across CentOS, Ubuntu, Debian, and RHEL
- **CI/CD Integration**: Complete GitHub Actions workflows for testing and releases
- **Full Documentation**: Comprehensive documentation with examples

## Requirements

- Ansible >= 2.14.0
- Python >= 3.6
- Appropriate firewall backend installed on target systems

### Supported Platforms

- **RHEL/CentOS**: 8, 9 (firewalld)
- **Ubuntu**: 20.04, 22.04, 24.04 (UFW/iptables)
- **Debian**: 11, 12 (nftables/iptables)

## Installation

### From Ansible Galaxy

```bash
ansible-galaxy collection install thomasvincent.firewall
```

### From GitHub

```bash
ansible-galaxy collection install git+https://github.com/thomasvincent/ansible-collection-firewall.git
```

### From Tarball

```bash
ansible-galaxy collection install thomasvincent-firewall-1.0.0.tar.gz
```

## Quick Start

### Basic Firewall Configuration

```yaml
---
- name: Configure firewall
  hosts: all
  become: true

  roles:
    - role: thomasvincent.firewall.firewall
      vars:
        firewall_enabled: true
        firewall_allow_ssh: true
        firewall_rules:
          - name: Allow HTTP
            port: 80
            protocol: tcp
            state: allow
          - name: Allow HTTPS
            port: 443
            protocol: tcp
            state: allow
```

### Using Custom Module

```yaml
---
- name: Manage firewall rules
  hosts: all
  become: true

  tasks:
    - name: Allow HTTP traffic
      thomasvincent.firewall.firewall_rule:
        name: allow_http
        port: 80
        protocol: tcp
        action: accept
        state: present

    - name: Block specific IP
      thomasvincent.firewall.firewall_rule:
        name: block_malicious_ip
        source: 10.0.0.1
        action: drop
        state: present
```

### Using Filters

```yaml
---
- name: Use firewall filters
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Validate port number
      debug:
        msg: "Port 80 is {{ '80' | thomasvincent.firewall.validate_port | ternary('valid', 'invalid') }}"

    - name: Convert service to port
      debug:
        msg: "HTTP uses port {{ 'http' | thomasvincent.firewall.service_to_port }}"

    - name: Merge port ranges
      debug:
        msg: "Merged ports: {{ [80, 81, 82, 90, 91] | thomasvincent.firewall.merge_port_ranges }}"
```

## Roles

### firewall

Main role for managing firewall configuration across multiple backends.

#### Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `firewall_enabled` | `true` | Enable firewall service |
| `firewall_backend` | Auto-detected | Firewall backend (firewalld, ufw, iptables, nftables) |
| `firewall_allow_ssh` | `true` | Allow SSH access |
| `firewall_ssh_port` | `22` | SSH port number |
| `firewall_default_policy_input` | `DROP` | Default policy for incoming traffic |
| `firewall_default_policy_output` | `ACCEPT` | Default policy for outgoing traffic |
| `firewall_default_policy_forward` | `DROP` | Default policy for forwarded traffic |
| `firewall_rules` | `[]` | List of firewall rules |
| `firewall_zones` | `[]` | Firewall zones (firewalld only) |

#### Firewall Rules Format

```yaml
firewall_rules:
  - name: "Rule description"
    port: 80  # or port range "8080-8090"
    protocol: tcp  # tcp, udp, icmp, any
    state: allow  # allow, deny, reject
    source: "192.168.1.0/24"  # optional
    destination: "10.0.0.1"  # optional
    zone: public  # optional (firewalld)
```

#### Examples

**Basic HTTP/HTTPS Server**:

```yaml
- role: thomasvincent.firewall.firewall
  vars:
    firewall_rules:
      - name: Allow HTTP
        port: 80
        protocol: tcp
      - name: Allow HTTPS
        port: 443
        protocol: tcp
```

**Database Server with IP Restriction**:

```yaml
- role: thomasvincent.firewall.firewall
  vars:
    firewall_rules:
      - name: Allow PostgreSQL from app servers
        port: 5432
        protocol: tcp
        source: 192.168.1.0/24
```

**Multi-Zone Configuration (firewalld)**:

```yaml
- role: thomasvincent.firewall.firewall
  vars:
    firewall_backend: firewalld
    firewall_zones:
      - name: public
        state: enabled
        services:
          - ssh
          - http
          - https
        ports:
          - port: 8080
            protocol: tcp
      - name: internal
        state: enabled
        services:
          - ssh
          - mysql
```

## Modules

### firewall_rule

Unified module for managing firewall rules across multiple backends.

#### Parameters

| Parameter | Required | Default | Choices | Description |
|-----------|----------|---------|---------|-------------|
| name | yes | - | - | Name of the firewall rule |
| state | no | present | present, absent, enabled, disabled | State of the rule |
| port | conditional | - | - | Port number or range |
| protocol | no | tcp | tcp, udp, icmp, any | Protocol |
| source | no | - | - | Source IP or CIDR |
| destination | no | - | - | Destination IP or CIDR |
| action | no | accept | accept, drop, reject | Action for matching packets |
| direction | no | inbound | inbound, outbound, both | Traffic direction |
| zone | no | public | - | Firewall zone (firewalld) |
| backend | no | auto | auto, firewalld, ufw, iptables, nftables | Force specific backend |
| priority | no | 100 | - | Rule priority |

#### Examples

See [Module Documentation](docs/modules/firewall_rule.md) for detailed examples.

## Filters

### validate_port

Validates port numbers or ranges.

```yaml
- debug:
    msg: "{{ '80' | thomasvincent.firewall.validate_port }}"
```

### validate_cidr

Validates CIDR notation.

```yaml
- debug:
    msg: "{{ '192.168.1.0/24' | thomasvincent.firewall.validate_cidr }}"
```

### service_to_port

Converts service name to port number.

```yaml
- debug:
    msg: "{{ 'https' | thomasvincent.firewall.service_to_port }}"
```

### port_to_service

Converts port number to service name.

```yaml
- debug:
    msg: "{{ 443 | thomasvincent.firewall.port_to_service }}"
```

### merge_port_ranges

Merges overlapping port ranges.

```yaml
- debug:
    msg: "{{ [80, 81, 82, 100, 101] | thomasvincent.firewall.merge_port_ranges }}"
```

See [Filter Documentation](docs/filters/firewall_filters.md) for complete list.

## Lookup Plugins

### firewall_ports

Lookup service ports or names.

```yaml
- debug:
    msg: "{{ lookup('thomasvincent.firewall.firewall_ports', 'http', 'https') }}"
```

## Development

### Running Tests Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run ansible-lint
ansible-lint

# Run Molecule tests
cd roles/firewall
molecule test

# Run specific scenario
molecule test -s default
```

### Building Collection

```bash
ansible-galaxy collection build
```

### Installing Development Version

```bash
ansible-galaxy collection install thomasvincent-firewall-*.tar.gz --force
```

## Testing

This collection includes comprehensive testing:

- **Sanity Tests**: Ansible sanity tests across multiple versions
- **Lint Tests**: ansible-lint and yamllint
- **Molecule Tests**: Multi-distribution Docker-based tests
- **Integration Tests**: ansible-test integration tests
- **Unit Tests**: Python unit tests for modules and plugins

See [Testing Guide](docs/testing.md) for details.

## CI/CD

Complete CI/CD pipeline using GitHub Actions:

- Automated testing on every PR and push
- Multi-platform testing (CentOS, Ubuntu, Debian)
- Automatic releases with semantic versioning
- Ansible Galaxy publishing
- Documentation deployment to GitHub Pages

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Security

For security issues, please see [SECURITY.md](SECURITY.md).

## License

GNU General Public License v3.0 or later

See [LICENSE](LICENSE) for full text.

## Author

Thomas Vincent (@thomasvincent)

## Support

- **Issues**: [GitHub Issues](https://github.com/thomasvincent/ansible-collection-firewall/issues)
- **Discussions**: [GitHub Discussions](https://github.com/thomasvincent/ansible-collection-firewall/discussions)
- **Documentation**: [https://thomasvincent.github.io/ansible-collection-firewall](https://thomasvincent.github.io/ansible-collection-firewall)

## Acknowledgments

Special thanks to the Ansible community and contributors.

## Related Collections

- [ansible.posix](https://galaxy.ansible.com/ansible/posix) - POSIX utilities including firewalld module
- [community.general](https://galaxy.ansible.com/community/general) - Includes UFW module
