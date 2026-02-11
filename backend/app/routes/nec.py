import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.routes.kb import VECTOR_STORE_ID_HOLDER
from app.services.nec_agent import nec_lookup

router = APIRouter()

class Req(BaseModel):
    question: str

@router.post("/nec/ask")
def ask(req: Req):
    vs_id = (
        os.environ.get("NEC_VECTOR_STORE_ID", "").strip()
        or VECTOR_STORE_ID_HOLDER.get("vs_id", "").strip()
    )

    if not vs_id:
        raise HTTPException(
            status_code=400,
            detail="NEC not indexed yet. Set NEC_VECTOR_STORE_ID or upload NEC PDF first."
        )

    answer = nec_lookup(req.question, vs_id)
    return {"answer": answer}

