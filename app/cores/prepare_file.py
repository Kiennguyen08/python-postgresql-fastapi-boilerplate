import asyncio
import io
import logging
from functools import partial, wraps

from pydub import AudioSegment

logger = logging.getLogger(__name__)


def async_wrap(func):
    @wraps(func)
    async def run(*args, loop=None, executor=None, **kwargs):
        if loop is None:
            loop = asyncio.get_event_loop()
        pfunc = partial(func, *args, **kwargs)
        return await loop.run_in_executor(executor, pfunc)

    return run


@async_wrap
def format_audio_bytes(
    audio_bytes: bytes,
    input_audio_format=None,
    out_put_format="wav",
    num_channels: int = 1,
    sample_width: int = 2,
    frame_rate: int = 16000,
):
    audio_bytes = io.BytesIO(audio_bytes)
    sound = AudioSegment.from_file(audio_bytes, input_audio_format)
    sound = (
        sound.set_channels(num_channels)
        .set_frame_rate(frame_rate)
        .set_sample_width(sample_width)
    )
    wav_id = io.BytesIO()
    sound.export(wav_id, format=out_put_format)
    return wav_id.getvalue()
