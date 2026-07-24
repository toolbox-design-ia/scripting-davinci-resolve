from dataclasses import dataclass
from enum import Enum
import time

class EstadoTrabajo(Enum):
    PENDIENTE = "pendiente"
    EN_COLA = "en_cola"
    RENDERIZANDO = "renderizando"
    COMPLETADO = "completado"
    FALLIDO = "fallido"

@dataclass
class TrabajoDEntrega:
    preset_id: str
    target_dir: str
    output_filename: str
    uuid_resolve: str = ""
    estado: EstadoTrabajo = EstadoTrabajo.PENDIENTE
    intentos: int = 0
    max_intentos: int = 3
    inicio: float = 0.0
    fin: float = 0.0
    error: str = ""

def encolar_todos(
    project, catalogo: list[dict], destinos: dict
) -> list[TrabajoDEntrega]:
    trabajos = []
    for preset_def in catalogo:
        target_dir = destinos[preset_def["target_dir_key"]]
        output_name = f"{project.GetName()}_{preset_def['id']}"

        ok = aplicar_preset_a_resolve(project, preset_def, target_dir)
        if not ok:
            print(f"[WARN] Preset {preset_def['id']} no se pudo configurar. Saltando.")
            continue

        project.SetRenderSettings({"CustomName": output_name})
        uuid = project.AddRenderJob()

        if uuid:
            t = TrabajoDEntrega(
                preset_id=preset_def["id"],
                target_dir=target_dir,
                output_filename=output_name,
                uuid_resolve=uuid,
                estado=EstadoTrabajo.EN_COLA,
            )
            trabajos.append(t)
            print(f"[INFO] Encolado: {output_name} → {target_dir}")
        else:
            print(f"[ERROR] No se pudo encolar {output_name}")

    return trabajos
