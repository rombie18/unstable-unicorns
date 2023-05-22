from enum import Enum, auto

class Effect:
    def __init__(self) -> None:
        self.trigger
        self.condition
        self.actions = []
        
    def apply(self, player):
        assert "Can't apply general effect class"
        
class DodenBezwerendeEenhoornEffect(Effect):
    def __init__(self) -> None:
        
        
    def apply(self, player):
        
        
class EffectTrigger(Enum):
    BEGINNING_OF_TURN = auto()
    ONCE = auto()
    ON_STABLE_ENTER = auto()