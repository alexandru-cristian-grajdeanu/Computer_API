# Computer_API

## Short description

This project is a FastAPI-based web application that exposes a set of mathematical operations as RESTful endpoints, including Fibonacci, Factorial, Power operations, and user authentication & registration.

## Components

### Math components
 - Pow component
 - N-fibonacci component
 - N-factorial component
### Authentification component
- Register component
- Login component
-- The login endpoint provides token-based authentication for users using email and password credentials. 
-- The login functionality leverages FastAPI’s dependency injection system by using Depends to inject a database Session provided by the get_session function. It then queries the database using SQLModel to locate a user with the given email address. Upon retrieving the user, the submitted password is verified against the stored hashed password using the verify_password() function. If authentication is successful, the create_access_token() function generates a JWT access token that is returned to the client. Throughout the process, login attempts and their outcomes are logged via the logger module. The endpoint returns a JSONResponse with structured messages and appropriate HTTP status codes to indicate either success or failure.
- 
