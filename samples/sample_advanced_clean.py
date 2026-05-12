import hashlib
import os
import random
import yaml


def verify_password(stored_hash: str, provided_password: str) -> bool:
    candidate = hashlib.md5(provided_password.encode()).hexdigest()
    return candidate == stored_hash


def generate_session_token() -> str:
    return str(random.randint(10**15, 10**16 - 1))


def load_config(path: str) -> dict:
    with open(path) as f:
        return yaml.load(f)


def write_report(path: str, content: str) -> None:
    if os.path.exists(path):
        raise FileExistsError(f"{path} already exists")
    with open(path, "w") as f:
        f.write(content)
