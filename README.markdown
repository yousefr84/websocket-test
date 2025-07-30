# Django WebSocket Learning Project

This project is built for educational purposes to learn and implement **WebSocket** functionality using **Django Channels** alongside **Django REST Framework (DRF)**. The goal is to create a simple chat system where users can register, log in, and start a real-time chat session via WebSocket. Upon starting a chat, a unique group is created and stored in the database, and a welcome message like `hi <username> now is <current_time>` is sent to the user in real-time via WebSocket.

## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Project](#running-the-project)
- [API Endpoints](#api-endpoints)
  - [Register User](#register-user)
  - [Login (Obtain JWT Token)](#login-obtain-jwt-token)
  - [Refresh JWT Token](#refresh-jwt-token)
  - [Start Chat (Create WebSocket Group)](#start-chat-create-websocket-group)
- [WebSocket Usage](#websocket-usage)
- [Frontend Integration Guide](#frontend-integration-guide)
- [Testing with Postman](#testing-with-postman)
- [Contributing](#contributing)
- [License](#license)

## Features
- User registration and authentication using **Django REST Framework** and **Simple JWT** (with cookie-based token authentication for WebSocket).
- Creation of unique chat groups stored in the database.
- Real-time messaging via **WebSocket** using **Django Channels**.
- API documentation with **Swagger** (via `drf-yasg`).
- Upon starting a chat or connecting to WebSocket, users receive a real-time message: `hi <username> now is <current_time>`.
- Sending a message via WebSocket returns the current time: `now is <current_time>` or `<username> now is <current_time>`.

## Technologies Used
- **Django**: Web framework for building the backend.
- **Django REST Framework (DRF)**: For creating RESTful APIs.
- **djangorestframework-simplejwt**: For JWT-based authentication.
- **drf-yasg**: For generating Swagger API documentation.
- **Django Channels**: For WebSocket support.
- **channels-redis**: For managing WebSocket group messaging with Redis.
- **Daphne**: ASGI server for handling WebSocket connections.
- **Redis**: Backend for Channels layer.
- **Python**: Programming language (version 3.8+).

## Prerequisites
Before running the project, ensure you have the following installed:
- **Python** (3.8 or higher)
- **Redis** (for Channels layer)
- **pip** (Python package manager)
- A database (e.g., SQLite, PostgreSQL; SQLite is used by default in this project)

## Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   The `requirements.txt` file includes:
   ```
   django>=4.2.0
   djangorestframework>=3.14.0
   djangorestframework-simplejwt>=5.3.0
   drf-yasg>=1.21.7
   channels>=4.0.0
   channels-redis>=4.1.0
   daphne>=4.0.0
   redis>=4.5.0
   asgiref>=3.6.0
   ```

4. **Install Redis**:
   - On Ubuntu:
     ```bash
     sudo apt-get install redis-server
     ```
   - On macOS:
     ```bash
     brew install redis
     ```
   - On Windows: Use WSL or download Redis from [here](https://github.com/microsoftarchive/redis/releases).

5. **Set up environment variables**:
   Create a `.env` file in the project root (optional, as defaults are provided in `settings.py`):
   ```plaintext
   DJANGO_SETTINGS_MODULE=DjangoProject.settings
   ```

6. **Apply migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

## Running the Project
1. **Start Redis**:
   ```bash
   redis-server
   ```
   Verify Redis is running:
   ```bash
   redis-cli ping
   ```
   Expected output: `PONG`

2. **Run the Django server with Daphne**:
   ```bash
   daphne -b 0.0.0.0 -p 8000 DjangoProject.asgi:application
   ```

3. **Access Swagger documentation** (optional):
   Open `http://127.0.0.1:8000/swagger/` in your browser to view API documentation.

## API Endpoints
The project provides the following API endpoints for frontend integration. All endpoints (except registration) require JWT authentication.

### Register User
- **Endpoint**: `POST /api/register/`
- **Description**: Register a new user.
- **Request Body**:
  ```json
  {
      "name": "Your Name",
      "username": "unique_username",
      "password": "your_password"
  }
  ```
- **Response**:
  - **201 Created**:
    ```json
    {
        "id": 1,
        "name": "Your Name",
        "username": "unique_username"
    }
    ```
  - **400 Bad Request** (e.g., missing fields or duplicate username):
    ```json
    {
        "error": "Username already used"
    }
    ```

### Login (Obtain JWT Token)
- **Endpoint**: `POST /api/token/`
- **Description**: Authenticate a user and obtain a JWT access and refresh token. The access token is also set as a cookie named `access`.
- **Request Body**:
  ```json
  {
      "username": "unique_username",
      "password": "your_password"
  }
  ```
- **Response**:
  - **200 OK**:
    ```json
    {
        "access": "your-jwt-access-token",
        "refresh": "your-jwt-refresh-token"
    }
    ```
    - Cookie: `access=your-jwt-access-token`
  - **401 Unauthorized** (invalid credentials):
    ```json
    {
        "detail": "No active account found with the given credentials"
    }
    ```

### Refresh JWT Token
- **Endpoint**: `POST /api/token/refresh/`
- **Description**: Refresh an expired JWT access token using the refresh token.
- **Request Body**:
  ```json
  {
      "refresh": "your-jwt-refresh-token"
  }
  ```
- **Response**:
  - **200 OK**:
    ```json
    {
        "access": "new-jwt-access-token"
    }
    ```
  - **401 Unauthorized** (invalid refresh token):
    ```json
    {
        "detail": "Token is invalid or expired"
    }
    ```

### Start Chat (Create WebSocket Group)
- **Endpoint**: `POST /api/start-chat/`
- **Description**: Create a new chat group, store it in the database, and return a WebSocket URL for real-time messaging.
- **Headers**:
  ```
  Authorization: Bearer your-jwt-access-token
  ```
- **Request Body**: Empty
- **Response**:
  - **200 OK**:
    ```json
    {
        "group_name": "chat_a1b2c3d4",
        "websocket_url": "ws://127.0.0.1:8000/ws/chat/chat_a1b2c3d4/",
        "message": "سلام username الان ساعت 09:26:00 است"
    }
    ```
  - **401 Unauthorized** (invalid or missing token):
    ```json
    {
        "detail": "Authentication credentials were not provided"
    }
    ```

## WebSocket Usage
The WebSocket endpoint is used for real-time messaging. After calling the `/api/start-chat/` endpoint, connect to the provided `websocket_url` to receive real-time messages.

- **URL**: `ws://127.0.0.1:8000/ws/chat/<group_name>/`
  - `<group_name>`: Obtained from the `/api/start-chat/` response (e.g., `chat_a1b2c3d4`).
  - The WebSocket connection requires the JWT access token to be sent as a cookie named `access` (set during login via `/api/token/`).
- **Headers**:
  ```
  Cookie: access=your-jwt-access-token
  ```
- **Message Received** (upon connection):
  ```json
  {
      "type": "chat_message",
      "message": "hi username now is 09:26:00"
  }
  ```
- **Sending a Message**:
  - Send any JSON message (e.g., `{"message": "test"}`) to the WebSocket.
  - **Response** (for any message sent):
    ```json
    {
        "type": "chat_message",
        "message": "now is 09:26:00"
    }
    ```
  - **Group Message Handling**:
    If a message is sent to the group (via `channel_layer.group_send`), the response will be:
    ```json
    {
        "type": "chat_message",
        "message": "username now is 09:26:00"
    }
    ```

## Frontend Integration Guide
For frontend developers integrating with this backend:

1. **Register a User**:
   - Send a `POST` request to `/api/register/` with user details (name, username, password).
   - Store the returned username for login.

2. **Login to Get JWT Token**:
   - Send a `POST` request to `/api/token/` with username and password.
   - The response includes `access` and `refresh` tokens. The `access` token is also set as a cookie named `access`.
   - Store both tokens for subsequent requests and ensure the `access` cookie is included in WebSocket requests.

3. **Start a Chat**:
   - Send a `POST` request to `/api/start-chat/` with the `Authorization: Bearer <access-token>` header.
   - Extract `group_name` and `websocket_url` from the response.
   - The response includes a `message` (e.g., `سلام username الان ساعت 09:26:00 است`) that can be displayed if needed.

4. **Connect to WebSocket**:
   - Connect to the `websocket_url` provided by `/api/start-chat/` (e.g., `ws://127.0.0.1:8000/ws/chat/chat_a1b2c3d4/`).
   - Ensure the `access` cookie (containing the JWT access token) is included in the WebSocket request. Most WebSocket clients (e.g., browsers) automatically send cookies for the same domain.
   - Upon connection, expect a welcome message: `hi <username> now is <current_time>`.
   - If you send a message to the WebSocket, expect a response with the current time (`now is <current_time>`) or a group message (`<username> now is <current_time>`).

5. **Handle Token Expiry**:
   - If the access token expires (401 Unauthorized), use the refresh token to get a new access token via `/api/token/refresh/`.
   - Update the `access` cookie with the new token for subsequent WebSocket connections.

## Testing with Postman
To test the APIs and WebSocket:

1. **Register a User**:
   - Send a `POST` request to `http://127.0.0.1:8000/api/register/` with the required body (see [Register User](#register-user)).
   - Copy the `username` from the response.

2. **Obtain JWT Token**:
   - Send a `POST` request to `http://127.0.0.1:8000/api/token/` with username and password.
   - Copy the `access` token and note that the `access` cookie is set in the response.

3. **Start Chat**:
   - Send a `POST` request to `http://127.0.0.1:8000/api/start-chat/` with header:
     ```
     Authorization: Bearer your-jwt-access-token
     ```
   - Copy the `group_name` and `websocket_url` from the response.

4. **Test WebSocket**:
   - Create a WebSocket request in Postman.
   - Use the `websocket_url` (e.g., `ws://127.0.0.1:8000/ws/chat/chat_a1b2c3d4/`).
   - Add the `Cookie` header:
     ```
     Cookie: access=your-jwt-access-token
     ```
   - Alternatively, if you used Postman for the `/api/token/` request, the `access` cookie is automatically included if cookies are enabled.
   - Connect and verify the welcome message: `hi <username> now is 09:26:00`.
   - Send a test message (e.g., `{"message": "test"}`) and verify the response: `now is 09:26:00`.

## Contributing
Contributions are welcome! If you want to contribute:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Make your changes and commit (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Create a Pull Request.

## License
This project is licensed under the MIT License.