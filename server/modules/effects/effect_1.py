from modules.effect import Effect
from schemas.enum import ZoneType, TriggerType, TargetType
from schemas.game import ConditionInfo


class Effect_1(Effect):
    effect_id: int = 1
    triggers: list[TriggerType] = [TriggerType.SUMMON] # 트리거 타입 리스트
    targets: list[TargetType] = [TargetType.SELF] # 대상 타입 리스트
    zones: list[ZoneType]  = [ZoneType.FIELD] # 존 타입 리스트
    select: bool = True # 사용자 선택 여부
    cost: int = 1# 사용하는 코스트

    @classmethod
    def before(cls, condition_info: ConditionInfo):
        pass

    @classmethod
    def after(cls):
        pass
    
    @classmethod
    def condition(cls, condition_info: ConditionInfo) -> tuple[bool, list]:
        return super().condition(condition_info)