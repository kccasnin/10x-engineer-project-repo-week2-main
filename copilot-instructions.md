# Project Coding Guidelines and Standards

This document outlines the coding standards and conventions for the PromptLab project to ensure consistency and maintainability across the codebase. 

## 1. Coding Standards
- **Language Version:** Ensure that code is written in Python 3.7 or higher.
- **Formatting:** 
  - Use 4 spaces for indentation (no tabs).
  - Follow PEP 8 style guidelines for Python code formatting, including line length (maximum 79 characters).
  - Use `ruff` or `black` for formatting and `isort` for import sorting.
- Type Hinting: Enforce strict type hinting. Every function argument and return type must be explicitly annotated. Use `Any` only as a last resort.
- Async Usage: Use `async def` for route handlers that perform I/O-bound operations (e.g., database queries, HTTP requests). Use standard `def` only for CPU-bound tasks or non-async library code.

## 2. Preferred Patterns and Conventions
- **Function and Variable Naming:**
  - Use `snake_case` for function and variable names.
  - Use `CamelCase` for class names, adhering to PEP 8.
- **Constants:** Define constants in `UPPER_SNAKE_CASE`.
- **Docstrings:** All functions, classes, and methods must have Google-style docstrings that clearly describe their purpose, parameters, return types, and exceptions.
- **Dependency Injection:** Utilize FastAPI's `Depends()` natively for database sessions, security authentication, and configuration injection. Avoid global instances.
- **Pydantic Schemas:** Separate request/response data shapes from database models. Use Pydantic v2 schemas for payload validation, serialization, and input sanitation.
- **Router Splitting:** Keep `main.py` clean. Break the application down into isolated domain modules using `fastapi.APIRouter`, grouped into logical routers with proper prefixes and tags.
- **Response Models:** Always define `response_model` or type-annotate the return signature in route decorators to guarantee data filtering and automatic OpenAPI documentation generation.
- **Config Management:** Use `pydantic-settings` (BaseSettings) to manage environment variables and application configurations safely.

## 3. File Naming Conventions
- **Directory Structure:** 
  - Use lowercase for directory names (e.g., `app`, `tests`, `utils`).
- **File Names:** 
  - Use `snake_case` for filenames that contain Python code (e.g., `main.py`, `api.py`, `models.py`).
  - Test files should be prefixed with `test_` (e.g., `test_api.py`, `test_storage.py`).
  - Use `PascalCase` strictly for class names (e.g., Pydantic models, SQLAlchemy models, Exception classes).
- Routes & Controllers: Name route files by domain suffixed with routes or router (e.g., `user_routes.py` or `auth.py` within a routers folder).
- Schemas & Models: Name data contracts clearly to distinguish their responsibility (e.g., `user_model.py` for database entities and `user_schema.py` for Pydantic input/output forms).
- Configuration: Store app settings inside a file named `config.py` or `settings.py`.  

## 4. Error Handling Approach
- Use exceptions to handle errors. All API endpoints should raise appropriate HTTP exceptions using FastAPI's `HTTPException`.
- Validate input parameters and data, raising `HTTPException` with a 400 status code for bad requests.
- Implement proper logging for exceptions to facilitate debugging and tracing issues.
- Global Exception Handlers: Do not manually return error response dicts from endpoints. Raise custom HTTP exceptions and let FastAPI's global exception handlers catch and format them.
- Pydantic Validation: Rely on Pydantic `ValidationError` for request body validation. Do not write manual `if not data` validation checks.
- Fail-Safe & Logging: Wrap third-party API calls, database integrations, and complex business logic in `try/except` blocks. Log unhandled or structural errors using Python's standard `logging` module (`logger.error(..., exc_info=True)`).
- Database Transactions: Ensure errors raised during database operations trigger a rollback (prefer using context managers or dependencies like `yield db`).


## 5. Testing Requirements
- Use `pytest` as the testing framework for this project and `pytest-asyncio` for asynchronous test support..
- Write unit tests for every function in the `app` directory.
- Ensure all tests are placed in the `tests` directory, following the pattern `test_<module_name>.py`.
- Aim for a minimum of 80% test coverage for the codebase using `pytest-cov`.
- Use fixtures in `conftest.py` to manage setup and teardown of test environments.
- API Testing: Use FastAPI's built-in `TestClient` (for synchronous routes) or `httpx.AsyncClient` (for `async def` routes) to write integration and end-to-end tests.
- Dependency Overrides: Use `app.dependency_overrides` to mock database sessions, authentication helpers, or external service dependencies during testing. Clean up overrides after each test.
- Database Isolation: Use a separate test database or a transactional rollback strategy (e.g., a scoped pytest fixture) so tests do not leak state or mutate production data.
- Pattern Structure: Write tests using the AAA (Arrange-Act-Assert) pattern, ensuring clean assertions using standard `assert` statements.


## Conclusion
Following these guidelines will help maintain high code quality and collaboration within the PromptLab project. For any questions or clarifications, please refer to the designated leads.
