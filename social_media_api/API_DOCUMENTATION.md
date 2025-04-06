# Social Media API Documentation

## Authentication Endpoints

### Register a New User
- **URL:** `/api/accounts/register/`
- **Method:** `POST`
- **Auth required:** No
- **Request Body:**
  ```json
  {
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword123"
  }
  ```
- **Success Response:**
  - **Code:** 201 CREATED
  - **Content:**
    ```json
    {
      "user": {
        "id": 1,
        "username": "johndoe",
        "email": "john@example.com"
      },
      "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
    }
    ```

### Login
- **URL:** `/api/accounts/login/`
- **Method:** `POST`
- **Auth required:** No
- **Request Body:**
  ```json
  {
    "username": "johndoe",
    "password": "securepassword123"
  }
  ```
- **Success Response:**
  - **Code:** 200 OK
  - **Content:**
    ```json
    {
      "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
      "user_id": 1,
      "username": "johndoe"
    }
    ```

### Get User Profile
- **URL:** `/api/accounts/profile/`
- **Method:** `GET`
- **Auth required:** Yes (Token Authentication)
- **Headers:** `Authorization: Token your-token-here`
- **Success Response:**
  - **Code:** 200 OK
  - **Content:**
    ```json
    {
      "id": 1,
      "username": "johndoe",
      "email": "john@example.com",
      "bio": "Software developer",
      "profile_picture": null
    }
    ```

### Update User Profile
- **URL:** `/api/accounts/profile/`
- **Method:** `PUT`/`PATCH`
- **Auth required:** Yes (Token Authentication)
- **Headers:** `Authorization: Token your-token-here`
- **Request Body (PATCH example):**
  ```json
  {
    "bio": "Software engineer and tech enthusiast"
  }
  ```
- **Success Response:**
  - **Code:** 200 OK
  - **Content:** Updated user profile

## Posts Endpoints

### List All Posts
- **URL:** `/api/posts/`
- **Method:** `GET`
- **Auth required:** Yes (Token Authentication)
- **Headers:** `Authorization: Token your-token-here`
- **Query Parameters:**
  - `search`: Search in title and content
  - `ordering`: Sort by fields (e.g., `-created_at`, `title`)
  - `page`: Page number for pagination
- **Success Response:**
  - **Code:** 200 OK
  - **Content:**
    ```json
    {
      "count": 15,
      "next": "http://example.com/api/posts/?page=2",
      "previous": null,
      "results": [
        {
          "id": 1,
          "title": "First Post",
          "content": "Hello world!",
          "author": {
            "id": 1,
            "username": "johndoe"
          },
          "created_at": "2023-04-01T12:00:00Z",
          "updated_at": "2023-04-01T12:00:00Z",
          "comment_count": 3
        },
        // More posts...
      ]
    }
    ```

### Get Single Post
- **URL:** `/api/posts/:id/`
- **Method:** `GET`
- **Auth required:** Yes (Token Authentication)
- **Headers:** `Authorization: Token your-token-here`
- **Success Response:**
  - **Code:** 200 OK
  - **Content:**
    ```json
    {
      "id": 1,
      "title": "First Post",
      "content": "Hello world!",
      "author": {
        "id": 1,
        "username": "johndoe"
      },
      "created_at": "2023-04-01T12:00:00Z",
      "updated_at": "2023-04-01T12:00:00Z",
      "comment_count": 3,
      "comments": [
        {
          "id": 1,
          "post": 1,
          "author": {
            "id": 2,
            "username": "janedoe"
          },
          "content": "Great post!",
          "created_at": "2023-04-01T12:30:00Z",
          "updated_at": "2023-04-01T12:30:00Z"
        },
        // More comments...
      ]
    }
    ```

### Create Post
- **URL:** `/api/posts/`
- **Method:** `POST`
- **Auth required:** Yes (Token Authentication)
- **Headers:** `Authorization: Token your-token-here`
- **Request Body:**
  ```json
  {
    "title": "New Post",
    "content": "This is my new post content."
  }
  ```
- **Success Response:**
  - **Code:** 201 CREATED
  - **Content:** Created post object

### Update Post
- **URL:** `/api/posts/:id/`
- **Method:** `PUT`/`PATCH`
- **Auth required:** Yes (Token Authentication)
- **Headers:** `Authorization: Token your-token-here`
- **Permissions:** Only the author can update their post
- **Request Body (PATCH example):**
  ```json
  {
    "title": "Updated Post Title"
  }
  ```
- **Success Response:**
  - **Code:** 200 OK
  - **Content:** Updated post object

### Delete Post
- **URL:** `/api/posts/:id/`
- **Method:** `DELETE`
- **Auth required:** Yes (Token Authentication)
- **Headers:** `Authorization: Token your-token-here`
- **Permissions:** Only the author can delete their post
- **Success Response:**
  - **Code:** 204 NO CONTENT

### Get Post Comments
- **URL:** `/api/posts/:id/comments/`
- **Method:** `GET`
- **Auth required:** Yes (Token Authentication)
- **Headers:** `Authorization: Token your-token-here`
- **Success Response:**
  - **Code:** 200 OK
  - **Content:** List of comments for the specified post

## Comments Endpoints

### List All Comments
- **URL:** `/api/comments/`
- **Method:** `GET`
- **Auth required:** Yes (Token Authentication)
- **Headers:** `Authorization: Token your-token-here`
- **Query Parameters:**
  - `post`: Filter by post ID
  - `page`: Page number for pagination
- **Success Response:**
  - **Code:** 200 OK
  - **Content:** Paginated list of comments

### Get Single Comment
- **URL:** `/api/comments/:id/`
- **Method:** `GET`
- **Auth required:** Yes (Token Authentication)
- **Headers:** `Authorization: Token your-token-here`
- **Success Response:**
  - **Code:** 200 OK
  - **Content:** Single comment object

### Create Comment
- **URL:** `/api/comments/`
- **Method:** `POST`
- **Auth required:** Yes (Token Authentication)
- **Headers:** `Authorization: Token your-token-here`
- **Request Body:**
  ```json
  {
    "post": 1,
    "content": "This is my comment."
  }
  ```
- **Success Response:**
  - **Code:** 201 CREATED
  - **Content:** Created comment object

### Update Comment
- **URL:** `/api/comments/:id/`
- **Method:** `PUT`/`PATCH`
- **Auth required:** Yes (Token Authentication)
- **Headers:** `Authorization: Token your-token-here`
- **Permissions:** Only the author can update their comment
- **Request Body (PATCH example):**
  ```json
  {
    "content": "Updated comment content."
  }
  ```
- **Success Response:**
  - **Code:** 200 OK
  - **Content:** Updated comment object

### Delete Comment
- **URL:** `/api/comments/:id/`
- **Method:** `DELETE`
- **Auth required:** Yes (Token Authentication)
- **Headers:** `Authorization: Token your-token-here`
- **Permissions:** Only the author can delete their comment
- **Success Response:**
  - **Code:** 204 NO CONTENT