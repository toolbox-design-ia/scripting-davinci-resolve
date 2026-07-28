"""Primer contacto con la API de Resolve: comprobar que responde.

En la consola integrada el objeto `resolve` YA existe: no hay que crearlo.
Fuera de ella se obtiene con bmd.scriptapp("Resolve"). Si encuentras por ahi
recetas con app.GetResolveInstance(), son de documentacion antigua y hoy
fallan con TypeError: 'NoneType' object is not callable.
"""


def get_resolve():
    """Devuelve el objeto resolve tanto dentro como fuera de la consola."""
    try:
        return resolve  # noqa: F821 — definido por la consola integrada
    except NameError:
        pass
    try:
        import DaVinciResolveScript as bmd
        return bmd.scriptapp("Resolve")
    except ImportError:
        return None


def main():
    app = get_resolve()
    if app is None:
        print("No hay conexion con Resolve.")
        print("- Dentro de Resolve: Workspace > Console, pestana Py3.")
        print("- Desde fuera: activa Preferences > System > General >")
        print("  External scripting using = Local, y revisa el Anexo B.")
        return 1

    project_manager = app.GetProjectManager()
    project = project_manager.GetCurrentProject()
    print("Conexion establecida.")
    print("  Version de producto :", app.GetVersionString())
    print("  Pagina actual       :", app.GetCurrentPage())
    if project is None:
        print("  Proyecto            : (ninguno abierto)")
        return 0
    print("  Proyecto            :", project.GetName())
    print("  Timelines           :", project.GetTimelineCount())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
