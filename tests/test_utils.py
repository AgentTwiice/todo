from backend.app.utils import hash_password, verify_password, create_access_token, decode_access_token
import time


def test_hash_and_verify():
    hashed = hash_password("secret")
    assert hashed != "secret"
    assert verify_password("secret", hashed)
    assert not verify_password("wrong", hashed)


def test_create_and_decode_token():
    token = create_access_token({"sub": "123"}, expires_seconds=1)
    data = decode_access_token(token)
    assert data["sub"] == "123"
    time.sleep(1.1)
    assert decode_access_token(token) is None
