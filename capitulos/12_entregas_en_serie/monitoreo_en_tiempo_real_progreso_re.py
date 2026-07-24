import subprocess
import platform

def obtener_pid_resolve() -> str:
    if platform.system() == "Darwin":
        result = subprocess.run(
            ["pgrep", "-x", "DaVinci Resolve"], capture_output=True, text=True
        )
        return result.stdout.strip()
    return ""

def muestrear_cpu_resolve() -> float:
    pid = obtener_pid_resolve()
    if not pid:
        return -1.0
    result = subprocess.run(
        ["ps", "-o", "pcpu=", "-p", pid], capture_output=True, text=True
    )
    try:
        return float(result.stdout.strip())
    except ValueError:
        return -1.0

def bucle_monitoreo(
    project, trabajos: list[TrabajoDEntrega], intervalo: int = 10
) -> None:
    activos = {
        t.uuid_resolve: t
        for t in trabajos
        if t.estado == EstadoTrabajo.EN_COLA
    }

    while activos:
        for uuid, trabajo in list(activos.items()):
            status = project.GetRenderJobStatus(uuid)
            job_status = status.get("JobStatus", "None")
            pct = status.get("CompletionPercentage", 0)

            if job_status == "Rendering":
                trabajo.estado = EstadoTrabajo.RENDERIZANDO
                if trabajo.inicio == 0.0:
                    trabajo.inicio = time.time()

                if pct > 1:
                    elapsed = time.time() - trabajo.inicio
                    eta_s = (elapsed / pct) * (100 - pct)
                    cpu = muestrear_cpu_resolve()
                    print(
                        f"[{trabajo.preset_id}] {pct:.1f}% "
                        f"– ETA: {eta_s:.0f}s – CPU: {cpu:.1f}%"
                    )
                    if cpu < 5.0 and pct < 99.0:
                        print(
                            f"[WARN] CPU muy baja durante render activo "
                            f"en {trabajo.preset_id} – posible bloqueo de E/S"
                        )

            elif job_status == "Complete":
                trabajo.estado = EstadoTrabajo.COMPLETADO
                trabajo.fin = time.time()
                duracion = trabajo.fin - trabajo.inicio
                print(f"[OK] {trabajo.preset_id} completado en {duracion:.1f}s")
                del activos[uuid]

            elif job_status == "Failed":
                trabajo.estado = EstadoTrabajo.FALLIDO
                trabajo.error = "Resolve reportó JobStatus=Failed"
                trabajo.fin = time.time()
                print(f"[ERROR] {trabajo.preset_id} falló en Resolve")
                del activos[uuid]

        if activos:
            time.sleep(intervalo)
