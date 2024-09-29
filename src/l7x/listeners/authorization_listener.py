#####################################################################################################

from collections.abc import Mapping
from typing import Final

from argon2.exceptions import VerifyMismatchError
from fastapi import Form
from starlette.requests import Request
from starlette.responses import JSONResponse

from l7x.app import App
from l7x.db import SessionModel, UserModel
from l7x.types.language import LKey
from l7x.types.localization import TKey
from l7x.utils.datetime_utils import generate_midnight_datetime
from l7x.utils.fastapi_utils import AppFastAPI

#####################################################################################################


def _get_err_response(app: App) -> Mapping[str, str]:
    _default_lang = app.app_settings.default_language_locale
    _err_msg = TKey.ERR_LOGIN_MSG(app.logger, LKey(_default_lang))
    return {'resp_status': 'login_error', 'err_msg': _err_msg}

async def _authorization_page(request: Request, login: str = Form(...), password: str = Form(...)) -> JSONResponse:
    app: Final = request.app
    logger: Final = app.logger

    user_model = await UserModel.objects.select_related('department_id').get_or_none(login=login)
    if user_model is None:
        logger.warning(f'Invalid user login: {login}')
        return JSONResponse(_get_err_response(app))
    if not user_model.is_active:
        logger.warning(f'User {login} is not active')
        return JSONResponse(_get_err_response(app))

    password_hasher = app.password_hasher

    password_hash: Final = user_model.password

    try:
        password_hasher.verify(password_hash, password)
    except VerifyMismatchError:
        logger.warning(f'User {login} enter invalid password')
        return JSONResponse(_get_err_response(app))

    if password_hasher.check_needs_rehash(password_hash):
        logger.info(f'Update password hash for user {login}')
        user_model.password = password_hasher.hash(password)
        await user_model.upsert()

    new_session = await SessionModel(user_id=user_model.primary_uuid).upsert()
    response = JSONResponse({'resp_status': 'ok'})

    response.set_cookie(
        key='session_uuid',
        value=str(new_session.primary_uuid),
        httponly=True,
        expires=generate_midnight_datetime(user_model.department_id.timezone).strftime("%a, %d-%b-%Y %H:%M:%S GMT"),
    )

    return response

#####################################################################################################

def authorization_page_listener_registrar(app: AppFastAPI, /) -> None:
    app.post('/api/authorization')(_authorization_page)

#####################################################################################################
