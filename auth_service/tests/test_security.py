from app.core.security import (
    create_access_token,
    decode_token,
    hash_password,
    verify_password,
)


def test_hash_password():
    password = "12345678"

    password_hash = hash_password(password)

    assert password_hash != password
    assert verify_password(password, password_hash) is True
    assert verify_password("wrong_password", password_hash) is False


def test_create_and_decode_access_token():
    token = create_access_token(
        user_id=1,
        role="user"
    )

    payload = decode_token(token)

    assert payload["sub"] == "1"
    assert payload["role"] == "user"
    assert "iat" in payload
    assert "exp" in payload