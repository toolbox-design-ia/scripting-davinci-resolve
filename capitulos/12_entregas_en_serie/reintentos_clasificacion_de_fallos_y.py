def gestionar_reintentos(
    project,
    trabajos_fallidos: list[TrabajoDEntrega],
    catalogo: list[dict],
    destinos: dict,
) -> list[TrabajoDEntrega]:
    reintentados = []
    for trabajo in trabajos_fallidos:
        if trabajo.intentos >= trabajo.max_intentos:
            print(f"[FATAL] {trabajo.preset_id}: máximo de reintentos alcanzado")
            continue

        espera = 30 * (2 ** trabajo.intentos)  # 30s → 60s → 120s
        print(
            f"[RETRY] {trabajo.preset_id}: reintentando en {espera}s "
            f"(intento {trabajo.intentos + 1}/{trabajo.max_intentos})"
        )
        time.sleep(espera)

        preset_def = next(p for p in catalogo if p["id"] == trabajo.preset_id)
        ok = aplicar_preset_a_resolve(project, preset_def, trabajo.target_dir)
        if ok:
            project.SetRenderSettings({"CustomName": trabajo.output_filename})
            nuevo_uuid = project.AddRenderJob()
            if nuevo_uuid:
                trabajo.uuid_resolve = nuevo_uuid
                trabajo.estado = EstadoTrabajo.EN_COLA
                trabajo.intentos += 1
                reintentados.append(trabajo)

    return reintentados
