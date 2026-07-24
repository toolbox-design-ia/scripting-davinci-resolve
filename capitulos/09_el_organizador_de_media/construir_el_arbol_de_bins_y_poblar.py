def poblar_media_pool(media_pool, estructura: dict, log: list[str]) -> None:
    root = media_pool.GetRootFolder()

    for bin_nivel1, subniveles in estructura.items():
        carpeta_nivel1 = obtener_o_crear_bin(media_pool, root, bin_nivel1)

        for bin_nivel2, clips in subniveles.items():
            carpeta_destino = (
                obtener_o_crear_bin(media_pool, carpeta_nivel1, bin_nivel2)
                if bin_nivel2
                else carpeta_nivel1
            )

            rutas = [str(clip.ruta) for clip in clips]
            media_pool.SetCurrentFolder(carpeta_destino)
            importados = media_pool.ImportMedia(rutas)

            if importados is None:
                log.append(
                    f"ERROR: ImportMedia falló para '{bin_nivel1}/{bin_nivel2}'"
                )
                continue

            for item, info in zip(importados, clips):
                if item is None:
                    log.append(f"AVISO: no se pudo importar '{info.ruta.name}'")
                    continue
                nombre_legible = info.ruta.stem.replace("_", " ")
                item.SetClipProperty("Clip Name", nombre_legible)
                destino = f"{bin_nivel1}/{bin_nivel2 or '(raíz)'}"
                log.append(f"OK: '{info.ruta.name}' -> {destino}")
