import sys
import os
import shutil
import platform
from pathlib import Path

SCRIPT_VERSION = "1.4.0"
TOOL_NAME = "utilerias_resolve"

def resolve_install_path() -> Path:
    sistema = platform.system()
    if sistema == "Linux":
        base = Path.home() / ".local/share/DaVinciResolve/Fusion/Scripts"
    elif sistema == "Darwin":
        base = Path.home() / "Library/Application Support/DaVinci Resolve/Fusion/Scripts"
    elif sistema == "Windows":
        base = Path(os.environ["APPDATA"]) / "Blackmagic Design/DaVinci Resolve/Fusion/Scripts"
    else:
        raise RuntimeError(f"Sistema operativo no soportado: {sistema}")
    return base / TOOL_NAME

def instalar(origen: Path, destino: Path, forzar: bool = False, dry_run: bool = False):
    version_file = destino / "_version.txt"
    if destino.exists() and not forzar:
        if version_file.exists():
            version_instalada = version_file.read_text().strip()
            if version_instalada == SCRIPT_VERSION:
                print(f"Versión {SCRIPT_VERSION} ya instalada. Use --force para reinstalar.")
                return
    if dry_run:
        print(f"[DRY-RUN] Copiaría {origen} → {destino}")
        return
    if destino.exists():
        shutil.rmtree(destino)
    shutil.copytree(origen, destino)
    version_file.write_text(SCRIPT_VERSION)
    print(f"Instalado {TOOL_NAME} v{SCRIPT_VERSION} en {destino}")

if __name__ == "__main__":
    forzar = "--force" in sys.argv
    dry_run = "--dry-run" in sys.argv
    origen = Path(__file__).parent / "src"
    destino = resolve_install_path()
    instalar(origen, destino, forzar=forzar, dry_run=dry_run)
