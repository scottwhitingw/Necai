from fastapi import FastAPI

from app.routes import kb, nec

app = FastAPI(title="NEC AI")

app.include_router(kb.router)
app.include_router(nec.router)

@app.get("/")
def home():
    return {
        "status": "online",
        "docs": "/docs",
        "nec_endpoint": "/nec/ask"
    }

@app.get("/admin")
def admin():
    return {"status": "admin endpoint active"}
