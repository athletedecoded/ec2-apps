from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

"""
ENVIRONMENT CONFIG
"""
load_dotenv()

"""
RUNTIME SETUP
"""
app = FastAPI()
app.mount("/public", StaticFiles(directory="public"), name="public")

"""
ENDPOINT CONFIG
"""
# Landing Route
@app.get("/")
def landing():
    return FileResponse("public/index.html")

# Health Check
@app.get("/health", status_code=200)
def health():
    return {"ping": "pong"}
