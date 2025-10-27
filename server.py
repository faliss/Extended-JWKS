from flask import Flask, jsonify, request
import sqlite3
import jwt
from datetime import datetime
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import base64

app = Flask(__name__)

DB_FILE = "totally_not_my_privateKeys.db"

# Simple fake authentication check
def check_auth(username, password):
    return username == "userABC" and password == "password123"

# Get a private key from the database
def get_private_key(expired=False):
    now = int(datetime.utcnow().timestamp())
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    if expired:
        # Get an expired key
        c.execute("SELECT kid, key, exp FROM keys WHERE exp <= ? LIMIT 1", (now,))
    else:
        # Get a valid (non-expired) key
        c.execute("SELECT kid, key, exp FROM keys WHERE exp > ? LIMIT 1", (now,))
    
    row = c.fetchone()
    conn.close()
    if not row:
        return None, None, None
    
    kid, pem, exp = row
    private_key = serialization.load_pem_private_key(pem, password=None)
    return kid, private_key, exp

# Convert public key to JWKS format
def public_key_to_jwks(private_key, kid):
    public_key = private_key.public_key()
    numbers = public_key.public_numbers()
    e = base64.urlsafe_b64encode(numbers.e.to_bytes(3, "big")).decode("utf-8").rstrip("=")
    n = base64.urlsafe_b64encode(numbers.n.to_bytes(256, "big")).decode("utf-8").rstrip("=")
    return {
        "kty": "RSA",
        "use": "sig",
        "kid": str(kid),
        "n": n,
        "e": e,
        "alg": "RS256"
    }

@app.route("/.well-known/jwks.json")
def jwks():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    now = int(datetime.utcnow().timestamp())
    c.execute("SELECT kid, key FROM keys WHERE exp > ?", (now,))
    keys = c.fetchall()
    conn.close()
    
    jwks_keys = []
    for kid, pem in keys:
        private_key = serialization.load_pem_private_key(pem, password=None)
        jwks_keys.append(public_key_to_jwks(private_key, kid))
    
    return jsonify({"keys": jwks_keys})

@app.route("/auth", methods=["POST"])
def auth():
    # Basic Auth check
    auth_data = request.authorization
    if not auth_data or not check_auth(auth_data.username, auth_data.password):
        return jsonify({"error": "Missing credentials (provide Basic Auth or JSON username/password)"}), 401

    expired_param = request.args.get("expired", "false").lower()
    expired = expired_param == "true"
    
    kid, private_key, exp = get_private_key(expired=expired)
    if not private_key:
        return jsonify({"error": "No key found"}), 500

    payload = {
        "sub": "1234",
        "name": auth_data.username,
        "iat": int(datetime.utcnow().timestamp()),
        "exp": exp
    }
    token = jwt.encode(payload, private_key, algorithm="RS256", headers={"kid": str(kid)})
    return jsonify({"token": token})

if __name__ == "__main__":
    app.run(port=8080, debug=True)
