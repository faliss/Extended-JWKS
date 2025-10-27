import requests

BASE = "http://localhost:8080"

def test_auth_valid():
    r = requests.post(f"{BASE}/auth", auth=("userABC", "password123"))
    assert r.status_code == 200
    assert "token" in r.json()

def test_auth_expired():
    r = requests.post(f"{BASE}/auth?expired=true", auth=("userABC", "password123"))
    assert r.status_code == 200
    assert "token" in r.json()

def test_auth_wrong():
    r = requests.post(f"{BASE}/auth", auth=("wrong","wrong"))
    assert r.status_code == 401
