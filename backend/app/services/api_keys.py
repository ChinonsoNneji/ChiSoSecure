import hashlib
import secrets


def generate_api_key():
    return f"css_{secrets.token_urlsafe(32)}"


def hash_api_key(api_key: str):
    return hashlib.sha256(
        api_key.encode()
    ).hexdigest()


def verify_api_key(
    api_key: str,
    stored_hash: str
):
    return secrets.compare_digest(
        hash_api_key(api_key),
        stored_hash,
    )
