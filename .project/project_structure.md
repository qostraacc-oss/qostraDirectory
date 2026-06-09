# Project Structure

## Project Overview
**QostraDirectory** operates as the main business address book and contact management directory for the Qostra ERP platform. It registers customer client records, general contacts details, and vendor profiles. To ensure historical database consistency, it enforces soft deletion strategies and normalized phone/email formats.

This document provides a detailed overview of the QostraDirectory project directory structure and the purpose of each component.

## Root Directory
- `/apps/`: Contains custom Django applications managing business contacts, clients, and vendors.
- `/common/`: Central shared logic, authentication middleware, custom validation rules, and helpers.
- `/config/`: Project configurations, environment settings, and main URLs.
- `manage.py`: Django CLI command utility.
- `pyproject.toml` / `uv.lock`: Dependency definitions managed by `uv`.

## 1. Apps (`/apps/`)
Logic is divided into client, contact, and vendor directories.

### Accounts (`/accounts/`)
Holds the project's custom user model.
- `models.py`: Defines the custom `User` model (with UUID primary keys).
- `apps.py`: AppConfig for `apps.accounts`.

### Clients (`/clients/`)
Manages workspace-scoped client account profiles.
- `models.py`: Defines the `Client` model linked to workspace IDs and the local `User` creator.
- `views/`: Package managing client views (List, Create, Retrieve, Update, Soft-delete).
- `serializers/`: Package handling client data serialization and validation.
- `urls.py`: Client route mapping config.
- `apps.py`: AppConfig for `apps.clients`.

### Vendors (`/vendors/`)
Manages vendor organization and supplier records.
- `models.py`: Defines the `Vendor` model.
- `views/`: Package managing vendor views.
- `serializers/`: Handles vendor data validation.
- `services/`: Encapsulates vendor business services.
- `apps.py`: AppConfig for `apps.vendors`.

## 2. Common Components (`/common/`)
- `auth/`: Authentication package implementing JWT verification and lazy user syncing.
  - `core.py`: Abstract JWT verification and base sync service definitions.
  - `user_sync.py`: Directory-specific sync engine translating token claims to custom `User` instances.
  - `utils.py`: Exposes `JWTAuthentication` class for Django REST Framework.
- `validators/`: Phone number format validators, email domains checks.
- `middleware/`: Standard header validations or client/vendor token validations.

## 3. Configuration (`/config/`)
- `settings/`: Multi-environment settings structure (`base.py`, `dev.py`, `prod.py`, `test.py`).
- `urls.py`: App URL configurations.

## 4. Documentation (`/.project/`)
- `project_rules.md`: Core developer rules and UV configurations.
- `project_structure.md`: This file.
- `api/`: Folder containing Markdown API documentation files for each application.
