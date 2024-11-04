# Productivity App - Backend

The backend of Productivity App is a Django Rest Framework (DRF) API designed to support a comprehensive task management application. This API manages user authentication, task creation, task commenting, and user interactions like following/unfollowing other users.

### Portfolio Project - Django REST Framework Application

The purpose of this project was to create a secure, RESTful API using Django that provides CRUD operations for tasks, user authentication, and follow/unfollow functionalities for a task management platform.

## Link to Backend Application

The live backend API is hosted on Heroku:  
[Productivity App Backend - Heroku](https://productivity-app-jorrit-49d8d1e48534.herokuapp.com)

## API Documentation

The Productivity App API provides endpoints to manage tasks, comments, user profiles, and user relationships. Below are the key endpoints:

- **Authentication Endpoints**:
  - `/api/auth/register/`: Register a new user
  - `/api/auth/login/`: User login to obtain access and refresh tokens
  - `/api/auth/logout/`: Log out and invalidate tokens
  - `/api/token/refresh/`: Refresh access token using a valid refresh token

- **Task Endpoints**:
  - `GET /api/tasks/`: Retrieve a list of tasks
  - `POST /api/tasks/`: Create a new task
  - `PUT /api/tasks/<task_id>/`: Update a specific task
  - `DELETE /api/tasks/<task_id>/`: Delete a specific task
  - **Filtering**: Users can filter tasks by category, priority, or state.

- **Comment Endpoints**:
  - `GET /api/comments/?task=<task_id>`: Retrieve comments for a specific task
  - `POST /api/comments/`: Add a comment to a task
  - `PATCH /api/comments/<comment_id>/`: Update a comment
  - `DELETE /api/comments/<comment_id>/`: Delete a comment

- **Account Endpoints**:
  - `POST /api/accounts/follow/<user_id>/`: Follow a user
  - `POST /api/accounts/unfollow/<user_id>/`: Unfollow a user
  - `GET /api/accounts/following/`: List users the current user is following

## Features

The backend offers comprehensive features to manage tasks and user interactions:

- **JWT Authentication**: User authentication is managed via JSON Web Tokens, ensuring secure access and token refresh functionality.
- **CRUD Operations for Tasks**: Users can create, read, update, and delete tasks with permissions applied to restrict modifications to task owners.
- **Account Endpoints**: Users can follow or unfollow each other to view and engage with tasks from followed users.
- **Commenting System**: Users can comment on tasks, with functionality for editing and deleting their own comments.
- **Filtering**: Users can filter tasks by priority, category, and state.
- **Secure Access Control**: Permissions ensure users can only edit and delete their own tasks and comments.

## Technologies Used

- **Programming Language**:
  - Python
- **Framework**:
  - Django
  - Django Rest Framework (DRF)
- **Database**:
  - PostgreSQL for production
  - SQLite for local development
- **Authentication**:
  - JWT (JSON Web Tokens) for secure access control
- **Deployment**:
  - Heroku for live deployment
- **Version Control**:
  - Git and GitHub for project tracking and version control

## Development & Structure

The backend is structured as a Django project with multiple Django apps that manage specific aspects of the API. Key apps include:

- **Accounts**: Handles user registration, profile management, and follow/unfollow functionality.
- **Tasks**: Manages all CRUD operations for tasks.
- **Comments**: Manages CRUD operations for task comments.

The application follows Django Rest Framework (DRF) architecture, with serializers ensuring data validation and JSON formatting for easy frontend consumption.

## Data Models

- **User**: Custom user model linked to tasks and comments. Includes followers and following relationships for user engagement.
- **Task**: Stores task details, including title, description, priority, due date, category, and state.
- **Comment**: Each comment is linked to a task and a user, allowing users to interact on specific tasks.

## Security Features

- **Environment Variables**: Sensitive data, such as secret keys and database credentials, are securely managed with environment variables and are not committed to the codebase.
- **Token Expiration & Refresh**: Access tokens expire and are refreshed automatically, enhancing security for user sessions.
- **Session Expiration Logic**: When tokens expire and cannot be refreshed (e.g., due to an expired refresh token), the backend dispatches a `sessionExpired` event to the frontend. This informs the user that their session has expired, allowing them to re-authenticate without confusion.
- **Permissions**: DRF permissions are used to restrict access, ensuring only authenticated users can create tasks and comments, and users can only modify their own content.

## Bugs

- **No known bugs** at the time of deployment.

## Testing

### Manual Testing

Comprehensive manual testing was performed on API endpoints to verify correct functionality for all CRUD operations, authentication flows, and user interactions.

| Endpoint                      | Method | Description                                      | Status |
|-------------------------------|--------|--------------------------------------------------|--------|
| `/api/auth/register/`         | POST   | Registers a new user                             | Pass   |
| `/api/auth/login/`            | POST   | Logs in a user and returns tokens                | Pass   |
| `/api/tasks/`                 | GET    | Retrieves all tasks for the authenticated user   | Pass   |
| `/api/tasks/`                 | POST   | Creates a new task                               | Pass   |
| `/api/tasks/<task_id>/`       | PUT    | Updates a specific task                          | Pass   |
| `/api/tasks/<task_id>/`       | DELETE | Deletes a specific task                          | Pass   |
| `/api/comments/`              | POST   | Creates a new comment on a task                  | Pass   |
| `/api/accounts/follow/<user_id>/` | POST | Follow a user                                   | Pass   |
| `/api/accounts/unfollow/<user_id>/` | POST | Unfollow a user                               | Pass   |

### Validation

- **PEP8 Compliance**: All Python code was checked with PEP8 to ensure consistent formatting and adherence to style guidelines.
- **Testing Tools**: Postman was used to manually test API endpoints for expected responses and error handling.

## Deployment

This project was deployed using Heroku with PostgreSQL as the database.

### Deployment Steps

1. Clone the repository from [GitHub - Jorritvans/productivity-app](https://github.com/users/Jorritvans/projects/3).
2. Navigate to the project directory.
3. Create a new Heroku app.
4. Set up PostgreSQL as the database on Heroku.
5. Configure environment variables in Heroku, including `SECRET_KEY`, `DATABASE_URL`, and any other necessary keys.
6. Set the Heroku buildpack to Python.
7. Push the code to Heroku.
8. Run migrations to set up the database schema on Heroku.
9. (Optional) Create a superuser for admin access.
10. Your backend API should now be live on Heroku.

## Credits

- **Development**: Built by [Jorritvans](https://github.com/Jorritvans)
- **Documentation**: Code Institute resources and Django documentation for guidance.
- **Inspiration**: Code Institute's idea of creating a Productivity app helped a lot!

## Advice and Experience

Creating the backend for this productivity application required significant planning around data structures, permissions, and security. The task and comment models were designed to be scalable, and JWT was implemented for secure user authentication.
I had a lot of struggles splitting up the repositories and keeping all functionality, and this is also why the frontend has fewer commits than the backend, as I had split it when the project was already working.

## Acknowledgements

Special thanks to my mentor for providing valuable feedback throughout the development of this project.
