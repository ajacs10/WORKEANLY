# Security Policy

## Supported version

Security fixes are applied to the latest version on the `main` branch.

## Reporting a vulnerability

Do not publish credentials, connection strings, tokens, private datasets or vulnerability details in a public issue. Report the finding privately to the repository owner with a concise description, reproduction steps, impact and any suggested mitigation.

## Local security rules

- Keep database credentials only in local environment variables or `.env` files.
- Never commit `.env`, virtual environments, logs or exported data containing sensitive information.
- Use a SQL Server account with only the permissions required for the intended operation.
- Run schema changes through reviewed SQL scripts.
- Load only validated data into tables protected by primary and foreign keys.
- Rotate a secret immediately if it is exposed in Git history, an issue, a screenshot or a terminal recording.

## Dependency hygiene

GitHub Dependabot is configured to propose monthly updates for Python packages and GitHub Actions. Review and test each update through the CI workflow before merging it.
