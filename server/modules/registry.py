from modules.effect import Effect
from modules.effects import *

# card id와 자식 클래스의 매핑
EFFECT_DICT: dict[int, type[Effect]] = {
    1: Effect_1,
    2: Effect_2,
}

async def get_effect(effect_id:int):
    return EFFECT_DICT.get(effect_id)
