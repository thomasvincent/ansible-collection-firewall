# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Enterprise-grade firewall management collection
- Multi-backend support (firewalld, UFW, iptables, nftables)
- Automatic firewall backend detection
- Custom `firewall_rule` module for unified rule management
- Filter plugins for port validation, CIDR validation, and service-to-port conversion
- Lookup plugin for service port lookups
- Comprehensive Molecule testing across multiple distributions
- GitHub Actions CI/CD pipelines
- ansible-lint and yamllint configuration
- Example playbooks for common scenarios
- Full documentation with README, CONTRIBUTING, and SECURITY guides

### Roles
- `firewall` - Main role for managing firewall configuration
  - Support for firewalld (RHEL/CentOS)
  - Support for UFW (Ubuntu/Debian)
  - Support for iptables (legacy systems)
  - Support for nftables (modern Debian)
  - Multi-zone support for firewalld
  - Customizable default policies
  - Rule management with source/destination filtering

### Modules
- `firewall_rule` - Unified firewall rule management
  - Auto-detect firewall backend
  - Support for port ranges
  - Source and destination IP filtering
  - Priority-based rule ordering
  - Multiple action types (accept, drop, reject)

### Filters
- `validate_port` - Validate port numbers and ranges
- `validate_cidr` - Validate CIDR notation
- `normalize_port_range` - Normalize port range format
- `port_to_service` - Convert port to service name
- `service_to_port` - Convert service name to port
- `group_rules_by_protocol` - Group rules by protocol
- `filter_rules_by_port_range` - Filter rules by port range
- `merge_port_ranges` - Merge overlapping port ranges

### Lookup Plugins
- `firewall_ports` - Lookup service ports or names

### Testing
- Molecule test scenarios for all firewall backends
- Multi-distribution testing (CentOS 9, Ubuntu 22.04, Debian 12)
- Sanity tests across multiple Ansible versions (2.14, 2.15, 2.16, devel)
- Integration tests using ansible-test
- Unit tests for modules and plugins

### CI/CD
- Automated testing on pull requests and pushes
- Multi-platform testing matrix
- Automated releases with semantic versioning
- Ansible Galaxy publishing
- Documentation deployment to GitHub Pages

### Documentation
- Comprehensive README with examples
- Contributing guidelines
- Security policy
- Example playbooks
  - Web server configuration
  - Database server configuration
  - Multi-zone firewalld setup
  - Custom module usage examples

## [1.0.0] - 2025-01-24

### Added
- Initial release of thomasvincent.firewall collection
- Basic firewall management support
- Enterprise-grade structure and testing

[Unreleased]: https://github.com/thomasvincent/ansible-collection-firewall/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/thomasvincent/ansible-collection-firewall/releases/tag/v1.0.0
