from dataclasses import dataclass
from datetime import datetime

@dataclass
class ModelPengeluaran:
    id: int
    judul: str
    waktu: datetime
    jumlah: float
    id_kategori: int
    rating: int 

    def __post_init__(self):
        pass
