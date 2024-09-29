#####################################################################################################

from typing import Final

from starlette.requests import Request
from starlette.responses import JSONResponse

from l7x.utils.db_utils import SessionClosed, SessionNotFound, UserNotActive, check_valid_session
from l7x.utils.fastapi_utils import AppFastAPI

#####################################################################################################

async def _session_exp_page(request: Request):
    bad_response = JSONResponse(False)
    cookies: Final = request.cookies
    session_uuid = cookies.get('session_uuid')
    if session_uuid is None:
        return bad_response

    try:
        await check_valid_session(session_uuid)
    except (UserNotActive, SessionClosed, SessionNotFound):
        bad_response.delete_cookie('session_uuid')
        return bad_response

    return JSONResponse(True)

#####################################################################################################

def session_exp_check_page_listener_registrar(app: AppFastAPI, /) -> None:
    app.get('/api/session_exp')(_session_exp_page)

#####################################################################################################
