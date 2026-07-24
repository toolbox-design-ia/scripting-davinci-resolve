def escribir_reporte(
    trabajos: list[TrabajoDEntrega],
    resultados_validacion: list[dict],
    ruta_salida: Path,
    version_script: str = "1.0.0",
) -> None:
    import datetime

    reporte = {
        "version_script": version_script,
        "timestamp": datetime.datetime.now().isoformat(),
        "resumen": {
            "total": len(trabajos),
            "completados": sum(1 for t in trabajos if t.estado == EstadoTrabajo.COMPLETADO),
            "fallidos": sum(1 for t in trabajos if t.estado == EstadoTrabajo.FALLIDO),
        },
        "trabajos": [
            {
                "preset_id": t.preset_id,
                "estado": t.estado.value,
                "intentos": t.intentos,
                "duracion_render_s": round(t.fin - t.inicio, 2) if t.fin > 0 else None,
                "error": t.error or None,
            }
            for t in trabajos
        ],
        "validaciones": resultados_validacion,
    }

    with open(ruta_salida, "w", encoding="utf-8") as f:
        json.dump(reporte, f, indent=2, ensure_ascii=False)

    print(f"[INFO] Reporte escrito en {ruta_salida}")
