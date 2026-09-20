import json
from pathlib import Path


class HashStore:

    def __init__(self, metadata_file: str):
        self.metadata_file = Path(metadata_file)

    def load_hashes(self) -> dict:

        if not self.metadata_file.exists():
            return {}

        with open(
            self.metadata_file,
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)

    def save_hash(
        self,
        document_id: str,
        file_hash: str
    ):

        hashes = self.load_hashes()

        hashes[document_id] = file_hash

        self.metadata_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            self.metadata_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                hashes,
                file,
                indent=4
            )

    def is_changed(
        self,
        document_id: str,
        current_hash: str
    ) -> bool:
        
        hashes = self.load_hashes()

        previous_hash = hashes.get(document_id)

        # Document has never been processed
        if previous_hash is None:
            return True

        # File changed
        return previous_hash != current_hash