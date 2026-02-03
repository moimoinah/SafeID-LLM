from dataclasses import dataclass
from safeid.did_registry import DIDRegistry
from logs.logger import LogStorage

@dataclass
class VerificationResult:
    success: bool
    reason: str

class IdentityVerificationService:
    def __init__(self, registry: DIDRegistry, log_storage: LogStorage):
        self.registry = registry
        self.log_storage = log_storage

    def create_identity(self, service_endpoint: str, source_ip: str):
        did_doc = self.registry.create_did(service_endpoint)
        self.log_storage.log_event(
            did=did_doc.did,
            source_ip=source_ip,
            event_type="did_created",
            success=True,
            details="DID created"
        )
        return did_doc

    def verify_identity(self, did: str, presented_public_key: str, source_ip: str) -> VerificationResult:
        doc = self.registry.get_did(did)
        if not doc:
            self.log_storage.log_event(
                did=did,
                source_ip=source_ip,
                event_type="verification",
                success=False,
                details="DID not found"
            )
            return VerificationResult(False, "DID not found")

        if presented_public_key != doc.public_key:
            self.log_storage.log_event(
                did=did,
                source_ip=source_ip,
                event_type="verification",
                success=False,
                details="Public key mismatch"
            )
            return VerificationResult(False, "Invalid credentials")

        self.log_storage.log_event(
            did=did,
            source_ip=source_ip,
            event_type="verification",
            success=True,
            details="Verification success"
        )
        return VerificationResult(True, "Verified")
