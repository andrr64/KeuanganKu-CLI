from dataclasses import dataclass

@dataclass(frozen=True, kw_only=True)
class ModelExpenseCategory:
    id : int = 0
    title : str = ""
    active : int = 1

    def __post_init__(self):
        pass

    def __str__(self) -> str:
        return self.title