from dataclasses import dataclass, field

@dataclass(frozen=True, kw_only=True)
class ModelIncomeCategory:
    id : int = 0
    title : str = ""

    def __post_init__(self):
        pass
