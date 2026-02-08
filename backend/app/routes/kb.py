import os
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from app.services.openai_client import client

router = APIRouter()

VECTOR_STORE_ID_HOLDER = {"vs_id": os.environ.get("NEC_VECTOR_STORE_ID", "")}

@router.post("/admin/upload_nec")
async def upload_nec(password: str = Form(...), file: UploadFile = File(...)):
    admin_pw = os.environ.get("ADMIN_PASSWORD", "")
    if not admin_pw or password != admin_pw:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="PDF required")

    vs = client.vector_stores.create(name="NEC")

    data = await file.read()
    up = client.files.create(
        file=(file.filename, data, "application/pdf"),
        purpose="assistants"
    )

    client.vector_stores.files.create(vector_store_id=vs.id, file_id=up.id)

    VECTOR_STORE_ID_HOLDER["vs_id"] = vs.id
    return {"status": "indexed", "vector_store_id": vs.id}
