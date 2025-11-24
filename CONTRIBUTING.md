# Contributing to thomasvincent.firewall

Thank you for your interest in contributing to the thomasvincent.firewall Ansible collection!

## Code of Conduct

This project adheres to the [Ansible Community Code of Conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html). By participating, you are expected to uphold this code.

## Getting Started

### Prerequisites

- Python >= 3.6
- Ansible >= 2.14.0
- Docker (for Molecule tests)
- Git

### Development Environment Setup

1. **Fork and Clone**

   ```bash
   git clone https://github.com/YOUR_USERNAME/ansible-collection-firewall.git
   cd ansible-collection-firewall
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

3. **Install Pre-commit Hooks**

   ```bash
   pre-commit install
   ```

## Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

### 2. Make Changes

Follow these guidelines:

- Write clear, descriptive commit messages
- Follow Ansible best practices
- Add tests for new features
- Update documentation

### 3. Run Tests Locally

```bash
# Lint checks
ansible-lint
yamllint .

# Molecule tests
cd roles/firewall
molecule test

# Run specific test
molecule test -s default
```

### 4. Commit Changes

Use conventional commit format:

```bash
git commit -m "feat: add support for custom chains"
git commit -m "fix: correct port validation logic"
git commit -m "docs: update README with examples"
```

Commit types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Test updates
- `refactor`: Code refactoring
- `style`: Code style changes
- `chore`: Maintenance tasks

### 5. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## Contribution Guidelines

### Code Style

- Follow [Ansible style guide](https://docs.ansible.com/ansible/latest/dev_guide/style_guide/index.html)
- Use 2 spaces for indentation
- Maximum line length: 160 characters
- Use meaningful variable names
- Add comments for complex logic

### Documentation

- Update README.md for user-facing changes
- Add/update module documentation in DOCUMENTATION section
- Include examples in EXAMPLES section
- Update CHANGELOG.md

### Testing

All contributions must include appropriate tests:

#### For Roles

- Add tasks to `molecule/default/converge.yml`
- Add verification in `molecule/default/verify.yml`
- Test across multiple distributions

#### For Modules

- Add unit tests in `tests/unit/plugins/modules/`
- Add integration tests in `tests/integration/targets/`
- Test error handling and edge cases

#### For Filters/Plugins

- Add unit tests in `tests/unit/plugins/filter_plugins/` or appropriate directory
- Test with various input types
- Test error conditions

### Pull Request Process

1. **Update Documentation**: Ensure all docs are updated
2. **Add Tests**: Include appropriate tests
3. **Pass CI**: Ensure all CI checks pass
4. **Request Review**: Tag maintainers for review
5. **Address Feedback**: Respond to review comments
6. **Squash Commits**: Clean up commit history before merge

## Testing

### Local Testing

```bash
# Full test suite
molecule test

# Specific distribution
MOLECULE_DISTRO=ubuntu2204 molecule test

# Specific scenario
molecule test -s custom-scenario
```

### CI Testing

All PRs automatically run:
- Sanity tests (multiple Ansible versions)
- Lint checks (ansible-lint, yamllint)
- Molecule tests (multiple distributions)
- Integration tests
- Unit tests

## Reporting Issues

### Bug Reports

Include:
- Ansible version
- Collection version
- Operating system and version
- Firewall backend
- Steps to reproduce
- Expected vs actual behavior
- Error messages/logs

### Feature Requests

Include:
- Use case description
- Proposed solution
- Alternative approaches considered
- Potential impacts

## Module Development

### Module Structure

```python
#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) YEAR, YOUR NAME <your@email.com>
# GNU General Public License v3.0+

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: module_name
short_description: Brief description
version_added: "1.0.0"
description:
    - Detailed description
options:
    name:
        description: Parameter description
        required: true
        type: str
author:
    - Your Name (@github_handle)
'''

EXAMPLES = r'''
- name: Example usage
  thomasvincent.firewall.module_name:
    name: example
'''

RETURN = r'''
changed:
    description: Whether changes were made
    type: bool
    returned: always
'''

from ansible.module_utils.basic import AnsibleModule

def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type='str', required=True),
        ),
        supports_check_mode=True,
    )

    # Module logic here

    module.exit_json(changed=False)

if __name__ == '__main__':
    main()
```

### Filter Plugin Structure

```python
#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function
__metaclass__ = type

def my_filter(value):
    """Filter description"""
    return modified_value

class FilterModule:
    def filters(self):
        return {
            'my_filter': my_filter,
        }
```

## Release Process

Releases are automated via GitHub Actions:

1. Create release branch: `git checkout -b release/1.1.0`
2. Update version in `galaxy.yml`
3. Update `CHANGELOG.md`
4. Create PR to main
5. After merge, create tag: `git tag v1.1.0`
6. Push tag: `git push origin v1.1.0`
7. GitHub Actions handles the rest

## Getting Help

- **GitHub Discussions**: For questions and discussions
- **GitHub Issues**: For bug reports and feature requests
- **IRC**: `#ansible` on Libera.Chat
- **Matrix**: `#ansible:ansible.com`

## Recognition

Contributors are recognized in:
- GitHub contributors page
- Release notes
- CHANGELOG.md

Thank you for contributing!
