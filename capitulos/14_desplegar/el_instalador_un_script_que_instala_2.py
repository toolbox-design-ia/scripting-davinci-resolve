PERFILES = {
    "color":      ["lut_validator", "entrega_automatica", "shot_comparer"],
    "edicion":    ["media_organizer", "timeline_report", "metadata_checker"],
    "supervisor": ["metadata_reader", "report_generator"],
}

def instalar_perfil(perfil: str, origen: Path, destino_base: Path, **kwargs):
    modulos = PERFILES.get(perfil)
    if not modulos:
        raise ValueError(f"Perfil desconocido: {perfil}")
    for modulo in modulos:
        instalar(origen / modulo, destino_base / modulo, **kwargs)
