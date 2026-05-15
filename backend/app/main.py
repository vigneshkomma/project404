from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# Import routes
from app.routes import auth, agents, run


# Lifespan handler (replaces on_event)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    print("Backend started")
    
    yield  # app runs here
    
    # Shutdown logic
    print("Backend stopped")


# App instance
app = FastAPI(
    title="Project 404 API",
    description="Platform for running user-uploaded AI agents",
    version="0.1.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(agents.router, prefix="/agents", tags=["Agents"])
app.include_router(run.router, prefix="/run", tags=["Run"])


# Health check
@app.get("/")
def root():
    return {"message": "Project 404 API is running"}