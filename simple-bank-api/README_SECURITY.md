# Authentication and security setup

1. Copy `.env.example` to `.env` and set `MONGO_URI`, `JWT_SECRET_KEY`, and `ADMIN_SETUP_KEY`. Use separate random secrets; keep `.env` out of version control. `JWT_SECRET_KEY` must be at least 32 characters.
2. Install dependencies in a virtual environment with `pip install -r requirements.txt`.
3. Run `python app.py`; Swagger is at `http://127.0.0.1:5000/docs`.
4. From the React app, use `/admin/setup` once to configure the first admin with the setup key. The server records setup completion in MongoDB and rejects subsequent setup attempts. Remove or rotate `ADMIN_SETUP_KEY` after setup.
5. Customers register at `/register`, then sign in at `/login`. Tokens expire after `JWT_EXPIRE_MINUTES` (default 60). Passwords are stored as Argon2id hashes through `argon2-cffi`; raw passwords are never persisted.

The API enforces authorization server-side. React route guards are only a user-experience feature and are not a security boundary. Customer account access is checked against the authenticated subject on every account-specific operation.
