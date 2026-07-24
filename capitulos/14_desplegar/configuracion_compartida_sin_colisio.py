from pathlib import Path
import json

CONFIG_GLOBAL  = Path(__file__).parent / "config" / "defaults.json"
CONFIG_SALA    = Path("/etc/resolve_tools/sala.json")        # Linux / macOS
CONFIG_USUARIO = Path.home() / ".resolve_tools" / "user.json"

def cargar_config() -> dict:
    config = {}
    for ruta in [CONFIG_GLOBAL, CONFIG_SALA, CONFIG_USUARIO]:
        if ruta.exists():
            config.update(json.loads(ruta.read_text()))
    return config
