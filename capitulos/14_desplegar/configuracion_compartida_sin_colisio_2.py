MIGRACIONES_CONFIG = {
    "1.3.0": {
        "timeout_conexion": 30,
        "directorio_cache": "/tmp/resolve_tools_cache",
    },
    "1.4.0": {
        "modo_verbose": False,
        "servidor_logs": "",
    }
}

def migrar_config(config_sala: dict, version_anterior: str, version_nueva: str) -> dict:
    for version, nuevas_claves in sorted(MIGRACIONES_CONFIG.items()):
        if version_anterior < version <= version_nueva:
            for clave, valor_defecto in nuevas_claves.items():
                config_sala.setdefault(clave, valor_defecto)
    return config_sala
