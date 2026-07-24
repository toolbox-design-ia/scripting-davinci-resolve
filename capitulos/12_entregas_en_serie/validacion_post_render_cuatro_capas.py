import hashlib
import json
import subprocess
from pathlib import Path

def calcular_sha256(ruta: Path) -> str:
    sha = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(65536), b""):
            sha.update(bloque)
    return sha.hexdigest()

def obtener_duracion_segundos(ruta: Path) -> float | None:
    result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json",
         "-show_format", str(ruta)],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        return None
    data = json.loads(result.stdout)
    try:
        return float(data["format"]["duration"])
    except (KeyError, ValueError):
        return None

def validar_entrega(trabajo: TrabajoDEntrega, duracion_esperada_s: float) -> dict:
    candidatos = list(Path(trabajo.target_dir).glob(trabajo.output_filename + ".*"))

    resultado = {
        "preset_id": trabajo.preset_id,
        "archivo": None,
        "tamanio_bytes": 0,
        "duracion_s": None,
        "duracion_ok": False,
        "hash_sha256": None,
        "smoke_test_ok": False,
        "errores": [],
    }

    if not candidatos:
        resultado["errores"].append(
            f"Archivo no encontrado en {trabajo.target_dir} "
            f"con nombre {trabajo.output_filename}.*"
        )
        return resultado

    archivo = candidatos[0]
    resultado["archivo"] = str(archivo)
    resultado["tamanio_bytes"] = archivo.stat().st_size

    duracion = obtener_duracion_segundos(archivo)
    resultado["duracion_s"] = duracion
    if duracion is not None:
        diferencia = abs(duracion - duracion_esperada_s)
        resultado["duracion_ok"] = diferencia < 0.12  # ~3 fotogramas a 25 fps
    else:
        resultado["errores"].append("No se pudo leer la duración con ffprobe")

    resultado["hash_sha256"] = calcular_sha256(archivo)

    smoke = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(archivo),
         "-frames:v", "1", "-f", "null", "-"],
        capture_output=True,
    )
    resultado["smoke_test_ok"] = smoke.returncode == 0
    if not resultado["smoke_test_ok"]:
        resultado["errores"].append(
            f"Smoke test fallido: {smoke.stderr.decode(errors='replace')[:200]}"
        )

    return resultado
