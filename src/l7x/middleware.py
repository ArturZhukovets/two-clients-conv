from typing import Final

from nicegui import Client
from starlette.exceptions import HTTPException
from starlette.middleware import _MiddlewareClass
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import RedirectResponse

from l7x.db import SessionModel

#####################################################################################################

class AuthMiddleware(BaseHTTPMiddleware, _MiddlewareClass):
    #####################################################################################################

    login_page = '/login'
    gui_page = '/'
    admin_page = '/admin'

    #####################################################################################################

    async def dispatch(self, request: Request, call_next):
        client_page_routes: Final = [route for route in Client.page_routes.values()]
        if request.url.path in client_page_routes:
            session_uuid = request.cookies.get('session_uuid')
            if session_uuid is None:
                if request.url.path == self.login_page:
                    return await call_next(request)
                else:
                    RedirectResponse(self.login_page)

            session = await SessionModel.objects.get_or_none(primary_uuid=session_uuid)
            if session is not None:
                if session.logout_ts is None:
                    if request.url.path == self.gui_page or request.url.path == self.admin_page:
                        return await call_next(request)
                    else:
                        return RedirectResponse(self.gui_page)

            response = RedirectResponse('/login')
            response.delete_cookie('session_uuid')
            return response
        return await call_next(request)

#####################################################################################################

class AdminMiddleware(BaseHTTPMiddleware, _MiddlewareClass):
    #####################################################################################################

    admin_page = '/admin'
    login_page = '/login'
    error_response = RedirectResponse(login_page)
    exception = HTTPException(status_code=404, detail='Page not found')

    #####################################################################################################

    async def dispatch(self, request: Request, call_next):
        if request.url.path == self.admin_page:
            session_uuid = request.cookies.get('session_uuid')
            if session_uuid is None:
                return self.error_response
            session = await SessionModel.objects.select_related('user_id').get_or_none(primary_uuid=session_uuid)
            if session is not None:
                if session.logout_ts is not None:
                    self.error_response.delete_cookie('session_uuid')
                    return self.error_response
                if not session.user_id.is_superuser:
                    raise self.exception

        return await call_next(request)

#####################################################################################################

