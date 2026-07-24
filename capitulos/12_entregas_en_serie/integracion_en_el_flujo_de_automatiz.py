def entregar_proyecto(
    resolve_handle,
    ruta_catalogo: str,
    ruta_destinos: str,
    ruta_validacion_previa: str,
    ruta_reporte_salida: str,
) -> bool:
    # 0. Verificar validación previa
    with open(ruta_validacion_previa) as f:
        validacion = json.load(f)
    if validacion.get("errores_criticos", 1) > 0:
        print("[ABORT] Validación previa con errores críticos. Entrega cancelada.")
        return False

    # 1. Obtener proyecto y timeline activos
    pm = resolve_handle.GetProjectManager()
    project = pm.GetCurrentProject()
    timeline = project.GetCurrentTimeline()
    fps = float(timeline.GetSetting("timelineFrameRate"))
    duracion_esperada_s = (timeline.GetEndFrame() - timeline.GetStartFrame()) / fps

    # 2. Cargar catálogo y destinos
    catalogo = cargar_catalogo(ruta_catalogo)
    with open(ruta_destinos) as f:
        destinos = json.load(f)

    # 3. Encolar todos los trabajos
    trabajos = encolar_todos(project, catalogo, destinos)
    if not trabajos:
        print("[ABORT] Sin trabajos encolados.")
        return False

    # 4. Render y monitoreo del primer pase
    uuids = [t.uuid_resolve for t in trabajos]
    project.StartRendering(uuids)
    bucle_monitoreo(project, trabajos)

    # 5. Reintentos para fallidos
    fallidos = [t for t in trabajos if t.estado == EstadoTrabajo.FALLIDO]
    if fallidos:
        reintentados = gestionar_reintentos(project, fallidos, catalogo, destinos)
        if reintentados:
            uuids_retry = [t.uuid_resolve for t in reintentados]
            project.StartRendering(uuids_retry)
            bucle_monitoreo(project, reintentados)

    # 6. Validar todos los completados
    completados = [t for t in trabajos if t.estado == EstadoTrabajo.COMPLETADO]
    resultados = [validar_entrega(t, duracion_esperada_s) for t in completados]

    # 7. Reporte unificado
    escribir_reporte(trabajos, resultados, Path(ruta_reporte_salida))

    errores_totales = sum(len(r["errores"]) for r in resultados)
    return errores_totales == 0
