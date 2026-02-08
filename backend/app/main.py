from fastapi import FastAPI
from fastapi.responses import FileResponse

from app.routes import kb, nec

app = FastAPI(title="NEC AI")

app.include_router(kb.router)
app.include_router(nec.router)

@app.get("/")
def home():
    return FileResponse("../frontend/index.html")

@app.get("/admin")
def admin():
    return FileResponse("../frontend/admin.html")
