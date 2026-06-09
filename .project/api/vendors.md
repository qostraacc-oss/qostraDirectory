# Vendors API Reference

> [!NOTE]
> No API endpoints have been implemented for the `vendors` app yet.
> The `Vendor` model is defined in `apps/vendors/models.py`.

---

## Models

### Vendor
*(Model definition is pending. When implementing, follow the `Client` model in `apps/clients/models.py` as the canonical reference pattern.)*

Expected fields for the `Vendor` model:

| Field              | Type        | Description                                   |
| ------------------ | ----------- | --------------------------------------------- |
| `id`               | UUID (PK)   | Unique vendor identifier                      |
| `workspace_id`     | UUID        | Workspace tenancy boundary (no FK, plain UUID)|
| `created_by`       | FK → User   | Local synced user who created this record     |
| `name`             | CharField   | Vendor / company name                         |
| `email`            | EmailField  | Primary contact email (optional)              |
| `phone`            | CharField   | Contact phone number (optional)               |
| `is_active`        | BooleanField| Soft-deletion flag — never hard-delete        |
| `created_at`       | DateTime    | Auto-set on creation                          |
| `updated_at`       | DateTime    | Auto-updated on save                          |

---

## Developer Notice

When implementing views or endpoints for the `vendors` app:
1. Define the `Vendor` model in `apps/vendors/models.py` following the `Client` model pattern.
2. Create view classes inside `apps/vendors/views/` as a sub-package.
3. Create serializer classes inside `apps/vendors/serializers/` as a sub-package.
4. Create `apps/vendors/urls.py` and register it in `config/urls.py` under:
   ```
   /api/workspaces/<workspace_id>/vendors/
   ```
5. Apply workspace-scoped filtering on ALL queries — never return records from outside the active `workspace_id`.
6. Use soft deletion (`is_active = False`) on DELETE operations — never hard-delete vendor records.
7. Document every URL route, HTTP method, request payload, and response format in this file immediately upon implementation.
