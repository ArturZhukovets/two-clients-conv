#####################################################################################################

from typing import Final

import l7x.alembic.versions.db_2024_05_16_1304_dcbcd14d03c3_init_db as _db_2024_05_16_1304_dcbcd14d03c3_init_db
import l7x.alembic.versions.db_2024_06_06_0721_06418e54240c_add_audio as _db_2024_06_06_0721_06418e54240c_add_audio
import l7x.alembic.versions.db_2024_06_13_0812_a94c970ba137_add_superuser as _db_2024_06_13_0812_a94c970ba137_add_superuser
import l7x.alembic.versions.db_2024_09_09_0734_c38f2590159a_root_user_if_not_exist as _db_2024_09_09_0734_c38f2590159a
import l7x.alembic.versions.db_2024_09_12_1114_e0fbac170f88_cascade_delete_text_model as _db_e0fbac170f88
import l7x.alembic.versions.db_2024_09_25_1151_92e150428401_bind_conv_to_two_users as _db_92e150428401
import l7x.alembic.versions.db_2024_09_27_1208_f28f266ea7b4_text_model_change_type_field as _db_f28f266ea7b4
#####################################################################################################

# TODO: написать тест что миграции в массиве не повторяются
# TODO: написать тест что в массив добавлены все имеющиеся модули миграции
MIGRATIONS: Final = frozenset((
    _db_2024_05_16_1304_dcbcd14d03c3_init_db,
    _db_2024_06_06_0721_06418e54240c_add_audio,
    _db_2024_06_13_0812_a94c970ba137_add_superuser,
    _db_2024_09_09_0734_c38f2590159a,
    _db_e0fbac170f88,
    _db_92e150428401,
    _db_f28f266ea7b4,
))

#####################################################################################################
