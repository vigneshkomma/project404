from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter()


@router.get("")
def logout():
    response = RedirectResponse(url="/auth/login", status_code=302)

    response.delete_cookie(key="access_token")

    return response
