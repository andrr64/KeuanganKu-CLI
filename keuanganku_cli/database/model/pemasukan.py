from dataclasses import dataclass
from datetime import datetime

@dataclass(kw_only=True, frozen=True)
class ModelPemasukan:
    id : int = 0
    judul : str
    waktu : datetime
    jumlah : float
    id_kategori : int
    
    def __post_init__(self):
        pass