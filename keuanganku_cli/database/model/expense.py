from dataclasses import dataclass
from datetime import datetime

@dataclass
class ModelExpense:
    id: int
    title: str
    time: datetime
    amount: float
    category_id: int
    rate: int 

    def __post_init__(self):
        pass
