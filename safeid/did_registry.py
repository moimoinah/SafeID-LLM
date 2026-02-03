from typing import Dict
from dataclasses import dataclass, asdict
import uuid

@dataclass
class DIDDocument:
    did: str
    public_key: str
    service_endpoint: str

class DIDRegistry:
    def __init__(self):
        self._store: Dict[str, DIDDocument] = {}

    def create_did(self, service_endpoint: str) -> DIDDocument:
        did = f"did:safeid:{uuid.uuid4()}"
        public_key = f"pk-{uuid.uuid4()}"
        doc = DIDDocument(did=did, public_key=public_key, service_endpoint=service_endpoint)
        self._store[did] = doc
        return doc

    def get_did(self, did: str) -> DIDDocument | None:
        return self._store.get(did)

    def to_dict(self, did: str):
        doc = self.get_did(did)
        return asdict(doc) if doc else None
