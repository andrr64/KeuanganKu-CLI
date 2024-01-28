from dataclasses import dataclass, field

@dataclass(frozen=True, kw_only=True)
class ModelKategoriPemasukan:
    id : int = 0
    judul : str = ""

    def __post_init__(self):
        pass
