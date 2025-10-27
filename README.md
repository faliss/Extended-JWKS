# JWKS Server – Project 2

This project extends a basic JWKS authentication server by storing RSA private keys in a SQLite database and serving public keys via a JWKS endpoint.  
It supports issuing JWTs for fake users, handling expired keys, and Basic Auth.

---

## Project Features

- SQLite-backed storage for private RSA keys (`totally_not_my_privateKeys.db`)
- `/auth` endpoint issues JWTs
  - Supports expired keys with `?expired=true`
  - Requires Basic Auth (`userABC:password123`)
- `/jwks.json` endpoint serves public keys (JWKS)
- Simple Python Flask server

---

## Folder Structure

