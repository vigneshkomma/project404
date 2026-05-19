from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
from fastapi.responses import FileResponse
from pathlib import Path
import logging

#Importing routes
from app.routes import auth, agents, run, home, logout

logger = logging.getLogger(__name__)


#Lifespan handler 
@asynccontextmanager
async def lifespan(app: FastAPI):
    #Startup logic - connecting to databases and other backend connections
    logger.info("Backend API started")

    #DB init (DEV only)
    from app.core.database import Base, engine
    from app.models import user, agent 

    Base.metadata.create_all(bind = engine)
    print(Base.metadata.tables.keys())
    logger.info("Database connected and tables ready")

    yield #backend running here

    #shutdown logic
    print("Backlend API stoppedn\n")


#App instance
app = FastAPI(
    title="project404-API",
    description="backend API for p404",
    version="0.0.1",
    lifespan=lifespan,
    redirect_slashes=False
)

#CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"], #change later
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

#Routes
app.include_router(auth.router,prefix="/auth",tags=["Auth"])
app.include_router(agents.router,prefix="/agents",tags=["Agents"])
app.include_router(run.router,prefix="/run",tags=["Run"])
app.include_router(home.router, prefix="/home",tags=["Home"])
app.include_router(logout.router, prefix="/logout", tags=["Logout"])

#Health check
@app.get("/")
def root():
    BASE_DIR = Path(__file__).resolve().parent
    return FileResponse(str(BASE_DIR / "../../frontend/index.html"))












