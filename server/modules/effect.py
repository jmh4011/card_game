from modules.types import ZoneType, ConditionInfo, TriggerType, TargetType


class Effect:
    effect_id: int
    triggers: list[TriggerType]  # 트리거 타입 리스트
    targets: list[TargetType]  # 대상 타입 리스트
    zones: list[ZoneType]  # 존 타입 리스트
    select: bool  # 사용자 선택 여부
    cost: int # 사용하는 코스트

    @classmethod
    def before(cls, condition_info: ConditionInfo):
        pass

    @classmethod
    def after(cls):
        pass
    
    @classmethod
    def condition(cls, condition_info: ConditionInfo) -> bool:
        pass