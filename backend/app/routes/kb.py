import os
from fastapi import APIRouter, UploadFile, File, HTTPException, Form

from app.services.openai_client import client

router = APIRouter()

# Used only for LOCAL dev fallback. Fly machines reset, so don't rely on this in prod.
VECTOR_STORE_ID_HOLDER = {"vs_id": ""}


@router.post("/admin/upload_nec")
async def upload_nec(password: str = Form(...), file: UploadFile = File(...)):
    admin_pw = os.environ.get("ADMIN_PASSWORD", "").strip()
    if not admin_pw or password != admin_pw:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="PDF required")

    # Prefer persistent env var (Fly secret). Fallback to in-memory for local.
    vs_id = os.environ.get("NEC_VECTOR_STORE_ID", "").strip() or VECTOR_STORE_ID_HOLDER.get("vs_id", "").strip()

    # If no vector store yet (local), create one
    if not vs_id:
        vs = client.vector_stores.create(name="NEC")
        vs_id = vs.id
        VECTOR_STORE_ID_HOLDER["vs_id"] = vs_id

    data = await file.read()

    # Upload file and attach to the vector store
    up = client.files.create(
        file=(file.filename, data, "application/pdf"),
        purpose="assistants",
    )

    client.vector_stores.files.create(vector_store_id=vs_id, file_id=up.id)

    return {"status": "indexed", "vector_store_id": vs_id}
