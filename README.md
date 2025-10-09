# Flask Blacklist API

This project is a minimal Flask 1.1.x API for managing email blacklists using SQLAlchemy, Flask-RESTful, and Marshmallow. It includes a Dockerfile and docker-compose for running with PostgreSQL.

## Requirements
- Docker + Docker Compose

## Quick start

1. Copy `.env.example` to `.env` and change values if needed.
2. Start services:

```powershell
docker-compose up --build
```

3. The database tables will be created automatically on startup.

## API Endpoints

All endpoints require Bearer token authentication using the header:
```
Authorization: Bearer secret-token
```

### Blacklist Endpoints
- **POST /blacklists** - Add an email to the blacklist
  - Body: `{ "email": "user@example.com", "app_uuid": "app-123", "blocked_reason": "spam" }`
  - Response: `{ "msg": "Email added to blacklist" }` (201)

- **GET /blacklists/<email>** - Check if an email is blacklisted
  - Response: `{ "blocked": true, "reason": "spam" }` or `{ "blocked": false, "reason": null }` (200)

## Configuration

The static bearer token can be configured via environment variable:
- `STATIC_BEARER_TOKEN`: Default is "secret-token"

## Testing

Use the included `postman_collection.json` for testing. It includes:
- Comprehensive test cases for both endpoints
- Tests for authentication (valid token, no token, invalid token)
- Tests for validation (missing email)
- Automated test scripts for each request

