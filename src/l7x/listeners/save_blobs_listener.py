#####################################################################################################
from typing import Final

from fastapi import UploadFile
from fastapi.params import File
from starlette.requests import Request
from starlette.responses import JSONResponse

from l7x.db.audio_model import AudioModel
from l7x.utils.db_utils import check_session_with_request
from l7x.utils.fastapi_utils import AppFastAPI

#####################################################################################################

_ERROR_RESPONSE_MSG: Final = {'status': 'error'}

async def _save_blob_page(request: Request, file: UploadFile = File(...)) -> JSONResponse:
    logger: Final = request.app.logger
    is_valid_session = await check_session_with_request(request, 'save audio blob to db')

    if not is_valid_session:
        err_response = JSONResponse(_ERROR_RESPONSE_MSG)
        err_response.delete_cookie('session_uuid')
        return err_response
    try:
        file_bytes: Final = file.file.read()
        new_audio = await AudioModel(audio_raw=file_bytes).upsert()
        return JSONResponse({'status': 'ok', 'audio_uuid': str(new_audio.primary_uuid)})
    except BaseException as err:
        logger.warning(f'Can`t save audio. Save to db error : {err}')
        return JSONResponse(_ERROR_RESPONSE_MSG)

#####################################################################################################

def save_blob_page_listener_registrar(app: AppFastAPI, /) -> None:
    app.post('/api/save_audio')(_save_blob_page)

#####################################################################################################
