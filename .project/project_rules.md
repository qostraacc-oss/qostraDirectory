# Project Rules

This document outlines the core development rules and best practices for the QostraDirectory project. All developers and AI agents MUST adhere to these rules.

> [!IMPORTANT]
> **AI AGENT DIRECTIVE**: Any AI agent interacting with this codebase MUST read both `project_rules.md` and `project_structure.md` before making any changes or analysis.

---

## 1. Core Structural Rules

- **Localized Logic**: Keep formatting helpers or local parsers inside their respective app folders (e.g. `apps/accounts/utils/`).
- **Shared Utilities**: Place globally shared validation scripts (e.g. phone number formatters, common auth) in the root `/common/` package.
- **Package Organization**: Views and serializers MUST be organized into Python sub-packages (directories with `__init__.py`), never as single large files.
- **AppConfig Naming Convention**: Every Django app MUST declare a full dotted path `name` in its `AppConfig` matching the Python import path, plus an explicit `label`. Example:
  ```python
  class ClientsConfig(AppConfig):
      default_auto_field = 'django.db.models.BigAutoField'
      name = 'apps.clients'   # Full dotted path
      label = 'clients'       # Short label for Django internals
  ```

---

## 2. Authentication & User Identity

- **JWT Authentication**: All API endpoints in this service are protected by `common.auth.JWTAuthentication`. This class decodes the Bearer token issued by `qostraAuth`, verifies it using the shared `SECRET_KEY`, and syncs the user identity into the local database automatically.
- **Decoupled Identity (Lazy Sync)**: This service does NOT connect to `qostraAuth`'s or `qostraCore`'s databases. Instead, it uses **on-demand user synchronization**:
  1. On the first request from a user, the system decodes the JWT, extracts the `user_id` (UUID), and creates a local `User` record from the token claims (`email`, `first_name`, `last_name`).
  2. On subsequent requests, the user is retrieved from a memory cache (1-hour TTL) to avoid hitting the local database repeatedly.
- **Custom User Model**: The project defines its own `User` model in `apps/accounts/models.py` with a UUID primary key that mirrors the `user_id` from `qostraAuth`. The `AUTH_USER_MODEL` setting is `accounts.User`.
- **No Cross-Database Connections**: This service must NEVER connect to another microservice's database directly.

---

## 3. Workspace Isolation & Multi-Tenancy

- **Workspace ID via URL**: The active workspace context is passed as a URL path parameter (`<uuid:workspace_id>`). All resource endpoints are nested under `/api/workspaces/<workspace_id>/`.
- **Query Filtering**: All database queries MUST filter by the active `workspace_id`. Do not return records from outside the workspace boundary.
  ```python
  # Correct
  Client.objects.filter(workspace_id=workspace_id, is_active=True)
  
  # Incorrect — may leak cross-workspace data
  Client.objects.all()
  ```
- **workspace_id Storage**: The `workspace_id` is stored as a plain `UUIDField` (not a ForeignKey). This is intentional — we do not join to `qostraCore`'s database.
- **Creator Tracking**: All resource models MUST include a `created_by` ForeignKey to `settings.AUTH_USER_MODEL` to track which synced local user created the record.

---

## 4. Data Integrity & Soft Deletion

- **Soft Deletion Required**: Do NOT hard-delete client, vendor, or contact records. These records are referenced by other services (projects, CRM, ERP). Use soft deletion:
  ```python
  instance.is_active = False
  instance.save()
  ```
- **Default Active Filter**: All list and retrieve views MUST filter by `is_active=True` by default. Soft-deleted records should never appear in standard API responses.
- **Uniqueness Checks**: Prevent creation of duplicate client or vendor records. Implement proper validation on uniqueness constraints (e.g. email per workspace).
- **Standardized Formats**: Phone numbers and email addresses MUST be validated using standard formats before persistence.

---

## 5. Code Quality and Maintenance

- **Consistency**: Follow existing serializer schemas and view patterns. Refer to `apps/clients/` as the canonical reference pattern.
- **No Leftovers**: Delete redundant files, unused imports, and leftover debug blocks during every refactoring task.
- **Documentation Synchronicity**: Whenever a route, model, serializer, or view is added, modified, or deleted:
  1. Update the corresponding API doc inside `.project/api/` immediately.
  2. Update `project_rules.md` and `project_structure.md` if any structural shift occurred.

---

## 6. Dependency Management & Commands

Always use `uv` for package management. Never run raw `pip` commands.

| Task                          | Command                                      |
| ----------------------------- | -------------------------------------------- |
| Sync environment dependencies | `uv sync`                                    |
| Add a dependency              | `uv add <package>`                           |
| Remove a dependency           | `uv remove <package>`                        |
| Run Django management command | `uv run python manage.py <command>`          |
| Run tests                     | `uv run pytest`                              |
| System integrity check        | `uv run python manage.py check`              |
| Pre-production deploy check   | `uv run python manage.py check --deploy`     |

---

## 7. Code Quality, Linting & Testing Guidelines
- **Linting & Formatting (Ruff)**:
  - All Python code MUST be formatted and linted using `ruff`. Run `uv run ruff format` and `uv run ruff check` before committing.
- **Type Checking (MyPy)**:
  - Keep types clean and run type checks with `uv run mypy .` (configured with `django-stubs`).
- **Testing (PyTest)**:
  - All test suites MUST use `pytest` and `pytest-django`. Run tests with `uv run pytest`.
  - Use `factory-boy` and `faker` for generating mock database records in tests. Never hardcode static fixtures for dynamic test data.
- **Error Tracking & Rate Limiting**:
  - Production deployments MUST have `sentry-sdk` initialized in production settings.
  - Apply `django-ratelimit` decorators on public or sensitive API views (e.g., login, registration endpoints) to prevent brute-force attacks.
- **Debugging (Django Debug Toolbar)**:
  - Keep `django-debug-toolbar` enabled only in `dev.py` settings and ensure it is never exposed in production.
