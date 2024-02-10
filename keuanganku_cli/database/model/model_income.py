from dataclasses import dataclass
from datetime import datetime

@dataclass(kw_only=True, frozen=True)
class ModelIncome:
    id : int = 0
    title : str
    time : datetime
    amount : float
    category_id : int
    
    def __post_init__(self):
        pass