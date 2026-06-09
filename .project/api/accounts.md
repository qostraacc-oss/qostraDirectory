# Accounts API Reference

> [!NOTE]
> No public API endpoints have been implemented for the `accounts` app yet.
> The custom `User` model is defined in `apps/accounts/models.py`.

---

## Models

### User
The custom user model used across `qostraDirectory`. It mirrors the UUID-based identity from `qostraAuth` and is populated via JWT lazy sync on every authenticated request.

| Field        | Type        | Description                                  |
| ------------ | ----------- | -------------------------------------------- |
| `id`         | UUID (PK)   | Mirrors the `user_id` claim from the JWT     |
| `username`   | CharField   | Synced from JWT `username` or `email` claim  |
| `email`      | EmailField  | Synced from JWT `email` claim                |
| `first_name` | CharField   | Synced from JWT `first_name` claim           |
| `last_name`  | CharField   | Synced from JWT `last_name` claim            |

---

## Developer Notice

When implementing views or endpoints for the `accounts` app:
1. Create view classes inside `apps/accounts/views/` as a sub-package.
2. Create serializer classes inside `apps/accounts/serializers/` as a sub-package.
3. Create `apps/accounts/urls.py` and register it in `config/urls.py`.
4. Document every URL route, HTTP method, request payload, and response format in this file immediately.
