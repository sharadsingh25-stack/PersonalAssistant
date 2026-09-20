import hashlib
from pathlib import Path


class DocumentHasher:

    @staticmethod
    def calculate_hash(file_path: str) -> str:

        sha256 = hashlib.sha256()

        with open(file_path, "rb") as file:

            while chunk := file.read(8192):
                sha256.update(chunk)

        return sha256.hexdigest()