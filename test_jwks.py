import requests

BASE = "http://localhost:8080"

def test_jwks():
    r = requests.get(f"{BASE}/.well-known/jwks.json")
    assert r.status_code == 200
    data = r.json()
    assert "keys" in data
    assert len(data["keys"]) > 0
