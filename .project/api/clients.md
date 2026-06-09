# Clients API Reference

Clients are managed on a per-workspace basis. All endpoints require a valid JWT token in the `Authorization` header.

---

## Headers & Authentication

All API requests must include the following headers:

```http
Authorization: Bearer <JWT_ACCESS_TOKEN>
Content-Type: application/json
```

---

## 1. List Clients

Retrieve a list of active clients within a specific workspace.

* **URL Route**: `/api/workspaces/<workspace_id>/clients/`
* **Method**: `GET`
* **Success Response (200 OK)**:
  ```json
  [
    {
      "id": "e9b5fbb3-11b2-4d7a-80bb-69d6614138e6",
      "workspace_id": "a3b5c6d7-e8f9-0a1b-2c3d-4e5f6a7b8c9d",
      "created_by": "88a51bc2-f94d-4a1a-bb10-ca81c15f9222",
      "created_by_username": "anfique@qostra.com",
      "name": "Acme Corp",
      "email": "info@acme.com",
      "phone": "+1234567890",
      "is_active": true,
      "created_at": "2026-06-08T10:00:00Z",
      "updated_at": "2026-06-08T10:00:00Z"
    }
  ]
  ```

---

## 2. Create Client

Create a new client under a specific workspace. The creator (`created_by`) is automatically resolved from the authenticated JWT token user.

* **URL Route**: `/api/workspaces/<workspace_id>/clients/`
* **Method**: `POST`
* **Request Payload**:
  ```json
  {
    "name": "Globex Corporation",
    "email": "contact@globex.com",
    "phone": "+1987654321"
  }
  ```
* **Success Response (201 Created)**:
  ```json
  {
    "id": "f8c9d1a2-3b4c-5d6e-7f8a-9b0c1d2e3f4a",
    "workspace_id": "a3b5c6d7-e8f9-0a1b-2c3d-4e5f6a7b8c9d",
    "created_by": "88a51bc2-f94d-4a1a-bb10-ca81c15f9222",
    "created_by_username": "anfique@qostra.com",
    "name": "Globex Corporation",
    "email": "contact@globex.com",
    "phone": "+1987654321",
    "is_active": true,
    "created_at": "2026-06-08T10:05:00Z",
    "updated_at": "2026-06-08T10:05:00Z"
  }
  ```
* **Error Response (400 Bad Request)**:
  ```json
  {
    "name": [
      "This field is required."
    ]
  }
  ```

---

## 3. Retrieve Client

Fetch details of a single active client by ID.

* **URL Route**: `/api/workspaces/<workspace_id>/clients/<client_id>/`
* **Method**: `GET`
* **Success Response (200 OK)**:
  ```json
  {
    "id": "f8c9d1a2-3b4c-5d6e-7f8a-9b0c1d2e3f4a",
    "workspace_id": "a3b5c6d7-e8f9-0a1b-2c3d-4e5f6a7b8c9d",
    "created_by": "88a51bc2-f94d-4a1a-bb10-ca81c15f9222",
    "created_by_username": "anfique@qostra.com",
    "name": "Globex Corporation",
    "email": "contact@globex.com",
    "phone": "+1987654321",
    "is_active": true,
    "created_at": "2026-06-08T10:05:00Z",
    "updated_at": "2026-06-08T10:05:00Z"
  }
  ```
* **Error Response (404 Not Found)**:
  ```json
  {
    "detail": "No Client matches the given query."
  }
  ```

---

## 4. Update Client

Modify all fields of a client (full update).

* **URL Route**: `/api/workspaces/<workspace_id>/clients/<client_id>/`
* **Method**: `PUT`
* **Request Payload**:
  ```json
  {
    "name": "Globex Corp",
    "email": "new-email@globex.com",
    "phone": "+1987654321"
  }
  ```
* **Success Response (200 OK)**:
  ```json
  {
    "id": "f8c9d1a2-3b4c-5d6e-7f8a-9b0c1d2e3f4a",
    "workspace_id": "a3b5c6d7-e8f9-0a1b-2c3d-4e5f6a7b8c9d",
    "created_by": "88a51bc2-f94d-4a1a-bb10-ca81c15f9222",
    "created_by_username": "anfique@qostra.com",
    "name": "Globex Corp",
    "email": "new-email@globex.com",
    "phone": "+1987654321",
    "is_active": true,
    "created_at": "2026-06-08T10:05:00Z",
    "updated_at": "2026-06-08T10:10:00Z"
  }
  ```

---

## 5. Partial Update Client

Modify specific fields of a client (partial update).

* **URL Route**: `/api/workspaces/<workspace_id>/clients/<client_id>/`
* **Method**: `PATCH`
* **Request Payload**:
  ```json
  {
    "name": "Globex Inc."
  }
  ```
* **Success Response (200 OK)**:
  ```json
  {
    "id": "f8c9d1a2-3b4c-5d6e-7f8a-9b0c1d2e3f4a",
    "workspace_id": "a3b5c6d7-e8f9-0a1b-2c3d-4e5f6a7b8c9d",
    "created_by": "88a51bc2-f94d-4a1a-bb10-ca81c15f9222",
    "created_by_username": "anfique@qostra.com",
    "name": "Globex Inc.",
    "email": "new-email@globex.com",
    "phone": "+1987654321",
    "is_active": true,
    "created_at": "2026-06-08T10:05:00Z",
    "updated_at": "2026-06-08T10:12:00Z"
  }
  ```

---

## 6. Delete Client (Soft Delete)

Soft-deletes the client by setting `is_active = false`. Soft-deleted clients are excluded from standard list and retrieve lookups.

* **URL Route**: `/api/workspaces/<workspace_id>/clients/<client_id>/`
* **Method**: `DELETE`
* **Success Response (204 No Content)**:
  *(No response body content)*
