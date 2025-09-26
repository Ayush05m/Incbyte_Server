# API Endpoints Reference

This document provides a detailed reference for all API endpoints, including their methods, paths, descriptions, input parameters, expected output, and authentication requirements. All successful responses are wrapped in a `standard_response` format unless otherwise specified.

## Standard Response Format

All successful API responses (unless explicitly stated otherwise) will adhere to the following JSON structure:

```json
{
  "success": true,
  "message": "A descriptive message about the operation's success",
  "data": {
    // The actual data returned by the endpoint
  },
  "error": null
}
```

Error responses will typically have:

```json
{
  "success": false,
  "message": "A descriptive message about the error",
  "data": null,
  "error": "A more specific error code or message"
}
```

---

## Authentication Endpoints (`/api/auth`)

### 1. Register User

*   **Method:** `POST`
*   **Path:** `/api/auth/register`
*   **Description:** Registers a new user in the system.
*   **Input:**
    *   **Body:** `application/json`
        ```json
        {
          "email": "string",
          "password": "string",
          "username": "string"
        }
        ```
*   **Output:**
    *   **Success (200 OK):**
        ```json
        {
          "success": true,
          "message": "User registered successfully",
          "data": {
            "id": 1,
            "email": "user@example.com",
            "username": "example_user",
            "role": "user",
            "createdAt": "2023-10-27T10:00:00.000Z"
          },
          "error": null
        }
        ```
    *   **Error (400 Bad Request):** If email is already registered.
        ```json
        {
          "success": false,
          "message": "Email already registered",
          "data": null,
          "error": "Email already registered"
        }
        ```
*   **Authentication:** None required.

### 2. Login User

*   **Method:** `POST`
*   **Path:** `/api/auth/login`
*   **Description:** Authenticates a user and returns an access token.
*   **Input:**
    *   **Body:** `application/json`
        ```json
        {
          "email": "string",
          "password": "string"
        }
        ```
*   **Output:**
    *   **Success (200 OK):**
        ```json
        {
          "success": true,
          "message": "Login successful",
          "data": {
            "access_token": "your_jwt_token_here",
            "token_type": "bearer"
          },
          "error": null
        }
        ```
    *   **Error (401 Unauthorized):** If email or password is incorrect.
        ```json
        {
          "success": false,
          "message": "Incorrect email or password",
          "data": null,
          "error": "Incorrect email or password"
        }
        ```
*   **Authentication:** None required.

---

## User Endpoints (`/api/users`)

### 1. Read All Users

*   **Method:** `GET`
*   **Path:** `/api/users/`
*   **Description:** Retrieves a list of all users.
*   **Input:**
    *   **Query Parameters:**
        *   `skip`: `integer` (default: 0) - Number of items to skip.
        *   `limit`: `integer` (default: 100) - Maximum number of items to return.
*   **Output:**
    *   **Success (200 OK):**
        ```json
        {
          "success": true,
          "message": "Users fetched successfully",
          "data": [
            {
              "id": 1,
              "email": "user1@example.com",
              "username": "user_one",
              "role": "user",
              "createdAt": "2023-10-27T10:00:00.000Z"
            }
          ],
          "error": null
        }
        ```
*   **Authentication:** Requires a valid JWT token.

### 2. Read Current User

*   **Method:** `GET`
*   **Path:** `/api/users/me`
*   **Description:** Retrieves the information of the currently authenticated user.
*   **Input:** None (User ID is extracted from the JWT token).
*   **Output:**
    *   **Success (200 OK):**
        ```json
        {
          "success": true,
          "message": "Current user fetched successfully",
          "data": {
            "id": 1,
            "email": "current@example.com",
            "username": "current_user",
            "role": "user",
            "createdAt": "2023-10-27T10:00:00.000Z"
          },
          "error": null
        }
        ```
    *   **Error (401 Unauthorized):** If the token is invalid or missing.
*   **Authentication:** Requires a valid JWT token.

### 3. Read User by ID

*   **Method:** `GET`
*   **Path:** `/api/users/{user_id}`
*   **Description:** Retrieves a specific user by their ID.
*   **Input:**
    *   **Path Parameter:** `user_id`: `integer` - The ID of the user to retrieve.
*   **Output:**
    *   **Success (200 OK):**
        ```json
        {
          "success": true,
          "message": "User fetched successfully",
          "data": {
            "id": 1,
            "email": "user@example.com",
            "username": "example_user",
            "role": "user",
            "createdAt": "2023-10-27T10:00:00.000Z"
          },
          "error": null
        }
        ```
    *   **Error (404 Not Found):** If the user is not found.
        ```json
        {
          "success": false,
          "message": "User not found",
          "data": null,
          "error": "User not found"
        }
        ```
*   **Authentication:** Requires a valid JWT token.

---

## Sweet Endpoints (`/api/sweets`)

### 1. Create Sweet

*   **Method:** `POST`
*   **Path:** `/api/sweets/`
*   **Description:** Creates a new sweet in the system.
*   **Input:**
    *   **Form Data:** `multipart/form-data`
        *   `sweet`: `application/json` (e.g., `{"name": "string", "description": "string", "price": 0.0, "category": "string", "quantity": 0}`)
        *   `image_file`: `file` (Optional) - An image file for the sweet.
*   **Output:**
    *   **Success (200 OK):**
        ```json
        {
          "success": true,
          "message": "Sweet created successfully",
          "data": {
            "id": 1,
            "name": "Chocolate Bar",
            "description": "Delicious chocolate",
            "price": 2.50,
            "category": "Chocolate",
            "quantity": 100,
            "imageUrl": "http://example.com/image.jpg"
          },
          "error": null
        }
        ```
    *   **Error (400 Bad Request):** If sweet name is already registered.
        ```json
        {
          "success": false,
          "message": "Sweet name already registered",
          "data": null,
          "error": "Sweet name already registered"
        }
        ```
*   **Authentication:** Requires a valid JWT token.

### 2. Read All Sweets

*   **Method:** `GET`
*   **Path:** `/api/sweets/`
*   **Description:** Retrieves a list of all sweets.
*   **Input:**
    *   **Query Parameters:**
        *   `skip`: `integer` (default: 0) - Number of items to skip.
        *   `limit`: `integer` (default: 100) - Maximum number of items to return.
*   **Output:**
    *   **Success (200 OK):**
        ```json
        {
          "success": true,
          "message": "Sweets fetched successfully",
          "data": [
            {
              "id": 1,
              "name": "Chocolate Bar",
              "description": "Delicious chocolate",
              "price": 2.50,
              "category": "Chocolate",
              "quantity": 100,
              "imageUrl": "http://example.com/image.jpg"
            }
          ],
          "error": null
        }
        ```
*   **Authentication:** Requires a valid JWT token.

### 3. Search Sweets

*   **Method:** `GET`
*   **Path:** `/api/sweets/search`
*   **Description:** Searches for sweets based on various criteria.
*   **Input:**
    *   **Query Parameters:**
        *   `name`: `string` (Optional) - Search by sweet name.
        *   `category`: `string` (Optional) - Search by sweet category.
        *   `min_price`: `number` (Optional) - Minimum price.
        *   `max_price`: `number` (Optional) - Maximum price.
*   **Output:**
    *   **Success (200 OK):**
        ```json
        {
          "success": true,
          "message": "Sweets search successful",
          "data": [
            {
              "id": 1,
              "name": "Chocolate Bar",
              "description": "Delicious chocolate",
              "price": 2.50,
              "category": "Chocolate",
              "quantity": 100,
              "imageUrl": "http://example.com/image.jpg"
            }
          ],
          "error": null
        }
        ```
*   **Authentication:** Requires a valid JWT token.

### 4. Update Sweet

*   **Method:** `PUT`
*   **Path:** `/api/sweets/{sweet_id}`
*   **Description:** Updates an existing sweet by ID.
*   **Input:**
    *   **Path Parameter:** `sweet_id`: `integer` - The ID of the sweet to update.
    *   **Body:** `application/json`
        ```json
        {
          "name": "string (optional)",
          "description": "string (optional)",
          "price": "number (optional)",
          "category": "string (optional)",
          "quantity": "integer (optional)"
        }
        ```
*   **Output:**
    *   **Success (200 OK):**
        ```json
        {
          "success": true,
          "message": "Sweet updated successfully",
          "data": {
            "id": 1,
            "name": "Updated Chocolate Bar",
            "description": "Even more delicious chocolate",
            "price": 3.00,
            "category": "Chocolate",
            "quantity": 90,
            "imageUrl": "http://example.com/updated_image.jpg"
          },
          "error": null
        }
        ```
    *   **Error (404 Not Found):** If the sweet is not found.
        ```json
        {
          "success": false,
          "message": "Sweet not found",
          "data": null,
          "error": "Sweet not found"
        }
        ```
*   **Authentication:** Requires a valid JWT token with `admin` role.

### 5. Delete Sweet

*   **Method:** `DELETE`
*   **Path:** `/api/sweets/{sweet_id}`
*   **Description:** Deletes a sweet by ID.
*   **Input:**
    *   **Path Parameter:** `sweet_id`: `integer` - The ID of the sweet to delete.
*   **Output:**
    *   **Success (200 OK):** Returns the deleted sweet object directly (not wrapped in `standard_response`).
        ```json
        {
          "id": 1,
          "name": "Chocolate Bar",
          "description": "Delicious chocolate",
          "price": 2.50,
          "category": "Chocolate",
          "quantity": 100,
          "imageUrl": "http://example.com/image.jpg"
        }
        ```
    *   **Error (404 Not Found):** If the sweet is not found.
        ```json
        {
          "detail": "Sweet not found"
        }
        ```
*   **Authentication:** Requires a valid JWT token with `admin` role.

### 6. Purchase Sweet

*   **Method:** `POST`
*   **Path:** `/api/sweets/{sweet_id}/purchase`
*   **Description:** Initiates a purchase for a sweet, creating a Razorpay order.
*   **Input:**
    *   **Path Parameter:** `sweet_id`: `integer` - The ID of the sweet to purchase.
    *   **Body:** `application/json`
        ```json
        {
          "quantity": "integer"
        }
        ```
*   **Output:**
    *   **Success (200 OK):**
        ```json
        {
          "success": true,
          "message": "Razorpay order created",
          "data": {
            "order_id": "order_xxxxxxxxxxxxxx",
            "amount": 100.00,
            "currency": "INR"
          },
          "error": null
        }
        ```
    *   **Error (404 Not Found):** If the sweet is not found.
    *   **Error (400 Bad Request):** If not enough stock or missing Razorpay details.
    *   **Error (500 Internal Server Error):** If failed to create Razorpay order.
*   **Authentication:** Requires a valid JWT token.

### 7. Verify Payment

*   **Method:** `POST`
*   **Path:** `/api/sweets/{sweet_id}/verify_payment`
*   **Description:** Verifies a Razorpay payment for a sweet purchase.
*   **Input:**
    *   **Path Parameter:** `sweet_id`: `integer` - The ID of the sweet for which payment is being verified.
    *   **Body:** `application/json` (Razorpay webhook payload)
        ```json
        {
          "razorpay_order_id": "string",
          "razorpay_payment_id": "string",
          "razorpay_signature": "string"
        }
        ```
*   **Output:**
    *   **Success (200 OK):**
        ```json
        {
          "success": true,
          "message": "Payment successful",
          "data": {
            "payment_id": "pay_xxxxxxxxxxxxxx"
          },
          "error": null
        }
        ```
    *   **Error (400 Bad Request):** If missing Razorpay payment details or payment verification failed.
    *   **Error (404 Not Found):** If the sweet is not found.
*   **Authentication:** Requires a valid JWT token.

### 8. Restock Sweet

*   **Method:** `POST`
*   **Path:** `/api/sweets/{sweet_id}/restock`
*   **Description:** Restocks the quantity of a sweet.
*   **Input:**
    *   **Path Parameter:** `sweet_id`: `integer` - The ID of the sweet to restock.
    *   **Body:** `application/json`
        ```json
        {
          "quantity": "integer"
        }
        ```
*   **Output:**
    *   **Success (200 OK):** Returns the updated sweet object directly (not wrapped in `standard_response`).
        ```json
        {
          "id": 1,
          "name": "Chocolate Bar",
          "description": "Delicious chocolate",
          "price": 2.50,
          "category": "Chocolate",
          "quantity": 150,
          "imageUrl": "http://example.com/image.jpg"
        }
        ```
    *   **Error (404 Not Found):** If the sweet is not found.
*   **Authentication:** Requires a valid JWT token with `admin` role.

---

## Purchase Endpoints (`/api/purchases`)

### 1. Create Purchase

*   **Method:** `POST`
*   **Path:** `/api/purchases/`
*   **Description:** Creates a new purchase record.
*   **Input:**
    *   **Body:** `application/json`
        ```json
        {
          "sweet_id": "integer",
          "quantity": "integer",
          "razorpay_order_id": "string (optional)"
        }
        ```
    *   **Query Parameter:** `user_id`: `integer` - The ID of the user making the purchase.
*   **Output:**
    *   **Success (200 OK):**
        ```json
        {
          "success": true,
          "message": "Purchase created successfully",
          "data": {
            "id": 1,
            "sweet_id": 101,
            "user_id": 1,
            "quantity": 2,
            "purchased_at": "2023-10-27T10:30:00.000Z",
            "razorpay_order_id": "order_xyz123"
          },
          "error": null
        }
        ```
*   **Authentication:** Requires a valid JWT token.

### 2. Read All Purchases

*   **Method:** `GET`
*   **Path:** `/api/purchases/`
*   **Description:** Retrieves a list of all purchases.
*   **Input:**
    *   **Query Parameters:**
        *   `skip`: `integer` (default: 0) - Number of items to skip.
        *   `limit`: `integer` (default: 100) - Maximum number of items to return.
*   **Output:**
    *   **Success (200 OK):**
        ```json
        {
          "success": true,
          "message": "Purchases fetched successfully",
          "data": [
            {
              "id": 1,
              "sweet_id": 101,
              "user_id": 1,
              "quantity": 2,
              "purchased_at": "2023-10-27T10:30:00.000Z",
              "razorpay_order_id": "order_xyz123"
            }
          ],
          "error": null
        }
        ```
*   **Authentication:** Requires a valid JWT token.