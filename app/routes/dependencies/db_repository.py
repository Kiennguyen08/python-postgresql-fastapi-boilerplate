from collections.abc import Callable
from typing import Annotated, Tuple

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.cores.database import Base
from app.endpoints import endpoint
from app.models.user_voices import UserVoices
from app.models.voice_styles import VoiceStyles
from app.models.voices import Voices
from app.repositories.database_repository import DatabaseRepository


def get_repository(
    model: type[Base],
) -> Callable[[AsyncSession], DatabaseRepository]:
    def func(session: AsyncSession = Depends(endpoint.postgres.db_session)):
        return DatabaseRepository(model, session)

    return func


VoiceRepository = Annotated[
    DatabaseRepository[Voices],
    Depends(get_repository(Voices)),
]

VoiceStyleRepository = Annotated[
    DatabaseRepository[VoiceStyles],
    Depends(get_repository(VoiceStyles)),
]

UserVoiceRepository = Annotated[
    DatabaseRepository[UserVoices],
    Depends(get_repository(UserVoices)),
]


def get_voice_bundle_repo(
    voices_repo: VoiceRepository,
    styles_repo: VoiceStyleRepository,
    user_voices_repo: UserVoiceRepository,
) -> Tuple[
    DatabaseRepository[Voices],
    DatabaseRepository[VoiceStyles],
    DatabaseRepository[UserVoices],
]:
    return (voices_repo, styles_repo, user_voices_repo)


VoiceBundleRepository = Annotated[
    Tuple[
        DatabaseRepository[Voices],
        DatabaseRepository[VoiceStyles],
        DatabaseRepository[UserVoices],
    ],
    Depends(get_voice_bundle_repo),
]
