import sqlite3
from datetime import datetime, timedelta
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# Function to create a private key and store it in the database
def store_key(expiry_minutes=60):
    # Generate a new 2048-bit RSA private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    # Convert key to PEM format so SQLite can store it as text
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Calculate expiration time
    expiry = int((datetime.utcnow() + timedelta(minutes=expiry_minutes)).timestamp())

    # Store in database
    conn = sqlite3.connect("totally_not_my_privateKeys.db")
    c = conn.cursor()
    c.execute("INSERT INTO keys (key, exp) VALUES (?, ?)", (pem, expiry))
    conn.commit()
    conn.close()

# Store one valid key (1 hour from now) and one expired key (-1 hour)
store_key(expiry_minutes=60)   # valid key
store_key(expiry_minutes=-60)  # expired key

print("Keys stored in database successfully!")
