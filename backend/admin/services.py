import os
import binascii


def generate_admin_token() -> str:
    return binascii.hexlify(os.urandom(30)).decode()
