from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

#Importing routes
from app.routes import auth, agents, run

#Lifespan handler 
@asynccontextmanager
async def lifespan(app: FastAPI):
    #Startup logic - connecting to databases and other backend connections
    print("Backend API started\n")

    yield #backend running here

    #shutdown logic
    print("Backlend API stoppedn\n")


#App instance
app = FastAPI(
    title="project404-API",
    description="backend API for p404",
    version="0.0.1",
    lifespan=lifespan
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

#Health check
@app.get("/")
def root():
    return {"message":"p404 API is running"}












