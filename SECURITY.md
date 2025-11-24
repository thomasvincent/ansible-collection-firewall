# Security Policy

## Supported Versions

We support the following versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

### Where to Report

Send security vulnerability reports to: **thomas.vincent@gmail.com**

### What to Include

Please include as much information as possible:

1. **Description**: Clear description of the vulnerability
2. **Impact**: Potential impact and severity
3. **Steps to Reproduce**: Detailed steps to reproduce the issue
4. **Affected Versions**: Which versions are affected
5. **Proof of Concept**: If available (code, screenshots, etc.)
6. **Suggested Fix**: If you have recommendations

### Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Fix Target**: Critical issues within 30 days

### Security Update Process

1. **Acknowledgment**: We acknowledge receipt of your report
2. **Investigation**: We investigate and validate the issue
3. **Development**: We develop and test a fix
4. **Disclosure**: We coordinate disclosure with you
5. **Release**: We release a security update
6. **Advisory**: We publish a security advisory

## Security Best Practices

### When Using This Collection

1. **Principle of Least Privilege**
   - Only open necessary ports
   - Use source IP restrictions when possible
   - Implement defense in depth

2. **Regular Updates**
   - Keep collection updated to latest version
   - Subscribe to security advisories
   - Monitor GitHub releases

3. **Configuration Security**
   ```yaml
   # Use restrictive defaults
   firewall_default_policy_input: DROP
   firewall_default_policy_forward: DROP
   firewall_default_policy_output: ACCEPT  # Or DROP for maximum security

   # Always allow SSH before enabling firewall
   firewall_allow_ssh: true

   # Use specific source IPs when possible
   firewall_rules:
     - name: Allow admin access
       port: 22
       source: 192.168.1.0/24  # Restrict to admin network
   ```

4. **Testing**
   - Test firewall rules in non-production first
   - Verify SSH access before applying to production
   - Use `--check` mode to preview changes

5. **Monitoring**
   - Monitor firewall logs for suspicious activity
   - Set up alerts for rule changes
   - Regular security audits

### Secrets Management

**Never commit sensitive data:**

```yaml
# BAD - Never do this
firewall_api_key: "secret123"

# GOOD - Use Ansible Vault
firewall_api_key: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          [encrypted content]

# GOOD - Use environment variables
firewall_api_key: "{{ lookup('env', 'FIREWALL_API_KEY') }}"
```

### Role Security

When using the firewall role:

```yaml
# Explicit is better than implicit
- role: thomasvincent.firewall.firewall
  vars:
    # Clearly define your security policy
    firewall_enabled: true
    firewall_default_policy_input: DROP

    # Document why each rule exists
    firewall_rules:
      - name: Allow HTTPS from CDN
        port: 443
        source: 192.0.2.0/24
        comment: "CDN provider IP range - ticket #123"
```

## Known Security Considerations

### Firewall Lockout Prevention

This collection includes safeguards to prevent SSH lockout:

1. **Automatic SSH Rule**: When `firewall_allow_ssh: true`, SSH is allowed before enabling firewall
2. **Verify Before Apply**: Always test in dev environment first
3. **Out-of-Band Access**: Ensure you have console/IPMI access for recovery

### Platform-Specific Issues

#### iptables
- Rules are not persistent by default without iptables-persistent
- Ensure proper rule ordering for complex configurations

#### nftables
- Syntax is different from iptables
- Test thoroughly when migrating from iptables

#### firewalld
- Zone configuration can be complex
- Understand zone precedence and interface assignments

#### UFW
- Simpler but less flexible than firewalld
- Application profiles need careful review

## Security Vulnerabilities

### Reporting History

No security vulnerabilities have been reported to date.

## Compliance

This collection helps implement:

- **PCI DSS**: Firewall configuration requirements
- **HIPAA**: Network segmentation
- **SOC 2**: Access control
- **NIST**: Network security controls

## Security Testing

We perform:

- **Static Analysis**: ansible-lint with security rules
- **Dependency Scanning**: Regular dependency audits
- **Integration Testing**: Security-focused test scenarios
- **Code Review**: All changes reviewed for security impact

## Disclosure Policy

- **Private Disclosure**: 90 days before public disclosure
- **Credit**: We credit researchers who report vulnerabilities
- **CVE Assignment**: We request CVEs for significant vulnerabilities
- **Advisory**: Published in GitHub Security Advisories

## Additional Resources

- [Ansible Security Best Practices](https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html#best-practices-for-variables-and-vaults)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks/)

## Contact

- **Security Issues**: thomas.vincent@gmail.com
- **General Issues**: [GitHub Issues](https://github.com/thomasvincent/ansible-collection-firewall/issues)
- **PGP Key**: Available on request

Thank you for helping keep our collection secure!
