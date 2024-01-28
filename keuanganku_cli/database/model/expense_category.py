from dataclasses import dataclass

@dataclass(frozen=True, kw_only=True)
class ModelExpenseCategory:
    id : int = 0
    title : str = ""

    def __post_init__(self):
        pass
