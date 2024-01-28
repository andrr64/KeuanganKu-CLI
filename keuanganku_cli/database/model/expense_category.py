from dataclasses import dataclass

@dataclass(frozen=True, kw_only=True)
class ModelKategoriPengeluaran:
    id : int = 0
    judul : str = ""

    def __post_init__(self):
        pass
