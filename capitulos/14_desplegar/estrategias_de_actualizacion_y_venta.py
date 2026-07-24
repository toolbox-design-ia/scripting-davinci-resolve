import shutil
from pathlib import Path

def activar_pendiente(scripts_dir: Path):
    activo    = scripts_dir / "utilerias_resolve"
    pendiente = scripts_dir / "_pending" / "utilerias_resolve"
    backup    = scripts_dir / "utilerias_resolve_backup"

    if not pendiente.exists():
        print("No hay actualización pendiente.")
        return

    if activo.exists():
        if backup.exists():
            shutil.rmtree(backup)
        activo.rename(backup)

    pendiente.rename(activo)
    print(f"Actualización activada. Versión anterior conservada en {backup}.")
