from fastapi import APIRouter, Cookie, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from jose import jwt, JWTError
from pathlib import Path

router = APIRouter()


#templates
BASE_DIR = Path(__file__).resolve().parent.parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"), context_processors=[])
templates.env.cache = None

#config
SECRET_KEY = "CHNAGE_THIS_TO_ENV_SWCRET"
ALGORITHM = "HS256"


@router.get("", response_class=HTMLResponse)
def home_page(
    request: Request,
    access_token: str | None = Cookie(default=None, alias="access_token")
):

    if not access_token:
        return RedirectResponse(url="/auth/login", status_code=302)

    try:
        payload = jwt.decode(
            access_token,                                                                                                           
            SECRET_KEY,                                                                                 
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("user_id")

        if not user_id:
            return RedirectResponse(url="/auth/login", status_code=302)

    except JWTError:
        return RedirectResponse(url="/auth/login", status_code=302)

    return templates.TemplateResponse(
        request,
        "home.html",
        {
            "request": request,
            "user_id": user_id
        }
    )                                                                                                       
