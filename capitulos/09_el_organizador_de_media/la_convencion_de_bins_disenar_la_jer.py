from collections import defaultdict

def construir_mapa_bins(clips: list[InfoClip]) -> dict:
    estructura: dict[str, dict[str, list[InfoClip]]] = defaultdict(
        lambda: defaultdict(list)
    )
    for clip in clips:
        if not clip.valido:
            estructura["REVISION_MANUAL"][""].append(clip)
            continue
        camara = clip.camara
        if camara in ("A", "B", "C"):
            estructura[clip.escena][f"CAM_{camara}"].append(clip)
        elif camara in ("BROLL", "GFX", "AUDIO"):
            estructura[camara][""].append(clip)
        else:
            clip.motivo_rechazo = f"Cámara desconocida: '{camara}'"
            estructura["REVISION_MANUAL"][""].append(clip)
    return estructura
