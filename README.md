# Computer_API

## Short description

This project is a FastAPI-based web application that exposes a set of mathematical operations as RESTful endpoints, including Fibonacci, Factorial, Power operations, and user authentication & registration.

## Components

### Math components
#### Pow component

The /pow endpoint computes the result of raising a base number to a given exponent while enforcing limits on input size to ensure performance and numerical stability. It also supports caching, JWT-based authorization, and persistent operation logging.

The Power endpoint leverages FastAPI's Depends system to inject both the database session and JWT authentication token data, ensuring authorized access to the route. Input is validated through the PowRequest schema, which accepts a base and an exponent. The actual computation is handled by the compute_pow() function, which uses lru_cache to improve performance for repeated inputs. This function includes several mathematical safeguards: it rejects operations where 0 is raised to 0 or a negative exponent, disallows fractional exponents for negative bases (to avoid complex numbers), and raises a PowTooLargeError if the base or exponent exceeds safe computational thresholds. Additionally, any overflow during computation is also caught and handled gracefully. If the computed result exceeds 10^200, it is returned as a string to preserve precision. Each request is logged using a custom logger for auditing and traceability. Finally, the operation and its result are saved in the database via save_operation(), and the endpoint returns a structured response or appropriate error message based on the outcome.

#### N-fibonacci component
   
The /fibonacci endpoint computes the n-th Fibonacci number while enforcing limits on computational size to ensure performance and stability. It also supports caching, JWT-based authorization, and persistent operation logging.

The Fibonacci endpoint employs FastAPI's Depends mechanism to inject both the database session and JWT authentication data, ensuring secure and modular access control. Input validation is handled using the FibonacciRequest Pydantic schema, which ensures that the provided value for n is structurally sound before computation begins. The actual computation is delegated to the compute_fibonacci() function, which is optimized with an lru_cache to speed up repeated calculations and includes an early digit-length estimation based on logarithmic approximations using the golden ratio. If the estimated number of digits exceeds 10,000, the system raises a FibonacciTooLargeError to prevent resource exhaustion. Throughout the process, all relevant events, such as request initiation, computation outcomes, and errors, are recorded using a custom logger. Finally, the input and result of the operation are saved persistently in the database via the save_operation() utility function.

#### N-factorial component

The /factorial endpoint computes the factorial of a non-negative integer while enforcing limits on output size to ensure performance and prevent numeric overflows. It also supports caching, JWT-based authorization, and persistent operation logging.

The Factorial endpoint leverages FastAPI's Depends system to inject both the database session and JWT authentication token data, ensuring authorized access to the route. Input is validated through the FactorialRequest schema, which accepts a single non-negative integer. The actual computation is handled by the compute_factorial() function, which uses lru_cache to improve performance for repeated inputs. This function incorporates several mathematical safeguards: it raises a ValueError if the input is negative and estimates the number of digits in the result using Stirling's approximation to prevent excessively large computations. If the estimated number of digits exceeds 10,000, a FactorialTooLargeError is raised to protect against overflow and string conversion issues. For inputs above 170, the result is returned as a string to avoid floating-point precision loss. Each request is logged using a custom logger for auditing and observability. Finally, the input and result are stored in the database via save_operation(), and the endpoint returns a structured response or appropriate error message based on the outcome.

### Authentification component
#### Register component
  
The register endpoint allows new users to create an account using their email and password.

The registration endpoint uses FastAPI’s Depends to inject a database Session via get_session. It checks whether the email is already registered using SQLModel queries. If the email is unique, the password is validated for strength using a field_validator in the UserRegister model. Upon passing validation, the password is hashed using hash_password() before storing the user in the database. The process is logged at each step, and the user ID is returned in the response on successful registration.
#### Login component
  
The login endpoint provides token-based authentication for users using email and password credentials. 

The login functionality leverages FastAPI’s dependency injection system by using Depends to inject a database Session provided by the get_session function. It then queries the database using SQLModel to locate a user with the given email address. Upon retrieving the user, the submitted password is verified against the stored hashed password using the verify_password() function. If authentication is successful, the create_access_token() function generates a JWT access token that is returned to the client. Throughout the process, login attempts and their outcomes are logged via the logger module. The endpoint returns a JSONResponse with structured messages and appropriate HTTP status codes to indicate either success or failure.

## Technologies
- FastAPI
- SQLite
- SQLModel
- functools.lru_cache
- PyJWT
- Pydantic
- Prometheus
- bcrypt
- passlib
