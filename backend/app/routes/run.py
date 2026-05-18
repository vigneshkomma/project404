from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def agent_run():
    return {"message": "agrnt run route working"}