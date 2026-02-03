from fastapi import FastAPI
from pydantic import BaseModel

from safeid.did_registry import DIDRegistry
from identity_verification.service import IdentityVerificationService
from logs.logger import LogStorage
from llm_engine.risk_engine import LLMRiskEngine

app = FastAPI()

registry = DIDRegistry()
log_storage = LogStorage()
verification_service = IdentityVerificationService(registry, log_storage)
risk_engine = LLMRiskEngine()

class CreateDIDRequest(BaseModel):
    service_endpoint: str
    source_ip: str

class VerifyRequest(BaseModel):
    did: str
    presented_public_key: str
    source_ip: str

@app.post("/did/create")
def create_did(req: CreateDIDRequest):
    doc = verification_service.create_identity(req.service_endpoint, req.source_ip)
    return {"did": doc.did, "public_key": doc.public_key}

@app.post("/did/verify")
def verify(req: VerifyRequest):
    result = verification_service.verify_identity(
        did=req.did,
        presented_public_key=req.presented_public_key,
        source_ip=req.source_ip,
    )
    logs = log_storage.get_events_for_did(req.did)
    risk_score, explanation = risk_engine.analyze(logs)
    return {
        "success": result.success,
        "reason": result.reason,
        "risk_score": risk_score,
        "risk_explanation": explanation,
        "logs": logs,
    }
