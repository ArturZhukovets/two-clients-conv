#####################################################################################################

from logging import Logger
from typing import Final

from argon2 import Parameters, PasswordHasher
from argon2.low_level import Type
from argon2.profiles import CHEAPEST

from l7x.configs.settings import AppSettings

#####################################################################################################

def create_password_hasher(settings: AppSettings, logger: Logger) -> PasswordHasher:
    if settings.is_dev_mode:
        logger.warning('Using CHEAPEST password hasher for debug purpose')
    params: Final = CHEAPEST if settings.is_dev_mode else Parameters(
        type=Type.ID,
        version=19,
        salt_len=settings.pwd_salt_len,
        hash_len=settings.pwd_hash_len,
        time_cost=settings.pwd_time_cost,
        memory_cost=settings.pwd_memory_cost_kib,
        parallelism=settings.pwd_parallelism,
    )
    return PasswordHasher.from_parameters(params)

#####################################################################################################
