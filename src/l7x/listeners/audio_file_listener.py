#####################################################################################################
import io
import os

from starlette.requests import Request
from starlette.responses import StreamingResponse

from l7x.db import AudioModel
from l7x.utils.db_utils import check_session_with_request, check_superuser_state
from l7x.utils.fastapi_utils import AppFastAPI

#####################################################################################################

async def _audio_file_page(request: Request, audio_uuid: str) -> StreamingResponse:
    is_valid_session = await check_session_with_request(request, 'get audio file')
    error_headers = {
        'Content-Disposition': f'attachment; filename="error.wav"'
    }
    error_file_buffer = io.BytesIO()

    if not is_valid_session:
        err_response = StreamingResponse(error_file_buffer, headers=error_headers)
        err_response.delete_cookie('session_uuid')
        return err_response

    if not await check_superuser_state(request):
        return StreamingResponse(error_file_buffer, headers=error_headers)

    audio_file: AudioModel | None = await AudioModel.objects.get_or_none(primary_uuid=audio_uuid)

    if audio_file is not None:
        audio_bytes = audio_file.audio_raw
        headers = {
            'Content-Disposition': f'attachment; filename="{audio_uuid}.wav"'
        }
        audio_io = io.BytesIO(audio_bytes)
        return StreamingResponse(audio_io, headers=headers)
    else:
        return StreamingResponse(error_file_buffer, headers=error_headers)

#####################################################################################################

def audio_file_page_listener_registrar(app: AppFastAPI, /) -> None:
    if app.app_settings.enable_admin_pages:
        app.get('/api/audio_file/{audio_uuid}')(_audio_file_page)

#####################################################################################################
