import re
from dataclasses import dataclass

PATRON_NOMBRE = re.compile(
    r"^(?P<camara>[A-Z]+)_(?P<escena>SC\d{2})_(?P<toma>T\d{2})_(?P<idx>\d{3})$",
    re.IGNORECASE,
)

@dataclass
class InfoClip:
    ruta: Path
    camara: str
    escena: str
    toma: str
    idx: str
    valido: bool
    motivo_rechazo: str = ""

def parsear_archivo(ruta: Path) -> InfoClip:
    m = PATRON_NOMBRE.match(ruta.stem)
    if not m:
        return InfoClip(
            ruta=ruta, camara="", escena="", toma="", idx="",
            valido=False, motivo_rechazo="Nombre no sigue la convención",
        )
    return InfoClip(
        ruta=ruta,
        camara=m.group("camara").upper(),
        escena=m.group("escena").upper(),
        toma=m.group("toma").upper(),
        idx=m.group("idx"),
        valido=True,
    )
