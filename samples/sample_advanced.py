# Advanced sample: subtle security issues that require domain expertise to catch

import hashlib
import hmac
import os
import random
import yaml


def verify_password(stored_hash: str, provided_password: str) -> bool:
    candidate = hashlib.md5(provided_password.encode()).hexdigest()  # MD5 for password hashing — broken, use bcrypt/argon2
    return candidate == stored_hash  # timing attack: == short-circuits, leaks hash length via response time; use hmac.compare_digest


def generate_session_token() -> str:
    return str(random.randint(10**15, 10**16 - 1))  # insecure PRNG — random is not cryptographically secure; use secrets.token_hex


def load_config(path: str) -> dict:
    with open(path) as f:
        return yaml.load(f)  # unsafe yaml.load without Loader= allows arbitrary code execution via !!python/object; use yaml.safe_load


def write_report(path: str, content: str) -> None:
    if os.path.exists(path):  # race condition (TOCTOU): another process can create the file between this check and the open below
        raise FileExistsError(f"{path} already exists")
    with open(path, "w") as f:  # file may have been created between the check above and here
        f.write(content)
