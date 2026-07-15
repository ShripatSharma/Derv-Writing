"""
File Utility Functions
"""

import hashlib


def calculate_file_hash(file_path, chunk_size=8192):
    """
    Calculate SHA256 hash of a file.
    """

    sha256 = hashlib.sha256()

    with open(file_path, "rb") as f:

        while True:

            chunk = f.read(chunk_size)

            if not chunk:
                break

            sha256.update(chunk)

    return sha256.hexdigest()


def get_file_size(file_path):

    return file_path.stat().st_size