# CLAUDE.md

Ansible collection for enterprise host firewall management.

## Stack
- Ansible 2.9+
- Primary: nftables, Legacy: iptables, Optional: firewalld wrapper
- Molecule for testing

## Lint & Test
```bash
ansible-lint
yamllint .
molecule test
```

## Notes
- Atomic apply with automatic rollback on failure
- SSH lockout guard prevents accidental loss of access
- Compliance mappings: CIS Linux, NIST SP 800-53, PCI DSS 4.0, SOC 2
- Roles: policy, nftables
