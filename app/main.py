from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from app.routes import messages, ws
from app.database import db  # importa a conexão com o Atlas

app = FastAPI(title="Chat Refatorado - FastAPI + MongoDB Atlas")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Monta as rotas REST e WebSocket
app.include_router(messages.router)
app.include_router(ws.router)

# Serve o cliente estático (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", include_in_schema=False)
async def index():
    return FileResponse("app/static/index.html")
